"""Second exact check of the witnesses, from the JSON specs (not from the CIP
files): evaluates every row and bound in Fraction arithmetic.
usage: python3 spec_check.py SPEC.json WITNESS.json"""
import json
import sys
from fractions import Fraction as F

spec, w = json.load(open(sys.argv[1])), {k: F(v) for k, v in json.load(open(sys.argv[2])).items()}
bad = []
for r in spec["rows"]:
    val = F(0)
    for a, ns in r["terms"]:
        t = F(a)
        for n in ns:
            t *= w[n]
        val += t
    if r["lhs"] is not None and val < F(r["lhs"]) or r["rhs"] is not None and val > F(r["rhs"]):
        bad.append(r["name"])
for v in spec["vars"]:
    x = w[v["name"]]
    if v["lb"] is not None and x < F(v["lb"]) or v["ub"] is not None and x > F(v["ub"]) or v["type"] == "B" and x not in (0, 1):
        bad.append(v["name"])
obj = sum(F(a) * w[n] for n, a in spec["obj"])
print(f"{sys.argv[1]}: {len(spec['rows'])} rows, {len(spec['vars'])} vars; violated: {bad or 'none'}; objective {obj} ~ {float(obj):.12f}")
