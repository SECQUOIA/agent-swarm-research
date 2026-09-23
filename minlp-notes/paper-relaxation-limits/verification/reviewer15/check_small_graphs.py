"""Exact finite corroboration; this does not prove universal graph bounds."""
from fractions import Fraction
from itertools import combinations, product

n = 4
edges = list(combinations(range(n), 2))
signs = list(product((-1, 1), repeat=n))
subsets = [set(i for i in range(n) if mask >> i & 1) for mask in range(1 << n)]
count = bipartite_count = 0
for coefficients in product((-1, 0, 1), repeat=len(edges)):
    weighted = [(i, j, a) for (i, j), a in zip(edges, coefficients) if a]
    q = [sum(a * s[i] * s[j] for i, j, a in weighted) for s in signs]
    radius = Fraction(max(q) - min(q), 2)
    polarized = max(
        sum(a * s[i] * s[j] for i, j, a in weighted if (i in side) != (j in side))
        for side in subsets for s in signs
    )
    assert radius == polarized
    length = len(weighted)
    density = max(Fraction(sum(i in side and j in side for i, j, _ in weighted), len(side))
                  for side in subsets if side)
    degree = [sum(i == k or j == k for i, j, _ in weighted) for k in range(n)]
    assert length**2 <= 16 * density * radius**2
    assert length**2 <= 4 * max(degree) * radius**2
    partitions = [side for side in subsets if all((i in side) != (j in side) for i, j, _ in weighted)]
    if length and partitions:
        side = partitions[0]
        part_degree = min(max(degree[i] for i in side), max(degree[i] for i in range(n) if i not in side))
        assert length**2 <= 2 * part_degree * radius**2
        bipartite_count += 1
    if coefficients == (1, 0, -1, 1, 0, 1):
        assert (length, radius, density) == (4, 2, 1)
    count += 1
print(f"PASS: {count} ternary coefficient vectors on K4; {bipartite_count} nonempty bipartite supports. All arithmetic exact.")
