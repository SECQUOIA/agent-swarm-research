"""Recompute the facts behind the nine revisions of bound-audit/audit-report.md. Read-only.

Usage: python3 recompute_fixes.py
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import json, collections
from fractions import Fraction as F
from decimal import Decimal

A = (_PUBLIC_REPO + '/research-20260929/bound-audit/')
R = json.load(open(A + 'results.json'))
P = {p['name']: p for p in json.load(open(A + 'pages.json'))}

print('== 1 ghg_3veh p2')
v = json.load(open(A + 'logs/verify/ghg_3veh.p2.json'))
print(v['route'], '|', v['attempt'], '|', v['route_A_failure'], '|', v['obj_lo'][:18], v['obj_hi'][:18])

print('== 2 class (ii) by solver, violations, squfl drop')
ii = [r for r in R if r['cls'].startswith('(ii)')]
by = collections.Counter((r['solver'], r['cls']) for r in {(r['name'], r['solver'], r['cls']): r for r in ii}.values())
print(sorted(by.items()))
print('solvers with (ii):', sorted({r['solver'] for r in ii}))
print('viol range', min(r['viol_eval'] for r in ii), max(r['viol_eval'] for r in ii))
sq = {(r['name'], r['point']): r for r in ii if r['name'].startswith('squfl')}
d = [float((F(r['obj_lo']) - F(r['obj_eval'])) / F(r['obj_lo'])) for r in sq.values()]
print('squfl relative drop vs repair: %.3g .. %.3g' % (min(d), max(d)))
c = collections.Counter(dd['solver'] for p in P.values() for dd in p['duals'])
print('solver labels on pages:', len(c), c.most_common())

print('== 3/4 dates')
for n in ['glider100', 'ghg_3veh', 'methanol50', 'sssd20-04persp', 'sssd22-08persp', 'sssd25-04persp', 'sssd25-08persp']:
    p = P[n]
    print(n, [(q['point'], q['value'], q['added']) for q in p['points']],
          [(x['solver'], x['value'], x['date']) for x in p['duals'] if x['solver'] in ('LINDO', 'COUENNE', 'ANTIGONE', 'BARON')])

print('== 6/7 class (i) relative margins (strongest point per pair)')
best = {}
for r in R:
    if r['cls'].startswith('(i) proven'):
        dd = F(r['d_listed']); m = dd - F(r['obj_hi']) if r['sense'] == 'min' else F(r['obj_lo']) - dd
        k = (r['name'], r['solver'])
        if k not in best or m > best[k][0]:
            best[k] = (m, m / abs(dd), r['i_group'], r['d_slack'])
for k, (m, rel, g, sl) in sorted(best.items(), key=lambda kv: -kv[1][1]):
    print(g, k, '%.4g' % float(m), 'rel %.3g' % float(rel), '1e-6/rel %.3g' % (1e-6 / float(rel)), 'units %.4g' % (float(m) / (2 * sl)))

print('== 8 glider100 altitude block x103..x203')
def rd(f):
    out = {}
    for line in open(f):
        s = line.split()
        if len(s) >= 2 and s[0][0] == 'x':
            out[s[0]] = float(s[1])
    return out
p = rd(A + 'sol/glider100.p2.sol'); cc = rd(A + 'logs/verify/glider100.p2.center.sol')
alt = [p.get('x%d' % i, 0.0) for i in range(103, 204)]
print('listed: node0', alt[0], 'node1', alt[1], "('x104' in sol:", 'x104' in p, ') max', max(alt), 'at node', alt.index(max(alt)), 'last', alt[-1])
g = json.load(open(A + 'logs/verify/glider100.p2.json'))
print('audit repair centre x104 =', cc.get('x104'), '; x104 basic:', 'x104' in g['B'], '; route C t =', g['t'])

print('== emfl listed points vs exact lower bound L (value + half unit < L means below)')
for n in ['emfl050_3_3', 'emfl050_5_5', 'emfl100_3_3', 'emfl100_5_5']:
    cj = json.load(open(A + f'logs/cert_socp_{n}.json'))
    L = F(cj['lower_bound_30_digits_rounded_down'].replace('e-30', '')) / 10**30
    U = F(cj['rigorous_upper_bound_from_numerical_optimum'])
    print(n, 'L', float(L), 'U(float)', float(U), 'float(L)-L = %.2g' % (float(F(cj['rigorous_lower_bound']) - L)))
    for q in P[n]['points']:
        h = F(1, 2) * F(10) ** Decimal(q['value']).as_tuple().exponent
        tag = 'below L' if F(q['value']) + h < L else ('above U' if F(q['value']) - h > U else 'undecided')
        print('   ', q['point'], q['section'], q['infeas'], q['value'], tag, 'L-v %.3g rel %.2g' % (float(L - F(q['value'])), float((L - F(q['value'])) / L)))
