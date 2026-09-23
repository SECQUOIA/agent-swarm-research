"""Feasibility MIQCP: is there an E-CG cut violated by at least `viol` at the fixed point z?
Variables (v0 >= 0, v), integers A_i, B_ij, G with
  A_i >= p_i = v_i^2 + 2 v_i v0,  B_ij >= q_ij = 2 v_i v_j,  G <= v0^2 <= G + 1 - eps,
  F := G + sum x_i A_i + sum X_ij B_ij <= -viol.
Valid strengthening (from F = q_M + sum w (ceil - value) - frac(v0^2)):
  q_M(v) <= 1 - viol, and for every weight w_k > 0: (ceil_k - value_k) <= (1 - viol)/w_k.
Gurobi (NonConvex=2) either finds a point (then verify exactly) or proves infeasibility
(numerical certificate only)."""
import numpy as np
import gurobipy as gp
from gurobipy import GRB
from bh import pairs, moment_matrix


def ecg_feasibility(n, z, viol, timelimit=600, eps=1e-3, threads=0):
    P = pairs(n)
    M = moment_matrix(n, z)
    Minv = np.linalg.inv(M)
    r = [float(np.sqrt(Minv[k, k] * (1 - viol))) * (1 + 1e-6) for k in range(n + 1)]
    m = gp.Model()
    m.Params.OutputFlag = 0
    m.Params.NonConvex = 2
    m.Params.FeasibilityTol = 1e-9
    m.Params.IntFeasTol = 1e-9
    m.Params.TimeLimit = timelimit
    if threads:
        m.Params.Threads = threads
    v0 = m.addVar(lb=0, ub=r[0])
    v = m.addVars(n, lb=[-r[i + 1] for i in range(n)], ub=[r[i + 1] for i in range(n)])
    allv = [v0] + [v[i] for i in range(n)]
    m.addQConstr(gp.quicksum(float(M[k, l]) * allv[k] * allv[l] for k in range(n + 1) for l in range(n + 1)) <= 1 - viol)
    big = 4 * max(r) ** 2 + 2
    A = m.addVars(n, lb=-big, ub=big, vtype=GRB.INTEGER)
    B = m.addVars(len(P), lb=-big, ub=big, vtype=GRB.INTEGER)
    G = m.addVar(lb=0, ub=r[0] ** 2, vtype=GRB.INTEGER)
    x = z[:n]
    X = z[n:]
    for i in range(n):
        m.addQConstr(A[i] >= v[i] * v[i] + 2 * v[i] * v0)
        if x[i] > 0:
            m.addQConstr(A[i] - v[i] * v[i] - 2 * v[i] * v0 <= (1 - viol) / x[i])
    for k, (i, j) in enumerate(P):
        m.addQConstr(B[k] >= 2 * v[i] * v[j])
        if X[k] > 0:
            m.addQConstr(B[k] - 2 * v[i] * v[j] <= (1 - viol) / X[k])
    m.addQConstr(G <= v0 * v0)
    m.addQConstr(v0 * v0 <= G + 1 - eps)
    m.addConstr(G + gp.quicksum(float(x[i]) * A[i] for i in range(n)) +
                gp.quicksum(float(X[k]) * B[k] for k in range(len(P))) <= -viol)
    m.setObjective(0)
    m.optimize()
    st = {GRB.INFEASIBLE: "infeasible", GRB.OPTIMAL: "feasible", GRB.TIME_LIMIT: "timelimit"}.get(m.Status, m.Status)
    sol = None
    if m.SolCount:
        sol = (v0.X, [v[i].X for i in range(n)])
    return st, sol, m.Runtime
