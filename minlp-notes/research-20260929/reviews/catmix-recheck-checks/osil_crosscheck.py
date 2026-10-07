"""Cross-check of the shared OSIL reader (osilx.py) on the catmix files with an independent
regex parse of the raw XML text. The authors and the previous verifier use the same reader,
so a reader bug would affect both; this compares every bound, objective term, linear
coefficient and quadratic term the reader returns against the regex parse (as decimal strings).

usage: osil_crosscheck.py N [N ...]
"""
import os
import re
import sys
from collections import Counter

import osilx

OSIL = os.path.join(os.path.expanduser("~/.cache/minlplib/minlplib/osil"), "catmix%d.osil")


def attrs(tag):
    return dict(re.findall(r'(\w+)="([^"]*)"', tag))


def expand(section):
    out = []
    for a, v in re.findall(r"<el([^>]*)>([^<]*)</el>", section):
        at = attrs(a)
        m = int(at.get("mult", "1"))
        if "incr" in at:
            out += [str(int(v) + k * int(at["incr"])) for k in range(m)]
        else:
            out += [v.strip()] * m
    return out


def regex_parse(text):
    assert "<nonlinearExpressions" not in text and "<integer" not in text.lower()
    vars_ = [attrs(t) for t in re.findall(r"<var\b([^>]*)/>", text)]
    nv = int(re.search(r'<variables numberOfVariables="(\d+)"', text).group(1))
    assert len(vars_) == nv and all("mult" not in v for v in vars_)
    lb = [v.get("lb", "0") for v in vars_]
    ub = [v.get("ub", "INF") for v in vars_]
    ty = {v.get("type", "C") for v in vars_}
    obj_tag = re.search(r"<obj\b([^>]*)>(.*?)</obj>", text, re.S)
    oa = attrs(obj_tag.group(1))
    olin = {int(i): v.strip() for i, v in re.findall(r'<coef idx="(\d+)">([^<]*)</coef>', obj_tag.group(2))}
    cons = [attrs(t) for t in re.findall(r"<con\b([^>]*)/>", text)]
    nc = int(re.search(r'<constraints numberOfConstraints="(\d+)"', text).group(1))
    assert len(cons) == nc and all("mult" not in c for c in cons)
    L = re.search(r"<linearConstraintCoefficients[^>]*>(.*?)</linearConstraintCoefficients>", text, re.S).group(1)
    start = [int(s) for s in expand(re.search(r"<start>(.*?)</start>", L, re.S).group(1))]
    col = [int(s) for s in expand(re.search(r"<colIdx>(.*?)</colIdx>", L, re.S).group(1))]
    val = expand(re.search(r"<value>(.*?)</value>", L, re.S).group(1))
    assert len(start) == nc + 1 and len(col) == len(val) == start[-1]
    lin = [{col[k]: val[k] for k in range(start[r], start[r + 1])} for r in range(nc)]
    quad = [[] for _ in range(nc)]
    for t in re.findall(r"<qTerm\b([^>]*)/>", text):
        a = attrs(t)
        quad[int(a["idx"])].append((int(a["idxOne"]), int(a["idxTwo"]), a.get("coef", "1")))
    nq = int(re.search(r'numberOfQuadraticTerms="(\d+)"', text).group(1))
    assert sum(len(q) for q in quad) == nq
    return dict(lb=lb, ub=ub, types=ty, obj=(oa.get("maxOrMin", "min"), oa.get("constant", "0"), olin),
                con_bounds=[(c.get("lb", "-INF"), c.get("ub", "INF"), c.get("constant", "0")) for c in cons],
                lin=lin, quad=quad)


for N in [int(v) for v in sys.argv[1:]]:
    text = open(OSIL % N).read()
    R = regex_parse(text)
    m = osilx.read(OSIL % N)
    assert R["lb"] == m["lb"] and R["ub"] == m["ub"] and R["types"] == set(m["vt"]) == {"C"}
    o = m["obj"]
    assert R["obj"] == (o["sense"], o["constant"], o["lin"]) and o["quad"] == [] and o["nl"] is None
    assert R["con_bounds"] == [(c["lb"], c["ub"], c["constant"]) for c in m["cons"]]
    assert R["lin"] == [c["lin"] for c in m["cons"]]
    assert all(Counter(R["quad"][r]) == Counter(c["quad"]) and c["nl"] is None for r, c in enumerate(m["cons"]))
    coefs = sorted({q[2] for qs in R["quad"] for q in qs} | {v for d in R["lin"] for v in d.values()})
    print("N=%d: osilx.read agrees with the regex parse (%d vars, %d rows, %d linear, %d quadratic terms); "
          "objective %s, constant %s; distinct coefficients %s" % (
              N, len(R["lb"]), len(R["lin"]), sum(len(d) for d in R["lin"]), sum(len(q) for q in R["quad"]),
              R["obj"][2], R["obj"][1], coefs), flush=True)
