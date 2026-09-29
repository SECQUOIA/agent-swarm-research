"""Exact checks for the polynomial optimization examples.

This verifies the example's global gap identity, Farkas elimination, and
one-field output, and a repeated-squaring degree family. It does not
implement the FPT algorithm or verify its uniform arithmetic and
complexity bounds.
"""

import sympy as sp


def main():
    a, u, v, z, t = sp.symbols("a u v z t")
    field_polynomial = 2 * a**3 - 1

    def reduce(expression):
        return sp.rem(sp.Poly(sp.expand(expression), a),
                      sp.Poly(field_polynomial, a)).as_expr()

    # a is the unique positive root, isolated by rational endpoints.
    assert field_polynomial.subs(a, sp.Rational(3, 4)) < 0
    assert field_polynomial.subs(a, sp.Rational(4, 5)) > 0
    assert sp.Poly(field_polynomial, a).is_irreducible

    objective = z**2 - z + sp.Rational(1, 4) + v - 2*u
    value = sp.Rational(1, 4) - sp.Rational(3, 2)*a
    nonnegative_gap = (
        z*(z - 1) + (v - u**4)
        + (u - a)**2 * ((u + a)**2 + 2*a**2)
    )
    assert reduce(objective - value - nonnegative_gap) == 0
    for integer in range(-20, 21):
        assert (z*(z - 1)).subs(z, integer) >= 0
    for integer in (0, 1):
        assert reduce(objective.subs({z: integer, u: a, v: a/2})
                      - value) == 0
    assert reduce(a**4 - a/2) == 0

    # The sole Farkas vertex is (1/2,1/2): opposite v coefficients.
    rows = [u**4 - v, objective - t]
    projected = u**4 + z**2 - z + sp.Rational(1, 4) - 2*u - t
    assert sp.expand(sum(rows) - projected) == 0
    assert sp.diff(projected, v) == 0
    assert sp.hessian(projected, (z, u, t)) == sp.diag(2, 12*u**2, 0)

    value_polynomial = 64*t**3 - 48*t**2 + 12*t + 107
    fiber_polynomial = 16*t**3 - 1
    assert reduce(value_polynomial.subs(t, value)) == 0
    assert reduce(fiber_polynomial.subs(t, a/2)) == 0
    assert sp.Poly(value_polynomial, t).is_irreducible
    assert sp.Poly(fiber_polynomial, t).is_irreducible

    # Explicit inverse maps show all three coordinates generate one field.
    assert sp.expand(sp.Rational(2, 3)*(sp.Rational(1, 4) - value)) == a
    assert 2*(a/2) == a
    # A repeated-squaring family has exact algebraic degree 2**r-1.
    # Eisenstein is checked directly, rather than inferred numerically.
    for dimension in range(1, 9):
        power = 2**dimension
        defining = sp.Poly(a**(power - 1) - 2, a)
        coefficients = defining.all_coeffs()
        assert coefficients[0] == 1
        assert all(coefficient % 2 == 0 for coefficient in coefficients[1:])
        assert coefficients[-1] % 4 != 0
        reduced_objective = a**power - 2*power*a
        assert sp.expand(sp.diff(reduced_objective, a)
                         - power*defining.as_expr()) == 0
        assert sp.expand(reduced_objective + 2*(power - 1)*a
                         - a*defining.as_expr()) == 0
        assert (2*power).bit_length() == dimension + 2
        hessians = [sp.diag(*[2 if j == i else 0
                             for j in range(dimension)])
                    for i in range(dimension)]
        assert sp.Matrix.vstack(*hessians).rank() == dimension

    print("PASS: quartic global gap identity; 41 integer gap checks; "
          "two optimal integer assignments; exact Farkas projection; "
          "three irreducible cubic encodings in one field; "
          "eight Eisenstein repeated-squaring instances")


if __name__ == "__main__":
    main()
