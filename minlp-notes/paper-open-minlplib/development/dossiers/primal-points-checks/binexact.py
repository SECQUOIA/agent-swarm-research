# Which OSIL numeric constants are not exactly representable in binary64?
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

import re, sys
from decimal import Decimal
from fractions import Fraction as F
def nonbin(s):
    if s in ('INF','-INF','inf','-inf'): return False
    try: d = Decimal(s)
    except Exception: return False
    return F(d) != F(float(d))
for n in sys.argv[1:]:
    txt = open(f'{_PUBLIC_HOME}/.cache/minlplib/minlplib/osil/{n}.osil').read()
    vals = re.findall(r'(?:lb|ub|value|coef|constant)="([^"]+)"', txt)
    m = re.search(r'<value>(.*?)</value>', txt, re.S)
    if m: vals += re.findall(r'>([^<>]+)</el>', m.group(1))
    bad = sorted({v for v in vals if nonbin(v)}, key=lambda s: abs(float(s)))
    print(f'{n}: {len(vals)} numeric strings, {len(bad)} distinct non-binary64-exact: {bad[:6]}{" ..." if len(bad)>6 else ""}')
