# Independent recount from a copy of pages.json, exact decimal arithmetic (Fraction).
import json, math
from fractions import Fraction
from collections import Counter
P = json.load(open('pages.json'))
def fr(s):
    try:
        v = float(s)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(v):
        return None
    return Fraction(s)
npts = sum(len(r['points']) for r in P)
nd = sum(len(r['duals']) for r in P)
ndf = sum(1 for r in P for d in r['duals'] if fr(d['value']) is not None)
senses = Counter(r['sense'] for r in P)
solvers = Counter(d['solver'] for r in P for d in r['duals'])
print('pages', len(P), 'points', npts, 'duals', nd, 'finite duals', ndf, 'labels', len(solvers))
print('senses', dict(senses))
pairs, ties, skipped_beyond = [], [], 0
for r in P:
    if r['sense'] not in ('min', 'max'):
        continue
    sg = 1 if r['sense'] == 'min' else -1
    for p in r['points']:
        pv = fr(p['value'])
        if pv is None:
            continue
        inf = fr(p['infeas'])
        for d in r['duals']:
            dv = fr(d['value'])
            if dv is None:
                continue
            beyond = sg * (dv - pv) > 0
            if inf is not None and inf > Fraction('1e-5'):
                skipped_beyond += beyond
                continue
            if beyond:
                pairs.append((r['name'], p['point'], d['solver'], p['section']))
            elif dv == pv:
                ties.append((r['name'], p['point'], d['solver']))
print('screen pairs', len(pairs), 'instances', len({x[0] for x in pairs}), 'points', len({x[:2] for x in pairs}),
      'other-section pairs', sum(1 for x in pairs if x[3] != 'primal'),
      '(instance,solver)', len({(x[0], x[2]) for x in pairs}))
print('ties', len(ties), 'instances', len({x[0] for x in ties}))
print('beyond-dual pairs skipped for infeas > 1e-5:', skipped_beyond)
S = json.load(open('screen.json'))
a = {(x['name'], x['point'], x['solver']) for x in S['pairs']}
b = {x[:3] for x in pairs}
print('screen.json pair set equal:', a == b, '| tie count in screen.json', len(S['ties']))
