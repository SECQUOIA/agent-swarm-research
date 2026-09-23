"""Independent exact checks for positive-polynomial shape packing.

Square rational inputs make even the odd-degree feature powers rational.
The checks support the analytical proof; no maximal packing is computed.
"""

from fractions import Fraction as Q
from math import comb
import random


rng = random.Random(2026090513)
feature_cases = secant_cases = jensen_cases = 0


def value(coefficients, x):
    return sum((c * x**k for k, c in coefficients.items()), Q(0))


def jensen(coefficients, a, b):
    return (value(coefficients, a) + value(coefficients, b)) / 2 - value(
        coefficients, (a + b) / 2
    )


def distance_squared(coefficients, s, t):
    # Inputs to the original polynomial are s^2 and t^2.
    return sum((c * (s**k - t**k) ** 2 for k, c in coefficients.items()), Q(0))


for _ in range(120):
    degree = rng.randrange(2, 15)
    coefficients = {k: Q(rng.randrange(0, 8), rng.randrange(1, 9))
                    for k in range(2, degree + 1)}
    coefficients[degree] = Q(rng.randrange(1, 8), rng.randrange(1, 9))
    roots = sorted({Q(0), Q(1), *(Q(rng.randrange(25), 24) for _ in range(5))})
    points = [x * x for x in roots]
    for left in range(len(roots)):
        for right in range(left + 1, len(roots)):
            gap = jensen(coefficients, points[left], points[right])
            dist = distance_squared(coefficients, roots[left], roots[right])
            assert dist / 4 <= gap <= dist / 2
            feature_cases += 1
            adjacent_distances = sum(
                (distance_squared(coefficients, roots[h], roots[h + 1])
                 for h in range(left, right)), Q(0)
            )
            assert dist >= adjacent_distances
            secant_cases += 1
            adjacent_gaps = sum(
                (jensen(coefficients, points[h], points[h + 1])
                 for h in range(left, right)), Q(0)
            )
            assert gap >= adjacent_gaps
            jensen_cases += 1


def lattice_ball_count(dimension, radius):
    # Choose the j nonzero coordinates, their signs, and positive magnitudes.
    return sum(2**j * comb(dimension, j) * comb(radius, j)
               for j in range(min(dimension, radius) + 1))


lattice_cases = 0
for dimension in range(1, 21):
    assert lattice_ball_count(dimension, dimension) <= 6**dimension
    assert lattice_ball_count(dimension, 2 * dimension) <= 12**dimension
    lattice_cases += 2

assert 6 * 481 < 2**12
assert 481 < 2**9
print(f"PASS: {feature_cases} exact feature comparisons, "
      f"{secant_cases} squared-secant and {jensen_cases} direct Jensen "
      f"superadditivity checks; {lattice_cases} exact lattice-ball bounds")
