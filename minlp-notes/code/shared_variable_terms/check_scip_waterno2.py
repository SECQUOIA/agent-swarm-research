"""SCIP 10 reports 'optimal' 42.343 on waterno2_02 (own OSiL reader), Gurobi 13 and MINLPLib give 39.571.
Is Gurobi's point feasible for SCIP?  Solve with Gurobi, hand the point to SCIP's checkSol."""
import math, os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "univariate_envelopes"))
import gurobipy as gp
from gurobipy import GRB
import pyscipopt as ps
from uenv.osil import read_osil

name = sys.argv[1]
path = os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil")
inst = read_osil(path)
assert all(r["nl"] is None or r["nl"][0] == "power" or True for r in inst.rows)
m = gp.Model(); m.Params.OutputFlag = 0; m.Params.MIPGap = 1e-6; m.Params.FeasibilityTol = 1e-9; m.Params.IntFeasTol = 1e-9; m.Params.TimeLimit = 300
x = [m.addVar(lb=(-GRB.INFINITY if math.isinf(l) else l), ub=(GRB.INFINITY if math.isinf(u) else u),
              vtype={"B": GRB.BINARY, "I": GRB.INTEGER}.get(t, GRB.CONTINUOUS)) for l, u, t in zip(inst.var_lb, inst.var_ub, inst.var_type)]
def ex(t):
    if t[0] == "num": return t[1]
    if t[0] == "var": return x[t[1]]
    k = [ex(c) for c in t[1:]]
    if t[0] == "sum": return sum(k[1:], k[0])
    if t[0] == "negate": return -1.0 * k[0]
    if t[0] == "times":
        o = k[0]
        for c in k[1:]: o = o * c
        return o
    if t[0] == "divide": return k[0] / k[1]
    if t[0] == "power": return k[0] ** k[1]
    if t[0] == "square": return k[0] ** 2
    raise NotImplementedError(t[0])
for ridx, r in enumerate(inst.rows):
    e = gp.QuadExpr()
    for i, c in r["lin"].items(): e += c * x[i]
    for i, j, c in r["quad"]: e += c * x[i] * x[j]
    if r["nl"] is not None:
        z = m.addVar(lb=-GRB.INFINITY); m.addGenConstrNL(z, ex(r["nl"])); e += z
    if ridx == 0: m.setObjective(e + inst.obj_const); continue
    if r["lb"] == r["ub"]: m.addConstr(e == r["lb"])
    else:
        if math.isfinite(r["lb"]): m.addConstr(e >= r["lb"])
        if math.isfinite(r["ub"]): m.addConstr(e <= r["ub"])
m.optimize()
print("gurobi", m.Status, m.ObjVal, m.ObjBound, "max constraint violation reported:", m.ConstrVio, m.ConstrResidual if hasattr(m, "ConstrResidual") else "")
s = ps.Model(); s.hideOutput(); s.readProblem(path)
sv = s.getVars()
assert len(sv) == len(x)
sol = s.createSol()
for v, g in zip(sv, x): s.setSolVal(sol, v, g.X)
print("SCIP checkSol (original problem, default tolerances):", s.checkSol(sol, printreason=True, original=True), "objective of the point in SCIP:", s.getSolObjVal(sol))
