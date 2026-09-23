"""Solve the LINKED model with Gurobi, save the best point (original variables), check it in the NATIVE model
with the reviewer's plain-float evaluator.  python run_linked_point.py <instance> <tl> <threads> [native]"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from gmodel import build
name, tl, threads = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
linked = not (len(sys.argv) > 4 and sys.argv[4] == "native")
M, m, x, trig, pw = build(name, linked=linked)
m.Params.TimeLimit = tl; m.Params.Threads = threads; m.Params.MIPGap = 1e-4
t0 = time.time(); m.optimize()
rec = {"name": name, "mode": "linked" if linked else "native", "status": m.Status, "primal": m.ObjVal if m.SolCount else None, "dual": m.ObjBound,
       "nodes": m.NodeCount, "time": time.time() - t0, "gurobi_constr_vio": m.ConstrVio if m.SolCount else None,
       "gurobi_bound_vio": m.BoundVio if m.SolCount else None, "gurobi_int_vio": m.IntVio if m.SolCount else None}
if m.SolCount:
    pt = [v.X for v in x]
    rec["native_check"] = M.check(pt)
    rec["native_check_rounded_int"] = M.check([round(v) if t != "C" else v for v, t in zip(pt, M.vt)])
    json.dump({"name": name, "x": pt}, open(Path(__file__).resolve().parent / f"point_{name}_{rec['mode']}.json", "w"))
print(json.dumps(rec))
