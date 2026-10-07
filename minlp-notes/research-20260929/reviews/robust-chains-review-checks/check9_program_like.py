"""Spot check of Section 2.4: u = t^2 - kappa t^4 + c t, balanced split (P_1) root gap, reviewer's code (cg4)."""
import numpy as np
from scipy.optimize import minimize
from cg4 import *
def fstar(u, B, n):
    G = np.linspace(-1, 1, 4001); uG = u(G); V = uG.copy(); back = []
    for _ in range(1, n):
        M = V[:, None] + B * G[:, None] * G[None, :]
        j = np.argmin(M, axis=0); back.append(j); V = M[j, np.arange(len(G))] + uG
    k = int(np.argmin(V)); path = [k]
    for j in reversed(back):
        k = int(j[k]); path.append(k)
    x0 = G[np.array(path[::-1])]
    f = lambda x: float(np.sum(u(x)) + B * np.sum(x[:-1] * x[1:]))
    r = minimize(f, x0, bounds=[(-1, 1)] * n, method="L-BFGS-B", options={"ftol": 1e-15, "gtol": 1e-13})
    return min(r.fun, f(x0))
for (ka, c, B) in [(0.1, 0.3, 0.8), (0.4, 0.3, 0.5), (0.6, 0.2, 0.4), (0.6, 0.2, -0.4)]:
    u = PP.poly([0, c, 1, 0, -ka])
    for n in (6, 10):
        fs = fstar(u, B, n)
        cb = ClassBound(uniform_chain(n, u, B), [PP.poly([0, 1])], K=7)
        lo, up, it = cb.bound(np.full(n, -1.0), np.full(n, 1.0), None, maxit=200, tol=1e-11)
        print(f"kappa={ka} c={c} b={B} n={n}: balanced root gap in [{fs-up:.2e}, {fs-lo:.2e}]", flush=True)
