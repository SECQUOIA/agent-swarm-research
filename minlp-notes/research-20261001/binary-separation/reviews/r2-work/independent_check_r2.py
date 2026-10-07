"""Reviewer r2: independent exact checks of the revised binary-separation note.

Does NOT import the author's code. Exact rational arithmetic (fractions.Fraction) for every
certificate; scipy is used only in part [I] (floating-point LP, labelled as numerical).

Parts
 [A] Lemma 5: max M_ii <= s = delta^T M^-1 delta <= 4n + p + 1/(4(p-1)) < N/2, N = 8n+2p+1,
     on random and degenerate exact-cover instances (empty sets, duplicates, full universe).
 [B] Corollary 3(c)-(e) at eps = 1/N: 4N*X integral, entries <= 4N, X PD, X - e0e0^T/2 PD,
     violated splits (own Fincke-Pohst, top-down LDL) = covers, value -1/(2N); J - 2 eps D = L X L^T;
     eps*d in (0,1); triangle iff no cover with <= 2 sets; perimeter always.
 [C] Corollary 8: all violated (12) (all ordered disjoint S,T; best integer s), all violated (11),
     and a bounded Boros-Hammer box search v in [-2,2]^{n+1}, all s.
 [D] Facets by exact rank: (12) (q,1,0); printed (11) for several (|S|,|T|); clique (10).
 [E] Theorem 1 at eta2 = p/12 (p = 2, 3) by own enumeration; violators below p/12.
 [F] Corollary 4(ii): b^T Z b = sigma(b')^2 - 4 Q(b', d^S) for b' = +-diag(s) b (random exact test).
 [G] NEW: switching X(1/N) on {g}: all violated Padberg clique inequalities (10) are exactly
     (C u {g}, s = 1) for exact covers C; the switched point is PD, in [0,1], satisfies the BQP triangle
     inequalities (q >= 3).
 [H] NEW: Corollary 5 point eps*d' switched on {g} u copies: all violated Barahona-Mahjoub clique
     inequalities (18) (b in {0,1}^V, |b| odd) are exactly 1_C + e_g + sum e_copies.
 [I] numerical: eps*d lies in the cut polytope for no-instances with |V| <= 6 (LP, HiGHS).
"""
import itertools
import math
import random
import sys
import time
from fractions import Fraction as F

T0 = time.time()
rng = random.Random(777002)


# ----------------------------------------------------------------- exact linear algebra
def ldl_top(A):
    """A = L D L^T, L unit lower triangular, top-down. Returns (L, D) or None if not PD."""
    k = len(A)
    L = [[F(0)] * k for _ in range(k)]
    D = [F(0)] * k
    for j in range(k):
        D[j] = F(A[j][j]) - sum((L[j][m] ** 2 * D[m] for m in range(j)), F(0))
        if D[j] <= 0:
            return None
        L[j][j] = F(1)
        for i in range(j + 1, k):
            L[i][j] = (F(A[i][j]) - sum((L[i][m] * L[j][m] * D[m] for m in range(j)), F(0))) / D[j]
    return L, D


def is_pd(A):
    return ldl_top(A) is not None


def solve_sym(A, b):
    LD = ldl_top(A)
    assert LD is not None
    L, D = LD
    k = len(A)
    y = [F(0)] * k
    for i in range(k):
        y[i] = F(b[i]) - sum((L[i][m] * y[m] for m in range(i)), F(0))
    z = [y[i] / D[i] for i in range(k)]
    x = [F(0)] * k
    for i in reversed(range(k)):
        x[i] = z[i] - sum((L[m][i] * x[m] for m in range(i + 1, k)), F(0))
    return x


def qf(A, u, v=None):
    v = u if v is None else v
    return sum(u[i] * A[i][j] * v[j] for i in range(len(u)) for j in range(len(v)) if u[i] and v[j])


def lattice_ellipsoid(A, c, R):
    """All integer v with (v-c)^T A (v-c) < R, using A = L D L^T (L lower): the form is
    sum_j D_j (sum_{i>=j} L_ij (v_i - c_i))^2. Enumerate j = k-1 .. 0."""
    L, D = ldl_top(A)
    k = len(A)
    v = [0] * k
    out = []

    def rec(j, rem):
        if j < 0:
            out.append(tuple(v))
            return
        shift = sum((L[i][j] * (v[i] - c[i]) for i in range(j + 1, k)), F(0))
        center = c[j] - shift  # t_j = v_j - center
        rad = math.sqrt(float(rem / D[j])) + 1
        lo, hi = math.floor(float(center) - rad) - 1, math.ceil(float(center) + rad) + 1
        for vj in range(lo, hi + 1):
            t = D[j] * (vj - center) ** 2
            if t < rem:
                v[j] = vj
                rec(j - 1, rem - t)
        v[j] = 0

    rec(k - 1, F(R))
    return out


def rank_exact(rows):
    rows = [[F(x) for x in r] for r in rows]
    rk = 0
    ncol = len(rows[0]) if rows else 0
    for c in range(ncol):
        piv = None
        for r in range(rk, len(rows)):
            if rows[r][c] != 0:
                piv = r
                break
        if piv is None:
            continue
        rows[rk], rows[piv] = rows[piv], rows[rk]
        pv = rows[rk][c]
        for r in range(len(rows)):
            if r != rk and rows[r][c] != 0:
                f = rows[r][c] / pv
                rows[r] = [a - f * b for a, b in zip(rows[r], rows[rk])]
        rk += 1
    return rk


# ----------------------------------------------------------------- construction (own code)
def Mmat(sets, p, eta2):
    """Order: sets 0..n-1, then g."""
    n = len(sets)
    M = [[F(0)] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(n):
            M[i][j] = F(len(set(sets[i]) & set(sets[j]))) + (4 if i == j else 0)
        M[i][n] = M[n][i] = F(len(sets[i]), 2)
    M[n][n] = F(p, 4) + eta2
    return M


def covers_of(sets, p):
    res = []
    for x in itertools.product((0, 1), repeat=len(sets)):
        cnt = [0] * p
        for i, xi in enumerate(x):
            if xi:
                for e in sets[i]:
                    cnt[e] += 1
        if all(c == 1 for c in cnt):
            res.append(x)
    return res


def bqp_point(M, N):
    """X(1/N) indexed 0 (root), 1..n+1 (sets..., g)."""
    k = len(M)
    eps = F(1, N)
    X = [[F(0)] * (k + 1) for _ in range(k + 1)]
    X[0][0] = F(1)
    for i in range(k):
        X[0][i + 1] = X[i + 1][0] = eps * M[i][i]
        for j in range(k):
            X[i + 1][j + 1] = eps * M[i][j]
    return X, eps


def cut_image(X):
    """Covariance map with root 0: d_0i = X_ii, d_ij = X_ii + X_jj - 2 X_ij."""
    k = len(X)
    D = [[F(0)] * k for _ in range(k)]
    for i in range(1, k):
        D[0][i] = D[i][0] = X[i][i]
        for j in range(1, k):
            if i != j:
                D[i][j] = X[i][i] + X[j][j] - 2 * X[i][j]
    return D


def gen_instance(p, nmax, plant_prob=0.5, allow_empty=True, allow_full=True):
    sets = []
    if rng.random() < plant_prob:
        U = list(range(p))
        rng.shuffle(U)
        k = 0
        while k < p:
            sz = rng.randint(1, min(3, p - k))
            sets.append(tuple(sorted(U[k:k + sz])))
            k += sz
    n = rng.randint(max(len(sets), 1), max(nmax, len(sets)))
    while len(sets) < n:
        r = rng.random()
        if allow_empty and r < 0.08:
            sets.append(())
        elif allow_full and r < 0.16:
            sets.append(tuple(range(p)))
        elif r < 0.30 and sets:
            sets.append(rng.choice(sets))  # duplicate
        else:
            sets.append(tuple(sorted(rng.sample(range(p), rng.randint(1, p)))))
    rng.shuffle(sets)
    return sets


def gen_x3c(q, extra):
    p = 3 * q
    sets = [tuple(sorted(rng.sample(range(p), 3))) for _ in range(extra)]
    if rng.random() < 0.5:
        U = list(range(p))
        rng.shuffle(U)
        sets += [tuple(sorted(U[3 * k:3 * k + 3])) for k in range(q)]
    rng.shuffle(sets)
    return sets, p


RESULTS = []


def report(tag, ok, msg):
    RESULTS.append(ok)
    print(f"[{tag}] {msg}: {'OK' if ok else 'FAIL'}", flush=True)


# ----------------------------------------------------------------- [A]
def part_A():
    bad = cnt = 0
    worst = F(0)
    insts = []
    for _ in range(60):
        p = rng.randint(2, 7)
        insts.append((gen_instance(p, 9), p))
    for q in (2, 3, 4, 6, 8):
        for _ in range(3):
            insts.append(gen_x3c(q, rng.randint(q, 3 * q)))
    # degenerate families
    insts.append(([()] * 10 + [(0, 1)], 2))
    insts.append(([tuple(range(5))] * 12, 5))
    insts.append(([(e,) for e in range(12)], 12))
    insts.append(([(e,) for e in range(12)] * 2, 12))
    insts.append((list(itertools.combinations(range(7), 2)), 7))
    insts.append(([(0, 1, 2)] * 60 + [(3, 4, 5)], 6))
    for sets, p in insts:
        n = len(sets)
        M = Mmat(sets, p, F(p - 1, 4))
        delta = [M[i][i] for i in range(n + 1)]
        w = solve_sym(M, delta)
        s = sum(a * b for a, b in zip(delta, w))
        ub = 4 * n + p + F(1, 4 * (p - 1))
        N = 8 * n + 2 * p + 1
        ok = max(delta) <= s <= ub and 2 * s < N
        worst = max(worst, s / ub)
        cnt += 1
        bad += not ok
    report("A", bad == 0, f"Lemma 5 on {cnt} instances (incl. empty/duplicate/full sets, singletons, n up to 61): "
                          f"{bad} failures; max s/(4n+p+1/(4(p-1))) = {float(worst):.4f}")


# ----------------------------------------------------------------- [B]
def split_violators(X):
    k = len(X)
    c = [F(-1, 2)] + [F(0)] * (k - 1)  # (v + e0/2)^T X (v + e0/2) < 1/4  <=>  u = 2v+e0 has u^T X u < 1
    return sorted(lattice_ellipsoid(X, c, F(1, 4)))


def part_B():
    bad = cnt = ncov = nsmall = 0
    for t in range(70):
        if t < 45:
            p = rng.randint(2, 5)
            sets = gen_instance(p, 6)
        else:
            sets, p = gen_x3c(rng.choice([2, 3]), rng.randint(1, 3))
        n = len(sets)
        N = 8 * n + 2 * p + 1
        M = Mmat(sets, p, F(p - 1, 4))
        X, eps = bqp_point(M, N)
        k = len(X)
        ok_int = all((4 * N * X[i][j]).denominator == 1 and 0 <= 4 * N * X[i][j] <= 4 * N for i in range(k) for j in range(k))
        ok_pd = is_pd(X)
        Y = [r[:] for r in X]
        Y[0][0] -= F(1, 2)
        ok_half = is_pd(Y)
        cov = covers_of(sets, p)
        ncov += bool(cov)
        want = sorted([(0,) + tuple(-a for a in x) + (1,) for x in cov] + [(-1,) + tuple(x) + (-1,) for x in cov])
        viol = split_violators(X)
        ok_viol = viol == want
        ok_val = all(qf(X, list(v)) + sum(X[0][j] * v[j] for j in range(k)) == -F(1, 2 * N) for v in viol)
        # J - 2 eps D = L X L^T with L = [[1,0],[1,-2I]]
        D = cut_image(X)
        Lm = [[F(0)] * k for _ in range(k)]
        Lm[0][0] = F(1)
        for i in range(1, k):
            Lm[i][0] = F(1)
            Lm[i][i] = F(-2)
        LX = [[sum(Lm[i][m] * X[m][j] for m in range(k)) for j in range(k)] for i in range(k)]
        LXL = [[sum(LX[i][m] * Lm[j][m] for m in range(k)) for j in range(k)] for i in range(k)]
        Z = [[1 - 2 * D[i][j] for j in range(k)] for i in range(k)]
        ok_cong = LXL == Z and is_pd(Z)
        # scaled distance equals eps * d(M)
        dM = [[F(0)] * k for _ in range(k)]
        for i in range(k - 1):
            dM[0][i + 1] = dM[i + 1][0] = M[i][i]
            for j in range(k - 1):
                if i != j:
                    dM[i + 1][j + 1] = M[i][i] + M[j][j] - 2 * M[i][j]
        ok_scale = all(D[i][j] == eps * dM[i][j] for i in range(k) for j in range(k))
        ok_box = all(0 < D[i][j] < 1 for i in range(k) for j in range(k) if i != j)
        small = any(sum(x) <= 2 for x in cov)
        nsmall += small
        tri = all(D[a][b] <= D[a][c] + D[b][c] and D[a][c] <= D[a][b] + D[b][c] and D[b][c] <= D[a][b] + D[a][c]
                  for a, b, c in itertools.combinations(range(k), 3))
        per = all(D[a][b] + D[a][c] + D[b][c] <= 2 for a, b, c in itertools.combinations(range(k), 3))
        ok_tri = (tri == (not small)) and per
        ok = ok_int and ok_pd and ok_half and ok_viol and ok_val and ok_cong and ok_scale and ok_box and ok_tri
        cnt += 1
        bad += not ok
        if not ok:
            print("  FAIL B", sets, p, ok_int, ok_pd, ok_half, ok_viol, ok_val, ok_cong, ok_scale, ok_box, ok_tri)
    report("B", bad == 0, f"Corollary 3(c)-(e) at eps = 1/(8n+2p+1), {cnt} instances ({ncov} with a cover, {nsmall} with a "
                          f"cover of <= 2 sets; empty/duplicate/full sets allowed): own split enumeration, theta = 1/2 margin, "
                          f"congruence J-2eps D = L X L^T, box, triangle/perimeter: {bad} failures")


# ----------------------------------------------------------------- [C]
def viol12(x, y, S, T, s):
    """LHS - RHS of Letchford (12)."""
    A = sum((x[i] for i in S), F(0))
    C = sum((x[i] for i in T), F(0))
    B = sum((y[i][j] for i in S for j in T), F(0))
    E = sum((y[i][j] for i, j in itertools.combinations(S, 2)), F(0)) + \
        sum((y[i][j] for i, j in itertools.combinations(T, 2)), F(0))
    return s * A + B - (s + 1) * C - E - F(s * (s + 1), 2)


def xy_from(X):
    k = len(X) - 1
    x = [X[i + 1][i + 1] for i in range(k)]
    y = [[X[i + 1][j + 1] for j in range(k)] for i in range(k)]
    return x, y


def part_C():
    bad = cnt = ncov = 0
    for t in range(40):
        if t < 25:
            sets, p = gen_x3c(rng.choice([2, 3, 4]), rng.randint(1, 3))
        else:
            p = rng.randint(2, 5)
            sets = gen_instance(p, 5)
        n = len(sets)
        N = 8 * n + 2 * p + 1
        M = Mmat(sets, p, F(p - 1, 4))
        X, eps = bqp_point(M, N)
        x, y = xy_from(X)
        k = n + 1
        g = n
        cov = covers_of(sets, p)
        ncov += bool(cov)
        covsets = {tuple(i for i in range(n) if c[i]) for c in cov}
        # (12): for fixed (S,T), LHS-RHS is concave in s with maximum at s = floor(x(S)-x(T)); check s0-1..s0+1
        found12 = {}
        found11 = set()
        for lab in itertools.product((0, 1, 2), repeat=k):
            S = tuple(i for i in range(k) if lab[i] == 1)
            T = tuple(i for i in range(k) if lab[i] == 2)
            ell = sum((x[i] for i in S), F(0)) - sum((x[i] for i in T), F(0))
            s0 = math.floor(ell)
            vals = {s: viol12(x, y, S, T, s) for s in (s0 - 2, s0 - 1, s0, s0 + 1, s0 + 2)}
            assert max(vals.values()) == vals[s0]  # concavity / argmax claim of the note
            for s, v in vals.items():
                if v > 0:
                    found12[(S, T, s)] = v
            if viol12(x, y, S, T, 0) > 0:
                found11.add((S, T))
        want12 = {}
        for C in covsets:
            want12[(C, (g,), 0)] = F(1, 4 * N)
            want12[((g,), C, -1)] = F(1, 4 * N)
        want11 = {(C, (g,)) for C in covsets}
        ok = found12 == want12 and found11 == want11
        # bounded Boros-Hammer box search: v in [-2,2]^k, s integer; violated iff linearized
        # (v^T x - s)(v^T x - s - 1) < 0 ; for fixed v the best s is floor(v^T x)
        bh = set()
        if k <= 6:
            for v in itertools.product(range(-2, 3), repeat=k):
                if not any(v):
                    continue
                vx = sum((v[i] * x[i] for i in range(k)), F(0))
                quad = sum((v[i] * v[i] * x[i] for i in range(k)), F(0)) + \
                    2 * sum((v[i] * v[j] * y[i][j] for i, j in itertools.combinations(range(k), 2)), F(0))
                for s in (math.floor(vx) - 1, math.floor(vx), math.floor(vx) + 1):
                    val = quad - (2 * s + 1) * vx + s * (s + 1)
                    if val < 0:
                        bh.add((v, s, val))
            wantbh = set()
            for C in covsets:
                v1 = tuple(1 if i in C else (-1 if i == g else 0) for i in range(k))
                v2 = tuple(-a for a in v1)
                wantbh.add((v1, 0, -F(1, 2 * N)))
                wantbh.add((v2, -1, -F(1, 2 * N)))
            ok = ok and bh == wantbh
        cnt += 1
        bad += not ok
        if not ok:
            print("  FAIL C", sets, p, sorted(found12)[:3], sorted(found11)[:3])
    report("C", bad == 0, f"Corollary 8 at X(1/N), {cnt} instances ({ncov} with a cover): violated (12) = "
                          f"{{(C,{{g}},0),({{g}},C,-1)}} with violation 1/(4N); violated (11) = {{(C,{{g}})}}; "
                          f"BH box [-2,2]^(n+1) (n+1 <= 6) violated only by +-(1_C - e_g); argmax s = floor(l): {bad} failures")


# ----------------------------------------------------------------- [D]
def bqp_points(k):
    for xb in itertools.product((0, 1), repeat=k):
        yield list(xb) + [xb[i] * xb[j] for i, j in itertools.combinations(range(k), 2)]


def facet_test(k, coef_fn):
    """coef_fn(point) -> slack (RHS - LHS) for 0/1 points; returns (valid, facet)."""
    tight = []
    valid = True
    for pt in bqp_points(k):
        sl = coef_fn(pt)
        if sl < 0:
            valid = False
        if sl == 0:
            tight.append([1] + pt)
    dim = k + k * (k - 1) // 2
    return valid, (rank_exact(tight) == dim if tight else False)


def ineq12(k, S, T, s):
    pairs = list(itertools.combinations(range(k), 2))
    idx = {pr: k + t for t, pr in enumerate(pairs)}

    def yv(pt, i, j):
        return pt[idx[(min(i, j), max(i, j))]]

    def slack(pt):
        A = sum(pt[i] for i in S)
        C = sum(pt[i] for i in T)
        B = sum(yv(pt, i, j) for i in S for j in T)
        E = sum(yv(pt, i, j) for i, j in itertools.combinations(S, 2)) + sum(yv(pt, i, j) for i, j in itertools.combinations(T, 2))
        return ((s + 1) * C + E + F(s * (s + 1), 2)) - (s * A + B)
    return slack


def ineq11_swapped(k, S, T):
    """Padberg-type form with x(S) instead of x(T) on the right: y(S:T) <= x(S) + y(E(S)) + y(E(T))."""
    pairs = list(itertools.combinations(range(k), 2))
    idx = {pr: k + t for t, pr in enumerate(pairs)}

    def yv(pt, i, j):
        return pt[idx[(min(i, j), max(i, j))]]

    def slack(pt):
        A = sum(pt[i] for i in S)
        B = sum(yv(pt, i, j) for i in S for j in T)
        E = sum(yv(pt, i, j) for i, j in itertools.combinations(S, 2)) + sum(yv(pt, i, j) for i, j in itertools.combinations(T, 2))
        return A + E - B
    return slack


def part_D():
    res = []
    ok = True
    for q in range(2, 7):
        v, f = facet_test(q + 1, ineq12(q + 1, tuple(range(q)), (q,), 0))
        res.append(f"(12)({q},1,0)/BQP{q + 1}:{v and f}")
        ok &= v and f
    for q in (2, 3):
        v, f = facet_test(q + 3, ineq12(q + 3, tuple(range(q)), (q,), 0))
        res.append(f"(12)({q},1,0)/BQP{q + 3}:{v and f}")
        ok &= v and f
    # printed (11) = (12) with s = 0
    for a, b, want in [(2, 1, True), (3, 1, True), (2, 2, True), (2, 3, True), (3, 2, True),
                       (1, 2, False), (1, 3, False), (1, 4, False)]:
        v, f = facet_test(a + b, ineq12(a + b, tuple(range(a)), tuple(range(a, a + b)), 0))
        res.append(f"(11)print({a},{b}):{f}")
        ok &= v and (f == want)
    # the x(S)-form (Padberg's original orientation, as commonly cited) with |S| >= 1, |T| >= 2
    for a, b in [(1, 2), (1, 3), (2, 2)]:
        v, f = facet_test(a + b, ineq11_swapped(a + b, tuple(range(a)), tuple(range(a, a + b))))
        res.append(f"(11)x(S)-form({a},{b}):valid={v},facet={f}")
        ok &= v and f
    # clique (10) = (12) with T empty: (|S'|, s') = (q+1, 1) is a facet (switching image of the violator)
    for q in range(2, 6):
        v, f = facet_test(q + 1, ineq12(q + 1, tuple(range(q + 1)), (), 1))
        res.append(f"(10)({q + 1},1):{v and f}")
        ok &= v and f
    report("D", ok, "facets by exact rank: " + "; ".join(res))


# ----------------------------------------------------------------- [E]
def hyp_violators(M):
    k = len(M)
    w = solve_sym(M, [M[i][i] / 2 for i in range(k)])
    R = qf(M, w)
    out = lattice_ellipsoid(M, w, R)
    return sorted(z for z in out if qf(M, list(z)) - sum(M[i][i] * z[i] for i in range(k)) < 0)


def part_E():
    bad = cnt = ncov = 0
    for _ in range(80):
        p = rng.choice([2, 3])
        sets = gen_instance(p, 6)
        M = Mmat(sets, p, F(p, 12))
        cov = covers_of(sets, p)
        ncov += bool(cov)
        V = hyp_violators(M)
        want = sorted(tuple(x) + (-1,) for x in cov)
        val_ok = all(qf(M, list(z)) - sum(M[i][i] * z[i] for i in range(len(M))) == -(F(p, 2) - 2 * F(p, 12)) for z in V)
        cnt += 1
        bad += not (V == want and val_ok)
    below = 0
    tot = 0
    for _ in range(30):
        p = rng.choice([2, 3])
        sets = gen_instance(p, 5, plant_prob=1.0)
        M = Mmat(sets, p, F(p, 12) - F(1, 50))
        V = set(hyp_violators(M))
        cov = covers_of(sets, p)
        tot += 1
        below += all(tuple(x) + (-2,) in V for x in cov) and bool(cov)
    nos = [(0, 1), (1, 2)]
    ex = (1, 1, -2) in set(hyp_violators(Mmat(nos, 3, F(1, 4) - F(1, 50)))) and not covers_of(nos, 3)
    report("E", bad == 0 and below == tot and ex,
           f"Theorem 1 at eta2 = p/12 (p in {{2,3}}), {cnt} instances ({ncov} with a cover): {bad} failures; "
           f"eta2 = p/12 - 1/50: extra (x,-2) in {below}/{tot}; no-instance example violated: {ex}")


# ----------------------------------------------------------------- [F]
def part_F():
    bad = 0
    trials = 300
    for _ in range(trials):
        V = rng.randint(3, 7)
        d = [[F(0)] * V for _ in range(V)]
        for u, v in itertools.combinations(range(V), 2):
            d[u][v] = d[v][u] = F(rng.randint(-20, 40), rng.randint(1, 13))
        while True:
            b = [rng.randint(-3, 3) for _ in range(V)]
            gam = min(abs(sum(si * bi for si, bi in zip(s, b))) for s in itertools.product((1, -1), repeat=V))
            if gam == 1:
                break
        s = next(s for s in itertools.product((1, -1), repeat=V) if abs(sum(si * bi for si, bi in zip(s, b))) == 1)
        sign = 1 if sum(si * bi for si, bi in zip(s, b)) == 1 else -1
        bp = [sign * si * bi for si, bi in zip(s, b)]
        dS = [[(1 - d[u][v]) if (s[u] != s[v]) else d[u][v] for v in range(V)] for u in range(V)]
        for u in range(V):
            dS[u][u] = F(0)
        Z = [[F(1) if u == v else 1 - 2 * d[u][v] for v in range(V)] for u in range(V)]
        Qp = sum(bp[u] * bp[v] * dS[u][v] for u, v in itertools.combinations(range(V), 2))
        lhs = qf(Z, b)
        bad += not (sum(bp) == 1 and lhs == 1 - 4 * Qp)
    report("F", bad == 0, f"Corollary 4(ii) switching identity b^T Z b = 1 - 4 Q(b', d^S) on {trials} random rational d: {bad} failures")


# ----------------------------------------------------------------- [G]
def switch_bqp(X, gidx):
    """Switch variable gidx (1-based index in X) : x_g -> 1 - x_g, y_ig -> x_i - y_ig. Moment-matrix congruence."""
    k = len(X)
    A = [[F(int(i == j)) for j in range(k)] for i in range(k)]
    A[gidx][0] = F(1)
    A[gidx][gidx] = F(-1)
    AX = [[sum(A[i][m] * X[m][j] for m in range(k)) for j in range(k)] for i in range(k)]
    return [[sum(AX[i][m] * A[j][m] for m in range(k)) for j in range(k)] for i in range(k)]


def part_G():
    bad = cnt = ncov = 0
    for t in range(40):
        if t < 30:
            sets, p = gen_x3c(rng.choice([3, 4]), rng.randint(1, 3))
        else:
            p = rng.randint(3, 5)
            sets = gen_instance(p, 5)
        n = len(sets)
        N = 8 * n + 2 * p + 1
        M = Mmat(sets, p, F(p - 1, 4))
        X, eps = bqp_point(M, N)
        g = n + 1  # 1-based index of g in X
        Xs = switch_bqp(X, g)
        k = n + 1
        x, y = xy_from(Xs)
        # direct check of the switching formulas
        ok_form = Xs[g][g] == 1 - X[g][g] and Xs[0][g] == 1 - X[0][g] and \
            all(Xs[i][g] == X[i][i] - X[i][g] for i in range(1, g)) and Xs[g][g] == Xs[0][g]
        ok_pd = is_pd(Xs)
        ok_box = all(0 <= v <= 1 for v in x) and all(0 <= y[i][j] <= 1 for i in range(k) for j in range(k) if i != j)
        cov = covers_of(sets, p)
        ncov += bool(cov)
        # all clique inequalities (10): S subset, s = 0..|S|-1 (and, for safety, all integers near floor(x(S)))
        found = {}
        for r in range(1, k + 1):
            for S in itertools.combinations(range(k), r):
                ell = sum((x[i] for i in S), F(0))
                for s in set(range(0, r)) | {math.floor(ell) - 1, math.floor(ell), math.floor(ell) + 1}:
                    v = viol12(x, y, S, (), s)
                    if v > 0:
                        found[(S, s)] = v
        want = {(tuple(sorted([i for i in range(n) if c[i]] + [n])), 1): F(1, 4 * N) for c in cov}
        # BQP triangle inequalities = (12) with |S|+|T| <= 3 hold iff no cover with <= 2 sets
        tri_ok = True
        for lab in itertools.product((0, 1, 2), repeat=k):
            S = tuple(i for i in range(k) if lab[i] == 1)
            T = tuple(i for i in range(k) if lab[i] == 2)
            if 1 <= len(S) + len(T) <= 3:
                for s in range(-3, 4):
                    if viol12(x, y, S, T, s) > 0:
                        tri_ok = False
        small = any(sum(c) <= 2 for c in cov)
        ok = ok_form and ok_pd and ok_box and found == want and (tri_ok == (not small))
        cnt += 1
        bad += not ok
        if not ok:
            print("  FAIL G", sets, p, ok_form, ok_pd, ok_box, sorted(found.items())[:3], tri_ok, small)
    report("G", bad == 0, f"switched point X(1/N)^{{g}}, {cnt} instances ({ncov} with a cover): PD, in [0,1], violated "
                          f"Padberg clique inequalities (10) = {{(C u {{g}}, s=1)}} with violation 1/(4N), BQP triangle "
                          f"inequalities hold iff no cover with <= 2 sets: {bad} failures")


# ----------------------------------------------------------------- [H]
def part_H():
    bad = cnt = ncov = 0
    for t in range(30):
        q = rng.choice([4, 5]) if t < 20 else 3
        sets, p = gen_x3c(q, rng.randint(1, 2))
        n = len(sets)
        N = 8 * n + 2 * p + 1
        M = Mmat(sets, p, F(p - 1, 4))
        X, eps = bqp_point(M, N)
        D = cut_image(X)  # eps*d on {0, sets, g}
        c = q - 2
        V = len(D)
        # append copies of 0
        D2 = [row[:] + [row[0]] * c for row in D]
        for _ in range(c):
            D2.append(D[0][:] + [F(0)] * c)
        W = V + c
        U = {V - 1} | set(range(V, W))  # g and the copies
        Dsw = [[(1 - D2[a][b]) if ((a in U) != (b in U)) else D2[a][b] for b in range(W)] for a in range(W)]
        for a in range(W):
            Dsw[a][a] = F(0)
        found = set()
        for r in range(1, W + 1, 2):
            for S in itertools.combinations(range(W), r):
                Qv = sum((Dsw[a][b] for a, b in itertools.combinations(S, 2)), F(0))
                if Qv > F(r * r - 1, 4):
                    found.add(S)
        cov = covers_of(sets, p)
        ncov += bool(cov)
        want = {tuple(sorted([i + 1 for i in range(n) if x[i]] + sorted(U))) for x in cov}
        metric = all(Dsw[a][b] <= Dsw[a][e] + Dsw[b][e] and Dsw[a][b] + Dsw[a][e] + Dsw[b][e] <= 2
                     for a, b, e in itertools.permutations(range(W), 3))
        ok = found == want and metric
        cnt += 1
        bad += not ok
        if not ok:
            print("  FAIL H", sets, p, sorted(found)[:3], sorted(want)[:3], metric)
    report("H", bad == 0, f"Corollary 5 point switched on {{g}} u copies, {cnt} X3C instances ({ncov} with a cover, q in "
                          f"{{3,4,5}}): violated Barahona-Mahjoub (18) (b in {{0,1}}) = {{1_C + e_g + copies}}; metric polytope: "
                          f"{bad} failures")


# ----------------------------------------------------------------- [I]
def part_I():
    try:
        import numpy as np
        from scipy.optimize import linprog
    except Exception as e:  # pragma: no cover
        report("I", False, f"scipy unavailable: {e}")
        return
    tested = inside = 0
    for _ in range(200):
        if tested >= 30:
            break
        p = rng.randint(3, 6)
        sets = gen_instance(p, 4, plant_prob=0.0)
        n = len(sets)
        if n + 2 > 6 or n < 2 or covers_of(sets, p):
            continue
        N = 8 * n + 2 * p + 1
        X, eps = bqp_point(Mmat(sets, p, F(p - 1, 4)), N)
        D = cut_image(X)
        V = len(D)
        pairs = list(itertools.combinations(range(V), 2))
        cuts = []
        for mask in range(0, 2 ** (V - 1)):
            S = {i for i in range(V - 1) if mask >> i & 1}
            cuts.append([1.0 if ((a in S) != (b in S)) else 0.0 for a, b in pairs])
        A = np.array(cuts).T
        Aeq = np.vstack([A, np.ones((1, A.shape[1]))])
        beq = np.array([float(D[a][b]) for a, b in pairs] + [1.0])
        res = linprog(np.zeros(A.shape[1]), A_eq=Aeq, b_eq=beq, bounds=(0, None), method="highs")
        tested += 1
        inside += res.status == 0
    report("I", inside == tested, f"numerical (HiGHS LP): eps*d in the cut polytope for {inside}/{tested} no-instances with "
                                  f"4-6 points (consistent with the CUT_n = HYP_n switching argument of note §10 item 4)")


if __name__ == "__main__":
    for part in (part_A, part_B, part_C, part_D, part_E, part_F, part_G, part_H, part_I):
        part()
    print(f"elapsed {time.time() - T0:.1f} s")
    print("REVIEWER R2 CHECKS PASSED" if all(RESULTS) else "SOME REVIEWER CHECK FAILED")
    sys.exit(0 if all(RESULTS) else 1)
