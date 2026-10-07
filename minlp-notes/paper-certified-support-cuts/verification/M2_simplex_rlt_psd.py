"""M2: context check for Report A's simplex example.

On the triangle T = {x, y >= 0, x + y <= 1}, Anstreicher-Burer (2010, Corollary
after Theorem 3) give conv{(x, y, x^2, xy, y^2)} = PSD + pairwise RLT of the three
facet constraints.  This script compares, for random directions, the exact
support (bordered enumeration, exact rationals) with the PSD+RLT relaxation bound
(numerical SDP, Clarabel).  Agreement supports the caveat that the example's
advantage over "box hull + row" is already obtained by PSD+RLT on the triangle.

Run: code/minlp_solver_lab/.venv/bin/python -B \
        paper-certified-support-cuts/verification/M2_simplex_rlt_psd.py
"""

import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

import random
from fractions import Fraction as Fr
from itertools import combinations

import cvxpy as cp
import numpy as np

random.seed(7)
TRI = [((-1, 0), Fr(0)), ((0, -1), Fr(0)), ((1, 1), Fr(1))]


def exact_support(cx, cy, cxx, cxy, cyy):
    """min of cx x + cy y + cxx x^2 + cxy xy + cyy y^2 over T by bordered enumeration."""
    H = [[2 * cxx, cxy], [cxy, 2 * cyy]]
    best = None
    for k in range(3):
        for S in combinations(TRI, k):
            n = 2 + k
            K = [[Fr(0)] * n for _ in range(n)]
            r = [Fr(-cx), Fr(-cy)] + [s[1] for s in S]
            for i in range(2):
                for j in range(2):
                    K[i][j] = Fr(H[i][j])
                for t, s in enumerate(S):
                    K[i][2 + t] = K[2 + t][i] = Fr(s[0][i])
            # exact Gaussian elimination
            M = [row[:] + [r[i]] for i, row in enumerate(K)]
            ok = True
            for col in range(n):
                piv = next((i for i in range(col, n) if M[i][col] != 0), None)
                if piv is None:
                    ok = False
                    break
                M[col], M[piv] = M[piv], M[col]
                for i in range(n):
                    if i != col and M[i][col] != 0:
                        f = M[i][col] / M[col][col]
                        M[i] = [a - f * b for a, b in zip(M[i], M[col])]
            if not ok:
                continue
            x, y = M[0][-1] / M[0][0], M[1][-1] / M[1][1]
            if x >= 0 and y >= 0 and x + y <= 1:
                v = cx * x + cy * y + cxx * x * x + cxy * x * y + cyy * y * y
                best = v if best is None or v < best else best
    return best


def psd_rlt_bound(cx, cy, cxx, cxy, cyy):
    Y = cp.Variable((3, 3), symmetric=True)   # [[1, x, y], [x, X, Z], [y, Z, W]]
    x, y, X, Z, W = Y[0, 1], Y[0, 2], Y[1, 1], Y[1, 2], Y[2, 2]
    # facet functions g = (x, y, 1 - x - y); RLT: linearized g_i g_j >= 0
    cons = [Y >> 0, Y[0, 0] == 1,
            X >= 0, W >= 0, Z >= 0,                 # x*x, y*y, x*y
            x - X - Z >= 0,                          # x * (1 - x - y)
            y - Z - W >= 0,                          # y * (1 - x - y)
            1 - 2 * x - 2 * y + X + 2 * Z + W >= 0]  # (1 - x - y)^2
    obj = cp.Minimize(cx * x + cy * y + cxx * X + cxy * Z + cyy * W)
    prob = cp.Problem(obj, cons)
    prob.solve(solver=cp.CLARABEL)
    return prob.value


worst = 0.0
for _ in range(25):
    coef = [Fr(random.randint(-6, 6), random.randint(1, 3)) for _ in range(5)]
    e = exact_support(*coef)
    b = psd_rlt_bound(*[float(v) for v in coef])
    worst = max(worst, abs(float(e) - b))
# the two specific inequalities of Report A
e1 = exact_support(Fr(1), Fr(1), Fr(-1), Fr(-2), Fr(-1))     # x + y - (x+y)^2 >= 0
e2 = exact_support(Fr(0), Fr(0), Fr(0), Fr(-1), Fr(0)) + Fr(1, 4)  # 1/4 - xy >= 0
print(f"max |exact support - PSD+RLT bound| over 25 random directions: {worst:.2e}")
print(f"Report A inequalities: min(x+y-(x+y)^2) = {e1}, min(1/4 - xy) = {e2}")
ok = worst < 1e-6 and e1 == 0 and e2 == 0
raise SystemExit(0 if ok else 1)
