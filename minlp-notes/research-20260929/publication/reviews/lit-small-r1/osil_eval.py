"""Reviewer's own OSIL reader and evaluator (lit-small review, round 1).

Written independently of the track's code. Reads an OSIL file, keeps all
numbers as decimal strings, and evaluates the objective and constraint
bodies at a point in mpmath arithmetic of the current precision.
Supported nonlinear nodes: sum, product, negate, minus, divide, power,
square, sqrt, ln, exp, cos, sin, number, variable.
"""
import xml.etree.ElementTree as ET
from mpmath import mp, mpf, log, exp, cos, sin, sqrt

NS = '{os.optimizationservices.org}'


def _tag(e):
    return e.tag.replace(NS, '')


def _expand(parent):
    """Expand an OSIL <el mult= incr=> list into a list of strings/ints."""
    out = []
    for el in parent:
        mult = int(el.get('mult', '1'))
        incr = el.get('incr')
        v = el.text.strip()
        for k in range(mult):
            if incr is None:
                out.append(v)
            else:
                out.append(str(mpf(v) + k * mpf(incr)) if '.' in v or '.' in incr else str(int(v) + k * int(incr)))
    return out


class Model:
    def __init__(self, path):
        root = ET.parse(path).getroot()
        d = root.find(NS + 'instanceData')
        self.vars = []
        for v in d.find(NS + 'variables'):
            self.vars.append(dict(name=v.get('name'), lb=v.get('lb', '0'), ub=v.get('ub', 'INF'),
                                  type=v.get('type', 'C')))
        self.n = len(self.vars)
        obj = d.find(NS + 'objectives')[0]
        self.sense = obj.get('maxOrMin', 'min')
        self.obj_const = obj.get('constant', '0')
        self.obj_lin = {int(c.get('idx')): c.text.strip() for c in obj if _tag(c) == 'coef'}
        self.cons = []
        cs = d.find(NS + 'constraints')
        if cs is not None:
            for c in cs:
                self.cons.append(dict(name=c.get('name'), lb=c.get('lb', '-INF'), ub=c.get('ub', 'INF'),
                                      const=c.get('constant', '0')))
        self.m = len(self.cons)
        self.lin = [dict() for _ in range(self.m)]
        lcc = d.find(NS + 'linearConstraintCoefficients')
        if lcc is not None:
            start = [int(s) for s in _expand(lcc.find(NS + 'start'))]
            vals = _expand(lcc.find(NS + 'value'))
            col = lcc.find(NS + 'colIdx')
            if col is not None:  # row-major
                idx = [int(s) for s in _expand(col)]
                for r in range(len(start) - 1):
                    for k in range(start[r], start[r + 1]):
                        self.lin[r][idx[k]] = vals[k]
            else:  # column-major
                idx = [int(s) for s in _expand(lcc.find(NS + 'rowIdx'))]
                for c in range(len(start) - 1):
                    for k in range(start[c], start[c + 1]):
                        self.lin[idx[k]][c] = vals[k]
        self.nl = {}
        nle = d.find(NS + 'nonlinearExpressions')
        if nle is not None:
            for e in nle:
                self.nl[int(e.get('idx'))] = e[0]

    def ev_node(self, e, x):
        t = _tag(e)
        ch = list(e)
        if t == 'variable':
            return mpf(e.get('coef', '1')) * x[int(e.get('idx'))]
        if t == 'number':
            return mpf(e.get('value'))
        if t == 'sum':
            return sum((self.ev_node(c, x) for c in ch), mpf(0))
        if t == 'product':
            p = mpf(1)
            for c in ch:
                p *= self.ev_node(c, x)
            return p
        if t == 'negate':
            return -self.ev_node(ch[0], x)
        if t == 'minus':
            return self.ev_node(ch[0], x) - self.ev_node(ch[1], x)
        if t == 'divide':
            return self.ev_node(ch[0], x) / self.ev_node(ch[1], x)
        if t == 'power':
            b = self.ev_node(ch[0], x)
            ex = self.ev_node(ch[1], x)
            if ex == int(ex):
                return b ** int(ex)
            return b ** ex
        if t == 'square':
            v = self.ev_node(ch[0], x)
            return v * v
        if t == 'sqrt':
            return sqrt(self.ev_node(ch[0], x))
        if t == 'ln':
            return log(self.ev_node(ch[0], x))
        if t == 'exp':
            return exp(self.ev_node(ch[0], x))
        if t == 'cos':
            return cos(self.ev_node(ch[0], x))
        if t == 'sin':
            return sin(self.ev_node(ch[0], x))
        raise ValueError('unsupported node ' + t)

    def objective(self, x):
        v = mpf(self.obj_const)
        for i, c in self.obj_lin.items():
            v += mpf(c) * x[i]
        if -1 in self.nl:
            v += self.ev_node(self.nl[-1], x)
        return v

    def body(self, r, x):
        v = mpf(self.cons[r]['const'])
        for i, c in self.lin[r].items():
            v += mpf(c) * x[i]
        if r in self.nl:
            v += self.ev_node(self.nl[r], x)
        return v

    def violation(self, x):
        """Max absolute violation of rows and bounds."""
        worst = mpf(0)
        for r, c in enumerate(self.cons):
            b = self.body(r, x)
            if c['lb'] not in ('-INF', '-inf'):
                worst = max(worst, mpf(c['lb']) - b)
            if c['ub'] not in ('INF', 'inf'):
                worst = max(worst, b - mpf(c['ub']))
        for i, v in enumerate(self.vars):
            if v['lb'] not in ('-INF', '-inf'):
                worst = max(worst, mpf(v['lb']) - x[i])
            if v['ub'] not in ('INF', 'inf'):
                worst = max(worst, x[i] - mpf(v['ub']))
        return worst
