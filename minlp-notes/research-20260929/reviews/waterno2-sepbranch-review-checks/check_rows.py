"""Period split of waterno2_06 (first verifier's vmodel): every variable in one
period, objective = 9 cost variables per period, every row inside a period or
a link row except the horizon row."""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import sys
sys.path.insert(0, _RESEARCH + "/reviews/waterno2-verification")
import vmodel

I = vmodel.instance(6)
m = I["m"]
allv = set(v for vs in I["per_vars"] for v in vs)
print("variables", len(m["names"]), "in periods", len(allv),
      "disjoint", sum(len(vs) for vs in I["per_vars"]) == len(allv))
print("objective variables", len(m["obj"]["lin"]), "all in periods", all(v in allv for v in m["obj"]["lin"]),
      "per period", [sum(1 for v in I["per_vars"][t] if v in m["obj"]["lin"]) for t in range(6)],
      "coefficients", sorted(set(m["obj"]["lin"].values())))
rows = set(i for rs in I["per_rows"] for i in rs) | set(i for lk in I["links"] for (i, a, b) in lk)
print("rows", len(m["cons"]), "in periods or links", len(rows), "outside:",
      [m["cons"][i]["name"] for i in range(len(m["cons"])) if i not in rows], "horizon row", I["hname"])
