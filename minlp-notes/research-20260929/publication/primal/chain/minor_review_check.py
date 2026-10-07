"""Check displayed bounds and recompute gaps from stored objective enclosures only."""
import json
from decimal import Decimal, localcontext, ROUND_CEILING
from fractions import Fraction as Q
from pathlib import Path
P = Path(__file__).resolve().parent
R = P.parents[2]
displays = {50:'5.0722614939828627',100:'5.0697846107387505',200:'5.0689173417931616',400:'5.068621694604009'}
s = (P/'logs/verify.log').read_text(); dec = json.JSONDecoder(); rows = []
while s.strip():
    v, n = dec.raw_decode(s.lstrip()); rows.append(v); s = s.lstrip()[n:]
def up(q):
    with localcontext() as c:
        c.prec = 60; x = Decimal(q.numerator)/Decimal(q.denominator)
        return str(x.quantize(Decimal(1).scaleb(x.adjusted()-2), rounding=ROUND_CEILING))
for v in rows:
    n = int(v['instance'][5:]); b = json.loads((R/f'open-instances-wave2/cops/logs/chain{n}_bound.json').read_text())['bnb']['bound']; L = Q(b); D = Q(displays[n]); U = Q(v['objective_hi']); assert D <= L
    print(v['instance'], 'safe display', displays[n], 'gap', up(U-D), 'relative', up((U-D)/D), 'exact-double gap',up(U-L))
for n in displays:
    for line in (P/f'logs/build_{n}.log').read_text().splitlines():
        if 'dist' in line.lower() or 'deviation' in line.lower() or 'max|du|' in line: print(n,line)
print('PASS: all four displays are valid; gaps use exact rational arithmetic.')
