"""Dense first-level relaxation on the full-gap instances of Proposition 3.4 (r = 1, 2, 3)
and on the four-variable path of Burer-Natarajan-Willemsen (2025, Example 4).

Relaxation: moment matrix Y of (1, v) positive semidefinite, plus the McCormick
inequalities of every product and square over the box. The SDP is solved numerically
(CVXPY + Clarabel); a rational point is then built by mixing the numerical solution with
the moment matrix of the uniform distribution on the box (positive definite, strictly
inside every McCormick inequality) and rounding. Positive semidefiniteness is checked
exactly (LDL^T in Fractions) and every McCormick inequality exactly, so the printed value
of the linearized objective at the rational point is a rigorous upper bound on the
relaxation value. The true minimum is computed exactly for comparison.
"""
import itertools
import os
import sys
from fractions import Fraction as F

os.environ.setdefault("OMP_NUM_THREADS", "1")
import cvxpy as cp
import numpy as np


def ldl_psd(M):
    """Exact test that a symmetric rational matrix is positive semidefinite."""
    n = len(M)
    A = [row[:] for row in M]
    for k in range(n):
        if A[k][k] < 0:
            return False
        if A[k][k] == 0:
            if any(A[k][j] != 0 for j in range(k + 1, n)):
                return False
            continue
        for i in range(k + 1, n):
            f = A[i][k] / A[k][k]
            for j in range(k + 1, n):
                A[i][j] -= f * A[k][j]
    return True


def solve(nvar, lo, hi, quad, lin, const, label):
    """min lin(f) over dense relaxation; quad[(i,j)] coefficients (i<=j), lin[i], const."""
    n = nvar + 1
    Y = cp.Variable((n, n), symmetric=True)
    cons = [Y >> 0, Y[0, 0] == 1]
    for i in range(nvar):
        for j in range(i, nvar):
            xi, xj, xij = Y[0, i + 1], Y[0, j + 1], Y[i + 1, j + 1]
            li, ui, lj, uj = lo[i], hi[i], lo[j], hi[j]
            cons += [xij - lj * xi - li * xj + li * lj >= 0,
                     ui * uj - uj * xi - ui * xj + xij >= 0,
                     uj * xi + li * xj - li * uj - xij >= 0,
                     lj * xi + ui * xj - ui * lj - xij >= 0]
    obj = const + sum(c * Y[0, i + 1] for i, c in lin.items()) + sum(c * Y[i + 1, j + 1] for (i, j), c in quad.items())
    prob = cp.Problem(cp.Minimize(obj), cons)
    prob.solve(solver=cp.CLARABEL)
    Yv = Y.value
    # uniform distribution on the box: E v_i = (l+u)/2, E v_i^2 = (l^2+lu+u^2)/3, E v_i v_j = product of means
    m = [F(lo[i] + hi[i], 2) for i in range(nvar)]
    s = [F(lo[i] ** 2 + lo[i] * hi[i] + hi[i] ** 2, 3) for i in range(nvar)]
    U = [[F(1)] + m]
    for i in range(nvar):
        U.append([m[i]] + [s[i] if i == j else m[i] * m[j] for j in range(nvar)])
    def value(Z):
        return F(const) + sum(F(c) * Z[0][i + 1] for i, c in lin.items()) + sum(F(c) * Z[i + 1][j + 1] for (i, j), c in quad.items())
    def mccormick_ok(Z):
        for i in range(nvar):
            for j in range(i, nvar):
                xi, xj, xij = Z[0][i + 1], Z[0][j + 1], Z[i + 1][j + 1]
                li, ui, lj, uj = F(lo[i]), F(hi[i]), F(lo[j]), F(hi[j])
                if (xij - lj * xi - li * xj + li * lj < 0 or ui * uj - uj * xi - ui * xj + xij < 0 or
                        uj * xi + li * xj - li * uj - xij < 0 or lj * xi + ui * xj - ui * lj - xij < 0):
                    return False
        return True
    best = None
    for eps in (F(1, 10**k) for k in (8, 7, 6, 5, 4, 3, 2)):
        Z = [[(1 - eps) * F(Yv[a, b]).limit_denominator(10**12) + eps * U[a][b] for b in range(n)] for a in range(n)]
        for a in range(n):
            for b in range(a):
                Z[a][b] = Z[b][a]
        Z[0][0] = F(1)
        if ldl_psd(Z) and mccormick_ok(Z):
            best = (eps, value(Z))
            break
    print(f"{label}: SDP value {prob.value:.10g}; rational feasible point {best[1] if best else None} "
          f"(= {float(best[1]) if best else float('nan'):.6g}, mixing eps {best[0] if best else None})")
    return prob.value, best


def fullgap(r):
    # variables: x_1..x_r, y, z_1..z_r ; Phi_L + Phi_R
    nvar = 2 * r + 1
    iy = r
    lo = [0] * nvar
    hi = [1] * nvar
    hi[iy] = 2 ** (r + 1) - 1
    quad, lin, const = {}, {}, F(0)
    def add_sq(terms, c0):
        # (sum_k a_k v_k + c0)^2
        nonlocal const
        for (i, a) in terms:
            lin[i] = lin.get(i, 0) + 2 * a * c0
            for (j, b) in terms:
                key = (min(i, j), max(i, j))
                quad[key] = quad.get(key, 0) + a * b
        const += c0 * c0
    add_sq([(iy, 1)] + [(j, -(2 ** (j + 1))) for j in range(r)], 0)
    add_sq([(iy, 1)] + [(r + 1 + j, -(2 ** (j + 1))) for j in range(r)], -1)
    for j in range(r):
        for idx in (j, r + 1 + j):
            w = 4 ** (j + 1)
            lin[idx] = lin.get(idx, 0) + w
            quad[(idx, idx)] = quad.get((idx, idx), 0) - w
    return nvar, lo, hi, quad, lin, const


def exact_min_fullgap(r):
    # min over vertices of x,z and continuous y: dist formula; true min is 1/2 (Prop. 3.4)
    best = None
    for xs in itertools.product((0, 1), repeat=r):
        for zs in itertools.product((0, 1), repeat=r):
            s = sum(2 ** (j + 1) * xs[j] for j in range(r))
            t = 1 + sum(2 ** (j + 1) * zs[j] for j in range(r))
            v = F((s - t) ** 2, 2)
            best = v if best is None else min(best, v)
    return best


if __name__ == "__main__":
    for r in (1, 2, 3):
        print(f"Proposition 3.4, r = {r}: exact minimum {exact_min_fullgap(r)}")
        solve(*fullgap(r), label=f"  dense relaxation, r = {r}")
    Q = [[8, -14, 0, 0], [-14, 25, -25, 0], [0, -25, 25, -14], [0, 0, -14, 8]]
    c = [12, 29, 0, 0]
    quad = {}
    for i in range(4):
        for j in range(i, 4):
            quad[(i, j)] = Q[i][j] if i == j else 2 * Q[i][j]
    quad = {k: v for k, v in quad.items() if v}
    print("BNW Example 4 (four-variable path): exact minimum 0 (Theorem 4.1 enumeration, R9 scripts)")
    solve(4, [0] * 4, [1] * 4, quad, {i: c[i] for i in range(4) if c[i]}, 0, "  dense relaxation, four-variable path")
