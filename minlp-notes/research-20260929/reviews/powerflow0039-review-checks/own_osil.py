"""Reviewer's own OSIL reader (ElementTree; no code shared with osilx/pf_model).

All numbers are kept as exact Fractions of the decimal strings in the file.
Returns dict with
  names[j], vlb[j], vub[j]                          (None = infinite)
  obj: const, lin {j: c}, quad {(i, j): c}, nl       (nl tree or None)
  cons[r]: name, lb, ub, const, lin {j: c}, quad {(i, j): c}, nl
nl trees are nested tuples: ('sum', ...), ('product', ...), ('square', t),
('cos', t), ('sin', t), ('var', j, coef), ('num', value).
"""
import xml.etree.ElementTree as ET
from fractions import Fraction as Fr

NS = "{os.optimizationservices.org}"


def num(s):
    s = s.strip()
    if s in ("INF", "+INF", "Infinity"):
        return None
    if s in ("-INF", "-Infinity"):
        return None
    return Fr(s)


def _expand(elem, integer=True):
    """expand an OSiL array element list with mult / incr attributes"""
    out = []
    for el in elem.findall(NS + "el"):
        mult = int(el.get("mult", "1"))
        incr = el.get("incr")
        v = int(el.text) if integer else Fr(el.text.strip())
        inc = (int(incr) if integer else Fr(incr)) if incr is not None else 0
        for t in range(mult):
            out.append(v + t * inc)
    return out


def _tree(e):
    tag = e.tag[len(NS):]
    if tag == "variable":
        return ("var", int(e.get("idx")), Fr(e.get("coef", "1")))
    if tag == "number":
        return ("num", Fr(e.get("value")))
    kids = [_tree(c) for c in e]
    if tag in ("sum", "product"):
        return (tag,) + tuple(kids)
    if tag in ("square", "cos", "sin"):
        assert len(kids) == 1
        return (tag, kids[0])
    raise ValueError(tag)


def read(path):
    root = ET.parse(path).getroot()
    d = root.find(NS + "instanceData")
    vs = d.find(NS + "variables").findall(NS + "var")
    names = [v.get("name") for v in vs]
    # OSiL defaults: lb = 0, ub = INF
    vlb = [num(v.get("lb", "0")) if v.get("lb", "0") not in ("-INF",) else None for v in vs]
    vub = [num(v.get("ub", "INF")) for v in vs]
    for v in vs:
        assert v.get("type", "C") == "C"
    o = d.find(NS + "objectives").findall(NS + "obj")
    assert len(o) == 1
    o = o[0]
    obj = dict(sense=o.get("maxOrMin"), const=Fr(o.get("constant", "0")),
               lin={int(c.get("idx")): Fr(c.text.strip()) for c in o.findall(NS + "coef")},
               quad={}, nl=None)
    cs = d.find(NS + "constraints").findall(NS + "con")
    cons = []
    for c in cs:
        lb = c.get("lb", "-INF")
        ub = c.get("ub", "INF")
        cons.append(dict(name=c.get("name"), lb=None if lb == "-INF" else Fr(lb),
                         ub=None if ub == "INF" else Fr(ub), const=Fr(c.get("constant", "0")),
                         lin={}, quad={}, nl=None))
    lc = d.find(NS + "linearConstraintCoefficients")
    if lc is not None:
        start = _expand(lc.find(NS + "start"))
        vals = _expand(lc.find(NS + "value"), integer=False)
        col = lc.find(NS + "colIdx")
        assert col is not None and lc.find(NS + "rowIdx") is None
        idx = _expand(col)
        assert len(start) == len(cons) + 1 and len(idx) == len(vals) == start[-1]
        for r in range(len(cons)):
            for t in range(start[r], start[r + 1]):
                j = idx[t]
                cons[r]["lin"][j] = cons[r]["lin"].get(j, Fr(0)) + vals[t]
    qc = d.find(NS + "quadraticCoefficients")
    if qc is not None:
        for q in qc.findall(NS + "qTerm"):
            r, i, j, c = int(q.get("idx")), int(q.get("idxOne")), int(q.get("idxTwo")), Fr(q.get("coef"))
            key = (min(i, j), max(i, j))
            tgt = obj["quad"] if r == -1 else cons[r]["quad"]
            tgt[key] = tgt.get(key, Fr(0)) + c
    nle = d.find(NS + "nonlinearExpressions")
    if nle is not None:
        for e in nle.findall(NS + "nl"):
            r = int(e.get("idx"))
            (ch,) = list(e)
            t = _tree(ch)
            if r == -1:
                assert obj["nl"] is None
                obj["nl"] = t
            else:
                assert cons[r]["nl"] is None
                cons[r]["nl"] = t
    return dict(names=names, vlb=vlb, vub=vub, obj=obj, cons=cons)


def ev_tree(t, z, mp):
    """evaluate a tree at z (list of mpf) with mpmath"""
    op = t[0]
    if op == "var":
        return (mp.mpf(t[2].numerator) / t[2].denominator) * z[t[1]]
    if op == "num":
        return mp.mpf(t[1].numerator) / t[1].denominator
    if op == "sum":
        return mp.fsum(ev_tree(c, z, mp) for c in t[1:])
    if op == "product":
        p = mp.mpf(1)
        for c in t[1:]:
            p *= ev_tree(c, z, mp)
        return p
    if op == "square":
        v = ev_tree(t[1], z, mp)
        return v * v
    if op == "cos":
        return mp.cos(ev_tree(t[1], z, mp))
    if op == "sin":
        return mp.sin(ev_tree(t[1], z, mp))
    raise ValueError(op)


def row_value(I, r, z, mp):
    c = I["cons"][r]
    q = lambda F: mp.mpf(F.numerator) / F.denominator
    v = q(c["const"]) + mp.fsum(q(a) * z[j] for j, a in c["lin"].items())
    v += mp.fsum(q(a) * z[i] * z[j] for (i, j), a in c["quad"].items())
    if c["nl"] is not None:
        v += ev_tree(c["nl"], z, mp)
    return v


def obj_value(I, z, mp):
    o = I["obj"]
    q = lambda F: mp.mpf(F.numerator) / F.denominator
    v = q(o["const"]) + mp.fsum(q(a) * z[j] for j, a in o["lin"].items())
    v += mp.fsum(q(a) * z[i] * z[j] for (i, j), a in o["quad"].items())
    if o["nl"] is not None:
        v += ev_tree(o["nl"], z, mp)
    return v
