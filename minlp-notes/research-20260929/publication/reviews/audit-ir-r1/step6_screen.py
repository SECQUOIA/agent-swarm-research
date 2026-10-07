"""Recompute the audit's screen from the reviewer's own parse and compare with
screen.json and results.json."""
import json
from fractions import Fraction as Q
import step4_pages as S

pj = json.load(open(S.BA + 'pages.json'))
names = sorted(r['name'] for r in pj)
flag, ties = set(), set()
for n in names:
    mine, _ = S.parse_page(S.PAGES + n + '.html')
    if mine['sense'] not in ('min', 'max'):
        continue
    for q in mine['points']:
        if Q(q['infeas']) > Q('1e-5'):
            continue
        p = Q(q['value'])
        for d in mine['duals']:
            if 'inf' in d['value']:
                continue
            dv = Q(d['value'])
            beyond = dv > p if mine['sense'] == 'min' else dv < p
            if beyond:
                flag.add((n, q['point'], d['solver']))
            elif dv == p:
                ties.add((n, q['point'], d['solver']))
# skipped high-infeas points beyond a dual?
hi = 0
for n in names:
    mine, _ = S.parse_page(S.PAGES + n + '.html')
    if mine['sense'] not in ('min', 'max'):
        continue
    for q in mine['points']:
        if Q(q['infeas']) > Q('1e-5'):
            p = Q(q['value'])
            for d in mine['duals']:
                if 'inf' in d['value']:
                    continue
                dv = Q(d['value'])
                if (dv > p if mine['sense'] == 'min' else dv < p):
                    hi += 1
print('flagged pairs', len(flag), 'instances', len({f[0] for f in flag}), 'points', len({f[:2] for f in flag}),
      '(instance, solver)', len({(f[0], f[2]) for f in flag}))
print('ties', len(ties), 'instances', len({t[0] for t in ties}))
print('pairs with infeas > 1e-5 points beyond a dual:', hi)
res = json.load(open(S.BA + 'results.json'))
rset = {(r['name'], r['point'], r['solver']) for r in res}
print('same set as results.json:', rset == flag)
sc = json.load(open(S.BA + 'screen.json'))
print('screen.json type', type(sc), list(sc.keys())[:10] if isinstance(sc, dict) else len(sc))
t0 = sc['ties'][0]
print('screen.json tie example', t0)
def key(t):
    return (t.get('name'), t.get('point'), t.get('solver'))
sty = {key(t) for t in sc['ties']}
spr = {key(t) for t in sc['pairs']}
print('ties equal screen.json:', sty == ties, 'pairs equal screen.json:', spr == flag)
# >10-digit values: any in a flagged pair?
big = set()
for n in names:
    mine, _ = S.parse_page(S.PAGES + n + '.html')
    for q in mine['points']:
        if len(q['value'].lstrip('+-').replace('.', '').strip('0')) > 10:
            big.add((n, 'pt', q['point']))
    for d in mine['duals']:
        if 'inf' not in d['value'] and len(d['value'].lstrip('+-').replace('.', '').lstrip('0')) > 10:
            big.add((n, 'du', d['solver']))
    for q in mine['points']:
        if len(q['value'].lstrip('+-').replace('.', '').lstrip('0')) > 10:
            big.add((n, 'pt', q['point']))
inflag = [b for b in big if any((b[0] == f[0] and ((b[1] == 'pt' and b[2] == f[1]) or (b[1] == 'du' and b[2] == f[2]))) for f in flag)]
intie = sorted({b[0] for b in big if any((b[0] == f[0] and ((b[1] == 'pt' and b[2] == f[1]) or (b[1] == 'du' and b[2] == f[2]))) for f in ties)})
print('>10-digit values (either definition) in flagged pairs:', inflag)
print('instances where a >10-digit value is in a tie:', intie)
