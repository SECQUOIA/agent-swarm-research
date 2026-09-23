"""Probe A: how much root gap does iterated OBBT (to a numerical fixed point) close in SCIP 10?

Per instance, with the MINLPLib primal value U given as objective limit in every run:
  off   : root node only, OBBT disabled
  r1..rK: root node only, OBBT enabled; round k starts from the original-variable global bounds
          left by round k-1. Two OBBT modes: 'dflt' (SCIP defaults) and 'full'
          (no LP iteration limit, all variables, not only nonconvex ones).
Stops when the total relative width reduction of a round is below 1e-3 or after 8 rounds.
"""
import sys, json, math, pandas as pd
from multiprocessing import Pool
from common import solve, global_bounds

ROOT = {'limits/nodes': 1, 'limits/time': 60}
MODES = {
    'dflt': {},
    'full': {'propagating/obbt/itlimitfactor': 0.0, 'propagating/obbt/itlimitfactorbilin': 0.0,
             'propagating/obbt/onlynonconvexvars': False, 'propagating/obbt/minitlimit': 10**7},
}

def width_gain(b0, b1):
    """Sum over variables with finite old width of relative width reduction; plus count of newly finite bounds."""
    s, newfin = 0.0, 0
    for k, (l1, u1) in b1.items():
        l0, u0 = b0.get(k, (-1e20, 1e20))
        if l0 > -1e19 and u0 < 1e19:
            w0 = u0 - l0
            if w0 > 1e-9:
                s += max(0.0, (w0 - (u1 - l1)) / w0)
        else:
            newfin += (l0 <= -1e19 and l1 > -1e19) + (u0 >= 1e19 and u1 < 1e19)
    return s, newfin

def job(args):
    name, U, sense = args
    tol = 1e-6 * max(1.0, abs(U))
    objlim = U + tol if sense == 'min' else U - tol
    out = dict(name=name, U=U, sense=sense)
    try:
        _, o = solve(name, dict(ROOT, **{'propagating/obbt/freq': -1}), objlimit=objlim)
        out['off'] = o['dual']; out['off_t'] = o['time']; out['off_status'] = o['status']
        for mode, extra in MODES.items():
            b = None; hist = []
            for k in range(6):
                m, o = solve(name, dict(ROOT, **extra), bounds=b, objlimit=objlim)
                nb = global_bounds(m) if o['status'] not in ('infeasible',) else b
                g, nf = width_gain(b or {}, nb) if b is not None else (float('nan'), 0)
                hist.append(dict(dual=o['dual'], t=o['time'], st=o['status'], wg=g, nf=nf))
                if o['status'] in ('optimal', 'infeasible'):
                    break
                if b is not None and g < 1e-3 and nf == 0:
                    break
                b = nb
                del m
            out[mode] = hist
            if mode == 'full':
                out['fp_bounds'] = b
    except Exception as e:
        out['error'] = str(e)[:200]
    print(json.dumps({k: v for k, v in out.items() if k != 'fp_bounds'}), flush=True)
    return out

if __name__ == '__main__':
    sel = pd.read_csv(sys.argv[1])
    jobs = [(r.name, r.primalbound, 'min' if r.objsense == 'min' else 'max') for r in sel.itertuples()]
    with Pool(17, maxtasksperchild=1) as p:
        res = p.map(job, jobs, chunksize=1)
    json.dump(res, open('probeA.json', 'w'))
