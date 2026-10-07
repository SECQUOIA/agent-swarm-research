"""Independent OSiL reader with exact rational evaluation (audit-ir track).

Written for this track only. It does not import or copy the audit's code
(audit.py, audit_eval.py, verify.py, verify_one.py, cert_*.py) or the
reviewers' readers.

Every constant is converted from its decimal string to a Python Fraction,
so the model is the OSiL file with exact decimal data. Expressions are
evaluated generically: with Fraction arguments the result is exact; with
RI (rational interval) arguments the result is an exact rational
enclosure (no floating point, no rounding assumption).

Only rational operators are supported (sum, plus, minus, negate, times,
product, divide, square, power with an integer constant exponent, number,
variable). Any other operator raises, so a model outside this class
cannot be evaluated silently wrong.
"""
from fractions import Fraction as Q
import xml.etree.ElementTree as ET

NS = '{os.optimizationservices.org}'


def dec(s):
    """Exact value of a decimal string; None for +-INF."""
    s = s.strip()
    if s in ('INF', '+INF', 'Infinity', '+Infinity'):
        return 'inf'
    if s in ('-INF', '-Infinity'):
        return '-inf'
    return Q(s)


def tag(e):
    return e.tag[len(NS):] if e.tag.startswith(NS) else e.tag


def expand(parent, integer):
    """Expand an OSiL <el mult incr> array."""
    out = []
    for el in parent:
        assert tag(el) == 'el', tag(el)
        m = int(el.get('mult', '1'))
        inc = el.get('incr')
        if integer:
            v = int(el.text)
            k = int(inc) if inc is not None else 0
            out.extend(v + i * k for i in range(m))
        else:
            assert inc is None, 'incr in a value array'
            v = Q(el.text.strip())
            out.extend([v] * m)
    return out


# ---------------------------------------------------------------- intervals
class RI:
    """Closed interval [lo, hi] with exact Fraction endpoints."""
    __slots__ = ('lo', 'hi')

    def __init__(self, lo, hi=None):
        lo = Q(lo)
        hi = lo if hi is None else Q(hi)
        assert lo <= hi, (lo, hi)
        self.lo, self.hi = lo, hi

    @staticmethod
    def c(x):
        return x if isinstance(x, RI) else RI(x)

    def __add__(a, b):
        b = RI.c(b)
        return RI(a.lo + b.lo, a.hi + b.hi)
    __radd__ = __add__

    def __neg__(a):
        return RI(-a.hi, -a.lo)

    def __sub__(a, b):
        b = RI.c(b)
        return RI(a.lo - b.hi, a.hi - b.lo)

    def __rsub__(a, b):
        return RI.c(b) - a

    def __mul__(a, b):
        b = RI.c(b)
        p = (a.lo * b.lo, a.lo * b.hi, a.hi * b.lo, a.hi * b.hi)
        return RI(min(p), max(p))
    __rmul__ = __mul__

    def __truediv__(a, b):
        b = RI.c(b)
        if b.lo <= 0 <= b.hi:
            raise ZeroDivisionError('interval divisor contains 0')
        return a * RI(1 / b.hi, 1 / b.lo)

    def __rtruediv__(a, b):
        return RI.c(b) / a

    def sq(a):
        if a.lo >= 0:
            return RI(a.lo * a.lo, a.hi * a.hi)
        if a.hi <= 0:
            return RI(a.hi * a.hi, a.lo * a.lo)
        return RI(0, max(a.lo * a.lo, a.hi * a.hi))

    def contains(a, x):
        return a.lo <= x <= a.hi

    def __repr__(self):
        return 'RI(%s, %s)' % (float(self.lo), float(self.hi))


def sq(x):
    return x.sq() if isinstance(x, RI) else x * x


def ipow(x, n):
    assert isinstance(n, int) and n >= 0
    if n == 0:
        return Q(1) if not isinstance(x, RI) else RI(1)
    if n % 2 == 0:
        return ipow(sq(x), n // 2)
    r = x
    for _ in range(n - 1):
        r = r * x
    return r


# --------------------------------------------------------------- expressions
def build(e):
    """Compile an OSnL element into a function of the variable vector."""
    t = tag(e)
    ch = list(e)
    if t == 'number':
        assert e.get('type', 'real') == 'real', e.attrib
        v = Q(e.get('value').strip())
        return lambda x: v
    if t == 'variable':
        assert not ch, 'variable with a child expression'
        j = int(e.get('idx'))
        cf = Q(e.get('coef', '1').strip())
        if cf == 1:
            return lambda x: x[j]
        return lambda x: cf * x[j]
    fs = [build(c) for c in ch]
    if t in ('sum', 'plus'):
        if t == 'plus':
            assert len(fs) == 2
        def f(x):
            s = fs[0](x)
            for g in fs[1:]:
                s = s + g(x)
            return s
        return f
    if t == 'minus':
        assert len(fs) == 2
        return lambda x: fs[0](x) - fs[1](x)
    if t == 'negate':
        assert len(fs) == 1
        return lambda x: -fs[0](x)
    if t in ('product', 'times'):
        if t == 'times':
            assert len(fs) == 2
        def f(x):
            s = fs[0](x)
            for g in fs[1:]:
                s = s * g(x)
            return s
        return f
    if t == 'divide':
        assert len(fs) == 2
        return lambda x: fs[0](x) / fs[1](x)
    if t == 'square':
        assert len(fs) == 1
        return lambda x: sq(fs[0](x))
    if t == 'power':
        assert len(fs) == 2
        assert tag(ch[1]) == 'number', 'non-constant exponent'
        n = Q(ch[1].get('value').strip())
        assert n.denominator == 1 and n >= 0, n
        n = int(n)
        return lambda x: ipow(fs[0](x), n)
    raise NotImplementedError('operator %s' % t)


def var_set(e, acc):
    if tag(e) == 'variable':
        acc.add(int(e.get('idx')))
    for c in e:
        var_set(c, acc)
    return acc


# --------------------------------------------------------------------- model
class Model:
    def __init__(self, path):
        root = ET.parse(path).getroot()
        d = root.find(NS + 'instanceData')
        known = {'variables', 'objectives', 'constraints',
                 'linearConstraintCoefficients', 'quadraticCoefficients',
                 'nonlinearExpressions'}
        for c in d:
            assert tag(c) in known, 'unsupported section %s' % tag(c)
        # variables
        self.names, self.lb, self.ub, self.vtype = [], [], [], []
        for v in d.find(NS + 'variables'):
            assert set(v.attrib) <= {'name', 'lb', 'ub', 'type'}, v.attrib
            ty = v.get('type', 'C')
            assert ty in ('C', 'B', 'I'), ty
            lb = dec(v.get('lb', '0'))
            ub = dec(v.get('ub', '1' if ty == 'B' else 'INF'))
            self.names.append(v.get('name'))
            self.lb.append(None if lb == '-inf' else lb)
            self.ub.append(None if ub == 'inf' else ub)
            self.vtype.append(ty)
        n = self.n = len(self.names)
        self.index = {s: i for i, s in enumerate(self.names)}
        # objective
        objs = list(d.find(NS + 'objectives'))
        assert len(objs) == 1
        o = objs[0]
        assert set(o.attrib) <= {'maxOrMin', 'name', 'numberOfObjCoef',
                                 'constant', 'weight'}, o.attrib
        self.sense = o.get('maxOrMin', 'min')
        assert Q(o.get('weight', '1')) == 1
        self.obj_const = Q(o.get('constant', '0'))
        self.obj_lin = {}
        for c in o:
            assert tag(c) == 'coef' and set(c.attrib) == {'idx'}, c.attrib
            j = int(c.get('idx'))
            self.obj_lin[j] = self.obj_lin.get(j, 0) + Q(c.text.strip())
        # constraints
        self.rnames, self.rlb, self.rub, self.rconst = [], [], [], []
        cons = d.find(NS + 'constraints')
        for c in (cons if cons is not None else []):
            assert set(c.attrib) <= {'name', 'lb', 'ub', 'constant'}, c.attrib
            lb = dec(c.get('lb', '-INF'))
            ub = dec(c.get('ub', 'INF'))
            self.rnames.append(c.get('name'))
            self.rlb.append(None if lb == '-inf' else lb)
            self.rub.append(None if ub == 'inf' else ub)
            self.rconst.append(Q(c.get('constant', '0')))
        m = self.m = len(self.rnames)
        # linear part
        self.lin = [dict() for _ in range(m)]
        lc = d.find(NS + 'linearConstraintCoefficients')
        if lc is not None:
            start = expand(lc.find(NS + 'start'), True)
            val = expand(lc.find(NS + 'value'), False)
            ci, ri = lc.find(NS + 'colIdx'), lc.find(NS + 'rowIdx')
            assert (ci is None) != (ri is None)
            if ci is not None:          # row major
                idx = expand(ci, True)
                assert len(start) == m + 1
                for i in range(m):
                    for k in range(start[i], start[i + 1]):
                        self.lin[i][idx[k]] = self.lin[i].get(idx[k], 0) + val[k]
            else:                       # column major
                idx = expand(ri, True)
                assert len(start) == n + 1
                for j in range(n):
                    for k in range(start[j], start[j + 1]):
                        self.lin[idx[k]][j] = self.lin[idx[k]].get(j, 0) + val[k]
            assert len(val) == len(idx) == start[-1]
        # quadratic part, keyed by row (-1 = objective)
        self.quad = {}
        qc = d.find(NS + 'quadraticCoefficients')
        if qc is not None:
            for qt in qc:
                assert tag(qt) == 'qTerm'
                assert set(qt.attrib) <= {'idx', 'idxOne', 'idxTwo', 'coef'}
                r = int(qt.get('idx'))
                self.quad.setdefault(r, []).append(
                    (int(qt.get('idxOne')), int(qt.get('idxTwo')),
                     Q(qt.get('coef', '1').strip())))
        # nonlinear part
        self.nl = {}
        self.nlvars = {}
        ne = d.find(NS + 'nonlinearExpressions')
        if ne is not None:
            for e in ne:
                assert tag(e) == 'nl'
                r = int(e.get('idx'))
                (body,) = list(e)
                self.nl.setdefault(r, []).append(build(body))
                self.nlvars.setdefault(r, set()).update(var_set(body, set()))

    # --- evaluation (generic in Fraction / RI)
    def _body(self, r, x, lin, const):
        s = const
        for j, a in lin.items():
            s = s + a * x[j]
        for (j, k, a) in self.quad.get(r, []):
            s = s + a * x[j] * x[k]
        for f in self.nl.get(r, []):
            s = s + f(x)
        return s

    def row(self, i, x):
        return self._body(i, x, self.lin[i], self.rconst[i])

    def obj(self, x):
        return self._body(-1, x, self.obj_lin, self.obj_const)

    def row_vars(self, i):
        s = set(self.lin[i])
        for (j, k, a) in self.quad.get(i, []):
            s.update((j, k))
        s.update(self.nlvars.get(i, set()))
        return s

    def is_eq(self, i):
        return self.rlb[i] is not None and self.rlb[i] == self.rub[i]


def read_sol(path, model):
    """Read a MINLPLib .sol file (name value per line) as exact decimals.
    Missing variables are 0. Returns (x, ignored_names)."""
    x = [Q(0)] * model.n
    ignored = []
    seen = set()
    for line in open(path):
        p = line.split()
        if not p:
            continue
        assert len(p) == 2, line
        if p[0] in model.index:
            assert p[0] not in seen
            seen.add(p[0])
            x[model.index[p[0]]] = Q(p[1])
        else:
            ignored.append(p[0])
    return x, ignored


def check_exact(model, x):
    """Exact check of every bound, integrality and row at a rational x.
    Returns (list of violations, objective). Each violation is
    (kind, name, amount) with amount > 0 an exact Fraction."""
    bad = []
    for j in range(model.n):
        if model.lb[j] is not None and x[j] < model.lb[j]:
            bad.append(('lb', model.names[j], model.lb[j] - x[j]))
        if model.ub[j] is not None and x[j] > model.ub[j]:
            bad.append(('ub', model.names[j], x[j] - model.ub[j]))
        if model.vtype[j] in ('B', 'I') and x[j].denominator != 1:
            bad.append(('int', model.names[j], abs(x[j] - round(x[j]))))
    for i in range(model.m):
        v = model.row(i, x)
        if model.rlb[i] is not None and v < model.rlb[i]:
            bad.append(('row<lb', model.rnames[i], model.rlb[i] - v))
        if model.rub[i] is not None and v > model.rub[i]:
            bad.append(('row>ub', model.rnames[i], v - model.rub[i]))
    return bad, model.obj(x)
