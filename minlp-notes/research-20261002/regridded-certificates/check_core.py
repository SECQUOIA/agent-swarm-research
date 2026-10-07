"""Targeted numerical checks of the regridded-certificate proof constants."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def occurrence_checks(rng):
    cases = 0
    max_ratio = 0.0
    for size in range(1, 17):
        for _ in range(30):
            parents = [-1] + [int(rng.integers(v)) for v in range(1, size)]
            incidence = np.zeros((size, 2 * size - 1))
            for v in range(size):
                current = v
                while current:
                    parent = parents[current]
                    incidence[v, parent] = 1
                    incidence[v, size + current - 1] = 1
                    current = parent
            bound = size * (size - 1)
            assert np.sum(incidence * incidence) <= bound
            widths = rng.uniform(0, 1, 2 * size - 1)
            drift = incidence @ widths
            assert drift @ drift <= bound * (widths @ widths) + 1e-12
            if bound:
                max_ratio = max(max_ratio, float((drift @ drift) / (bound * (widths @ widths))))
            cases += 1
    return {"cases": cases, "max_observed_drift_bound_ratio": max_ratio}


def constants_checks(rng):
    cases = 0
    for _ in range(500):
        k, p = int(rng.integers(1, 9)), int(rng.integers(1, 6))
        M, A0, g = 10 ** rng.uniform(-3, 3, 3)
        if cases % 17 == 0:
            M = 0.0
        if cases % 19 == 0:
            A0 = 0.0
        C0 = k * (k - 1) * p
        B0 = M * C0 / 2 + A0 / 4
        eta = g / 20
        C = 12 * B0 + 6 * k * C0 * M * M / eta
        B = max(p, 2 * C / g)
        caps = [0.5]
        if C0:
            caps.append(1 / np.sqrt(12 * C0))
        if C0 * M:
            caps.append(eta / (4 * np.sqrt(12) * k * np.sqrt(C0) * M))
        if B0:
            caps.append(np.sqrt(eta / (48 * k * B0)))
        theta = 2.0 ** np.floor(np.log2(min(caps)))
        assert 12 * C0 * theta * theta <= 1 + 1e-12
        assert np.sqrt(12) * k * np.sqrt(C0) * M * theta <= eta / 4 * (1 + 1e-12)
        assert 12 * k * B0 * theta * theta <= eta / 4 * (1 + 1e-12)
        # Normalize N h_j^2=1; the old squared error is at most 4B.
        new_error_bound = 4 * B / 9 + 10 * C / (9 * g)
        assert new_error_bound <= B * (1 + 1e-12)
        assert g * B / 2 + C <= g * B * (1 + 1e-12)
        # The complete aggregate-error expression is bounded for arbitrary R,h.
        radius, nh2 = 10 ** rng.uniform(-4, 4, 2)
        full_error = (
            np.sqrt(12 * k * C0) * M * np.sqrt(nh2) * radius
            + (np.sqrt(12) * k * np.sqrt(C0) * M * theta + 12 * k * B0 * theta * theta) * radius * radius
            + 12 * B0 * nh2
        )
        upper = eta * radius * radius + C * nh2
        assert full_error <= upper * (1 + 1e-12) + 1e-20
        cases += 1
    return {"cases": cases, "includes_zero_M_A0_and_k_one": True}


def uniform_interval(z, h):
    index = min(int(np.floor(z / h)), int(round(1 / h)) - 1)
    return index * h, (index + 1) * h


def configuration_checks(rng):
    """Actual valid uniform-grid configurations of a boundary-minimum family."""
    a, h = 0.2, 1 / 16
    cases, largest_identity_error = 0, 0.0
    for depth in range(1, 7):
        n = 2 ** (depth + 1) - 1
        parents = [-1] + [(v - 1) // 2 for v in range(1, n)]
        H = np.eye(n)
        for v in range(1, n):
            H[v, parents[v]] = H[parents[v], v] = -a
        M = np.linalg.norm(np.array([[0.0, -a], [-a, 1.0]]), 2)
        k, p, A0 = 3, 2, a
        C0 = k * (k - 1) * p
        assert np.linalg.eigvalsh(H)[0] >= 1 - 2 * np.sqrt(2) * a - 1e-12
        # F(x)=.5 x'Hx + sum x has unique boundary minimum at zero;
        # grad F(0)=1 is explicitly nonzero.
        for _ in range(30):
            x, center = rng.uniform(0, 1, (2, n))
            phi = 0.5 * x[0] ** 2 + x[0]
            remainders = relaxation_error = E = 0.0
            for v in range(1, n):
                parent = parents[v]
                parent_low, _ = uniform_interval(x[parent], h)
                parent_index = int(round(parent_low / h))
                adjacent = [j for j in (parent_index - 1, parent_index, parent_index + 1) if 0 <= j < 16]
                cell_index = int(rng.choice(adjacent))
                separator_low = cell_index * h
                copied_parent = separator_low + rng.uniform() * h
                # Separator cell meets the parent's own-coordinate leaf interval,
                # including the permitted closed touching case.
                assert abs(copied_parent - x[parent]) <= 2 * h + 1e-12
                lo_p, up_p = uniform_interval(copied_parent, h)
                lo_v, up_v = uniform_interval(x[v], h)
                error = a / 2 * (
                    (copied_parent - lo_p) * (up_p - copied_parent)
                    + (x[v] - lo_v) * (up_v - x[v])
                )
                bag_at_copy = 0.5 * x[v] ** 2 + x[v] - a * copied_parent * x[v]
                bag_at_x = 0.5 * x[v] ** 2 + x[v] - a * x[parent] * x[v]
                slope = -a * center[v]
                phi += bag_at_copy - error + slope * (x[parent] - copied_parent)
                remainders += bag_at_copy - bag_at_x - slope * (copied_parent - x[parent])
                relaxation_error += error
                E += (copied_parent - x[parent]) ** 2
            F = 0.5 * x @ H @ x + x.sum()
            identity_error = abs(phi - (F + remainders - relaxation_error))
            largest_identity_error = max(largest_identity_error, identity_error)
            assert identity_error <= 1e-10
            Q = (2 * n - 1) * h * h
            assert E <= C0 * Q + 1e-12
            R = np.linalg.norm(x - center)
            raw_bound = M * np.sqrt(k) * R * np.sqrt(E) + M * E / 2 + A0 * Q / 4
            assert abs(F - phi) <= raw_bound + 1e-10
            cases += 1
    return {"cases": cases, "maximum_telescoping_identity_error": largest_identity_error, "nonstationary_boundary_minimizer": True}


def main():
    rng = np.random.default_rng(2026100202)
    result = {
        "status": "passed",
        "occurrence_subtrees": occurrence_checks(rng),
        "parameter_and_contraction_constants": constants_checks(rng),
        "actual_certificate_configurations": configuration_checks(rng),
        "scope": "Targeted floating-point proof checks; no implementation or enumeration of the full regridded DP, no project-wide checks, no CI inspection.",
    }
    Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
