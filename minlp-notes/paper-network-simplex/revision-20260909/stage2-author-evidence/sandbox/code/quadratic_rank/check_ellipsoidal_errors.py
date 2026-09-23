"""Exact checks for correlated quadratic error budgets and their energies."""

import random

import sympy as sp


rng = random.Random(2026090528)
cases = 0
for n in range(1, 5):
    for m in range(1, 6):
        hessians = []
        for output in range(m):
            raw = sp.Matrix(n, n, lambda i, k: rng.randint(-3, 3))
            hessians.append(raw + raw.T)
        factor = sp.eye(n)
        for i in range(n):
            for k in range(i):
                factor[i, k] = rng.randint(-2, 2)
        covariance = factor * factor.T
        matrices = [factor.T * h * factor for h in hessians]
        # Rectangular factors include singular and correlated PSD budgets.
        budget_factor = sp.Matrix(max(1, m - 1), m,
                                  lambda i, k: rng.randint(-2, 2))
        budget = budget_factor.T * budget_factor
        transformed = [sum((budget_factor[a, j] * matrices[j] for j in range(m)),
                           sp.zeros(n)) for a in range(budget_factor.rows)]
        numerator = sum((budget[j, k] * matrices[j] * matrices[k]
                         for j in range(m) for k in range(m)), sp.zeros(n))
        factor_sum = sum((matrix * matrix for matrix in transformed), sp.zeros(n))
        assert numerator == factor_sum
        assert numerator == numerator.T
        energy = sum(budget[j, k] * sp.trace(hessians[j] * covariance * hessians[k] * covariance)
                     for j in range(m) for k in range(m))
        assert energy == sp.trace(numerator)

        residual = sp.Matrix(n, n, lambda i, k: sp.Rational(rng.choice((-1, 0, 1)), 4 * n))
        residual = (residual + residual.T) / 2
        errors = sp.Matrix([sp.trace(matrix * residual) / 2 for matrix in matrices])
        assert (errors.T * budget * errors)[0] <= energy / 64

        points = [sp.Matrix([rng.randint(-2, 2) for _ in range(n)]) for _ in range(5)]
        mean = sum(points, sp.zeros(n, 1)) / len(points)
        points = [point - mean for point in points]
        sigma = sum((point * point.T for point in points), sp.zeros(n)) / len(points)

        def raw_quadratics(point):
            return sp.Matrix([(point.T * hessian * point)[0] for hessian in hessians])

        values = [raw_quadratics(point) for point in points]
        mean_values = sum(values, sp.zeros(m, 1)) / len(points)
        moment = sum((raw_quadratics(x - y).T * budget * raw_quadratics(x - y))[0] / 4
                     for x in points for y in points) / len(points) ** 2
        covariance_energy = sum(budget[j, k] * sp.trace(hessians[j] * sigma * hessians[k] * sigma)
                                for j in range(m) for k in range(m))
        remainder = sum((value.T * budget * value)[0] for value in values) / (2 * len(points))
        remainder += (mean_values.T * budget * mean_values)[0] / 2
        assert moment == covariance_energy + remainder
        assert remainder >= 0
        cases += 1

print(f'PASS: {cases} exact correlated-budget gradient factorizations, '
      'shared residual bounds, and vector fourth-moment identities')
