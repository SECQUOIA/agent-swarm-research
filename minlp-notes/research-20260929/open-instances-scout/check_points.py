"""Evaluate downloaded MINLPLib points (sol/<name>.<p>.sol) on the OSIL model
with the 50-digit evaluator of ../open-instances/osil_eval.py.
Variables missing from a .sol file are taken as 0. The OSIL objective
constant (<obj constant=...>), which osil.py ignores, is added here.

Usage: python3 check_points.py methanol50.p4 hvycrash.p1
"""
import os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "open-instances"))
import osil_eval

HERE = os.path.dirname(os.path.abspath(__file__))

for tag in sys.argv[1:]:
    name = tag.split(".")[0]
    I = osil_eval.load(name)
    vals = {}
    for line in open(os.path.join(HERE, "sol", tag + ".sol")):
        parts = line.split()
        if len(parts) == 2:
            vals[parts[0]] = float(parts[1])
    missing = [v for v in I["names"] if v not in vals]
    x = [vals.get(v, 0.0) for v in I["names"]]
    res = osil_eval.check(name, x, I)
    with open(os.path.join(osil_eval.OSIL_DIR, name + ".osil")) as f:
        m = re.search(r'<obj [^>]*constant="([^"]+)"', f.read(200000))
    const = float(m.group(1)) if m else 0.0
    print(tag, "objective", repr(res["obj"] + const), "(constant", const, ")", "bound viol", res["bound_viol"], "cons viol", res["cons_viol"],
          "worst row", res["worst_row"], "missing vars", len(missing))
