"""Review round 2: independent audit of stored data for r1 issues 2, 5, 9, 11
and of the position post-processing. Reads the stream's logs only; no solves.
"""
import ast
import collections
import glob
import itertools
import json
import math
import os

LOGS = os.path.join(os.path.dirname(__file__), '..', '..', 'logs')


def jl(path):
    return [json.loads(s) for s in open(path) if s.strip()]


# Issue 2: stored stratum examples; boundary = config with a vertex contact.
vals = []
for f in sorted(glob.glob(os.path.join(LOGS, 'stratum_enum*_*.jsonl'))):
    for r in jl(f):
        cfg = ast.literal_eval(r['config'])
        nvert = sum(1 for face, _ in cfg if -1 not in face)
        for e in r.get('examples', []):
            vals.append((nvert, e['r_d3'], e['r_R'], min(e['p'][4:7])))
bnd = [v for v in vals if v[0] > 0]
print('issue 2: stored examples %d, boundary %d; boundary R_D range %.6g .. %.6g; '
      'min square coeff (all) %.3g'
      % (len(vals), len(bnd), min(v[1] for v in bnd), max(v[1] for v in bnd),
         min(v[3] for v in vals)))

# Issue 5: fit costs -> distances between unit vectors, sqrt(2 c).
costs = [float(s.split()[0]) for s in open(os.path.join(LOGS, 'fit_more.txt'))
         if 'positions_retest ratios' in s]
dist = sorted(math.sqrt(2 * c) for c in costs)
print('issue 5: %d retest fit costs %.3g .. %.3g -> distances %.3g .. %.3g'
      % (len(costs), min(costs), max(costs), dist[0], dist[-1]))

# Issue 9: 265 post-processed vs 264 retested.
post = jl(os.path.join(LOGS, 'postprocess_positions.jsonl'))
ret = json.load(open(os.path.join(LOGS, 'positions_retest.json')))
low = [r for r in ret if r['search_resid'] <= 1e-6]
passed = [r for r in ret if r['inner'] is not None and r['inner'] < 1e-6]
tested = [r for r in ret if r.get('r_R') is not None]
print('issue 9: retest records %d; search cost <= 1e-6: %d; retest cost < 1e-6: %d; '
      'tested against R: %d; post-processed: %d'
      % (len(ret), len(low), len(passed), len(tested), len(post)))
for r in low:
    if r not in passed:
        print('   failed retest:', r['config'], 'search', r['search_resid'], 'retest', r['inner'])
print('   min r_R over tested %.3g; r_d3 < -1e-6: %d'
      % (min(r['r_R'] for r in tested), sum(r['r_d3'] < -1e-6 for r in tested)))

# Position post-processing: exact-contact max p(0).
st = collections.Counter('none' if r['maxp0'] is None else
                         ('>1e-4' if r['maxp0'] > 1e-4 else '<=1e-4') for r in post)
print('post-processing max p(0) under exact contacts:', dict(st))
panics, cur = collections.Counter(), 0
for s in open(os.path.join(LOGS, 'postprocess_positions.txt')):
    if 'panicked' in s:
        cur += 1
    elif ' maxp0 ' in s:
        panics[(s.split()[2] == 'None', cur > 0)] += 1
        cur = 0
print('   main log (None?, preceded by a Clarabel panic?):', dict(panics))

# Issue 11: sign patterns of (q12, q13, q23); complementing i flips edges at i.
edges = ((0, 1), (0, 2), (1, 2))
for signs in itertools.product((-1, 1), repeat=3):
    need = None
    for size in range(4):
        for S in itertools.combinations(range(3), size):
            new = [s * (-1) ** sum(i in S for i in e) for s, e in zip(signs, edges)]
            if all(v > 0 for v in new):
                need = size if need is None else need
                break
        if need is not None:
            break
    print('issue 11: signs', signs, 'product', math.prod(signs),
          'min complementations to all-positive:', need)
