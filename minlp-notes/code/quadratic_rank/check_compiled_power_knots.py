"""Supporting exact-arithmetic checks for compiled inverse-power knots.

Rational-exponent comparisons use high-precision numerical references;
the uniform error guarantee is proved in the accompanying note.
"""

from fractions import Fraction as F
import mpmath as mp


def ceil_log2(value):
    result = 0
    power = F(1)
    while power < value:
        power *= 2
        result += 1
    return result


def power_down(base, exponent, precision):
    scale = 1 << precision
    factor = base.numerator * scale // base.denominator
    result = scale
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = result * factor // scale
        remaining >>= 1
        if remaining:
            factor = factor * factor // scale
    return F(result, scale)


def integer_knot(index, depth, degree, tolerance):
    if index == 0:
        return F(0)
    if index == 1 << depth:
        return F(1)
    target = F(index, 1 << depth) ** 2
    tau = tolerance * F(1, 1 << (2 * depth)) / 16
    steps = ceil_log2(2 / tolerance)
    precision = max(steps + 1, ceil_log2(degree / tau))
    lower, upper = F(0), F(1)
    for _ in range(steps):
        middle = (lower + upper) / 2
        estimate = power_down(middle, degree, precision)
        if estimate + tau < target:
            lower = middle
        elif estimate > target:
            upper = middle
        else:
            return middle
    return (lower + upper) / 2


def logarithm_series(value, terms):
    z = (value - 1) / (value + 1)
    return 2 * sum((z ** (2 * j + 1) / (2 * j + 1)
                    for j in range(terms)), F(0))


def rational_knot(index, depth, exponent, tolerance):
    if index == 0:
        return F(0)
    if index == 1 << depth:
        return F(1)
    t = F(index, 1 << depth)
    e, v = 0, t
    while v < 1:
        e += 1
        v *= 2
    terms = 1
    while F(6 * (depth + 1), 9 ** terms) > tolerance / 8:
        terms += 1
    a = (2 / exponent) * (
        logarithm_series(v, terms) - e * logarithm_series(F(2), terms))
    assert -2 * depth <= a <= 0
    scale = 1
    while scale < 4 * depth:
        scale *= 2
    q = a / scale
    order = 1
    while F(1, 1 << (order + 1)) > tolerance / (16 * scale):
        order += 2
    term, series = F(1), F(1)
    for j in range(1, order + 1):
        term *= q / j
        series += term
    assert F(1, 2) <= series <= 1
    answer = series ** scale
    bits = ceil_log2(4 / tolerance)
    units = answer.numerator * (1 << bits) // answer.denominator
    return F(units, 1 << bits)


def as_mpf(value):
    return mp.mpf(value.numerator) / value.denominator


rounding_checks = 0
for precision in (4, 8, 16):
    for numerator in range(17):
        base = F(numerator, 16)
        for degree in range(2, 31):
            estimate = power_down(base, degree, precision)
            assert 0 <= base ** degree - estimate <= F(degree, 1 << precision)
            rounding_checks += 1

mp.mp.dps = 300
inverse_checks = 0
for depth in (2, 4, 7):
    indices = sorted({0, 1, (1 << depth) // 2, (1 << depth) - 1, 1 << depth})
    for degree in (2, 3, 17, 10**40 + 1):
        tolerance = F(1, 1 << 22)
        for index in indices:
            answer = integer_knot(index, depth, degree, tolerance)
            reference = mp.power(mp.mpf(index) / (1 << depth), mp.mpf(2) / degree)
            assert abs(as_mpf(answer) - reference) <= as_mpf(tolerance)
            inverse_checks += 1

rational_checks = 0
for depth in (2, 5):
    for exponent in (F(3, 2), F(1000001, 1000000), F(2), F(7, 3),
                     F(19, 4), F(10**35 + 7, 13)):
        tolerance = F(1, 1 << 16)
        for index in (0, 1, (1 << depth) - 1, 1 << depth):
            answer = rational_knot(index, depth, exponent, tolerance)
            reference = mp.power(mp.mpf(index) / (1 << depth),
                                 2 / as_mpf(exponent))
            assert 0 <= answer <= 1
            assert abs(as_mpf(answer) - reference) <= as_mpf(tolerance)
            rational_checks += 1

geometry_checks = 0
for rational_alpha in (F(10**30 + 1, 10**30), F(3, 2), F(199, 100),
                       F(2), F(3), F(10**20)):
    alpha = as_mpf(rational_alpha)
    s = min(mp.mpf(1), alpha - 1)
    for left in range(17):
        for right in range(left, 17):
            a, b = mp.mpf(left) / 16, mp.mpf(right) / 16
            jensen = (a**alpha + b**alpha) / 2 - ((a + b) / 2)**alpha
            transformed = (b**(alpha/2) - a**(alpha/2))**2
            assert jensen + mp.mpf('1e-260') >= s * transformed / 8
            geometry_checks += 1
    for cell in range(8):
        a, b = mp.mpf(cell) / 8, mp.mpf(cell + 1) / 8
        for lam in (mp.mpf(0), mp.mpf('.25'), mp.mpf('.5'),
                    mp.mpf('.75'), mp.mpf(1)):
            x = (1-lam)*a**(2/alpha) + lam*b**(2/alpha)
            y = (1-lam)*a*a + lam*b*b
            assert -mp.mpf('1e-260') <= y-x**alpha <= 4*s/64+mp.mpf('1e-260')
            geometry_checks += 1

print(f"PASS: {rounding_checks} exact rounded-power bounds; "
      f"{inverse_checks} integer inverse checks; "
      f"{rational_checks} rational-exponent inverse checks; "
      f"{geometry_checks} scaled Jensen/chord checks.")
