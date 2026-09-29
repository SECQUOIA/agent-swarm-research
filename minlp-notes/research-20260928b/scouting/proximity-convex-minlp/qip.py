"""Small exact tools for convex quadratic integer programs
    min 1/2 x^T Q x + c^T x  s.t.  A x <= b,  x in Z^n   (Q positive definite).

Continuous optimum: exact active-set enumeration with Fractions.
Integer optima: exhaustive enumeration inside the ellipsoid
    {z : 1/2 ||z - x*||_Q^2 <= f(z0) - f(x*)},
which contains every integer optimum by the KKT inequality
    f(z) - f(x*) >= grad f(x*)^T (z - x*) + 1/2 ||z - x*||_Q^2 >= 1/2 ||z - x*||_Q^2.
"""
from fractions import Fraction as F
from itertools import combinations, product
import math
import numpy as np


def solve(M, rhs):
    """Exact Gaussian elimination; returns None if singular."""
    n = len(M)
    a = [list(map(F, row)) + [F(r)] for row, r in zip(M, rhs)]
    for col in range(n):
        piv = next((r for r in range(col, n) if a[r][col] != 0), None)
        if piv is None:
            return None
        a[col], a[piv] = a[piv], a[col]
        for r in range(n):
            if r != col and a[r][col] != 0:
                fac = a[r][col] / a[col][col]
                a[r] = [x - fac * y for x, y in zip(a[r], a[col])]
    return [a[i][n] / a[i][i] for i in range(n)]


def fval(Q, c, x):
    n = len(x)
    return sum(F(Q[i][j]) * x[i] * x[j] for i in range(n) for j in range(n)) / 2 + sum(
        F(c[i]) * x[i] for i in range(n))


def feasible(A, b, x):
    return all(sum(F(A[r][j]) * x[j] for j in range(len(x))) <= b[r] for r in range(len(A)))


def qp_opt(Q, c, A, b):
    """Exact optimum of the strictly convex QP by active-set enumeration."""
    n, m = len(Q), len(A)
    for k in range(0, min(n, m) + 1):
        for S in combinations(range(m), k):
            K = [[F(Q[i][j]) for j in range(n)] + [F(A[s][i]) for s in S] for i in range(n)]
            K += [[F(A[s][j]) for j in range(n)] + [F(0)] * k for s in S]
            rhs = [-F(ci) for ci in c] + [F(b[s]) for s in S]
            sol = solve(K, rhs)
            if sol is None:
                continue
            x, lam = sol[:n], sol[n:]
            if all(l >= 0 for l in lam) and feasible(A, b, x):
                return x
    return None


def int_opt(Q, c, A, b, xs, max_points=400000, search_radius=40):
    """All integer optima (exact); None if infeasible within search or too large."""
    n = len(Q)
    base = [math.floor(v) for v in xs]
    z0 = None
    for r in range(0, search_radius + 1):
        for d in product(range(-r, r + 1), repeat=n):
            if r > 0 and max(abs(v) for v in d) < r:
                continue
            z = [base[i] + d[i] for i in range(n)]
            if feasible(A, b, z):
                z0 = z
                break
        if z0 is not None:
            break
    if z0 is None:
        return None
    fstar = fval(Q, c, xs)
    gap = fval(Q, c, z0) - fstar
    Qn = np.array([[float(v) for v in row] for row in Q])
    Qi = np.linalg.inv(Qn)
    rad = [math.sqrt(max(0.0, 2 * float(gap) * Qi[i][i])) + 1e-9 for i in range(n)]
    lo = [math.ceil(float(xs[i]) - rad[i] - 1e-7) for i in range(n)]
    hi = [math.floor(float(xs[i]) + rad[i] + 1e-7) for i in range(n)]
    npts = 1
    for i in range(n):
        npts *= hi[i] - lo[i] + 1
    if npts > max_points:
        return "big"
    xf = np.array([float(v) for v in xs])
    best, arg = None, []
    for z in product(*[range(lo[i], hi[i] + 1) for i in range(n)]):
        d = np.array(z) - xf
        if 0.5 * d @ Qn @ d > float(gap) * (1 + 1e-9) + 1e-9:
            continue
        if not feasible(A, b, z):
            continue
        v = fval(Q, c, z)
        if best is None or v < best:
            best, arg = v, [list(z)]
        elif v == best:
            arg.append(list(z))
    return arg


def prox_inf(xs, opts):
    return min(max(abs(F(z[i]) - xs[i]) for i in range(len(z))) for z in opts)


def max_subdet(A):
    m, n = len(A), len(A[0])
    best = 0
    for k in range(1, min(m, n) + 1):
        for R in combinations(range(m), k):
            for C in combinations(range(n), k):
                M = np.array([[A[r][c] for c in C] for r in R], dtype=float)
                best = max(best, abs(round(np.linalg.det(M))))
    return best


def voronoi_linf_radius(Q, box=None):
    """l_inf radius of the Voronoi cell of Z^n in the Q-norm (float LP).
    Candidate relevant vectors: all nonzero z with ||z||_Q^2 <= tr(Q)
    (relevant vectors have ||z||_Q <= 2*mu <= sqrt(tr Q))."""
    from scipy.optimize import linprog
    Qn = np.array([[float(v) for v in row] for row in Q])
    n = len(Qn)
    tr = np.trace(Qn)
    Qi = np.linalg.inv(Qn)
    rad = [int(math.floor(math.sqrt(tr * Qi[i][i]))) for i in range(n)]
    cons, rhs = [], []
    for z in product(*[range(-r, r + 1) for r in rad]):
        z = np.array(z, dtype=float)
        if not z.any():
            continue
        q = z @ Qn @ z
        if q <= tr * (1 + 1e-9):
            cons.append(z @ Qn)
            rhs.append(q / 2)
    Aub, bub = np.array(cons), np.array(rhs)
    best = 0.0
    for i in range(n):
        obj = np.zeros(n)
        obj[i] = -1
        res = linprog(obj, A_ub=Aub, b_ub=bub, bounds=[(None, None)] * n, method="highs")
        best = max(best, -res.fun)
    return best
