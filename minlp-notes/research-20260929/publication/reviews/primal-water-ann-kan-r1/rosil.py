"""Reviewer's own OSIL reader (independent of the author's osil.py).

Everything numeric is read as an exact Fraction from the decimal text.
Returns a model dict:
  names, vtype ('C','B','I'), lb, ub (Fraction or None for infinite)
  obj: sense, const, lin {j: a}, quad [(i, j, a)], nl tree or None
  cons: list of dict name, lb, ub (Fraction/None), const, lin, quad, nl
Nonlinear trees are nested tuples: ('var', j, coef), ('num', q), (op, child, ...)
"""
import os
import xml.etree.ElementTree as ET
from fractions import Fraction as Fr

OSIL_DIR = os.path.expanduser("~/.cache/minlplib/minlplib/osil")


def _num(s):
    s = s.strip()
    if s in ("INF", "+INF", "Infinity"):
        return "inf"
    if s in ("-INF", "-Infinity"):
        return "-inf"
    return Fr(s)


def _tag(e):
    return e.tag.split("}")[-1]


def _expand(elem, as_int):
    """Expand a list of <el mult=.. incr=..> entries (OSiL compressed arrays)."""
    out = []
    for el in elem:
        assert _tag(el) == "el", _tag(el)
        m = int(el.get("mult", "1"))
        v = int(el.text) if as_int else Fr(el.text.strip())
        d = el.get("incr")
        d = (int(d) if as_int else Fr(d)) if d is not None else 0
        for k in range(m):
            out.append(v + k * d)
    return out


def _tree(e):
    t = _tag(e)
    if t == "variable":
        return ("var", int(e.get("idx")), Fr(e.get("coef", "1")))
    if t == "number":
        return ("num", Fr(e.get("value")))
    ch = [_tree(c) for c in e]
    if t in ("plus", "minus", "times", "divide", "power"):
        assert len(ch) == 2, t
    elif t in ("negate", "exp", "tanh", "ln", "sqrt", "square", "log"):
        assert len(ch) == 1, t
    elif t in ("sum", "product"):
        pass
    else:
        raise ValueError("unsupported operator " + t)
    return (t,) + tuple(ch)


def load(name):
    root = ET.parse(os.path.join(OSIL_DIR, name + ".osil")).getroot()
    data = [c for c in root if _tag(c) == "instanceData"][0]
    sec = {_tag(c): c for c in data}
    unknown = set(sec) - {"variables", "objectives", "constraints", "linearConstraintCoefficients",
                          "quadraticCoefficients", "nonlinearExpressions"}
    assert not unknown, unknown
    names, vtype, lb, ub = [], [], [], []
    for v in sec["variables"]:
        assert set(v.attrib) <= {"name", "type", "lb", "ub"}, v.attrib
        names.append(v.get("name"))
        vtype.append(v.get("type", "C"))
        l = _num(v.get("lb", "0"))
        u = _num(v.get("ub", "INF"))
        lb.append(None if l == "-inf" else l)
        ub.append(None if u == "inf" else u)
        assert l != "inf" and u != "-inf"
    assert len(names) == int(sec["variables"].get("numberOfVariables"))
    n = len(names)
    objs = list(sec["objectives"])
    assert len(objs) == 1
    o = objs[0]
    assert set(o.attrib) <= {"maxOrMin", "name", "numberOfObjCoef", "constant", "weight"}, o.attrib
    obj = dict(sense=o.get("maxOrMin", "min"), const=Fr(o.get("constant", "0")), lin={}, quad=[], nl=None)
    for c in o:
        assert _tag(c) == "coef"
        j = int(c.get("idx"))
        obj["lin"][j] = obj["lin"].get(j, 0) + Fr(c.text.strip())
    cons = []
    for c in sec["constraints"]:
        assert set(c.attrib) <= {"name", "lb", "ub", "constant"}, c.attrib
        l = _num(c.get("lb", "-INF"))
        u = _num(c.get("ub", "INF"))
        cons.append(dict(name=c.get("name"), lb=None if l == "-inf" else l, ub=None if u == "inf" else u,
                         const=Fr(c.get("constant", "0")), lin={}, quad=[], nl=None))
    assert len(cons) == int(sec["constraints"].get("numberOfConstraints"))
    L = sec.get("linearConstraintCoefficients")
    if L is not None:
        parts = {_tag(c): c for c in L}
        start = _expand(parts["start"], True)
        vals = _expand(parts["value"], False)
        if "colIdx" in parts:
            idx = _expand(parts["colIdx"], True)
            rowmajor = True
        else:
            idx = _expand(parts["rowIdx"], True)
            rowmajor = False
        assert len(idx) == len(vals) == int(L.get("numberOfValues")) == start[-1]
        for k in range(len(start) - 1):
            for p in range(start[k], start[k + 1]):
                r, j = (k, idx[p]) if rowmajor else (idx[p], k)
                d = cons[r]["lin"]
                d[j] = d.get(j, 0) + vals[p]
        if rowmajor:
            assert len(start) - 1 <= len(cons)
    Q = sec.get("quadraticCoefficients")
    if Q is not None:
        for q in Q:
            r = int(q.get("idx"))
            t = (int(q.get("idxOne")), int(q.get("idxTwo")), Fr(q.get("coef", "1")))
            (obj["quad"] if r == -1 else cons[r]["quad"]).append(t)
    N = sec.get("nonlinearExpressions")
    if N is not None:
        for e in N:
            r = int(e.get("idx"))
            kids = list(e)
            assert len(kids) == 1
            tr = _tree(kids[0])
            tgt = obj if r == -1 else cons[r]
            tgt["nl"] = tr if tgt["nl"] is None else ("plus", tgt["nl"], tr)
    for d in [obj] + cons:
        d["lin"] = {j: a for j, a in d["lin"].items() if a != 0}
        for j in d["lin"]:
            assert 0 <= j < n
    return dict(names=names, vtype=vtype, lb=lb, ub=ub, obj=obj, cons=cons, n=n)


def tree_vars(t, acc=None):
    if acc is None:
        acc = set()
    if t[0] == "var":
        acc.add(t[1])
    elif t[0] != "num":
        for c in t[1:]:
            tree_vars(c, acc)
    return acc


def row_vars(c):
    s = set(c["lin"])
    for i, j, _ in c["quad"]:
        s.add(i)
        s.add(j)
    if c["nl"] is not None:
        tree_vars(c["nl"], s)
    return s


def eval_tree(t, X, A):
    """Evaluate a tree with arithmetic object A (methods num, exp, tanh) on values X."""
    op = t[0]
    if op == "var":
        return A.num(t[2]) * X[t[1]]
    if op == "num":
        return A.num(t[1])
    a = [eval_tree(c, X, A) for c in t[1:]]
    if op == "plus":
        return a[0] + a[1]
    if op == "minus":
        return a[0] - a[1]
    if op == "times":
        return a[0] * a[1]
    if op == "divide":
        return A.div(a[0], a[1])
    if op == "negate":
        return -a[0]
    if op == "sum":
        s = a[0]
        for b in a[1:]:
            s = s + b
        return s
    if op == "product":
        s = a[0]
        for b in a[1:]:
            s = s * b
        return s
    if op == "square":
        return a[0] * a[0]
    if op == "power":
        assert t[2][0] == "num" and t[2][1].denominator == 1 and t[2][1] >= 0, "only integer powers supported"
        k = int(t[2][1])
        r = A.num(Fr(1))
        for _ in range(k):
            r = r * a[0]
        return r
    if op == "exp":
        return A.exp(a[0])
    if op == "tanh":
        return A.tanh(a[0])
    raise ValueError(op)


def eval_body(c, X, A):
    """Row body (without the bounds): const + lin + quad + nl."""
    s = A.num(c["const"])
    for j, a in c["lin"].items():
        s = s + A.num(a) * X[j]
    for i, j, a in c["quad"]:
        s = s + A.num(a) * X[i] * X[j]
    if c["nl"] is not None:
        s = s + eval_tree(c["nl"], X, A)
    return s
