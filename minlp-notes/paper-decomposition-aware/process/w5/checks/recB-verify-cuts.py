"""W5 recB verification: exact checks of the proofs changed in W5.

1. prop:cr-cut(a): Phi(z) = Phi_0 + sum_i min{0,rho_i} + cap(S_z), with pair
   arcs of capacity -omega_ij/2 (the removed symbol r_ij).
2. prop:cr-submod(c): F~(t)+F~(t') >= F~(t^t')+F~(tvt') for a quadratic with
   nonpositive off-diagonal entries, t,t' in [0,1]^R (renamed from s,t).
3. prop:cr-submod(c) and prop:cr-greedy(a) on the concave-convex class with
   one continuous convex coordinate in R_+ (exact 1-D minimization):
   Phi is submodular, and for every ordering pi, every S and every i in S,
   a^pi_i <= hatPhi(S_<i + i) - hatPhi(S_<i) (new proof of (a)), hence
   a^pi(S) <= hatPhi(S) and a^pi(R_-) = hatPhi(R_-).
"""
from fractions import Fraction as Fr
from itertools import permutations, product
import random

random.seed(20261003)


def rnd(a=-5, b=5, den=4):
    return Fr(random.randint(a * den, b * den), den)


def check_cut(trials=300):
    for _ in range(trials):
        m = random.randint(1, 5)
        phi0, mu = rnd(), [rnd() for _ in range(m)]
        om = {(i, j): (min(Fr(0), rnd()) if random.random() < 0.7 else Fr(0))
              for i in range(m) for j in range(i + 1, m)}
        w = lambda i, j: om[(min(i, j), max(i, j))]
        rho = [mu[i] + Fr(1, 2) * sum(w(i, j) for j in range(m) if j != i)
               for i in range(m)]
        for z in product((0, 1), repeat=m):
            Phi = phi0 + sum(mu[i] * z[i] for i in range(m)) + sum(
                om[(i, j)] * z[i] * z[j] for (i, j) in om)
            S = {i for i in range(m) if z[i]}
            cap = Fr(0)
            for i in range(m):
                if i in S:
                    cap += max(rho[i], 0)          # arc i -> t
                else:
                    cap += max(-rho[i], 0)         # arc s -> i
            for (i, j), o in om.items():
                if o != 0 and ((i in S) != (j in S)):
                    cap += -o / 2                  # exactly one of i->j, j->i
            assert Phi == phi0 + sum(min(Fr(0), r) for r in rho) + cap
    print("cut identity with capacities -omega_ij/2: OK")


def check_lattice(trials=300):
    for _ in range(trials):
        m = random.randint(2, 5)
        H = [[Fr(0)] * m for _ in range(m)]
        for i in range(m):
            H[i][i] = rnd()
            for j in range(i + 1, m):
                H[i][j] = H[j][i] = min(Fr(0), rnd())
        b = [rnd() for _ in range(m)]
        F = lambda t: Fr(1, 2) * sum(H[i][j] * t[i] * t[j]
                                     for i in range(m) for j in range(m)) + sum(
            b[i] * t[i] for i in range(m))
        for _ in range(10):
            t = [Fr(random.randint(0, 8), 8) for _ in range(m)]
            tp = [Fr(random.randint(0, 8), 8) for _ in range(m)]
            lo = [min(x, y) for x, y in zip(t, tp)]
            hi = [max(x, y) for x, y in zip(t, tp)]
            assert F(t) + F(tp) >= F(lo) + F(hi)
            for i in range(m):
                for j in range(m):
                    if i != j and (t[i] - tp[i]) * (t[j] - tp[j]) < 0:
                        lhs = (t[i] * t[j] + tp[i] * tp[j] - lo[i] * lo[j]
                               - hi[i] * hi[j])
                        assert lhs == (t[i] - tp[i]) * (t[j] - tp[j])
    print("lattice inequality of prop:cr-submod(c): OK")


def min_convex_1d(a, c, lo, hi):
    """min of a/2 y^2 + c y on [lo,hi], a >= 0, exact."""
    cands = [lo, hi]
    if a > 0:
        y = -c / a
        if lo < y < hi:
            cands.append(y)
    return min(a / 2 * y * y + c * y for y in cands)


def check_greedy(trials=200):
    for _ in range(trials):
        m = random.randint(1, 4)          # |R_-|; index m is the R_+ coordinate
        n = m + 1
        o = [random.choice((-1, 1)) for _ in range(n)]
        H = [[Fr(0)] * n for _ in range(n)]
        for i in range(m):
            H[i][i] = min(Fr(0), rnd())   # (R1) on R_-
        H[m][m] = max(Fr(0), rnd())       # convex R_+
        for i in range(n):
            for j in range(i + 1, n):
                x = abs(rnd()) if random.random() < 0.8 else Fr(0)
                H[i][j] = H[j][i] = -o[i] * o[j] * x   # o_i o_j H_ij <= 0
        b = [rnd() for _ in range(n)]
        lo = [Fr(random.randint(-4, 0)) for _ in range(n)]
        up = [l + Fr(random.randint(1, 4), random.choice((1, 2))) for l in lo]
        alpha = [lo[i] if o[i] == 1 else up[i] for i in range(n)]
        delta = [(up[i] - lo[i]) * o[i] for i in range(n)]

        def Phi(S):
            y = [alpha[i] + delta[i] * (1 if i in S else 0) for i in range(m)]
            const = Fr(1, 2) * sum(H[i][j] * y[i] * y[j]
                                   for i in range(m) for j in range(m)) + sum(
                b[i] * y[i] for i in range(m))
            c = b[m] + sum(H[m][i] * y[i] for i in range(m))
            return const + min_convex_1d(H[m][m], c, lo[m], up[m])

        subsets = [frozenset(i for i in range(m) if bits >> i & 1)
                   for bits in range(2 ** m)]
        val = {S: Phi(S) for S in subsets}
        for S in subsets:
            for T in subsets:
                assert val[S] + val[T] >= val[S & T] + val[S | T]
        hat = {S: val[S] - val[frozenset()] for S in subsets}
        for pi in permutations(range(m)):
            pre = [frozenset(pi[:l]) for l in range(m + 1)]
            a = {pi[l - 1]: hat[pre[l]] - hat[pre[l - 1]]
                 for l in range(1, m + 1)}
            assert sum(a.values()) == hat[frozenset(range(m))]
            pos = {pi[l]: l for l in range(m)}
            for S in subsets:
                for i in S:
                    Sless = frozenset(j for j in S if pos[j] < pos[i])
                    assert Sless <= pre[pos[i]] and i not in pre[pos[i]]
                    assert a[i] <= hat[Sless | {i}] - hat[Sless]
                assert sum(a[i] for i in S) <= hat[S]
    print("submodularity and greedy inequality (new proof of (a)): OK")


check_cut()
check_lattice()
check_greedy()
print("ALL PASS")
