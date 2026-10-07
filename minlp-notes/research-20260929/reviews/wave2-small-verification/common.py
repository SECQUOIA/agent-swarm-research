"""Shared helpers for the wave-2 small-instance verification (own code).

Uses the verifier's decimal-preserving OSIL reader (osilx.py from the earlier
review) only for parsing; evaluation, interval enclosure and pretty-printing are
defined here.  Objective and row `constant` attributes are included.
"""
import os
import sys
from fractions import Fraction

import mpmath
from mpmath import iv, mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "open-instances-verification"))
import osilx  # noqa: E402

OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil")


def load(name):
    return osilx.read(os.path.join(OSIL, name + ".osil"))


def fmt(t, names=None):
    """Readable infix form of an osilx expression tree."""
    op = t[0]
    if op == "num":
        return t[1]
    if op == "var":
        v = names[t[1]] if names else "x%d" % t[1]
        return v if t[2] == "1" else "%s*%s" % (t[2], v)
    a = [fmt(c, names) for c in t[1:]]
    if op in ("sum", "plus"):
        return "(" + " + ".join(a) + ")"
    if op in ("product", "times"):
        return "(" + " * ".join(a) + ")"
    if op == "minus":
        return "(%s - %s)" % tuple(a)
    if op == "negate":
        return "-(%s)" % a[0]
    if op == "divide":
        return "(%s / %s)" % tuple(a)
    if op == "square":
        return "(%s)^2" % a[0]
    if op == "power":
        return "(%s)^(%s)" % tuple(a)
    return "%s(%s)" % (op, ", ".join(a))


def row_str(m, r, names=None):
    c = m["cons"][r]
    parts = []
    if c["constant"] != "0":
        parts.append(c["constant"])
    for j, v in sorted(c["lin"].items()):
        parts.append("%s*%s" % (v, names[j] if names else "x%d" % j))
    for i, j, v in c["quad"]:
        parts.append("%s*x%d*x%d" % (v, i, j))
    if c["nl"] is not None:
        parts.append(fmt(c["nl"], names))
    return "%s <= %s <= %s" % (c["lb"], " + ".join(parts), c["ub"])


# ---------------- number systems ----------------
def _mp_power(a, b):
    return a ** b


MPFNS = {"ln": mpmath.log, "log": mpmath.log, "exp": mpmath.exp, "cos": mpmath.cos,
         "sin": mpmath.sin, "sqrt": mpmath.sqrt, "power": _mp_power}


def _iv_power(a, b):
    # integer exponent: repeated multiplication semantics (valid for any sign)
    if b.a == b.b and mpmath.mpf(b.a) == int(mpmath.mpf(b.a)):
        k = int(mpmath.mpf(b.a))
        if k >= 0:
            r = iv.mpf(1)
            for _ in range(k):
                r = r * a
            return r
    assert a.a > 0, "non-integer power needs a positive base"
    return iv.exp(b * iv.log(a))


IVFNS = {"ln": iv.log, "log": iv.log, "exp": iv.exp, "cos": iv.cos, "sin": iv.sin,
         "sqrt": iv.sqrt, "power": _iv_power}


def mpnum(s):
    return mpmath.mpf(s)


def ivnum(s):
    return iv.mpf(s)  # decimal strings are enclosed outward by mpmath iv


def fracnum(s):
    return Fraction(s)


def obj_value(m, x, num, fns):
    o = m["obj"]
    s = num(o["constant"])
    for j, c in o["lin"].items():
        s = s + num(c) * x[j]
    for i, j, c in o["quad"]:
        s = s + num(c) * x[i] * x[j]
    if o["nl"] is not None:
        s = s + osilx.ev_tree(o["nl"], x, num, fns)
    return s


def row_value(m, r, x, num, fns):
    return osilx.ev_row(m["cons"][r], x, num, fns)


def read_sol(path):
    """Read a MINLPLib .sol file: lines 'name value'; returns dict name->str."""
    out = {}
    for line in open(path):
        p = line.split()
        if len(p) >= 2 and not line.startswith("#"):
            out[p[0]] = p[1]
    return out
