"""SCIP 10 baseline on a MINLPLib OSIL instance: default settings, time limit.
Usage: python run_scip_baseline.py NAME TIMELIMIT
Writes logs/scip_NAME.log (SCIP output) and appends a JSON line to logs/scip_baseline.jsonl."""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../..'))
import json, sys, time
from pyscipopt import Model
name, tl = sys.argv[1], float(sys.argv[2])
m = Model()
m.setLogfile(f"logs/scip_{name}.log")
m.readProblem(_repro_os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil"))
m.setParam("limits/time", tl)
m.setParam("parallel/maxnthreads", 1)
t0 = time.time(); m.optimize(); wall = time.time() - t0
rec = dict(name=name, tl=tl, status=m.getStatus(), primal=m.getPrimalbound(), dual=m.getDualbound(),
           gap=m.getGap(), nodes=m.getNNodes(), time=m.getSolvingTime(), wall=wall, version=m.version())
print(rec)
with open("logs/scip_baseline.jsonl", "a") as f: f.write(json.dumps(rec) + "\n")
