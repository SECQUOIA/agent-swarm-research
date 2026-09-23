"""Fresh exact review of the fixed two-mode weighted-trace certifier.

Uses the dense mixture covariance for local conditionals and selected Fisher
information, and a tuple-history dynamic program for the recorded integer
price. The previously reviewed integer interval arithmetic is reused as a
component; this review checks its new inputs and certificate integration.
"""

from copy import deepcopy
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import random
from time import perf_counter

import sympy as sp

import certify_partial_trace as author
from integer_interval_scores import IntegerIntervalScores
import integer_interval_scores as integer_component


HERE = Path(__file__).resolve().parent


def rational(x):
    return Q(str(x))


def matrix(values):
    return sp.Matrix([[sp.Rational(str(x)) for x in row] for row in values])


def covariance(i, j, variance):
    lag = abs(i-j)
    return variance*(Q(9, 25)*Q(2, 5)**lag + Q(16, 25)*Q(1, 5)**lag + (i == j))


@lru_cache(None)
def conditional(ages, variance):
    if not ages:
        return (), 2*variance
    R = matrix([[covariance(-i, -j, variance) for j in ages] for i in ages])
    cross = matrix([[covariance(0, -i, variance) for i in ages]])
    b = cross*R.inv()
    d = covariance(0, 0, variance)-rational((b*cross.T)[0])
    return tuple(rational(x) for x in b), d


class Reference:
    def __init__(self, record):
        self.F, self.prior, self.W = (matrix(record[key]) for key in ('F', 'prior', 'W'))
        self.n, self.p, self.k = self.F.rows, self.F.cols, record['k']
        self.variance = rational(record['variance'])

    @lru_cache(None)
    def information(self, selected):
        if not selected:
            return self.prior
        F = self.F.extract(selected, range(self.p))
        R = matrix([[covariance(i, j, self.variance) for j in selected] for i in selected])
        return self.prior + F.T*R.inv()*F

    def score(self, selected):
        return rational(sp.trace(self.W*self.information(tuple(selected))))


def independent_delta(n, L, normalized, root_grid):
    if L >= n-1:
        return Q(0), Q(0)
    # Independent exact integer bisection instead of the author's isqrt code.
    lo, hi = 0, root_grid
    while lo < hi:
        middle = (lo+hi)//2
        if 2*middle*middle >= root_grid*root_grid:
            hi = middle
        else:
            lo = middle+1
    coefficient = Q(lo, root_grid) if normalized else Q(1)
    gamma = Q(2, 5)
    near = sum((gamma**(h+2*d) for h in range(1, L+1)
                for d in range(L+1-h, L+1)), Q(0))
    far = gamma**(L+1)/(1-gamma)
    return (1 if normalized else 2)*(far+coefficient*near), coefficient


def verify(result, ref, enumerate_subsets=False):
    normalized = result['bound_kind'] == 'normalized partial observation'
    delta, coefficient = independent_delta(ref.n, result['L'], normalized, result['square_root_grid'])
    assert delta == rational(result['delta'])
    assert coefficient == rational(result['near_coefficient_upper'])
    H = [[rational(ref.W[i, j])/(1-delta) for j in range(ref.p)] for i in range(ref.p)]
    F = [[rational(x) for x in row] for row in ref.F.tolist()]
    scorer = IntegerIntervalScores(F, H, feature_grid=result['integer_feature_grid'],
                                   coefficient_grid=result['integer_coefficient_grid'],
                                   score_grid=result['score_grid'])
    L, patterns, arcs = result['L'], {}, {}
    states, visited = {(0, ()): (0, ())}, 1
    for t in range(ref.n):
        following = {}
        for (chosen, history), (value, path) in states.items():
            retained = tuple(j for j in history if j >= t+1-L)
            moves = []
            if chosen+ref.n-t-1 >= ref.k:
                moves.append(((chosen, retained), (value, path)))
            if chosen < ref.k:
                key = t, history
                if key not in arcs:
                    ages = tuple(t-j for j in history)
                    if ages not in patterns:
                        b, d = conditional(ages, ref.variance)
                        patterns[ages] = scorer.prepare(ages, b, d)
                    arcs[key] = scorer.upper(t, patterns[ages])
                moves.append(((chosen+1, retained+((t,) if L else ())),
                              (value+arcs[key], path+(t,))))
            for state, candidate in moves:
                following[state] = max(following.get(state, candidate), candidate)
        states = following
        visited += len(states)
    price, path = max(value for (chosen, _), value in states.items() if chosen == ref.k)
    assert price == result['integer_price'] and path == tuple(result['priced_selection'])
    assert len(patterns) == result['conditional_patterns']
    assert len(arcs) == result['priced_arcs'] and visited == result['visited_states']
    chosen = tuple(result['selected'])
    assert len(chosen) == ref.k and len(set(chosen)) == ref.k
    assert all(type(t) is int and 0 <= t < ref.n for t in chosen)
    lower = ref.score(chosen)
    upper = rational(sp.trace(ref.W*ref.prior))+Q(price, result['score_grid'])
    assert lower == rational(result['lower_bound'])
    assert upper == rational(result['upper_bound'])
    assert upper-lower == rational(result['gap'])
    assert (None if lower == 0 else (upper-lower)/lower) == (
        None if result['relative_gap'] is None else rational(result['relative_gap']))
    enumerated = 0
    if enumerate_subsets:
        for subset in combinations(range(ref.n), ref.k):
            assert ref.score(subset) <= upper
            enumerated += 1
    return {'n': ref.n, 'k': ref.k, 'L': L, 'arcs': len(arcs),
            'patterns': len(patterns), 'tuple_states': visited,
            'enumerated_subsets': enumerated, 'integer_price': price,
            'display_relative_gap': None if lower == 0 else float((upper-lower)/lower)}


def tests():
    rng = random.Random(90341)
    counts = {'dense_conditional_identities': 0, 'dense_information_identities': 0,
              'delta_comparisons': 0, 'tiny_certificates': 0,
              'enumerated_subset_bounds': 0, 'malformed_rejections': 0}
    for variance in [Q(1, 800), Q(2, 3), Q(100)]:
        for n in range(1, 7):
            for size in range(n):
                for history in combinations(range(n-1), size):
                    ages = tuple(n-1-j for j in history)
                    assert conditional(ages, variance) == author.local_pattern(ages, variance)
                    counts['dense_conditional_identities'] += 1
    for n in range(1, 7):
        p = 1+n%3
        F = [[str(Q(rng.randrange(-5, 6), rng.randrange(1, 7))) for _ in range(p)] for _ in range(n)]
        A = matrix([[rng.randrange(-2, 3) for _ in range(p)] for _ in range(p)])
        W = A.T*A
        for variant in ('positive', 'singular', 'zero'):
            prior = sp.eye(p)/7 if variant == 'positive' else sp.ones(p)/11
            weight = W if variant != 'zero' else sp.zeros(p)
            record = {'F': F, 'prior': [[str(x) for x in row] for row in prior.tolist()],
                      'W': [[str(x) for x in row] for row in weight.tolist()],
                      'variance': '2/3', 'k': 0}
            ref = Reference(record)
            for size in range(n+1):
                for subset in combinations(range(n), size):
                    author_info = author.exact_information(author.matrix(record['F']),
                                                          author.matrix(record['prior']), subset, Q(2, 3))
                    assert author_info == ref.information(subset)
                    counts['dense_information_identities'] += 1
            for k in sorted({0, n//2, n}):
                record['k'], ref.k = k, k
                for L in sorted({0, max(0, n-2), n-1, n+3}):
                    for normalized in (False, True):
                        delta, _ = independent_delta(n, min(L, n-1), normalized, 10**12)
                        if delta >= 1:
                            continue
                        result = author.certify(record, {'L': L, 'selected': list(reversed(range(k)))},
                                                normalized=normalized, score_grid=31, integer_grid=101)
                        checked = verify(result, ref, enumerate_subsets=True)
                        counts['tiny_certificates'] += 1
                        counts['enumerated_subset_bounds'] += checked['enumerated_subsets']
    for n in [1, 2, 5, 20]:
        for L in [0, 1, 2, 8, 30]:
            for grid in [1, 2, 3, 17, 10**12]:
                for normalized in (False, True):
                    assert author.delta_bound(n, L, normalized=normalized, square_root_grid=grid) == independent_delta(n, L, normalized, grid)
                    counts['delta_comparisons'] += 1
    base = {'F': [['1', '-1'], ['2', '3']], 'prior': [['1', '0'], ['0', '0']],
            'W': [['1', '-1'], ['-1', '1']], 'variance': '1', 'k': 1}
    proposal = {'L': 1, 'selected': [0]}
    changes = [('data', 'F', []), ('data', 'F', [['1'], ['1', '2']]),
               ('data', 'F', [[0.2], [1]]), ('data', 'prior', [['1']]),
               ('data', 'prior', [['1', '1'], ['0', '1']]),
               ('data', 'prior', [['1', '0'], ['0', '-1']]),
               ('data', 'W', [['1', '2'], ['2', '1']]),
               ('data', 'W', [['1', '0'], ['1', '1']]),
               ('data', 'variance', '0'), ('data', 'variance', '-1'),
               ('data', 'variance', '1/100000000000000000000'),
               ('data', 'variance', True), ('data', 'variance', 1.0),
               ('data', 'k', -1), ('data', 'k', 3), ('data', 'k', True),
               ('proposal', 'L', -1), ('proposal', 'L', True),
               ('proposal', 'selected', [2]), ('proposal', 'selected', [True]),
               ('proposal', 'selected', []), ('proposal', 'selected', [0, 0])]
    for owner, key, value in changes:
        data, prop = deepcopy(base), deepcopy(proposal)
        (data if owner == 'data' else prop)[key] = value
        try:
            author.certify(data, prop)
        except (ValueError, TypeError, MemoryError):
            counts['malformed_rejections'] += 1
        else:
            raise AssertionError(('malformed input accepted', owner, key, value))
    for options in [{'normalized': 1}, {'score_grid': 0}, {'integer_grid': True},
                    {'max_states': 0}, {'max_states': 1}]:
        try:
            author.certify(base, proposal, **options)
        except (ValueError, TypeError, MemoryError):
            counts['malformed_rejections'] += 1
        else:
            raise AssertionError(('malformed option accepted', options))
    return counts


def main():
    started = perf_counter()
    counts = tests()
    print(json.dumps({'stage': 'tiny_checks_passed', 'counts': counts}), flush=True)
    saved_reviews = []
    for path in sorted((HERE/'results').glob('partial-observation-trace-certificate-*.json')):
        saved = json.loads(path.read_text())
        assert saved['source_sha256'] == sha256(Path(author.__file__).read_bytes()).hexdigest()
        assert saved['integer_scorer_sha256'] == sha256(Path(integer_component.__file__).read_bytes()).hexdigest()
        input_path = Path(saved['input_file'])
        if not input_path.is_absolute():
            input_path = HERE.parent.parent/input_path
        assert saved['input_sha256'] == sha256(input_path.read_bytes()).hexdigest()
        record = json.loads(input_path.read_text(), parse_float=str)['results'][saved['input_case_index']]
        for key in ('F', 'prior', 'W'):
            assert matrix(record[key]) == matrix(saved['problem_data'][key])
        for key in ('k', 'variance'):
            assert rational(record[key]) == rational(saved['problem_data'][key])
        assert tuple(map(rational, saved['problem_data']['latent_transition'])) == (Q(2, 5), Q(1, 5))
        assert tuple(map(rational, saved['problem_data']['observation_row'])) == (Q(3, 5), Q(4, 5))
        review = verify(saved, Reference(saved['problem_data']))
        review.update({'file': path.name, 'sha256': sha256(path.read_bytes()).hexdigest()})
        saved_reviews.append(review)
        print(json.dumps({'stage': 'saved_certificate_passed', **review}), flush=True)
    assert saved_reviews
    report = {'status': 'passed', 'counts': counts, 'saved_certificates': saved_reviews,
              'author_sha256': sha256(Path(author.__file__).read_bytes()).hexdigest(),
              'integer_scorer_sha256': sha256(Path(integer_component.__file__).read_bytes()).hexdigest(),
              'reviewer_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'wall_seconds': perf_counter()-started}
    (HERE/'results/partial-trace-certificate-independent-review.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'status': 'passed', 'saved_certificates': len(saved_reviews),
                      'wall_seconds': report['wall_seconds']}), flush=True)


if __name__ == '__main__':
    main()
