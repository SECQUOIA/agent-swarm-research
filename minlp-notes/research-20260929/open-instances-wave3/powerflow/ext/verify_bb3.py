"""Re-check a pf_bb3 run from its JSON (no SDP solves):
  1. the leaf boxes cover the root box: exact volumes sum to the root volume and the
     interiors are pairwise disjoint (a finite union of closed boxes of full measure is the
     whole box);
  2. every leaf bound is recomputed with pf_cert.certify from the stored multipliers
     (exact rationals + interval Cholesky) and must be >= the stored bound;
     leaves without stored multipliers (inherited parent bounds) are reported;
  3. at the MINLPLib point p1 (50 digits) the leaf identity W_NN = F(Pg, Qg, W_LL) holds and,
     for the leaves containing p1, every cut row holds at p1.
    python3 verify_bb3.py <name>
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../../..'))
import json
import os
import sys
from fractions import Fraction as Fr

import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave2/small")
import ev  # noqa: E402
import pf_cert as pc  # noqa: E402
import pf_model as pm  # noqa: E402
import leafcut as lc  # noqa: E402
from pf_bb3 import node_model  # noqa: E402


def main(name, tag="bb3"):
    D = json.load(open(os.path.join(HERE, "logs", f"{name}.{tag}.json")))
    M = pm.decode(name)
    info = lc.leaf_info(M)
    root = ((info["plo"], info["phi"]), (info["qlo"], info["qhi"]), info["WLL"])
    leaves = [(tuple((Fr(a), Fr(c)) for a, c in L["box"]), Fr(L["bound"]), L["raw"]) for L in D["leaves"]]
    vol = lambda bx: (bx[0][1] - bx[0][0]) * (bx[1][1] - bx[1][0]) * (bx[2][1] - bx[2][0])
    assert all(all(root[d][0] <= bx[d][0] < bx[d][1] <= root[d][1] for d in range(3)) for bx, _, _ in leaves)
    tot = sum(vol(bx) for bx, _, _ in leaves)
    disj = all(any(a[d][1] <= b[d][0] or b[d][1] <= a[d][0] for d in range(3))
               for i, (a, _, _) in enumerate(leaves) for (b, _, _) in leaves[i + 1:])
    print(f"{name}: {len(leaves)} leaves; volume sum == root volume: {tot == vol(root)}; interiors disjoint: {disj}")
    LB = None
    noraw = 0
    for bx, bd, raw in leaves:
        if raw is None:
            noraw += 1
            continue
        MM, extra = node_model(M, info, bx)
        MM = dict(MM, rows=list(MM["rows"]) + extra)
        res = pc.certify(MM, raw, log=lambda s: None)
        assert res is not None
        assert res[0] >= bd or abs(res[0] - bd) < Fr(1, 10**9), (float(res[0]), float(bd))
        LB = res[0] if LB is None else min(LB, res[0])
    print(f"  recomputed min leaf bound {float(LB)!r} (stored LB {D['LB']!r}); leaves with inherited bounds: {noraw}")
    # p1 checks
    mp.mp.dps = 50
    I = M["I"]
    vals = ev.read_sol(os.path.join(HERE, "..", "..", "sol", f"{name}.p1.sol"))
    z = {v: mp.mpf(vals.get(v, "0")) for v in I["names"]}
    names = I["names"]
    N, L = info["N"], info["L"]
    if M["polar"]:
        V = {k: (z[names[vv]] * mp.cos(z[names[tt]]), z[names[vv]] * mp.sin(z[names[tt]])) for k, (vv, tt) in enumerate(M["busmap"])}
    else:
        # bus pairs as in pf_model: voltage rows (e^2 + f^2, no linear part) over the variables
        # that occur in quadratic terms of equality rows
        xset = {j for c in I["cons"] if c["quad"] and c["lb"] == c["ub"] for a, b_, _ in c["quad"] for j in (a, b_)}
        keys = sorted({tuple(sorted(a for a, b, _ in c["quad"])) for c in I["cons"]
                       if c["quad"] and not c["lin"] and {a for a, b, _ in c["quad"]} <= xset})
        assert sorted(j for k in keys for j in k) == sorted(xset) and len(keys) == M["n"]
        V = {k: (z[names[a]], z[names[b]]) for k, (a, b) in enumerate(keys)}
    WNN = V[N][0] ** 2 + V[N][1] ** 2
    WLL = V[L][0] ** 2 + V[L][1] ** 2
    Pg, Qg = z[names[info["Pg"]]], z[names[info["Qg"]]]
    q = lambda F_: mp.mpf(F_.numerator) / F_.denominator
    b = q(info["b"])
    Fv = WLL - 2 * Qg / b + (Qg ** 2 + Pg ** 2) / (b * b * WLL)
    print(f"  p1: W_NN {mp.nstr(WNN, 15)}  F(Pg,Qg,W_LL) {mp.nstr(Fv, 15)}  difference {mp.nstr(WNN - Fv, 3)}")
    # p1 is feasible only to ~1e-11; locate its leaf with a 1e-9 tolerance
    tol = mp.mpf("1e-9")
    print(f"  p1: Pg {mp.nstr(Pg, 15)} Qg {mp.nstr(Qg, 15)} W_LL {mp.nstr(WLL, 15)}")
    inside = [lf for lf in leaves if all(q(lf[0][d][0]) - tol <= v <= q(lf[0][d][1]) + tol for d, v in enumerate((Pg, Qg, WLL)))]
    x = [mp.mpf(0)] * (2 * M["n"])
    for k, (e_, f_) in V.items():
        x[2 * k], x[2 * k + 1] = e_, f_
    zz = [z[v] for v in names]
    obj = q(M["obj"]["const"]) + sum(q(c) * zz[j] for j, c in M["obj"]["lin"].items()) + \
        sum(q(c) * zz[j] ** 2 for j, c in M["obj"]["qy"].items())
    for bx, bd, raw in inside:
        worst = max(WNN - (q(al) * Pg + q(be) * Qg + q(ga) * WLL + q(de)) for al, be, ga, de in lc.planes3(info, bx))
        print(f"  leaf containing p1: box {[[float(a), float(c)] for a, c in bx]} bound {float(bd)!r}; "
              f"max cut violation at p1 {mp.nstr(worst, 3)} (<= 0 expected, up to p1 rounding)")
        if raw is None:
            continue
        # Lagrangian at p1 with the leaf's multipliers: bound <= L(p1) <= obj(p1) + |w| * (p1 row violations)
        MM, extra = node_model(M, info, bx)
        rows = list(MM["rows"]) + extra
        Lg = obj
        viol = mp.mpf(0)
        for r, rv in zip(rows, raw):
            e = sum(q(c) * zz[j] for j, c in r["lin"].items()) + sum(q(c) * x[i] * x[j] for (i, j), c in r["Q"].items()) \
                + sum(q(c) * zz[j] ** 2 for j, c in r["qy"].items())
            if rv[0] == "eq":
                Lg += q(Fr(rv[1])) * (e - q(r["lb"])); viol = max(viol, abs(e - q(r["lb"])))
            else:
                if rv[1] is not None and rv[1] > 0:
                    Lg += q(Fr(rv[1])) * (e - q(r["ub"])); viol = max(viol, e - q(r["ub"]))
                if rv[2] is not None and rv[2] > 0:
                    Lg += q(Fr(rv[2])) * (q(r["lb"]) - e); viol = max(viol, q(r["lb"]) - e)
        print(f"  obj(p1) {mp.nstr(obj, 17)}  L(p1) {mp.nstr(Lg, 17)}  bound <= L(p1): {q(bd) <= Lg}  "
              f"L(p1) - bound {mp.nstr(Lg - q(bd), 3)}  max node-row violation at p1 {mp.nstr(viol, 3)}")


if __name__ == "__main__":
    main(*sys.argv[1:])
