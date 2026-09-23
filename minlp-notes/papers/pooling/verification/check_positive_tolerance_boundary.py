"""Exact K4 witnesses showing loss of integral optimality at positive tolerance.

All capacities are one and all four layer degrees are exactly two. The script
checks original physical constraints and enumerates every integral routing.
The manuscript supplies the argument for every delta in (0,1/2].
"""
from fractions import Fraction as F
from itertools import product

E1 = [(0, 1), (2, 3)]
E2 = [(0, 2), (1, 3)]
E3 = [(0, 3), (1, 2)]


def feasible(flows, delta):
    for a, d, s, b in flows:
        if min(a, d, s, b) < 0 or a + d != s + b or a + d > 1:
            return False
    for u, v in E1:
        if flows[u][0] + flows[v][0] > 1:
            return False
    for u, v in E3:
        if flows[u][1] + flows[v][1] > 1 or flows[u][3] + flows[v][3] > 1:
            return False
    for u, v in E2:
        volume = flows[u][2] + flows[v][2]
        mass = F(0)
        for w in (u, v):
            a, d, s, b = flows[w]
            if a + d:
                mass += F(d, a + d) * s
        if volume > 1 or mass > delta * volume:
            return False
    return True


def profit(flows):
    original_cost = sum(a - 2*s - b for a, d, s, b in flows)
    value = sum(s + d for a, d, s, b in flows)
    assert value == -original_cost
    return value


# With integral flows and unit pool capacity these are all possible routings.
modes = [(0, 0, 0, 0), (1, 0, 1, 0), (1, 0, 0, 1), (0, 1, 1, 0), (0, 1, 0, 1)]
for k in range(1, 13):
    delta = F(1, 2**k)
    witness = [(1-delta, delta, 1, 0), (0, 1, 0, 1),
               (0, 0, 0, 0), (1-delta, delta, 1, 0)]
    assert feasible(witness, delta)
    assert profit(witness) == 3 + 2*delta
    best_integral = max(profit(f) for f in product(modes, repeat=4) if feasible(f, delta))
    assert best_integral == 3 < profit(witness)
print('PASS: 12 exact positive-tolerance witnesses and exhaustive integral routing comparisons on K4')
