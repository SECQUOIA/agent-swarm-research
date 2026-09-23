"""SCIP 10 (PySCIPOpt) and Gurobi 13 (general nonlinear constraints) on the same models.

Model: x in the input box; per neuron z = w.y_prev + b and y = sigma(z) with the
root interval bounds on z and y; objective min sense * (w_out . y + b_out).
Native expressions: tanh(z) = 2/(1+exp(-2z)) - 1 in SCIP (no tanh operator) and
nlfunc.tanh in Gurobi; sigmoid = 1/(1+exp(-z)) (SCIP) / nlfunc.logistic
(Gurobi); SiLU = z/(1+exp(-z)) (SCIP) / z * logistic(z) (Gurobi); sin native.
GELU needs erf, which neither interface provides, so GELU networks are skipped.
Time limits: SCIP uses its CPU clock; Gurobi's TimeLimit is wall-clock.
"""
import time

import numpy as np

from relax import ibp

SUPPORTED = {"tanh", "sigmoid", "silu", "sin"}


def solve_scip(net, sense, time_limit=600.0, gap=1e-4, absgap=1e-6):
    import pyscipopt as ps
    B = ibp(net, net.lo, net.hi)
    m = ps.Model()
    m.hideOutput()
    m.setParam("timing/clocktype", 1)  # CPU time, as in the Python B&B
    m.setParam("limits/time", time_limit)
    m.setParam("limits/gap", gap)
    m.setParam("limits/absgap", absgap)
    m.setParam("randomization/randomseedshift", 0)
    prev = [m.addVar(lb=float(net.lo[i]), ub=float(net.hi[i]), name="x%d" % i) for i in range(net.d)]
    for l, (W, b) in enumerate(zip(net.Ws, net.bs)):
        cur = []
        for j in range(W.shape[0]):
            z = m.addVar(lb=float(B.Lz[l][j]), ub=float(B.Uz[l][j]), name="z%d_%d" % (l, j))
            y = m.addVar(lb=float(B.ly[l][j]), ub=float(B.uy[l][j]), name="y%d_%d" % (l, j))
            m.addCons(ps.quicksum(float(W[j, i]) * prev[i] for i in range(len(prev))) + float(b[j]) == z)
            a = net.actname
            if a == "tanh":
                e = 2.0 / (1.0 + ps.exp(-2.0 * z)) - 1.0
            elif a == "sigmoid":
                e = 1.0 / (1.0 + ps.exp(-z))
            elif a == "silu":
                e = z / (1.0 + ps.exp(-z))
            elif a == "sin":
                e = ps.sin(z)
            else:
                raise ValueError(a)
            m.addCons(y == e)
            cur.append(y)
        prev = cur
    obj = m.addVar(lb=None, ub=None, name="obj")
    m.addCons(obj == sense * (ps.quicksum(float(net.w_out[j]) * prev[j] for j in range(len(prev))) + net.b_out))
    m.setObjective(obj, "minimize")
    t0, c0 = time.time(), time.process_time()
    m.optimize()
    el, cpu = time.time() - t0, time.process_time() - c0
    st = m.getStatus()
    pb = m.getPrimalbound() if m.getNSols() > 0 else float("inf")
    db = m.getDualbound()
    xs = None
    if m.getNSols() > 0:
        sol = m.getBestSol()
        xs = [m.getSolVal(sol, v) for v in m.getVars() if v.name.startswith("x")][:net.d]
    return dict(solver="scip", status=st, time=cpu, wall_time=el, solver_time=m.getSolvingTime(), UB=float(pb), LB=float(db), nodes=int(m.getNNodes()), x=xs)


def solve_gurobi(net, sense, time_limit=600.0, gap=1e-4, absgap=1e-6):
    import gurobipy as gp
    from gurobipy import GRB, nlfunc
    B = ibp(net, net.lo, net.hi)
    env = gp.Env(empty=True)
    env.setParam("OutputFlag", 0)
    env.start()
    m = gp.Model(env=env)
    m.Params.TimeLimit = time_limit
    m.Params.MIPGap = gap
    m.Params.MIPGapAbs = absgap
    m.Params.Threads = 1
    m.Params.Seed = 0
    prev = [m.addVar(lb=float(net.lo[i]), ub=float(net.hi[i]), name="x%d" % i) for i in range(net.d)]
    xs_vars = list(prev)
    for l, (W, b) in enumerate(zip(net.Ws, net.bs)):
        cur = []
        for j in range(W.shape[0]):
            z = m.addVar(lb=float(B.Lz[l][j]), ub=float(B.Uz[l][j]))
            y = m.addVar(lb=float(B.ly[l][j]), ub=float(B.uy[l][j]))
            m.addConstr(gp.quicksum(float(W[j, i]) * prev[i] for i in range(len(prev))) + float(b[j]) == z)
            a = net.actname
            if a == "tanh":
                e = nlfunc.tanh(z)
            elif a == "sigmoid":
                e = nlfunc.logistic(z)
            elif a == "silu":
                e = z * nlfunc.logistic(z)
            elif a == "sin":
                e = nlfunc.sin(z)
            else:
                raise ValueError(a)
            m.addGenConstrNL(y, e)
            cur.append(y)
        prev = cur
    m.setObjective(sense * (gp.quicksum(float(net.w_out[j]) * prev[j] for j in range(len(prev))) + net.b_out),
                   GRB.MINIMIZE)
    t0, c0 = time.time(), time.process_time()
    m.optimize()
    el, cpu = time.time() - t0, time.process_time() - c0
    has = m.SolCount > 0
    res = dict(solver="gurobi", status=int(m.Status), time=cpu, wall_time=el, solver_time=m.Runtime, UB=float(m.ObjVal) if has else float("inf"),
               LB=float(m.ObjBound), nodes=int(m.NodeCount), x=[v.X for v in xs_vars] if has else None)
    m.dispose()
    env.dispose()
    return res
