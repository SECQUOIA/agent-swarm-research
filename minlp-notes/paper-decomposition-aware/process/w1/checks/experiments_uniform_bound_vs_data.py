"""Check Proposition (filtered uniform grids) against every filtered uniform run.

Radius bound: ((1/2 + 1/(2 sqrt 2)) sqrt(n kappa) + 1) h_j for continuous coordinates,
using kappa_ub (a certified upper bound on kappa). Label bound for the next
stage: (2 + sqrt 2) sqrt(n kappa) + 7.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import csv
import math
from pathlib import Path

RES = Path((_PUBLIC_REPO + '/paper-decomposition-aware/experiments/results'))
worst_r, worst_n, count = 0.0, 0.0, 0
for e in ('E1', 'E2', 'E3'):
    runs = {r['key']: r for r in csv.DictReader(open(RES / f'{e}_runs.csv'))}
    for r in csv.DictReader(open(RES / f'{e}_stages.csv')):
        run = runs[r['key']]
        if not (r['method'] in ('uniform_pruned', 'unif')):
            continue
        n, k = int(r['n']), float(run['kappa_ub'])
        rb = (0.5 + 1 / (2 * math.sqrt(2))) * math.sqrt(n * k) + 1
        nb = (2 + math.sqrt(2)) * math.sqrt(n * k) + 7
        worst_r = max(worst_r, float(r['radius_over_h']) / rb)
        if int(r['stage']) >= 1:
            worst_n = max(worst_n, int(r['max_nodes']) / nb)
        count += 1
print(f'{count} uniform stages: max radius/bound = {worst_r:.3f}, max labels/bound = {worst_n:.3f}',
      'PASS' if worst_r <= 1 and worst_n <= 1 else 'FAIL')
