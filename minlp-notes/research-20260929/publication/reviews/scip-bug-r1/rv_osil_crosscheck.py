#!/usr/bin/env python3
"""Reviewer's cross-check: every constraint of a waterno2 period CIP file is an exact copy of the
same-named constraint of the cached MINLPLib OSIL file, and CIP variable bounds equal or lie
inside the OSIL bounds. Exact rationals from the decimal text; no track code.

Usage: rv_osil_crosscheck.py OSIL CIP [CIP ...]
"""
import re
import sys
import xml.etree.ElementTree as ET
from fractions import Fraction as F

sys.path.insert(0, __import__("os").path.dirname(__file__))
from rv_cip_exact import parse_cip

NS = "{os.optimizationservices.org}"


def expand(el):
    out = []
    for e in el.findall(NS + "el"):
        mult = int(e.get("mult", "1"))
        incr = e.get("incr")
        v = e.text.strip()
        if incr is None:
            out += [v] * mult
        else:
            base = int(v)
            out += [str(base + k * int(incr)) for k in range(mult)]
    return out


def load_osil(path):
    root = ET.parse(path).getroot()
    d = root.find(NS + "instanceData")
    vs = d.find(NS + "variables").findall(NS + "var")
    vnames = [v.get("name") for v in vs]
    vinfo = {}
    for v in vs:
        t = v.get("type", "C")
        lb = v.get("lb", "0")
        ub = v.get("ub", "INF")
        vinfo[v.get("name")] = (t, None if lb == "-INF" else F(lb), None if ub == "INF" else F(ub))
    cs = d.find(NS + "constraints").findall(NS + "con")
    cnames = [c.get("name") for c in cs]
    cb = [(None if c.get("lb") in (None, "-INF") else F(c.get("lb")),
           None if c.get("ub") in (None, "INF") else F(c.get("ub"))) for c in cs]
    poly = [dict() for _ in cs]
    lcc = d.find(NS + "linearConstraintCoefficients")
    start = [int(x) for x in expand(lcc.find(NS + "start"))]
    col = [int(x) for x in expand(lcc.find(NS + "colIdx"))]
    val = [F(x) for x in expand(lcc.find(NS + "value"))]
    assert lcc.find(NS + "rowIdx") is None
    for r in range(len(start) - 1):
        for k in range(start[r], start[r + 1]):
            key = (vnames[col[k]],)
            poly[r][key] = poly[r].get(key, F(0)) + val[k]
    q = d.find(NS + "quadraticCoefficients")
    for t in q.findall(NS + "qTerm"):
        r = int(t.get("idx"))
        key = tuple(sorted([vnames[int(t.get("idxOne"))], vnames[int(t.get("idxTwo"))]]))
        poly[r][key] = poly[r].get(key, F(0)) + F(t.get("coef"))
    for nl in d.find(NS + "nonlinearExpressions").findall(NS + "nl"):
        r = int(nl.get("idx"))
        p = nl[0]
        assert p.tag == NS + "power", p.tag
        var, num = p[0], p[1]
        assert var.tag == NS + "variable" and num.tag == NS + "number"
        assert var.get("coef", "1") == "1"
        k = int(num.get("value"))
        key = tuple([vnames[int(var.get("idx"))]] * k)
        poly[r][key] = poly[r].get(key, F(0)) + 1
    return vinfo, {cnames[i]: (poly[i], cb[i]) for i in range(len(cs))}


def main():
    vinfo, cons = load_osil(sys.argv[1])
    for cip in sys.argv[2:]:
        var, order, ccons = parse_cip(cip)
        nd = 0
        msgs = []
        for cname, kind, terms, rel, rhs in ccons:
            d = {}
            for c, ns in terms:
                k = tuple(sorted(ns))
                d[k] = d.get(k, F(0)) + c
            d = {k: v for k, v in d.items() if v != 0}
            base = cname
            if "_" in cname:
                base = cname.split("_")[0]  # one side of a ranged OSIL row (suffix _lo/_hi/_up/...)
            if base not in cons:
                msgs.append("constraint %s not in OSIL" % cname)
                nd += 1
                continue
            op, (lo, up) = cons[base]
            op = {k: v for k, v in op.items() if v != 0}
            want = {"<=": (None, rhs), ">=": (rhs, None), "==": (rhs, rhs)}[rel]
            if base != cname:
                side_ok = (rel == ">=" and lo == rhs) or (rel == "<=" and up == rhs)
                if not (op == d and side_ok):
                    msgs.append("ranged side %s differs from OSIL" % cname)
                    nd += 1
                continue
            if op != d or (lo, up) != want:
                # allow a row negated
                neg = {k: -v for k, v in d.items()}
                wantn = {"<=": (-rhs, None), ">=": (None, -rhs), "==": (-rhs, -rhs)}[rel]
                if not (op == neg and (lo, up) == wantn):
                    msgs.append("constraint %s differs from OSIL" % cname)
                    nd += 1
        tighter = []
        wider = []
        typed = []
        for n in order:
            t, lo, up = vinfo[n]
            v = var[n]
            if (t == "B") != (v["type"] == "binary"):
                typed.append(n)
            if t == "B":
                lo, up = F(0), F(1)
            l2, u2 = v["lb"], v["ub"]
            le = (lo is None and l2 is None) or (lo is not None and l2 is not None and l2 == lo)
            ue = (up is None and u2 is None) or (up is not None and u2 is not None and u2 == up)
            if le and ue:
                continue
            inside = (lo is None or (l2 is not None and l2 >= lo)) and (up is None or (u2 is not None and u2 <= up))
            (tighter if inside else wider).append((n, (lo, up), (l2, u2)))
        print("%s: %d constraints, %d differ from OSIL; vars %d, type mismatches %d, bounds tighter than OSIL %d, bounds outside OSIL %d"
              % (cip, len(ccons), nd, len(order), len(typed), len(tighter), len(wider)))
        for m in msgs[:5]:
            print("   ", m)
        for t in (tighter[:6]):
            print("    tighter:", t[0], "osil", [str(x) for x in t[1]], "cip", [str(x) for x in t[2]])
        for t in wider[:6]:
            print("    OUTSIDE:", t[0], "osil", [str(x) for x in t[1]], "cip", [str(x) for x in t[2]])


if __name__ == "__main__":
    main()
