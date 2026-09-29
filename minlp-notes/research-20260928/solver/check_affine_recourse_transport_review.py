"""Independent exact checks of the kernel transport calculation.

This finite check does not prove the all-order theorem, preordering
positivity, Hoffman bounds, projection measurability, or sparse gluing.
"""

from fractions import Fraction
from math import comb

import sympy as sp


def coefficients(m):
    triangular = {j: m - abs(j) for j in range(-m + 1, m)}

    def a(k):
        return sum(value * triangular.get(j - k, 0)
                   for j, value in triangular.items())

    return a


for m in range(2, 61):
    a = coefficients(m)
    a0 = a(0)
    assert a0 == m * (2 * m * m + 1) // 3
    assert a0 - a(1) == m
    assert a0 - a(2) == 4 * m - 3
    g1, g2 = Fraction(a(1), a0), Fraction(a(2), a0)
    slope, constant = 1 - 2 * g1 + g2, (1 - g2) / 2
    assert slope == Fraction(3 - 2 * m, a0) < 0
    assert constant == Fraction(4 * m - 3, 2 * a0)
    assert constant == (Fraction(6, 2 * m * m + 1)
                        - Fraction(9, 2 * m * (2 * m * m + 1)))
    assert 0 <= slope + constant <= constant <= Fraction(6, 2 * m * m + 1)

x, v = sp.symbols("x v")
for m in range(2, 11):
    a = coefficients(m)
    kernel = 1 + sum(
        2 * sp.Rational(a(k), a(0)) * sp.chebyshevt(k, x) * sp.chebyshevt(k, v)
        for k in range(1, 2 * m - 1)
    )
    polynomial = sp.Poly(sp.expand(kernel * (x - v) ** 2), v)
    integral = sum(
        coefficient * sp.Rational(comb(degree, degree // 2), 2 ** degree)
        for (degree,), coefficient in polynomial.terms()
        if degree % 2 == 0
    )
    target = (sp.Rational(3 - 2 * m, a(0)) * x * x
              + sp.Rational(4 * m - 3, 2 * a(0)))
    assert sp.expand(integral - target) == 0

print("PASS: exact multipliers and sharp displacement for m=2,...,60; "
      "independent monomial arcsine integration for m=2,...,10.")
