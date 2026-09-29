"""Exact finite-example checks for one-parameter singleton spectrahedra.

The checker uses rational principal-minor signs and isolating intervals,
not numerical eigenvalues. It does not prove the universal classification
or the minimum-size lower bound.
"""

from itertools import combinations

import sympy as sp


x = sp.Symbol("x")


def multiplication_matrix(f):
    degree = f.degree()
    columns = []
    for j in range(degree):
        remainder = sp.rem(sp.Poly(x ** (j + 1), x), f)
        columns.append([remainder.nth(i) for i in range(degree)])
    return sp.Matrix.hstack(*(sp.Matrix(column) for column in columns))


def principal_minors(matrix):
    result = []
    for size in range(1, matrix.rows + 1):
        for indices in combinations(range(matrix.rows), size):
            result.append((size, sp.Poly(matrix.extract(indices, indices).det(), x)))
    return result


def sign_at_root(polynomial, f, interval):
    remainder = polynomial.rem(f)
    if remainder.is_zero:
        return 0
    left, right = interval
    if left == right:
        return sp.sign(remainder.eval(left))
    # Irreducibility guarantees that a nonzero remainder does not vanish
    # at any root of f. Refine until its sign is constant on this interval.
    while remainder.count_roots(left, right) != 0 or remainder.eval(left) == 0 or remainder.eval(right) == 0:
        left, right = f.refine_root(left, right, steps=2)
    return sp.sign(remainder.eval((left + right) / 2))


def check_polynomial(expression):
    f = sp.Poly(expression, x, domain=sp.QQ)
    degree = f.degree()
    assert f.is_irreducible
    isolated = f.intervals(eps=sp.Rational(1, 100))
    assert len(isolated) == degree
    assert all(multiplicity == 1 for _, multiplicity in isolated)
    intervals = [interval for interval, _ in isolated]
    matrix = multiplication_matrix(f)
    gram = sp.Matrix(degree, degree, lambda i, j: sp.trace(matrix ** (i + j)))
    assert gram == gram.T
    assert all(gram[:i, :i].det() > 0 for i in range(1, degree + 1))
    assert gram * matrix == matrix.T * gram

    for selected, interval in enumerate(intervals):
        left, right = interval
        if left == right:
            assert degree == 1
            left -= sp.Rational(1, 4)
            right += sp.Rational(1, 4)
        assert f.eval(left) * f.eval(right) < 0
        blocks = [
            (gram * (matrix - x * sp.eye(degree)) * (matrix - r * sp.eye(degree)).inv()).applyfunc(sp.cancel)
            for r in (left, right)
        ]
        assert all(block == block.T for block in blocks)
        minors = [principal_minors(block) for block in blocks]
        product = sp.factor(blocks[0].det() * blocks[1].det())
        factor = sp.cancel(product / f.as_expr() ** 2)
        assert factor.is_Rational and factor < 0
        assert sp.expand(product - factor * f.as_expr() ** 2) == 0

        for candidate, candidate_interval in enumerate(intervals):
            signs = [
                [(size, sign_at_root(minor, f, candidate_interval)) for size, minor in block_minors]
                for block_minors in minors
            ]
            feasible = all(sign >= 0 for block_signs in signs for _, sign in block_signs)
            assert feasible == (candidate == selected)
            if feasible:
                ranks = [max([0] + [size for size, sign in block_signs if sign != 0]) for block_signs in signs]
                assert ranks == [degree - 1, degree - 1]
    return degree


def check_singular_and_simple_root_boundaries():
    # A common zero block makes the determinant identically zero without
    # changing the singleton. The surviving block has a double root.
    singleton = sp.Matrix([[1, x], [x, 0]])
    singular = sp.diag(singleton, sp.zeros(2))
    assert singular.det() == 0
    assert singleton.det() == -x ** 2
    assert singleton.subs(x, 0).rank() == 1
    # A simple root opens a positive-definite side; zero kernel derivative
    # instead gives a double root and can isolate the feasible parameter.
    for beta in (-3, -1, 1, 4):
        pencil = sp.Matrix([[2 + x, 3 * x], [3 * x, beta * x]])
        assert sp.diff(pencil.det(), x).subs(x, 0) == 2 * beta
        point = sp.Rational(sp.sign(beta), 100)
        assert pencil[0, 0].subs(x, point) > 0
        assert pencil.det().subs(x, point) > 0


if __name__ == "__main__":
    count = sum(check_polynomial(f) for f in (
        3 * x - 2,
        x ** 2 - 2,
        3 * x ** 2 - 2,
        x ** 3 - 3 * x + 1,
        x ** 4 - 5 * x ** 2 + 1,
    ))
    check_singular_and_simple_root_boundaries()
    print(f"Passed: {count} exact singleton constructions, singular-pencil and simple-root boundary checks.")
