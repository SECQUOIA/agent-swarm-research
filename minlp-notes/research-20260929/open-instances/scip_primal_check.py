"""Run SCIP briefly on an instance, save its best solution, and evaluate its exact violation."""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../..'))
import sys, json
from pyscipopt import Model
from osil_eval import check, load
name, tl = sys.argv[1], float(sys.argv[2])
m = Model(); m.hideOutput()
m.readProblem(_repro_os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil"))
m.setParam("limits/time", tl); m.setParam("parallel/maxnthreads", 1)
m.optimize()
sol = m.getBestSol(); I = load(name)
vars_ = {v.name: v for v in m.getVars()}
x = [m.getSolVal(sol, vars_[nm]) if nm in vars_ else 0.0 for nm in I["names"]]
c = check(name, x, I)
rec = dict(name=name, tl=tl, scip_primal=m.getPrimalbound(), scip_dual=m.getDualbound(), obj_recomputed=c["obj"],
           cons_viol=c["cons_viol"], worst_row=c["worst_row"], bound_viol=c["bound_viol"])
print(json.dumps(rec))
with open("logs/scip_primal_check.jsonl", "a") as f: f.write(json.dumps(rec) + "\n")
