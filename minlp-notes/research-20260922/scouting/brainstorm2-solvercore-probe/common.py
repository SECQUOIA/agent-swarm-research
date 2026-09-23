"""Shared helpers for the solver-core feasibility probes (SCIP 10 via PySCIPOpt)."""
import os, json, time, math
from pyscipopt import Model

OSIL = os.path.expanduser('~/.cache/minlplib/minlplib/osil')


def load(name, params=None, bounds=None, quiet=True):
    m = Model()
    if quiet:
        m.hideOutput()
    m.readProblem(os.path.join(OSIL, name + '.osil'))
    m.setParam('limits/memory', 6000)
    for k, v in (params or {}).items():
        m.setParam(k, v)
    if bounds:
        byname = {v.name: v for v in m.getVars()}
        for vn, (lb, ub) in bounds.items():
            v = byname[vn]
            if lb is not None and lb > v.getLbOriginal():
                m.chgVarLb(v, lb)
            if ub is not None and ub < v.getUbOriginal():
                m.chgVarUb(v, ub)
    return m


def solve(name, params=None, bounds=None, objlimit=None):
    m = load(name, params, bounds)
    if objlimit is not None:
        m.setObjlimit(objlimit)
    t = time.time()
    m.optimize()
    out = dict(name=name, status=m.getStatus(), time=time.time() - t,
               nodes=m.getNNodes(), dual=m.getDualbound(),
               primal=m.getPrimalbound() if m.getNSols() > 0 else None,
               sense=m.getObjectiveSense())
    return m, out


def global_bounds(m):
    """Global bounds of original variables after solving, read from their transformed copies.
    Only variables whose transformed copy is active (loose/column) or fixed are used."""
    res = {}
    for v in m.getVars():  # original vars
        try:
            tv = m.getTransformedVar(v)
        except Exception:
            continue
        st = tv.getStatus()
        if st in ('LOOSE', 'COLUMN'):
            res[v.name] = (tv.getLbGlobal(), tv.getUbGlobal())
        elif st == 'FIXED':
            x = tv.getLbGlobal()
            res[v.name] = (x, x)
    return res
