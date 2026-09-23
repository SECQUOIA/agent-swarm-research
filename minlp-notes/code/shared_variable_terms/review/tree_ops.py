"""Which expression-node shapes occur in the 46 instances that gurobi_link.py translates (power bases/exponents, divide)."""
import sys, os, collections
from pathlib import Path
D = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(D.parent / "univariate_envelopes"))
from uenv.osil import read_osil
c = collections.Counter()
def walk(t, name):
    if t[0] in ("num", "var"): return
    if t[0] == "power": c[(name, "power", t[1][0], t[2][0], "int" if t[2][0] == "num" and float(t[2][1]).is_integer() else "nonint")] += 1
    if t[0] == "divide": c[(name, "divide", t[1][0], t[2][0])] += 1
    if t[0] == "sum" and len(t) == 2: c[(name, "unary sum")] += 1
    for k in t[1:]: walk(k, name)
for name in open(D / "link_instances.txt").read().split():
    inst = read_osil(os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil"))
    for r in inst.rows:
        if r["nl"] is not None: walk(r["nl"], name)
    ranged = sum(1 for r in inst.rows[1:] if r["lb"] != r["ub"] and all(map(__import__("math").isfinite, (r["lb"], r["ub"]))))
    if ranged: c[(name, "ranged rows")] = ranged
    if inst.obj_const: c[(name, "obj const", inst.obj_const)] = 1
    if inst.obj_sense == "max": c[(name, "MAX")] = 1
    if inst.rows[0]["nl"] is not None or inst.rows[0]["quad"]: c[(name, "nonlinear objective")] = 1
for k, v in sorted(c.items()): print(k, v)
