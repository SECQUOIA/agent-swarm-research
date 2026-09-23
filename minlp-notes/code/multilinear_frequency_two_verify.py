"""Check the frequency-two gap bound against full binary-distribution LPs.

This verifier computes the exact finite LP formulation in floating point; it
does not implement the matching-rounding proof. Parallel graph edges and
single-incidence variables are included in the random cases.
"""

from fractions import Fraction
from itertools import combinations, permutations
import random

import numpy as np
from scipy.optimize import linprog


def odd_girth(n, edges):
    adjacency = [set() for _ in range(n)]
    for u, v in edges:
        if v is not None:
            adjacency[u].add(v)
            adjacency[v].add(u)
    for length in range(3, n + 1, 2):
        for subset in combinations(range(n), length):
            first, *rest = subset
            for tail in permutations(rest):
                cycle = (first,) + tail
                if all(cycle[(i + 1) % length] in adjacency[cycle[i]]
                       for i in range(length)):
                    return length
    return None


def exact_distribution_lp(n, edges, failures, weights):
    edge_count = len(edges)
    states = np.arange(1 << edge_count, dtype=np.uint64)
    selected = ((states[:, None] >> np.arange(edge_count, dtype=np.uint64)) & 1)
    incident = [[i for i, edge in enumerate(edges) if v in edge] for v in range(n)]
    coverage = np.column_stack([np.any(selected[:, ids], axis=1) for ids in incident])
    objective = coverage @ np.asarray(weights, dtype=float)
    equalities = np.vstack([np.ones(len(states)), selected.T])
    target = np.array([1.0] + list(map(float, failures)))
    result = linprog(-objective, A_eq=equalities, b_eq=target,
                     bounds=(0, None), method="highs")
    assert result.success, result.message
    baseline = sum(weights[v] * max((failures[i] for i in ids), default=Fraction(0))
                   for v, ids in enumerate(incident))
    termwise = sum(weights[v] * (
        min(Fraction(1), sum((failures[i] for i in ids), Fraction(0)))
        - max((failures[i] for i in ids), default=Fraction(0)))
        for v, ids in enumerate(incident))
    hull = -result.fun - float(baseline)
    return termwise, hull


def main():
    rng = random.Random(26090422)
    tested = 0
    max_ratio = 1.0
    bipartite_count = 0
    while tested < 200:
        n = rng.randrange(2, 7)
        edge_count = rng.randrange(4, 12)
        edges = []
        for _ in range(edge_count):
            u = rng.randrange(n)
            v = None if rng.random() < 0.2 else rng.choice([j for j in range(n) if j != u])
            edges.append((u, v))
        if any(sum(v in edge for edge in edges) < 2 for v in range(n)):
            continue
        failures = [Fraction(rng.randrange(11), 10) for _ in edges]
        weights = [rng.randrange(1, 10) for _ in range(n)]
        termwise, hull = exact_distribution_lp(n, edges, failures, weights)
        girth = odd_girth(n, edges)
        factor = 1.0 if girth is None else girth / (girth - 1)
        tolerance = 1e-8 * max(1, float(termwise))
        assert float(termwise) <= factor * hull + tolerance, (
            edges, failures, weights, girth, termwise, hull)
        if girth is None:
            bipartite_count += 1
            assert abs(float(termwise) - hull) <= tolerance
        if hull > tolerance:
            max_ratio = max(max_ratio, float(termwise) / hull)
        tested += 1

    for length in (3, 5, 7, 9):
        edges = [(i, (i + 1) % length) for i in range(length)]
        termwise, hull = exact_distribution_lp(
            length, edges, [Fraction(1, 2)] * length, [1] * length)
        assert termwise == Fraction(length, 2)
        assert abs(hull - (length - 1) / 2) < 1e-8

    print(f"Passed {tested} full-distribution LP comparisons; "
          f"{bipartite_count} bipartite cases were exact.")
    print(f"Largest random gap ratio: {max_ratio:.12g}.")
    print("Sharp odd-cycle ratios checked for lengths 3, 5, 7, and 9.")
    print("Termwise baselines use rational arithmetic; HiGHS envelope solves use floating point.")


if __name__ == "__main__":
    main()
