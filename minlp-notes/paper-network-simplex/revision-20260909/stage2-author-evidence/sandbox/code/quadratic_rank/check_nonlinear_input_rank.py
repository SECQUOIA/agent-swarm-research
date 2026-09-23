"""Exact checks for nonlinear input quotient and rational normalization.

The classical LP and ellipsoid-rounding algorithms are not implemented.
"""

import random

import sympy as sp

rng = random.Random(2026090553)
quotient_cases = normalization_cases = 0
for n in range(2, 8):
    for rank in range(1, min(n, 4) + 1):
        generator = sp.eye(rank).row_join(sp.Matrix(rank, n - rank, lambda i, j: rng.randint(-2, 2)))
        generators = [sp.eye(rank)]
        for _ in range(2):
            raw = sp.Matrix(rank, rank, lambda i, j: rng.randint(-2, 2))
            generators.append(raw + raw.T)
        hessians = [generator.T * matrix * generator for matrix in generators]
        stacked = sp.Matrix.vstack(*hessians)
        basis = sp.Matrix.vstack(*stacked.rowspace())
        assert basis.rows == rank
        right_inverse = basis.T * (basis * basis.T).inv()
        reduced = [right_inverse.T * matrix * right_inverse for matrix in hessians]
        assert all(matrix == basis.T * small * basis for matrix, small in zip(hessians, reduced))
        center = sp.ones(n, 1) / 2
        point = sp.Matrix([sp.Rational(rng.randint(0, 16), 16) for _ in range(n)])
        z = basis * (point - center)
        for matrix, small in zip(hessians, reduced):
            linear = sp.Matrix([rng.randint(-2, 2) for _ in range(n)])
            constant = rng.randint(-2, 2)
            original = (point.T * matrix * point)[0] / 2 + (linear.T * point)[0] + constant
            affine = (linear.T * point)[0] + constant + (point.T * matrix * center)[0] - (center.T * matrix * center)[0] / 2
            assert original == affine + (z.T * small * z)[0] / 2
        quotient_cases += 1

        triangular = sp.eye(rank)
        for i in range(rank):
            for j in range(i):
                triangular[i, j] = sp.Rational(rng.randint(-3, 3), rng.randint(1, 4))
        diagonal = sp.diag(*[sp.Rational(rng.randint(1, 20), rng.randint(1, 20)) for _ in range(rank)])
        metric = triangular * diagonal * triangular.T
        lower, pivots = metric.LDLdecomposition(hermitian=False)
        values = []
        for i in range(rank):
            exponent = 0
            while sp.Integer(2) ** (2 * exponent) < pivots[i, i]:
                exponent += 1
            while sp.Integer(2) ** (2 * (exponent - 1)) >= pivots[i, i]:
                exponent -= 1
            value = sp.Integer(2) ** exponent
            assert pivots[i, i] <= value ** 2 <= 4 * pivots[i, i]
            values.append(value)
        normalization = sp.diag(*values) * lower.T
        # Congruence to diagonal verifies both PSD inequalities exactly.
        difference = lower.inv() * (normalization.T * normalization - metric) * lower.T.inv()
        assert difference.is_diagonal()
        assert all(difference[i, i] >= 0 for i in range(rank))
        upper_difference = lower.inv() * (4 * metric - normalization.T * normalization) * lower.T.inv()
        assert upper_difference.is_diagonal()
        assert all(upper_difference[i, i] >= 0 for i in range(rank))
        mapped = sp.ones(rank, 1) / 2 + normalization * z / 4
        recovered = 4 * normalization.inv() * (mapped - sp.ones(rank, 1) / 2)
        assert recovered == z
        normalization_cases += 1

print(f'PASS: {quotient_cases} exact common-kernel quotient/affine-fiber identities and '
      f'{normalization_cases} rational LDL normalization sandwiches/inverse maps')
