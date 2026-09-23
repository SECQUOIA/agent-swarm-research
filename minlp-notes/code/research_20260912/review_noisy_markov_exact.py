"""Independent audit of rational noisy-Markov objective certificates.

Local conditionals and true information use dense rational covariance inverses.
The full-grid floor uses exact LDL factorization, and independent log bounds use
the positive -log(1-u) series rather than the author's atanh series. The integer
pricing check is a recursive suffix search with tuples of recent visit times.
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

import mpmath as mp
import sympy as sp

import certify_noisy_markov as author


HERE = Path(__file__).resolve().parent


def q(x):
    return Q(str(x))


def sm(values):
    return sp.Matrix([[sp.Rational(str(x)) for x in row] for row in values])


def rows(M):
    return tuple(tuple(q(M[i, j]) for j in range(M.cols)) for i in range(M.rows))


def independent_log(x, terms=128):
    """Rational enclosure using log(z)=sum (1-1/z)^j/j for 1<=z<2."""
    x = q(x)
    assert x > 0
    exponent = 0
    while x >= 2:
        x /= 2
        exponent += 1
    while x < 1:
        x *= 2
        exponent -= 1

    def evaluate(z):
        u = 1 - 1 / z
        power, total = Q(1), Q(0)
        for j in range(1, terms + 1):
            power *= u
            total += power / j
        return total, total + power * u / ((terms + 1) * (1 - u))

    lower, upper = evaluate(x)
    lo2, hi2 = evaluate(Q(2))
    return ((lower + exponent * lo2, upper + exponent * hi2) if exponent >= 0
            else (lower + exponent * hi2, upper + exponent * lo2))


class Reference:
    def __init__(self, record):
        self.F, self.prior = sm(record['F']), sm(record['prior'])
        self.n, self.p = self.F.rows, self.F.cols
        self.k = record['k']
        self.rho, self.latent, self.nugget = (
            sp.Rational(str(record[key]))
            for key in ('rho', 'latent_variance', 'nugget_variance'))
        self.R = sp.Matrix(self.n, self.n, lambda i, j:
                           self.latent * self.rho ** abs(i-j)
                           + (self.nugget if i == j else 0))

    @lru_cache(None)
    def conditional(self, ages):
        if not ages:
            return (), self.latent + self.nugget
        C = sp.Matrix(len(ages), len(ages), lambda i, j:
                      self.latent * self.rho ** abs(ages[i]-ages[j])
                      + (self.nugget if i == j else 0))
        cross = sp.Matrix([[self.latent * self.rho ** age for age in ages]])
        b = cross * C.inv()
        variance = self.latent + self.nugget - (b * cross.T)[0]
        return tuple(b), variance

    @lru_cache(None)
    def increment(self, t, history):
        ages = tuple(t-j for j in history)
        b, variance = self.conditional(ages)
        adjusted = self.F[t, :]
        for j, coefficient in zip(history, b):
            adjusted -= coefficient * self.F[j, :]
        return adjusted.T * adjusted / variance

    @lru_cache(None)
    def true(self, selected):
        if not selected:
            return self.prior
        F = self.F.extract(selected, range(self.p))
        R = self.R.extract(selected, selected)
        return self.prior + F.T * R.inv() * F

    def floor(self):
        # Gaussian elimination of the dense covariance, independent of Kalman.
        _, D = self.R.LDLdecomposition(hermitian=False)
        return min(D[i, i] for i in range(self.n))

    def delta(self, L):
        if self.rho == 0 or self.latent == 0 or L >= self.n-1:
            return sp.Rational(0)
        a = abs(self.rho)
        # Sum both residual-pair distance regimes explicitly. This is the same
        # proved bound but not the closed-form expression used by the author.
        gain = self.latent / (self.latent + self.nugget)
        near = sum(gain * sum(a ** (h+2*d) for d in range(L+1-h, L+1))
                   for h in range(1, L+1))
        far = a ** (L+1) / (1-a) * (1+gain * sum(a ** (2*d) for d in range(1, L+1)))
        return 2 * self.latent / self.floor() * (near+far)

    def price(self, L, H, grid):
        @lru_cache(None)
        def arc(t, history):
            return int(sp.ceiling(grid * sp.trace(H * self.increment(t, history))))

        @lru_cache(None)
        def suffix(t, remaining, history):
            if remaining == 0:
                return 0, ()
            if self.n-t < remaining:
                return None
            next_history = tuple(j for j in history if j >= t+1-L)
            candidates = []
            skip = suffix(t+1, remaining, next_history)
            if skip is not None:
                candidates.append(skip)
            take_history = next_history + ((t,) if L else ())
            rest = suffix(t+1, remaining-1, take_history)
            if rest is not None:
                candidates.append((arc(t, history)+rest[0], (t,)+rest[1]))
            return max(candidates) if candidates else None

        result = suffix(0, self.k, ())
        return result, suffix.cache_info().currsize, arc.cache_info().currsize


def verify_certificate(result, ref, exhaustive=False):
    L, grid = result['L'], result['score_grid']
    delta = ref.delta(L)
    assert q(delta) == q(result['delta'])
    assert q(ref.floor()) == q(result['full_grid_innovation_variance_floor'])
    N = sm(result['tangent_reference'])
    assert N == N.T and N.is_positive_definite
    H = N.inv() / (1-delta)
    (price, path), states, arcs = ref.price(L, H, grid)
    assert price == result['integer_price']
    assert tuple(result['priced_selection']) == path
    lower, upper = q(result['lower_bound']), q(result['upper_bound'])
    assert upper-lower == q(result['gap'])
    chosen = tuple(result['selected'])
    assert len(chosen) == ref.k and len(set(chosen)) == ref.k
    assert all(type(t) is int and 0 <= t < ref.n for t in chosen)
    selected_log = independent_log(ref.true(chosen).det())
    assert lower <= selected_log[0]
    lnN = independent_log(N.det())
    linear = -ref.p + q(sp.trace(N.inv() * ref.prior)) + Q(price, grid)
    assert upper >= lnN[1] + linear
    checked = 0
    if exhaustive:
        for selected in combinations(range(ref.n), ref.k):
            J = ref.true(selected)
            interval = independent_log(J.det())
            assert interval[1] <= upper
            approximate = ref.prior.copy()
            integer_price = 0
            for i, t in enumerate(selected):
                history = tuple(j for j in selected[:i] if t-j <= L)
                increment = ref.increment(t, history)
                approximate += increment
                integer_price += int(sp.ceiling(grid * sp.trace(H * increment)))
            assert integer_price <= price
            # The exact PSD sandwich transfer, tested independently on each
            # sensitivity/prior image. Matrix.is_positive_semidefinite is exact.
            envelope = ref.prior + (approximate-ref.prior)/(1-delta)
            assert (envelope-J).is_positive_semidefinite
            checked += 1
    mp.mp.dps = 90
    true_display = mp.log(mp.mpf(str(ref.true(chosen).det().p)) /
                          mp.mpf(str(ref.true(chosen).det().q)))
    return {'subsets': checked, 'suffix_states': states, 'arcs': arcs,
            'selected_true_objective_90_digits': str(true_display),
            'display_gap': float(upper-lower)}


def main():
    started = perf_counter()
    saved_path = HERE / 'results/noisy-markov-exact-certificate-n48.json'
    saved = json.loads(saved_path.read_text())
    source_path = Path(author.__file__)
    assert saved['source_sha256'] == sha256(source_path.read_bytes()).hexdigest()
    original = Path(saved['input_file'])
    original = original if original.is_absolute() else HERE.parent.parent / original
    benchmark = json.loads(original.read_text(), parse_float=str)
    record = benchmark['results'][saved['input_case_index']]
    for name, value in saved['problem_data'].items():
        if name in ('F', 'prior'):
            assert sm(value) == sm(record[name])
        else:
            assert q(value) == q(record[name])
    assert saved['input_sha256'] == sha256(original.read_bytes()).hexdigest()
    saved_review = verify_certificate(saved, Reference(saved['problem_data']))

    generator = random.Random(73209)
    counts = {'certificates': 0, 'subsets': 0, 'local_conditionals': 0,
              'true_information': 0, 'log_enclosures': 0, 'malformed_rejected': 0}
    for n in range(1, 7):
        for rho, latent, nugget in [('0', '1', '1'), ('1/4', '0', '3/4'),
                                     ('1/4', '2/3', '4/3'), ('-1/3', '1', '2')]:
            p = 1 + n % 3
            record = {'F': [[str(Q(generator.randrange(-9, 10), 5)) for _ in range(p)]
                            for _ in range(n)],
                      'prior': [[str(Q(1, 7) if i == j else 0) for j in range(p)]
                                for i in range(p)],
                      'rho': rho, 'latent_variance': latent, 'nugget_variance': nugget, 'k': 0}
            ref = Reference(record)
            for size in range(n+1):
                for selected in combinations(range(n), size):
                    actual = author.true_information(author.matrix(record['F']), author.matrix(record['prior']),
                                                     selected, q(rho), q(latent), q(nugget))
                    assert actual == rows(ref.true(selected))
                    counts['true_information'] += 1
                    if selected:
                        history, target = selected[:-1], selected[-1]
                        ages = tuple(target-j for j in history)
                        b, d = ref.conditional(ages)
                        assert author.local_coefficients(history, target, q(rho), q(latent), q(nugget)) == (
                            tuple(q(x) for x in b), q(d))
                        counts['local_conditionals'] += 1
            for k in sorted({0, n//2, n}):
                record['k'] = k
                ref.k = k
                for L in sorted({0, max(0, n-2), n-1, n+2}):
                    if ref.delta(min(L, n-1)) >= 1:
                        continue
                    hull = {'L': L, 'selected': list(reversed(range(k))),
                            'hull_information': record['prior']}
                    result = author.certify(record, hull, score_grid=37, reference_grid=1000)
                    reviewed = verify_certificate(result, ref, exhaustive=True)
                    counts['certificates'] += 1
                    counts['subsets'] += reviewed['subsets']

    values = [Q(1), Q(2), Q(1, 2), Q(2)**300, Q(2)**-300,
              Q(10**80+1, 10**80), Q(2*10**80-1, 10**80)]
    values += [Q(generator.randrange(1, 10**20), generator.randrange(1, 10**20))
               * Q(2)**generator.randrange(-100, 101) for _ in range(40)]
    for value in values:
        reference = independent_log(value, 256)
        for terms, grid in [(1, 1), (2, 3), (32, 10**14)]:
            interval = author.log_enclosure(value, terms=terms, grid=grid)
            assert interval[0] <= reference[0] <= reference[1] <= interval[1]
            counts['log_enclosures'] += 1

    base = {'F': [['1', '2'], ['3', '4']], 'prior': [['1', '0'], ['0', '1']],
            'rho': '1/4', 'latent_variance': '1', 'nugget_variance': '1', 'k': 1}
    base_hull = {'L': 1, 'selected': [0], 'hull_information': base['prior']}
    mutations = [('record', 'k', value) for value in [-1, 3, True, '1', 1.0]]
    mutations += [('record', 'rho', value) for value in ['1', '-1', 'NaN', 0.2, True]]
    mutations += [('record', 'latent_variance', '-1'), ('record', 'nugget_variance', '0'),
                  ('record', 'F', []), ('record', 'F', [['1'], ['2']]),
                  ('record', 'prior', [['1', '1'], ['0', '1']]),
                  ('record', 'prior', [['1', '0'], ['0', '0']]),
                  ('hull', 'L', -1), ('hull', 'L', True),
                  ('hull', 'selected', [True]), ('hull', 'selected', [2]),
                  ('hull', 'selected', [0, 0]), ('hull', 'selected', []),
                  ('hull', 'hull_information', [['1']]),
                  ('hull', 'hull_information', [['1', '0', '0']]*3),
                  ('hull', 'hull_information', [['-1', '0'], ['0', '-1']])]
    for owner, key, value in mutations:
        record, hull = deepcopy(base), deepcopy(base_hull)
        (record if owner == 'record' else hull)[key] = value
        try:
            author.certify(record, hull)
        except (TypeError, ValueError, MemoryError):
            counts['malformed_rejected'] += 1
        else:
            raise AssertionError(('malformed input accepted', owner, key, value))
    for kwargs in [{'score_grid': 0}, {'reference_grid': True}, {'max_states': 0}, {'max_states': 1}]:
        try:
            author.certify(base, base_hull, **kwargs)
        except (TypeError, ValueError, MemoryError):
            counts['malformed_rejected'] += 1
        else:
            raise AssertionError(('malformed option accepted', kwargs))
    output = {'status': 'passed', 'counts': counts, 'saved_n48_certificate': saved_review,
              'author_source_sha256': sha256(source_path.read_bytes()).hexdigest(),
              'certificate_sha256': sha256(saved_path.read_bytes()).hexdigest(),
              'verifier_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'wall_seconds': perf_counter()-started}
    destination = HERE / 'results/noisy-markov-exact-independent-review.json'
    destination.write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
