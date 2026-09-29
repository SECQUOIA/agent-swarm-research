"""Small exact checks of the cube moment bound used in the fresh review.

Run from the repository root with:
    python research-20260927/check_interior_gram_bit_lower_bound_review.py

These finite checks do not prove the bound in arbitrary dimension.
"""

from math import comb

import sympy as sp


def cube_moment(exponents):
    result = sp.Integer(1)
    for exponent in exponents:
        if exponent % 2:
            return sp.Integer(0)
        result /= exponent + 1
    return result


def check_dimension(n):
    unit = [tuple(int(i == j) for j in range(n)) for i in range(n)]
    monomials = [(0,) * n, *unit]
    monomials.extend(tuple(2 * value for value in exponent) for exponent in unit)
    monomials.extend(tuple(unit[i][a] + unit[j][a] for a in range(n))
                     for i in range(n) for j in range(i + 1, n))
    dimension = len(monomials)
    assert dimension == comb(n + 2, 2)
    moment = sp.Matrix(dimension, dimension,
                       lambda i, j: cube_moment(tuple(a + b for a, b in
                                                     zip(monomials[i], monomials[j]))))
    centering = sp.eye(dimension)
    for i in range(n):
        centering[1 + n + i, 0] = -sp.Rational(1, 3)
    weights = ([sp.Integer(1)] + [sp.Rational(1, 3)] * n
               + [sp.Rational(4, 45)] * n
               + [sp.Rational(1, 9)] * comb(n, 2))
    assert centering * moment * centering.T == sp.diag(*weights)
    difference = moment - sp.eye(dimension) / (15 * (n + 1))
    left, diagonal = difference.LDLdecomposition(hermitian=False)
    assert left * diagonal * left.T == difference
    assert all(pivot > 0 for pivot in diagonal.diagonal())
    print(f"PASS: n={n}, D={dimension}; exact centered moments and "
          "B - I/[15(n+1)] positive definite")


if __name__ == "__main__":
    for n in range(1, 5):
        check_dimension(n)
