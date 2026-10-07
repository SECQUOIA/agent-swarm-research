"""Referee check R5: aligned hp value at p = 4, 8, 12 (note: 6.2e-3 / 2.4e-6 / 1.3e-10).

gap = max over the two cells of 2 E_p(psi | cell).  E_p bracketed by a Remez
de la Vallee Poussin lower bound (levelled error on an alternating reference)
and the Chebyshev-interpolant error on a 200001-point grid (upper bound up to
grid resolution).  Cells whose error is at round-off (Remez cannot level) are
reported with the interpolation bound only.
"""
import numpy as np
from numpy.polynomial import chebyshev as C
import r3_kink_rates as r

c0 = 1 / np.sqrt(7)
f = lambda t: -np.abs(t - c0) + 0.3 * np.sin(3 * t) + 0.2 * t ** 2
for p in [4, 8, 12]:
    los, ups = [], []
    for (lo, hi) in [(-1, c0), (c0, 1)]:
        x = np.linspace(lo, hi, 20001)
        basis = lambda t, lo=lo, hi=hi: C.chebvander((2 * t - lo - hi) / (hi - lo), p)
        l, u = r.remez(f, basis, lo, hi, x, iters=100)
        tt = np.cos(np.pi * (np.arange(p + 1) + 0.5) / (p + 1))
        coef = C.chebfit(tt, f(lo + (tt + 1) / 2 * (hi - lo)), p)
        xf = np.linspace(lo, hi, 200001)
        interp = np.max(np.abs(f(xf) - C.chebval((2 * xf - lo - hi) / (hi - lo), coef)))
        if u > interp:          # Remez did not level (round-off cell)
            l = 0.0
        los.append(l); ups.append(min(u, interp))
    print(f"p={p:2d} N={2 * (p + 1)}: gap = max_D 2E_p in [{2 * max(los):.4e}, {2 * max(ups):.4e}]")
