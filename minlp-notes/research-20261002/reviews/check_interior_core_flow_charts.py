"""Small cyclic-network chart certificates, checked with exact fractions.

This enumerates a tiny fixture's labels for independent verification;
the theorem's ordinary algorithm does not enumerate labels.
"""

from fractions import Fraction as Q
from itertools import product
from random import Random

ZERO = (Q(0), Q(0), Q(0))
ARCS = [(0, 1), (1, 2), (0, 2), (1, 0), (2, 1)]
NODES, SOURCE = 3, 3


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(a, t):
    return tuple(t * x for x in a)


def value(a, t):
    return a[0] + t * (a[1] + t * a[2])


def minimum(a, lo, hi):
    vals = [value(a, lo), value(a, hi)]
    if a[2] > 0:
        stationary = -a[1] / (2 * a[2])
        if lo <= stationary <= hi:
            vals.append(value(a, stationary))
    return min(vals)


def feasible(z):
    balances = [0] * NODES
    for (u, v), amount in zip(ARCS, z):
        balances[u] += amount
        balances[v] -= amount
    return balances == [1, 0, -1]


LABELS = [z for z in product(range(3), repeat=len(ARCS)) if feasible(z)]


def objective(costs, z):
    ans = ZERO
    for (quadratic, linear), amount in zip(costs, z):
        ans = add(ans, add(scale(quadratic, amount**2), scale(linear, amount)))
    return ans


def residual(costs, z):
    edges = []
    for (u, v), (a, b), amount in zip(ARCS, costs, z):
        if amount < 2:
            edges.append((u, v, add(scale(a, 2 * amount + 1), b)))
        if amount > 0:
            edges.append((v, u, add(scale(a, 1 - 2 * amount), scale(b, -1))))
    return edges + [(SOURCE, node, ZERO) for node in range(NODES)]


def chart(edges, at):
    distances = [None] * (NODES + 1)
    distances[SOURCE] = Q(0)
    for _ in range(NODES):
        for u, v, cost in edges:
            if distances[u] is None:
                continue
            cand = distances[u] + value(cost, at)
            if distances[v] is None or cand < distances[v]:
                distances[v] = cand
    assert all(x is not None for x in distances)
    assert all(distances[v] <= distances[u] + value(c, at) for u, v, c in edges)

    # Search the tight-edge graph, rather than retaining Bellman-Ford
    # predecessors, so even all-zero cycles cannot create a predecessor cycle.
    potentials = {SOURCE: ZERO}
    queue = [SOURCE]
    for u in queue:
        for tail, v, cost in edges:
            if tail == u and v not in potentials and distances[v] == distances[u] + value(cost, at):
                potentials[v] = add(potentials[u], cost)
                queue.append(v)
    assert len(potentials) == NODES + 1
    assert all(value(potentials[v], at) == distances[v] for v in potentials)
    reduced = [add(c, add(potentials[u], scale(potentials[v], -1))) for u, v, c in edges]
    assert all(value(c, at) >= 0 for c in reduced)
    return reduced


def run():
    rng = Random(20261002)
    queries = accepted = comparisons = identities = tied = 0
    for fixture in range(41):
        if fixture == 0:
            costs = [(ZERO, ZERO) for _ in ARCS]
        else:
            costs = [((Q(rng.randrange(3)), Q(0), Q(rng.randrange(3))),
                      tuple(Q(rng.randrange(-3, 4)) for _ in range(3))) for _ in ARCS]
        slices = {z: objective(costs, z) for z in LABELS}
        for at in [Q(0), Q(1, 4), Q(1, 2), Q(3, 4), Q(1)]:
            best = min(value(p, at) for p in slices.values())
            winners = [z for z, p in slices.items() if value(p, at) == best]
            tied += len(winners) > 1
            z = min(winners)
            reduced = chart(residual(costs, z), at)
            queries += 1
            identities += sum(p == ZERO for p in reduced)
            lo, hi = max(Q(0), at-Q(1, 8)), min(Q(1), at+Q(1, 8))
            if all(minimum(p, lo, hi) >= 0 for p in reduced):
                accepted += 1
                for w in LABELS:
                    diff = add(slices[w], scale(slices[z], -1))
                    assert minimum(diff, lo, hi) >= 0
                    comparisons += 1
            if fixture == 0:
                assert all(p == ZERO for p in reduced)
                assert len(winners) == len(LABELS)
    assert accepted > 50 and tied > 5 and identities > queries
    print(f"PASS: {len(LABELS)} feasible fixture labels; {queries} cyclic-network charts; "
          f"{accepted} uniform interval certificates; {comparisons} exact competing-label "
          f"interval checks; {identities} identity reduced costs; {tied} tied query optima")


if __name__ == "__main__":
    run()
