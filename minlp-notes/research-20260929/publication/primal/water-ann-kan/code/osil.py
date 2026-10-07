"""Minimal OSIL reader that keeps every decimal constant exact (Fraction).

Written for this track; it does not import any earlier reader.

load(name) returns a dict with
  names, vtype ('C', 'B' or 'I'), lb, ub        (Fraction, or None for an infinite bound)
  obj: dict(sense, const, lin {j: a}, quad [(i, j, a)], nl tree or None)
  cons: list of dict(name, lb, ub, const, lin {j: a}, quad [(i, j, a)], nl tree or None)
Row value = const + sum lin + sum quad + nl; the row requires lb <= value <= ub.

Expression trees are tuples:
  ('var', j, coef) ('num', c) ('neg', t) ('sum', [t, ...]) ('prod', [t, ...])
  ('minus', a, b) ('div', a, b) ('pow', a, b) ('sq', a) ('sqrt', a) ('exp', a) ('ln', a) ('tanh', a)
"""
import os
import xml.etree.ElementTree as ET
from fractions import Fraction

OSIL_DIR = os.path.expanduser("~/.cache/minlplib/minlplib/osil")
NS = "{os.optimizationservices.org}"


def _num(s):
    s = s.strip()
    if s.upper() in ("INF", "+INF", "INFINITY", "+INFINITY"):
        return "inf"
    if s.upper() in ("-INF", "-INFINITY"):
        return "-inf"
    return Fraction(s)


def _bound(s, default):
    if s is None:
        return default
    v = _num(s)
    if v in ("inf", "-inf"):
        return None
    return v


def _expand(elem, kind):
    """Expand <el mult= incr=> lists. kind 'int' or 'frac'."""
    out = []
    for el in elem.findall(NS + "el"):
        mult = int(el.get("mult", "1"))
        if kind == "int":
            v = int(el.text)
            inc = int(el.get("incr", "0"))
            out.extend(v + k * inc for k in range(mult))
        else:
            v = Fraction(el.text.strip())
            inc = Fraction(el.get("incr", "0"))
            out.extend(v + k * inc for k in range(mult))
    return out


def _tree(e):
    tag = e.tag[len(NS):]
    ch = list(e)
    if tag == "variable":
        return ("var", int(e.get("idx")), Fraction(e.get("coef", "1")))
    if tag == "number":
        return ("num", Fraction(e.get("value")))
    if tag == "negate":
        return ("neg", _tree(ch[0]))
    if tag == "sum":
        return ("sum", [_tree(c) for c in ch])
    if tag in ("product",):
        return ("prod", [_tree(c) for c in ch])
    if tag == "times":
        return ("prod", [_tree(ch[0]), _tree(ch[1])])
    if tag == "plus":
        return ("sum", [_tree(ch[0]), _tree(ch[1])])
    if tag == "minus":
        return ("minus", _tree(ch[0]), _tree(ch[1]))
    if tag == "divide":
        return ("div", _tree(ch[0]), _tree(ch[1]))
    if tag == "power":
        return ("pow", _tree(ch[0]), _tree(ch[1]))
    if tag == "square":
        return ("sq", _tree(ch[0]))
    if tag == "sqrt":
        return ("sqrt", _tree(ch[0]))
    if tag == "exp":
        return ("exp", _tree(ch[0]))
    if tag == "ln":
        return ("ln", _tree(ch[0]))
    if tag == "tanh":
        return ("tanh", _tree(ch[0]))
    raise ValueError("unsupported OSIL node " + tag)


def load(name, path=None):
    path = path or os.path.join(OSIL_DIR, name + ".osil")
    root = ET.parse(path).getroot()
    D = root.find(NS + "instanceData")
    names, vtype, lb, ub = [], [], [], []
    for v in D.find(NS + "variables").findall(NS + "var"):
        names.append(v.get("name"))
        t = v.get("type", "C")
        vtype.append(t)
        lo = _bound(v.get("lb"), Fraction(0))
        hi = _bound(v.get("ub"), None)
        if t == "B":
            lo = max(lo, Fraction(0)) if lo is not None else Fraction(0)
            hi = min(hi, Fraction(1)) if hi is not None else Fraction(1)
        lb.append(lo)
        ub.append(hi)
    n = len(names)
    objs = D.find(NS + "objectives").findall(NS + "obj")
    assert len(objs) == 1
    o = objs[0]
    obj = dict(sense=o.get("maxOrMin", "min"), const=Fraction(o.get("constant", "0")), lin={}, quad=[], nl=None)
    for c in o.findall(NS + "coef"):
        j = int(c.get("idx"))
        obj["lin"][j] = obj["lin"].get(j, Fraction(0)) + Fraction(c.text.strip())
    cons = []
    C = D.find(NS + "constraints")
    if C is not None:
        for c in C.findall(NS + "con"):
            cons.append(dict(name=c.get("name"), lb=_bound(c.get("lb"), None), ub=_bound(c.get("ub"), None),
                             const=Fraction(c.get("constant", "0")), lin={}, quad=[], nl=None))
    L = D.find(NS + "linearConstraintCoefficients")
    if L is not None:
        start = _expand(L.find(NS + "start"), "int")
        col = L.find(NS + "colIdx")
        row = L.find(NS + "rowIdx")
        val = _expand(L.find(NS + "value"), "frac")
        if col is not None:
            idx = _expand(col, "int")
            assert len(start) == len(cons) + 1 and len(idx) == len(val) == start[-1]
            for i in range(len(cons)):
                for k in range(start[i], start[i + 1]):
                    cons[i]["lin"][idx[k]] = cons[i]["lin"].get(idx[k], Fraction(0)) + val[k]
        else:
            idx = _expand(row, "int")
            assert len(start) == n + 1 and len(idx) == len(val) == start[-1]
            for j in range(n):
                for k in range(start[j], start[j + 1]):
                    cons[idx[k]]["lin"][j] = cons[idx[k]]["lin"].get(j, Fraction(0)) + val[k]
    Q = D.find(NS + "quadraticCoefficients")
    if Q is not None:
        for q in Q.findall(NS + "qTerm"):
            i = int(q.get("idx"))
            t = (int(q.get("idxOne")), int(q.get("idxTwo")), Fraction(q.get("coef", "1")))
            (obj["quad"] if i == -1 else cons[i]["quad"]).append(t)
    N = D.find(NS + "nonlinearExpressions")
    if N is not None:
        for e in N.findall(NS + "nl"):
            i = int(e.get("idx"))
            t = _tree(list(e)[0])
            tgt = obj if i == -1 else cons[i]
            tgt["nl"] = t if tgt["nl"] is None else ("sum", [tgt["nl"], t])
    for c in cons:
        for j in list(c["lin"]):
            if c["lin"][j] == 0:
                del c["lin"][j]
    return dict(name=name, names=names, vtype=vtype, lb=lb, ub=ub, obj=obj, cons=cons)


def tree_vars(t, acc=None):
    acc = set() if acc is None else acc
    k = t[0]
    if k == "var":
        acc.add(t[1])
    elif k == "num":
        pass
    elif k in ("sum", "prod"):
        for s in t[1]:
            tree_vars(s, acc)
    else:
        for s in t[1:]:
            tree_vars(s, acc)
    return acc


def row_vars(c):
    s = set(c["lin"])
    for a, b, _ in c["quad"]:
        s.add(a)
        s.add(b)
    if c["nl"] is not None:
        tree_vars(c["nl"], s)
    return s


def eval_tree(t, x, F):
    """Evaluate tree t at x with function table F (keys: exp, ln, tanh, sqrt, pow, num)."""
    k = t[0]
    if k == "var":
        return F["num"](t[2]) * x[t[1]] if t[2] != 1 else x[t[1]]
    if k == "num":
        return F["num"](t[1])
    if k == "neg":
        return -eval_tree(t[1], x, F)
    if k == "sum":
        s = eval_tree(t[1][0], x, F)
        for u in t[1][1:]:
            s = s + eval_tree(u, x, F)
        return s
    if k == "prod":
        s = eval_tree(t[1][0], x, F)
        for u in t[1][1:]:
            s = s * eval_tree(u, x, F)
        return s
    if k == "minus":
        return eval_tree(t[1], x, F) - eval_tree(t[2], x, F)
    if k == "div":
        return eval_tree(t[1], x, F) / eval_tree(t[2], x, F)
    if k == "pow":
        e = t[2]
        assert e[0] == "num" and e[1].denominator == 1 and e[1] >= 0, "only nonnegative integer powers supported"
        b = eval_tree(t[1], x, F)
        r = F["num"](Fraction(1))
        for _ in range(int(e[1])):
            r = r * b
        return r
    if k == "sq":
        b = eval_tree(t[1], x, F)
        return b * b
    return F[k](eval_tree(t[1], x, F))


def eval_row(c, x, F):
    s = F["num"](c["const"])
    for j, a in c["lin"].items():
        s = s + F["num"](a) * x[j]
    for i, j, a in c["quad"]:
        s = s + F["num"](a) * x[i] * x[j]
    if c["nl"] is not None:
        s = s + eval_tree(c["nl"], x, F)
    return s
