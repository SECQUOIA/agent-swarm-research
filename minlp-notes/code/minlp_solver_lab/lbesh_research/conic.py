"""Independent exact quadratic GDP hull baseline, solved as a convex MIQCP.

No epsilon perspective and no LBESH extraction/cut code are used.  ``solve``
leaves the input model unchanged and returns original-name primal values.
Unsupported expressions raise ``UnsupportedConic`` instead of silently
relaxing them. See notes/lbesh-development-conic.md for domain and proof.
"""
from __future__ import annotations

from fractions import Fraction
import math
import time

import gurobipy as gp
from gurobipy import GRB
import pyomo.environ as pe
from pyomo.gdp import Disjunct, Disjunction
from pyomo.core.expr.visitor import identify_variables
from pyomo.repn import generate_standard_repn
from pyomo.contrib.fbbt.fbbt import compute_bounds_on_expr


class UnsupportedConic(ValueError):
    """The supplied model is outside this baseline's verified scope."""


def _finite(value):
    return value is not None and math.isfinite(float(pe.value(value)))


def _repn(expr):
    return generate_standard_repn(expr, compute_values=True, quadratic=True)


def _square_parts(expr, weight=1.):
    """Keep explicit affine squares intact before polynomial expansion.

    Return an affine Pyomo expression and weighted affine-square components.
    This prevents expansion roundoff turning a rank-deficient PSD quadratic
    into an indefinite matrix. Unrecognized polynomial forms use a separate
    exact-PSD check of their expanded coefficients.
    """
    if _repn(expr).is_linear():
        return weight * expr, []
    kind, args = type(expr).__name__, expr.args
    if kind in ("SumExpression", "LinearExpression"):
        parts = [_square_parts(arg, weight) for arg in args]
        return sum(part[0] for part in parts), [square for part in parts for square in part[1]]
    if kind in ("ProductExpression", "MonomialTermExpression"):
        for i in (0, 1):
            if pe.is_fixed(args[i]):
                return _square_parts(args[1-i], weight * float(pe.value(args[i])))
    if kind == "DivisionExpression" and pe.is_fixed(args[1]):
        return _square_parts(args[0], weight / float(pe.value(args[1])))
    if kind == "NegationExpression":
        return _square_parts(args[0], -weight)
    if kind == "PowExpression" and pe.is_fixed(args[1]) and pe.value(args[1]) == 2:
        if weight >= 0 and _repn(args[0]).is_linear():
            return 0., [(weight, args[0])]
    raise UnsupportedConic("quadratic is not an explicit nonnegative sum of affine squares")


def _require_psd(repn, name):
    """Exact rational Schur complements certify the entered float matrix.

    Retain original quadratic coefficients in Gurobi; never clip eigenvalues.
    Fraction(float) represents the actual binary floating point coefficient.
    Zero pivots in a PSD matrix must have a zero remaining row/column.
    """
    variables = {id(v): v for pair in repn.quadratic_vars for v in pair}
    index = {key: j for j, key in enumerate(variables)}
    n = len(index)
    matrix = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for (v, w), c in zip(repn.quadratic_vars, repn.quadratic_coefs):
        i, j = index[id(v)], index[id(w)]
        value = Fraction(float(c))
        if i == j:
            matrix[i][j] += value
        else:
            matrix[i][j] += value / 2
            matrix[j][i] += value / 2
    for k in range(n):
        pivot = matrix[k][k]
        if pivot < 0 or (pivot == 0 and any(matrix[k][j] for j in range(k + 1, n))):
            raise UnsupportedConic(f"non-PSD quadratic in {name}")
        if pivot:
            for i in range(k + 1, n):
                for j in range(i, n):
                    matrix[i][j] -= matrix[i][k] * matrix[k][j] / pivot
                    matrix[j][i] = matrix[i][j]


class _Builder:
    def __init__(self, source, relax_integrality, output_flag):
        self.model = source.clone()
        self.original_booleans = list(self.model.component_data_objects(
            pe.BooleanVar, descend_into=(pe.Block, Disjunct)))
        self.env = gp.Env(empty=True)
        self.env.setParam("OutputFlag", int(output_flag))
        self.env.start()
        self.g = gp.Model("exact_quadratic_gdp_hull", env=self.env)
        self.g.Params.NonConvex = 0
        self.variables = {}
        self.pyvariables = {}
        self.relax_integrality = relax_integrality
        self.count = 0

    def close(self):
        self.g.dispose()
        self.env.dispose()

    def auxiliary(self, prefix, lb=0.0, ub=GRB.INFINITY):
        self.count += 1
        return self.g.addVar(lb=lb, ub=ub, name=f"_{prefix}_{self.count}")

    def linear(self, repn, mapping, scale=1):
        return gp.LinExpr(float(repn.constant) * scale) + gp.quicksum(
            float(c) * mapping[id(v)] for v, c in zip(repn.linear_vars, repn.linear_coefs)
        )

    def quadratic(self, repn, mapping):
        return gp.QuadExpr(gp.quicksum(
            float(c) * mapping[id(v)] * mapping[id(w)]
            for (v, w), c in zip(repn.quadratic_vars, repn.quadratic_coefs)
        ))

    def quadratic_parts(self, expr, mapping, name, indicator=None):
        try:
            affine_expr, squares = _square_parts(expr)
        except UnsupportedConic:
            repn = _repn(expr)
            _require_psd(repn, name)
            affine = gp.quicksum(float(c) * mapping[id(v)]
                                for v, c in zip(repn.linear_vars, repn.linear_coefs))
            affine += float(repn.constant) * (1 if indicator is None else indicator)
            return affine, self.quadratic(repn, mapping), bool(repn.quadratic_vars)
        affine_repn = _repn(affine_expr)
        affine = gp.quicksum(float(c) * mapping[id(v)]
                            for v, c in zip(affine_repn.linear_vars, affine_repn.linear_coefs))
        affine += float(affine_repn.constant) * (1 if indicator is None else indicator)
        quadratic = gp.QuadExpr()
        for weight, component_expr in squares:
            if not weight:
                continue
            repn = _repn(component_expr)
            component = gp.quicksum(float(c) * mapping[id(v)]
                                   for v, c in zip(repn.linear_vars, repn.linear_coefs))
            component += float(repn.constant) * (1 if indicator is None else indicator)
            lifted = self.auxiliary("square_component", lb=-GRB.INFINITY)
            self.g.addConstr(lifted == component)
            quadratic += weight * lifted * lifted
        return affine, quadratic, bool(squares)

    def affine(self, expr, mapping):
        repn = _repn(expr)
        if not repn.is_linear():
            raise UnsupportedConic("norm component is not affine")
        return self.linear(repn, mapping)

    def norm_squares(self, expr, mapping):
        """Parse an explicit sum of nonnegative weighted affine squares."""
        if pe.is_fixed(expr):
            value = float(pe.value(expr))
            if value < 0:
                raise UnsupportedConic("negative constant in norm radicand")
            return [(value, gp.LinExpr(1))] if value else []
        kind = type(expr).__name__
        args = expr.args
        if kind in ("SumExpression", "LinearExpression"):
            return [term for arg in args for term in self.norm_squares(arg, mapping)]
        if kind in ("ProductExpression", "MonomialTermExpression"):
            for i in (0, 1):
                if pe.is_fixed(args[i]):
                    c = float(pe.value(args[i]))
                    if c < 0:
                        raise UnsupportedConic("negative multiplier in norm radicand")
                    return [(c * a, b) for a, b in self.norm_squares(args[1-i], mapping)]
        if kind == "PowExpression" and pe.is_fixed(args[1]) and pe.value(args[1]) == 2:
            return [(1., self.affine(args[0], mapping))]
        raise UnsupportedConic(f"unsupported norm radicand: {expr}")

    def convex(self, expr, mapping, name):
        """A convex expression's exact monotone epigraph representation."""
        repn = _repn(expr)
        if repn.is_quadratic() or repn.is_linear():
            affine, quadratic, _ = self.quadratic_parts(expr, mapping, name)
            return affine + quadratic
        kind = type(expr).__name__
        args = expr.args
        if kind in ("SumExpression", "LinearExpression"):
            return gp.quicksum(self.convex(arg, mapping, name) for arg in args)
        if kind in ("ProductExpression", "MonomialTermExpression"):
            for i in (0, 1):
                if pe.is_fixed(args[i]):
                    c = float(pe.value(args[i]))
                    if c >= 0:
                        return c * self.convex(args[1-i], mapping, name)
        if kind == "DivisionExpression" and pe.is_fixed(args[0]):
            numerator = float(pe.value(args[0]))
            denominator = args[1]
        elif kind == "PowExpression" and pe.is_fixed(args[1]) and pe.value(args[1]) == -1:
            numerator, denominator = 1., args[0]
        else:
            numerator = None
        if numerator is not None:
            lower, _ = compute_bounds_on_expr(denominator)
            if numerator < 0 or lower is None or lower < 0 or (numerator == 0 and lower == 0):
                raise UnsupportedConic(f"nonnegative affine reciprocal domain required in {name}")
            affine = self.affine(denominator, mapping)
            denom_var = self.auxiliary("reciprocal_denominator", lb=float(lower))
            value = self.auxiliary("reciprocal")
            self.g.addConstr(denom_var == affine)
            self.g.addQConstr(numerator <= value * denom_var)
            return value
        if (kind == "PowExpression" and pe.is_fixed(args[1]) and pe.value(args[1]) == .5):
            radicand = args[0]
        elif kind == "UnaryFunctionExpression" and expr.getname() == "sqrt":
            radicand = args[0]
        else:
            raise UnsupportedConic(f"unsupported nonquadratic expression in {name}: {expr}")
        squares = self.norm_squares(radicand, mapping)
        radius = self.auxiliary("norm")
        terms = []
        for weight, affine in squares:
            if not weight:
                continue
            component = self.auxiliary("norm_component", lb=-GRB.INFINITY)
            self.g.addConstr(component == affine)
            terms.append(weight * component * component)
        self.g.addQConstr(gp.quicksum(terms) <= radius * radius)
        return radius

    def row(self, expr, mapping, name, indicator=None):
        """Add expr <= 0, optionally its closed bounded perspective."""
        if indicator is None:
            value = self.convex(expr, mapping, name)
            self.g.addConstr(value <= 0, name=name)
            return
        repn = _repn(expr)
        if not (repn.is_linear() or repn.is_quadratic()):
            raise UnsupportedConic(f"nonquadratic disjunct row {name}")
        affine, quadratic, has_quadratic = self.quadratic_parts(expr, mapping, name, indicator)
        if not has_quadratic:
            self.g.addConstr(affine <= 0, name=name)
        else:
            slack = self.auxiliary("perspective_slack")
            self.g.addConstr(slack == -affine, name=name + "_slack")
            self.g.addQConstr(quadratic <= slack * indicator, name=name)

    def constraint(self, constraint, mapping, indicator=None):
        if constraint.has_ub():
            self.row(constraint.body - constraint.upper, mapping,
                     constraint.name + "_ub", indicator)
        if constraint.has_lb():
            self.row(constraint.lower - constraint.body, mapping,
                     constraint.name + "_lb", indicator)

    def build(self):
        m = self.model
        pe.TransformationFactory("core.logical_to_linear").apply_to(m)
        supported_components = {pe.Var, pe.BooleanVar, pe.Constraint, pe.Objective,
                                pe.Block, pe.Set, pe.RangeSet, pe.Param, pe.Expression,
                                pe.Suffix, Disjunct, Disjunction}
        for component in m.component_objects(active=True, descend_into=(pe.Block, Disjunct)):
            if (component.ctype not in supported_components
                    and any(getattr(data, "active", True) for data in component.values())):
                raise UnsupportedConic(f"unsupported active component {component.name}: {component.ctype.__name__}")
        disjunctions = list(m.component_data_objects(
            Disjunction, active=True, descend_into=(pe.Block, Disjunct)))
        indicator_ids = {id(d.binary_indicator_var) for dj in disjunctions for d in dj.disjuncts}
        owners = set()
        for dj in disjunctions:
            if not dj.xor:
                raise UnsupportedConic(f"nonexclusive disjunction {dj.name}")
            for d in dj.disjuncts:
                if id(d) in owners:
                    raise UnsupportedConic(f"disjunct occurs in multiple disjunctions: {d.name}")
                owners.add(id(d))
                if any(d.component_data_objects(Disjunction, active=True, descend_into=(pe.Block, Disjunct))):
                    raise UnsupportedConic(f"nested disjunction in {d.name}")
                if not d.active and not (d.binary_indicator_var.fixed and pe.value(d.binary_indicator_var) == 0):
                    raise UnsupportedConic(f"inactive disjunct without fixed-false indicator: {d.name}")
        for d in m.component_data_objects(Disjunct, active=True, descend_into=(pe.Block, Disjunct)):
            if id(d) not in owners:
                raise UnsupportedConic(f"orphan disjunct {d.name}")
        for v in m.component_data_objects(pe.Var, descend_into=(pe.Block, Disjunct)):
            lb = -GRB.INFINITY if v.lb is None else float(pe.value(v.lb))
            ub = GRB.INFINITY if v.ub is None else float(pe.value(v.ub))
            if v.fixed:
                lb = ub = float(pe.value(v))
            vtype = GRB.CONTINUOUS
            if not self.relax_integrality:
                vtype = GRB.BINARY if v.is_binary() else GRB.INTEGER if v.is_integer() else GRB.CONTINUOUS
            self.variables[id(v)] = self.g.addVar(lb=lb, ub=ub, vtype=vtype, name=v.name)
            self.pyvariables[id(v)] = v
        for con in m.component_data_objects(pe.Constraint, active=True, descend_into=(pe.Block,)):
            self.constraint(con, self.variables)
        for dj in disjunctions:
            self.g.addConstr(gp.quicksum(self.variables[id(d.binary_indicator_var)] for d in dj.disjuncts) == 1,
                             name=dj.name + "_xor")
            rows = {id(d): list(d.component_data_objects(pe.Constraint, active=True, descend_into=(pe.Block,)))
                    if d.active else [] for d in dj.disjuncts}
            union = {}
            for constraints in rows.values():
                for con in constraints:
                    for v in identify_variables(con.body, include_fixed=False):
                        if id(v) in indicator_ids:
                            raise UnsupportedConic(f"indicator referenced inside disjunct row {con.name}")
                        union[id(v)] = v
            copies = {key: [] for key in union}
            for d in dj.disjuncts:
                indicator = self.variables[id(d.binary_indicator_var)]
                mapping = {}
                for key, v in union.items():
                    if not (_finite(v.lb) and _finite(v.ub)):
                        raise UnsupportedConic(f"finite declared bounds required for disjunct variable {v.name}")
                    lo, hi = float(pe.value(v.lb)), float(pe.value(v.ub))
                    nu = self.auxiliary("disaggregated", lb=min(0., lo), ub=max(0., hi))
                    self.g.addConstr(nu >= lo * indicator)
                    self.g.addConstr(nu <= hi * indicator)
                    mapping[key] = nu
                    copies[key].append(nu)
                for con in rows[id(d)]:
                    self.constraint(con, mapping, indicator)
            for key, parts in copies.items():
                self.g.addConstr(self.variables[key] == gp.quicksum(parts))
        objectives = list(m.component_data_objects(pe.Objective, active=True, descend_into=(pe.Block, Disjunct)))
        if len(objectives) != 1:
            raise UnsupportedConic("exactly one objective is required")
        self.objective = objectives[0]
        parent = self.objective.parent_block()
        while parent is not None:
            if parent.ctype is Disjunct:
                raise UnsupportedConic("objectives inside disjuncts are unsupported")
            parent = parent.parent_block()
        self.sense = 1 if self.objective.sense == pe.minimize else -1
        expression = self.convex(self.sense * self.objective.expr, self.variables, "objective")
        self.g.setObjective(expression, GRB.MINIMIZE)
        self.g.update()


def solve(model, time_limit=300, threads=1, mip_gap=1e-4, abs_gap=1e-6,
          relax_integrality=False, output_flag=False):
    """Return a JSONable result, with dual bound in original objective sense.

    ``lb`` means a lower bound for minimization and upper bound for maximization.
    ``boolean_witness`` retains original Boolean names across the clone's
    logical transformation. Fractional associated binaries give ``None``;
    their unrounded numerical values remain in ``witness``.
    A relaxed solve's witness is not an integer GDP witness. Its objective and
    bound describe the continuous hull relaxation, with global constraints kept
    outside the disjunctions. ``time`` includes building the formulation.
    """
    start = time.perf_counter()
    builder = _Builder(model, relax_integrality, output_flag)
    try:
        builder.build()
        g = builder.g
        options = {"Threads": int(threads), "TimeLimit": float(time_limit),
                   "MIPGap": float(mip_gap), "MIPGapAbs": float(abs_gap),
                   "NonConvex": 0, "FeasibilityTol": 1e-8, "IntFeasTol": 1e-8}
        for key, value in options.items():
            g.setParam(key, value)
        g.optimize()
        status = {GRB.OPTIMAL: "optimal", GRB.INFEASIBLE: "infeasible",
                  GRB.INF_OR_UNBD: "infeasible_or_unbounded", GRB.UNBOUNDED: "unbounded",
                  GRB.TIME_LIMIT: "time_limit", GRB.NUMERIC: "numerical_error",
                  GRB.SUBOPTIMAL: "suboptimal"}.get(g.Status, f"gurobi_status_{g.Status}")
        witness = {}
        boolean_witness = {}
        obj = None
        if g.SolCount:
            for key, variable in builder.variables.items():
                pyvariable = builder.pyvariables[key]
                witness[pyvariable.name] = float(variable.X)
                pyvariable.set_value(variable.X, skip_validation=True)
            for boolean in builder.original_booleans:
                binary = boolean.get_associated_binary()
                truth = None
                if binary is not None and id(binary) in builder.variables:
                    value = float(builder.variables[id(binary)].X)
                    if abs(value) <= options["IntFeasTol"]:
                        truth = False
                    elif abs(value - 1) <= options["IntFeasTol"]:
                        truth = True
                elif boolean.value is not None:
                    truth = bool(boolean.value)
                boolean_witness[boolean.name] = truth
            obj = float(pe.value(builder.objective))
        try:
            bound = builder.sense * float(g.ObjBound)
        except (AttributeError, gp.GurobiError):
            bound = None
        if bound is not None and (not math.isfinite(bound) or abs(bound) >= 1e99):
            bound = None
        return {"status": status, "obj": obj, "lb": bound, "witness": witness,
                "boolean_witness": boolean_witness,
                "raw_status": int(g.Status), "options": options, "nodes": float(g.NodeCount),
                "time": time.perf_counter() - start, "solver_runtime": float(g.Runtime),
                "relax_integrality": bool(relax_integrality),
                "gurobi_version": ".".join(map(str, gp.gurobi.version()))}
    finally:
        builder.close()
