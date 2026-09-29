"""Exact, targeted checks for the one-binary penalty construction.

This checks finite exact-rational cases of the derived projected dual.
It does not replace the symbolic proof for all dimensions or validate novelty.
"""

from fractions import Fraction as F
from itertools import combinations


def lower_envelope(lines, x):
    return min(slope * x + intercept for slope, intercept in lines)


def maximize_lower_envelope(lines):
    candidates = [F(0)]
    for (slope_a, offset_a), (slope_b, offset_b) in combinations(lines, 2):
        if slope_a != slope_b:
            candidates.append((offset_b - offset_a) / (slope_a - slope_b))
    return max(lower_envelope(lines, point) for point in candidates)


cases = 0
for n in range(1, 13):
    a = [F(1, 2 ** (2**i)) for i in range(1, n + 1)]
    delta = a[-1]
    assert a[0] == F(1, 4)
    assert all(a[i + 1] == a[i] ** 2 for i in range(n - 1))
    threshold = F(1, 2 * delta)
    assert threshold.denominator == 1
    assert threshold.numerator.bit_length() == 2**n

    # Feasible and native-infeasible-slice strict points: all slacks >= 1/8.
    for q, y in [(0, F(0)), (1, F(1, 2))]:
        strict_a = F(3, 8)
        slacks = [strict_a - F(1, 4), strict_a, 1 - strict_a,
                  y + 1, 1 - y, y - strict_a + 2 * (1 - q)]
        if n > 1:
            slacks.append(strict_a - strict_a**2)
        assert min(slacks) >= F(1, 8)

    for multiplier in [F(0), F(1, 16), F(1, 2), F(1), F(2), F(17, 3)]:
        rho = multiplier * threshold
        # q=0: residuals -1,0; q=1: residuals delta,1.
        # Piecewise linearity in residual makes these endpoints sufficient.
        lines = [(-1, rho), (0, F(0)),
                 (delta, -1 + delta * rho), (1, -1 + rho)]
        actual = maximize_lower_envelope(lines)
        expected = min(F(0), (2 * rho * delta - 1) / (1 + delta))
        assert actual == expected, (n, multiplier, actual, expected)
        chosen_lambda = ((1 + rho * (1 - delta)) / (1 + delta)
                         if rho <= threshold else rho)
        assert lower_envelope(lines, chosen_lambda) == expected
        cases += 1

print(f"PASS: {cases} exact dual-envelope cases; n=1..12; "
      "chain identities, penalty bit lengths, and strict-point margins.")
