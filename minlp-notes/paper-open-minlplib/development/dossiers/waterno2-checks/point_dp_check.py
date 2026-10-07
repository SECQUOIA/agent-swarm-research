"""Exact consistency check of certB with the exactly feasible waterno2_06 point (dossier)."""
import json, math
from fractions import Fraction as F
import xml.etree.ElementTree as ET
import numpy as np
import osilmini, load_cs
exec(open('dp_check.py').read().split('# 3. exact DP')[0].replace("load_cs.load(sys.argv[1])", "load_cs.load('certB_cert.pkl.gz')"))
m = osilmini.read('waterno2_06.osil'); NS = osilmini.NS
V, C, R, NL = m['vars'], m['cons'], m['rows'], m['nonlin']
names = [v['name'] for v in V]; idx = {n: j for j, n in enumerate(names)}
root = ET.parse('waterno2_06.osil').getroot(); d = root.find(NS + 'instanceData')
rowvars = [set(r) for r in R]
for q in d.find(NS + 'quadraticCoefficients').findall(NS + 'qTerm'):
    rowvars[int(q.get('idx'))] |= {int(q.get('idxOne')), int(q.get('idxTwo'))}
for e in d.find(NS + 'nonlinearExpressions').findall(NS + 'nl'):
    rowvars[int(e.get('idx'))].add(int(e.find(NS + 'power').find(NS + 'variable').get('idx')))
link_names = {'e%d' % k for k in range(111, 126)}; hor = 'e56'
par = list(range(len(V)))
def find(a):
    while par[a] != a: par[a] = par[par[a]]; a = par[a]
    return a
for i, c in enumerate(C):
    if c['name'] in link_names or c['name'] == hor: continue
    vs = list(rowvars[i])
    for v in vs[1:]: par[find(v)] = find(vs[0])
ends = [['x243', 'x255', 'x267'], ['x245', 'x257', 'x269'], ['x247', 'x259', 'x271'], ['x249', 'x261', 'x273'], ['x251', 'x263', 'x275']]
starts = [['x244', 'x256', 'x268'], ['x246', 'x258', 'x270'], ['x248', 'x260', 'x272'], ['x250', 'x262', 'x274'], ['x252', 'x264', 'x276']]
comp = [find(idx['x242'])] + [find(idx[s[0]]) for s in starts]
assert len(set(comp)) == 6
pt = json.load(open('waterno2_06.exact.json'))['x']
val = lambda n: F(pt[n])
costs = [[j for j in m['obj'] if find(j) == comp[t]] for t in range(6)]
assert all(len(c) == 9 for c in costs)
# leaves containing the point's link levels
path = []
for l in range(5):
    y = [val(n) for n in ends[l]]
    assert y == [val(n) for n in starts[l]]
    hits = [a for a, i in enumerate(leaves[l]) if all(F(cells[l][i]['lo'][k]) <= y[k] <= F(cells[l][i]['hi'][k]) for k in range(3))]
    path.append(hits)
print('leaves containing the point per link:', [len(h) for h in path])
tot = F(0); fsum = F(0); minmargin = None
for t in range(6):
    cost = sum(val(names[j]) for j in costs[t]); fsum += cost
    rows_ = path[t - 1] if t > 0 else [0]; cols_ = path[t] if t < 5 else [0]
    for a in rows_:
        for c in cols_:
            lin = F(0)
            if t > 0: lin += sum(F(lam[t - 1][leaves[t - 1][a]][k]) * val(starts[t - 1][k]) for k in range(3))
            if t < 5: lin -= sum(F(lam[t][leaves[t][c]][k]) * val(ends[t][k]) for k in range(3))
            pv = cost + lin; b = pair[t][(a, c)]
            assert b is not None and b <= pv, (t, a, c)
            mg = pv - b; minmargin = mg if minmargin is None or mg < minmargin else minmargin
    a0 = rows_[0]; c0 = cols_[0]
    tot += pair[t][(a0, c0)]
print('f(point) =', float(fsum), '== stored objective:', fsum == F(json.load(open('waterno2_06.exact.json'))['objective']))
print('sum of pair bounds along the point\'s cells:', float(tot), ' smallest per-period margin:', float(minmargin))
