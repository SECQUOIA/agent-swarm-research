"""Independent exact tools for the split-separation review (standard library only).

Nothing here is copied from check_split_separation.py. Differences on purpose:
  * the LDL^T factorization runs in the forward order (X = L D L^T, enumeration from the
    last coordinate down), where the note's script eliminates the last variable first;
  * a second, provably complete enumerator uses the Cauchy-Schwarz box
    |u_i| < sqrt(X00 * (X^-1)_ii) of Theorem 2, so the two can be cross-checked;
  * matrices are built from the formula printed in Theorem 1, not from vectors.
"""
from fractions import Fraction as F
from itertools import product
from math import isqrt, floor, ceil


def q(X, v):
    """<v (v+e0)^T, X> computed directly from the definition."""
    N = len(X)
    w = list(v)
    w[0] += 1
    return sum(v[i] * X[i][j] * w[j] for i in range(N) for j in range(N))


def quad(X, u):
    N = len(X)
    return sum(u[i] * X[i][j] * u[j] for i in range(N) for j in range(N))


def ldl(X):
    """Forward LDL^T: X = L diag(d) L^T, L unit lower triangular. Returns (L, d) or None if
    some pivot is <= 0 (then X is not positive definite)."""
    N = len(X)
    L = [[F(0)] * N for _ in range(N)]
    d = [F(0)] * N
    for i in range(N):
        s = F(X[i][i]) - sum(L[i][k] ** 2 * d[k] for k in range(i))
        if s <= 0:
            return None
        d[i] = s
        L[i][i] = F(1)
        for j in range(i + 1, N):
            L[j][i] = (F(X[j][i]) - sum(L[j][k] * L[i][k] * d[k] for k in range(i))) / s
    return L, d


def is_pd(X):
    return ldl(X) is not None


def fp_enum(X, bound, parity=True, center=None):
    """All integer u with (u-center)^T X (u-center) < bound, X positive definite.
    If parity: u0 odd and u_i even for i >= 1. Forward LDL, enumerate k = N-1 .. 0."""
    L, d = ldl(X)
    N = len(X)
    c0 = [F(0)] * N if center is None else [F(c) for c in center]
    out, u = [], [0] * N

    def rec(k, rem):
        if k < 0:
            out.append(tuple(u))
            return
        # term_k = d_k (y_k + sum_{j>k} L[j][k] y_j)^2 with y = u - center
        s = sum(L[j][k] * (u[j] - c0[j]) for j in range(k + 1, N))
        mid = c0[k] - s  # u_k - c0_k + s = 0  <=>  u_k = c0_k - s
        rad2 = rem / d[k]
        r = isqrt(floor(rad2)) + 1
        for uk in range(floor(mid) - r - 1, ceil(mid) + r + 2):
            if parity and (uk % 2 != (1 if k == 0 else 0)):
                continue
            t = d[k] * (uk - mid) ** 2
            if t < rem:
                u[k] = uk
                rec(k - 1, rem - t)
        u[k] = 0

    rec(N - 1, F(bound))
    return out


def violators_fp(X, zero_first=False):
    """All violated split vectors v (q_X(v) < 0) for positive definite X with X00 = 1.
    zero_first: enumerate coordinate 0 first (reverse the order; fast when X is near e0 e0^T).
    Parity is handled by shifting: u = 2y + e0, enumerate y with center -e0/2."""
    N = len(X)
    perm = list(reversed(range(N))) if zero_first else list(range(N))
    Y = [[4 * X[perm[i]][perm[j]] for j in range(N)] for i in range(N)]  # u^T X u = y'^T (4X) y'
    center = [F(-1, 2) if perm[i] == 0 else F(0) for i in range(N)]
    ys = fp_enum(Y, X[0][0], parity=False, center=center)
    vs = []
    for y in ys:
        v = [0] * N
        for i in range(N):
            v[perm[i]] = y[i]
        vs.append(tuple(v))
    assert all(q(X, v) < 0 for v in vs)
    return set(vs)


def inverse(X):
    N = len(X)
    A = [[F(x) for x in row] + [F(int(i == j)) for j in range(N)] for i, row in enumerate(X)]
    for c in range(N):
        p = next(r for r in range(c, N) if A[r][c] != 0)
        A[c], A[p] = A[p], A[c]
        piv = A[c][c]
        A[c] = [x / piv for x in A[c]]
        for r in range(N):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return [row[N:] for row in A]


def violators_box(X, limit=400000):
    """Complete by Cauchy-Schwarz: u^T X u < X00 implies u_i^2 < X00 (X^-1)_ii.
    Returns None if the box is larger than limit."""
    N = len(X)
    Xi = inverse(X)
    ranges = []
    for i in range(N):
        b2 = X[0][0] * Xi[i][i]
        m = isqrt(floor(b2))
        if m * m == b2:
            m -= 1  # strict inequality
        vals = [k for k in range(-m, m + 1) if k % 2 == (1 if i == 0 else 0)]
        ranges.append(vals)
    size = 1
    for r in ranges:
        size *= max(1, len(r))
    if size > limit:
        return None
    out = set()
    for u in product(*ranges):
        if quad(X, u) < X[0][0]:
            out.add(tuple((ui - (i == 0)) // 2 for i, ui in enumerate(u)))
    return out


def theorem1_G(A, b, gamma2=None, h2=None):
    """Gram matrix of b0=(0,0,-2gamma,2h), b_i=(A_i,2e_i,0,0), b_g=(b,1,gamma,0), written out
    by hand from the vectors (general gamma^2, h^2). For gamma^2 = h^2 = n+1 this must equal
    the table printed in Theorem 1 (checked separately against that table)."""
    p, n = len(A), len(A[0])
    g2 = F(n + 1) if gamma2 is None else F(gamma2)
    hh = g2 if h2 is None else F(h2)
    N = n + 2
    G = [[F(0)] * N for _ in range(N)]
    G[0][0] = 4 * g2 + 4 * hh
    G[0][N - 1] = G[N - 1][0] = -2 * g2
    col = [[A[r][i] for r in range(p)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            G[1 + i][1 + j] = F(sum(x * y for x, y in zip(col[i], col[j])) + 4 * (i == j))
        G[1 + i][N - 1] = G[N - 1][1 + i] = F(sum(x * y for x, y in zip(col[i], b)) + 2)
    G[N - 1][N - 1] = F(sum(x * x for x in b) + n) + g2
    return G


def theorem1_table(A, b):
    """The integer matrix exactly as printed in Theorem 1 of the note."""
    p, n = len(A), len(A[0])
    N = n + 2
    G = [[0] * N for _ in range(N)]
    G[0][0] = 8 * (n + 1)
    G[0][N - 1] = G[N - 1][0] = -2 * (n + 1)
    for i in range(n):
        Ai = [A[r][i] for r in range(p)]
        for j in range(n):
            Aj = [A[r][j] for r in range(p)]
            G[1 + i][1 + j] = sum(x * y for x, y in zip(Ai, Aj)) + 4 * (i == j)
        G[1 + i][N - 1] = G[N - 1][1 + i] = sum(x * y for x, y in zip(Ai, b)) + 2
    G[N - 1][N - 1] = sum(x * x for x in b) + 2 * n + 1
    return G


def normalize(G):
    return [[F(x) / F(G[0][0]) for x in row] for row in G]


def zero_one_solutions(A, b):
    n = len(A[0])
    return [x for x in product((0, 1), repeat=n)
            if all(sum(A[r][i] * x[i] for i in range(n)) == b[r] for r in range(len(A)))]


def predicted(sols):
    return ({(0,) + tuple(-t for t in x) + (1,) for x in sols}
            | {(-1,) + tuple(x) + (-1,) for x in sols})


def egcd(a, b):
    if b == 0:
        return (abs(a), 1 if a >= 0 else -1, 0)
    g, x, y = egcd(b, a % b)
    return (g, y, x - (a // b) * y)


def column_hnf(M):
    """Integer M (r x N). Returns (MU, U, c): U unimodular N x N, the columns c.. of MU are 0,
    and the first c columns of MU are independent (c = rank M)."""
    r, N = len(M), len(M[0])
    A = [list(row) for row in M]
    U = [[int(i == j) for j in range(N)] for i in range(N)]

    def colop(c, j, x, y, s, t):  # new col c = x*col c + y*col j ; new col j = s*col c + t*col j
        for Mx in (A, U):
            for row in Mx:
                a, b = row[c], row[j]
                row[c], row[j] = x * a + y * b, s * a + t * b

    c = 0
    for i in range(r):
        if c >= N:
            break
        for j in range(c + 1, N):
            if A[i][j] != 0:
                a, b = A[i][c], A[i][j]
                g, x, y = egcd(a, b)
                colop(c, j, x, y, -b // g, a // g)
        if A[i][c] != 0:
            c += 1
    return A, U, c
