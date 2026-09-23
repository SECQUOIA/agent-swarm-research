"""Reviewer's own root B4 (aggregate-burn relaxation) model, built from the reviewer's parser.

Relaxation of the power model over all F1 patterns: eigen rows only at t = T; the steps t < T are replaced by
b = sum_{t<T} p_t with k_T = k_1 - a b, V'b = T - 1, 0 <= b <= (T-1) c. Reload, node, type and tie rows kept.
Variable boxes: k_1, k_T, kappa in [KF - (Amax+1) a c (T-1), KF] (valid by (K+)), lam in [0, 2].
Same relaxation as the author's b4root.py; written independently. Gurobi values are floating point.
usage: b4_root_rv.py name timelimit threads [pattern-json|none] [aux]"""
import sys, json
import numpy as np
import gurobipy as gp
from rv_common import D

nm, tl, th = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
pat = json.loads(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4] != "none" else None   # optional fixed pattern (leaf B4)
aux = len(sys.argv) > 5 and sys.argv[5] == "aux"   # model (G p)_i by auxiliary variables s_i
tag = nm + ("_leaf" if pat else "") + ("_aux" if aux else "")
d = D(nm); N, T, ng = d.N, d.T, d.ng
lo = d.KF - d.a * d.c * (T - 1) * (d.maxage + 1)
m = gp.Model()
m.Params.NonConvex = 2; m.Params.TimeLimit = tl; m.Params.Threads = th; m.Params.OutputFlag = 1
m.Params.LogFile = f"../../runs/review/b4_{tag}.log"; m.Params.LogToConsole = 0
y = {(i, g): m.addVar(vtype=gp.GRB.BINARY) for i in range(N) for g in range(ng)}
kap = {g: m.addVar(lb=lo, ub=d.KF) for g in range(ng) if not d.fresh[g]}
k1 = [m.addVar(lb=lo, ub=d.KF) for i in range(N)]
kT = [m.addVar(lb=lo, ub=d.KF) for i in range(N)]
b = [m.addVar(lb=0, ub=(T - 1) * d.c) for i in range(N)]
p = [m.addVar(lb=0, ub=d.c) for i in range(N)]
lam = m.addVar(lb=0, ub=2)
for i in range(N):
    m.addConstr(gp.quicksum(y[i, g] for g in range(ng)) == 1)
    m.addConstr(k1[i] == gp.quicksum(d.KF * y[i, g] if d.fresh[g] else y[i, g] * kap[g] for g in range(ng)))
    m.addConstr(kT[i] == k1[i] - d.a * b[i])
    if aux:
        si = m.addVar(lb=0, ub=float(d.G[i].max()) * d.c * N)
        m.addConstr(si == gp.quicksum(float(d.G[i, j]) * p[j] for j in range(N) if d.G[i, j] != 0))
        m.addConstr(lam * p[i] == kT[i] * si)
    else:
        m.addConstr(lam * p[i] == gp.quicksum(float(d.G[i, j]) * kT[i] * p[j] for j in range(N) if d.G[i, j] != 0))
for g in range(ng):
    m.addConstr(gp.quicksum(d.V[i] * y[i, g] for i in range(N)) == 1)
    if not d.fresh[g]:
        m.addConstr(kap[g] == gp.quicksum(d.V[j] * y[j, d.pred[g]] * kT[j] for j in range(N)))
for (i, j) in d.S.ties:
    for g in range(ng): m.addConstr(y[i, g] == y[j, g])
m.addConstr(gp.quicksum(d.V[i] * b[i] for i in range(N)) == T - 1)
m.addConstr(gp.quicksum(d.V[i] * p[i] for i in range(N)) == 1)
if pat:
    for i in range(N):
        for g in range(ng): y[i, g].LB = y[i, g].UB = int(pat[i] == g)
    out0 = dict(pattern=pat)
m.setObjective(lam, gp.GRB.MAXIMIZE)
m.optimize()
out = dict(name=nm, status=m.Status, time=m.Runtime, bound=m.ObjBound, value=m.ObjVal if m.SolCount else None)
if m.SolCount:
    typ = [max(range(ng), key=lambda g: y[i, g].X) for i in range(N)]
    out["typ"] = typ; out["p"] = [v.X for v in p]; out["kT"] = [v.X for v in kT]
print(json.dumps(out))
json.dump(out, open(f"../../runs/review/b4_{tag}.json", "w"))
