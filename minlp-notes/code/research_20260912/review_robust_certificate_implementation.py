"""Independent dense and tuple-history checks of robust certificate integration."""

from collections import Counter
from copy import deepcopy
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations
import hashlib
import json
from pathlib import Path
import sys

import sympy as sp

from certify_robust_design import certify
from integer_interval_scores import IntegerIntervalScores
from review_robust_certificate_theorem import log_bounds


HERE = Path(__file__).resolve().parent


def rational_matrix(values):
    return sp.Matrix([[sp.Rational(Q(x).numerator, Q(x).denominator) for x in row] for row in values])


@lru_cache(None)
def dense_precision(selected, rho, latent, nugget):
    return sp.Matrix([[latent*rho**abs(i-j)+int(i == j)*nugget
                       for j in selected] for i in selected]).inv()


def dense_information(scenario, selected):
    selected = tuple(selected)
    prior = rational_matrix(scenario['prior'])
    if not selected:
        return prior
    features = rational_matrix(scenario['F']).extract(selected, range(prior.rows))
    parameters = [sp.Rational(Q(scenario[key]).numerator, Q(scenario[key]).denominator)
                  for key in ('rho', 'latent_variance', 'nugget_variance')]
    return prior + features.T*dense_precision(selected, *parameters)*features


def narrow_log(value):
    """Keep mantissa denominators bounded before the independent log series."""
    value, exponent = Q(value), 0
    while value < 1:
        value *= 2
        exponent -= 1
    while value >= 2:
        value /= 2
        exponent += 1
    grid = 10**20
    scaled = value*grid
    lower = Q(scaled.numerator//scaled.denominator, grid)
    upper = Q(-((-scaled.numerator)//scaled.denominator), grid)
    lo, hi = log_bounds(lower)[0], log_bounds(upper)[1]
    log2 = log_bounds(2)
    return lo+exponent*log2[0 if exponent >= 0 else 1], hi+exponent*log2[1 if exponent >= 0 else 0]


def tuple_price(report):
    """Price with actual recent calendar tuples; use the accepted arc scorer."""
    n, k, L = report['n'], report['k'], report['L']
    scorers, parameters = [], []
    for scenario, center, weight, delta in zip(report['problem_data'], report['tangent_references'],
                                               report['dual_weights'], report['deltas']):
        inv = rational_matrix(center).inv()
        H = [[Q(inv[i, j])*Q(weight)/(1-Q(delta)) for j in range(inv.cols)] for i in range(inv.rows)]
        scorers.append(IntegerIntervalScores(scenario['F'], H,
                       coefficient_grid=report['integer_grid'], score_grid=report['score_grid']))
        parameters.append(tuple(Q(scenario[key]) for key in ('rho', 'latent_variance', 'nugget_variance')))
    @lru_cache(None)
    def patterns(ages):
        return [scorer.prepare_history(ages, *parameter) for scorer, parameter in zip(scorers, parameters)]
    @lru_cache(None)
    def price(t, history):
        ages = tuple(t-j for j in history)
        return sum(scorer.upper(t, pattern) for scorer, pattern in zip(scorers, patterns(ages)))
    states = {(0, ()): (0, ())}
    for t in range(n):
        after = {}
        for (count, history), (value, path) in states.items():
            for choose in (False, True):
                new_count = count+choose
                if not new_count <= k <= new_count+n-t-1:
                    continue
                new_history = tuple(j for j in history+((t,) if choose else ()) if j >= t+1-L)
                candidate = (value+(price(t, history) if choose else 0), path+((t,) if choose else ()))
                key = (new_count, new_history)
                after[key] = max(after.get(key, (-1, ())), candidate)
        states = after
    return max(states.values())


def verify_report(record, report, counts, exhaustive):
    weights = list(map(Q, report['dual_weights']))
    assert min(weights) >= 0 and sum(weights) == 1
    price, priced = tuple_price(report)
    assert price == report['integer_price'] and priced == tuple(report['priced_selection'])
    counts['independent_tuple_history_prices'] += 1
    for index, scenario in enumerate(record['scenarios']):
        determinant = dense_information(scenario, report['selected']).det()
        lo, hi = narrow_log(determinant)
        a, b = map(Q, report['selected_logdet_intervals'][index])
        assert a <= lo <= hi <= b
        individual = report['individual_certificates'][index]
        own_lo = narrow_log(dense_information(scenario, individual['selected']).det())[0]
        assert Q(individual['lower_bound']) <= own_lo
        assert Q(report['individual_optimum_lower_bounds'][index]) <= Q(individual['lower_bound'])
        assert Q(report['individual_optimum_upper_bounds'][index]) >= Q(individual['upper_bound'])
        counts['dense_incumbent_and_reference_log_checks'] += 1
    if exhaustive:
        schedules = list(combinations(range(report['n']), report['k']))
        all_determinants = [[dense_information(scenario, schedule).det() for schedule in schedules]
                            for scenario in record['scenarios']]
        best = list(map(max, all_determinants))
        for index, value in enumerate(best):
            lo, hi = narrow_log(value)
            assert Q(report['individual_optimum_lower_bounds'][index]) <= lo
            assert hi <= Q(report['individual_optimum_upper_bounds'][index])
        for j, path in enumerate(schedules):
            fixed_hi = min(narrow_log(values[j])[1]-Q(offset)
                           for values, offset in zip(all_determinants, report['offsets']))
            standard_hi = min(narrow_log(values[j]/optimum)[1]
                              for values, optimum in zip(all_determinants, best))
            assert fixed_hi <= Q(report['fixed_offset']['upper_bound'])
            assert standard_hi <= Q(report['standardized']['upper_bound'])
            if path == tuple(report['selected']):
                fixed_lo = min(narrow_log(values[j])[0]-Q(offset)
                               for values, offset in zip(all_determinants, report['offsets']))
                standard_lo = min(narrow_log(values[j]/optimum)[0]
                                  for values, optimum in zip(all_determinants, best))
                assert Q(report['fixed_offset']['lower_bound']) <= fixed_lo
                assert Q(report['standardized']['lower_bound']) <= standard_lo
            counts['enumerated_common_schedule_bounds'] += 1


def fixture(k=2, window=1, rho='1/3'):
    scenarios = [{'F': [[1, '1/2'], [2, -1], [-1, 2], [3, 1]],
                  'prior': [[1, '1/4'], ['1/4', 1]], 'k': k,
                  'rho': rho, 'latent_variance': '1/5', 'nugget_variance': 1},
                 {'F': [[-1, 1], [2, '1/3'], [3, -2], [1, 3]],
                  'prior': [[2, '-1/3'], ['-1/3', 1]], 'k': k,
                  'rho': '-1/4', 'latent_variance': '1/3', 'nugget_variance': 1}]
    selected = list(range(k))
    centers = [dense_information(scenario, selected).tolist() for scenario in scenarios]
    centers = [[[str(x) for x in row] for row in center] for center in centers]
    record = {'scenarios': scenarios, 'k': k, 'offsets': ['3/7', '-4/9'],
              'references': [{'hull': {'L': 3, 'selected': selected,
                                      'hull_information': center}} for center in centers]}
    proposal = {'L': window, 'selected': selected, 'hull_information': centers,
                'dual_weights': ['-1/10', '7/3']}
    return record, proposal


def main():
    sys.set_int_max_str_digits(0)
    counts = Counter()
    for k, window, rho in ((2, 1, '1/3'), (2, 3, '1/3'), (0, 3, '1/3'),
                            (4, 3, '1/3'), (1, 0, '0')):
        record, proposal = fixture(k, window, rho)
        # Make L=0 usable in the second scenario as well.
        if window == 0:
            record['scenarios'][1]['rho'] = '0'
        report = certify(record, proposal)
        verify_report(record, report, counts, exhaustive=True)
        assert tuple(report['dual_weights']) == (Q(0), Q(1))
        counts['exact_weight_clipping'] += 1
    record, proposal = fixture()
    for grid in (1, 3, 10**16):
        report = certify(record, proposal, log_grid=grid)
        verify_report(record, report, counts, exhaustive=True)
        counts['log_grid_variants'] += 1
    # Numerical objective labels and offsets are not exact standardizers.
    baseline = certify(record, proposal)
    changed = deepcopy(record)
    changed['offsets'] = ['-999', '888']
    for reference in changed['references']:
        reference['hull']['true_upper_bound'] = '-999999999'
        reference['hull']['true_lower_bound'] = '999999999'
    other = certify(changed, proposal)
    assert other['standardized'] == baseline['standardized']
    counts['untrusted_numerical_reference_labels_ignored'] += 1

    changes = [lambda r, p: p.update(dual_weights=[0, 0]),
               lambda r, p: p.update(dual_weights=[-1, -2]),
               lambda r, p: p.update(selected=[0, 0]),
               lambda r, p: p.update(selected=[False, 1]),
               lambda r, p: p.update(selected=[0, 4]),
               lambda r, p: p.update(L=True),
               lambda r, p: p.update(hull_information=[[[0, 0], [0, 0]]]*2),
               lambda r, p: p.update(hull_information=[[[1]], [[1]]]),
               lambda r, p: r.update(offsets=[0]),
               lambda r, p: r.update(scenarios=[]),
               lambda r, p: r['scenarios'][1].update(k=3),
               lambda r, p: r['scenarios'][1].update(rho=1),
               lambda r, p: r['scenarios'][1].update(nugget_variance=0),
               lambda r, p: r['scenarios'][1].update(prior=[[1, 1], [0, 1]]),
               lambda r, p: r['scenarios'][1].update(F=[[1, 2]])]
    for mutate in changes:
        damaged, candidate = deepcopy(record), deepcopy(proposal)
        mutate(damaged, candidate)
        try:
            certify(damaged, candidate)
        except (ValueError, TypeError, MemoryError):
            counts['malformed_inputs_rejected'] += 1
        else:
            raise AssertionError('Malformed input was accepted')
    for options in ({'score_grid': False}, {'reference_grid': 0}, {'integer_grid': 0},
                    {'log_grid': 0}, {'max_states': 1}):
        try:
            certify(record, proposal, **options)
        except (ValueError, TypeError, MemoryError):
            counts['invalid_or_insufficient_grids_rejected'] += 1
        else:
            raise AssertionError(f'Invalid or insufficient grid accepted: {options}')
    small_variance, candidate = fixture(window=3)
    for scenario in small_variance['scenarios']:
        scenario.update(latent_variance='1/100', nugget_variance='1/100')
    try:
        certify(small_variance, candidate, integer_grid=1)
    except ValueError:
        counts['invalid_or_insufficient_grids_rejected'] += 1
    else:
        raise AssertionError('A zero variance grid floor was accepted')

    artifacts = []
    def canonical(value):
        if isinstance(value, dict):
            return {k: canonical(v) for k, v in value.items() if not k.endswith('_seconds')}
        if isinstance(value, list):
            return [canonical(v) for v in value]
        return value
    for n in (48, 96):
        input_path = HERE/f'results/robust-kinetic-n{n}.json'
        certificate_path = HERE/f'results/robust-kinetic-n{n}-certificate.json'
        record = json.loads(input_path.read_text(), parse_float=str)
        saved = json.loads(certificate_path.read_text(), parse_float=str)
        assert saved['input_sha256'] == hashlib.sha256(input_path.read_bytes()).hexdigest()
        assert saved['source_sha256'] == hashlib.sha256((HERE/'certify_robust_design.py').read_bytes()).hexdigest()
        for filename, digest in saved['dependency_sha256'].items():
            assert digest == hashlib.sha256((HERE/filename).read_bytes()).hexdigest()
        proposal = deepcopy(record['robust'])
        proposal['selected'] = record[saved['incumbent_source']]['selected']
        replay = json.loads(json.dumps(certify(record, proposal), default=str), parse_float=str)
        assert canonical(replay) == canonical({k: saved[k] for k in replay})
        counts['saved_artifacts_exactly_replayed'] += 1
        verify_report(record, saved, counts, exhaustive=False)
        artifacts.append({'file': certificate_path.name,
                          'sha256': hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
                          'standardized_gap': saved['standardized']['gap']})
        print(f'Passed saved n={n} certificate replay and independent dense/tuple checks', flush=True)
    output = {'status': 'passed', 'counts': dict(counts), 'artifacts': artifacts,
              'certifier_sha256': hashlib.sha256((HERE/'certify_robust_design.py').read_bytes()).hexdigest(),
              'reviewer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'results/robust-certificate-implementation-independent-review.json').write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps(output), flush=True)


if __name__ == '__main__':
    main()
