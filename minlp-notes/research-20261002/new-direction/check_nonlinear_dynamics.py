"""Exact-rational checks of the nonlinear-dynamics proof's new identities.

This checks sampled valid configurations, not the full dynamic program.
"""

from fractions import Fraction as F
import json
from pathlib import Path
from random import Random


def phi(s, u):
    return s / 4 + u / 2 + s * s / 8


def partial_s(s):
    return F(1, 4) + s / 4


def objective(t, z):
    s, u, v = z
    return (s * s if t == 0 else 0) + v * v + u * u - u**4 / 4


def adjusted_gradient(t, z, mu):
    s, u, v = z
    return (
        (2 * s if t == 0 else 0) - mu * partial_s(s),
        2 * u - u**3 - mu / 2,
        2 * v + mu,
    )


def check():
    rng = Random(20261002)
    horizons = [1, 2, 3, 4, 6]
    configurations = 0
    nonzero_strip_residuals = 0
    nonzero_copy_mismatches = 0
    largest_multiplier = F(0)
    width = F(1, 8)
    half_width = width / 2
    curvature = F(1, 4)
    residual_constant = curvature / 2

    for horizon in horizons:
        for _ in range(40):
            center_controls = [
                F(rng.randint(-8, 8), 16) for _ in range(horizon)
            ]
            center_states = [F(rng.randint(-8, 8), 16)]
            for control in center_controls:
                center_states.append(phi(center_states[-1], control))

            multipliers = [F(0) for _ in range(horizon)]
            multipliers[-1] = -2 * center_states[-1]
            for t in range(horizon - 1, 0, -1):
                multipliers[t - 1] = (
                    partial_s(center_states[t]) * multipliers[t]
                    - 2 * center_states[t]
                )
            assert max(map(abs, multipliers)) <= 4
            largest_multiplier = max(
                largest_multiplier, max(map(abs, multipliers))
            )

            copies = []
            for t in range(horizon):
                s = center_states[t] + F(rng.randint(-4, 4), 128)
                u = center_controls[t] + F(rng.randint(-4, 4), 128)
                linear_value = (
                    center_states[t + 1]
                    + partial_s(center_states[t]) * (s - center_states[t])
                    + (u - center_controls[t]) / 2
                )
                strip_offset = (
                    F(rng.randint(-4, 4), 4) * curvature * width**2 / 4
                )
                v = linear_value + strip_offset
                assert abs(s - center_states[t]) <= half_width
                assert abs(u - center_controls[t]) <= half_width
                assert abs(v - center_states[t + 1]) <= half_width
                assert abs(v - linear_value) <= curvature * width**2 / 4
                assert abs(v - phi(s, u)) <= residual_constant * width**2
                nonzero_strip_residuals += v != phi(s, u)
                copies.append((s, u, v))

            # Each bag leaf is centered at the feasible center and has the
            # same width. Its state projection is the adjacent separator
            # cell, so the selected copies form a valid configuration.
            states = [copies[0][0]] + [z[2] for z in copies]
            controls = [z[1] for z in copies]
            repaired_states = [states[0]]
            for control in controls:
                repaired_states.append(phi(repaired_states[-1], control))
            assert all(-1 <= value <= 1 for value in repaired_states)
            repaired = [
                (repaired_states[t], controls[t], repaired_states[t + 1])
                for t in range(horizon)
            ]
            center = [
                (center_states[t], center_controls[t], center_states[t + 1])
                for t in range(horizon)
            ]
            slopes = [None] + [
                -multipliers[t] * partial_s(center_states[t])
                for t in range(1, horizon)
            ]
            errors = [
                F(1, 2)
                * (copies[t][1] - (center_controls[t] - half_width))
                * ((center_controls[t] + half_width) - copies[t][1])
                for t in range(horizon)
            ]
            configuration_value = sum(
                objective(t, copies[t]) - errors[t] for t in range(horizon)
            ) + sum(
                slopes[t] * (copies[t - 1][2] - copies[t][0])
                for t in range(1, horizon)
            )
            nonzero_copy_mismatches += sum(
                copies[t - 1][2] != copies[t][0]
                for t in range(1, horizon)
            )

            remainders = F(0)
            multiplier_residual = F(0)
            for t in range(horizon):
                local_residual = copies[t][2] - phi(*copies[t][:2])
                multiplier_residual += multipliers[t] * local_residual
                adjusted_value = (
                    objective(t, copies[t]) + multipliers[t] * local_residual
                )
                linear_term = sum(
                    gradient * (copy - feasible)
                    for gradient, copy, feasible in zip(
                        adjusted_gradient(t, center[t], multipliers[t]),
                        copies[t],
                        repaired[t],
                    )
                )
                remainders += (
                    adjusted_value - objective(t, repaired[t]) - linear_term
                )
            assert configuration_value == (
                sum(objective(t, repaired[t]) for t in range(horizon))
                + remainders
                - multiplier_residual
                - sum(errors)
            )

            residual_squared = sum(
                (states[t + 1] - phi(states[t], controls[t])) ** 2
                for t in range(horizon)
            )
            repair_squared = sum(
                (repaired_states[t] - states[t]) ** 2
                for t in range(horizon + 1)
            )
            assert repair_squared <= 4 * residual_squared
            for t in range(1, horizon):
                assert (
                    2 * center_states[t]
                    + multipliers[t - 1]
                    - multipliers[t] * partial_s(center_states[t])
                    == 0
                )
            assert 2 * center_states[horizon] + multipliers[-1] == 0
            configurations += 1

    assert nonzero_strip_residuals > 0
    assert nonzero_copy_mismatches > 0
    return {
        "arithmetic": "exact rational",
        "dynamics": "phi(s,u)=s/4+u/2+s^2/8",
        "configurations": configurations,
        "horizons": horizons,
        "checks": [
            "leaf and affine-strip membership",
            "quadratic graph-residual bound",
            "sampled repair box preservation",
            "adjoint bound and state cancellation",
            "exact adjusted telescoping identity",
            "stable repair residual bound",
        ],
        "nonzero_strip_residuals": nonzero_strip_residuals,
        "nonzero_copy_mismatches": nonzero_copy_mismatches,
        "maximum_identity_residual": "0",
        "maximum_observed_multiplier": float(largest_multiplier),
        "scope": "Sampled configurations; no full dynamic-program execution.",
    }


if __name__ == "__main__":
    result = check()
    serialized = json.dumps(result, indent=2) + "\n"
    Path(__file__).with_suffix(".json").write_text(serialized)
    print(serialized, end="")
