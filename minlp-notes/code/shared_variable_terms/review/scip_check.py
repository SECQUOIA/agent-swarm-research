"""Task 3: does SCIP 10's checkSol accept a point better than SCIP's own 'optimal' value on waterno2_02/_03?
Reviewer's version of check_scip_waterno2.py with Threads=1, plus SCIP runs with default / presolve off / feastol 1e-7.
python scip_check.py <instance> <scip time limit>"""
import json, math, os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pyscipopt as ps
from gmodel import build
name, tl = sys.argv[1], float(sys.argv[2])
path = os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil")
M, m, x, _, _ = build(name, linked=False)
m.Params.Threads = 1; m.Params.TimeLimit = 300; m.Params.MIPGap = 1e-6; m.Params.FeasibilityTol = 1e-9; m.Params.IntFeasTol = 1e-9
m.optimize()
pt = [v.X for v in x]
chk = M.check(pt)
print(json.dumps({"gurobi_status": m.Status, "gurobi_obj": m.ObjVal, "gurobi_bound": m.ObjBound, "native_check": chk}))
s = ps.Model(); s.hideOutput(); s.readProblem(path)
sv = s.getVars(); assert len(sv) == len(x)
sol = s.createSol()
for v, g in zip(sv, pt): s.setSolVal(sol, v, g)
print("SCIP checkSol original, default tol:", s.checkSol(sol, printreason=True, original=True), "obj", s.getSolObjVal(sol))
print("SCIP checkSol original, completely=True:", s.checkSol(sol, printreason=True, completely=True, original=True))
# also with the point's integers rounded and re-checked by the evaluator
pt2 = [round(v) if t != "C" else v for v, t in zip(pt, M.vt)]
print("evaluator check with integers rounded:", json.dumps(M.check(pt2)))
for label, params in (("default", {}), ("presolve off", {"presolving/maxrounds": 0}), ("feastol 1e-7", {"numerics/feastol": 1e-7}),
                      ("presolve off + feastol 1e-7", {"presolving/maxrounds": 0, "numerics/feastol": 1e-7})):
    s = ps.Model(); s.hideOutput(); s.readProblem(path); s.setParam("limits/time", tl); s.setParam("limits/gap", 1e-4)
    for k, v in params.items(): s.setParam(k, v)
    t0 = time.time(); s.optimize()
    out = {"scip": label, "status": s.getStatus(), "primal": s.getObjVal() if s.getNSols() else None, "dual": s.getDualbound(), "time": round(time.time() - t0, 1)}
    if s.getNSols():
        best = s.getBestSol(); ptS = [s.getSolVal(best, v) for v in s.getVars(transformed=False)[:len(x)]]
        out["scip_point_in_evaluator"] = M.check(ptS)
    print(json.dumps(out))
