"""Minimal OSiL reader that keeps every constant as an exact Fraction, plus
exact (Fraction) and outward-rounded interval (mpmath.iv) evaluation.

Written for this track; it does not import the other readers in the repository.

OSiL 2.0 conventions used:
- var: lb default 0, ub default +INF (binary: ub default 1), type default C;
- con: lb default -INF, ub default +INF, constant default 0;
- obj: constant default 0, linear terms as <coef idx=..>;
- linear coefficients: start + (colIdx | rowIdx) + value, each possibly
  compressed with <el mult=.. incr=..>;
- quadratic terms: qTerm idx (-1 = objective), idxOne, idxTwo, coef;
- nonlinear expressions: one tree per row (idx -1 = objective).
Unknown attributes or tree nodes raise, so nothing is silently ignored.
"""
import xml.etree.ElementTree as ET
from fractions import Fraction

NS = "{os.optimizationservices.org}"
INF_STRINGS = {"INF", "+INF", "-INF", "Infinity", "-Infinity"}


def _tag(e):
    return e.tag.replace(NS, "")


def _bound(s):
    """None for an infinite bound, else the exact Fraction."""
    return None if s.strip() in INF_STRINGS else Fraction(s.strip())


def _expand(parent, conv):
    out = []
    for e in parent:
        assert _tag(e) == "el", _tag(e)
        assert set(e.attrib) <= {"mult", "incr"}, e.attrib
        mult = int(e.get("mult", "1"))
        incr = e.get("incr")
        text = e.text.strip()
        if incr is None:
            out += [conv(text)] * mult
        else:
            base, step = conv(text), conv(incr)
            out += [base + k * step for k in range(mult)]
    return out


def _tree(e):
    t = _tag(e)
    if t == "number":
        assert set(e.attrib) <= {"value", "type"} and e.get("type", "real") == "real", e.attrib
        assert len(e) == 0
        return ("num", Fraction(e.get("value", "0")))
    if t == "variable":
        assert set(e.attrib) <= {"idx", "coef"}, e.attrib
        assert len(e) == 0
        return ("var", int(e.get("idx")), Fraction(e.get("coef", "1")))
    assert not e.attrib, (t, e.attrib)
    return (t,) + tuple(_tree(c) for c in e)


def read(path):
    root = ET.parse(path).getroot()
    data = root.find(NS + "instanceData")
    V = data.find(NS + "variables")
    names, lb, ub, vtype = [], [], [], []
    for v in V:
        assert _tag(v) == "var" and set(v.attrib) <= {"name", "lb", "ub", "type"}, v.attrib
        typ = v.get("type", "C")
        names.append(v.get("name"))
        vtype.append(typ)
        lb.append(_bound(v.get("lb", "0")))
        ub.append(_bound(v.get("ub", "1" if typ == "B" else "INF")))
    n = len(names)
    assert n == int(V.get("numberOfVariables"))

    objs = data.find(NS + "objectives")
    assert len(objs) == 1
    o = objs[0]
    assert set(o.attrib) <= {"maxOrMin", "name", "numberOfObjCoef", "constant", "weight"}, o.attrib
    assert o.get("weight", "1") == "1"
    obj = dict(sense=o.get("maxOrMin", "min"), constant=Fraction(o.get("constant", "0")),
               lin={}, quad=[], nl=None, name=o.get("name"))
    for c in o:
        assert _tag(c) == "coef"
        obj["lin"][int(c.get("idx"))] = Fraction(c.text.strip())
    assert len(obj["lin"]) == int(o.get("numberOfObjCoef", "0"))

    C = data.find(NS + "constraints")
    cons = []
    for c in (C if C is not None else []):
        assert _tag(c) == "con" and set(c.attrib) <= {"name", "lb", "ub", "constant"}, c.attrib
        cons.append(dict(name=c.get("name"), lb=_bound(c.get("lb", "-INF")), ub=_bound(c.get("ub", "INF")),
                         constant=Fraction(c.get("constant", "0")), lin={}, quad=[], nl=None))
    if C is not None:
        assert len(cons) == int(C.get("numberOfConstraints"))

    L = data.find(NS + "linearConstraintCoefficients")
    if L is not None:
        start = _expand(L.find(NS + "start"), int)
        vals = _expand(L.find(NS + "value"), Fraction)
        ri, ci = L.find(NS + "rowIdx"), L.find(NS + "colIdx")
        assert (ri is None) != (ci is None)
        idx = _expand(ri if ri is not None else ci, int)
        assert len(vals) == len(idx) == int(L.get("numberOfValues"))
        if ci is not None:  # row-major
            assert len(start) == len(cons) + 1
            for r in range(len(cons)):
                for k in range(start[r], start[r + 1]):
                    assert idx[k] not in cons[r]["lin"]
                    cons[r]["lin"][idx[k]] = vals[k]
        else:  # column-major
            assert len(start) == n + 1
            for col in range(n):
                for k in range(start[col], start[col + 1]):
                    assert col not in cons[idx[k]]["lin"]
                    cons[idx[k]]["lin"][col] = vals[k]

    Q = data.find(NS + "quadraticCoefficients")
    if Q is not None:
        for q in Q:
            assert _tag(q) == "qTerm" and set(q.attrib) <= {"idx", "idxOne", "idxTwo", "coef"}, q.attrib
            r = int(q.get("idx"))
            term = (int(q.get("idxOne")), int(q.get("idxTwo")), Fraction(q.get("coef", "1")))
            (obj if r == -1 else cons[r])["quad"].append(term)
        assert len(Q) == int(Q.get("numberOfQuadraticTerms"))

    N = data.find(NS + "nonlinearExpressions")
    if N is not None:
        for e in N:
            assert _tag(e) == "nl" and len(e) == 1
            r = int(e.get("idx"))
            target = obj if r == -1 else cons[r]
            assert target["nl"] is None
            target["nl"] = _tree(e[0])
    for blk in data:
        assert _tag(blk) in {"variables", "objectives", "constraints", "linearConstraintCoefficients",
                             "quadraticCoefficients", "nonlinearExpressions"}, _tag(blk)
    return dict(names=names, lb=lb, ub=ub, vtype=vtype, obj=obj, cons=cons)


# --------------------------------------------------------------------------------------------
# Evaluation. `A` is an arithmetic adapter: A.const(Fraction) -> number, A.square(v),
# A.power(base, expo, expo_tree), plus the usual + - * operators on its numbers.

class ExactArith:
    """Exact rational arithmetic; only polynomial operations are allowed."""

    @staticmethod
    def const(q):
        return q

    @staticmethod
    def square(v):
        return v * v

    @staticmethod
    def power(base, expo, expo_tree):
        assert expo.denominator == 1 and expo >= 0, "non-integer power cannot be evaluated exactly"
        return base ** int(expo)


class IntervalArith:
    """mpmath.iv arithmetic (outward rounded). Assumes mpmath.iv encloses exp and log correctly."""

    def __init__(self, iv):
        self.iv = iv

    def const(self, q):
        iv = self.iv
        return iv.mpf(q.numerator) / iv.mpf(q.denominator)

    @staticmethod
    def square(v):
        return v ** 2  # mpmath iv: even power, lower end >= 0

    def power(self, base, expo, expo_tree):
        iv = self.iv
        if expo_tree[0] == "num" and expo_tree[1].denominator == 1 and expo_tree[1] >= 0:
            return base ** int(expo_tree[1])
        # real power with a non-constant or non-integer exponent: base must be > 0
        assert base.a > 0, "power base interval not strictly positive"
        return iv.exp(expo * iv.log(base))


def eval_tree(t, x, A):
    op = t[0]
    if op == "num":
        return A.const(t[1])
    if op == "var":
        return x[t[1]] if t[2] == 1 else A.const(t[2]) * x[t[1]]
    k = [eval_tree(c, x, A) for c in t[1:]]
    if op in ("sum", "plus"):
        s = k[0]
        for v in k[1:]:
            s = s + v
        return s
    if op in ("times", "product"):
        s = k[0]
        for v in k[1:]:
            s = s * v
        return s
    if op == "minus":
        return k[0] - k[1]
    if op == "negate":
        return -k[0]
    if op == "square":
        return A.square(k[0])
    if op == "power":
        return A.power(k[0], k[1], t[2])
    raise ValueError(f"unsupported operator {op}")


def eval_row(row, x, A):
    """Row body value (linear + quadratic + nonlinear + constant)."""
    v = A.const(row["constant"])
    for j, c in row["lin"].items():
        v = v + A.const(c) * x[j]
    for i, j, c in row["quad"]:
        v = v + A.const(c) * x[i] * x[j]
    if row["nl"] is not None:
        v = v + eval_tree(row["nl"], x, A)
    return v
