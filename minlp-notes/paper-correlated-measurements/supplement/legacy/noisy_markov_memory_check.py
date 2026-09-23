"""Numerical checks for the scalar finite-calendar-memory theorem draft.

Independent of markov_design.py; this validates algebra, not proof or priority.
Run with: uv run --frozen noisy_markov_memory_check.py
"""

from itertools import combinations
import json
from pathlib import Path
import platform

import numpy as np


def delta(rho, ratio, length):
    return (
        2 * ratio * rho ** (length + 1) * (1 - rho ** (length + 1))
        / (1 - rho) ** 2
    )


def covariance(transitions, variances, noise):
    n = len(variances)
    latent = np.diag(variances)
    for j in range(n):
        product = 1.0
        for t in range(j + 1, n):
            product *= transitions[t - 1]
            latent[t, j] = latent[j, t] = variances[j] * product
    return latent + np.diag(noise)


def local_residuals(full_covariance, selected, length):
    k = len(selected)
    transform = np.eye(k)
    variances = np.empty(k)
    for row, time in enumerate(selected):
        history = [j for j in range(row) if selected[j] >= time - length]
        hist_times = [selected[j] for j in history]
        coefficients = np.linalg.solve(
            full_covariance[np.ix_(hist_times, hist_times)],
            full_covariance[hist_times, time],
        ) if history else np.empty(0)
        transform[row, history] = -coefficients
        variances[row] = (
            full_covariance[time, time]
            - coefficients @ full_covariance[hist_times, time]
        )
    return transform, variances


def check_case(name, transitions, variances, noise, rho, max_window=6):
    full = covariance(transitions, variances, noise)
    pbar, rmin = max(variances), min(noise)
    assert np.all(variances[1:] - transitions**2 * variances[:-1] >= -1e-12)
    report = {"name": name, "rho": rho, "ratio": pbar / rmin, "windows": []}
    n = len(variances)
    for length in range(max_window + 1):
        largest_spectral_error = 0.0
        largest_pair_fraction = 0.0
        largest_coefficient_fraction = 0.0
        largest_old_cov_fraction = 0.0
        count = 0
        for cardinality in range(1, n + 1):
            for selected in combinations(range(n), cardinality):
                count += 1
                transform, innovation = local_residuals(full, selected, length)
                selected_cov = full[np.ix_(selected, selected)]
                residual_cov = transform @ selected_cov @ transform.T
                normalized = residual_cov / np.sqrt(np.outer(innovation, innovation))
                spectral_error = max(abs(np.linalg.eigvalsh(normalized) - 1))
                largest_spectral_error = max(largest_spectral_error, spectral_error)
                assert spectral_error <= delta(rho, pbar / rmin, length) + 1e-10
                assert np.max(abs(np.diag(normalized) - 1)) < 1e-12
                residual_to_observed = transform @ selected_cov
                for row, t in enumerate(selected):
                    for column in range(row):
                        s = selected[column]
                        lag = t - s
                        if lag <= length:
                            coeff_fraction = abs(transform[row, column]) / rho**lag
                            largest_coefficient_fraction = max(
                                largest_coefficient_fraction, coeff_fraction
                            )
                            assert coeff_fraction <= 1 + 1e-10
                            assert abs(residual_to_observed[row, column]) < 1e-12
                            pair_bound = pbar * rho ** (2 * length + 2 - lag) * (1-rho**(2*lag)) / (1-rho**2)
                        else:
                            old_fraction = abs(residual_to_observed[row, column]) / (pbar * rho**lag)
                            largest_old_cov_fraction = max(largest_old_cov_fraction, old_fraction)
                            assert old_fraction <= 1 + 1e-10
                            pair_bound = pbar * rho**lag * (1-rho**(2*length+2)) / (1-rho**2)
                        pair_fraction = abs(residual_cov[row, column]) / pair_bound
                        largest_pair_fraction = max(largest_pair_fraction, pair_fraction)
                        assert pair_fraction <= 1 + 1e-10
        report["windows"].append({
            "L": length, "subsets": count,
            "delta_bound": delta(rho, pbar / rmin, length),
            "worst_spectral_error": largest_spectral_error,
            "worst_pair_bound_fraction": largest_pair_fraction,
            "worst_coefficient_bound_fraction": largest_coefficient_fraction,
            "worst_old_covariance_bound_fraction": largest_old_cov_fraction,
        })
    return report


def main():
    rng = np.random.default_rng(20260912)
    n = 9
    cases = []
    for rho in [0.4, 0.6, 0.9]:
        cases.append(check_case(
            f"stationary_rho_{rho}", np.full(n - 1, rho),
            np.ones(n), np.ones(n), rho,
        ))
    a = rng.uniform(0.1, 0.6, n - 1) * rng.choice([-1, 1], n - 1)
    a[3] = 0
    p = rng.uniform(0.6, 1.0, n)
    r = rng.uniform(0.7, 2.0, n)
    cases.append(check_case("signed_nonstationary_zero_transition", a, p, r, 0.6))
    # Stable deterministic latent evolution is included: no process-noise floor.
    a = np.full(n - 1, -0.6)
    p = 0.6 ** (2 * np.arange(n))
    cases.append(check_case("zero_process_noise_signed", a, p, np.ones(n), 0.6))
    thresholds = []
    for rho in [0.4, 0.6, 0.9]:
        for target in [0.1, 0.05, 0.01]:
            length = next(j for j in range(1000) if delta(rho, 1, j) <= target)
            thresholds.append({
                "rho": rho, "Pbar_over_rmin": 1,
                "target_delta": target, "L": length,
                "delta": delta(rho, 1, length), "state_multiplier": 2**length,
                "logdet_gap_per_parameter": np.log1p(delta(rho, 1, length)) - np.log1p(-delta(rho, 1, length)),
            })
    report = {
        "seed": 20260912, "python": platform.python_version(),
        "numpy": np.__version__, "all_checks_passed": True,
        "total_subset_window_checks": sum(w["subsets"] for c in cases for w in c["windows"]),
        "cases": cases, "thresholds": thresholds,
    }
    output = Path(__file__).parent / "results" / "noisy-markov-memory-check.json"
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"output": str(output), "checks": report["total_subset_window_checks"], "thresholds": thresholds}, indent=2))


if __name__ == "__main__":
    main()
