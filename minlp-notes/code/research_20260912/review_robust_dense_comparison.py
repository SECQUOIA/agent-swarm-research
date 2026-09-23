"""Independent numerical reconstruction of dense robust comparison evidence.

The production solver is imported only for interface, finite-difference and
stop-behavior tests. Saved values use direct symmetric covariance solves.
"""

from collections import Counter
from fractions import Fraction as Q
from itertools import combinations
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from time import perf_counter
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np
from scipy.linalg import cho_factor, cho_solve
from scipy.optimize import linprog

import robust_dense_comparison as production
from noisy_markov_design import NoisyDesign, TimeBudgetExceeded
from robust_kinetic_design import RobustDesign


HERE = Path(__file__).resolve().parent
EXPECTED = 'b458885e5c848086e181928d3f454469222e1598e5cffc2e677c9ab961201fb3'
COUNTS = Counter()
ERRORS = Counter()


def close(name, actual, expected, tolerance=2e-8):
    error = float(np.max(np.abs(np.asarray(actual)-np.asarray(expected))))
    ERRORS[name] = max(ERRORS[name], error)
    assert error <= tolerance, (name, error, tolerance)
    COUNTS[name] += 1


def logdet(matrix):
    factor = np.linalg.cholesky(matrix)
    return float(2*np.log(np.diag(factor)).sum())


def scenario_dict(scenario):
    return {name: getattr(scenario, name) for name in
            ('F', 'prior', 'rho', 'latent_variance', 'nugget_variance', 'k')}


class Independent:
    def __init__(self, scenarios, offsets):
        self.offsets = np.asarray(offsets)
        self.rows = []
        for row in scenarios:
            F, prior = np.asarray(row['F']), np.asarray(row['prior'])
            times = np.arange(len(F))
            covariance = row['latent_variance']*row['rho']**np.abs(times[:, None]-times)
            covariance += row['nugget_variance']*np.eye(len(F))
            split = .99*float(np.linalg.eigvalsh(covariance)[0])
            self.rows.append((F, prior, covariance, split))
        self.n, self.p = self.rows[0][0].shape

    def selected_values(self, selected):
        selected = list(selected)
        result = []
        for F, prior, covariance, _ in self.rows:
            features = F[selected]
            info = prior.copy()
            if selected:
                info += features.T@cho_solve(cho_factor(covariance[np.ix_(selected, selected)]), features)
            result.append(logdet(info))
        return np.asarray(result)

    def score(self, selected):
        return float(np.min(self.selected_values(selected)-self.offsets))

    def fractional(self, z):
        # Positive z is equivalent to observing with covariance
        # R + diag(a*(1/z-1)); zero entries are unobserved. This is a
        # symmetric formulation distinct from the production I+S*D solve.
        z = np.asarray(z)
        active = np.flatnonzero(z > 0)
        values, gradients = [], []
        for F, prior, R, a in self.rows:
            S = R-a*np.eye(self.n)
            info, V = prior.copy(), F.copy()
            if len(active):
                augmented = R[np.ix_(active, active)]+np.diag(a*(1/z[active]-1))
                weighted = cho_solve(cho_factor(augmented), F[active])
                info += F[active].T@weighted
                V -= S[:, active]@weighted
            values.append(logdet(info))
            gradients.append(np.sum(V*cho_solve(cho_factor(info), V.T).T, axis=1)/a)
        return np.asarray(values)-self.offsets, np.asarray(gradients)


def check_witness(witness, independent, k):
    weights, z = np.asarray(witness['dual_weights']), np.asarray(witness['z'])
    assert np.all(weights >= 0) and abs(weights.sum()-1) < 1e-14
    assert np.all(z >= 0) and np.all(z <= 1)
    values, gradients = independent.fractional(z)
    constants = values-gradients@z
    weighted = weights@gradients
    support = sum(sorted(weighted, reverse=True)[:k])
    bound = weights@constants+support
    for name, actual in [('scenario_values_minus_offsets', values), ('scenario_gradients', gradients),
                         ('scenario_constants', constants), ('weighted_gradient', weighted),
                         ('top_k_linear_price', support), ('upper_bound', bound)]:
        close('witness_'+name, actual, witness[name])
    # Independently solve the primal max-min linearized epigraph. LP weak
    # duality checks the weight certificate without using its LP objective.
    q = len(weights)
    linear = linprog(np.r_[np.zeros(independent.n), -1.],
                     A_ub=np.c_[-gradients, np.ones(q)], b_ub=constants,
                     A_eq=np.array([np.r_[np.ones(independent.n), 0.]]), b_eq=[k],
                     bounds=[(0, 1)]*independent.n+[(None, None)], method='highs')
    assert linear.success and -linear.fun <= bound+2e-8
    COUNTS['witness_primal_LP_checks'] += 1
    return float(bound)


def check_dense(record, independent, k):
    assert len(set(record['selected'])) == k
    close('dense_selected_score', independent.score(record['selected']), record['true_lower_bound'])
    close('dense_initial_score', independent.score(record['disclosed_initial_selected']), record['disclosed_initial_score'])
    assert record['true_lower_bound'] >= record['disclosed_initial_score']-1e-12
    close('dense_rounding_score', independent.score(record['rounded_selected']), record['rounded_true_score'])
    z = np.asarray(record['continuous_z'])
    close('continuous_cardinality', z.sum(), k, 1e-8)
    values, _ = independent.fractional(z)
    close('continuous_value', min(values), record['continuous_value'])
    assert sorted(np.argsort(z)[-k:].tolist()) == record['rounded_selected'] if k else record['rounded_selected'] == []
    upper = check_witness(record['upper_bound_witness'], independent, k)
    close('dense_upper', upper, record['true_upper_bound'])
    close('continuous_gap', upper-min(values), record['continuous_tangent_gap'])
    close('discrete_gap', upper-independent.score(record['selected']), record['true_gap'])
    close('split_parameters', [row[3] for row in independent.rows], record['split_a_by_scenario'])
    assert record['initial_incumbent_affects_continuous_search'] is False
    assert all(a['upper_bound'] >= b['upper_bound'] for a,b in zip(record['history'], record['history'][1:]))


def check_polish(record, independent, k):
    path = tuple(record['selected'])
    score = independent.score(path)
    close('polished_score', score, record['true_lower_bound'])
    close('polished_initial_score', independent.score(record['initial_selected']), record['initial_score'])
    close('polished_improvement', score-record['initial_score'], record['improvement'])
    if 'selected_scenario_logdet' in record:
        close('polished_logdets', independent.selected_values(path), record['selected_scenario_logdet'])
    neighbors = []
    for dropped in path:
        for added in set(range(independent.n))-set(path):
            neighbor = tuple(sorted((set(path)-{dropped})|{added}))
            neighbors.append(independent.score(neighbor))
    assert record['status'] == 'single_exchange_local_optimum'
    assert not neighbors or max(neighbors) <= score+1e-11
    assert len(neighbors) == k*(independent.n-k)
    assert record['objective_evaluations'] == 1+(record['accepted_exchanges']+1)*len(neighbors)
    COUNTS['final_exchange_neighbors'] += len(neighbors)
    return {'score': score, 'neighbors': len(neighbors),
            'best_neighbor_minus_current': max(neighbors)-score if neighbors else None}


def check_case(n):
    path = HERE/'results'/f'robust-dense-n{n}.json'
    payload = json.loads(path.read_text())
    metadata = payload['metadata']
    original_path = HERE.parents[1]/metadata['input_path']
    original = json.loads(original_path.read_text())
    assert hashlib.sha256(original_path.read_bytes()).hexdigest() == metadata['input_sha256']
    assert metadata['source_sha256'] == EXPECTED
    assert hashlib.sha256((HERE/'robust_kinetic_design.py').read_bytes()).hexdigest() == metadata['robust_source_sha256']
    assert hashlib.sha256((HERE/'noisy_markov_design.py').read_bytes()).hexdigest() == original['metadata']['reviewed_core_sha256']
    assert payload['complete'] and payload['offsets'] == original['offsets']
    assert (payload['n'], payload['p'], payload['k']) == (original['n'], original['p'], original['k'])
    independent = Independent(original['scenarios'], original['offsets'])
    k, p = payload['k'], payload['p']
    refs_low = np.array([row['hull']['true_lower_bound'] for row in original['references']])
    refs_high = np.array([row['hull']['true_upper_bound'] for row in original['references']])
    close('offsets_equal_feasible_references', refs_low, independent.offsets, 0)
    for s, ref in enumerate(original['references']):
        close('feasible_reference_score', independent.selected_values(ref['hull']['selected'])[s], refs_low[s])
    check_dense(payload['dense'], independent, k)
    polished = {label: check_polish(payload[label], independent, k)
                for label in ('hull_polish', 'dense_rounding_polish')}
    assert payload['hull_polish']['initial_selected'] == original['robust']['selected']
    assert payload['dense_rounding_polish']['initial_selected'] == payload['dense']['rounded_selected']
    for record in [*payload['evaluations'].values(), payload['best_shared_incumbent']]:
        values = independent.selected_values(record['selected'])
        expected = {'scenario_logdet': values, 'fixed_offset_score': min(values-independent.offsets),
                    'raw_worst_logdet': min(values), 'standardized_score_lower': min(values-refs_high),
                    'standardized_score_upper': min(values-refs_low),
                    'scenario_logdet_loss_to_reference': refs_low-values,
                    'scenario_efficiency_lower': np.exp((values-refs_high)/p),
                    'scenario_efficiency_upper': np.exp((values-refs_low)/p)}
        for label, value in expected.items():
            close('evaluation_'+label, value, record[label])
    timings = payload['timing']
    ref, hull, greedy = original['reference_wall_seconds'], original['robust']['wall_seconds'], original['greedy_exchange']['wall_seconds']
    hp, dense, dp = [payload[key]['wall_seconds'] for key in ('hull_polish', 'dense', 'dense_rounding_polish')]
    expected = {'existing_reference_generation': ref, 'existing_hull_generation': hull,
                'existing_greedy_generation': greedy, 'hull_polishing': hp, 'dense_solver': dense,
                'dense_rounding_polishing': dp, 'hull_with_reference_and_polishing': ref+hull+hp,
                'standalone_dense_with_references_and_own_polishing': ref+dense+dp,
                'supplied_shared_incumbent_generation': ref+hull+greedy+hp,
                'all_generation_and_new_methods': ref+hull+greedy+hp+dense+dp}
    for label, value in expected.items():
        close('timing_'+label, value, timings[label], 1e-12)
    assert timings['new_driver_wall_seconds'] >= hp+dense+dp
    assert all(payload[key]['time_limit'] == 30 and payload[key]['wall_seconds'] < 30
               for key in ('hull_polish', 'dense', 'dense_rounding_polish'))
    assert all(v == '1' for v in metadata['blas_environment'].values())
    cap = float(min(refs_high-independent.offsets))
    comparison = payload['upper_comparison']
    assert comparison['shared_hull_true_upper'] == original['robust']['true_upper_bound']
    assert comparison['dense_true_upper'] == payload['dense']['true_upper_bound']
    close('common_incumbent', comparison['common_fixed_offset_lower'], payload['best_shared_incumbent']['fixed_offset_score'])
    assert comparison['shared_hull_true_upper'] < cap < comparison['dense_true_upper']
    return {'n': n, 'polishing': polished, 'reference_only_discrete_upper': cap,
            'continuous_lower': payload['dense']['continuous_value'],
            'continuous_upper': payload['dense']['true_upper_bound'],
            'artifact_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def tiny_checks():
    rng = np.random.default_rng(28741)
    scenarios = tuple(NoisyDesign(rng.integers(-9, 10, size=(10, 2))/10, .4, 1., 1., .1*np.eye(2), 3) for _ in range(3))
    rows = [scenario_dict(s) for s in scenarios]
    raw = Independent(rows, np.zeros(3))
    paths = list(combinations(range(10), 3))
    values = np.array([raw.selected_values(path) for path in paths])
    offsets = values.max(axis=0)
    independent = Independent(rows, offsets)
    design = RobustDesign(scenarios, offsets)
    oracle = production.RobustDenseOracle(design)
    optimum = float(np.min(values-offsets, axis=1).max())
    saved = json.loads((HERE/'results/robust-dense-validation.json').read_text())
    assert saved['source_sha256'] == EXPECTED and saved['status'] == 'passed'
    close('tiny_exhaustive_optimum', optimum, saved['true_enumerated_optimum'])
    for path in paths:
        z = np.zeros(10)
        z[list(path)] = 1
        close('tiny_binary_identity', oracle.values_gradients(z)[0], independent.selected_values(path)-offsets)
    check_witness(saved['dual_lp_witness'], independent, 3)
    check_dense(saved['dense'], independent, 3)
    check_polish(saved['polished'], independent, 3)
    assert saved['dense']['true_lower_bound'] <= optimum <= saved['dense']['true_upper_bound']
    z = rng.uniform(.2, .8, 10)
    value, gradient = oracle.values_gradients(z)
    close('tiny_independent_fractional_value', value, independent.fractional(z)[0])
    close('tiny_independent_gradient', gradient, independent.fractional(z)[1])
    for _ in range(12):
        direction = rng.normal(size=10)
        direction -= direction.mean()
        direction /= np.linalg.norm(direction)
        h = 1e-5
        derivative = (independent.fractional(z+h*direction)[0]-independent.fractional(z-h*direction)[0])/(2*h)
        close('tiny_directional_gradient', derivative, gradient@direction, 2e-8)
    for weights in ([1e308, 1e308, 1e308], [1, 0, 0], [.1, .2, .7], [-1, 2, 0]):
        upper, witness = production.tangent_bound(value, gradient, z, weights, 3)
        assert upper >= optimum-1e-9
        check_witness(witness, independent, 3)
    for path in paths:
        indicator = np.zeros(10)
        indicator[list(path)] = 1
        assert np.all(independent.selected_values(path)-offsets <= value+gradient@(indicator-z)+1e-9)
        COUNTS['tiny_exhaustive_scenario_tangents'] += 3
    for _ in range(20):
        target = rng.uniform(0, 1, 10)
        assert np.all(independent.fractional(target)[0] <= value+gradient@(target-z)+1e-9)
        COUNTS['tiny_continuous_scenario_tangents'] += 3
    single = NoisyDesign(np.array([[1.], [2.]]), 0., 0., 1., np.array([[1.]]), 1)
    analytic = Independent([scenario_dict(single)]*2, [0, 0])
    check_dense(saved['analytic'], analytic, 1)
    close('analytic_log5', saved['analytic']['true_upper_bound'], np.log(5))
    # Distinct priors, negative rho and cardinality endpoints test contracts
    # that the application instances do not exercise.
    for k in (0, 1, 4):
        scenarios = (NoisyDesign(np.array([[1.,2.],[-1.,3.],[2.,1.],[4.,-1.]]), -.3, .7, .4, np.array([[1.,.2],[.2,2.]]), k),
                     NoisyDesign(np.array([[2.,-1.],[3.,2.],[-1.,4.],[1.,1.]]), -.3, .7, .4, np.array([[2.,-.1],[-.1,.5]]), k))
        other = RobustDesign(scenarios, np.array([.3, -.7]))
        independent_other = Independent([scenario_dict(s) for s in scenarios], other.offsets)
        optimum_other = max(independent_other.score(path) for path in combinations(range(4), k))
        result = production.solve_dense_robust(other, time_limit=5)
        assert result['true_lower_bound'] <= optimum_other+1e-9 <= result['true_upper_bound']+1e-9
        close('endpoint_selected_score', independent_other.score(result['selected']), result['true_lower_bound'])
        COUNTS['distinct_prior_negative_rho_endpoint_cases'] += 1
    return {'exhaustive_optimum': optimum, 'schedules': len(paths)}


def stop_checks():
    single = NoisyDesign(np.array([[1.], [2.], [3.]]), 0., 0., 1., np.array([[1.]]), 1)
    design = RobustDesign((single, single), np.zeros(2))
    independent = Independent([scenario_dict(single)]*2, [0, 0])
    # Force a timeout after seeing a better neighbor, before completing a pass.
    with patch.object(production, 'check_time', side_effect=[None, TimeBudgetExceeded('forced')]):
        result = production.polish_schedule(design, (0,), time_limit=5)
    assert result['status'] == 'time_limit' and result['selected'] == (1,)
    assert result['accepted_exchanges'] == 0 and result['objective_evaluations'] == 2
    close('capped_polish_held_incumbent', result['true_lower_bound'], independent.score((1,)))
    with patch.object(production, 'minimize', side_effect=TimeBudgetExceeded('forced')):
        result = production.solve_dense_robust(design, initial_selected=(2,), time_limit=5)
    assert result['status'] == 'time_limit' and result['selected'] == (2,)
    assert result['upper_bound_witness'] is not None and result['true_lower_bound'] <= result['true_upper_bound']+1e-9
    with patch.object(production, 'check_time', side_effect=TimeBudgetExceeded('forced')):
        result = production.solve_dense_robust(design, initial_selected=(2,), time_limit=5)
    assert result['status'] == 'time_limit' and result['selected'] == (2,) and result['continuous_z'] is None
    assert result['upper_bound_witness'] is None and result['true_upper_bound'] >= result['true_lower_bound']
    z = np.array([.2, .3, .5])
    values, gradients = independent.fractional(z)
    for fake in (SimpleNamespace(x=None, status=1, message='forced LP cap'),
                 SimpleNamespace(x=np.array([-3., 8., 0., 0., 0., 0.]), status=1, message='inexact stopped LP')):
        with patch.object(production, 'linprog', return_value=fake):
            upper, witness = production.optimize_tangent_dual(values, gradients, z, 1, perf_counter()+5)
        assert witness['dual_lp_status'] == 1
        close('capped_LP_recomputed_support', upper, check_witness(witness, independent, 1))
    first = production.solve_dense_robust(design, initial_selected=(0,), time_limit=5)
    second = production.solve_dense_robust(design, initial_selected=(2,), time_limit=5)
    close('initial_incumbent_search_independence', first['continuous_z'], second['continuous_z'], 0)
    assert first['rounded_selected'] == second['rounded_selected']
    for bad in (0, -1, 31, float('nan'), float('inf')):
        try:
            production.deadline_from(bad)
        except ValueError:
            COUNTS['invalid_time_limits_rejected'] += 1
        else:
            raise AssertionError('invalid deadline accepted')
    with patch.object(production, 'DenseLiuOracle', side_effect=AssertionError('allocated before preflight')):
        try:
            production.RobustDenseOracle(design, max_memory_mb=1e-10)
        except MemoryError:
            COUNTS['memory_preflight_before_allocation'] += 1
    COUNTS['forced_stop_contracts'] += 5


def exact_polish_extension():
    # Reuse the accepted independent rational dense-matrix checker, rather
    # than the certificate's information routine, for the changed incumbent.
    from review_robust_certificate_implementation import dense_information, narrow_log

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def canonical(value):
        if isinstance(value, dict):
            return {k: canonical(v) for k, v in value.items() if not k.endswith('_seconds')}
        if isinstance(value, list):
            return [canonical(v) for v in value]
        return value

    source = HERE/'results/robust-kinetic-n96.json'
    comparison = HERE/'results/robust-dense-n96.json'
    artifact = HERE/'results/robust-kinetic-n96-polished-certificate.json'
    baseline = HERE/'results/robust-kinetic-n96-certificate.json'
    wrapper = HERE/'certify_robust_polish.py'
    record = json.loads(source.read_text(), parse_float=str)
    payload = json.loads(comparison.read_text(), parse_float=str)
    saved = json.loads(artifact.read_text(), parse_float=str)
    old = json.loads(baseline.read_text(), parse_float=str)
    accepted = json.loads((HERE/'results/robust-certificate-implementation-independent-review.json').read_text())
    assert accepted['status'] == 'passed'
    assert digest(baseline) == next(row['sha256'] for row in accepted['artifacts'] if row['file'] == baseline.name)
    assert accepted['certifier_sha256'] == digest(HERE/'certify_robust_design.py')
    assert saved['source_sha256'] == digest(wrapper)
    assert saved['input_sha256'] == digest(source) and saved['comparison_sha256'] == digest(comparison)
    for filename, expected in saved['dependency_sha256'].items():
        assert digest(HERE/filename) == expected
    assert payload['hull_polish']['status'] == 'single_exchange_local_optimum'
    assert saved['selected'] == payload['hull_polish']['selected']
    changed = {'selected', 'selected_logdet_intervals', 'fixed_offset', 'standardized',
               'incumbent_source', 'source_sha256', 'dependency_sha256', 'comparison_sha256'}
    assert canonical({k:v for k,v in saved.items() if k not in changed}) == canonical({k:v for k,v in old.items() if k not in changed})
    # The complete price, tangent, scenario and reference witnesses are the
    # already reviewed baseline witnesses, exactly unchanged.
    COUNTS['exact_upper_witness_unchanged_from_reviewed_artifact'] += 1
    for index, scenario in enumerate(record['scenarios']):
        determinant = dense_information(scenario, saved['selected']).det()
        lo, hi = narrow_log(determinant)
        a, b = map(Q, saved['selected_logdet_intervals'][index])
        assert a <= lo <= hi <= b
        COUNTS['exact_polished_dense_determinant_log_enclosures'] += 1
    grid = saved['log_grid']

    def floor_grid(value):
        scaled = value*grid
        return Q(scaled.numerator//scaled.denominator, grid)

    selected_lower = [Q(interval[0]) for interval in saved['selected_logdet_intervals']]
    expected_fixed = floor_grid(min(a-Q(c) for a,c in zip(selected_lower, saved['offsets'])))
    expected_standardized = floor_grid(min(a-Q(u) for a,u in zip(selected_lower, saved['individual_optimum_upper_bounds'])))
    for label, expected in [('fixed_offset', expected_fixed), ('standardized', expected_standardized)]:
        bounds = saved[label]
        lower, upper, gap = [Q(bounds[name]) for name in ('lower_bound', 'upper_bound', 'gap')]
        assert lower == expected and lower <= upper and gap == upper-lower
        assert bounds['upper_bound'] == old[label]['upper_bound']
        for name, value in [('lower_bound', lower), ('upper_bound', upper), ('gap', gap)]:
            close('exact_certificate_display_'+name, float(bounds['display_'+name]), float(value), 0)
    # Exercise the thin wrapper end to end into a temporary file.
    with tempfile.TemporaryDirectory(prefix='robust-polish-review-') as temporary:
        replay = Path(temporary)/'certificate.json'
        subprocess.run([sys.executable, str(wrapper), str(source), str(comparison), str(replay)],
                       check=True, stdout=subprocess.PIPE, text=True, timeout=60)
        assert canonical(json.loads(replay.read_text(), parse_float=str)) == canonical(saved)
    COUNTS['exact_polish_wrapper_replayed'] += 1
    return {'status': 'passed', 'artifact_sha256': digest(artifact), 'wrapper_sha256': digest(wrapper),
            'fixed_offset': saved['fixed_offset'], 'standardized': saved['standardized'],
            'standardized_efficiency_lower_display': float(np.exp(float(expected_standardized)/saved['p']))}


def main():
    started = perf_counter()
    assert hashlib.sha256((HERE/'robust_dense_comparison.py').read_bytes()).hexdigest() == EXPECTED
    report = {'status': 'passed', 'reviewed_source_sha256': EXPECTED,
              'cases': [check_case(n) for n in (48, 96)], 'tiny': tiny_checks()}
    stop_checks()
    report['exact_polish_extension'] = exact_polish_extension()
    report.update(counts=dict(COUNTS), maximum_absolute_errors=dict(ERRORS), wall_seconds=perf_counter()-started,
                  checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    output = HERE/'results/robust-dense-independent-review.json'
    output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
