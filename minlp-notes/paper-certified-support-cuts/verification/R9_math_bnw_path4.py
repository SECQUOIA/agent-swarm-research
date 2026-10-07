#!/usr/bin/env python3
"""Round-2 math check: is the advantage of joint blocks over pairs only one of representation?

Burer, Natarajan and Willemsen (2025, arXiv 2504.03996), Example 4 / Proposition 12:
    f(x) = x^T Q x + c^T x on [0,1]^4,
    Q = [[8,-14,0,0],[-14,25,-25,0],[0,-25,25,-14],[0,0,-14,8]],  c = (12, 29, 0, 0).
Q is tridiagonal, so the interaction graph is the path x1-x2-x3-x4 (a four-variable block,
within the paper's block size limit and within the scope of Theorem 4.1 with d = 4).

Checks:
  1. min_{[0,1]^4} f = 0, attained only at x = 0 (exact candidate enumeration of Theorem 4.1).
  2. Dense moment relaxation of (1,x) with ALL McCormick/RLT inequalities (all pairs, including
     the nonedges x1x3, x1x4, x2x4, and the squares): value about -0.122 (Clarabel).
  3. The same plus the triangle inequalities: value about -1.4e-4 (still negative).
  4. The glued pair relaxation (edge hulls of the path, each exact = SDP+RLT on a 2-D box,
     glued on shared (x_i, x_i^2)): its value.
  5. Consequence: the exact support cut lin f >= 0 of the four-variable block (coordinates
     x_i, x_i^2, x1x2, x2x3, x3x4 only) is violated by the projection of the optimal dense
     solution, so the joint block is strictly stronger than dense SDP + all McCormick here.

Run: OMP_NUM_THREADS=1 .venv/bin/python R9_math_bnw_path4.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import itertools  # noqa: E402
from fractions import Fraction as Fr  # noqa: E402

import numpy as np  # noqa: E402
import cvxpy as cp  # noqa: E402
import sympy as sp  # noqa: E402

Qm = [[8, -14, 0, 0], [-14, 25, -25, 0], [0, -25, 25, -14], [0, 0, -14, 8]]
c = [12, 29, 0, 0]
n = 4


def f_exact(x):
    return sum(Qm[i][j] * x[i] * x[j] for i in range(n) for j in range(n)) + sum(c[i] * x[i] for i in range(n))


def enumerate_min():
    """Theorem 4.1: candidates from row sets I (|I| <= d) with M_I nonsingular, feasible."""
    H = sp.Matrix(Qm) * 2          # q = 1/2 x^T H x + c^T x
    cv = sp.Matrix(c)
    rows = []                      # A x <= b: x_i <= 1, -x_i <= 0
    for i in range(n):
        e = [0] * n
        e[i] = 1
        rows.append((e, 1))
        e2 = [0] * n
        e2[i] = -1
        rows.append((e2, 0))
    best, arg = None, []
    for k in range(n + 1):
        for I in itertools.combinations(range(len(rows)), k):
            A = sp.Matrix([rows[r][0] for r in I]) if I else sp.zeros(0, n)
            b = sp.Matrix([rows[r][1] for r in I]) if I else sp.zeros(0, 1)
            M = sp.zeros(n + k, n + k)
            M[:n, :n] = H
            if k:
                M[:n, n:] = A.T
                M[n:, :n] = A
            if M.det() == 0:
                continue
            sol = M.LUsolve(sp.Matrix.vstack(-cv, b))
            x = [sol[i] for i in range(n)]
            if all(0 <= xi <= 1 for xi in x):
                v = f_exact(x)
                if best is None or v < best:
                    best, arg = v, [tuple(x)]
                elif v == best and tuple(x) not in arg:
                    arg.append(tuple(x))
    return best, arg


def dense(triangles=False):
    Y = cp.Variable((n + 1, n + 1), symmetric=True)
    x = Y[0, 1:]
    X = Y[1:, 1:]
    cons = [Y >> 0, Y[0, 0] == 1]
    for i in range(n):
        for j in range(i, n):
            cons += [X[i, j] >= 0, X[i, j] <= x[i], X[i, j] <= x[j], X[i, j] >= x[i] + x[j] - 1]
    if triangles:
        for i, j, k in itertools.combinations(range(n), 3):
            cons += [x[i] + x[j] + x[k] - X[i, j] - X[i, k] - X[j, k] <= 1,
                     X[i, j] + X[i, k] - X[j, k] <= x[i],
                     X[i, j] + X[j, k] - X[i, k] <= x[j],
                     X[i, k] + X[j, k] - X[i, j] <= x[k]]
    obj = cp.Minimize(cp.trace(np.array(Qm, dtype=float) @ X) + np.array(c, float) @ x)
    prob = cp.Problem(obj, cons)
    prob.solve(solver=cp.CLARABEL)
    return prob.value, np.array(Y.value)


def glued_pairs():
    """Edge hulls of the path glued on (x_i, x_i^2): 3x3 moment blocks PSD + RLT per edge."""
    xs = cp.Variable(n)
    sq = cp.Variable(n)
    p = cp.Variable(n - 1)
    cons = []
    for e in range(n - 1):
        i, j = e, e + 1
        B = cp.bmat([[np.ones((1, 1)), cp.reshape(xs[i], (1, 1)), cp.reshape(xs[j], (1, 1))],
                     [cp.reshape(xs[i], (1, 1)), cp.reshape(sq[i], (1, 1)), cp.reshape(p[e], (1, 1))],
                     [cp.reshape(xs[j], (1, 1)), cp.reshape(p[e], (1, 1)), cp.reshape(sq[j], (1, 1))]])
        cons += [B >> 0, p[e] >= 0, p[e] <= xs[i], p[e] <= xs[j], p[e] >= xs[i] + xs[j] - 1]
    for i in range(n):
        cons += [sq[i] <= xs[i], sq[i] >= 0, sq[i] >= 2 * xs[i] - 1]
    obj = sum(Qm[i][i] * sq[i] for i in range(n)) + sum(2 * Qm[e][e + 1] * p[e] for e in range(n - 1)) \
        + sum(c[i] * xs[i] for i in range(n))
    prob = cp.Problem(cp.Minimize(obj), cons)
    prob.solve(solver=cp.CLARABEL)
    return prob.value


if __name__ == "__main__":
    m, arg = enumerate_min()
    print("exact min over [0,1]^4:", m, "argmin:", arg)
    v1, Y1 = dense(False)
    v2, _ = dense(True)
    v3 = glued_pairs()
    print(f"dense SDP + all McCormick/RLT          : {v1:.7f}")
    print(f"dense SDP + all RLT + triangles         : {v2:.7f}")
    print(f"glued exact edge hulls (path pairs)     : {v3:.7f}")
    # support cut in model coordinates: lin f >= 0 evaluated at the projection of Y1
    x = Y1[0, 1:]
    X = Y1[1:, 1:]
    linf = sum(Qm[i][i] * X[i, i] for i in range(n)) + 2 * sum(Qm[i][i + 1] * X[i, i + 1] for i in range(n - 1)) \
        + float(np.dot(c, x))
    print(f"lin f at projected dense optimum (uses only x_i, x_i^2, x_i x_(i+1)): {linf:.7f}")
    ok = (m == 0 and arg == [(0, 0, 0, 0)] and v1 < -0.12 and v2 < -1e-4 and linf < -0.12)
    print("RESULT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)
