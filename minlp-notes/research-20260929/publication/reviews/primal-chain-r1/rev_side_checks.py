"""Reviewer's side checks (not part of the exact proof).

(a) distance of the exact point to the wave-2 double point, against the exact
    binary values of the doubles (as the track measured it);
(b) SCIP 10 (pyscipopt) floating-point check of the reviewer's own doubles of
    the exact point, one thread, feastol 1e-12 -- evidence only;
(c) mpmath iv evaluation of all rows and the objective over the box file
    (centre +- radius) -- consistency only (assumes mpmath iv rounds outward).

Usage: python3 rev_side_checks.py 50 100 200 400
"""
import io
import json
import contextlib
import sys
from fractions import Fraction as Q

import mpmath as mp
import pyscipopt

import rev_chain_exact as R

sys.set_int_max_str_digits(0)


def build_point(N):
    """rerun the exact check, capturing the field and the exact point"""
    cap = {}

    def grab(X, F):
        cap["X"], cap["F"] = list(X), F
    with contextlib.redirect_stdout(io.StringIO()):
        R.run(N, [], grab)
    return cap["X"], cap["F"]


def iv_of(q):
    return mp.iv.mpf(q.numerator) / q.denominator


def iv_ev(e, X):
    t = e[0]
    if t == "c":
        return iv_of(e[1])
    if t == "v":
        return iv_of(e[2]) * X[e[1]]
    a = [iv_ev(k, X) for k in e[1:]]
    if t in ("sum", "plus"):
        s = mp.iv.mpf(0)
        for v in a:
            s = s + v
        return s
    if t in ("product", "times"):
        s = mp.iv.mpf(1)
        for v in a:
            s = s * v
        return s
    if t == "square":
        return a[0] ** 2
    if t == "sqrt":
        return mp.iv.sqrt(a[0])
    raise NotImplementedError(t)


def iv_row(r, X):
    s = iv_of(r["const"])
    for j, c in r["lin"].items():
        s = s + iv_of(c) * X[j]
    assert not r["quad"]
    if r["nl"] is not None:
        s = s + iv_ev(r["nl"], X)
    return s


def main(N):
    X, F = build_point(N)
    V, OBJ, C = R.parse_osil(R.OSIL % N)
    out = {"N": N}
    # (a)
    src = [float(z) for z in open(R.PRIMAL % N).read().split()]
    near = [R.enclose(F, X[j], 40)[0] for j in range(len(X))]
    out["max_dist_x_to_double_point"] = float(max(abs(near[j] - Q(src[j])) for j in range(N + 1)))
    out["max_dist_u_to_double_point"] = float(max(abs(near[j] - Q(src[j])) for j in range(N + 1, 2 * N + 2)))
    # (b)
    m = pyscipopt.Model()
    m.hideOutput()
    m.readProblem(R.OSIL % N)
    m.setParam("numerics/feastol", 1e-12)
    byname = {v.name: v for v in m.getVars()}
    sol = m.createSol()
    for j, v in enumerate(V):
        m.setSolVal(sol, byname[v["name"]], float(near[j]))
    f = R.ev_row(OBJ, X, F)
    flo, fhi = R.enclose(F, f, 40)
    extra = [n for n in byname if n not in {v["name"] for v in V}]
    for n in extra:
        m.setSolVal(sol, byname[n], float(fhi))
    out["scip_extra_vars"] = extra
    out["scip_checkSol_feastol_1e-12"] = bool(m.checkSol(sol, printreason=False, completely=True, checkbounds=True,
                                                         checkintegrality=True, checklprows=True, original=True))
    # (c)
    box = json.load(open("%s/points/chain%d_box.json" % (R.TRACK, N)))
    rad = Q(box["radius"])
    mp.iv.dps = 60
    IX = []
    for bv in box["variables"]:
        c = Q(bv["centre"])
        lo, hi = iv_of(c - rad), iv_of(c + rad)
        IX.append(mp.iv.mpf([lo.a, hi.b]))
    worst = mp.mpf(0)
    ok = True
    for r in C:
        v = iv_row(r, IX)
        tgt = r["lb"]
        assert tgt == r["ub"]
        ok = ok and (v.a <= iv_of(tgt).a and iv_of(tgt).b <= v.b)
        worst = max(worst, mp.mpf(v.b - v.a))
    fo = iv_row(OBJ, IX)
    out["iv_rows_contain_rhs"] = bool(ok)
    out["iv_max_row_width"] = mp.nstr(worst, 3)
    out["iv_objective"] = [mp.nstr(fo.a, 45), mp.nstr(fo.b, 45)]
    print(json.dumps(out), flush=True)


if __name__ == "__main__":
    for a in sys.argv[1:]:
        main(int(a))
