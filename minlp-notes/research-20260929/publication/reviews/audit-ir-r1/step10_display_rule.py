"""Evidence on the page display rule: is every displayed finite value a fixed
point of  disp(v) = ('%.8f' % round(v, 10 - k)).rstrip('0'),  k = number of
integer digits of |v| (floating point, as a display program would do)?"""
import json, math
import step4_pages as S

def disp(v):
    if v == 0:
        return '0.'
    k = math.floor(math.log10(abs(v))) + 1
    r = round(v, 10 - k)
    return ('%.8f' % r).rstrip('0')

pj = json.load(open(S.BA + 'pages.json'))
tot = ok = 0
bad = []
for n in sorted(r['name'] for r in pj):
    mine, _ = S.parse_page(S.PAGES + n + '.html')
    for v in [q['value'] for q in mine['points']] + [d['value'] for d in mine['duals']]:
        if 'inf' in v:
            continue
        tot += 1
        if disp(float(v)) == v:
            ok += 1
        else:
            bad.append((n, v, disp(float(v))))
print('finite values', tot, 'fixed points of the rule', ok)
print('non-fixed examples', bad[:10], len(bad))
for v in [160912612.4, -132117.08301998901, 4099.0599536, 0.8462456656431543, 119948.68833333, -9.999999981e19]:
    print(v, '->', disp(v))
nz = [b for b in bad if b[1] not in ('-0.', '0.')]
print(len(bad), 'non-fixed;', len(bad) - len(nz), 'are -0. ; others:', nz)
