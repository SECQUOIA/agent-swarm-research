"""OSIL model access for the powerflow primal-point certificates.

Rows read  lb <= constant + lin + quad + nl <= ub  (osilx conventions).  Every
evaluation takes a context `ctx` (mpmath `mp` for floating point, `iv` for
outward-rounded intervals) and returns values with sparse gradients, so the
same code serves Newton (mp) and the Krawczyk test (iv).
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../../..'))
import os
import sys
from fractions import Fraction as Fr

sys.path.insert(0, _REPRO_ROOT + "/research-20260929/reviews/open-instances-verification")
import osilx  # noqa: E402  (independent OSIL reader written for the verification review)

OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil")
SOL = _REPRO_ROOT + "/research-20260929/open-instances-wave3/sol"


def load(name):
    I = osilx.read(os.path.join(OSIL, name + ".osil"))
    assert set(I["vt"]) == {"C"}, "all variables continuous"
    assert all(osilx.isinf(a) and osilx.isinf(b) for a, b in zip(I["lb"], I["ub"])), "all variables free"
    assert I["obj"]["nl"] is None and I["obj"]["sense"] == "min" and I["obj"]["weight"] == "1"
    for c in I["cons"]:
        c["lbF"] = None if osilx.isinf(c["lb"]) else Fr(c["lb"])
        c["ubF"] = None if osilx.isinf(c["ub"]) else Fr(c["ub"])
        c["vars"] = sorted(set(c["lin"]) | {a for a, b, _ in c["quad"]} | {b for a, b, _ in c["quad"]}
                           | (tree_vars(c["nl"]) if c["nl"] is not None else set()))
    return I


def tree_vars(t):
    if t[0] == "var":
        return {t[1]}
    if t[0] == "num":
        return set()
    s = set()
    for c in t[1:]:
        s |= tree_vars(c)
    return s


def read_p1(I, name):
    vals = {}
    for line in open(os.path.join(SOL, f"{name}.p1.sol")):
        p = line.split()
        if len(p) == 2:
            vals[p[0]] = p[1]
    return [vals.get(v, "0") for v in I["names"]]   # absent = 0 (GAMS writes nonzeros only)


# ---------------- forward-mode evaluation (value, sparse gradient) ----------------
class D:
    __slots__ = ("v", "g")

    def __init__(self, v, g):
        self.v, self.g = v, g


def _add(a, b):
    g = dict(a.g)
    for j, d in b.g.items():
        g[j] = g[j] + d if j in g else d
    return D(a.v + b.v, g)


def _mul(a, b):
    g = {j: d * b.v for j, d in a.g.items()}
    for j, d in b.g.items():
        t = d * a.v
        g[j] = g[j] + t if j in g else t
    return D(a.v * b.v, g)


def _scale(a, c):
    return D(c * a.v, {j: c * d for j, d in a.g.items()})


def ev_tree(t, x, ctx, num):
    op = t[0]
    if op == "num":
        return D(num(t[1]), {})
    if op == "var":
        j, c = t[1], t[2]
        if c == "1":
            return D(x[j], {j: ctx.mpf(1)})
        cc = num(c)
        return D(cc * x[j], {j: cc})
    a = [ev_tree(c, x, ctx, num) for c in t[1:]]
    if op in ("sum", "plus"):
        s = a[0]
        for b in a[1:]:
            s = _add(s, b)
        return s
    if op in ("product", "times"):
        s = a[0]
        for b in a[1:]:
            s = _mul(s, b)
        return s
    if op == "minus":
        return _add(a[0], _scale(a[1], ctx.mpf(-1)))
    if op == "negate":
        return _scale(a[0], ctx.mpf(-1))
    if op == "square":
        return _mul(a[0], a[0])
    if op == "sin":
        (u,) = a
        return D(ctx.sin(u.v), {j: ctx.cos(u.v) * d for j, d in u.g.items()})
    if op == "cos":
        (u,) = a
        return D(ctx.cos(u.v), {j: -ctx.sin(u.v) * d for j, d in u.g.items()})
    raise NotImplementedError(op)


def ev_row(c, x, ctx, num):
    """value and gradient of the row body (constant + lin + quad + nl)"""
    s = D(num(c["constant"]), {})
    for j, a in c["lin"].items():
        s = _add(s, D(num(a) * x[j], {j: num(a)}))
    for i, j, a in c["quad"]:
        s = _add(s, _scale(_mul(D(x[i], {i: ctx.mpf(1)}), D(x[j], {j: ctx.mpf(1)})), num(a)))
    if c["nl"] is not None:
        s = _add(s, ev_tree(c["nl"], x, ctx, num))
    return s


def ev_obj(I, x, ctx, num):
    o = I["obj"]
    s = num(o["constant"])
    for j, a in o["lin"].items():
        s = s + num(a) * x[j]
    for i, j, a in o["quad"]:
        s = s + num(a) * x[i] * x[j]
    return s


def ctx_num(ctx):
    """decimal-string constants -> ctx numbers (iv: outward-rounded enclosure)"""
    cache = {}

    def num(s):
        if s not in cache:
            cache[s] = ctx.mpf(s)
        return cache[s]
    return num


def frac_of_iv_end(t):
    s, m, e, bc = t
    v = Fr(m) * (Fr(2) ** e)
    return -v if s else v


def iv_ends(x):
    """exact rational endpoints of an mpmath iv interval"""
    a, b = x._mpi_
    return frac_of_iv_end(a), frac_of_iv_end(b)


def iv_of_frac(iv, q):
    """outward enclosure of a rational"""
    return iv.mpf(q.numerator) / iv.mpf(q.denominator)
