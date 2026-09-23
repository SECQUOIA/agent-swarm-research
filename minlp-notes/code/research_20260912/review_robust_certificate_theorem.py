"""Independent exact fixtures for the robust-design certificate derivation.

No certificate-generator or optimization code is imported. Small schedules are
enumerated, and all information is formed from dense rational covariances.
"""

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


@lru_cache(None)
def log_bounds(value):
    """Independent dyadic reduction and positive atanh-series enclosure."""
    x = Fraction(value)
    assert x > 0
    exponent = 0
    while x < 1:
        x *= 2
        exponent -= 1
    while x >= 2:
        x /= 2
        exponent += 1

    def local(z):
        y = (z - 1) / (z + 1)
        terms = 40
        lower = sum((2*y**(2*i+1)/(2*i+1) for i in range(terms)), Fraction())
        tail = 2*y**(2*terms+1)/((2*terms+1)*(1-y*y))
        return lower, lower + tail

    lo, hi = local(x)
    a, b = local(Fraction(2))
    if exponent >= 0:
        return lo + exponent*a, hi + exponent*b
    return lo + exponent*b, hi + exponent*a


def psd(matrix):
    assert matrix == matrix.T
    return all(matrix.extract(index, index).det() >= 0
               for size in range(1, matrix.rows + 1)
               for index in combinations(range(matrix.rows), size))


def dense_fixture(counts):
    n, k, p, window = 6, 3, 2, 1
    schedules = list(combinations(range(n), k))
    true, local, priors, deltas, increments = [], [], [], [], []
    for scenario, rho in enumerate((sp.Rational(1, 3), -sp.Rational(1, 4), sp.Rational(1, 5))):
        covariance = sp.Matrix(n, n, lambda i, j: rho**abs(i-j) + int(i == j))
        sensitivities = sp.Matrix(n, p, lambda i, j:
            sp.Rational((i+1)*(scenario+1)+1, 5) if j == 0
            else sp.Rational((-1)**i*(i+scenario+2), 7))
        prior = sp.eye(p)/4 + sp.Matrix([1, scenario+1])*sp.Matrix([[1, scenario+1]])/10
        magnitude = abs(rho)
        delta = 2*magnitude**(window+1)*(1-magnitude**(window+1))/(1-magnitude)**2
        assert 0 <= delta < 1
        q = {}
        exact_by_path, local_by_path = {}, {}
        for schedule in schedules:
            selected = sensitivities.extract(schedule, range(p))
            exact = prior + selected.T*covariance.extract(schedule, schedule).inv()*selected
            approximation = prior.copy()
            for t in schedule:
                history = tuple(i for i in schedule if t-window <= i < t)
                key = (t, history)
                if key not in q:
                    if history:
                        row = covariance.extract([t], history)
                        regression = row*covariance.extract(history, history).inv()
                        conditional = covariance[t, t] - (regression*row.T)[0]
                        residual = sensitivities[t, :] - regression*sensitivities.extract(history, range(p))
                    else:
                        conditional, residual = covariance[t, t], sensitivities[t, :]
                    q[key] = residual.T*residual/conditional
                    assert psd(q[key])
                approximation += q[key]
            assert psd(approximation-prior-(1-delta)*(exact-prior))
            assert psd((1+delta)*(exact-prior)-(approximation-prior))
            assert psd(prior+(approximation-prior)/(1-delta)-exact)
            counts['scenario_schedule_memory_checks'] += 1
            exact_by_path[schedule] = exact
            local_by_path[schedule] = approximation
        true.append(exact_by_path)
        local.append(local_by_path)
        priors.append(prior)
        deltas.append(delta)
        increments.append(q)

    determinants = [{path: values[path].det() for path in schedules} for values in true]
    best = [max(values.values()) for values in determinants]
    best_bounds = [log_bounds(value) for value in best]
    ell = [lo-Fraction(1, 100) for lo, _ in best_bounds]
    upper = [hi+Fraction(1, 100) for _, hi in best_bounds]
    score_bounds = {path: (
        min(log_bounds(determinants[s][path]/best[s])[0] for s in range(3)),
        min(log_bounds(determinants[s][path]/best[s])[1] for s in range(3)))
        for path in schedules}
    # Deliberately arbitrary references, different paths and scales by scenario.
    references = [sp.Rational(s+3, 4)*(priors[s]+(local[s][schedules[3*s]]-priors[s])/(1-deltas[s]))
                  for s in range(3)]
    inverses = [matrix.inv() for matrix in references]
    arc_prices = [{edge: sp.trace(inverses[s]*q)/(1-deltas[s])
                   for edge, q in increments[s].items()} for s in range(3)]
    assert all(value >= 0 for prices in arc_prices for value in prices.values())
    paths = {path: [(t, tuple(i for i in path if t-window <= i < t)) for t in path]
             for path in schedules}
    for first in range(5):
        for second in range(5-first):
            weights = [Fraction(first, 4), Fraction(second, 4), Fraction(4-first-second, 4)]
            intercept = sum((weights[s]*(log_bounds(references[s].det())[1]-p
                + Fraction(sp.trace(inverses[s]*priors[s]))-ell[s]) for s in range(3)), Fraction())
            combined = {path: sum((weights[s]*sum((Fraction(arc_prices[s][edge])
                for edge in paths[path]), Fraction()) for s in range(3)), Fraction()) for path in schedules}
            shared_maximum = max(combined.values())
            separate_maxima = sum(weights[s]*max(sum((Fraction(arc_prices[s][edge])
                for edge in paths[path]), Fraction()) for path in schedules) for s in range(3))
            assert shared_maximum <= separate_maxima
            U = min(Fraction(), intercept+shared_maximum)
            for path in schedules:
                assert score_bounds[path][1] <= intercept+combined[path]
                assert score_bounds[path][1] <= U
                L = min(log_bounds(determinants[s][path])[0]-upper[s] for s in range(3))
                assert L <= score_bounds[path][0]
                assert L <= U
                counts['shared_support_and_standardization_checks'] += 1
            counts['simplex_weights_including_boundary'] += 1
    return {'scenarios': 3, 'dimension': p, 'candidates': n, 'cardinality': k,
            'schedules': len(schedules), 'history': window,
            'scenario_memory_bounds': [str(value) for value in deltas]}


def exact_limitations(counts):
    # Two feasible scalar paths, with different scenarios preferring each one.
    paths = [(Fraction(4), Fraction(1)), (Fraction(1), Fraction(4))]
    reference, prior = Fraction(5, 2), Fraction(1)
    combined = max(sum((value-prior)/reference/2 for value in path) for path in paths)
    separate = sum(max((path[s]-prior)/reference/2 for path in paths) for s in range(2))
    assert combined == Fraction(3, 5) and separate-combined == Fraction(3, 5)
    exact_efficiency = min(paths[0])/4
    hull_efficiency = reference/4
    assert exact_efficiency == Fraction(1, 4) < hull_efficiency == Fraction(5, 8)
    # With ell=log 1 and u=log 8, reversed bounds fail in both directions.
    assert log_bounds(1)[0] == 0 > log_bounds(Fraction(1, 4))[1]
    assert log_bounds(Fraction(4, 8))[1] < 0
    counts['explicit_limitations'] += 3

    # A two-sided simultaneous cover whose in-set standardizers lose two factors.
    t = Fraction(3, 4)
    target = (Fraction(1, 2), Fraction(1, 2))
    scenario_one = (Fraction(1), Fraction(1, 10))
    cover = [(Fraction(3, 4), Fraction(1, 10)), (Fraction(1, 10), Fraction(1)),
             (Fraction(3, 8), Fraction(3, 8)), (Fraction(9, 32), Fraction(3, 8))]
    family = cover + [target, scenario_one]
    for path in family:
        assert any(all(t*x <= y <= (2-t)*x for x, y in zip(path, representative))
                   for representative in cover)
    true_best = [max(path[s] for path in family) for s in range(2)]
    cover_best = [max(path[s] for path in cover) for s in range(2)]
    criterion = lambda path, norm: min(x/y for x, y in zip(path, norm))
    true_optimum = max(criterion(path, true_best) for path in family)
    returned = cover[-1]
    assert criterion(returned, cover_best) == max(criterion(path, cover_best) for path in cover)
    assert criterion(returned, true_best)/true_optimum == t*t
    counts['same_set_normalizer_two_factor_example'] += 1
    return {'common_path_improvement_in_log_bound': str(separate-combined),
            'integer_standardized_efficiency': str(exact_efficiency),
            'hull_standardized_efficiency': str(hull_efficiency),
            'same_set_spectral_factor': str(t), 'same_set_efficiency_ratio': str(t*t)}


def main():
    counts = Counter()
    dense = dense_fixture(counts)
    limitations = exact_limitations(counts)
    for epsilon in (Fraction(1, 1000), Fraction(1, 7), Fraction(9, 10)):
        eta, delta = epsilon/4, epsilon/8
        factor = (1-eta)*(1-delta)/(1+delta)
        assert factor*factor >= 1-epsilon
        counts['finite_memory_standardized_loss_constants'] += 1
    note = HERE.parents[1]/'notes/research-20260912-robust-design-certificates.md'
    report = {'status': 'passed', 'scope': 'Independent theorem fixtures; no production certifier imported',
              'counts': dict(counts), 'dense_fixture': dense, 'limitations': limitations,
              'candidate_note_sha256': hashlib.sha256(note.read_bytes()).hexdigest(),
              'reviewer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    destination = HERE/'results/robust-certificate-theorem-independent-review.json'
    destination.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
