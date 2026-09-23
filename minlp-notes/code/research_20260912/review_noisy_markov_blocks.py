"""Independent audit of the full-block, noise-whitened memory extension."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np
from scipy.linalg import block_diag, eigh


def matrix_power_spd(M, power):
    values, vectors = np.linalg.eigh(M)
    return (vectors * values ** power) @ vectors.T


def indices(times, block_size):
    return [time * block_size + j for time in times for j in range(block_size)]


def latent_covariance(transitions, innovations):
    n, d = len(innovations), len(innovations[0])
    loading = np.zeros((n * d, n * d))
    for t in range(n):
        loading[t*d:(t+1)*d, t*d:(t+1)*d] = np.eye(d)
        if t:
            loading[t*d:(t+1)*d, :t*d] = transitions[t-1] @ loading[(t-1)*d:t*d, :t*d]
    return loading @ block_diag(*innovations) @ loading.T


def block_local_model(R, chosen, window, d):
    size = len(chosen) * d
    A = np.eye(size)
    residual_variance_blocks = []
    histories = []
    for row, t in enumerate(chosen):
        history = [j for j in chosen[:row] if j >= t - window]
        histories.append(history)
        ti = indices([t], d)
        if history:
            hi = indices(history, d)
            beta = np.linalg.solve(R[np.ix_(hi, hi)], R[np.ix_(hi, ti)]).T
            A[row*d:(row+1)*d, indices([chosen.index(j) for j in history], d)] = -beta
            D = R[np.ix_(ti, ti)] - beta @ R[np.ix_(hi, ti)]
        else:
            D = R[np.ix_(ti, ti)].copy()
        residual_variance_blocks.append((D + D.T) / 2)
    D = block_diag(*residual_variance_blocks)
    Q = A.T @ np.linalg.solve(D, A)
    return A, D, Q, histories, residual_variance_blocks


def run_review():
    rng = np.random.default_rng(849163)
    worst = dict.fromkeys([
        "whitened_covariance_discrepancy", "whitening_fisher_discrepancy",
        "whitening_surrogate_information_discrepancy",
        "gain_coefficient_excess", "excluded_cross_covariance_excess",
        "pair_bound_excess", "block_row_excess", "spectral_excess",
        "relative_precision_excess", "local_information_discrepancy",
        "logdet_bound_excess", "full_history_conditioning_excess"], 0.0)
    counts = {"covariance_cases": 0, "subset_windows": 0,
              "regression_blocks": 0, "excluded_cross_covariance_blocks": 0,
              "residual_pairs": 0, "fisher_checks": 0}
    noncommutativity = 0.0
    n, parameters = 6, 3
    for dimension in (2, 3):
        d = dimension
        for variant in range(10):
            nominal_rho = (0.0, 0.15, 0.55, 0.8, 0.96)[variant % 5]
            T = []
            for t in range(n - 1):
                M = rng.normal(size=(d, d))
                M *= nominal_rho / np.linalg.norm(M, 2)
                if variant == 8 and t == 2:
                    M[:] = 0
                T.append(M)
            Qwhite = []
            for t in range(n):
                M = rng.normal(size=(d, d))
                q = M @ M.T / d
                if variant in (6, 8) and t:
                    q[:] = 0
                if variant == 9:
                    q[:] = 0
                Qwhite.append(q)
            Pwhite = latent_covariance(T, Qwhite)
            beta_cap = max(np.linalg.eigvalsh(Pwhite[t*d:(t+1)*d, t*d:(t+1)*d]).max()
                           for t in range(n))
            rho = max(np.linalg.norm(M, 2) for M in T)
            gain_cap = beta_cap / (beta_cap + 1)
            V, sqrtV, inverse_sqrtV = [], [], []
            for _ in range(n):
                rotation, _ = np.linalg.qr(rng.normal(size=(d, d)))
                noise = (rotation * np.exp(rng.uniform(-2.5, 2.5, d))) @ rotation.T
                V.append(noise)
                sqrtV.append(matrix_power_spd(noise, .5))
                inverse_sqrtV.append(matrix_power_spd(noise, -.5))
            # Construct the original model, then independently recover its
            # whitened covariance from the original transitions/innovations.
            original_T = [sqrtV[t] @ T[t-1] @ inverse_sqrtV[t-1] for t in range(1, n)]
            original_Q = [sqrtV[t] @ Qwhite[t] @ sqrtV[t].T for t in range(n)]
            original_P = latent_covariance(original_T, original_Q)
            R = original_P + block_diag(*V)
            W = block_diag(*inverse_sqrtV)
            Rwhite = W @ R @ W.T
            discrepancy = np.max(np.abs(Rwhite - Pwhite - np.eye(n*d)))
            worst["whitened_covariance_discrepancy"] = max(worst["whitened_covariance_discrepancy"], discrepancy)
            assert discrepancy < 1e-10
            _, _, _, _, full_history_D = block_local_model(Rwhite, list(range(n)), n, d)
            d_star = min(np.linalg.eigvalsh(M).min() for M in full_history_D)
            if len(T):
                P0 = Pwhite[:d, :d]
                noncommutativity = max(noncommutativity, np.linalg.norm(T[0] @ P0 - P0 @ T[0], 2))
            F = rng.normal(size=(n*d, parameters))
            Fwhite = W @ F
            prior = np.diag([.01, .3, 1.0])
            counts["covariance_cases"] += 1
            for bits in itertools.product((0, 1), repeat=n):
                chosen = [i for i, bit in enumerate(bits) if bit]
                if not chosen:
                    continue
                chosen_indices = indices(chosen, d)
                Rsub = Rwhite[np.ix_(chosen_indices, chosen_indices)]
                true_precision = np.linalg.inv(Rsub)
                selected_F = Fwhite[chosen_indices]
                Jtrue = prior + selected_F.T @ true_precision @ selected_F
                original_Rsub = R[np.ix_(chosen_indices, chosen_indices)]
                original_F = F[chosen_indices]
                original_J = prior + original_F.T @ np.linalg.solve(original_Rsub, original_F)
                discrepancy = np.max(np.abs(Jtrue - original_J))
                worst["whitening_fisher_discrepancy"] = max(worst["whitening_fisher_discrepancy"], discrepancy)
                assert discrepancy < 2e-9
                for window in range(n + 1):
                    counts["subset_windows"] += 1
                    A, D, Q, histories, Dblocks = block_local_model(Rwhite, chosen, window, d)
                    E_cov = A @ Rsub @ A.T
                    inverse_sqrtD = block_diag(*[matrix_power_spd(M, -.5) for M in Dblocks])
                    C = inverse_sqrtD @ E_cov @ inverse_sqrtD
                    C_error = C - np.eye(len(chosen)*d)
                    old_cov = A @ Rsub
                    comparison = np.zeros((len(chosen), len(chosen)))
                    for row, t in enumerate(chosen):
                        ri = indices([row], d)
                        assert np.linalg.eigvalsh(Dblocks[row]).min() >= 1 - 1e-10
                        excess = -np.linalg.eigvalsh(Dblocks[row] - full_history_D[t]).min()
                        worst["full_history_conditioning_excess"] = max(worst["full_history_conditioning_excess"], excess)
                        assert excess < 2e-10
                        assert np.linalg.norm(C_error[np.ix_(ri, ri)], 2) < 2e-10
                        for col, s in enumerate(chosen[:row]):
                            ci = indices([col], d)
                            h = t - s
                            if s in histories[row]:
                                counts["regression_blocks"] += 1
                                excess = np.linalg.norm(A[np.ix_(ri, ci)], 2) - gain_cap * rho ** h
                                worst["gain_coefficient_excess"] = max(worst["gain_coefficient_excess"], excess)
                                assert excess < 2e-10
                                assert np.linalg.norm(old_cov[np.ix_(ri, ci)], 2) < 2e-10
                            else:
                                counts["excluded_cross_covariance_blocks"] += 1
                                excess = np.linalg.norm(old_cov[np.ix_(ri, ci)], 2) - beta_cap * rho ** h
                                worst["excluded_cross_covariance_excess"] = max(worst["excluded_cross_covariance_excess"], excess)
                                assert excess < 2e-10
                            counts["residual_pairs"] += 1
                            if h > window:
                                pair_bound = beta_cap * rho ** h * (1 + gain_cap * sum(rho ** (2*k) for k in range(1, window+1)))
                            else:
                                pair_bound = gain_cap * beta_cap * sum(rho ** (h+2*k) for k in range(window+1-h, window+1))
                            excess = np.linalg.norm(E_cov[np.ix_(ri, ci)], 2) - pair_bound
                            worst["pair_bound_excess"] = max(worst["pair_bound_excess"], excess)
                            assert excess < 2e-10
                            comparison[row, col] = comparison[col, row] = np.linalg.norm(C[np.ix_(ri, ci)], 2)
                    delta = (2*beta_cap/d_star*rho**(window+1)/(1-rho)
                             * (1+gain_cap*rho*(1-rho**window)/(1-rho)))
                    block_row_excess = comparison.sum(axis=1).max() - delta
                    spectral_error = np.linalg.norm(C_error, 2)
                    worst["block_row_excess"] = max(worst["block_row_excess"], block_row_excess)
                    worst["spectral_excess"] = max(worst["spectral_excess"], spectral_error - delta)
                    assert block_row_excess < 2e-10
                    assert spectral_error <= np.linalg.norm(comparison, 2) + 2e-10
                    assert spectral_error <= delta + 2e-10
                    eigenvalues = eigh(Q, true_precision, eigvals_only=True)
                    excess = max(1-delta-eigenvalues.min(), eigenvalues.max()-1-delta)
                    worst["relative_precision_excess"] = max(worst["relative_precision_excess"], excess)
                    assert excess < 2e-9
                    counts["fisher_checks"] += 1
                    Jlocal = prior + selected_F.T @ Q @ selected_F
                    _, _, original_local_Q, _, _ = block_local_model(R, chosen, window, d)
                    original_local_J = prior + original_F.T @ original_local_Q @ original_F
                    discrepancy = np.max(np.abs(Jlocal - original_local_J))
                    worst["whitening_surrogate_information_discrepancy"] = max(
                        worst["whitening_surrogate_information_discrepancy"], discrepancy)
                    assert discrepancy < 2e-9
                    G = A @ selected_F
                    Jsum = prior.copy()
                    for row in range(len(chosen)):
                        g = G[row*d:(row+1)*d]
                        Jsum += g.T @ np.linalg.solve(Dblocks[row], g)
                    discrepancy = np.max(np.abs(Jlocal - Jsum))
                    worst["local_information_discrepancy"] = max(worst["local_information_discrepancy"], discrepancy)
                    assert discrepancy < 2e-9
                    if delta < 1:
                        gap = np.linalg.slogdet(Jlocal)[1] - np.linalg.slogdet(Jtrue)[1]
                        excess = max(parameters*np.log1p(-delta)-gap, gap-parameters*np.log1p(delta))
                        worst["logdet_bound_excess"] = max(worst["logdet_bound_excess"], excess)
                        assert excess < 2e-9
    P = np.diag([100, .01])
    V = np.array([[1, .9], [.9, 1]])
    unwhitened_gain = np.linalg.solve((P + V).T, P.T).T
    return {"status": "passed", "scope": "Numerical independent checks, not interval arithmetic",
            "row_bound": "Gain refinement with full-history d_star normalization",
            "counts": counts, "worst": worst,
            "largest_transition_marginal_commutator_norm": noncommutativity,
            "unwhitened_gain_norm_counterexample": np.linalg.norm(unwhitened_gain, 2),
            "unwhitened_identity_minus_gain_norm_counterexample": np.linalg.norm(np.eye(2)-unwhitened_gain, 2)}


if __name__ == "__main__":
    report = run_review()
    Path(__file__).with_name("noisy-markov-block-independent-validation.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
