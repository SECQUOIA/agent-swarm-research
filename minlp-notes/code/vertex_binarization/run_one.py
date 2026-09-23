"""Solve one (family, n, m, seed, formulation, solver) cell and print a JSON record."""
import argparse
import json

from sob.backends import SOLVERS
from sob.instances import FAMILIES
from sob.model import binarized_ir, original_ir

ap = argparse.ArgumentParser()
ap.add_argument("family"); ap.add_argument("n", type=int); ap.add_argument("m", type=int)
ap.add_argument("seed", type=int); ap.add_argument("form", choices=["orig", "sob"])
ap.add_argument("solver", choices=list(SOLVERS)); ap.add_argument("--tl", type=float, default=60)
ap.add_argument("--threads", type=int, default=4); ap.add_argument("--log", action="store_true")
a = ap.parse_args()
p = FAMILIES[a.family](a.n, a.m, a.seed)
ir = original_ir(p) if a.form == "orig" else binarized_ir(p)
r = SOLVERS[a.solver](ir, a.tl, threads=a.threads, log=a.log)
x = r.pop("x")
if x:  # recompute the true objective at the returned x
    r["true_obj"] = sum(f(x[f"x{i}"]) for i, f in enumerate(p.funcs))
r.update(instance=p.name, form=a.form, solver=a.solver, nvars=len(ir.vars),
         nbin=sum(t != "C" for _, _, t in ir.vars.values()), budget=p.concave_rank())
print(json.dumps(r))
