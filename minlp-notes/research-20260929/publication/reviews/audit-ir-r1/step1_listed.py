"""Exact check of the stored listed points of the four (i-r) instances."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import sys
from fractions import Fraction as F
import rv_osil as R

SOL = (_PUBLIC_REPO + '/research-20260929/bound-audit/sol/')
for name, pt in [('lop97icx', 'p2'), ('stockcycle', 'p2'), ('eniplac', 'p2'),
                 ('spring', 'p3'), ('spring', 'p2')]:
    m = R.load(name)
    x, unk = R.read_sol(m, SOL + '%s.%s.sol' % (name, pt))
    bad = R.check(m, x)
    f = R.obj_value(m, x)
    print(name, pt, 'n=%d m=%d sense=%s' % (len(m.vname), len(m.cname), m.sense),
          'unknown names', unk, 'violations', len(bad))
    print('   obj exact =', f, '~', '%.20f' % float(f) if abs(f) < 10 else float(f))
    for b in sorted(bad, key=lambda t: -abs(t[2]))[:6]:
        print('   ', b[0], b[1], float(b[2]))
