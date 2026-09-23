"""Pilot: variables theta that occur in both sin(theta) and cos(theta).  SCIP native model against the
same model plus  s = sin(theta), c = cos(theta), s^2 + c^2 = 1  (SCIP shares the common subexpressions).
python trig_pilot.py <instance> {native|circle|disc} [tl]"""
import json, math, os, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "univariate_envelopes"))
import pyscipopt as ps
from uenv.osil import read_osil, build_scip


def trig_vars(t, acc):
    if t[0] in ("sin", "cos") and t[1][0] == "var":
        acc.setdefault(t[1][1], set()).add(t[0])
    if t[0] not in ("num", "var"):
        for c in t[1:]:
            trig_vars(c, acc)
    return acc


name, mode = sys.argv[1], sys.argv[2]
tl = float(sys.argv[3]) if len(sys.argv) > 3 else 120
inst = read_osil(os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil"))
acc = {}
for r in inst.rows:
    if r["nl"] is not None:
        trig_vars(r["nl"], acc)
both = [v for v, k in acc.items() if len(k) == 2]
m, _h, _st = build_scip(inst, "native")
xs = {int(v.name[1:]): v for v in m.getVars() if v.name.startswith("v") and v.name[1:].isdigit()}
if mode != "native":
    for v in both:
        s = m.addVar(lb=-1, ub=1, name=f"sin_{v}"); c = m.addVar(lb=-1, ub=1, name=f"cos_{v}")
        m.addCons(s == ps.sin(xs[v])); m.addCons(c == ps.cos(xs[v]))
        m.addCons(s * s + c * c == 1 if mode == "circle" else s * s + c * c <= 1)
m.hideOutput(); m.setParam("limits/time", tl); m.setParam("limits/gap", 1e-4)
t0 = time.time(); m.optimize()
print(json.dumps({"name": name, "mode": mode, "pairs": len(both), "status": m.getStatus(),
                  "primal": m.getObjVal() if m.getNSols() else None, "dual": m.getDualbound(),
                  "nodes": m.getNTotalNodes(), "time": time.time() - t0}))
