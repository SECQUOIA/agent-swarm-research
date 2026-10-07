"""Group A independent recheck of chain gaps vs safe displays, display validity, u-distance."""
import json, sys
from fractions import Fraction as F
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]   # research-20260929
CH = ROOT/'publication/primal/chain'
def sci_up(q, sig=3):
    # round positive rational up to `sig` significant digits, return string
    assert q > 0
    e = 0
    while q >= 10**(e+1): e += 1
    while q < 10**e: e -= 1
    scale = F(10)**(e - sig + 1)
    m = -((-q) // scale)  # ceil
    if m >= 10**sig: m //= 10; e += 1; scale *= 10; m = -((-q)//scale)
    return f"{int(m)}e{e-sig+1}"
displays = {50:'5.0722614939828627',100:'5.0697846107387505',200:'5.0689173417931616',400:'5.068621694604009'}
oldshort = {50:'5.072261493982863',200:'5.068917341793162'}
for n in (50,100,200,400):
    bj = json.loads((ROOT/f'open-instances-wave2/cops/logs/chain{n}_bound.json').read_text())
    b = bj['bnb']['bound']
    assert isinstance(b, float), type(b)
    L = F(b)
    box = json.loads((CH/f'points/chain{n}_box.json').read_text())
    enc = box['objective_enclosure_decimal']
    hi = F(enc[1]) if isinstance(enc, list) else None
    D = F(displays[n])
    print(f'chain{n}: repr(L)={b!r}  L exact first 25 digits: {float(L)!r}')
    print('  display', displays[n], 'D<=L:', D <= L, ' L-D =', float(L-D))
    print('  gap(hi - D) up:', sci_up(hi-D), ' rel (hi-D)/D up:', sci_up((hi-D)/D), ' rel (hi-D)/L up:', sci_up((hi-D)/L))
    print('  gap(hi - L) up:', sci_up(hi-L), ' rel (hi-L)/L up:', sci_up((hi-L)/L))
    if n in oldshort:
        S = F(oldshort[n]); print('  old shortest repr', oldshort[n], 'S-L =', float(S-L), 'S>L:', S > L)
    # u distance: box centres vs wave-2 double primal
    vals = [F(float(x)) for x in (ROOT/f'open-instances-wave2/cops/logs/chain{n}_primal.txt').read_text().split()]
    cen = [F(v['centre']) for v in box['variables']]
    assert len(vals) == len(cen) == 2*n+2, (len(vals), len(cen))
    dx = max(abs(a-c) for a, c in zip(vals[:n+1], cen[:n+1]))
    du = max(abs(a-c) for a, c in zip(vals[n+1:], cen[n+1:]))
    print('  max|dx| =', float(dx), ' max|du| =', float(du), ' (box radius 1e-40)')
