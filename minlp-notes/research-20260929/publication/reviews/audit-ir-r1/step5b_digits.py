"""Digit statistics with the definition 'first to last nonzero digit', zero and
inf excluded (the author's stated definition), from the reviewer's parse."""
import collections, json, math
import step4_pages as S
from fractions import Fraction as Q
from decimal import Decimal, ROUND_HALF_UP

pj = json.load(open(S.BA + 'pages.json'))
recs = {r['name']: r for r in pj}
vals = []
for n in sorted(recs):
    mine, _ = S.parse_page(S.PAGES + n + '.html')
    for q in mine['points']:
        vals.append(('point', n, q['point'], q['value'], q['added'], mine['sense'], q['infeas']))
    for d in mine['duals']:
        vals.append(('dual', n, d['solver'], d['value'], d['date'], mine['sense'], None))


def sig_nz(v):
    s = v.lstrip('+-').replace('.', '').strip('0')
    return len(s)


def sig_all(v):
    return len(v.lstrip('+-').replace('.', '').lstrip('0'))


fin = [t for t in vals if 'inf' not in t[3]]
nz = [t for t in fin if Q(t[3]) != 0]
h = collections.defaultdict(collections.Counter)
for t in nz:
    if t[0] == 'point':
        key = 'points'
    else:
        if t[5] not in ('min', 'max'):
            key = 'duals on pages without sense'
        else:
            key = 'duals 17 Sep 2013' if t[4] == '17 Sep 2013' else 'other duals'
    h[key][sig_nz(t[3])] += 1
for k, v in h.items():
    print(k, 'n=%d' % sum(v.values()), '6-digit %d, 7-digit %d' % (v[6], v[7]), dict(sorted(v.items())))
o11 = [t for t in fin if sig_nz(t[3]) > 10]
o11all = [t for t in fin if sig_all(t[3]) > 10]
print('>10 digits (first-to-last nonzero):', len(o11), ' (counting trailing integer zeros):', len(o11all))
print('  max', max(sig_nz(t[3]) for t in o11), max(sig_all(t[3]) for t in o11all))
print('  only in the second count:', sorted({(t[1], t[3]) for t in o11all} - {(t[1], t[3]) for t in o11}))
print('  first-to-last list:', sorted({(t[1], t[3]) for t in o11}))
# the 7 (i-r) values equal the best listed point rounded half-up to 6 sig digits
def round_sig(v, n):
    d = Decimal(v)
    return d.quantize(Decimal(1).scaleb(d.adjusted() - n + 1), rounding=ROUND_HALF_UP)
for n, solv in [('eniplac', 'COUENNE'), ('eniplac', 'LINDO'), ('eniplac', 'SCIP'), ('lop97icx', 'ANTIGONE'),
                ('stockcycle', 'ANTIGONE'), ('stockcycle', 'BARON'), ('stockcycle', 'COUENNE')]:
    d = [t for t in vals if t[1] == n and t[0] == 'dual' and t[2] == solv][0]
    best = [t for t in vals if t[1] == n and t[0] == 'point'][0]   # first listed = bold best
    print(n, solv, d[3], 'best point', best[2], best[3], 'rounded to 6:', round_sig(best[3], 6), Decimal(d[3]) == round_sig(best[3], 6))
