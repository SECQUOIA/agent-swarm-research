"""Independent exhaustive-branch audit of the original continuous flow model.

The LPs retain clean-to-lax waste and mixed clean/dirty intakes. The exact
quality disjunction at each pool is dirty intake = 0 OR strict outflow = 0.
Thus enumerating all branches tests the original formulation, rather than
assuming the candidate's pure-mode or integral replacement conclusions.
"""

from itertools import product
from random import Random

import numpy as np
from scipy.optimize import linprog


def matchings(vertices):
    if not vertices:
        yield ()
        return
    u, *rest = vertices
    for v in rest:
        for tail in matchings([w for w in rest if w != v]):
            yield ((u, v),) + tail


def independence_number(n, edges):
    masks = [(1 << u) | (1 << v) for u, v in edges]
    return max(
        s.bit_count()
        for s in range(1 << n)
        if all(s & edge != edge for edge in masks)
    )


def audit(n, colors, relax=False):
    # Block variables: clean a, dirty d, strict s, lax b.
    objective = np.tile([0.0], 4 * n)
    objective[0:n] = 1
    objective[2 * n:3 * n] = -2
    objective[3 * n:4 * n] = -1
    equalities = np.zeros((n, 4 * n))
    for v in range(n):
        equalities[v, [v, n + v, 2 * n + v, 3 * n + v]] = [1, 1, -1, -1]
    capacities = []
    for block, matching in zip([0, 2, 1], colors):
        for u, v in matching:
            row = np.zeros(4 * n)
            row[block * n + u] = row[block * n + v] = 1
            capacities.append(row)
    for v in range(n):
        row = np.zeros(4 * n)
        row[[v, n + v]] = 1
        capacities.append(row)
    capacities = np.array(capacities)
    best, branches = -float("inf"), 0
    for modes in ([None] if relax else product([0, 1], repeat=n)):
        bounds = [(0, 1)] * (4 * n)
        if modes is not None:
            for v, mode in enumerate(modes):
                bounds[(1 if mode == 0 else 2) * n + v] = (0, 0)
        solution = linprog(
            objective,
            A_ub=capacities,
            b_ub=np.ones(len(capacities)),
            A_eq=equalities,
            b_eq=np.zeros(n),
            bounds=bounds,
            method="highs",
        )
        assert solution.success, solution.message
        branches += 1
        best = max(best, -solution.fun)
        if modes is None:
            continue
        a, d, s, b = solution.x.reshape(4, n)
        p = np.divide(d, a + d, out=np.zeros(n), where=a + d > 0)
        assert max(abs(p * (a + d) - d)) < 1e-8
        assert max(abs(p * s)) < 1e-8
        # Directly check the candidate's deletion map on the original LP point.
        normalized = np.concatenate([s, d, s, d])
        assert np.max(capacities @ normalized) <= 1 + 1e-8
        assert np.max(abs(equalities @ normalized)) < 1e-8
        assert abs(objective @ normalized - solution.fun) < 1e-8
    return best, branches


def main():
    instances = []
    for n in [4, 6]:
        first = tuple((v, v + 1) for v in range(0, n, 2))
        candidates = list(matchings(list(range(n))))
        for second, third in product(candidates, repeat=2):
            if len(set(first + second + third)) == 3 * n // 2:
                instances.append((n, (first, second, third)))
    random = Random(93517)
    n = 8
    candidates = list(matchings(list(range(n))))
    samples = set()
    while len(samples) < 12:
        colors = tuple(random.sample(candidates, 3))
        if len(set(sum(colors, ()))) == 3 * n // 2:
            samples.add(colors)
    instances.extend((n, colors) for colors in sorted(samples))
    branch_total = 0
    for n, colors in instances:
        alpha = independence_number(n, sum(colors, ()))
        optimum, branches = audit(n, colors)
        assert abs(optimum - (n // 2 + alpha)) < 1e-8, (n, colors, optimum, alpha)
        branch_total += branches
    n, colors = instances[0]
    relaxed, _ = audit(n, colors, relax=True)
    exact = n // 2 + independence_number(n, sum(colors, ()))
    assert relaxed > exact + 0.5
    print(f"PASS: {len(instances)} graph/coloring instances; {branch_total} original-flow LP branches.")
    print("Includes all colorings at n=4,6 with first matching fixed, plus 12 seeded n=8 instances.")
    print(f"Negative control K4: dropping quality disjunction gives {relaxed:g}, true optimum {exact}.")
    print("Every branch checked original pool quality, deletion feasibility, and exact profit preservation (tolerance 1e-8).")


if __name__ == "__main__":
    main()
