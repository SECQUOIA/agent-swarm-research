"""Independent full-covariance validation; no ranking-generator imports.

Uses mode/species/time row order, unlike the generator's time-local patterns.
The default verifies all schedules. --winners checks every winner and runner-up.
"""
import argparse
import csv
from fractions import Fraction
import hashlib
import json
from math import comb
from pathlib import Path
from time import perf_counter

import sympy as s

HERE = Path(__file__).resolve().parent
DATA_HASH = '54506ecb5606ea8900a99cb8490508bdd4b9a364aba4f26efe2676f9a7f6f3ca'
NAMES = ['trace_information', 'determinant_information', 'trace_inverse_information']


def validate(args):
    started = perf_counter()
    raw = args.record.read_bytes()
    result = json.loads(raw)
    records = result['all_schedules']
    expected = sum(comb(3, c)*sum(comb(9-k, k)*(3-c)**k for k in range(5))
                   for c in range(4))-1
    assert expected == 2347 and len(records) == expected
    identities = set()
    for record in records:
        schedule = record['selection']
        static, manual = schedule['static_mask'], schedule['manual_indices']
        assert isinstance(static, int) and 0 <= static < 8
        assert static or manual
        assert len(manual) <= 4
        assert all(len(pair) == 2 and 0 <= pair[0] < 8 and 0 <= pair[1] < 3 for pair in manual)
        assert all(not static & (1 << species) for _, species in manual)
        assert all(b[0]-a[0] >= 2 for a, b in zip(manual, manual[1:]))
        cost = 2000*static.bit_count()+400*len(manual)+200*len({species for _, species in manual})
        assert cost == schedule['cost']
        identities.add((static, tuple(map(tuple, manual))))
    assert len(identities) == expected  # feasible, distinct, and exhausts the known count
    for comparison in result['comparisons']:
        name = comparison['criterion']
        minimize = name == 'trace_inverse_information'
        feasible = [i for i, r in enumerate(records) if r['selection']['cost'] <= comparison['budget']]
        assert len(feasible) == comparison['feasible_count']
        winners = []
        for formula in ['marginal', 'gated']:
            values = {i: Fraction(records[i][formula+'_objectives'][name]) for i in feasible}
            best_value = (min if minimize else max)(values.values())
            optimal = [i for i in feasible if values[i] == best_value]
            stated = comparison[formula]
            assert optimal == stated['optimal_indices']
            assert Fraction(stated['objective']) == best_value
            ordered = sorted(values, key=lambda i: (values[i] if minimize else -values[i], i))
            assert ordered[0] == stated['winning_index'] and ordered[1] == stated['runner_up_index']
            direction = -1 if minimize else 1
            assert Fraction(stated['margin_to_runner_up']) == direction*(values[ordered[0]]-values[ordered[1]])
            winners.append(ordered[0])
        a, b = [Fraction(records[i]['marginal_objectives'][name]) for i in winners]
        regret = (-1 if minimize else 1)*(a-b)
        assert Fraction(comparison['true_regret_at_gated_choice']) == regret
        assert Fraction(comparison['relative_true_regret']) == regret/a
    assert len(result['comparisons']) == 33
    assert args.data.is_file() and hashlib.sha256(args.data.read_bytes()).hexdigest() == DATA_HASH
    with args.data.open(newline='') as stream:
        rows = list(csv.reader(stream))[1:]
    F24 = s.Matrix([[s.Rational(x) for x in row[1:]] for row in rows])
    F = F24.col_join(F24)
    B = s.Matrix([[1, s.Rational(1, 10), s.Rational(1, 10)],
                  [s.Rational(1, 10), 4, s.Rational(1, 2)],
                  [s.Rational(1, 10), s.Rational(1, 2), 8]])
    R = s.kronecker_product(s.Matrix([[1, s.Rational(1, 2)], [s.Rational(1, 2), 1]]), B, s.eye(8))
    K = R.inv(method='DM')
    indices = sorted({c[f][key] for c in result['comparisons']
                      for f in ['marginal', 'gated'] for key in ['winning_index', 'runner_up_index']}) if args.winners else range(len(records))
    checked = 0
    for index in indices:
        record = records[index]
        static, manual = record['selection']['static_mask'], record['selection']['manual_indices']
        selected = [8*species+t for species in range(3) if static & (1 << species) for t in range(8)]
        selected += [24+8*species+t for t, species in manual]
        FS = F.extract(selected, range(4))
        matrices = [s.eye(4)/10000+FS.T*R.extract(selected, selected).inv(method='DM')*FS,
                    s.eye(4)/10000+FS.T*K.extract(selected, selected)*FS]
        for formula, J in zip(['marginal', 'gated'], matrices):
            objectives = [s.trace(J), J.det(method='domain-ge'), s.trace(J.inv(method='DM'))]
            for name, objective in zip(NAMES, objectives):
                assert objective == s.Rational(record[formula+'_objectives'][name]), (index, formula, name)
        checked += 1
    report = {'status': 'PASS', 'arithmetic': 'exact SymPy rationals; full selected covariance inverses in independent row order',
              'all_feasible_schedules_validated': len(records), 'criterion_budget_rankings_validated': 33,
              'direct_full_covariance_schedules': checked, 'direct_objective_equalities': 6*checked,
              'record_sha256': hashlib.sha256(raw).hexdigest(), 'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'elapsed_seconds': perf_counter()-started,
              'scope': 'Independent numerical formulation and complete exact rankings; no physical noise or sensitivity validation'}
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record', type=Path, default=HERE/'exact-rankings.json')
    parser.add_argument('--data', type=Path, default=HERE/'kinetics_Q_drop0.csv')
    parser.add_argument('--output', type=Path, default=HERE/'independent-validation.json')
    parser.add_argument('--winners', action='store_true')
    validate(parser.parse_args())
