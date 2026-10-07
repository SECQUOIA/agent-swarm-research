"""Re-evaluate the MINLPLib point p1 at 50 digits with the reviewer's own OSIL reader:
objective, every native OSIL row, the leaf identity, the cut rows of the leaf(s)
containing p1, and the Lagrangian L(p1) of those leaves (own rows, stored multipliers).
    python3 p1_check.py <name> <tag> [<tag> ...]
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import json
import os
import sys
from fractions import Fraction as Fr

import mpmath as mp

sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave3/powerflow")
import pf_model as pm  # noqa: E402  (row order only)
import own_osil  # noqa: E402
import own_relax as orl  # noqa: E402
from verify_leaves import leaf_data, node_rows, LOGS, N, L  # noqa: E402

SOL = _REPRO_ROOT + "/research-20260929/open-instances-wave3/sol"


def q(F):
    return mp.mpf(F.numerator) / F.denominator


def main(name, tags):
    mp.mp.dps = 50
    R = orl.build(name)
    I = R["I"]
    vals = {}
    for line in open(os.path.join(SOL, f"{name}.p1.sol")):
        p = line.split()
        if len(p) == 2:
            vals[p[0]] = p[1]
    missing = [v for v in I["names"] if v not in vals]
    z = [mp.mpf(vals.get(v, "0")) for v in I["names"]]
    obj = own_osil.obj_value(I, z, mp)
    viol, where = mp.mpf(0), None
    for r, c in enumerate(I["cons"]):
        v = own_osil.row_value(I, r, z, mp)
        e = max(mp.mpf(0), (q(c["lb"]) - v) if c["lb"] is not None else 0, (v - q(c["ub"])) if c["ub"] is not None else 0)
        if e > viol:
            viol, where = e, c["name"]
    print(f"== {name}: p1 missing vars (set to 0): {missing}; obj(p1) = {mp.nstr(obj, 20)}; "
          f"max native row violation {mp.nstr(viol, 3)} at {where}")
    x = orl.x_of_point(R, z)
    ld = leaf_data(R)
    WNN = x[2 * N] ** 2 + x[2 * N + 1] ** 2
    WLL = x[2 * L] ** 2 + x[2 * L + 1] ** 2
    Pg, Qg, b = z[ld["Pg"]], z[ld["Qg"]], q(ld["b"])
    Fv = WLL - 2 * Qg / b + (Qg ** 2 + Pg ** 2) / (b * b * WLL)
    print(f"  p1: Pg {mp.nstr(Pg, 12)} Qg {mp.nstr(Qg, 15)} W_LL {mp.nstr(WLL, 15)} (v_L {mp.nstr(mp.sqrt(WLL), 15)}); "
          f"W_NN {mp.nstr(WNN, 15)}; W_NN - F {mp.nstr(WNN - Fv, 3)}")
    # all relaxation rows at p1
    rv = mp.mpf(0)
    for nm, r in R["rows"].items():
        v = orl.row_val(r, z, x)
        rv = max(rv, (q(r["lb"]) - v) if r["lb"] is not None else 0, (v - q(r["ub"])) if r["ub"] is not None else 0)
    print(f"  max violation of own relaxation rows (without angle rows) at mapped p1: {mp.nstr(rv, 3)}")
    M = pm.decode(name)
    tol = mp.mpf("1e-9")
    for tag in tags:
        D = json.load(open(os.path.join(LOGS, f"{name}.{tag}.json")))
        for lf in D["leaves"]:
            bx = tuple((Fr(a), Fr(c)) for a, c in lf["box"])
            if not all(q(bx[d][0]) - tol <= v <= q(bx[d][1]) + tol for d, v in enumerate((Pg, Qg, WLL))):
                continue
            rows, ybox, npl = node_rows(R, M, ld, bx)
            Lg = q(R["obj"]["const"]) + mp.fsum(q(c) * z[j] for j, c in R["obj"]["lin"].items()) + \
                mp.fsum(q(c) * z[j] ** 2 for j, c in R["obj"]["qy"].items())
            assert abs(Lg - obj) < mp.mpf("1e-40")
            worst_cut, worst_row = mp.mpf("-inf"), mp.mpf(0)
            for r, rvv in zip(rows, lf["raw"]):
                h = orl.row_val(r, z, x)
                if r["ub"] is not None:
                    worst_row = max(worst_row, h - q(r["ub"]))
                if r["lb"] is not None:
                    worst_row = max(worst_row, q(r["lb"]) - h)
                if r["lb"] is None and r["ub"] is not None and (2 * N, 2 * N) in r["Q"]:
                    worst_cut = max(worst_cut, h - q(r["ub"]))
                if rvv[0] == "eq":
                    Lg += q(Fr(rvv[1])) * (h - q(r["lb"]))
                else:
                    if rvv[1] is not None and rvv[1] > 0:
                        Lg += q(Fr(rvv[1])) * (h - q(r["ub"]))
                    if rvv[2] is not None and rvv[2] > 0:
                        Lg += q(Fr(rvv[2])) * (q(r["lb"]) - h)
            bd = Fr(lf["bound"])
            print(f"  [{tag}] leaf {[[float(a), float(c)] for a, c in bx]}: max cut-row value - rhs at p1 {mp.nstr(worst_cut, 3)}; "
                  f"max node-row violation {mp.nstr(worst_row, 3)}; L(p1) {mp.nstr(Lg, 17)}; stored bound {float(bd)!r}; "
                  f"L(p1) - bound {mp.nstr(Lg - q(bd), 3)}; obj(p1) - L(p1) {mp.nstr(obj - Lg, 3)}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
