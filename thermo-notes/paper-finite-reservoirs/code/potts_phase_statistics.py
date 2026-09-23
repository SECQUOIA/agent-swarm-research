"""Reproduce the pure-spin Voronoi phase statistics in Section 7.

The model has J=1, beta=4 log(2), and no momenta. Euclidean Voronoi
distance in the three occupation fractions assigns a configuration to
the combined ordered phase when max(n_j) >= N/2, including ties.
Occupation sums are exact apart from floating-point evaluation.
"""
import json
from pathlib import Path

import numpy as np
from scipy.special import gammaln


def phase_statistics(n):
    """Sum color-permutation orbits, retaining the phase assignment."""
    beta = 4 * np.log(2)
    log_factorial = gammaln(np.arange(n + 1) + 1)
    # Remove the common leading partition exponent before exponentiating.
    log_scale = n * (np.log(3) + 2 * np.log(2) / 3)
    total_mass = ordered_mass = first_moment = second_moment = 0.0
    for n1 in range((n + 2) // 3, n + 1):
        n2 = np.arange((n - n1 + 1) // 2, min(n1, n - n1) + 1)
        n3 = n - n1 - n2
        multiplicity = np.where(
            (n1 == n2) & (n2 == n3), 1,
            np.where((n1 == n2) | (n2 == n3), 3, 6),
        )
        squared_sum = n1 * n1 + n2 * n2 + n3 * n3
        log_weight = (
            log_factorial[n] - log_factorial[n1] - log_factorial[n2]
            - log_factorial[n3] + np.log(multiplicity)
            + beta * squared_sum / (2 * n) - log_scale
        )
        weights = np.exp(log_weight)
        mass = weights.sum()
        total_mass += mass
        if 2 * n1 >= n:
            # Center at the ordered energy to avoid subtracting O(N^2) moments.
            deviation = -squared_sum / (2 * n) + n / 4
            ordered_mass += mass
            first_moment += np.dot(weights, deviation)
            second_moment += np.dot(weights, deviation * deviation)
    variance = second_moment / ordered_mass - (first_moment / ordered_mass) ** 2
    return {
        "n": n,
        "ordered_probability": float(ordered_mass / total_mass),
        "ordered_variance_per_spin": float(variance / n),
    }


if __name__ == "__main__":
    beta = 4 * np.log(2)
    phase_ratio = np.sqrt(2 * (3 - beta) / (6 - beta))
    results = {
        "model": {"J": 1, "beta": float(beta), "kinetic_shape": 0},
        "phase_assignment": "Euclidean Voronoi cells in three occupation fractions",
        "ordered_event": "2 * max(n_j) >= N; ordered-disordered ties go to ordered",
        "rate_excess": float(np.log(3) - 19 * np.log(2) / 12),
        "limiting_ordered_probability": float(3 * phase_ratio / (1 + 3 * phase_ratio)),
        "limiting_ordered_variance_per_spin": float(1 / (6 * (3 - beta))),
        "finite_size_results": [phase_statistics(n) for n in (3000, 12000)],
    }
    output = Path(__file__).resolve().parents[1] / "data" / "potts-phase-statistics.json"
    output.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
