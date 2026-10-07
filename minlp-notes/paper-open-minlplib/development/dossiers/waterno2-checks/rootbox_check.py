import json
from fractions import Fraction as F
import osilmini, load_cs
m = osilmini.read('waterno2_06.osil')
V, C, R, NL = m['vars'], m['cons'], m['rows'], m['nonlin']
name = [v['name'] for v in V]
tank = {F(1800): 0, F(720): 1, F(1600): 2}
L, E = {}, {}  # var index -> tank
for i, c in enumerate(C):
    if i in NL: continue
    r = R[i]
    vals = sorted(r.values())
    if len(r) == 4 and F(3600) in vals and F(-3600) in vals and c['lb'] == 0 == c['ub']:
        for j, v in r.items():
            if abs(v) != 3600:
                (L if v > 0 else E)[j] = tank[abs(v)]
links = []
for i, c in enumerate(C):
    if i in NL: continue
    r = R[i]
    if len(r) == 2 and sorted(r.values()) == [-1, 1] and c['lb'] == 0 == c['ub']:
        a, b = list(r)
        if (a in E and b in L) or (a in L and b in E):
            e, s = (a, b) if a in E else (b, a)
            assert E[e] == L[s]
            links.append((e, s, E[e], C[i]['name']))
print('link rows:', len(links))
# period of each variable: union of balance rows sharing? use the fixed start levels to order
fixed_L = [j for j in L if V[j]['lb'] == V[j]['ub']]
print('fixed start levels:', [(name[j], str(V[j]['lb'])) for j in fixed_L])
# chain: period 0 end vars are E vars in same balance rows as fixed L vars
bal_rows = [i for i, c in enumerate(C) if i not in NL and len(R[i]) == 4 and any(j in L for j in R[i]) and any(j in E for j in R[i])]
LtoE = {}
for i in bal_rows:
    l = [j for j in R[i] if j in L][0]; e = [j for j in R[i] if j in E][0]; LtoE[l] = e
EtoL = {e: s for e, s, k, nm in links}
cur = sorted(fixed_L, key=lambda j: L[j])
imp = json.load(open('my_implied_06.json'))
st = load_cs.load('certB_cert.pkl.gz')
for l in range(5):
    ends = [LtoE[j] for j in cur]; starts = [EtoL[e] for e in ends]
    box_lo, box_hi = [], []
    for e, s in zip(ends, starts):
        lo = max(F(x) for x in [V[e]['lb'], V[s]['lb']] + [F(imp[n][0]) for n in (name[e], name[s]) if n in imp])
        hi = min(F(x) for x in [V[e]['ub'], V[s]['ub']] + [F(imp[n][1]) for n in (name[e], name[s]) if n in imp])
        box_lo.append(lo); box_hi.append(hi)
    root = st['cells'][l][0]
    ok = all(F(root['lo'][k]) <= box_lo[k] and box_hi[k] <= F(root['hi'][k]) for k in range(3))
    print(f'link {l}: ends {[name[e] for e in ends]} starts {[name[s] for s in starts]} box lo {[float(x) for x in box_lo]} hi {[float(x) for x in box_hi]} root contains box: {ok}')
    cur = starts
