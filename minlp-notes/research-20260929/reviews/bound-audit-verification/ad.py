"""Forward-mode differentiation of OSIL rows over floats or ivl intervals.

ev(e, x, T, active) returns (value, {j: d value / d x_j}) where only indices in
`active` (a set, or None for all) get derivatives. T is FloatT or IvT.
"""
import math
from fractions import Fraction as F

import ivl


class FloatT:
    @staticmethod
    def c(v):
        return float(v)

    x = c
    zero = 0.0
    one = 1.0

    @staticmethod
    def sqr(a):
        return a * a

    @staticmethod
    def powi(a, p):
        return a ** p

    sqrt = staticmethod(math.sqrt)

    @staticmethod
    def exp(a):
        return math.exp(a) if a > -745 else 0.0

    ln = staticmethod(math.log)


class IvT:
    @staticmethod
    def c(v):
        return ivl.I(v)

    @staticmethod
    def x(v):
        return ivl.I.of(v)

    zero = ivl.I(0)
    one = ivl.I(1)

    @staticmethod
    def sqr(a):
        return a.sqr()

    @staticmethod
    def powi(a, p):
        return a.powi(p)

    @staticmethod
    def sqrt(a):
        return a.sqrt()

    @staticmethod
    def exp(a):
        return a.exp()

    @staticmethod
    def ln(a):
        return a.ln()


def _add(g, h, s=None):
    r = dict(g)
    for k, v in h.items():
        v = v if s is None else s * v
        r[k] = r[k] + v if k in r else v
    return r


def _scale(g, s):
    return {k: s * v for k, v in g.items()}


def ev(e, x, T, active):
    t = e[0]
    if t == "num":
        return T.c(e[1]), {}
    if t == "var":
        j = e[1]
        c = T.c(e[2])
        return c * T.x(x[j]), ({j: c} if (active is None or j in active) else {})
    ch = [ev(c, x, T, active) for c in e[1]]
    if t == "sum":
        v, g = T.zero, {}
        for (a, ga) in ch:
            v = v + a
            g = _add(g, ga)
        return v, g
    if t in ("product", "times"):
        vals = [a for a, _ in ch]
        n = len(vals)
        pre = [T.one] * (n + 1)
        for k in range(n):
            pre[k + 1] = pre[k] * vals[k]
        suf = [T.one] * (n + 1)
        for k in range(n - 1, -1, -1):
            suf[k] = suf[k + 1] * vals[k]
        g = {}
        for k in range(n):
            if ch[k][1]:
                g = _add(g, ch[k][1], pre[k] * suf[k + 1])
        return pre[n], g
    if t == "plus":
        return ch[0][0] + ch[1][0], _add(ch[0][1], ch[1][1])
    if t == "minus":
        return ch[0][0] - ch[1][0], _add(ch[0][1], _scale(ch[1][1], -T.one))
    if t == "negate":
        return -ch[0][0], _scale(ch[0][1], -T.one)
    if t == "divide":
        (a, ga), (b, gb) = ch
        q = a / b
        g = _scale(ga, T.one / b)
        if gb:
            g = _add(g, gb, -(q / b))
        return q, g
    if t == "square":
        a, ga = ch[0]
        return T.sqr(a), _scale(ga, T.c(2) * a)
    if t == "power":
        (a, ga), (p, gp) = ch
        assert not gp
        pp = e[1][1][1]
        assert e[1][1][0] == "num" and pp.denominator == 1 and pp >= 0
        pp = int(pp)
        if pp == 0:
            return T.one, {}
        return T.powi(a, pp), _scale(ga, T.c(pp) * T.powi(a, pp - 1))
    if t == "sqrt":
        a, ga = ch[0]
        s = T.sqrt(a)
        return s, (_scale(ga, T.one / (T.c(2) * s)) if ga else {})
    if t == "exp":
        a, ga = ch[0]
        s = T.exp(a)
        return s, _scale(ga, s)
    if t == "ln":
        a, ga = ch[0]
        return T.ln(a), _scale(ga, T.one / a)
    raise NotImplementedError(t)


def row(M, i, x, T, active):
    """Row body value (including OSIL constant) and gradient."""
    v = T.c(M.cconst[i])
    g = {}
    for j, c in M.lin[i].items():
        cc = T.c(c)
        v = v + cc * T.x(x[j])
        if active is None or j in active:
            g[j] = g[j] + cc if j in g else cc
    for (a, b, c) in M.quad[i]:
        cc = T.c(c)
        xa, xb = T.x(x[a]), T.x(x[b])
        if a == b:
            v = v + cc * T.sqr(xa)
            if active is None or a in active:
                d = T.c(2) * cc * xa
                g[a] = g[a] + d if a in g else d
        else:
            v = v + cc * xa * xb
            if active is None or a in active:
                d = cc * xb
                g[a] = g[a] + d if a in g else d
            if active is None or b in active:
                d = cc * xa
                g[b] = g[b] + d if b in g else d
    if M.nl[i] is not None:
        a, ga = ev(M.nl[i], x, T, active)
        v = v + a
        g = _add(g, ga)
    return v, g
