"""Reviewer r3: independent exact checks of the material added in revision r2 of note.md
(Lemma 6, Corollary 9, remark after Corollary 9, Corollary 10 and its control, facets of (10)/(18),
closed form s(n) after Lemma 5).  Does not import the author's code.  Exact Fraction arithmetic.

Enumeration: standard L D L^T (unit lower L), q(y) = sum_j D_j (y_j + sum_{i>j} L_ij y_i)^2, enumerated
from the last coordinate down (float bounds widened by 1, exact filtering).
"""
import itertools
import math
import random
import sys
import time
from fractions import Fraction as F

random.seed(20261002)
T0 = time.time()


# ----------------------------------------------------------------- exact linear algebra
def ldl(G):
    k = len(G)
    L = [[F(0)] * k for _ in range(k)]
    D = [F(0)] * k
    for j in range(k):
        D[j] = G[j][j] - sum(L[j][m] ** 2 * D[m] for m in range(j))
        if D[j] <= 0:
            return None
        L[j][j] = F(1)
        for i in range(j + 1, k):
            L[i][j] = (G[i][j] - sum(L[i][m] * L[j][m] * D[m] for m in range(j))) / D[j]
    return L, D


def is_pd(G):
    return ldl(G) is not None


def solve(G, b):
    k = len(G)
    A = [list(G[i]) + [b[i]] for i in range(k)]
    for c in range(k):
        piv = next(r for r in range(c, k) if A[r][c] != 0)
        A[c], A[piv] = A[piv], A[c]
        for r in range(k):
            if r != c and A[r][c] != 0:
                f = A[r][c] / A[c][c]
                A[r] = [a - f * bb for a, bb in zip(A[r], A[c])]
    return [A[i][k] / A[i][i] for i in range(k)]


def enum_ellipsoid(G, c, R, first=()):
    """All integer z with (z - c)^T G (z - c) < R (G positive definite).  The coordinates listed in `first` are
    moved to the front of the order, so they are enumerated innermost (this matters for speed only)."""
    k0 = len(G)
    order = list(first) + [i for i in reversed(range(k0)) if i not in first]
    Gp = [[G[a][b] for b in order] for a in order]
    cp = [c[a] for a in order]
    res = _enum(Gp, cp, R)
    out = []
    for zp in res:
        z = [0] * k0
        for pos, a in enumerate(order):
            z[a] = zp[pos]
        out.append(tuple(z))
    return out


def _enum(G, c, R):
    L, D = ldl(G)
    k = len(G)
    out = []
    z = [0] * k

    def rec(j, rem):
        # term_j = D_j (z_j - c_j + sum_{i>j} L_ij (z_i - c_i))^2
        t = c[j] - sum(L[i][j] * (z[i] - c[i]) for i in range(j + 1, k))
        w = math.sqrt(max(float(rem / D[j]), 0.0))
        lo, hi = math.floor(float(t) - w) - 1, math.ceil(float(t) + w) + 1
        for zj in range(lo, hi + 1):
            val = D[j] * (zj - t) ** 2
            if val < rem:
                z[j] = zj
                if j == 0:
                    out.append(tuple(z))
                else:
                    rec(j - 1, rem - val)
        z[j] = 0

    rec(k - 1, F(R))
    return out


def affine_rank(pts):
    if not pts:
        return -1
    base = pts[0]
    rows = [[F(a - b) for a, b in zip(p, base)] for p in pts[1:]]
    r = 0
    ncol = len(base)
    for c in range(ncol):
        piv = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c] / rows[r][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        r += 1
    return r


# ----------------------------------------------------------------- construction (from note.md section 3)
def build_M(sets, p):
    n = len(sets)
    eta2 = F(p - 1, 4)
    M = [[F(0)] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(n):
            M[i][j] = (4 if i == j else 0) + len(set(sets[i]) & set(sets[j]))
        M[i][n] = M[n][i] = F(len(sets[i]), 2)
    M[n][n] = F(p, 4) + eta2
    return M


def covers(sets, p):
    out = []
    n = len(sets)
    for r in range(1, n + 1):
        for T in itertools.combinations(range(n), r):
            cnt = [0] * p
            for i in T:
                for e in sets[i]:
                    cnt[e] += 1
            if all(c == 1 for c in cnt):
                out.append(T)
    return out


def x3c(q, nextra, plant):
    p = 3 * q
    sets = []
    if plant:
        U = list(range(p))
        random.shuffle(U)
        sets += [tuple(sorted(U[3 * k:3 * k + 3])) for k in range(q)]
    while len(sets) < (q if plant else 0) + nextra:
        t = tuple(sorted(random.sample(range(p), 3)))
        sets.append(t)
    random.shuffle(sets)
    return sets, p


def moment(M, eps):
    """X = [[1, eps*delta^T], [eps*delta, eps*M]]."""
    k = len(M)
    X = [[F(1)] + [eps * M[j][j] for j in range(k)]]
    for i in range(k):
        X.append([eps * M[i][i]] + [eps * M[i][j] for j in range(k)])
    return X


def dist_from_M(M):
    """d on {0} u W (index 0 = root) with d_0i = M_ii, d_ij = M_ii + M_jj - 2 M_ij."""
    k = len(M)
    d = [[F(0)] * (k + 1) for _ in range(k + 1)]
    for i in range(k):
        d[0][i + 1] = d[i + 1][0] = M[i][i]
        for j in range(k):
            if i != j:
                d[i + 1][j + 1] = M[i][i] + M[j][j] - 2 * M[i][j]
    return d


def cut_of_moment(X):
    k = len(X)
    d = [[F(0)] * k for _ in range(k)]
    for i in range(1, k):
        d[0][i] = d[i][0] = X[i][i]
        for j in range(1, k):
            if i != j:
                d[i][j] = X[i][i] + X[j][j] - 2 * X[i][j]
    return d


def moment_of_cut(d):
    k = len(d)
    X = [[F(0)] * k for _ in range(k)]
    X[0][0] = F(1)
    for i in range(1, k):
        X[0][i] = X[i][0] = X[i][i] = d[0][i]
    for i in range(1, k):
        for j in range(1, k):
            if i != j:
                X[i][j] = (d[0][i] + d[0][j] - d[i][j]) / 2
    return X


def switch_cut(d, U):
    k = len(d)
    return [[(1 - d[a][b]) if a != b and ((a in U) != (b in U)) else d[a][b] for b in range(k)] for a in range(k)]


def switch_bqp(X, g):
    """Letchford Definition 2 on S = {g}: x_g -> 1 - x_g, y_ig -> x_i - y_ig."""
    k = len(X)
    Y = [r[:] for r in X]
    Y[g][g] = Y[0][g] = Y[g][0] = 1 - X[0][g]
    for i in range(1, k):
        if i != g:
            Y[i][g] = Y[g][i] = X[0][i] - X[i][g]
    return Y


def Qb(b, d):
    k = len(b)
    return sum(b[u] * b[v] * d[u][v] for u in range(k) for v in range(u + 1, k))


def bh_lin(X, v, s):
    """Explicit linearization of (v^T x - s)(v^T x - s - 1) with x_i^2 -> x_i, x_i x_j -> y_ij (>= 0 is valid)."""
    k = len(X)
    val = F(s * (s + 1))
    for i in range(1, k):
        val += (v[i - 1] ** 2 - (2 * s + 1) * v[i - 1]) * X[0][i]
        for j in range(i + 1, k):
            val += 2 * v[i - 1] * v[j - 1] * X[i][j]
    return val


def elliptope_pd(d):
    k = len(d)
    return is_pd([[1 - 2 * d[i][j] if i != j else F(1) for j in range(k)] for i in range(k)])


def metric_ok(d):
    k = len(d)
    for a, b, c in itertools.combinations(range(k), 3):
        if d[a][b] + d[a][c] + d[b][c] > 2:
            return False
        for (u, v, w) in ((a, b, c), (a, c, b), (b, c, a)):
            if d[u][v] > d[u][w] + d[v][w]:
                return False
    return True


def bqp_triangles_ok(X):
    """Explicit Padberg triangle family: McCormick (3)-(5), y >= 0, (8), (9)."""
    k = len(X)
    x = lambda i: X[0][i]
    y = lambda i, j: X[i][j]
    for i, j in itertools.combinations(range(1, k), 2):
        if not (y(i, j) >= 0 and y(i, j) <= x(i) and y(i, j) <= x(j) and y(i, j) >= x(i) + x(j) - 1):
            return False
    for i, j, l in itertools.combinations(range(1, k), 3):
        if x(i) + x(j) + x(l) > y(i, j) + y(i, l) + y(j, l) + 1:
            return False
        for (a, b, c) in ((i, j, l), (j, i, l), (l, i, j)):
            if y(a, b) + y(a, c) > x(a) + y(b, c):
                return False
    return True


def bh_violators(X, first=()):
    """All integer (v, s) with linearized (v^T x - s)(v^T x - s - 1) < 0 at moment matrix X (PD, X_ii = X_0i).
    With u = (-s, v): slack = u^T X u - e0^T X u = (u - e0/2)^T X (u - e0/2) - 1/4."""
    k = len(X)
    c = [F(1, 2)] + [F(0)] * (k - 1)
    out = []
    for u in enum_ellipsoid(X, c, F(1, 4), first):
        out.append((tuple(u[1:]), -u[0]))
    return out


FAIL = []


def check(name, cond, info=""):
    if not cond:
        FAIL.append((name, info))
        print("  FAIL", name, info)


# ----------------------------------------------------------------- [A] Lemma 6
def check_lemma6(trials=300):
    for _ in range(trials):
        k = random.randint(2, 6)
        X = [[F(0)] * (k + 1) for _ in range(k + 1)]
        X[0][0] = F(1)
        for i in range(1, k + 1):
            X[0][i] = X[i][0] = X[i][i] = F(random.randint(-7, 7), random.randint(1, 7))
            for j in range(i + 1, k + 1):
                X[i][j] = X[j][i] = F(random.randint(-7, 7), random.randint(1, 7))
        g = random.randint(1, k)
        A = [[F(int(i == j)) for j in range(k + 1)] for i in range(k + 1)]
        A[g][0], A[g][g] = F(1), F(-1)
        AXAt = [[sum(A[i][a] * X[a][b] * A[j][b] for a in range(k + 1) for b in range(k + 1))
                 for j in range(k + 1)] for i in range(k + 1)]
        Y = switch_bqp(X, g)
        check("L6(i)", Y == AXAt)
        v = [random.randint(-3, 3) for _ in range(k)]
        s = random.randint(-4, 4)
        v2 = v[:]
        v2[g - 1] = -v2[g - 1]
        check("L6(ii)", bh_lin(Y, v, s) == bh_lin(X, v2, s - v[g - 1]))
        check("L6(iv)", cut_of_moment(Y) == switch_cut(cut_of_moment(X), {g}))
    print(f"[A] Lemma 6 (i), (ii), (iv): {trials} random rational points, k <= 6 variables")


# ----------------------------------------------------------------- [B] Corollary 9
def check_cor9():
    cnt = withc = 0
    for trial in range(36):
        if trial < 16:
            q = 3
        elif trial < 28:
            q = 4
        else:
            q = 5
        sets, p = x3c(q, random.randint(1, 3) if q < 5 else random.randint(0, 2), plant=random.random() < 0.6)
        n = len(sets)
        N = 8 * n + 2 * p + 1
        eps = F(1, N)
        M = build_M(sets, p)
        X = moment(M, eps)
        g = n + 1
        P = switch_bqp(X, g)
        K = len(P)
        C = covers(sets, p)
        cnt += 1
        withc += bool(C)
        # (a)
        check("C9(a) entries", P[0][g] == 1 - F(2 * p - 1, 4 * N) and all(P[i][g] == F(22, 4 * N) for i in range(1, n + 1)))
        check("C9(a) box/int", all(0 <= P[i][j] <= 1 and (4 * N * P[i][j]).denominator == 1 and 4 * N * P[i][j] <= 4 * N
                                   for i in range(K) for j in range(K)))
        check("C9(a) PD", is_pd(P) and all(P[i][i] == P[0][i] for i in range(1, K)))
        # (b) complete BH violators
        bv = set(bh_violators(P))
        want = set()
        for T in C:
            v = tuple(1 if (i < n and i in T) or i == n else 0 for i in range(n + 1))
            want.add((v, 1))
            want.add((tuple(-a for a in v), -2))
        check("C9(b) BH set", bv == want, (sets, sorted(bv)))
        for (v, s) in bv:
            check("C9(b) slack", bh_lin(P, v, s) == -F(1, 2 * N))
        # (10) brute force
        v10 = {}
        for r in range(1, K):
            for S in itertools.combinations(range(1, K), r):
                xs = sum(P[0][i] for i in S)
                ys = sum(P[i][j] for i, j in itertools.combinations(S, 2))
                for s in range(r):
                    viol = s * xs - ys - F(s * (s + 1), 2)
                    if viol > 0:
                        v10[(S, s)] = viol
        want10 = {(tuple(sorted([i + 1 for i in T] + [g])), 1): F(1, 4 * N) for T in C}
        check("C9(b) (10) set", v10 == want10, (sets, v10))
        # (c) explicit triangle family, (e) cut image
        check("C9(c) triangles", bqp_triangles_ok(P))
        dP = cut_of_moment(P)
        check("C9(e) cut image", dP == switch_cut([[eps * a for a in r] for r in dist_from_M(M)], {g}))
        check("C9(e) elliptope/metric", elliptope_pd(dP) and metric_ok(dP))
    print(f"[B] Corollary 9: {cnt} X3C instances (q = 3: 16, q = 4: 12, q = 5: 8; {withc} with a cover): "
          f"entries, box, 4N-integrality, PD; complete BH violators (own enumeration) = (1_C+e_g,1) ~ (-1_C-e_g,-2), "
          f"slack -1/(2N); all violated (10) = (C u g, 1) with 1/(4N); explicit BQP triangles; cut image")


# ----------------------------------------------------------------- [C] Corollary 10
def lifted(sets, p, q, tau2):
    n = len(sets)
    m = q - 2
    M = build_M(sets, p)
    L = n + 1 + m
    Mt = [[F(0)] * L for _ in range(L)]
    for i in range(n + 1):
        for j in range(n + 1):
            Mt[i][j] = M[i][j]
    for j in range(n + 1, L):
        Mt[j][j] = tau2
    return M, Mt


def check_cor10():
    cnt = withc = bf = 0
    sizes = set()
    for trial in range(40):
        q = 3 if trial < 18 else (4 if trial < 32 else 5)
        sets, p = x3c(q, random.randint(1, 3) if q < 5 else random.randint(0, 2), plant=random.random() < 0.6)
        n = len(sets)
        m = q - 2
        N = 8 * n + 2 * p + 1
        eps = F(1, N)
        tau2 = F(1, 8 * q)
        M, Mt = lifted(sets, p, q, tau2)
        C = covers(sets, p)
        cnt += 1
        withc += bool(C)
        V = n + 2 + m                       # root, n sets, g, m copies
        g = n + 1
        U = set(range(g, V))
        # explicit d~ from the note's formulas vs d(M~)
        d = dist_from_M(M)                  # on {0} u sets u {g}
        dt = dist_from_M(Mt)
        okd = all(dt[a][b] == d[a][b] for a in range(n + 2) for b in range(n + 2))
        for j in range(n + 2, V):
            okd &= dt[0][j] == tau2
            for k2 in range(n + 2, V):
                if k2 != j:
                    okd &= dt[j][k2] == 2 * tau2
            for u in range(1, n + 2):
                okd &= dt[j][u] == d[0][u] + tau2
        check("C10 explicit d~", okd)
        # (a) complete hypermetric violators of d~
        delta = [Mt[i][i] for i in range(len(Mt))]
        w = solve(Mt, delta)
        st = sum(a * b for a, b in zip(delta, w))
        c = [a / 2 for a in w]
        hv = set(enum_ellipsoid(Mt, c, st / 4, first=tuple(range(n + 1, n + 1 + m))))
        # filter g < 0 exactly (strict ellipsoid equals g < 0)
        gfun = lambda z: sum(z[i] * Mt[i][j] * z[j] for i in range(len(z)) for j in range(len(z))) - sum(
            delta[i] * z[i] for i in range(len(z)))
        check("C10(a) g<0", all(gfun(z) < 0 for z in hv))
        R = 2 * math.isqrt(q) + 3
        want = set()
        for T in C:
            x = tuple(1 if i in T else 0 for i in range(n))
            for ww in itertools.product(range(-R, R + 1), repeat=m):
                if sum(t * (t - 1) for t in ww) < 4 * q:
                    want.add(x + (-1,) + ww)
        check("C10(a) set", hv == want, (sets, len(hv), len(want)))
        check("C10(a) gonality", all(abs(1 - sum(z)) + sum(abs(t) for t in z) >= 2 * q - 1 for z in hv))
        # (b)
        X = moment(Mt, eps)
        Y = [r[:] for r in X]
        Y[0][0] -= F(1, 4)
        s0 = sum(a * b for a, b in zip(delta[:n + 1], solve(M, delta[:n + 1])))
        check("C10(b) s~", st == s0 + m * tau2 and eps * st < F(3, 4) and eps * s0 < F(1, 2))
        check("C10(b) PD", is_pd(X) and is_pd(Y))
        check("C10(b) int", all((8 * q * N * X[i][j]).denominator == 1 and 0 <= X[i][j] <= 1
                                for i in range(V) for j in range(V)))
        D = [[eps * a for a in r] for r in dt]
        check("C10(b) cut image", cut_of_moment(X) == D)
        check("C10(b) box/ell/metric", all(0 < D[a][b] < 1 for a in range(V) for b in range(V) if a != b)
              and elliptope_pd(D) and metric_ok(D))
        # complete rounded psd violators of eps*d~ (split enumeration on X): u = (-s, v) <-> b = -(2s+1-sum v, ...)?
        # Use the identity: rounded psd b (sigma odd) violated at cut image  <=>  BH (v, s) violated at X with
        # v = -b_W and s = (sigma - 1)/2 ... derive b from (v, s): b_W = -v, sigma = -(2s+1), b_0 = sigma - sum b_W.
        rp = set()
        for (v, s) in bh_violators(X, first=tuple(range(n + 2, V))):
            bW = [-a for a in v]
            sig = -(2 * s + 1)
            b = tuple([sig - sum(bW)] + bW)
            check("C10 rp identity", Qb(b, D) - F(sig * sig - 1, 4) == -bh_lin(X, v, s) / 1)
            rp.add(b)
        check("C10(b) |sigma|=1", all(abs(sum(b)) == 1 for b in rp))
        hyp_b = set()
        for z in hv:
            b = tuple([1 - sum(z)] + list(z))
            hyp_b.add(b)
            hyp_b.add(tuple(-a for a in b))
        check("C10(b) rp = +-hyp", rp == hyp_b)
        oc = {b for b in rp if all(a in (-1, 0, 1) for a in b)}
        check("C10(c) oc iff cover", bool(oc) == bool(C))
        for T in C:
            bstar = tuple([0] + [1 if i in T else 0 for i in range(n)] + [-1] + [-1] * m)
            check("C10(c) b*", bstar in oc and eps * Qb(bstar, dt) == F(q + 2, 4 * q * N))
        if V <= 10:   # brute force odd clique over {0,+-1}^V
            den = 8 * q * N
            Di = [[int(den * D[a][b]) for b in range(V)] for a in range(V)]
            bfs = set()
            for b in itertools.product((-1, 0, 1), repeat=V):
                sg = sum(b)
                if sg % 2 and 4 * sum(b[a] * b[c2] * Di[a][c2] for a in range(V) for c2 in range(a + 1, V)) > den * (sg * sg - 1):
                    bfs.add(b)
            check("C10(c) brute force", bfs == oc)
            bf += 1
        # (d) switched point
        D2 = switch_cut(D, U)
        check("C10(d) box/int/ell/metric", all(0 < D2[a][b] < 1 and (8 * q * N * D2[a][b]).denominator == 1
                                                for a in range(V) for b in range(V) if a != b)
              and elliptope_pd(D2) and metric_ok(D2))
        v18 = {}
        for r in range(3, V + 1, 2):
            for S in itertools.combinations(range(V), r):
                lhs = sum(D2[a][b] for a, b in itertools.combinations(S, 2))
                if lhs > F(r * r - 1, 4):
                    v18[S] = lhs - F(r * r - 1, 4)
        want18 = {tuple(sorted([i + 1 for i in T] + sorted(U))): F(q + 2, 4 * q * N) for T in C}
        check("C10(d) (18) set", v18 == want18, (sets, v18))
        sizes |= {len(S) for S in v18}
        # complete rounded psd violators at d'' (split enumeration on its moment matrix), then filter +-1_S
        X2 = moment_of_cut(D2)
        rp2 = set()
        for (v, s) in bh_violators(X2, first=tuple(range(n + 2, V))):
            bW = [-a for a in v]
            sig = -(2 * s + 1)
            rp2.add(tuple([sig - sum(bW)] + bW))
        sig_map = {tuple((-1 if i in U else 1) * b[i] for i in range(V)) for b in rp}
        check("C10(d) rp at d'' = Sigma * rp", rp2 == sig_map)
        ones = {b for b in rp2 if set(b) <= {0, 1} or set(b) <= {0, -1}}
        want_ones = set()
        for S in want18:
            bb = tuple(1 if i in S else 0 for i in range(V))
            want_ones.add(bb)
            want_ones.add(tuple(-a for a in bb))
        check("C10(d) +-1_S among all rp", ones == want_ones)
    print(f"[C] Corollary 10: {cnt} X3C instances (q = 3: 18, q = 4: 14, q = 5: 8; {withc} with a cover), "
          f"tau2 = 1/(8q): explicit d~ formulas; complete hypermetric violators (own enumeration) = (1_C,-1,w), "
          f"sum w(w-1) < 4q; s~ = s + m tau2, eps s~ < 3/4; X~ and X~ - e0e0^T/4 PD; 8qN-integral; complete rounded "
          f"psd violators of eps d~ have |sigma| = 1 and equal +-hypermetric; odd clique iff cover; b* value "
          f"(q+2)/(4qN); brute force over {{0,+-1}}^V on {bf} instances; d'' in box, 8qN-integral, elliptope, metric; "
          f"all violated (18) = C u U (sizes {sorted(sizes)}); complete rounded psd violators at d'' = Sigma*(those at "
          f"eps d~), and their +-1_S members are exactly C u U")


def check_cor10_control_and_threshold():
    """tau2 = 1/4: no odd clique violated although a cover exists (q in {4,5}); and threshold: b* is violated iff
    2(q-2) tau2 < 1/2, i.e. tau2 < 1/(4(q-2))."""
    ok_ctrl = 0
    for trial in range(8):
        q = 4 + trial % 2
        sets, p = x3c(q, random.randint(1, 2), plant=True)
        n = len(sets)
        N = 8 * n + 2 * p + 1
        eps = F(1, N)
        M, Mt = lifted(sets, p, q, F(1, 4))
        X = moment(Mt, eps)
        Y = [r[:] for r in X]
        Y[0][0] -= F(1, 4)
        viol = bh_violators(X, first=tuple(range(n + 2, n + 2 + q - 2)))
        oc = []
        for (v, s) in viol:
            bW = [-a for a in v]
            sig = -(2 * s + 1)
            b = [sig - sum(bW)] + bW
            if all(a in (-1, 0, 1) for a in b):
                oc.append(b)
        ok_ctrl += is_pd(Y) and bool(viol) and not oc
    thr = 0
    for q in (3, 4, 5, 6):
        sets, p = x3c(q, 1, plant=True)
        n = len(sets)
        T = covers(sets, p)[0]
        m = q - 2
        for tau2, expect in ((F(1, 4 * m) - F(1, 1000), True), (F(1, 4 * m), False)):
            M, Mt = lifted(sets, p, q, tau2)
            dt = dist_from_M(Mt)
            bstar = [0] + [1 if i in T else 0 for i in range(n)] + [-1] + [-1] * m
            thr += (Qb(bstar, dt) > 0) == expect
    print(f"[C'] control tau2 = 1/4: {ok_ctrl}/8 instances with a cover have hypermetric violators but no violated "
          f"odd clique inequality (expected 8); threshold tau2 < 1/(4(q-2)) for b*: {thr}/8 as expected")
    check("C10 control", ok_ctrl == 8)
    check("C10 threshold", thr == 8)


# ----------------------------------------------------------------- [D] facets
def facet10(nv, S, s):
    pts = []
    E = list(itertools.combinations(range(nv), 2))
    for x in itertools.product((0, 1), repeat=nv):
        xs = sum(x[i] for i in S)
        ys = sum(x[i] * x[j] for i, j in itertools.combinations(S, 2))
        lhs, rhs = 2 * s * xs, 2 * ys + s * (s + 1)
        assert lhs <= rhs
        if lhs == rhs:
            pts.append(list(x) + [x[i] * x[j] for i, j in E])
    return affine_rank(pts) == nv + len(E) - 1


def facet18(nv, S):
    E = list(itertools.combinations(range(nv), 2))
    pts = []
    r = len(S)
    for side in itertools.product((0, 1), repeat=nv - 1):
        sd = (0,) + side
        z = [int(sd[a] != sd[b]) for a, b in E]
        lhs = sum(z[k] for k, (a, b) in enumerate(E) if a in S and b in S)
        assert 4 * lhs <= r * r - 1
        if 4 * lhs == r * r - 1:
            pts.append(z)
    return affine_rank(pts) == len(E) - 1


def check_facets():
    r10 = [facet10(q + 1, tuple(range(q + 1)), 1) for q in (3, 4, 5)] + [facet10(6, (0, 1, 2, 3), 1)]
    # (18) containing the root vertex 0 (the case not covered by the permutation argument when S = V)
    r18 = [facet18(5, (0, 1, 2, 3, 4)), facet18(6, (1, 2, 3, 4, 5)), facet18(7, (0, 2, 3, 5, 6)), facet18(7, tuple(range(7)))]
    print(f"[D] facets by exact affine rank (dimension - 1): (10) (|S|,s) = (4,1),(5,1),(6,1) in BQP_|S|, (4,1) in BQP_6: "
          f"{r10}; (18) |S| = 5 in CUT_5 (S = V), CUT_6, CUT_7 (root in S), |S| = 7 in CUT_7: {r18}")
    check("facets", all(r10) and all(r18))


# ----------------------------------------------------------------- [E] cut image of (10), symbolic
def check_cut_image_symbolic():
    import sympy as sp
    ok = True
    for k in range(1, 7):
        x = sp.symbols(f"x1:{k + 1}")
        y = {(i, j): sp.Symbol(f"y{i}_{j}") for i in range(k) for j in range(i + 1, k)}
        s = sp.Symbol("s", integer=True)
        lhs10 = s * sum(x) - sum(y.values()) - s * (s + 1) / 2          # (10) violated iff > 0
        # cut image: z_0i = x_i, z_ij = x_i + x_j - 2 y_ij; b = -(2s+1-k, 1_S)
        b0 = -(2 * s + 1 - k)
        Q = sum(b0 * (-1) * x[i] for i in range(k)) + sum(x[i] + x[j] - 2 * y[(i, j)] for (i, j) in y)
        sig = b0 - k
        viol_rp = Q - (sig ** 2 - 1) / 4
        ok &= sp.simplify(viol_rp - 2 * lhs10) == 0
    print(f"[E] remark after Corollary 9 (symbolic, |S| = 1..6, symbolic s): violation of rounded psd b = -(2s+1-|S|, 1_S) "
          f"at the cut image = 2 x violation of (10): {ok}")
    check("cut image", ok)


# ----------------------------------------------------------------- [F] closed form s(n)
def check_closed_form():
    ok = True
    for nn in range(1, 31):
        sets = [(0, 1, 2)] * nn + [(3, 4, 5)]
        M = build_M(sets, 6)
        dl = [M[i][i] for i in range(len(M))]
        s = sum(a * b for a, b in zip(dl, solve(M, dl)))
        ok &= s == F(77 * (193 * nn + 108), 4 * (141 * nn + 272))
    lim = F(77 * 193, 4 * 141)
    print(f"[F] s(n) = 77(193n+108)/(4(141n+272)) for n = 1..30 (own solve): {ok}; limit 77*193/(4*141) = {lim} "
          f"(= 14861/564: {lim == F(14861, 564)}); increasing since 193*272 - 108*141 = {193 * 272 - 108 * 141} > 0")
    check("closed form", ok and lim == F(14861, 564))


if __name__ == "__main__":
    check_lemma6()
    check_cor9()
    check_cor10()
    check_cor10_control_and_threshold()
    check_facets()
    check_cut_image_symbolic()
    check_closed_form()
    print(f"elapsed {time.time() - T0:.1f} s")
    print("REVIEWER R3 CHECKS PASSED" if not FAIL else f"REVIEWER R3 CHECKS FAILED: {len(FAIL)}")
    sys.exit(0 if not FAIL else 1)
