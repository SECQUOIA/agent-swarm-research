"""Group A extra checks: lnts duals vs certified N*h2; chain L-column digits."""
import json
from decimal import Decimal, getcontext
from fractions import Fraction as Q
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
getcontext().prec = 60
d = {x['name']: x for x in json.loads((ROOT/'reviews/open-instances-verification/logs/lnts_verify.json').read_text())}
sd = {50: '0.5546687649381', 100: '0.5545954011663', 200: '0.5545770161025', 400: '0.5545724137001'}
for N in (50, 100, 200, 400):
    c = d[f'lnts{N}']['cert_1e-12']; h2 = Q(c['h2']); err = N*Q(1, 2)*Q(10)**(-(len(c['h2'].lstrip('0.'))+c['h2'].index(c['h2'].lstrip('0.')[0])-2))
    Nh2 = N*h2; b = Q(c['bound'])
    hi = Q(json.loads((ROOT/f'publication/primal/lnts/points/lnts{N}_point.json').read_text())['objective_enclosure'][1])
    print(f'lnts{N}: N*h2(printed)={Decimal(Nh2.numerator)/Decimal(Nh2.denominator)} (print error <= {float(err):.1e}); '
          f'16-digit bound {c["bound"]} - N*h2 = {float(b-Nh2):.2e}; summary dual - N*h2 = {float(Q(sd[N])-Nh2):.2e}; '
          f'gap f_hi - N*h2 = {float(hi-Nh2):.6e}')
for n in (50, 100, 200, 400):
    L = Q(json.loads((ROOT/f'open-instances-wave2/cops/logs/chain{n}_bound.json').read_text())['bnb']['bound'])
    print(f'chain{n} L = {Decimal(L.numerator)/Decimal(L.denominator)}')
