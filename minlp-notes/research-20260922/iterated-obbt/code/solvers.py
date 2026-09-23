"""Gurobi 13 and SCIP 10 runs on a QCQP with an optional tightened box and start solution.

All returned objective values (primal, dual, root_dual) are in minimization form (sense * value).
"""
import os, math, time
import numpy as np

MEMGB = 2.0


def gurobi_run(P, env, lb=None, ub=None, time_limit=600.0, seed=0, params=None, start=None,
               want_x=False):
    import gurobipy as gp
    from gurobipy import GRB
    t0 = time.time()
    lb = P.lb if lb is None else np.maximum(lb, P.lb)
    ub = P.ub if ub is None else np.minimum(ub, P.ub)
    m, xs = P.gurobi_model(env, lb, ub)
    m.Params.OutputFlag = 0
    m.Params.Threads = 1
    m.Params.NonConvex = 2
    m.Params.Seed = seed
    m.Params.MemLimit = MEMGB
    for k, v in (params or {}).items():
        m.setParam(k, v)
    m.Params.TimeLimit = max(time_limit - (time.time() - t0), 0.01)
    if start is not None:
        for v, s in zip(xs, start):
            v.Start = s
    root = {'bnd': None}

    def cb(model, where):
        if where == GRB.Callback.MIP:
            if model.cbGet(GRB.Callback.MIP_NODCNT) == 0:
                root['bnd'] = model.cbGet(GRB.Callback.MIP_OBJBND)
        elif where == GRB.Callback.MIPNODE:
            if model.cbGet(GRB.Callback.MIPNODE_NODCNT) == 0:
                root['bnd'] = model.cbGet(GRB.Callback.MIPNODE_OBJBND)

    m.optimize(cb)
    st = m.Status
    names = {GRB.OPTIMAL: 'optimal', GRB.TIME_LIMIT: 'timelimit', GRB.INFEASIBLE: 'infeasible',
             GRB.NODE_LIMIT: 'nodelimit', GRB.MEM_LIMIT: 'memlimit', GRB.INF_OR_UNBD: 'inf_or_unbd',
             GRB.NUMERIC: 'numeric', GRB.INTERRUPTED: 'interrupted', GRB.SOLUTION_LIMIT: 'sollimit',
             GRB.CUTOFF: 'cutoff'}
    out = dict(status=names.get(st, str(st)), time=time.time() - t0, nodes=m.NodeCount)
    s = P.sense
    out['primal'] = s * m.ObjVal if m.SolCount > 0 else None
    try:
        out['dual'] = s * m.ObjBound
    except Exception:
        out['dual'] = None
    rb = root['bnd']
    if rb is None and out['nodes'] <= 1:
        rb = out['dual'] if out['dual'] is None else out['dual'] * s
    out['root_dual'] = None if rb is None or abs(rb) >= 1e99 else s * rb
    if want_x and m.SolCount > 0:
        out['x'] = [v.X for v in xs]
    m.dispose()
    return out


def scip_run(P, lb=None, ub=None, time_limit=600.0, seed=0, params=None, start=None, objlim=None,
             want_x=False):
    from pyscipopt import Model
    t0 = time.time()
    m = Model()
    m.hideOutput()
    m.readProblem(os.path.join(os.path.expanduser('~/.cache/minlplib/minlplib/osil'), P.name + '.osil'))
    m.setParam('limits/memory', MEMGB * 1000)
    m.setParam('randomization/randomseedshift', seed)
    for k, v in (params or {}).items():
        m.setParam(k, v)
    byname = {v.name: v for v in m.getVars()}
    xs = [byname[nm] for nm in P.names]
    if lb is not None:
        for v, l, u, l0, u0 in zip(xs, lb, ub, P.lb, P.ub):
            if l > l0:
                m.chgVarLb(v, l)
            if u < u0:
                m.chgVarUb(v, u)
    s = P.sense
    if objlim is not None:   # objlim in minimization form
        m.setObjlimit(s * objlim)
    if start is not None:
        sol = m.createSol()
        for v, val in zip(xs, start):
            m.setSolVal(sol, v, val)
        # the objective variable of OSiL is an original variable, so the start is complete
        try:
            m.addSol(sol, free=True)
        except Exception:
            pass
    m.setParam('limits/time', max(time_limit - (time.time() - t0), 0.01))
    m.optimize()
    st = m.getStatus()
    out = dict(status=st, time=time.time() - t0, nodes=m.getNNodes())
    out['primal'] = s * m.getPrimalbound() if m.getNSols() > 0 else None
    d = m.getDualbound()
    out['dual'] = s * d if abs(d) < 1e19 else None
    try:
        r = m.getDualboundRoot()
        out['root_dual'] = s * r if abs(r) < 1e19 else None
    except Exception:
        out['root_dual'] = None
    if want_x and m.getNSols() > 0:
        b = m.getBestSol()
        out['x'] = [m.getSolVal(b, v) for v in xs]
    m.freeProb()
    return out
