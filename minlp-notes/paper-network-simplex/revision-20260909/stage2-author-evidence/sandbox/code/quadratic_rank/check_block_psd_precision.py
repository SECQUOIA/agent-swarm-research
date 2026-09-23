"""Exact block covariance and noncommuting PSD residual checks."""

import itertools
import random

import sympy as sp

rng = random.Random(2026090556)
cases = 0
for dimensions in ([1, 1], [1, 2], [2, 2], [1, 3], [2, 3], [1, 2, 3]):
    size = sum(dimensions)
    offsets = [sum(dimensions[:i]) for i in range(len(dimensions))]
    for trial in range(6):
        hessians = []
        for output in range(3):
            blocks = []
            for dimension in dimensions:
                raw = sp.Matrix(dimension + 1, dimension, lambda i, j: rng.randint(-2, 2))
                blocks.append(raw.T * raw)
            hessians.append(blocks)
        points = [sp.Matrix([sp.Rational(rng.randint(0, 16), 16) for _ in range(size)]) for _ in range(size + 3)]
        mean = sum(points, sp.zeros(size, 1)) / len(points)
        covariance = sum(((point - mean) * (point - mean).T for point in points), sp.zeros(size)) / len(points)
        covariance_blocks = [covariance[offset:offset + dimension, offset:offset + dimension]
                             for offset, dimension in zip(offsets, dimensions)]
        block_product = sp.prod(block.det() for block in covariance_blocks)
        assert covariance.det() <= block_product
        scaled = [block / max(sp.Integer(4), sp.Rational(dimension, 4))
                  for block, dimension in zip(covariance_blocks, dimensions)]
        for block, dimension in zip(scaled, dimensions):
            slack = sp.eye(dimension) - block
            for count in range(1, dimension + 1):
                for subset in itertools.combinations(range(dimension), count):
                    assert slack.extract(subset, subset).det() >= 0
        for blocks in hessians:
            full = sp.diag(*blocks)
            maximum_jensen = max(((x - y).T * full * (x - y))[0] / 8 for x in points for y in points)
            assert sum(sp.trace(h * p) for h, p in zip(blocks, scaled)) <= maximum_jensen

        metrics = []
        residuals = []
        for dimension in dimensions:
            factor = sp.eye(dimension)
            for i in range(dimension):
                for j in range(i):
                    factor[i, j] = sp.Rational(rng.randint(-2, 2), 2)
            metrics.append(factor)
            raw = sp.Matrix(dimension, dimension, lambda i, j: sp.Rational(rng.randint(-1, 1), 4 * dimension))
            residual = (raw + raw.T) / 2
            for sign in (-1, 1):
                slack = sp.eye(dimension) / 4 + sign * residual
                for count in range(1, dimension + 1):
                    for subset in itertools.combinations(range(dimension), count):
                        assert slack.extract(subset, subset).det() >= 0
            residuals.append(residual)
        for blocks in hessians:
            transformed = [factor.T * h * factor for factor, h in zip(metrics, blocks)]
            error = sum(sp.trace(h * z) for h, z in zip(transformed, residuals)) / 2
            energy = sum(sp.trace(h) for h in transformed)
            assert abs(error) <= energy / 8
        cases += 1

print(f'PASS: {cases} exact block determinant/cap/trace checks and '
      'noncommuting PSD shared-residual bounds')
