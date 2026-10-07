"""Minimal independent OSIL reader (ElementTree), decimal strings kept exact.

Written for the small-family dossier; shares no code with osilx.py.
Model dict: names, lb, ub (strings, '-INF'/'INF'), cons (list of dict: name, lb, ub,
constant, lin {j: str}, nl tree or None), obj (sense, constant, lin {j: str}, nl).
Trees: ('num', s) | ('var', j, coef_str) | (op, child, ...).
"""
import xml.etree.ElementTree as ET
from fractions import Fraction

NS = '{os.optimizationservices.org}'


def _tag(e):
    return e.tag.replace(NS, '')


def _expand(parent):
    """expand <el mult incr> sequences into a list of strings"""
    out = []
    for el in parent:
        mult = int(el.get('mult', '1'))
        incr = el.get('incr')
        v = el.text.strip()
        if incr is None:
            out += [v] * mult
        else:
            x = Fraction(v)
            for _ in range(mult):
                out.append(str(x))
                x += Fraction(incr)
    return out


def _tree(e):
    t = _tag(e)
    if t == 'number':
        return ('num', e.get('value'))
    if t == 'variable':
        return ('var', int(e.get('idx')), e.get('coef', '1'))
    return (t,) + tuple(_tree(c) for c in e)


def read(path):
    root = ET.parse(path).getroot()
    data = root.find(NS + 'instanceData')
    V = data.find(NS + 'variables')
    names, lb, ub = [], [], []
    for v in V:
        names.append(v.get('name'))
        lb.append(v.get('lb', '0'))
        ub.append(v.get('ub', 'INF'))
        assert v.get('type', 'C') == 'C'
    n = len(names)
    O = data.find(NS + 'objectives')
    o = O[0]
    obj = dict(sense=o.get('maxOrMin'), constant=o.get('constant', '0'),
               lin={int(c.get('idx')): c.text.strip() for c in o}, nl=None)
    C = data.find(NS + 'constraints')
    cons = []
    if C is not None:
        for c in C:
            cons.append(dict(name=c.get('name'), lb=c.get('lb', '-INF'), ub=c.get('ub', 'INF'),
                             constant=c.get('constant', '0'), lin={}, nl=None))
    L = data.find(NS + 'linearConstraintCoefficients')
    if L is not None:
        start = [int(x) for x in _expand(L.find(NS + 'start'))]
        if L.find(NS + 'rowIdx') is not None:
            idx = [int(x) for x in _expand(L.find(NS + 'rowIdx'))]
            colmajor = True
        else:
            idx = [int(x) for x in _expand(L.find(NS + 'colIdx'))]
            colmajor = False
        val = _expand(L.find(NS + 'value'))
        for k in range(len(start) - 1):
            for p in range(start[k], start[k + 1]):
                if colmajor:
                    cons[idx[p]]['lin'][k] = val[p]
                else:
                    cons[k]['lin'][idx[p]] = val[p]
    assert data.find(NS + 'quadraticCoefficients') is None
    NL = data.find(NS + 'nonlinearExpressions')
    if NL is not None:
        for e in NL:
            i = int(e.get('idx'))
            tr = _tree(e[0])
            if i == -1:
                assert obj['nl'] is None
                obj['nl'] = tr
            else:
                assert cons[i]['nl'] is None
                cons[i]['nl'] = tr
    return dict(names=names, lb=lb, ub=ub, cons=cons, obj=obj, n=n)


def ev(tr, x, num, F):
    """evaluate a tree; num(str) -> number; F: dict of functions (cos, ln, exp, sqrt, pow)"""
    op = tr[0]
    if op == 'num':
        return num(tr[1])
    if op == 'var':
        c = tr[2]
        return x[tr[1]] if c == '1' else num(c) * x[tr[1]]
    a = [ev(c, x, num, F) for c in tr[1:]]
    if op in ('sum', 'plus'):
        s = a[0]
        for v in a[1:]:
            s = s + v
        return s
    if op in ('product', 'times'):
        s = a[0]
        for v in a[1:]:
            s = s * v
        return s
    if op == 'minus':
        return a[0] - a[1]
    if op == 'negate':
        return -a[0]
    if op == 'divide':
        return a[0] / a[1]
    if op == 'square':
        return a[0] * a[0]
    if op == 'power':
        return F['pow'](a[0], a[1], tr[2])
    if op in ('ln', 'log'):
        return F['ln'](a[0])
    if op in F:
        return F[op](a[0])
    raise NotImplementedError(op)


def row(m, i, x, num, F):
    c = m['cons'][i]
    s = num(c['constant'])
    for j, v in c['lin'].items():
        s = s + num(v) * x[j]
    if c['nl'] is not None:
        s = s + ev(c['nl'], x, num, F)
    return s


def objective(m, x, num, F):
    o = m['obj']
    s = num(o['constant'])
    for j, v in o['lin'].items():
        s = s + num(v) * x[j]
    if o['nl'] is not None:
        s = s + ev(o['nl'], x, num, F)
    return s
