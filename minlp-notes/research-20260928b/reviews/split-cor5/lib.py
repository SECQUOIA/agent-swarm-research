"""Shared exact-arithmetic helpers for the Corollary 3 / Corollary 5 recheck.

Written independently of side-results/check_split_separation.py.
Standard library only; all arithmetic is exact (fractions.Fraction).
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import isqrt, floor, ceil


# ---------------------------------------------------------------- construction
def build_X(A, b, gamma2, h2, M=1):
    """Gram matrix of b0 = (0, 0, -2*gamma, 2h), b_i = (M*A_i, 2e_i, 0, 0), g = (M*b, 1, gamma, 0),
    ordered 0, 1..n, g, divided by |b0|^2.  gamma and h enter only through gamma2 and h2, so each
    vector is a coefficient list and the inner product carries weights (1,...,1, gamma2, h2).
    Returns (X, G) with G the unnormalized Gram matrix."""
    p, n = len(A), len(A[0])
    gamma2, h2 = F(gamma2), F(h2)
    w = [F(1)] * (p + n) + [gamma2, h2]
    b0 = [0] * (p + n) + [-2, 2]
    cols = [[M * A[r][i] for r in range(p)] + [2 if k == i else 0 for k in range(n)] + [0, 0]
            for i in range(n)]
    g = [M * b[r] for r in range(p)] + [1] * n + [1, 0]
    vecs = [b0] + cols + [g]
    G = [[sum(wk * s * t for wk, s, t in zip(w, u, v)) for v in vecs] for u in vecs]
    return [[e / G[0][0] for e in row] for row in G], G


def x3c_matrix(sets, universe):
    """Incidence matrix A (rows = elements, columns = sets) and b = all-ones."""
    return [[1 if e in S else 0 for S in sets] for e in universe], [1] * len(universe)


def exact_covers(sets, universe):
    """All 0/1 vectors x with A x = 1."""
    out = []
    for x in product((0, 1), repeat=len(sets)):
        cnt = {e: 0 for e in universe}
        for xi, S in zip(x, sets):
            if xi:
                for e in S:
                    cnt[e] += 1
        if all(c == 1 for c in cnt.values()):
            out.append(x)
    return out


def predicted_violators(sols):
    """Theorem 1(b): (0, -x, 1) and (-1, x, -1) for each solution x."""
    return ({(0,) + tuple(-t for t in x) + (1,) for x in sols}
            | {(-1,) + tuple(x) + (-1,) for x in sols})


# ---------------------------------------------------------------- split values
def qval(X, v):
    """q_X(v) = v^T X v + v^T X e0."""
    N = len(X)
    return (sum(v[i] * X[i][j] * v[j] for i in range(N) for j in range(N))
            + sum(v[i] * X[i][0] for i in range(N)))


def ldl(X):
    """u^T X u = sum_k d[k] * (u_k + sum_{j>k} R[k][j] u_j)^2.  Returns None unless X is PD."""
    N = len(X)
    S = [[F(e) for e in row] for row in X]
    d, R = [F(0)] * N, [[F(0)] * N for _ in range(N)]
    for k in range(N):
        d[k] = S[k][k]
        if d[k] <= 0:
            return None
        for j in range(k + 1, N):
            R[k][j] = S[k][j] / d[k]
        for i in range(k + 1, N):
            for j in range(k + 1, N):
                S[i][j] -= S[i][k] * S[k][j] / d[k]
    return d, R


def all_violators(X):
    """Every v in Z^N with q_X(v) < 0, for PD X with X00 = 1 (complete enumeration of
    u = 2v + e0 with u^T X u < X00 = 1; u0 odd, u_i even for i >= 1)."""
    fac = ldl(X)
    assert fac is not None, "X not positive definite"
    d, R = fac
    N = len(X)
    u = [0] * N
    found = []

    def go(k, rem):
        if k < 0:
            found.append(tuple((u[i] - (1 if i == 0 else 0)) // 2 for i in range(N)))
            return
        c = -sum((R[k][j] * u[j] for j in range(k + 1, N)), F(0))
        r = isqrt(floor(rem / d[k])) + 1
        for uk in range(floor(c) - r, ceil(c) + r + 1):
            if (uk % 2 == 1) != (k == 0):
                continue
            t = d[k] * (uk - c) ** 2
            if t < rem:
                u[k] = uk
                go(k - 1, rem - t)
        u[k] = 0

    go(N - 1, F(X[0][0]))
    for v in found:
        assert qval(X, v) < 0
    return set(found)


def inverse_diag(X):
    """Diagonal of X^{-1} by exact Gauss-Jordan."""
    N = len(X)
    M = [[F(e) for e in row] + [F(int(i == j)) for j in range(N)] for i, row in enumerate(X)]
    for c in range(N):
        p = next(r for r in range(c, N) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        piv = M[c][c]
        M[c] = [e / piv for e in M[c]]
        for r in range(N):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [a - f * bb for a, bb in zip(M[r], M[c])]
    return [M[i][N + i] for i in range(N)]


def brute_violators(X):
    """Independent box search: |u_i| < sqrt((X^-1)_ii) for any u with u^T X u < 1 (Cauchy-Schwarz)."""
    dg = inverse_diag(X)
    N = len(X)
    ranges = []
    for i in range(N):
        B = isqrt(floor(dg[i])) + 1
        ranges.append([t for t in range(-B, B + 1) if (t % 2 == 1) == (i == 0)])
    out = set()
    for u in product(*ranges):
        v = tuple((u[i] - (1 if i == 0 else 0)) // 2 for i in range(N))
        if qval(X, v) < 0:
            out.add(v)
    return out


# ---------------------------------------------------------------- de Meijer et al. families
def split_xY(X):
    """x_i = X_{i0}, Y = X on the variable indices 1..N-1."""
    return [X[i][0] for i in range(1, len(X))], [row[1:] for row in X[1:]]


def slacks(X):
    """Minimum slack (lhs - rhs) of each family of de Meijer et al. (arXiv:2603.28979v1) at X.
    PDF numbering; forms checked against the arXiv HTML:
      (4.1)  diag(Y) >= x, diag(Y) >= -x, diag(Y) <= 1   [PSD checked separately]
      (2.1)-(2.2)  the four sign patterns for 1 <= i < j < k
      (2.3)  Y_ij <= Y_ii and Y_ij >= -Y_ii for all i != j
      (4.4)  sum_{i<j in S} v_i v_j Y_ij >= ceil(-|S|/2), |S| odd, v in {+-1}^S
      (4.5)-(4.8) Y_ij + x_i + x_j >= -1, Y_ij - x_i - x_j >= -1,
                  -Y_ij + x_i - x_j >= -1, -Y_ij - x_i + x_j >= -1, i < j
    Written family by family from the source text (not via a sign-vector shortcut)."""
    x, Y = split_xY(X)
    m = len(x)
    out = {}
    out["4.1"] = min(min(Y[i][i] - x[i], Y[i][i] + x[i], 1 - Y[i][i]) for i in range(m))
    tri = []
    for i, j, k in combinations(range(m), 3):
        tri += [Y[i][j] + Y[i][k] + Y[j][k] + 1, -Y[i][j] + Y[i][k] - Y[j][k] + 1,
                Y[i][j] - Y[i][k] - Y[j][k] + 1, -Y[i][j] - Y[i][k] + Y[j][k] + 1]
    out["2.1-2.2"] = min(tri) if tri else None
    pr = []
    for i in range(m):
        for j in range(m):
            if i != j:
                pr += [Y[i][i] - Y[i][j], Y[i][j] + Y[i][i]]
    out["2.3"] = min(pr) if pr else None
    odd = []
    for k in range(1, m + 1, 2):
        rhs = ceil(F(-k, 2))  # ceil(-|S|/2), as printed in the source
        for S in combinations(range(m), k):
            for v in product((1, -1), repeat=k):
                lhs = sum(v[a] * v[c] * Y[S[a]][S[c]] for a, c in combinations(range(k), 2))
                odd.append(lhs - rhs)
    out["4.4"] = min(odd)
    rlt = []
    for i, j in combinations(range(m), 2):
        rlt += [Y[i][j] + x[i] + x[j] + 1, Y[i][j] - x[i] - x[j] + 1,
                -Y[i][j] + x[i] - x[j] + 1, -Y[i][j] - x[i] + x[j] + 1]
    out["4.5-4.8"] = min(rlt) if rlt else None
    return out


def satisfies_all(X):
    s = slacks(X)
    return ldl(X) is not None and all(val is None or val >= 0 for val in s.values()), s


def flip(X, sigma):
    """D X D with D = diag(1, sigma)."""
    D = [1] + list(sigma)
    return [[D[i] * D[j] * X[i][j] for j in range(len(X))] for i in range(len(X))]
