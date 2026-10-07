"""Exact checks for research-20261001/binary-separation/note.md (standard library only).

All arithmetic is exact (fractions.Fraction). Violator sets are computed completely
by Fincke-Pohst enumeration over an exact LDL^T factorization, not by a box search.

Notation (see note.md, Section 2).
  Exact-cover instance: sets S_1..S_n of the universe [p], p >= 2.
  M (order n+1, indices 0..n-1 for the sets and n for the extra point g):
      M_ij = 4 delta_ij + |S_i & S_j|,  M_ig = |S_i|/2,  M_gg = p/4 + eta2.
  Hypermetric correlation form: g_M(z) = z^T M z - sum_i M_ii z_i.
  Cut form: d on V = {0} u [n] u {g}: d_0i = M_ii, d_ij = M_ii + M_jj - 2 M_ij.
  Hypermetric inequality for b in Z^V with sum b = 1:  Q(b, d) = sum_{u<v} b_u b_v d_uv <= 0.
  Q(b, d) = -g_M(z) for b = (1 - sum z, z).

Checks
  1. closed form    g_M(x, k) formula of Lemma 1 on random integer points
  2. theorem        violators of g_M are exactly (x, -1), x an exact cover, value
                    -(p/2 - 2 eta2); random exact-cover and X3C instances, eta2 = (p-1)/4
                    and the variant eta2 = (p-2)/4 (p >= 4)
  3. cut form       Q(b, d) = -g_M(z); integrality of 4d; triangle inequalities of d hold
                    iff no exact cover uses <= 2 sets
  4. binary point   X(eps) = [[1, eps*delta^T], [eps*delta, eps*M]], eps = 1/(2 delta^T M^-1 delta),
                    is positive definite, has X_ii = X_0i; ALL violated splits u^T X u < 1
                    (u0 odd, rest even) are hypermetric (|u0| = 1) and correspond to exact
                    covers; the cut image is eps*d; triangle inequalities hold iff no exact
                    cover uses <= 2 sets; perimeter inequalities always hold
  5. gonality       for X3C every violator has gonality 2q - 1 and support q + 2
  6. pure version   with q - 2 copies of point 0 the pure vector b' violates by 1/2
  7. controls       eta2 >= p/4: no violators even with a cover; eta2 small: extra
                    violators with k <= -2
"""
import random
import sys
from fractions import Fraction as F
from itertools import combinations, product
from math import ceil, floor, isqrt

random.seed(20261001)


# ------------------------------------------------------------------ linear algebra
def ldl_rev(X):
    """z^T X z = sum_i d_i (z_i + sum_{j<i} mu_ij z_j)^2, or None if X is not positive definite."""
    N = len(X)
    A = [[F(x) for x in row] for row in X]
    d, mu = [None] * N, [[F(0)] * N for _ in range(N)]
    for i in reversed(range(N)):
        d[i] = A[i][i]
        if d[i] <= 0:
            return None
        for j in range(i):
            mu[i][j] = A[i][j] / d[i]
        for j in range(i):
            for k in range(i):
                A[j][k] -= A[j][i] * A[i][k] / d[i]
    return d, mu


def solve(M, rhs):
    """Exact solution of M y = rhs (M nonsingular)."""
    N = len(M)
    A = [[F(M[i][j]) for j in range(N)] + [F(rhs[i])] for i in range(N)]
    for c in range(N):
        piv = next(r for r in range(c, N) if A[r][c] != 0)
        A[c], A[piv] = A[piv], A[c]
        for r in range(N):
            if r != c and A[r][c] != 0:
                f = A[r][c] / A[c][c]
                A[r] = [a - f * b for a, b in zip(A[r], A[c])]
    return [A[i][N] / A[i][i] for i in range(N)]


def quad(X, u):
    N = len(X)
    return sum(u[i] * X[i][j] * u[j] for i in range(N) for j in range(N))


def ellipsoid_points(X, center, R, parity=None, strict=True):
    """All integer u with (u - center)^T X (u - center) < R (<= R if not strict).
    X positive definite; parity[i] in {None, 0, 1} restricts u_i mod 2."""
    d, mu = ldl_rev(X)
    N, u, out = len(X), [0] * len(X), []

    def rec(i, rem):
        if i == N:
            out.append(tuple(u))
            return
        c = center[i] - sum((mu[i][j] * (u[j] - center[j]) for j in range(i)), F(0))
        r = isqrt(floor(rem / d[i])) + 1
        for ui in range(floor(c) - r, ceil(c) + r + 1):
            if parity is not None and parity[i] is not None and (ui - parity[i]) % 2:
                continue
            t = d[i] * (ui - c) ** 2
            if t < rem or (not strict and t == rem):
                u[i] = ui
                rec(i + 1, rem - t)
        u[i] = 0

    rec(0, F(R))
    return out


# ------------------------------------------------------------------ construction
def build_M(sets, p, eta2):
    n = len(sets)
    N = n + 1
    M = [[F(0)] * N for _ in range(N)]
    for i in range(n):
        for j in range(n):
            M[i][j] = F(4 * (i == j) + len(set(sets[i]) & set(sets[j])))
        M[i][n] = M[n][i] = F(len(sets[i]), 2)
    M[n][n] = F(p, 4) + F(eta2)
    return M


def g_M(M, z):
    return quad(M, z) - sum(M[i][i] * z[i] for i in range(len(M)))


def hyp_violators(M):
    """All z in Z^N with g_M(z) < 0, M positive definite (complete list)."""
    N = len(M)
    w = solve(M, [M[i][i] / 2 for i in range(N)])  # g_M(z) = (z-w)^T M (z-w) - w^T M w
    R = quad(M, w)
    out = ellipsoid_points(M, w, R)
    assert all(g_M(M, z) < 0 for z in out)
    return out


def exact_covers(sets, p):
    n = len(sets)
    sols = []
    for x in product((0, 1), repeat=n):
        cnt = [0] * p
        for i in range(n):
            if x[i]:
                for e in sets[i]:
                    cnt[e] += 1
        if all(c == 1 for c in cnt):
            sols.append(x)
    return sols


def distances(M):
    """Cut-form distance on V = {0, 1..N}: index 0 is the point 0, index i+1 is variable i."""
    N = len(M)
    D = [[F(0)] * (N + 1) for _ in range(N + 1)]
    for i in range(N):
        D[0][i + 1] = D[i + 1][0] = M[i][i]
        for j in range(N):
            if i != j:
                D[i + 1][j + 1] = M[i][i] + M[j][j] - 2 * M[i][j]
    return D


def Q(b, D):
    V = len(D)
    return sum(b[u] * b[v] * D[u][v] for u in range(V) for v in range(u + 1, V))


def triangle_ok(D):
    V = len(D)
    for i, j, k in combinations(range(V), 3):
        a, b_, c = D[i][j], D[i][k], D[j][k]
        if a > b_ + c or b_ > a + c or c > a + b_:
            return False
    return True


def perimeter_ok(D):
    V = len(D)
    return all(D[i][j] + D[i][k] + D[j][k] <= 2 for i, j, k in combinations(range(V), 3))


# ------------------------------------------------------------------ instances
def random_exact_cover(p, nmin=2, nmax=7, plant=None):
    U = list(range(p))
    sets = []
    if plant is None:
        plant = random.random() < 0.5
    if plant:  # random partition of U into blocks of size 1..3
        random.shuffle(U)
        k = 0
        while k < p:
            s = random.randint(1, 3)
            sets.append(tuple(sorted(U[k:k + s])))
            k += s
    target = random.randint(nmin, nmax)
    while len(sets) < target:
        s = random.randint(1, min(3, p))
        sets.append(tuple(sorted(random.sample(range(p), s))))
    random.shuffle(sets)
    return sets


def random_x3c(q, extra=None):
    p = 3 * q
    U = list(range(p))
    sets = [tuple(sorted(random.sample(U, 3))) for _ in range(random.randint(1, 4) if extra is None else extra)]
    if random.random() < 0.5:
        random.shuffle(U)
        sets += [tuple(sorted(U[3 * k:3 * k + 3])) for k in range(q)]
    random.shuffle(sets)
    return sets, p


# ------------------------------------------------------------------ checks
def check_closed_form(trials=300):
    bad = 0
    for _ in range(trials):
        p = random.randint(2, 6)
        sets = random_exact_cover(p)
        eta2 = F(random.randint(0, 40), random.randint(1, 9))
        M = build_M(sets, p, eta2)
        n = len(sets)
        x = [random.randint(-3, 3) for _ in range(n)]
        k = random.randint(-4, 4)
        y = [sum(x[i] for i in range(n) if e in sets[i]) for e in range(p)]
        rhs = 4 * sum(xi * (xi - 1) for xi in x) + sum(ye * ye + (k - 1) * ye for ye in y) \
            + (k * k - k) * (F(p, 4) + eta2)
        bad += g_M(M, x + [k]) != rhs
    print(f"[closed form] {trials} random (instance, eta2, x, k): {bad} mismatches")
    return bad == 0


def check_instance(sets, p, eta2, expect_value):
    M = build_M(sets, p, eta2)
    assert ldl_rev(M) is not None, "M not positive definite"
    viol = sorted(hyp_violators(M))
    covers = exact_covers(sets, p)
    want = sorted(tuple(x) + (-1,) for x in covers)
    ok = viol == want and all(g_M(M, z) == expect_value for z in viol)
    return ok, M, viol, covers


def check_theorem():
    ok_all = True
    stats = {}
    for label, gen, eta in [
        ("exact cover, p=2..6, eta2=(p-1)/4", lambda: (lambda p: (random_exact_cover(p), p))(random.randint(2, 6)), lambda p: F(p - 1, 4)),
        ("exact cover, p=4..6, eta2=(p-2)/4", lambda: (lambda p: (random_exact_cover(p), p))(random.randint(4, 6)), lambda p: F(p - 2, 4)),
        ("X3C q=2, eta2=(p-1)/4", lambda: random_x3c(2), lambda p: F(p - 1, 4)),
        ("X3C q=3, eta2=(p-1)/4", lambda: random_x3c(3), lambda p: F(p - 1, 4)),
        ("X3C q=3, eta2=(p-2)/4", lambda: random_x3c(3), lambda p: F(p - 2, 4)),
    ]:
        cnt = solv = bad = maxn = 0
        T = 120 if "q=3" in label else 200
        for _ in range(T):
            sets, p = gen()
            e2 = eta(p)
            ok, M, viol, covers = check_instance(sets, p, e2, -(F(p, 2) - 2 * e2))
            cnt += 1
            solv += bool(covers)
            bad += not ok
            maxn = max(maxn, len(sets))
        stats[label] = (cnt, solv, bad, maxn)
        ok_all &= bad == 0
        print(f"[theorem] {label}: {cnt} instances ({solv} with an exact cover, n <= {maxn}): {bad} failures")
    return ok_all


def check_cut_form(trials=200):
    bad_id = bad_tri = bad_int = 0
    for _ in range(trials):
        p = random.randint(2, 6)
        sets = random_exact_cover(p)
        M = build_M(sets, p, F(p - 1, 4))
        D = distances(M)
        bad_int += any((4 * D[u][v]).denominator != 1 for u in range(len(D)) for v in range(len(D)))
        small = any(sum(x) <= 2 for x in exact_covers(sets, p))
        bad_tri += triangle_ok(D) == small  # triangle inequalities hold iff no exact cover with <= 2 sets
        n1 = len(M)
        for _ in range(20):
            z = [random.randint(-3, 3) for _ in range(n1)]
            b = [1 - sum(z)] + z
            bad_id += Q(b, D) != -g_M(M, z)
    print(f"[cut form] {trials} instances: identity Q(b,d) = -g_M(z) on 20 random b each: {bad_id} failures; "
          f"4d integral: {bad_int} failures; triangle inequalities hold iff no exact cover uses <= 2 sets: {bad_tri} failures")
    return bad_id == bad_tri == bad_int == 0


def binary_point(M):
    """X(eps) with eps = 1 / (2 delta^T M^{-1} delta), delta = diag(M)."""
    N = len(M)
    delta = [M[i][i] for i in range(N)]
    s = sum(a * b for a, b in zip(delta, solve(M, delta)))
    eps = 1 / (2 * s)
    X = [[F(1)] + [eps * delta[j] for j in range(N)]]
    for i in range(N):
        X.append([eps * delta[i]] + [eps * M[i][j] for j in range(N)])
    return X, eps


def split_violators(X):
    """All u in e0 + 2 Z^{N} with u^T X u < X00 (complete), returned as v = (u - e0)/2."""
    N = len(X)
    pts = ellipsoid_points(X, [F(0)] * N, X[0][0], parity=[1] + [0] * (N - 1))
    return sorted(tuple((u[k] - (k == 0)) // 2 for k in range(N)) for u in pts)


def check_binary_point():
    bad = cnt = solv = 0
    for trial in range(80):
        if trial < 50:
            p = random.randint(2, 5)
            sets = random_exact_cover(p, nmax=6)
        else:
            sets, p = random_x3c(2, extra=random.randint(1, 3))
        M = build_M(sets, p, F(p - 1, 4))
        X, eps = binary_point(M)
        N = len(X)
        okpd = ldl_rev(X) is not None
        okbin = all(X[i][i] == X[0][i] for i in range(1, N))
        # X - (1/4) e0 e0^T is PD: then u^T X u > u0^2/4 >= 9/4 > 1 whenever |u0| >= 3
        Y = [row[:] for row in X]
        Y[0][0] -= F(1, 4)
        okmargin = ldl_rev(Y) is not None
        viol = split_violators(X)
        covers = exact_covers(sets, p)
        want = sorted([(0,) + tuple(-c for c in x) + (1,) for x in covers]
                      + [(-1,) + tuple(x) + (-1,) for x in covers])
        # cut image on {0} u [N-1]: y_0i = X_ii, y_ij = X_ii + X_jj - 2 X_ij
        Dn = [[F(0)] * N for _ in range(N)]
        for i in range(1, N):
            Dn[0][i] = Dn[i][0] = X[i][i]
            for j in range(1, N):
                if i != j:
                    Dn[i][j] = X[i][i] + X[j][j] - 2 * X[i][j]
        D = distances(M)
        okscale = all(Dn[i][j] == eps * D[i][j] for i in range(N) for j in range(N))
        small = any(sum(x) <= 2 for x in covers)
        oktri = (triangle_ok(Dn) != small) and perimeter_ok(Dn)
        okbox = all(0 <= Dn[i][j] <= 1 for i in range(N) for j in range(N))
        # elliptope: J - 2 eps D is positive definite (equivalent to X(eps) PD)
        okell = ldl_rev([[1 - 2 * Dn[i][j] for j in range(N)] for i in range(N)]) is not None
        # split value at violators: q = eps * g_M(z) = -eps/2
        okval = all((quad(X, [2 * v[0] + 1] + [2 * t for t in v[1:]]) - 1) / 4 == -eps / 2 for v in viol)
        ok = okpd and okbin and okmargin and viol == want and oktri and okbox and okval and okscale and okell
        cnt += 1
        solv += bool(covers)
        bad += not ok
        if not ok:
            print("  FAIL", sets, p, okpd, okbin, okmargin, viol == want, oktri, okbox, okval, okscale, okell)
    print(f"[binary point] {cnt} instances ({solv} with an exact cover): X(eps) positive definite, X_ii = X_0i, "
          f"X - e0e0^T/4 PD, all violated splits = hypermetric ones from exact covers, value -eps/2, "
          f"cut image = eps*d in [0,1], J - 2 eps*D PD, perimeter inequalities hold, triangle inequalities hold iff no "
          f"exact cover uses <= 2 sets: {bad} failures")
    return bad == 0


def check_gonality():
    bad = cnt = 0
    for _ in range(150):
        q = random.choice([2, 3])
        sets, p = random_x3c(q)
        M = build_M(sets, p, F(p - 1, 4))
        for z in hyp_violators(M):
            b = [1 - sum(z)] + list(z)
            cnt += 1
            bad += (sum(abs(t) for t in b) != 2 * q - 1) or (sum(t != 0 for t in b) != q + 2 - (q == 2))
    print(f"[gonality] X3C q in {{2,3}}: {cnt} violators; gonality 2q-1 and support q+2 (q+1 if q=2): {bad} failures")
    return bad == 0


def check_pure():
    bad = cnt = 0
    for _ in range(60):
        q = random.choice([3, 4])
        sets, p = random_x3c(q, extra=random.randint(1, 2))
        M = build_M(sets, p, F(p - 1, 4))
        D = distances(M)
        covers = exact_covers(sets, p)
        V = len(D)
        c = q - 2  # copies of point 0 appended at the end
        D2 = [row[:] + [row[0]] * c for row in D]
        for _ in range(c):
            D2.append(D[0][:] + [F(0)] * c)
        for x in covers:
            b = [0] + list(x) + [-1] + [-1] * c
            cnt += 1
            pure = all(t in (-1, 0, 1) for t in b) and sum(b) == 1
            bad += not (pure and Q(b, D2) == F(1, 2) and triangle_ok(D2))
    print(f"[pure] X3C q in {{3,4}} with q-2 copies of point 0: {cnt} pure violators b in {{0,+-1}}, sum b = 1, "
          f"Q = 1/2, triangle inequalities hold: {bad} failures")
    return bad == 0


def check_controls():
    # eta2 >= p/4: never violated, even with an exact cover
    none_found = cnt = 0
    for _ in range(60):
        p = random.randint(2, 6)
        sets = random_exact_cover(p, plant=True)
        M = build_M(sets, p, F(p, 4))
        cnt += 1
        none_found += len(hyp_violators(M)) == 0
    # eta2 small: violators with k <= -2 appear (here: all sets = universe split in blocks, duplicated)
    extra = 0
    for _ in range(40):
        p = random.randint(4, 6)
        sets = random_exact_cover(p, plant=True)
        sets = sets + sets  # every element now covered exactly twice by x = 1
        M = build_M(sets, p, F(p, 16))
        extra += any(z[-1] <= -2 for z in hyp_violators(M))
    print(f"[controls] eta2 = p/4: {none_found}/{cnt} instances with a cover have no violator (expected all); "
          f"eta2 = p/16 on doubled instances: {extra}/40 have a violator with k <= -2 (expected all)")
    return none_found == cnt and extra == 40


def example():
    """The smallest example printed in the note: universe {0,1,2}, sets {0,1,2}, {0,1}, {2}."""
    sets, p = [(0, 1, 2), (0, 1), (2,)], 3
    M = build_M(sets, p, F(p - 1, 4))
    print("[example] 4M =", [[str(4 * a) for a in row] for row in M])
    print("[example] violators z:", sorted(hyp_violators(M)), " exact covers:", exact_covers(sets, p))
    D = distances(M)
    print("[example] 4d =", [[str(4 * a) for a in row] for row in D])
    X, eps = binary_point(M)
    print("[example] eps =", eps)
    return True


if __name__ == "__main__":
    results = [check_closed_form(), check_theorem(), check_cut_form(), check_binary_point(),
               check_gonality(), check_pure(), check_controls(), example()]
    print("ALL CHECKS PASSED" if all(results) else "SOME CHECK FAILED")
    sys.exit(0 if all(results) else 1)
