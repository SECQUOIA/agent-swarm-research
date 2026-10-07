"""Sampling check of egfast.fexp against 50-digit mpmath (not a proof; the proof is the
error analysis in the egfast docstring)."""
import mpmath as mp
import numpy as np
from fractions import Fraction as Fr

import egfast

rng = np.random.default_rng(1)
xs = np.concatenate([rng.uniform(-700, 0, 4000), rng.uniform(-50, 0, 4000), rng.uniform(-1, 1, 2000),
                     rng.uniform(0, 600, 1000), np.array([0.0, -1e-300, 5e-324, -700.0, 600.0, 1e-16, -1e-16])])
lo, hi = egfast.fexp(xs)
mp.mp.dps = 50
worst = 0.0
bad = 0
for x, l, h in zip(xs, lo, hi):
    e = mp.exp(mp.mpf(float(x)))   # floats convert exactly
    if not (mp.mpf(l) <= e <= mp.mpf(h)):
        bad += 1
    worst = max(worst, float((mp.mpf(h) - mp.mpf(l)) / e))
print(f"fexp: {len(xs)} points, {bad} enclosure failures, max relative width {worst:.3e}")
xs2 = rng.uniform(-750, -700, 100)
lo2, hi2 = egfast.fexp(xs2)
print("x < -700 handled:", bool(np.all(lo2 == 0) and np.all(hi2 == 1e-300)))
