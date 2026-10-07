"""R8 check: how good is the incumbent before the first grid stage?

For planted instances (F* = 0) and the chain G_m (minimizer 0 = lower corner),
report the initial upper bound U_0 (after the solver's polishing starts) and
whether the starting point equals the planted minimizer.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import sys, time
from fractions import Fraction as F
sys.path.insert(0, (_PUBLIC_REPO + '/paper-decomposition-aware/experiments'))
sys.path.insert(0, (_PUBLIC_REPO + '/paper-decomposition-aware/experiments/chain'))
from instances import planted
from certified_grid import solve

for kind, n, kt, seed in [('path', 16, 2, 101), ('path', 16, 4, 101), ('path', 128, 4, 101),
                          ('band3', 8, 4, 101), ('path', 16, 256, 101)]:
    p, info = planted(kind, n, kt, seed)
    cert = solve(p, epsilon=F(1, 10**6), max_stages=0, time_limit=60, convex_presolve=False)
    U0 = F(cert['initial']['upper'])
    x0 = [F(v) for v in cert['initial']['point']]
    xs = [F(v) for v in info['xstar']]
    dist2 = sum((a - b) ** 2 for a, b in zip(x0, xs))
    print(f"{kind}{n} kappa_t={kt}: U0-F* = {float(U0):.3e}, |x0-x*|^2 = {float(dist2):.3e}, x0==x*: {x0 == xs}")
