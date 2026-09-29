"""Targeted checks for branching-degeneracy-barrier.md.

These finite checks support, but do not establish, the infinite construction
or the convex-cover lower bound. Run directly with Python; requires SymPy.
"""

from fractions import Fraction

import sympy as sp


def main():
    x, y = sp.symbols("x y", real=True)
    a, r = sp.symbols("a r", positive=True)
    u = sp.Matrix([x, y])
    s = (x * x + y * y) / r**2
    well = -a * (1 - s) ** 3
    hessian = sp.hessian(well, (x, y))
    claimed = (
        6 * a / r**2 * (1 - s) ** 2 * sp.eye(2)
        - 24 * a / r**4 * (1 - s) * u * u.T
    )
    assert (hessian - claimed).applyfunc(sp.simplify) == sp.zeros(2)
    radial = 6 * a / r**2 * (1 - s) * (1 - 5 * s)
    tangent = 6 * a / r**2 * (1 - s) ** 2
    assert (hessian * u - radial * u).applyfunc(sp.simplify) == sp.zeros(2, 1)
    v = sp.Matrix([-y, x])
    assert (hessian * v - tangent * v).applyfunc(sp.simplify) == sp.zeros(2, 1)
    for numerator in range(1001):
        s_value = Fraction(numerator, 1000)
        tangential = 6 * (1 - s_value) ** 2
        radial_value = 6 * (1 - s_value) * (1 - 5 * s_value)
        assert tangential >= 0
        assert abs(radial_value) <= 6
        assert tangential <= 6
    for m in range(16, 301):
        radius = Fraction(1, 2**m)
        length = Fraction(1, 16 * m**2)
        depth = radius**2 / m
        next_depth = Fraction(1, 2 ** (2 * (m + 1)) * (m + 1))
        assert length >= 8 * radius
        q1 = length // (4 * radius)
        q = Fraction(1) // (4 * radius)
        assert q1 >= length / (8 * radius)
        assert q >= 1 / (8 * radius)
        assert depth / next_depth == Fraction(4 * (m + 1), m)
        assert depth / next_depth <= 8
        for dimension in (2, 3, 5, 10):
            count = q1 * q ** (dimension - 1)
            assert count >= length / (8**dimension * radius**dimension)
    print("PASS: symbolic Hessian and radial/tangential eigenvectors")
    print("PASS: 1,001 exact rational eigenvalue samples")
    print("PASS: packing and depth inequalities for m=16..300, n=2,3,5,10")


if __name__ == "__main__":
    main()
