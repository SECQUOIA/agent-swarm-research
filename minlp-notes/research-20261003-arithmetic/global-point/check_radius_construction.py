#!/usr/bin/env python3
"""Exact finite diagnostics for the integrated-Hessian radius proof.

Fixtures have convexity and optimizers justified by their displayed form.
This is not a general optimizer, convexity recognizer, or proof checker.
Only elementary polynomial/matrix helpers are reused from the cubic checks.
"""

from collections import Counter
from fractions import Fraction as F
from itertools import product
from math import lcm, prod
from pathlib import Path
from runpy import run_path


ROOT = Path(__file__).resolve().parents[2]
HELPERS = run_path(str(ROOT / "research-20261002/new-direction/check_convex_cubic_point_oracle.py"))
poly_add = HELPERS["poly_add"]
poly_scale = HELPERS["poly_scale"]
poly_mul = HELPERS["poly_mul"]
poly_power = HELPERS["poly_power"]
variable = HELPERS["variable"]
constant = HELPERS["constant"]
derivative = HELPERS["derivative"]
evaluate = HELPERS["evaluate"]
dot = HELPERS["dot"]
matvec = HELPERS["matvec"]
quadratic = HELPERS["quadratic"]
psd = HELPERS["psd"]
rowspace_projection = HELPERS["rowspace_projection"]


def integral(polynomial):
    return sum((coefficient / prod(power + 1 for power in powers)
                for powers, coefficient in polynomial.items()), F(0))


def norm1(vector):
    return sum(map(abs, vector), F(0))


def matrix_max(matrix):
    return max((abs(value) for row in matrix for value in row), default=F(0))


def integrated_quadratic(polynomial, n, degree):
    k = (degree + 1) * degree ** (degree + 2)
    coordinates = [variable(n, i) for i in range(n)]
    gradient = [derivative(polynomial, i) for i in range(n)]
    hessian = [[derivative(gradient[i], j) for j in range(n)] for i in range(n)]
    matrix = tuple(tuple(integral(entry) for entry in row) for row in hessian)
    ha = [poly_add(*(poly_mul(hessian[i][j], coordinates[j]) for j in range(n)))
          for i in range(n)]
    linear = tuple(integral(poly_add(gradient[i], poly_scale(ha[i], F(-2, k))))
                   for i in range(n))
    scalar = integral(poly_add(
        polynomial,
        *(poly_scale(poly_mul(gradient[i], coordinates[i]), -1) for i in range(n)),
        *(poly_scale(poly_mul(coordinates[i], ha[i]), F(1, k)) for i in range(n))))
    return scalar, linear, matrix, k


def interpolation_checks(counts):
    for degree in range(2, 11):
        k = (degree + 1) * degree ** (degree + 2)
        derivative_sum = F(0)
        for node in range(degree + 1):
            basis = {(0,): F(1)}
            denominator = F(1)
            for other in range(degree + 1):
                if other == node:
                    continue
                basis = poly_mul(basis, {(1,): F(1), (0,): F(-other, degree)})
                denominator *= F(node - other, degree)
            second = 2 * basis.get((2,), F(0)) / denominator
            assert abs(second) <= degree ** (degree + 2)
            derivative_sum += abs(second)
        assert derivative_sum <= k
        counts["interpolation degrees"] += 1


def fixtures():
    x = variable(1, 0)
    yield "unconstrained quartic", poly_power(x, 4), 1, 4, [], [], (), (F(2),), (F(0),)
    yield "affine rank zero", poly_scale(x, -3), 1, 2, [(F(1),)], [F(2)], (F(3),), (F(0),), (F(2),)

    x, y, z = (variable(3, i) for i in range(3))
    f = poly_add(poly_power(poly_add(x, y), 4), poly_scale(x, -2), poly_scale(y, 2))
    yield "singular Hessian with free direction", f, 3, 4, [(F(1), F(-1), F(0))], [F(0)], (F(2),), (F(-1), F(1), F(0)), (F(0),) * 3

    x, y = variable(2, 0), variable(2, 1)
    f = poly_add(poly_power(poly_add(x, constant(2, -3)), 4), poly_scale(y, -4))
    yield "nonzero range certificate", f, 2, 4, [(F(-1), F(1))], [F(0)], (F(4),), (F(0), F(0)), (F(4), F(4))
    yield "constant objective", constant(2, 7), 2, 2, [], [], (), (F(1), F(-1)), (F(0), F(0))


def fixture_checks(counts):
    for name, polynomial, n, degree, inequalities, rhs, lam, anchor, optimizer in fixtures():
        c, ell, matrix, k = integrated_quadratic(polynomial, n, degree)
        projection, rank = rowspace_projection(matrix)
        assert psd(matrix), name
        zero = (F(0),) * n
        f0 = evaluate(polynomial, zero)
        g0 = tuple(evaluate(derivative(polynomial, i), zero) for i in range(n))
        w = tuple(pg - g for pg, g in zip(matvec(projection, g0), g0))
        assert tuple(e - pe for e, pe in zip(ell, matvec(projection, ell))) == tuple(-a for a in w), name
        bt_lam = tuple(sum((row[i] * scale for row, scale in zip(inequalities, lam)), F(0))
                       for i in range(n))
        v = tuple(a - b for a, b in zip(w, bt_lam))
        assert matvec(projection, v) == v, name
        assert all(scale >= 0 for scale in lam), name
        denominator = lcm(*(value.denominator for row in matrix for value in row))
        spectral_upper = n * max(F(1), denominator * matrix_max(matrix))
        rho = F(1, k * denominator * int(spectral_upper) ** (n - 1))
        residual_matrix = [[matrix[i][j] - k * rho * projection[i][j] for j in range(n)] for i in range(n)]
        assert psd(residual_matrix), name

        objective_anchor = evaluate(polynomial, anchor)
        beta = c - dot(lam, rhs)
        a_coefficient = norm1(tuple(a - b for a, b in zip(matvec(projection, ell), v)))
        t_bound = 1 + (a_coefficient + abs(objective_anchor - beta) + 1) / rho
        w_bound = 1 + abs(dot(lam, rhs)) + norm1(v) * t_bound + abs(f0) + norm1(g0) * t_bound + abs(objective_anchor)
        q_denominator = lcm(*(value.denominator for row in (*matrix, w) for value in row))
        invariant_matrix = tuple(tuple(q_denominator * value for value in row) for row in (*matrix, w))
        coefficient_bound = max(F(1), matrix_max(invariant_matrix), matrix_max(inequalities))
        hoffman = (n * coefficient_bound) ** (n - 1)
        radius = 1 + norm1(anchor) + hoffman * (norm1(matvec(invariant_matrix, anchor))
                 + q_denominator * (n * n * matrix_max(matrix) * t_bound + w_bound))
        assert all(dot(row, anchor) <= bound for row, bound in zip(inequalities, rhs)), name
        assert all(dot(row, optimizer) <= bound for row, bound in zip(inequalities, rhs)), name
        assert dot(optimizer, optimizer) <= radius * radius, name

        grid = (F(-4), F(-1), F(0), F(1, 2), F(1), F(4), F(7))
        for point in product(grid, repeat=n):
            objective = evaluate(polynomial, point)
            lower = c + dot(ell, point) + quadratic(matrix, point) / k
            assert objective >= lower, (name, point)
            projected = matvec(projection, point)
            assert objective == evaluate(polynomial, projected) - dot(w, point), (name, point)
            counts["quadratic and affine decomposition checks"] += 1
            if all(dot(row, point) <= bound for row, bound in zip(inequalities, rhs)) and objective <= objective_anchor:
                assert dot(projected, projected) <= t_bound * t_bound, (name, point)
                assert abs(dot(w, point)) <= w_bound, (name, point)
                assert norm1(matvec(invariant_matrix, point)) <= q_denominator * (n * n * matrix_max(matrix) * t_bound + w_bound), (name, point)
                counts["sublevel invariant checks"] += 1

        if name == "unconstrained quartic":
            assert matrix == ((F(4),),)
            assert ell == (1 - F(6, k),)
            assert c == F(-3, 5) + F(12, 5 * k)
            counts["closed-form integration checks"] += 1
        if name == "singular Hessian with free direction":
            far_point = (F(-1), F(1), 10 * radius)
            representative = (F(-1), F(1), F(0))
            assert dot(far_point, far_point) > radius * radius
            assert matvec(invariant_matrix, far_point) == matvec(invariant_matrix, representative)
            assert evaluate(polynomial, far_point) == evaluate(polynomial, representative)
            assert dot(representative, representative) <= radius * radius
            counts["bounded representative, unbounded sublevel checks"] += 1
        counts["radius fixtures"] += 1


def source_and_unboundedness_checks(counts):
    # Hesse's Redemption v1, equation (22): the absolute value is invalid.
    point = (F(0), F(-1))
    w = (F(0), F(1))
    lam, b = F(1), F(0)
    assert point[1] <= b
    assert dot(w, point) <= lam * b
    assert abs(dot(w, point)) == 1 > abs(lam) * abs(b)
    counts["source absolute-value counterexample"] += 1

    # A common-kernel recession direction gives exact linear decrease.
    x, y = variable(2, 0), variable(2, 1)
    polynomial = poly_add(poly_power(x, 4), poly_scale(y, -2))
    _, _, matrix, _ = integrated_quadratic(polynomial, 2, 4)
    direction = (F(0), F(1))
    assert matvec(matrix, direction) == (F(0), F(0))
    assert dot((F(0), F(-1)), direction) <= 0
    assert dot((F(0), F(2)), direction) > 0
    for t in (F(1), F(3), F(100)):
        assert evaluate(polynomial, (F(0), t)) == -2 * t
    counts["unboundedness certificate"] += 1


def main():
    counts = Counter()
    interpolation_checks(counts)
    fixture_checks(counts)
    source_and_unboundedness_checks(counts)
    print("PASS: " + "; ".join(f"{value} {name}" for name, value in counts.items()))
    print("Scope: exact finite diagnostics; no generic optimizer, convexity recognition, or external proof validation.")


if __name__ == "__main__":
    main()
