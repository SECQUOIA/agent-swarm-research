"""Solve an OSiL QCQP with Gurobi and verify the incumbent with osil_eval."""
import sys, os, json
from osil_eval import Model, FloatB
from grb_build import build
name, tlim = sys.argv[1], float(sys.argv[2])
M = Model(os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil"))
g, x = build(M)
g.Params.TimeLimit = tlim; g.Params.Threads = 1
g.optimize()
out = {"name": name, "status": g.Status, "time": g.Runtime, "primal": g.ObjVal if g.SolCount else None,
       "dual": g.ObjBound, "gap": g.MIPGap if g.SolCount else None}
if g.SolCount:
    xv = [v.X for v in x]; c = M.check(xv, FloatB)
    out.update(obj_eval=M.objective(xv, FloatB), max_bound_viol=c["bound"][0], max_row_viol=c["row"][0], max_int_viol=c["int"][0])
print(json.dumps(out)); json.dump(out, open(f"../{name}_gurobi.json", "w"), indent=1)
