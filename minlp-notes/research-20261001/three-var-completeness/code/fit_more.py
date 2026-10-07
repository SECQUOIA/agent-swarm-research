"""Fit the rays outside D3 from signclass_sup_2.json and positions_retest.json
to family members (48 symmetries, full parameter range).  Numerical."""
import json
import numpy as np
from fit_family import fit

rows = []
for o in json.load(open('../logs/signclass_sup_2.json'))['records']:
    if o['r_d3'] < -1e-6:
        rows.append(('signclass_sup_2', o['p']))
for o in json.load(open('../logs/positions_retest.json')):
    if o.get('r_d3') is not None and o['r_d3'] < -1e-6:
        rows.append(('positions_retest', o['p']))
worst = 0
for src, p in rows:
    c, g, par = fit(p, n_starts=3)
    h, d1, d2, d3, k = par
    D = d1 + d2 - h
    rat = [h / d1, h / d2, (d1 - h) / d3, (d2 - h) / d3, (D + k) / d3]
    worst = max(worst, c)
    print('%.2e' % c, src, 'ratios', np.round(rat, 4).tolist(), flush=True)
print('rays', len(rows), 'max residual %.2e' % worst, flush=True)
