"""Review r2: exact row-by-row comparison of ghg_3veh, MINLPLib 1 text (2010) vs current .gms.
Rows are compared as exact expressions (decimals read as exact rationals); exp() kept symbolic."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import sys
from fractions import Fraction
import sympy as sp
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import exactcmp as X
D = (_PUBLIC_REPO + '/research-20260929/publication/reviews/minlplib-status-r1/dl')
old, ov, osn = X.read_gms(f'{D}/old/MINLPLib.ghg_3veh.gms')
cur, cv, csn = X.read_gms(f'{D}/gms/ghg_3veh.gms')
print('eqs old', len(old), 'cur', len(cur), 'objvar', ov, cv, osn, csn, 'same names', set(old) == set(cur))
for k in sorted(cur, key=lambda s: int(s[1:])):
    eo, so = old[k]; ec, sc = cur[k]
    assert so == sc
    d = sp.expand(eo - ec)
    if d == 0:
        continue
    d2 = sp.cancel(sp.together(eo - ec))
    if d2 == 0:
        print(k, 'same after cancel (rewritten)')
        continue
    # find the constants responsible: compare numerators of together() forms
    print(k, 'DIFFERS')
# exact products
pairs = [('150000', '0.0181052631578947', '2715.7894736842'),
         ('11.34', '33.1610917987189', '376.046780997472'),
         ('0.854659090909091', '33.1610917987189', '28.341428570246'),
         ('150000', '0.03458', '5187')]
for a, b, c in pairs:
    p = Fraction(a) * Fraction(b); w = Fraction(c)
    print(f'{a}*{b} = {p} = {float(p)!r} ; written {c} ; rel diff {float(abs(p - w) / p):.3e}')
# occurrences of the written constants in current file
src = open(f'{D}/gms/ghg_3veh.gms').read()
import re
for c in ['2715.7894736842', '376.046780997472', '28.341428570246']:
    print(c, 'occurrences', len(re.findall(re.escape(c) + r'(?!\d)', src)))
