"""How many digits do the listed dual bounds carry? (evidence on the
rounding slack of class (i-r); not a proof)

From the re-parsed pages: histograms of the number of significant digits
(first to last nonzero digit) of listed dual bounds dated 17 Sep 2013, of
the other dual bounds and of the listed points; and the short dual bounds
(at most 6 significant digits) that equal a listed point value (infeas <=
1e-5, same page) rounded half-up to the same number of significant digits,
where the point shows more digits.
"""
import collections
import glob
import json
import os
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as Q

import parse_check as pc

HERE = os.path.dirname(os.path.abspath(__file__))
mine = {}
for f in sorted(glob.glob(os.path.join(pc.PAGES, '*.html'))):
    if not f.endswith('instances.html'):
        p = pc.parse_page(f)
        mine[p['name']] = p


def round_sig(v, n):
    d = Decimal(v)
    return d.quantize(Decimal(1).scaleb(d.adjusted() - n + 1), rounding=ROUND_HALF_UP)


hist = collections.defaultdict(collections.Counter)
match = collections.Counter()
examples = collections.defaultdict(list)
for p in mine.values():
    for x in p['points']:
        if Q(x['value']) != 0:
            hist['points'][pc.sig_digits(x['value'])[0]] += 1
    if p['sense'] not in ('min', 'max'):
        continue
    pts = [x for x in p['points'] if Q(x['infeas']) <= Q('1e-5')]
    for d in p['duals']:
        v = d['value']
        if 'inf' in v or Q(v) == 0:
            continue
        s = pc.sig_digits(v)[0]
        key = 'duals dated 17 Sep 2013' if d['date'] == '17 Sep 2013' else 'other duals'
        hist[key][s] += 1
        if s <= 6:
            hit = [x for x in pts if pc.sig_digits(x['value'])[0] > s
                   and Decimal(v) == round_sig(x['value'], s)]
            match['%s, %d digits, equals rounded point: %s' % (key, s, bool(hit))] += 1
            if hit:
                examples[key].append((p['name'], d['solver'], d['date'], v, hit[0]['value']))
out = dict(histograms={k: dict(sorted(v.items())) for k, v in hist.items()},
           short_duals=dict(sorted(match.items())), examples=dict(examples))
json.dump(out, open(os.path.join(HERE, 'logs', 'digits_check.json'), 'w'), indent=1)
for k, v in out['histograms'].items():
    print(k, v)
for k, v in out['short_duals'].items():
    print(k, v)
for k, v in out['examples'].items():
    print(k, len(v))
    for e in v:
        print('   ', e)
