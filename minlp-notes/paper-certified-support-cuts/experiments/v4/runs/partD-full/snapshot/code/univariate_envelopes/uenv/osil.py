"""Read a MINLPLib OSiL file and build a SCIP model, optionally collapsing composite
univariate subexpressions into  w == g(x)  constraints handled by ``UnivariateHdlr``.

Expression trees are nested tuples: ("num", v), ("var", idx), or (op, child, ...).
"""
from __future__ import annotations

import math
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

import pyscipopt as ps
import sympy as sp

from .curvature import X
from .envelope import Univariate
from .scip_plugin import add_univariate, install

NS = "{os.optimizationservices.org}"
UNARY = {"ln": "log", "exp": "exp", "sqrt": "sqrt", "sin": "sin", "cos": "cos", "square": "square",
         "negate": "negate", "abs": "abs"}


@dataclass
class Instance:
    name: str
    var_lb: list[float]
    var_ub: list[float]
    var_type: list[str]
    obj_sense: str
    obj_const: float
    rows: list[dict]                     # row -1 is the objective: {"lin": {}, "quad": [], "nl": tree|None, "lb", "ub"}
    var_names: list[str] = field(default_factory=list)


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


def read_osil(path: str) -> Instance:
    root = ET.parse(path).getroot()
    data = root.find(f"{NS}instanceData")
    vs = data.find(f"{NS}variables")
    lb, ub, vt, names = [], [], [], []
    for v in vs:
        t = v.get("type", "C")
        lb.append(float(v.get("lb", "0").replace("-INF", "-inf").replace("INF", "inf")))
        default_ub = "1" if t == "B" else "INF"
        ub.append(float(v.get("ub", default_ub).replace("-INF", "-inf").replace("INF", "inf")))
        vt.append(t)
        names.append(v.get("name", f"x{len(names)}"))
    rows = {}
    objs = data.find(f"{NS}objectives")
    sense, const = "min", 0.0
    rows[-1] = {"lin": {}, "quad": [], "nl": None, "lb": None, "ub": None}
    if objs is not None and len(objs):
        o = objs[0]
        sense, const = o.get("maxOrMin", "min"), float(o.get("constant", "0"))
        for c in o:
            rows[-1]["lin"][int(c.get("idx"))] = float(c.text)
    cons = data.find(f"{NS}constraints")
    ncons = 0
    if cons is not None:
        for i, c in enumerate(cons):
            rows[i] = {"lin": {}, "quad": [], "nl": None,
                       "lb": float(c.get("lb", "-inf").replace("INF", "inf")),
                       "ub": float(c.get("ub", "inf").replace("INF", "inf"))}
            ncons += 1
    lcc = data.find(f"{NS}linearConstraintCoefficients")
    if lcc is not None:
        def expand(el):
            out = []
            for e in el:
                mult, incr = int(e.get("mult", "1")), float(e.get("incr", "0"))
                val = float(e.text)
                out += [val + k * incr for k in range(mult)]
            return out
        start = [int(v) for v in expand(lcc.find(f"{NS}start"))]
        values = expand(lcc.find(f"{NS}value"))
        if lcc.find(f"{NS}rowIdx") is not None:
            idx = [int(v) for v in expand(lcc.find(f"{NS}rowIdx"))]
            for col in range(len(start) - 1):
                for k in range(start[col], start[col + 1]):
                    rows[idx[k]]["lin"][col] = values[k]
        else:
            idx = [int(v) for v in expand(lcc.find(f"{NS}colIdx"))]
            for r in range(len(start) - 1):
                for k in range(start[r], start[r + 1]):
                    rows[r]["lin"][idx[k]] = values[k]
    qc = data.find(f"{NS}quadraticCoefficients")
    if qc is not None:
        for q in qc:
            rows[int(q.get("idx"))]["quad"].append((int(q.get("idxOne")), int(q.get("idxTwo")), float(q.get("coef", "1"))))
    nle = data.find(f"{NS}nonlinearExpressions")
    if nle is not None:
        for e in nle:
            rows[int(e.get("idx"))]["nl"] = _tree(e[0])
    return Instance(path.split("/")[-1].removesuffix(".osil"), lb, ub, vt, sense, const,
                    [rows[i] for i in [-1, *range(ncons)]], names)


# ---------------------------------------------------------------- analysis
def variables(t, acc=None) -> set[int]:
    acc = set() if acc is None else acc
    if t[0] == "var":
        acc.add(t[1])
    elif t[0] != "num":
        for c in t[1:]:
            variables(c, acc)
    return acc


def nonlinear_ops(t) -> int:
    if t[0] in ("num", "var"):
        return 0
    own = 0
    if t[0] == "times":
        own = int(sum(1 for c in t[1:] if variables(c)) >= 2)
    elif t[0] == "divide":
        own = int(bool(variables(t[2])))
    elif t[0] not in ("sum", "negate"):
        own = 1
    return own + sum(nonlinear_ops(c) for c in t[1:])


def to_sympy(t, sym):
    op = t[0]
    if op == "num":
        return sp.Float(t[1]) if t[1] != int(t[1]) else sp.Integer(int(t[1]))
    if op == "var":
        return sym
    k = [to_sympy(c, sym) for c in t[1:]]
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
    return {"log": sp.log, "exp": sp.exp, "sqrt": sp.sqrt, "sin": sp.sin, "cos": sp.cos, "abs": sp.Abs}[op](k[0])


def collapse(t, found: list, min_ops: int = 2):
    """Replace maximal univariate subtrees with >= min_ops nonlinear operators by ("uni", k).

    Inside a sum, the univariate summands in the same variable are grouped into one function.
    ``found[k]`` = (variable index, subtree).
    """
    if t[0] in ("num", "var"):
        return t
    vs = variables(t)
    if len(vs) == 1 and nonlinear_ops(t) >= min_ops and not _has(t, "abs"):
        found.append((next(iter(vs)), t))
        return ("uni", len(found) - 1)
    if t[0] == "sum":
        groups: dict[int, list] = {}
        rest = []
        for c in t[1:]:
            cv = variables(c)
            if len(cv) == 1 and not _has(c, "abs"):
                groups.setdefault(next(iter(cv)), []).append(c)
            else:
                rest.append(collapse(c, found, min_ops))
        for v, cs in groups.items():
            g = cs[0] if len(cs) == 1 else ("sum", *cs)
            if nonlinear_ops(g) >= min_ops:
                found.append((v, g))
                rest.append(("uni", len(found) - 1))
            else:
                rest += cs
        return ("sum", *rest)
    return (t[0], *[collapse(c, found, min_ops) for c in t[1:]])


def _has(t, op) -> bool:
    return t[0] == op or (t[0] not in ("num", "var", "uni") and any(_has(c, op) for c in t[1:]))


# ---------------------------------------------------------------- SCIP model
def _scip_expr(t, xs, uni_vars):
    op = t[0]
    if op == "num":
        return t[1]
    if op == "var":
        return xs[t[1]]
    if op == "uni":
        return uni_vars[t[1]]
    k = [_scip_expr(c, xs, uni_vars) for c in t[1:]]
    if op == "sum":
        out = k[0]
        for c in k[1:]:
            out = out + c
        return out
    if op == "times":
        out = k[0]
        for c in k[1:]:
            out = out * c
        return out
    if op == "negate":
        return -k[0]
    if op == "divide":
        return k[0] / k[1]
    if op == "power":
        if not isinstance(k[1], (int, float)):
            raise NotImplementedError("variable exponent")
        return k[0] ** (int(k[1]) if float(k[1]).is_integer() else k[1])
    if op == "square":
        return k[0] ** 2
    if op == "abs":
        return abs(k[0])
    return {"log": ps.log, "exp": ps.exp, "sqrt": ps.sqrt, "sin": ps.sin, "cos": ps.cos}[op](k[0])


def presolved_bounds(inst: Instance, time_limit: float = 30.0) -> tuple[list[float], list[float]]:
    """Variable bounds implied by the constraints, from SCIP presolve without dual reductions."""
    m, _, _ = build_scip(inst, "native")
    m.hideOutput()
    m.setParam("misc/allowstrongdualreds", False)
    m.setParam("misc/allowweakdualreds", False)
    m.setParam("limits/time", time_limit)
    m.presolve()
    lb, ub = list(inst.var_lb), list(inst.var_ub)
    if m.getStage() in (ps.SCIP_STAGE.PRESOLVED, ps.SCIP_STAGE.PRESOLVING):
        for i, v in enumerate(m.getVars(transformed=False)[:len(lb)]):
            if v.name != f"v{i}":
                continue
            t = m.getTransformedVar(v)
            lb[i], ub[i] = max(lb[i], t.getLbGlobal()), min(ub[i], t.getUbGlobal())
    return [(-math.inf if l <= -1e20 else l) for l in lb], [(math.inf if u >= 1e20 else u) for u in ub]


_CACHE: dict = {}


def _univariate(expr, lo, hi) -> Univariate:
    key = (sp.srepr(expr), lo, hi)
    if key not in _CACHE:
        _CACHE[key] = Univariate(expr, lo, hi)
    return _CACHE[key]


def build_scip(inst: Instance, mode: str = "native", min_ops: int = 2, bounds=None):
    """mode: "native" (as given), "hybrid" (collapse + handler), "split" (collapse only).

    ``bounds`` = (lb, ub) overrides the declared variable bounds for the univariate domains.
    """
    dom_lb, dom_ub = bounds if bounds is not None else (inst.var_lb, inst.var_ub)
    m = ps.Model(inst.name)
    xs = [m.addVar(name=f"v{i}", lb=(None if math.isinf(l) else l), ub=(None if math.isinf(u) else u),
                   vtype={"C": "C", "B": "B", "I": "I"}.get(t, "C"))
          for i, (l, u, t) in enumerate(zip(inst.var_lb, inst.var_ub, inst.var_type))]
    hdlr = install(m, hybrid=True) if mode == "hybrid" else None
    stats = {"collapsed": 0, "skipped": 0}
    for ridx, row in enumerate(inst.rows):
        found: list = []
        nl = row["nl"]
        if nl is not None and mode != "native":
            nl = collapse(nl, found, min_ops)
        uni_vars = {}
        for k, (vi, sub) in enumerate(found):
            lo, hi = dom_lb[vi], dom_ub[vi]
            f = None
            if math.isfinite(lo) and math.isfinite(hi) and hi > lo:
                try:
                    f = _univariate(to_sympy(sub, X), lo, hi)
                    glo, ghi = f.range(lo, hi)
                    if not (math.isfinite(glo) and math.isfinite(ghi)):
                        f = None
                except Exception:
                    f = None
            if f is None:                      # keep the subtree native
                stats["skipped"] += 1
                uni_vars[k] = _scip_expr(sub, xs, {})
                continue
            # The domain of f is an implied bound; impose it so that SCIP and the handler agree.
            if xs[vi].getLbOriginal() < lo:
                m.chgVarLb(xs[vi], lo)
            if xs[vi].getUbOriginal() > hi:
                m.chgVarUb(xs[vi], hi)
            w = m.addVar(name=f"uni_{ridx}_{k}", lb=glo, ub=ghi)
            m.addCons(w == _scip_expr(sub, xs, {}), name=f"unidef_{ridx}_{k}")
            if hdlr is not None:
                add_univariate(m, hdlr, w, xs[vi], f, f"uni_{ridx}_{k}")
            uni_vars[k] = w
            stats["collapsed"] += 1
        expr = sum(c * xs[i] for i, c in row["lin"].items()) if row["lin"] else 0.0
        for i, j, c in row["quad"]:
            expr = expr + c * xs[i] * xs[j]
        if nl is not None:
            expr = expr + _scip_expr(nl, xs, uni_vars)
        if ridx == 0:
            if row["quad"] or nl is not None:
                z = m.addVar(name="objvar", lb=None, ub=None)
                m.addCons(z >= expr + inst.obj_const if inst.obj_sense == "min" else z <= expr + inst.obj_const)
                m.setObjective(z, "minimize" if inst.obj_sense == "min" else "maximize")
            else:
                m.setObjective(expr + inst.obj_const, "minimize" if inst.obj_sense == "min" else "maximize")
            continue
        if isinstance(expr, float):
            continue
        lb, ub = row["lb"], row["ub"]
        if lb == ub:
            m.addCons(expr == lb)
        else:
            if math.isfinite(lb):
                m.addCons(expr >= lb)
            if math.isfinite(ub):
                m.addCons(expr <= ub)
    return m, hdlr, stats
