"""Consistency check of Lemma N6 (separable bracket) in exact rationals, written for this recheck.

m(x, z) = m_1(x) + m_2(z), m_i = H_i - t^2 with H_i piecewise linear (pl1d.py), min m_i = eps_i,
eps_1 + eps_2 = eps (random split).  For each instance:
  slice_i = N^1(m_i + eps_j)     (greedy, exact)      lower bound on N_opt
  prod    = N^1(m_1) N^1(m_2)    (greedy, exact)      upper bound on N_guill
  G       = exact least guillotine certificate restricted to a grid containing all knots, both
            coordinates' greedy breakpoints and uniform points (DP).  G >= N_guill >= N_opt.
Asserts max(slice_1, slice_2) <= G <= prod (the product certificate lies on the grid).  A failure
of the left inequality would refute the lemma; the check cannot confirm N_opt itself.
Also asserts that N^1(m_i + eps_j) does not depend on the split (it equals N^1 of m_i - eps_i + eps).
Usage: python3 lemma_n6_check.py N_INSTANCES SEED
"""
import random
import sys
from fractions import Fraction as Fr
from functools import lru_cache

from pl1d import PL1D


def rand_1d(rng, epsi):
    k = rng.randint(2, 5)
    xs = sorted(set([Fr(0), Fr(1)] + [Fr(rng.randint(1, 99), 100) for _ in range(k)]))
    ms = [epsi + Fr(rng.randint(0, 1000), 1000) ** 2 / rng.choice([2, 4, 8]) for _ in xs]
    ms[rng.randrange(len(ms))] = epsi
    return PL1D(xs, ms)


def shifted(P, c):
    return PL1D(P.xs, [P.m(x) + c for x in P.xs])


def main(n, seed):
    rng = random.Random(seed)
    stats = dict(done=0, G_lt_prod=0, G_eq_slice=0, max_prod_over_G=Fr(0), max_G_over_slice=Fr(0))
    for _ in range(n):
        eps = Fr(1, rng.choice([50, 200, 1000]))
        e1 = eps * Fr(rng.randint(1, 9), 10)
        e2 = eps - e1
        P1, P2 = rand_1d(rng, e1), rand_1d(rng, e2)
        n1, b1 = P1.greedy()
        n2, b2 = P2.greedy()
        s1, sb1 = P1.greedy(-e2)
        s2, sb2 = P2.greedy(-e1)
        # split independence: m_i + eps_j == (m_i - eps_i) + eps
        assert s1 == shifted(P1, -e1 + eps).greedy()[0] and s2 == shifted(P2, -e2 + eps).greedy()[0]
        if n1 * n2 > 40:
            continue
        gx = sorted(set(P1.xs) | set(b1) | set(sb1) | {Fr(i, 6) for i in range(7)})
        gz = sorted(set(P2.xs) | set(b2) | set(sb2) | {Fr(i, 6) for i in range(7)})
        if len(gx) > 16 or len(gz) > 16:
            continue
        Fx = {(i, j): P1.minphi(gx[i], gx[j]) for i in range(len(gx)) for j in range(i + 1, len(gx))}
        Fz = {(i, j): P2.minphi(gz[i], gz[j]) for i in range(len(gz)) for j in range(i + 1, len(gz))}

        @lru_cache(maxsize=None)
        def G(i1, i2, j1, j2):
            if Fx[i1, i2] + Fz[j1, j2] >= 0:
                return 1
            best = 10 ** 9
            for c in range(i1 + 1, i2):
                best = min(best, G(i1, c, j1, j2) + G(c, i2, j1, j2))
            for c in range(j1 + 1, j2):
                best = min(best, G(i1, i2, j1, c) + G(i1, i2, c, j2))
            return best

        g = G(0, len(gx) - 1, 0, len(gz) - 1)
        assert g < 10 ** 9
        lo, hi = max(s1, s2), n1 * n2
        assert lo <= g <= hi, (lo, g, hi)
        stats["done"] += 1
        stats["G_lt_prod"] += g < hi
        stats["G_eq_slice"] += g == lo
        stats["max_prod_over_G"] = max(stats["max_prod_over_G"], Fr(hi, g))
        stats["max_G_over_slice"] = max(stats["max_G_over_slice"], Fr(g, lo))
    print({k: (str(v) if isinstance(v, Fr) else v) for k, v in stats.items()})


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]))
