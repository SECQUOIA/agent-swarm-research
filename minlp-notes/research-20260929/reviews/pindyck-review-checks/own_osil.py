"""Reviewer's own OSIL reader (ElementTree; shares no code with osilx.py / ev.py).

read(path) -> dict with
  names, lb, ub            variable names and bound strings ("-INF"/"INF" for infinite)
  cons: list of dict(name, lb, ub, lin={var_index: coef_str}, nl=tree or None)
  obj: dict(sense, lin={var_index: coef_str}, constant)
Trees: ("num", str) | ("var", idx, coef_str) | (op, child, ...)
ev(tree, x, ctx) evaluates a tree with an mpmath context (mp or iv).
"""
import xml.etree.ElementTree as ET

NS = "{os.optimizationservices.org}"


def _expand(el):
    """expand an OSiL <el mult= incr=> integer array"""
    out = []
    for e in el:
        v = int(e.text)
        mult = int(e.get("mult", "1"))
        inc = int(e.get("incr", "0"))
        out += [v + k * inc for k in range(mult)]
    return out


def _expand_vals(el):
    out = []
    for e in el:
        mult = int(e.get("mult", "1"))
        assert e.get("incr") is None
        out += [e.text.strip()] * mult
    return out


def _tree(e):
    tag = e.tag.replace(NS, "")
    if tag == "number":
        return ("num", e.get("value"))
    if tag == "variable":
        return ("var", int(e.get("idx")), e.get("coef", "1"))
    return (tag,) + tuple(_tree(c) for c in e)


def read(path):
    root = ET.parse(path).getroot()
    d = root.find(NS + "instanceData")
    names, lb, ub = [], [], []
    for v in d.find(NS + "variables"):
        names.append(v.get("name"))
        lb.append(v.get("lb", "0"))
        ub.append(v.get("ub", "INF"))
        assert v.get("type") in (None, "C")
    cons = []
    for c in d.find(NS + "constraints"):
        cons.append(dict(name=c.get("name"), lb=c.get("lb", "-INF"), ub=c.get("ub", "INF"),
                         lin={}, nl=None, constant=c.get("constant", "0")))
    lc = d.find(NS + "linearConstraintCoefficients")
    start = _expand(lc.find(NS + "start"))
    col = _expand(lc.find(NS + "colIdx"))
    val = _expand_vals(lc.find(NS + "value"))
    assert len(col) == len(val) == int(lc.get("numberOfValues"))
    assert len(start) == len(cons) + 1
    for i in range(len(cons)):
        for k in range(start[i], start[i + 1]):
            assert col[k] not in cons[i]["lin"]
            cons[i]["lin"][col[k]] = val[k]
    objs = d.find(NS + "objectives")
    ob = list(objs)
    assert len(ob) == 1
    o = ob[0]
    obj = dict(sense=o.get("maxOrMin"), constant=o.get("constant", "0"), lin={})
    for cf in o:
        obj["lin"][int(cf.get("idx"))] = cf.text.strip()
    obj["nl"] = None
    nle = d.find(NS + "nonlinearExpressions")
    for e in nle:
        idx = int(e.get("idx"))
        kids = list(e)
        assert len(kids) == 1
        if idx == -1:
            obj["nl"] = _tree(kids[0])
        else:
            assert cons[idx]["nl"] is None
            cons[idx]["nl"] = _tree(kids[0])
    assert d.find(NS + "quadraticCoefficients") is None
    return dict(names=names, lb=lb, ub=ub, cons=cons, obj=obj)


def ev(t, x, ctx):
    op = t[0]
    if op == "num":
        return ctx.mpf(t[1])
    if op == "var":
        return ctx.mpf(t[2]) * x[t[1]]
    a = [ev(c, x, ctx) for c in t[1:]]
    if op in ("sum", "plus"):
        s = a[0]
        for b in a[1:]:
            s = s + b
        return s
    if op in ("product", "times"):
        s = a[0]
        for b in a[1:]:
            s = s * b
        return s
    if op == "minus":
        return a[0] - a[1]
    if op == "negate":
        return -a[0]
    if op == "divide":
        return a[0] / a[1]
    if op == "power":
        # a^b = exp(b ln a) for a > 0
        return ctx.exp(a[1] * ctx.log(a[0]))
    if op == "exp":
        return ctx.exp(a[0])
    if op == "ln":
        return ctx.log(a[0])
    raise ValueError(op)


def row_value(c, x, ctx):
    v = ctx.mpf(c["constant"])
    for j, cf in c["lin"].items():
        v = v + ctx.mpf(cf) * x[j]
    if c["nl"] is not None:
        v = v + ev(c["nl"], x, ctx)
    return v


def obj_value(o, x, ctx):
    v = ctx.mpf(o["constant"])
    for j, cf in o["lin"].items():
        v = v + ctx.mpf(cf) * x[j]
    if o["nl"] is not None:
        v = v + ev(o["nl"], x, ctx)
    return v
