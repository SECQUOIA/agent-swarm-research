"""Exact small fixtures for the joint finite-critical-limit construction.

This is a diagnostic, not the proposed general component solver.  All
calculations use rational polynomials.  No numerical eigenvalues are used.
"""

from functools import lru_cache

import sympy as sp


Z, T, U = sp.symbols("z T u")
COUNTS = {"systems": 0, "forms": 0, "finite_limits": 0, "matrix_relations": 0}


def quotient_matrices(f, variables, deformation_degree):
    """Memoized total-degree reductions for monic coprime-power equations."""
    a = deformation_degree - 1
    r = len(variables)
    basis = list(__import__("itertools").product(range(a), repeat=r))
    indices = {monomial: i for i, monomial in enumerate(basis)}
    derivatives = [sp.Poly(sp.diff(f, x), *variables) for x in variables]

    @lru_cache(None)
    def normal_form(exponent):
        if all(e < a for e in exponent):
            return {exponent: sp.Integer(1)}
        i = next(i for i, e in enumerate(exponent) if e >= a)
        reduced = list(exponent)
        reduced[i] -= a
        result = {}
        for powers, coefficient in derivatives[i].terms():
            if coefficient == 0:
                continue
            target = tuple(e + p for e, p in zip(reduced, powers))
            assert sum(target) < sum(exponent)
            for monomial, value in normal_form(target).items():
                result[monomial] = result.get(monomial, 0) - (
                    Z * coefficient * value / deformation_degree
                )
        return {key: sp.expand(value) for key, value in result.items() if value != 0}

    matrices = []
    for coordinate in range(r):
        matrix = sp.zeros(len(basis))
        for column, powers in enumerate(basis):
            raised = list(powers)
            raised[coordinate] += 1
            for monomial, value in normal_form(tuple(raised)).items():
                matrix[indices[monomial], column] = value
        matrices.append(matrix)

    identity = sp.eye(len(basis))
    for i, matrix in enumerate(matrices):
        relation = matrix**a
        for powers, coefficient in derivatives[i].terms():
            monomial = identity
            for other, power in zip(matrices, powers):
                monomial = monomial * other**power
            relation += Z * coefficient * monomial / deformation_degree
        assert relation.applyfunc(sp.expand) == sp.zeros(len(basis))
        COUNTS["matrix_relations"] += 1
        for other in matrices[:i]:
            assert (matrix * other - other * matrix).applyfunc(sp.expand).is_zero_matrix
    COUNTS["systems"] += 1
    return matrices


def leading_coefficient_z(polynomial, degree=None):
    polynomial = sp.Poly(polynomial, Z)
    if degree is None:
        degree = polynomial.degree()
    return sp.expand(polynomial.nth(degree))


def extract(matrices, weights):
    """Return the candidate univariate representation, or a skip reason."""
    n = matrices[0].rows
    combined = sp.zeros(n)
    for weight, matrix in zip(weights, matrices):
        combined += weight * matrix
    characteristic = combined.charpoly(T).as_expr()

    # adj(TI-M)=sum_j B_j T^(n-1-j), B_0=I, B_j=M B_(j-1)+c_j I.
    # This independently computes -d/dlambda_i det(TI-M_lambda).
    coefficients = sp.Poly(characteristic, T).all_coeffs()
    adjugate_coefficient = sp.eye(n)
    derivatives = [sp.Integer(0) for _ in matrices]
    for j in range(n):
        for i, matrix in enumerate(matrices):
            derivatives[i] += sp.trace(adjugate_coefficient * matrix) * T ** (n - 1 - j)
        adjugate_coefficient = (
            combined * adjugate_coefficient + coefficients[j + 1] * sp.eye(n)
        ).applyfunc(sp.expand)
    derivatives = list(map(sp.expand, derivatives))

    degree = sp.degree(characteristic, Z)
    p = leading_coefficient_z(characteristic, degree)
    COUNTS["forms"] += 1
    if sp.degree(p, T) == 0:
        return "constant", characteristic, derivatives
    if any(sp.degree(q, Z) > degree for q in derivatives):
        return "degree", characteristic, derivatives
    b = [leading_coefficient_z(q, degree) for q in derivatives]
    gcd = sp.gcd(p, sp.diff(p, T))
    if any(sp.rem(q, gcd, T) != 0 for q in b):
        return "divisibility", characteristic, derivatives
    squarefree = sp.div(p, gcd, T)[0]
    denominator = sp.div(sp.diff(p, T), gcd, T)[0]
    assert sp.degree(sp.gcd(squarefree, denominator), T) == 0
    inverse = sp.invert(denominator, squarefree, T)
    coordinates = [sp.rem(sp.div(q, gcd, T)[0] * inverse, squarefree, T) for q in b]
    return (squarefree, coordinates), characteristic, derivatives


def has_limit(representation, weights, point):
    assert not isinstance(representation, str), representation
    polynomial, coordinates = representation
    projected = sum(w * x for w, x in zip(weights, point))
    assert sp.simplify(polynomial.subs(T, projected)) == 0
    assert all(sp.simplify(r.subs(T, projected) - x) == 0 for r, x in zip(coordinates, point))
    COUNTS["finite_limits"] += 1


def main():
    x, y = sp.symbols("x y")

    # Nonradical stationary quotient: all nine algebraic branches are zero.
    matrices = quotient_matrices(sp.Integer(0), (x, y), 4)
    representation, characteristic, _ = extract(matrices, (1, 2))
    assert characteristic == T**9
    has_limit(representation, (1, 2), (0, 0))

    # Positive-dimensional original critical set, made finite by deformation.
    matrices = quotient_matrices((x - y) ** 2, (x, y), 4)
    representation, _, _ = extract(matrices, (1, 2))
    has_limit(representation, (1, 2), (0, 0))

    # Only one finite limit, while eight stationary branches escape.
    target = (sp.Rational(1, 3), sp.Rational(2, 5))
    matrices = quotient_matrices((x - target[0]) ** 2 + (y - target[1]) ** 2, (x, y), 4)
    # One bad form yields a harmless feasible spurious point; another hides
    # cancelling poles and must fail the multiplicity divisibility check.
    bad_representation, _, _ = extract(matrices, (1, 0))
    assert bad_representation[1] == [sp.Rational(1, 3), 0]
    assert (target[1] - bad_representation[1][1]) ** 2 > 0
    assert extract(matrices, (1, 1))[0] == "divisibility"
    representation, _, _ = extract(matrices, (1, 2))
    has_limit(representation, (1, 2), target)

    # Two distinct finite limits from a cubic, plus one escaping branch.
    matrices = quotient_matrices(x**3 - 3 * x, (x,), 4)
    representation, characteristic, derivatives = extract(matrices, (1,))
    has_limit(representation, (1,), (-1,))
    has_limit(representation, (1,), (1,))
    # Check the adjugate derivative against an independent symbolic determinant.
    direct = -sp.diff((T * sp.eye(3) - (1 + U) * matrices[0]).det(), U).subs(U, 0)
    assert sp.expand(direct - derivatives[0]) == 0

    # A linear objective has no finite free stationary limit; endpoints suffice.
    matrices = quotient_matrices(x, (x,), 2)
    assert extract(matrices, (1,))[0] == "constant"

    # A repeated finite limit survives squarefree gcd cancellation.
    matrices = quotient_matrices((x - sp.Rational(1, 2)) ** 4, (x,), 6)
    representation, _, _ = extract(matrices, (1,))
    has_limit(representation, (1,), (sp.Rational(1, 2),))

    # A genuinely algebraic optimizer: include both zero-dimensional faces
    # and every reconstructed real stationary limit on the free face.
    f = x**3 - 2 * x
    matrices = quotient_matrices(f, (x,), 4)
    representation, _, _ = extract(matrices, (1,))
    p, coordinates = representation
    expected = sp.sqrt(sp.Rational(2, 3))
    has_limit(representation, (1,), (-expected,))
    has_limit(representation, (1,), (expected,))
    candidates = [sp.Integer(-1), sp.Integer(1)]
    candidates.extend(coordinates[0].subs(T, alpha) for alpha in sp.real_roots(p))
    candidates = [candidate for candidate in candidates if -1 <= candidate <= 1]
    winner = min(candidates, key=lambda candidate: f.subs(x, candidate))
    assert sp.simplify(winner - expected) == 0
    assert sp.simplify(f.subs(x, winner) + 4 * sp.sqrt(6) / 9) == 0

    # Objective-value resultant keeps both algebraic coordinates in one field.
    p = T**2 - 2
    r_x, r_y = T, 1 + T
    value = sp.expand(r_x**2 + r_y**2)
    result = sp.resultant(p, U - value, T)
    assert sp.expand(result - (U**2 - 10 * U + 17)) == 0
    assert sp.degree(result, U) == sp.degree(p, T)

    print("Exact primitive-limit diagnostics passed:", COUNTS)


if __name__ == "__main__":
    main()
