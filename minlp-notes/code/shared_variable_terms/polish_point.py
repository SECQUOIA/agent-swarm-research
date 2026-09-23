"""Improved primal point for waterno2_18: solve the linked model with Gurobi (4 threads, time limit),
fix the binaries at the incumbent, re-solve the continuous NONCONVEX problem in the NATIVE model with
tight tolerances from that start, then evaluate every native constraint in plain floating point.
python polish_point.py <instance> <tl_linked> <tl_polish>"""
import json, math, os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "univariate_envelopes"))
import gurobipy as gp
from gurobipy import GRB, nlfunc
from uenv.osil import read_osil
import link_detect


def expr(t, x):
    op = t[0]
    if op == "num": return t[1]
    if op == "var": return x[t[1]]
    k = [expr(c, x) for c in t[1:]]
    if op == "sum":
        o = k[0]
        for c in k[1:]: o = o + c
        return o
    if op == "negate": return -1.0 * k[0]
    if op == "times":
        o = k[0]
        for c in k[1:]: o = o * c
        return o
    if op == "divide": return k[0] / k[1]
    if op == "power": return k[0] ** k[1]
    if op == "square": return k[0] ** 2
    return getattr(nlfunc, op)(k[0])


def ev(t, val):
    op = t[0]
    if op == "num": return t[1]
    if op == "var": return val[t[1]]
    k = [ev(c, val) for c in t[1:]]
    if op == "sum": return sum(k)
    if op == "negate": return -k[0]
    if op == "times":
        o = 1.0
        for c in k: o *= c
        return o
    if op == "divide": return k[0] / k[1]
    if op == "power": return k[0] ** k[1]
    if op == "square": return k[0] ** 2
    return getattr(math, op)(k[0])


def build(inst, linked, fix=None, tol=1e-6, tl=60, threads=4, start=None):
    m = gp.Model(); m.Params.OutputFlag = 0; m.Params.TimeLimit = tl; m.Params.Threads = threads; m.Params.MIPGap = 1e-4
    m.Params.FeasibilityTol = tol; m.Params.IntFeasTol = min(tol, 1e-5); m.Params.OptimalityTol = tol
    x = []
    for i, (l, u, t) in enumerate(zip(inst.var_lb, inst.var_ub, inst.var_type)):
        vt = {"B": GRB.BINARY, "I": GRB.INTEGER}.get(t, GRB.CONTINUOUS)
        if fix is not None and t in ("B", "I"):
            l = u = round(fix[i]); vt = GRB.CONTINUOUS
        x.append(m.addVar(lb=(-GRB.INFINITY if math.isinf(l) else l), ub=(GRB.INFINITY if math.isinf(u) else u), vtype=vt))
    for ridx, r in enumerate(inst.rows):
        e = gp.QuadExpr()
        for i, c in r["lin"].items(): e += c * x[i]
        for i, j, c in r["quad"]: e += c * x[i] * x[j]
        if r["nl"] is not None:
            z = m.addVar(lb=-GRB.INFINITY); m.addGenConstrNL(z, expr(r["nl"], x)); e += z
        if ridx == 0: m.setObjective(e + inst.obj_const, GRB.MINIMIZE if inst.obj_sense == "min" else GRB.MAXIMIZE); continue
        if r["lb"] == r["ub"]: m.addConstr(e == r["lb"])
        else:
            if math.isfinite(r["lb"]): m.addConstr(e >= r["lb"])
            if math.isfinite(r["ub"]): m.addConstr(e <= r["ub"])
    if linked:
        trig, pw = link_detect.detect(inst)
        for vi, ps_ in pw.items():
            lo, hi = inst.var_lb[vi], inst.var_ub[vi]; ref = min(ps_, key=abs); tv = {}
            for p in ps_:
                a, b = sorted((lo ** p, hi ** p)); tv[p] = m.addVar(lb=a, ub=b); m.addGenConstrNL(tv[p], x[vi] ** p)
            for p in ps_:
                if p != ref: m.addGenConstrNL(tv[p], tv[ref] ** (p / ref))
    if start is not None:
        for xi, s in zip(x, start): xi.Start = s
    m.optimize()
    return m, x


def violation(inst, val):
    worst = 0.0
    for i, (l, u, t) in enumerate(zip(inst.var_lb, inst.var_ub, inst.var_type)):
        worst = max(worst, l - val[i], val[i] - u)
        if t in ("B", "I"): worst = max(worst, abs(val[i] - round(val[i])))
    for ridx, r in enumerate(inst.rows):
        if ridx == 0: continue
        a = sum(c * val[i] for i, c in r["lin"].items()) + sum(c * val[i] * val[j] for i, j, c in r["quad"])
        if r["nl"] is not None: a += ev(r["nl"], val)
        worst = max(worst, r["lb"] - a, a - r["ub"])
    obj = inst.rows[0]
    o = sum(c * val[i] for i, c in obj["lin"].items()) + sum(c * val[i] * val[j] for i, j, c in obj["quad"]) + inst.obj_const
    if obj["nl"] is not None: o += ev(obj["nl"], val)
    return worst, o


name = sys.argv[1]; tl1 = float(sys.argv[2]); tl2 = float(sys.argv[3])
inst = read_osil(os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil"))
m, x = build(inst, True, tl=tl1)
pt = [xi.X for xi in x]
w0, o0 = violation(inst, pt)
print(json.dumps({"stage": "linked", "status": m.Status, "objective_native_eval": o0, "max_violation": w0, "dual": m.ObjBound}))
best = (w0, o0, pt)
for tol in (1e-8, 1e-9):
    m2, x2 = build(inst, False, fix=pt, tol=tol, tl=tl2, start=pt)
    if m2.SolCount:
        p2 = [xi.X for xi in x2]; w, o = violation(inst, p2)
        print(json.dumps({"stage": f"polish_tol_{tol}", "status": m2.Status, "objective_native_eval": o, "max_violation": w}))
        if w < best[0]: best = (w, o, p2)
json.dump({"name": name, "objective": best[1], "max_violation": best[0], "point": best[2]}, open(f"point_{name}.json", "w"))
print(json.dumps({"stage": "saved", "objective": best[1], "max_violation": best[0]}))
