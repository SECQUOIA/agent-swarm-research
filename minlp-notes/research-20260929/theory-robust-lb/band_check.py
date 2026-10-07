"""Check Proposition 12 numerically: gamma_d = inf_{rho in P_d} [max(L - rho) + max(rho - U)] on [-1,1]
(grid LP; a lower bound on the true inf up to grid effects) against the LP relaxation gaps."""
import numpy as np
from numpy.polynomial import chebyshev as C
from scipy.optimize import linprog
y1, eta, eps = 0.38, 0.05, 0.02
c = 1 + eta + eps
y = np.cos(np.linspace(0, np.pi, 6001))
L = np.where(np.abs(y) <= y1, y * y, 2 * y1 * np.abs(y) - y1 * y1)           # L = -h1
h2 = -eta * y * y - (1 - eta) * np.maximum(np.abs(y) - y1, 0) ** 2
U = h2 + c * y * y
M = len(y)
for d in [2, 3, 4, 5, 6, 8, 9, 10, 12]:
    V = C.chebvander(y, d); k = V.shape[1]
    # vars: a (k free), t1, t2 >= 0; min t1 + t2;  L - V a <= t1 ; V a - U <= t2
    A = np.vstack([np.hstack([-V, -np.ones((M, 1)), np.zeros((M, 1))]),
                   np.hstack([V, np.zeros((M, 1)), -np.ones((M, 1))])])
    b = np.concatenate([-L, U])
    cc = np.zeros(k + 2); cc[-2:] = 1
    res = linprog(cc, A_ub=A, b_ub=b, bounds=[(None, None)] * k + [(None, None)] * 2, method="highs")
    print("d=%d  band gap = %.6f" % (d, res.fun))
