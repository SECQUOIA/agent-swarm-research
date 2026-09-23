"""Independent dense-covariance audit of partial latent observation bounds.

Does not import the author implementation or earlier review implementations.
Run with the isolated research_20260912 uv environment.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np
from scipy.linalg import block_diag, eigh
import sympy as sp


def root(matrix, inverse=False):
    vals, vecs = np.linalg.eigh(matrix)
    factors = np.sqrt(np.maximum(vals, 0))
    if inverse:
        factors = np.where(vals > 1e-12, 1 / np.sqrt(np.maximum(vals, 1e-300)), 0)
    return (vecs * factors) @ vecs.T


def build_covariance(P0, transitions, innovations, observation, noise):
    n, d = len(observation), len(P0)
    loading = np.zeros((n*d, n*d))
    for t in range(n):
        loading[t*d:(t+1)*d, t*d:(t+1)*d] = np.eye(d)
        if t:
            loading[t*d:(t+1)*d, :t*d] = transitions[t-1] @ loading[(t-1)*d:t*d, :t*d]
    latent = loading @ block_diag(P0, *innovations) @ loading.T
    H = block_diag(*observation)
    return latent, H @ latent @ H.T + block_diag(*noise)


def exact_rational_checks():
    half, quarter = sp.Rational(1, 2), sp.Rational(1, 4)
    P0 = sp.diag(0, 1)
    transitions = [sp.Matrix([[0, half], [2, 0]]),
                   sp.Matrix([[0, 1], [half, 0]]),
                   sp.Matrix([[half, half], [0, half]])]
    innovations = [sp.diag(quarter, half), sp.diag(quarter, sp.Rational(3, 8)), sp.eye(2)*quarter]
    H = [sp.Matrix([[1, 1]]), sp.Matrix([[1, 0]]), sp.Matrix([[0, 1]]), sp.Matrix([[half, -half]])]
    V = sp.diag(half, sp.Rational(3, 4), half, 1)
    loading = sp.zeros(8)
    for t in range(4):
        loading[2*t:2*t+2, 2*t:2*t+2] = sp.eye(2)
        if t:
            loading[2*t:2*t+2, :2*t] = transitions[t-1]*loading[2*t-2:2*t, :2*t]
    latent = loading*sp.diag(P0, *innovations)*loading.T
    observed = sp.diag(*H)
    R = observed*latent*observed.T + V
    gamma2, C, B2 = sp.Rational(3, 4), sp.Integer(4), sp.Integer(8)
    snr, kappa = B2, B2/(1+B2)
    # Time-varying rational state coordinates destroy the original Euclidean
    # constants but preserve the intrinsic covariance and SNR promises.
    coordinates = [sp.diag(100, sp.Rational(1, 100)), sp.Matrix([[1, 2], [0, 3]]),
                   sp.diag(sp.Rational(1, 5), 7), sp.Matrix([[2, 1], [1, 1]])]
    packet_scale = [sp.Integer(2), sp.Rational(1, 3), sp.Integer(5), sp.Rational(1, 7)]
    transformed_A = [coordinates[t]*transitions[t-1]*coordinates[t-1].inv() for t in range(1, 4)]
    transformed_Q = [coordinates[t]*innovations[t-1]*coordinates[t].T for t in range(1, 4)]
    transformed_H = [packet_scale[t]*H[t]*coordinates[t].inv() for t in range(4)]
    transformed_P0 = coordinates[0]*P0*coordinates[0].T
    transformed_V = sp.diag(*[packet_scale[t]**2*V[t, t] for t in range(4)])
    transformed_loading = sp.zeros(8)
    for t in range(4):
        transformed_loading[2*t:2*t+2, 2*t:2*t+2] = sp.eye(2)
        if t:
            transformed_loading[2*t:2*t+2, :2*t] = transformed_A[t-1]*transformed_loading[2*t-2:2*t, :2*t]
    transformed_latent = transformed_loading*sp.diag(transformed_P0, *transformed_Q)*transformed_loading.T
    transformed_observed = sp.diag(*transformed_H)
    transformed_R = transformed_observed*transformed_latent*transformed_observed.T+transformed_V
    packet_change = sp.diag(*packet_scale)
    assert transformed_R == packet_change*R*packet_change.T
    for t in range(4):
        Pt = transformed_latent[2*t:2*t+2, 2*t:2*t+2]
        assert (transformed_H[t]*Pt*transformed_H[t].T)[0] <= snr*transformed_V[t, t]
        if t:
            difference = transformed_Q[t-1]-(1-gamma2)*Pt
            assert difference[0, 0] >= 0 and difference[1, 1] >= 0 and difference.det() >= 0
    checks = dict(subset_windows=0, coefficients=0, old_covariances=0, pairs=0,
                  rational_coordinate_invariance_models=0)
    for bits in itertools.product((0, 1), repeat=4):
        selected = [t for t, bit in enumerate(bits) if bit]
        if not selected:
            continue
        S = R.extract(selected, selected)
        for L in range(5):
            checks['subset_windows'] += 1
            A = sp.eye(len(selected))
            histories = []
            for row, t in enumerate(selected):
                history = [j for j in selected[:row] if t-j <= L]
                histories.append(history)
                if history:
                    coefficients = R.extract([t], history)*R.extract(history, history).inv()
                    for k, j in enumerate(history):
                        b = coefficients[k]
                        assert b*b <= B2*gamma2**(t-j)
                        A[row, selected.index(j)] = -b
                        checks['coefficients'] += 1
            residual = A*S*A.T
            old = A*S
            transformed_residual_map = sp.eye(len(selected))
            for row, t in enumerate(selected):
                history = histories[row]
                if history:
                    coefficients = transformed_R.extract([t], history)*transformed_R.extract(history, history).inv()
                    for k, j in enumerate(history):
                        transformed_residual_map[row, selected.index(j)] = -coefficients[k]
            selected_change = packet_change.extract(selected, selected)
            transformed_S = transformed_R.extract(selected, selected)
            transformed_residual = transformed_residual_map*transformed_S*transformed_residual_map.T
            assert transformed_residual_map == selected_change*A*selected_change.inv()
            assert transformed_residual == selected_change*residual*selected_change.T
            checks['rational_coordinate_invariance_models'] += 1
            for row, t in enumerate(selected):
                for col, s in enumerate(selected[:row]):
                    h = t-s
                    if s in histories[row]:
                        assert old[row, col] == 0
                        coefficient = -A[row, col]
                        assert coefficient**2*V[s, s]/residual[row, row] <= kappa**2*gamma2**h
                    else:
                        assert old[row, col]**2 <= C*C*gamma2**h
                        assert old[row, col]**2/(residual[row, row]*V[s, s]) <= kappa*snr*gamma2**h
                        checks['old_covariances'] += 1
                    if h > L:
                        square_bound = C*C*gamma2**h
                        normalized_square_bound = kappa**2*gamma2**h
                    else:
                        series = sum(gamma2**d for d in range(L+1-h, L+1))
                        square_bound = C*C*B2*gamma2**h*series**2
                        normalized_square_bound = kappa**3*snr*gamma2**h*series**2
                    assert residual[row, col]**2 <= square_bound
                    assert residual[row, col]**2/(residual[row, row]*residual[col, col]) <= normalized_square_bound
                    checks['pairs'] += 1
    return checks


def numerical_checks():
    rng = np.random.default_rng(1368572)
    counts = dict(covariance_cases=0, subset_windows=0, coefficients=0,
                  old_covariances=0, residual_pairs=0, contractions=0,
                  nontrivial_delta_models=0, nontrivial_refined_delta_models=0)
    worst = {name: 0.0 for name in (
        'coefficient_excess', 'old_covariance_excess', 'pair_excess',
        'row_excess', 'spectral_excess', 'precision_excess',
        'transport_covariance_excess', 'regression_transport_discrepancy',
        'far_pair_transport_discrepancy', 'prediction_covariance_discrepancy',
        'gain_refinement_excess', 'normalized_coefficient_excess',
        'normalized_old_covariance_excess', 'normalized_pair_excess',
        'refined_row_excess', 'refined_spectral_excess', 'refined_precision_excess')}
    largest_A, largest_update, largest_commutator = 0.0, 0.0, 0.0
    for d in (2, 3, 5):
        n = 6
        for variant in range(8):
            q, Pbar, r = (.25, .6, .95)[variant % 3], 1.0, .4
            hbar = 1.5 if variant < 5 else .5
            gamma = np.sqrt(1-q/Pbar)
            rotation, _ = np.linalg.qr(rng.normal(size=(d, d)))
            initial_eigs = np.linspace(.002, 1, d)
            if variant % 2 == 0:
                initial_eigs[0] = 0
            P0 = (rotation*initial_eigs) @ rotation.T
            marginal = [P0]
            transitions, innovations = [], []
            for t in range(1, n):
                rotation, _ = np.linalg.qr(rng.normal(size=(d, d)))
                target = (rotation*rng.uniform(q+.05*(1-q), 1, d)) @ rotation.T
                M = rng.normal(size=(d, d))
                M *= (.25+.1*variant)/np.linalg.norm(M, 2)
                A = root(target-q*np.eye(d)) @ M @ root(marginal[-1], inverse=True)
                if t == 1 and variant % 2 == 0:
                    vals, vecs = np.linalg.eigh(P0)
                    A += 4*rng.normal(size=(d, 1)) @ vecs[:, :1].T
                Q = target-A @ marginal[-1] @ A.T
                assert np.linalg.eigvalsh(Q).min() >= q-1e-10
                largest_A = max(largest_A, np.linalg.norm(A, 2))
                largest_commutator = max(largest_commutator, np.linalg.norm(A @ marginal[-1]-marginal[-1] @ A, 2))
                transitions.append(A)
                innovations.append(Q)
                marginal.append(target)
            H, V = [], []
            for t in range(n):
                packet = 1+(t+variant) % min(d, 3)
                obs = rng.normal(size=(packet, d))
                obs *= hbar/np.linalg.norm(obs, 2)
                if variant == 3 and t == 2:
                    obs[:] = 0
                if packet > 1 and variant == 4:
                    obs[-1] = obs[0]
                    obs *= hbar/np.linalg.norm(obs, 2)
                M = rng.normal(size=(packet, packet))
                noise = r*np.eye(packet)+(.1+.5*variant)*(M @ M.T)
                H.append(obs)
                V.append(noise)
            latent, R = build_covariance(P0, transitions, innovations, H, V)
            calendar_offsets = np.cumsum([0]+[len(obs) for obs in H])
            idx = [list(range(calendar_offsets[t], calendar_offsets[t+1])) for t in range(n)]
            Cbound, Bbound = hbar*hbar*Pbar, hbar*np.sqrt(Pbar/r)
            snr = Cbound/r
            kappa = snr/(1+snr)
            sqrtV = [root(M) for M in V]
            inverse_sqrtV = [root(M, inverse=True) for M in V]
            counts['covariance_cases'] += 1
            for bits in itertools.product((0, 1), repeat=n):
                selected = [t for t, bit in enumerate(bits) if bit]
                if not selected:
                    continue
                sel_idx = [i for t in selected for i in idx[t]]
                S = R[np.ix_(sel_idx, sel_idx)]
                offsets = np.cumsum([0]+[len(H[t]) for t in selected])
                local_idx = [list(range(offsets[k], offsets[k+1])) for k in range(len(selected))]
                for L in range(n+1):
                    counts['subset_windows'] += 1
                    Ares = np.eye(len(sel_idx))
                    D, histories, predictions, filters = [], [], [], []
                    for row, t in enumerate(selected):
                        history = [j for j in selected[:row] if t-j <= L]
                        histories.append(history)
                        hi = [i for j in history for i in idx[j]]
                        if hi:
                            regression = np.linalg.solve(R[np.ix_(hi, hi)], R[np.ix_(hi, idx[t])]).T
                            columns = [i for j in history for i in local_idx[selected.index(j)]]
                            Ares[np.ix_(local_idx[row], columns)] = -regression
                            residual_covariance = R[np.ix_(idx[t], idx[t])]-regression @ R[np.ix_(hi, idx[t])]
                        else:
                            residual_covariance = R[np.ix_(idx[t], idx[t])]
                        D.append((residual_covariance+residual_covariance.T)/2)
                        # A separate Kalman calculation checks telescoping and
                        # transport against the dense conditional regression.
                        pred, post, gains, updates = {}, {}, {}, {}
                        for j in range(t+1):
                            pred[j] = P0.copy() if j == 0 else transitions[j-1] @ post[j-1] @ transitions[j-1].T+innovations[j-1]
                            if j in history:
                                gain = np.linalg.solve(H[j] @ pred[j] @ H[j].T+V[j], H[j] @ pred[j]).T
                                E = np.eye(d)-gain @ H[j]
                                post[j] = E @ pred[j] @ E.T+gain @ V[j] @ gain.T
                                excess = -np.linalg.eigvalsh(kappa*post[j]-gain @ V[j] @ gain.T).min()
                                worst['gain_refinement_excess'] = max(worst['gain_refinement_excess'], excess)
                                assert excess < 2e-8
                                gains[j] = gain
                                largest_update = max(largest_update, np.linalg.norm(E, 2))
                            else:
                                E = np.eye(d)
                                post[j] = pred[j]
                            updates[j] = E
                        discrepancy = np.linalg.norm(D[-1]-H[t] @ pred[t] @ H[t].T-V[t], 2)
                        worst['prediction_covariance_discrepancy'] = max(worst['prediction_covariance_discrepancy'], discrepancy)
                        assert discrepancy < 2e-8
                        predictions.append(pred[t])
                        filters.append((pred, post, gains, updates))
                    Dfull = block_diag(*D)
                    residual = Ares @ S @ Ares.T
                    old = Ares @ S
                    Dinvroot = block_diag(*[root(M, inverse=True) for M in D])
                    C = Dinvroot @ residual @ Dinvroot
                    comparison = np.zeros((len(selected), len(selected)))
                    for row, t in enumerate(selected):
                        pred, post, gains, updates = filters[row]
                        for col, s in enumerate(selected[:row]):
                            h = t-s
                            T = np.eye(d)
                            for j in range(s+1, t+1):
                                T = transitions[j-1] @ T
                                if j < t:
                                    T = updates[j] @ T
                            excess = -np.linalg.eigvalsh(gamma**(2*h)*pred[t]-T @ post[s] @ T.T).min()
                            worst['transport_covariance_excess'] = max(worst['transport_covariance_excess'], excess)
                            assert excess < 2e-8
                            counts['contractions'] += 1
                            ri, ci = local_idx[row], local_idx[col]
                            if s in histories[row]:
                                coefficient = -Ares[np.ix_(ri, ci)]
                                excess = np.linalg.norm(coefficient, 2)-Bbound*gamma**h
                                worst['coefficient_excess'] = max(worst['coefficient_excess'], excess)
                                assert excess < 2e-8
                                discrepancy = np.linalg.norm(coefficient-H[t] @ T @ gains[s], 2)
                                worst['regression_transport_discrepancy'] = max(worst['regression_transport_discrepancy'], discrepancy)
                                assert discrepancy < 2e-8
                                assert np.linalg.norm(old[np.ix_(ri, ci)], 2) < 2e-8
                                normalized_coefficient = Dinvroot[np.ix_(ri, ri)] @ coefficient @ sqrtV[s]
                                excess = np.linalg.norm(normalized_coefficient, 2)-kappa*gamma**h
                                worst['normalized_coefficient_excess'] = max(worst['normalized_coefficient_excess'], excess)
                                assert excess < 2e-8
                                counts['coefficients'] += 1
                            else:
                                excess = np.linalg.norm(old[np.ix_(ri, ci)], 2)-Cbound*gamma**h
                                worst['old_covariance_excess'] = max(worst['old_covariance_excess'], excess)
                                assert excess < 2e-8
                                normalized_old = Dinvroot[np.ix_(ri, ri)] @ old[np.ix_(ri, ci)] @ inverse_sqrtV[s]
                                excess = np.linalg.norm(normalized_old, 2)-np.sqrt(kappa*snr)*gamma**h
                                worst['normalized_old_covariance_excess'] = max(worst['normalized_old_covariance_excess'], excess)
                                assert excess < 2e-8
                                counts['old_covariances'] += 1
                            if h > L:
                                bound = Cbound*gamma**h
                                normalized_bound = kappa*gamma**h
                                transported = H[t] @ T @ predictions[col] @ H[s].T
                                discrepancy = np.linalg.norm(residual[np.ix_(ri, ci)]-transported, 2)
                                worst['far_pair_transport_discrepancy'] = max(worst['far_pair_transport_discrepancy'], discrepancy)
                                assert discrepancy < 2e-8
                            else:
                                bound = Cbound*Bbound*sum(gamma**(h+2*j) for j in range(L+1-h, L+1))
                                normalized_bound = kappa*np.sqrt(kappa*snr)*sum(gamma**(h+2*j) for j in range(L+1-h, L+1))
                            excess = np.linalg.norm(residual[np.ix_(ri, ci)], 2)-bound
                            worst['pair_excess'] = max(worst['pair_excess'], excess)
                            assert excess < 2e-8
                            counts['residual_pairs'] += 1
                            comparison[row, col] = comparison[col, row] = np.linalg.norm(C[np.ix_(ri, ci)], 2)
                            excess = comparison[row, col]-normalized_bound
                            worst['normalized_pair_excess'] = max(worst['normalized_pair_excess'], excess)
                            assert excess < 2e-8
                    near = gamma**(L+2)*(1-gamma**L)*(1-gamma**(L+1))/((1-gamma)*(1-gamma**2))
                    delta = 2*Cbound/r*(gamma**(L+1)/(1-gamma)+Bbound*near)
                    refined_delta = 2*kappa*(gamma**(L+1)/(1-gamma)+np.sqrt(kappa*snr)*near)
                    counts['nontrivial_delta_models'] += int(delta < 1)
                    counts['nontrivial_refined_delta_models'] += int(refined_delta < 1)
                    excess = comparison.sum(axis=1).max()-delta
                    worst['row_excess'] = max(worst['row_excess'], excess)
                    assert excess < 2e-8
                    excess = comparison.sum(axis=1).max()-refined_delta
                    worst['refined_row_excess'] = max(worst['refined_row_excess'], excess)
                    assert excess < 2e-8
                    eigenvalues = np.linalg.eigvalsh(C)
                    error = max(abs(eigenvalues-1))
                    worst['spectral_excess'] = max(worst['spectral_excess'], error-delta)
                    assert error <= delta+2e-8
                    worst['refined_spectral_excess'] = max(worst['refined_spectral_excess'], error-refined_delta)
                    assert error <= refined_delta+2e-8
                    Qlocal = Ares.T @ np.linalg.solve(Dfull, Ares)
                    relative_eigenvalues = eigh(Qlocal, np.linalg.inv(S), eigvals_only=True)
                    excess = max(abs(relative_eigenvalues-1))-delta
                    worst['precision_excess'] = max(worst['precision_excess'], excess)
                    assert excess < 2e-8
                    excess = max(abs(relative_eigenvalues-1))-refined_delta
                    worst['refined_precision_excess'] = max(worst['refined_precision_excess'], excess)
                    assert excess < 2e-8
    # gamma=0 permits nonzero A on a singular initial covariance's nullspace.
    P0 = np.diag([0., 1.])
    transitions = [np.array([[4., 0.], [-3., 0.]]), np.zeros((2, 2))]
    H = [np.array([[1., 1.]]), np.array([[1., 0.]]), np.array([[0., 1.]])]
    _, R = build_covariance(P0, transitions, [np.eye(2), np.eye(2)], H, [np.eye(1)]*3)
    assert np.array_equal(R, np.diag(np.diag(R)))
    return dict(counts=counts, worst=worst, largest_transition_norm=largest_A,
                largest_update_operator_norm=largest_update,
                largest_transition_marginal_commutator_norm=largest_commutator,
                gamma_zero_with_nonzero_transition='exact independence passed')


if __name__ == '__main__':
    report = dict(status='passed', caveat='Numerical tests supplement the proof; only the rational subsection uses exact arithmetic.',
                  exact=exact_rational_checks(), numerical=numerical_checks())
    path = Path(__file__).with_name('partial-latent-memory-independent-validation.json')
    path.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
