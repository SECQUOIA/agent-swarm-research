"""Checks for the revision after review (Section 12 of the note).
(1) E2 = quadratic example: n^2 * 2E_n((s_+)^2) for n = 64..256, computed
    from the residual after Chebyshev interpolation (so the LP works at
    relative accuracy) on dense grids;
(2) aligned hp at p = 12: per-cell E_12 of psi, same residual method, plus
    the interpolant error as an upper bound;
(3) T1 at K = 100, n = 4 on a finer grid than check_tree.py."""
import numpy as np
from numpy.polynomial import chebyshev as C
from consistency_lib import grid, cheb_basis, band_gap
import check_tree as CT

out = open("logs/check_revision.log", "w")
def log(m):
    print(m); out.write(m + "\n"); out.flush()

def E_n(f, n, lo=-1.0, hi=1.0, m=40001, extra=()):
    """Best uniform error of degree n on [lo, hi]: LP on the residual after
    degree-n Chebyshev interpolation (rescaled to max 1). Returns (lower,
    interpolant error = upper bound)."""
    k = np.arange(n + 1)
    t = np.cos(np.pi * (k + 0.5) / (n + 1))
    c = C.chebfit(t, f(0.5 * (lo + hi) + 0.5 * (hi - lo) * t), n)
    s = grid(lo, hi, m, extra)
    tt = (2 * s - lo - hi) / (hi - lo)
    r = f(s) - C.chebval(tt, c)
    scale = np.max(np.abs(r))
    g, *_ = band_gap(cheb_basis(s, n, lo, hi), r / scale, r / scale, tight=True)
    return g / 2 * scale, scale

h = lambda s: np.maximum(s, 0) ** 2
log("(1) quadratic example: n^2 * gap, gap = 2 E_n((s_+)^2)")
prev = None
for n in [64, 128, 256]:
    e, up = E_n(h, n, extra=(0.0,), m=60001)
    val = n * n * 2 * e
    log(f"  n={n}: n^2 gap = {val:.5f} (interpolant bound {n*n*2*up:.5f})"
        + (f", difference to previous {prev - val:.5f}" if prev else ""))
    prev = val

c0 = 1 / np.sqrt(7)
psi = lambda s: -np.abs(s - c0) + 0.3 * np.sin(3 * s) + 0.2 * s ** 2
log("(2) aligned hp, cells [-1,c0] and [c0,1]: gap = 2 max_D E_p")
for p in [4, 8, 12]:
    vals = [E_n(psi, p, a, b, m=20001) for a, b in [(-1, c0), (c0, 1)]]
    log(f"  p={p}: gap = {2 * max(v[0] for v in vals):.4e} "
        f"(per-cell E_p {vals[0][0]:.4e}, {vals[1][0]:.4e}; interpolant bounds {vals[0][1]:.4e}, {vals[1][1]:.4e})")

log("(3) T1 at n = 4: gap / 2E_n on finer grids")
for npts in [161, 321]:
    s = np.unique(np.concatenate([np.linspace(-1, 1, npts), [0.0]]))
    a, c = -np.abs(s), np.abs(s)
    S1, S2 = np.meshgrid(s, s, indexing="ij")
    B = cheb_basis(s, 4)
    b0 = np.abs(S1) - np.abs(S2)
    g1 = CT.fstar(a, b0, c) - CT.tree_rho(a, b0, c, B, B, full2=True)
    for K in [100.0, 1000.0]:
        b = b0 + K * (S1 - S2) ** 2
        g = CT.fstar(a, b, c) - CT.tree_rho(a, b, c, B, B)
        log(f"  grid {npts}: K={K:.0f}: gap/2E_n = {g / g1:.4f}")
