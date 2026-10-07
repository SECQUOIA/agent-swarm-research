"""Exact check of the chain points in points/chainN_generator.json against the cached OSIL files.

Written separately from build_points.py and shares no code with it:
  - its own OSIL reader (xml.etree; every constant kept as an exact rational);
  - its own arithmetic in the quadratic field Q(sqrt(R)) with exact sign tests;
  - the point is rebuilt from the generator's definition, then every variable
    bound, integrality requirement, row and the objective are evaluated from
    the OSIL expression trees in exact arithmetic. sqrt is evaluated exactly:
    the root is searched in Q(sqrt(R)) and accepted only if its square equals
    the argument exactly and it is nonnegative.
  - the objective value (an exact element of Q(sqrt(R))) is enclosed by integer
    square roots, and the gap to the certified dual bound is computed exactly.
  - the box file (decimal centres, common radius) is checked to contain the
    exact point; then rows and objective are re-evaluated over the box with
    mpmath interval arithmetic as a consistency check.

Usage: python3 verify_points.py 50 100 200 400
"""
import json
import math
import os
import sys
import xml.etree.ElementTree as ET
from fractions import Fraction

import mpmath as mp

sys.set_int_max_str_digits(0)
HERE = os.path.dirname(os.path.abspath(__file__))
R29 = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))  # research-20260929/
OSIL = os.path.join(os.path.expanduser("~/.cache/minlplib/minlplib/osil"), "chain%d.osil")
BOUND = os.path.join(R29, "open-instances-wave2/cops/logs/chain%d_bound.json")
INF = ("INF", "+INF", "-INF", "inf", "-inf", "Infinity", "-Infinity")


# ----------------------------------------------------------------- OSIL reader
def tag(e):
    return e.tag.split("}")[-1]


def expand(parent, as_int):
    out = []
    for el in parent:
        assert tag(el) == "el"
        mult = int(el.get("mult", "1"))
        incr = el.get("incr")
        v = el.text.strip()
        if as_int:
            v0, d = int(v), int(incr or 0)
            out += [v0 + k * d for k in range(mult)]
        else:
            v0, d = Fraction(v), Fraction(incr or 0)
            out += [v0 + k * d for k in range(mult)]
    return out


def tree(e):
    t = tag(e)
    if t == "number":
        assert e.get("type", "real") == "real" and len(e) == 0
        return ("num", Fraction(e.get("value")))
    if t == "variable":
        assert len(e) == 0
        return ("var", int(e.get("idx")), Fraction(e.get("coef", "1")))
    return (t,) + tuple(tree(c) for c in e)


def read_osil(path):
    root = ET.parse(path).getroot()
    data = [c for c in root if tag(c) == "instanceData"][0]
    sec = {tag(c): c for c in data}
    allowed = {"variables", "objectives", "constraints", "linearConstraintCoefficients",
               "quadraticCoefficients", "nonlinearExpressions"}
    assert set(sec) <= allowed, set(sec) - allowed
    var = []
    for v in sec["variables"]:
        assert tag(v) == "var"
        typ = v.get("type", "C")
        var.append(dict(name=v.get("name"), type=typ, lb=v.get("lb", "0"),
                        ub=v.get("ub", "1" if typ == "B" else "INF")))
    assert len(var) == int(sec["variables"].get("numberOfVariables"))
    objs = list(sec["objectives"])
    assert len(objs) == 1
    o = objs[0]
    obj = dict(sense=o.get("maxOrMin", "min"), constant=Fraction(o.get("constant", "0")),
               lin={int(c.get("idx")): Fraction(c.text.strip()) for c in o}, quad=[], nl=None)
    cons = [dict(name=c.get("name"), lb=c.get("lb", "-INF"), ub=c.get("ub", "INF"),
                 constant=Fraction(c.get("constant", "0")), lin={}, quad=[], nl=None)
            for c in sec.get("constraints", [])]
    if "linearConstraintCoefficients" in sec:
        L = {tag(c): c for c in sec["linearConstraintCoefficients"]}
        start = expand(L["start"], True)
        val = expand(L["value"], False)
        if "colIdx" in L:          # row-major
            idx = expand(L["colIdx"], True)
            assert len(start) == len(cons) + 1
            for r in range(len(cons)):
                for k in range(start[r], start[r + 1]):
                    assert idx[k] not in cons[r]["lin"]
                    cons[r]["lin"][idx[k]] = val[k]
        else:                      # column-major
            idx = expand(L["rowIdx"], True)
            assert len(start) == len(var) + 1
            for j in range(len(var)):
                for k in range(start[j], start[j + 1]):
                    assert j not in cons[idx[k]]["lin"]
                    cons[idx[k]]["lin"][j] = val[k]
        assert len(val) == int(sec["linearConstraintCoefficients"].get("numberOfValues"))
    if "quadraticCoefficients" in sec:
        for q in sec["quadraticCoefficients"]:
            r = int(q.get("idx"))
            term = (int(q.get("idxOne")), int(q.get("idxTwo")), Fraction(q.get("coef", "1")))
            (obj if r == -1 else cons[r])["quad"].append(term)
    if "nonlinearExpressions" in sec:
        for e in sec["nonlinearExpressions"]:
            r = int(e.get("idx"))
            assert len(e) == 1
            tgt = obj if r == -1 else cons[r]
            assert tgt["nl"] is None
            tgt["nl"] = tree(e[0])
    return var, obj, cons


# ----------------------------------------------------------- field Q(sqrt R)
class Field:
    def __init__(self, R):
        assert R > 0 and math.isqrt(R) ** 2 != R, "R must be a positive non-square"
        self.R = R

    def el(self, a, b=0):
        return (Fraction(a), Fraction(b))

    def add(self, x, y):
        return (x[0] + y[0], x[1] + y[1])

    def sub(self, x, y):
        return (x[0] - y[0], x[1] - y[1])

    def mul(self, x, y):
        return (x[0] * y[0] + self.R * x[1] * y[1], x[0] * y[1] + x[1] * y[0])

    def inv(self, x):
        n = x[0] * x[0] - self.R * x[1] * x[1]
        if n == 0:
            raise ZeroDivisionError
        return (x[0] / n, -x[1] / n)

    def sgn(self, x):
        a, b = x
        sa = (a > 0) - (a < 0)
        sb = (b > 0) - (b < 0)
        if sb == 0:
            return sa
        if sa == 0 or sa == sb:
            return sb
        # a and b sqrt(R) have opposite signs: the larger magnitude wins
        return sa if a * a > self.R * b * b else sb

    def sqrt(self, y):
        """exact nonnegative square root of y inside the field, or raise."""
        assert self.sgn(y) >= 0
        a, b = y
        if b == 0:
            r = rat_sqrt(a)
            if r is not None:
                return (r, Fraction(0))
            r = rat_sqrt(a / self.R)       # a = c^2 R  ->  sqrt = c sqrt(R)
            if r is not None:
                return (Fraction(0), r)
            raise ValueError("sqrt not in field")
        nrm = rat_sqrt(a * a - self.R * b * b)
        if nrm is None:
            raise ValueError("sqrt not in field (norm)")
        for m2 in ((a + nrm) / 2, (a - nrm) / 2):
            m = rat_sqrt(m2) if m2 > 0 else None
            if m is None:
                continue
            z = (m, b / (2 * m))
            if self.sgn(z) < 0:
                z = (-z[0], -z[1])
            if self.mul(z, z) == y:
                return z
        raise ValueError("sqrt not in field")

    def enclose(self, x, k):
        r = math.isqrt(self.R * 10 ** (2 * k))
        lo, hi = Fraction(r, 10 ** k), Fraction(r + 1, 10 ** k)
        v1, v2 = x[0] + x[1] * lo, x[0] + x[1] * hi
        return min(v1, v2), max(v1, v2)


def rat_sqrt(q):
    if q < 0:
        return None
    n, d = q.numerator, q.denominator
    rn, rd = math.isqrt(n), math.isqrt(d)
    return Fraction(rn, rd) if rn * rn == n and rd * rd == d else None


def ev(t, X, K):
    op = t[0]
    if op == "num":
        return K.el(t[1])
    if op == "var":
        return K.mul(K.el(t[2]), X[t[1]])
    args = [ev(c, X, K) for c in t[1:]]
    if op in ("sum", "plus"):
        s = K.el(0)
        for a in args:
            s = K.add(s, a)
        return s
    if op in ("product", "times"):
        s = K.el(1)
        for a in args:
            s = K.mul(s, a)
        return s
    if op == "minus":
        return K.sub(args[0], args[1])
    if op == "negate":
        return K.sub(K.el(0), args[0])
    if op == "divide":
        return K.mul(args[0], K.inv(args[1]))
    if op == "square":
        return K.mul(args[0], args[0])
    if op == "sqrt":
        return K.sqrt(args[0])
    raise NotImplementedError(op)


def ev_row(row, X, K):
    s = K.el(row["constant"])
    for j, c in row["lin"].items():
        s = K.add(s, K.mul(K.el(c), X[j]))
    for i, j, c in row["quad"]:
        s = K.add(s, K.mul(K.el(c), K.mul(X[i], X[j])))
    if row["nl"] is not None:
        s = K.add(s, ev(row["nl"], X, K))
    return s


# ------------------------------------------------------------ rebuild point
def rebuild(gen):
    N, a, b = gen["N"], gen["a"], gen["b"]
    assert 0 < a < b < N
    w = [1] + [2] * (N - 1) + [1]
    t = {i: Fraction(gen["t"][i]) for i in range(N + 1) if i not in (a, b)}
    assert all(gen["t"][i] is None for i in (a, b)) and all(v > 0 for v in t.values())
    assert all(len(gen["t"][i].split(".")[1]) == gen["decimal_places"] for i in t)
    alpha = (12 * N - sum(w[i] * t[i] for i in t)) / 2
    beta = (4 * N - sum(w[i] / t[i] for i in t)) / 2
    disc = alpha * alpha - 4 * alpha / beta
    # sqrt(disc) = sqrt(R) / den with R = num * den
    R = disc.numerator * disc.denominator
    assert str(R) == gen["R"]
    K = Field(R)
    sq = (Fraction(0), Fraction(1, disc.denominator))
    r1 = K.sub(K.el(alpha / 2), K.mul(K.el(Fraction(1, 2)), sq))   # smaller root
    r2 = K.add(K.el(alpha / 2), K.mul(K.el(Fraction(1, 2)), sq))   # larger root
    assert K.mul(sq, sq) == K.el(disc)
    ta, tb = (r1, r2) if gen["root_a"] == "smaller" else (r2, r1)
    T = [K.el(t[i]) if i in t else (ta if i == a else tb) for i in range(N + 1)]
    half = K.el(Fraction(1, 2))
    u = [K.mul(half, K.sub(Ti, K.inv(Ti))) for Ti in T]
    eta = Fraction(1, 2 * N)
    x = [K.el(1)]
    for i in range(N):
        x.append(K.add(x[i], K.mul(K.el(eta), K.add(u[i], u[i + 1]))))
    return K, x + u, T


def check(N, log):
    gen = json.load(open("%s/points/chain%d_generator.json" % (HERE, N)))
    box = json.load(open("%s/points/chain%d_box.json" % (HERE, N)))
    var, obj, cons = read_osil(OSIL % N)
    K, X, T = rebuild(gen)
    assert len(X) == len(var) == 2 * N + 2
    out = dict(instance="chain%d" % N, n_vars=len(var), n_rows=len(cons), R_digits=len(gen["R"]))
    # t_a, t_b > 0 (so that u and the rows are defined and the roots are the intended ones)
    out["t_free_positive"] = all(K.sgn(T[i]) > 0 for i in (gen["a"], gen["b"]))
    assert out["t_free_positive"]
    # variable bounds and integrality
    nb = 0
    for j, v in enumerate(var):
        if v["type"] != "C":
            assert X[j][1] == 0 and X[j][0].denominator == 1, "integrality"
            if v["type"] == "B":
                assert X[j][0] in (0, 1)
        if v["lb"] not in INF:
            assert K.sgn(K.sub(X[j], K.el(Fraction(v["lb"])))) >= 0, (j, "lb")
            nb += 1
        if v["ub"] not in INF:
            assert K.sgn(K.sub(K.el(Fraction(v["ub"])), X[j])) >= 0, (j, "ub")
            nb += 1
    out["finite_bounds_checked"] = nb
    out["integer_or_binary_vars"] = sum(v["type"] != "C" for v in var)
    # rows
    nz = 0
    for r, c in enumerate(cons):
        val = ev_row(c, X, K)
        if c["lb"] not in INF:
            assert K.sgn(K.sub(val, K.el(Fraction(c["lb"])))) >= 0, (r, "row lb")
        if c["ub"] not in INF:
            assert K.sgn(K.sub(K.el(Fraction(c["ub"])), val)) >= 0, (r, "row ub")
        if c["lb"] == c["ub"] and c["lb"] not in INF:
            nz += (val == K.el(Fraction(c["lb"])))
    out["rows_checked"] = len(cons)
    out["equality_rows_exact"] = nz
    # objective
    assert obj["sense"] == "min"
    f = ev_row(obj, X, K)
    lo, hi = K.enclose(f, 60)
    out["objective_lo"] = dec(lo, 40, "down")
    out["objective_hi"] = dec(hi, 40, "up")
    bj = json.load(open(BOUND % N))
    L = Fraction(bj["bnb"]["bound"])                   # exact value of the certified double
    Ldisp = Fraction(repr(bj["bnb"]["bound"]))         # its shortest decimal display
    out["dual_bound_double_exact"] = dec(L, 40, "down")
    out["dual_bound_display"] = repr(bj["bnb"]["bound"])
    out["gap_abs_upper"] = dec(hi - L, 3, "up", sci=True)
    out["gap_rel_upper"] = dec((hi - L) / L, 3, "up", sci=True)
    out["gap_abs_upper_vs_display"] = dec(hi - min(L, Ldisp), 3, "up", sci=True)
    kkt = Fraction(bj["primal"]["kkt_value"])
    out["objective_minus_wave2_kkt_value_25digits"] = float(lo - kkt)
    # box containment, exact
    rad = Fraction(box["radius"])
    for j, v in enumerate(box["variables"]):
        assert v["index"] == j and v["name"] == var[j]["name"]
        c = Fraction(v["centre"])
        assert K.sgn(K.sub(X[j], K.el(c + rad))) <= 0 and K.sgn(K.sub(X[j], K.el(c - rad))) >= 0, j
    out["box_contains_point"] = True
    out["box_radius"] = box["radius"]
    # interval evaluation over the whole box (consistency, mpmath iv)
    mp.iv.dps = 60
    IX = [mp.iv.mpf([iv_const(Fraction(v["centre"]) - rad).a, iv_const(Fraction(v["centre"]) + rad).b])
          for v in box["variables"]]
    worst = Fraction(0)
    for c in cons:
        tgt = Fraction(c["lb"])
        assert c["lb"] == c["ub"]
        vlo, vhi = ends(iv_row(c, IX))
        assert vlo <= tgt <= vhi
        worst = max(worst, tgt - vlo, vhi - tgt)
    flo, fhi = ends(iv_row(obj, IX))
    out["iv_box_row_residual_max"] = dec(worst, 2, "up", sci=True)
    out["iv_box_objective"] = [dec(flo, 40, "down"), dec(fhi, 40, "up")]
    out["iv_box_gap_abs_upper"] = dec(fhi - L, 3, "up", sci=True)
    assert flo <= lo and hi <= fhi
    print(json.dumps(out, indent=1), file=log, flush=True)
    print(json.dumps(out, indent=1), flush=True)
    return out


def iv_tree(t, X):
    op = t[0]
    if op == "num":
        return iv_const(t[1])
    if op == "var":
        return iv_const(t[2]) * X[t[1]]
    a = [iv_tree(c, X) for c in t[1:]]
    if op in ("sum", "plus"):
        s = a[0]
        for v in a[1:]:
            s = s + v
        return s
    if op in ("product", "times"):
        s = a[0]
        for v in a[1:]:
            s = s * v
        return s
    if op == "square":
        return a[0] * a[0]
    if op == "sqrt":
        return mp.iv.sqrt(a[0])
    raise NotImplementedError(op)


def ends(x):
    """exact rational endpoints of an mpmath interval"""
    res = []
    for d in (x.a, x.b):
        with mp.workprec(4000):
            sign, man, e, _ = mp.mpf(d)._mpf_
        res.append((-1) ** sign * Fraction(man) * Fraction(2) ** e)
    return res


def iv_const(q):
    return mp.iv.mpf(q.numerator) / q.denominator


def iv_row(row, X):
    s = iv_const(row["constant"])
    for j, c in row["lin"].items():
        s = s + iv_const(c) * X[j]
    assert not row["quad"]
    if row["nl"] is not None:
        s = s + iv_tree(row["nl"], X)
    return s


def dec(q, k, mode, sci=False):
    if sci:
        if q == 0:
            return "0"
        e = math.floor(math.log10(abs(float(q)))) - k + 1
        sc = q / Fraction(10) ** e
        n = math.ceil(sc) if mode == "up" else math.floor(sc)
        sgn, d = ("-" if n < 0 else ""), str(abs(n))
        return "%s%s.%se%d" % (sgn, d[0], d[1:], e + len(d) - 1)
    n = q * 10 ** k
    n = math.ceil(n) if mode == "up" else math.floor(n)
    s = "-" if n < 0 else ""
    n = abs(n)
    return "%s%d.%0*d" % (s, n // 10 ** k, k, n % 10 ** k)


if __name__ == "__main__":
    with open("%s/logs/verify.log" % HERE, "a") as log:
        for arg in sys.argv[1:]:
            check(int(arg), log)
