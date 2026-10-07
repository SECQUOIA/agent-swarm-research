"""Revision after review round 1: exact comparison of the .gms text form and
the MINLPLib OSIL form for the instances where they differ by rounding
(catmix100-800, methanol50, lop97icx).

The .gms file is read as text: every decimal literal is taken as the exact
rational number it denotes, and all arithmetic is exact (Fractions). The
cached MINLPLib OSIL is read the same way (attribute decimals as exact
rationals). Each row and the objective are expanded into rational functions
(numerator and denominator polynomials with Fraction coefficients); these
instances use only + - * / and sqr, so the expansion is exact and complete.
Rows are compared as rational functions (n1*d2 == n2*d1); polynomial rows and
the objective are also compared coefficient by coefficient. The OSIL
eliminates the objective variable objvar; the .gms objective is recovered by
solving its defining row for objvar.

No GAMS, no floating point: the comparison is exact under the stated reading
of both files. Variable bounds and types are not compared here (history.py
compared them exactly; they are equal).

Optionally the objective of both forms is evaluated exactly at an audit point
(bound-audit/sol/<name>.<p>.sol, decimals read as exact rationals; variables
missing from the file are 0, as in MINLPLib).

Usage: python3 exact_forms.py [name ...]
Output: data/exact_forms.json, printed summary (logs/exact_forms.log)
"""
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.abspath(os.path.join(HERE, "..", ".."))
OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil")
NS = "{os.optimizationservices.org}"
NAMES = ["catmix100", "catmix200", "catmix400", "catmix800", "methanol50", "lop97icx"]
POINTS = {"methanol50": "p4", "lop97icx": "p2"}
ONE = ()  # the empty monomial

# ---------------------------------------------------------------- polynomials
# A polynomial is a dict {monomial: Fraction}; a monomial is a sorted tuple of
# (variable name, exponent). A rational function is a pair (num, den).


def p_const(c):
    return {ONE: F(c)} if c != 0 else {}


def p_var(v):
    return {((v, 1),): F(1)}


def p_add(a, b, s=1):
    r = dict(a)
    for m, c in b.items():
        v = r.get(m, 0) + s * c
        if v:
            r[m] = v
        else:
            r.pop(m, None)
    return r


def m_mul(m1, m2):
    d = dict(m1)
    for v, e in m2:
        d[v] = d.get(v, 0) + e
    return tuple(sorted(d.items()))


def p_mul(a, b):
    r = {}
    for m1, c1 in a.items():
        for m2, c2 in b.items():
            m = m_mul(m1, m2)
            v = r.get(m, 0) + c1 * c2
            if v:
                r[m] = v
            else:
                r.pop(m, None)
    return r


def is_one(p):
    return p == {ONE: F(1)}


def r_add(x, y, s=1):
    (n1, d1), (n2, d2) = x, y
    if d1 == d2:
        return (p_add(n1, n2, s), d1)
    return (p_add(p_mul(n1, d2), p_mul(n2, d1), s), p_mul(d1, d2))


def r_mul(x, y):
    return (p_mul(x[0], y[0]), p_mul(x[1], y[1]))


def r_div(x, y):
    n2, d2 = y
    if len(n2) == 1 and ONE in n2:  # division by a constant
        c = n2[ONE]
        return ({m: v / c for m, v in x[0].items()}, p_mul(x[1], d2))
    return (p_mul(x[0], d2), p_mul(x[1], n2))


def r_neg(x):
    return ({m: -c for m, c in x[0].items()}, x[1])


def r_pow(x, k):
    assert k == int(k) and k >= 0, k
    r = (p_const(1), p_const(1))
    for _ in range(int(k)):
        r = r_mul(r, x)
    return r


def R_(p):
    return (p, p_const(1))


def r_equal(x, y):
    return p_add(p_mul(x[0], y[1]), p_mul(y[0], x[1]), -1) == {}


# ---------------------------------------------------------------- GAMS text
TOK = re.compile(r"\s*(?:(\d+\.?\d*(?:[eE][+-]?\d+)?|\.\d+(?:[eE][+-]?\d+)?)|([A-Za-z_][A-Za-z0-9_]*)|(\*\*|[-+*/(),]))")


def tokens(s):
    out, i = [], 0
    s = s.rstrip()
    while i < len(s):
        m = TOK.match(s, i)
        if not m or m.end() == i:
            raise ValueError(f"cannot tokenize at {s[i:i + 30]!r}")
        i = m.end()
        if m.group(1):
            out.append(("num", m.group(1)))
        elif m.group(2):
            out.append(("id", m.group(2)))
        else:
            out.append(("op", m.group(3)))
    return out


class Parser:
    """expr := term (('+'|'-') term)*; term := unary (('*'|'/') unary)*;
    unary := ('-'|'+') unary | power; power := atom ('**' unary)?"""

    def __init__(self, toks):
        self.t, self.i = toks, 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else (None, None)

    def take(self, val=None):
        tok = self.peek()
        if val is not None and tok[1] != val:
            raise ValueError(f"expected {val}, got {tok}")
        self.i += 1
        return tok

    def expr(self):
        x = self.term()
        while self.peek()[1] in ("+", "-"):
            s = 1 if self.take()[1] == "+" else -1
            x = r_add(x, self.term(), s)
        return x

    def term(self):
        x = self.unary()
        while self.peek()[1] in ("*", "/"):
            op = self.take()[1]
            y = self.unary()
            x = r_mul(x, y) if op == "*" else r_div(x, y)
        return x

    def unary(self):
        if self.peek()[1] == "-":
            self.take()
            return r_neg(self.unary())
        if self.peek()[1] == "+":
            self.take()
            return self.unary()
        return self.power()

    def power(self):
        x = self.atom()
        if self.peek()[1] == "**":
            self.take()
            e = self.unary()
            assert e[1] == p_const(1) and set(e[0]) <= {ONE}, "non-constant exponent"
            x = r_pow(x, e[0].get(ONE, F(0)))
        return x

    def atom(self):
        kind, val = self.take()
        if kind == "num":
            return R_(p_const(F(val)))
        if kind == "id":
            if self.peek()[1] == "(":
                self.take("(")
                args = [self.expr()]
                while self.peek()[1] == ",":
                    self.take(",")
                    args.append(self.expr())
                self.take(")")
                f = val.lower()
                if f == "sqr":
                    return r_mul(args[0], args[0])
                if f == "power":
                    e = args[1]
                    assert e[1] == p_const(1) and set(e[0]) <= {ONE}
                    return r_pow(args[0], e[0].get(ONE, F(0)))
                raise NotImplementedError(f"function {val}")
            return R_(p_var(val))
        if val == "(":
            x = self.expr()
            self.take(")")
            return x
        raise ValueError(f"unexpected token {val}")


def read_gms(path):
    text = open(path).read()
    sense = re.search(r"(?mi)^Solve\s+\w+\s+using\s+\S+\s+(minimizing|maximizing)\s+(\w+)", text)
    rows = {}
    for m in re.finditer(r"(?ms)^(e\d+)\.\.(.*?);", text):
        name, body = m.group(1), m.group(2)
        parts = re.split(r"=([EeLlGg])=", body)
        assert len(parts) == 3, name
        lhs = Parser(tokens(parts[0]))
        a = lhs.expr()
        assert lhs.i == len(lhs.t)
        rhs = Parser(tokens(parts[2]))
        b = rhs.expr()
        assert rhs.i == len(rhs.t)
        rows[name] = (parts[1].upper(), r_add(a, b, -1))  # lhs - rhs (sense) 0
    return dict(sense="min" if sense.group(1).lower() == "minimizing" else "max", objvar=sense.group(2), rows=rows)


# ---------------------------------------------------------------- OSIL
def els(node, cast):
    out = []
    for e in node:
        mult = int(e.get("mult", 1))
        v = cast(e.text)
        inc = cast(e.get("incr", "0"))
        for k in range(mult):
            out.append(v + k * inc)
    return out


def read_osil(path):
    d = ET.parse(path).getroot().find(NS + "instanceData")
    var = [v.get("name") for v in d.find(NS + "variables")]
    assert all("mult" not in v.attrib for v in d.find(NS + "variables"))
    cons = list(d.find(NS + "constraints")) if d.find(NS + "constraints") is not None else []
    assert all("mult" not in c.attrib for c in cons)
    body = [R_(p_const(F(c.get("constant", "0")))) for c in cons]
    obj = d.find(NS + "objectives")[0]
    ob = R_(p_const(F(obj.get("constant", "0"))))
    for c in obj:
        ob = r_add(ob, R_({((var[int(c.get("idx"))], 1),): F(c.text)}))
    lc = d.find(NS + "linearConstraintCoefficients")
    if lc is not None:
        start = els(lc.find(NS + "start"), int)
        rowmajor = lc.find(NS + "colIdx") is not None
        idx = els(lc.find(NS + "colIdx" if rowmajor else NS + "rowIdx"), int)
        val = els(lc.find(NS + "value"), F)
        for k in range(len(start) - 1):
            for j in range(start[k], start[k + 1]):
                r, v = (k, idx[j]) if rowmajor else (idx[j], k)
                body[r] = r_add(body[r], R_({((var[v], 1),): val[j]}))
    q = d.find(NS + "quadraticCoefficients")
    if q is not None:
        for t in q:
            r = int(t.get("idx"))
            term = R_(p_mul({((var[int(t.get("idxOne"))], 1),): F(t.get("coef", "1"))},
                            p_var(var[int(t.get("idxTwo"))])))
            if r == -1:
                ob = r_add(ob, term)
            else:
                body[r] = r_add(body[r], term)
    nl = d.find(NS + "nonlinearExpressions")
    if nl is not None:
        for e in nl:
            r = int(e.get("idx"))
            t = tree(e[0], var)
            if r == -1:
                ob = r_add(ob, t)
            else:
                body[r] = r_add(body[r], t)
    rows = {}
    for c, b in zip(cons, body):
        lb, ub = c.get("lb"), c.get("ub")
        rows[c.get("name")] = (b, None if lb is None else F(lb), None if ub is None else F(ub))
    return dict(sense=obj.get("maxOrMin", "min"), obj=ob, rows=rows)


def tree(e, var):
    tag = e.tag[len(NS):]
    ch = [tree(c, var) for c in e]
    if tag == "number":
        return R_(p_const(F(e.get("value"))))
    if tag == "variable":
        return R_({((var[int(e.get("idx"))], 1),): F(e.get("coef", "1"))})
    if tag in ("sum", "plus"):
        r = R_({})
        for c in ch:
            r = r_add(r, c)
        return r
    if tag in ("product", "times"):
        r = R_(p_const(1))
        for c in ch:
            r = r_mul(r, c)
        return r
    if tag == "minus":
        return r_add(ch[0], ch[1], -1)
    if tag == "negate":
        return r_neg(ch[0])
    if tag == "divide":
        return r_div(ch[0], ch[1])
    if tag == "square":
        return r_mul(ch[0], ch[0])
    if tag == "power":
        e2 = ch[1]
        assert e2[1] == p_const(1) and set(e2[0]) <= {ONE}
        return r_pow(ch[0], e2[0].get(ONE, F(0)))
    raise NotImplementedError(tag)


# ---------------------------------------------------------------- compare
def coef_diffs(a, b):
    """coefficientwise differences of two polynomials: list of
    (monomial, coef_a, coef_b)"""
    out = []
    for m in set(a) | set(b):
        ca, cb = a.get(m, F(0)), b.get(m, F(0))
        if ca != cb:
            out.append((m, ca, cb))
    return out


def summarize(diffs):
    if not diffs:
        return dict(n=0)
    absd = [abs(cb - ca) for _, ca, cb in diffs]
    rel = [abs(cb - ca) / abs(ca) if ca else None for _, ca, cb in diffs]
    pairs = sorted({(str(ca), str(cb)) for _, ca, cb in diffs}, key=lambda p: F(p[0]))
    return dict(n=len(diffs), max_abs=float(max(absd)),
                max_rel=float(max(r for r in rel if r is not None)) if any(r is not None for r in rel) else None,
                min_rel=float(min(r for r in rel if r is not None)) if any(r is not None for r in rel) else None,
                new_or_removed_terms=sum(1 for r in rel if r is None),
                distinct_pairs=len(pairs),
                examples=[(float(F(a)), float(F(b)), float(abs(F(b) - F(a)) / abs(F(a))) if F(a) else None)
                          for a, b in pairs[:6]])


def gms_objective(g):
    """solve the defining row a*objvar + rest = 0 (a = +-1) for objvar"""
    ov = g["objvar"]
    m = ((ov, 1),)
    hits = [n for n, (_, r) in g["rows"].items() if any(v == ov for mono in r[0] for v, _ in mono)]
    assert len(hits) == 1, hits
    n = hits[0]
    s, (num, den) = g["rows"][n]
    assert s == "E" and is_one(den)
    a = num[m]
    assert abs(a) == 1 and all(not any(v == ov for v, _ in mono) for mono in num if mono != m)
    rest = {k: v for k, v in num.items() if k != m}
    return n, {k: -v / a for k, v in rest.items()}


def compare(name):
    g = read_gms(os.path.join(HERE, "pages", "models", "gms", name + ".gms"))
    o = read_osil(os.path.join(OSIL, name + ".osil"))
    objrow, gobj = gms_objective(g)
    assert is_one(o["obj"][1]), "OSIL objective not polynomial"
    res = dict(name=name, sense=(g["sense"], o["sense"]), objective_row=objrow,
               rows_gms=len(g["rows"]) - 1, rows_osil=len(o["rows"]))
    res["objective"] = summarize(coef_diffs(gobj, o["obj"][0]))
    rows_equal, rows_diff, row_coef = 0, [], []
    for n, (s, gr) in g["rows"].items():
        if n == objrow:
            continue
        ob, lb, ub = o["rows"][n]
        # OSIL row: lb <= body <= ub; .gms row: (lhs - rhs) sense 0
        if s == "E":
            assert lb == ub
            target = r_add(ob, R_(p_const(lb)), -1)
        else:  # one-sided row; orient the OSIL row like the .gms row
            assert (lb is None) != (ub is None), (n, lb, ub)
            target = r_add(ob, R_(p_const(lb if ub is None else ub)), -1)
            if (s == "L") != (ub is not None):
                target = r_neg(target)
        if r_equal(gr, target) or (s == "E" and r_equal(gr, r_neg(target))):
            rows_equal += 1
            continue
        rows_diff.append(n)
        if is_one(gr[1]) and is_one(target[1]):
            d1, d2 = coef_diffs(gr[0], target[0]), coef_diffs(gr[0], r_neg(target)[0])
            row_coef += d1 if (s != "E" or len(d1) <= len(d2)) else d2
    res.update(rows_equal=rows_equal, rows_different=len(rows_diff), rows_different_names=rows_diff[:10],
               rows_coefficients=summarize(row_coef))
    p = POINTS.get(name)
    if p:
        sol = {}
        for line in open(os.path.join(R, "bound-audit", "sol", f"{name}.{p}.sol")):
            k, v = line.split()
            sol[k] = F(v)

        def ev(poly):
            tot = F(0)
            for mono, c in poly.items():
                t = c
                for v, e in mono:
                    t *= sol.get(v, F(0)) ** e  # MINLPLib: missing variables are 0
                tot += t
            return tot
        vg, vo = ev(gobj), ev(o["obj"][0])
        res["point"] = dict(point=p, obj_gms=str(vg), obj_osil=str(vo), gms_minus_osil=float(vg - vo),
                            obj_gms_decimal=f"{float(vg):.17g}", obj_osil_dec25=dec(vo, 25), obj_gms_dec25=dec(vg, 25))
    return res


def dec(x, digits):
    """x as a decimal string with `digits` digits after the point (exact rounding toward zero)"""
    s = "-" if x < 0 else ""
    x = abs(x)
    ip = x.numerator // x.denominator
    fr = x - ip
    return f"{s}{ip}." + str((fr * 10 ** digits).numerator // (fr * 10 ** digits).denominator).zfill(digits)


def main():
    names = sys.argv[1:] or NAMES
    out = {}
    for n in names:
        r = compare(n)
        out[n] = r
        print(json.dumps(r, default=str), flush=True)
    path = os.path.join(HERE, "data", "exact_forms.json")
    old = json.load(open(path)) if os.path.exists(path) else {}
    old.update(out)
    json.dump(old, open(path, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
