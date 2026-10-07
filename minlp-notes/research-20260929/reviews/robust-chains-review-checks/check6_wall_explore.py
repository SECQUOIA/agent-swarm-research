"""Exploration (reviewer): uniform symmetric chain outside (H1) with an alternating bulk, u(x) = x^2 + c x,
w = b x y (b > 1).  Grid DP for f*_n, x*, and the energies of configurations with a 'wall' at each position."""
import numpy as np
from scipy.optimize import minimize
c, b = float(__import__("sys").argv[1]), float(__import__("sys").argv[2])
u = lambda t: t * t + c * t
G = np.linspace(-1, 1, 2001)
X, Y = np.meshgrid(G, G, indexing="ij")
P = 0.5 * (u(X) + u(Y)) + b * X * Y
k = np.unravel_index(np.argmin(P), P.shape)
print(f"c={c} b={b}: min phi = {P[k]:.5f} at ({G[k[0]]:.3f}, {G[k[1]]:.3f}); u(-1)={u(-1):.3f}")
def dp(n, fix=None):
    uG = u(G); V = uG.copy(); back = []
    for i in range(1, n):
        M = V[:, None] + b * G[:, None] * G[None, :]
        j = np.argmin(M, axis=0); back.append(j)
        V = M[j, np.arange(len(G))] + uG
    kk = int(np.argmin(V)); path = [kk]
    for j in reversed(back):
        kk = int(j[kk]); path.append(kk)
    x0 = G[np.array(path[::-1])]
    f = lambda x: float(np.sum(u(x)) + b * np.sum(x[:-1] * x[1:]))
    r = minimize(f, x0, bounds=[(-1, 1)] * n, method="L-BFGS-B", options={"ftol": 1e-15, "gtol": 1e-13})
    return min(r.fun, f(x0)), (r.x if r.fun < f(x0) else x0)
for n in range(3, 15):
    fs, xs = dp(n)
    print(f"  n={n:2d} f*={fs:+.6f} f*-(n-1)m={fs-(n-1)*P[k]:+.5f} x*={np.round(xs, 3).tolist()}")
