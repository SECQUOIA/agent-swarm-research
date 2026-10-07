"""Dossier check (exact): the exactly feasible waterno2 points against
(a) every implied-bound file used by the certificates, and
(b) the wave-2 period-Lagrangian certificates: each stored period bound B_t must be
    <= the exact period-Lagrangian value of the point's restriction to period t.
Also: period structure recovered independently (horizon row, copy rows, balance rows,
link rows oriented by the sign of the area coefficient), and counts of cube variables
that sit at a lower bound whose cube identity fails in binary64.
usage: python3 point_consistency.py T   (files in the current directory)"""
import json, sys
from fractions import Fraction as F
import xml.etree.ElementTree as ET
import osilmini

T = int(sys.argv[1]); TT = '%02d' % T
m = osilmini.read(f'waterno2_{TT}.osil'); NS = osilmini.NS
V, C, R, NL = m['vars'], m['cons'], m['rows'], m['nonlin']
names = [v['name'] for v in V]; idx = {n: j for j, n in enumerate(names)}
d = ET.parse(f'waterno2_{TT}.osil').getroot().find(NS + 'instanceData')
rowvars = [set(r) for r in R]
for q in d.find(NS + 'quadraticCoefficients').findall(NS + 'qTerm'):
    rowvars[int(q.get('idx'))] |= {int(q.get('idxOne')), int(q.get('idxTwo'))}
cubes = []  # (row, var) for power-3 terms
for e in d.find(NS + 'nonlinearExpressions').findall(NS + 'nl'):
    p = e.find(NS + 'power'); v = int(p.find(NS + 'variable').get('idx'))
    rowvars[int(e.get('idx'))].add(v)
    if F(p.find(NS + 'number').get('value')) == 3: cubes.append((int(e.get('idx')), v))

lin = [i for i in range(len(C)) if i not in NL]
hor = [i for i in lin if C[i]['lb'] is not None and C[i]['lb'] > 0 and C[i]['ub'] is None
       and len(R[i]) == T and all(v == 1 for v in R[i].values())]
assert len(hor) == 1; hor = hor[0]
copy = [i for i in lin if len(R[i]) == 2 and sorted(R[i].values()) == [-1, 1] and C[i]['lb'] == 0 and C[i]['ub'] == 0]
AREA = {F(1800): 0, F(720): 1, F(1600): 2}
bal = {}  # var -> (tank, sign of area coefficient)
for i in lin:
    r = R[i]
    if len(r) == 4 and C[i]['lb'] == 0 == C[i]['ub'] and F(3600) in r.values() and F(-3600) in r.values():
        for j, v in r.items():
            if abs(v) != 3600: bal[j] = (AREA[abs(v)], 1 if v > 0 else -1)
# cores: union-find over all rows except the horizon row and copy rows
par = list(range(len(V)))
def find(a):
    while par[a] != a: par[a] = par[par[a]]; a = par[a]
    return a
skip = set(copy) | {hor}
for i in range(len(C)):
    if i in skip: continue
    vs = sorted(rowvars[i])
    for v in vs[1:]: par[find(v)] = find(vs[0])
core_size = {}
for j in range(len(V)): core_size[find(j)] = core_size.get(find(j), 0) + 1
big = {k for k, s in core_size.items() if s > 1}
assert len(big) == T, (len(big), sorted(core_size.values())[-T - 2:])
links = []
for i in copy:
    a, b = list(R[i]); ca, cb = find(a), find(b)
    if ca in big and cb in big and ca != cb:
        links.append(i)
    else:  # attach singleton to its core
        if ca in big and cb not in big: par[cb] = ca
        elif cb in big and ca not in big: par[ca] = cb
        elif ca not in big and cb not in big: par[ca] = cb
assert len(links) == 3 * (T - 1), len(links)
# orient links: end var has negative area coefficient, start var positive
L = []  # (core_end, core_start, tank, end_var, start_var)
for i in links:
    a, b = list(R[i])
    (ta, sa), (tb, sb) = bal[a], bal[b]
    assert ta == tb and sa == -sb
    e, s = (a, b) if sa < 0 else (b, a)
    L.append((find(e), find(s), ta, e, s))
nxt = {}
for ce, cs, k, e, s in L: nxt.setdefault(ce, set()).add(cs)
assert all(len(v) == 1 for v in nxt.values())
first = [c for c in big if c not in {cs for _, cs, _, _, _ in L}]
assert len(first) == 1
order = [first[0]]
while order[-1] in nxt: order.append(next(iter(nxt[order[-1]])))
assert len(order) == T
pos = {c: t for t, c in enumerate(order)}
ends = [[None] * 3 for _ in range(T - 1)]; starts = [[None] * 3 for _ in range(T - 1)]
for ce, cs, k, e, s in L:
    t = pos[ce]; assert pos[cs] == t + 1
    ends[t][k] = e; starts[t][k] = s
hvar = [None] * T
for j in R[hor]: hvar[pos[find(j)]] = j
costs = [[j for j in m['obj'] if find(j) == order[t]] for t in range(T)]
assert all(len(c) == 9 for c in costs) and all(h is not None for h in hvar)
print(f'T={T}: structure: {T} periods, {len(links)} link rows, horizon row {C[hor]["name"]}; link 0 ends',
      [names[j] for j in ends[0]], 'starts', [names[j] for j in starts[0]])

# --- point values (exact rational, or enclosure c0 + c1*[lo, hi] for quadratic irrationals)
pt = json.load(open(f'waterno2_{TT}.exact.json'))
sym = {int(k): (F(v['lo']), F(v['hi'])) for k, v in pt['symbols'].items()}
def enc(n):
    v = pt['x'][n]
    if isinstance(v, str): return F(v), F(v)
    lo, hi = sym[v['w']]; c0, c1 = F(v['c0']), F(v['c1'])
    a, b = c0 + c1 * lo, c0 + c1 * hi
    return min(a, b), max(a, b)
def exact(n):
    lo, hi = enc(n); assert lo == hi, n; return lo

# (a) implied bounds
def check_box(path, getter):
    raw = json.load(open(path)); b = raw['bounds'] if 'bounds' in raw else raw
    n_ok = n_viol = n_undec = 0; tight = 0
    for n, (blo, bhi) in b.items():
        blo, bhi = getter(blo), getter(bhi)
        lo, hi = enc(n)
        ok_lo = blo is None or blo <= lo; ok_hi = bhi is None or hi <= bhi
        bad = (blo is not None and hi < blo) or (bhi is not None and lo > bhi)
        if ok_lo and ok_hi: n_ok += 1
        elif bad: n_viol += 1; print('  VIOLATION', path, n, float(lo), float(blo or 0), float(bhi or 0))
        else: n_undec += 1; print('  undecided', path, n)
        if (blo is not None and lo - blo < F(1, 10**9)) or (bhi is not None and bhi - hi < F(1, 10**9)): tight += 1
    print(f'  implied {path}: {len(b)} bounded variables, satisfied {n_ok}, violated {n_viol}, undecided {n_undec}, within 1e-9 of a bound {tight}')
def num(s):
    s = str(s)
    if s in ('inf', '-inf', 'Infinity', '-Infinity', 'nan'): return None
    return F(float(s))
import os
for p in [f'implied_{TT}.json', f'my_implied_{TT}.json']:
    if os.path.exists(p): check_box(p, num)

# (b) wave-2 period Lagrangian
cert = json.load(open(f'cert_{TT}_w1_impl.json'))
lam = [[F(float(s)) for s in row] for row in cert['lam']]; mu = F(float(cert['mu']))
assert mu >= 0 and len(lam) == T - 1
c_rhs = C[hor]['lb']
B = [None] * T
for r in cert['results']:
    assert r['t1'] == r['t0'] + 1 and r['status'] == 'certified'; B[r['t0']] = F(r['bound'])
f = sum(exact(names[j]) for t in range(T) for j in costs[t])
assert f == F(pt['objective'])
tot = mu * c_rhs; margins = []
for t in range(T):
    val = sum(exact(names[j]) for j in costs[t]) - mu * exact(names[hvar[t]])
    if t > 0: val += sum(lam[t - 1][k] * exact(names[starts[t - 1][k]]) for k in range(3))
    if t < T - 1: val -= sum(lam[t][k] * exact(names[ends[t][k]]) for k in range(3))
    assert val >= B[t], ('VIOLATION', t, float(val), float(B[t]))
    margins.append(val - B[t]); tot += val
slack = sum(exact(names[h]) for h in hvar) - c_rhs
assert tot == f - mu * slack   # link residuals are exactly zero at the point
cb = F(cert['certified_bound_exact'])
assert cb == mu * c_rhs + sum(B)
print(f'  wave-2 Lagrangian: all {T} period values >= stored B_t; smallest margin {float(min(margins)):.6g} (period {margins.index(min(margins))}),'
      f' largest {float(max(margins)):.6g} (period {margins.index(max(margins))})')
print(f'  f(x) = {float(f):.9f}; mu*c + sum_t L_t(x) = {float(tot):.9f}; horizon slack sum h - c = {float(slack):.3g} (mu*slack = {float(mu*slack):.6g})')
print(f'  gap f - bound = {float(f - cb):.6f} = sum of margins {float(sum(margins)):.6f} + mu*slack {float(mu*slack):.6f}')
print('  per-period margins:', ' '.join('%.4f' % float(x) for x in margins))

# (c) cube variables at a lower bound whose identity fails in binary64
n_at = n_bin_fail = 0
for i, v in cubes:
    others = [j for j in R[i]]  # linear part: -w
    assert len(others) == 1; w = others[0]
    lw = V[w]['lb']; lv = V[v]['lb']
    if lw is None or lv is None: continue
    xv = enc(names[v]); xw = enc(names[w])
    if xw[0] == xw[1] == lw and xv[0] == xv[1] == lv:
        n_at += 1
        if F(float(lv)) ** 3 != F(float(lw)): n_bin_fail += 1
print(f'  cube rows with both variables at their lower bounds: {n_at}; of these, binary64 cube identity fails: {n_bin_fail}')
