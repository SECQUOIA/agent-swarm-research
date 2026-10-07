"""Rigorous lower bound of the tangent-plane function
    D(y) = G(y) - lambda.y   on   {y_i >= ymin, y1 + y2 + y3 = 1}
for a UNIQUAC-type phase, by a 2-D interval branch and bound in mpmath iv
(own code; different arithmetic and bounding rules from the authors').

Coordinates (y1, y2); y3 = 1 - y1 - y2 is enclosed per box and clipped to
[ymin, 1].  Lower bounds per box (the largest is used):
  (N) natural interval extension;
  (M) mean-value form D(c) + [grad D](B).(B - c);
  (Q) second-order form with the 2x2 interval Hessian H(B):
      D(y) >= D(c) + g.d + 1/2 (a d1^2 + e d2^2) + min(b_lo d1 d2, b_hi d1 d2),
      a = H11_lo, e = H22_lo, b in [H12]; when both 2x2 matrices [[a,b],[b,e]]
      (b = b_lo, b_hi) are positive definite the unconstrained minimum
      D(c) - 1/2 g^T Q^{-1} g is used (valid on all of R^2, so on the box);
      otherwise the box-restricted separable bound.
  c is a feasible point of the box (the centre, pulled towards the box corner
  (y1lo, y2lo) if the centre violates y3 >= ymin).  D(c) and grad D(c) are
  enclosed at 40 digits; box quantities at 53 bits.
A box is fathomed when its bound is >= -tau.  The certified minimum is the
smallest fathomed bound.  Boxes are split at the midpoint, or at the geometric
mean when lo < hi/64 (dilute coordinates).
"""
import json
import math
import sys
import time
from multiprocessing import Pool

import mpmath
import sympy as sp
from mpmath import iv

import gibbs_sym
import ivgen

CFG = {}


def setup(name, ptype, lam_strs, ymin_str, tau):
    A = gibbs_sym.analyse(name, verbose=False)
    y = A["y"]
    G = A["G"][ptype]
    grad = [sp.diff(G, v) for v in y]
    hess = [sp.diff(G, y[i], y[j]) for i, j in ((0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2))]
    CFG.update(name=name, ptype=ptype,
               fF=ivgen.compile_exprs(y, [G], "F"), fG=ivgen.compile_exprs(y, grad, "GR"),
               fH=ivgen.compile_exprs(y, hess, "HS"), lam=lam_strs, ymin=ymin_str, tau=tau)


_W = {}


def _worker_init(name, ptype, lam_strs, ymin_str, tau):
    setup(name, ptype, lam_strs, ymin_str, tau)
    iv.dps = 40
    _W["F40"], _W["G40"] = CFG["fF"](), CFG["fG"]()
    L = [iv.mpf(s) for s in lam_strs]
    _W["L40"] = L
    iv.prec = 53
    _W["F53"], _W["G53"], _W["H53"] = CFG["fF"](), CFG["fG"](), CFG["fH"]()
    _W["L53"] = [iv.mpf(s) for s in lam_strs]
    _W["ymin"] = mpmath.mpf(ymin_str)
    _W["tau"] = mpmath.mpf(tau)


def lower(y1lo, y1hi, y2lo, y2hi):
    """rigorous lower bound (mpf) of D over the box intersected with the simplex."""
    ymin = _W["ymin"]
    iv.prec = 53
    L = _W["L53"]
    Y1 = iv.mpf([y1lo, y1hi]); Y2 = iv.mpf([y2lo, y2hi])
    Y3r = 1 - Y1 - Y2
    y3hi = min(mpmath.mpf(Y3r.b), mpmath.mpf(1))
    y3lo = min(max(mpmath.mpf(Y3r.a), ymin), y3hi)
    Y3 = iv.mpf([y3lo, y3hi])
    lin = L[2] + (L[0] - L[2]) * Y1 + (L[1] - L[2]) * Y2
    (Fb,) = _W["F53"](Y1, Y2, Y3)
    bN = mpmath.mpf((Fb - lin).a)
    best = bN
    if best >= -_W["tau"]:
        return best, "N"
    # feasible centre
    c1 = (y1lo + y1hi) / 2; c2 = (y2lo + y2hi) / 2
    room = 1 - ymin - y1lo - y2lo
    if c1 + c2 > 1 - ymin:
        al = room / ((c1 - y1lo) + (c2 - y2lo)) * mpmath.mpf("0.999999")
        c1 = y1lo + al * (c1 - y1lo); c2 = y2lo + al * (c2 - y2lo)
    # centre values at 40 digits
    iv.dps = 40
    L4 = _W["L40"]
    C1 = iv.mpf(c1); C2 = iv.mpf(c2); C3 = 1 - C1 - C2
    (Fc,) = _W["F40"](C1, C2, C3)
    Dc = Fc - (L4[2] + (L4[0] - L4[2]) * C1 + (L4[1] - L4[2]) * C2)
    g1c, g2c, g3c = _W["G40"](C1, C2, C3)
    ga = g1c - g3c - (L4[0] - L4[2]); gb = g2c - g3c - (L4[1] - L4[2])
    iv.prec = 53
    Dc = iv.mpf([Dc.a, Dc.b]); ga = iv.mpf([ga.a, ga.b]); gb = iv.mpf([gb.a, gb.b])
    # the Taylor forms need the hull of the feasible part and c: include c3
    C3 = iv.mpf([C3.a, C3.b])
    Y3 = iv.mpf([min(mpmath.mpf(Y3.a), mpmath.mpf(C3.a)), max(mpmath.mpf(Y3.b), mpmath.mpf(C3.b))])
    d1 = Y1 - iv.mpf(c1); d2 = Y2 - iv.mpf(c2)
    # (M) mean value form
    G1, G2, G3 = _W["G53"](Y1, Y2, Y3)
    gB1 = G1 - G3 - (L[0] - L[2]); gB2 = G2 - G3 - (L[1] - L[2])
    bM = mpmath.mpf((Dc + gB1 * d1 + gB2 * d2).a)
    if bM > best:
        best, how = bM, "M"
    if best >= -_W["tau"]:
        return best, "M"
    # (Q) second-order form
    h11, h12, h13, h22, h23, h33 = _W["H53"](Y1, Y2, Y3)
    A11 = h11 - 2 * h13 + h33
    A22 = h22 - 2 * h23 + h33
    A12 = h12 - h13 - h23 + h33
    a = mpmath.mpf(A11.a); e = mpmath.mpf(A22.a)
    blo = mpmath.mpf(A12.a); bhi = mpmath.mpf(A12.b)
    bQ = None
    if a > 0 and e > 0:
        worst = None
        ok = True
        for bb in (blo, bhi):
            det = iv.mpf(a) * iv.mpf(e) - iv.mpf(bb) * iv.mpf(bb)
            if not det.a > 0:
                ok = False
                break
            q = (iv.mpf(e) * ga * ga - 2 * iv.mpf(bb) * ga * gb + iv.mpf(a) * gb * gb) / det
            worst = q.b if worst is None else max(worst, q.b)
        if ok:
            bQ = mpmath.mpf((Dc - iv.mpf(worst) / 2).a)
    if bQ is None:
        quad = (iv.mpf(a) * d1 ** 2 + iv.mpf(e) * d2 ** 2) / 2 + A12 * d1 * d2
        bQ = mpmath.mpf((Dc + ga * d1 + gb * d2 + quad).a)
    if bQ > best:
        best = bQ
    return best, ("Q" if best == bQ else ("M" if best == bM else "N"))


def split(box):
    y1lo, y1hi, y2lo, y2hi = box
    w1 = y1hi - y1lo; w2 = y2hi - y2lo
    # measure width relative to position for dilute coordinates
    s1 = w1 if y1lo * 64 >= y1hi else w1 * 4
    s2 = w2 if y2lo * 64 >= y2hi else w2 * 4
    if s1 >= s2:
        m = mpmath.sqrt(y1lo * y1hi) if y1lo * 64 < y1hi else (y1lo + y1hi) / 2
        return [(y1lo, m, y2lo, y2hi), (m, y1hi, y2lo, y2hi)]
    m = mpmath.sqrt(y2lo * y2hi) if y2lo * 64 < y2hi else (y2lo + y2hi) / 2
    return [(y1lo, y1hi, y2lo, m), (y1lo, y1hi, m, y2hi)]


def solve_box(box, budget=2_000_000, minw=mpmath.mpf("1e-14")):
    iv.prec = 53
    mpmath.mp.prec = 53
    ymin = _W["ymin"]
    stack = [box]
    nbox = 0
    minlb = mpmath.inf
    argmin = None
    stats = {"N": 0, "M": 0, "Q": 0, "out": 0}
    while stack:
        b = stack.pop()
        nbox += 1
        if nbox > budget:
            return dict(ok=False, reason="budget", nbox=nbox, box=list(map(str, b)))
        with mpmath.workdps(60):
            outside = mpmath.mpf(b[0]) + b[2] > 1 - ymin
        if outside:  # box has no point with y3 >= ymin (exact test)
            stats["out"] += 1
            continue
        lb, how = lower(*b)
        if lb >= -_W["tau"]:
            stats[how] += 1
            if lb < minlb:
                minlb, argmin = lb, b
            continue
        if max(b[1] - b[0], b[3] - b[2]) < minw:
            return dict(ok=False, reason="minwidth", nbox=nbox, box=list(map(str, b)), lb=str(lb))
        stack.extend(split(b))
    return dict(ok=True, nbox=nbox, minlb=str(minlb), argmin=list(map(str, argmin)) if argmin else None,
                stats=stats)


def _run(box):
    t = time.time()
    r = solve_box(tuple(mpmath.mpf(v) for v in box))
    r["sec"] = round(time.time() - t, 1)
    r["root"] = [str(v) for v in box]
    return r


def main(name, ptype, lam_strs, ymin_str, tau, procs=6, ngrid=8):
    ymin = mpmath.mpf(ymin_str)
    # initial grid of root boxes over [ymin, 1-2 ymin]^2 (geometric near 0)
    cuts = sorted(set([ymin, mpmath.mpf("1e-6"), mpmath.mpf("1e-4"), mpmath.mpf("1e-2")] +
                      [mpmath.mpf(k) / ngrid for k in range(1, ngrid)] + [1 - 2 * ymin]))
    roots = []
    for i in range(len(cuts) - 1):
        for j in range(len(cuts) - 1):
            if cuts[i] + cuts[j] <= 1 - ymin:
                roots.append((str(cuts[i]), str(cuts[i + 1]), str(cuts[j]), str(cuts[j + 1])))
    t = time.time()
    with Pool(procs, initializer=_worker_init, initargs=(name, ptype, lam_strs, ymin_str, tau)) as pool:
        res = pool.map(_run, roots, chunksize=1)
    ok = all(r["ok"] for r in res)
    out = dict(name=name, ptype=ptype, lam=lam_strs, ymin=ymin_str, tau=tau, ok=ok,
               nbox=sum(r["nbox"] for r in res), sec=round(time.time() - t, 1), nroots=len(roots))
    if ok:
        k = min(range(len(res)), key=lambda i: mpmath.mpf(res[i]["minlb"]))
        out["certified_min"] = res[k]["minlb"]
        out["argmin_box"] = res[k]["argmin"]
        st = {}
        for r in res:
            for kk, v in r["stats"].items():
                st[kk] = st.get(kk, 0) + v
        out["stats"] = st
    else:
        out["failures"] = [r for r in res if not r["ok"]][:5]
    return out


if __name__ == "__main__":
    name, ptype = sys.argv[1], int(sys.argv[2])
    tau = sys.argv[3]
    kk = json.load(open("logs/%s_kkt.json" % name))
    mpmath.mp.dps = 50
    lam = [mpmath.nstr(mpmath.mpf(v), 20) for v in kk["lam"]]
    b = gibbs_sym.analyse(name, verbose=False)["b"]
    tmax = sum(mpmath.mpf(v) for v in b)
    mpmath.mp.dps = 50
    ymin = mpmath.nstr(mpmath.mpf("0.99e-7") / tmax, 6)  # a little below the true 1e-7/tmax
    assert mpmath.mpf(ymin) * (1 + mpmath.mpf(2) ** -50) < mpmath.mpf("1e-7") / tmax
    procs = int(sys.argv[4]) if len(sys.argv) > 4 else 6
    out = main(name, ptype, lam, ymin, tau, procs=procs)
    print(json.dumps(out, indent=1))
    json.dump(out, open("logs/%s_bb_type%d_tau%s.json" % (name, ptype, tau), "w"), indent=1)
