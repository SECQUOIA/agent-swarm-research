"""Does the LP optimum of check_kink_sharp_lp.py stay below M s^2 between grid
points?  The script bounds phi_i <= M s_i^2 - M ds^2/4 at the grid points,
which keeps the interpolant below M s^2, but it then fixes phi(0) = -W, which
replaces that bound at s = 0.  When W < M ds^2/4 the interpolant can exceed
M s^2 near 0.  Run from any directory; imports the note's script to confirm
that the LP values are the same.
"""
import os
import sys

import numpy as np
from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "theory-decomposition", "covering"))
import check_kink_sharp_lp as K  # noqa: E402


def solve(W, M, h, m):
    s = np.linspace(-h, h, 2 * m + 1); ds = h / m; N = len(s)
    ia, ib = m - m // 2, m + m // 2
    c = np.zeros(N); c[ib] -= 1 / ds; c[ib - 1] += 1 / ds
    c[ia + 1] += 1 / ds; c[ia] -= 1 / ds
    A = np.zeros((N - 2, N))
    for i in range(1, N - 1):
        A[i - 1, i - 1] = -1; A[i - 1, i] = 2; A[i - 1, i + 1] = -1
    bounds = [(None, M * si ** 2 - M * ds ** 2 / 4) for si in s]
    bounds[m] = (-W, -W)
    res = linprog(c, A_ub=A, b_ub=np.zeros(N - 2), bounds=bounds, method="highs")
    return s, res.x, -res.fun


for W, M, h in [(0.0, 1.0, 1.0), (0.01, 5.0, 1.0), (1.0, 1.0, 1.0)]:
    for m in [8, 64, 512]:
        s, x, v = solve(W, M, h, m)
        assert abs(v - K.lp_max_rise(W, M, h, m)) < 1e-9
        f = np.linspace(-h, h, 400001)
        phi = np.interp(f, s, x)
        print(f"W={W}, M={M}, h={h}, m={m}: LP value {v:.6f}; max over fine grid "
              f"of (interpolant - M s^2) = {np.max(phi - M * f ** 2):.2e}; "
              f"M ds^2/4 = {M * (h / m) ** 2 / 4:.2e}")
