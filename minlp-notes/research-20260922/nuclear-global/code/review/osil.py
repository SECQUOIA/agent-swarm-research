"""Reviewer's exact OSiL reader (independent of the author's and the earlier reviewer's code).

read(name) -> dict with
  vars: list of dict(name, type, lb, ub)   (Fraction or None for infinite)
  obj:  dict(sense, lin{j: Fraction})
  rows: list of dict(name, lb, ub, lin{j: F}, quad{(j1, j2) sorted: F})
Only the OSiL features used by the nuclear* files are accepted; anything else raises.
"""
import os
import xml.etree.ElementTree as ET
from fractions import Fraction as F

DIR = os.path.expanduser("~/.cache/minlplib/minlplib/osil")
NS = "{os.optimizationservices.org}"


def num(s):
    s = s.strip()
    if s in ("INF", "+INF"):
        return None
    if s == "-INF":
        return None
    return F(s)


def expand(el, integer=True):
    out = []
    for e in el.findall(NS + "el"):
        extra = set(e.attrib) - {"mult", "incr"}
        assert not extra, extra
        mult = int(e.get("mult", "1"))
        v = int(e.text) if integer else F(e.text.strip())
        inc = int(e.get("incr", "0")) if integer else F(e.get("incr", "0"))
        out += [v + r * inc for r in range(mult)]
    return out


def read(name):
    root = ET.parse(os.path.join(DIR, name + ".osil")).getroot()
    d = root.find(NS + "instanceData")
    allowed = {"variables", "objectives", "constraints", "linearConstraintCoefficients", "quadraticCoefficients"}
    assert {c.tag.replace(NS, "") for c in d} <= allowed, [c.tag for c in d]
    V = []
    for v in d.find(NS + "variables"):
        assert set(v.attrib) <= {"name", "type", "lb", "ub"}, v.attrib
        typ = v.get("type", "C"); assert typ in ("C", "B")
        lb = v.get("lb", "0"); ub = v.get("ub", "INF")
        V.append(dict(name=v.get("name"), type=typ,
                      lb=None if lb == "-INF" else F(lb), ub=None if ub == "INF" else F(ub)))
    objs = d.find(NS + "objectives").findall(NS + "obj")
    assert len(objs) == 1
    o = objs[0]
    assert set(o.attrib) <= {"maxOrMin", "name", "numberOfObjCoef"}
    obj = dict(sense=o.get("maxOrMin"), lin={int(c.get("idx")): F(c.text) for c in o.findall(NS + "coef")})
    rows = []
    for c in d.find(NS + "constraints"):
        assert set(c.attrib) <= {"name", "lb", "ub"}, c.attrib   # no 'constant' attribute in these files
        rows.append(dict(name=c.get("name"), lb=None if c.get("lb") in (None, "-INF") else F(c.get("lb")),
                         ub=None if c.get("ub") in (None, "INF") else F(c.get("ub")), lin={}, quad={}))
    L = d.find(NS + "linearConstraintCoefficients")
    assert L.find(NS + "rowIdx") is None
    start = expand(L.find(NS + "start")); col = expand(L.find(NS + "colIdx"))
    val = expand(L.find(NS + "value"), integer=False)
    assert len(start) == len(rows) + 1 and len(col) == len(val) == start[-1]
    for r in range(len(rows)):
        for q in range(start[r], start[r + 1]):
            j = col[q]; assert j not in rows[r]["lin"]
            rows[r]["lin"][j] = val[q]
    Q = d.find(NS + "quadraticCoefficients")
    for t in Q.findall(NS + "qTerm"):
        r, a, b = int(t.get("idx")), int(t.get("idxOne")), int(t.get("idxTwo"))
        assert r >= 0  # no quadratic objective
        key = (min(a, b), max(a, b))
        rows[r]["quad"][key] = rows[r]["quad"].get(key, 0) + F(t.get("coef", "1"))
    for r in rows:
        r["lin"] = {j: v for j, v in r["lin"].items() if v != 0}
        r["quad"] = {k: v for k, v in r["quad"].items() if v != 0}
    return dict(vars=V, obj=obj, rows=rows)
