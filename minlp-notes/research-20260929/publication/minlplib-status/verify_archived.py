"""Part B: re-run the audit's existence proofs on model versions that differ
from the current MINLPLib OSIL by rounding of constants.

history.py found three such cases among the audited instances:
  ghg_3veh    the 2010 MINLPLib 1 file and the 2017 MINLPLib.jl file write
              2715.789473684205 and 376.0467809974723 where the current
              files write 2715.7894736842 and 376.046780997472 (rows e32,
              e39, e46, e113; relative change about 2e-15);
  methanol50  the current .gms (text-identical, after GAMS conversion, to the
              2001 GLOBALLib file) has objective constant 5.01625659; the
              current OSIL, which expands the squares in floating point,
              has 5.016256589999999;
  lop97icx    the OSIL folds constants of the objective in floating point
              (relative difference about 1e-17 to the .gms form).
For each case the audit's point is checked on the OSiL that GAMS 54.3 writes
for the other version, with the audit's own code (bound-audit/verify.py:
route A exact check, else route B polish + Krawczyk), and the resulting
objective enclosure is compared with the listed dual bounds.

Assumptions as in the audit (Section 7): mpmath iv encloses the elementary
functions correctly; IEEE double arithmetic in numpy; exact checks use
Python Fractions. GAMS 54.3 writes each constant of the archived .gms in
OSiL as a decimal that rounds to the same double; the check is for that
decimal model.

Usage: python3 verify_archived.py
Output: data/verify_archived.json
"""
import json
import os
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(R, "bound-audit"))
import audit_eval as A  # noqa: E402
import verify as V  # noqa: E402
import osilx  # noqa: E402

CASES = [
    ("ghg_3veh", "gamsworld-MINLPLib", "ghg_3veh.p2", {"ANTIGONE": "7.7543245", "BARON": "7.7543245"}),
    ("ghg_3veh", "jl2017", "ghg_3veh.p2", {"ANTIGONE": "7.7543245", "BARON": "7.7543245"}),
    ("methanol50", "current", "methanol50.p4", {"LINDO": "0.00802826"}),
    ("lop97icx", "gamsworld-MINLPLib", "lop97icx.p2", {"ANTIGONE": "4099.06"}),
]


def slack(d):
    """half a unit in the last shown digit, at least half a unit in the 10th
    significant digit (audit Section 2)"""
    s = d.lstrip("-")
    dec = len(s.split(".")[1]) if "." in s else 0
    unit = Fraction(1, 10 ** dec)
    v = abs(Fraction(d))
    if v == 0:
        return Fraction(5, 10 ** 9)
    e = len(str(int(v))) if v >= 1 else -len(str(v.denominator)) + 1
    tenth = Fraction(10) ** (e - 10)
    return max(unit, tenth) / 2


def main():
    out = []
    for name, tag, pt, duals in CASES:
        t0 = time.time()
        osil = os.path.join(HERE, "pages", "canon", name, tag, name + ".osil")
        m = osilx.read(osil)
        assert m["obj"]["sense"] == "min"
        vals = A.read_sol(os.path.join(R, "bound-audit", "sol", pt + ".sol"))
        res = V.exact_check(m, vals)
        if res["ok"]:
            res.update(status="proved", route="A (exactly feasible as listed)")
        else:
            why = res["reason"]
            res = V.verify_point(m, vals, log=lambda s: None)
            res["route"] = "B (polish + Krawczyk)"
            res["route_A_failure"] = why
        res.pop("_center", None)
        rec = dict(instance=name, version=tag, osil=os.path.relpath(osil, HERE), point=pt,
                   status=res.get("status"), route=res.get("route"), route_A_failure=res.get("route_A_failure"),
                   obj_lo=str(res.get("obj_lo")), obj_hi=str(res.get("obj_hi")), seconds=round(time.time() - t0, 1))
        if res.get("status") == "proved":
            hi = Fraction(str(res["obj_hi"])) if not isinstance(res["obj_hi"], Fraction) else res["obj_hi"]
            cls = {}
            for s, d in duals.items():
                marg = Fraction(d) - hi
                cls[s] = dict(dual=d, margin_lower_bound=float(marg), slack=float(slack(d)),
                              verdict=("invalid beyond rounding (class i)" if marg > slack(d) else
                                       "invalid within rounding (class i-r)" if marg > 0 else "not refuted"))
            rec["duals"] = cls
        else:
            rec["detail"] = {k: str(v)[:300] for k, v in res.items() if k not in ("B", "xt")}
        out.append(rec)
        print(json.dumps(rec, default=str), flush=True)
    json.dump(out, open(os.path.join(HERE, "data", "verify_archived.json"), "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
