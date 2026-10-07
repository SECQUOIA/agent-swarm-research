"""R8 probe: E3 (dimension) uses kappa_target = 2, for which the planted
generator sets the free-free coupling to zero (H_SS = 2I).  Repeat E3's
design with kappa_target = 4 (coupled free block) for n = 8..128, seeds
101/202, geometric (theorem theta) and uniform filtered grids, 11 stages.
Reports the plateau of max nodes over free coordinates (median of the last
4 stages), as in summarize.py.  4 workers; nothing is written to experiments/.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import os, sys, json
for v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[v] = '1'
from statistics import median
from concurrent.futures import ProcessPoolExecutor
sys.path.insert(0, (_PUBLIC_REPO + '/paper-decomposition-aware/experiments'))

def run(spec):
    import run_all
    rec = run_all.task_grid(spec)
    st = rec['stages']
    plateau = median(s['max_nodes_free'] for s in st[-4:])
    rad = median(s['radius_over_h_free'] for s in st[-4:])
    return (spec['n'], spec['seed'], spec['method'], plateau, rad, rec['verify']['valid'], rec['instance']['kappa_ub'])

if __name__ == '__main__':
    specs = []
    for n in (8, 16, 32, 64, 128):
        for seed in (101, 202):
            for tag, mode in (('geom_theorem', 'geometric'), ('unif', 'uniform')):
                specs.append(dict(exp='E3x', kind='path', n=n, kappa_target=4, seed=seed, grid_mode=mode,
                                  pruning=True, theta=None, method=tag, max_stages=11, time_limit=60,
                                  max_table_states=200000))
    with ProcessPoolExecutor(max_workers=4) as ex:
        res = list(ex.map(run, specs))
    for r in sorted(res):
        print(r)
