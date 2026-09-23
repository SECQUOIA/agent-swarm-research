"""Independent vertex-LP checks for the convex-cardinality factor gap theorem.

Exact rational arithmetic checks local envelope values and odd-cycle rounding.
Full hull comparisons use floating-point HiGHS and are numerical corroboration,
not proof certificates. Run with Python, NumPy, and SciPy installed.
"""

from collections import deque
from fractions import Fraction as Q

import numpy as np
from scipy.optimize import linprog


def interpolate(phi, value):
    k = value.numerator // value.denominator
    if k == len(phi) - 1:
        return phi[k]
    return phi[k] + (value - k) * (phi[k + 1] - phi[k])


def upper(phi, means):
    breaks = sorted(set([Q(0), Q(1), *means]))
    return sum(
        (right - left) * phi[sum(p > left for p in means)]
        for left, right in zip(breaks, breaks[1:])
    )


def odd_girth(vertex_count, edges):
    adjacency = [set() for _ in range(vertex_count)]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    best = float("inf")
    for root in range(vertex_count):
        distances = {(root, 0): 0}
        queue = deque([(root, 0)])
        while queue:
            node, parity = queue.popleft()
            for neighbor in adjacency[node]:
                state = (neighbor, 1 - parity)
                if state not in distances:
                    distances[state] = distances[(node, parity)] + 1
                    queue.append(state)
        best = min(best, distances.get((root, 1), float("inf")))
    return best


def check_cycle_rounding():
    checks = 0
    for length in [3, 5, 7, 9, 11]:
        laws = []
        for missing in range(length):
            matching = {(missing + j) % length for j in range(1, length, 2)}
            laws.extend([matching, set(range(length)) - matching])
        assert all(sum(e in state for state in laws) == length for e in range(length))
        for m in range(5):
            # Nonmonotone discrete-convex sequence, with nonconstant curvatures.
            phi = [Q(k**3 - 7 * k + 3, 5) for k in range(m + 3)]
            curvature_gap = (phi[m] + phi[m + 2]) / 2 - phi[m + 1]
            for vertex in range(length):
                actual = sum(
                    phi[m + int(vertex in state) + int((vertex - 1) % length in state)]
                    for state in laws
                ) / len(laws)
                assert actual == phi[m + 1] + curvature_gap / length
                checks += 1
    return checks


def check_full_hulls(samples=240):
    rng = np.random.default_rng(40492026)
    bipartite = 0
    maximum_ratio = 1.0
    for sample in range(samples):
        n = int(rng.integers(3, 10))
        factors = int(rng.integers(2, 6))
        supports = [[] for _ in range(factors)]
        edges = []
        vertices = factors
        for coordinate in range(n):
            a = int(rng.integers(factors))
            if rng.random() < 0.3:
                b = vertices
                vertices += 1
            else:
                choices = [v for v in range(factors) if v != a]
                b = int(rng.choice(choices))
                supports[b].append(coordinate)
            supports[a].append(coordinate)
            edges.append((a, b))
        p = [Q(int(rng.integers(0, 9)), 8) for _ in range(n)]
        sequences = []
        for support in supports:
            # Distinct convex sequences can have negative entries and slopes.
            slopes = sorted(int(v) for v in rng.integers(-9, 10, len(support)))
            phi = [Q(int(rng.integers(-5, 6)), 3)]
            for slope in slopes:
                phi.append(phi[-1] + Q(slope, 3))
            sequences.append(phi)
        local_lower = sum(
            interpolate(phi, sum((p[i] for i in support), Q(0)))
            for phi, support in zip(sequences, supports)
        )
        local_upper = sum(
            upper(phi, [p[i] for i in support])
            for phi, support in zip(sequences, supports)
        )
        states = ((np.arange(2**n)[:, None] >> np.arange(n)) & 1).astype(int)
        values = np.array([
            float(sum(phi[int(state[support].sum())]
                      for phi, support in zip(sequences, supports)))
            for state in states
        ])
        equality = np.vstack([np.ones(2**n), states.T])
        rhs = np.array([1.0, *map(float, p)])
        low = linprog(values, A_eq=equality, b_eq=rhs, bounds=(0, None), method="highs")
        high = linprog(-values, A_eq=equality, b_eq=rhs, bounds=(0, None), method="highs")
        assert low.success and high.success, (sample, low.message, high.message)
        tolerance = 1e-7 * (1 + max(abs(values)))
        assert abs(-high.fun - float(local_upper)) <= tolerance, sample
        term_gap = float(local_upper - local_lower)
        hull_gap = -high.fun - low.fun
        girth = odd_girth(vertices, edges)
        factor = 1 if girth == float("inf") else 1 - 1 / girth
        assert hull_gap + tolerance >= factor * term_gap, sample
        if girth == float("inf"):
            bipartite += 1
            assert abs(hull_gap - term_gap) <= tolerance, sample
        if hull_gap > tolerance:
            maximum_ratio = max(maximum_ratio, term_gap / hull_gap)
    return samples, bipartite, maximum_ratio


if __name__ == "__main__":
    print("Exact cycle curvature checks:", check_cycle_rounding())
    samples, bipartite, ratio = check_full_hulls()
    print("Full vertex-LP samples:", samples)
    print("Bipartite equality samples:", bipartite)
    print("Largest sampled ratio:", ratio)
