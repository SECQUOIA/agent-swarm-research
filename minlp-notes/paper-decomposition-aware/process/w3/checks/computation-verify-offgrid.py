"""Classify the free coordinates of the planted x* that are nodes of the last grid.

Reruns the single-trial runs of E1 (filtered, kappa_target = 4) and E3
(kappa_target = 4, all three methods) with the settings of run_all.py and
splits the on-grid free coordinates into
  zero:    x*_i = 0 (a dyadic rational),
  descent: x*_i = k/21 with k != 0 and the initial descent already set x*_i,
  dyadic offset: the first center differs from x*_i by a nonzero dyadic rational,
  unexplained:   anything else (must be empty by the dyadic-node argument).
The per-run counts are compared with xstar_nodes_free of the saved results.
"""
import csv
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

EXP = Path(__file__).resolve().parents[3] / 'experiments'
sys.path.insert(0, str(EXP))
from instances import planted  # noqa: E402
from certified_grid import solve  # noqa: E402
from run_all import theorem_theta  # noqa: E402

saved = {}
for e in ('E1', 'E3'):
    with open(EXP / 'results' / f'{e}_stages.csv') as fh:
        for r in csv.DictReader(fh):
            k = r['key']
            if k not in saved or int(r['stage']) > saved[k][0]:
                saved[k] = (int(r['stage']), int(r['xstar_nodes_free']))

specs = []
for kind, n in (('path', 16), ('tree', 16), ('band2', 12), ('band3', 8)):
    for seed in (101, 202, 303):
        for mode in ('geometric', 'uniform'):
            specs.append(('E1', kind, n, seed, mode, None, 16, 100000))
for n in (4, 8, 16, 32, 64, 128):
    for seed in (101, 202, 303):
        for mode, theta in (('geometric', None), ('uniform', None), ('geometric', F(1, 4))):
            specs.append(('E3', 'path', n, seed, mode, theta, 11, 200000))

tot = Counter()
mismatch = []
for e, kind, n, seed, mode, theta, stages, cap in specs:
    prob, info = planted(kind, n, 4, seed)
    th = theta if theta is not None else theorem_theta(info['kappa_ub'])
    c = solve(prob, epsilon=F(1, 2 ** 80), max_stages=stages, time_limit=60, max_table_states=cap,
              pruning=True, grid_mode=mode, schedule='adaptive', theta=th, slope_decay_period=0,
              convex_presolve=False)
    xs = [F(v) for v in info['xstar']]
    y0 = [F(v) for v in c['initial']['point']]
    free = [i for i in range(n) if i not in set(info['active'])]
    last = c['stages'][-1]
    on = [i for i in free if xs[i] in set(map(F, last['grids'][i]))]
    def dyadic(q):
        return q.denominator & (q.denominator - 1) == 0
    cls = Counter('zero' if xs[i] == 0 else 'descent' if y0[i] == xs[i]
                  else 'dyadic offset' if dyadic(y0[i] - xs[i]) else 'unexplained' for i in on)
    tot.update(cls)
    tot['free'] += len(free)
    tot['runs'] += 1
    if e == 'E1':
        key = f"E1_{kind}{n}_s{seed}_{'geom' if mode == 'geometric' else 'unif'}_pruned"
    else:
        tag = 'geom_quarter' if theta is not None else ('geom_theorem' if mode == 'geometric' else 'unif')
        key = f'E3_k4_n{n}_s{seed}_{tag}'
    if key in saved and saved[key][1] != len(on):
        mismatch.append((key, saved[key][1], len(on)))
print(dict(tot))
print('mismatches with saved results:', mismatch[:10], len(mismatch))
