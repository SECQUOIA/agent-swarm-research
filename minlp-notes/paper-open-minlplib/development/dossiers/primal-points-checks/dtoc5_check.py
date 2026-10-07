# Independent exact check of the stored dtoc5 point against the OSIL file
# (own parser; linear + quadratic coefficients; Fraction arithmetic).
import gzip, xml.etree.ElementTree as ET
from fractions import Fraction as F
from decimal import Decimal
NS = '{os.optimizationservices.org}'
def Q(s): return F(Decimal(s))
def expand(p):
    out = []
    for el in p:
        mult = int(el.get('mult', '1')); incr = el.get('incr'); v = el.text.strip()
        out += [v]*mult if incr is None else [str(int(v)+i*int(incr)) for i in range(mult)]
    return out
root = ET.parse('data/dtoc5.osil').getroot(); d = root.find(NS+'instanceData')
V = list(d.find(NS+'variables')); n = len(V); names = [v.get('name') for v in V]
pt = {}
for line in gzip.open('data/dtoc5_point.txt.gz','rt'):
    if line.startswith('#') or not line.strip(): continue
    k, v = line.split(); pt[k] = Q(v)
x = [pt[nm] for nm in names]
nb = 0
for v, xv in zip(V, x):
    lb = v.get('lb', '0'); ub = v.get('ub', 'INF'); assert v.get('type','C') == 'C'
    if lb != '-INF': assert xv >= Q(lb); nb += 1
    if ub != 'INF': assert xv <= Q(ub); nb += 1
C = list(d.find(NS+'constraints')); m = len(C)
row = [F(0)]*m
lcc = d.find(NS+'linearConstraintCoefficients')
start = [int(s) for s in expand(lcc.find(NS+'start'))]; col = [int(s) for s in expand(lcc.find(NS+'colIdx'))]; val = expand(lcc.find(NS+'value'))
for i in range(m):
    for k in range(start[i], start[i+1]): row[i] += Q(val[k]) * x[col[k]]
obj = F(0)
for q in d.find(NS+'quadraticCoefficients'):
    i = int(q.get('idx')); a = int(q.get('idxOne')); b = int(q.get('idxTwo')); c = Q(q.get('coef', '1'))
    if i == -1: obj += c * x[a] * x[b]
    else: row[i] += c * x[a] * x[b]
assert d.find(NS+'nonlinearExpressions') is None
o = d.find(NS+'objectives').find(NS+'obj'); assert o.get('maxOrMin','min') == 'min' and o.get('constant') is None and len(list(o)) == 0
bad = 0
for i, c in enumerate(C):
    lb = c.get('lb'); ub = c.get('ub')
    if lb is not None and row[i] < Q(lb): bad += 1
    if ub is not None and row[i] > Q(ub): bad += 1
stored = F(open('data/dtoc5_check_objective_exact.txt').read().strip())
print(f'dtoc5: {n} vars, {nb} finite bounds hold, {m} rows, violated rows: {bad}; objective == stored rational: {obj == stored}; f = {float(obj)!r}')
print('row types:', {(c.get("lb"), c.get("ub")) for c in C})
