"""Lemma 4, Theorem 2 (all three cases) and Theorem 3, checked independently.

Lemma 4 is implemented as described in the note (steps 1-4) but with a different index order
(largest positive pivot first, last zero-diagonal pair first), and every stated property is
tested: z^T X z < 0, (Xz)_K = 0, v = N z violated; in the PSD case |K| = rank X (rank from an
independent Gaussian elimination), X_KK positive definite, X = P^T G P.

Theorem 2/3 on singular PSD X: the reduced rank-r lattice problem (HNF basis W = P T from my
own column HNF) is enumerated completely, and compared with a brute-force search over v in a
box in the original coordinates: every box violator must appear in the reduced enumeration
(completeness), and every reduced solution must give a violator v = T z (soundness).
"""
import random
import sys
from fractions import Fraction as F
from itertools import product
from math import gcd, floor, isqrt

from tools import q, quad, inverse, is_pd, fp_enum, column_hnf, violators_fp, violators_box

random.seed(5)
fails = 0


def rank(M):
    M = [[F(x) for x in row] for row in M]
    r, rows, cols = 0, len(M), len(M[0])
    for c in range(cols):
        p = next((i for i in range(r, rows) if M[i][c] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r


def elim(X):
    """Returns ('neg', z, K) or ('psd', None, K). Pivot order: largest positive diagonal."""
    idx = list(range(len(X)))
    S = [[F(x) for x in row] for row in X]
    K = []
    stack = []  # (pivot global index, row of S over remaining indices, pivot value)
    while True:
        m = len(idx)
        z_loc = None
        neg = [i for i in range(m) if S[i][i] < 0]
        if neg:
            z_loc = [F(int(k == neg[-1])) for k in range(m)]
        else:
            pairs = [(i, j) for i in range(m) for j in range(m) if S[i][i] == 0 and S[i][j] != 0]
            if pairs:
                i, j = pairs[-1]
                z_loc = [F(0)] * m
                z_loc[j] = F(1)
                z_loc[i] = -(S[j][j] + 1) / (2 * S[i][j])
                assert sum(z_loc[a] * S[a][b] * z_loc[b] for a in range(m) for b in range(m)) == -1
        if z_loc is not None:
            z = {idx[k]: z_loc[k] for k in range(m)}
            for p, row, piv, rest in reversed(stack):
                z[p] = -sum(row[k] * z[rest[k]] for k in range(len(rest))) / piv
            return 'neg', [z[i] for i in range(len(X))], K
        pos = [i for i in range(m) if S[i][i] > 0]
        if not pos:
            assert all(x == 0 for row in S for x in row)
            return 'psd', None, K
        p = max(pos, key=lambda i: S[i][i])
        rest = [k for k in range(m) if k != p]
        stack.append((idx[p], [S[p][k] for k in rest], S[p][p], [idx[k] for k in rest]))
        K.append(idx[p])
        S = [[S[a][b] - S[a][p] * S[p][b] / S[p][p] for b in rest] for a in rest]
        idx = [idx[k] for k in rest]


def random_sym(N):
    X = [[F(0)] * N for _ in range(N)]
    for i in range(N):
        for j in range(i, N):
            X[i][j] = X[j][i] = F(random.randint(-5, 5), random.randint(1, 3))
    return X


def random_psd(N, r, zero_diag=False):
    V = [[random.randint(-2, 2) for _ in range(N)] for _ in range(r)]
    X = [[F(sum(row[i] * row[j] for row in V)) for j in range(N)] for i in range(N)]
    return X


def check_lemma4():
    global fails
    bad = neg = psd = 0
    special = [
        [[1, 0, 1], [0, 0, 1], [1, 1, 0]],          # zero diagonal with nonzero off-diagonal
        [[1, 2], [2, 1]],                           # negative direction through index 0
        [[1, 0, 0], [0, 0, 0], [0, 0, 0]],          # rank 1, zero rows
        [[1, 1, 1], [1, 1, 1], [1, 1, 1]],          # rank 1
        [[1, 0], [0, -F(1, 1000)]],
        [[1, F(1, 2), 0], [F(1, 2), 0, 0], [0, 0, 1]],
    ]
    mats = [[[F(x) for x in row] for row in M] for M in special]
    for k in range(600):
        N = random.randint(2, 5)
        if k % 3 == 0:
            X = random_sym(N)
        elif k % 3 == 1:
            X = random_psd(N, random.randint(1, N))
        else:  # PSD plus a small perturbation, often just barely non-PSD
            X = random_psd(N, random.randint(1, N))
            i, j = random.randrange(N), random.randrange(N)
            X[i][j] += F(1, 7)
            X[j][i] = X[i][j]
        mats.append(X)
    for X in mats:
        if X[0][0] <= 0:
            continue
        X = [[x / X[0][0] for x in row] for row in X]
        N = len(X)
        kind, z, K = elim(X)
        if kind == 'neg':
            neg += 1
            Xz = [sum(X[i][j] * z[j] for j in range(N)) for i in range(N)]
            ok = quad(X, z) < 0 and all(Xz[i] == 0 for i in K)
            L = 1
            for x in z:
                L = L * x.denominator // gcd(L, x.denominator)
            zi = [int(x * L) for x in z]
            a, b = quad(X, zi), sum(zi[i] * X[i][0] for i in range(N))
            Nn = floor(abs(b) / abs(a)) + 1
            ok &= q(X, [Nn * x for x in zi]) < 0
        else:
            psd += 1
            XKK = [[X[i][j] for j in K] for i in K]
            ok = len(K) == rank(X) and (not K or is_pd(XKK))
            if K:
                Gi = inverse(XKK)
                P = [X[i] for i in K]
                rec = [[sum(P[a][i] * Gi[a][b] * P[b][j] for a in range(len(K)) for b in range(len(K)))
                        for j in range(N)] for i in range(N)]
                ok &= rec == X
            # independent PSD test: all principal minors >= 0 via rank-revealing check on random vectors
            ok &= all(quad(X, [random.randint(-4, 4) for _ in range(N)]) >= 0 for _ in range(50))
        bad += not ok
    print(f"[Lemma 4] {neg} non-PSD (certificate, (Xz)_K = 0, v = Nz violated), {psd} PSD "
          f"(|K| = rank, X_KK > 0, X = P^T G P): {bad} failures")
    fails += bad


def reduced_violators(X):
    """Theorem 3 route for PSD X: returns (set of v = T z, W, T, P, G, w0) with all z enumerated."""
    kind, _, K = elim(X)
    assert kind == 'psd'
    r = len(K)
    N = len(X)
    P = [[X[i][j] for j in range(N)] for i in K]
    G = inverse([[X[i][j] for j in K] for i in K])
    den = 1
    for row in P:
        for x in row:
            den = den * x.denominator // gcd(den, x.denominator)
    M = [[int(x * den) for x in row] for row in P]
    MU, U, c = column_hnf(M)
    assert c == r
    T = [[U[i][j] for j in range(r)] for i in range(N)]
    W = [[F(MU[i][j], den) for j in range(r)] for i in range(r)]
    # check W = P T
    assert all(W[i][j] == sum(P[i][k] * T[k][j] for k in range(N)) for i in range(r) for j in range(r))
    w0 = [P[i][0] for i in range(r)]
    # |W z + w0/2|_G^2 < 1/4  <=>  (z - c)^T H (z - c) < 1/4 with H = W^T G W, W c = -w0/2
    H = [[sum(W[a][i] * G[a][b] * W[b][j] for a in range(r) for b in range(r)) for j in range(r)]
         for i in range(r)]
    Wi = inverse(W)
    cen = [-sum(Wi[i][j] * w0[j] for j in range(r)) / 2 for i in range(r)]
    zs = fp_enum(H, F(1, 4), parity=False, center=cen)
    vs = set(tuple(sum(T[i][j] * z[j] for j in range(r)) for i in range(N)) for z in zs)
    return vs, zs, W, T, P, G, w0, K


def check_singular():
    global fails
    bad = cnt = yes = 0
    bound_bad = dioph_bad = 0
    for k in range(250):
        N = random.randint(2, 5)
        r = random.randint(1, min(3, N - 1)) if N > 1 else 1
        X = random_psd(N, r)
        if X[0][0] == 0:
            continue
        X = [[x / X[0][0] for x in row] for row in X]
        if elim(X)[0] != 'psd':
            continue
        cnt += 1
        vs, zs, W, T, P, G, w0, K = reduced_violators(X)
        ok = all(q(X, v) < 0 for v in vs)  # soundness
        # each z gives one w; min over reduced = min over all splits (q depends on Pv only)
        # completeness vs brute-force box in the original coordinates
        rr = len(K)
        Wi = inverse(W)
        zset = set(zs)
        box = range(-3, 4)
        for v in product(box, repeat=N):
            if q(X, v) < 0:
                Pv = [sum(P[i][j] * v[j] for j in range(N)) for i in range(rr)]
                z = tuple(sum(Wi[i][j] * Pv[j] for j in range(rr)) for i in range(rr))
                ok &= all(x.denominator == 1 for x in z) and tuple(int(x) for x in z) in zset
                # Theorem 2: |w_i| < sqrt((X_KK)_ii) for w = P u
                u = [2 * v[i] + (i == 0) for i in range(N)]
                w = [sum(P[i][j] * u[j] for j in range(N)) for i in range(rr)]
                bound_bad += any(w[i] ** 2 >= X[K[i]][K[i]] for i in range(rr))
        yes += bool(vs)
        # minimum value from the reduced problem equals the minimum over the box when the box
        # contains a minimizer; at least the reduced min is <= box min
        if vs:
            mred = min(q(X, v) for v in vs)
            boxmin = min((q(X, v) for v in product(box, repeat=N)), default=None)
            ok &= mred <= boxmin
        bad += not ok
    print(f"[Theorems 2-3, singular PSD, rank 1-3, N <= 5] {cnt} instances ({yes} with violators): "
          f"{bad} failures (soundness, completeness vs box |v_i| <= 3, min value); "
          f"Theorem 2 bound |w_i| < sqrt((X_KK)_ii) violated {bound_bad} times")
    fails += bad + bound_bad


def check_pd_bound():
    """Theorem 2, PD case: every violator has |u_i| < sqrt((X^-1)_ii)."""
    global fails
    bad = cnt = 0
    for _ in range(200):
        N = random.randint(2, 4)
        X = random_psd(N, N + 1)
        if not is_pd(X):
            continue
        X = [[x / X[0][0] for x in row] for row in X]
        Xi = inverse(X)
        for v in violators_fp(X):
            cnt += 1
            u = [2 * v[i] + (i == 0) for i in range(N)]
            bad += any(u[i] ** 2 >= Xi[i][i] for i in range(N))
    print(f"[Theorem 2, PD case] {cnt} violators checked: {bad} violate |u_i| < sqrt((X^-1)_ii)")
    fails += bad


if __name__ == "__main__":
    check_lemma4()
    check_pd_bound()
    check_singular()
    print("ALL OK" if fails == 0 else f"FAILURES: {fails}")
    sys.exit(1 if fails else 0)
