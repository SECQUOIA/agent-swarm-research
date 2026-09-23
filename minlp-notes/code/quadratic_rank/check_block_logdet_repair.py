"""Exact feasibility checks for the rational block-logdet central repair."""

import itertools
import random

import mpmath as mp
import sympy as sp

mp.mp.dps = 100
rng = random.Random(2026090557)
cases = 0
for dimensions in ([1], [2], [1, 2], [2, 2], [1, 3], [2, 3]):
    size = sum(dimensions)
    for outputs in range(1, 5):
        matrices = []
        for _ in range(outputs):
            row = []
            for dimension in dimensions:
                raw = sp.Matrix(dimension + 1, dimension, lambda i, j: rng.randint(-2, 2))
                row.append(raw.T * raw)
            matrices.append(row)
        total_trace = sum(sp.trace(matrix) for row in matrices for matrix in row)
        matrices = [[matrix / (1 + 2 * total_trace) for matrix in row] for row in matrices]
        coordinates = [(b, i, j) for b, dimension in enumerate(dimensions)
                       for i in range(dimension) for j in range(i, dimension)]
        linear = sp.Matrix(outputs, len(coordinates),
                           lambda out, k: matrices[out][coordinates[k][0]][coordinates[k][1], coordinates[k][2]] *
                           (1 if coordinates[k][1] == coordinates[k][2] else 2))
        bound = 1 + sum(abs(value) for value in linear)
        exponent = 0
        delta = sp.Integer(1)
        while delta * size * bound > sp.Rational(1, 4):
            exponent += 1
            delta /= 2
        lower = delta ** size / 4
        height = size * (size * exponent + 2) + 4
        center_t = -size * (exponent + 1) - 2
        sigma = min(delta / (32 * size), 1 / (8 * bound), sp.Rational(1, 4))
        nu = sp.Rational(1, 8)
        rho = nu * sigma / (4 * (height + sigma + 1))
        weak = [sp.eye(dimension) for dimension in dimensions]
        if dimensions[-1] >= 2:
            weak[-1][0, 1] = weak[-1][1, 0] = rho / 2
        else:
            weak[0][0, 0] += rho / 2
        weak_t = rho / 2
        fixed = [(sigma * matrix + rho * delta * sp.eye(dimension) / 2) / (sigma + rho)
                 for matrix, dimension in zip(weak, dimensions)]
        fixed_t = (sigma * weak_t + rho * center_t) / (sigma + rho)
        for matrix, dimension in zip(fixed, dimensions):
            for slack in (matrix - lower * sp.eye(dimension), sp.eye(dimension) - matrix):
                for count in range(1, dimension + 1):
                    for subset in itertools.combinations(range(dimension), count):
                        assert slack.extract(subset, subset).det() >= 0
        energies = sp.Matrix([sum(sp.trace(h * p) for h, p in zip(row, fixed)) for row in matrices])
        assert energies.dot(energies) <= 1
        assert -height <= fixed_t <= 0
        assert -fixed_t <= nu
        determinant = sp.prod(matrix.det() for matrix in fixed)
        logdet = mp.log(mp.mpf(str(sp.numer(determinant))) / mp.mpf(str(sp.denom(determinant))))
        t_value = mp.mpf(str(sp.numer(fixed_t))) / mp.mpf(str(sp.denom(fixed_t)))
        assert t_value <= logdet + mp.mpf('1e-90')
        assert logdet >= -mp.mpf('0.125') - mp.mpf('1e-90')
        cases += 1

print(f'PASS: {cases} rational block-logdet repairs with exact spectral/body/objective '
      'bounds and 100-digit log-determinant hypographs')
