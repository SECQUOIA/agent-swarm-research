"""Reviewer's own OSiL reader and exact evaluator (audit-ir review, round 1).

Written from the OSiL 2.0 schema conventions, without reading or importing the
audit's or the track author's readers.

Conventions implemented:
- <var>: lb default 0, ub default +INF; type C (default), I, B (B: bounds 0/1
  unless given).
- <con>: lb default -INF, ub default +INF; optional constant attribute is added
  to the row body.
- <obj>: maxOrMin, constant attribute (default 0), weight must be 1,
  <coef idx> linear coefficients.
- linearConstraintCoefficients: <start> plus <colIdx> (row-major) or <rowIdx>
  (column-major), and <value>; <el mult incr> expansion (incr only for
  integer arrays; for value arrays mult repeats the value).
- quadraticCoefficients: <qTerm idx idxOne idxTwo coef> (idx -1 = objective).
- nonlinearExpressions: <nl idx> trees with the rational operators used by the
  checked instances (sum, product, negate, minus, divide, square, power with
  a nonnegative integer exponent, number, variable). Anything else raises.

All numbers are kept as exact Fractions built from the decimal strings.
"""
import os
import xml.etree.ElementTree as ET
from fractions import Fraction as F

OSIL_DIR = os.path.expanduser('~/.cache/minlplib/minlplib/osil')
INF = None


def tag(e):
    return e.tag.split('}', 1)[-1]


def fr(s):
    s = s.strip()
    if s in ('INF', '+INF', 'inf', 'Infinity'):
        return 'INF'
    if s in ('-INF', '-inf', '-Infinity'):
        return '-INF'
    return F(s)


def expand(parent, is_int):
    out = []
    for el in parent:
        if tag(el) != 'el':
            raise ValueError('unexpected tag ' + tag(el))
        mult = int(el.get('mult', '1'))
        if is_int:
            v = int(el.text)
            inc = int(el.get('incr', '0'))
            out.extend(v + k * inc for k in range(mult))
        else:
            if el.get('incr') is not None:
                raise ValueError('incr in value array')
            out.extend([F(el.text.strip())] * mult)
    return out


class Model:
    pass


def load(name):
    root = ET.parse(os.path.join(OSIL_DIR, name + '.osil')).getroot()
    idata = [c for c in root if tag(c) == 'instanceData'][0]
    m = Model()
    m.name = name
    sec = {tag(c): c for c in idata}
    m.vname, m.vlb, m.vub, m.vtype = [], [], [], []
    for v in sec['variables']:
        t = v.get('type', 'C')
        if t not in ('C', 'I', 'B'):
            raise ValueError('var type ' + t)
        lb = v.get('lb')
        ub = v.get('ub')
        lb = fr(lb) if lb is not None else F(0)
        if ub is not None:
            ub = fr(ub)
        else:
            ub = F(1) if t == 'B' else 'INF'
        m.vname.append(v.get('name'))
        m.vlb.append(lb)
        m.vub.append(ub)
        m.vtype.append(t)
    n = len(m.vname)
    assert n == int(sec['variables'].get('numberOfVariables'))
    objs = list(sec['objectives'])
    assert len(objs) == 1
    o = objs[0]
    m.sense = o.get('maxOrMin', 'min')
    assert F(o.get('weight', '1')) == 1
    m.obj_const = F(o.get('constant', '0'))
    m.obj_lin = {}
    for c in o:
        assert tag(c) == 'coef'
        i = int(c.get('idx'))
        m.obj_lin[i] = m.obj_lin.get(i, F(0)) + F(c.text.strip())
    assert len(list(o)) == int(o.get('numberOfObjCoef', '0'))
    m.cname, m.clb, m.cub, m.cconst = [], [], [], []
    if 'constraints' in sec:
        for c in sec['constraints']:
            m.cname.append(c.get('name'))
            lb = c.get('lb')
            ub = c.get('ub')
            m.clb.append(fr(lb) if lb is not None else '-INF')
            m.cub.append(fr(ub) if ub is not None else 'INF')
            m.cconst.append(F(c.get('constant', '0')))
    nc = len(m.cname)
    m.lin = [dict() for _ in range(nc)]
    if 'linearConstraintCoefficients' in sec:
        L = sec['linearConstraintCoefficients']
        parts = {tag(c): c for c in L}
        start = expand(parts['start'], True)
        vals = expand(parts['value'], False)
        if 'colIdx' in parts:
            idx = expand(parts['colIdx'], True)
            assert len(start) == nc + 1
            for r in range(nc):
                for k in range(start[r], start[r + 1]):
                    m.lin[r][idx[k]] = m.lin[r].get(idx[k], F(0)) + vals[k]
        else:
            idx = expand(parts['rowIdx'], True)
            assert len(start) == n + 1
            for j in range(n):
                for k in range(start[j], start[j + 1]):
                    m.lin[idx[k]][j] = m.lin[idx[k]].get(j, F(0)) + vals[k]
        assert len(idx) == len(vals) == int(L.get('numberOfValues'))
    m.quad = {}  # row -> list of (i, j, coef)
    if 'quadraticCoefficients' in sec:
        for q in sec['quadraticCoefficients']:
            r = int(q.get('idx'))
            m.quad.setdefault(r, []).append(
                (int(q.get('idxOne')), int(q.get('idxTwo')), F(q.get('coef', '1'))))
    m.nl = {}
    if 'nonlinearExpressions' in sec:
        for e in sec['nonlinearExpressions']:
            r = int(e.get('idx'))
            kids = list(e)
            assert len(kids) == 1
            m.nl.setdefault(r, []).append(kids[0])
    for s in sec:
        if s not in ('variables', 'objectives', 'constraints', 'linearConstraintCoefficients',
                     'quadraticCoefficients', 'nonlinearExpressions'):
            raise ValueError('unhandled section ' + s)
    return m


def ev(e, x):
    t = tag(e)
    k = list(e)
    if t == 'number':
        assert e.get('type', 'real') == 'real'
        return F(e.get('value'))
    if t == 'variable':
        c = F(e.get('coef', '1'))
        assert len(k) == 0
        return c * x[int(e.get('idx'))]
    if t == 'sum':
        return sum((ev(c, x) for c in k), F(0))
    if t == 'product':
        p = F(1)
        for c in k:
            p *= ev(c, x)
        return p
    if t == 'negate':
        assert len(k) == 1
        return -ev(k[0], x)
    if t == 'minus':
        assert len(k) == 2
        return ev(k[0], x) - ev(k[1], x)
    if t == 'divide':
        assert len(k) == 2
        den = ev(k[1], x)
        if den == 0:
            raise ZeroDivisionError
        return ev(k[0], x) / den
    if t == 'square':
        assert len(k) == 1
        v = ev(k[0], x)
        return v * v
    if t == 'power':
        assert len(k) == 2
        expo = ev(k[1], x)
        assert expo.denominator == 1 and expo >= 0, 'non-integer power'
        return ev(k[0], x) ** int(expo)
    raise ValueError('operator not handled: ' + t)


def row_value(m, r, x):
    v = m.cconst[r]
    for j, c in m.lin[r].items():
        v += c * x[j]
    for i, j, c in m.quad.get(r, []):
        v += c * x[i] * x[j]
    for e in m.nl.get(r, []):
        v += ev(e, x)
    return v


def obj_value(m, x):
    v = m.obj_const
    for j, c in m.obj_lin.items():
        v += c * x[j]
    for i, j, c in m.quad.get(-1, []):
        v += c * x[i] * x[j]
    for e in m.nl.get(-1, []):
        v += ev(e, x)
    return v


def check(m, x):
    """Exact check. Returns a list of (kind, name, amount) violations."""
    bad = []
    for j in range(len(m.vname)):
        lb, ub = m.vlb[j], m.vub[j]
        if lb != '-INF' and x[j] < lb:
            bad.append(('var<lb', m.vname[j], lb - x[j]))
        if ub != 'INF' and x[j] > ub:
            bad.append(('var>ub', m.vname[j], x[j] - ub))
        if m.vtype[j] in ('I', 'B') and x[j].denominator != 1:
            bad.append(('nonint', m.vname[j], x[j]))
    for r in range(len(m.cname)):
        v = row_value(m, r, x)
        if m.clb[r] != '-INF' and v < m.clb[r]:
            bad.append(('row<lb', m.cname[r], m.clb[r] - v))
        if m.cub[r] != 'INF' and v > m.cub[r]:
            bad.append(('row>ub', m.cname[r], v - m.cub[r]))
    return bad


def read_sol(m, path):
    """Read a MINLPLib .sol file (name value lines). Missing variables are 0.
    Returns (x, unknown_names)."""
    pos = {nm: j for j, nm in enumerate(m.vname)}
    x = [F(0)] * len(m.vname)
    unknown = []
    seen = set()
    for line in open(path):
        p = line.split()
        if not p:
            continue
        assert len(p) == 2, line
        if p[0] in pos:
            assert p[0] not in seen
            seen.add(p[0])
            x[pos[p[0]]] = F(p[1])
        else:
            unknown.append(p[0])
    return x, unknown
