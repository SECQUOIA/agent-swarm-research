"""Probe A2: full solves (300 s, objective limit = MINLPLib primal) from the original box versus
from the box left by iterated OBBT (probe A, 'full' mode), two seeds each."""
import json, pandas as pd
from multiprocessing import Pool
from common import solve

def job(a):
    name, U, sense, arm, seed, b = a
    tol = 1e-6 * max(1.0, abs(U))
    p = {'limits/time': 300, 'randomization/randomseedshift': seed, 'randomization/permutationseed': seed}
    try:
        _, o = solve(name, p, bounds=b if arm == 'fp' else None, objlimit=U + tol if sense == 'min' else U - tol)
    except Exception as e:
        o = dict(name=name, status='error:' + str(e)[:80])
    o.update(arm=arm, seed=seed)
    print(json.dumps(o), flush=True)
    return o

if __name__ == '__main__':
    A = {r['name']: r for r in json.load(open('probeA.json'))}
    S = pd.read_csv('probeA_summary.csv')
    names = list(S[S.extra > 0.1].name)
    jobs = [(n, A[n]['U'], A[n]['sense'], arm, s, A[n].get('fp_bounds'))
            for n in names for arm in ('dflt', 'fp') for s in (0, 1)]
    with Pool(32, maxtasksperchild=1) as p:
        res = p.map(job, jobs, chunksize=1)
    pd.DataFrame(res).to_csv('probeA2.csv', index=False)
