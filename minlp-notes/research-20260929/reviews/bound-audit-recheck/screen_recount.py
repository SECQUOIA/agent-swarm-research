"""Own recount of the audit's screen from the audit's parsed pages (bound-audit/pages.json).

Checks the counts quoted in the audit (points, duals, flagged pairs, display ties) and that the
flagged pair set equals the pairs in results.json. The page parsing itself is not rechecked here,
except that the listed values of the 9 instances fetched for this recheck match (logs/listed.log).
"""
import json
import os
from decimal import Decimal as D, InvalidOperation

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIT = os.path.join(HERE, "..", "..", "bound-audit")


def num(s):
    s = s.strip()
    try:
        return D(s[:-1] if s.endswith(".") else s)
    except InvalidOperation:
        return None


P = json.load(open(os.path.join(AUDIT, "pages.json")))
fin = sum(1 for q in P for d in q["duals"] if num(d["value"]) is not None and num(d["value"]).is_finite())
flag, ties, skipped = [], [], 0
for q in P:
    if q["sense"] not in ("min", "max"):
        continue
    for d in q["duals"]:
        dv = num(d["value"])
        if dv is None or not dv.is_finite():
            continue
        for p in q["points"]:
            pv, inf = num(p["value"]), num(p["infeas"])
            if pv is None or inf is None:
                continue
            beyond = dv > pv if q["sense"] == "min" else dv < pv
            if inf > D("1e-5"):
                skipped += beyond
            elif beyond:
                flag.append((q["name"], d["solver"], p["point"], p["section"]))
            elif dv == pv:
                ties.append((q["name"], d["solver"], p["point"]))
print("pages", len(P), "points", sum(len(q["points"]) for q in P), "duals", sum(len(q["duals"]) for q in P),
      "finite", fin, "no sense", [q["name"] for q in P if q["sense"] not in ("min", "max")])
print("flagged pairs", len(flag), "instances", len({f[0] for f in flag}), "points", len({(f[0], f[2]) for f in flag}),
      "other-section", sum(f[3] == "other" for f in flag), "distinct (instance, solver)", len({(f[0], f[1]) for f in flag}))
print("display ties", len(ties), "instances", len({t[0] for t in ties}))
print("pairs beyond the dual with listed infeas > 1e-5:", skipped)
res = json.load(open(os.path.join(AUDIT, "results.json")))
A = {(r["name"], r["solver"], r["point"]) for r in res}
B = {(f[0], f[1], f[2]) for f in flag}
print("same pair set as results.json:", A == B)
