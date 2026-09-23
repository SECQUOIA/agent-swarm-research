"""Root version of the aggregate-burn relaxation B4 (F1 instances): the MINLP in power variables with the
eigen rows at t < T replaced by the cycle burn b_i = sum_{t<T} p_it (0 <= b_i <= (T-1) c, V'b = T - 1).
  k_T = k_1 - a b ;  k_1 = KF sum_{fresh} y_ig + sum_{old} y_ig kappa_g ;  kappa_g = sum_j V_j y_{j,pred g} k_{jT}
  lam p_i = k_{iT} (G p)_i,  V'p = 1,  0 <= p <= c ;  node, type, tie rows.   max lam.
Valid relaxation: every feasible point of the MINLP maps to a feasible point with the same lam_T.
usage: b4root.py name tlim threads"""
import sys, json, numpy as np
import gurobipy as gp
from nucsim import Data

name, tlim, th = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
D = Data(name); N, T, ng = D.N, D.T, D.ntypes
lo = D.KF - D.a * D.c * (T - 1) * D.nages
m = gp.Model(); m.Params.NonConvex = 2; m.Params.TimeLimit = tlim; m.Params.Threads = th; m.Params.OutputFlag = 0
kT = m.addMVar(N, lb=lo, ub=D.KF); k1 = m.addMVar(N, lb=lo, ub=D.KF); b = m.addMVar(N, lb=0, ub=(T - 1) * D.c)
p = m.addMVar(N, lb=0, ub=D.c); lam = m.addVar(lb=0, ub=D.KF * 1.1); s = m.addMVar(N, lb=0)
y = m.addVars(N, ng, vtype=gp.GRB.BINARY); kap = m.addVars(ng, lb=lo, ub=D.KF)
m.addConstr(kT == k1 - D.a * b); m.addConstr(D.V @ b == T - 1)
m.addConstr(D.V @ p == 1); m.addConstr(s == D.G @ p)
for i in range(N):
    m.addConstr(lam * p[i] == kT[i] * s[i])
    m.addConstr(y.sum(i, "*") == 1)
    m.addConstr(k1[i] == gp.quicksum(D.KF * y[i, g] for g in range(ng) if D.fresh[g])
                + gp.quicksum(y[i, g] * kap[g] for g in range(ng) if not D.fresh[g]))
for g in range(ng):
    m.addConstr(gp.quicksum(D.V[i] * y[i, g] for i in range(N)) == 1)
    if not D.fresh[g]:
        m.addConstr(kap[g] == gp.quicksum(D.V[j] * y[j, D.pred[g]] * kT[j] for j in range(N)))
for (i, j) in D.ties:
    for g in range(ng): m.addConstr(y[i, g] == y[j, g])
m.setObjective(lam, gp.GRB.MAXIMIZE); m.optimize()
print(json.dumps(dict(name=name, status=m.Status, time=m.Runtime, bound=m.ObjBound, value=m.ObjVal if m.SolCount else None)))
