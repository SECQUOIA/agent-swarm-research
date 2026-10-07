import json, math
from fractions import Fraction as F
P = {r['name']: r for r in json.load(open('pages.json'))}
solu = {}
for line in open('minlplib.solu'):
    t = line.split()
    if len(t) >= 2:
        solu.setdefault(t[1], {})[t[0]] = t[2] if len(t) > 2 else None
def fr(s):
    try:
        v = float(s)
    except Exception:
        return None
    return F(s) if math.isfinite(v) else None
def kth_best(r, k):
    sg = 1 if r['sense'] == 'min' else -1
    v = sorted({fr(d['value']) for d in r['duals'] if fr(d['value']) is not None}, key=lambda x: -sg * x)
    # k-th best counting multiplicity over solvers
    allv = sorted([fr(d['value']) for d in r['duals'] if fr(d['value']) is not None], key=lambda x: -sg * x)
    return allv[k-1] if len(allv) >= k else None
def bold_duals(r):
    return [fr(d['value']) for d in r['duals'] if d['bold'] and fr(d['value']) is not None]
n = agree3 = agree_min = 0; mism = []
for name, s in solu.items():
    if '=bestdual=' not in s or name not in P:
        continue
    r = P[name]
    if r['sense'] not in ('min', 'max'):
        continue
    sg = 1 if r['sense'] == 'min' else -1
    bd = F(s['=bestdual='])
    third = kth_best(r, 3)
    pts = [fr(p['value']) for p in r['points'] if fr(p['value']) is not None]
    lowp = (min(pts) if sg == 1 else max(pts)) if pts else None
    cand = [x for x in (third, lowp) if x is not None]
    agg = (min(cand) if sg == 1 else max(cand)) if cand else None
    n += 1
    tol = lambda a, b: a is not None and abs(a - b) <= F(6, 10**9) * max(1, abs(b))
    if tol(third, bd): agree3 += 1
    if tol(agg, bd): agree_min += 1
    else: mism.append((name, str(bd), str(third), str(lowp), str(kth_best(r, 2))))
print('instances with =bestdual=:', n, '| equals third-best:', agree3, '| equals min(third-best, lowest point):', agree_min)
for m in mism: print('  mismatch', m)
