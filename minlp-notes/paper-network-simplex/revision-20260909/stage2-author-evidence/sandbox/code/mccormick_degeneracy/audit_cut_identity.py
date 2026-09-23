"""Independent finite checks of polarization and the squared-weight local-cut bound.

This is supporting evidence, not a replacement for the mathematical proof.
Run: python code/mccormick_degeneracy/audit_cut_identity.py
"""
from itertools import product
from math import isclose, sqrt
from random import Random


def verify(n, edges):
    adjacency = [[0.0] * n for _ in range(n)]
    for i, j, weight in edges:
        adjacency[i][j] = adjacency[j][i] = weight
    cuts = list(product((0, 1), repeat=n))
    cut_values = [sum(w for i, j, w in edges if side[i] != side[j]) for side in cuts]
    cut_range = max(cut_values) - min(cut_values)
    block_max = 0.0
    for side in cuts:
        rows = [i for i in range(n) if side[i]]
        columns = [i for i in range(n) if not side[i]]
        for signs in product((-1, 1), repeat=len(columns)):
            block_max = max(block_max, sum(abs(sum(adjacency[i][j] * sign
                for j, sign in zip(columns, signs))) for i in rows))
    assert isclose(cut_range, block_max, abs_tol=1e-9), (n, edges, cut_range, block_max)
    best_side = max(cuts, key=lambda side: sum(w * w for i, j, w in edges if side[i] != side[j]))
    row_sum = 0.0
    for i in range(n):
        total = sum(w * w for w in adjacency[i])
        crossing = sum(adjacency[i][j] ** 2 for j in range(n) if best_side[i] != best_side[j])
        assert 2 * crossing >= total - 1e-9
        row_sum += sqrt(total)
    assert cut_range >= row_sum / 4 - 1e-9, (n, edges, cut_range, row_sum)
    # Density of the nonzero support: enumerate every induced subgraph independently.
    density = 0.0
    for side in cuts:
        vertices = sum(side)
        if vertices:
            count = sum(1 for i, j, w in edges if w and side[i] and side[j])
            density = max(density, count / vertices)
    edge_l1 = sum(abs(w) for _, _, w in edges)
    assert edge_l1 <= 4 * sqrt(density) * cut_range + 1e-9
    return cut_range


cases = [(0, []), (1, []), (4, []), (3, [(0, 1, 0.0)]),
         (2, [(0, 1, -7)]),
         (4, [(0, 1, 1), (1, 2, 1), (2, 3, 1), (0, 3, -1)])]
for n, edges in cases:
    verify(n, edges)
assert verify(*cases[-1]) == 2
rng = Random(916)
for _ in range(240):
    n = rng.randint(2, 7)
    edges = [(i, j, rng.choice([-3, -1, 0, 0.25, 1, 2]))
             for i in range(n) for j in range(i + 1, n) if rng.random() < 0.6]
    verify(n, edges)
print('Polarization identity, row-norm bound, and density bound passed 6 boundary cases and 240 seeded weighted graphs.')
