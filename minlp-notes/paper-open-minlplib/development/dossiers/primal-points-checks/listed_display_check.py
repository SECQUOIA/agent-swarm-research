"""Listed MINLPLib primal displays (rounded, 7-10 significant digits) of the 13 instances
versus our safe dual displays and our exact-point enclosure upper ends.
Input: part_a.json (copy of R/publication/minlplib-status/data/part_a.json)."""
import json
from fractions import Fraction as F
d = json.load(open('part_a.json'))['instances']
duals = {'lnts50': '0.5546687649381', 'lnts100': '0.5545954011663', 'lnts200': '0.5545770161025', 'lnts400': '0.5545724137001',
         'dtoc5': '5.38967211918114', 'lukvle10': '352.2380254050784', 'chain50': '5.0722614939828627', 'chain100': '5.0697846107387505',
         'chain200': '5.0689173417931616', 'chain400': '5.068621694604009', 'powerflow0030p': '576.8934122988004',
         'powerflow0039p': '41869.05148485014', 'powerflow0039r': '41869.05148327243'}
for k, dl in duals.items():
    for p in d[k]['page']['points']:
        if not p.get('bold'):
            continue
        v = F(p['value'])
        sig = len(p['value'].replace('-', '').replace('.', '').lstrip('0'))
        print(f"{k:15s} {p['point']} {p['value']:>14s} ({sig} sig. digits, listed infeas {p['infeas']}): display - our dual = {float(v - F(dl)):+.2e}")
