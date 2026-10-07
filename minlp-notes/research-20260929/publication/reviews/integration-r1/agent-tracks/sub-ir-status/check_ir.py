"""Own checks of (i-r) pairs, 6-digit entry dates, rounding, display counts.
Reads bound-audit/results.json and pages.json only (json parsing, Fractions)."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[6])

import json, collections, re
from fractions import Fraction as Q
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
B = (_PUBLIC_REPO + '/research-20260929/bound-audit/')
res = json.load(open(B + 'results.json'))
pages = json.load(open(B + 'pages.json'))

def sig(s):
    s = s.strip().lstrip('-+').replace('−', '')
    d = s.replace('.', '').lstrip('0').rstrip('0')
    return len(d)

print('classes:', collections.Counter(r['cls'] for r in res))
ir = [r for r in res if r['cls'].startswith('(i-r)')]
print('(i-r) rows:', len(ir))
pairs = sorted({(r['name'], r['solver'], r['d_listed'], r['d_date']) for r in ir})
print('(i-r) distinct pairs:', len(pairs))
for p in pairs: print('  ', p, 'sig digits', sig(p[2]))
byinst = collections.defaultdict(list)
for n, s, _, _ in pairs: byinst[n].append(s)
print({k: v for k, v in byinst.items()})

# spring rounding: proven optimum lower/upper (25 decimals from audit-ir)
fstar = Decimal('0.84624566564315428125166463503714129527532857794010')
print('spring f* rounded to 8 decimals:', fstar.quantize(Decimal('1e-8'), ROUND_HALF_UP))

# six-sig-digit entries: round each instance's best listed point and proven f to 6 sig digits
def round_sig(x, n):
    x = Decimal(x)
    e = x.adjusted() - n + 1
    return x.quantize(Decimal(1).scaleb(e), ROUND_HALF_UP)
pg = {p['name']: p for p in pages}
ex = {r['name']: r['obj_eval'] for r in ir}
for n in ['eniplac', 'lop97icx', 'stockcycle']:
    p = pg[n]
    best = min(Decimal(q['value']) for q in p['points'])
    print(n, 'best point', best, '->6sig', round_sig(best, 6), '| proven f', ex[n][:20], '->6sig', round_sig(ex[n], 6),
          '| listed', {r['d_listed'] for r in ir if r['name'] == n})

# all 6-sig-digit duals involved in the audit (results.json rows), with dates
six = collections.Counter((r['name'], r['solver'], r['d_listed'], r['d_date'], r['cls']) for r in res if sig(r['d_listed']) == 6)
print('6-sig-digit duals in results.json rows (distinct pairs):', len(six))
for k in sorted(six): print('  ', k)
print('dates of those:', collections.Counter(k[3] for k in six))
print('dates of all <=6-sig duals in results.json:', collections.Counter((sig(r['d_listed']), r['d_date']) for r in res if sig(r['d_listed']) <= 6))

# display precision recount from pages.json values (duals + points + listing fields)
vals = []
for p in pages:
    for q in p['duals']: vals.append(('dual', p['name'], q['value']))
    for q in p['points']: vals.append(('point', p['name'], q['value']))
    for f in ('listing_dual', 'listing_primal'):
        if p.get(f): vals.append((f, p['name'], p[f]))
num = re.compile(r'^[-−]?\d+\.?\d*(e[-+]?\d+)?$', re.I)
fin = [v for v in vals if num.match(v[2].strip())]
print('values total', len(vals), 'numeric', len(fin))
maxdec = max(len(v[2].split('.')[1]) if '.' in v[2] else 0 for v in fin)
print('max decimals:', maxdec)
def sig_nz(s):
    s = s.lstrip('-−')
    d = s.replace('.', '').lstrip('0').rstrip('0'); return len(d)
def sig_tz(s):
    s = s.lstrip('-−')
    ip, _, fp = s.partition('.')
    d = (ip + fp).lstrip('0')
    fp2 = fp.rstrip('0')
    d = (ip + fp2).lstrip('0') if fp2 else ip.lstrip('0')
    return len(d)
for label, sub in [('duals+points', [v for v in fin if v[0] in ('dual', 'point')]), ('incl listing', fin)]:
    a = [v for v in sub if '.' in v[2] and v[2].split('.')[1].rstrip('0') and sig_nz(v[2]) > 10]
    b = [v for v in sub if sig_nz(v[2]) > 10]
    c = [v for v in sub if sig_tz(v[2]) > 10]
    print(label, 'A frac>10:', len(a), 'distinct', len({v[2] for v in a}), 'range', min(map(lambda v: sig_nz(v[2]), a)), max(map(lambda v: sig_nz(v[2]), a)))
    print(label, 'B nofilter>10:', len(b), 'range', min(sig_nz(v[2]) for v in b), max(sig_nz(v[2]) for v in b))
    print(label, 'C trailing int zeros>10:', len(c), 'range', min(sig_tz(v[2]) for v in c), max(sig_tz(v[2]) for v in c))
    print('   C-B extras:', sorted({v[2] for v in c} - {v[2] for v in b}))
    print('   B-A extras:', sorted({(v[1], v[2]) for v in b} - {(v[1], v[2]) for v in a}))
    print('   instances of A:', sorted({v[1] for v in a}))
