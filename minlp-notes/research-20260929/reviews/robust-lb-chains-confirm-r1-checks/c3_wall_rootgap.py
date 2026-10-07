"""Root gap of the fixed balanced split on WALL by a grid LP (mean-consistent families on a grid; a lower bound on
the gap, since grid families are feasible). Grid: 161 uniform points on [-1,1] plus c and a few fooling points."""
import sys
import numpy as np
from numpy.polynomial import polynomial as P
from scipy.optimize import linprog, brentq
from scipy import sparse
UC = np.array([0.0, 1.022, 0.189, 1.774, 1.086]); B = 0.962
u = lambda t: P.polyval(t, UC)
c = brentq(lambda t: P.polyval(t, P.polyder(UC)) - 2 * B, -1, 1, xtol=1e-15)
grid = np.unique(np.concatenate([np.linspace(-1, 1, int(sys.argv[2]) if len(sys.argv) > 2 else 161), [c, 0.2335146, 0.2335240]]))
K = len(grid)
for n in [int(v) for v in sys.argv[1].split(",")]:
    X, Y = np.meshgrid(grid, grid, indexing="ij")
    costs = []
    for e in range(n - 1):
        F = 0.5 * (u(X) + u(Y)) + B * X * Y
        if e == 0:
            F = F + 0.5 * u(X)
        if e == n - 2:
            F = F + 0.5 * u(Y)
        costs.append(F.ravel())
    cost = np.concatenate(costs); nv = K * K
    rows = []; cols = []; vals = []; beq = []; r = 0
    for e in range(n - 1):
        rows += [r] * nv; cols += list(range(e * nv, (e + 1) * nv)); vals += [1.0] * nv; beq.append(1.0); r += 1
    for e in range(n - 2):
        rows += [r] * nv; cols += list(range(e * nv, (e + 1) * nv)); vals += list(Y.ravel())
        rows += [r] * nv; cols += list(range((e + 1) * nv, (e + 2) * nv)); vals += list(-X.ravel()); beq.append(0.0); r += 1
    A = sparse.csr_matrix((vals, (rows, cols)), shape=(r, (n - 1) * nv))
    res = linprog(cost, A_eq=A, b_eq=beq, bounds=(0, None), method="highs")
    if n % 2 == 0:
        fs = (n // 2 + 1) * u(-1.0) + (n // 2 - 1) * u(c) + B * (1 - (n - 2) * c)
    else:
        fs = (n + 1) // 2 * u(-1.0) + (n - 1) // 2 * u(c) - B * (n - 1) * c
    print(f"n={n}: grid ({K} points) LP root gap of the fixed balanced split >= {fs - res.fun:.7f}; per wall pair {(fs-res.fun)/max(n//2-1,1):.7f}", flush=True)
