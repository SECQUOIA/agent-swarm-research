"""Audit stored data for review-r1 issues 2, 5-7, 9 and 11; no new solves.

Run from any directory. All inputs are read-only. Printed fit costs come
from rounded logs; distances are sqrt(2 * cost) between unit coefficient
vectors, not certified distances to the entire family.
"""
import ast
from itertools import product
import json
import math
from pathlib import Path
import re

LOGS = Path(__file__).resolve().parents[1] / 'logs'

# The five-edge type has no vertex contact; each of S1-S5 has one.
boundary = []
all_examples = []
for path in sorted(LOGS.glob('stratum_enum*_*.jsonl')):
    for line in path.read_text().splitlines():
        rec = json.loads(line)
        config = ast.literal_eval(rec['config'])
        examples = rec.get('examples', [])
        all_examples.extend(examples)
        if any(-1 not in face for face, tangencies in config):
            boundary.extend(examples)
assert len(all_examples) == 34 and len(boundary) == 30
lo = min(ex['r_d3'] for ex in boundary)
hi = max(ex['r_d3'] for ex in boundary)
assert -1.75e-3 < lo < -1.73e-3 and -9.4e-6 < hi < -9.3e-6
assert all(ex['r_d3'] < 0 for ex in boundary)
assert all(min(ex['p'][4:7]) > 0 for ex in boundary)
print(f'PASS: 30 stored boundary examples of 34 total; R_D range {lo:.17g} to {hi:.17g}; positive squares')

costs = []
for line in (LOGS / 'fit_more.txt').read_text().splitlines():
    if 'positions_retest ratios' in line:
        costs.append(float(line.split()[0]))
assert len(costs) == 8
distances = [math.sqrt(2 * c) for c in costs]
assert 7.9e-4 < min(distances) < 8.1e-4
assert 0.086 < max(distances) < 0.087
print(f'PASS: 8 retest fits; cost range {min(costs):.3g} to {max(costs):.3g}; unit-vector distances {min(distances):.9g} to {max(distances):.9g}')

stored = []
for line in (LOGS / 'check_min_rR_dense.txt').read_text().splitlines():
    stored.append(float(re.match(r'stored (\S+)', line)[1]))
assert len(stored) == 5 and min(stored) == -1.37e-10 and max(stored) == 1.04e-11
assert min(ex['r_R'] for ex in all_examples) > -7e-9
print('PASS: 5 re-solved rays had stored R values -1.37e-10 to 1.04e-11; none was the -7.0e-9 ray')

for name, positive in (('project_probe_l1_34_p003.txt', True),
                       ('project_probe_l2_33_p0.txt', False)):
    vals = [float(m[1]) for line in (LOGS / name).read_text().splitlines()
            if (m := re.search(r'sep\(y0\) (\S+)', line))]
    assert len(vals) == 6
    assert all((v > 0) == positive for v in vals)
    print(f'PASS: {name}: all 6 logged starting-point separations have the expected sign; range {min(vals):.9g} to {max(vals):.9g}')

post = [json.loads(line) for line in (LOGS / 'postprocess_positions.jsonl').read_text().splitlines()]
retest = json.loads((LOGS / 'positions_retest.json').read_text())
key = lambda rec: repr(rec['config'])
post_by_config = {key(rec): rec for rec in post}
retest_by_config = {key(rec): rec for rec in retest}
tested = {key(rec) for rec in retest if rec.get('r_R') is not None}
assert len(post) == len(post_by_config) == 265
assert len(retest) == len(retest_by_config) == 312 and len(tested) == 264
assert all(rec['resid'] <= 1e-6 for rec in post)
assert tested <= post_by_config.keys()
dropped = list(post_by_config.keys() - tested)
assert len(dropped) == 1
rec = retest_by_config[dropped[0]]
assert rec['search_resid'] == 1.48e-9
assert rec['inner'] == 2.535309231191649e-6
assert rec.get('r_R') is None and rec.get('p') is None
print('PASS: 265 original search costs <= 1e-6; 264 retests passed < 1e-6')
print('Excluded configuration:', rec['config'])
print('Search cost:', rec['search_resid'], '| retest cost:', rec['inner'])

# Strictly positive product means either no negative edge or two sharing
# one vertex. Complementing that vertex makes all three signs positive.
edges = ((0, 1), (0, 2), (1, 2))
for signs in product((-1, 1), repeat=3):
    if math.prod(signs) != 1:
        continue
    assert any(all(s * (-1 if i in edge else 1) > 0
                   for s, edge in zip(signs, edges)) for i in (-1, 0, 1, 2))
print('PASS: all 4 strict positive-product sign patterns become all-positive with at most one complementation')
