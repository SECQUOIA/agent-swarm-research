"""Separable family solved by SCIP with the univariate handler (mode=uenv) or natively (mode=native)."""
import argparse, json, sys, time
sys.path.insert(0, "../vertex_binarization")
import pyscipopt as ps
from sob.instances import FAMILIES
from sob.backends import _walk
from uenv.envelope import Univariate
from uenv.scip_plugin import install, add_univariate

ap = argparse.ArgumentParser()
ap.add_argument("family"); ap.add_argument("n", type=int); ap.add_argument("m", type=int); ap.add_argument("seed", type=int)
ap.add_argument("mode", choices=["uenv", "hybrid", "native"]); ap.add_argument("--tl", type=float, default=60); ap.add_argument("--log", action="store_true")
a = ap.parse_args()
p = FAMILIES[a.family](a.n, a.m, a.seed)
t0 = time.time()
m = ps.Model()
if not a.log: m.hideOutput()
m.setParam("limits/time", a.tl); m.setParam("limits/gap", 1e-4)
hd = install(m, hybrid=a.mode == "hybrid") if a.mode != "native" else None
fn = {"exp": ps.exp, "log": ps.log, "sin": ps.sin, "cos": ps.cos, "sqrt": ps.sqrt, "Abs": abs}
xs, ws = [], []
for i, f in enumerate(p.funcs):
    uf = Univariate(f.expr, f.lo, f.hi)
    glo, ghi = uf.range(f.lo, f.hi)          # both modes get the same finite bounds on w
    x = m.addVar(lb=f.lo, ub=f.hi, name=f"x{i}"); w = m.addVar(lb=glo, ub=ghi, name=f"w{i}")
    xs.append(x); ws.append(w)
    if hd: add_univariate(m, hd, w, x, uf, f"u{i}")
    if a.mode != "uenv": m.addCons(w == _walk(f.expr, x, fn))
for r in range(p.A.shape[0]):
    lhs = ps.quicksum(float(p.A[r, i]) * xs[i] for i in range(p.n))
    m.addCons(lhs == float(p.b[r]) if p.sense[r] == "==" else lhs <= float(p.b[r]) if p.sense[r] == "<=" else lhs >= float(p.b[r]))
m.setObjective(ps.quicksum(ws)); m.optimize()
sol = m.getBestSol() if m.getNSols() else None
rec = dict(instance=p.name, mode=a.mode, status=m.getStatus(), primal=m.getObjVal() if sol else None, dual=m.getDualbound(),
           nodes=m.getNTotalNodes(), time=time.time() - t0)
if sol:
    xv = [min(max(m.getSolVal(sol, x), f.lo), f.hi) for f, x in zip(p.funcs, xs)]
    rec["max_viol"] = max(abs(m.getSolVal(sol, w) - f(v)) for f, v, w in zip(p.funcs, xv, ws))
    rec["true_obj"] = sum(f(v) for f, v in zip(p.funcs, xv))
if hd: rec.update(cuts=hd.ncuts, branch=hd.nbranch, props=hd.nprop)
print(json.dumps(rec))
