#!/usr/bin/env python3
"""Exact finite challenges to the count, partition, and parameter-net claims.

This is an exhaustive-support test oracle, not the spectral grid algorithm.
Only Python's standard library is used. No files are written.
"""

from fractions import Fraction as F
from heapq import heappop, heappush
from itertools import combinations, product
from random import Random


def enumerate_near(cost, epsilon, delta):
    """Use the worst admissible oracle answer; verify the cell invariant."""
    m = len(next(iter(cost)))
    heap, outputs, calls, serial = [], [], 0, 0

    def members(p):
        return {z for z in cost if all(a is None or z[i] == a
                                      for i, a in enumerate(p))}

    def query(p):
        nonlocal calls, serial
        calls += 1
        feasible = members(p)
        if not feasible:
            return None
        best = min(cost[z] for z in feasible)
        z = max((z for z in feasible if cost[z] <= best + epsilon),
                key=lambda z: (cost[z], z))
        serial += 1
        heappush(heap, (cost[z] - epsilon, serial, p, z))
        return cost[z]

    upper = query((None,) * m)
    while heap and heap[0][0] <= upper + delta:
        _, _, p, z = heappop(heap)
        assert z not in outputs
        outputs.append(z)
        prefix = list(p)
        for j, value in enumerate(p):
            if value is None:
                child = prefix.copy()
                child[j] = 1 - z[j]
                query(tuple(child))
                prefix[j] = z[j]
        remaining = set(cost) - set(outputs)
        cells = [members(item[2]) for item in heap]
        assert sum(map(len, cells)) == len(remaining)
        assert set().union(*cells) == remaining
    best = min(cost.values())
    assert {z for z in cost if cost[z] <= best + delta} <= set(outputs)
    assert all(cost[z] <= best + delta + 2 * epsilon for z in outputs)
    assert calls <= 1 + m * len(outputs)
    return set(outputs), calls


def check_count():
    cases = outcomes = informative = tied_outcomes = 0
    for m in range(1, 4):
        cube = list(product((0, 1), repeat=m))
        # All families in dimensions <= 2; selected sizes and all label
        # choices in dimension 3, including the complete cube.
        sizes = range(1, len(cube) + 1) if m < 3 else (1, 2, 3, 4, 8)
        for size in sizes:
            for family in combinations(cube, size):
                offset_tables = (
                    {z: F(sum((i + 1) * a for i, a in enumerate(z))
                          - 3 * z[0] * z[-1], 7) for z in family},
                    {z: F(sum(z) + 2 * z[0] * z[-1]) for z in family},
                )
                for offsets in offset_tables:
                    for grid in ((F(-1), F(1)), (F(-1), F(0), F(1))):
                        totals = {a: 0 for a in (F(0), F(1, 7), F(2, 3))}
                        for xi in product(grid, repeat=m):
                            cost = {z: offsets[z] + sum(x * a for x, a in zip(xi, z))
                                    for z in family}
                            best = min(cost.values())
                            tied_outcomes += sum(v == best for v in cost.values()) > 1
                            for a in totals:
                                totals[a] += sum(v <= best + a for v in cost.values())
                            outcomes += 1
                        for a, count in totals.items():
                            expected = F(count, len(grid) ** m)
                            bound = (1 + a + F(1, len(grid))) ** m
                            assert expected <= bound
                            informative += bound < len(family)
                            cases += 1
    assert informative > 0 and tied_outcomes > 0
    return cases, outcomes, informative, tied_outcomes


def check_tight_atomic_count():
    """g(z)=sum(z), xi in {-1,1}: exact equality in the atomic bound."""
    for m in range(1, 5):
        cube = list(product((0, 1), repeat=m))
        total = 0
        for xi in product((-1, 1), repeat=m):
            costs = [sum(z) + sum(x * a for x, a in zip(xi, z)) for z in cube]
            total += sum(v == min(costs) for v in costs)
        expected = F(total, 2 ** m)
        assert expected == F(3, 2) ** m  # In particular, 3/2 for m=1.
        assert expected < len(cube)
    return 4


def check_noisy_dictionary():
    """Q=1,c=0,lambda=-5/6,xi=1: recovery must use noisy constants."""
    q = {(0,): F(0), (1,): F(-5, 6)}
    noisy = {z: value + z[0] for z, value in q.items()}
    dictionary, _ = enumerate_near(noisy, F(1, 6), F(1, 6))
    assert dictionary == set(q)
    assert min(dictionary, key=noisy.get) == (0,)
    assert min(dictionary, key=q.get) == (1,)
    assert min(noisy[z] for z in dictionary) == 0


def active_affine(branches, radius=F(1)):
    active = set()
    for z, (slope, offset) in branches.items():
        lo, hi = -radius, radius
        for a, b in branches.values():
            d, rhs = slope - a, b - offset
            if d > 0:
                hi = min(hi, rhs / d)
            elif d < 0:
                lo = max(lo, rhs / d)
            elif rhs < 0:
                lo, hi = F(1), F(0)
        if lo <= hi:
            active.add(z)
    return active


def check_enumeration_and_net():
    rng = Random(70927)
    calls = points = runs = 0
    families = [{(0, 0): (F(-1), F(0)),
                 (0, 1): (F(0), F(0)),
                 (1, 0): (F(1), F(0))}]
    assert (0, 1) in active_affine(families[0])  # Active only at t = 0.
    for _ in range(45):
        m = rng.randrange(1, 6)
        cube = list(product((0, 1), repeat=m))
        family = rng.sample(cube, rng.randrange(1, len(cube) + 1))
        families.append({z: (F(rng.randrange(-3, 4), 3),
                              F(rng.randrange(-5, 6), 7)) for z in family})
    for branches in families:
        epsilon = F(1, 6)
        lipschitz = max(abs(a) for a, _ in branches.values())
        h = max(1, -(-2 * lipschitz // epsilon))
        found = set()
        for j in range(h):
            t = -1 + F(2 * j + 1, h)
            cost = {z: a * t + b for z, (a, b) in branches.items()}
            emitted, used = enumerate_near(cost, epsilon, epsilon)
            found.update(emitted)
            calls += used
            points += 1
        assert active_affine(branches) <= found
        runs += 1
    return runs, points, calls


if __name__ == "__main__":
    cases, outcomes, informative, tied_outcomes = check_count()
    tight = check_tight_atomic_count()
    check_noisy_dictionary()
    runs, points, calls = check_enumeration_and_net()
    print(f"PASS: {cases} exact count bounds over {outcomes} noise outcomes "
          f"({informative} bounds below family size; {tied_outcomes} tied outcomes); "
          f"{tight} tight atomic equalities; noisy-constant recovery regression; "
          f"{runs} affine families, {points} net points, {calls} oracle calls.")
