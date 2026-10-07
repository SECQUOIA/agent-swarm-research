"""Spot checks for Section 11 claims: (1) for kappa_target = 2 the initial coordinate
descent returns x* on all E2/E3 instances; (2) the three E4 instances with n = 3 have no
continuous coordinate with positive curvature; (3) E6 kappa brackets rounded outward."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import sys, json, glob, math
from fractions import Fraction as F
sys.path.insert(0, (_PUBLIC_REPO + '/paper-decomposition-aware/experiments'))
from instances import planted, random_small
from certified_grid import solve
ok = []
for n in (4, 8, 16, 32, 64, 128):
    for seed in (101, 202, 303):
        p, info = planted('path', n, 2, seed)
        c = solve(p, epsilon=F(1, 10**6), max_stages=0, time_limit=60, convex_presolve=False)
        ok.append([F(v) for v in c['initial']['point']] == [F(v) for v in info['xstar']])
print('kappa=2 initial descent returns x*:', sum(ok), 'of', len(ok))
for seed, kind in ((4001, 'path'), (4002, 'tree'), (4003, 'band2')):
    p = random_small(3, kind, 1, seed)
    print(p.name, 'continuous with A_ii>0:', [i for i in range(3) if i not in p.integers and p.A[i][i] > 0])
br = []
for f in glob.glob((_PUBLIC_REPO + '/paper-decomposition-aware/experiments/results/raw/E6_*.json')):
    g = json.load(open(f))['growth']
    if g['status'] == 'certified':
        br.append((g['kappa_lb'], g['kappa_ub']))
for lo, hi in sorted(br, key=lambda t: t[1]):
    d = 1 if hi < 1000 else 0
    print(f'[{math.floor(lo*10)/10:.1f}, {math.ceil(hi*10**d)/10**d}]', lo, hi)
