"""Semantic comparison of two OSIL files (Part B).

Reads both files with reviews/open-instances-verification/osilx.py (every
constant kept as its decimal string) and compares:
  * variables by name: type, lower and upper bound (exact rationals);
  * objective sense;
  * constraints by name: the row function and its bounds;
  * the objective function.
Row functions are first compared structurally (linear coefficients and
quadratic terms as exact rationals, nonlinear expression trees as written).
Rows whose representations differ are compared numerically: both row
functions are evaluated with mpmath at 50 digits at several random points
(the same points for both files), and the difference of the functions must
equal the difference of the row bounds (a converter may move a constant
between the function and the bounds). This numerical test is evidence of
equality, not a proof; any difference it reports is a real difference.

Usage: python3 osil_compare.py A.osil B.osil  (prints a JSON report)
"""
import json
import os
import random
import sys
from fractions import Fraction

import mpmath
from mpmath import mp

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(R, "reviews", "open-instances-verification"))
sys.path.insert(0, os.path.join(R, "bound-audit"))
import osilx  # noqa: E402
import audit_eval  # noqa: E402  (function table with domain checks)

DPS = 50
TIGHT = mpmath.mpf("1e-40")
LOOSE = mpmath.mpf("1e-13")


def fr(s):
    """exact value of a bound string; None for +-INF"""
    return None if osilx.isinf(s) else Fraction(s)


def norm_row(row):
    lin = {j: Fraction(c) for j, c in row["lin"].items() if Fraction(c) != 0}
    quad = {}
    for i, j, c in row["quad"]:
        k = (min(i, j), max(i, j))
        quad[k] = quad.get(k, Fraction(0)) + Fraction(c)
    quad = {k: v for k, v in quad.items() if v != 0}
    return lin, quad, row["nl"]


def remap_tree(t, m):
    if t is None:
        return None
    if t[0] == "num":
        return t
    if t[0] == "var":
        return ("var", m[t[1]], t[2])
    return (t[0],) + tuple(remap_tree(c, m) for c in t[1:])


def tree_vars(t, out):
    if t is None:
        return out
    if t[0] == "var":
        out.add(t[1])
    elif t[0] != "num":
        for c in t[1:]:
            tree_vars(c, out)
    return out


def sample_points(names, lb, ub, k, seed):
    """k points; names -> mpf. Half general, half kept positive where allowed."""
    rng = random.Random(seed)
    pts = []
    for s in range(k):
        x = {}
        for n in names:
            lo, hi = lb[n], ub[n]
            if s % 2 == 0:
                v = rng.uniform(0.5, 2.0)
            else:
                v = rng.uniform(-2.0, 2.0)
            if lo is not None and hi is not None:
                v = float(lo) + rng.random() * float(hi - lo)
            elif lo is not None:
                v = float(lo) + abs(v) * max(1.0, abs(float(lo)))
            elif hi is not None:
                v = float(hi) - abs(v) * max(1.0, abs(float(hi)))
            x[n] = mpmath.mpf(v)
        pts.append(x)
    return pts


def ev(row, xs):
    try:
        v = osilx.ev_row(row, xs, audit_eval.num, audit_eval.FNS)
        v = audit_eval._real(v)
        if not mpmath.isfinite(v):
            return None
        return v
    except (audit_eval.DomainError, ZeroDivisionError, ValueError, OverflowError):
        return None


def compare(pa, pb, npts=6, seed=12345):
    A, B = osilx.read(pa), osilx.read(pb)
    rep = dict(a=pa, b=pb)
    na, nb = A["names"], B["names"]
    ia = {n: j for j, n in enumerate(na)}
    ib = {n: j for j, n in enumerate(nb)}
    rep["nvars"] = [len(na), len(nb)]
    rep["vars_only_a"] = [n for n in na if n not in ib]
    rep["vars_only_b"] = [n for n in nb if n not in ia]
    common = [n for n in na if n in ib]
    rep["var_order_same"] = na == nb
    vdiff, vdouble = [], []

    def close(x, y):
        if x is None or y is None:
            return x is y
        return abs(x - y) <= Fraction(1, 10 ** 14) * max(1, abs(x), abs(y))

    for n in common:
        ta, tb = A["vt"][ia[n]], B["vt"][ib[n]]
        la, lb_ = fr(A["lb"][ia[n]]), fr(B["lb"][ib[n]])
        ua, ub_ = fr(A["ub"][ia[n]]), fr(B["ub"][ib[n]])
        if (ta, la, ua) != (tb, lb_, ub_):
            d = dict(var=n, a=[ta, A["lb"][ia[n]], A["ub"][ia[n]]], b=[tb, B["lb"][ib[n]], B["ub"][ib[n]]])
            (vdouble if ta == tb and close(la, lb_) and close(ua, ub_) else vdiff).append(d)
    rep["var_diffs"] = vdiff
    rep["var_diffs_double_only"] = vdouble
    rep["obj_sense"] = [A["obj"]["sense"], B["obj"]["sense"]]
    ca = {c["name"]: c for c in A["cons"]}
    cb = {c["name"]: c for c in B["cons"]}
    rep["ncons"] = [len(ca), len(cb)]
    rep["cons_only_a"] = [n for n in ca if n not in cb]
    rep["cons_only_b"] = [n for n in cb if n not in ca]
    # map B variable indices to A's indices (by name) for structural compare
    b2a = {ib[n]: ia[n] for n in common}
    # sample points over the union of variables (A's bounds where available)
    allnames = na + [n for n in nb if n not in ia]
    lbs, ubs = {}, {}
    for n in allnames:
        src, j = (A, ia[n]) if n in ia else (B, ib[n])
        lbs[n], ubs[n] = fr(src["lb"][j]), fr(src["ub"][j])
    mp.dps = DPS
    pts = sample_points(allnames, lbs, ubs, npts, seed)
    xa = [[p[n] for n in na] for p in pts]
    xb = [[p[n] for n in nb] for p in pts]

    def row_like(o):
        return dict(constant=o.get("constant", "0"), lin=o["lin"], quad=o["quad"], nl=o["nl"])

    def compare_rows(label, ra, rb, la_, ua_, lb2, ub2):
        """returns None if equal structurally, else a dict"""
        lina, quada, nla = norm_row(ra)
        linb, quadb, nlb = norm_row(rb)
        try:
            linb2 = {b2a[j]: v for j, v in linb.items()}
            quadb2 = {}
            for (i, j), v in quadb.items():
                k = (min(b2a[i], b2a[j]), max(b2a[i], b2a[j]))
                quadb2[k] = quadb2.get(k, 0) + v
            nlb2 = remap_tree(nlb, b2a)
            mapped = True
        except KeyError:
            mapped = False
        ca_, cb_ = Fraction(ra.get("constant", "0")), Fraction(rb.get("constant", "0"))
        bounds_a = (None if la_ is None else la_ - ca_, None if ua_ is None else ua_ - ca_)
        bounds_b = (None if lb2 is None else lb2 - cb_, None if ub2 is None else ub2 - cb_)
        if mapped and lina == linb2 and quada == quadb2 and nla == nlb2 and bounds_a == bounds_b:
            return None
        # numerical comparison: (fa - fb) must equal the shift of the bounds
        shift = None
        if (bounds_a[0] is None) != (bounds_b[0] is None) or (bounds_a[1] is None) != (bounds_b[1] is None):
            return dict(row=label, verdict="different", why="bound sides differ",
                        a=[str(x) for x in bounds_a], b=[str(x) for x in bounds_b])
        shifts = set()
        for x, y in zip(bounds_a, bounds_b):
            if x is not None:
                shifts.add(x - y)
        if len(shifts) > 1:
            return dict(row=label, verdict="different", why="bounds differ by different shifts",
                        a=[str(x) for x in bounds_a], b=[str(x) for x in bounds_b])
        shift = shifts.pop() if shifts else Fraction(0)
        sh = mpmath.mpf(shift.numerator) / shift.denominator
        rowa = dict(ra, constant="0")
        rowb = dict(rb, constant="0")
        worst, valid = mpmath.mpf(0), 0
        for k in range(len(pts)):
            va, vb = ev(rowa, xa[k]), ev(rowb, xb[k])
            if va is None or vb is None:
                continue
            valid += 1
            d = abs((va - vb) - sh) / max(1, abs(va), abs(vb))
            worst = max(worst, d)
        if valid == 0:
            return dict(row=label, verdict="undecided", why="no sample point in the domain of both")
        verdict = ("equal (numerically, 40 digits)" if worst <= TIGHT else
                   "equal to double precision only" if worst <= LOOSE else "different")
        return dict(row=label, verdict=verdict, valid_points=valid, worst_rel=mpmath.nstr(worst, 3),
                    structural=("same" if mapped and lina == linb2 and quada == quadb2 and nla == nlb2
                                else "differs"))

    rdiff = []
    for n in ca:
        if n not in cb:
            continue
        r = compare_rows(n, ca[n], cb[n], fr(ca[n]["lb"]), fr(ca[n]["ub"]), fr(cb[n]["lb"]), fr(cb[n]["ub"]))
        if r is not None:
            rdiff.append(r)
    oa, ob = row_like(A["obj"]), row_like(B["obj"])
    r = compare_rows("objective", oa, ob, Fraction(0), Fraction(0), Fraction(0), Fraction(0))
    if r is not None:
        rdiff.append(r)
    rep["row_diffs"] = rdiff
    sets_same = (not rep["vars_only_a"] and not rep["vars_only_b"] and not vdiff and not rep["cons_only_a"]
                 and not rep["cons_only_b"] and rep["obj_sense"][0] == rep["obj_sense"][1])
    n_diff = sum(1 for d in rdiff if d["verdict"] in ("different",))
    n_und = sum(1 for d in rdiff if d["verdict"] == "undecided")
    dbl = [d for d in rdiff if d["verdict"].startswith("equal to double")]
    if not sets_same or n_diff:
        verdict = "DIFFERENT"
    elif n_und:
        verdict = f"UNDECIDED ({n_und} rows without a sample point in both domains)"
    elif dbl or vdouble:
        worst = max([float(d["worst_rel"]) for d in dbl] or [0.0])
        verdict = (f"same up to double-precision rounding of constants ({len(dbl)} rows, max relative "
                   f"difference {worst:.1e}; {len(vdouble)} bounds)")
    elif rdiff:
        verdict = "same (rows equal at 50-digit sample points; representation differs)"
    else:
        verdict = "identical (structurally, exact)"
    rep["verdict"] = verdict
    rep["summary"] = dict(vars_only_a=len(rep["vars_only_a"]), vars_only_b=len(rep["vars_only_b"]),
                          var_diffs=len(vdiff), var_diffs_double_only=len(vdouble), cons_only_a=len(rep["cons_only_a"]),
                          cons_only_b=len(rep["cons_only_b"]),
                          rows_structurally_different=len(rdiff),
                          rows_numerically_different=sum(1 for d in rdiff if d["verdict"] == "different"),
                          rows_double_only=sum(1 for d in rdiff if d["verdict"].startswith("equal to double")),
                          rows_undecided=sum(1 for d in rdiff if d["verdict"] == "undecided"))
    return rep


if __name__ == "__main__":
    rep = compare(sys.argv[1], sys.argv[2])
    print(json.dumps(dict(verdict=rep["verdict"], summary=rep["summary"], nvars=rep["nvars"],
                          ncons=rep["ncons"], obj_sense=rep["obj_sense"],
                          var_diffs=rep["var_diffs"][:10], row_diffs=rep["row_diffs"][:10],
                          vars_only_a=rep["vars_only_a"][:10], vars_only_b=rep["vars_only_b"][:10],
                          cons_only_a=rep["cons_only_a"][:10], cons_only_b=rep["cons_only_b"][:10]),
                     indent=1, default=str))
