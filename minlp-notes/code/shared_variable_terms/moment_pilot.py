"""Pairs (x^2, x^3) of a variable x in [l,u], l >= 0: add the exact convex hull of the moment curve
(x, x^2, x^3) on [l,u] as two rotated second-order cone constraints (Karlin-Shapley / Hankel form):
   (x - l)(t3 - l t2) >= (t2 - l x)^2,      (u - x)(u t2 - t3) >= (u x - t2)^2,
with all four factors nonnegative.  python moment_pilot.py <instance> {native|linked|moment} [tl]"""
import json, math, os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "univariate_envelopes"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from uenv.osil import read_osil, build_scip
import link_detect

name, mode = sys.argv[1], sys.argv[2]
tl = float(sys.argv[3]) if len(sys.argv) > 3 else 60
inst = read_osil(os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil"))
trig, pw = link_detect.detect(inst)
pw = {v: p for v, p in pw.items() if p == [2.0, 3.0]}
m, _h, _s = build_scip(inst, "native")
xs = {int(v.name[1:]): v for v in m.getVars() if v.name.startswith("v") and v.name[1:].isdigit()}
for v in pw:
    if mode == "native":
        break
    l, u = inst.var_lb[v], inst.var_ub[v]
    x = xs[v]
    t2 = m.addVar(lb=l * l, ub=u * u); t3 = m.addVar(lb=l ** 3, ub=u ** 3)
    m.addCons(t2 == x ** 2); m.addCons(t3 == x ** 3)
    if mode == "linked":
        m.addCons(t3 == t2 ** 1.5)
    else:
        a1 = m.addVar(lb=0, ub=u - l); b1 = m.addVar(lb=0, ub=None); c1 = m.addVar(lb=None, ub=None)
        m.addCons(a1 == x - l); m.addCons(b1 == t3 - l * t2); m.addCons(c1 == t2 - l * x)
        m.addCons(c1 * c1 <= a1 * b1)
        a2 = m.addVar(lb=0, ub=u - l); b2 = m.addVar(lb=0, ub=None); c2 = m.addVar(lb=None, ub=None)
        m.addCons(a2 == u - x); m.addCons(b2 == u * t2 - t3); m.addCons(c2 == u * x - t2)
        m.addCons(c2 * c2 <= a2 * b2)
m.hideOutput(); m.setParam("limits/time", tl); m.setParam("limits/gap", 1e-4)
t0 = time.time(); m.optimize()
print(json.dumps({"name": name, "solver": "scip", "mode": mode, "pairs": len(pw), "status": m.getStatus(),
                  "primal": m.getObjVal() if m.getNSols() else None, "dual": m.getDualbound(),
                  "nodes": m.getNTotalNodes(), "time": time.time() - t0}))
