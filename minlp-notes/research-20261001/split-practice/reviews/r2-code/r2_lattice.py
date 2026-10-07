"""Review r2: test the revised exact lattice code against independent reference code.

System under test (imported from the stream): col_hnf, lll_rows_exact,
shorten_mod_kernel, thm3_exact, q_exact. All reference routines below are written
here and use only Python integers and Fractions:
  - column HNF by a different algorithm (smallest-entry Euclid), compared using
    uniqueness of the reduced lower-triangular column HNF;
  - exact Gram-Schmidt recomputed from scratch, lattice equality by solving for the
    integer transformation, Bareiss determinant;
  - brute-force shortest coset representative;
  - exact rational Fincke-Pohst minimum of q over Z^N via the image lattice.
Usage from split-practice/: python3 reviews/r2-code/r2_lattice.py [seed]
"""
import itertools
import math
import random
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'code'))
import lattice as SUT  # system under test only

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 20261003)


# ------------------------------------------------------------ reference code
def det_bareiss(A):
    A = [list(map(int, r)) for r in A]
    n = len(A); sign = 1; prev = 1
    for k in range(n - 1):
        if A[k][k] == 0:
            sw = next((i for i in range(k + 1, n) if A[i][k] != 0), None)
            if sw is None:
                return 0
            A[k], A[sw] = A[sw], A[k]; sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) // prev
        prev = A[k][k]
    return sign * A[n - 1][n - 1]


def ref_hnf(M):
    """Reduced lower-triangular column HNF H of a full-row-rank integer M (r x N)."""
    r, N = len(M), len(M[0])
    A = [row[:] for row in M]
    cols = lambda j: [A[i][j] for i in range(r)]

    def addcol(dst, src, m):
        for i in range(r):
            A[i][dst] += m * A[i][src]

    def swapcol(a, b):
        for i in range(r):
            A[i][a], A[i][b] = A[i][b], A[i][a]
    for i in range(r):
        while True:
            nz = [j for j in range(i, N) if A[i][j] != 0]
            if len(nz) <= 1:
                break
            p = min(nz, key=lambda j: abs(A[i][j]))
            for j in nz:
                if j != p:
                    addcol(j, p, -(A[i][j] // A[i][p]))
        j = next(j for j in range(i, N) if A[i][j] != 0)
        swapcol(i, j)
        if A[i][i] < 0:
            for k in range(r):
                A[k][i] = -A[k][i]
        for j in range(i):
            addcol(j, i, -(A[i][j] // A[i][i]))
    return [row[:r] for row in A]


def gso(rows):
    bs, norms, mu = [], [], []
    for i, row in enumerate(rows):
        b = [F(a) for a in row]; m = []
        for bj, nj in zip(bs, norms):
            c = sum(F(a) * x for a, x in zip(row, bj)) / nj
            m.append(c); b = [x - c * y for x, y in zip(b, bj)]
        bs.append(b); norms.append(sum(x * x for x in b)); mu.append(m)
    return bs, norms, mu


def solve_exact(A, b):
    """Solve A x = b for square nonsingular rational A."""
    n = len(A)
    M = [[F(x) for x in A[i]] + [F(b[i])] for i in range(n)]
    for c in range(n):
        p = next(i for i in range(c, n) if M[i][c] != 0)
        M[c], M[p] = M[p], M[c]
        for i in range(n):
            if i != c and M[i][c] != 0:
                f = M[i][c] / M[c][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def coords(rows, v):
    """Exact coordinates of v in the row basis `rows` (independent), or None."""
    k = len(rows)
    G = [[sum(a * b for a, b in zip(rows[i], rows[j])) for j in range(k)] for i in range(k)]
    rhs = [sum(a * b for a, b in zip(rows[i], v)) for i in range(k)]
    c = solve_exact(G, rhs)
    back = [sum(c[i] * rows[i][t] for i in range(k)) for t in range(len(v))]
    return c if back == [F(x) for x in v] else None


def same_lattice(B, C):
    """True if row bases B and C span the same integer lattice."""
    for row in C:
        c = coords(B, row)
        if c is None or any(x.denominator != 1 for x in c):
            return False
    for row in B:
        c = coords(C, row)
        if c is None or any(x.denominator != 1 for x in c):
            return False
    return True


def is_lll(rows, delta=F(3, 4)):
    _, norms, mu = gso(rows)
    size = all(abs(mu[i][j]) <= F(1, 2) for i in range(len(rows)) for j in range(i))
    lov = all(norms[i] >= (delta - mu[i][i - 1] ** 2) * norms[i - 1] for i in range(1, len(rows)))
    return size and lov


def shortest_coset(v, K, R):
    """Brute force min ||v + K c||^2 over integer c with |c_i| <= R (K rows)."""
    best = None
    for c in itertools.product(range(-R, R + 1), repeat=len(K)):
        w = [a + sum(ci * row[t] for ci, row in zip(c, K)) for t, a in enumerate(v)]
        n2 = sum(a * a for a in w)
        if best is None or n2 < best:
            best = n2
    return best


def ldl(A):
    n = len(A); L = [[F(int(i == j)) for j in range(n)] for i in range(n)]; D = [F(0)] * n
    for j in range(n):
        D[j] = A[j][j] - sum(L[j][k] ** 2 * D[k] for k in range(j))
        for i in range(j + 1, n):
            L[i][j] = (A[i][j] - sum(L[i][k] * L[j][k] * D[k] for k in range(j))) / D[j]
    return L, D


def ref_min_q(B, C):
    """Exact min over v in Z^N of q(v) for X = B^T C B (B integer r x N with full
    row rank, C rational PD r x r, X00 = 1): min_z (Hz + b0/2)^T C (Hz + b0/2) - 1/4."""
    r = len(B)
    H = ref_hnf(B)
    t = [F(-B[i][0], 2) for i in range(r)]
    A = [[sum(F(H[k][i]) * C[k][l] * H[l][j] for k in range(r) for l in range(r)) for j in range(r)] for i in range(r)]
    c = solve_exact(H, t)  # minimize (z - c)^T A (z - c)
    # Fincke-Pohst in exact arithmetic with A = L D L^T (L unit lower):
    # (z-c)^T A (z-c) = sum_k D_k (y_k + sum_{j>k} L_jk y_j)^2, y = z - c,
    # so enumerate k = r-1 (outermost) down to 0.
    L, D = ldl(A)
    best = [F(1, 4), None]  # q < 0 iff value < 1/4; value 1/4 means q = 0
    z = [0] * r

    def rec(k, partial):
        center = c[k] - sum(L[j][k] * (z[j] - c[j]) for j in range(k + 1, r))
        room = best[0] - partial
        if room < 0:
            return
        rad = math.sqrt(float(room / D[k])) + 1
        for zk in range(math.floor(center - rad), math.ceil(center + rad) + 1):
            val = partial + D[k] * (zk - center) ** 2
            if val <= best[0]:
                z[k] = zk
                if k == 0:
                    if best[1] is None or val < best[0]:
                        best[0], best[1] = val, z[:]
                else:
                    rec(k - 1, val)
    rec(r - 1, F(0))
    return best[0] - F(1, 4)


def q_ref(X, v):
    N = len(v)
    return sum(F(v[i]) * X[i][j] * v[j] for i in range(N) for j in range(N)) + sum(F(v[i]) * X[i][0] for i in range(N))


# ------------------------------------------------------------ tests
out = []
t0 = time.time()

# 1. column HNF
n_hnf = 0
for trial in range(300):
    r = rng.randint(1, 5); N = rng.randint(r, r + 5)
    big = rng.choice([5, 10**3, 10**8, 10**20])
    while True:
        M = [[rng.randint(-big, big) for _ in range(N)] for _ in range(r)]
        if det_bareiss([[sum(a * b for a, b in zip(M[i], M[j])) for j in range(r)] for i in range(r)]) != 0:
            break
    H, U = SUT.col_hnf(M)
    MU = [[sum(M[i][k] * U[k][j] for k in range(N)) for j in range(N)] for i in range(r)]
    assert all(MU[i][j] == (H[i][j] if j < r else 0) for i in range(r) for j in range(N)), 'M U != [H|0]'
    assert abs(det_bareiss(U)) == 1, 'U not unimodular'
    assert H == ref_hnf(M), 'HNF differs from reference'
    n_hnf += 1
out.append(f'col_hnf: {n_hnf} random matrices (entries up to 1e20): M U = [H|0], det U = +-1, H equals independent reduced HNF')

# 2. lll_rows_exact
n_lll = 0
for trial in range(120):
    kind = trial % 3
    if kind == 0:
        d = rng.randint(2, 7); m = d + rng.randint(0, 2)
        big = rng.choice([10, 10**6, 10**30])
        B = [[rng.randint(-big, big) for _ in range(m)] for _ in range(d)]
    elif kind == 1:  # graph lattice as in thm3_exact
        N = rng.randint(3, 8); r = rng.randint(1, 3)
        Mm = [[rng.randint(-10**6, 10**6) for _ in range(N)] for _ in range(r)]
        B = [[int(i == j) for j in range(N)] + [10**6 * Mm[k][i] for k in range(r)] for i in range(N)]
    else:  # nearly dependent rows
        d = rng.randint(2, 6)
        base = [rng.randint(-10**9, 10**9) for _ in range(d + 1)]
        B = [[b + rng.randint(-2, 2) for b in base] for _ in range(d)]
    _, norms, _ = gso(B)
    if any(x == 0 for x in norms):
        continue
    R = SUT.lll_rows_exact(B)
    assert same_lattice(B, R), 'lattice changed'
    assert is_lll(R), 'output not LLL-reduced (delta 3/4) by fresh GSO'
    n_lll += 1
out.append(f'lll_rows_exact: {n_lll} bases (random up to 1e30, graph lattices, near-dependent): same lattice, LLL(3/4) by fresh exact GSO')

# 3. shorten_mod_kernel
n_sh = opt_sh = 0; worst = F(1)
for trial in range(150):
    N = rng.randint(3, 6); k = rng.randint(1, min(3, N - 1))
    K0 = [[rng.randint(-3, 3) for _ in range(N)] for _ in range(k)]
    if any(x == 0 for x in gso(K0)[1]):
        continue
    # scramble with a unimodular matrix with large entries
    Kr = [row[:] for row in K0]
    for _ in range(6):
        i, j = rng.sample(range(k), 2) if k > 1 else (0, 0)
        if i != j:
            m = rng.randint(-10**8, 10**8)
            Kr[i] = [a + m * b for a, b in zip(Kr[i], Kr[j])]
    Kern = [[Kr[c][i] for c in range(k)] for i in range(N)]  # columns
    v = [rng.randint(-5, 5) + sum(rng.randint(-10**9, 10**9) * K0[c][i] for c in range(k)) for i in range(N)]
    v2 = SUT.shorten_mod_kernel(v, Kern)
    c = coords(K0, [a - b for a, b in zip(v2, v)])
    assert c is not None and all(x.denominator == 1 for x in c), 'coset changed'
    Kred = SUT.lll_rows_exact(K0)  # reduced basis just to bound the brute-force box
    best = shortest_coset(v2, Kred, 4)
    n2 = sum(a * a for a in v2)
    n_sh += 1; opt_sh += n2 == best
    worst = max(worst, F(n2, best) if best else F(1))
out.append(f'shorten_mod_kernel: {n_sh} cosets with scrambled 1e8 kernel bases and 1e9 representatives: coset preserved in all; '
           f'result equals brute-force shortest (box 4 in reduced coordinates) in {opt_sh}; worst squared-norm ratio {float(worst):.3f}')

# 4. thm3_exact against exact rational reference minimum
n_t = agree = 0; flagged = 0
for trial in range(160):
    r = rng.randint(1, 3); N = rng.randint(r + 1, 6)
    while True:
        B = [[rng.randint(-4, 4) for _ in range(N)] for _ in range(r)]
        if any(B[i][0] for i in range(r)) and det_bareiss([[sum(a * b for a, b in zip(B[i], B[j])) for j in range(r)] for i in range(r)]) != 0:
            break
    while True:
        Lm = [[F(rng.randint(-3, 3), rng.randint(1, 4)) for _ in range(r)] for _ in range(r)]
        C = [[sum(Lm[k][i] * Lm[k][j] for k in range(r)) + (F(1, 7) if i == j else 0) for j in range(r)] for i in range(r)]
        if det_bareiss([[int(x * 10**6) for x in row] for row in C]) != 0:
            break
    s = sum(F(B[i][0]) * C[i][j] * B[j][0] for i in range(r) for j in range(r))
    C = [[x / s for x in row] for row in C]
    X = [[sum(F(B[k][a]) * C[k][l] * B[l][b] for k in range(r) for l in range(r)) for b in range(N)] for a in range(N)]
    assert X[0][0] == 1
    ref = ref_min_q(B, C)
    ref = min(ref, F(0))
    res = SUT.thm3_exact(X)
    q = res['q']
    if res['v'] is not None:
        assert q_ref(X, res['v']) == q, 'returned q is not the exact value of returned v'
    n_t += 1; agree += q == ref
    flagged += not res['complete']
    if q != ref:
        out.append(f'  MISMATCH thm3 q={q} ref={ref} r={r} N={N}')
out.append(f'thm3_exact: {n_t} random rational psd matrices (rank 1-3, order 2-6): q equals independent exact minimum in {agree}; '
           f'returned v reproduces q exactly in all; incomplete flags {flagged}')

# 5. flags under a forced first-enumeration cap
X = [[F(1), F(1, 3), F(2, 7)], [F(1, 3), F(1, 9), F(2, 21)], [F(2, 7), F(2, 21), F(4, 49)]]
res = SUT.thm3_exact(X, max_nodes=1)
out.append(f'thm3_exact with max_nodes=1 on a rank-1 matrix: complete={res["complete"]}, first={res["first_complete"]}, '
           f'second={res["second_complete"]}, q={res["q"]}, certified={res["optimum_certified"]}')

out.append(f'time {time.time() - t0:.1f}s')
print('\n'.join(out))
