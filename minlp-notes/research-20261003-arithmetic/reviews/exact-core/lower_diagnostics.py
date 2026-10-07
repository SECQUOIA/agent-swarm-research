"""Independent exact identities used in the quartic PosSLP lower bound.

These finite checks support the analytic audit in lower-review.md. They do
not establish uniform inequalities, all-input complexity, or novelty.
"""

import sympy as sp


def check_exposing_identity_and_jacobian():
    alpha, t, radicand = sp.symbols("alpha t radicand")
    for n in range(2, 7):
        degree = 2 * n - 1
        variables = sp.symbols(f"x1:{n + 1}")
        local = (sp.Integer(1),) + variables
        ell = sp.Matrix([local[j + 1] - alpha * local[j] for j in range(n)])
        matrix = sp.zeros(n)
        for j in range(n):
            matrix[j, j] = alpha ** (degree - 1 - 2 * j)
            if j + 1 < n:
                matrix[j, j + 1] = matrix[j + 1, j] = (
                    alpha ** (degree - 2 - 2 * j) / 2
                )
        exposing = (ell.T * matrix * ell)[0]
        power_curve = {variables[j]: t ** (j + 1) for j in range(n)}
        assert sp.expand(exposing.subs(power_curve) - (t - alpha) * (t**degree - alpha**degree)) == 0
        residuals = [variables[0] * variables[j] - variables[j + 1] for j in range(n - 1)]
        residuals.append(variables[n - 2] * variables[n - 1] - radicand)
        jacobian = sp.Matrix(residuals).jacobian(variables)
        root = {variables[j]: alpha ** (j + 1) for j in range(n)}
        assert sp.factor(jacobian.subs(root).det()) == degree * alpha ** (degree - 1)


def check_full_hessian_gram():
    n = 3
    x = sp.Matrix(sp.symbols("x0:3"))
    y = sp.Matrix(sp.symbols("y0:3"))
    center = sp.Matrix([sp.Rational(3, 2), -2, sp.Rational(1, 3)])
    u = x - center
    hessian_parts = [
        (sp.Matrix([1, -2, 3]), sp.Matrix([[3, 1, -1], [1, 4, 2], [-1, 2, 5]]), sp.Rational(2, 3)),
        (sp.Matrix([-2, 1, 4]), sp.Matrix([[0, 1, 0], [1, -1, 2], [0, 2, 0]]), sp.Rational(1, 7)),
    ]
    polynomial = 0
    gram = sp.zeros(n + n * n)
    for b, matrix, weight in hessian_parts:
        polynomial += weight * ((b.T * u)[0] + (u.T * matrix * u)[0]) ** 2
        constant = 2 * b * b.T
        cross = sp.Matrix(n, n * n, lambda i, column: (
            2 * b[column // n] * matrix[i, column % n]
            + 4 * b[i] * matrix[column // n, column % n]
        ))
        vector = sp.Matrix([matrix[k, j] for k in range(n) for j in range(n)])
        quadratic = 8 * vector * vector.T + 4 * sp.kronecker_product(matrix, matrix)
        block = constant.row_join(cross).col_join(cross.T.row_join(quadratic))
        gram += weight * block
    shift = sp.eye(n + n * n)
    shift[n:, :n] = -sp.kronecker_product(center, sp.eye(n))
    gram = shift.T * gram * shift
    basis = y.col_join(sp.kronecker_product(x, y))
    target = (y.T * sp.hessian(polynomial, x) * y)[0]
    assert sp.expand((basis.T * gram * basis)[0] - target) == 0

    # Recover the exact coefficient equations from a perturbed rational matrix.
    groups = {}
    for i in range(len(basis)):
        for j in range(len(basis)):
            key = sp.expand(basis[i] * basis[j])
            groups.setdefault(key, []).append((i, j))
    approximate = gram + sp.eye(len(basis)) / 101
    projected = approximate.copy()
    for positions in groups.values():
        correction = sum(gram[i, j] - approximate[i, j] for i, j in positions) / len(positions)
        for i, j in positions:
            projected[i, j] += correction
    assert sp.expand((basis.T * projected * basis)[0] - target) == 0
    assert projected == projected.T
    old_error = sum(entry**2 for entry in approximate - gram)
    new_error = sum(entry**2 for entry in projected - gram)
    assert new_error <= old_error


def check_tilt():
    xa, xb, ya, yb, kappa = sp.symbols("xa xb ya yb kappa")
    variables = sp.Matrix([xa, xb])
    direction = sp.Matrix([ya, yb])
    perturbation = -(xa - kappa) ** 2 * (xb - kappa)
    basis = sp.Matrix([ya, yb, xa * ya, xa * yb, xb * ya, xb * yb])
    gram = sp.zeros(6)
    gram[0, 0] = gram[0, 1] = gram[1, 0] = 2 * kappa
    gram[0, 4] = gram[4, 0] = -1
    gram[1, 2] = gram[2, 1] = -2
    target = (direction.T * sp.hessian(perturbation, variables) * direction)[0]
    assert sp.expand((basis.T * gram * basis)[0] - target) == 0
    assert sum(entry**2 for entry in gram) == 12 * kappa**2 + 10
    q, t = sp.symbols("q t")
    no_case = q * (t - 2 * t**2 - q / 2)
    margin = q * (t * (sp.Rational(1, 4) - 2 * t) + (t / 2 - q) / 2)
    assert sp.expand(no_case - q * t / 2 - margin) == 0


if __name__ == "__main__":
    check_exposing_identity_and_jacobian()
    check_full_hessian_gram()
    check_tilt()
    print("PASS: exposing/Jacobian identities for odd degrees 3..11, full translated Hessian Gram, rational coefficient projection, and cubic sign tilt")
