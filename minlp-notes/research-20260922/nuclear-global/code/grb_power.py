"""Gurobi on the power-variable reformulation (F1 instances), optionally with a fixed pattern.

Variables p_it in [0, c], k_it in [klo_it, KF], lam_t >= 0, s_it = (G p_t)_i, y_ig binary, kappa_g.
  k_{i,t+1} = k_it - a p_it ;  V'p_t = 1 ;  lam_t p_it = k_it s_it  (bilinear, the only nonconvexity
  besides the reload products) ;  k_i1 = KF sum_{fresh} y_ig + sum_{old} y_ig kappa_g ;
  kappa_g = sum_j V_j y_{j,pred g} k_{jT} ;  node, type and tie rows as in the OSiL file.
Valid bounds used (proofs in assessment.md): k_it <= KF (K); k_it >= KF - a c (age (T-1) + t) for fuel of
age `age` (each step burns at most a c); lam_T <= certified bound from nuclear_cw_bounds.json.
usage: grb_power.py name tlim [pattern-json|none] [threads]
"""
import sys, json, os, numpy as np
import gurobipy as gp
from nucsim import Data

name, tlim = sys.argv[1], float(sys.argv[2])
pat = None if len(sys.argv) < 4 or sys.argv[3] == "none" else json.loads(sys.argv[3])
threads = int(sys.argv[4]) if len(sys.argv) > 4 else 1
D = Data(name); N, T, a, c, KF = D.N, D.T, D.a, D.c, D.KF
ng = D.ntypes; maxage = D.nages - 1
B = {r["name"]: r for r in json.load(open(os.path.join(os.path.dirname(__file__), "../../benchmark-observations/nuclear_cw_bounds.json")))}[name]
m = gp.Model(); m.Params.OutputFlag = 1; m.Params.TimeLimit = tlim; m.Params.Threads = threads; m.Params.NonConvex = 2
p = m.addVars(N, T, lb=0, ub=c, name="p")
klo = lambda t: KF - a * c * (maxage * (T - 1) + t)
k = m.addVars(N, T, lb={(i, t): klo(t) for i in range(N) for t in range(T)}, ub=KF, name="k")
lam = m.addVars(T, lb=0, ub=B["best_bound"] * (1 + 1e-9), name="lam")
s = m.addVars(N, T, lb=0, name="s")
y = m.addVars(N, ng, vtype=gp.GRB.BINARY, name="y")
kap = m.addVars(ng, lb=klo(0), ub=KF, name="kap")
for t in range(T):
    m.addConstr(gp.quicksum(D.V[i] * p[i, t] for i in range(N)) == 1)
    for i in range(N):
        m.addConstr(s[i, t] == gp.quicksum(D.G[i, j] * p[j, t] for j in range(N) if D.G[i, j]))
        m.addConstr(lam[t] * p[i, t] == k[i, t] * s[i, t])
        if t < T - 1: m.addConstr(k[i, t + 1] == k[i, t] - a * p[i, t])
for i in range(N):
    m.addConstr(y.sum(i, "*") == 1)
    m.addConstr(k[i, 0] == gp.quicksum(KF * y[i, g] for g in range(ng) if D.fresh[g])
                + gp.quicksum(y[i, g] * kap[g] for g in range(ng) if not D.fresh[g]))
for g in range(ng):
    m.addConstr(gp.quicksum(D.V[i] * y[i, g] for i in range(N)) == 1)
    if not D.fresh[g]:
        m.addConstr(kap[g] == gp.quicksum(D.V[j] * y[j, D.pred[g]] * k[j, T - 1] for j in range(N)))
for (i, j) in D.ties:
    for g in range(ng): m.addConstr(y[i, g] == y[j, g])
if pat is not None:
    for i in range(N):
        for g in range(ng): y[i, g].LB = y[i, g].UB = 1.0 if pat[i] == g else 0.0
m.setObjective(lam[T - 1], gp.GRB.MAXIMIZE)
m.optimize()
print(json.dumps(dict(name=name, fixed=pat is not None, status=m.Status, time=m.Runtime, primal=m.ObjVal if m.SolCount else None,
                      dual=m.ObjBound, nodes=m.NodeCount)))
