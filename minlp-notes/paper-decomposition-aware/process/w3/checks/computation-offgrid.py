"""Which free coordinates of the planted x* are grid nodes at the last stage, and why."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import sys
from fractions import Fraction as F
sys.path.insert(0, (_PUBLIC_REPO + '/paper-decomposition-aware/experiments'))
from instances import planted
from certified_grid import solve
import run_all
for kind, n, kt, seed in [('path', 16, 16, 101), ('path', 16, 4, 202), ('tree', 16, 4, 303)]:
    p, info = planted(kind, n, kt, seed)
    th = run_all.theorem_theta(info['kappa_ub'])
    c = solve(p, epsilon=F(1, 2**80), max_stages=12, time_limit=60, max_table_states=200000, theta=th,
              slope_decay_period=0, schedule='adaptive', convex_presolve=False)
    x = [F(v) for v in info['xstar']]; free = [i for i in range(n) if i not in set(info['active'])]
    y0 = [F(v) for v in c['initial']['point']]
    last = c['stages'][-1]
    on = [i for i in free if x[i] in set(map(F, last['grids'][i]))]
    print(kind, n, kt, seed, 'on-grid free coords:', [(i, str(x[i]), 'y0_i==x*_i' if y0[i] == x[i] else '') for i in on])
