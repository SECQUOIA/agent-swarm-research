"""Independent finite geometry checks for reviewer 11 (not a proof)."""
from itertools import combinations, product
from fractions import Fraction
from math import prod
import random
import numpy as np
import sympy as sp
from scipy.spatial import ConvexHull

forest_count = minor_count = hull_count = 0
for n in range(2, 6):
    edges = list(combinations(range(n), 2))
    for mask in range(1, 1 << len(edges)):
        parent = list(range(n))
        def root(i):
            while parent[i] != i:
                i = parent[i]
            return i
        chosen = [e for j, e in enumerate(edges) if (mask >> j) & 1]
        for u, v in chosen:
            a, b = root(u), root(v)
            if a == b:
                break
            parent[a] = b
        else:
            r = len(chosen)
            B = sp.zeros(r, n)
            for j, (u, v) in enumerate(chosen):
                B[j, u], B[j, v] = 1, -1
            sizes = [sum(root(i) == a for i in range(n)) for a in set(root(i) for i in range(n))]
            minors = [abs(int(B[:, list(I)].det())) for I in combinations(range(n), r)]
            assert set(minors) <= {0, 1}
            assert sum(minors) == prod(sizes)
            assert B.rank() == r
            minor_count += len(minors)
            forest_count += 1
            if r >= 2 and forest_count % 5 == 0:
                verts = np.array(list(product((0, 1), repeat=n)), dtype=float)
                image = (verts @ np.array(B, dtype=float).T + 1) / 2
                actual = ConvexHull(image).volume
                expected = prod(sizes) / (2 ** r)
                assert abs(actual - expected) < 1e-8
                hull_count += 1

random.seed(11)
feature_count = 0
for r in range(1, 5):
    n = r + 1
    for _ in range(12):
        while True:
            T = sp.Matrix([[random.randrange(-4, 5) for _ in range(n)] for _ in range(r)])
            if T.rank() == r:
                break
        widths = [sum(abs(T[i, j]) for j in range(n)) for i in range(r)]
        offsets = sp.Matrix([sum(min(0, T[i,j]) for j in range(n)) for i in range(r)])
        minors = [abs(T[:, list(I)].det()) for I in combinations(range(n), r)]
        V = sum(minors) / prod(widths)
        assert V >= max(minors) / prod(widths) >= sp.Rational(1, prod(widths))
        assert V <= 1
        verts = list(product((0, 1), repeat=n))
        images = [sp.diag(*[1/w for w in widths]) * (T*sp.Matrix(v)-offsets) for v in verts]
        assert all(0 <= z <= 1 for y in images for z in y)
        assert all(min(y[i] for y in images) == 0 and max(y[i] for y in images) == 1 for i in range(r))
        if r >= 2:
            actual = ConvexHull(np.array(images, dtype=float).reshape(-1, r)).volume
            assert abs(actual - float(V)) < 1e-8
        feature_count += 1

for L in range(1, 25):
    eps = Fraction(1, 4**L)
    delta = eps / 16
    assert eps/4 + 2*delta + delta**2 < eps
    assert (1+delta)/(4*eps) > 4**L / 4
print(f'PASS: {forest_count} forests; {minor_count} exact incidence minors; {hull_count} independent forest hull volumes; {feature_count} full-rank integer-feature cases; 24 exact thin-domain budgets.')
