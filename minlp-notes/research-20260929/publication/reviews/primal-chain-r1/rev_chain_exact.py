"""Reviewer's exact check of the primal-chain points (round 1).

Written by the reviewer; imports nothing from the track's code.

What it does, per N:
  1. Reads the cached OSIL file with its own parser. Every number is kept as
     an exact rational (fractions.Fraction). OSIL defaults are applied
     (variable lb = 0, ub = +inf, type C; row lb = -inf, ub = +inf). Unknown
     sections, attributes or expression operators raise an error.
  2. Rebuilds the point from points/chainN_generator.json, following the
     definition text in that file. Field elements are pairs (p, q) meaning
     p + q*sqrt(D), with D = disc a positive rational (not the integer R the
     track uses).
  3. Checks every variable bound, integrality requirement and row of the
     OSIL model exactly. A row "holds with equality" only if lhs - rhs has
     representation (0, 0) (a sufficient condition for the real value 0).
     Inequalities use an exact sign test.
     sqrt(y) is evaluated by lookup: candidates s_k = (t_k + 1/t_k)/2 are
     precomputed, and sqrt(y) := z only if z*z == y exactly and z >= 0
     (the nonnegative square root is unique, so this is exact).
  4. Encloses the objective with an integer square root of the numerator *
     denominator of D, rounds outward to 40 decimals, and computes the gap
     to the exact value of the certified double bound.
  5. Checks the box file: every centre is within the stated radius of the
     exact coordinate (exact sign tests), and names/indices match the OSIL.

Usage: python3 rev_chain_exact.py 50 100 200 400
"""
import json
import math
import os
import sys
import time
import xml.etree.ElementTree as ET
from fractions import Fraction as Q

sys.set_int_max_str_digits(0)

R29 = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))  # research-20260929/
TRACK = os.path.join(R29, "publication/primal/chain")
OSIL = os.path.join(os.path.expanduser("~/.cache/minlplib/minlplib/osil"), "chain%d.osil")
BOUND = os.path.join(R29, "open-instances-wave2/cops/logs/chain%d_bound.json")
PRIMAL = os.path.join(R29, "open-instances-wave2/cops/logs/chain%d_primal.txt")

POS_INF = object()
NEG_INF = object()


def num(s, default):
    if s is None:
        return default
    s = s.strip()
    if s in ("INF", "+INF", "Infinity", "+Infinity", "inf"):
        return POS_INF
    if s in ("-INF", "-Infinity", "-inf"):
        return NEG_INF
    return Q(s)


def local(e):
    return e.tag.rsplit("}", 1)[-1]


def expand_els(node, conv):
    """expand <el mult= incr=> lists"""
    out = []
    for el in node:
        assert local(el) == "el", local(el)
        assert set(el.attrib) <= {"mult", "incr"}, el.attrib
        m = int(el.attrib.get("mult", "1"))
        inc = conv(el.attrib.get("incr", "0"))
        v = conv(el.text)
        out.extend(v + k * inc for k in range(m))
    return out


def parse_expr(e):
    t = local(e)
    if t == "number":
        assert set(e.attrib) <= {"value", "type"} and e.attrib.get("type", "real") == "real"
        assert len(e) == 0
        return ("c", Q(e.attrib["value"]))
    if t == "variable":
        assert set(e.attrib) <= {"idx", "coef"} and len(e) == 0
        return ("v", int(e.attrib["idx"]), Q(e.attrib.get("coef", "1")))
    assert not e.attrib, (t, e.attrib)
    kids = [parse_expr(c) for c in e]
    arity = {"square": 1, "sqrt": 1, "negate": 1, "minus": 2, "divide": 2, "plus": 2, "times": 2}
    if t in arity:
        assert len(kids) == arity[t], (t, len(kids))
    elif t not in ("sum", "product"):
        raise NotImplementedError(t)
    return (t,) + tuple(kids)


def parse_osil(path):
    root = ET.parse(path).getroot()
    assert local(root) == "osil"
    data = [c for c in root if local(c) == "instanceData"]
    assert len(data) == 1
    secs = {}
    for c in data[0]:
        assert local(c) not in secs
        secs[local(c)] = c
    assert set(secs) <= {"variables", "objectives", "constraints", "linearConstraintCoefficients",
                         "quadraticCoefficients", "nonlinearExpressions"}, set(secs)
    V = []
    for v in secs["variables"]:
        assert local(v) == "var" and set(v.attrib) <= {"name", "lb", "ub", "type"}, v.attrib
        typ = v.attrib.get("type", "C")
        V.append(dict(name=v.attrib.get("name"), type=typ,
                      lb=num(v.attrib.get("lb"), Q(0)),
                      ub=num(v.attrib.get("ub"), Q(1) if typ == "B" else POS_INF)))
    assert len(V) == int(secs["variables"].attrib["numberOfVariables"])
    ob = list(secs["objectives"])
    assert len(ob) == 1
    o = ob[0]
    assert set(o.attrib) <= {"maxOrMin", "name", "numberOfObjCoef", "constant", "weight"}, o.attrib
    OBJ = dict(sense=o.attrib.get("maxOrMin", "min"), const=Q(o.attrib.get("constant", "0")),
               lin={}, quad=[], nl=None)
    for c in o:
        assert local(c) == "coef"
        OBJ["lin"][int(c.attrib["idx"])] = Q(c.text)
    assert len(OBJ["lin"]) == int(o.attrib.get("numberOfObjCoef", "0"))
    C = []
    if "constraints" in secs:
        for c in secs["constraints"]:
            assert local(c) == "con" and set(c.attrib) <= {"name", "lb", "ub", "constant"}, c.attrib
            C.append(dict(name=c.attrib.get("name"), lb=num(c.attrib.get("lb"), NEG_INF),
                          ub=num(c.attrib.get("ub"), POS_INF), const=Q(c.attrib.get("constant", "0")),
                          lin={}, quad=[], nl=None))
        assert len(C) == int(secs["constraints"].attrib["numberOfConstraints"])
    if "linearConstraintCoefficients" in secs:
        L = secs["linearConstraintCoefficients"]
        parts = {local(c): c for c in L}
        start = expand_els(parts["start"], int)
        vals = expand_els(parts["value"], Q)
        assert len(vals) == int(L.attrib["numberOfValues"])
        if "rowIdx" in parts:          # column major
            idx = expand_els(parts["rowIdx"], int)
            assert len(start) == len(V) + 1 and start[-1] == len(vals) == len(idx)
            for j in range(len(V)):
                for k in range(start[j], start[j + 1]):
                    assert j not in C[idx[k]]["lin"]
                    C[idx[k]]["lin"][j] = vals[k]
        else:
            idx = expand_els(parts["colIdx"], int)
            assert len(start) == len(C) + 1 and start[-1] == len(vals) == len(idx)
            for r in range(len(C)):
                for k in range(start[r], start[r + 1]):
                    assert idx[k] not in C[r]["lin"]
                    C[r]["lin"][idx[k]] = vals[k]
    if "quadraticCoefficients" in secs:
        for qt in secs["quadraticCoefficients"]:
            r = int(qt.attrib["idx"])
            (OBJ if r == -1 else C[r])["quad"].append(
                (int(qt.attrib["idxOne"]), int(qt.attrib["idxTwo"]), Q(qt.attrib.get("coef", "1"))))
    if "nonlinearExpressions" in secs:
        nls = list(secs["nonlinearExpressions"])
        assert len(nls) == int(secs["nonlinearExpressions"].attrib["numberOfNonlinearExpressions"])
        for nl in nls:
            r = int(nl.attrib["idx"])
            assert len(nl) == 1
            tgt = OBJ if r == -1 else C[r]
            assert tgt["nl"] is None
            tgt["nl"] = parse_expr(nl[0])
    return V, OBJ, C


# ---------------------------------------------------------- Q(sqrt(D)) arithmetic
class K:
    """elements are (p, q) = p + q sqrt(D), D a positive rational"""

    def __init__(self, D):
        assert D > 0
        self.D = D
        self.sqmap = {}

    @staticmethod
    def c(a):
        return (Q(a), Q(0))

    @staticmethod
    def add(x, y):
        return (x[0] + y[0], x[1] + y[1])

    @staticmethod
    def neg(x):
        return (-x[0], -x[1])

    def mul(self, x, y):
        return (x[0] * y[0] + x[1] * y[1] * self.D, x[0] * y[1] + x[1] * y[0])

    def recip(self, x):
        nrm = x[0] * x[0] - x[1] * x[1] * self.D
        assert nrm != 0
        return (x[0] / nrm, -x[1] / nrm)

    def sign(self, x):
        p, q = x
        sp = (p > 0) - (p < 0)
        sq = (q > 0) - (q < 0)
        if sq == 0:
            return sp
        if sp == 0 or sp == sq:
            return sq
        lhs, rhs = p * p, q * q * self.D        # |p| vs |q| sqrt(D)
        if lhs > rhs:
            return sp
        if lhs < rhs:
            return sq
        return 0

    def sqrt(self, y):
        z = self.sqmap.get(y)
        if z is None:
            raise ValueError("no certified square root candidate")
        assert self.mul(z, z) == y and self.sign(z) >= 0
        return z


def ev(e, X, F):
    t = e[0]
    if t == "c":
        return F.c(e[1])
    if t == "v":
        return F.mul(F.c(e[2]), X[e[1]])
    a = [ev(k, X, F) for k in e[1:]]
    if t in ("sum", "plus"):
        s = F.c(0)
        for v in a:
            s = F.add(s, v)
        return s
    if t in ("product", "times"):
        s = F.c(1)
        for v in a:
            s = F.mul(s, v)
        return s
    if t == "minus":
        return F.add(a[0], F.neg(a[1]))
    if t == "negate":
        return F.neg(a[0])
    if t == "divide":
        return F.mul(a[0], F.recip(a[1]))
    if t == "square":
        return F.mul(a[0], a[0])
    if t == "sqrt":
        return F.sqrt(a[0])
    raise NotImplementedError(t)


def ev_row(r, X, F):
    s = F.c(r["const"])
    for j, a in r["lin"].items():
        s = F.add(s, F.mul(F.c(a), X[j]))
    for i, j, a in r["quad"]:
        s = F.add(s, F.mul(F.c(a), F.mul(X[i], X[j])))
    if r["nl"] is not None:
        s = F.add(s, ev(r["nl"], X, F))
    return s


# ---------------------------------------------------------- outward decimals
def floor_dec(q, k):
    n = math.floor(q * 10 ** k)
    return fmt_int(n, k)


def ceil_dec(q, k):
    n = math.ceil(q * 10 ** k)
    return fmt_int(n, k)


def fmt_int(n, k):
    sgn = "-" if n < 0 else ""
    n = abs(n)
    return "%s%d.%s" % (sgn, n // 10 ** k, str(n % 10 ** k).zfill(k))


def sci_up(q, digits=3):
    """upper bound of a positive rational in d.dd e-xx form"""
    assert q > 0
    e = 0
    while q * Q(10) ** (-e) >= 10:
        e += 1
    while q * Q(10) ** (-e) < 1:
        e -= 1
    m = math.ceil(q * Q(10) ** (-e) * 10 ** (digits - 1))
    if m >= 10 ** digits:
        m //= 10
        m += 1
        e += 1
    s = str(m)
    return "%s.%se%d" % (s[0], s[1:], e)


def enclose(F, x, k):
    """rational interval containing p + q sqrt(D), via isqrt of num*den of D"""
    n, d = F.D.numerator, F.D.denominator
    r = math.isqrt(n * d * 10 ** (2 * k))          # r <= sqrt(n d) 10^k < r + 1
    lo_s, hi_s = Q(r, d * 10 ** k), Q(r + 1, d * 10 ** k)
    assert lo_s * lo_s <= F.D <= hi_s * hi_s
    a, b = x[0] + x[1] * lo_s, x[0] + x[1] * hi_s
    return min(a, b), max(a, b)


# ---------------------------------------------------------- main check
def run(N, out, perturb=None):
    t0 = time.time()
    V, OBJ, C = parse_osil(OSIL % N)
    gen = json.load(open("%s/points/chain%d_generator.json" % (TRACK, N)))
    box = json.load(open("%s/points/chain%d_box.json" % (TRACK, N)))
    assert gen["N"] == N
    a, b = gen["a"], gen["b"]
    tdec = gen["t"]
    assert len(tdec) == N + 1 and tdec[a] is None and tdec[b] is None
    assert sum(v is None for v in tdec) == 2
    w = [1] + [2] * (N - 1) + [1]
    fixed = {i: Q(tdec[i]) for i in range(N + 1) if i not in (a, b)}
    for i, s in enumerate(tdec):
        if s is not None:
            assert len(s.split(".")[1]) == 20 and fixed[i] > 0
    alpha = (12 * N - sum(w[i] * fixed[i] for i in fixed)) / 2
    beta = (4 * N - sum(Q(w[i]) / fixed[i] for i in fixed)) / 2
    D = alpha * alpha - 4 * alpha / beta
    assert alpha > 0 and beta > 0 and D > 0
    Dn, Dd = D.numerator, D.denominator
    D_is_rational_square = math.isqrt(Dn) ** 2 == Dn and math.isqrt(Dd) ** 2 == Dd
    R_mine = Dn * Dd
    F = K(D)
    small = (alpha / 2, Q(-1, 2))     # alpha/2 - sqrt(D)/2
    large = (alpha / 2, Q(1, 2))
    # both are roots of T^2 - alpha T + alpha/beta
    for r in (small, large):
        val = F.add(F.add(F.mul(r, r), F.mul(F.c(-alpha), r)), F.c(alpha / beta))
        assert val == (0, 0)
    assert F.sign(small) > 0 and F.sign(large) > 0
    assert F.sign(F.add(large, F.neg(small))) > 0
    ta, tb = (small, large) if gen["root_a"] == "smaller" else (large, small)
    T = [F.c(fixed[i]) if i in fixed else (ta if i == a else tb) for i in range(N + 1)]
    half = F.c(Q(1, 2))
    u = [F.mul(half, F.add(Ti, F.neg(F.recip(Ti)))) for Ti in T]
    s = [F.mul(half, F.add(Ti, F.recip(Ti))) for Ti in T]
    for si in s:
        F.sqmap[F.mul(si, si)] = si
    eta = Q(1, 2 * N)
    x = [F.c(1)]
    for i in range(N):
        x.append(F.add(x[i], F.mul(F.c(eta), F.add(u[i], u[i + 1]))))
    X = x + u
    assert len(X) == len(V)
    if perturb is not None:          # negative controls only
        perturb(X, F)
    res = dict(instance="chain%d" % N, n_vars=len(V), n_rows=len(C),
               R_digits_mine=len(str(R_mine)), R_matches_generator=(str(R_mine) == gen["R"]),
               D_is_rational_square=D_is_rational_square, a=a, b=b, root_a=gen["root_a"])
    # variable types, bounds
    nfin = 0
    for j, v in enumerate(V):
        if v["type"] in ("B", "I"):
            assert X[j][1] == 0 and X[j][0].denominator == 1
        else:
            assert v["type"] == "C", v["type"]
        if v["lb"] is not NEG_INF:
            assert v["lb"] is not POS_INF
            assert F.sign(F.add(X[j], F.c(-v["lb"]))) >= 0, ("lb", j)
            nfin += 1
        if v["ub"] is not POS_INF:
            assert v["ub"] is not NEG_INF
            assert F.sign(F.add(F.c(v["ub"]), F.neg(X[j]))) >= 0, ("ub", j)
            nfin += 1
    res["types"] = sorted(set(v["type"] for v in V))
    res["finite_var_bounds"] = nfin
    res["fixed_vars"] = [(j, V[j]["name"], str(V[j]["lb"])) for j in range(len(V))
                         if V[j]["lb"] is not NEG_INF and V[j]["lb"] == V[j]["ub"]]
    # rows
    neq = nineq = 0
    for r, c in enumerate(C):
        val = ev_row(c, X, F)
        if c["lb"] is not NEG_INF and c["ub"] is not POS_INF and c["lb"] == c["ub"]:
            assert F.add(val, F.c(-c["lb"])) == (0, 0), ("row", r)
            neq += 1
        else:
            if c["lb"] is not NEG_INF:
                assert F.sign(F.add(val, F.c(-c["lb"]))) >= 0
            if c["ub"] is not POS_INF:
                assert F.sign(F.add(F.c(c["ub"]), F.neg(val))) >= 0
            nineq += 1
    res["equality_rows_exact"] = neq
    res["inequality_rows"] = nineq
    res["sqrt_candidates_used"] = True
    # objective
    assert OBJ["sense"] == "min"
    f = ev_row(OBJ, X, F)
    lo, hi = enclose(F, f, 70)
    res["obj_lo_40"] = floor_dec(lo, 40)
    res["obj_hi_40"] = ceil_dec(hi, 40)
    assert hi - lo < Q(1, 10 ** 60)
    bj = json.load(open(BOUND % N))
    Lf = bj["bnb"]["bound"]
    assert isinstance(Lf, float) and Lf == bj["target"] and bj["bnb"]["unresolved"] == 0
    L = Q(Lf)                       # exact binary value of the double
    Ldisp = Q(repr(Lf))
    res["L_double_exact_40"] = floor_dec(L, 40)
    res["L_display"] = repr(Lf)
    res["display_minus_double"] = float(Ldisp - L)
    res["display_is_valid_bound(<= double)"] = Ldisp <= L
    res["gap_abs_up"] = sci_up(hi - L)
    res["gap_rel_up"] = sci_up((hi - L) / L)
    res["gap_abs_vs_display_up"] = sci_up(hi - min(L, Ldisp))
    res["gap_abs_vs_display_raw_up"] = sci_up(hi - Ldisp)
    # truncated safe display, 16 decimals
    res["L_truncated_16dp"] = floor_dec(L, 16)
    # box
    rad = Q(box["radius"])
    assert len(box["variables"]) == len(V)
    for j, bv in enumerate(box["variables"]):
        assert bv["index"] == j and bv["name"] == V[j]["name"]
        cj = Q(bv["centre"])
        assert F.sign(F.add(X[j], F.c(-(cj + rad)))) <= 0 and F.sign(F.add(X[j], F.c(-(cj - rad)))) >= 0
    res["box_contains_point"] = True
    res["box_radius"] = box["radius"]
    bo = [Q(z) for z in box["objective_enclosure"]]
    # the track's exact enclosure and its 40-dp decimal must contain the exact value
    bd = [Q(z) for z in box["objective_enclosure_decimal"]]
    res["track_obj_enclosure_valid"] = (F.sign(F.add(f, F.c(-bo[0]))) >= 0 and F.sign(F.add(F.c(bo[1]), F.neg(f))) >= 0)
    res["track_obj_decimal_valid"] = (F.sign(F.add(f, F.c(-bd[0]))) >= 0 and F.sign(F.add(F.c(bd[1]), F.neg(f))) >= 0)
    res["track_obj_decimal_equals_mine"] = (box["objective_enclosure_decimal"] == [res["obj_lo_40"], res["obj_hi_40"]])
    # information: start-point t at a, b; argmin/argmax; distance to source
    src = [Q(z) for z in open(PRIMAL % N).read().split()]
    us = src[N + 1:]
    approx_t = []
    for i in range(N + 1):
        uu = float(us[i])
        approx_t.append(uu + math.sqrt(1 + uu * uu))
    inner = range(1, N)
    res["argmin_t_interior"] = min(inner, key=lambda i: approx_t[i])
    res["argmax_t_interior"] = max(inner, key=lambda i: approx_t[i])
    res["t_start_a_b"] = [approx_t[a], approx_t[b]]
    ta_lo, ta_hi = enclose(F, ta, 30)
    tb_lo, tb_hi = enclose(F, tb, 30)
    res["t_a_exact"] = float(ta_lo)
    res["t_b_exact"] = float(tb_lo)
    dx = max(abs(enclose(F, x[i], 30)[0] - src[i]) for i in range(N + 1))
    du = max(abs(enclose(F, u[i], 30)[0] - us[i]) for i in range(N + 1))
    res["max_abs_diff_to_source_x_u"] = [float(dx), float(du)]
    res["seconds"] = round(time.time() - t0, 1)
    print(json.dumps(res, indent=1), flush=True)
    out.append(res)


if __name__ == "__main__":
    out = []
    for arg in sys.argv[1:]:
        run(int(arg), out)
