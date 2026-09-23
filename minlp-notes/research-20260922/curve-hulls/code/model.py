"""OSiL instance -> Gurobi model, optionally with every univariate term of selected variables
replaced by an auxiliary variable, so that the curve-hull cuts can act on (x, t_1, ..., t_k).

Atoms.  A univariate *atom* of variable x is a maximal nonlinear subexpression in x alone, after
splitting sums, negations and constant factors/divisors (so exp(x) + 3 x^2 gives the atoms exp(x)
and x^2).  Diagonal quadratic terms c x_i^2 give the atom x_i^2.  Atoms are identified up to a
constant factor through their sympy form.

Selection.  A variable is selected when it is not binary, has finite bounds l < u, and has at least
`kmin` atoms that are finite on [l, u] and linearly independent of each other and of (1, x)
(numerical rank test on 64 Chebyshev points).  Atoms that fail the tests stay as they are.

Substitution (mode "sub").  Each selected atom f of x gets a variable t with bounds equal to a
rigorous enclosure of g([l, u]) and the defining constraint t = g(x), where f = factor * g is a
power-of-two rescaling (class Scale) that gives t a range of order 1 (a quadratic equality for x^2,
a general nonlinear constraint otherwise); every occurrence c*f in the model becomes (c * factor) t.
Mode "orig" builds the same model without substitution.
"""
from __future__ import annotations

import math
import os
import xml.etree.ElementTree as ET
from types import SimpleNamespace

import numpy as np
import sympy as sp

import gurobipy as gp
from gurobipy import GRB, nlfunc

from curvehull import T, Curve  # noqa: E402


NS = "{os.optimizationservices.org}"
UNARY = {"ln": "log", "exp": "exp", "sqrt": "sqrt", "sin": "sin", "cos": "cos", "square": "square",
         "negate": "negate", "abs": "abs"}


def _tree(node):
    tag = node.tag.replace(NS, "")
    if tag == "number":
        return ("num", float(node.get("value")))
    if tag == "variable":
        coef = float(node.get("coef", "1"))
        v = ("var", int(node.get("idx")))
        return v if coef == 1.0 else ("times", ("num", coef), v)
    kids = [_tree(c) for c in node]
    if tag in ("sum", "plus"):
        return ("sum", *kids)
    if tag == "minus":
        return ("sum", kids[0], ("negate", kids[1]))
    if tag in ("times", "product"):
        return ("times", *kids)
    if tag in ("divide", "power"):
        return (tag, *kids)
    if tag in UNARY:
        return (UNARY[tag], kids[0])
    raise NotImplementedError(tag)


def read_osil(path):
    """Same format as code/univariate_envelopes/uenv/osil.py (rows[0] is the objective)."""
    fl = lambda s: float(s.replace("-INF", "-inf").replace("INF", "inf"))
    data = ET.parse(path).getroot().find(f"{NS}instanceData")
    I = SimpleNamespace(var_lb=[], var_ub=[], var_type=[], var_names=[])
    for v in data.find(f"{NS}variables"):
        t = v.get("type", "C")
        I.var_type.append(t)
        I.var_lb.append(fl(v.get("lb", "0")))
        I.var_ub.append(fl(v.get("ub", "1" if t == "B" else "INF")))
        I.var_names.append(v.get("name"))
    rows = {-1: {"lin": {}, "quad": [], "nl": None, "lb": None, "ub": None}}
    objs = data.find(f"{NS}objectives")
    I.obj_sense, I.obj_const = "min", 0.0
    if objs is not None and len(objs):
        o = objs[0]
        I.obj_sense, I.obj_const = o.get("maxOrMin", "min"), float(o.get("constant", "0"))
        for c in o:
            rows[-1]["lin"][int(c.get("idx"))] = float(c.text)
    cons = data.find(f"{NS}constraints")
    ncons = 0
    if cons is not None:
        for i, c in enumerate(cons):
            assert c.get("constant") is None
            rows[i] = {"lin": {}, "quad": [], "nl": None, "lb": fl(c.get("lb", "-INF")), "ub": fl(c.get("ub", "INF"))}
            ncons += 1
    lcc = data.find(f"{NS}linearConstraintCoefficients")
    if lcc is not None:
        def expand(el):
            out = []
            for e in el:
                mult, incr = int(e.get("mult", "1")), float(e.get("incr", "0"))
                out += [float(e.text) + k * incr for k in range(mult)]
            return out
        start = [int(v) for v in expand(lcc.find(f"{NS}start"))]
        values = expand(lcc.find(f"{NS}value"))
        byrow = lcc.find(f"{NS}rowIdx") is None
        idx = [int(v) for v in expand(lcc.find(f"{NS}colIdx" if byrow else f"{NS}rowIdx"))]
        for a in range(len(start) - 1):
            for k in range(start[a], start[a + 1]):
                r, col = (a, idx[k]) if byrow else (idx[k], a)
                rows[r]["lin"][col] = values[k]
    qc = data.find(f"{NS}quadraticCoefficients")
    if qc is not None:
        for q in qc:
            rows[int(q.get("idx"))]["quad"].append((int(q.get("idxOne")), int(q.get("idxTwo")), float(q.get("coef", "1"))))
    nle = data.find(f"{NS}nonlinearExpressions")
    if nle is not None:
        for e in nle:
            rows[int(e.get("idx"))]["nl"] = _tree(e[0])
    I.rows = [rows[i] for i in [-1, *range(ncons)]]
    return I


OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil/{}.osil")
FUNCS = {"exp": sp.exp, "log": sp.log, "sqrt": sp.sqrt, "sin": sp.sin, "cos": sp.cos, "abs": sp.Abs}


def variables(t, acc=None):
    acc = set() if acc is None else acc
    if t[0] == "var":
        acc.add(t[1])
    elif t[0] not in ("num", "aux"):
        for c in t[1:]:
            variables(c, acc)
    return acc


def _num(v: float, exponent=False):
    if v == int(v) and abs(v) < 1e15:
        return sp.Integer(int(v))
    return sp.Rational(repr(v)) if exponent else sp.Float(v, 17)


def to_sympy(t):
    op = t[0]
    if op == "num":
        return _num(t[1])
    if op == "var":
        return T
    if op == "power" and t[2][0] == "num":
        return to_sympy(t[1]) ** _num(t[2][1], exponent=True)
    k = [to_sympy(c) for c in t[1:]]
    if op == "sum":
        return sp.Add(*k)
    if op == "times":
        return sp.Mul(*k)
    if op == "negate":
        return -k[0]
    if op == "divide":
        return k[0] / k[1]
    if op == "power":
        return k[0] ** k[1]
    if op == "square":
        return k[0] ** 2
    return FUNCS[op](k[0])


def canon(e):
    """(coefficient, key expression) with e = coefficient * key."""
    c, rest = e.as_coeff_Mul()
    return float(c), rest


def _walk_atoms(t, visit):
    """Call visit(v, subtree) for every univariate atom; returns the rewritten tree
    (visit returns a replacement tree or None to keep the atom)."""
    op = t[0]
    if op in ("num", "var", "aux"):
        return t
    vs = variables(t)
    if len(vs) == 1:
        v = next(iter(vs))
        if op in ("sum", "negate"):
            return (op, *[_walk_atoms(c, visit) for c in t[1:]])
        if op == "times":
            nc = [c for c in t[1:] if variables(c)]
            if len(nc) == 1:
                return (op, *[_walk_atoms(c, visit) if variables(c) else c for c in t[1:]])
        if op == "divide" and not variables(t[2]):
            return (op, _walk_atoms(t[1], visit), t[2])
        e = to_sympy(t)
        if sp.diff(e, T, 2) == 0:  # affine in x
            return t
        r = visit(v, t, e)
        return t if r is None else r
    return (op, *[_walk_atoms(c, visit) for c in t[1:]])


def cheb(l, u, n=64):
    k = np.arange(n)
    return 0.5 * (l + u) + 0.5 * (u - l) * np.cos(np.pi * (k + 0.5) / n)


class Detected:
    """Per selected variable: list of (key, sympy expr) and its Curve."""

    def __init__(self, inst, kmin=2, max_vars=None):
        self.inst = inst
        found: dict[int, dict] = {}

        def rec(v, t, e):
            c, key = canon(e)
            found.setdefault(v, {}).setdefault(sp.srepr(key), key)
            return None

        for r in inst.rows:
            if r["nl"] is not None:
                _walk_atoms(r["nl"], rec)
            for i, j, c in r["quad"]:
                if i == j:
                    found.setdefault(i, {}).setdefault(sp.srepr(T**2), T**2)
        self.all_atoms = found
        self.sel: dict[int, list] = {}
        self.curves: dict[int, Curve] = {}
        self.rejected = {}
        curve_cache = {}
        for v, atoms in sorted(found.items()):
            l, u = inst.var_lb[v], inst.var_ub[v]
            if inst.var_type[v] == "B" or not (math.isfinite(l) and math.isfinite(u)) or u <= l:
                self.rejected[v] = "binary or unbounded"
                continue
            if len(atoms) < kmin:
                continue
            ts = cheb(l, u)
            basis = [np.ones_like(ts), ts]
            keep = []
            for sk, key in sorted(atoms.items(), key=lambda kv: sp.count_ops(kv[1])):
                try:
                    with np.errstate(all="ignore"):
                        vals = np.broadcast_to(np.asarray(sp.lambdify(T, key, "numpy")(ts), float), ts.shape)
                    Curve([key], l, u, npieces=64, ngrid=64)  # finiteness on [l, u] (interval enclosure)
                except Exception:
                    continue
                if not np.all(np.isfinite(vals)):
                    continue
                A = np.column_stack(basis)
                coef, *_ = np.linalg.lstsq(A, vals, rcond=None)
                res = np.linalg.norm(A @ coef - vals) / max(np.linalg.norm(vals), 1e-300)
                if res < 1e-8:
                    continue
                basis.append(vals)
                keep.append((sk, key, Scale(key, np.abs(vals).max())))
            if len(keep) < kmin:
                self.rejected[v] = f"{len(keep)} independent finite atoms"
                continue
            ck = (tuple((sk, sc.a, sc.b) for sk, _, sc in keep), l, u)
            if ck not in curve_cache:
                curve_cache[ck] = Curve([sc.g for _, _, sc in keep], l, u)
            self.sel[v] = keep
            self.curves[v] = curve_cache[ck]
            if max_vars and len(self.sel) >= max_vars:
                break


class Scale:
    """Power-of-two scaling of an auxiliary variable: t = g(x) with key(x) = factor * g(x).
    factor = 2^e with e = ceil(log2 max|key|) - 30 when max|key| > 2^30 (so |t| <= 2^30), and
    e = ceil(log2 max|key|) when max|key| < 1 (so |t| is of order 1); otherwise no scaling.
    Scaling down is limited because Gurobi's absolute feasibility tolerance on t = g(x) is multiplied
    by the factor in the original term; it is needed at all because Gurobi drops coefficients below
    1e-13, which cuts on huge ranges (x^3 ~ 4e12) would otherwise contain.  An earlier version scaled
    every atom to order 1 (factors up to 2^42); that let Gurobi accept points violating the original
    model by 8.6e-4 on ex8_4_7 and is why the affected instances were rerun.
    Powers key = x^p: g(x) = (2^-a x)^p, factor = 2^(a p) with a = round(e / p) (the scale is applied to
    the argument, because Gurobi treats constants below 1e-13 inside nonlinear expressions as zero).
    Other atoms: g(x) = 2^-b key(x), factor = 2^b, b = e clipped to [-30, 30]."""

    def __init__(self, key, vmax):
        L = math.ceil(math.log2(max(vmax, 1e-300)))
        e = L - 30 if L > 30 else (L if L < 0 else 0)
        self.power = None
        if key.is_Pow and key.args[0] == T and key.args[1].is_Number:
            p = key.args[1]
            self.power, self.a, self.b = float(p), int(round(e / float(p))), 0
            self.factor = 2.0 ** (self.a * float(p))
            self.g = key * sp.Integer(2) ** (-self.a * p)
        else:
            self.a, self.b = 0, max(-30, min(30, e))
            self.factor = 2.0 ** self.b
            self.g = key * sp.Integer(2) ** (-self.b)

    def grb(self, key, x):
        if self.power is not None:
            xs = x * 2.0 ** (-self.a)
            if self.power == 2:
                return xs * xs
            if self.power == -1:
                return 1.0 / xs
            return xs ** self.power
        return 2.0 ** (-self.b) * sym_to_grb(key, x)


# ------------------------------------------------------------------ Gurobi
def sym_to_grb(e, x):
    if e == T:
        return x
    if e.is_Number:
        return float(e)
    if e.is_Add:
        out = 0.0
        for a in e.args:
            out = out + sym_to_grb(a, x)
        return out
    if e.is_Mul:
        out = 1.0
        for a in e.args:
            out = out * sym_to_grb(a, x)
        return out
    if e.is_Pow:
        b, p = e.args
        B = sym_to_grb(b, x)
        if p == 2:
            return B * B
        if p == sp.Rational(1, 2):
            return nlfunc.sqrt(B)
        if p.is_Integer and int(p) == -1:
            return 1.0 / B
        return B ** float(p)
    f = e.func
    if f in (sp.exp, sp.log, sp.sin, sp.cos):
        return getattr(nlfunc, f.__name__)(sym_to_grb(e.args[0], x))
    raise NotImplementedError(str(f))


def _is_quad(e):
    return isinstance(e, (int, float, gp.Var, gp.LinExpr, gp.QuadExpr))


class Built:
    pass


def build(name, mode="orig", kmin=2, threads=1, det=None, quiet=True):
    inst = read_osil(OSIL.format(name))
    m = gp.Model(name)
    m.Params.OutputFlag = 0 if quiet else 1
    m.Params.Threads = threads
    m.Params.NonConvex = 2
    m.Params.MIPGap = 1e-4
    x = [m.addVar(lb=(-GRB.INFINITY if math.isinf(l) else l), ub=(GRB.INFINITY if math.isinf(u) else u),
                  vtype={"B": GRB.BINARY, "I": GRB.INTEGER}.get(t, GRB.CONTINUOUS), name=f"x{j}")
         for j, (l, u, t) in enumerate(zip(inst.var_lb, inst.var_ub, inst.var_type))]
    aux = {}  # (v, srepr) -> Var
    if mode == "sub":
        det = det or Detected(inst, kmin=kmin)
        for v, keep in det.sel.items():
            C = det.curves[v]
            for j, (sk, key, sc) in enumerate(keep):
                lo, hi = C.rlo[j + 1], C.rhi[j + 1]
                t = m.addVar(lb=lo, ub=hi, name=f"t{v}_{j}")
                aux[(v, sk)] = (t, sc.factor)
                g = sc.grb(key, x[v])
                if isinstance(g, gp.QuadExpr):
                    m.addQConstr(t == g, name=f"def{v}_{j}")
                else:
                    m.addGenConstrNL(t, g, name=f"def{v}_{j}")

    def visit(v, t, e):
        c, key = canon(e)
        a = aux.get((v, sp.srepr(key)))
        return None if a is None else ("times", ("num", c * a[1]), ("aux", a[0]))

    def gexpr(t):
        op = t[0]
        if op == "num":
            return t[1]
        if op == "var":
            return x[t[1]]
        if op == "aux":
            return t[1]
        k = [gexpr(c) for c in t[1:]]
        if op == "sum":
            out = k[0]
            for c in k[1:]:
                out = out + c
            return out
        if op == "negate":
            return -1.0 * k[0]
        if op == "times":
            out = k[0]
            for c in k[1:]:
                out = out * c
            return out
        if op == "divide":
            if isinstance(k[1], (int, float)):
                return k[0] * (1.0 / k[1])
            return k[0] / k[1]
        if op == "power":
            if isinstance(k[1], (int, float)) and k[1] == 2:
                return k[0] * k[0]
            return k[0] ** k[1]
        if op == "square":
            return k[0] * k[0]
        if op in ("sin", "cos", "exp", "log", "sqrt"):
            return getattr(nlfunc, op)(k[0])
        if op == "abs":
            inner = m.addVar(lb=-GRB.INFINITY)
            m.addGenConstrNL(inner, k[0])
            out = m.addVar()
            m.addGenConstrAbs(out, inner)
            return out
        raise NotImplementedError(op)

    sq_aux = {v: a for (v, sk), a in aux.items() if sk == sp.srepr(T**2)}
    nnl = 0
    for ridx, r in enumerate(inst.rows):
        e = gp.QuadExpr()
        for i, c in r["lin"].items():
            e += c * x[i]
        for i, j, c in r["quad"]:
            if i == j and i in sq_aux:
                e += c * sq_aux[i][1] * sq_aux[i][0]
            else:
                e += c * x[i] * x[j]
        if r["nl"] is not None:
            tree = _walk_atoms(r["nl"], visit) if aux else r["nl"]
            g = gexpr(tree)
            if _is_quad(g):
                e += g
            else:
                z = m.addVar(lb=-GRB.INFINITY, name=f"nl{ridx}")
                m.addGenConstrNL(z, g)
                e += z
                nnl += 1
        if ridx == 0:
            m.setObjective(e + inst.obj_const, GRB.MINIMIZE if inst.obj_sense == "min" else GRB.MAXIMIZE)
            continue
        if r["lb"] == r["ub"]:
            m.addConstr(e == r["lb"], name=f"r{ridx}")
        else:
            if math.isfinite(r["lb"]):
                m.addConstr(e >= r["lb"], name=f"r{ridx}lo")
            if math.isfinite(r["ub"]):
                m.addConstr(e <= r["ub"], name=f"r{ridx}up")
    m.update()
    B = Built()
    B.m, B.x, B.aux, B.inst, B.det, B.nnl = m, x, aux, inst, det, nnl
    return B


def summary(det):
    """Human-readable list of the selected curves."""
    out = {}
    for v, keep in det.sel.items():
        key = ", ".join(str(k) for _, k, _ in keep) + f" on [{det.inst.var_lb[v]:g}, {det.inst.var_ub[v]:g}]"
        out[key] = out.get(key, 0) + 1
    return out
