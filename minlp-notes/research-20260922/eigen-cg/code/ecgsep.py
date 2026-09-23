"""E-CG separation at a fixed point z: minimize the E-CG left-hand side over (v0, v).

min  sum_{i<j} B_ij X_ij + sum_i A_i x_i + G
s.t. B_ij >= 2 v_i v_j, A_i >= v_i^2 + 2 v_i v0, G <= v0^2 <= G + 1 - eps,  B, A, G integer, |v| <= V.
Because z >= 0, at an optimum B, A are the ceilings and G is the floor, so the optimum is
min over (v0, v) in the box of the E-CG left-hand side at z.  Nonconvex MIQCP (Gurobi).
"""
import numpy as np
import gurobipy as gp
from gurobipy import GRB
from bh import pairs, moment_matrix


def separate_ecg(n, z, V=6.0, timelimit=60, pool=10, threads=0, eps=1e-4):
    m = gp.Model()
    m.Params.OutputFlag = 0
    m.Params.NonConvex = 2
    m.Params.TimeLimit = timelimit
    m.Params.PoolSolutions = pool
    if threads:
        m.Params.Threads = threads
    # a violation needs q_M(v) = (v0,v)^T M (v0,v) < 1; impose it and the implied box
    M = moment_matrix(n, z)
    Minv = np.linalg.inv(M)
    r = [min(V, float(np.sqrt(Minv[k, k])) * (1 + 1e-6)) for k in range(n + 1)]
    v0 = m.addVar(lb=0.0, ub=r[0])  # (v0,v) and -(v0,v) give the same cut
    v = m.addVars(n, lb=[-r[k + 1] for k in range(n)], ub=[r[k + 1] for k in range(n)])
    allv = [v0] + [v[i] for i in range(n)]
    m.addQConstr(gp.quicksum(float(M[k, l]) * allv[k] * allv[l]
                             for k in range(n + 1) for l in range(n + 1)) <= 1)
    P = pairs(n)
    B = m.addVars(len(P), lb=-4 * V * V, ub=4 * V * V, vtype=GRB.INTEGER)
    A = m.addVars(n, lb=-4 * V * V, ub=4 * V * V, vtype=GRB.INTEGER)
    G = m.addVar(lb=0, ub=V * V, vtype=GRB.INTEGER)
    for k, (i, j) in enumerate(P):
        m.addQConstr(B[k] >= 2 * v[i] * v[j])
    for i in range(n):
        m.addQConstr(A[i] >= v[i] * v[i] + 2 * v[i] * v0)
    m.addQConstr(G <= v0 * v0)
    m.addQConstr(v0 * v0 <= G + 1 - eps)  # G = floor(v0^2)
    obj = gp.quicksum(float(z[n + k]) * B[k] for k in range(len(P)) if z[n + k] != 0)
    obj += gp.quicksum(float(z[i]) * A[i] for i in range(n) if z[i] != 0) + G
    m.setObjective(obj, GRB.MINIMIZE)
    m.Params.BestObjStop = -1e-6
    m.optimize()
    sols = []
    for s in range(m.SolCount):
        m.Params.SolutionNumber = s
        sols.append((m.PoolObjVal, v0.Xn, [v[i].Xn for i in range(n)],
                     [int(round(A[i].Xn)) for i in range(n)] + [int(round(B[k].Xn)) for k in range(len(P))],
                     int(round(G.Xn))))
    return m.ObjVal if m.SolCount else None, m.ObjBound, sols
