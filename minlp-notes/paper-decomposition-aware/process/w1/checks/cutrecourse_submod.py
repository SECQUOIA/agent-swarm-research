"""Exact checks of the mixed concave/convex submodular residual oracle.

Random instances 1/2 z'Az + b'z on a rational box with orientation signs
o_i o_j A_ij <= 0, A_ii <= 0 on D and A_CC PSD.  We check, exactly:
  * endpoint reduction: no grid point of the D coordinates (with exact convex
    completion) beats min_S g(S);
  * g(S) + g(T) >= g(S&T) + g(S|T) for all S, T;
  * every greedy vector lies in the base polytope B(h);
  * Edmonds' min-max: the best mixture of at most |D|+1 greedy vectors (exact
    vertex enumeration) certifies min h exactly;
  * the two-label fixture 0, 13/16, 13/16, 0 needs a two-vector mixture.
"""
import random
from fractions import Fraction as Fr
from itertools import product, permutations

def qp_min_box(P, p, const, lo, hi):
    """Exact min of 1/2 v'Pv + p'v + const over prod [lo_i, hi_i], dim <= 2."""
    k = len(p)
    best = None
    for face in product((0, 1, None), repeat=k):
        free = [i for i in range(k) if face[i] is None]
        v = [None] * k
        for i in range(k):
            if face[i] == 0: v[i] = lo[i]
            elif face[i] == 1: v[i] = hi[i]
        fixed = [i for i in range(k) if face[i] is not None]
        rhs = [-(p[i] + sum(P[i][j] * v[j] for j in fixed)) for i in free]
        if len(free) == 1:
            i = free[0]
            if P[i][i] == 0: continue
            v[i] = rhs[0] / P[i][i]
        elif len(free) == 2:
            a, bb, c, d = P[free[0]][free[0]], P[free[0]][free[1]], P[free[1]][free[0]], P[free[1]][free[1]]
            det = a * d - bb * c
            if det == 0: continue
            v[free[0]] = (d * rhs[0] - bb * rhs[1]) / det
            v[free[1]] = (-c * rhs[0] + a * rhs[1]) / det
        if any(not (lo[i] <= v[i] <= hi[i]) for i in range(k)):
            continue
        val = const + sum(p[i] * v[i] for i in range(k)) + sum(P[i][j] * v[i] * v[j] for i in range(k) for j in range(k)) / 2
        best = val if best is None else min(best, val)
    return best

def rnd(rng):
    return Fr(rng.randint(-10, 10), rng.choice((1, 2, 3, 4)))

def instance(rng, mD, mC):
    n = mD + mC
    o = [rng.choice((-1, 1)) for _ in range(n)]
    A = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < 0.8:
                w = -abs(rnd(rng)) * o[i] * o[j]
                A[i][j] = A[j][i] = w
    for i in range(mD):
        A[i][i] = -abs(rnd(rng)) if rng.random() < 0.8 else Fr(0)
    # make the C block PSD: diagonal >= sum of |offdiag| in C block (diagonally dominant), sometimes singular
    for i in range(mD, n):
        s = sum(abs(A[i][j]) for j in range(mD, n) if j != i)
        A[i][i] = s + (abs(rnd(rng)) if rng.random() < 0.6 else 0)
    b = [rnd(rng) for _ in range(n)]
    lo = [rnd(rng) for _ in range(n)]
    hi = [lo[i] + abs(rnd(rng)) + Fr(1, 3) for i in range(n)]
    return A, b, o, lo, hi

def g_of(A, b, lo, hi, mD, zD):
    n = len(b); C = list(range(mD, n))
    P = [[A[i][j] for j in C] for i in C]
    p = [b[i] + sum(A[i][j] * zD[j] for j in range(mD)) for i in C]
    const = sum(b[j] * zD[j] for j in range(mD)) + sum(A[i][j] * zD[i] * zD[j] for i in range(mD) for j in range(mD)) / 2
    return qp_min_box(P, p, const, [lo[i] for i in C], [hi[i] for i in C])

def run(rng, trials=40):
    for _ in range(trials):
        mD, mC = 3, rng.randint(1, 2)
        A, b, o, lo, hi = instance(rng, mD, mC)
        D = list(range(mD))
        # label S (indicator t) -> z_i = alpha_i + d_i t_i (orientation)
        def zD_of(S):
            return [(lo[i] if o[i] == 1 else hi[i]) + (o[i] * (hi[i] - lo[i]) if i in S else 0) for i in D]
        subsets = [frozenset(s) for r in range(mD + 1) for s in __import__('itertools').combinations(D, r)]
        g = {S: g_of(A, b, lo, hi, mD, zD_of(S)) for S in subsets}
        gmin = min(g.values())
        # endpoint reduction against a grid on D
        for t in product(range(4), repeat=mD):
            zD = [lo[i] + (hi[i] - lo[i]) * Fr(t[i], 3) for i in D]
            assert g_of(A, b, lo, hi, mD, zD) >= gmin
        # submodularity
        for S in subsets:
            for T in subsets:
                assert g[S] + g[T] >= g[S & T] + g[S | T]
        h = {S: g[S] - g[frozenset()] for S in subsets}
        greedy = []
        for pi in permutations(D):
            w = [Fr(0)] * mD; pref = frozenset()
            for e in pi:
                w[e] = h[pref | {e}] - h[pref]; pref = pref | {e}
            for T in subsets:
                assert sum(w[i] for i in T) <= h[T]
            assert sum(w) == h[frozenset(D)]
            greedy.append(w)
        # Edmonds: max over mixtures of sum min(0,w_i) equals min h.  The maximum of this
        # concave piecewise-linear function over the simplex is attained at a vertex:
        # support of size s <= mD+1 and s-1 coordinates with w_i = 0.  Enumerate exactly.
        from itertools import combinations
        hmin = min(h.values())
        best = None
        nP = len(greedy)
        for s in range(1, mD + 2):
            for supp in combinations(range(nP), s):
                for Z in combinations(D, s - 1):
                    # equations: sum lambda = 1 ; sum_p lambda_p w_p,i = 0 (i in Z)
                    M = [[Fr(1)] * s + [Fr(1)]] + [[greedy[p][i] for p in supp] + [Fr(0)] for i in Z]
                    # Gaussian elimination
                    rows = [r[:] for r in M]; ok = True
                    for col in range(s):
                        piv = next((r for r in range(col, s) if rows[r][col] != 0), None)
                        if piv is None: ok = False; break
                        rows[col], rows[piv] = rows[piv], rows[col]
                        pv = rows[col][col]
                        rows[col] = [x / pv for x in rows[col]]
                        for r in range(s):
                            if r != col and rows[r][col] != 0:
                                f = rows[r][col]
                                rows[r] = [a - f * bb for a, bb in zip(rows[r], rows[col])]
                    if not ok: continue
                    lam = [rows[r][s] for r in range(s)]
                    if any(x < 0 for x in lam): continue
                    w = [sum(lam[q] * greedy[supp[q]][i] for q in range(s)) for i in D]
                    val = sum(min(Fr(0), wi) for wi in w)
                    assert val <= hmin
                    best = val if best is None else max(best, val)
        assert best == hmin, (best, hmin)
    return trials

def fixture():
    # -a^2 - b^2 + 2a + 2b - 3/2 ab + z^2 - 1/2 (1+a+b) z + 1/16 on [0,1]^3
    def val(a, bb):
        z = (1 + a + bb) / 4
        return -a * a - bb * bb + 2 * a + 2 * bb - Fr(3, 2) * a * bb + z * z - (1 + a + bb) * z / 2 + Fr(1, 16)
    g = {(0, 0): val(Fr(0), Fr(0)), (1, 0): val(Fr(1), Fr(0)), (0, 1): val(Fr(0), Fr(1)), (1, 1): val(Fr(1), Fr(1))}
    assert list(g.values()) == [0, Fr(13, 16), Fr(13, 16), 0]
    w1 = (g[(1, 0)] - g[(0, 0)], g[(1, 1)] - g[(1, 0)])
    w2 = (g[(1, 1)] - g[(0, 1)], g[(0, 1)] - g[(0, 0)])
    assert w1 == (Fr(13, 16), Fr(-13, 16)) and w2 == (Fr(-13, 16), Fr(13, 16))
    assert sum(min(0, x) for x in w1) == Fr(-13, 16)
    mix = tuple((x + y) / 2 for x, y in zip(w1, w2))
    assert sum(min(0, x) for x in mix) == 0
    return True

if __name__ == "__main__":
    rng = random.Random(99)
    fixture()
    print("fixture 0,13/16,13/16,0 with two-vector mixture: passed")
    n = run(rng)
    print("mixed submodular oracle: %d random instances passed (endpoint reduction, submodularity, base polytope, exact min-max mixture)" % n)
    print("ALL SUBMODULAR CHECKS PASSED")
