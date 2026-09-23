"""Exact diagnostics for rational-centered positive-polynomial inversion.

Checks formal reversion, certified inverse enclosures on representative
panels, and complex derivative bounds using Gaussian rational arithmetic.
The complete all-panel guarantee and polynomial complexity are analytical.
"""

from fractions import Fraction as F
from math import comb, lcm


def value(coefficients, x):
    answer = F(0)
    for coefficient in reversed(coefficients):
        answer = (answer + coefficient) * x
    return answer


def root_interval(coefficients, target, width):
    low, high = F(0), F(1)
    while high - low > width:
        middle = (low + high) / 2
        if value(coefficients, middle) <= target:
            low = middle
        else:
            high = middle
    return low, high


def multiply(left, right, degree):
    result = [F(0)] * (degree + 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right[:degree + 1 - i]):
            result[i + j] += a * b
    return result


def reversion(coefficients, center, degree):
    maximum = len(coefficients)
    shifted = [sum(coefficients[k - 1] * comb(k, h) * center**(k-h)
                   for k in range(max(1, h), maximum + 1))
               for h in range(maximum + 1)]
    series = [F(0)] * (degree + 1)
    for n in range(1, degree + 1):
        power = [F(1)] + [F(0)] * n
        coefficient = F(0)
        for h in range(1, min(maximum, n) + 1):
            power = multiply(power, series[:n + 1], n)
            coefficient += shifted[h] * power[n]
        series[n] = (F(n == 1) - coefficient) / shifted[1]
    composed = [shifted[0]] + [F(0)] * degree
    power = [F(1)] + [F(0)] * degree
    for h in range(1, maximum + 1):
        power = multiply(power, series, degree)
        composed = [a + shifted[h] * b for a, b in zip(composed, power)]
    assert composed == [value(coefficients, center), F(1)] + [F(0)] * (degree - 1)
    denominator = lcm(*(a.denominator for a in shifted[1:]))
    first = int(shifted[1] * denominator)
    for n in range(1, degree + 1):
        assert (series[n] * first**(2*n-1) / denominator**n).denominator == 1
    series[0] = center
    return series, shifted[1]


def complex_add(a, b):
    return a[0] + b[0], a[1] + b[1]


def complex_multiply(a, b):
    return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def complex_derivative(coefficients, z):
    answer = (F(0), F(0))
    for k in range(len(coefficients), 0, -1):
        answer = complex_add(complex_multiply(answer, z), (k*coefficients[k-1], F(0)))
    return answer


families = [[F(1)], [F(0), F(0), F(0), F(1)],
            [F(1, 2**30), F(0), F(0), F(1)],
            [F(1), F(0), F(0), F(1, 2**40)],
            [F(1), F(3), F(0), F(5), F(2)]]
centers = values = complex_checks = 0
maximum_coefficient_bits = 0
for original in families:
    coefficients = [a / sum(original) for a in original]
    maximum = len(coefficients)
    for eta in (F(1, 32), F(3, 100)):
        m = 0
        while F(1, 2**m) > eta:
            m += 1
        cutoff_depth = maximum * m
        degree = m + 3
        assert value(coefficients, eta) >= F(1, 2**cutoff_depth)
        for k in sorted({0, cutoff_depth // 2, cutoff_depth - 1}):
            left_dyadic = F(1, 2**(k + 1))
            panel_count = 32 * maximum
            width = left_dyadic / panel_count
            for panel in (0, panel_count // 2, panel_count - 1):
                left = left_dyadic + panel * width
                right = left + width
                nominal = (left + right) / 2
                low, high = root_interval(coefficients, nominal, nominal / (64 * maximum**2))
                center = (low + high) / 2
                target_center = value(coefficients, center)
                assert abs(target_center - nominal) <= nominal / (64 * maximum)
                inverse_radius = target_center / (8 * maximum)
                assert max(abs(left-target_center), abs(right-target_center)) < inverse_radius / 2
                series, derivative = reversion(coefficients, center, degree)
                for coefficient in series:
                    maximum_coefficient_bits = max(maximum_coefficient_bits,
                                                   coefficient.numerator.bit_length(),
                                                   coefficient.denominator.bit_length())
                for fraction in (F(0), F(1, 4), F(1, 2), F(3, 4), F(1)):
                    target = left + fraction * width
                    displacement = target - target_center
                    polynomial = sum(a * displacement**n for n, a in enumerate(series))
                    root_low, root_high = root_interval(coefficients, target, eta / 64)
                    assert max(abs(polynomial-root_low), abs(polynomial-root_high)) <= eta / 4
                    values += 1
                z_radius = center / (4 * maximum)
                for direction in ((F(1), F(0)), (F(-1), F(0)),
                                  (F(0), F(1)), (F(3, 5), F(4, 5))):
                    z = (center + z_radius*direction[0], z_radius*direction[1])
                    changed = complex_derivative(coefficients, z)
                    difference = (changed[0] - derivative, changed[1])
                    assert difference[0]**2 + difference[1]**2 < derivative**2 / 9
                    complex_checks += 1
                centers += 1

print(f"PASS: {centers} exact rational Taylor reversions, {values} certified "
      f"inverse values, {complex_checks} Gaussian-rational derivative bounds; "
      f"largest tested coefficient encoding {maximum_coefficient_bits} bits.")
