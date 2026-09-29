"""Exact interface checks for strict Farkas projection and shallow cuts.

This checks selected rational identities and boundary cases. It is not an
implementation of the ellipsoid/lattice algorithm or a runtime verification.
"""

import sympy as sp


def dyadic_below_square_root(value):
    power = 0
    while sp.Rational(2)**(2*power) > value:
        power -= 1
    while sp.Rational(2)**(2*(power+1)) <= value:
        power += 1
    result = sp.Rational(2)**power
    assert result**2 <= value <= 4*result**2
    return result


def integer_section_matrix(direction):
    """Construct U with d^T U=e_last^T by exact extended-gcd operations."""
    row = sp.Matrix([direction])
    dimension = len(direction)
    transform = sp.eye(dimension)
    for j in range(1, dimension):
        current = row*transform
        a, b = current[0], current[j]
        if a == 0 and b == 0:
            continue
        s, t, common = sp.gcdex(a, b)
        operation = sp.eye(dimension)
        operation[0, 0], operation[0, j] = s, -b/common
        operation[j, 0], operation[j, j] = t, a/common
        transform = transform*operation
    swap = sp.eye(dimension)
    swap.col_swap(0, dimension-1)
    transform = transform*swap
    expected = sp.zeros(1, dimension)
    expected[dimension-1] = 1
    assert row*transform == expected
    assert abs(transform.det()) == 1
    assert all(value.is_Integer for value in transform)
    assert all(value.is_Integer for value in transform.inv())
    return transform


def main():
    y, w = sp.symbols("y w", real=True)
    p1, p2 = y**4 - 1, y - 1
    projected = (p1+p2)/2
    sigma = -projected
    fiber_point = (p2-p1)/2
    assert sp.expand(fiber_point+p1+sigma) == 0
    assert sp.expand(-fiber_point+p2+sigma) == 0
    # Adding the two primal rows bounds every feasible sigma above by
    # -(p1+p2)/2; the displayed point attains that bound.
    assert sp.expand(2*projected-(p1+p2)) == 0
    derivative = sp.diff(projected, y)
    assert sp.diff(projected, y, 2) == 6*y**2

    queries = [sp.Rational(j, 4) for j in range(-12, 13)]
    feasible = [x for x in queries if projected.subs(y, x) < 0]
    infeasible = [x for x in queries if projected.subs(y, x) >= 0]
    cut_checks = 0
    for query in queries:
        assert (sigma.subs(y, query) > 0) == (projected.subs(y, query) < 0)
    for query in infeasible:
        normal = derivative.subs(y, query)
        assert normal != 0
        for point in feasible:
            assert normal*(point-query) < 0
            cut_checks += 1
    assert sigma.subs(y, 1) == 0  # A boundary point is not a strict member.

    # Integer affine recursion preserves the exact polynomial, its integer
    # coefficients after denominator clearing, and convexity.
    transformed = sp.Poly(sp.expand(2*projected.subs(y, 3*w+1)), w)
    assert all(coefficient.is_Integer for coefficient in transformed.all_coeffs())
    assert sp.expand(sp.diff(transformed.as_expr(), w, 2)-108*(3*w+1)**2) == 0

    # Zero gradient at a violated convex row certifies strict emptiness.
    for polynomial in [y**2, y**2+1]:
        assert sp.diff(polynomial, y).subs(y, 0) == 0
        assert polynomial.subs(y, 0) >= 0
    assert sp.Rational(1, 2)**2 > 0
    assert sp.Rational(1, 2)**2-1 < 0  # Weak-row oracle cannot be reused.

    ellipsoid_checks = 0
    for dimension in range(1, 6):
        lower = sp.eye(dimension)
        for i in range(dimension):
            for j in range(i):
                lower[i, j] = (i+2*j+1) % 5-2
        diagonal = [sp.Rational(2*i+1, i+2) for i in range(dimension)]
        matrix = lower*sp.diag(*diagonal)*lower.T
        inverse = matrix.inv()
        columns = []
        for i, value in enumerate(diagonal):
            scale = dyadic_below_square_root(value)
            vector = lower[:, i]*scale
            norm_squared = (vector.T*inverse*vector)[0]
            assert sp.simplify(norm_squared-scale**2/value) == 0
            assert sp.Rational(1, 4) <= norm_squared <= 1
            point = vector/(dimension+1)
            assert (point.T*inverse*point)[0] <= sp.Rational(1, (dimension+1)**2)
            columns.append(vector)
            ellipsoid_checks += 2
        # The cross-polytope contains its stated smaller ellipsoid because
        # the diagonal coordinate factors have inverse squared at most 4.
        cross_basis = sp.Matrix.hstack(*columns)
        transformed_shape = cross_basis.inv()*matrix*cross_basis.inv().T
        assert transformed_shape.is_diagonal()
        assert all(1 <= transformed_shape[i, i] <= 4 for i in range(dimension))

    directions = [[1, 1], [2, 3, 5], [-7, 11, 13, 4], [3, 6, 10]]
    for direction in directions:
        transform = integer_section_matrix(direction)
        parameter = sp.Matrix(list(range(len(direction)-1))+[7])
        assert (sp.Matrix([direction])*transform*parameter)[0] == 7
    # A unimodular basis merely containing d as its last column need not
    # parameterize the hyperplanes normal to d.
    wrong = sp.Matrix([[1, 1], [0, 1]])
    assert wrong.det() == 1 and wrong[:, 1] == sp.Matrix([1, 1])
    assert sp.Matrix([[1, 1]])*wrong != sp.Matrix([[0, 1]])

    print(f"PASS: {len(queries)} strict projection queries; {cut_checks} exact cuts; "
          f"{ellipsoid_checks} rational ellipsoid test points; "
          f"{len(directions)} integer section maps; "
          "boundary, zero-gradient, and affine-recursion identities")


if __name__ == "__main__":
    main()
