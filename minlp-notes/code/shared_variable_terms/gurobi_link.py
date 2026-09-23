"""Gurobi 13 on a MINLPLib OSiL instance, native or with the links of link_pilot.py.
python gurobi_link.py <instance> {native|linked} [tl] [threads]"""
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
        out = k[0]
        for c in k[1:]: out = out + c
        return out
    if op == "negate": return -1.0 * k[0]
    if op == "times":
        out = k[0]
        for c in k[1:]: out = out * c
        return out
    if op == "divide": return k[0] / k[1]
    if op == "power": return k[0] ** k[1]
    if op == "square": return k[0] ** 2
    if op in ("sin", "cos", "exp", "log", "sqrt"): return getattr(nlfunc, op)(k[0])
    if op == "abs":
        inner = m.addVar(lb=-GRB.INFINITY); m.addGenConstrNL(inner, k[0])
        out = m.addVar(); m.addGenConstrAbs(out, inner); return out
    raise NotImplementedError(op)

name, mode = sys.argv[1], sys.argv[2]
rule = "positive" if mode == "linked2" else "smallest"
tl = float(sys.argv[3]) if len(sys.argv) > 3 else 60
threads = int(sys.argv[4]) if len(sys.argv) > 4 else 4
inst = read_osil(os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil"))
m = gp.Model(); m.Params.OutputFlag = 0; m.Params.TimeLimit = tl; m.Params.Threads = threads; m.Params.MIPGap = 1e-4
x = [m.addVar(lb=(-GRB.INFINITY if math.isinf(l) else l), ub=(GRB.INFINITY if math.isinf(u) else u),
              vtype={"B": GRB.BINARY, "I": GRB.INTEGER}.get(t, GRB.CONTINUOUS)) for l, u, t in zip(inst.var_lb, inst.var_ub, inst.var_type)]
for ridx, r in enumerate(inst.rows):
    e = gp.QuadExpr()
    for i, c in r["lin"].items(): e += c * x[i]
    for i, j, c in r["quad"]: e += c * x[i] * x[j]
    if r["nl"] is not None:
        z = m.addVar(lb=-GRB.INFINITY)
        m.addGenConstrNL(z, expr(r["nl"], x))
        e += z
    if ridx == 0:
        m.setObjective(e + inst.obj_const, GRB.MINIMIZE if inst.obj_sense == "min" else GRB.MAXIMIZE); continue
    if r["lb"] == r["ub"]: m.addConstr(e == r["lb"])
    else:
        if math.isfinite(r["lb"]): m.addConstr(e >= r["lb"])
        if math.isfinite(r["ub"]): m.addConstr(e <= r["ub"])
trig, pw = link_detect.detect(inst)
nlinks = 0
if mode in ("moment", "linkmoment"):
    # exact hull of (x, x^2, x^3) on [l,u] (Karlin-Shapley): two rotated cones
    for v_, ps_ in pw.items():
        if ps_ != [2.0, 3.0]: continue
        lo, hi = inst.var_lb[v_], inst.var_ub[v_]
        t2 = m.addVar(lb=lo * lo, ub=hi * hi); t3 = m.addVar(lb=lo ** 3, ub=hi ** 3)
        m.addGenConstrNL(t2, x[v_] ** 2); m.addGenConstrNL(t3, x[v_] ** 3)
        a1 = m.addVar(lb=0, ub=hi - lo); b1 = m.addVar(lb=0); c1 = m.addVar(lb=-GRB.INFINITY)
        m.addConstr(a1 == x[v_] - lo); m.addConstr(b1 == t3 - lo * t2); m.addConstr(c1 == t2 - lo * x[v_])
        m.addQConstr(c1 * c1 <= a1 * b1)
        a2 = m.addVar(lb=0, ub=hi - lo); b2 = m.addVar(lb=0); c2 = m.addVar(lb=-GRB.INFINITY)
        m.addConstr(a2 == hi - x[v_]); m.addConstr(b2 == hi * t2 - t3); m.addConstr(c2 == hi * x[v_] - t2)
        m.addQConstr(c2 * c2 <= a2 * b2)
        if mode == "linkmoment": m.addGenConstrNL(t3, t2 ** 1.5)
        nlinks += 1
if mode in ("linked", "linked2"):
    for v in trig:
        s = m.addVar(lb=-1, ub=1); c = m.addVar(lb=-1, ub=1)
        m.addGenConstrNL(s, nlfunc.sin(x[v])); m.addGenConstrNL(c, nlfunc.cos(x[v])); m.addConstr(s * s + c * c == 1); nlinks += 1
    for v, ps_ in pw.items():
        lo, hi = inst.var_lb[v], inst.var_ub[v]
        ref = link_detect.reference(ps_, rule); tv = {}
        for p in ps_:
            a, b = sorted((lo ** p, hi ** p)); tv[p] = m.addVar(lb=a, ub=b); m.addGenConstrNL(tv[p], x[v] ** p)
        for p in ps_:
            if p != ref: m.addGenConstrNL(tv[p], tv[ref] ** (p / ref)); nlinks += 1
t0 = time.time(); m.optimize()
print(json.dumps({"name": name, "solver": "gurobi", "mode": mode, "links": nlinks, "sense": inst.obj_sense, "status": m.Status,
                  "primal": m.ObjVal if m.SolCount else None, "dual": m.ObjBound, "nodes": m.NodeCount, "time": time.time() - t0}))
