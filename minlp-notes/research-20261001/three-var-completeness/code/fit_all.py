"""Fit every stored ray outside D3 to a family member (48 symmetries, full
parameter range) and classify its parameter regime.  Numerical."""
import json, sys, collections
import numpy as np
from fit_family import fit

rows = []
for f in sys.argv[1:]:
    for o in json.load(open(f)):
        if o.get('r0', 1) < -1e-6:
            rows.append((f, o))
regimes = collections.Counter(); worst = 0
for f, o in rows:
    c, g, par = fit(o['p'], n_starts=6)
    h, d1, d2, d3, k = par
    D = d1 + d2 - h
    rat = np.array([h / d1, h / d2, (d1 - h) / d3, (d2 - h) / d3, (D + k) / d3])
    if np.all(rat > 1e-4) and np.all(rat < 1 - 1e-4):
        reg = 'five-contact'
    elif abs(rat[4] - 1) < 1e-4 and np.all(rat[:4] > 1e-4) and np.all(rat[:4] < 1 - 1e-4):
        reg = 'boundary d3=D+k'
    else:
        reg = 'other ' + str(np.round(rat, 3).tolist())
    regimes[reg] += 1; worst = max(worst, c)
    print('%.2e' % c, reg, f.split('/')[-1], flush=True)
print('rays', len(rows), 'max residual %.2e' % worst, dict(regimes))
