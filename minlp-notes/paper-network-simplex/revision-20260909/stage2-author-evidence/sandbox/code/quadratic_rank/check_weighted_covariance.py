"""Finite unequal-accuracy covariance law: independent numerical boundary checks."""

import math

import numpy as np
from scipy.optimize import linprog


rng = np.random.default_rng(2026090517)
projected_checks = 0
boundary_checks = 0
graph_checks = 0

for n in range(1, 7):
    for trial in range(12):
        rotation, _ = np.linalg.qr(rng.normal(size=(n, n)))
        eigenvalues = 2.0 ** (-rng.uniform(0, 22, n))
        covariance = (rotation * eigenvalues) @ rotation.T
        widths = np.abs(rotation).sum(axis=0)
        depths = np.ceil(np.log2(widths * np.sqrt(n / eigenvalues))).astype(int)
        steps = widths * 2.0 ** (-depths)
        phi = -np.log2(eigenvalues).sum() / 2
        assert depths.sum() <= phi + n * math.log2(n) + n + 1e-10
        assert np.all(steps <= np.sqrt(eigenvalues / n) * (1 + 1e-12))

        # Check the bounding-box endpoints, including the all-one prefix case.
        for point in (np.zeros(n), np.ones(n), rng.random(n)):
            lower = np.minimum(rotation, 0).sum(axis=0)
            coordinates = rotation.T @ point - lower
            assert np.all(coordinates >= -1e-12)
            assert np.all(coordinates <= widths + 1e-12)
            index = np.minimum(np.floor(coordinates / steps), 2.0 ** depths - 1)
            prefix = steps * index
            residual = coordinates - prefix
            assert np.all(residual >= -1e-12)
            assert np.all(residual <= steps + 1e-12)
            boundary_checks += 1

        pairs = [(i, k) for i in range(n) for k in range(i, n)]
        residual = rng.random(n) * steps
        # For fixed residual inputs, project every McCormick/square polytope.
        bounds = []
        exact = []
        for i, k in pairs:
            exact.append(residual[i] * residual[k])
            if i == k:
                bounds.append((max(0, 2 * steps[i] * residual[i] - steps[i] ** 2),
                               steps[i] * residual[i]))
            else:
                bounds.append((max(0, steps[k] * residual[i] + steps[i] * residual[k]
                                   - steps[i] * steps[k]),
                               min(steps[k] * residual[i], steps[i] * residual[k])))

        for output in range(4):
            matrix = rng.integers(-7, 8, size=(n, n)).astype(float)
            hessian = matrix + matrix.T
            transformed = rotation.T @ hessian @ rotation
            scaled = transformed * np.sqrt(eigenvalues[:, None] * eigenvalues[None, :])
            tolerance = np.linalg.norm(scaled, 'fro') * (1 + output / 3)
            energy = np.trace(hessian @ covariance @ hessian @ covariance)
            assert np.isclose(energy, np.linalg.norm(scaled, 'fro') ** 2,
                              rtol=2e-8, atol=1e-15)
            objective = np.array([transformed[i, k] * (0.5 if i == k else 1)
                                  for i, k in pairs])
            true_value = objective @ exact
            for sign in (-1, 1):
                result = linprog(sign * objective, bounds=bounds, method='highs')
                assert result.success
                error = abs(sign * result.fun - true_value)
                # LP feasibility tolerances can matter for extremely small cells.
                assert error <= tolerance / 8 + 2e-8
                projected_checks += 1

for n in range(2, 10):
    for trial in range(10):
        edges = [(i, k) for i in range(n) for k in range(i + 1, n)
                 if rng.random() < 0.4]
        if not edges:
            edges = [(0, 1)]
        tolerance = 2.0 ** (-rng.uniform(-1, 12, len(edges)))
        rows = np.zeros((len(edges), n))
        for row, (i, k) in enumerate(edges):
            rows[row, i] = rows[row, k] = -1
        rhs = -np.log2(np.sqrt(2) / tolerance)
        solution = linprog(np.ones(n), A_ub=rows, b_ub=rhs,
                           bounds=(0, None), method='highs')
        assert solution.success
        diagonal = 2.0 ** (-2 * solution.x)
        assert np.isclose(-np.log2(diagonal).sum() / 2, solution.fun)
        for eps, (i, k) in zip(tolerance, edges):
            assert 2 * diagonal[i] * diagonal[k] <= eps ** 2 * (1 + 1e-9)
        graph_checks += 1

print(f'PASS: {projected_checks} projected residual LP extrema, '
      f'{boundary_checks} rotated-cube representations, '
      f'{graph_checks} unequal-accuracy graph LP reductions')
