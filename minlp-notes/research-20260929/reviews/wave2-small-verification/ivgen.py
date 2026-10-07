"""Compile sympy expressions (exact rational coefficients, log, integer powers)
into Python functions over mpmath `iv` intervals.

Rigour: every rational constant p/q is enclosed as iv.mpf(p)/iv.mpf(q) at the
precision active when the constants are built; integer powers are evaluated by
repeated interval multiplication (division for negative exponents); log is
iv.log.  Only these node types are accepted; anything else raises.
"""
import sympy as sp
from mpmath import iv


def _ipow(x, k):
    if k < 0:
        return 1 / _ipow(x, -k)
    if k == 2:
        return x * x
    r = x
    for _ in range(k - 1):
        r = r * x
    return r


def _rpow(x, e):
    assert x.a > 0, "rational power of a non-positive interval"
    return iv.exp(e * iv.log(x))


class _Gen:
    def __init__(self):
        self.consts = []
        self.cidx = {}

    def const(self, r):
        r = sp.Rational(r)
        if r not in self.cidx:
            self.cidx[r] = len(self.consts)
            self.consts.append(r)
        return "K[%d]" % self.cidx[r]

    def code(self, e):
        if e.is_Symbol:
            return e.name
        if e.is_Rational:
            if e == 1:
                return "ONE"
            return self.const(e)
        if e.is_Add:
            return "(" + " + ".join(self.code(a) for a in e.args) + ")"
        if e.is_Mul:
            return "(" + " * ".join(self.code(a) for a in e.args) + ")"
        if e.is_Pow:
            k = e.args[1]
            if k.is_Integer:
                return "IPOW(%s, %d)" % (self.code(e.args[0]), int(k))
            assert k.is_Rational, e
            # non-integer rational exponent: positive base required (iv.log domain)
            return "RPOW(%s, %s)" % (self.code(e.args[0]), self.const(k))
        if isinstance(e, sp.log):
            return "LOG(%s)" % self.code(e.args[0])
        raise NotImplementedError(type(e))


def compile_exprs(args, exprs, name="f"):
    """Return (factory) where factory() builds the function at the current iv precision."""
    reps, red = sp.cse(exprs, symbols=sp.numbered_symbols("s"))
    g = _Gen()
    lines = ["def %s(%s):" % (name, ", ".join(a.name for a in args))]
    for s, e in reps:
        lines.append("    %s = %s" % (s.name, g.code(e)))
    lines.append("    return (" + ", ".join(g.code(e) for e in red) + ",)")
    src = "\n".join(lines)
    consts = list(g.consts)

    def factory():
        K = [iv.mpf(int(r.p)) / iv.mpf(int(r.q)) for r in consts]
        ns = dict(K=K, ONE=iv.mpf(1), IPOW=_ipow, LOG=iv.log, RPOW=_rpow)
        exec(src, ns)
        return ns[name]

    factory.src = src
    return factory
