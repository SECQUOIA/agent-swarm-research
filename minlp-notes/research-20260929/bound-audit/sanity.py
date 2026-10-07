"""Negative controls for verify.py (not part of any proof).

1. ghg_3veh.p2 verifies as listed-point repair (positive control).
2. Krawczyk test (methanol50) with the centre moved by 1e-11 (relative) and radius 1e-12 must fail;
   with radius 1e-11 (box contains the solution) it must pass.
3. The box check passes on a tiny box around the proof centre and fails once an inactive
   inequality row is tightened by 1e-9 (relative) below its value there.
4. Tightening a variable bound to cut off the listed value must make route A fail.

Usage: python3 sanity.py
"""
import copy

import numpy as np

import audit_eval as A
import verify as V


def main():
    m = A.load("ghg_3veh")
    vals = A.read_sol("sol/ghg_3veh.p2.sol")
    r = V.verify_point(m, vals, log=lambda s: None)
    print("1 positive control:", r["status"], r.get("obj_lo"), r.get("obj_hi"))
    assert r["status"] == "proved"

    # 2: methanol50 (all rows are equalities, so the square system is all rows and the
    #    proof's basis); perturb the centre
    from fractions import Fraction
    mm = A.load("methanol50")
    rm = V.verify_point(mm, A.read_sol("sol/methanol50.p4.sol"), log=lambda s: None)
    assert rm["status"] == "proved"
    nm = mm["names"]
    B = [nm.index(b) for b in rm["B"]]
    Bs = set(B)
    fixed = {j: Fraction(rm["_center"][j]) for j in range(len(nm)) if j not in Bs}
    rows = list(range(len(mm["cons"])))
    sides = ["lb"] * len(rows)
    xt = np.array([float(v) for v in rm["xt"]])
    rad = lambda rho: rho * np.maximum(1, np.abs(xt))
    ok0, _ = V.krawczyk(mm, rows, sides, B, xt, rad(1e-12), fixed)
    xb = xt.copy()
    xb[0] *= 1 + 1e-11
    bad, _ = V.krawczyk(mm, rows, sides, B, xb, rad(1e-12), fixed)
    big, _ = V.krawczyk(mm, rows, sides, B, xb, rad(1e-11), fixed)
    print("2 Krawczyk (methanol50): unperturbed", ok0["ok"], "| moved 1e-11, r=1e-12:", bad["ok"],
          "| moved 1e-11, r=1e-11:", big["ok"])
    assert ok0["ok"] and not bad["ok"] and big["ok"]
    names = m["names"]
    cen = r["_center"]
    B = [names.index(b) for b in r["B"]]

    # 3: box check on a small box around the proof centre: passes for the model, and fails
    #    once an inactive inequality row is tightened below its value there
    from mpmath import iv
    import osilx
    Bs = set(B)
    fx = {j: Fraction(cen[j]) for j in range(len(names)) if j not in Bs}
    X = [iv.mpf([float(Fraction(cen[j])) * (1 - 1e-12), float(Fraction(cen[j])) * (1 + 1e-12)])
         if float(Fraction(cen[j])) >= 0 else
         iv.mpf([float(Fraction(cen[j])) * (1 + 1e-12), float(Fraction(cen[j])) * (1 - 1e-12)]) for j in B]
    x = [A.num(cen[j]) for j in range(len(names))]
    eqs = set()  # equality rows and rows active at the centre (these were in the square system)
    for k, c in enumerate(m["cons"]):
        v = float(osilx.ev_row(c, x, A.num, A.FNS))
        if c["lb"] == c["ub"] or (not osilx.isinf(c["lb"]) and v - float(c["lb"]) < 1e-9) or \
                (not osilx.isinf(c["ub"]) and float(c["ub"]) - v < 1e-9):
            eqs.add(k)
    res0 = {}
    V.check_on_box(m, fx, B, X, eqs, res0)
    for k, c in enumerate(m["cons"]):
        if k not in eqs and not osilx.isinf(c["ub"]):
            v = osilx.ev_row(c, x, A.num, A.FNS)
            if float(v) < float(c["ub"]) - 1e-3:
                m2 = copy.deepcopy(m)
                m2["cons"][k]["ub"] = repr(float(v) - 1e-9 * max(1.0, abs(float(v))))
                res2 = {}
                V.check_on_box(m2, fx, B, X, eqs, res2)
                print("3 box check: model", res0["status"], "| row", c["name"], "tightened:", res2["status"], res2.get("bad"))
                assert res0["status"] == "proved" and res2["status"] == "fail" and "row " + c["name"] in res2["bad"]
                break

    # 4: a variable bound that cuts off the listed value
    for j, n in enumerate(names):
        if m["vt"][j] == "C" and vals.get(n) and float(vals[n]) > 1e-3 and osilx.isinf(m["ub"][j]):
            m3 = copy.deepcopy(m)
            m3["ub"][j] = repr(float(vals[n]) / 2)
            r3 = V.exact_check(m3, vals)
            print("4 bound of", n, "cut off:", r3["ok"], r3["reason"])
            assert not r3["ok"]
            break


if __name__ == "__main__":
    main()
