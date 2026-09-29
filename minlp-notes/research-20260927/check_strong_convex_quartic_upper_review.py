"""Exact checks supporting the independent unconstrained-quartic review.

Symbolic identities supplement the all-input analytic proof. The finite
constant checks do not establish the source theorems or algebraic gap.
"""

from fractions import Fraction

import sympy as sp


def check_newton_integral_identity():
    x, y, u, v, t = sp.symbols("x y u v t")
    # A convex example with mixed terms, a nonzero gradient at the origin,
    # and a full-rank Hessian: the identity does not assume p is stationary.
    f = (x**2 + y**2) ** 2 + x**2 + 2 * y**2 + x - 3 * y
    variables = sp.Matrix([x, y])
    point = sp.Matrix([u, v])
    difference = variables - point
    gradient = sp.Matrix([sp.diff(f, item) for item in variables])
    hessian = sp.hessian(f, variables)
    substitutions = {
        x: u + t * (x - u),
        y: v + t * (y - v),
    }
    integral = sp.integrate(
        (hessian - hessian.subs(substitutions, simultaneous=True))
        * difference,
        (t, 0, 1),
    )
    expected = hessian * difference - (
        gradient - gradient.subs({x: u, y: v}, simultaneous=True)
    )
    assert all(sp.expand(entry) == 0 for entry in integral - expected)


def check_ldl_solve():
    a, b, c, s, t = sp.symbols("a b c s t")
    pivot = c - b**2 / a
    second = (t - b * s / a) / pivot
    first = s / a - b * second / a
    matrix = sp.Matrix([[a, b], [b, c]])
    residual = matrix * sp.Matrix([first, second]) - sp.Matrix([s, t])
    assert all(sp.cancel(entry) == 0 for entry in residual)


def check_comparison_margins():
    # Set g=1 by positive scaling. The tested endpoints are the worst
    # perturbations in the zero case and nearest nonzero cases.
    for alpha in (-1, 0, 1):
        for error in (Fraction(-1, 8), Fraction(1, 8)):
            approximate = alpha + error
            values = (
                approximate - Fraction(1, 2),
                approximate + Fraction(1, 2),
                -approximate - Fraction(1, 2),
                -approximate + Fraction(1, 2),
                Fraction(1, 4) - approximate**2,
            )
            desired = (
                alpha > 0,
                alpha >= 0,
                alpha < 0,
                alpha <= 0,
                alpha == 0,
            )
            assert tuple(value > 0 for value in values) == desired
            assert all(value != 0 for value in values)


def check_constant_margins():
    for length in range(2, 65):
        bound_exponent = 20 * length
        assert 18 * length + 4 <= bound_exponent
        assert 15 * length + 5 <= bound_exponent
        assert 11 * length + 6 <= bound_exponent
        assert 8 * length + 6 <= bound_exponent
        exponent = 40 * length + 10
        assert 21 * length + 4 <= 10 * 2**exponent
        assert exponent + 2**exponent <= 2 ** (exponent + 1)


if __name__ == "__main__":
    check_newton_integral_identity()
    check_ldl_solve()
    check_comparison_margins()
    check_constant_margins()
    print("PASS: polynomial Newton integral identity")
    print("PASS: rational LDL solve identity")
    print("PASS: all five comparison signs, including exact zero")
    print("PASS: constant exponent margins for input lengths 2 through 64")
