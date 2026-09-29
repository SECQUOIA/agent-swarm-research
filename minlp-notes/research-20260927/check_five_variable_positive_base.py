"""Exact arithmetic and ideal checks for the five-variable base analysis."""

import sympy as sp


def contribution(dimension, degree, normal_degrees):
    h = sp.Symbol("h")
    quotient = (1 + 2 * h) ** 5 / sp.prod(1 + d * h for d in normal_degrees)
    coefficient = sp.series(quotient, h, 0, dimension + 1).removeO().coeff(h, dimension)
    return degree * coefficient


def ideal_intersection(first, second, variables, domain=sp.QQ):
    parameter = sp.Dummy("parameter")
    groebner = sp.groebner(
        [parameter * f for f in first] + [(1 - parameter) * f for f in second],
        parameter, *variables, domain=domain,
    )
    return [p.as_expr() for p in groebner.polys if not p.as_expr().has(parameter)]


def assert_same_ideal(first, second, variables, domain=sp.QQ):
    gb_first = sp.groebner(first, *variables, domain=domain)
    gb_second = sp.groebner(second, *variables, domain=domain)
    assert all(gb_first.reduce(f)[1] == 0 for f in second)
    assert all(gb_second.reduce(f)[1] == 0 for f in first)


def main():
    cases = {
        "conic": contribution(1, 2, [1, 1, 1, 2]),
        "two skew lines": 2 * contribution(1, 1, [1, 1, 1, 1]),
        "quartic CI": contribution(1, 4, [1, 1, 2, 2]),
        # Normal degree of a rational normal quartic in P5 is 3*6+4.
        "rational normal quartic": 10 * 4 - (3 * 6 + 4),
        "two disjoint conics in the allowed plane positions":
            2 * contribution(1, 2, [1, 1, 1, 2]),
        "quadric surface": contribution(2, 2, [1, 1, 2]),
        "two disjoint planes": 2 * contribution(2, 1, [1, 1, 1]),
    }
    expected_residual = [22, 20, 16, 14, 12, 10, 0]
    assert [32 - cost for cost in cases.values()] == expected_residual
    assert all(cost >= 10 for cost in cases.values())

    # Two conics whose planes meet at an external point in P4.
    x = sp.symbols("x0:5")
    x0, x1, x2, x3, x4 = x
    first = [x3, x4, x0**2 + x1**2 + x2**2]
    second = [x1, x2, x0**2 + x3**2 + x4**2]
    actual = ideal_intersection(first, second, x)
    proposed = [x1*x3, x1*x4, x2*x3, x2*x4, sum(t**2 for t in x)]
    assert_same_ideal(actual, proposed, x)

    # Actual conjugate planes meeting in a real line: their conics meet
    # at the two nonreal points x0^2+x1^2=0 on that line.
    y = sp.symbols("y0:4")
    y0, y1, y2, y3 = y
    conic = y0**2 + y1**2 + y2**2
    first = [y2 + sp.I*y3, conic]
    second = [y2 - sp.I*y3, conic]
    gaussian_field = sp.QQ.algebraic_field(sp.I)
    actual = ideal_intersection(first, second, y, domain=gaussian_field)
    assert_same_ideal(actual, [y2**2 + y3**2, conic], y, domain=gaussian_field)

    for (name, cost), residual in zip(cases.items(), expected_residual):
        print(f"{name}: contribution {cost}, residual bound {residual}")
    print("Conic union ideals: external point and conjugate line-intersection checks passed")


if __name__ == "__main__":
    main()
