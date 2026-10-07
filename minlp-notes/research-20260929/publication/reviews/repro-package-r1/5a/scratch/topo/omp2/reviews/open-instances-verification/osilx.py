"""Independent OSIL reader that keeps every numeric constant as its decimal string.

Written for the verification review; it does not reuse the authors' reader.
Constants can be converted exactly with `Fraction(s)` or enclosed with
`mpmath.iv.mpf(s)` (mpmath rounds decimal strings outward for intervals).

Conventions (OSiL 2.0): var lb default 0, ub default +INF; con lb/ub default
-INF/+INF; con and obj may carry a `constant` attribute (asserted absent or
recorded); linear coefficients use start/(rowIdx|colIdx)/value with el
mult/incr compression.
"""
import xml.etree.ElementTree as ET
from fractions import Fraction

NS = "{os.optimizationservices.org}"


def _t(e):
    return e.tag.replace(NS, "")


def _expand(el, conv):
    out = []
    for e in el:
        assert _t(e) == "el"
        m = int(e.get("mult", "1"))
        inc = e.get("incr")
        v = e.text.strip()
        if inc is None:
            out += [v] * m
        else:
            # incr is used only for integer index arrays here
            a, d = int(v), int(inc)
            out += [str(a + k * d) for k in range(m)]
    return [conv(x) for x in out]


def _tree(e):
    t = _t(e)
    if t == "number":
        assert e.get("type") in (None, "real"), e.attrib
        return ("num", e.get("value"))
    if t == "variable":
        return ("var", int(e.get("idx")), e.get("coef", "1"))
    return (t,) + tuple(_tree(c) for c in e)


def read(path):
    root = ET.parse(path).getroot()
    d = root.find(NS + "instanceData")
    V = d.find(NS + "variables")
    names, lb, ub, vt = [], [], [], []
    for v in V:
        assert _t(v) == "var"
        names.append(v.get("name"))
        typ = v.get("type", "C")
        vt.append(typ)
        lb.append(v.get("lb", "0"))
        ub.append(v.get("ub", "1" if typ == "B" else "INF"))
    assert len(names) == int(V.get("numberOfVariables"))
    objs = d.find(NS + "objectives")
    assert len(objs) == 1
    o = objs[0]
    obj = dict(sense=o.get("maxOrMin", "min"), constant=o.get("constant", "0"),
               weight=o.get("weight", "1"),
               lin={int(c.get("idx")): c.text.strip() for c in o})
    assert len(obj["lin"]) == int(o.get("numberOfObjCoef", "0"))
    C = d.find(NS + "constraints")
    cons = []
    for c in (C if C is not None else []):
        cons.append(dict(name=c.get("name"), lb=c.get("lb", "-INF"),
                         ub=c.get("ub", "INF"), constant=c.get("constant", "0"),
                         lin={}, quad=[], nl=None))
    L = d.find(NS + "linearConstraintCoefficients")
    if L is not None:
        start = _expand(L.find(NS + "start"), int)
        vals = _expand(L.find(NS + "value"), str)
        ri = L.find(NS + "rowIdx")
        ci = L.find(NS + "colIdx")
        if ri is not None:  # column-major
            idx = _expand(ri, int)
            for col in range(len(start) - 1):
                for k in range(start[col], start[col + 1]):
                    assert col not in cons[idx[k]]["lin"]
                    cons[idx[k]]["lin"][col] = vals[k]
        else:  # row-major
            idx = _expand(ci, int)
            assert len(start) == len(cons) + 1, (len(start), len(cons))
            for r in range(len(start) - 1):
                for k in range(start[r], start[r + 1]):
                    assert idx[k] not in cons[r]["lin"]
                    cons[r]["lin"][idx[k]] = vals[k]
        assert len(vals) == int(L.get("numberOfValues"))
    objquad = []
    Q = d.find(NS + "quadraticCoefficients")
    if Q is not None:
        for q in Q:
            r = int(q.get("idx"))
            term = (int(q.get("idxOne")), int(q.get("idxTwo")), q.get("coef", "1"))
            (objquad if r == -1 else cons[r]["quad"]).append(term)
    objnl = None
    N = d.find(NS + "nonlinearExpressions")
    if N is not None:
        for e in N:
            r = int(e.get("idx"))
            assert len(e) == 1
            tr = _tree(e[0])
            if r == -1:
                objnl = tr
            else:
                assert cons[r]["nl"] is None
                cons[r]["nl"] = tr
    obj["quad"] = objquad
    obj["nl"] = objnl
    return dict(names=names, lb=lb, ub=ub, vt=vt, obj=obj, cons=cons)


def isinf(s):
    return s.upper() in ("INF", "-INF", "+INF")


def F(s):
    """exact rational value of a decimal string"""
    return Fraction(s)


# ---------------- evaluation with a pluggable number type -----------------
def ev_tree(t, x, num, fns):
    op = t[0]
    if op == "num":
        return num(t[1])
    if op == "var":
        c = t[2]
        return x[t[1]] if c == "1" else num(c) * x[t[1]]
    a = [ev_tree(c, x, num, fns) for c in t[1:]]
    if op in ("sum", "plus"):
        s = a[0]
        for b in a[1:]:
            s = s + b
        return s
    if op in ("product", "times"):
        s = a[0]
        for b in a[1:]:
            s = s * b
        return s
    if op == "minus":
        return a[0] - a[1]
    if op == "negate":
        return -a[0]
    if op == "divide":
        return a[0] / a[1]
    if op == "square":
        return a[0] * a[0]
    if op in fns:
        return fns[op](*a)
    raise NotImplementedError(op)


def ev_row(row, x, num, fns):
    s = num(row.get("constant", "0"))
    for j, c in row["lin"].items():
        s = s + num(c) * x[j]
    for i, j, c in row["quad"]:
        s = s + num(c) * x[i] * x[j]
    if row["nl"] is not None:
        s = s + ev_tree(row["nl"], x, num, fns)
    return s
