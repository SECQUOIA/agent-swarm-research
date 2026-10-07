import json
from fractions import Fraction as F
R = json.load(open('results.json'))
best = {}
for r in R:
    if not r.get('cls', '').startswith('(i'):
        continue
    if r['cls'].startswith('(ii') or r['cls'].startswith('(iii'):
        continue
    sg = 1 if r['sense'] == 'min' else -1
    d = F(r['d_listed']); hi = F(str(r['obj_hi'])); lo = F(str(r['obj_lo']))
    worst = hi if sg == 1 else lo
    m = sg * (d - worst)
    s = r['d_listed'].lstrip('-')
    k = len(s.split('.')[1]) if '.' in s else 0
    u = F(1, 10**k)
    key = (r['name'], r['solver'])
    if key not in best or m > best[key][0]:
        best[key] = (m, r['point'], r['cls'][:5], r.get('i_group', ''), d, u, worst, r['d_date'])
rows = sorted(best.items(), key=lambda kv: -float(kv[1][0] / abs(kv[1][4])))
print('%-30s %-8s %-4s %-5s %-15s %-16s %-11s %-10s %-9s %s' % ('instance','solver','pt','cls','d','margin','rel|d|','units','/slack','date'))
for (n, s), (m, p, c, g, d, u, w, dt) in rows:
    print('%-30s %-8s %-4s %-5s %-15s %-16.6g %-11.4g %-10.4g %-9.4g %s %s' % (n, s, p, c, str(float(d)), float(m), float(m/abs(d)), float(m/u), float(m/(u/2)), dt, g))
ci = [v for v in best.values() if v[2] == '(i) p']
cir = [v for v in best.values() if v[2] == '(i-r)']
print('class (i) pairs', len(ci), 'instances', len({k[0] for k, v in best.items() if v[2] == '(i) p'}))
print('class (i-r) pairs', len(cir))
print('min units over (i):', float(min(v[0]/v[5] for v in ci)), ' max units over (i-r):', float(max(v[0]/v[5] for v in cir)))
print('min margin/slack over (i):', float(min(v[0]/(v[5]/2) for v in ci)))
