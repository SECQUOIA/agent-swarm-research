"""Independent graph enumeration and symbolic contacts for the cube review.

This enumerates graph automorphisms directly, rather than assuming the signed
coordinate permutation description used by the author's finite checker.
It does not prove the analytic perturbation argument or establish novelty.
"""
from itertools import combinations, permutations

import sympy as sp


# Literal endpoint table in the note, with binary vertices encoded as integers.
edges = [(0, 4), (0, 2), (0, 1), (1, 5), (1, 3), (2, 6),
         (2, 3), (3, 7), (4, 6), (4, 5), (5, 7), (6, 7)]
edge_sets = {frozenset(e) for e in edges}
edge_index = {frozenset(e): i for i, e in enumerate(edges)}
automorphisms = [p for p in permutations(range(8))
                 if all(frozenset((p[a], p[b])) in edge_sets for a, b in edges)]
assert len(automorphisms) == 48
maps = [[edge_index[frozenset((p[a], p[b]))] for a, b in edges]
        for p in automorphisms]
representatives = sorted({min(tuple(sorted(f[i] for i in subset)) for f in maps)
                          for subset in combinations(range(12), 5)})
expected = [
    (0, 1, 2, 3, 4), (0, 1, 2, 3, 5), (0, 1, 2, 3, 6), (0, 1, 2, 3, 7),
    (0, 1, 2, 3, 9), (0, 1, 2, 3, 10), (0, 1, 2, 3, 11), (0, 1, 2, 7, 10),
    (0, 1, 3, 4, 5), (0, 1, 3, 4, 6), (0, 1, 3, 4, 11), (0, 1, 3, 5, 7),
    (0, 1, 3, 5, 8), (0, 1, 3, 5, 9), (0, 1, 3, 5, 10), (0, 1, 3, 5, 11),
    (0, 1, 3, 6, 7), (0, 1, 3, 6, 8), (0, 1, 3, 6, 9), (0, 1, 3, 6, 10),
    (0, 1, 3, 6, 11), (0, 1, 3, 7, 8), (0, 1, 3, 7, 11), (0, 1, 6, 7, 9),
]
assert representatives == expected

h, d1, d2, d3, k, x, y, z = sp.symbols('h d1 d2 d3 k x y z', nonzero=True)
D = d1 + d2 - h
family = ((h - d1*x - d2*y + d3*z)**2 + 2*d3*k*z*(1 - x - y)
          + k*(2*D + k)*x*y)
family_contacts = [
    ({x: h/d1, y: 0, z: 0}, x), ({x: 0, y: h/d2, z: 0}, y),
    ({x: 1, y: 0, z: (d1 - h)/d3}, z),
    ({x: 0, y: 1, z: (d2 - h)/d3}, z),
    ({x: 1, y: 1, z: (D + k)/d3}, z),
]
K = sp.symbols('K')
triangle = z + x*y - x*z - y*z
cycle = (h - d1*x - d2*y + d3*z)**2 + 2*K*triangle
cycle_contacts = [
    ({x: h/d1, y: 0, z: 0}, x), ({x: 0, y: h/d2, z: 0}, y),
    ({x: 0, y: 1, z: (d2 - h)/d3}, z),
    ({x: 1, y: 0, z: (d1 - h)/d3}, z),
    ({x: (d3 - d2 + h)/d1, y: 1, z: 1}, x),
    ({x: 1, y: (d3 - d1 + h)/d2, z: 1}, y),
]
for polynomial, contacts in [(family, family_contacts), (cycle, cycle_contacts)]:
    for point, direction in contacts:
        assert sp.factor(polynomial.subs(point)) == 0
        assert sp.factor(sp.diff(polynomial, direction).subs(point)) == 0
assert sp.expand(triangle - (z*(1 - x)*(1 - y) + x*y*(1 - z))) == 0
print('PASS: direct graph automorphisms reproduce all 24 table rows.')
print('PASS: symbolic family and six-cycle values and tangent derivatives.')
