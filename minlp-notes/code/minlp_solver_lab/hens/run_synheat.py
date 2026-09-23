"""Run one (example, formulation, solver) job of the Task 2 comparison.
usage: uv run python run_synheat.py <example> <orig|lift|lift_cubic> <gurobi|baron> <time_s>
Writes results/synheat_<example>_<form>_<solver>.json (bounds, nodes, time, root bound, solution point).
"""
import re
import sys
from common import *
from gurobi_util import solve_gurobi, parse_baron_log
from synheat import EXAMPLES, build, point

ex, form, solver, T = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
lifted = form.startswith("lift")
m = build(EXAMPLES[ex], lifted=lifted, lift_form="cubic" if form == "lift_cubic" else "pow")
tag = f"synheat_{ex}_{form}_{solver}"
if solver == "gurobi":
    out = solve_gurobi(m, T, threads=4, logfile=RES / f"{tag}.log")
else:
    d = RES / tag
    res, t = solve_gams(m, "baron", T, threads=4, optcr=1e-4, keepfiles=True, tmpdir=str(d), tee=True)
    p, l = gams_bounds(res)
    out = {"primal": p, "dual": l, "time": t, "status": str(res.solver.termination_condition)}
    log = open(RES / f"{tag}.stdout").read() if (RES / f"{tag}.stdout").exists() else ""
    out.update(parse_baron_log(log) if log else {})
out["point"] = point(m)
out["obj"] = pe.value(m.obj)
dump(f"{tag}.json", out)
print(tag, {k: v for k, v in out.items() if k != "point"})
