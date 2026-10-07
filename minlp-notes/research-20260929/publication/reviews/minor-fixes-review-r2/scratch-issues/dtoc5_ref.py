"""Read-only: min/max of listed coordinates in saved QPLIB_8585.sol."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

from fractions import Fraction as Q
f = (_PUBLIC_REPO + '/research-20260929/publication/literature/control/sources/qplib/QPLIB_8585.sol')
v = {}
for l in open(f):
    p = l.split()
    if len(p) == 2 and p[0].startswith('x'):
        v[p[0]] = Q(p[1])
mn = min(v.items(), key=lambda t: t[1]); mx = max(v.items(), key=lambda t: t[1])
print('listed x', len(v), 'min', mn[0], float(mn[1]), 'max', mx[0], float(mx[1]), 'x50001', v.get('x50001'), 'x1', v.get('x1'))
