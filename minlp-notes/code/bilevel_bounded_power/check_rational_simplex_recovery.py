"""Independent exact diagnostics for algebraic-to-rational cell recovery.

Uses polynomial objectives with known algebraic minimizers on a triangle and
a lower-dimensional line segment. All recovered points and objective bounds
are checked rationally; integer square roots implement exact algebraic floors.
This tests the recovery lemma, not a general quantifier-elimination solver.
"""

from fractions import Fraction as F
from math import isqrt


checks = 0
for accuracy_bits in (1, 2, 5, 12, 40, 100):
    epsilon = F(1, 2**accuracy_bits)

    # Triangle vertices (1,0), (0,1), (0,0). The minimizer is
    # (sqrt(2)/4,sqrt(3)/4), in a degree-four common algebraic field.
    derivative_bound = F(37, 4)
    denominator = 148 * 2**accuracy_bits
    first_floor = isqrt(denominator**2 // 8)
    second_floor = isqrt(3 * denominator**2 // 16)
    assert 8 * first_floor**2 <= denominator**2 < 8 * (first_floor + 1)**2
    assert 16 * second_floor**2 <= 3 * denominator**2 < 16 * (second_floor + 1)**2
    x, y = F(first_floor, denominator), F(second_floor, denominator)
    last_weight = 1 - x - y
    assert min(x, y, last_weight) >= 0
    objective = (x*x-F(1, 8))**2 + (y*y-F(3, 16))**2
    assert 2 * 2 * derivative_bound / denominator <= epsilon / 4
    assert objective <= epsilon / 4
    checks += 1

    # A line-segment cell x+y=1. Exact simplex rounding preserves its
    # equality even when the minimizing x=sqrt(2)/2 is irrational.
    derivative_bound = F(6)
    denominator = 96 * 2**accuracy_bits
    first_floor = isqrt(denominator**2 // 2)
    assert 2 * first_floor**2 <= denominator**2 < 2 * (first_floor + 1)**2
    x = F(first_floor, denominator)
    y = 1 - x
    assert x + y == 1 and 0 <= x <= 1 and 0 <= y <= 1
    objective = (x*x-F(1, 2))**2
    assert 2 * 2 * derivative_bound / denominator <= epsilon / 4
    assert objective <= epsilon / 4
    checks += 1

print(f"PASS: {checks} exact rational simplex recoveries, including "
      "lower-dimensional cells and accuracy requests up to 100 bits.")
