"""Small exact checks of the reviewed binary-box penalty construction.

This enumerates vertices and every breakpoint of the scalar dual objective.
It tests a finite sample; it is not a proof of the theorem or its complexity.
"""

from fractions import Fraction
from itertools import product
from random import Random


def subset_sums(items):
    return {
        sum(item * bit for item, bit in zip(items, bits))
        for bits in product((0, 1), repeat=len(items))
    }


def direct_dual(points, penalty):
    lines = list({(r, Fraction(f) + penalty * abs(r)) for f, r in points})
    breakpoints = {Fraction(0)}
    for i, (slope, intercept) in enumerate(lines):
        for other_slope, other_intercept in lines[:i]:
            if slope != other_slope:
                breakpoints.add(
                    (other_intercept - intercept) / (slope - other_slope)
                )
    return max(
        min(slope * multiplier + intercept for slope, intercept in lines)
        for multiplier in breakpoints
    )


def main():
    random = Random(825031)
    instances = 0
    for n in range(1, 5):
        for _ in range(10):
            original = tuple(random.randrange(1, 9) for _ in range(n))
            original_sums = subset_sums(original)
            target = random.randrange(1, sum(original) + 1)
            native_sums = subset_sums(original + (target + 1,))
            predecessor = max(s for s in original_sums if s <= target)
            for scale in (2, 4, 16):
                points = [
                    (-q, scale * s - (scale * target + 1) * q)
                    for q in (0, 1)
                    for s in native_sums
                ]
                assert [point for point in points if point[1] == 0] == [(0, 0)]
                negative_distance = scale * (target - predecessor) + 1
                positive_distance = scale - 1
                threshold = (
                    Fraction(1, negative_distance)
                    + Fraction(1, positive_distance)
                ) / 2
                yes = target in original_sums
                assert (threshold == Fraction(scale, 2 * (scale - 1))) == yes
                if not yes:
                    assert threshold <= Fraction(scale, scale * scale - 1)
                fixed_zero_threshold = max(
                    Fraction(-f, abs(r)) for f, r in points if r != 0
                )
                assert fixed_zero_threshold == (
                    Fraction(1) if yes else Fraction(1, scale - 1)
                )
                for penalty in (Fraction(0), threshold / 2, threshold, 2 * threshold):
                    expected = min(
                        Fraction(0),
                        -1 + 2 * penalty * Fraction(
                            negative_distance * positive_distance,
                            negative_distance + positive_distance,
                        ),
                    )
                    assert direct_dual(points, penalty) == expected
                instances += 1
    print(
        f"PASS: {instances} box instances and {4 * instances} exact dual values; "
        "all vertices and all dual breakpoints enumerated."
    )


if __name__ == "__main__":
    main()
