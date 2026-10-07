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
  4. binary point   X(eps) = [[1, eps*delta^T], [eps*delta, eps*M]], eps = 1/N with
                    N = 8n + 2p + 1 (revision r1; round 0 used eps = 1/(2 delta^T M^-1 delta)),
                    is positive definite, has X_ii = X_0i, eps*s < 1/2 for s = delta^T M^-1 delta,
                    4N*X is integral; ALL violated splits u^T X u < 1 (u0 odd, rest even) are
                    hypermetric (|u0| = 1), correspond to exact covers and have value -1/(2N);
                    the cut image is eps*d in [0,1] (also where triangle inequalities fail);
                    triangle inequalities hold iff no exact cover uses <= 2 sets; perimeter
                    inequalities always hold
  5. gonality       for X3C every violator has gonality 2q - 1 and support q + 2
  6. pure version   with q - 2 copies of point 0 the pure vector b' violates by 1/2
  7. controls       eta2 >= p/4: no violators even with a cover; eta2 small: extra
                    violators with k <= -2
  Added in revision r1 (run after the round-0 checks, so the round-0 random instances are unchanged):
  8. eps bound      s = delta^T M^-1 delta <= 4||c*||^2 = 4n + p + 1/(4(p-1)) for c* = (1_n, 1_p/2, gamma),
                    B^T c* = delta/2 (exact), s >= max_i M_ii; digit counts of the old eps = 1/(2s)
  9. window p/12    Theorem 1 at the sharp lower endpoint eta2 = p/12 (p in {2,3}); below it,
                    extra violators (x, -2) appear in yes-instances and in a no-instance
 10. Padberg (11)/(12)  at X(1/N) the violated inequalities of Letchford's family (12) (all
                    disjoint S, T and all integers s), found by complete enumeration, are exactly
                    S = exact cover, T = {g}, s = 0 (= Padberg cut inequality (11)), up to the
                    trivial relabelling (T, S, -1)
 11. facets         exact affine rank of the tight 0/1 points: (12) with |S| = q, |T| = 1, s = 0
                    defines a facet of BQP; (11) with |S| = 1, |T| >= 2 does not
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


def binary_point(M, p):
    """X(eps) with eps = 1/N, N = 8n + 2p + 1 (revision r1), delta = diag(M); also returns s.

    n = len(M) - 1 sets, p elements, eta2 = (p-1)/4.  Note: s <= 4n + p + 1/(4(p-1)) < N/2, so eps*s < 1/2."""
    N = len(M)
    n = N - 1
    delta = [M[i][i] for i in range(N)]
    s = sum(a * b for a, b in zip(delta, solve(M, delta)))
    eps = F(1, 8 * n + 2 * p + 1)
    X = [[F(1)] + [eps * delta[j] for j in range(N)]]
    for i in range(N):
        X.append([eps * delta[i]] + [eps * M[i][j] for j in range(N)])
    return X, eps, s


def split_violators(X):
    """All u in e0 + 2 Z^{N} with u^T X u < X00 (complete), returned as v = (u - e0)/2."""
    N = len(X)
    pts = ellipsoid_points(X, [F(0)] * N, X[0][0], parity=[1] + [0] * (N - 1))
    return sorted(tuple((u[k] - (k == 0)) // 2 for k in range(N)) for u in pts)


def check_binary_point():
    bad = cnt = solv = smallcov = 0
    for trial in range(80):
        if trial < 50:
            p = random.randint(2, 5)
            sets = random_exact_cover(p, nmax=6)
        else:
            sets, p = random_x3c(2, extra=random.randint(1, 3))
        M = build_M(sets, p, F(p - 1, 4))
        X, eps, s = binary_point(M, p)
        N = len(X)
        Nden = 8 * len(sets) + 2 * p + 1
        okeps = eps == F(1, Nden) and eps * s < F(1, 2)
        okint = all((4 * Nden * X[i][j]).denominator == 1 for i in range(N) for j in range(N))
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
        smallcov += small
        oktri = (triangle_ok(Dn) != small) and perimeter_ok(Dn)
        okbox = all(0 <= Dn[i][j] <= 1 for i in range(N) for j in range(N))
        # elliptope: J - 2 eps D is positive definite (equivalent to X(eps) PD)
        okell = ldl_rev([[1 - 2 * Dn[i][j] for j in range(N)] for i in range(N)]) is not None
        # split value at violators: q = eps * g_M(z) = -eps/2 = -1/(2N)
        okval = all((quad(X, [2 * v[0] + 1] + [2 * t for t in v[1:]]) - 1) / 4 == -F(1, 2 * Nden) for v in viol)
        ok = (okeps and okint and okpd and okbin and okmargin and viol == want and oktri and okbox and okval
              and okscale and okell)
        cnt += 1
        solv += bool(covers)
        bad += not ok
        if not ok:
            print("  FAIL", sets, p, okeps, okint, okpd, okbin, okmargin, viol == want, oktri, okbox, okval, okscale,
                  okell)
    print(f"[binary point] {cnt} instances ({solv} with an exact cover, {smallcov} with a cover of <= 2 sets): "
          f"eps = 1/(8n+2p+1), eps*s < 1/2, 4N*X integral, X(eps) positive definite, X_ii = X_0i, "
          f"X - e0e0^T/4 PD, all violated splits = hypermetric ones from exact covers, value -1/(2N), "
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
    X, eps, s = binary_point(M, p)
    print("[example] eps = 1/(8n+2p+1) =", eps, "; s = delta^T M^-1 delta =", s, "; old eps 1/(2s) =", 1 / (2 * s))
    return True


# ------------------------------------------------------------------ revision r1 checks
def check_eps_bound():
    """Review item M1: s = delta^T M^-1 delta satisfies max_i M_ii <= s <= 4||c*||^2 = 4n + p + 1/(4(p-1)),
    where c* = (1_n, 1_p/2, gamma), gamma = (eta2 - p/4)/(2 eta), satisfies B^T c* = delta/2.  Hence
    eps = 1/(8n + 2p + 1) gives eps*s < 1/2.  Also prints the digit counts of the round-0 eps = 1/(2s)."""
    bad = cnt = nmax_x3c = 0
    lines = []

    def one(sets, p):
        n = len(sets)
        eta2 = F(p - 1, 4)
        M = build_M(sets, p, eta2)
        X, eps, s = binary_point(M, p)
        # B^T c* = delta/2, checked exactly: u_i^T c* = 2 + |S_i|/2 and u_g^T c* = p/4 + eta*gamma = p/4 + (eta2 - p/4)/2
        okc = all(2 + F(len(S), 2) == M[i][i] / 2 for i, S in enumerate(sets)) \
            and F(p, 4) + (eta2 - F(p, 4)) / 2 == M[n][n] / 2
        cstar2 = n + F(p, 4) + (eta2 - F(p, 4)) ** 2 / (4 * eta2)   # ||c*||^2
        bound = 4 * n + p + F(1, 4 * (p - 1))
        ok = okc and 4 * cstar2 == bound and max(M[i][i] for i in range(n + 1)) <= s <= bound \
            and eps * s < F(1, 2)
        return ok, s, eps

    for q in [2, 3, 4, 5, 6, 8, 10]:
        for rep in range(6 if q <= 6 else 3):
            pp = 3 * q
            n = random.randint(q, 4 * q)
            U = list(range(pp))
            sets = [tuple(sorted(random.sample(U, 3))) for _ in range(n)]
            if rep % 2 == 0:
                random.shuffle(U)
                sets[:q] = [tuple(sorted(U[3 * k:3 * k + 3])) for k in range(q)]
            ok, s, eps = one(sets, pp)
            cnt += 1
            bad += not ok
            nmax_x3c = max(nmax_x3c, n)
            old = 1 / (2 * s)
            if rep == 0:
                lines.append(f"    X3C q={q:2d} n={n:2d}: s = {float(s):8.3f}, bound 4n+p+1/(4(p-1)) = {float(4*n+pp+F(1,4*(pp-1))):7.3f}; "
                             f"round-0 eps = 1/(2s) has {len(str(old.numerator))}/{len(str(old.denominator))} digits, "
                             f"new eps = {eps}")
    for _ in range(40):
        pp = random.randint(2, 8)
        sets = random_exact_cover(pp, nmax=10)
        ok, s, eps = one(sets, pp)
        cnt += 1
        bad += not ok
    # families where s stays bounded as n grows (review item m1)
    for n in (5, 20, 40):
        ok, s, eps = one([(0, 1, 2)] * n + [(3, 4, 5)], 6)
        cnt += 1
        bad += not ok
        lines.append(f"    n copies of {{0,1,2}} plus {{3,4,5}} (p = 6), n = {n}: s = {float(s):.3f}")
    for pp in (6, 9):
        sets = list(combinations(range(pp), 3))
        ok, s, eps = one(sets, pp)
        cnt += 1
        bad += not ok
        lines.append(f"    all triples of [{pp}] (n = {len(sets)}): s = {float(s):.3f}, s/(n+p) = {float(s / (len(sets) + pp)):.3f}")
    print(f"[eps bound] {cnt} instances (X3C with q <= 10 and n <= {nmax_x3c}; random exact cover p <= 8; bounded-s families): "
          f"B^T c* = delta/2, max M_ii <= s <= 4n + p + 1/(4(p-1)) = 4||c*||^2, eps*s < 1/2 for eps = 1/(8n+2p+1): "
          f"{bad} failures")
    print("\n".join(lines))
    return bad == 0


def check_window_p12():
    """Review item o1: Theorem 1 holds at the lower endpoint eta2 = p/12 (relevant only for p <= 3);
    for eta2 < p/12 every exact cover x gives the extra violator (x, -2), and the no-instance
    {0,1}, {1,2} (p = 3) gets the violator (1, 1, -2)."""
    bad = cnt = solv = 0
    for _ in range(100):
        p = random.choice([2, 3])
        sets = random_exact_cover(p, nmax=6)
        e2 = F(p, 12)
        ok, M, viol, covers = check_instance(sets, p, e2, -(F(p, 2) - 2 * e2))
        cnt += 1
        solv += bool(covers)
        bad += not ok
    extra = yes = 0
    for _ in range(40):
        p = random.choice([2, 3])
        sets = random_exact_cover(p, plant=True)
        M = build_M(sets, p, F(p, 12) - F(1, 100))
        V = set(hyp_violators(M))
        yes += 1
        extra += all(tuple(x) + (-2,) in V for x in exact_covers(sets, p))
    no_sets = [(0, 1), (1, 2)]
    okno = not exact_covers(no_sets, 3) and (1, 1, -2) in hyp_violators(build_M(no_sets, 3, F(3, 12) - F(1, 100)))
    print(f"[window p/12] eta2 = p/12, p in {{2,3}}: {cnt} instances ({solv} with an exact cover): {bad} failures of "
          f"Theorem 1; eta2 = p/12 - 1/100: {extra}/{yes} instances with a cover have the extra violators (x, -2) "
          f"(expected all); no-instance {{0,1}},{{1,2}} has violator (1,1,-2): {okno}")
    return bad == 0 and extra == yes and okno


def family12_violations(x, y):
    """All (S, T, s), S and T disjoint (S u T nonempty), s integer, violating Letchford's (12):
        s x(S) + y(S:T) <= (s+1) x(T) + y(E(S)) + y(E(T)) + s(s+1)/2.
    f(t) = LHS - RHS = -t^2/2 + t (x(S) - x(T) - 1/2) + (y(S:T) - x(T) - y(E(S)) - y(E(T))) is a concave
    quadratic, so all violated t satisfy (t - t*)^2 < 2 f(t*) with t* = x(S) - x(T) - 1/2: the list is complete."""
    N = len(x)
    out = {}
    for lab in product((0, 1, 2), repeat=N):
        S = tuple(i for i in range(N) if lab[i] == 1)
        T = tuple(i for i in range(N) if lab[i] == 2)
        if not S and not T:
            continue
        A = sum((x[i] for i in S), F(0))
        C = sum((x[i] for i in T), F(0))
        B = sum((y[i][j] for i in S for j in T), F(0))
        E = sum((y[i][j] for i, j in combinations(S, 2)), F(0)) + sum((y[i][j] for i, j in combinations(T, 2)), F(0))
        tstar = A - C - F(1, 2)
        fmax = tstar * tstar / 2 + B - C - E
        if fmax <= 0:
            continue
        r = isqrt(floor(2 * fmax)) + 1
        for t in range(floor(tstar) - r, ceil(tstar) + r + 1):
            f = t * A + B - (t + 1) * C - E - F(t * (t + 1), 2)
            if f > 0:
                out[(S, T, t)] = f
    return out


def check_padberg():
    """Review item m3: at X(1/N), the violated members of Letchford's (12) (which contains Padberg's cut
    inequalities (11) as s = 0) are exactly (S, T, s) = (cover, {g}, 0) and the same inequality written as
    ({g}, cover, -1); the violation of (12) is 1/(4N).  Independent of the ellipsoid enumeration."""
    bad = cnt = solv = 0
    for trial in range(60):
        if trial < 20:
            sets, p = random_x3c(3, extra=random.randint(1, 3))
        elif trial < 30:
            sets, p = random_x3c(4, extra=random.randint(1, 3))
        elif trial < 40:
            sets, p = random_x3c(2, extra=random.randint(1, 3))
        else:
            p = random.randint(2, 5)
            sets = random_exact_cover(p, nmax=6)
        n = len(sets)
        M = build_M(sets, p, F(p - 1, 4))
        X, eps, s = binary_point(M, p)
        Nv = len(X) - 1                      # variables 0..n-1 (sets) and n (= g)
        x = [X[i + 1][i + 1] for i in range(Nv)]
        y = [[X[i + 1][j + 1] for j in range(Nv)] for i in range(Nv)]
        viol = family12_violations(x, y)
        covers = exact_covers(sets, p)
        want = {}
        for c in covers:
            C = tuple(i for i in range(n) if c[i])
            want[(C, (n,), 0)] = eps / 4
            want[((n,), C, -1)] = eps / 4
        # Padberg (11) directly: y(S:T) <= x(T) + y(E(S)) + y(E(T))
        v11 = set()
        for lab in product((0, 1, 2), repeat=Nv):
            S = tuple(i for i in range(Nv) if lab[i] == 1)
            T = tuple(i for i in range(Nv) if lab[i] == 2)
            lhs = sum((y[i][j] for i in S for j in T), F(0))
            rhs = sum((x[i] for i in T), F(0)) + sum((y[i][j] for i, j in combinations(S, 2)), F(0)) \
                + sum((y[i][j] for i, j in combinations(T, 2)), F(0))
            if lhs > rhs:
                v11.add((S, T))
        want11 = {(S, T) for (S, T, t) in want if t == 0}
        ok = viol == want and v11 == want11
        cnt += 1
        solv += bool(covers)
        bad += not ok
        if not ok:
            print("  FAIL", sets, p, sorted(viol.items())[:4], sorted(v11)[:4])
    print(f"[Padberg/Letchford] {cnt} instances ({solv} with an exact cover): violated (12) over all disjoint S, T "
          f"and all integers s = {{(cover, {{g}}, 0), ({{g}}, cover, -1)}} with violation 1/(4N); violated (11) = "
          f"{{(cover, {{g}})}}: {bad} failures")
    return bad == 0


def affine_rank(points):
    rows = [[F(1)] + [F(v) for v in pt] for pt in points]
    rank, ncol = 0, len(rows[0]) if rows else 0
    for c in range(ncol):
        piv = next((r for r in range(rank, len(rows)) if rows[r][c] != 0), None)
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        for r in range(len(rows)):
            if r != rank and rows[r][c] != 0:
                f = rows[r][c] / rows[rank][c]
                rows[r] = [a - f * b for a, b in zip(rows[r], rows[rank])]
        rank += 1
    return rank


def facet12(Nv, S, T, s):
    """Is (12) for (S, T, s) valid and facet-defining for BQP_Nv?  Exact rank of the tight 0/1 points."""
    tight = []
    for xb in product((0, 1), repeat=Nv):
        A = sum(xb[i] for i in S)
        C = sum(xb[i] for i in T)
        B = sum(xb[i] * xb[j] for i in S for j in T)
        E = sum(xb[i] * xb[j] for i, j in combinations(S, 2)) + sum(xb[i] * xb[j] for i, j in combinations(T, 2))
        lhs, rhs = s * A + B, (s + 1) * C + E + s * (s + 1) // 2
        assert lhs <= rhs, "invalid inequality"
        if lhs == rhs:
            tight.append(list(xb) + [xb[i] * xb[j] for i, j in combinations(range(Nv), 2)])
    dim = Nv + Nv * (Nv - 1) // 2      # BQP_Nv is full-dimensional
    return affine_rank(tight) == dim   # facet: tight points span an affine space of dimension dim - 1


def check_facets():
    """Review item m3: the violators (12) with |S| = q >= 2, |T| = 1, s = 0 are facets of BQP (Letchford 2022,
    p. 9: facets when |S|+|T| >= 3 and 1-|T| <= s <= |S|-2); checked exactly, also with 2 unused variables.
    (11) with |S| = 1, |T| >= 2 is not a facet, although the condition printed for (11) on p. 8 allows it."""
    res = []
    ok = True
    for q in range(2, 7):
        f = facet12(q + 1, tuple(range(q)), (q,), 0)
        res.append(f"(|S|,|T|,s)=({q},1,0) in BQP_{q + 1}: {f}")
        ok &= f
    for q in range(2, 5):
        f = facet12(q + 3, tuple(range(q)), (q,), 0)
        res.append(f"({q},1,0) in BQP_{q + 3}: {f}")
        ok &= f
    for (a, b, want) in [(2, 1, True), (3, 1, True), (2, 2, True), (1, 2, False), (1, 3, False)]:
        f = facet12(a + b, tuple(range(a)), tuple(range(a, a + b)), 0)
        res.append(f"(11) with (|S|,|T|)=({a},{b}) in BQP_{a + b}: {f}")
        ok &= f == want
    print("[facets] " + "; ".join(res) + f": {'as expected' if ok else 'UNEXPECTED'}")
    return ok


if __name__ == "__main__":
    results = [check_closed_form(), check_theorem(), check_cut_form(), check_binary_point(),
               check_gonality(), check_pure(), check_controls(), example(),
               check_eps_bound(), check_window_p12(), check_padberg(), check_facets()]
    print("ALL CHECKS PASSED" if all(results) else "SOME CHECK FAILED")
    sys.exit(0 if all(results) else 1)
