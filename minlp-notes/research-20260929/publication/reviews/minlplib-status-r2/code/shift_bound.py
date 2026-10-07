"""Review r2: exact upper bound of |obj_gms - obj_osil| on the box p +- 1 (methanol50 p4, lop97icx p2).
Uses the differing coefficients saved by cmp_forms.py (exact rationals) and |x_i| <= |p_i| + 1."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import json, sys
from fractions import Fraction
import sympy as sp
B = (_PUBLIC_REPO + '/research-20260929/publication/reviews/minlplib-status-r2/logs')
S = (_PUBLIC_REPO + '/research-20260929/bound-audit/sol')
for name, pt in [('methanol50', 'methanol50.p4.sol'), ('lop97icx', 'lop97icx.p2.sol')]:
    r = json.load(open(f'{B}/cmp_forms_{name}.json'))
    p = {}
    for line in open(f'{S}/{pt}'):
        a = line.split()
        if len(a) >= 2:
            p[a[0]] = Fraction(a[1])
    tot = Fraction(0)
    for m, a, b in r['diffs']:
        d = abs(Fraction(a) - Fraction(b))
        mon = sp.sympify(m)
        bound = Fraction(1)
        for s, e in mon.as_powers_dict().items():
            if s == 1:
                continue
            bound *= (abs(p.get(str(s), Fraction(0))) + 1) ** int(e)
        tot += d * bound
    print(name, pt, 'sum |delta_m| * max_box |m| =', float(tot), '(exact', tot, ')')
