"""Probe D: what do the disabled nonlinear cut families add in SCIP 10?
Root node only (objective limit = MINLPLib primal), settings: default; quadratic intersection cuts
(with monoidal strengthening, SCIP default when enabled); edge-concave cuts; flower cuts on
continuous products. Gap closed is measured against the default root bound."""
import sys, json, pandas as pd
from multiprocessing import Pool
from common import solve

SET = {
    'dflt': {},
    'ic': {'nlhdlr/quadratic/useintersectioncuts': True},
    'ecc': {'separating/eccuts/freq': 0},
    'flowerprod': {'separating/flower/scanproduct': True},
}

def job(a):
    name, U, sense, s, mode = a
    tol = 1e-6 * max(1.0, abs(U))
    p = dict(SET[s])
    p.update({'limits/nodes': 1, 'limits/time': 120} if mode == 'root' else {'limits/time': 300})
    try:
        _, o = solve(name, p, objlimit=U + tol if sense == 'min' else U - tol)
    except Exception as e:
        o = dict(name=name, status='error:' + str(e)[:80])
    o.update(setting=s, mode=mode)
    print(json.dumps(o), flush=True)
    return o

if __name__ == '__main__':
    A = pd.read_csv('selA.csv'); B = pd.read_csv('selB.csv')
    jobs = [(r.name, r.primalbound, 'min' if r.objsense == 'min' else 'max', s, 'root') for r in A.itertuples() for s in SET]
    jobs += [(r.name, r.primalbound, 'min' if r.objsense == 'min' else 'max', s, 'full') for r in B.itertuples() for s in SET if s != 'dflt']
    with Pool(int(sys.argv[1]), maxtasksperchild=1) as p:
        res = p.map(job, jobs, chunksize=1)
    pd.DataFrame(res).to_csv('probeD.csv', index=False)
