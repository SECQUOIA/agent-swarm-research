"""Exact shared-error and rational elliptope repair checks.

This verifies the new algebraic reductions, not an implementation of the
classical weak-optimization algorithm.
"""

import itertools
import random

import sympy as sp

rng = random.Random(2026090551)
residual_cases = repair_cases = 0
for n in range(1, 5):
    for m in range(1, 7):
        matrices = []
        for _ in range(m):
            raw = sp.Matrix(n, n, lambda i, k: rng.randint(-3, 3))
            matrices.append(raw + raw.T)
        gram = sp.Matrix(m, m, lambda j, k: sp.trace(matrices[j] * matrices[k]))
        residual = sp.Matrix(n, n, lambda i, k: sp.Rational(rng.randint(-1, 1), 4 * n))
        residual = (residual + residual.T) / 2
        errors = [sp.trace(matrix * residual) / 2 for matrix in matrices]
        maximum = max((sp.Matrix(signs).T * gram * sp.Matrix(signs))[0]
                      for signs in itertools.product((-1, 1), repeat=m))
        assert sum(abs(error) for error in errors) ** 2 <= maximum / 64
        residual_cases += 1

for m in range(2, 7):
    for _ in range(6):
        vector = sp.Matrix([rng.choice((-3, -2, -1, 1, 2, 3)) for j in range(m)])
        signs = vector.applyfunc(sp.sign)
        gram = vector * vector.T / (vector.T * vector)[0]
        optimum = sum(abs(value) for value in vector) ** 2 / (vector.T * vector)[0]
        exact_optimizer = signs * signs.T
        nu = sp.Rational(1, rng.randint(10, 40))
        rho = nu / (4 * (m + 1))
        perturbation = sp.zeros(m)
        for i in range(m):
            for j in range(i):
                perturbation[i, j] = perturbation[j, i] = rho * rng.randint(-1, 1) / m
        assert sum(perturbation[i, j] ** 2 for i in range(m) for j in range(i)) <= rho ** 2
        near = exact_optimizer + perturbation
        # This deliberately constructed weak-feasible point need not obey
        # the weak objective guarantee; check the universal repair bound,
        # then the certified upper value when the objective premise holds.
        a = sp.trace(gram * near)
        fixed = (near + 2 * rho * sp.eye(m)) / (1 + 2 * rho)
        assert all(fixed[i, i] == 1 for i in range(m))
        for subset_size in range(1, m + 1):
            for subset in itertools.combinations(range(m), subset_size):
                assert fixed.extract(subset, subset).det() >= 0
        lower = sp.trace(gram * fixed)
        assert 0 <= optimum - lower
        assert optimum - lower <= (optimum - a + 2 * rho * (optimum - 1)) / (1 + 2 * rho)
        if a >= optimum - rho:
            assert lower <= optimum <= lower + nu
            assert lower >= sp.Rational(1, 2)
            assert (lower + nu) / lower <= 1 + 2 * nu
            repair_cases += 1

print(f'PASS: {residual_cases} exact l1 shared-residual bounds and '
      f'{repair_cases} exact rational elliptope feasibility/upper-bound repairs')
