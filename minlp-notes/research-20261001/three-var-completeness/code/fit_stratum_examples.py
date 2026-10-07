"""Fit the stored examples outside D3 from the stratum enumeration
(stratum_enum{TAG}_*.jsonl) to family members.  Numerical.
usage: python fit_stratum_examples.py [TAG]"""
import glob
import json
import sys

import numpy as np

from fit_family import fit

tag = sys.argv[1] if len(sys.argv) > 1 else ''
recs = []
for f in sorted(glob.glob(f'../logs/stratum_enum{tag}_[0-9].jsonl')):
    recs += [json.loads(l) for l in open(f)]
worst = 0
n = 0
for r in recs:
    if r['notd3'] == 0:
        continue
    for ex in r['examples']:
        c, g, par = fit(ex['p'], n_starts=3)
        h, d1, d2, d3, k = par
        D = d1 + d2 - h
        rat = [h / d1, h / d2, (d1 - h) / d3, (d2 - h) / d3, (D + k) / d3]
        worst = max(worst, c)
        n += 1
        print(r['config'], 'r_d3 %.2e r_R %.2e' % (ex['r_d3'], ex['r_R']), 'fit %.1e' % c,
              'ratios', np.round(rat, 4).tolist(), 'k %.3g' % k, flush=True)
print('examples', n, 'max residual %.2e' % worst, flush=True)
