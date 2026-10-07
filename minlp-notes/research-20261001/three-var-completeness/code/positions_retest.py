"""Robust re-test of the position search (blocking_positions.py).

For every minimal blocking configuration B and the best positions theta found
by the search, solve the inner problem again,
    min ||A(theta) p||^2  over the base of P3plus with p(0) >= 0.01,
and test the minimizer p directly.  p is an exactly valid quadratic (it
satisfies the exact six-simplex description of P3plus up to solver
accuracy) with p(0) >= 0.01 and approximately the prescribed contacts; we
record its relaxation values over D3 and over R.  A negative R value would
exhibit a valid quadratic missing from cl(D3) + family copies.
Numerical only.
"""
import ast
import glob
import json
import re
import warnings

import numpy as np

warnings.filterwarnings("ignore")
from blocking_positions import Inner  # noqa: E402
from sdp3 import Relaxation, cube_min  # noqa: E402

inner = Inner()
R1 = Relaxation(use_family=True)
R0 = Relaxation(use_family=False)


def safe(fn, *a):
    try:
        return fn(*a)
    except BaseException as e:
        if isinstance(e, KeyboardInterrupt):
            raise
        return None


recs = {}
for f in sorted(glob.glob('../logs/blocking_positions_*.txt')):
    for ln in open(f):
        m = re.match(r'^(\S+) (family-sub|NEW) (\(\(.*\)\)) (\[.*\]) elapsed', ln)
        if m:
            B = ast.literal_eval(m.group(3))
            recs[repr(B)] = dict(config=B, resid=float(m.group(1)), theta=ast.literal_eval(m.group(4)),
                                 family_sub=(m.group(2) == 'family-sub'))
print('configurations with search results:', len(recs), flush=True)
out = []
for key, r in recs.items():
    val = safe(inner, r['config'], np.array(r['theta']))
    p = inner.pv.value
    rec = dict(config=r['config'], theta=r['theta'], search_resid=r['resid'], inner=val)
    if val is not None and p is not None and val < 1e-6:
        p = np.array(p) / np.abs(p).max()
        a0 = safe(R0.solve, p)
        a1 = safe(R1.solve, p)
        rec.update(p0=float(p[0]), cubemin=float(cube_min(p)),
                   r_d3=None if a0 is None else float(a0[0]),
                   r_R=None if a1 is None else float(a1[0]), p=p.tolist())
    out.append(rec)
    print('%-9s' % ('%.2e' % val if val is not None else 'fail'), 'p0', rec.get('p0'),
          'r_d3', rec.get('r_d3'), 'r_R', rec.get('r_R'), r['config'], flush=True)
json.dump(out, open('../logs/positions_retest.json', 'w'), default=float)
tested = [o for o in out if o.get('r_R') is not None]
print('tested', len(tested), 'min r_R', min(o['r_R'] for o in tested),
      'n r_R < -1e-6:', sum(o['r_R'] < -1e-6 for o in tested),
      'n r_d3 < -1e-6:', sum(o['r_d3'] is not None and o['r_d3'] < -1e-6 for o in tested), flush=True)
