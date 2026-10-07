"""Reviewer r2: evaluate the old GAMS World MINLPLib point for eg_int_s on the cached OSIL
(mpmath, 40 digits; numerical evidence). Reports max row violation and objective."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])
_PUBLIC_HOME = str(_PublicPath.home())

import sys
sys.path.insert(0, (_PUBLIC_REPO + '/research-20260929/publication/reviews/lit-small-r1'))
from osil_eval import Model
from mpmath import mp, mpf
mp.dps = 40
M = Model((_PUBLIC_HOME + '/.cache/minlplib/minlplib/osil/eg_int_s.osil'))
names = [v['name'] for v in M.vars]
pt = {'x1': '0.564219345767541', 'x2': '0.646847189043049', 'x3': '1', 'x4': '0.93906996780249',
      'i5': '2', 'i6': '4', 'i7': '3', 'objvar': '6.4531031527'}
x = [mpf(pt[n]) for n in names]
print('n', M.n, 'm', M.m, 'names', names)
print('objective', M.objective(x))
print('max violation', mp.nstr(M.violation(x), 6))
# smallest objvar making the point feasible (objvar appears linearly in rows)
worst = []
for r, c in enumerate(M.cons):
    b = M.body(r, x)
    lo = mpf(c['lb']) if c['lb'] not in ('-INF',) else None
    hi = mpf(c['ub']) if c['ub'] not in ('INF',) else None
    v = max((lo - b) if lo is not None else mpf(0), (b - hi) if hi is not None else mpf(0))
    if v > 0: worst.append((float(v), r, c['name']))
print('violated rows', sorted(worst, reverse=True)[:5])
