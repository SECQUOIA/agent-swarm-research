"""Own exact check: does the 10th-significant-digit slack floor change any slack?"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[6])

import json, collections
from fractions import Fraction as Q
from decimal import Decimal
B = (_PUBLIC_REPO + '/research-20260929/bound-audit/')
s = json.load(open(B + 'screen.json'))
def slacks(txt):
    t = txt.replace('−', '-').strip()
    d = Decimal(t)
    if d == 0:
        return None
    exp_last = d.as_tuple().exponent          # unit of last shown digit
    last = Q(1, 2) * Q(10) ** exp_last
    floor = Q(1, 2) * Q(10) ** (d.adjusted() - 9)
    return last, floor
for key in ('pairs', 'ties'):
    ch = [r for r in s[key] if slacks(r['d_listed']) and slacks(r['d_listed'])[1] > slacks(r['d_listed'])[0]]
    print(key, len(s[key]), 'floor changes slack:', len(ch), collections.Counter(r['name'] for r in ch))
    # also point side
    chp = [r for r in s[key] if slacks(r['p_listed']) and slacks(r['p_listed'])[1] > slacks(r['p_listed'])[0]]
    print('   (point value would be affected:', len(chp), collections.Counter(r['name'] for r in chp), ')')
