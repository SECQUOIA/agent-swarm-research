"""Convert a CIP file in the subset read by exact_check.py into a spec JSON
(models/<key>.json) and copy its witness to witness/<key>.json, so that
minimize.py can work on it.  usage: python3 cip2spec.py MODEL.cip WITNESS.json KEY"""
import json
import shutil
import sys
from decimal import Decimal, getcontext

import exact_check as ec

getcontext().prec = 60


def dec(q):
    if q is None:
        return None
    s = format(Decimal(q.numerator) / Decimal(q.denominator), "f")
    assert ec.F(s) == q, q
    return s


vars_, rows = ec.parse_cip(sys.argv[1])
spec = dict(name=sys.argv[3],
            vars=[dict(name=v["name"], type="B" if v["type"] == "binary" else "C", lb=dec(v["lb"]), ub=dec(v["ub"]))
                  for v in vars_],
            rows=[dict(name=r["name"], terms=[[dec(a), ns] for a, ns in r["terms"]],
                       lhs=dec(r["rhs"]) if r["op"] in ("==", ">=") else None,
                       rhs=dec(r["rhs"]) if r["op"] in ("==", "<=") else None) for r in rows],
            obj=[[v["name"], dec(v["obj"])] for v in vars_ if v["obj"] != 0])
json.dump(spec, open(f"models/{sys.argv[3]}.json", "w"), indent=0)
shutil.copy(sys.argv[2], f"witness/{sys.argv[3]}.json")
print("wrote", f"models/{sys.argv[3]}.json")
