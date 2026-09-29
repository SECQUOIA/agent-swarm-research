"""Theorem 4 (rank one), Remark 1 (location), Section 6 identity, the rational-gamma remark,
and the pair-inequality observation for exact-cover instances."""
import random
import sys
from fractions import Fraction as F
from itertools import combinations, product
from math import gcd, isqrt, lcm

from tools import q, theorem1_G, theorem1_table, normalize, zero_one_solutions, predicted, violators_fp

random.seed(3)
fails = 0


def rank_one():
    """Brute force over a box; the box contains a minimizer because v_1..v_n in [0, D) hit every
    residue of p^T v mod D and v0 is then free (|v0| <= |p|_1 + 1 suffices)."""
    global fails
    bad = 0
    for _ in range(300):
        n = random.randint(1, 2)
        x = [F(random.randint(-9, 9), random.randint(1, 5)) for _ in range(n)]
        D = lcm(*[xi.denominator for xi in x])
        X = [[a * b for b in [F(1)] + x] for a in [F(1)] + x]
        p = [D] + [int(D * xi) for xi in x]
        g = 0
        for t in p:
            g = gcd(g, t)
        ok = g == 1
        R = sum(abs(t) for t in p) + 2
        best = min(q(X, (v0,) + w) for w in product(range(D), repeat=n) for v0 in range(-R, R + 1))
        ok &= best == min(F(0), -F(D * D // 4, D * D))
        ok &= best == -F((D // 2) * ((D + 1) // 2), D * D)
        ok &= (best < 0) == any(xi.denominator != 1 for xi in x)
        # identity q = m(m+D)/D^2 on random v
        for _ in range(20):
            v = [random.randint(-5, 5) for _ in range(n + 1)]
            m = sum(a * b for a, b in zip(p, v))
            ok &= q(X, v) == F(m * (m + D), D * D)
        # elementary split for a fractional coordinate
        for i, xi in enumerate(x):
            if xi.denominator != 1:
                fl = xi.numerator // xi.denominator
                v = [0] * (n + 1)
                v[0], v[1 + i] = -fl - 1, 1  # (x_i <= fl) or (x_i >= fl+1)
                ok &= q(X, v) < 0
        # criterion (c) for a scaled integer vector p' = kappa p
        kappa = random.choice([-3, -2, -1, 1, 2, 5])
        pp = [kappa * t for t in p]
        gp = 0
        for t in pp:
            gp = gcd(gp, t)
        Xp = [[F(a * b, pp[0] ** 2) for b in pp] for a in pp]
        ok &= Xp == X and ((abs(pp[0]) >= 2 * gp) == (best < 0))
        bad += not ok
    print(f"[Theorem 4] 300 random l(x), n <= 2: {bad} failures (gcd(p)=1, max violation, criterion, identity, (c))")
    fails += bad


def de_meijer_ok(X, k_gonal=False):
    """Inequalities of de Meijer et al. as printed: X is the full (n+1)x(n+1) matrix, x = X[0][1:],
    Y = X[1:][1:] (their X). (4.1) without linear constraints: diag(Y) >= x, >= -x, <= 1
    (PSD is checked separately). (2.1)-(2.2) triangle, (2.3) pair, (4.5)-(4.8) RLT, optional (4.4)."""
    x = X[0][1:]
    Y = [row[1:] for row in X[1:]]
    m = len(x)
    res = {}
    res['4.1'] = all(Y[i][i] >= x[i] and Y[i][i] >= -x[i] and Y[i][i] <= 1 for i in range(m))
    tri = True
    for i, j, k in combinations(range(m), 3):
        a, b, c = Y[i][j], Y[i][k], Y[j][k]
        tri &= a + b + c >= -1 and -a + b - c >= -1 and a - b - c >= -1 and -a - b + c >= -1
    res['2.1-2.2'] = tri
    res['2.3'] = all(Y[i][j] <= Y[i][i] and Y[i][j] >= -Y[i][i] for i in range(m) for j in range(m) if i != j)
    rlt = True
    for i, j in combinations(range(m), 2):
        rlt &= (Y[i][j] + x[i] + x[j] >= -1 and Y[i][j] - x[i] - x[j] >= -1
                and -Y[i][j] + x[i] - x[j] >= -1 and -Y[i][j] - x[i] + x[j] >= -1)
    res['4.5-4.8'] = rlt
    if k_gonal:
        ok = True
        for size in range(3, m + 1, 2):
            for S in combinations(range(m), size):
                for signs in product((1, -1), repeat=size - 1):
                    s = (1,) + signs
                    val = sum(s[a] * s[b] * Y[S[a]][S[b]] for a, b in combinations(range(size), 2))
                    ok &= val >= -(size // 2)
        res['4.4'] = ok
    return res


def location():
    global fails
    # subset-sum instances with s != 0 and X3C instances
    inst = []
    for n in (1, 2, 3):
        for a in product(range(1, 6), repeat=n):
            if list(a) == sorted(a):
                inst += [([list(a)], [s]) for s in range(1, sum(a) + 2)]
    x3c = []
    for _ in range(60):
        qq = random.choice([2, 3])
        U = list(range(3 * qq))
        sets = [tuple(sorted(random.sample(U, 3))) for _ in range(random.randint(0, 3))]
        if random.random() < 0.5:
            random.shuffle(U)
            sets += [tuple(sorted(U[3 * j:3 * j + 3])) for j in range(qq)]
        if not sets:
            sets = [tuple(U[:3])]
        x3c.append(([[int(e in S) for S in sets] for e in range(3 * qq)], [1] * (3 * qq)))
    counts = {}
    bad = 0
    x3c_pair_fail = 0
    ss_pair_fail = 0
    for kind, lst in (("ss", inst), ("x3c", x3c)):
        for A, b in lst:
            n = len(A[0])
            G = theorem1_table(A, b)
            Ghat = max(abs(G[i][j]) for i in range(n + 2) for j in range(n + 2) if (i, j) != (0, 0))
            h2 = F(3 * Ghat, 4)
            X = normalize(theorem1_G(A, b, h2=h2))
            # entries of X - l(0) are < Ghat/(4h^2) = 1/3 in absolute value
            ok = all(abs(X[i][j] - (1 if i == j == 0 else 0)) < F(1, 3) for i in range(n + 2) for j in range(n + 2))
            ok &= violators_fp(X, zero_first=True) == predicted(zero_one_solutions(A, b))
            r = de_meijer_ok(X)
            ok &= r['4.1'] and r['2.1-2.2'] and r['4.5-4.8']
            if not r['2.3']:
                if kind == "x3c":
                    x3c_pair_fail += 1
                else:
                    ss_pair_fail += 1
            bad += not ok
            counts[kind] = counts.get(kind, 0) + 1
    print(f"[Remark 1, 4h^2 = 3 Ghat] {counts['ss']} subset-sum (s != 0) + {counts['x3c']} X3C instances: "
          f"{bad} failures of (4.1), (2.1)-(2.2), (4.5)-(4.8), |X - l(0)| < 1/3, violated set")
    print(f"    pair inequalities (2.3) fail on {ss_pair_fail} subset-sum instances and on {x3c_pair_fail} X3C instances")
    fails += bad + x3c_pair_fail
    # the note's example a = (1, 6)
    X = normalize(theorem1_table([[1, 6]], [6]))
    ok = X[1][2] == F(1, 4) and X[1][1] == F(5, 24)
    print(f"    a = (1,6): X12 = {X[1][2]}, X11 = {X[1][1]} -> {'OK' if ok else 'FAIL'}")
    fails += not ok
    # b = 0 breaks diag(X) >= |x| at index g (G_gg - |G_0g| = |b|^2 - 1)
    X = normalize(theorem1_table([[1, 2]], [0]))
    ok = X[3][3] < abs(X[0][3])
    print(f"    b = 0 example a=(1,2), s=0: X_gg = {X[3][3]} < |X_0g| = {abs(X[0][3])} -> {'as stated' if ok else 'FAIL'}")
    fails += not ok
    # stronger placement: 4h^2 >= (n+1) Ghat also gives all (4.4) generalized triangle inequalities
    bad4 = cnt4 = 0
    for A, b in x3c[:25] + inst[:60]:
        n = len(A[0])
        if n + 1 > 7:
            continue
        G = theorem1_table(A, b)
        Ghat = max(abs(G[i][j]) for i in range(n + 2) for j in range(n + 2) if (i, j) != (0, 0))
        X = normalize(theorem1_G(A, b, h2=F((n + 1) * Ghat, 4)))
        r = de_meijer_ok(X, k_gonal=True)
        cnt4 += 1
        bad4 += not (r['4.4'] and r['4.1'] and r['2.1-2.2'] and r['4.5-4.8'])
        bad4 += violators_fp(X, zero_first=True) != predicted(zero_one_solutions(A, b))
    print(f"[observation] 4h^2 = (n+1) Ghat: {cnt4} instances satisfy all (4.4) as well: {bad4} failures")
    fails += bad4
    # slack bound: valid inequality <A', X> >= beta with slack eps at l(0); h^2 >= |A'|_1 Ghat / (4 eps)
    badS = 0
    for A, b in inst[:80]:
        n = len(A[0])
        N = n + 2
        G = theorem1_table(A, b)
        Ghat = max(abs(G[i][j]) for i in range(N) for j in range(N) if (i, j) != (0, 0))
        for _ in range(5):
            Ap = [[F(0)] * N for _ in range(N)]
            for i in range(N):
                for j in range(i, N):
                    Ap[i][j] = Ap[j][i] = F(random.randint(-3, 3))
            eps = F(random.randint(1, 5), random.randint(1, 5))
            beta = Ap[0][0] - eps  # <A', l(0)> - eps
            A1 = sum(abs(a) for row in Ap for a in row)
            if A1 == 0:
                continue
            h2 = max(A1 * Ghat / (4 * eps), F(n + 1, 8))
            X = normalize(theorem1_G(A, b, h2=h2))
            badS += sum(Ap[i][j] * X[i][j] for i in range(N) for j in range(N)) < beta
    print(f"[Remark 1 slack bound] 400 random (A', eps): {badS} failures")
    fails += badS


def binary_identity():
    global fails
    bad = 0
    for _ in range(500):
        N = random.randint(2, 6)
        X = [[F(0)] * N for _ in range(N)]
        for i in range(N):
            for j in range(i, N):
                X[i][j] = X[j][i] = F(random.randint(-7, 7), random.randint(1, 6))
        X[0][0] = F(1)
        for i in range(1, N):
            X[i][i] = X[0][i]
        s = random.randint(-4, 4)
        w = [random.randint(-4, 4) for _ in range(N - 1)]
        v = [-s - 1] + w
        sigma = 2 * s + 1
        bvec = [sigma - sum(w)] + w
        d = lambda i, j: X[0][j] if i == 0 else X[i][i] + X[j][j] - 2 * X[i][j]
        lhs = sum(bvec[i] * bvec[j] * d(i, j) for i, j in combinations(range(N), 2))
        bad += q(X, v) != F(sigma * sigma - 1, 4) - lhs
        bad += sum(bvec) != sigma
    # affine span claim: {l(x) : x in {0,1}^n} spans an affine space of dimension n + C(n,2)
    from check_membership_rank import rank
    for n in range(1, 6):
        pts = []
        for x in product((0, 1), repeat=n):
            c = (1,) + x
            pts.append([c[i] * c[j] for i in range(n + 1) for j in range(i, n + 1)])
        diffs = [[a - b for a, b in zip(p, pts[0])] for p in pts[1:]] or [[0]]
        bad += rank(diffs) != n + n * (n - 1) // 2
    print(f"[Section 6] 500 random X with X_ii = X_0i: split = rounded psd identity; affine-span dims n<=5: {bad} failures")
    fails += bad


def rational_gamma():
    global fails
    bad = 0
    for n in list(range(1, 20001)) + [10 ** 12 + k for k in range(50)] + [k * k for k in range(1, 300)]:
        c = isqrt(n) + 1
        g = (F(c) + F(n, c)) / 2
        e = g * g - n
        bad += not (0 < e < 1) or e != F((c * c - n) ** 2, 4 * c * c)
    print(f"[rational gamma] gamma = (c + n/c)/2, c = floor(sqrt n)+1: gamma^2 - n in (0,1) for all tested n: {bad} failures")
    fails += bad
    # the rational-gamma route end to end (explicit rational vectors, h = gamma)
    bad = 0
    for _ in range(60):
        n = random.randint(1, 4)
        a = [random.randint(0, 6) for _ in range(n)]
        s = random.randint(0, sum(a) + 1)
        c = isqrt(n) + 1
        g = (F(c) + F(n, c)) / 2
        h = g
        b0 = [F(0), *[F(0)] * n, -2 * g, 2 * h]
        bi = [[F(a[i]), *[F(2 * (k == i)) for k in range(n)], F(0), F(0)] for i in range(n)]
        bg = [F(s), *[F(1)] * n, g, F(0)]
        B = [b0] + bi + [bg]
        Gm = [[sum(x * y for x, y in zip(u, w)) for w in B] for u in B]
        X = normalize(Gm)
        bad += violators_fp(X, zero_first=True) != predicted(zero_one_solutions([a], [s]))
    print(f"[rational gamma route, explicit rational vectors] 60 subset-sum instances: {bad} failures")
    fails += bad


if __name__ == "__main__":
    rank_one()
    location()
    binary_identity()
    rational_gamma()
    print("ALL OK" if fails == 0 else f"FAILURES: {fails}")
    sys.exit(1 if fails else 0)
