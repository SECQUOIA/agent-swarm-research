"""Targeted exact checks of the recorded polynomial escape construction.

These examples check signs, integrality, and the need for T >= 1. They do
not prove the general recession reduction or circuit-size theorem.
"""

from fractions import Fraction

import sympy as sp


def lift(bound, scalar_bound, row_coefficient_norm, negative_slope, t):
    c = 1 + scalar_bound + row_coefficient_norm / negative_slope
    assert c.denominator == 1
    increment = c * t * (1 + bound * bound)
    return increment, bound + scalar_bound + increment


def check_nested_chain():
    # 100 z^2 <= x1, x1^2 <= x2, anchored at the origin.
    for t in [Fraction(1), Fraction(2), Fraction(10), Fraction(101)]:
        bound = 1 + t
        x1, bound = lift(bound, Fraction(1), Fraction(100), Fraction(1), t)
        x2, bound = lift(bound, Fraction(1), Fraction(1), Fraction(1), t)
        assert 100 * t * t - x1 <= 0
        assert x1 * x1 - x2 <= 0
        assert max(abs(t), abs(x1), abs(x2)) <= bound
    # The anchored polynomial need not remain feasible between 0 and 1.
    t = Fraction(1, 100)
    x1, bound = lift(1 + t, Fraction(1), Fraction(100), Fraction(1), t)
    x2, _ = lift(bound, Fraction(1), Fraction(1), Fraction(1), t)
    assert x1 * x1 - x2 > 0


def check_unimodular_integer_lift():
    # z1 = y+s, z2=s, q=(z1-z2)^2-z1=y^2-y-s.
    # The integer recession direction (1,1) preserves objective -z1+z2.
    for t in [Fraction(1), Fraction(2), Fraction(7)]:
        s, _ = lift(1 + t, Fraction(1), Fraction(2), Fraction(1), t)
        z1, z2 = t + s, s
        assert z1.denominator == z2.denominator == 1
        assert (z1 - z2) ** 2 - z1 <= 0
        assert -z1 + z2 == -t


def check_algebraic_anchor():
    # x1 >= z^2, x2 >= x1^2, anchored at (0,sqrt(2),2).
    # The integer increment z=T stays integral despite the algebraic anchor.
    for t in [Fraction(1), Fraction(3), Fraction(11)]:
        p1, bound = lift(2 * (1 + t), Fraction(2), Fraction(1), Fraction(1), t)
        p2, _ = lift(bound, Fraction(2), Fraction(1), Fraction(1), t)
        x1 = sp.sqrt(2) + sp.Rational(p1.numerator, p1.denominator)
        x2 = 2 + sp.Rational(p2.numerator, p2.denominator)
        assert sp.simplify(x1 - t * t).is_positive
        assert sp.simplify(x2 - x1 * x1).is_positive
        assert t.denominator == 1


def check_fractional_projected_anchor():
    # Both original coordinates are integral, but projection along
    # d=(1/2,1) sends anchor (0,1) to y0=-1/2. Clearing d by D=2
    # still gives integer increments in both original coordinates.
    for t in [Fraction(1), Fraction(2), Fraction(9)]:
        bound = 1 + t
        removed_increment = 2 * 3 * t * (1 + bound * bound)
        w1 = t + removed_increment / 2
        w2 = 1 + removed_increment
        assert w1.denominator == w2.denominator == 1
        assert (w1 - w2 / 2) ** 2 - w2 <= 0
        assert -(w1 - w2 / 2) == Fraction(1, 2) - t


def check_degree_growth():
    t = sp.Symbol("T")
    bound = 1 + t
    for ell in range(1, 6):
        increment = 3 * t * (1 + bound**2)
        bound = sp.expand(bound + 1 + increment)
        assert sp.degree(bound, t) == 2 ** (ell + 1) - 1


if __name__ == "__main__":
    check_nested_chain()
    check_unimodular_integer_lift()
    check_algebraic_anchor()
    check_fractional_projected_anchor()
    check_degree_growth()
    print("PASS: nested rows, integer shear, algebraic and fractional anchors, degrees")
