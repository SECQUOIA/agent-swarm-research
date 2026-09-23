"""Independent dense verification of the two saved robust/nominal comparisons."""

from collections import Counter
from copy import deepcopy
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys

from compare_robust_nominal import compare
from review_robust_certificate_implementation import dense_information, narrow_log


HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    sys.set_int_max_str_digits(0)
    counts = Counter()
    reviewed = json.loads((HERE/'results/robust-certificate-implementation-independent-review.json').read_text())
    verified_certificates = {artifact['file']: artifact['sha256'] for artifact in reviewed['artifacts']}
    assert reviewed['status'] == 'passed'
    outputs = []
    for n in (48, 96):
        input_path = HERE/f'results/robust-kinetic-n{n}.json'
        certificate_path = HERE/f'results/robust-kinetic-n{n}-certificate.json'
        comparison_path = HERE/f'results/robust-kinetic-n{n}-nominal-comparison.json'
        record = json.loads(input_path.read_text(), parse_float=str)
        certificate = json.loads(certificate_path.read_text(), parse_float=str)
        saved = json.loads(comparison_path.read_text(), parse_float=str)
        assert digest(certificate_path) == verified_certificates[certificate_path.name]
        assert saved['certificate_sha256'] == digest(certificate_path)
        assert saved['input_sha256'] == digest(input_path)
        assert saved['source_sha256'] == digest(HERE/'compare_robust_nominal.py')
        replay = json.loads(json.dumps(compare(record, certificate), default=str), parse_float=str)
        assert replay == {key: saved[key] for key in replay}
        counts['comparison_artifacts_exactly_replayed'] += 1
        ell = list(map(Q, certificate['individual_optimum_lower_bounds']))
        upper = list(map(Q, certificate['individual_optimum_upper_bounds']))
        dense_nominal, dense_selected = [], []
        for scenario, interval in zip(record['scenarios'], saved['nominal_logdet_intervals']):
            bounds = narrow_log(dense_information(scenario, saved['nominal_selected']).det())
            assert Q(interval[0]) <= bounds[0] <= bounds[1] <= Q(interval[1])
            dense_nominal.append(bounds)
            dense_selected.append(narrow_log(dense_information(scenario, saved['certified_selected']).det()))
            counts['nominal_and_selected_dense_scenario_checks'] += 1
        for values, interval in ((dense_nominal, saved['nominal_standardized_interval']),
                                 (dense_selected, saved['selected_standardized_interval'])):
            lower = min(bounds[0]-u for bounds, u in zip(values, upper))
            higher = min(bounds[1]-l for bounds, l in zip(values, ell))
            assert Q(interval[0]) <= lower <= higher <= Q(interval[1])
            counts['standardized_interval_direction_checks'] += 1
        exact_log_ratio = (Q(saved['selected_standardized_interval'][0])
                           -Q(saved['nominal_standardized_interval'][1]))/certificate['p']
        assert exact_log_ratio == Q(saved['log_efficiency_ratio_lower_bound']) > 0
        # Independent inner log enclosures also separate in the required direction.
        independent_lower = (min(bounds[0]-u for bounds, u in zip(dense_selected, upper))
                             -min(bounds[1]-l for bounds, l in zip(dense_nominal, ell)))/certificate['p']
        assert independent_lower >= exact_log_ratio
        assert saved['strict_improvement_proved'] is True
        counts['strict_ratio_improvements'] += 1
        for mutation in ('model', 'schedule'):
            changed = deepcopy(record)
            if mutation == 'model':
                changed['scenarios'][0]['nugget_variance'] = '123'
            else:
                changed['evaluations']['nominal_central']['selected'] = [0]*certificate['k']
            try:
                compare(changed, certificate)
            except ValueError:
                counts['mismatched_models_or_infeasible_schedules_rejected'] += 1
            else:
                raise AssertionError(f'Invalid {mutation} accepted')
        outputs.append({'n': n, 'comparison_sha256': digest(comparison_path),
                        'verified_certificate_sha256': digest(certificate_path),
                        'log_efficiency_ratio_lower_bound': str(exact_log_ratio)})
        print(f'Passed exact replay and dense comparison n={n}', flush=True)
    report = {'status': 'passed', 'counts': dict(counts), 'comparisons': outputs,
              'scope': 'Conditional on the exact certificates already independently reviewed; hashes matched',
              'source_sha256': digest(HERE/'compare_robust_nominal.py'),
              'reviewer_sha256': digest(Path(__file__))}
    (HERE/'results/robust-nominal-comparison-independent-review.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
