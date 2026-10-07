"""Targeted matrix and configuration checks for stable affine repair."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def matrices(T, a, b):
    A = np.zeros((T, 2 * T + 1))
    K = np.zeros((2 * T + 1, T))
    for t in range(T):
        A[t, t], A[t, t + 1], A[t, T + 1 + t] = -a, 1, -b
        for i in range(t + 1, T + 1):
            K[i, t] = a ** (i - t - 1)
    return A, K


def objective(x, T):
    states, controls = x[: T + 1], x[T + 1 :]
    return float(states @ states + np.sum(controls**2 - controls**4 / 4))


def gradient(x, T):
    return np.concatenate([2 * x[: T + 1], 2 * x[T + 1 :] - x[T + 1 :] ** 3])


def bag_value(z, first):
    state, control, next_state = z
    return (state * state if first else 0.0) + next_state**2 + control**2 - control**4 / 4


def bag_gradient(z, first):
    state, control, next_state = z
    return np.array([2 * state if first else 0.0, 2 * control - control**3, 2 * next_state])


def interval(value, h):
    index = min(int(np.floor((value + 1) / h)), int(round(2 / h)) - 1)
    return -1 + index * h, -1 + (index + 1) * h


def main():
    rng = np.random.default_rng(2026100203)
    matrix_cases = configuration_cases = 0
    worst_right_inverse = worst_idempotence = worst_telescope = 0.0
    max_repair_norm = 0.0
    for T in [1, 2, 3, 8, 16, 32]:
        for a, b in [(0.5, 0.5), (-0.5, 0.5), (0.8, -0.2), (0.0, 0.7)]:
            A, K = matrices(T, a, b)
            P = np.eye(2 * T + 1) - K @ A
            inverse_error = np.max(np.abs(A @ K - np.eye(T)))
            projection_error = np.max(np.abs(P @ P - P))
            worst_right_inverse = max(worst_right_inverse, inverse_error)
            worst_idempotence = max(worst_idempotence, projection_error)
            assert inverse_error < 1e-12
            assert projection_error < 1e-12
            K_norm = np.linalg.norm(K, 2)
            max_repair_norm = max(max_repair_norm, K_norm)
            assert K_norm <= 1 / (1 - abs(a)) + 1e-12
            # Row l1 norm at most one verifies whole-box preservation, not samples.
            assert np.max(np.sum(np.abs(P), axis=1)) <= 1 + 1e-12
            for _ in range(10):
                x = rng.uniform(-1, 1, 2 * T + 1)
                y = P @ x
                center = P @ rng.uniform(-1, 1, 2 * T + 1)
                multipliers = -K.T @ gradient(center, T)
                adjusted_gradient = gradient(center, T) + A.T @ multipliers
                assert np.max(np.abs(A @ y)) < 1e-12
                assert abs(adjusted_gradient @ (x - y)) < 1e-10
                assert objective(y, T) >= 0.75 * (y @ y) - 1e-12
            matrix_cases += 1

    # Full valid copied configurations on the nonlinear-cost dynamics family.
    a, b, h, k, p, M, A0 = 0.5, 0.5, 1 / 16, 2, 3, 2, 0.5
    for T in [1, 2, 3, 8, 16, 32]:
        A, K = matrices(T, a, b)
        P = np.eye(2 * T + 1) - K @ A
        chi = np.linalg.norm(K, 2) * np.sqrt(1 + a * a + b * b)
        C0 = k * (k - 1) * p
        D = C0 * (1 + np.sqrt(k) * chi) ** 2
        for _ in range(40):
            center = P @ rng.uniform(-1, 1, 2 * T + 1)
            mu = -K.T @ gradient(center, T)
            x = np.zeros(2 * T + 1)
            x[0] = rng.uniform(-1, 1)
            copies, errors = [], []
            for t in range(T):
                if t == 0:
                    copied_state = x[0]
                else:
                    left, _ = interval(x[t], h)
                    index = int(round((left + 1) / h))
                    options = [j for j in [index - 1, index, index + 1] if 0 <= j < 32]
                    cell = int(rng.choice(options))
                    copied_state = -1 + (cell + rng.uniform()) * h
                control = rng.uniform(-1, 1)
                next_state = a * copied_state + b * control
                x[t + 1], x[T + 1 + t] = next_state, control
                z = np.array([copied_state, control, next_state])
                copies.append(z)
                lo, hi = interval(control, h)
                errors.append(0.5 * (control - lo) * (hi - control))
                assert abs(next_state - a * copied_state - b * control) < 1e-12
            y = P @ x
            phi = sum(bag_value(z, t == 0) - errors[t] for t, z in enumerate(copies))
            phi += sum((-a * mu[t]) * (x[t] - copies[t][0]) for t in range(1, T))
            remainders = Ex = Ey = 0.0
            for t, z in enumerate(copies):
                indices = [t, T + 1 + t, t + 1]
                remainders += bag_value(z, t == 0) - bag_value(y[indices], t == 0) - bag_gradient(center[indices], t == 0) @ (z - y[indices])
                Ex += np.sum((z - x[indices]) ** 2)
                Ey += np.sum((z - y[indices]) ** 2)
            identity_error = abs(phi - (objective(y, T) + remainders - sum(errors)))
            worst_telescope = max(worst_telescope, identity_error)
            assert identity_error < 1e-10
            assert np.linalg.norm(y - x) <= chi * np.sqrt(Ex) + 1e-12
            Q = (2 * T - 1) * h * h
            assert Ey <= D * Q + 1e-12
            R = np.linalg.norm(y - center)
            bound = M * np.sqrt(k) * R * np.sqrt(Ey) + M * Ey / 2 + A0 * Q / 4
            assert abs(objective(y, T) - phi) <= bound + 1e-10
            configuration_cases += 1

    result = {
        "status": "passed",
        "matrix_cases": matrix_cases,
        "valid_nonlinear_certificate_configurations": configuration_cases,
        "maximum_right_inverse_residual": float(worst_right_inverse),
        "maximum_retraction_idempotence_residual": float(worst_idempotence),
        "maximum_adjusted_slope_telescope_residual": float(worst_telescope),
        "maximum_observed_K_norm": float(max_repair_norm),
        "scope": "Targeted floating-point checks; row l1 norm checks verify box preservation of each tested linear map. No full dynamic-program implementation, project-wide verification, or CI inspection.",
    }
    Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
