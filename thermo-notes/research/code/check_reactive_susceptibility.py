"""Independent finite-difference checks of the candidate conductance identities.

Run: python research/code/check_reactive_susceptibility.py
No molecular dynamics or experimental validation is implied.
"""
import json
import numpy as np


def solve_capacity(edges, conductance, n):
    incidence = np.zeros((len(edges), n))
    for k, (i, j) in enumerate(edges):
        incidence[k, i] = -1
        incidence[k, j] = 1
    laplacian = incidence.T @ (conductance[:, None] * incidence)
    q = np.zeros(n)
    q[-1] = 1
    q[1:-1] = np.linalg.solve(laplacian[1:-1, 1:-1], -laplacian[1:-1, -1])
    drop = incidence @ q
    cap = np.sum(conductance * drop**2)
    return cap, q, incidence, laplacian, drop


def main():
    rng = np.random.default_rng(772951)
    worst_slope = worst_curvature = worst_bound_violation = 0.0
    curvature_fraction = []
    count = 0
    for _ in range(100):
        n = int(rng.integers(4, 18))
        edges = [(i, i + 1) for i in range(n - 1)]
        edges += [(i, j) for i in range(n) for j in range(i + 2, n)
                  if rng.uniform() < 0.2]
        c = np.exp(rng.normal(0, 1, len(edges)))
        field = rng.normal(0, 1, len(edges))
        cap, q, incidence, laplacian, drop = solve_capacity(edges, c, n)
        nu = c * drop**2 / cap
        mean = nu @ field
        variance = nu @ (field - mean)**2
        forcing = incidence.T @ (c * field * drop)
        h = np.zeros(n)
        h[1:-1] = np.linalg.solve(laplacian[1:-1, 1:-1], -forcing[1:-1])
        response = np.sum(c * (incidence @ h)**2)
        analytic_curvature = variance - 2 * response / cap
        eps = 2e-4
        plus = np.log(solve_capacity(edges, c * np.exp(eps * field), n)[0])
        minus = np.log(solve_capacity(edges, c * np.exp(-eps * field), n)[0])
        fd_slope = (plus - minus) / (2 * eps)
        fd_curvature = (plus + minus - 2 * np.log(cap)) / eps**2
        worst_slope = max(worst_slope, abs(fd_slope - mean))
        worst_curvature = max(worst_curvature, abs(fd_curvature - analytic_curvature))
        assert abs(analytic_curvature) <= variance + 1e-10
        curvature_fraction.append(analytic_curvature / variance)
        for lam in rng.uniform(-2, 2, 12):
            exact = solve_capacity(edges, c * np.exp(lam * field), n)[0] / cap
            lower = 1 / (nu @ np.exp(-lam * field))
            upper = nu @ np.exp(lam * field)
            violation = max(lower - exact, exact - upper, 0)
            worst_bound_violation = max(worst_bound_violation, violation)
            assert violation < 1e-10
            count += 1
    # Exactly solvable examples with opposite curvature and identical nu at lambda=0.
    fields = np.array([-1.0, 1.0])
    parallel = [(0, 1), (0, 1)]
    series = [(0, 1), (1, 2)]
    for lam in [-2.0, -0.5, 0.0, 0.5, 2.0]:
        p = solve_capacity(parallel, np.exp(lam * fields), 2)[0] / 2
        s = solve_capacity(series, np.exp(lam * fields), 3)[0] / 0.5
        assert np.isclose(p, np.cosh(lam))
        assert np.isclose(s, 1 / np.cosh(lam))
    report = {
        "seed": 772951,
        "random_networks": 100,
        "finite_perturbation_comparisons": count,
        "maximum_bound_violation": worst_bound_violation,
        "maximum_slope_absolute_finite_difference_error": worst_slope,
        "maximum_curvature_absolute_finite_difference_error": worst_curvature,
        "minimum_curvature_over_variance": min(curvature_fraction),
        "maximum_curvature_over_variance": max(curvature_fraction),
        "sharp_series_and_parallel_examples": "passed",
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
