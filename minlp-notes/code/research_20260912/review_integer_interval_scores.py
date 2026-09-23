"""Independent exact review of integer interval arc upper scores.

The saved-case conditionals use dense covariance inverses. Reachability and
pricing use tuples of calendar indices rather than bit masks. Generic score
checks use symbolic dense matrix multiplication and exact rational inputs.
"""

from dataclasses import replace
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import random
from time import perf_counter

import sympy as sp

from integer_interval_scores import IntegerIntervalScores, IntegerPattern
import integer_interval_scores as component


HERE = Path(__file__).resolve().parent


def fraction(value):
    return Q(str(value))


def symbolic(rows):
    return sp.Matrix([[sp.Rational(str(x)) for x in row] for row in rows])


def ceiling(value):
    return int(sp.ceiling(sp.Rational(value.numerator, value.denominator)))


def tests():
    rng = random.Random(80513)
    counts = {'interval_products': 0, 'interval_squares': 0,
              'dense_exact_arcs': 0, 'negative_exact_arcs': 0,
              'stationary_conditionals': 0, 'malformed_rejections': 0}
    intervals = [(a, b) for a in range(-4, 5) for b in range(a, 5)]
    for left, right in product(intervals, repeat=2):
        values = [x*y for x in range(left[0], left[1]+1)
                  for y in range(right[0], right[1]+1)]
        assert component._product(left, right) == (min(values), max(values))
        counts['interval_products'] += 1
    for interval in intervals:
        values = [x*x for x in range(interval[0], interval[1]+1)]
        assert component._square(interval) == (min(values), max(values))
        counts['interval_squares'] += 1
    for _ in range(650):
        n, p = rng.randrange(1, 7), rng.randrange(1, 5)
        F = [[Q(rng.randrange(-12, 13), rng.randrange(1, 20)) for _ in range(p)]
             for _ in range(n)]
        A = symbolic([[Q(rng.randrange(-12, 13), rng.randrange(1, 20)) for _ in range(p)]
                      for _ in range(p)])
        H = A + A.T
        t = rng.randrange(n)
        ages = tuple(rng.sample(range(1, t+1), rng.randrange(t+1)))
        coefficients = tuple(Q(rng.randrange(-12, 13), rng.randrange(1, 20)) for _ in ages)
        variance = Q(rng.randrange(1, 20), rng.randrange(1, 20))
        Fm = symbolic(F)
        adjusted = Fm[t, :]
        if ages:
            adjusted -= symbolic([coefficients]) * Fm.extract([t-age for age in ages], range(p))
        truth = fraction((adjusted * H * adjusted.T)[0] / sp.Rational(str(variance)))
        for Gf, Gc, Gs in [(1, 20, 7), (17, 101, 10**8), (10**18, 10**12, 10**8)]:
            scorer = IntegerIntervalScores(F, [[str(x) for x in row] for row in H.tolist()], feature_grid=Gf,
                                           coefficient_grid=Gc, score_grid=Gs)
            pattern = scorer.prepare(ages, coefficients, variance)
            assert scorer.upper(t, pattern) >= ceiling(truth*Gs)
            counts['dense_exact_arcs'] += 1
            counts['negative_exact_arcs'] += truth < 0
    # Exact cancellation with independent feature rounding can straddle zero.
    for sign in (-1, 1):
        scorer = IntegerIntervalScores((('1/3',), ('1/3',)), ((sign,),),
                                       feature_grid=2, coefficient_grid=3)
        assert scorer.upper(1, scorer.prepare((1,), ('1',), '1')) >= 0
    # Dense covariance regression checks exercise the convenience constructor.
    F = [['-1/3', '2/7'], ['3/8', '-4/9'], ['1/5', '1/11'], ['-5/3', '7/4']]
    H = [['2', '-3/4'], ['-3/4', '1']]
    scorer = IntegerIntervalScores(F, H)
    for rho, latent, nugget in product([Q(-3, 4), Q(0), Q(3, 4)], [Q(0), Q(2, 3)], [Q(1, 5), Q(3)]):
        for ages in [(), (1,), (3,), (3, 1), (3, 2, 1)]:
            C = sp.Matrix(len(ages), len(ages), lambda i, j:
                          sp.Rational(str(latent*rho**abs(ages[i]-ages[j]) + (nugget if i == j else 0))))
            cross = symbolic([[latent*rho**age for age in ages]]) if ages else None
            b = cross*C.inv() if ages else sp.zeros(1, 0)
            d = latent+nugget-fraction((b*cross.T)[0]) if ages else latent+nugget
            adjusted = symbolic(F)[3, :]
            if ages:
                adjusted -= b * symbolic(F).extract([3-age for age in ages], range(2))
            truth = fraction((adjusted*symbolic(H)*adjusted.T)[0])/d
            assert scorer.upper(3, scorer.prepare_history(ages, rho, latent, nugget)) >= ceiling(truth*scorer.score_grid)
            counts['stationary_conditionals'] += 1
    good = scorer.prepare((1,), ('1/2',), '1')
    pattern_changes = [dict(ages=(-1,)), dict(ages=(True,)), dict(ages=(Q(1),)),
                       dict(ages=(1, 1), coefficients=((0, 1), (0, 1))),
                       dict(coefficients=()), dict(coefficients=((2, 1),)),
                       dict(coefficients=((False, 1),)), dict(coefficients=((Q(0), 1),)),
                       dict(coefficients=((0, 1, 2),)), dict(variance_lower=0),
                       dict(variance_lower=-1), dict(coefficient_grid=0),
                       dict(score_denominator=0), dict(score_denominator=-1)]
    failures = [lambda change=change: scorer.upper(3, replace(good, **change))
                for change in pattern_changes]
    failures += [lambda: scorer.prepare((), (), Q(1, 10**13)),
                 lambda: scorer.prepare((), (), Q(0)),
                 lambda: scorer.prepare((), (), Q(-1)),
                 lambda: scorer.upper(0, good),
                 lambda: scorer.upper(True, good),
                 lambda: scorer.upper(4, good),
                 lambda: scorer.upper(3, object()),
                 lambda: IntegerIntervalScores(F, H, score_grid=False),
                 lambda: IntegerIntervalScores(F, H, coefficient_grid=1.0),
                 lambda: IntegerIntervalScores(F, [['1']]),
                 lambda: IntegerIntervalScores(F, [['1', '0'], ['1', '1']]),
                 lambda: IntegerIntervalScores([[0.2]], [['1']]),
                 lambda: scorer.upper(3, IntegerIntervalScores(F, H, feature_grid=3).prepare((1,), ('1/2',), '1'))]
    for fail in failures:
        try:
            fail()
        except (ValueError, TypeError):
            counts['malformed_rejections'] += 1
        else:
            raise AssertionError('Malformed input accepted')
    return counts


def saved_case():
    path = HERE / 'results/noisy-markov-spacing-kinetics-certificate.json'
    saved = json.loads(path.read_text())
    data = saved['problem_data']
    F = tuple(tuple(fraction(x) for x in row) for row in data['F'])
    N = symbolic(saved['tangent_reference'])
    delta = sp.Rational(saved['delta'])
    HH = N.inv()/(1-delta)
    H = tuple(tuple(fraction(HH[i, j]) for j in range(HH.cols)) for i in range(HH.rows))
    n, k, L, gap = saved['n'], saved['k'], saved['L'], saved['minimum_gap']
    rho, latent, nugget = (fraction(data[key]) for key in ('rho', 'latent_variance', 'nugget_variance'))
    scorer = IntegerIntervalScores(F, H, score_grid=saved['score_grid'])
    width = max(L, min(gap-1, n-1))
    # Track calendar-index tuples. Every accepted transition has an independently
    # computed exact score and its interval replacement, priced simultaneously.
    patterns, arc_cache = {}, {}
    states = {(0, ()): (0, 0)}
    visited = 1
    max_loss = changed = 0
    started = perf_counter()
    for t in range(n):
        following = {}
        for (chosen, history), (exact_prefix, interval_prefix) in states.items():
            shifted = tuple(j for j in history if j >= t+1-width)
            moves = []
            if chosen+n-t-1 >= k:
                moves.append(((chosen, shifted), (exact_prefix, interval_prefix)))
            if chosen < k and (not history or t-history[-1] >= gap):
                recent = tuple(j for j in history if t-j <= L)
                key = t, recent
                if key not in arc_cache:
                    ages = tuple(t-j for j in recent)
                    if ages not in patterns:
                        C = symbolic([[latent*rho**abs(i-j)+(nugget if i == j else 0)
                                       for j in ages] for i in ages]) if ages else None
                        cross = symbolic([[latent*rho**age for age in ages]]) if ages else None
                        bmat = cross*C.inv() if ages else sp.zeros(1, 0)
                        b = tuple(fraction(x) for x in bmat)
                        d = latent+nugget-fraction((bmat*cross.T)[0]) if ages else latent+nugget
                        patterns[ages] = b, d, scorer.prepare(ages, b, d)
                    b, d, prepared = patterns[ages]
                    adjusted = tuple(F[t][j]-sum((coefficient*F[row][j] for row, coefficient in zip(recent, b)), Q(0))
                                     for j in range(len(H)))
                    quadratic = sum((H[i][i]*adjusted[i]**2 for i in range(len(H))), Q(0))
                    quadratic += 2*sum((H[i][j]*adjusted[i]*adjusted[j] for i in range(len(H)) for j in range(i)), Q(0))
                    exact = ceiling(scorer.score_grid*quadratic/d)
                    upper = scorer.upper(t, prepared)
                    assert upper >= exact
                    loss = upper-exact
                    max_loss, changed = max(max_loss, loss), changed+(loss != 0)
                    arc_cache[key] = exact, upper
                exact, upper = arc_cache[key]
                target = shifted+((t,) if width else ())
                moves.append(((chosen+1, target), (exact_prefix+exact, interval_prefix+upper)))
            for target, values in moves:
                old = following.get(target, values)
                following[target] = max(old[0], values[0]), max(old[1], values[1])
        states = following
        visited += len(states)
    exact_price = max(value[0] for (chosen, _), value in states.items() if chosen == k)
    interval_price = max(value[1] for (chosen, _), value in states.items() if chosen == k)
    assert exact_price == saved['integer_price']
    assert len(arc_cache) == saved['priced_arcs']
    assert len(patterns) == saved['conditional_patterns']
    return {'certificate_sha256': sha256(path.read_bytes()).hexdigest(),
            'n': n, 'k': k, 'L': L, 'minimum_gap': gap,
            'exact_dense_conditional_patterns': len(patterns),
            'all_arcs_verified': len(arc_cache), 'visited_tuple_states': visited,
            'max_arc_loss_units': max_loss, 'changed_arc_scores': changed,
            'exact_price': exact_price, 'interval_price': interval_price,
            'objective_upper_increase': str(Q(interval_price-exact_price, scorer.score_grid)),
            'wall_seconds': perf_counter()-started}


def main():
    started = perf_counter()
    counts = tests()
    print(json.dumps({'stage': 'generic_checks_passed', 'counts': counts}), flush=True)
    benchmark = saved_case()
    report = {'status': 'passed', 'counts': counts, 'saved_n96_case': benchmark,
              'component_sha256': sha256(Path(component.__file__).read_bytes()).hexdigest(),
              'reviewer_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'wall_seconds': perf_counter()-started}
    (HERE / 'results/integer-interval-scores-independent-review.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
