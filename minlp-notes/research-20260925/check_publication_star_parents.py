"""Independent exact PSD-parent audit of the rational accuracy examples.

Builds positive definite joint pattern matrices explicitly for every required
subset through eight leaves, rather than using only a perimeter comparison.
All arithmetic is rational. This is a finite verification, not an all-order
proof or a novelty check.
"""

from fractions import Fraction as F
from itertools import combinations
from math import isqrt


def exact_root(value):
    num, den = isqrt(value.numerator), isqrt(value.denominator)
    assert num * num == value.numerator
    assert den * den == value.denominator
    return F(num, den)


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def generators(points):
    following = points[1:] + [tuple(-x for x in points[0])]
    return [tuple((b - a) / 2 for a, b in zip(p, q))
            for p, q in zip(points, following)]


def construct(k):
    n = 2 * k
    points = []
    for i in range(n):
        tau = F(2 * i - (n - 1), 64 * (n - 1))
        base_x = (1 - tau * tau) / (1 + tau * tau)
        base_y = 2 * tau / (1 + tau * tau)
        px, py = base_x * base_x - base_y * base_y, 2 * base_x * base_y
        points.append(((5 * px + 12 * py) / 13,
                       (-12 * px + 5 * py) / 13))
    perimeter = 4 * sum(exact_root(x*x + y*y)
                        for x, y in generators(points))
    upper = perimeter - F(k, 11664 * (n - 1)**3)
    eta = 2 / perimeter + 2 / upper
    return [tuple(eta * x for x in p) for p in points]


def verify_parent(points):
    count = len(points)
    pieces = generators(points)
    lengths = [exact_root(x*x + y*y) for x, y in pieces]
    residual = 1 - sum(lengths)
    assert residual > 0
    matrices = [(residual / 2**count, F(0), residual / 2**count)
                for _ in range(2**count)]
    for j, ((hx, hz), length) in enumerate(zip(pieces, lengths)):
        # Vertex i has coefficient +1 on generator j exactly when j < i.
        positive_pattern = sum(1 << i for i in range(count) if j < i)
        negative_pattern = (2**count - 1) ^ positive_pattern
        plus = ((length + hz) / 2, hx / 2, (length - hz) / 2)
        minus = ((length - hz) / 2, -hx / 2, (length + hz) / 2)
        matrices[positive_pattern] = add(matrices[positive_pattern], plus)
        matrices[negative_pattern] = add(matrices[negative_pattern], minus)
    total = tuple(sum(m[j] for m in matrices) for j in range(3))
    assert total == (1, 0, 1)
    for m00, m01, m11 in matrices:
        assert m00 > 0 and m00*m11 - m01*m01 > 0
    for i, (px, pz) in enumerate(points):
        marginal = tuple(sum(m[j] for pattern, m in enumerate(matrices)
                             if pattern & (1 << i)) for j in range(3))
        assert marginal == ((1 + pz) / 2, px / 2, (1 - pz) / 2)
    return len(matrices)


if __name__ == "__main__":
    subsets = parents = 0
    for k in range(1, 5):
        points = construct(k)
        for size in range(1, k + 1):
            for chosen in combinations(points, size):
                parents += verify_parent(list(chosen))
                subsets += 1
    print(f"PASS: {subsets} exact local laws represented by {parents} "
          "positive definite pattern matrices; all totals and marginals exact.")
