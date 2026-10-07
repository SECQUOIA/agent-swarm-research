"""Reviewer check (lit-small r1, numerical evidence, floating point):
optimum of the INTEGER version (x_i in {0,...,10}) of MINLPLib pricing050,
to test the author's claim that it equals 1825 (Davarnia & van Hoeve 2021,
Table 6.1, n = 50, instance #2).

Own parser of the MINLPLib .gms file (not the author's code). The parsed rows
are cross-checked against pyscipopt's reading of the cached OSIL at random
points. The integer problem is solved as a MILP with one binary per
(product, value) and HiGHS (scipy.optimize.milp).
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import re, os, math, random, sys
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

GMS = (_PUBLIC_REPO + '/research-20260929/publication/literature/small/sources/minlplib_gms/pricing050.gms')
OSIL = os.path.expanduser('~/.cache/minlplib/minlplib/osil/pricing050.osil')
txt = open(GMS).read()
body = txt[txt.index('e1..'):]
eqs = {}
for m in re.finditer(r'(e\d+)\.\.(.*?);', body, flags=re.S):
    eqs[m.group(1)] = re.sub(r'\s+', '', m.group(2))
# objective row e1: -sum c_i x_i - objvar =E= 0  (maximize objvar => minimize sum c x)
e1 = eqs['e1']
lhs = e1.split('=E=')[0]
c = {}
for m in re.finditer(r'([+-])(?:(\d+(?:\.\d+)?)\*)?x(\d+)', lhs):
    s = -1.0 if m.group(1) == '-' else 1.0
    a = float(m.group(2)) if m.group(2) else 1.0
    c[int(m.group(3))] = -s * a        # min-form cost
idx = list(range(2, 52))
rows = []
for name in ['e2', 'e3', 'e4', 'e5', 'e6']:
    lhs, rhs = eqs[name].split('=L=')
    terms = []
    pat = re.compile(r'([+-])(?:(\d+(?:\.\d+)?)\*)?x(\d+)\*exp\(-(\d+(?:\.\d+)?)\*(power\(x(\d+),(\d+)\)|sqr\(x(\d+)\)|x(\d+))\)')
    pos = 0
    for m in pat.finditer(lhs):
        assert m.start() == pos, (name, lhs[pos:m.start()+40])
        pos = m.end()
        s = -1.0 if m.group(1) == '-' else 1.0
        a = float(m.group(2)) if m.group(2) else 1.0
        i = int(m.group(3)); cc = float(m.group(4))
        if m.group(6): j, k = int(m.group(6)), int(m.group(7))
        elif m.group(8): j, k = int(m.group(8)), 2
        else: j, k = int(m.group(9)), 1
        assert i == j
        terms.append((i, -s * a, cc, k))     # profit term a*x*exp(-cc*x^k), row: sum >= b
    assert pos == len(lhs), (name, lhs[pos:pos+60])
    rows.append((name, terms, -float(rhs)))
print('cost vars', len(c), 'rows', [(r[0], len(r[1]), r[2]) for r in rows])
print('k values', sorted(set(t[3] for r in rows for t in r[1])), 'exp coefs', sorted(set(t[2] for r in rows for t in r[1])))

def G(t, x):
    i, a, cc, k = t
    return a * x * math.exp(-cc * x ** k)

# cross-check against the reviewer OSIL evaluator (osil_eval.py, mpmath) on the cached OSIL
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from osil_eval import Model
from mpmath import mpf
om = Model(OSIL)
names = [v['name'] for v in om.vars]
assert om.sense == 'max' and all(v['lb'] == '0' and v['ub'] == '10' for v in om.vars)
assert {int(n[1:]): -float(om.obj_lin.get(k, 0)) for k, n in enumerate(names)} == {i: c.get(i, 0.0) for i in idx}
random.seed(3)
worst = 0.0
for trial in range(5):
    pt = {i: random.uniform(0, 10) for i in idx}
    xo = [mpf(pt[int(n[1:])]) for n in names]
    for r, con in enumerate(om.cons):
        rr = [q for q in rows if q[0] == con['name']][0]
        assert float(con['ub']) == -rr[2]
        mine = sum(G(t, pt[t[0]]) for t in rr[1])
        worst = max(worst, abs(float(om.body(r, xo)) + mine) / (1 + abs(mine)))
print('max rel diff of parsed rows vs OSIL rows at 5 random points: %.2e' % worst)

# MILP: y_{i,v} binary, v = 0..10, sum_v y_{i,v} = 1
vals = list(range(11))
nv = len(idx) * len(vals)
col = {(i, v): n for n, (i, v) in enumerate((i, v) for i in idx for v in vals)}
obj = np.zeros(nv)
for (i, v), n in col.items(): obj[n] = c.get(i, 0.0) * v
A = []; lb = []; ub = []
for i in idx:
    r = np.zeros(nv)
    for v in vals: r[col[(i, v)]] = 1
    A.append(r); lb.append(1); ub.append(1)
for name, terms, b in rows:
    r = np.zeros(nv)
    for t in terms:
        for v in vals: r[col[(t[0], v)]] += G(t, v)
    A.append(r); lb.append(b); ub.append(np.inf)
res = milp(obj, constraints=LinearConstraint(np.array(A), lb, ub), integrality=np.ones(nv),
           bounds=Bounds(0, 1), options={'mip_rel_gap': 0, 'time_limit': 500, 'disp': False})
print('status', res.status, res.message)
print('integer-version optimum (min form) = %.6f ; mip dual bound = %s' % (res.fun, getattr(res, 'mip_dual_bound', None)))
x = {i: max(vals, key=lambda v: res.x[col[(i, v)]]) for i in idx}
print('slacks', [round(sum(G(t, x[t[0]]) for t in terms) - b, 6) for name, terms, b in rows])
print('cost of rounded point', sum(c.get(i, 0) * x[i] for i in idx))
