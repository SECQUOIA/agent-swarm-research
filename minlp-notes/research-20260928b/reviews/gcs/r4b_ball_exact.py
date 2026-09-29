"""Check kappa_true == ball_best (best enclosing ball) on random polygons, including
wide apertures and far-from-origin / near-origin sets.  See r4_squared.py for definitions."""
import numpy as np
from r4_squared import kappa_true, ball_best, product_bound, ball_min
rng = np.random.default_rng(1)
worst = 0.0; n = 0; prod_wins = 0
for k in range(150):
    npts = int(rng.integers(2, 10))
    half = np.radians(rng.uniform(1, 80))
    ang = rng.uniform(-half, half, npts) + rng.uniform(0, 2*np.pi)
    rad = rng.uniform(0.2, rng.uniform(0.3, 10), npts)
    V = np.c_[rad*np.cos(ang), rad*np.sin(ang)]
    bb = ball_best(V)
    if not np.isfinite(bb): continue
    kt = kappa_true(V, hi=min(1e4, 2*bb))
    pb = product_bound(V)
    n += 1
    worst = max(worst, abs(kt-bb)/bb)
    prod_wins += pb < bb*(1-1e-6)
print(f"{n} polygons: max |kappa_true - ball_best|/ball_best = {worst:.2e}; product bound strictly better in {prod_wins}")
