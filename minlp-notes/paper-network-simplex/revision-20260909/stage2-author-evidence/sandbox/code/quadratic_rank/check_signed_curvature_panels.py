"""Exact adaptive panel certificates with numerical quadrature comparisons.

Every polynomial below is nonnegative and nondecreasing on [0,1] but has
negative coefficients. The first is 16*(1+x-x*x/4)^2; the others are
integrals of even powers, with optional positive constants and scaling.
"""

from fractions import Fraction as F
from math import comb

import mpmath as mp


def evaluate(coefficients, x):
    result = 0
    for coefficient in reversed(coefficients):
        result = result * x + coefficient
    return result


def ceil_log2(value):
    k = max(0, value.numerator.bit_length() - value.denominator.bit_length())
    while F(1 << k) < value:
        k += 1
    return k


def numeric(value):
    return mp.mpf(value.numerator) / value.denominator


def integrated_even_power(center, exponent, offset=F(0)):
    result = [offset] + [F(comb(exponent, k)) * (-center)**(exponent-k) / (k+1)
                         for k in range(exponent+1)]
    total = sum(result)
    return [16*c/total for c in result]


def panels(coefficients, cutoff):
    degree = len(coefficients) - 1
    stack = [(cutoff, F(1), 0)]
    accepted, failures, max_depth = [], 0, 0
    while stack:
        left, right, depth = stack.pop()
        max_depth = max(max_depth, depth)
        center, length = (left+right)/2, right-left
        powers = [center**i for i in range(degree+1)]
        shifted = [sum((coefficients[j] * comb(j, k) * powers[j-k]
                        for j in range(k, degree+1)), F(0))
                   for k in range(degree+1)]
        assert shifted[0] > 0
        variation = sum((abs(shifted[k]) * length**k for k in range(1, degree+1)), F(0))
        if 2*variation <= shifted[0]:
            accepted.append((left, right))
        else:
            failures += 1
            assert depth < 100
            stack.extend([(center, right, depth+1), (left, center, depth+1)])
    return sorted(accepted), failures, max_depth


def run():
    mp.mp.dps = 90
    tolerance = F(1, 1024)
    cases = [[F(16), F(32), F(8), F(-8), F(1)],
             integrated_even_power(F(1, 2), 2, F(1, 1 << 40)),
             integrated_even_power(F(3, 4), 8),
             integrated_even_power(F(1, 1 << 40), 2)]
    total = 0
    for index, coefficients in enumerate(cases):
        assert any(c < 0 for c in coefficients)
        upper = max(F(1), sum(coefficients))
        cutoff = F(1, 1 << max(1, ceil_log2(16*upper/tolerance)))
        intervals, failures, depth = panels(coefficients, cutoff)
        assert intervals[0][0] == cutoff and intervals[-1][1] == 1
        assert all(a[1] == b[0] for a, b in zip(intervals, intervals[1:]))
        order = (ceil_log2(128*upper/tolerance)+1)//2
        nodes, weights = mp.gauss_quadrature(order, "legendre")
        numbers = list(map(numeric, coefficients))

        def function(x):
            return mp.sqrt(evaluate(numbers, x))

        approximate = mp.mpf(0)
        for left, right in intervals:
            center, half = numeric((left+right)/2), numeric((right-left)/2)
            approximate += half * mp.fsum(w*function(center+half*r)
                                          for r, w in zip(nodes, weights))
        if index == 0:
            reference = mp.mpf(17)/3
        else:
            reference = mp.quad(function, [0, numeric(cutoff), mp.mpf('.25'),
                                          mp.mpf('.5'), mp.mpf('.75'), 1])
        error = abs(approximate-reference)
        assert error < numeric(tolerance)
        total += len(intervals)
        print(f"case={index}, degree={len(coefficients)-1}, panels={len(intervals)}, "
              f"failures={failures}, depth={depth}, error={mp.nstr(error, 8)}")
    print(f"Passed four signed-coefficient cases with {total} certified panels.")


if __name__ == "__main__":
    run()
