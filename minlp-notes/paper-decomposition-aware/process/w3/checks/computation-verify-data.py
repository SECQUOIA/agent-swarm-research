"""Verifier checks of the numbers quoted in sections/computation.tex against
experiments/results/*.csv (independent of summarize.py)."""
import csv
import math
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

R = Path(__file__).resolve().parents[3] / 'experiments' / 'results'


def rows(name):
    with open(R / f'{name}.csv') as fh:
        return list(csv.DictReader(fh))


def fl(x):
    return float(x) if x not in ('', None) else None


print('== kappa brackets for kappa_target = 4 (E1, E3, E5)')
for name in ('E1_runs', 'E3_runs', 'E5_grid_runs', 'E2_runs'):
    rs = [r for r in rows(name) if r['kappa_target'] in ('4', '4.0')]
    if rs:
        print(name, 'kappa_lb min', min(fl(r['kappa_lb']) for r in rs),
              'kappa_ub max', max(fl(r['kappa_ub']) for r in rs))
allr = rows('E1_runs') + rows('E2_runs') + rows('E3_runs') + rows('E5_grid_runs')
print('max kappa_ub/kappa_lb over E1-E3,E5:', max(fl(r['kappa_ub']) / fl(r['kappa_lb']) for r in allr))
print('planted H indefinite in all runs (nu>0):', all(fl(r['nu']) > 0 for r in allr),
      'min nu', min(fl(r['nu']) for r in allr))

print('== E2 per method: status/final trial by kappa_target')
e2 = rows('E2_runs')
by = defaultdict(list)
for r in e2:
    by[(r['method'], int(float(r['kappa_target'])))].append(r)
for (m, k), rs in sorted(by.items()):
    print(m, k, sorted({r['status'] for r in rs}), sorted({r['final_trial'] for r in rs}),
          'theta', sorted({r['theta'] for r in rs}))

print('== E3 node plateaus by method, kappa_target, n (median over seeds of max over last 4 stages)')
st = rows('E3_stages')
plate = defaultdict(list)
groups = defaultdict(list)
for r in st:
    groups[(r['method'], r['kappa_target'], int(r['n']), r['seed'])].append(r)
for (m, k, n, s), rs in groups.items():
    rs.sort(key=lambda r: int(r['stage']))
    last = rs[-4:]
    plate[(m, k, n)].append(sorted(int(r['max_nodes_free']) for r in last)[len(last) // 2])
for key in sorted(plate):
    v = sorted(plate[key])
    print(key, v)

print('== separable count 4(floor(sqrt(n/4))+1)+1 for uniform, kappa_target 2')
for n in (4, 8, 16, 32, 64, 128):
    print(n, 4 * (math.isqrt(n // 4) + 1) + 1)
