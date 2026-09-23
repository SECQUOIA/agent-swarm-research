"""Independent finite-history covariance and finite-state hull review.

This deliberately builds latent covariances from innovation loadings and local
regressions from dense principal submatrices. It imports no proposed solver.
Run with uv run --project code/research_20260912 python <this file>.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np
from scipy.linalg import eigh
from scipy.optimize import linprog


def latent_covariance(a, innovation_variance):
    n = len(innovation_variance)
    loading = np.eye(n)
    for t in range(1, n):
        loading[t, :t] = a[t - 1] * loading[t - 1, :t]
    return (loading * innovation_variance) @ loading.T


def local_model(R, chosen, window):
    A = np.eye(len(chosen))
    variances = []
    histories = []
    for row, t in enumerate(chosen):
        earlier = [j for j in chosen[:row] if j >= t - window]
        histories.append(earlier)
        if earlier:
            beta = np.linalg.solve(R[np.ix_(earlier, earlier)], R[earlier, t])
            for j, b in zip(earlier, beta, strict=True):
                A[row, chosen.index(j)] = -b
            variances.append(R[t, t] - R[t, earlier] @ beta)
        else:
            variances.append(R[t, t])
    D = np.array(variances)
    Q = A.T @ (A / D[:, None])
    return A, D, Q, histories


def all_subsets(n, include_empty=False):
    for bits in itertools.product((0, 1), repeat=n):
        chosen = [i for i, bit in enumerate(bits) if bit]
        if chosen or include_empty:
            yield chosen


def run_covariance_review():
    rng = np.random.default_rng(847209)
    cases = []
    n = 8
    for rho in (0.0, 0.2, 0.55, 0.9, 0.985):
        for nugget in (0.025, 1.0, 25.0):
            a = np.full(n - 1, rho)
            q = np.r_[1.0, np.full(n - 1, 1 - rho * rho)]
            cases.append((f"stationary-{rho}-{nugget}", a, q, np.full(n, nugget)))
    for k in range(12):
        a = rng.uniform(-0.95, 0.95, n - 1)
        q = rng.uniform(0, 2, n)
        q[rng.random(n) < 0.4] = 0
        if k % 3 == 0:
            a[rng.integers(0, n - 1)] = 0
        r = np.exp(rng.uniform(-3, 3, n))
        cases.append((f"nonstationary-{k}", a, q, r))
    cases.extend([
        ("deterministic-signed", np.array([-.8, .3, -.6, .9, -.9, -.4, .5]),
         np.r_[1.0, np.zeros(n - 1)], np.exp(rng.uniform(-2, 2, n))),
        ("zero-latent", np.full(n - 1, -.75), np.zeros(n), np.ones(n)),
    ])
    counts = {"covariance_cases": len(cases), "subset_windows": 0,
              "local_coefficients": 0, "excluded_covariances": 0,
              "residual_pairs": 0, "information_checks": 0}
    worst = {"coefficient_excess": 0.0, "excluded_covariance_excess": 0.0,
             "gain_pair_excess": 0.0, "gain_row_excess": 0.0,
             "spectral_excess": 0.0, "sandwich_excess": 0.0,
             "logdet_excess": 0.0, "dense_information_discrepancy": 0.0,
             "largest_eigenvalue_error_over_bound": 0.0}
    for label, a, q, nugget in cases:
        P = latent_covariance(a, q)
        R = P + np.diag(nugget)
        Pbar, rmin, rho = np.diag(P).max(), nugget.min(), np.abs(a).max()
        gain_cap = Pbar / (Pbar + rmin)
        F = rng.normal(size=(n, 3))
        prior = np.diag([0.03, 0.4, 2.0])
        for chosen in all_subsets(n):
            Rsub = R[np.ix_(chosen, chosen)]
            precision = np.linalg.inv(Rsub)
            true_J = prior + F[chosen].T @ precision @ F[chosen]
            for window in range(n + 1):
                counts["subset_windows"] += 1
                A, D, Q, histories = local_model(R, chosen, window)
                residual_cov = A @ Rsub @ A.T
                C = residual_cov / np.sqrt(D[:, None] * D[None, :])
                assert np.max(np.abs(np.diag(C) - 1)) < 2e-10, label
                assert D.min() >= rmin - 2e-12, label
                old_cov = A @ Rsub
                for row, t in enumerate(chosen):
                    for col, j in enumerate(chosen[:row]):
                        if j in histories[row]:
                            counts["local_coefficients"] += 1
                            excess = abs(A[row, col]) - gain_cap * rho ** (t - j)
                            worst["coefficient_excess"] = max(worst["coefficient_excess"], excess)
                            assert excess < 2e-10, (label, chosen, window, t, j, excess)
                            assert abs(old_cov[row, col]) < 2e-10, label
                        else:
                            counts["excluded_covariances"] += 1
                            excess = abs(old_cov[row, col]) - Pbar * rho ** (t - j)
                            worst["excluded_covariance_excess"] = max(worst["excluded_covariance_excess"], excess)
                            assert excess < 2e-10, (label, chosen, window, t, j, excess)
                        counts["residual_pairs"] += 1
                        h = t - j
                        if h > window:
                            pair_bound = Pbar * rho ** h * (1 + gain_cap * sum(rho ** (2 * d) for d in range(1, window + 1)))
                        else:
                            pair_bound = gain_cap * Pbar * sum(rho ** (h + 2 * d) for d in range(window + 1 - h, window + 1))
                        excess = abs(residual_cov[row, col]) - pair_bound
                        worst["gain_pair_excess"] = max(worst["gain_pair_excess"], excess)
                        assert excess < 2e-10, (label, chosen, window, t, j, excess)
                delta = (2 * Pbar / rmin * rho ** (window + 1) / (1 - rho)
                         * (1 + gain_cap * rho * (1 - rho ** window) / (1 - rho)))
                E = C - np.eye(len(chosen))
                row_excess = np.abs(E).sum(axis=1).max() - delta
                eigen_error = np.max(np.abs(np.linalg.eigvalsh(E)))
                worst["gain_row_excess"] = max(worst["gain_row_excess"], row_excess)
                worst["spectral_excess"] = max(worst["spectral_excess"], eigen_error - delta)
                assert row_excess < 3e-10, (label, chosen, window, row_excess)
                # A generalized eigenvalue check uses a different path from B B^T.
                relative_Q_eigenvalues = eigh(Q, precision, eigvals_only=True)
                sandwich_excess = max(1 - delta - relative_Q_eigenvalues.min(),
                                      relative_Q_eigenvalues.max() - 1 - delta)
                worst["sandwich_excess"] = max(worst["sandwich_excess"], sandwich_excess)
                assert sandwich_excess < 3e-9, (label, chosen, window, sandwich_excess)
                if delta > 1e-14:
                    worst["largest_eigenvalue_error_over_bound"] = max(
                        worst["largest_eigenvalue_error_over_bound"], eigen_error / delta)
                counts["information_checks"] += 1
                surrogate_J = prior + F[chosen].T @ Q @ F[chosen]
                components = (A @ F[chosen]) / np.sqrt(D[:, None])
                discrepancy = np.max(np.abs(surrogate_J - prior - components.T @ components))
                worst["dense_information_discrepancy"] = max(worst["dense_information_discrepancy"], discrepancy)
                assert discrepancy < 3e-9, label
                relative_J_eigenvalues = eigh(surrogate_J, true_J, eigvals_only=True)
                assert relative_J_eigenvalues.min() >= 1 - delta - 2e-9, label
                assert relative_J_eigenvalues.max() <= 1 + delta + 2e-9, label
                if delta < 1:
                    log_difference = np.linalg.slogdet(surrogate_J)[1] - np.linalg.slogdet(true_J)[1]
                    excess = max(3 * np.log1p(-delta) - log_difference,
                                 log_difference - 3 * np.log1p(delta))
                    worst["logdet_excess"] = max(worst["logdet_excess"], excess)
                    assert excess < 2e-9, (label, chosen, window, excess)
                if window >= n - 1:
                    assert eigen_error < 2e-10, label
    return {"bound_checked": "Finite-window row bound with K <= Pbar/(Pbar+rmin)",
            "counts": counts, "worst": worst}


def finite_state_graph(R, F, window, count=None):
    """Construct only reachable states, with a separate terminal sink."""
    n, p = F.shape
    source = (0, 0, 0)
    states = {source: 0}
    frontier = {source}
    arcs = []
    for t in range(n):
        following = set()
        for state in sorted(frontier):
            _, mask, used = state
            history = [t - d for d in range(1, window + 1)
                       if t - d >= 0 and mask & (1 << (d - 1))]
            history.sort()
            for choose in (0, 1):
                next_used = used + choose if count is not None else 0
                if count is not None and (next_used > count or next_used + n - t - 1 < count):
                    continue
                next_mask = ((mask << 1) | choose) & ((1 << window) - 1)
                target = (t + 1, next_mask, next_used)
                states.setdefault(target, len(states))
                following.add(target)
                W = np.zeros((p, p))
                if choose:
                    if history:
                        beta = np.linalg.solve(R[np.ix_(history, history)], R[history, t])
                        f = F[t] - beta @ F[history]
                        variance = R[t, t] - R[t, history] @ beta
                    else:
                        f, variance = F[t], R[t, t]
                    W = np.outer(f, f) / variance
                arcs.append((state, target, t, choose, W))
        frontier = following
    sink = (n + 1, -1, -1)
    states[sink] = len(states)
    for state in sorted(frontier):
        arcs.append((state, sink, n, 0, np.zeros((p, p))))
    flow = np.zeros((len(states), len(arcs)))
    visits = np.zeros((n, len(arcs)))
    information = np.array([arc[-1] for arc in arcs])
    rhs = np.zeros(len(states))
    rhs[states[source]], rhs[states[sink]] = 1, -1
    for j, (start, end, t, choose, _) in enumerate(arcs):
        flow[states[start], j], flow[states[end], j] = 1, -1
        if choose:
            visits[t, j] = 1
    return flow, rhs, visits, information


def run_hull_review():
    rng = np.random.default_rng(63918)
    n, p = 7, 3
    a = rng.uniform(-0.85, 0.85, n - 1)
    P = latent_covariance(a, rng.uniform(0, 2, n))
    R = P + np.diag(rng.uniform(0.05, 3, n))
    F = rng.normal(size=(n, p))
    checks = 0
    worst = 0.0
    for window in (0, 1, 2, 4):
        for count in (None, 0, 1, 3, 7):
            flow, rhs, visits, information = finite_state_graph(R, F, window, count)
            designs = []
            for chosen in all_subsets(n, include_empty=True):
                if count is not None and len(chosen) != count:
                    continue
                z = np.zeros(n)
                z[chosen] = 1
                J = np.zeros((p, p))
                if chosen:
                    _, _, Q, _ = local_model(R, chosen, window)
                    J = F[chosen].T @ Q @ F[chosen]
                designs.append((z, J))
            for _ in range(20):
                H = rng.normal(size=(p, p))
                H = (H + H.T) / 2
                v = rng.normal(size=n)
                costs = np.einsum("ij,kij->k", H, information) + v @ visits
                result = linprog(-costs, A_eq=flow, b_eq=rhs, bounds=(0, None), method="highs")
                assert result.success, result.message
                brute = max(np.sum(H * J) + v @ z for z, J in designs)
                difference = abs(-result.fun - brute)
                assert difference < 2e-8, (window, count, difference)
                worst = max(worst, difference)
                checks += 1
            # Fix every design's visits. All feasible flows must induce its J.
            for z, J in designs:
                H = rng.normal(size=(p, p))
                costs = np.einsum("ij,kij->k", H, information)
                result = linprog(-costs, A_eq=np.vstack((flow, visits)),
                                 b_eq=np.r_[rhs, z], bounds=(0, None), method="highs")
                assert result.success, result.message
                difference = abs(-result.fun - np.sum(H * J))
                assert difference < 2e-8, (window, count, z, difference)
                worst = max(worst, difference)
                checks += 1
    return {"linear_hull_and_fixed_visits_checks": checks, "maximum_objective_discrepancy": worst}


def run_algebra_review():
    worst = 0.0
    for rho in np.r_[np.linspace(0, .99, 51), .999, .9999]:
        for window in range(31):
            near = sum(sum(rho ** (h + 2 * d) for d in range(window + 1 - h, window + 1))
                       for h in range(1, window + 1))
            far = rho ** (window + 1) / (1 - rho) * sum(rho ** (2 * d) for d in range(window + 1))
            closed = rho ** (window + 1) * (1 - rho ** (window + 1)) / (1 - rho) ** 2
            relative_error = abs(near + far - closed) / max(1, closed)
            worst = max(worst, relative_error)
            assert relative_error < 5e-13
    # Nonzero overlapping-window residual covariance, exactly -1/32.
    R = np.array([[2, .5, .25], [.5, 2, .5], [.25, .5, 2]])
    A, D, _, _ = local_model(R, [0, 1, 2], 1)
    residual = A @ R @ A.T
    assert residual[2, 1] == -1 / 32
    assert D[1] == D[2] == 15 / 8
    return {"finite_series_max_relative_error": worst,
            "overlap_example_residual_covariance": residual[2, 1],
            "overlap_example_normalized_covariance": residual[2, 1] / D[1]}


if __name__ == "__main__":
    report = {"status": "passed", "scope": "Independent numerical checks, not interval arithmetic",
              "algebra": run_algebra_review(),
              "covariance": run_covariance_review(), "finite_state_hull": run_hull_review()}
    output = Path(__file__).with_name("noisy-markov-independent-validation.json")
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
