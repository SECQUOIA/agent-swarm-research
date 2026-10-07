"""Independent OSIL reader (reviewer code; does not use osilx or pfmodel).

Everything numeric is kept as exact Fractions parsed from the decimal strings.
Row i of the model reads  lb_i <= constant_i + lin_i(x) + quad_i(x) + nl_i(x) <= ub_i.
OSiL defaults: var lb = 0, ub = +INF, type C; con lb = -INF, ub = +INF.
"""
import xml.etree.ElementTree as ET
from fractions import Fraction as Fr

NS = "{os.optimizationservices.org}"
INF = None   # marker for an infinite bound


def _bound(s):
    if s is None:
        return "default"
    if s in ("INF", "-INF", "Infinity", "-Infinity"):
        return INF
    return Fr(s)


def _expand(parent, conv):
    """expand <el mult=.. incr=..>v</el> lists"""
    out = []
    for el in parent.findall(NS + "el"):
        v = conv(el.text.strip())
        mult = int(el.get("mult", "1"))
        incr = conv(el.get("incr", "0"))
        for k in range(mult):
            out.append(v + k * incr)
    return out


def _tree(e):
    tag = e.tag[len(NS):]
    if tag == "variable":
        return ("var", int(e.get("idx")), Fr(e.get("coef", "1")))
    if tag == "number":
        return ("num", Fr(e.get("value")))
    kids = [_tree(c) for c in e]
    if tag in ("sum", "product", "square", "sin", "cos"):
        if tag in ("square", "sin", "cos"):
            assert len(kids) == 1
        return (tag, *kids)
    raise NotImplementedError(tag)


def read(path):
    root = ET.parse(path).getroot()
    d = root.find(NS + "instanceData")
    V = d.find(NS + "variables")
    names, lb, ub, vtype = [], [], [], []
    for v in V.findall(NS + "var"):
        names.append(v.get("name"))
        a, b = _bound(v.get("lb")), _bound(v.get("ub"))
        lb.append(Fr(0) if a == "default" else a)
        ub.append(INF if b == "default" else b)
        vtype.append(v.get("type", "C"))
    assert len(names) == int(V.get("numberOfVariables"))
    n = len(names)
    O = d.find(NS + "objectives").findall(NS + "obj")
    assert len(O) == 1
    o = O[0]
    obj = dict(sense=o.get("maxOrMin", "min"), weight=o.get("weight", "1"),
               constant=Fr(o.get("constant", "0")), lin={}, quad=[], nl=None)
    for c in o.findall(NS + "coef"):
        j = int(c.get("idx"))
        assert j not in obj["lin"]
        obj["lin"][j] = Fr(c.text.strip())
    assert len(obj["lin"]) == int(o.get("numberOfObjCoef", "0"))
    C = d.find(NS + "constraints")
    cons = []
    for c in C.findall(NS + "con"):
        a, b = _bound(c.get("lb")), _bound(c.get("ub"))
        cons.append(dict(name=c.get("name"), lb=INF if a == "default" else a, ub=INF if b == "default" else b,
                         constant=Fr(c.get("constant", "0")), lin={}, quad=[], nl=None))
    assert len(cons) == int(C.get("numberOfConstraints"))
    L = d.find(NS + "linearConstraintCoefficients")
    if L is not None:
        start = _expand(L.find(NS + "start"), int)
        assert L.find(NS + "rowIdx") is None, "only row-major (colIdx) storage handled"
        col = _expand(L.find(NS + "colIdx"), int)
        val = _expand(L.find(NS + "value"), Fr)
        assert len(start) == len(cons) + 1 and len(col) == len(val) == int(L.get("numberOfValues")) == start[-1]
        for i in range(len(cons)):
            for k in range(start[i], start[i + 1]):
                j = col[k]
                assert 0 <= j < n and j not in cons[i]["lin"], "duplicate linear entry"
                cons[i]["lin"][j] = val[k]
    Q = d.find(NS + "quadraticCoefficients")
    if Q is not None:
        qt = Q.findall(NS + "qTerm")
        assert len(qt) == int(Q.get("numberOfQuadraticTerms"))
        for q in qt:
            i, a, b = int(q.get("idx")), int(q.get("idxOne")), int(q.get("idxTwo"))
            term = (a, b, Fr(q.get("coef", "1")))
            (obj if i == -1 else cons[i])["quad"].append(term)
    N = d.find(NS + "nonlinearExpressions")
    if N is not None:
        nls = N.findall(NS + "nl")
        assert len(nls) == int(N.get("numberOfNonlinearExpressions"))
        for e in nls:
            i = int(e.get("idx"))
            (ch,) = list(e)
            tgt = obj if i == -1 else cons[i]
            assert tgt["nl"] is None, "two nl blocks for one row"
            tgt["nl"] = _tree(ch)
    # leftovers that this reader does not handle must not exist
    for tag in ("matrices", "cones", "timeDomain", "matrixProgramming"):
        assert d.find(NS + tag) is None, tag
    return dict(names=names, lb=lb, ub=ub, vtype=vtype, obj=obj, cons=cons)


def row_vars(c):
    s = set(c["lin"]) | {a for a, b, _ in c["quad"]} | {b for a, b, _ in c["quad"]}

    def walk(t):
        if t[0] == "var":
            s.add(t[1])
        elif t[0] != "num":
            for k in t[1:]:
                walk(k)
    if c["nl"] is not None:
        walk(c["nl"])
    return s
