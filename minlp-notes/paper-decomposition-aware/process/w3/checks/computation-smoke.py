"""Smoke test of the new run_all task types on single instances (no files written to results/)."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import os, sys, json, time
for v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[v] = '1'
from concurrent.futures import ProcessPoolExecutor
sys.path.insert(0, (_PUBLIC_REPO + '/paper-decomposition-aware/experiments'))

def run(item):
    import run_all
    kind, spec = item
    t0 = time.perf_counter()
    rec = run_all.TASKS[kind](spec)
    rec.pop('stages', None)
    return kind, round(time.perf_counter() - t0, 1), json.dumps(rec, default=str)[:1500]

if __name__ == '__main__':
    items = [
        ('localized', dict(exp='S1', kind='band2', n=16, n_int=2, seed=7029, max_stages=60)),
        ('random_growth', dict(exp='E6', kind='band2', n=24, seed=24501, q_list=[10, 20, 30, 40, 50])),
        ('grid', dict(exp='E3', kind='path', n=16, kappa_target=4, seed=101, grid_mode='geometric', pruning=True, theta=None, method='geom_theorem', max_stages=11, time_limit=60, max_table_states=200000)),
        ('exact', dict(exp='E4', family='random', kind='band2', n=6, n_int=2, seed=4012, time_limit=30)),
        ('scip', dict(exp='E5V', kind='path', n=16, kappa_target=4, seed=101, absgap=1e-6, variant='offset', time_limit=20, offset=True)),
    ]
    with ProcessPoolExecutor(max_workers=4) as ex:
        for k, t, r in ex.map(run, items):
            print('=====', k, t, 's\n', r, flush=True)
