"""Exact finite checks of the proposed balanced-cardinality refinement.

All expectations are computed from explicit distributions, using fractions.
Finite checks supplement, and do not replace, the coefficient proof.
"""

from fractions import Fraction as Q
from itertools import combinations, product
from math import comb, prod
import random


def potential(k, coefficients):
    return sum(a * comb(k, j) for j, a in enumerate(coefficients) if j <= k)


def independent(means, coefficients):
    return sum(
        prod(p if bit else 1 - p for p, bit in zip(means, bits))
        * potential(sum(bits), coefficients)
        for bits in product((0, 1), repeat=len(means))
    )


def threshold_expectation(means, coefficients, starts):
    intervals = [(Q(0), p) if left else (1 - p, Q(1)) for p, left in zip(means, starts)]
    breaks = sorted({Q(0), Q(1), *(v for interval in intervals for v in interval)})
    return sum(
        (b - a) * potential(sum(lo <= (a + b) / 2 <= hi for lo, hi in intervals), coefficients)
        for a, b in zip(breaks, breaks[1:])
    )


def check_case(ambient, scope, all_means, coefficients, bound):
    means = [all_means[i] for i in scope]
    upper = threshold_expectation(means, coefficients, [True] * len(scope))
    mean_count = sum(means)
    lower_count = mean_count.numerator // mean_count.denominator
    fraction = mean_count - lower_count
    lower = (1 - fraction) * potential(lower_count, coefficients)
    if fraction:
        lower += fraction * potential(lower_count + 1, coefficients)
    independent_value = independent(means, coefficients)
    orientations = list(combinations(range(ambient), ambient // 2))
    orientation_value = sum(
        threshold_expectation(means, coefficients, [i in left for i in scope])
        for left in orientations
    ) / len(orientations)
    beta = Q(ambient * (ambient - 1), 2 * (ambient // 2) * (ambient - ambient // 2))
    assert upper - lower <= (1 + bound) * (upper - independent_value) + beta * (upper - orientation_value)


def main():
    rng = random.Random(584913)
    count = 0
    for ambient in range(2, 8):
        for _ in range(60):
            means = [Q(rng.randrange(9), 8) for _ in range(ambient)]
            scope = sorted(rng.sample(range(ambient), rng.randrange(1, ambient + 1)))
            bound = rng.choice([Q(0), Q(1, 2), Q(1), Q(2), Q(5)])
            coefficients = [Q(1), Q(2)]
            if len(scope) >= 2:
                coefficients.append(Q(1))
            for _ in range(3, len(scope) + 1):
                coefficients.append(coefficients[-1] * bound * Q(rng.randrange(5), 4))
            check_case(ambient, scope, means, coefficients, bound)
            count += 1
    print(f"PASS: {count} exact cardinality cases with fixed ambient balanced orientations.")
    print("Includes proper restrictions, odd ambient dimensions, deterministic coordinates, and L=0.")
    print("This is finite evidence; the universal claim still requires its coefficient proof and review.")


if __name__ == "__main__":
    main()
