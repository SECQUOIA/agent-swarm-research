"""Reviewer's own OSiL reader (exact Fractions). Written for this review; shares no code with
the track's osil_exact.py or the earlier verifier's osilx.py.

Returns a dict with
  vars: list of (name, lb, ub, type)   lb/ub are Fraction or None (= -INF / +INF)
  obj:  (sense, linear {j: c}, constant)
  cons: list of (name, lb, ub, constant)
  lin:  list per row of {j: c}
  quad: dict idx -> list of (i, j, c)     idx -1 = objective
  nl:   dict idx -> ElementTree element (expression root)
"""
import xml.etree.ElementTree as ET
from fractions import Fraction

NS = "{os.optimizationservices.org}"


def num(s):
    s = s.strip()
    if s in ("INF", "+INF", "Infinity"):
        return "INF"
    if s in ("-INF", "-Infinity"):
        return "-INF"
    return Fraction(s)


def expand(el_parent, is_int=True):
    """Expand an OSiL array with <el mult incr> compression."""
    out = []
    for el in el_parent.findall(NS + "el"):
        mult = int(el.get("mult", "1"))
        if is_int:
            v = int(el.text)
            inc = int(el.get("incr", "0"))
        else:
            v = Fraction(el.text.strip())
            inc = Fraction(el.get("incr", "0"))
        for k in range(mult):
            out.append(v + k * inc)
    return out


def read(path):
    root = ET.parse(path).getroot()
    data = root.find(NS + "instanceData")
    V = data.find(NS + "variables")
    vars_ = []
    for v in V.findall(NS + "var"):
        lb = num(v.get("lb", "0"))
        ub = num(v.get("ub", "INF"))
        lb = None if lb == "-INF" else lb
        ub = None if ub == "INF" else ub
        assert lb != "INF" and ub != "-INF"
        vars_.append((v.get("name"), lb, ub, v.get("type", "C")))
    assert len(vars_) == int(V.get("numberOfVariables"))

    O = data.find(NS + "objectives")
    objs = O.findall(NS + "obj")
    assert len(objs) == 1
    ob = objs[0]
    olin = {}
    for c in ob.findall(NS + "coef"):
        olin[int(c.get("idx"))] = Fraction(c.text.strip())
    assert len(olin) == int(ob.get("numberOfObjCoef", "0"))
    assert ob.get("weight") in (None, "1")
    obj = (ob.get("maxOrMin", "min"), olin, Fraction(ob.get("constant", "0")))

    C = data.find(NS + "constraints")
    cons = []
    if C is not None:
        for c in C.findall(NS + "con"):
            lb = num(c.get("lb", "-INF"))
            ub = num(c.get("ub", "INF"))
            cons.append((c.get("name"), None if lb == "-INF" else lb, None if ub == "INF" else ub,
                         Fraction(c.get("constant", "0"))))
        assert len(cons) == int(C.get("numberOfConstraints"))
    m = len(cons)

    lin = [dict() for _ in range(m)]
    L = data.find(NS + "linearConstraintCoefficients")
    if L is not None:
        start = expand(L.find(NS + "start"))
        vals = expand(L.find(NS + "value"), is_int=False)
        ri, ci = L.find(NS + "rowIdx"), L.find(NS + "colIdx")
        assert (ri is None) != (ci is None)
        idx = expand(ri if ri is not None else ci)
        assert len(idx) == len(vals) == int(L.get("numberOfValues"))
        assert start[0] == 0 and start[-1] == len(vals)
        assert all(start[k] <= start[k + 1] for k in range(len(start) - 1))
        if ci is not None:  # row-major: start indexes rows
            assert len(start) == m + 1
            for r in range(m):
                for k in range(start[r], start[r + 1]):
                    assert idx[k] not in lin[r]
                    lin[r][idx[k]] = vals[k]
        else:  # column-major: start indexes columns
            assert len(start) == len(vars_) + 1
            for j in range(len(vars_)):
                for k in range(start[j], start[j + 1]):
                    assert j not in lin[idx[k]]
                    lin[idx[k]][j] = vals[k]

    quad = {}
    Q = data.find(NS + "quadraticCoefficients")
    if Q is not None:
        qt = Q.findall(NS + "qTerm")
        assert len(qt) == int(Q.get("numberOfQuadraticTerms"))
        for q in qt:
            quad.setdefault(int(q.get("idx")), []).append(
                (int(q.get("idxOne")), int(q.get("idxTwo")), Fraction(q.get("coef", "1"))))

    nl = {}
    N = data.find(NS + "nonlinearExpressions")
    if N is not None:
        for e in N.findall(NS + "nl"):
            kids = list(e)
            assert len(kids) == 1
            k = int(e.get("idx"))
            assert k not in nl
            nl[k] = kids[0]
    # sections this reader does not handle must be absent
    for tag in ("matrices", "cones", "matrixProgramming", "timeDomain", "specialOrderedSets"):
        assert data.find(NS + tag) is None, tag
    return dict(vars=vars_, obj=obj, cons=cons, lin=lin, quad=quad, nl=nl)
