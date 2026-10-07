"""Verifier checks (group exact, second pass) for two denominator claims.

1. Proof of Corollary cor:poly: for an explicit polynomial F of degree <= d on a
   box, the curvature bounds L_i of Lemma lem:intcurv lie in
   (Gamma_F Gamma_X^(d-2))^-1 Z, where Gamma_F is the product of the
   coefficient denominators and Gamma_X that of the endpoint denominators.
   Then L_i w^2 has a denominator dividing Gamma_F (Gamma_X 2^a)^d whenever w
   has a denominator dividing Gamma_X 2^a and d >= 2.
2. Proof of Proposition prop:margin: with the common mesh h_j = s 2^-j and
   grading theta = 2^-mu, the graded-grid nodes of stage j (centers taken from
   earlier nodes, boxes shrunk to hulls of earlier nodes) have denominators
   dividing Gamma_X 2^(j + mu K) on X = [0, 1/2]^m, where K is the cap.
Exact arithmetic (fractions); random instances.
"""
import itertools
import math
from fractions import Fraction as F
from random import Random


def monomial_range(alpha, box):
    lo, hi = F(1), F(1)
    for k, a in enumerate(alpha):
        if a == 0:
            continue
        l, u = box[k]
        vals = [l ** a, u ** a]
        if a % 2 == 0 and l < 0 < u:
            vals.append(F(0))
        cand = [x * y for x in (lo, hi) for y in (min(vals), max(vals))]
        lo, hi = min(cand), max(cand)
    return lo, hi


def check_intcurv(rng, trials=400):
    for _ in range(trials):
        n = rng.randint(1, 3)
        d = rng.randint(2, 5)
        box = []
        for _ in range(n):
            l = F(rng.randint(-5, 3), rng.randint(1, 6))
            box.append((l, l + F(rng.randint(1, 7), rng.randint(1, 6))))
        terms = {}
        for _ in range(rng.randint(1, 6)):
            deg = rng.randint(0, d)
            alpha = [0] * n
            for _ in range(deg):
                alpha[rng.randrange(n)] += 1
            terms[tuple(alpha)] = F(rng.randint(-9, 9), rng.randint(1, 9))
        GF = math.prod(c.denominator for c in terms.values())
        GX = math.prod(e.denominator for bd in box for e in bd)
        for i in range(n):
            dd = {}
            for alpha, c in terms.items():
                if alpha[i] >= 2:
                    beta = list(alpha)
                    beta[i] -= 2
                    dd[tuple(beta)] = dd.get(tuple(beta), F(0)) + c * alpha[i] * (alpha[i] - 1)
            Lhat = F(0)
            for beta, c in dd.items():
                lo, hi = monomial_range(beta, box)
                Lhat += max(c * lo, c * hi)
            Li = max(Lhat, F(0))
            assert (Li * GF * GX ** (d - 2)).denominator == 1, 'L_i denominator'
            # correction L_i w^2 with w in (GX 2^a)^-1 Z
            a = rng.randint(0, 6)
            w = F(rng.randint(0, 50), GX * 2 ** a)
            assert (Li * w * w * GF * (GX * 2 ** a) ** d).denominator == 1, 'correction'
    return True


def graded(lo, hi, c, h, theta):
    nodes, steps = {c}, 0
    for sign, end in ((1, hi), (-1, lo)):
        t, R = F(0), abs(end - c)
        while t < R:
            t = min(t + h + theta * t, R)
            nodes.add(c + sign * t)
            steps += 1
    return sorted(nodes)


def check_margin_denominators(rng, trials=300):
    for _ in range(trials):
        m = rng.randint(1, 3)
        mu = rng.randint(2, 4)
        theta = F(1, 2 ** mu)
        box = [(F(0), F(1, 2))] * m
        GX = 2 ** m          # product of endpoint denominators (0 and 1/2)
        s = F(1, 2)
        cur = list(box)
        c = [F(0)] * m
        Kmax = 0
        for j in range(rng.randint(1, 7)):
            h = s / 2 ** j
            grids = [graded(cur[i][0], cur[i][1], c[i], h, theta) for i in range(m)]
            K = max(len(G) for G in grids)
            Kmax = max(Kmax, K)
            for G in grids:
                for v in G:
                    assert (GX * 2 ** (j + mu * Kmax)) % v.denominator == 0, 'node denominator'
            # shrink to the hull of a random run of consecutive nodes containing a new center
            newc, newbox = [], []
            for G in grids:
                a = rng.randrange(len(G))
                b = rng.randrange(a, len(G))
                newbox.append((G[a], G[b]))
                newc.append(G[rng.randint(a, b)])
            cur, c = newbox, newc
    return True


if __name__ == '__main__':
    rng = Random(20261003)
    check_intcurv(rng)
    print('PASS cor:poly: L_i in (Gamma_F Gamma_X^(d-2))^-1 Z; L_i w^2 over Gamma_F (Gamma_X 2^a)^d')
    check_margin_denominators(rng)
    print('PASS prop:margin: common-mesh nodes have denominators dividing Gamma_X 2^(j+mu K)')
    # rem:cf: g/(64 n^2 R^2) >= g/(32 R^4)  iff  R^2 >= 2 n^2
    for n in range(1, 30):
        for R in range(1, 200):
            assert (F(1, 64 * n * n * R * R) >= F(1, 32 * R ** 4)) == (R * R >= 2 * n * n)
    print('PASS rem:cf: threshold comparison holds iff R^2 >= 2 n^2')
    print('ALL PASS')
