"""Search small-denominator rational bilinear corners (side '+', S = {w <= xy}) whose
corner minimizer lies in the relative interior of a tangent edge and for which the
kappa-sets of the vertices have empty intersection (numerical screen)."""
import numpy as np, itertools, warnings; warnings.filterwarnings('ignore')
from fractions import Fraction as Fr
from core import bilinear_quadratic, corner_bound, qval, best_orbit_bound
from kappa_family import kappa_pencil, feasible_kappas
rng = np.random.default_rng(5)
Q, b, c = bilinear_quadratic('+')
kg = np.concatenate([-np.logspace(5, -5, 3000), [0.0], np.logspace(-5, 5, 3000)])
found = []
for trial in range(60000):
    x0, y0 = rng.integers(-3, 4, 2)
    dx = int(rng.integers(1, 4)); dy = -int(rng.integers(1, 4))
    t0 = np.array([x0, y0, x0 * y0], float)
    d = np.array([dx, dy, y0 * dx + x0 * dy], float)
    a, bb = rng.integers(1, 4, 2)
    v1 = t0 + a * d; v2 = t0 - bb * d
    sbar = t0 + np.array(rng.integers(-3, 4, 3), float) / 2
    v3 = t0 + np.array(rng.integers(-6, 7, 3), float) / 2
    if qval(Q, b, c, sbar) <= 0: continue
    P = np.stack([v1 - sbar, v2 - sbar, v3 - sbar], 1)
    if abs(np.linalg.det(P)) < 1e-9: continue
    w = np.ones(3)
    zk, lam = corner_bound(Q, b, c, sbar, P, w, return_point=True)
    if not (abs(zk - 1) < 1e-9 and lam[2] < 1e-9 and lam[0] > 1e-6 and lam[1] > 1e-6): continue
    # unique minimizer? require all other supports strictly > 1
    G0, G1 = kappa_pencil('+', t0, d)
    ok = feasible_kappas(G0, G1, '+', [sbar, v1, v2, v3], kg)
    if ok.any(): continue
    cert, hi, F = best_orbit_bound('+', sbar, P, w, 1.0, iters=30)
    found.append((hi, sbar, v1, v2, v3, t0, d))
    print('found', trial, 'orbit/zK <= %.4f' % hi, 'sbar', sbar, 'v1', v1, 'v2', v2, 'v3', v3, 't0', t0, 'd', d, flush=True)
    if len(found) >= 10: break
