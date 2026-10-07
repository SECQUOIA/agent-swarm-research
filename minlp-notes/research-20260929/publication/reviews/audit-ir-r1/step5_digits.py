"""Digit statistics of the displayed values, from the reviewer's own parse."""
import collections
import json
import math
import re
import step4_pages as S

BA = S.BA
pj = json.load(open(BA + 'pages.json'))
names = sorted(r['name'] for r in pj)
vals = []  # (kind, name, label, value string, date)
for n in names:
    mine, _ = S.parse_page(S.PAGES + n + '.html')
    for q in mine['points']:
        vals.append(('point', n, q['point'], q['value'], q['added']))
    for d in mine['duals']:
        vals.append(('dual', n, d['solver'], d['value'], d['date']))


def finite(v):
    try:
        return math.isfinite(float(v))
    except ValueError:
        return False


def sig(v):
    s = v.lstrip('+-')
    if 'e' in s.lower():
        raise ValueError(v)
    s = s.replace('.', '').lstrip('0')
    return len(s)


def decs(v):
    return len(v.split('.', 1)[1]) if '.' in v else 0


fin = [t for t in vals if finite(t[3])]
nonfin = collections.Counter(t[3] for t in vals if not finite(t[3]))
print('values', len(vals), 'finite', len(fin), 'non-finite', dict(nonfin))
print('any exponent notation:', sum('e' in t[3].lower() for t in fin))
print('max decimals:', max(decs(t[3]) for t in fin))
over10 = [t for t in fin if sig(t[3]) > 10]
print('values with > 10 significant digits:', len(over10), 'range', min(map(lambda t: sig(t[3]), over10)), max(map(lambda t: sig(t[3]), over10)))
print('  examples:', [(t[1], t[2], t[3]) for t in over10 if t[1] in ('optcdeg2', 'fac1')])
print('  instances:', sorted({t[1] for t in over10}))
# 6 vs 7 significant digits
def bucket(sel):
    c = collections.Counter(sig(t[3]) for t in sel)
    return c[6], c[7]
d17 = [t for t in fin if t[0] == 'dual' and t[4] == '17 Sep 2013']
dother = [t for t in fin if t[0] == 'dual' and t[4] != '17 Sep 2013']
pts = [t for t in fin if t[0] == 'point']
print('duals dated 17 Sep 2013: n=%d, 6-digit %d, 7-digit %d' % ((len(d17),) + bucket(d17)))
print('other duals: n=%d, 6-digit %d, 7-digit %d' % ((len(dother),) + bucket(dother)))
print('points: n=%d, 6-digit %d, 7-digit %d' % ((len(pts),) + bucket(pts)))
# which entries in d17 have >= 7 digits
print('17 Sep 2013 duals with sig >= 7:', [(t[1], t[2], t[3]) for t in d17 if sig(t[3]) >= 7][:10])
print('17 Sep 2013 sig distribution:', sorted(collections.Counter(sig(t[3]) for t in d17).items()))
# date distribution of the (i-r) entries
for n in ('eniplac', 'lop97icx', 'stockcycle', 'spring'):
    print(n, [(t[2], t[3], t[4]) for t in vals if t[1] == n])
