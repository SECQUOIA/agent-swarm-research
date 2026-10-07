"""Exactly feasible point near a listed topopt-cantilever point (Krawczyk + exact checks).

Structure (asserted from the OSIL file): continuous c_e >= 0, binaries y_e, free stress
variables w; cone rows  sum_{w in W_e} w^2 - c_e y_e <= 0;  linear equality rows in the
w only; all other rows involve binaries only; objective sum_e c_e.

Construction:
  * y rounded; for y_e = 0 the cone forces W_e = 0, and the listed decimals are 0 there
    (asserted); these w stay exactly 0;
  * equality rows: a basis B of |rows| solid-element w's is chosen by QR with column
    pivoting; the other w keep their listed decimals; Newton (one step, the system is
    linear) and a Krawczyk test (verify.krawczyk, same operator as the reviewed code)
    prove a solution w_B in a box X;
  * c_e := the (exact binary) upper endpoint of the interval enclosure of sum_{W_e} w^2
    over X, so every cone row holds on X; void c_e keep their decimals;
  * verify.check_on_box then checks every row not in the Krawczyk system, all bounds and
    integrality, and encloses the objective.

Usage: python3 cert_topopt.py <name>.<pk>
"""
import json
import os
import sys
import time
from fractions import Fraction

import mpmath
import numpy as np
import scipy.linalg
from mpmath import iv

import audit_eval as A
import verify as V

HERE = os.path.dirname(os.path.abspath(__file__))


def main(tag):
    t0 = time.time()
    name = tag.rsplit(".", 1)[0]
    m = A.load(name)
    vals = A.read_sol(os.path.join(HERE, "sol", tag + ".sol"))
    names, cons = m["names"], m["cons"]
    nv = len(names)
    cones = []
    for r, c in enumerate(cons):
        if c["quad"]:
            assert c["lb"] == "-INF" and c["ub"] == "0" and not c["lin"] and c["nl"] is None
            bil = [q for q in c["quad"] if q[0] != q[1]]
            assert len(bil) == 1 and Fraction(bil[0][2]) == -1
            a, b = bil[0][:2]
            cv, yv = (a, b) if m["vt"][a] == "C" else (b, a)
            assert m["vt"][yv] == "B" and m["lb"][cv] == "0"
            ws = [q[0] for q in c["quad"] if q[0] == q[1]]
            assert all(Fraction(q[2]) == 1 for q in c["quad"] if q[0] == q[1])
            cones.append((r, cv, yv, ws))
    o = m["obj"]
    assert o["nl"] is None and not o["quad"] and set(o["lin"]) <= {cv for _, cv, _, _ in cones}
    eqrows = [r for r, c in enumerate(cons) if c["lb"] == c["ub"]]
    wset = {w for _, _, _, ws in cones for w in ws}
    for r in eqrows:
        assert not cons[r]["quad"] and cons[r]["nl"] is None and set(cons[r]["lin"]) <= wset
    fixed = {}
    for j in range(nv):
        if m["vt"][j] in ("B", "I"):
            fixed[j] = Fraction(round(Fraction(vals.get(names[j], "0"))))
    solid = []
    for r, cv, yv, ws in cones:
        if fixed[yv] == 0:
            for w in ws:
                assert Fraction(vals.get(names[w], "0")) == 0, "void element with nonzero stress"
                fixed[w] = "0"
            fixed[cv] = vals.get(names[cv], "0")
        else:
            solid.append((r, cv, ws))
    cand = sorted({w for _, _, ws in solid for w in ws})
    rows = [r for r in eqrows if set(cons[r]["lin"]) - fixed.keys()]
    const_rows = [r for r in eqrows if r not in set(rows)]
    for r in const_rows:  # equality rows over fixed (zero) w only: must hold exactly
        assert V.row_ok_frac(cons[r], V.row_frac(cons[r], [Fraction(fixed.get(j, "0")) if j in fixed else Fraction(0)
                                                           for j in range(nv)]))
    x0 = np.array([float(Fraction(vals.get(names[j], "0"))) for j in cand])
    fx = dict(fixed)
    for _, cv, _ in solid:
        fx[cv] = vals.get(names[cv], "0")
    _, _, J, _ = V.resid_jac(m, rows, ["lb"] * len(rows), cand, x0, fx)
    J = J.toarray()
    print("system", J.shape, round(time.time() - t0), "s", flush=True)
    _, Rq, piv = scipy.linalg.qr(J, pivoting=True, mode="economic", overwrite_a=True)
    d = np.abs(np.diag(Rq))
    rank = int(np.sum(d > 1e-12 * d.max()))
    assert rank == len(rows), (rank, len(rows))
    B = sorted(cand[k] for k in piv[:len(rows)])
    Bs = set(B)
    for j in cand:
        if j not in Bs:
            fx[j] = vals.get(names[j], "0")
    print("basis chosen", round(time.time() - t0), "s", flush=True)
    xB0 = np.array([float(Fraction(vals.get(names[j], "0"))) for j in B])
    xt, hist = V.newton(m, rows, ["lb"] * len(rows), B, xB0, fx, iters=3)
    print("newton", hist, round(time.time() - t0), "s", flush=True)
    kt = X = None
    for rho in (1e-14, 1e-12, 1e-10):
        kt, X = V.krawczyk(m, rows, ["lb"] * len(rows), B, xt, rho * np.maximum(1e-3, np.abs(xt)), fx)
        print("krawczyk", rho, kt, round(time.time() - t0), "s", flush=True)
        if kt["ok"]:
            break
    out = dict(tag=tag, n_rows=len(rows), n_solid=len(solid), newton=hist, krawczyk=kt)
    if not kt["ok"]:
        out["status"] = "fail: Krawczyk"
        print(json.dumps(out, default=str))
        return
    Bpos = {j: k for k, j in enumerate(B)}
    for _, cv, ws in solid:
        s = iv.mpf(0)
        for w in ws:
            s += (X[Bpos[w]] if w in Bpos else V.exact_iv(fx[w])) ** 2
        up = V._exact(s.b)  # exact binary value of the upper endpoint (400-bit copy)
        assert up >= 0
        fx[cv] = up  # exact rational, >= sum of squares for every w in X
    res = {}
    V.check_on_box(m, fx, B, X, set(rows) | set(const_rows), res)
    cen = res.pop("_center", None)
    if cen is not None:  # centre of the proof box, for the independent numerical cross-check
        with open(os.path.join(HERE, "logs", f"cert_topopt_{tag}.center.sol"), "w") as f:
            for n_, v_ in zip(names, cen):
                f.write(f"{n_} {v_}\n")
    out.update(status=res["status"], n_bad=res["n_bad"], bad=res["bad"],
               obj_lo=res["obj_lo"], obj_hi=res["obj_hi"],
               sec=round(time.time() - t0))
    print(json.dumps(out, indent=1, default=str))
    json.dump(out, open(os.path.join(HERE, "logs", f"cert_topopt_{tag}.json"), "w"), indent=1, default=str)


if __name__ == "__main__":
    main(sys.argv[1])
