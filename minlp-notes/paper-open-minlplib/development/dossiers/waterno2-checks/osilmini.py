"""Minimal independent OSIL reader for linear rows and bounds (exact decimals)."""
import xml.etree.ElementTree as ET
from fractions import Fraction as F

NS = '{os.optimizationservices.org}'

def _num(s):
    if s in ('INF', 'Infinity', '+INF'): return None
    if s in ('-INF', '-Infinity'): return None
    return F(s)

def _expand(elem, kind):
    out = []
    for el in elem.findall(NS + 'el'):
        mult = int(el.get('mult', '1'))
        incr = el.get('incr')
        v = el.text.strip()
        if kind == 'int':
            v0 = int(v); inc = int(incr) if incr else 0
            out.extend(v0 + i * inc for i in range(mult))
        else:
            v0 = F(v); inc = F(incr) if incr else F(0)
            out.extend(v0 + i * inc for i in range(mult))
    return out

def read(path):
    root = ET.parse(path).getroot()
    d = root.find(NS + 'instanceData')
    vars_ = []
    for v in d.find(NS + 'variables').findall(NS + 'var'):
        lb = v.get('lb', '0'); ub = v.get('ub', 'INF')
        vars_.append(dict(name=v.get('name'), type=v.get('type', 'C'),
                          lb=None if lb.startswith('-INF') else F(lb),
                          ub=None if ub in ('INF', '+INF') else F(ub)))
    cons = []
    for c in d.find(NS + 'constraints').findall(NS + 'con'):
        lb = c.get('lb'); ub = c.get('ub')
        assert c.get('constant') is None
        cons.append(dict(name=c.get('name'), lb=None if lb is None or lb.startswith('-INF') else F(lb),
                         ub=None if ub is None or ub in ('INF', '+INF') else F(ub)))
    lcc = d.find(NS + 'linearConstraintCoefficients')
    start = _expand(lcc.find(NS + 'start'), 'int')
    val = _expand(lcc.find(NS + 'value'), 'frac')
    rows = [dict() for _ in cons]
    if lcc.find(NS + 'rowIdx') is not None:   # column-major
        idx = _expand(lcc.find(NS + 'rowIdx'), 'int')
        for j in range(len(start) - 1):
            for p in range(start[j], start[j + 1]):
                rows[idx[p]][j] = rows[idx[p]].get(j, 0) + val[p]
    else:
        idx = _expand(lcc.find(NS + 'colIdx'), 'int')
        for i in range(len(start) - 1):
            for p in range(start[i], start[i + 1]):
                rows[i][idx[p]] = rows[i].get(idx[p], 0) + val[p]
    nonlin = set()
    q = d.find(NS + 'quadraticCoefficients')
    if q is not None:
        for t in q.findall(NS + 'qTerm'):
            nonlin.add(int(t.get('idx')))
    n = d.find(NS + 'nonlinearExpressions')
    if n is not None:
        for e in n.findall(NS + 'nl'):
            nonlin.add(int(e.get('idx')))
    obj = d.find(NS + 'objectives').find(NS + 'obj')
    assert obj.get('constant') is None
    objc = {int(c.get('idx')): F(c.text) for c in obj.findall(NS + 'coef')}
    return dict(vars=vars_, cons=cons, rows=rows, nonlin=nonlin, obj=objc, sense=obj.get('maxOrMin'))
