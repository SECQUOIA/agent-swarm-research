"""Minimal OSiL reader that keeps every numeric constant as its decimal string,
plus an outward-rounded interval evaluator (mpmath.iv) for rows and objective.

Written for this track. It supports the OSiL features used by the lnts files:
variables (lb/ub/type with OSiL defaults lb=0, ub=INF, type C), one linear
objective, constraints (lb/ub/constant), linearConstraintCoefficients in
start/colIdx/value form (with mult/incr), quadraticCoefficients (qTerm), and
nonlinear expressions built from sum, product, cos, sin, number, variable.
Anything else raises an error, so an unsupported feature cannot be silently
ignored.
"""
import xml.etree.ElementTree as ET
from fractions import Fraction

from mpmath import iv

NS = "{os.optimizationservices.org}"
INF = ("INF", "+INF", "Infinity", "inf")


def _tag(e):
    return e.tag.replace(NS, "")


def _expand(parent, numeric):
    """Expand <el mult= incr=> lists. numeric=int for indices, str for values."""
    out = []
    for el in parent:
        assert _tag(el) == "el", _tag(el)
        mult = int(el.get("mult", "1"))
        incr = el.get("incr")
        txt = el.text.strip()
        if numeric is int:
            v0, d = int(txt), int(incr or "0")
            out += [v0 + k * d for k in range(mult)]
        else:
            assert incr is None, "incr on values not supported"
            out += [txt] * mult
    return out


def _nl(e):
    t = _tag(e)
    if t == "number":
        assert set(e.attrib) <= {"value"}, e.attrib
        return ("num", e.get("value"))
    if t == "variable":
        assert set(e.attrib) <= {"idx", "coef"}, e.attrib
        return ("var", int(e.get("idx")), e.get("coef", "1"))
    if t in ("sum", "product", "cos", "sin"):
        assert not e.attrib, e.attrib
        kids = tuple(_nl(k) for k in e)
        if t in ("cos", "sin"):
            assert len(kids) == 1
        return (t,) + kids
    raise ValueError(f"unsupported nonlinear node {t}")


def read(path):
    root = ET.parse(path).getroot()
    data = root.find(NS + "instanceData")
    known = {"variables", "objectives", "constraints", "linearConstraintCoefficients",
             "quadraticCoefficients", "nonlinearExpressions"}
    for child in data:
        assert _tag(child) in known, _tag(child)
    names, lb, ub, vt = [], [], [], []
    for v in data.find(NS + "variables"):
        assert set(v.attrib) <= {"name", "lb", "ub", "type"}, v.attrib
        names.append(v.get("name"))
        lb.append(v.get("lb", "0"))
        ub.append(v.get("ub", "INF"))
        vt.append(v.get("type", "C"))
    objs = list(data.find(NS + "objectives"))
    assert len(objs) == 1
    o = objs[0]
    assert set(o.attrib) <= {"maxOrMin", "name", "numberOfObjCoef"}, o.attrib  # no constant/weight
    obj = dict(sense=o.get("maxOrMin", "min"), lin={}, quad=[], nl=None)
    for cf in o:
        assert _tag(cf) == "coef"
        obj["lin"][int(cf.get("idx"))] = cf.text.strip()
    cons = []
    for c in data.find(NS + "constraints"):
        assert set(c.attrib) <= {"name", "lb", "ub"}, c.attrib  # no constant attribute
        cons.append(dict(name=c.get("name"), lb=c.get("lb", "-INF"), ub=c.get("ub", "INF"),
                         lin={}, quad=[], nl=None))
    lcc = data.find(NS + "linearConstraintCoefficients")
    if lcc is not None:
        assert lcc.find(NS + "rowIdx") is None, "column-major form not supported"
        start = _expand(lcc.find(NS + "start"), int)
        col = _expand(lcc.find(NS + "colIdx"), int)
        val = _expand(lcc.find(NS + "value"), str)
        assert len(start) == len(cons) + 1 and len(col) == len(val) == start[-1]
        for r in range(len(cons)):
            for k in range(start[r], start[r + 1]):
                assert col[k] not in cons[r]["lin"]
                cons[r]["lin"][col[k]] = val[k]
    qc = data.find(NS + "quadraticCoefficients")
    if qc is not None:
        for q in qc:
            r = int(q.get("idx"))
            tgt = obj if r == -1 else cons[r]
            tgt["quad"].append((int(q.get("idxOne")), int(q.get("idxTwo")), q.get("coef", "1")))
    nle = data.find(NS + "nonlinearExpressions")
    if nle is not None:
        for e in nle:
            r = int(e.get("idx"))
            kids = list(e)
            assert len(kids) == 1
            tgt = obj if r == -1 else cons[r]
            assert tgt["nl"] is None
            tgt["nl"] = _nl(kids[0])
    return dict(names=names, lb=lb, ub=ub, vt=vt, obj=obj, cons=cons)


def isinf(s):
    return s.lstrip("-+") in ("INF", "Infinity", "inf")


def frac(s):
    """Exact rational value of a decimal string."""
    return Fraction(s)


def ivnum(s):
    """Outward-rounded interval enclosing the exact decimal value s."""
    q = Fraction(s)
    return iv.mpf(q.numerator) / q.denominator


def ev_nl(t, X):
    k = t[0]
    if k == "num":
        return ivnum(t[1])
    if k == "var":
        return ivnum(t[2]) * X[t[1]]
    if k == "sum":
        s = iv.mpf(0)
        for u in t[1:]:
            s = s + ev_nl(u, X)
        return s
    if k == "product":
        p = iv.mpf(1)
        for u in t[1:]:
            p = p * ev_nl(u, X)
        return p
    if k == "cos":
        return iv.cos(ev_nl(t[1], X))
    if k == "sin":
        return iv.sin(ev_nl(t[1], X))
    raise ValueError(k)


def ev_row(row, X):
    """Interval enclosure of lin + quad + nl part of a row (or objective) over box X."""
    s = iv.mpf(0)
    for j, c in row["lin"].items():
        s = s + ivnum(c) * X[j]
    for i, j, c in row["quad"]:
        s = s + ivnum(c) * X[i] * X[j]
    if row["nl"] is not None:
        s = s + ev_nl(row["nl"], X)
    return s
