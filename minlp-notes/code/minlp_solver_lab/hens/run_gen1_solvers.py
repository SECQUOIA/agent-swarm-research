"""Task 1(c): BARON, SCIP, Gurobi 13 for 300 s each on the original heatexch_gen1."""
import sys
from common import *
from gurobi_util import solve_gurobi

name = sys.argv[1] if len(sys.argv) > 1 else "heatexch_gen1"
T = float(sys.argv[2]) if len(sys.argv) > 2 else 300
out = {}
for solver in ["baron", "scip"]:
    m = load_minlplib(name)
    d = RES / f"{name}_{solver}{int(T)}"
    res, t = solve_gams(m, solver, T, threads=4, keepfiles=True, tmpdir=str(d))
    p, l = gams_bounds(res)
    out[solver] = {"primal": p, "dual": l, "time": t, "status": str(res.solver.termination_condition)}
    print(solver, out[solver], flush=True)
m = load_minlplib(name)
out["gurobi"] = solve_gurobi(m, T, threads=4, logfile=RES / f"{name}_gurobi{int(T)}.log")
print("gurobi", out["gurobi"], flush=True)
dump(f"{name}_solvers{int(T)}.json", out)
