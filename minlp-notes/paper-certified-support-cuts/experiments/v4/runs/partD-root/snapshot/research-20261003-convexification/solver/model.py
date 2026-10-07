"""Build identical native models and bind cuts to their exact source expressions.

The checked boundary is the submitted PySCIPOpt expression DAG, not SCIP's
floating point presolve or solve. Extra variables, when needed, preserve only
partial-function domains by exact existential witnesses; graph atoms are not
reformulated. See ``numerics/model-contract.md``.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math
from pathlib import Path
import sys

import pyscipopt as ps
from pyscipopt.scip import Constant, PowExpr, ProdExpr, SumExpr, VarExpr
import sympy as sp

from .bounds import propagate_bounds, replay_bounds
from .model_binding import (native_expression, normalize_constant_trees,
                            same_expression)

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "code" / "univariate_envelopes"))
from uenv.osil import Instance, read_osil, _scip_expr

Q = Fraction
INF = math.inf
_UNARY = {"log": sp.log, "exp": sp.exp, "sqrt": sp.sqrt,
          "sin": sp.sin, "cos": sp.cos, "abs": sp.Abs}


class ModelAdmissionError(ValueError):
    def __init__(self, status, diagnostic):
        super().__init__(diagnostic)
        self.status = status
        self.diagnostic = diagnostic


@dataclass
class BuiltModel:
    model: object
    xs: list
    objective_var: object | None
    source_symbols: tuple
    source_rows: tuple
    bounds: tuple
    exact_bounds: tuple
    metadata: dict


def _q(value):
    value = float(value)
    if not math.isfinite(value):
        raise ModelAdmissionError("unsupported_model", "nonfinite source constant")
    return Q(value)


def expression(tree, symbols):
    """Source values, with positive-base variable powers in exp/log form.

    ``source_domains`` must establish the positivity premise before these
    expressions can be used. This is a local identity, not forced symbolic
    simplification of arbitrary powers.
    """
    op = tree[0]
    if op == "num":
        return sp.Rational(_q(tree[1]))
    if op == "var":
        return symbols[tree[1]]
    args = [expression(c, symbols) for c in tree[1:]]
    if op == "sum": return sp.Add(*args)
    if op == "times": return sp.Mul(*args)
    if op == "negate": return -args[0]
    if op == "divide": return args[0] / args[1]
    if op == "square": return args[0] ** 2
    if op == "power":
        return (sp.exp(args[1] * sp.log(args[0])) if args[1].free_symbols
                else args[0] ** args[1])
    if op in _UNARY: return _UNARY[op](args[0])
    raise ModelAdmissionError("unsupported_operator", f"source operator {op!r}")


def _product(a, b):
    # Extended interval multiplication: zero times an unbounded interval is
    # exactly zero, not a NaN. All finite arithmetic remains rational.
    values = [Q(0) if u == 0 or v == 0 else u*v for u in a for v in b]
    return min(values), max(values)


def _power(a, k):
    if abs(k) > 1024: return -INF, INF
    lo, hi = a
    if k == 0: return Q(1), Q(1)
    if k < 0:
        if lo <= 0 <= hi: return -INF, INF
        p = _power(a, -k)
        return Q(0) if p[1] == INF else 1/p[1], Q(0) if p[0] == -INF else 1/p[0]
    if k % 2: return lo**k, hi**k
    return (Q(0) if lo <= 0 <= hi else min(lo**k, hi**k), max(lo**k, hi**k))


def _affine_range(expr, symbols, inst, current):
    """Tighten an affine argument using proportional original affine rows."""
    indices = [i for i, s in enumerate(symbols) if s in expr.free_symbols]
    if not indices:
        return (Q(expr), Q(expr)) if expr.is_Rational else current
    used_symbols = [symbols[i] for i in indices]
    try:
        poly = sp.Poly(expr, *used_symbols)
    except sp.PolynomialError:
        return current
    if poly.total_degree() > 1: return current
    c = poly.coeff_monomial(1)
    raw = {i: poly.coeff_monomial(symbols[i]) for i in indices
           if poly.coeff_monomial(symbols[i]) != 0}
    if not c.is_Rational or any(not v.is_Rational for v in raw.values()): return current
    coeff = {i: Q(v) for i, v in raw.items()}
    if not coeff: return Q(c), Q(c)
    lo, hi = current
    for row in inst.rows[1:]:
        if row["nl"] is not None or row["quad"]: continue
        rc = {i: _q(v) for i, v in row["lin"].items() if v != 0}
        if rc.keys() != coeff.keys(): continue
        first = next(iter(coeff))
        ratio = coeff[first] / rc[first]
        if any(coeff[i] != ratio*rc[i] for i in coeff): continue
        lower, upper = row["lb"], row["ub"]
        lower = _q(lower) if math.isfinite(lower) else -INF
        upper = _q(upper) if math.isfinite(upper) else INF
        a, b = ((ratio*lower+Q(c), ratio*upper+Q(c)) if ratio > 0
                else (ratio*upper+Q(c), ratio*lower+Q(c)))
        lo, hi = max(lo, a), min(hi, b)
    return lo, hi


def source_domains(tree, bounds, symbols, inst, *, row_index=0):
    """Visit every source node before simplification; prove or retain domains.

    Returned guards are exact projection constraints. A variable exponent is
    admitted only if its base is independently proved strictly positive.
    """
    requirements = []
    artificial = sp.Symbol("_argument", real=True)

    def elementary(op, interval, exponent=None):
        lo, hi = interval
        if op == "abs":
            return (Q(0) if lo <= 0 <= hi else min(abs(lo), abs(hi)), max(abs(lo), abs(hi)))
        if op in ("sin", "cos"): return Q(-1), Q(1)
        if not math.isfinite(lo) or not math.isfinite(hi):
            if op == "exp": return Q(0), INF
            if op == "sqrt": return Q(0), INF
            return -INF, INF
        from .certified import elementary_interval
        expr = artificial**sp.Rational(exponent) if op == "power" else _UNARY[op](artificial)
        try:
            return elementary_interval(expr, artificial, interval)
        except (ValueError, ArithmeticError, ImportError):
            return -INF, INF

    def require(kind, argument, interval, path, allow_guard=True):
        interval = _affine_range(expression(argument, symbols), symbols, inst, interval)
        lo, hi = interval
        proved = ((lo > 0) if kind == "positive" else (lo >= 0) if kind == "nonnegative"
                  else (hi < 0 or lo > 0))
        if not proved and not allow_guard:
            raise ModelAdmissionError("unsupported_variable_power_domain", f"row {row_index}: a variable power requires a proved positive base")
        if lo > hi or (kind == "positive" and hi <= 0) or (kind == "nonnegative" and hi < 0) or (kind == "nonzero" and lo == hi == 0):
            raise ModelAdmissionError("source_domain_infeasible", f"row {row_index} has an empty {kind} source domain at {path}")
        requirements.append({"kind": kind, "argument": argument, "row": row_index,
                             "path": path, "proved": proved,
                             "interval": [str(lo), str(hi)]})
        return interval

    def visit(node, path=()):
        op = node[0]
        if op == "num":
            q = _q(node[1]); return q, q
        if op == "var": return bounds[node[1]]
        args = [visit(c, (*path, i)) for i, c in enumerate(node[1:])]
        if op == "sum": return sum((a for a, _ in args), Q(0)), sum((b for _, b in args), Q(0))
        if op == "times":
            value = (Q(1), Q(1))
            for a in args: value = _product(value, a)
            return value
        if op == "negate": return -args[0][1], -args[0][0]
        if op == "divide":
            den = require("nonzero", node[2], args[1], path)
            if den[0] <= 0 <= den[1]: return -INF, INF
            inv = (Q(0) if math.isinf(den[1]) else 1/den[1], Q(0) if math.isinf(den[0]) else 1/den[0])
            return _product(args[0], inv)
        if op == "square": return _power(args[0], 2)
        if op in ("log", "sqrt"):
            arg = require("positive" if op == "log" else "nonnegative", node[1], args[0], path)
            if (op == "log" and arg[0] <= 0) or arg[0] < 0: return -INF, INF
            return elementary(op, arg)
        if op == "power":
            exp = expression(node[2], symbols)
            if exp.free_symbols:
                require("positive", node[1], args[0], path, allow_guard=False)
                return Q(0), INF
            if not exp.is_Rational:
                raise ModelAdmissionError("unsupported_power_exponent", "a fixed power exponent must be rational")
            exponent = Q(exp)
            base = args[0]
            if exponent.denominator != 1:
                base = require("positive" if exponent < 0 else "nonnegative", node[1], base, path)
            elif exponent < 0:
                base = require("nonzero", node[1], base, path)
            if exponent.denominator == 1: return _power(base, exponent.numerator)
            if base[0] < 0 or (exponent < 0 and base[0] <= 0): return -INF, INF
            return elementary("power", base, exponent)
        if op in _UNARY: return elementary(op, args[0])
        raise ModelAdmissionError("unsupported_operator", f"source operator {op!r}")

    if tree is not None: visit(tree)
    return requirements


def _sum(children):
    out = SumExpr(); out.children = list(children); out.coefs = [1.0]*len(out.children)
    return out


def _prod(children):
    out = ProdExpr(); out.children = list(children)
    return out


def _pow(base, exponent):
    out = PowExpr(); out.children = [base]; out.expo = float(exponent)
    return out


def generic_expression(tree, xs, symbols):
    """Build a generic DAG without folding products of stored coefficients."""
    op = tree[0]
    if op == "num": return Constant(float(tree[1]))
    if op == "var": return VarExpr(xs[tree[1]])
    args = [generic_expression(c, xs, symbols) for c in tree[1:]]
    if op == "sum": return _sum(args)
    if op == "times": return _prod(args)
    if op == "negate": return _prod([Constant(-1.0), args[0]])
    if op == "divide": return _prod([args[0], _pow(args[1], -1)])
    if op == "square": return _pow(args[0], 2)
    if op == "power":
        exponent = expression(tree[2], symbols)
        if exponent.free_symbols:
            return ps.exp(_prod([args[1], ps.log(args[0])]))
        if not exponent.is_Rational or sp.Rational(float(exponent)) != exponent:
            # A scalar exponent that is not binary64 representable cannot be
            # stored in a PowExpr. Positive bases can use exp(e*log(base)),
            # but that broader grammar is deliberately not implicit here.
            raise ModelAdmissionError("unsupported_power_exponent", "fixed exponent is not exactly binary64 representable")
        return _pow(args[0], float(exponent))
    if op == "abs": return abs(args[0])
    if op in _UNARY:
        return {"log": ps.log, "exp": ps.exp, "sqrt": ps.sqrt,
                "sin": ps.sin, "cos": ps.cos}[op](args[0])
    raise ModelAdmissionError("unsupported_operator", f"source operator {op!r}")


def _row_tree(row, objective_constant=0.0):
    parts = [("times", ("num", float(c)), ("var", i)) for i, c in row["lin"].items()]
    parts += [("times", ("num", float(c)), ("var", i), ("var", j)) for i, j, c in row["quad"]]
    if row["nl"] is not None: parts.append(row["nl"])
    if objective_constant: parts.append(("num", float(objective_constant)))
    return ("sum", *parts) if parts else ("num", 0.0)


def _check_bounds(inst, infinity):
    n = len(inst.var_lb)
    if not n == len(inst.var_ub) == len(inst.var_type):
        raise ModelAdmissionError("unsupported_model", "inconsistent variable arrays")
    if any(t not in ("C", "I", "B") for t in inst.var_type):
        raise ModelAdmissionError("unsupported_model", "unsupported variable type")
    if inst.obj_sense not in ("min", "max"):
        raise ModelAdmissionError("unsupported_model", "unknown objective sense")
    pairs = [*zip(inst.var_lb, inst.var_ub), *((r["lb"], r["ub"]) for r in inst.rows[1:])]
    for lo, hi in pairs:
        if math.isnan(lo) or math.isnan(hi) or lo == INF or hi == -INF or lo > hi:
            raise ModelAdmissionError("unsupported_model", "invalid variable or row bounds")
        if any(math.isfinite(v) and abs(v) >= infinity for v in (lo, hi)):
            raise ModelAdmissionError("unsupported_model", "finite source bound reaches SCIP infinity sentinel")


def build_model(inst: Instance) -> BuiltModel:
    """Return a common native model; raise a structured admission error."""
    model = ps.Model(inst.name)
    try:
        _check_bounds(inst, model.infinity())
        symbols = tuple(sp.Symbol(f"x{i}", real=True) for i in range(len(inst.var_lb)))
        propagation = propagate_bounds(inst)
        if not replay_bounds(inst, propagation.certificate):
            raise ModelAdmissionError("invalid_bound_certificate", "internal affine-bound replay failed")
        if propagation.infeasible:
            raise ModelAdmissionError("affine_infeasible", "original affine rows and bounds have a rational contradiction")
        exact_bounds = tuple(zip(propagation.lower, propagation.upper))
        bounds = tuple(zip(propagation.float_lower, propagation.float_upper))
        # The solver retains declared bounds. Deductions only supply validated
        # support domains and source-domain proofs; all original rows remain.
        xs = [model.addVar(name=f"v{i}", lb=None if math.isinf(lo) else lo,
                          ub=None if math.isinf(hi) else hi, vtype=kind)
              for i, (lo, hi, kind) in enumerate(zip(inst.var_lb, inst.var_ub, inst.var_type))]
        native_symbols = {v.name: s for v, s in zip(xs, symbols)}
        source_rows, native_rows, requirements, fallback_rows = [], [], [], []
        for ri, row in enumerate(inst.rows):
            requirements.extend(source_domains(row["nl"], exact_bounds, symbols, inst, row_index=ri))
            tree = _row_tree(row, inst.obj_const if ri == 0 else 0.0)
            source = expression(tree, symbols)
            try:
                native = _scip_expr(normalize_constant_trees(tree), xs, {})
                equal = same_expression(source, native_expression(native, native_symbols))
            except (ValueError, NotImplementedError, TypeError, OverflowError, ZeroDivisionError):
                equal = False
            if not equal:
                native = generic_expression(tree, xs, symbols)
                fallback_rows.append(ri)
            elif ri and any(len(term) == 0 and c != 0 for term, c in getattr(native, "terms", {}).items()):
                # ExprCons subtracts polynomial constants from row sides in
                # binary64. Keep these constants as generic DAG children, so
                # an exact source side never becomes a rounded different side.
                native = generic_expression(tree, xs, symbols)
                fallback_rows.append(ri)
            if not same_expression(source, native_expression(native, native_symbols)):
                raise ModelAdmissionError("source_model_mismatch", f"row {ri} differs after native expression assembly")
            source_rows.append(source); native_rows.append(native)

        # Domain proofs above are accepted only after every original row,
        # including every affine row used for propagation, passes binding.
        guards, guard_keys = [], set()
        for requirement in requirements:
            if requirement["proved"]: continue
            arg = expression(requirement["argument"], symbols)
            key = (requirement["kind"], sp.srepr(arg))
            if key in guard_keys: continue
            guard_keys.add(key)
            native = generic_expression(requirement["argument"], xs, symbols)
            if not same_expression(arg, native_expression(native, native_symbols)):
                raise ModelAdmissionError("source_model_mismatch", "domain guard differs from its source argument")
            gi = len(guards)
            if requirement["kind"] == "nonnegative":
                guard_constraint = native >= 0
                witness_name = None
                witness_bounds = None
                guard_symbols = native_symbols
            else:
                u = model.addVar(name=f"source_domain_witness_{gi}",
                                 lb=0.0 if requirement["kind"] == "positive" else None, ub=None)
                guard_constraint = _prod([native, VarExpr(u)]) == 1
                witness_name = u.name
                witness_bounds = [float(u.getLbOriginal()), float(u.getUbOriginal())]
                guard_symbols = {**native_symbols, u.name: sp.Symbol(u.name, real=True)}
            submitted_expression = native_expression(guard_constraint.expr, guard_symbols)
            expected_expression = (arg if witness_name is None else
                                   arg * guard_symbols[witness_name])
            if not same_expression(expected_expression, submitted_expression):
                raise ModelAdmissionError("source_model_mismatch", "domain witness equation differs from exact source projection")
            submitted = model.addCons(guard_constraint, name=f"source_domain_{gi}")
            guards.append({"kind": requirement["kind"], "row": requirement["row"],
                           "path": requirement["path"], "witness": witness_name,
                           "argument": sp.srepr(arg), "constraint": submitted.name,
                           "submitted_expression": sp.srepr(submitted_expression),
                           "submitted_lhs": guard_constraint._lhs,
                           "submitted_rhs": guard_constraint._rhs,
                           "stored_lhs": float(model.getLhs(submitted)),
                           "stored_rhs": float(model.getRhs(submitted)),
                           "witness_bounds": witness_bounds,
                           "scip_infinity": float(model.infinity())})

        objective_var = None
        for ri, (row, native) in enumerate(zip(inst.rows, native_rows)):
            if ri == 0:
                sense = "minimize" if inst.obj_sense == "min" else "maximize"
                # Generic expressions cannot be used directly as an objective.
                if row["quad"] or row["nl"] is not None or ri in fallback_rows:
                    objective_var = model.addVar(name="objective_epigraph", lb=None, ub=None)
                    model.addCons(native <= objective_var if inst.obj_sense == "min" else native >= objective_var,
                                  name="objective_definition")
                    model.setObjective(objective_var, sense)
                else:
                    model.setObjective(native, sense)
            else:
                lhs = row["lb"] if math.isfinite(row["lb"]) else None
                rhs = row["ub"] if math.isfinite(row["ub"]) else None
                if lhs is not None or rhs is not None:
                    if isinstance(native, (int, float)):
                        native = Constant(native)
                    model.addCons(ps.ExprCons(native, lhs=lhs, rhs=rhs), name=f"source_row_{ri}")
        metadata = {"schema": "source-model-v2", "binding_boundary": "submitted PySCIPOpt expression DAG",
                    "bound_certificate": propagation.certificate, "bound_status": propagation.status,
                    "domain_requirements": len(requirements), "proved_domain_requirements": sum(r["proved"] for r in requirements),
                    "domain_guards": guards, "generic_fallback_rows": fallback_rows,
                    "source_variables": [v.name for v in xs],
                    "objective_variable": None if objective_var is None else objective_var.name,
                    "domain_preservation": "exact real projection; no epsilon substitutes strict domains"}
        return BuiltModel(model, xs, objective_var, symbols, tuple(source_rows), bounds, exact_bounds, metadata)
    except ModelAdmissionError:
        model.freeProb()
        raise
    except RecursionError as error:
        model.freeProb()
        raise ModelAdmissionError("unsupported_expression_depth", "expression exceeds the supported recursive construction depth") from error
    except (ValueError, TypeError, IndexError, KeyError, OverflowError, ZeroDivisionError, NotImplementedError) as error:
        model.freeProb()
        raise ModelAdmissionError("unsupported_model", str(error)) from error
