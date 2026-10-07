"""Review round 3: independent exact checks of the material added in revision r2
(Lemma 6, Corollary 9 and its remark, Corollary 10 and its control, facets, Section 9
violation numbers).  Written from the note's statements only; does not import the
stream's code or the earlier partial r3 script.  Exact Fraction arithmetic throughout.

Complete enumeration of violated inequalities uses one generic routine: all integer y with
(y - c)^T G (y - c) < R for a positive definite rational G (LDL^T, last coordinate first,
float ranges widened by 1 and exact filtering at every level).

* Violated Boros-Hammer data (v, s) at a Boolean quadric moment matrix X: with
  uhat = (-s, v), the slack of (13) is uhat^T X uhat - e0^T X uhat, so the violated data are
  the integer uhat with (uhat - e0/2)^T X (uhat - e0/2) < X_00 / 4 = 1/4.
* Violated rounded psd inequalities b (sigma(b) odd) at a cut vector z: with
  Z = J - 2 D(z), b violates iff b^T Z b < 1.  Odd sigma is parametrized by
  y = (k, b_W), b_0 = 2k + 1 - sum(b_W), an affine bijection onto the odd-sigma vectors.
  This works in cut space directly and does not use the split identity of the note.
"""
import itertools
import math
import random
import sys
import time
from fractions import Fraction as F

random.seed(31003)
T0 = time.time()
FAIL = []


def check(cond, msg):
    if not cond:
        FAIL.append(msg)
        print("FAIL:", msg)


# ------------------------------------------------------------------ linear algebra
def ldl(G):
    k = len(G)
    L = [[F(0)] * k for _ in range(k)]
    D = [F(0)] * k
    for j in range(k):
        D[j] = G[j][j] - sum(L[j][m] * L[j][m] * D[m] for m in range(j))
        if D[j] <= 0:
            return None
        L[j][j] = F(1)
        for i in range(j + 1, k):
            L[i][j] = (G[i][j] - sum(L[i][m] * L[j][m] * D[m] for m in range(j))) / D[j]
    return L, D


def is_pd(G):
    return ldl(G) is not None


def inv(G):
    k = len(G)
    A = [list(map(F, G[i])) + [F(int(i == j)) for j in range(k)] for i in range(k)]
    for c in range(k):
        piv = next(r for r in range(c, k) if A[r][c] != 0)
        A[c], A[piv] = A[piv], A[c]
        pv = A[c][c]
        A[c] = [a / pv for a in A[c]]
        for r in range(k):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [a - f * b for a, b in zip(A[r], A[c])]
    return [row[k:] for row in A]


def matvec(G, v):
    return [sum(G[i][j] * v[j] for j in range(len(v))) for i in range(len(G))]


def qform(G, v):
    return sum(v[i] * G[i][j] * v[j] for i in range(len(v)) for j in range(len(v)) if v[i] and v[j])


def rank(rows):
    A = [list(map(F, r)) for r in rows]
    if not A:
        return 0
    rk, ncol = 0, len(A[0])
    for c in range(ncol):
        piv = next((r for r in range(rk, len(A)) if A[r][c] != 0), None)
        if piv is None:
            continue
        A[rk], A[piv] = A[piv], A[rk]
        for r in range(rk + 1, len(A)):
            if A[r][c] != 0:
                f = A[r][c] / A[rk][c]
                A[r] = [a - f * b for a, b in zip(A[r], A[rk])]
        rk += 1
    return rk


def enum_ellipsoid(G, c, R):
    """All integer y with (y - c)^T G (y - c) < R (G positive definite).
    Coordinates are reordered so that those with the smallest (G^-1)_jj (narrowest range) are
    enumerated first; this only changes the search order, not the set returned."""
    k = len(G)
    Gi = inv(G)
    perm = sorted(range(k), key=lambda j: -Gi[j][j])
    Gp = [[G[perm[a]][perm[b]] for b in range(k)] for a in range(k)]
    cp = [c[perm[a]] for a in range(k)]
    res = []
    for yp in _enum_ellipsoid(Gp, cp, R):
        y = [0] * k
        for a in range(k):
            y[perm[a]] = yp[a]
        res.append(tuple(y))
    return res


def _enum_ellipsoid(G, c, R):
    k = len(G)
    L, D = ldl(G)
    out = []
    y = [0] * k

    def rec(j, used):
        if j < 0:
            out.append(tuple(y))
            return
        t = c[j] - sum(L[i][j] * (y[i] - c[i]) for i in range(j + 1, k))
        rem = R - used
        rad = math.sqrt(max(float(rem / D[j]), 0.0))
        lo, hi = math.floor(float(t) - rad) - 1, math.ceil(float(t) + rad) + 1
        for val in range(lo, hi + 1):
            term = D[j] * (val - t) ** 2
            if used + term < R:
                y[j] = val
                rec(j - 1, used + term)
        y[j] = 0

    rec(k - 1, F(0))
    return out


# ------------------------------------------------------------------ objects
def moment(xv, yv, k):
    """Moment matrix, index 0 = constant, 1..k = variables; yv[(i,j)] with i<j (1-based)."""
    X = [[F(0)] * (k + 1) for _ in range(k + 1)]
    X[0][0] = F(1)
    for i in range(1, k + 1):
        X[0][i] = X[i][0] = X[i][i] = xv[i]
    for (i, j), val in yv.items():
        X[i][j] = X[j][i] = val
    return X


def from_moment(X):
    k = len(X) - 1
    xv = {i: X[0][i] for i in range(1, k + 1)}
    yv = {(i, j): X[i][j] for i in range(1, k + 1) for j in range(i + 1, k + 1)}
    return xv, yv


def bh_slack(xv, yv, v, s):
    """Slack RHS - LHS of (13): sum v_i(2s+1-v_i) x_i <= 2 sum v_i v_j y_ij + s(s+1)."""
    lhs = sum(v[i] * (2 * s + 1 - v[i]) * xv[i] for i in xv)
    rhs = 2 * sum(v[i] * v[j] * yv[(i, j)] for (i, j) in yv) + s * (s + 1)
    return rhs - lhs


def eq12_slack(xv, yv, S, T, s):
    """Slack of Letchford's (12) as printed (p. 9)."""
    lhs = s * sum(xv[i] for i in S) + sum(yv[tuple(sorted((i, j)))] for i in S for j in T)
    rhs = ((s + 1) * sum(xv[i] for i in T)
           + sum(yv[(i, j)] for i, j in itertools.combinations(sorted(S), 2))
           + sum(yv[(i, j)] for i, j in itertools.combinations(sorted(T), 2))
           + F(s * (s + 1), 2))
    return rhs - lhs


def eq10_slack(xv, yv, S, s):
    """Slack of Padberg's clique inequality (10): s x(S) <= y(S) + s(s+1)/2."""
    return (sum(yv[(i, j)] for i, j in itertools.combinations(sorted(S), 2)) + F(s * (s + 1), 2)
            - s * sum(xv[i] for i in S))


def cut_image(xv, yv):
    """Covariance map (Letchford 2022, Thm 1) with root 0: z_0i = x_i, z_ij = x_i + x_j - 2y_ij."""
    z = {}
    for i in xv:
        z[(0, i)] = xv[i]
    for (i, j), val in yv.items():
        z[(i, j)] = xv[i] + xv[j] - 2 * val
    return z


def zget(z, u, v):
    return z[(u, v)] if u < v else z[(v, u)]


def Zmat(z, nodes):
    return [[F(1) if u == v else 1 - 2 * zget(z, u, v) for v in nodes] for u in nodes]


def Qb(b, z, nodes):
    return sum(b[a] * b[c] * zget(z, nodes[a], nodes[c])
               for a in range(len(nodes)) for c in range(a + 1, len(nodes)) if b[a] and b[c])


def switch_cut(z, U):
    return {e: (1 - val if ((e[0] in U) != (e[1] in U)) else val) for e, val in z.items()}


def metric_ok(z, nodes):
    for a, b, c in itertools.combinations(nodes, 3):
        ab, ac, bc = zget(z, a, b), zget(z, a, c), zget(z, b, c)
        if ab + ac + bc > 2 or ab > ac + bc or ac > ab + bc or bc > ab + ac:
            return False
    return True


def violated_rpsd(z, nodes):
    """All b in Z^nodes with sigma(b) odd and Q(b,z) > (sigma^2-1)/4 (complete)."""
    Z = Zmat(z, nodes)
    if not is_pd(Z):
        raise ValueError("Z not PD")
    k = len(nodes)
    # b = T y + e0, y = (k0, b_1..b_{k-1}), b_0 = 2 k0 + 1 - sum b_W
    T = [[F(0)] * k for _ in range(k)]
    T[0][0] = F(2)
    for i in range(1, k):
        T[0][i] = F(-1)
        T[i][i] = F(1)
    e0 = [F(1)] + [F(0)] * (k - 1)
    G = [[sum(T[a][i] * Z[a][b] * T[b][j] for a in range(k) for b in range(k)) for j in range(k)]
         for i in range(k)]
    h = [sum(T[a][i] * Z[a][0] for a in range(k)) for i in range(k)]  # T^T Z e0
    Gi = inv(G)
    c = [-x for x in matvec(Gi, h)]
    R = 1 - Z[0][0] + qform(G, c)
    res = []
    for y in enum_ellipsoid(G, c, R):
        b = [2 * y[0] + 1 - sum(y[1:])] + list(y[1:])
        sig = sum(b)
        viol = Qb(b, z, nodes) - F(sig * sig - 1, 4)
        check(viol > 0 and sig % 2 != 0, "rpsd enumeration returned a non-violator")
        res.append((tuple(b), viol))
    return res


def violated_bh(X):
    """All integer (v, s) with BH slack < 0 at moment matrix X (complete)."""
    # slack = u^T X u - (X e0)^T u = (u - e0/2)^T X (u - e0/2) - X_00/4
    c = [F(1, 2)] + [F(0)] * (len(X) - 1)
    R = X[0][0] / 4
    xv, yv = from_moment(X)
    res = []
    for u in enum_ellipsoid(X, c, R):
        s = -u[0]
        v = {i: u[i] for i in range(1, len(X))}
        sl = bh_slack(xv, yv, v, s)
        check(sl < 0, "BH enumeration returned a non-violator")
        res.append((tuple(u[1:]), s, sl))
    return res


# ------------------------------------------------------------------ instances
def x3c_instance(q, n, plant, two_covers=False):
    p = 3 * q
    sets = []
    if plant:
        perm = list(range(p))
        random.shuffle(perm)
        sets += [frozenset(perm[3 * t:3 * t + 3]) for t in range(q)]
        if two_covers:
            random.shuffle(perm)
            sets += [frozenset(perm[3 * t:3 * t + 3]) for t in range(q)]
    while len(sets) < n:
        sets.append(frozenset(random.sample(range(p), 3)))
    random.shuffle(sets)
    return p, sets


def exact_covers(p, sets):
    out = []
    n = len(sets)
    q = p // 3
    for C in itertools.combinations(range(n), q):
        u = set()
        ok = True
        for i in C:
            if u & sets[i]:
                ok = False
                break
            u |= sets[i]
        if ok and len(u) == p:
            out.append(frozenset(C))
    return sorted(set(out), key=sorted)


def build_M(p, sets):
    """Section 3 with eta^2 = (p-1)/4; indices 0..n-1 sets, n = g."""
    n = len(sets)
    eta2 = F(p - 1, 4)
    M = [[F(0)] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(n):
            M[i][j] = F(4 * (i == j) + len(sets[i] & sets[j]))
        M[i][n] = M[n][i] = F(len(sets[i]), 2)
    M[n][n] = F(p, 4) + eta2
    return M


def bq_point(M, eps):
    """X(eps) as dicts with variables 1..k (k = len(M))."""
    k = len(M)
    xv = {i + 1: eps * M[i][i] for i in range(k)}
    yv = {(i + 1, j + 1): eps * M[i][j] for i in range(k) for j in range(i + 1, k)}
    return xv, yv


# ================================================================== [A] Lemma 6
def check_lemma6():
    nfail0 = len(FAIL)
    trials = 0
    for _ in range(300):
        k = random.randint(2, 6)
        g = random.randint(1, k)
        xv = {i: F(random.randint(-9, 9), random.randint(1, 7)) for i in range(1, k + 1)}
        yv = {(i, j): F(random.randint(-9, 9), random.randint(1, 7))
              for i in range(1, k + 1) for j in range(i + 1, k + 1)}
        # switching on {g} exactly as in Letchford 2022, Definition 2
        xs = dict(xv)
        xs[g] = 1 - xv[g]
        ys = {}
        for (i, j), val in yv.items():
            if g in (i, j):
                other = i if j == g else j
                ys[(i, j)] = xv[other] - val
            else:
                ys[(i, j)] = val
        X = moment(xv, yv, k)
        A = [[F(int(r == c)) for c in range(k + 1)] for r in range(k + 1)]
        A[g] = [F(0)] * (k + 1)
        A[g][0], A[g][g] = F(1), F(-1)
        AXAt = [[sum(A[r][a] * X[a][b] * A[c][b] for a in range(k + 1) for b in range(k + 1))
                 for c in range(k + 1)] for r in range(k + 1)]
        check(AXAt == moment(xs, ys, k), "Lemma 6(i) AXA^T")
        A2 = [[sum(A[r][a] * A[a][c] for a in range(k + 1)) for c in range(k + 1)] for r in range(k + 1)]
        check(all(A2[r][c] == (r == c) for r in range(k + 1) for c in range(k + 1)), "A^2 = I")
        # (ii)
        for _ in range(5):
            v = {i: random.randint(-3, 3) for i in range(1, k + 1)}
            s = random.randint(-4, 4)
            vp = dict(v)
            vp[g] = -v[g]
            check(bh_slack(xs, ys, v, s) == bh_slack(xv, yv, vp, s - v[g]), "Lemma 6(ii)")
            trials += 1
        # (iii) on (12) directly
        idx = list(range(1, k + 1))
        lab = [random.choice("ST0") for _ in idx]
        S = {i for i, l in zip(idx, lab) if l == "S"}
        T = {i for i, l in zip(idx, lab) if l == "T"}
        s = random.randint(-3, 3)
        if g in S:
            S2, T2, s2 = S - {g}, T | {g}, s - 1
        elif g in T:
            S2, T2, s2 = S | {g}, T - {g}, s + 1
        else:
            S2, T2, s2 = S, T, s
        check(eq12_slack(xs, ys, S, T, s) == eq12_slack(xv, yv, S2, T2, s2), "Lemma 6(iii)")
        # (iv)
        z = cut_image(xv, yv)
        check(cut_image(xs, ys) == switch_cut(z, {g}), "Lemma 6(iv)")
    print(f"[A] Lemma 6 (i)-(iv): 300 random rational points (k <= 6), {trials} (v,s) pairs, "
          f"(12) map and cut switching: {len(FAIL) - nfail0} failures")


def check_lemma6_symbolic():
    import sympy as sp
    k = 4
    xs = sp.symbols("x1:%d" % (k + 1))
    ys = {(i, j): sp.Symbol(f"y{i}{j}") for i in range(1, k + 1) for j in range(i + 1, k + 1)}
    vs = sp.symbols("v1:%d" % (k + 1))
    s = sp.Symbol("s")
    g = 2

    def sl(x, y, v, s):
        lhs = sum(v[i - 1] * (2 * s + 1 - v[i - 1]) * x[i - 1] for i in range(1, k + 1))
        rhs = 2 * sum(v[i - 1] * v[j - 1] * y[(i, j)] for (i, j) in y) + s * (s + 1)
        return rhs - lhs

    x2 = list(xs)
    x2[g - 1] = 1 - xs[g - 1]
    y2 = {}
    for (i, j), val in ys.items():
        if g in (i, j):
            other = i if j == g else j
            y2[(i, j)] = xs[other - 1] - val
        else:
            y2[(i, j)] = val
    vp = list(vs)
    vp[g - 1] = -vs[g - 1]
    diff = sp.expand(sl(x2, y2, vs, s) - sl(xs, ys, vp, s - vs[g - 1]))
    check(diff == 0, "Lemma 6(ii) symbolic")
    # Corollary 10: d~ formulas from M~ = M + tau^2 I, symbolic
    t2, a, b2 = sp.symbols("tau2 a b")
    # d(0,o) = M~_oo = tau2; d(o,o') = 2 tau2; d(o,u) = M_uu + tau2 - 0 = d(0,u) + tau2
    ok = sp.simplify((t2 + t2 - 0) - 2 * t2) == 0 and sp.simplify((a + t2 - 0) - (a + t2)) == 0
    check(ok, "d~ formulas")
    print(f"[A'] Lemma 6(ii) symbolic identity (sympy {sp.__version__}, k = 4, g = 2, generic x, y, v, s): "
          f"{'holds' if diff == 0 else 'FAILS'}")


# ================================================================== [B] Corollary 9
def check_cor9(instances):
    nfail0 = len(FAIL)
    stats = {"yes": 0, "inst": 0}
    for p, sets in instances:
        n = len(sets)
        q = p // 3
        N = 8 * n + 2 * p + 1
        eps = F(1, N)
        M = build_M(p, sets)
        covers = exact_covers(p, sets)
        stats["inst"] += 1
        print(f"  [B] instance {stats['inst']} q={q} n={n} t={time.time() - T0:.1f}", file=sys.stderr, flush=True)
        stats["yes"] += bool(covers)
        k = n + 1
        g = n + 1  # 1-based index of g
        xv, yv = bq_point(M, eps)
        # switching on {g} (Letchford Def. 2)
        xs = dict(xv)
        xs[g] = 1 - xv[g]
        ys = {(i, j): (xv[i] - val if j == g else val) for (i, j), val in yv.items()}
        # (a)
        check(xs[g] == 1 - F(2 * p - 1, 4 * N), "9(a) x'_g")
        for i in range(1, n + 1):
            check(ys[(i, g)] == F(22, 4 * N), "9(a) y'_ig = 22/(4N)")
        Xp = moment(xs, ys, k)
        check(is_pd(Xp), "9(a) PD")
        ent = [Xp[i][j] for i in range(k + 1) for j in range(k + 1)]
        check(all(0 <= e <= 1 for e in ent), "9(a) in [0,1]")
        check(all((4 * N * e).denominator == 1 and 4 * N * e <= 4 * N for e in ent), "9(a) 4N integral")
        # (b) complete BH enumeration
        bh = violated_bh(Xp)
        pred = set()
        for C in covers:
            v = tuple(1 if (i - 1 in C or i == g) else 0 for i in range(1, k + 1))
            pred.add((v, 1))
            pred.add((tuple(-a for a in v), -2))
        got = {(v, s) for v, s, _ in bh}
        check(got == pred, f"9(b) violated BH data {got} vs {pred}")
        check(all(sl == F(-1, 2 * N) for _, _, sl in bh), "9(b) BH slack -1/(2N)")
        # (10) directly, all S and s = 0..|S|-1
        v10 = set()
        for r in range(1, k + 1):
            for S in itertools.combinations(range(1, k + 1), r):
                for s in range(0, r):
                    sl = eq10_slack(xs, ys, S, s)
                    if sl < 0:
                        v10.add((frozenset(S), s))
                        check(sl == F(-1, 4 * N), "9(b) (10) violation 1/(4N)")
        pred10 = {(frozenset({i + 1 for i in C} | {g}), 1) for C in covers}
        check(v10 == pred10, "9(b) violated (10)")
        # (12) directly, all ordered disjoint (S,T), s in a wide range
        v12 = set()
        for lab in itertools.product((0, 1, 2), repeat=k):
            S = [i + 1 for i in range(k) if lab[i] == 1]
            T = [i + 1 for i in range(k) if lab[i] == 2]
            if not S and not T:
                continue
            for s in range(-len(T) - 3, len(S) + 3):
                if eq12_slack(xs, ys, S, T, s) < 0:
                    v12.add((frozenset(S), frozenset(T), s))
        pred12 = set()
        for C in covers:
            SC = frozenset({i + 1 for i in C} | {g})
            pred12 |= {(SC, frozenset(), 1), (frozenset(), SC, -2)}
        check(v12 == pred12, "9(b) violated (12)")
        # (c) BH with support <= q satisfied: follows from complete enumeration; check supports
        check(all(sum(1 for a in v if a) == q + 1 for v, _, _ in bh), "9(c) support q+1")
        # triangle family (3)-(5), y>=0, (8), (9) directly
        tri = True
        for i, j in itertools.combinations(range(1, k + 1), 2):
            y = ys[(i, j)]
            if y < 0 or y > xs[i] or y > xs[j] or xs[i] + xs[j] > 1 + y:
                tri = False
        for i, j, l in itertools.combinations(range(1, k + 1), 3):
            yij, yil, yjl = ys[(i, j)], ys[(i, l)], ys[(j, l)]
            if xs[i] + xs[j] + xs[l] > yij + yil + yjl + 1:
                tri = False
            for a, b_, c_ in ((i, j, l), (j, i, l), (l, i, j)):
                if (ys[tuple(sorted((a, b_)))] + ys[tuple(sorted((a, c_)))]
                        > xs[a] + ys[tuple(sorted((b_, c_)))]):
                    tri = False
        check(tri, "9(c) triangle family")
        # (e) cut image: = eps*d switched on g; elliptope interior; metric; rpsd gonality
        nodes = list(range(0, k + 1))
        z = cut_image(xs, ys)
        z0 = cut_image(xv, yv)
        # eps*d from M by the inverse map, independently of the covariance map
        dM = {}
        for i in range(1, k + 1):
            dM[(0, i)] = eps * M[i - 1][i - 1]
        for i in range(1, k + 1):
            for j in range(i + 1, k + 1):
                dM[(i, j)] = eps * (M[i - 1][i - 1] + M[j - 1][j - 1] - 2 * M[i - 1][j - 1])
        check(z0 == dM, "cut image of X(eps) = eps*d")
        check(z == switch_cut(dM, {g}), "9(e) cut image = switched eps*d")
        check(is_pd(Zmat(z, nodes)), "9(e) elliptope interior")
        check(metric_ok(z, nodes), "9(e) metric polytope")
        rp = violated_rpsd(z, nodes)
        check(bool(rp) == bool(covers), "9(e) rpsd violated iff cover")
        check(all(sum(abs(a) for a in b) == 2 * q - 1 for b, _ in rp), "9(e) gonality 2q-1")
        # remark after Cor 9: violated (10) at P' has root coefficient |2s+1-|S|| = q-2
        for (S, s) in v10:
            check(abs(2 * s + 1 - len(S)) == q - 2, "remark: root coefficient q-2")
    print(f"[B] Corollary 9: {stats['inst']} X3C instances (q in {{3,4}}, {stats['yes']} with a cover): "
          f"P' entries, PD, 4N-integrality; complete BH enumeration = {{(1_C+e_g,1),(-1_C-e_g,-2)}} "
          f"slack -1/(2N); all (10) and all (12) by direct formulas; triangle family; cut image = "
          f"switched eps*d, elliptope, metric, all violated rounded psd of the cut image have gonality "
          f"2q-1: {len(FAIL) - nfail0} failures")


def check_clique_cut_image():
    nfail0 = len(FAIL)
    for _ in range(300):
        k = random.randint(2, 6)
        xv = {i: F(random.randint(-9, 9), random.randint(1, 7)) for i in range(1, k + 1)}
        yv = {(i, j): F(random.randint(-9, 9), random.randint(1, 7))
              for i in range(1, k + 1) for j in range(i + 1, k + 1)}
        S = random.sample(range(1, k + 1), random.randint(1, k))
        s = random.randint(-2, len(S) + 1)
        z = cut_image(xv, yv)
        nodes = list(range(0, k + 1))
        b = [-(2 * s + 1 - len(S))] + [-(1 if i in S else 0) for i in range(1, k + 1)]
        sig = sum(b)
        rpsd_slack = F(sig * sig - 1, 4) - Qb(b, z, nodes)
        check(2 * eq10_slack(xv, yv, S, s) == rpsd_slack, "remark after Cor 9: cut image of (10)")
    # (18) membership conditions of the remark
    ok = True
    for size in range(1, 9):
        for s in range(0, size):
            r = 2 * s + 1 - size
            is18 = r in (0, 1)
            pred = (size % 2 == 1 and s == (size - 1) // 2) or (size % 2 == 0 and s == size // 2)
            ok &= (is18 == pred)
    check(ok, "remark (18) subfamilies")
    print(f"[C] Remark after Cor 9: 2 x slack(10) = slack of rounded psd b = -(2s+1-|S|, 1_S) at the cut image, "
          f"300 random points; (18) arises iff (|S| odd, s=(|S|-1)/2) or (|S| even, s=|S|/2): "
          f"{len(FAIL) - nfail0} failures")


# ================================================================== [D] Corollary 10
def lifted(p, sets, tau2):
    n = len(sets)
    q = p // 3
    m = q - 2
    M = build_M(p, sets)
    k = n + 1 + m
    Mt = [[F(0)] * k for _ in range(k)]
    for i in range(n + 1):
        for j in range(n + 1):
            Mt[i][j] = M[i][j]
    for j in range(n + 1, k):
        Mt[j][j] = tau2
    return M, Mt


def d_explicit(p, sets, tau2):
    """d~ from the note's explicit formulas (Cor 1 for V, Cor 10 for the o_j). Nodes 0..k."""
    n = len(sets)
    q = p // 3
    m = q - 2
    g = n + 1
    d = {}
    for i in range(1, n + 1):
        d[(0, i)] = F(4 + len(sets[i - 1]))
        for j in range(i + 1, n + 1):
            d[(i, j)] = F(8 + len(sets[i - 1] ^ sets[j - 1]))
        d[(i, g)] = F(2 * p + 15, 4)
    d[(0, g)] = F(2 * p - 1, 4)
    os_ = list(range(n + 2, n + 2 + m))
    for o in os_:
        d[(0, o)] = tau2
        for u in range(1, n + 2):
            d[(u, o)] = d[(0, u)] + tau2
    for a, b in itertools.combinations(os_, 2):
        d[(a, b)] = 2 * tau2
    return d


def d_from_M(Mt):
    k = len(Mt)
    d = {}
    for i in range(1, k + 1):
        d[(0, i)] = Mt[i - 1][i - 1]
        for j in range(i + 1, k + 1):
            d[(i, j)] = Mt[i - 1][i - 1] + Mt[j - 1][j - 1] - 2 * Mt[i - 1][j - 1]
    return d


def check_cor10(instances):
    nfail0 = len(FAIL)
    sizes18 = set()
    yes = 0
    maxviol_info = []
    brute = 0
    for p, sets in instances:
        n = len(sets)
        q = p // 3
        m = q - 2
        tau2 = F(1, 8 * q)
        N = 8 * n + 2 * p + 1
        eps = F(1, N)
        covers = exact_covers(p, sets)
        yes += bool(covers)
        print(f"  [D] q={q} n={n} t={time.time() - T0:.1f}", file=sys.stderr, flush=True)
        M, Mt = lifted(p, sets, tau2)
        k = len(Mt)
        g = n + 1
        U = {g} | set(range(n + 2, n + 2 + m))
        nodes = list(range(0, k + 1))
        # (a)
        check(is_pd(Mt), "10(a) M~ PD")
        dt = d_from_M(Mt)
        check(dt == d_explicit(p, sets, tau2), "10 explicit d~ formulas")
        delta = [Mt[i][i] for i in range(k)]
        Mi = inv(Mt)
        w0 = matvec(Mi, delta)
        st = sum(a * b for a, b in zip(delta, w0))
        c = [a / 2 for a in w0]
        viol_z = enum_ellipsoid(Mt, c, st / 4)
        hyp = set()
        for z in viol_z:
            gval = qform(Mt, z) - sum(delta[i] * z[i] for i in range(k))
            check(gval < 0, "10(a) enumeration")
            hyp.add(tuple([1 - sum(z)] + list(z)))
        pred = set()
        rng = range(-8, 10)
        for C in covers:
            for w in itertools.product(rng, repeat=m):
                if sum(a * (a - 1) for a in w) < 4 * q:
                    b = [2 - q - sum(w)] + [1 if i in C else 0 for i in range(n)] + [-1] + list(w)
                    pred.add(tuple(b))
        check(hyp == pred, "10(a) hypermetric violators of d~")
        check(all(sum(abs(a) for a in b) >= 2 * q - 1 for b in hyp), "10(a) gonality")
        # (b)
        xv, yv = bq_point(Mt, eps)
        X = moment(xv, yv, k)
        check(is_pd(X), "10(b) X~ PD")
        X4 = [row[:] for row in X]
        X4[0][0] -= F(1, 4)
        check(is_pd(X4), "10(b) X~ - e0e0/4 PD")
        check(eps * st < F(3, 4), "10(b) eps s~ < 3/4")
        ent = [X[i][j] for i in range(k + 1) for j in range(k + 1)]
        check(all(0 <= e <= 1 and (8 * q * N * e).denominator == 1 for e in ent), "10(b) 8qN integral")
        z = cut_image(xv, yv)
        epsd = {e: eps * val for e, val in dt.items()}
        check(z == epsd, "10(b) cut image = eps d~")
        check(all(0 < val < 1 for val in z.values()), "10(b) (0,1)")
        check(metric_ok(z, nodes), "10(b) metric")
        check(is_pd(Zmat(z, nodes)), "10(b) elliptope interior")
        rp = violated_rpsd(z, nodes)
        rpset = {b for b, _ in rp}
        hyp_pm = hyp | {tuple(-a for a in b) for b in hyp}
        check(rpset == hyp_pm, "10(b) violated rpsd = +-hypermetric violators")
        check(all(abs(sum(b)) == 1 for b in rpset), "10(b) sigma = +-1")
        check(all(sum(abs(a) for a in b) >= 2 * q - 1 for b in rpset), "10(b) gonality >= 2q-1")
        # (c)
        oc = [(b, v) for b, v in rp if all(a in (-1, 0, 1) for a in b)]
        check(bool(oc) == bool(covers), "10(c) odd clique iff cover")
        for C in covers:
            bstar = tuple([0] + [1 if i in C else 0 for i in range(n)] + [-1] + [-1] * m)
            vb = dict(rp).get(bstar)
            check(vb == F(q + 2, 4 * q * N), "10(c) b* violation (q+2)/(4qN)")
        if covers:
            mx_oc = max(v for _, v in oc)
            mx_all = max(v for _, v in rp)
            maxviol_info.append((q, mx_oc * 4 * q * N, mx_all * 2 * N))
            check(mx_oc == F(q + 3, 4 * q * N), "max odd clique violation (q+3)/(4qN) [reviewer prediction]")
            check(mx_all == F(1, 2 * N), "max rpsd violation 1/(2N) [reviewer prediction]")
            # pure violators: b* and the m vectors with root -1
            predpure = set()
            for C in covers:
                base = [1 if i in C else 0 for i in range(n)] + [-1]
                predpure.add(tuple([0] + base + [-1] * m))
                for j in range(m):
                    w = [-1] * m
                    w[j] = 0
                    predpure.add(tuple([-1] + base + w))
            check({b for b, _ in oc if sum(b) == 1} == predpure, "pure violators [reviewer prediction]")
        # brute force over {0,+-1}^V for small V
        if k + 1 <= 9:
            brute += 1
            bf = set()
            for b in itertools.product((-1, 0, 1), repeat=k + 1):
                sig = sum(b)
                if sig % 2 and Qb(b, z, nodes) > F(sig * sig - 1, 4):
                    bf.add(b)
            check(bf == {b for b, _ in oc}, "10(c) brute force odd clique")
        # (d)
        dpp = switch_cut(z, U)
        check(all(0 < val < 1 and (8 * q * N * val).denominator == 1 for val in dpp.values()), "10(d) (0,1), 8qN")
        check(metric_ok(dpp, nodes), "10(d) metric")
        check(is_pd(Zmat(dpp, nodes)), "10(d) elliptope interior")
        rp2 = violated_rpsd(dpp, nodes)
        check(all(sum(abs(a) for a in b) >= 2 * q - 1 for b, _ in rp2), "10(d) gonality")
        sw = [(-1 if u in U else 1) for u in nodes]
        check({b for b, _ in rp2} == {tuple(s_ * a for s_, a in zip(sw, b)) for b in rpset}, "10(d) Sigma b")
        bm = {frozenset(i for i, a in enumerate(b) if a) for b, _ in rp2
              if all(a in (0, 1) for a in b) or all(a in (0, -1) for a in b)}
        predS = {frozenset({i + 1 for i in C} | U) for C in covers}
        check(bm == predS, "10(d) violated (18) via enumeration")
        for b, v in rp2:
            if all(a in (0, 1) for a in b):
                check(v == F(q + 2, 4 * q * N), "10(d) violation")
        # direct brute force over all odd subsets (independent of enumeration)
        if k + 1 <= 16:
            bms = set()
            for r in range(3, k + 2, 2):
                for S in itertools.combinations(nodes, r):
                    tot = sum(zget(dpp, a, b) for a, b in itertools.combinations(S, 2))
                    if tot > F(r * r - 1, 4):
                        bms.add(frozenset(S))
                        check(tot - F(r * r - 1, 4) == F(q + 2, 4 * q * N), "10(d) brute violation")
            check(bms == predS, "10(d) brute force (18)")
        for S in bm:
            sizes18.add(len(S))
            check(len(S) == 2 * q - 1, "|S| = 2q-1")
    print(f"[D] Corollary 10: {len(instances)} X3C instances ({yes} with a cover; q in "
          f"{sorted({p // 3 for p, _ in instances})}): M~ PD, explicit d~ formulas = d(M~); complete "
          f"hypermetric violators of d~ = predicted (1_C,-1,w), sum w(w-1) < 4q; X~ PD, X~-e0e0/4 PD, "
          f"8qN-integral, eps s~ < 3/4; eps d~ in (0,1), metric, elliptope; all violated rounded psd "
          f"(complete, cut space) = +-hypermetric violators, sigma = +-1, gonality >= 2q-1; odd clique "
          f"iff cover, b* violated by (q+2)/(4qN); brute force over {{0,+-1}}^V on {brute} instances; "
          f"d'' in (0,1), metric, elliptope, 8qN-integral; violated (18) = {{C u U}} (sizes "
          f"{sorted(sizes18)}), by enumeration and by direct subset brute force: "
          f"{len(FAIL) - nfail0} failures")
    print(f"    maximum violations at eps*d~ (instances with a cover): odd clique / pure hypermetric = "
          f"(q+3)/(4qN), all rounded psd = 1/(2N), b* = (q+2)/(4qN) is not the maximum; "
          f"samples (q, 4qN*max_oc, 2N*max_rpsd): {maxviol_info[:6]}")


def check_cor10_control(instances):
    nfail0 = len(FAIL)
    cnt = 0
    for p, sets in instances:
        n = len(sets)
        q = p // 3
        print(f"  [E] q={q} n={n} t={time.time() - T0:.1f}", file=sys.stderr, flush=True)
        tau2 = F(1, 4)
        N = 8 * n + 2 * p + 1
        eps = F(1, N)
        covers = exact_covers(p, sets)
        M, Mt = lifted(p, sets, tau2)
        k = len(Mt)
        xv, yv = bq_point(Mt, eps)
        z = cut_image(xv, yv)
        nodes = list(range(0, k + 1))
        rp = violated_rpsd(z, nodes)
        check(bool(rp) == bool(covers), "control: rpsd violated iff cover")
        oc = [b for b, _ in rp if all(a in (-1, 0, 1) for a in b)]
        if q >= 4:
            check(not oc, "control tau2=1/4: no odd clique violated for q >= 4")
        else:
            check(bool(oc) == bool(covers), "control q=3: odd clique still violated")
        cnt += 1
    print(f"[E] Control tau^2 = 1/4: {cnt} X3C instances with a planted cover (q in {{3,4,5}}): rounded psd "
          f"violated; no odd clique violated for q >= 4; for q = 3 an odd clique is still violated "
          f"(consistent with the remark's restriction to q >= 4): {len(FAIL) - nfail0} failures")


# ================================================================== [F] facets
def bqp_facet(k, slack_fn):
    rows = []
    for xs in itertools.product((0, 1), repeat=k):
        xv = {i + 1: F(xs[i]) for i in range(k)}
        yv = {(i + 1, j + 1): F(xs[i] * xs[j]) for i in range(k) for j in range(i + 1, k)}
        sl = slack_fn(xv, yv)
        if sl < 0:
            return "invalid"
        if sl == 0:
            rows.append([xv[i] for i in range(1, k + 1)] + [yv[e] for e in sorted(yv)] + [F(1)])
    return rank(rows) == k + k * (k - 1) // 2


def cut_facet(nn, b):
    """Rounded psd b on nodes 0..nn-1: facet of CUT_nn?"""
    sig = sum(b)
    rhs = F(sig * sig - 1, 4)
    edges = list(itertools.combinations(range(nn), 2))
    rows = []
    for bits in itertools.product((0, 1), repeat=nn - 1):
        side = (0,) + bits
        zz = {e: F(int(side[e[0]] != side[e[1]])) for e in edges}
        val = sum(b[u] * b[v] * zz[(u, v)] for (u, v) in edges)
        if val > rhs:
            return "invalid"
        if val == rhs:
            rows.append([zz[e] for e in edges] + [F(1)])
    return rank(rows) == len(edges)


def check_facets(small_instances):
    res = []
    for q in (3, 4, 5):
        S = list(range(1, q + 2))
        res.append(("(10) |S|=%d s=1 in BQP_%d" % (q + 1, q + 1),
                    bqp_facet(q + 1, lambda xv, yv, S=S: eq10_slack(xv, yv, S, 1))))
    for q in (3, 4):
        S = list(range(1, q + 2))
        res.append(("(10) |S|=%d s=1 in BQP_%d" % (q + 1, q + 2),
                    bqp_facet(q + 2, lambda xv, yv, S=S: eq10_slack(xv, yv, S, 1))))
    for size, nn in ((5, 5), (5, 6), (5, 7), (7, 7), (7, 8), (9, 9)):
        b = [1] * size + [0] * (nn - size)
        res.append(("(18) |S|=%d in CUT_%d" % (size, nn), cut_facet(nn, b)))
    # b* on actual small Corollary 10 instances (q = 3, |V~| <= 9)
    for p, sets in small_instances:
        n = len(sets)
        q = p // 3
        covers = exact_covers(p, sets)
        for C in covers[:1]:
            bstar = [0] + [1 if i in C else 0 for i in range(n)] + [-1] + [-1] * (q - 2)
            res.append(("b* (n=%d, q=%d) in CUT_%d" % (n, q, len(bstar)), cut_facet(len(bstar), bstar)))
    ok = all(r is True for _, r in res)
    check(ok, "facets")
    print("[F] facets by exact affine rank of tight 0/1 points: " + "; ".join(f"{a}: {b}" for a, b in res))


# ================================================================== main
def main():
    secs = set(sys.argv[1:]) or {"A", "B", "C", "D", "E", "F"}
    if "A" in secs:
        check_lemma6()
        check_lemma6_symbolic()
    insts9 = []
    for q, nmax, cnt in ((3, 7, 24), (4, 7, 16)):
        for t in range(cnt):
            n = random.randint(q + 1, nmax)
            plant = t % 3 != 2
            two = (t % 7 == 0) and n >= 2 * q
            insts9.append(x3c_instance(q, n, plant, two))
    if "B" in secs:
        check_cor9(insts9)
    if "C" in secs:
        check_clique_cut_image()
    insts10 = []
    for q, nmax, cnt in ((3, 7, 20), (4, 8, 14), (5, 7, 3)):
        for t in range(cnt):
            n = random.randint(q + 1, nmax)
            plant = t % 3 != 2
            two = (t % 5 == 0) and n >= 2 * q
            insts10.append(x3c_instance(q, n, plant, two))
    if "D" in secs:
        check_cor10(insts10)
    ctrl = [x3c_instance(q, q + 2, True) for q in (3, 4, 4, 5, 5) for _ in range(2)]
    if "E" in secs:
        check_cor10_control(ctrl)
    small = [x3c_instance(3, n, True) for n in (4, 5)]
    if "F" in secs:
        check_facets(small)
    print(f"sections {sorted(secs)}; elapsed {time.time() - T0:.1f} s")
    if FAIL:
        print(f"{len(FAIL)} FAILURES")
        sys.exit(1)
    print("REVIEWER R3 CHECKS PASSED")


if __name__ == "__main__":
    main()
