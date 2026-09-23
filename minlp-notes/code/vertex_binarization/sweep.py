"""Run a grid of run_one.py cells in parallel and append JSON lines to an output file."""
import argparse
import itertools
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

ap = argparse.ArgumentParser()
ap.add_argument("out"); ap.add_argument("--families", nargs="+", required=True)
ap.add_argument("--n", nargs="+", type=int, required=True); ap.add_argument("--m", nargs="+", type=int, default=[1])
ap.add_argument("--seeds", nargs="+", type=int, default=[1]); ap.add_argument("--solvers", nargs="+", default=["gurobi", "scip", "baron"])
ap.add_argument("--forms", nargs="+", default=["orig", "sob"]); ap.add_argument("--tl", type=float, default=60)
ap.add_argument("--threads", type=int, default=4); ap.add_argument("--workers", type=int, default=6)
a = ap.parse_args()

done = set()
try:
    for line in open(a.out):
        r = json.loads(line); done.add((r["cell"]))
except FileNotFoundError:
    pass

def run(cell):
    fam, n, m, seed, form, solver = cell
    key = "/".join(map(str, cell))
    if key in done:
        return
    cmd = [sys.executable, "run_one.py", fam, str(n), str(m), str(seed), form, solver,
           "--tl", str(a.tl), "--threads", str(a.threads)]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=a.tl + 300).stdout
        rec = json.loads([l for l in out.split("\n") if l.startswith("{")][-1])
    except Exception as e:  # record failures instead of hiding them
        rec = {"status": f"error:{type(e).__name__}"}
    rec.update(cell=key, family=fam, n=n, m=m, seed=seed, form=form, solver=solver, tl=a.tl)
    with open(a.out, "a") as fh:
        fh.write(json.dumps(rec) + "\n")
    print(key, rec.get("status"), rec.get("time"), flush=True)

cells = list(itertools.product(a.families, a.n, a.m, a.seeds, a.forms, a.solvers))
with ThreadPoolExecutor(a.workers) as ex:
    list(ex.map(run, cells))
