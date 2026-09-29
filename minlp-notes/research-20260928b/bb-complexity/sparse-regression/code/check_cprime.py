"""Largest c' admitted by the proof of Theorem 4.3: maximize c' subject to c' < (1-mu) theta and
(*) (1+mu)(1-theta) x / B > e^x - 1, B = 1 + 2 sqrt(c'x) + 2c'x, over mu, theta in (0,1)
(fine grid, then Nelder-Mead polish).  Planted (Theorem 4.4) at kappa_s = K(x)/2:
(1+kappa_s) < e^{-x}(1 + (1+mu)(1-theta)x/B).  As x -> 0 the supremum is 3 - 2 sqrt 2."""
import numpy as np
from scipy.optimize import minimize
K = lambda x: np.exp(-x) * (1 + 2 * x) - 1
def cmax(mu, th, x, planted):
    A = (1 + mu) * (1 - th) * x
    rhs = (np.exp(x) - 1) if not planted else ((1 + K(x) / 2) * np.exp(x) - 1)
    Bmax = A / rhs
    if Bmax <= 1 or not (0 < mu < 1 and 0 < th < 1): return 0.0
    u = (-2 + np.sqrt(4 - 8 * (1 - Bmax))) / 4          # 2u^2 + 2u + 1 = Bmax, u = sqrt(c'x)
    return min(u * u / x, (1 - mu) * th)
def best(x, planted=False):
    grid = [(cmax(m, t, x, planted), m, t) for m in np.linspace(0.005, 0.995, 199) for t in np.linspace(0.002, 0.998, 250)]
    c0, m0, t0 = max(grid)
    r = minimize(lambda v: -cmax(v[0], v[1], x, planted), [m0, t0], method='Nelder-Mead', options=dict(xatol=1e-9, fatol=1e-12, maxiter=4000))
    return max(c0, -r.fun)
print("limit x -> 0: 3 - 2 sqrt 2 = %.4f" % (3 - 2 * np.sqrt(2)))
for x in [1e-6, 1e-3, 1e-2, 0.05, 0.2, 0.5, 0.8, 1.0, 1.2]:
    a, b = best(x), best(x, True)
    print("x=%-6g c'_max pure noise %.5f   planted (kappa_s = K/2) %.5f   ratio %.2f" % (x, a, b, a / b if b > 0 else float('nan')))
