"""Post-check normalized maxima using Lemma A, at stored matrices.

Enumerate integer directions up to the adaptive squared-norm bound, modulo
global sign. Floating eigenvalues use a 1e-9 safety slack; agreement within
1e-6 is a numerical certificate, not an exact rational certificate.
Usage: python3 code/certify_ratio_r1.py OUT.jsonl [max_directions]
"""
import collections
import itertools
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def patterns(bound, dimension, largest=None, prefix=()):
    if prefix:
        yield prefix
    if len(prefix) == dimension:
        return
    largest = min(math.isqrt(bound), largest if largest is not None else math.isqrt(bound))
    for a in range(largest, 0, -1):
        yield from patterns(bound - a * a, dimension, a, prefix + (a,))


def sign_orders(pattern):
    for order in set(itertools.permutations(pattern)):
        for signs in itertools.product((1, -1), repeat=len(order) - 1):
            yield np.array((order[0],) + tuple(a * s for a, s in zip(order[1:], signs)))


def direction_count(n, bound):
    if bound > 16:
        return math.inf
    total = 0
    for pattern in patterns(bound, n):
        orders = math.factorial(len(pattern))
        for count in collections.Counter(pattern).values():
            orders //= math.factorial(count)
        total += math.comb(n, len(pattern)) * orders * 2**(len(pattern) - 1)
    return total


def enumerate_best(Y, bound):
    x = Y[0, 1:]
    S = Y[1:, 1:] - np.outer(x, x)
    best, arg = -math.inf, None
    for pattern in patterns(bound, len(x)):
        k = len(pattern)
        norm = sum(a * a for a in pattern)
        combinations = itertools.combinations(range(len(x)), k)
        while True:
            C = np.array(list(itertools.islice(combinations, 100000)), dtype=int).reshape(-1, k)
            if not len(C):
                break
            for signs in sign_orders(pattern):
                t = x[C] @ signs
                frac = t - np.floor(t)
                variance = sum(signs[i] * signs[j] * S[C[:, i], C[:, j]]
                               for i in range(k) for j in range(k))
                ratios = (frac * (1 - frac) - variance) / norm
                index = int(np.argmax(ratios))
                if ratios[index] > best:
                    best = float(ratios[index])
                    w = np.zeros(len(x), dtype=int)
                    w[C[index]] = signs
                    arg = [-math.ceil(float(t[index]))] + w.tolist()
    return best, arg


if __name__ == '__main__':
    maxwork = float(sys.argv[2]) if len(sys.argv) > 2 else 2e8
    records = [json.loads(line) for k in range(3)
               for line in (ROOT / f'logs/sep_run2_s{k}.jsonl').read_text().splitlines()]
    stats = collections.Counter()
    worst = 0.0
    with open(sys.argv[1], 'w') as out:
        for d in records:
            start = time.monotonic()
            file = d['file']
            size = file.split('_n')[1].split('_')[0]
            family = 'BT' if file.startswith('bt') else 'DM'
            Y = np.load(ROOT / f'data/points_{family}{size}' / file)['Y']
            Y = (Y + Y.T) / 2
            scale = float(Y[0, 0])
            Y = Y / scale  # Lemma A requires exactly Y00 = 1.
            x = Y[0, 1:]
            lmin = float(np.linalg.eigvalsh(Y[1:, 1:] - np.outer(x, x))[0])
            slack = max(0.0, -lmin) + 1e-9
            rho = d['ratio']['ratio']
            rec = dict(file=file, finished=d['ratio']['complete'], rho=rho,
                       scale=scale, eigen_slack=slack, certified=False)
            if rho / scale <= slack:
                rec['status'] = 'no_finite_bound'
            else:
                bound = math.floor(1 / (4 * (rho / scale - slack)))
                work = direction_count(len(x), bound)
                rec.update(bound=bound, directions=work if math.isfinite(work) else None)
                if work > maxwork:
                    rec['status'] = 'too_large'
                else:
                    best, v = enumerate_best(Y, bound)
                    diff = scale * best - rho
                    rec.update(best_at_stored=scale * best, excess=diff, v=v,
                               certified=diff <= 1e-6,
                               status='certified' if diff <= 1e-6 else 'better_found')
                    worst = max(worst, diff)
            rec['time'] = time.monotonic() - start
            stats[rec['status']] += 1
            stats['new_certificates'] += rec['certified'] and not rec['finished']
            stats['finished_or_certified'] += rec['finished'] or rec['certified']
            out.write(json.dumps(rec) + '\n'); out.flush()
            print(json.dumps(rec), flush=True)
    print('SUMMARY', dict(stats), 'max_excess', worst)
    assert stats['new_certificates'] == 17 and stats['finished_or_certified'] == 120
    assert stats['better_found'] == 0
