"""Independent check of the primal-lnts points (review round 1).

Usage: python3 verify_lnts_points.py 50 100 200 400

Written by the reviewer; does not import or copy the track's code. Inputs taken
from the track: only the point files (fixed controls, box centre and radius,
stored per-variable enclosures, stored objective enclosure).

Method
  1. Own OSiL reader (OSiL defaults: var lb=0, ub=INF, type C; con lb=-INF,
     ub=INF). Unknown attributes or node types raise an error.
  2. Parameters: the variables named in 'fixed_controls' (exact decimals) and
     in 'unknowns_box' (box). Every other variable is found by a generic
     elimination over the parsed rows: a row with exactly one undetermined
     variable, appearing only linearly with nonzero coefficient, defines that
     variable exactly as (b - rest)/c. Fixed variables (lb == ub) start as
     known. Rows whose variables are all known when reached are the residual
     equations F(z) = 0. No index layout is assumed.
  3. Forward-mode derivatives (own class) in mpmath iv at DPS digits; Krawczyk
     test on the stored box (exact decimal centre +- radius, enclosed
     outward). Zero enclosure Z = K(X) n X. A second step uses a point y2 in Z
     (so the mean-value argument is valid) to narrow Z.
  4. Every variable enclosure is checked against the OSIL bounds (exact
     decimal value and the double value of the bound string), against the
     stored 60-digit enclosures, and every row is evaluated over the full box
     (consistency: 0 must lie in the enclosure).
  5. Objective enclosed from the parsed objective over the box; gaps to the
     two dual values are computed exactly with Fractions.
"""
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from fractions import Fraction as Fr

from mpmath import iv, mp
from mpmath.libmp import to_rational, finf, fninf, fnan

DPS = 120
mp.dps = iv.dps = DPS
import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../../.."))
PT = _REPO + "/research-20260929/publication/primal/lnts/points/lnts{}_point.json"
DUALS = {  # summary display, verification report (margin 1e-12)
    50: ("0.5546687649381", "0.5546687649381242"),
    100: ("0.5545954011663", "0.5545954011663566"),
    200: ("0.5545770161025", "0.5545770161025291"),
    400: ("0.5545724137001", "0.5545724137001325"),
}


# ------------------------------------------------------------------ reader
def strip(t):
    return t.split("}", 1)[1] if "}" in t else t


def is_inf(s):
    return s in ("INF", "+INF", "-INF", "Infinity", "-Infinity", "inf", "-inf")


def expand(node, kind):
    out = []
    for el in node:
        assert strip(el.tag) == "el"
        assert set(el.attrib) <= {"mult", "incr"}, el.attrib
        m = int(el.get("mult", "1"))
        if kind == "int":
            b, d = int(el.text), int(el.get("incr", "0"))
            out.extend(b + k * d for k in range(m))
        else:
            b, d = Fr(el.text.strip()), Fr(el.get("incr", "0"))
            out.extend(b + k * d for k in range(m))
    return out


def tree(e):
    t = strip(e.tag)
    if t == "number":
        assert set(e.attrib) <= {"value", "type"} and e.get("type", "real") == "real", e.attrib
        assert len(e) == 0
        return ("c", Fr(e.get("value")))
    if t == "variable":
        assert set(e.attrib) <= {"idx", "coef"} and len(e) == 0, e.attrib
        return ("v", int(e.get("idx")), Fr(e.get("coef", "1")))
    assert not e.attrib, (t, e.attrib)
    kids = [tree(k) for k in e]
    if t in ("sum", "product"):
        return (t,) + tuple(kids)
    if t in ("cos", "sin"):
        assert len(kids) == 1
        return (t, kids[0])
    raise ValueError("node " + t)


def nl_vars(t, acc):
    if t[0] == "v":
        acc.add(t[1])
    elif t[0] != "c":
        for k in t[1:]:
            nl_vars(k, acc)
    return acc


def read_osil(path):
    root = ET.parse(path).getroot()
    data = [c for c in root if strip(c.tag) == "instanceData"][0]
    sec = {strip(c.tag): c for c in data}
    assert set(sec) <= {"variables", "objectives", "constraints", "linearConstraintCoefficients",
                        "quadraticCoefficients", "nonlinearExpressions"}, set(sec)
    V = []
    for v in sec["variables"]:
        assert set(v.attrib) <= {"name", "lb", "ub", "type"}, v.attrib
        assert v.get("type", "C") == "C"
        V.append(dict(name=v.get("name"), lb=v.get("lb", "0"), ub=v.get("ub", "INF")))
    assert int(sec["variables"].get("numberOfVariables")) == len(V)
    objs = list(sec["objectives"])
    assert len(objs) == 1
    o = objs[0]
    assert set(o.attrib) <= {"maxOrMin", "name", "numberOfObjCoef"}, o.attrib
    obj = dict(sense=o.get("maxOrMin", "min"), lin={}, quad=[], nl=None)
    for cf in o:
        assert strip(cf.tag) == "coef" and set(cf.attrib) == {"idx"}
        obj["lin"][int(cf.get("idx"))] = Fr(cf.text.strip())
    C = []
    for c in sec["constraints"]:
        assert set(c.attrib) <= {"name", "lb", "ub"}, c.attrib
        C.append(dict(name=c.get("name"), lb=c.get("lb", "-INF"), ub=c.get("ub", "INF"), lin={}, quad=[], nl=None))
    assert int(sec["constraints"].get("numberOfConstraints")) == len(C)
    L = sec.get("linearConstraintCoefficients")
    if L is not None:
        parts = {strip(k.tag): k for k in L}
        assert set(parts) == {"start", "colIdx", "value"}, set(parts)
        st, col, val = expand(parts["start"], "int"), expand(parts["colIdx"], "int"), expand(parts["value"], "fr")
        assert len(st) == len(C) + 1 and st[0] == 0 and st[-1] == len(col) == len(val)
        assert int(L.get("numberOfValues")) == len(val)
        for r in range(len(C)):
            for k in range(st[r], st[r + 1]):
                assert col[k] not in C[r]["lin"]
                C[r]["lin"][col[k]] = val[k]
    Q = sec.get("quadraticCoefficients")
    if Q is not None:
        n = 0
        for q in Q:
            assert set(q.attrib) <= {"idx", "idxOne", "idxTwo", "coef"}
            r = int(q.get("idx"))
            (obj if r == -1 else C[r])["quad"].append((int(q.get("idxOne")), int(q.get("idxTwo")), Fr(q.get("coef", "1"))))
            n += 1
        assert n == int(Q.get("numberOfQuadraticTerms"))
    NL = sec.get("nonlinearExpressions")
    if NL is not None:
        n = 0
        for e in NL:
            assert set(e.attrib) == {"idx"} and len(e) == 1
            r = int(e.get("idx"))
            tgt = obj if r == -1 else C[r]
            assert tgt["nl"] is None
            tgt["nl"] = tree(e[0])
            n += 1
        assert n == int(NL.get("numberOfNonlinearExpressions"))
    return V, obj, C


# ------------------------------------------------- interval forward mode
def I(q):
    q = Fr(q)
    return iv.mpf(q.numerator) / iv.mpf(q.denominator)


ZERO3 = None


class AD:
    __slots__ = ("v", "g")

    def __init__(self, v, g):
        self.v, self.g = v, g

    @staticmethod
    def const(q):
        return AD(q if isinstance(q, iv.mpf) else I(q), ZERO3)

    def __add__(s, o):
        return AD(s.v + o.v, tuple(a + b for a, b in zip(s.g, o.g)))

    def __mul__(s, o):
        return AD(s.v * o.v, tuple(s.v * b + o.v * a for a, b in zip(s.g, o.g)))

    def cmul(s, c):  # c an interval constant
        return AD(s.v * c, tuple(a * c for a in s.g))

    def cos(s):
        d = -iv.sin(s.v)
        return AD(iv.cos(s.v), tuple(d * a for a in s.g))

    def sin(s):
        d = iv.cos(s.v)
        return AD(iv.sin(s.v), tuple(d * a for a in s.g))


def ev_tree(t, X):
    k = t[0]
    if k == "c":
        return AD.const(t[1])
    if k == "v":
        return X[t[1]].cmul(I(t[2]))
    if k == "sum":
        s = ev_tree(t[1], X)
        for u in t[2:]:
            s = s + ev_tree(u, X)
        return s
    if k == "product":
        p = ev_tree(t[1], X)
        for u in t[2:]:
            p = p * ev_tree(u, X)
        return p
    if k == "cos":
        return ev_tree(t[1], X).cos()
    if k == "sin":
        return ev_tree(t[1], X).sin()
    raise ValueError(k)


def ev_row(row, X, skip=None):
    """lin + quad + nl part of a row, leaving out the linear term of `skip`."""
    s = AD.const(0)
    for j, c in row["lin"].items():
        if j != skip:
            s = s + X[j].cmul(I(c))
    for i, j, c in row["quad"]:
        s = s + (X[i] * X[j]).cmul(I(c))
    if row["nl"] is not None:
        s = s + ev_tree(row["nl"], X)
    return s


def ends(x):
    r = []
    for t in x._mpi_:
        assert t not in (finf, fninf, fnan)
        p, q = to_rational(t)
        r.append(Fr(p, q))
    return tuple(r)


def mk(lo_raw, hi_raw):
    """Interval from two raw mpf end points (exact at the working precision)."""
    return iv.mpf([mp.make_mpf(lo_raw), mp.make_mpf(hi_raw)])


def meet(A, B):
    """A intersect B, assuming they overlap."""
    lo = A._mpi_[0] if ends(A)[0] >= ends(B)[0] else B._mpi_[0]
    hi = A._mpi_[1] if ends(A)[1] <= ends(B)[1] else B._mpi_[1]
    r = mk(lo, hi)
    assert ends(r) == (max(ends(A)[0], ends(B)[0]), min(ends(A)[1], ends(B)[1]))
    return r


# ------------------------------------------------------------- elimination
def plan(V, C, params):
    """Generic elimination order. Returns list of (row, var) solves and residual rows."""
    known = set(params) | {j for j, v in enumerate(V) if v["lb"] == v["ub"] and not is_inf(v["lb"])}
    rowvars = []
    for c in C:
        assert c["lb"] == c["ub"] and not is_inf(c["lb"]), "only equality rows expected"
        s = set(c["lin"]) | {i for i, _, _ in c["quad"]} | {j for _, j, _ in c["quad"]}
        if c["nl"] is not None:
            nl_vars(c["nl"], s)
        rowvars.append(s)
    done = [False] * len(C)
    steps, resid = [], []
    progress = True
    while progress:
        progress = False
        for r, c in enumerate(C):
            if done[r]:
                continue
            unk = rowvars[r] - known
            if len(unk) == 0:
                resid.append(r)
                done[r] = progress = True
            elif len(unk) == 1:
                u = next(iter(unk))
                inquad = any(u in (i, j) for i, j, _ in c["quad"])
                innl = c["nl"] is not None and u in nl_vars(c["nl"], set())
                if c["lin"].get(u, 0) != 0 and not inquad and not innl:
                    steps.append((r, u))
                    known.add(u)
                    done[r] = progress = True
    assert all(done), "some rows not processed"
    assert known == set(range(len(V))), "some variables not determined"
    return steps, resid


def evaluate(V, C, steps, resid, parvals):
    """parvals: dict var -> AD. Returns full variable list (AD) and residuals F (AD)."""
    X = [None] * len(V)
    for j, a in parvals.items():
        X[j] = a
    for j, v in enumerate(V):
        if v["lb"] == v["ub"] and not is_inf(v["lb"]):
            assert X[j] is None
            X[j] = AD.const(Fr(v["lb"]))
    for r, u in steps:
        c = C[r]
        rest = ev_row(c, X, skip=u)
        # c_u * x_u + rest = b  =>  x_u = (b - rest) / c_u  (exact real definition)
        cu = I(c["lin"][u])
        X[u] = AD(( I(Fr(c["lb"])) - rest.v) / cu, tuple(-a / cu for a in rest.g))
    F = []
    for r in resid:
        val = ev_row(C[r], X)
        F.append(AD(val.v - I(Fr(C[r]["lb"])), val.g))
    return X, F


# --------------------------------------------------------------- Krawczyk
def krawczyk(V, C, steps, resid, fixedpars, zvars, Y, Xb):
    """Y: list of intervals (enclosing a point y in Xb); Xb: box. Returns K."""
    global ZERO3
    n = len(zvars)
    ZERO3 = tuple(iv.mpf(0) for _ in range(n))
    unit = lambda k: tuple(iv.mpf(1) if m == k else iv.mpf(0) for m in range(n))
    base = {j: AD(q, ZERO3) for j, q in fixedpars.items()}
    pv = dict(base)
    pv.update({zvars[k]: AD(Y[k], ZERO3) for k in range(n)})
    _, Fy = evaluate(V, C, steps, resid, pv)
    pv = dict(base)
    pv.update({zvars[k]: AD(Xb[k], unit(k)) for k in range(n)})
    _, FX = evaluate(V, C, steps, resid, pv)
    J = [[FX[i].g[j] for j in range(n)] for i in range(n)]
    M = mp.matrix(n, n)
    for i in range(n):
        for j in range(n):
            a, b = ends(J[i][j])
            M[i, j] = mp.mpf((a + b).numerator) / (2 * (a + b).denominator)
    Cm = M ** -1
    Ci = [[iv.mpf(Cm[i, j]) for j in range(n)] for i in range(n)]
    for i in range(n):  # the conversion must be exact (point intervals)
        for j in range(n):
            a, b = ends(Ci[i][j])
            assert a == b
    K = []
    for i in range(n):
        s = Y[i]
        for k in range(n):
            s = s - Ci[i][k] * Fy[k].v
        for j in range(n):
            m = iv.mpf(1 if i == j else 0)
            for k in range(n):
                m = m - Ci[i][k] * J[k][j]
            s = s + m * (Xb[j] - Y[j])
        K.append(s)
    return K, Fy, J


def run(N):
    P = json.load(open(PT.format(N)))
    path = P["osil"]
    assert path == f"{_PUBLIC_HOME}/.cache/minlplib/minlplib/osil/lnts{N}.osil"
    sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
    assert sha == P["osil_sha256"]
    V, obj, C = read_osil(path)
    names = [v["name"] for v in V]
    idx = {nm: j for j, nm in enumerate(names)}
    assert len(idx) == len(names)
    fixedpars_q = {idx[nm]: Fr(s) for nm, s in P["fixed_controls"].items()}
    zvars = [idx[nm] for nm in P["unknowns_box"]]
    cen = [Fr(P["unknowns_box"][names[j]]["centre"]) for j in zvars]
    rad = [Fr(P["unknowns_box"][names[j]]["radius"]) for j in zvars]
    params = set(fixedpars_q) | set(zvars)
    steps, resid = plan(V, C, params)
    assert len(resid) == len(zvars), (len(resid), len(zvars))
    fixedpars = {j: I(q) for j, q in fixedpars_q.items()}
    # outward enclosure of the exact box, and of the exact centre
    Xb = [mk(I(c - r)._mpi_[0], I(c + r)._mpi_[1]) for c, r in zip(cen, rad)]
    Y = [I(c) for c in cen]
    K, Fy, J = krawczyk(V, C, steps, resid, fixedpars, zvars, Y, Xb)
    ok = all(ends(K[k])[0] > ends(Xb[k])[0] and ends(K[k])[1] < ends(Xb[k])[1] for k in range(3))
    assert ok, "Krawczyk test failed on the stored box"
    Z1 = [meet(K[k], Xb[k]) for k in range(3)]
    # is the stored centre inside Z1? (the track's second step assumes the mean value
    # theorem on Z with y = centre)
    centre_in_Z1 = all(ends(Z1[k])[0] <= cen[k] <= ends(Z1[k])[1] for k in range(3))
    # valid second step: y2 = midpoint of Z1 (a point of Z1)
    y2 = []
    for k in range(3):
        a, b = ends(Z1[k])
        m = (a + b) / 2
        y2.append(iv.mpf(mp.mpf(m.numerator) / m.denominator))
    for k in range(3):
        a, b = ends(y2[k])
        assert a == b and ends(Z1[k])[0] <= a <= ends(Z1[k])[1]
    K2, _, _ = krawczyk(V, C, steps, resid, fixedpars, zvars, y2, Z1)
    Z2 = [meet(K2[k], Z1[k]) for k in range(3)]
    # zero lies strictly inside the exact decimal box
    for k in range(3):
        a, b = ends(Z1[k])
        assert cen[k] - rad[k] < a and b < cen[k] + rad[k]
    # full-variable enclosure over Z (use Z1 = the one-step result, and Z2)
    out = dict(instance=f"lnts{N}", nvars=len(V), nrows=len(C), n_solves=len(steps),
               residual_rows=[C[r]["name"] for r in resid], unknowns=[names[j] for j in zvars],
               krawczyk_ok=ok, centre_in_Z1=centre_in_Z1,
               max_abs_F_centre=float(max(max(abs(e) for e in ends(f.v)) for f in Fy)),
               Z1_widths=[float(ends(z)[1] - ends(z)[0]) for z in Z1],
               Z2_widths=[float(ends(z)[1] - ends(z)[0]) for z in Z2])
    for tag, Z in (("Z1", Z1), ("Z2", Z2)):
        global ZERO3
        ZERO3 = (iv.mpf(0),) * 3
        pv = {j: AD(q, ZERO3) for j, q in fixedpars.items()}
        pv.update({zvars[k]: AD(Z[k], ZERO3) for k in range(3)})
        X, F = evaluate(V, C, steps, resid, pv)
        for f in F:
            a, b = ends(f.v)
            assert a <= 0 <= b
        # bounds: exact decimal and double value of the bound string
        minslack = None
        for j, v in enumerate(V):
            a, b = ends(X[j].v)
            for s, side in ((v["lb"], "lb"), (v["ub"], "ub")):
                if is_inf(s):
                    continue
                for bq in (Fr(s), Fr(float(s))):
                    sl = (a - bq) if side == "lb" else (bq - b)
                    assert sl >= 0, (names[j], side, s)
                    if v["lb"] != v["ub"]:
                        minslack = sl if minslack is None else min(minslack, sl)
        # every row over the full box (0 must be inside; consistency only)
        maxw = 0
        for c in C:
            R = ev_row(c, X).v
            a, b = ends(R)
            assert a <= Fr(c["lb"]) and Fr(c["ub"]) <= b
            maxw = max(maxw, b - a)
        # stored enclosures must contain mine
        enc = P["enclosures"]
        assert [e[0] for e in enc] == names
        worst_in = None
        for j in range(len(V)):
            a, b = ends(X[j].v)
            lo, hi = Fr(enc[j][1]), Fr(enc[j][2])
            assert lo <= a and b <= hi, (names[j], tag)
            if V[j]["lb"] == V[j]["ub"]:
                continue  # fixed variables: stored lo = hi = exact value
            m = min(a - lo, hi - b)
            worst_in = m if worst_in is None else min(worst_in, m)
        # objective
        assert obj["sense"] == "min"
        O = ev_row(obj, X).v
        olo, ohi = ends(O)
        slo, shi = Fr(P["objective_enclosure"][0]), Fr(P["objective_enclosure"][1])
        assert slo <= olo and ohi <= shi, "stored objective enclosure does not contain mine"
        g = {}
        for name, d in zip(("summary", "verifier"), DUALS[N]):
            gap = ohi - Fr(d)
            g[name] = dict(abs=float(gap), abs_15sig=mp.nstr(mp.mpf(gap.numerator) / gap.denominator, 15),
                           rel=float(gap / Fr(d)))
        out[tag] = dict(min_bound_slack_nonfixed=float(minslack), max_row_width=float(maxw),
                        min_margin_inside_stored_enclosures=float(worst_in),
                        obj_lo=mp.nstr(mp.mpf(olo.numerator) / olo.denominator, 30),
                        obj_hi=mp.nstr(mp.mpf(ohi.numerator) / ohi.denominator, 30),
                        obj_width=float(ohi - olo), gaps=g)
    print(json.dumps(out), flush=True)
    return out


if __name__ == "__main__":
    res = [run(int(a)) for a in sys.argv[1:]]
    json.dump(res, open("verify_lnts_points_" + "_".join(sys.argv[1:]) + ".json", "w"), indent=1)
