"""Exact rational checks for compression to the quadratic output image."""

import random

import sympy as sp

rng = random.Random(2026090552)
cases = 0
for n in range(1, 5):
    pairs = [(i, j) for i in range(n) for j in range(i, n)]
    size = len(pairs)
    for m in (1, 3, 7, 12):
        for nominal_rank in (1, min(m, size)):
            first = sp.Matrix(m, nominal_rank, lambda i, j: rng.randint(-2, 2))
            second = sp.Matrix(nominal_rank, size, lambda i, j: rng.randint(-2, 2))
            coefficients = first * second
            columns = coefficients.columnspace()
            if not columns:
                assert coefficients == sp.zeros(m, size)
                continue
            basis = sp.Matrix.hstack(*columns)
            left_inverse = (basis.T * basis).inv() * basis.T
            compressed = left_inverse * coefficients
            assert basis * compressed == coefficients
            assert left_inverse * basis == sp.eye(basis.cols)
            assert basis.cols <= n * (n + 1) // 2

            def hessians(matrix):
                result = []
                for row in range(matrix.rows):
                    hessian = sp.zeros(n)
                    for k, (i, j) in enumerate(pairs):
                        if i == j:
                            hessian[i, j] = 2 * matrix[row, k]
                        else:
                            hessian[i, j] = hessian[j, i] = matrix[row, k]
                    result.append(hessian)
                return result

            original_h = hessians(coefficients)
            compressed_h = hessians(compressed)
            for j, hessian in enumerate(original_h):
                assert hessian == sum((basis[j, k] * compressed_h[k]
                                       for k in range(basis.cols)), sp.zeros(n))
            raw = sp.Matrix(n, n, lambda i, j: rng.randint(-2, 2))
            covariance = raw * raw.T + sp.eye(n)
            budget_factor = sp.Matrix(m + 1, m, lambda i, j: rng.randint(-2, 2))
            budget = budget_factor.T * budget_factor
            effective_budget = basis.T * budget * basis
            original_energy = sum(budget[j, k] * sp.trace(original_h[j] * covariance * original_h[k] * covariance)
                                  for j in range(m) for k in range(m))
            compressed_energy = sum(effective_budget[j, k] * sp.trace(compressed_h[j] * covariance * compressed_h[k] * covariance)
                                    for j in range(basis.cols) for k in range(basis.cols))
            assert original_energy == compressed_energy
            residual = sp.Matrix([sp.Rational(rng.randint(-3, 3), 16) for _ in pairs])
            original_error = coefficients * residual
            compressed_error = compressed * residual
            assert original_error == basis * compressed_error
            assert (original_error.T * budget * original_error)[0] == (compressed_error.T * effective_budget * compressed_error)[0]
            cases += 1

print(f'PASS: {cases} exact effective-image decompositions, Hessian reconstructions, '
      'covariance energies, and shared-error budget identities')
