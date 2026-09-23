"""Reviewer's own minimal OSiL reader (independent of the author's osil_eval.py).

Reads variables, objectives, constraints, linear/quadratic coefficients and
nonlinear expression trees. Unknown elements raise, so nothing is silently
dropped.
"""
import xml.etree.ElementTree as ET
from fractions import Fraction

NS = "{os.optimizationservices.org}"


def strip(tag):
    return tag[len(NS):] if tag.startswith(NS) else tag


def num(s):
    if s in ("INF", "Infinity"):
        return "INF"
    if s in ("-INF", "-Infinity"):
        return "-INF"
    return Fraction(s)


def read(path):
    root = ET.parse(path).getroot()
    data = root.find(NS + "instanceData")
    known = {"variables", "objectives", "constraints", "linearConstraintCoefficients",
             "quadraticCoefficients", "nonlinearExpressions"}
    for ch in data:
        assert strip(ch.tag) in known, strip(ch.tag)
    m = {}
    vs = data.find(NS + "variables")
    m["vars"] = []
    for v in vs:
        assert strip(v.tag) == "var"
        a = dict(v.attrib)
        extra = set(a) - {"name", "lb", "ub", "type"}
        assert not extra, extra
        m["vars"].append(dict(name=a.get("name"), type=a.get("type", "C"),
                              lb=num(a.get("lb", "0")), ub=num(a.get("ub", "INF"))))
    assert len(m["vars"]) == int(vs.attrib["numberOfVariables"])
    objs = data.find(NS + "objectives")
    m["objs"] = []
    for o in objs:
        a = dict(o.attrib)
        extra = set(a) - {"name", "maxOrMin", "numberOfObjCoef", "constant", "weight"}
        assert not extra, extra
        coefs = {}
        for c in o:
            assert strip(c.tag) == "coef"
            coefs[int(c.attrib["idx"])] = coefs.get(int(c.attrib["idx"]), 0) + Fraction(c.text)
        assert len(list(o)) == int(a.get("numberOfObjCoef", 0))
        m["objs"].append(dict(sense=a["maxOrMin"], constant=Fraction(a.get("constant", "0")),
                              lin=coefs))
    cons = data.find(NS + "constraints")
    m["cons"] = []
    for c in cons:
        a = dict(c.attrib)
        extra = set(a) - {"name", "lb", "ub", "constant"}
        assert not extra, extra
        m["cons"].append(dict(name=a.get("name"), lb=num(a.get("lb", "-INF")),
                              ub=num(a.get("ub", "INF")),
                              constant=Fraction(a.get("constant", "0")), lin={}, quad={}))
    lcc = data.find(NS + "linearConstraintCoefficients")
    if lcc is not None:
        start = [int(e.text) for e in lcc.find(NS + "start")]
        colidx = lcc.find(NS + "colIdx")
        rowidx = lcc.find(NS + "rowIdx")
        vals = [Fraction(e.text) for e in lcc.find(NS + "value")]
        if colidx is not None:  # row-major storage
            cols = [int(e.text) for e in colidx]
            for r in range(len(start) - 1):
                for k in range(start[r], start[r + 1]):
                    d = m["cons"][r]["lin"]
                    d[cols[k]] = d.get(cols[k], 0) + vals[k]
        else:
            rows = [int(e.text) for e in rowidx]
            for cidx in range(len(start) - 1):
                for k in range(start[cidx], start[cidx + 1]):
                    d = m["cons"][rows[k]]["lin"]
                    d[cidx] = d.get(cidx, 0) + vals[k]
        for e in lcc.iter():
            assert "mult" not in e.attrib and "incr" not in e.attrib, "compressed el unsupported"
    m["objquad"] = {}
    qc = data.find(NS + "quadraticCoefficients")
    if qc is not None:
        for q in qc:
            i, a, b, c = int(q.attrib["idx"]), int(q.attrib["idxOne"]), int(q.attrib["idxTwo"]), Fraction(q.attrib["coef"])
            key = tuple(sorted((a, b)))
            d = m["objquad"] if i == -1 else m["cons"][i]["quad"]
            d[key] = d.get(key, 0) + c
    m["nl"] = {}
    ne = data.find(NS + "nonlinearExpressions")
    if ne is not None:
        for nl in ne:
            i = int(nl.attrib["idx"])
            assert i not in m["nl"]
            ch = list(nl)
            assert len(ch) == 1
            m["nl"][i] = ch[0]
    return m
