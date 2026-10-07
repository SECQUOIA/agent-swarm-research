"""Remark 7: S = {y^2 >= x^2 + 1}, sbar = 0, rays r1 = (a, r), r2 = -r1 + eta n, w = (1,1).
Upper bound on the closure of all constant-lambda sets via the explicit point c(1,1),
c = 1/min_u (a_1(u) + a_2(u)) (convex 1-D), vs z_K and the oblique split."""
import numpy as np
from scipy.optimize import minimize_scalar
from core import corner_bound
Q = np.diag([1.0, -1.0]); b = np.zeros(2); c = 1.0; sbar = np.zeros(2); w = np.ones(2)
for a in (10, 100, 1000):
    r = np.sqrt(1 + a * a); eta = a ** -3.0
    n = np.array([r, -a]) / np.hypot(r, a)
    P = np.stack([np.array([a, r]), -np.array([a, r]) + eta * n], 1)
    zk = corner_bound(Q, b, c, sbar, P, w)
    f = lambda u: sum(max(0.0, abs(P[1, j]) * np.sqrt(1 + u * u) - u * P[0, j]) for j in range(2))
    res = minimize_scalar(f, bounds=(-1e3, 1e3), method='bounded', options=dict(xatol=1e-12))
    grid = min(f(u) for u in np.linspace(-50, 50, 200001))
    m = min(res.fun, grid)
    zs = min(1.0 / abs(r * P[1, j] - a * P[0, j]) for j in range(2))
    print('a=%5d eta=a^-3: z_K=%.7f  closure(const-lambda) <= 2/min(a1+a2) = %.7f (1/r=%.7f)  split=%.7f' % (a, zk, 2 / m, 1 / r, zs))
