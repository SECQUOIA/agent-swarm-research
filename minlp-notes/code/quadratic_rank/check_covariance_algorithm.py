"""Check rational Jacobi invariants and covariance penalty derivatives."""

import math

import mpmath as mp
import numpy as np
import sympy as sp
from scipy.linalg import expm


mp.mp.dps = 100
rng = np.random.default_rng(2026090521)
jacobi_steps = 0

for n in (2, 3, 4):
    for trial in range(2):
        raw = sp.Matrix(rng.integers(-3, 4, (n, n)).tolist())
        original = raw * raw.T + sp.eye(n)
        current = original.copy()
        orthogonal = sp.eye(n)
        sigma = sp.Rational(1, 8)
        magnitude = max(1, sum(abs(x) for x in original))
        pair_count = n * (n - 1)
        precision = math.ceil(math.log2(float(128 * pair_count * magnitude / sigma)))
        scale = 2 ** precision
        step_limit = math.ceil(2 * pair_count * math.log(float(magnitude / sigma))) + 1

        def off_squared(matrix):
            return sum(matrix[i, k] ** 2 for i in range(n) for k in range(n) if i != k)

        for step in range(step_limit):
            previous_squared = off_squared(current)
            if previous_squared <= sigma ** 2:
                break
            i, k = max(((i, k) for i in range(n) for k in range(i + 1, n)),
                       key=lambda pair: abs(current[pair[0], pair[1]]))

            def real(value):
                return mp.mpf(int(sp.numer(value))) / int(sp.denom(value))

            angle = mp.atan2(2 * real(current[i, k]), real(current[k, k] - current[i, i])) / 2
            if angle > mp.pi / 4:
                angle -= mp.pi / 2
            elif angle < -mp.pi / 4:
                angle += mp.pi / 2
            half_tangent = sp.Rational(int(mp.nint(mp.tan(angle / 2) * scale)), scale)
            cosine = (1 - half_tangent ** 2) / (1 + half_tangent ** 2)
            sine = 2 * half_tangent / (1 + half_tangent ** 2)
            rotation = sp.eye(n)
            rotation[i, i] = rotation[k, k] = cosine
            rotation[i, k] = sine
            rotation[k, i] = -sine
            assert cosine ** 2 + sine ** 2 == 1
            current = rotation.T * current * rotation
            orthogonal = orthogonal * rotation
            # The proved contraction while the off-norm exceeds its target.
            assert off_squared(current) <= (1 - sp.Rational(3, 4 * pair_count)) ** 2 * previous_squared
            jacobi_steps += 1
        assert off_squared(current) <= sigma ** 2
        assert orthogonal.T * orthogonal == sp.eye(n)
        assert original == orthogonal * current * orthogonal.T
        diagonal = sp.diag(*(current[i, i] for i in range(n)))
        reconstructed = orthogonal * diagonal * orthogonal.T
        assert sum(x ** 2 for x in original - reconstructed) <= sigma ** 2
        # This input has lambda_min >= 1; sigma=1/8 gives ample grid margin.
        covariance_grid = reconstructed / 4
        for positive_matrix in (covariance_grid - original / 8, original / 2 - covariance_grid):
            assert all(positive_matrix[:k, :k].det() > 0 for k in range(1, n + 1))


def penalty_and_gradient(point, hessians, tolerance):
    values, vectors = np.linalg.eigh(point)
    root = (vectors * np.sqrt(values)) @ vectors.T
    components = [0.0, math.log(values[-1])]
    normalized = [np.zeros_like(point), np.outer(vectors[:, -1], vectors[:, -1])]
    for hessian, eps in zip(hessians, tolerance):
        matrix = root @ hessian @ root
        square = matrix @ matrix
        energy = np.trace(square)
        components.append(math.log(energy / eps ** 2) / 2)
        normalized.append(square / energy)
    active = int(np.argmax(components))
    n = len(point)
    value = -np.log(values).sum() + n * components[active]
    gradient = -np.eye(n) + n * normalized[active]
    assert np.linalg.norm(gradient, 'fro') <= 2 * n + 1e-10
    repaired = point * math.exp(-components[active])
    assert np.linalg.eigvalsh(repaired)[-1] <= 1 + 1e-10
    for hessian, eps in zip(hessians, tolerance):
        assert np.trace(hessian @ repaired @ hessian @ repaired) <= eps ** 2 * (1 + 1e-10)
    assert abs(value + np.linalg.slogdet(repaired)[1]) <= 1e-9
    return value, gradient, root


derivative_checks = 0
for n in range(2, 7):
    for trial in range(8):
        raw = rng.normal(size=(n, n))
        point = expm((raw + raw.T) / 3)
        hessians = []
        for output in range(3):
            raw = rng.normal(size=(n, n))
            hessians.append(raw + raw.T)
        tolerances = np.exp(rng.uniform(-2, 2, 3))
        value, gradient, root = penalty_and_gradient(point, hessians, tolerances)
        direction = rng.normal(size=(n, n))
        direction += direction.T
        direction /= np.linalg.norm(direction, 'fro')
        step = 1e-6
        plus = penalty_and_gradient(root @ expm(step * direction) @ root, hessians, tolerances)[0]
        minus = penalty_and_gradient(root @ expm(-step * direction) @ root, hessians, tolerances)[0]
        finite_difference = (plus - minus) / (2 * step)
        assert np.isclose(finite_difference, np.trace(gradient @ direction), atol=3e-7)
        assert value <= (plus + minus) / 2 + 1e-10
        derivative_checks += 1

print(f'PASS: {jacobi_steps} exact rational Jacobi contractions across 6 matrices, '
      f'{derivative_checks} penalty derivative and feasibility-repair checks')
