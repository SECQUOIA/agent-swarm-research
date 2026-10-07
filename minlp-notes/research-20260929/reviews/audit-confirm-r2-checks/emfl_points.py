"""Place each emfl listed point relative to the exact bounds of cert_socp.py.

Read-only. Run from research-20260929/bound-audit. For each listed point, the
displayed value v is widened by h = half a unit in its last shown digit.
"below L" means v + h < L, with L the 30-digit rounded-down lower bound (<= exact L).
"above U" means v - h > U, with U the stored upper bound (str(float(ub)), within 2e-15).
"""
import json
from decimal import Decimal
from fractions import Fraction as F

pages = {p['name']: p for p in json.load(open('pages.json'))}


def half_ulp(s):
    return F(1, 2) * F(10) ** Decimal(s).as_tuple().exponent


prim = []
for k in ['emfl050_3_3', 'emfl050_5_5', 'emfl100_3_3', 'emfl100_5_5']:
    c = json.load(open(f'logs/cert_socp_{k}.json'))
    L = F(Decimal(c['lower_bound_30_digits_rounded_down']))
    U = F(Decimal(c['rigorous_upper_bound_from_numerical_optimum']))
    print(k, pages[k]['sense'], 'L', float(L), 'U', float(U))
    for p in sorted(pages[k]['points'], key=lambda p: p['point']):
        v, h = F(Decimal(p['value'])), half_ulp(p['value'])
        if v + h < L:
            tag = 'below L by >= %.4g' % float(L - (v + h))
        elif v - h > U:
            tag = 'above U by >= %.4g' % float((v - h) - U)
        else:
            tag = 'undecided'
        print('  ', p['point'], p['section'], p['value'], 'infeas', p['infeas'], tag)
        if p['section'] == 'primal' and float(p['infeas']) < 1e-8:
            prim.append((k, p['point'], float(p['infeas']), tag.split()[0]))

print('primal-section points with listed infeas < 1e-8:')
for r in prim:
    print('  ', *r)
allv = [r[2] for r in prim]
bel = [r[2] for r in prim if r[3] == 'below']
print('range over all: %g to %g' % (min(allv), max(allv)))
print('range over those below L: %g to %g' % (min(bel), max(bel)))
