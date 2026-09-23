"""Exact small-network checks for the reviewed common-capacity argument.

Independent vertex enumeration, not an implementation of its symbolic
polynomial-time algorithm. Uses only the Python standard library.
"""

from fractions import Fraction as F
from itertools import combinations
from random import Random


def solve_square(rows, rhs):
    n = len(rhs)
    a = [list(map(F, row)) + [F(b)] for row, b in zip(rows, rhs)]
    for col in range(n):
        pivot = next((i for i in range(col, n) if a[i][col]), None)
        if pivot is None:
            return None
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        a[col] = [v / scale for v in a[col]]
        for i in range(n):
            if i != col:
                scale = a[i][col]
                a[i] = [x - scale * y for x, y in zip(a[i], a[col])]
    return tuple(row[-1] for row in a)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def main():
    rng = Random(608905)
    counts = dict(networks=0, vertices=0, subset_supports=0,
                  signed_objectives=0, interpolations=0)
    for case in range(36):
        # Path, triangle, and disconnected graph with isolated vertices.
        if case % 3 == 0:
            n, edges = 4, [(0, 1), (1, 2), (2, 3)]
        elif case % 3 == 1:
            n, edges = 3, [(0, 1), (1, 2), (2, 0)]
        else:
            n, edges = 5, [(0, 1), (2, 3)]
        edges = [(u, v) if rng.randrange(2) else (v, u) for u, v in edges]
        m = len(edges)
        incidence = [[F((v == u) - (v == w)) for u, w in edges]
                     for v in range(n)]
        seed = tuple(F(rng.randrange(-6, 7), 3) for _ in edges)
        lower = [x - F(rng.randrange(4), 2) for x in seed]
        upper = [x + F(rng.randrange(4), 2) for x in seed]
        div_seed = [dot(row, seed) for row in incidence]
        alpha = [x - F(rng.randrange(3), 2) for x in div_seed]
        beta = [x + F(rng.randrange(3), 2) for x in div_seed]
        rows, rhs = [], []
        for e in range(m):
            unit = [F(int(j == e)) for j in range(m)]
            rows += [unit, [-v for v in unit]]
            rhs += [upper[e], -lower[e]]
        for row, a, b in zip(incidence, alpha, beta):
            rows += [row, [-v for v in row]]
            rhs += [b, -a]
        vertices = set()
        for active in combinations(range(len(rows)), m):
            x = solve_square([rows[i] for i in active], [rhs[i] for i in active])
            if x is not None and all(dot(row, x) <= b for row, b in zip(rows, rhs)):
                vertices.add(x)
        assert vertices
        divergences = {x: tuple(dot(row, x) for row in incidence) for x in vertices}
        masks = range(1 << n)

        def total(vec, mask):
            return sum((vec[i] for i in range(n) if mask >> i & 1), F(0))

        def cut(mask):
            ans = F(0)
            for e, (u, v) in enumerate(edges):
                if mask >> u & 1 and not mask >> v & 1:
                    ans += upper[e]
                if mask >> v & 1 and not mask >> u & 1:
                    ans -= lower[e]
            return ans

        g = {s: min(cut(t) + total(beta, s & ~t) - total(alpha, t & ~s)
                    for t in masks) for s in masks}
        assert g[0] == g[(1 << n) - 1] == 0
        for s in masks:
            assert g[s] == max(total(d, s) for d in divergences.values())
            counts['subset_supports'] += 1
        for _ in range(8):
            cost = [F(rng.randrange(-8, 9), rng.randrange(1, 5)) for _ in range(n)]
            order = sorted(range(n), key=lambda i: -cost[i])
            greedy, s = [F(0)] * n, 0
            for i in order:
                old, s = s, s | (1 << i)
                greedy[i] = g[s] - g[old]
            expected = max(dot(cost, d) for d in divergences.values())
            assert dot(cost, greedy) == expected
            assert all(alpha[i] <= greedy[i] <= beta[i] for i in range(n))
            assert all(total(greedy, s) <= cut(s) for s in masks)
            lo_flow = min(vertices, key=lambda x: dot(cost, divergences[x]))
            hi_flow = max(vertices, key=lambda x: dot(cost, divergences[x]))
            lo, hi = [dot(cost, divergences[x]) for x in (lo_flow, hi_flow)]
            # A chosen resource interval overlapping, touching, or outside
            # the support interval. Verify the exact overlap rule.
            for a, b in [(lo, hi), (hi, hi), (hi + 1, hi + 2),
                         (lo - 2, lo - 1), ((lo + hi) / 2, hi + 1)]:
                overlap = lo <= b and hi >= a
                if overlap:
                    target = max(lo, a)
                    lam = (target - lo) / (hi - lo) if hi != lo else F(0)
                    flow = tuple((1 - lam) * x + lam * y
                                 for x, y in zip(lo_flow, hi_flow))
                    assert all(dot(row, flow) <= bound for row, bound in zip(rows, rhs))
                    value = dot(cost, [dot(row, flow) for row in incidence])
                    assert a <= value <= b and value == target
                    counts['interpolations'] += 1
            counts['signed_objectives'] += 1
        counts['networks'] += 1
        counts['vertices'] += len(vertices)
    print('PASS', counts)


if __name__ == '__main__':
    main()
