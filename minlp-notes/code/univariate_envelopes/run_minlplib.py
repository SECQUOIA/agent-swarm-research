"""Solve one MINLPLib instance (OSiL) with SCIP in native / split / hybrid mode; print a JSON record."""
import argparse, json, time
from uenv.osil import build_scip, presolved_bounds, read_osil

ap = argparse.ArgumentParser()
ap.add_argument("osil"); ap.add_argument("mode", choices=["native", "split", "hybrid"])
ap.add_argument("--tl", type=float, default=120); ap.add_argument("--log", action="store_true")
a = ap.parse_args()
t0 = time.time()
inst = read_osil(a.osil)
bounds = presolved_bounds(inst) if a.mode != "native" else None
m, hd, stats = build_scip(inst, a.mode, bounds=bounds)
build = time.time() - t0
if not a.log: m.hideOutput()
m.setParam("limits/time", a.tl); m.setParam("limits/gap", 1e-4)
m.optimize()
rec = dict(instance=inst.name, mode=a.mode, status=m.getStatus(), sense=inst.obj_sense,
           primal=m.getObjVal() if m.getNSols() else None, dual=m.getDualbound(), root_dual=m.getDualboundRoot(),
           nodes=m.getNTotalNodes(), time=time.time() - t0, build=build, **stats)
if hd: rec.update(cuts=hd.ncuts, props=hd.nprop)
print(json.dumps(rec))
