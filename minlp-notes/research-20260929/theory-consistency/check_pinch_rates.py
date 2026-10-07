"""Polynomial rates at a pinch point (note, Section 5.4): curvature jump vs kink.

E5(c): U = -(s_+)^2, L = U - c s^2  (curvature jump 2 at the pinch s = 0)
E6(c): U = -|s|,     L = U - c s^2  (kink of size 2 at the pinch)
Grid refined geometrically near the pinch; HiGHS tolerances 1e-10.
Reported: LP value on the grid (lower estimate) and the LP solution
re-evaluated on a 10x finer grid (upper estimate).
"""
import numpy as np
from consistency_lib import grid, cheb_basis, band_gap, eval_gap

geo = np.concatenate([10.0 ** -np.arange(1, 7, 0.05), -10.0 ** -np.arange(1, 7, 0.05), [0.0]])


def gap(U, L, n):
    s = np.unique(np.concatenate([grid(-1, 1, 8001), geo]))
    g, c, _, _ = band_gap(cheb_basis(s, n), U(s), L(s), tight=True)
    sf = np.unique(np.concatenate([grid(-1, 1, 80001), geo]))
    return g, eval_gap(cheb_basis(sf, n) @ c, U(sf), L(sf))


out = open("logs/check_pinch_rates.log", "w")
def log(m):
    print(m); out.write(m + "\n"); out.flush()

log("E5(c): n^2 * gap (lower / upper estimates)")
for c in [0.0, 0.1, 0.3, 0.5, 0.8, 0.95, 1.0]:
    U = lambda s: -np.maximum(s, 0) ** 2
    L = lambda s, c=c: -np.maximum(s, 0) ** 2 - c * s ** 2
    row = []
    for n in [4, 8, 16, 32, 64]:
        g, gu = gap(U, L, n)
        row.append(f"n={n}: {n*n*g:.3e}/{n*n*gu:.3e}")
    log(f"  c={c:4.2f}: " + "; ".join(row))
log("E6(c): n * gap (lower / upper estimates); 2*beta = 0.5603")
for c in [0.0, 0.5, 2.0, 8.0]:
    U = lambda s: -np.abs(s)
    L = lambda s, c=c: -np.abs(s) - c * s ** 2
    row = []
    for n in [4, 8, 16, 32, 64, 128]:
        g, gu = gap(U, L, n)
        row.append(f"n={n}: {n*g:.4f}/{n*gu:.4f}")
    log(f"  c={c:4.1f}: " + "; ".join(row))
