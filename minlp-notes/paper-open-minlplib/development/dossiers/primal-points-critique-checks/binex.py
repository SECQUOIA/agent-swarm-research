from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

import re, sys
from decimal import Decimal
from fractions import Fraction as F
def nonbin(s):
    if s.strip() in ('INF','-INF','inf','-inf','Infinity','-Infinity'): return False
    try: d = Decimal(s.strip())
    except Exception: return False
    return F(d) != F(float(d))
for n in sys.argv[1:]:
    try: txt = open(f'{_PUBLIC_HOME}/.cache/minlplib/minlplib/osil/{n}.osil').read()
    except Exception as e: print(n, 'missing'); continue
    vals = re.findall(r'\b(?:lb|ub|value|coef|constant)="([^"]+)"', txt)
    for m in re.finditer(r'<value>(.*?)</value>', txt, re.S):
        vals += re.findall(r'>([^<>]+)</el>', m.group(1))
    vals += re.findall(r'<coef[^>]*>([^<]+)</coef>', txt)
    bad = sorted({v for v in vals if nonbin(v)}, key=lambda s: abs(float(s)))
    print(f'{n}: {len(vals)} strings, {len(bad)} distinct non-binary64-exact: {bad[:5]}')
