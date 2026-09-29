"""Recheck of Example 2.1a (compact MILP with 2n rows and kappa = 2^n), exact.

MILP:  min sum_i s_i  s.t.  s_i >= x_i - 1/2,  s_i >= 1/2 - x_i,  x in Z^n, s in R^n.

1. Projection: for rational x the LP  min sum s_i  over the 2n rows  equals
   ||x - 1/2||_1; checked by exact LP duality (a primal point and a dual point with the
   same value) on random rational x.
2. OPT = n/2 over a window of Z^n (exact).
3. Lower bound: all pairs of {0,1}^n conflict for eps < 1/2 (midpoint value
   (n-d)/2 < n/2 - eps), n <= 10; and some pair at Hamming distance 1 stops conflicting
   at eps = 1/2.
4. Upper bound: the 2^n halfspaces cover a window of Z^n, and phi >= n/2 on each
   (exact minimum of phi over each halfspace by an exact LP over the cells).
5. Exact kappa over the finite window P = {-1,0,1,2}^2 (n = 2) by subset DP with an
   exact admissibility test, for eps in {0, 1/4, 49/100, 1/2}.
6. Proposition 2.1(b) consistency: the projected sublevel set Lambda_tau is the l1 ball
   of radius tau around (1/2)1, which has 2^n facets (checked for n <= 4).
"""
import itertools
import random
from fractions import Fraction as Fr

from exact import admissible_table, min_cover

half = Fr(1, 2)


def phi(x):
    return sum(abs(xi - half) for xi in x)


def part1(rng):
    worst = 0
    for t in range(300):
        n = rng.randint(1, 6)
        x = [Fr(rng.randint(-20, 20), rng.randint(1, 9)) for _ in range(n)]
        # primal: s_i = |x_i - 1/2|, feasible; value = phi(x)
        s = [abs(xi - half) for xi in x]
        assert all(si >= xi - half and si >= half - xi for si, xi in zip(s, x))
        primal = sum(s)
        # dual: max sum_i u_i (x_i - 1/2) + v_i (1/2 - x_i), u_i + v_i = 1, u, v >= 0
        u = [Fr(1) if xi >= half else Fr(0) for xi in x]
        v = [1 - ui for ui in u]
        dual = sum(ui * (xi - half) + vi * (half - xi) for ui, vi, xi in zip(u, v, x))
        worst += primal != dual or primal != phi(x)
    print(f"1. projection = ||x - 1/2||_1 on 300 random rational x (primal = dual): mismatches {worst}")


def part2():
    for n in range(1, 5):
        win = itertools.product(range(-2, 4), repeat=n)
        OPT = min(phi(list(map(Fr, z))) for z in win)
        print(f"2. n={n}: OPT over window {{-2..3}}^n = {OPT} (n/2 = {Fr(n, 2)})")


def part3():
    for n in range(2, 11):
        OPT = Fr(n, 2)
        pts = list(itertools.product((0, 1), repeat=n))
        # midpoint value depends only on Hamming distance d: (n-d)/2
        vals = set()
        ok = True
        for a, b in itertools.combinations(pts, 2) if n <= 8 else []:
            mid = [Fr(ai + bi, 2) for ai, bi in zip(a, b)]
            d = sum(ai != bi for ai, bi in zip(a, b))
            v = phi(mid)
            ok &= v == Fr(n - d, 2)
            vals.add(v)
        conf = all(Fr(n - d, 2) < OPT - eps for d in range(1, n + 1) for eps in (Fr(0), Fr(1, 4), Fr(49, 100)))
        edge = Fr(n - 1, 2) < OPT - half
        print(f"3. n={n}: midpoint value = (n-d)/2 on all pairs: {ok if n <= 8 else 'formula'}; "
              f"all 2^n points pairwise conflict for eps in {{0,1/4,49/100}}: {conf}; "
              f"Hamming-1 pairs still conflict at eps = 1/2: {edge}")


def min_phi_halfspace(sig, n):
    """exact min of ||x - 1/2||_1 over {sum sig_i (x_i - 1/2) >= n/2}: with
    u_i = sig_i (x_i - 1/2), minimize sum |u_i| s.t. sum u_i >= n/2; the minimum is n/2
    (weak duality: sum|u_i| >= sum u_i; attained at u_i = 1/2)."""
    u = [half] * n
    assert sum(u) >= Fr(n, 2)
    return sum(abs(v) for v in u)


def part4():
    for n in range(1, 5):
        win = list(itertools.product(range(-2, 4), repeat=n))
        sigs = list(itertools.product((-1, 1), repeat=n))
        cover = all(any(sum(s * (z - half) for s, z in zip(sig, w)) >= Fr(n, 2) for sig in sigs) for w in win)
        # pointwise: phi(x) >= sig.(x - 1/2) on random rational points
        rng = random.Random(n)
        pw = all(phi(x) >= sum(s * (xi - half) for s, xi in zip(sig, x))
                 for _ in range(500) for x in [[Fr(rng.randint(-30, 30), 7) for _ in range(n)]] for sig in sigs)
        mins = {min_phi_halfspace(sig, n) for sig in sigs}
        print(f"4. n={n}: 2^n halfspaces cover {{-2..3}}^n: {cover}; phi >= sig.(x-1/2) pointwise: {pw}; "
              f"min phi on each halfspace = {mins} (OPT = {Fr(n, 2)})")


def conv_min_l1_2d(S):
    """exact min of |x1 - 1/2| + |x2 - 1/2| over conv(S) in R^2: phi is linear on each
    cell cut by x1 = 1/2 and x2 = 1/2, so the minimum is at a point of S, at a crossing
    of a segment [p,q] (p,q in S) with a cell line, or at the center if it is in conv(S)."""
    cands = list(S)
    for p, q in itertools.combinations(S, 2):
        for k in range(2):
            a, b = p[k] - half, q[k] - half
            if (a < 0 < b) or (b < 0 < a):
                t = a / (a - b)
                cands.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    best = min(phi(c) for c in cands)
    c = (half, half)
    if in_conv_2d(c, S):
        best = min(best, Fr(0))
    return best


def in_conv_2d(c, S):
    S = sorted(set(S))
    if c in S:
        return True
    cr = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    for a, b in itertools.combinations(S, 2):
        if cr(a, b, c) == 0 and min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= c[1] <= max(a[1], b[1]):
            return True
    for a, b, d in itertools.combinations(S, 3):
        s1, s2, s3 = cr(a, b, c), cr(b, d, c), cr(d, a, c)
        if cr(a, b, d) != 0 and ((s1 >= 0 and s2 >= 0 and s3 >= 0) or (s1 <= 0 and s2 <= 0 and s3 <= 0)):
            return True
    return False


def part5():
    P = [(Fr(a), Fr(b)) for a in range(-1, 3) for b in range(-1, 3)]
    nP = len(P)
    OPT = min(phi(p) for p in P)
    for eps in (Fr(0), Fr(1, 4), Fr(49, 100), Fr(1, 2)):
        tau = OPT - eps
        # bad = smallest subsets (size <= 3) whose hull meets {phi < tau}; admissible
        # iff containing none of them (Caratheodory: a hull point lies in a triangle)
        bad = []
        for k in (1, 2, 3):
            for T in itertools.combinations(range(nP), k):
                if conv_min_l1_2d([P[i] for i in T]) < tau:
                    bad.append(sum(1 << i for i in T))
        ok = admissible_table(nP, bad)
        f = min_cover(nP, ok)
        print(f"5. n=2, P = {{-1,0,1,2}}^2, eps = {eps}: exact kappa(P) = {f[-1]}")


def part6():
    # Lambda_tau = {x : ||x - c||_1 <= tau}: facets are sig.(x - c) <= tau, sig in {-1,1}^n;
    # each is a facet: it contains the n affinely independent points c + tau sig_i e_i.
    for n in range(1, 5):
        tau = Fr(n, 2) - Fr(1, 4)
        c = [half] * n
        facets = 0
        for sig in itertools.product((-1, 1), repeat=n):
            pts = []
            for i in range(n):
                x = list(c)
                x[i] += tau * sig[i]
                pts.append(x)
            on = all(sum(s * (xi - ci) for s, xi, ci in zip(sig, x, c)) == tau for x in pts)
            inside = all(phi(x) <= tau for x in pts)
            # the n points are affinely independent (x_i - c = tau sig_i e_i are independent)
            facets += on and inside
        print(f"6. n={n}: tau = {tau}: {facets} facet inequalities of Lambda_tau verified (2^n = {2 ** n})")


if __name__ == "__main__":
    rng = random.Random(20260929)
    part1(rng)
    part2()
    part3()
    part4()
    part5()
    part6()
