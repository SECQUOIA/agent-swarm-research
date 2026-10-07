"""Review r2: exact comparison of a GAMS scalar model (.gms text) with an OSiL file.

Own code (not derived from the author's exact_forms.py). Every decimal in
either file is read as the exact rational it denotes (fractions.Fraction of the
decimal string). Rows are built as sympy expressions with Rational
coefficients; no floating point is used anywhere.

Functions:
  read_gms(path)   -> dict eqname -> (expr lhs-rhs, sense), objvar name
  read_osil(path)  -> dict conname -> (expr f - const, lb, ub), objective expr, var names
  gms_objective(eqs, objvar) -> (eqname, objective expression) for the row that defines objvar
"""
import re
import xml.etree.ElementTree as ET
from fractions import Fraction

import sympy as sp

NUM = re.compile(r"(?<![\w.])(\d+\.\d*|\.\d+|\d+)([eE][+-]?\d+)?(?![\w.])")
_syms = {}


def S(name):
    s = _syms.get(name)
    if s is None:
        s = _syms[name] = sp.Symbol(name)
    return s


def Q(txt):
    f = Fraction(txt.strip())
    return sp.Rational(f.numerator, f.denominator)


class _Env(dict):
    def __missing__(self, key):
        return S(key)


def _env():
    e = _Env()
    e.update(R=lambda s: Q(s), sqr=lambda a: a ** 2, power=lambda a, b: a ** b, POWER=lambda a, b: a ** b,
             exp=sp.exp, log=sp.log, sqrt=sp.sqrt, vcpower=lambda a, b: a ** b, rpower=lambda a, b: a ** b)
    e["__builtins__"] = {}
    return e


def gms_expr(text):
    t = " ".join(text.split())
    t = NUM.sub(lambda m: "R('" + m.group(0) + "')", t)
    return eval(t, _env())


def read_gms(path):
    src = open(path).read()
    # equation definitions start at a line 'name.. '
    eqs = {}
    for m in re.finditer(r"^(\w+)\.\.(.*?);", src, flags=re.M | re.S):
        name, body = m.group(1), m.group(2)
        mm = re.search(r"=([EGLN])=", body, flags=re.I)
        sense = mm.group(1).upper()
        lhs, rhs = body[:mm.start()], body[mm.end():]
        eqs[name] = (gms_expr(lhs) - gms_expr(rhs), sense)
    mo = re.search(r"Solve\s+m\s+using\s+\S+\s+(minimizing|maximizing)\s+(\w+)\s*;", src)
    return eqs, mo.group(2), mo.group(1)


def gms_objective(eqs, objvar):
    v = S(objvar)
    hits = [k for k, (e, s) in eqs.items() if v in e.free_symbols]
    assert len(hits) == 1, hits
    k = hits[0]
    e, s = eqs[k]
    if s != "E":  # objvar kept as a variable (objective row is an inequality)
        return None, v
    a = sp.diff(e, v)
    assert a.free_symbols == set(), "objvar not linear with constant coefficient"
    rest = e.subs(v, 0)
    assert sp.expand(e - rest - a * v) == 0
    return k, -rest / a


def _strip(tag):
    return tag.split("}")[-1]


def _expand_els(parent, kind):
    """OSiL <el mult incr> compression."""
    out = []
    for el in parent:
        if _strip(el.tag) != "el":
            continue
        mult = int(el.get("mult", "1"))
        if kind == "int":
            v = int(el.text)
            inc = int(el.get("incr", "0"))
            out.extend(v + i * inc for i in range(mult))
        else:
            v = Q(el.text)
            assert el.get("incr") is None
            out.extend([v] * mult)
    return out


def _osnl(node, names):
    t = _strip(node.tag)
    ch = [c for c in node]
    if t == "variable":
        v = S(names[int(node.get("idx"))])
        c = Q(node.get("coef", "1"))
        if ch:
            v = _osnl(ch[0], names)
            raise NotImplementedError("variable with child")
        return c * v
    if t == "number":
        return Q(node.get("value"))
    if t in ("sum", "plus"):
        return sp.Add(*[_osnl(c, names) for c in ch])
    if t in ("product", "times"):
        return sp.Mul(*[_osnl(c, names) for c in ch])
    if t == "minus":
        return _osnl(ch[0], names) - _osnl(ch[1], names)
    if t == "negate":
        return -_osnl(ch[0], names)
    if t == "divide":
        return _osnl(ch[0], names) / _osnl(ch[1], names)
    if t == "square":
        return _osnl(ch[0], names) ** 2
    if t == "power":
        return _osnl(ch[0], names) ** _osnl(ch[1], names)
    if t == "exp":
        return sp.exp(_osnl(ch[0], names))
    if t == "ln":
        return sp.log(_osnl(ch[0], names))
    if t == "sqrt":
        return sp.sqrt(_osnl(ch[0], names))
    raise NotImplementedError(t)


def read_osil(path):
    root = ET.parse(path).getroot()
    data = [c for c in root if _strip(c.tag) == "instanceData"][0]
    sec = {_strip(c.tag): c for c in data}
    names, bounds = [], []
    for v in sec["variables"]:
        names.append(v.get("name"))
        bounds.append((v.get("lb", "0"), v.get("ub", "INF"), v.get("type", "C")))
    cons = []
    for c in sec["constraints"]:
        cons.append(dict(name=c.get("name"), lb=c.get("lb"), ub=c.get("ub"), const=Q(c.get("constant", "0"))))
    rows = [sp.Integer(0)] * len(cons)
    lcc = sec.get("linearConstraintCoefficients")
    if lcc is not None:
        parts = {_strip(c.tag): c for c in lcc}
        start = _expand_els(parts["start"], "int")
        vals = _expand_els(parts["value"], "rat")
        if "colIdx" in parts:  # row-wise
            idx = _expand_els(parts["colIdx"], "int")
            terms = [[] for _ in cons]
            for r in range(len(start) - 1):
                for k in range(start[r], start[r + 1]):
                    terms[r].append(vals[k] * S(names[idx[k]]))
        else:
            idx = _expand_els(parts["rowIdx"], "int")
            terms = [[] for _ in cons]
            for cidx in range(len(start) - 1):
                for k in range(start[cidx], start[cidx + 1]):
                    terms[idx[k]].append(vals[k] * S(names[cidx]))
        rows = [sp.Add(*t) for t in terms]
    obj_terms = []
    objs = [o for o in sec["objectives"]]
    assert len(objs) == 1
    o = objs[0]
    obj_sense = o.get("maxOrMin")
    obj_const = Q(o.get("constant", "0"))
    for c in o:
        obj_terms.append(Q(c.text) * S(names[int(c.get("idx"))]))
    rows = list(rows)
    if "quadraticCoefficients" in sec:
        for q in sec["quadraticCoefficients"]:
            i = int(q.get("idx"))
            term = Q(q.get("coef")) * S(names[int(q.get("idxOne"))]) * S(names[int(q.get("idxTwo"))])
            if i == -1:
                obj_terms.append(term)
            else:
                rows[i] = rows[i] + term
    if "nonlinearExpressions" in sec:
        for nl in sec["nonlinearExpressions"]:
            i = int(nl.get("idx"))
            e = _osnl([c for c in nl][0], names)
            if i == -1:
                obj_terms.append(e)
            else:
                rows[i] = rows[i] + e
    out = {}
    for c, r in zip(cons, rows):
        out[c["name"]] = (r + c["const"], c["lb"], c["ub"])
    obj = sp.Add(*obj_terms) + obj_const
    return out, obj, obj_sense, names, bounds
