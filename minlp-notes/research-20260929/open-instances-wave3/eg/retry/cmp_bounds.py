"""Tightness comparison (sampling, not a proof): for boxes of relative width rho around the
eg_int_s point found by the search (integers fixed at (2, 4, 3)), the median over boxes and
objective rows of  (sampled minimum of g_k over the box) - (lower bound of g_k on the box)
for
  wave 3:  natural enclosure intersected with the mean-value form (../eg_bb.py, Prob.bound),
  natural: the natural enclosure of this retry (egfast.Fast.natural),
  TM:      min over the box of the affine minorant of egfast.Fast.taylor (2nd/3rd order).
The sampled minimum overestimates the true minimum, so all gaps are slightly inflated.

    python3 cmp_bounds.py
"""
import os
import sys

import numpy as np

import egbb
import egfast

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import eg_bb  # noqa: E402

name = "eg_int_s"
F = egfast.Fast(name)
D = F.D
P3 = eg_bb.Prob(name)
xs = np.array([0.564219345763436, 0.6468471890552644, 1.0, 0.9390699678023392, 2.0, 4.0, 3.0])
rng = np.random.default_rng(5)
W = F.hi0 - F.lo0
print("rho     wave3(nat+MVF)  natural     TM        (median gap over 64 boxes x 24 rows)")
for rho in (0.3, 0.1, 0.03, 0.01, 0.003):
    N = 64
    c = xs + (rng.random((N, 7)) - 0.5) * W * rho
    lo = np.clip(c - W * rho / 2, F.lo0, F.hi0); hi = np.clip(c + W * rho / 2, F.lo0, F.hi0)
    lo[:, 4:] = xs[4:]; hi[:, 4:] = xs[4:]
    X = lo[:, None, :] + rng.random((N, 400, 7)) * (hi - lo)[:, None, :]
    g, _ = D.g(X.reshape(-1, 7)); g = g.reshape(N, 400, 28)
    gmin = g.min(1)[:, :24]
    _, _, enc = P3.bound(lo, hi)
    nat = F.natural(lo, hi)
    T = F.taylor(lo, hi)
    fixed = hi == lo
    dl = np.where(fixed, 0.0, lo - T["c"]); dh = np.where(fixed, 0.0, hi - T["c"])
    tm = T["aL"] + egbb.lin_min(T["beta"], dl, dh)
    print(f"{rho:<7g} {np.median(gmin - enc.lo[:, :24]):<15.3e} {np.median(gmin - nat.lo[:, :24]):<11.3e} "
          f"{np.median(gmin - tm[:, :24]):.3e}")
