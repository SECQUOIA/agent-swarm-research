"""Finite exact checks for review 07; no claim of universal verification."""
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import json


def check(n, weights):
    edges = [(i, j, a) for (i, j), a in zip(combinations(range(n), 2), weights) if a]
    signs = list(product((-1, 1), repeat=n))
    values = [sum(a * s[i] * s[j] for i, j, a in edges) for s in signs]
    cut_range = Fraction(max(values) - min(values), 2)
    mass = sum(abs(a) for _, _, a in edges)
    # Independently optimize the rectangular form by choosing row signs last.
    rectangular = 0
    bipartitions = []
    density = Fraction(0)
    for mask in range(1 << n):
        side = {i for i in range(n) if mask >> i & 1}
        if side:
            density = max(density, Fraction(sum(i in side and j in side for i, j, _ in edges), len(side)))
        if all((i in side) != (j in side) for i, j, _ in edges):
            bipartitions.append(side)
        for s in signs:
            total = 0
            for i in side:
                total += abs(sum(a * s[v] for u, v, a in edges if u == i and v not in side)
                             + sum(a * s[u] for u, v, a in edges if v == i and u not in side))
            rectangular = max(rectangular, total)
    assert rectangular == cut_range
    if not edges:
        assert cut_range == 0
        return
    assert 0 < cut_range <= mass
    degrees = [sum(i in (u, v) for u, v, _ in edges) for i in range(n)]
    assert mass**2 <= 16 * density * cut_range**2
    assert mass**2 <= 4 * max(degrees) * cut_range**2
    for side in bipartitions:
        max_p = max((degrees[i] for i in side), default=0)
        max_q = max((degrees[i] for i in range(n) if i not in side), default=0)
        assert mass**2 <= 2 * min(max_p, max_q) * cut_range**2
    # Exactness checked against realizability of the two prescribed edge cuts.
    plus = any(all((s[i] != s[j]) == (a > 0) for i, j, a in edges) for s in signs)
    minus = any(all((s[i] != s[j]) == (a < 0) for i, j, a in edges) for s in signs)
    assert (cut_range == mass) == (plus and minus)


counts = {}
for n in range(1, 5):
    count = 0
    for weights in product((-1, 0, 1), repeat=n * (n - 1) // 2):
        check(n, weights)
        count += 1
    counts[n] = count
result = {"arithmetic": "exact integers and fractions", "ternary_weight_vectors_by_n": counts,
          "checks": ["cut polarization", "zero support", "density upper bound", "degree upper bound",
                     "bipartite degree bound", "two-cut exactness criterion"],
          "limit": "Only n <= 4 and weights in {-1,0,1}; does not prove universal claims."}
Path(__file__).with_name("result.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
