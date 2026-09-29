"""Exact checks for split-separation-np-complete.md (standard library only).

All arithmetic is exact (fractions.Fraction). For positive definite X the set of
violated splits is computed completely, not by a box search: every u = 2v + e0 with
u^T X u < X00 is enumerated by Fincke-Pohst over an exact LDL^T factorization.

  1. identities   q(v) = <v(v+e0)^T, X> = ((2v+e0)^T X (2v+e0) - X00)/4 = q(-v-e0)
  2. reduction    Theorem 1 on subset-sum, multi-row 0/1-equation and exact-cover
                  instances: X is positive definite with X00 = 1; the violated splits
                  are exactly (0,-x,1), (-1,x,-1) for the 0/1 solutions x; the minimum
                  of q is -1/(4(n+1+h^2)); after the sign flip the violated 0/1 splits
                  are exactly (0,x,1); Corollary 3: gap 2/(n+9) with M = 3, gamma^2 = n+8,
                  h^2 = 1, and 2/(8n+9) with M = 1, h^2 = 1/8
  3. threshold    Lemma 3 with L = Z, t = 1/3 at 8h^2 = |t|^2 and 8h^2 < |t|^2
  4. non-PSD      Lemma 4: elimination gives z with z^T X z < 0 and v = N z violates
  5. rank one     Theorem 4: q(v) = m(m+D)/D^2 for X = l(x), maximum violation
                  floor(D^2/4)/D^2, violated iff x is not integral
  6. location     Remark 1 and Corollary 5 (hard points satisfy de Meijer et al.'s ternary
                  constraints; for X3C including the pair inequalities (2.3) and (4.4)) and
                  the split = rounded-psd identity at points with X_ii = X_0i (Section 6)
"""
import random
from fractions import Fraction as F
from itertools import combinations, product
from math import ceil, floor, gcd, isqrt

random.seed(20260928)


def q(X, v):
    N = len(X)
    return sum(v[i] * X[i][j] * (v[j] + (j == 0)) for i in range(N) for j in range(N))


def quad(X, u):
    return sum(u[i] * X[i][j] * u[j] for i in range(len(X)) for j in range(len(X)))


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


def violators(X):
    """All v in Z^N with q(v) < 0 for positive definite X (complete list)."""
    d, mu = ldl_rev(X)
    N, u, out = len(X), [0] * len(X), []

    def rec(i, rem):
        if i == N:
            out.append(tuple((u[k] - (k == 0)) // 2 for k in range(N)))
            return
        c = -sum((mu[i][j] * u[j] for j in range(i)), F(0))
        r = isqrt(floor(rem / d[i])) + 1
        for ui in range(floor(c) - r, ceil(c) + r + 1):
            if (ui - (i == 0)) % 2:  # u0 odd, all other u_i even
                continue
            t = d[i] * (ui - c) ** 2
            if t < rem:
                u[i] = ui
                rec(i + 1, rem - t)
        u[i] = 0

    rec(0, X[0][0])
    assert all(q(X, v) < 0 for v in out)
    return out


# ---------------------------------------------------------------- 1. identities
def check_identities(trials=300):
    for _ in range(trials):
        N = random.randint(2, 5)
        X = [[F(0)] * N for _ in range(N)]
        for i in range(N):
            for j in range(i, N):
                X[i][j] = X[j][i] = F(random.randint(-9, 9), random.randint(1, 5))
        X[0][0] = F(1)
        v = [random.randint(-4, 4) for _ in range(N)]
        u = [2 * v[i] + (i == 0) for i in range(N)]
        assert q(X, v) == (quad(X, u) - 1) / 4 == q(X, [-v[i] - (i == 0) for i in range(N)])
    print(f"[identities] {trials} random rational symmetric X: parity and symmetry identities hold")


# ---------------------------------------------------------------- 2. reduction
def reduction(A, b, h2=None, M=1, g2=None):
    """X = Gram(b0, b_1..b_n, g)/|b0|^2 with b0 = (0,0,-2gamma,2h), b_i = (M A_i, 2e_i, 0, 0),
    g = (M b, 1, gamma, 0); by default M = 1 and gamma^2 = h^2 = n+1. Coordinates gamma and h
    enter only through gamma^2 and h^2, so vectors are stored as coefficient lists with a
    weighted inner product."""
    p, n = len(A), len(A[0])
    g2 = F(n + 1) if g2 is None else F(g2)
    h2 = g2 if h2 is None else F(h2)
    w = [1] * (p + n) + [g2, h2]
    b0 = [0] * (p + n) + [-2, 2]
    bi = [[M * A[r][i] for r in range(p)] + [2 * (k == i) for k in range(n)] + [0, 0] for i in range(n)]
    g = [M * t for t in b] + [1] * n + [1, 0]
    vecs = [b0] + bi + [g]
    G = [[sum(wk * x * y for wk, x, y in zip(w, a, c)) for c in vecs] for a in vecs]
    if M == 1 and g2 == h2 == n + 1:  # the explicit integer matrix of Theorem 1
        col = lambda i: [A[r][i] for r in range(p)]
        dot = lambda x, y: sum(s * t for s, t in zip(x, y))
        E = [[0] * (n + 2) for _ in range(n + 2)]
        E[0][0], E[0][n + 1], E[n + 1][0] = 8 * (n + 1), -2 * (n + 1), -2 * (n + 1)
        for i in range(n):
            for j in range(n):
                E[1 + i][1 + j] = dot(col(i), col(j)) + 4 * (i == j)
            E[1 + i][n + 1] = E[n + 1][1 + i] = dot(col(i), b) + 2
        E[n + 1][n + 1] = dot(b, b) + 2 * n + 1
        assert G == E
    return [[x / G[0][0] for x in row] for row in G], G


def solutions(A, b):
    n = len(A[0])
    return [x for x in product((0, 1), repeat=n)
            if all(sum(A[r][i] * x[i] for i in range(n)) == b[r] for r in range(len(A)))]


def check_instance(A, b, h2=None, M=1, g2=None):
    n = len(A[0])
    X, G = reduction(A, b, h2, M, g2)
    assert X[0][0] == 1 and ldl_rev(X) is not None  # rational, X00 = 1, positive definite
    sols = solutions(A, b)
    pred = {(0,) + tuple(-t for t in x) + (1,) for x in sols} | {(-1,) + x + (-1,) for x in sols}
    viol = set(violators(X))
    ok = viol == pred
    if sols:  # minimum (n - gamma^2)/(4(gamma^2 + h^2))
        gg = F(n + 1) if g2 is None else F(g2)
        hh = gg if h2 is None else F(h2)
        ok &= min(q(X, v) for v in viol) == (n - gg) / (4 * (gg + hh))
    Xf = flip(X)  # Corollary 2: D X D, D = diag(1,-1,...,-1,1)
    vf = set(violators(Xf))
    D = [1] + [-1] * n + [1]
    ok &= vf == {tuple(D[i] * v[i] for i in range(n + 2)) for v in pred}
    ok &= {v for v in vf if set(v) <= {0, 1}} == {(0,) + x + (1,) for x in sols}
    return ok, bool(sols), viol, G


def flip(X):
    N = len(X)
    D = [1] + [-1] * (N - 2) + [1]
    return [[D[i] * D[j] * X[i][j] for j in range(N)] for i in range(N)]


def x3c_instance(qq, pad=False):
    """Random exact-cover instance (A = 3q x n incidence matrix, b = 1); half get a planted cover.
    With pad=True, sets are repeated until n >= 3q (this does not change the answer)."""
    U = list(range(3 * qq))
    sets = [tuple(random.sample(U, 3)) for _ in range(random.randint(1, 4))]
    if random.random() < 0.5:
        random.shuffle(U)
        sets += [tuple(U[3 * k:3 * k + 3]) for k in range(qq)]
        random.shuffle(sets)
    while pad and len(sets) < 3 * qq:
        sets.append(sets[0])
    return [[int(e in S) for S in sets] for e in range(3 * qq)], [1] * (3 * qq)


def subset_sum_instances():
    inst = []
    for n in (1, 2, 3):
        for a in product(range(1, 6), repeat=n):
            if list(a) == sorted(a):
                inst += [([list(a)], [s]) for s in range(sum(a) + 2)]
    for a in product(range(1, 4), repeat=4):
        if list(a) == sorted(a):
            inst += [([list(a)], [s]) for s in range(sum(a) + 2)]
    return inst


def run(label, inst, h2fun=None):
    bad = yes = 0
    for A, b in inst:
        ok, y, _, _ = check_instance(A, b, None if h2fun is None else h2fun(len(A[0])))
        bad += not ok
        yes += y
    print(f"[{label}] {len(inst)} instances ({yes} solvable): {bad} mismatches")
    return bad


def check_reduction():
    for s in (4, 8, 9, 10, 11, 13, 15, 16):  # the scout's instances
        _, y, viol, _ = check_instance([[3, 5, 7]], [s])
        X, _ = reduction([[3, 5, 7]], [s])
        mq = min((q(X, v) for v in viol), default=None)
        print(f"  a=(3,5,7) s={s:2d}: solvable={y!s:5} violators={sorted(viol)} min q={mq}")
    ss = subset_sum_instances()
    bad = run("subset sum, h^2 = n+1", ss)
    bad += run("subset sum, h^2 = (n+1)/8 (boundary 8h^2 = |t|^2)", ss, lambda n: F(n + 1, 8))
    bad += run("subset sum, h^2 = 1000(n+1) (near l(0))", ss, lambda n: 1000 * (n + 1))
    neg = sum(not check_instance(A, b, F(len(A[0]) + 1, 100))[0] for A, b in ss)
    print(f"[negative control: subset sum, h^2 = (n+1)/100, so 8h^2 < |t|^2] {neg} of {len(ss)} "
          f"instances mismatch (expected > 0)")
    bad += neg == 0
    multi = []
    for _ in range(300):
        p, n = random.randint(2, 3), random.randint(2, 4)
        A = [[random.randint(-2, 2) for _ in range(n)] for _ in range(p)]
        if random.random() < 0.5:
            x0 = [random.randint(0, 1) for _ in range(n)]
            b = [sum(A[r][i] * x0[i] for i in range(n)) for r in range(p)]
        else:
            b = [random.randint(-3, 3) for _ in range(p)]
        multi.append((A, b))
    bad += run("0/1 equations, 2-3 rows, entries in -2..2", multi)
    # exact cover by 3-sets: A = incidence matrix (3q x m), b = 1
    nbad = nyes = maxg = 0
    trials = 200
    for _ in range(trials):
        qq = random.choice([2, 3])
        A, b = x3c_instance(qq)
        ok, y, viol, G = check_instance(A, b)
        ok &= all(sum(t != 0 for t in v[1:]) == qq + 1 for v in viol)  # |supp w| = q+1
        nbad += not ok
        nyes += y
        maxg = max(maxg, max(abs(x) for row in G for x in row))
    print(f"[exact cover by 3-sets] {trials} instances ({nyes} with a cover): {nbad} mismatches; "
          f"every violated w has support q+1; largest |Gram entry| = {maxg}")
    # Corollary 3: M = 3, gamma^2 = n+8, h^2 = 1 (refined threshold 8h^2 >= gamma^2 - n) gives the
    # gap 2/(n+9); M = 1, gamma^2 = n+1, h^2 = 1/8 gives 2/(8n+9)
    x3c = [x3c_instance(random.choice([2, 3])) for _ in range(60)]
    gbad = 0
    for label, inst, M, g2f, h2f in [
            ("subset sum", ss, 3, lambda n: n + 8, lambda n: 1),
            ("0/1 equations", multi, 3, lambda n: n + 8, lambda n: 1),
            ("X3C", x3c, 3, lambda n: n + 8, lambda n: 1),
            ("subset sum", ss, 1, lambda n: n + 1, lambda n: F(1, 8)),
            ("X3C", x3c, 1, lambda n: n + 1, lambda n: F(1, 8))]:
        b1 = 0
        for A, b in inst:
            n = len(A[0])
            ok, y, viol, _ = check_instance(A, b, h2f(n), M, g2f(n))
            X, _ = reduction(A, b, h2f(n), M, g2f(n))
            gap = F(2, n + 9) if M == 3 else F(2, 8 * n + 9)
            ok &= (min(q(X, v) for v in viol) == -gap) if y else not viol
            b1 += not ok
        print(f"[Corollary 3: M={M}, gamma^2=n+{8 if M == 3 else 1}, h^2={h2f(1)}] {label}: {len(inst)} "
              f"instances: violated set as in Theorem 1, gap {'2/(n+9)' if M == 3 else '2/(8n+9)'}: {b1} failures")
        gbad += b1
    # sharpness of 8h^2 >= gamma^2 - n: three copies of a 3-element universe (q = 1), M = 1
    A, b = [[1, 1, 1]] * 3, [1, 1, 1]
    sharp_ok = check_instance(A, b, F(1, 8))[0] and not check_instance(A, b, F(1, 9))[0]
    print(f"[refined threshold] A = three copies of U, M=1: h^2 = 1/8 exact, h^2 = 1/9 spurious violators: "
          f"{'as expected' if sharp_ok else 'UNEXPECTED'}")
    gbad += not sharp_ok
    # entries in [-1, 1] for padded X3C with n >= 14q (M = 3, h^2 = 1), and one enumeration at q = 1
    pbad = 0
    for qq in (1, 2, 3):
        A, b = x3c_instance(qq)
        while len(A[0]) < 14 * qq:
            A = [row + [row[0]] for row in A]
        X, _ = reduction(A, b, 1, 3, len(A[0]) + 8)
        pbad += any(abs(t) > 1 for row in X for t in row)
    A, b = x3c_instance(1)
    A = [row + [row[0]] * (14 - len(row)) for row in A]
    pbad += not check_instance(A, b, 1, 3, 22)[0]
    print(f"[Corollary 3 padding] X3C with n = 14q, q = 1,2,3: all |X_ij| <= 1; q = 1 violated set checked: "
          f"{pbad} failures")
    gbad += pbad
    return bad + nbad + gbad


# ---------------------------------------------------------------- 3. threshold
def lemma3_matrix(C, t, h2):
    """X = Gram(b0, b_1..b_m)/|b0|^2 with b0 = (2t, 2h), b_j = (c_j, 0)."""
    vecs = [[2 * x for x in t] + [2]] + [list(c) + [0] for c in C]
    w = [1] * len(t) + [h2]
    G = [[sum(wk * x * y for wk, x, y in zip(w, a, c)) for c in vecs] for a in vecs]
    return [[x / G[0][0] for x in row] for row in G]


def check_threshold():
    t = [F(1, 3)]
    closer = any(abs(t[0] - l) < abs(t[0]) for l in range(-3, 4))  # L = Z: nearest points are 0 and 1
    v_edge = violators(lemma3_matrix([[1]], t, F(1, 72)))  # 8h^2 = |t|^2
    v_below = violators(lemma3_matrix([[1]], t, F(1, 81)))  # 8h^2 < |t|^2
    print(f"[threshold] L=Z, t=1/3: CLOSER={closer}; 8h^2=|t|^2: violators={v_edge}; "
          f"h^2=|t|^2/9: violators={v_below}")
    return int(closer or v_edge != [] or v_below == [] or any(v[0] not in (1, -2) for v in v_below))


# ---------------------------------------------------------------- 4. non-PSD
def negative_direction(S):
    """Rational z with z^T S z < 0, or None if S is PSD (symmetric elimination, diagonal pivots)."""
    n = len(S)
    for i in range(n):
        if S[i][i] < 0:
            return [F(k == i) for k in range(n)]
    for i in range(n):
        for j in range(n):
            if S[i][i] == 0 and S[i][j] != 0:
                z = [F(0)] * n
                z[i], z[j] = -(S[j][j] + 1) / (2 * S[i][j]), F(1)  # z^T S z = -1
                return z
    p = next((i for i in range(n) if S[i][i] > 0), None)
    if p is None:
        return None  # S = 0
    R = [k for k in range(n) if k != p]
    zr = negative_direction([[S[a][c] - S[a][p] * S[p][c] / S[p][p] for c in R] for a in R])
    if zr is None:
        return None
    z = [F(0)] * n
    for a, k in enumerate(R):
        z[k] = zr[a]
    z[p] = -sum(S[p][k] * z[k] for k in R) / S[p][p]
    return z


def det(M):
    M = [row[:] for row in M]
    n, s = len(M), F(1)
    for c in range(n):
        r = next((r for r in range(c, n) if M[r][c] != 0), None)
        if r is None:
            return F(0)
        if r != c:
            M[c], M[r], s = M[r], M[c], -s
        s *= M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return s


def check_non_psd(trials=400):
    found = psd = bad = 0
    for k in range(trials):
        N = random.randint(2, 5)
        if k % 2:  # random symmetric
            X = [[F(0)] * N for _ in range(N)]
            for i in range(N):
                for j in range(i, N):
                    X[i][j] = X[j][i] = F(random.randint(-6, 6), random.randint(1, 4))
        else:  # singular or regular Gram matrix, often PSD
            V = [[random.randint(-2, 2) for _ in range(N)] for _ in range(random.randint(1, N))]
            X = [[F(sum(r[i] * r[j] for r in V)) for j in range(N)] for i in range(N)]
        if X[0][0] <= 0:
            continue
        X = [[x / X[0][0] for x in row] for row in X]
        z = negative_direction(X)
        if z is None:
            psd += 1
            minors = [det([[X[i][j] for j in T] for i in T])
                      for r in range(1, N + 1) for T in combinations(range(N), r)]
            bad += any(m < 0 for m in minors)
            continue
        found += 1
        L = 1
        for x in z:
            L = L * x.denominator // gcd(L, x.denominator)
        z = [int(x * L) for x in z]
        alpha, beta = quad(X, z), sum(z[i] * X[i][0] for i in range(N))
        Nf = floor(abs(beta) / abs(alpha)) + 1
        bad += not (alpha < 0 and q(X, [Nf * x for x in z]) < 0)
    print(f"[non-PSD] {found} non-PSD X: z^T X z < 0 and v = N z violates; {psd} reported PSD "
          f"(all principal minors checked); {bad} failures")
    return bad


# ---------------------------------------------------------------- 5. rank one
def check_rank_one(trials=400):
    bad = 0
    for _ in range(trials):
        n = random.randint(1, 3)
        x = [F(random.randint(-12, 12), random.randint(1, 6 if n < 3 else 4)) for _ in range(n)]
        D = 1
        for xi in x:
            D = D * xi.denominator // gcd(D, xi.denominator)
        c = [F(1)] + x
        X = [[ci * cj for cj in c] for ci in c]  # X = l(x)
        p = [int(D * ci) for ci in c]
        k = random.randint(1, 4)  # the gcd form is invariant under scaling p
        pk = [k * t for t in p]
        gk = 0
        for t in pk:
            gk = gcd(gk, abs(t))
        best = None
        for w in product(range(D), repeat=n):  # all residues of m = p^T v mod D occur here
            cw = sum(p[i + 1] * w[i] for i in range(n))
            for v0 in {floor((-F(D, 2) - cw) / D), ceil((-F(D, 2) - cw) / D)}:
                v = (v0,) + w
                m = sum(p[i] * v[i] for i in range(n + 1))
                val = q(X, v)
                bad += val != F(m * (m + D), D * D)
                best = val if best is None else min(best, val)
        expect = -F((D * D) // 4, D * D)
        integral = all(xi.denominator == 1 for xi in x)
        bad += best != expect or (best < 0) == integral or (abs(pk[0]) >= 2 * gk) == integral
    print(f"[rank one] {trials} random X = l(x): q(v) = m(m+D)/D^2, maximum violation "
          f"floor(D^2/4)/D^2, violated iff x not integral iff |p0| >= 2 gcd(p); {bad} failures")
    return bad


# ---------------------------------------------------------------- 6. location, binary analogue
def ternary_failures(X, odd_sets=True):
    """Constraint families of de Meijer et al. that X violates (X is PSD by construction):
    (4.1) |x| <= diag(Y) <= 1, (2.1)-(2.2) triangle, (2.3) pair |Y_ij| <= Y_ii, (4.4) odd-set
    sum_{i<j in S} v_i v_j Y_ij >= -floor(|S|/2), (4.5)-(4.8) RLT for bounds -1 <= x <= 1."""
    m = len(X) - 1
    x, Y = X[0][1:], [row[1:] for row in X[1:]]
    fail = set()
    if not all(abs(x[i]) <= Y[i][i] <= 1 for i in range(m)):
        fail.add("4.1")
    if not all(si * sj * Y[i][j] + si * sk * Y[i][k] + sj * sk * Y[j][k] >= -1
               for i, j, k in combinations(range(m), 3) for si, sj, sk in product((1, -1), repeat=3)):
        fail.add("2.1-2.2")
    if not all(abs(Y[i][j]) <= Y[i][i] for i in range(m) for j in range(m) if i != j):
        fail.add("2.3")
    if not all(si * sj * Y[i][j] + si * x[i] + sj * x[j] >= -1
               for i, j in combinations(range(m), 2) for si, sj in product((1, -1), repeat=2)):
        fail.add("4.5-4.8")
    if odd_sets and not all(
            sum(v[a] * v[c] * Y[S[a]][S[c]] for a, c in combinations(range(k), 2)) >= -(k // 2)
            for k in range(3, m + 1, 2) for S in combinations(range(m), k)
            for v in ((1,) + w for w in product((1, -1), repeat=k - 1))):
        fail.add("4.4")
    return fail


def g_hat(G):
    return max(abs(G[i][j]) for i in range(len(G)) for j in range(len(G)) if i or j)


def check_location():
    """Remark 1: subset sum with 4h^2 = 3*Ghat and b != 0 satisfies (4.1), (2.1)-(2.2), (4.5)-(4.8);
    the pair inequalities (2.3) often fail there."""
    bad = cnt = pair = 0
    for A, b in subset_sum_instances():
        if b == [0]:
            continue
        h2 = F(3 * g_hat(reduction(A, b)[1]), 4)
        fail = ternary_failures(reduction(A, b, h2)[0], odd_sets=False)
        bad += (not check_instance(A, b, h2)[0]) or bool(fail - {"2.3"})
        pair += "2.3" in fail
        cnt += 1
    X, _ = reduction([[1, 6]], [6])
    print(f"[Remark 1] {cnt} subset-sum instances with 4h^2 = 3*Ghat: {bad} failures of (4.1), (2.1)-(2.2), "
          f"(4.5)-(4.8) or of the violated set; pair inequalities (2.3) fail on {pair} of them "
          f"(a=(1,6): X12={X[1][2]} > X11={X[1][1]})")
    return bad


def check_x3c_ternary(trials=100):
    """Corollary 5: X3C with 4h^2 = max(3, n+1)*Ghat; X and its flip D X D satisfy (4.1), (2.1)-(2.3),
    (4.4), (4.5)-(4.8), and the violated splits are those of Theorem 1. (2.3) also holds at h^2 = n+1."""
    # liveness: unit diagonal and off-diagonal -6/25 on five variables (positive definite) passes
    # (2.1)-(2.3), (4.1) and RLT but fails (4.4) for |S| = 5
    probe = [[F(int(i == j)) if 0 in (i, j) or i == j else F(-6, 25) for j in range(6)] for i in range(6)]
    bad = int(ternary_failures(probe) != {"4.4"} or ldl_rev(probe) is None)
    yes = 0
    small = 0
    cases = [(1, ([[1], [1], [1]], [1, 1, 1]))]  # (q, n) = (1, 1), where Ghat = 7 > 3q + 2n + 1
    cases += [(qq, x3c_instance(qq)) for qq in (random.choice([1, 2, 2, 3]) for _ in range(trials - 1))]
    for qq, (A, b) in cases:
        n = len(A[0])
        small += n == 1
        X1, G = reduction(A, b)
        ok = g_hat(G) == max(7, 3 * qq + 2 * n + 1)
        h2 = F(max(3, n + 1) * g_hat(G), 4)
        ok2, y, viol, _ = check_instance(A, b, h2)
        X = reduction(A, b, h2)[0]
        ok &= ok2 and not ternary_failures(X) and not ternary_failures(flip(X))
        ok &= "2.3" not in ternary_failures(X1, odd_sets=False)
        if qq >= 2:  # (4.3), (4.11)-(4.12) hold: no violated split has |supp w| <= 2
            ok &= all(sum(t != 0 for t in v[1:]) >= 3 for v in viol)
        bad += not ok
        yes += y
    print(f"[Corollary 5] {trials} X3C instances ({yes} with a cover; q in 1..3; {small} with n = 1, "
          f"including (q, n) = (1, 1)), "
          f"4h^2 = max(3,n+1)*Ghat, Ghat = max(7, 3q+2n+1): X and D X D satisfy (4.1), (2.1)-(2.3), (4.4), "
          f"(4.5)-(4.8); violated set as in Theorem 1; no violated split with |supp w| <= 2 for q >= 2: "
          f"{bad} failures")
    return bad


def check_binary_identity(trials=1000):
    """Section 6: if X_ii = X_0i, then q(v) = (sigma^2-1)/4 - sum_{i<j} b_i b_j d_ij with
    sigma = 2s+1, b = (sigma - sum w, w), d_0i = X_0i, d_ij = X_ii + X_jj - 2 X_ij."""
    bad = 0
    for _ in range(trials):
        N = random.randint(2, 6)
        X = [[F(0)] * N for _ in range(N)]
        for i in range(N):
            for j in range(i, N):
                X[i][j] = X[j][i] = F(random.randint(-9, 9), random.randint(1, 5))
        X[0][0] = F(1)
        for i in range(1, N):
            X[i][i] = X[0][i]
        v = [random.randint(-4, 4) for _ in range(N)]
        sigma = -2 * v[0] - 1  # s = -v0 - 1
        bb = [sigma - sum(v[1:])] + v[1:]
        dd = lambda i, j: X[0][j] if i == 0 else X[i][i] + X[j][j] - 2 * X[i][j]
        rhs = F(sigma * sigma - 1, 4) - sum(bb[i] * bb[j] * dd(i, j) for i, j in combinations(range(N), 2))
        bad += q(X, v) != rhs
    print(f"[binary analogue] {trials} random X with X_ii = X_0i: split = rounded psd inequality; {bad} failures")
    return bad


if __name__ == "__main__":
    check_identities()
    total = check_reduction() + check_threshold() + check_non_psd() + check_rank_one()
    total += check_location() + check_x3c_ternary() + check_binary_identity()
    print("ALL CHECKS PASSED" if total == 0 else f"FAILURES: {total}")
