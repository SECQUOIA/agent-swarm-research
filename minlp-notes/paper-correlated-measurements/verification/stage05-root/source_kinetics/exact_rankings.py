"""Exhaustive rational rankings of the pinned public kinetics input.

Standard-library only. This independently constructs schedules and information;
it does not import the original reanalysis or execute third-party software.
The supplied decimal sensitivities are data, not certified physical derivatives.
"""
from __future__ import annotations

import argparse
import csv
from fractions import Fraction as Q
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import platform
from time import perf_counter

SOURCE_COMMIT = '430090e610446aab88328ce495ffb15b684c56c4'
DATA_SHA256 = '54506ecb5606ea8900a99cb8490508bdd4b9a364aba4f26efe2676f9a7f6f3ca'
SOURCE_URL = ('https://raw.githubusercontent.com/dowlinglab/measurement-opt/'
              + SOURCE_COMMIT + '/kinetics_source_data/Q_drop0.csv')
BUDGETS = tuple(range(1000, 5001, 400))
CRITERIA = ('trace_information', 'determinant_information', 'trace_inverse_information')


def det(a):
    b = [row[:] for row in a]
    value = Q(1)
    for j in range(len(b)):
        i = next((i for i in range(j, len(b)) if b[i][j]), None)
        if i is None:
            return Q(0)
        if i != j:
            b[i], b[j] = b[j], b[i]
            value = -value
        pivot = b[j][j]
        value *= pivot
        for i in range(j+1, len(b)):
            ratio = b[i][j]/pivot
            for k in range(j+1, len(b)):
                b[i][k] -= ratio*b[j][k]
    return value


def inv(a):
    n = len(a)
    b = [row[:] + [Q(i == j) for j in range(n)] for i, row in enumerate(a)]
    for j in range(n):
        i = next((i for i in range(j, n) if b[i][j]), None)
        if i is None:
            raise ValueError('singular matrix')
        b[i], b[j] = b[j], b[i]
        pivot = b[j][j]
        b[j] = [x/pivot for x in b[j]]
        for i in range(n):
            if i != j:
                ratio = b[i][j]
                b[i] = [x-ratio*y for x, y in zip(b[i], b[j])]
    return [row[n:] for row in b]


def sub(a, ix):
    return [[a[i][j] for j in ix] for i in ix]


def information(f, precision):
    return [[sum((f[i][a]*precision[i][j]*f[j][b]
                  for i in range(len(f)) for j in range(len(f))), Q(0))
             for b in range(4)] for a in range(4)]


def enumerate_schedules():
    # Primary construction: an independent four-state calendar traversal.
    found = set()
    for states in product(range(4), repeat=8):
        times = [i for i, x in enumerate(states) if x]
        if len(times) > 4 or any(b-a < 2 for a, b in zip(times, times[1:])):
            continue
        manual = tuple((i, states[i]-1) for i in times)
        used = {s for _, s in manual}
        available = [s for s in range(3) if s not in used]
        for switches in product((False, True), repeat=len(available)):
            static = sum(1 << s for s, use in zip(available, switches) if use)
            if static or manual:
                found.add((static, manual))
    # Independent combinations construction, checked as sets, not just counts.
    other = set()
    for static in range(8):
        channels = [s for s in range(3) if not static & (1 << s)]
        for k in range(5):
            for times in combinations(range(8), k):
                if any(b-a < 2 for a, b in zip(times, times[1:])):
                    continue
                for species in product(channels, repeat=k):
                    if static or k:
                        other.add((static, tuple(zip(times, species))))
    assert found == other and len(found) == 2347
    return sorted(found, key=lambda x: (cost(x), x))


def cost(schedule):
    static, manual = schedule
    return 2000*static.bit_count()+200*len({s for _, s in manual})+400*len(manual)


def describe(schedule):
    static, manual = schedule
    return {'scm_species': ['ABC'[s] for s in range(3) if static & (1 << s)],
            'manual_samples': [{'species': 'ABC'[s], 'time_minutes': str(Q(15*(t+1), 2))}
                               for t, s in manual],
            'cost': cost(schedule), 'static_mask': static,
            'manual_indices': [list(x) for x in manual]}


def run(data):
    started = perf_counter()
    assert hashlib.sha256(data.read_bytes()).hexdigest() == DATA_SHA256
    with data.open(newline='') as stream:
        rows = list(csv.reader(stream))
    assert rows[0] == ['Unnamed: 0', 'A1', 'A2', 'E1', 'E2'] and len(rows) == 25
    f = [[Q(x) for x in row[1:]] for row in rows[1:]]
    assert all(len(row) == 4 for row in f)
    base = [[Q(1), Q(1, 10), Q(1, 10)],
            [Q(1, 10), Q(4), Q(1, 2)],
            [Q(1, 10), Q(1, 2), Q(8)]]
    covariance = [[base[i % 3][j % 3]*(Q(1) if i//3 == j//3 else Q(1, 2))
                   for j in range(6)] for i in range(6)]
    assert all(det(sub(covariance, list(range(j)))) > 0 for j in range(1, 7))
    precision = inv(covariance)
    schedules = enumerate_schedules()
    enumeration_seconds = perf_counter()-started
    pattern_cache = {}
    for t in range(8):
        for static in range(8):
            for channel in [-1]+[s for s in range(3) if not static & (1 << s)]:
                mask = static | (0 if channel < 0 else 1 << (channel+3))
                selected = [i for i in range(6) if mask & (1 << i)]
                fs = [f[(i % 3)*8+t] for i in selected]
                marginal = information(fs, inv(sub(covariance, selected)))
                gated = information(fs, sub(precision, selected))
                difference = [[gated[a][b]-marginal[a][b] for b in range(4)] for a in range(4)]
                assert all(det(sub(difference, ix)) >= 0
                           for k in range(1, 5) for ix in combinations(range(4), k))
                pattern_cache[t, mask] = (marginal, gated)
    pattern_seconds = perf_counter()-started-enumeration_seconds
    values = [[], []]
    for static, manual in schedules:
        masks = [static]*8
        for t, s in manual:
            masks[t] |= 1 << (s+3)
        for formula in range(2):
            matrix = [[Q(a == b, 10000)+sum((pattern_cache[t, mask][formula][a][b]
                        for t, mask in enumerate(masks)), Q(0))
                       for b in range(4)] for a in range(4)]
            assert matrix == [list(row) for row in zip(*matrix)]
            determinant = det(matrix)
            assert determinant > 0
            assert all(det(sub(matrix, list(range(j)))) > 0 for j in range(1, 4))
            # trace(M^-1) = sum of principal cofactors / det(M).
            cofactor_sum = sum((det(sub(matrix, [j for j in range(4) if j != i]))
                                for i in range(4)), Q(0))
            criteria = (sum(matrix[i][i] for i in range(4)), determinant,
                        cofactor_sum/determinant)
            values[formula].append(criteria)
    comparisons = []
    for budget in BUDGETS:
        feasible = [i for i, schedule in enumerate(schedules) if cost(schedule) <= budget]
        for criterion, name in enumerate(CRITERIA):
            direction = -1 if criterion == 2 else 1
            ranking = []
            for formula in range(2):
                ordered = sorted(feasible, key=lambda i: (-direction*values[formula][i][criterion], i))
                best, second = ordered[:2]
                ties = [i for i in ordered if values[formula][i][criterion] == values[formula][best][criterion]]
                ranking.append({'winning_index': best, 'optimal_indices': ties,
                                'winning_selection': describe(schedules[best]),
                                'objective': str(values[formula][best][criterion]),
                                'runner_up_index': second,
                                'margin_to_runner_up': str(direction*(values[formula][best][criterion]-values[formula][second][criterion]))})
            true_best, gated_best = (r['winning_index'] for r in ranking)
            regret = direction*(values[0][true_best][criterion]-values[0][gated_best][criterion])
            comparisons.append({'budget': budget, 'criterion': name, 'feasible_count': len(feasible),
                                'marginal': ranking[0], 'gated': ranking[1],
                                'same_exact_optimal_set': ranking[0]['optimal_indices'] == ranking[1]['optimal_indices'],
                                'true_regret_at_gated_choice': str(regret),
                                'relative_true_regret': str(regret/values[0][true_best][criterion])})
    assert len(pattern_cache) == 160
    elapsed = perf_counter()-started
    return {'provenance': {'source_commit': SOURCE_COMMIT, 'source_url': SOURCE_URL,
                           'data_sha256': DATA_SHA256, 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                           'python': platform.python_version(),
                           'interpretation': 'CSV decimals and source covariance constants interpreted exactly; no physical sensitivity-generation claim',
                           'arithmetic': 'Python Fraction; every objective, equality, ordering and regret exact; no tolerance',
                           'regularization': 'J0=I4/10000',
                           'selection_provenance': 'Independent exhaustive reconstruction; no original optimizer or stored pickle selections executed'},
            'validation': {'independent_enumerations_match': True, 'nonempty_schedules': len(schedules),
                           'exact_pattern_gating_PSD_checks': 160, 'exact_SPD_information_checks': 2*len(schedules),
                           'unique_optimum_in_every_formula_criterion_budget': all(len(r[form]['optimal_indices']) == 1 for r in comparisons for form in ['marginal', 'gated'])},
            'comparisons': comparisons,
            'all_schedules': [{'selection': describe(schedule),
                               'marginal_objectives': dict(zip(CRITERIA, map(str, values[0][i]))),
                               'gated_objectives': dict(zip(CRITERIA, map(str, values[1][i])))}
                              for i, schedule in enumerate(schedules)],
            'timing_seconds': {'enumeration_and_input': enumeration_seconds, 'pattern_construction_and_PSD_checks': pattern_seconds,
                               'remaining_objectives_and_rankings': elapsed-enumeration_seconds-pattern_seconds,
                               'total_before_serialization': elapsed,
                               'interpretation': 'One observed standard-library run, includes validation; not a solver benchmark'}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=Path(__file__).with_name('kinetics_Q_drop0.csv'))
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('exact-rankings.json'))
    args = parser.parse_args()
    result = run(args.data)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    print(json.dumps({'validation': result['validation'], 'changed_comparisons': [
        {'budget': r['budget'], 'criterion': r['criterion'], 'relative_regret': r['relative_true_regret']}
        for r in result['comparisons'] if not r['same_exact_optimal_set']],
        'timing_seconds': result['timing_seconds']}, indent=2))
