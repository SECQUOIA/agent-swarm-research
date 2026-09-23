"""lnts family: terms tf*cos(u_k) and tf*sin(u_k) share both variables.  Modes:
  native | circle (s^2+c^2 = 1) | soc (p = tf*c, q = tf*s, p^2+q^2 = tf^2, and the circle)."""
import json, os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "univariate_envelopes"))
import pyscipopt as ps
from uenv.osil import read_osil, build_scip

name, mode, tl = sys.argv[1], sys.argv[2], float(sys.argv[3])
inst = read_osil(os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil"))
angles, tfs = set(), set()
def walk(t):
    if t[0] in ("sin", "cos") and t[1][0] == "var": angles.add(t[1][1])
    if t[0] == "times":
        for c in t[1:]:
            if c[0] == "var": tfs.add(c[1])
    if t[0] not in ("num", "var"):
        for c in t[1:]: walk(c)
for r in inst.rows:
    if r["nl"] is not None: walk(r["nl"])
assert len(tfs) == 1
tfi = tfs.pop()
m, _h, _s = build_scip(inst, "native")
xs = {int(v.name[1:]): v for v in m.getVars() if v.name.startswith("v") and v.name[1:].isdigit()}
if mode != "native":
    for u in sorted(angles):
        s = m.addVar(lb=-1, ub=1); c = m.addVar(lb=-1, ub=1)
        m.addCons(s == ps.sin(xs[u])); m.addCons(c == ps.cos(xs[u])); m.addCons(s * s + c * c == 1)
        if mode == "soc":
            p = m.addVar(lb=None, ub=None); q = m.addVar(lb=None, ub=None)
            m.addCons(p == xs[tfi] * c); m.addCons(q == xs[tfi] * s)
            m.addCons(p * p + q * q == xs[tfi] * xs[tfi])
m.hideOutput(); m.setParam("limits/time", tl); m.setParam("limits/gap", 1e-4)
t0 = time.time(); m.optimize()
print(json.dumps({"name": name, "mode": mode, "status": m.getStatus(), "primal": m.getObjVal() if m.getNSols() else None,
                  "dual": m.getDualbound(), "nodes": m.getNTotalNodes(), "time": time.time() - t0}))
