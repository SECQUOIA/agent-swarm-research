"""Independent exact checks of selected risky identities; not a proof verifier.

Run from any directory with Python 3. Only standard-library arithmetic is used.
The manuscript and existing verification scripts are not imported.
"""
from fractions import Fraction as F
from itertools import product
from random import Random
import json

rng = Random(9032026)
counts = {}


def divergence(n, edges, w):
    d = [0] * n
    for (u, v), x in zip(edges, w):
        d[u] += x
        d[v] -= x
    return d


def signed_support():
    # Integral bounded incidence polytopes: enumerating integer arc values
    # captures every vertex and therefore the exact support for these cases.
    total = 0
    for n in range(2, 7):
        for case in range(35):
            edges = [(i, i + 1) if rng.randrange(2) else (i + 1, i)
                     for i in range(n - 1)]
            if case % 2 == 0 and n > 2:
                edges.append((n - 1, 0))
            lo = [rng.randint(-2, 0) for _ in edges]
            hi = [a + rng.randint(0, 2) for a in lo]
            alpha = [rng.randint(-3, 1) for _ in range(n)]
            beta = [a + rng.randint(0, 4) for a in alpha]
            ds = []
            for w in product(*(range(a, b + 1) for a, b in zip(lo, hi))):
                d = divergence(n, edges, w)
                if all(a <= x <= b for a, x, b in zip(alpha, d, beta)):
                    ds.append(d)
            sets = list(range(1 << n))
            def sum_on(vec, s):
                return sum(v for i, v in enumerate(vec) if (s >> i) & 1)
            def cut(s, upper):
                ans = 0
                for e, (u, v) in enumerate(edges):
                    su, sv = (s >> u) & 1, (s >> v) & 1
                    if su and not sv:
                        ans += hi[e] if upper else lo[e]
                    elif sv and not su:
                        ans -= lo[e] if upper else hi[e]
                return ans
            cuts = all(sum_on(alpha, s) <= cut(s, True) and
                       sum_on(beta, s) >= cut(s, False) for s in sets)
            assert bool(ds) == cuts
            if not ds:
                total += 1
                continue
            g = {s: min(cut(t, True) + sum_on(beta, s & ~t)
                        - sum_on(alpha, t & ~s) for t in sets) for s in sets}
            assert g[0] == g[(1 << n) - 1] == 0
            for a in sets:
                for b in sets:
                    assert g[a] + g[b] >= g[a | b] + g[a & b]
            costs = [F(rng.randint(-9, 9), rng.randint(1, 6)) for _ in range(n)]
            order = sorted(range(n), key=lambda i: (-costs[i], i))
            greedy = [0] * n
            s = 0
            for i in order:
                prev = s
                s |= 1 << i
                greedy[i] = g[s] - g[prev]
            assert greedy in ds
            value = sum(c * d for c, d in zip(costs, greedy))
            assert value == max(sum(c * v for c, v in zip(costs, d)) for d in ds)
            total += 1
    counts['signed_cut_and_box_support_instances'] = total


def clamp():
    total = 0
    for n in range(1, 9):
        for _ in range(60):
            unary = [(F(rng.randint(-9, 9), 3), F(rng.randint(-9, 9), 3))
                     for _ in range(n)]
            a = [F(rng.randint(0, 9), 4) for _ in range(n)]
            b = [F(rng.randint(0, 9), 4) for _ in range(n)]
            e0, e1 = unary[0]
            p = e1 - e0
            z = F(0)
            for i in range(1, n):
                oldd = p + z
                e0 += unary[i][0] + min(0, oldd + b[i])
                z = min(max(z, -b[i] - p), a[i] - p)
                p += unary[i][1] - unary[i][0]
            predicted = e0 + min(0, p + z)
            actual = min(sum(unary[i][x[i]] for i in range(n)) +
                         sum(a[i] * (x[i - 1] == 0 and x[i] == 1) +
                             b[i] * (x[i - 1] == 1 and x[i] == 0)
                             for i in range(1, n))
                         for x in product([0, 1], repeat=n))
            assert predicted == actual
            total += 1
    counts['signed_unary_clamp_instances'] = total


def round_generator(m, r, c):
    s = sum(r)
    if not s:
        b = [1] * m + [0] * m
        return [[F(b[i] * b[j], m) for j in range(2 * m)]
                for i in range(2 * m)]
    a = [int(x >= F(1, 2)) for x in r]
    for i in range(m):
        if a[i] == a[m + i]:
            a[i], a[m + i] = 1, 0
    return [[F(a[i] * a[j], m) for j in range(2 * m)] for i in range(2 * m)]


def conic():
    total = 0
    for m in range(1, 6):
        for _ in range(100):
            matrices, repairs = [], []
            for _ in range(3):
                r = [F(rng.randrange(11), 10) for _ in range(2 * m)]
                c = list(r)
                # Redistribute column margins to test unequal margins at
                # identical totals, including zeros and unit boundary entries.
                for _ in range(20):
                    i, j = rng.sample(range(2 * m), 2)
                    shift = min(c[i], 1 - c[j], F(rng.randrange(11), 10))
                    c[i] -= shift
                    c[j] += shift
                s = sum(r)
                matrices.append([[r[i] * c[j] / s if s else F(0)
                                  for j in range(2 * m)] for i in range(2 * m)])
                repairs.append(round_generator(m, r, c))
            weights = [F(1, 7), F(2, 7), F(4, 7)]
            w = [[sum(l * a[i][j] for l, a in zip(weights, matrices))
                  for j in range(2 * m)] for i in range(2 * m)]
            v = [[sum(l * a[i][j] for l, a in zip(weights, repairs))
                  for j in range(2 * m)] for i in range(2 * m)]
            mass = sum(map(sum, w))
            d = 1 - sum(w[i][i] for i in range(2 * m))
            b = sum(w[i][m + i] for i in range(m))
            assert mass <= m + 2 * m * b + 4 * m * d
            distance = sum(abs(w[i][j] - v[i][j])
                           for i in range(2 * m) for j in range(2 * m))
            assert distance <= 28 * m * b + 156 * m * d + 5 * (m - mass)
            assert sum(map(sum, v)) == m
            assert sum(v[i][i] for i in range(2 * m)) == 1
            assert sum(v[i][m + i] for i in range(m)) == 0
            total += 1
    counts['unequal_margin_mixture_face_repairs'] = total


def transformed_outlets():
    total = 0
    for _ in range(1000):
        q = F(rng.randrange(1, 20), 20)
        z0, z1, v = [F(rng.randrange(21), 10) for _ in range(3)]
        demand = z0 + z1 + v
        if not demand:
            continue
        target = (z1 + q * v) / demand
        w0, w1 = -q * z0, (1 - q) * z1
        assert w0 + w1 == demand * (target - q)
        assert w0 == q * demand * (target - 1) + q * (1 - q) * v
        for cap in [F(0), v, v + 1]:
            assert (v <= cap) == (w0 <= q * demand * (target - 1) + cap * q * (1 - q))
        # The general distinct-quality formula is checked on both sides of
        # every source quality, including negative transformed flow.
        c1, c2 = F(-2), F(3)
        qq = F(rng.choice([-5, -1, 0, 1, 2, 4, 7]), 1)
        g1, g2 = c1 - qq, c2 - qq
        mass = z0 + z1
        residual = g1 * z0 + g2 * z1
        assert g1 * z0 == g1 * (residual - g2 * mass) / (c1 - c2)
        total += 1
    counts['physical_signed_outlet_identities'] = total


if __name__ == '__main__':
    signed_support()
    clamp()
    conic()
    transformed_outlets()
    print(json.dumps({'status': 'PASS', 'seed': 9032026, 'checks': counts}, indent=2))
