"""Independent OSIL reader and exact/interval evaluator (written for this review).

All data are kept as exact Fractions parsed from the decimal strings.
Row value = linear + quadratic + nonlinear(nl) + constant (OSIL con attribute).
Objective = obj constant + linear + quadratic(idx=-1) + nl(idx=-1).
Variables: default lb = 0, ub = +inf (OSiL defaults); type C/B/I.

Expressions are nested tuples:
  ('num', F) | ('var', j, coef F) | (op, [children]) | ('pow', base, expo)
"""
import xml.etree.ElementTree as ET
from fractions import Fraction as F

import ivl

NS = "{os.optimizationservices.org}"


def num(s):
    s = s.strip()
    if s in ("INF", "+INF", "Infinity"):
        return None
    if s in ("-INF", "-Infinity"):
        return None
    return F(s)


def expand(parent):
    """Expand an OSiL array of <el mult incr> into a list of Fractions."""
    out = []
    for el in parent:
        assert el.tag == NS + "el", el.tag
        m = int(el.get("mult", "1"))
        inc = F(el.get("incr", "0"))
        v = F(el.text.strip())
        for k in range(m):
            out.append(v + k * inc)
    return out


class Model:
    pass


def parse_expr(e):
    t = e.tag[len(NS):]
    ch = [parse_expr(c) for c in e]
    if t == "number":
        assert e.get("type", "real") == "real"
        return ("num", F(e.get("value")))
    if t == "variable":
        assert not ch, "variable with child expression not supported"
        return ("var", int(e.get("idx")), F(e.get("coef", "1")))
    if t in ("sum", "product"):
        return (t, ch)
    if t in ("plus", "minus", "times", "divide", "power"):
        assert len(ch) == 2
        return (t, ch)
    if t in ("negate", "square", "sqrt", "exp", "ln", "sin", "cos", "abs"):
        assert len(ch) == 1
        return (t, ch)
    raise NotImplementedError(t)


def parse(path):
    root = ET.parse(path).getroot()
    d = root.find(NS + "instanceData")
    M = Model()
    vs = d.find(NS + "variables")
    M.vname, M.lb, M.ub, M.vtype = [], [], [], []
    for v in vs:
        M.vname.append(v.get("name"))
        lb = v.get("lb", "0")
        M.lb.append(None if lb.strip().startswith("-INF") else F(lb))
        ub = v.get("ub", "INF")
        M.ub.append(None if ub.strip().lstrip("+") == "INF" else F(ub))
        t = v.get("type", "C")
        assert t in ("C", "B", "I"), t
        if t == "B":  # OSiL binary: bounds are [0,1] intersected with given
            M.lb[-1] = max(M.lb[-1] or F(0), F(0))
            M.ub[-1] = F(1) if M.ub[-1] is None else min(M.ub[-1], F(1))
        M.vtype.append(t)
    M.n = len(M.vname)
    assert M.n == int(vs.get("numberOfVariables"))
    objs = d.find(NS + "objectives")
    ob = list(objs)
    assert len(ob) == 1
    ob = ob[0]
    M.sense = ob.get("maxOrMin", "min")
    assert ob.get("weight", "1") in ("1", "1.0")
    M.obj_const = F(ob.get("constant", "0"))
    M.obj_lin = {}
    for c in ob:
        j = int(c.get("idx"))
        M.obj_lin[j] = M.obj_lin.get(j, F(0)) + F(c.text.strip())
    cs = d.find(NS + "constraints")
    M.cname, M.clb, M.cub, M.cconst = [], [], [], []
    if cs is not None:
        for c in cs:
            M.cname.append(c.get("name"))
            lb = c.get("lb")
            ub = c.get("ub")
            M.clb.append(None if lb is None or lb.strip().startswith("-INF") else F(lb))
            M.cub.append(None if ub is None or ub.strip().lstrip("+") == "INF" else F(ub))
            M.cconst.append(F(c.get("constant", "0")))
    M.m = len(M.cname)
    M.lin = [dict() for _ in range(M.m)]
    lc = d.find(NS + "linearConstraintCoefficients")
    if lc is not None:
        start = [int(x) for x in expand(lc.find(NS + "start"))]
        vals = expand(lc.find(NS + "value"))
        ci = lc.find(NS + "colIdx")
        ri = lc.find(NS + "rowIdx")
        if ci is not None:  # row-major
            idx = [int(x) for x in expand(ci)]
            assert len(start) == M.m + 1
            for i in range(M.m):
                for k in range(start[i], start[i + 1]):
                    M.lin[i][idx[k]] = M.lin[i].get(idx[k], F(0)) + vals[k]
        else:  # column-major
            idx = [int(x) for x in expand(ri)]
            assert len(start) == M.n + 1
            for j in range(M.n):
                for k in range(start[j], start[j + 1]):
                    i = idx[k]
                    M.lin[i][j] = M.lin[i].get(j, F(0)) + vals[k]
        assert len(vals) == int(lc.get("numberOfValues"))
    M.quad = [[] for _ in range(M.m)]
    M.obj_quad = []
    qc = d.find(NS + "quadraticCoefficients")
    if qc is not None:
        for q in qc:
            i = int(q.get("idx"))
            t = (int(q.get("idxOne")), int(q.get("idxTwo")), F(q.get("coef")))
            (M.obj_quad if i == -1 else M.quad[i]).append(t)
    M.nl = [None] * M.m
    M.obj_nl = None
    ne = d.find(NS + "nonlinearExpressions")
    if ne is not None:
        for e in ne:
            i = int(e.get("idx"))
            ch = list(e)
            assert len(ch) == 1
            ex = parse_expr(ch[0])
            if i == -1:
                assert M.obj_nl is None
                M.obj_nl = ex
            else:
                assert M.nl[i] is None
                M.nl[i] = ex
    for tag in ("specialOrderedSets",):
        assert d.find(NS + tag) is None, tag
    return M


# ---------------------------------------------------------------- evaluation
def ev_exact(e, x):
    """Exact Fraction evaluation; raises for non-algebraic operators."""
    t = e[0]
    if t == "num":
        return e[1]
    if t == "var":
        return e[2] * x[e[1]]
    a = [ev_exact(c, x) for c in e[1]]
    if t == "sum":
        return sum(a, F(0))
    if t == "product" or t == "times":
        r = F(1)
        for v in a:
            r *= v
        return r
    if t == "plus":
        return a[0] + a[1]
    if t == "minus":
        return a[0] - a[1]
    if t == "negate":
        return -a[0]
    if t == "divide":
        return a[0] / a[1]
    if t == "square":
        return a[0] * a[0]
    if t == "power":
        p = a[1]
        assert p.denominator == 1, "non-integer power"
        return a[0] ** int(p)
    raise ValueError("non-algebraic " + t)


def ev_iv(e, x):
    """Interval evaluation; x is a list of ivl.I (or Fractions)."""
    t = e[0]
    if t == "num":
        return ivl.I(e[1])
    if t == "var":
        return ivl.I(e[2]) * ivl.I.of(x[e[1]])
    a = [ev_iv(c, x) for c in e[1]]
    if t == "sum":
        r = ivl.I(0)
        for v in a:
            r = r + v
        return r
    if t in ("product", "times"):
        r = ivl.I(1)
        for v in a:
            r = r * v
        return r
    if t == "plus":
        return a[0] + a[1]
    if t == "minus":
        return a[0] - a[1]
    if t == "negate":
        return -a[0]
    if t == "divide":
        return a[0] / a[1]
    if t == "square":
        return a[0].sqr()
    if t == "power":
        p = a[1]
        assert p.lo == p.hi and p.lo.denominator == 1, "non-integer power"
        return a[0].powi(int(p.lo))
    if t == "sqrt":
        return a[0].sqrt()
    if t == "exp":
        return a[0].exp()
    if t == "ln":
        return a[0].ln()
    raise NotImplementedError(t)


def is_algebraic(e):
    if e is None:
        return True
    t = e[0]
    if t in ("num", "var"):
        return True
    if t in ("sqrt", "exp", "ln", "sin", "cos", "abs"):
        return False
    if t == "power" and not (e[1][1][0] == "num" and e[1][1][1].denominator == 1):
        return False
    return all(is_algebraic(c) for c in e[1])


def row_exact(M, i, x):
    v = M.cconst[i]
    for j, c in M.lin[i].items():
        v += c * x[j]
    for (a, b, c) in M.quad[i]:
        v += c * x[a] * x[b]
    if M.nl[i] is not None:
        v += ev_exact(M.nl[i], x)
    return v


def row_iv(M, i, x):
    v = ivl.I(M.cconst[i])
    for j, c in M.lin[i].items():
        v = v + ivl.I(c) * ivl.I.of(x[j])
    for (a, b, c) in M.quad[i]:
        if a == b:
            v = v + ivl.I(c) * ivl.I.of(x[a]).sqr()
        else:
            v = v + ivl.I(c) * ivl.I.of(x[a]) * ivl.I.of(x[b])
    if M.nl[i] is not None:
        v = v + ev_iv(M.nl[i], x)
    return v


def obj_exact(M, x):
    v = M.obj_const
    for j, c in M.obj_lin.items():
        v += c * x[j]
    for (a, b, c) in M.obj_quad:
        v += c * x[a] * x[b]
    if M.obj_nl is not None:
        v += ev_exact(M.obj_nl, x)
    return v


def obj_iv(M, x):
    v = ivl.I(M.obj_const)
    for j, c in M.obj_lin.items():
        v = v + ivl.I(c) * ivl.I.of(x[j])
    for (a, b, c) in M.obj_quad:
        v = v + (ivl.I(c) * ivl.I.of(x[a]).sqr() if a == b else ivl.I(c) * ivl.I.of(x[a]) * ivl.I.of(x[b]))
    if M.obj_nl is not None:
        v = v + ev_iv(M.obj_nl, x)
    return v


def row_vars(M, i):
    s = set(M.lin[i])
    for (a, b, c) in M.quad[i]:
        s.add(a)
        s.add(b)
    if M.nl[i] is not None:
        st = [M.nl[i]]
        while st:
            e = st.pop()
            if e[0] == "var":
                s.add(e[1])
            elif e[0] != "num":
                st.extend(e[1])
    return s


def read_sol(path, M):
    """MINLPLib .sol: lines 'name value'. Missing variables -> 0 (reported)."""
    idx = {nm: j for j, nm in enumerate(M.vname)}
    x = [None] * M.n
    extra = []
    with open(path) as f:
        for line in f:
            p = line.split()
            if len(p) < 2 or p[0].startswith("#"):
                continue
            if p[0] in idx:
                x[idx[p[0]]] = F(p[1])
            else:
                extra.append((p[0], p[1]))
    missing = [j for j in range(M.n) if x[j] is None]
    for j in missing:
        x[j] = F(0)
    return x, missing, extra
