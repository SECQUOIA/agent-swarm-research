"""Recompute revised reporting numbers from saved points and revision logs."""
import collections
import json
from fractions import Fraction as F
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
load = lambda path: [json.loads(line) for line in (ROOT / path).read_text().splitlines()]
old = {d['file']: d for k in range(3) for d in load(f'logs/sep_run2_s{k}.jsonl')}
new = load('logs/thm3_r1.jsonl')
assert {d['file'] for d in new} == {file for file, d in old.items() if d['rank']['1e-05'] <= 12}
assert len(new) == 113 and not any('error' in d for d in new)
opened = (ROOT / 'logs/open_gap.txt').read_text().split()
groups = collections.defaultdict(list)
for d in new:
    group = ('root' if d['file'].endswith('root.npz') else
             'open' if d['file'].split('__')[0] in opened else 'near')
    groups[group].append(d['thm3'])
summary = {}
for group, rows in groups.items():
    vectors = [r for r in rows if r['v'] is not None]
    summary[group] = dict(
        records=len(rows), returned=len(vectors),
        near_quarter=sum(abs(F(r['q_exact']) + F(1, 4)) <= F(1, 10**9) for r in rows),
        exact_quarter=sum(F(r['q_exact']) == -F(1, 4) for r in rows),
        first_complete=sum(r['first_complete'] for r in rows),
        second_complete=sum(r['second_complete'] for r in rows),
        complete=sum(r['complete'] for r in rows),
        sane=sum(-0.250001 <= r['q_at_Y'] < 0 for r in vectors),
        violation_above_1e3=sum(r['q_at_Y'] < -1e-3 for r in vectors),
        coefficients=[float(np.median([r['vmax'] for r in vectors])), max(r['vmax'] for r in vectors)],
        support=[min(r['supp'] for r in vectors), max(r['supp'] for r in vectors)],
        normalized=[min(r['ratio_at_Y'] for r in vectors), float(np.median([r['ratio_at_Y'] for r in vectors])), max(r['ratio_at_Y'] for r in vectors)],
        matrix_error=max(r['err'] for r in rows),
        time=[float(np.median([r['total_time'] for r in rows])), max(r['total_time'] for r in rows)],
        q_at_Y=[min(r['q_at_Y'] for r in vectors), max(r['q_at_Y'] for r in vectors)],
        max_raw_change=max(abs(r['q_at_Y'] - r['q']) for r in vectors))
    print(group, json.dumps(summary[group]))
print('no split:', [d['file'] for d in new if d['thm3']['v'] is None])
print('failed sanity:', [(d['file'], d['thm3']['vmax'], d['thm3']['q_at_Y']) for d in new
                         if d['thm3']['v'] is not None and not -0.250001 <= d['thm3']['q_at_Y'] < 0])
print('uncertified optimality:', [d['file'] for d in new if not d['thm3']['complete'] and not d['thm3']['optimum_certified']])
rank1 = load('logs/rank1_short_r1.jsonl')
assert len(rank1) == 9 and all(F(r['q_exact']) == -F(1, 4) and r['vmax'] <= 4 for r in rank1)
summary['rank1'] = dict(count=9, coefficients=max(r['vmax'] for r in rank1),
                       support=[min(r['support'] for r in rank1), max(r['support'] for r in rank1)],
                       normalized=[min(r['normalized'] for r in rank1), max(r['normalized'] for r in rank1)],
                       best_normalized=[min(r['best_normalized'] for r in rank1), max(r['best_normalized'] for r in rank1)],
                       max_raw_change=max(abs(r['q_at_Y'] + 0.25) for r in rank1))
print('rank1', summary['rank1'])
certs = load('logs/ratio_certificates_r1.jsonl')
assert len(certs) == 123 and sum(r['certified'] for r in certs) == 110
assert sum(r['certified'] and not r['finished'] for r in certs) == 17
assert sum(r['certified'] or r['finished'] for r in certs) == 120
assert all(r['certified'] or r['finished'] for r in certs if r['file'].endswith('root.npz'))
print('uncertified normalized:', [(r['file'], r['bound']) for r in certs if not r['finished'] and not r['certified']])
bt = load('logs/loop_bt_BT10.jsonl')
general = lambda h: all(h['fam_viol'].get(k, 0) <= 1e-6 for k in ('1', '2', '3')) and -(h['ratio_q'] or 0) > 1e-6
assert sum(general(h) for d in bt for h in d['hist']) == 2057
for p in range(11):
    counts = [sum(general(h) for h in d['hist']) for d in bt if int(d['name'].split('_p')[1].split('_')[0]) == p]
    print('BT10', p, 'general-only mean', np.mean(counts))
calls = [len(d['hist']) for mode in ('bt', 'btfam') for size in ('BT10', 'BT20')
         for d in load(f'logs/loop_{mode}_{size}.jsonl')]
assert sum(calls) == 5168
openrows = [d for d in old.values() if not d['file'].endswith('root.npz') and d['file'].split('__')[0] in opened]
family_values = [max(d[f'fam{k}']['max_viol'] for k in (1, 2, 3)) for d in openrows]
print('family medians all17 / violating15', np.median(family_values), np.median([x for x in family_values if x > 1e-3]))
for d in load('reviews/r1-logs/r1_dense_cap.out'):
    original = old[d['file']]['ratio']['ratio']
    print('dense ratio change', d['file'], d['ratio'], 100 * (d['ratio'] / original - 1))
Y = np.load(ROOT / 'data/points_DM30/dm_QUTO_t2_n30_p25_s0__DM__root.npz')['Y']
Y = (Y + Y.T) / 2
w, V = np.linalg.eigh(Y)
clipped = (V * np.maximum(w, 0)) @ V.T
print('clipped Y00 residual', clipped[0, 0] - 1)
reset = clipped.copy(); reset[0, 0] = 1
print('reset eigenvalue', np.linalg.eigvalsh(reset)[0])
scale = 1 / np.sqrt(clipped[0, 0]); clipped[0, :] *= scale; clipped[:, 0] *= scale
np.linalg.cholesky(clipped + np.diag([0] + [1e-6] * (len(Y) - 1)))
print('congruence Cholesky passed')
(ROOT / 'logs/revision_summary_r1.json').write_text(json.dumps(summary, indent=2) + '\n')
print('ALL REVISED REPORTING CHECKS PASSED')
