"""Reviewer's independent checks for binary-separation/note.md (review r1).

Written from the note's statements only; it does not import the author's code.
  A. Lemma 0 and Lemma 1 symbolically (sympy).
  B. Theorem 1 by exhaustive box enumeration (box from exact ellipsoid bounds), including
     edge cases the author's script does not cover: empty and duplicate sets, eta^2 at the
     lower window endpoint max(p/8, (p-2)/4), eta^2 just below p/4.
  C. Size of eps = 1/(2 s), s = delta^T M^{-1} delta, on larger X3C instances (strong NP-hardness
     at the scaled points needs polynomially bounded numerators/denominators).
  D. The bound s <= 4n + p + 1/(4(p-1)) (projection of an explicit equidistant point), so that
     eps' = 1/(8n + 2p + 1) satisfies eps' s < 1/2; ratio s/(n+p) on random and degenerate
     instances (the note's Theta(1/(n+p)) violation claim).
  E. Corollary 3(c)-(e) at eps' (exact): X(eps') PD, X - e0e0^T/4 PD, eps'd in [0,1], elliptope;
     also eps d in [0,1] for instances whose triangle inequalities fail (q = 2 / small covers).
  F. Theorem 4 (gap-0) for n = 4, which the theorem allows but the author's script does not test,
     with a different basis of s-perp and an exact LDL test.
"""
import itertools
import math
import random
import sys
from fractions import Fraction as F

import numpy as np
import sympy as sp

rng = random.Random(31337)


# ---------------------------------------------------------------- exact helpers
def ldl_pd(A):
    """True iff the rational symmetric matrix A is positive definite (exact)."""
    A = [[F(x) for x in r] for r in A]
    n = len(A)
    for k in range(n):
        if A[k][k] <= 0:
            return False
        for i in range(k + 1, n):
            f = A[i][k] / A[k][k]
            for j in range(k + 1, n):
                A[i][j] -= f * A[k][j]
    return True


def psd_exact(A):
    """Exact PSD test with diagonal pivoting (handles singular matrices)."""
    A = [[F(x) for x in r] for r in A]
    while A:
        n = len(A)
        if any(A[i][i] < 0 for i in range(n)):
            return False
        if any(A[i][i] == 0 and any(A[i][j] != 0 for j in range(n)) for i in range(n)):
            return False
        piv = next((i for i in range(n) if A[i][i] > 0), None)
        if piv is None:
            return True
        rest = [i for i in range(n) if i != piv]
        A = [[A[i][j] - A[i][piv] * A[piv][j] / A[piv][piv] for j in rest] for i in rest]
    return True


def solve_exact(M, b):
    S = sp.Matrix(M)
    return list(S.LUsolve(sp.Matrix(b)))


def build(sets, p, eta2):
    n = len(sets)
    M = [[F(0)] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(n):
            M[i][j] = F(4 * (i == j) + len(set(sets[i]) & set(sets[j])))
        M[i][n] = M[n][i] = F(len(sets[i]), 2)
    M[n][n] = F(p, 4) + F(eta2)
    return M


def covers(sets, p):
    out = []
    for x in itertools.product((0, 1), repeat=len(sets)):
        c = [0] * p
        for i, xi in enumerate(x):
            if xi:
                for e in sets[i]:
                    c[e] += 1
        if all(t == 1 for t in c):
            out.append(x)
    return out


# ---------------------------------------------------------------- A
def check_symbolic():
    N = 3
    Ms = sp.Matrix(N, N, lambda i, j: sp.Symbol(f"m{min(i, j)}{max(i, j)}"))
    z = sp.symbols(f"z0:{N}")
    # Lemma 0: d0i = Mii, dij = Mii + Mjj - 2Mij, b = (1 - sum z, z)
    b = [1 - sum(z)] + list(z)
    d = {}
    for i in range(N):
        d[(0, i + 1)] = Ms[i, i]
        for j in range(i + 1, N):
            d[(i + 1, j + 1)] = Ms[i, i] + Ms[j, j] - 2 * Ms[i, j]
    Q = sum(b[u] * b[v] * d[(u, v)] for (u, v) in d)
    zv = sp.Matrix(z)
    g = (zv.T * Ms * zv)[0] - sum(Ms[i, i] * z[i] for i in range(N))
    ok0 = sp.expand(Q + g) == 0
    # Lemma 1 for a symbolic 2-set instance on p = 3: S1 = {0,1}, S2 = {1,2}
    x1, x2, k, e2 = sp.symbols("x1 x2 k eta2")
    sets, p = [(0, 1), (1, 2)], 3
    M = sp.Matrix([[6, 1, 1], [1, 6, 1], [1, 1, sp.Rational(3, 4) + e2]])
    zz = sp.Matrix([x1, x2, k])
    gl = (zz.T * M * zz)[0] - (6 * x1 + 6 * x2 + (sp.Rational(3, 4) + e2) * k)
    y = [x1, x1 + x2, x2]
    rhs = 4 * (x1 * (x1 - 1) + x2 * (x2 - 1)) + sum(t ** 2 + (k - 1) * t for t in y) + k * (k - 1) * (sp.Rational(p, 4) + e2)
    ok1 = sp.expand(gl - rhs) == 0
    print(f"[A] Lemma 0 symbolic (N=3): {ok0}; Lemma 1 symbolic (2-set instance): {ok1}")
    return ok0 and ok1


# ---------------------------------------------------------------- B
def violators_box(M):
    """All integer z with g_M(z) < 0, by enumerating a box that provably contains them."""
    N = len(M)
    Ms = sp.Matrix(M)
    delta = [M[i][i] for i in range(N)]
    w = Ms.LUsolve(sp.Matrix(delta)) / 2          # g = (z-w)^T M (z-w) - w^T M w
    R = (w.T * Ms * w)[0]
    Minv = Ms.inv()
    lo, hi = [], []
    for i in range(N):
        r = math.sqrt(float(R * Minv[i, i]))
        lo.append(math.floor(float(w[i]) - r) - 1)
        hi.append(math.ceil(float(w[i]) + r) + 1)
    L = 1
    for row in M:
        for a in row:
            L = L * a.denominator // math.gcd(L, a.denominator)
    G = np.array([[int(a * L) for a in row] for row in M], dtype=np.int64)
    dg = np.diag(G)
    grids = np.array(list(itertools.product(*[range(lo[i], hi[i] + 1) for i in range(N)])), dtype=np.int64)
    vals = np.einsum("ij,jk,ik->i", grids, G, grids) - grids @ dg   # = L * g_M(z), exact integers
    idx = np.nonzero(vals < 0)[0]
    return sorted(tuple(int(t) for t in grids[i]) for i in idx), {tuple(int(t) for t in grids[i]): F(int(vals[i]), L) for i in idx}, len(grids)


def random_instance(p, n):
    sets = []
    if rng.random() < 0.5:  # plant a cover (blocks of size 1..3)
        U = list(range(p))
        rng.shuffle(U)
        k = 0
        while k < p:
            s = rng.randint(1, 3)
            sets.append(tuple(sorted(U[k:k + s])))
            k += s
    while len(sets) < n:
        r = rng.random()
        if r < 0.1:
            sets.append(())                       # empty set
        elif r < 0.25 and sets:
            sets.append(rng.choice(sets))         # duplicate set
        else:
            sets.append(tuple(sorted(rng.sample(range(p), rng.randint(1, min(4, p))))))
    rng.shuffle(sets)
    return sets[:max(n, len(sets))]


def check_theorem1(T=150):
    bad = cnt = withcov = pts = 0
    for t in range(T):
        p = rng.randint(2, 6)
        n = rng.randint(1, 5)
        sets = random_instance(p, n)
        lo = max(F(p, 8), F(p - 2, 4))
        eta2 = rng.choice([lo, F(p - 1, 4), F(p, 4) - F(1, 64)])
        M = build(sets, p, eta2)
        assert ldl_pd(M)
        viol, vals, npts = violators_box(M)
        pts += npts
        cov = covers(sets, p)
        want = sorted(tuple(x) + (-1,) for x in cov)
        ok = viol == want and all(vals[z] == -(F(p, 2) - 2 * eta2) for z in viol)
        bad += not ok
        cnt += 1
        withcov += bool(cov)
        if not ok:
            print("  FAIL", sets, p, eta2, viol[:5], want[:5])
    print(f"[B] Theorem 1 by box enumeration: {cnt} instances ({withcov} with a cover; empty/duplicate sets "
          f"allowed; eta2 in {{window min, (p-1)/4, p/4 - 1/64}}), {pts} lattice points evaluated: {bad} failures")
    return bad == 0


# ---------------------------------------------------------------- C, D, E
def x3c_instance(q, n):
    p = 3 * q
    U = list(range(p))
    sets = []
    if rng.random() < 0.5:
        rng.shuffle(U)
        sets = [tuple(sorted(U[3 * k:3 * k + 3])) for k in range(q)]
    while len(sets) < n:
        sets.append(tuple(sorted(rng.sample(range(p), 3))))
    rng.shuffle(sets)
    return sets, p


def s_value(M):
    N = len(M)
    delta = [M[i][i] for i in range(N)]
    y = solve_exact(M, delta)
    return F(str(sum(sp.Rational(d.numerator, d.denominator) * yi for d, yi in zip(delta, y))))


def check_eps_size():
    print("[C] size of eps = 1/(2s) on X3C instances (digits of numerator / denominator):")
    rows = []
    for q, n in [(3, 6), (4, 10), (5, 15), (6, 20), (8, 30), (10, 40)]:
        sets, p = x3c_instance(q, n)
        M = build(sets, p, F(p - 1, 4))
        s = s_value(M)
        eps = 1 / (2 * s)
        rows.append((q, n, len(str(eps.numerator)), len(str(eps.denominator))))
        print(f"    q={q:2d} n={n:2d}: eps has {len(str(eps.numerator))} / {len(str(eps.denominator))} digits;"
              f" s = {float(s):.3f}, 4n+p = {4 * n + p}")
    return rows


def check_s_bound_and_fix(T=60):
    bad_bound = bad_fix = 0
    ratios = []
    for t in range(T):
        q = rng.randint(2, 4)
        n = rng.randint(q, q + 5)
        sets, p = x3c_instance(q, n)
        e2 = F(p - 1, 4)
        M = build(sets, p, e2)
        s = s_value(M)
        bound = 4 * n + p + F(1, 4 * (p - 1))
        bad_bound += not (s <= bound)
        ratios.append(float(s) / (n + p))
        eps = F(1, 8 * n + 2 * p + 1)
        N = len(M)
        delta = [M[i][i] for i in range(N)]
        X = [[F(1)] + [eps * dl for dl in delta]] + [[eps * delta[i]] + [eps * M[i][j] for j in range(N)] for i in range(N)]
        Y = [r[:] for r in X]
        Y[0][0] -= F(1, 4)
        Dn = [[F(0)] * (N + 1) for _ in range(N + 1)]
        for i in range(1, N + 1):
            Dn[0][i] = Dn[i][0] = X[i][i]
            for j in range(1, N + 1):
                if i != j:
                    Dn[i][j] = X[i][i] + X[j][j] - 2 * X[i][j]
        ok = eps * s < F(1, 2) and ldl_pd(X) and ldl_pd(Y)
        ok &= all(0 <= Dn[i][j] <= 1 for i in range(N + 1) for j in range(N + 1))
        ok &= ldl_pd([[1 - 2 * Dn[i][j] for j in range(N + 1)] for i in range(N + 1)])
        bad_fix += not ok
    # degenerate family: n copies of one triple plus a cover of the rest (p = 3q)
    deg = []
    for n in [5, 20, 80]:
        q = 2
        sets = [(0, 1, 2)] * n + [(3, 4, 5)]
        M = build(sets, 6, F(5, 4))
        deg.append((n, float(s_value(M))))
    print(f"[D] s <= 4n + p + 1/(4(p-1)) on {T} X3C instances: {bad_bound} failures; with eps' = 1/(8n+2p+1): "
          f"eps' s < 1/2, X PD, X - e0e0^T/4 PD, eps'd in [0,1], J - 2eps'D PD: {bad_fix} failures")
    print(f"    s/(n+p) on random X3C: min {min(ratios):.3f}, max {max(ratios):.3f}")
    print(f"    degenerate family (n copies of {{0,1,2}} plus {{3,4,5}}, p = 6): (n, s) = "
          + ", ".join(f"({a}, {b:.3f})" for a, b in deg))
    # duplicate-free family with n >> p: all triples of [p]
    for p in (6, 9):
        sets = list(itertools.combinations(range(p), 3))
        s = float(s_value(build(sets, p, F(p - 1, 4))))
        print(f"    all triples of [{p}] (n = {len(sets)}): s = {s:.3f}, s/(n+p) = {s / (len(sets) + p):.3f}")
    return bad_bound == 0 and bad_fix == 0


def check_box_small_covers(T=60):
    """eps d in [0,1] also when triangle inequalities fail (general exact cover with a 1- or 2-set cover)."""
    bad = cnt = 0
    for t in range(T):
        p = rng.randint(2, 5)
        sets = random_instance(p, rng.randint(1, 4))
        cov = covers(sets, p)
        if not any(sum(x) <= 2 for x in cov):
            continue
        M = build(sets, p, F(p - 1, 4))
        s = s_value(M)
        eps = 1 / (2 * s)
        N = len(M)
        D = [[F(0)] * (N + 1) for _ in range(N + 1)]
        for i in range(N):
            D[0][i + 1] = D[i + 1][0] = M[i][i]
            for j in range(N):
                if i != j:
                    D[i + 1][j + 1] = M[i][i] + M[j][j] - 2 * M[i][j]
        cnt += 1
        bad += not all(0 <= eps * D[i][j] <= 1 for i in range(N + 1) for j in range(N + 1))
    print(f"[E] eps d in [0,1] at instances with a cover of <= 2 sets (triangle fails): {cnt} instances, {bad} failures")
    return bad == 0


# ---------------------------------------------------------------- F
def gap0_construct(c):
    n = len(c)
    C = sum(c)
    K = 4 * n * C
    a = [ci + K for ci in c]
    A2 = sum(t * t for t in a)
    amin, amax = min(a), max(a)
    tlb = F(2 * (n - 1) * amin ** 2 - (n + 1) * amax ** 2, (n - 1) * (n - 2))
    nu = tlb / (A2 * amax ** 2)
    rho = [t * t * (1 + nu * t * t / A2) for t in a]
    Dl = sum(rho)
    th = [[(rho[i] + rho[j]) / (n - 2) - Dl / ((n - 1) * (n - 2)) if i != j else F(0) for j in range(n)] for i in range(n)]
    L = [[(sum(th[i]) if i == j else -th[i][j]) for j in range(n)] for i in range(n)]
    Z = [[L[i][j] / (a[i] * a[j]) - nu * a[i] * a[j] / A2 for j in range(n)] for i in range(n)]
    return a, tlb, nu, th, Z


def check_gap0_n4(T=25):
    bad = yes = 0
    for t in range(T):
        c = [rng.randint(0, 9) for _ in range(4)]
        if sum(c) == 0:
            c[0] = 1
        a, tlb, nu, th, Z = gap0_construct(c)
        ok = tlb > 0 and all(Z[i][i] == 1 for i in range(4))
        ok &= all(th[i][j] >= tlb for i in range(4) for j in range(4) if i != j)
        anyb = False
        for s in itertools.product((1, -1), repeat=4):
            # basis of s-perp: f_j = e_j - s_0 s_j e_0, j = 1..3
            B = [[(-s[0] * s[j] if k == 0 else int(k == j)) for k in range(4)] for j in range(1, 4)]
            G = [[sum(B[i][k] * Z[k][l] * B[j][l] for k in range(4) for l in range(4)) for j in range(3)] for i in range(3)]
            notpsd = not psd_exact(G)
            bal = sum(si * ci for si, ci in zip(s, c)) == 0 and sum(s) == 0
            ok &= notpsd == bal
            anyb |= bal
        yes += anyb
        bad += not ok
    print(f"[F] Theorem 4 at n = 4: {T} instances ({yes} balanced): theta_lb > 0, Z_ii = 1, theta >= theta_lb, "
          f"Z|s-perp not PSD <=> balanced partition, for all 16 s: {bad} failures")
    return bad == 0


if __name__ == "__main__":
    r = [check_symbolic(), check_theorem1()]
    check_eps_size()
    r += [check_s_bound_and_fix(), check_box_small_covers(), check_gap0_n4()]
    print("REVIEWER CHECKS PASSED" if all(r) else "SOME REVIEWER CHECK FAILED")
    sys.exit(0 if all(r) else 1)
