"""Exact rational tools for the split-separation review (independent of the scout's code).

enum_below(G, R, center, parity): all integer z with (z-c)^T G (z-c) < R, optionally with
fixed parities z_i = parity_i (mod 2). G must be positive definite rational. Exact
Fincke-Pohst enumeration via a rational LDL^T factorization, so the list is complete.
"""
from fractions import Fraction as F
from math import isqrt, floor, ceil


def ldl_upper(G):
    """Return d, mu with z^T G z = sum_i d_i (z_i + sum_{j>i} mu[i][j] z_j)^2."""
    N = len(G)
    A = [[F(x) for x in row] for row in G]
    d = [F(0)] * N
    mu = [[F(0)] * N for _ in range(N)]
    for i in range(N):
        d[i] = A[i][i]
        if d[i] <= 0:
            raise ValueError("matrix is not positive definite")
        for j in range(i + 1, N):
            mu[i][j] = A[i][j] / d[i]
        for j in range(i + 1, N):
            for k in range(i + 1, N):
                A[j][k] -= A[i][j] * A[i][k] / d[i]
    return d, mu


def enum_below(G, R, center=None, parity=None):
    N = len(G)
    c = [F(0)] * N if center is None else [F(x) for x in center]
    d, mu = ldl_upper(G)
    z = [0] * N
    out = []

    def rec(i, rem):
        if i < 0:
            out.append(tuple(z))
            return
        # term_i = d_i (y_i + sum_{j>i} mu_ij y_j)^2 with y = z - c
        shift = sum((mu[i][j] * (z[j] - c[j]) for j in range(i + 1, N)), F(0))
        cc = c[i] - shift  # term_i = d_i (z_i - cc)^2
        q = rem / d[i]
        r = isqrt(floor(q)) + 1
        for zi in range(floor(cc) - r, ceil(cc) + r + 1):
            if parity is not None and parity[i] is not None and (zi - parity[i]) % 2:
                continue
            t = d[i] * (zi - cc) ** 2
            if t < rem:
                z[i] = zi
                rec(i - 1, rem - t)
        z[i] = 0

    rec(N - 1, F(R))
    return out


def qform(Y, v):
    N = len(Y)
    return sum(v[i] * Y[i][j] * v[j] for i in range(N) for j in range(N))


def split_q(Y, v):
    """<v (v+e0)^T, Y> = v^T Y v + v^T Y e0."""
    N = len(Y)
    return qform(Y, v) + sum(v[i] * Y[i][0] for i in range(N))


def violators_pd(Y):
    """All v in Z^{N} with split_q(Y, v) < 0, for positive definite Y (complete list).

    Uses q(v) = ((2v+e0)^T Y (2v+e0) - Y00)/4 and enumerates u = 2v+e0 with u^T Y u < Y00.
    """
    N = len(Y)
    # Reverse the coordinate order so that u0 (odd) is enumerated outermost; its range
    # is then sqrt((Y^-1)_00), which keeps the search small.
    perm = list(range(N))[::-1]
    Yp = [[Y[perm[i]][perm[j]] for j in range(N)] for i in range(N)]
    par = [1 if perm[i] == 0 else 0 for i in range(N)]
    us_p = enum_below(Yp, Y[0][0], parity=par)
    us = []
    for up in us_p:
        u = [0] * N
        for i in range(N):
            u[perm[i]] = up[i]
        us.append(tuple(u))
    vs = []
    for u in us:
        v = tuple((u[i] - (1 if i == 0 else 0)) // 2 for i in range(N))
        assert split_q(Y, v) < 0
        vs.append(v)
    return vs


def gram(vectors):
    return [[sum(F(a) * F(b) for a, b in zip(x, y)) for y in vectors] for x in vectors]


def mat_inv(A):
    n = len(A)
    M = [[F(x) for x in row] + [F(int(i == j)) for j in range(n)] for i, row in enumerate(A)]
    for col in range(n):
        piv = next(r for r in range(col, n) if M[r][col] != 0)
        M[col], M[piv] = M[piv], M[col]
        p = M[col][col]
        M[col] = [x / p for x in M[col]]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [x - f * y for x, y in zip(M[r], M[col])]
    return [row[n:] for row in M]


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def transpose(A):
    return [list(r) for r in zip(*A)]
