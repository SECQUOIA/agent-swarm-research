"""Exact, finite stress checks for the quadratic perturbation multiplier review.

These examples check identities and rational arithmetic, not the universal theorem.
Run from the repository root with:
    python research-20260927/check_quadratic_perturbation_multiplier_review.py
"""

import sympy as sp


def assert_zero(expression):
    assert sp.expand(expression) == 0


def assert_positive_definite(matrix):
    left, diagonal = matrix.LDLdecomposition(hermitian=False)
    assert left * diagonal * left.T == matrix
    assert all(pivot > 0 for pivot in diagonal.diagonal())
    return left, diagonal


def binary_squares(weight):
    numerator, denominator = sp.fraction(weight)
    integer = int(numerator * denominator)
    scalars = []
    exponent = 0
    while integer:
        if integer & 1:
            scalar = sp.Rational(2 ** (exponent // 2), denominator)
            scalars.extend([scalar] * (1 if exponent % 2 == 0 else 2))
        integer >>= 1
        exponent += 1
    assert sum(scalar**2 for scalar in scalars) == weight
    return scalars


def check_case(name, variables, quadratics, hessian, linear, constant,
               coordinates, target_matrices, target_linears, target_constants,
               perturbations):
    """The first baseline factor is the supplied coercive quadratic G."""
    x_vector = sp.Matrix(variables)
    n, m = len(variables), len(quadratics)
    w = sp.Matrix([multiplier * q for multiplier in [1, *variables]
                   for q in quadratics])
    d = len(w)
    g = sp.eye(d)[:, 0]
    u_matrix = sp.zeros(d, n)
    for j in range(n):
        u_matrix[(j + 1) * m, j] = 1
    g_polynomial = quadratics[0]
    assert_zero(g_polynomial - (x_vector.T * hessian * x_vector)[0]
                - (linear.T * x_vector)[0] - constant)
    a_matrix = sp.Matrix.hstack(*coordinates)
    targets = a_matrix.T * w
    a_block = sp.zeros(d, d)
    cross_blocks = []
    lower_vectors = []
    for index, a_vector in enumerate(coordinates):
        t_matrix = target_matrices[index]
        r_vector = target_linears[index]
        s_constant = target_constants[index]
        target = targets[index]
        assert_zero(target - (x_vector.T * t_matrix * x_vector)[0]
                    - (r_vector.T * x_vector)[0] - s_constant)
        lower = x_vector * target
        lower_vectors.append(lower)
        assert_zero((lower.T * hessian * lower)[0]
                    + target * (linear.T * lower)[0] + constant * target**2
                    - ((x_vector * g_polynomial).T * t_matrix * lower)[0]
                    - g_polynomial * (r_vector.T * lower)[0]
                    - s_constant * g_polynomial * target)
        a_block += (constant * a_vector * a_vector.T
                    - sp.Rational(s_constant, 2)
                    * (g * a_vector.T + a_vector * g.T))
        cross_blocks.append((a_vector * linear.T - u_matrix * t_matrix
                             - g * r_vector.T) / 2)
    cross = sp.Matrix.hstack(*cross_blocks)
    lower_block = sp.kronecker_product(sp.eye(len(coordinates)), hessian)
    vector = sp.Matrix.vstack(w, *lower_vectors)
    zero_gram = a_block.row_join(cross).col_join(
        cross.T.row_join(lower_block))
    assert_zero((vector.T * zero_gram * vector)[0])
    eta = hessian.det() / sp.trace(hessian)**(n - 1)
    epsilon = min(sp.Integer(1),
                  1 / (2 * (1 + sum(abs(entry) for entry in a_block))),
                  eta / (4 * (1 + sum(entry**2 for entry in cross))))
    q_matrix = (sp.eye(d) + epsilon * a_block).row_join(
        epsilon * cross).col_join(
        (epsilon * cross.T).row_join(epsilon * lower_block))
    assert_positive_definite(q_matrix)
    radial = 1 + sum(variable**2 for variable in variables)
    baseline = sum(q**2 for q in quadratics)
    assert_zero((vector.T * q_matrix * vector)[0] - radial * baseline)
    delta = q_matrix.det() / sp.trace(q_matrix)**(q_matrix.rows - 1)
    for j_matrix in perturbations:
        d_matrix = sp.diag(a_matrix * j_matrix * a_matrix.T,
                           sp.kronecker_product(j_matrix, sp.eye(n)))
        perturbation = (targets.T * j_matrix * targets)[0]
        assert_zero((vector.T * d_matrix * vector)[0] - radial * perturbation)
        row_bound = max(sum(abs(d_matrix[i, j]) for j in range(d_matrix.cols))
                        for i in range(d_matrix.rows))
        scaling = sp.ceiling((1 + row_bound) / delta)
        certificate = scaling * q_matrix - d_matrix
        assert_positive_definite(certificate - sp.eye(certificate.rows))
        left, diagonal = assert_positive_definite(certificate)
        factors = left.T * vector
        square_count = 0
        square_sum = 0
        for weight, factor in zip(diagonal.diagonal(), factors):
            scalars = binary_squares(weight)
            square_count += len(scalars)
            square_sum += sum(scalar**2 for scalar in scalars) * factor**2
        assert_zero(square_sum - radial * (scaling * baseline - perturbation))
        print(f"PASS: {name}; det(J)={j_matrix.det()}; "
              f"Gram dimension={q_matrix.rows}; epsilon={epsilon}; "
              f"scaling bits={int(scaling).bit_length()}; "
              f"rational squares={square_count}")


def main():
    x, y = sp.symbols("x y")
    hessian = sp.Matrix([[2, 1], [1, 3]])
    linear = sp.Matrix([5, -7])
    g_polynomial = 2*x*x + 2*x*y + 3*y*y + 5*x - 7*y - 11
    coordinates = [sp.zeros(9, 1), sp.zeros(9, 1)]
    coordinates[0][1] = 1
    coordinates[0][5] = 1
    coordinates[0][7] = -1
    coordinates[1][1] = -3
    coordinates[1][2] = 2
    coordinates[1][5] = 1
    coordinates[1][7] = -1
    check_case("two inhomogeneous quadratic targets", [x, y],
               [g_polynomial, x*x-y-1, x*y-x+2], hessian, linear, -11,
               coordinates, [sp.diag(0, 1), sp.Matrix([[-4, 1], [1, 1]])],
               [sp.Matrix([2, 0]), sp.Matrix([0, 4])], [-1, 7],
               [sp.eye(2), sp.Matrix([[2, 3], [3, -5]])])
    check_case("zero, constant, and linear targets", [x], [x*x+3*x-2, 1],
               sp.Matrix([[1]]), sp.Matrix([3]), -2,
               [sp.zeros(4, 1), sp.eye(4)[:, 1], sp.eye(4)[:, 3]],
               [sp.zeros(1), sp.zeros(1), sp.zeros(1)],
               [sp.Matrix([0]), sp.Matrix([0]), sp.Matrix([1])], [0, 1, 0],
               [sp.eye(3)])


if __name__ == "__main__":
    main()
