"""Exhaustive finite checks of the Max-Cut integer-dimension gap gadget."""

from fractions import Fraction
from itertools import combinations, product
import random


rng = random.Random(2026090534)
graphs = 0
packing_pairs = 0
for n in range(2, 8):
    for trial in range(8):
        edges = [edge for edge in combinations(range(n), 2) if rng.random() < 0.5]
        vertices = list(product((0, 1), repeat=n))

        def quadratic(point):
            return sum((point[i] - point[j]) ** 2 for i, j in edges)

        maximum = max(map(quadratic, vertices))
        maximizer = next(point for point in vertices if quadratic(point) == maximum)
        complement = tuple(1 - value for value in maximizer)
        assert quadratic(complement) == maximum
        assert quadratic((Fraction(1, 2),) * n) == 0
        for sample in range(8):
            point = tuple(Fraction(rng.randrange(9), 8) for _ in range(n))
            assert 0 <= quadratic(point) <= maximum
        # Check both sides of the integer threshold and its unit-tolerance scaling.
        for target in (max(1, maximum), maximum + 1):
            tolerance = Fraction(2 * target - 1, 2)
            if maximum >= target:
                t = 3
                choices = list(product((0, 1), repeat=t + 1))
                for left, right in combinations(choices, 2):
                    errors = []
                    for block in range(t):
                        x = complement if left[block] else maximizer
                        y = complement if right[block] else maximizer
                        midpoint = tuple(Fraction(a + b, 2) for a, b in zip(x, y))
                        errors.append(abs(Fraction(maximum, 1) - quadratic(midpoint)) / tolerance)
                    z, y = left[-1], right[-1]
                    errors.append(abs(Fraction(8 * z * z + 8 * y * y, 2)
                                      - 8 * Fraction(z + y, 2) ** 2))
                    assert max(errors) > 1
                    packing_pairs += 1
            else:
                assert maximum < tolerance
        graphs += 1

# Explicit one-binary square lift on all tested residual fractions.
for bit in (0, 1):
    for numerator in range(65):
        residual = Fraction(numerator, 64)
        z = (bit + residual) / 2
        for square_surrogate in (max(0, 2 * residual - 1), residual):
            output = 2 * (bit + 2 * bit * residual + square_surrogate)
            assert abs(output - 8 * z * z) <= Fraction(1, 2)

print(f'PASS: {graphs} exhaustive Max-Cut gadgets, {packing_pairs} augmented packing pairs, '
      '260 one-binary scalar-lift extrema')
