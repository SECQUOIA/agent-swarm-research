"""Read-only numerical checks for review-r1 corrections; run from the stream directory."""
import json
from pathlib import Path

import numpy as np


root = Path(__file__).resolve().parent.parent


def read(path):
    return json.loads((root / path).read_text())


pool = [json.loads(l) for l in (root / 'data/pool_hard3.jsonl').read_text().splitlines()]
for method in ('K', 'A', 'KA', 'F', 'KAF'):
    c = np.array([(p[method + '_safe'] - p['B_safe']) / (p['X_safe'] - p['B_safe'])
                  for p in pool])
    print(json.dumps(dict(method=method, safe_mean=float(c.mean()),
                          safe_median=float(np.median(c)), safe_min=float(c.min()))))

names = ('chain_m300_e0.3_s1', 'chain_m1000_e0.3_s1', 'chain_m3000_e0.3_s1',
         'cactus_m300_s1', 'ht_plus_n300_k3_s1', 'ht_plus_n1000_k2_s1')
audits = [read('logs/audit/' + name + '.json') for name in names]
for name, r in zip(names, audits):
    gain = r['eps'] * (r['f_uniform'] - r['F_pobj']) / (1 + r['eps'])
    assert abs(gain - r['max_X_improvement']) < 1e-14
    margin = r['F_pobj'] - r['F_safe']
    print(json.dumps(dict(name=name, family_min=r['family_stqp_min'],
                          gain_term=gain, primal_safe_margin=margin,
                          gain_plus_margin=gain + margin, pinf=r['F_pinf'],
                          F_blocks=r['F_blocks'])))
print('family minimum range:', min(r['family_stqp_min'] for r in audits),
      max(r['family_stqp_min'] for r in audits))

ht = []
for p in sorted((root / 'logs/ht').glob('*.jsonl')):
    rs = [json.loads(l) for l in p.read_text().splitlines()]
    r = next(r for r in rs if r['method'] == 'K' and r['round'] == 0)
    ht.append(r['selected'])
    print('ht comparison base selection:', p.stem, r['selected'])
assert (min(ht), max(ht)) == (0, 7)

spar = [json.loads(p.read_text()) for d in ('audit', 'spar_audit')
        for p in (root / 'logs' / d).glob('spar*.json') if not p.name.endswith('.tri.json')]
print('original spar maximum pinf:', max(r['pinf'] for r in spar))

review = read('reviews/r1-logs/spar090_strict.json')
with np.load(root / 'reviews/r1-logs/spar090_strict.depth.npz') as z:
    assert float(z['depths'].min()) == review['min_depth']
    assert len(z['depths']) == 117480
print('reviewer strict result:', json.dumps(review))

fresh = read('logs/strict_r1/spar090-075-1.json')
for k in ('B', 'B_safe', 'min_depth', 'pinf', 'tri', 'gain_term', 'gain_over_gap',
          'gain_plus_margin_over_gap'):
    assert fresh[k] == review[k], k
with np.load(root / 'logs/strict_r1/spar090-075-1.depth.npz') as fresh_depths, \
        np.load(root / 'reviews/r1-logs/spar090_strict.depth.npz') as review_depths:
    assert np.array_equal(fresh_depths['depths'], review_depths['depths'])
print('PASS: all 117480 strict depths and eight headline quantities equal reviewer records bit for bit')

recomputed = [json.loads(l) for l in (root / 'logs/r1_fix_spar_recompute.out').read_text().splitlines()
              if l.startswith('{')]
saved = [r for r in recomputed if 'argmin_depth_triple' in r]
assert len(saved) == 15
assert sum(r['argmin_depth_triple'] == r['argmax_tv_triple'] for r in saved) == 9
for r in saved:
    if r['tv_logged'] == 0:
        assert 0 < r['tv_recomputed'] < 1e-7
print('PASS: 9-of-15 triangle correspondence and all thresholded zero interpretations')
