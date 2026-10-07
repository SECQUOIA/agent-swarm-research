"""Compare the r2 rerun with r1 and verify the non-root/rank-1 wording."""
import json
import math
import statistics
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return [json.loads(line) for line in (ROOT / 'logs' / name).read_text().splitlines()]


old, new = load('thm3_r1.jsonl'), load('thm3_r2.jsonl')
assert len(old) == len(new) == 113
by_file = {d['file']: d for d in old}
assert len({d['file'] for d in new}) == 113
assert {d['file'] for d in new} == set(by_file)
keys = ('v', 'q_exact', 'q_at_Y_exact', 'vmax', 'supp', 'delta',
        'complete', 'first_complete', 'second_complete', 'optimum_certified')
for d in new:
    assert 'error' not in d
    for method in ('thm3', 'rank1_grid'):
        if method not in d:
            assert method not in by_file[d['file']]
            continue
        a, b = by_file[d['file']][method], d[method]
        assert all(a.get(k) == b.get(k) for k in keys), (d['file'], method)
print('113/113 reruns: identical vectors, exact neighbour/stored values, coefficients, supports and flags.')
assert sum(d['thm3']['v'] is not None for d in new) == 111
assert sum(d['thm3']['complete'] for d in new) == 99
assert sum(F(d['thm3']['q_exact']) == -F(1, 4) for d in new) == 35
assert sum(abs(F(d['thm3']['q_exact']) + F(1, 4)) <= F(1, 10**9) for d in new) == 109
print('111 vectors; 99 combined complete; 35 exact -1/4; 109 within 1e-9; no numerical claim changes.')

rank1 = [d for d in new if 'rank1_grid' in d]
assert len(rank1) == 10
fractional = []
for d in rank1:
    a, b = d['thm3'], d['rank1_grid']
    assert all(a.get(k) == b.get(k) for k in ('delta', 'v', 'q_exact', 'q_at_Y_exact'))
    if a['v'] is not None:
        assert F(a['q_exact']) == -F(1, 4) and a['vmax'] <= 5
        fractional.append(a)
    print('rank1', d['file'], 'identical results; thm3 vmax', a.get('vmax'))
assert len(fractional) == 9
assert min(a['vmax'] for a in fractional) == 1 and max(a['vmax'] for a in fractional) == 5
print('10/10 rank-1 rationalizations agree; main thm3 coefficients 1-5 at all 9 fractional roots.')

nonroot = load('nonroot_r2.jsonl')
assert len(nonroot) == 13
review = {d['file']: d for d in map(json.loads,
          (ROOT / 'reviews/r2-logs/r2_nonroot.jsonl').read_text().splitlines())}
for d in nonroot:
    r = review[d['file']]
    assert F(d['q_exact']) == F(r['q_neighbour'])
    assert d['vmax'] == r['logged_vmax'] and d['norm2'] == r['logged_norm2']
    assert math.isclose(d['coset_bound_one'], r['coset_norm_lower_bound'], rel_tol=1e-12)
print('All 13 independent one-direction coset bounds reproduce the reviewer’s bounds.')
violated = [d for d in nonroot if d['q_at_Y'] < 0]
assert len(violated) == 5
assert min(d['vmax'] for d in nonroot) == 30 and max(d['vmax'] for d in nonroot) == 69618975
assert max(d['ratio_at_Y'] for d in violated) <= 8.2e-6
print('Non-root: 13 vectors, coefficients 30-69618975, 8 unviolated; 5 ratios max',
      max(d['ratio_at_Y'] for d in violated), 'median', statistics.median(d['ratio_at_Y'] for d in violated))
forced = [d for d in nonroot if 'maximizing_images' in d]
assert len(forced) == 4 and all(d['both_complete'] for d in forced)
for d in forced:
    assert d['returned_over_shortest_bound'] <= 1.015
    assert d['all_maximizers_bound'] >= 1.1e4
    assert d['tail_part'] / d['q_at_Y'] >= 0.998
    print('forced', d['file'], 'maximizing images', d['maximizing_images'],
          'norm lower bound', d['all_maximizers_bound'], 'returned norm', math.sqrt(d['norm2']),
          'returned/shortest <=', d['returned_over_shortest_bound'],
          'lambda_r+1', d['lambda_r1'], 'tail/q', d['tail_part'] / d['q_at_Y'])
print('All maximizing images checked exactly; returned norms within 1.5% of shortest at all 4 points.')
print('ALL R2 REPORTING CHECKS PASSED')
