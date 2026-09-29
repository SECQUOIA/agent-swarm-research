"""Normalize the worst E9 instances to S = {y^2 >= x^2 + 1}: report xbar, rays, w, ratios."""
import numpy as np
from scipy.optimize import linprog
from sfree import corner_bound, qval
from exp7_sym_worst import U, transform
from exp9_family_closure import cut_coeffs, closure_bound

# canonical S = {y^2 >= x^2 + 1}: q = x^2 - y^2 + 1
Q = np.diag([1.0, -1.0]); b = np.zeros(2); c = 1.0
xy = lambda s: (s[0], s[1]); kappa = 1.0

def ratios(sbar, P, w):
    zk = corner_bound(Q, b, c, sbar, P, w)
    sym = [a for a in (cut_coeffs(xy, kappa, sbar, P, u, u) for u in U) if a is not None]
    asym = [a for a in (cut_coeffs(xy, kappa, sbar, P, u, v) for u in U[::4] for v in U[::4]
                        if abs(u[0] + v[0]) + abs(u[1] + v[1]) > 1e-9) if a is not None]
    return zk, closure_bound(sym, w) / zk, closure_bound(asym, w) / zk

rng = np.random.default_rng(5)
best = (1, None)
for t in range(3000):
    sbar = np.array([rng.normal() * 2, rng.uniform(-0.99, 0.99)])
    sbar[1] *= np.sqrt(sbar[0] ** 2 + 1)
    ang = rng.uniform(0, 2 * np.pi, 2)
    P = np.array([np.cos(ang), np.sin(ang)])
    if abs(np.linalg.det(P)) < 1e-3:
        continue
    w = rng.uniform(0.01, 1, 2)
    zk = corner_bound(Q, b, c, sbar, P, w)
    if not np.isfinite(zk):
        continue
    sym = [a for a in (cut_coeffs(xy, kappa, sbar, P, u, u) for u in U[::3]) if a is not None]
    r = closure_bound(sym, w) / zk
    if r < best[0]:
        best = (r, (sbar, P, w))
r, (sbar, P, w) = best
print('worst sampled sym-closure ratio', r)
print('sbar', sbar, 'ray angles (deg)', np.degrees(np.arctan2(P[1], P[0])), 'w', w)
print('full recompute (zK, sym ratio, asym ratio):', ratios(sbar, P, w))
