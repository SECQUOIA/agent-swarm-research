"""Exact rational evaluation of every constraint, bound and integrality condition of the NATIVE
OSiL model at a saved point (floats are exact rationals).  Works for models built from +, -, *, /,
integer powers and squares only.  python exact_check_point.py <instance> <point.json>"""
import json, math, os, sys
from fractions import Fraction as F
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "univariate_envelopes"))
from uenv.osil import read_osil


def ev(t, v):
    op = t[0]
    if op == "num": return F(t[1])
    if op == "var": return v[t[1]]
    k = [ev(c, v) for c in t[1:]]
    if op == "sum": return sum(k, F(0))
    if op == "negate": return -k[0]
    if op == "times":
        o = F(1)
        for c in k: o *= c
        return o
    if op == "divide": return k[0] / k[1]
    if op == "square": return k[0] ** 2
    if op == "power":
        e = t[2][1]
        assert t[2][0] == "num" and float(e) == int(e), "non-integer exponent: not exact"
        return k[0] ** int(e)
    raise NotImplementedError(op)


name, pf = sys.argv[1], sys.argv[2]
inst = read_osil(os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil"))
pt = json.load(open(pf))["point"]
v = [F(x) for x in pt]
worst, worst_where = F(0), None
for i, (l, u, t) in enumerate(zip(inst.var_lb, inst.var_ub, inst.var_type)):
    for val, tag in ((F(l) - v[i] if math.isfinite(l) else F(0), f"lb{i}"), (v[i] - F(u) if math.isfinite(u) else F(0), f"ub{i}")):
        if val > worst: worst, worst_where = val, tag
    if t in ("B", "I"):
        d = abs(v[i] - round(v[i]))
        if d > worst: worst, worst_where = d, f"int{i}"
for ridx, r in enumerate(inst.rows):
    if ridx == 0: continue
    a = sum((F(c) * v[i] for i, c in r["lin"].items()), F(0)) + sum((F(c) * v[i] * v[j] for i, j, c in r["quad"]), F(0))
    if r["nl"] is not None: a += ev(r["nl"], v)
    for val, tag in ((F(r["lb"]) - a if math.isfinite(r["lb"]) else F(0), f"row{ridx}lb"), (a - F(r["ub"]) if math.isfinite(r["ub"]) else F(0), f"row{ridx}ub")):
        if val > worst: worst, worst_where = val, tag
obj = inst.rows[0]
o = sum((F(c) * v[i] for i, c in obj["lin"].items()), F(0)) + sum((F(c) * v[i] * v[j] for i, j, c in obj["quad"]), F(0)) + F(inst.obj_const)
if obj["nl"] is not None: o += ev(obj["nl"], v)
print(json.dumps({"name": name, "objective_exact": str(o), "objective_float": float(o),
                  "max_violation_exact": str(worst), "max_violation_float": float(worst), "where": worst_where,
                  "nvars": len(v), "nrows": len(inst.rows) - 1}))
