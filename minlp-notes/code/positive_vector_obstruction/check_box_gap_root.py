"""Exact independent checks for the degree-32 ternary box construction."""

from fractions import Fraction as Q
from itertools import combinations, product


A, c = Q(7, 4), Q(1, 48)
L, d = A * (1 - c) ** 32, A * c**32


def graph(x):
    return A * (1 - x) ** 32, A * x**32


assert A - 1 < L < 1
assert 0 < d < 2 - A
assert max(L, (A + d) / 2) < 1

boxes = [
    ((Q(0), c), (L, A), (Q(0), d)),
    ((c, 1 - c), (Q(0), L), (Q(0), L)),
    ((1 - c, Q(1)), (Q(0), d), (L, A)),
]
vertices = [list(product(*box)) for box in boxes]
middle_vertices = vertices[1] + [
    tuple((u + v) / 2 for u, v in zip(left, right))
    for left in vertices[0]
    for right in vertices[2]
]
for x, w1, w2 in middle_vertices:
    assert c <= x <= 1 - c
    assert 0 <= w1 <= max(L, (A + d) / 2)
    assert 0 <= w2 <= max(L, (A + d) / 2)
    f1, f2 = graph(x)
    assert abs(w1 - f1) < 1 and abs(w2 - f2) < 1

mixtures = 0
for left, middle, right in product(*vertices):
    for t in (Q(0), Q(1, 7), Q(1, 4), Q(1, 2)):
        x, w1, w2 = tuple(
            t * u + (1 - 2 * t) * v + t * w
            for u, v, w in zip(left, middle, right)
        )
        assert c <= x <= 1 - c
        f1, f2 = graph(x)
        assert abs(w1 - f1) < 1 and abs(w2 - f2) < 1
        mixtures += 1

pairs = 0
for n in range(1, 4):
    points = list(product((Q(0), Q(1, 2), Q(1)), repeat=n))
    for u, v in combinations(points, 2):
        incompatible = False
        for weight in (Q(1, 3), Q(2, 3)):
            for x, y in zip(u, v):
                fx, fy = graph(x), graph(y)
                fm = graph(weight * x + (1 - weight) * y)
                if any(
                    weight * a + (1 - weight) * b - z > 1
                    for a, b, z in zip(fx, fy, fm)
                ):
                    incompatible = True
        assert incompatible
        pairs += 1

print(
    "PASS:", len(middle_vertices), "middle-slice vertices,",
    mixtures, "exact integer-slice mixtures,", pairs,
    "product contact-pair obstructions."
)
