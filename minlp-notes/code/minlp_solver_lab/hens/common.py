"""Shared helpers for the HENS experiments (Task 1 singularity audit, Task 2 lift test)."""
import importlib.util
import json
import os
import pathlib
import time

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import pyomo.environ as pe

ROOT = pathlib.Path(__file__).resolve().parents[1]
INST = ROOT / "instances" / "hens"
RES = pathlib.Path(__file__).resolve().parent / "results"
RES.mkdir(exist_ok=True)
# Configure ipopt and gams on PATH before running these experiments.


def load_minlplib(name):
    """Load instances/hens/<name>.py (GAMS Convert Pyomo format) and return the model."""
    path = INST / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.model


def solve_gams(m, solver, reslim, threads=4, optcr=1e-4, extra=(), tee=False, keepfiles=False, tmpdir=None):
    """Solve via GAMS. Returns (results, wall_time)."""
    opts = [f"option reslim={reslim};", f"option optcr={optcr};", f"option threads={threads};", *extra]
    opt = pe.SolverFactory("gams")
    t0 = time.time()
    kw = dict(solver=solver, add_options=opts, tee=tee, keepfiles=keepfiles)
    if tmpdir is not None:
        kw["tmpdir"] = tmpdir
    res = opt.solve(m, **kw)
    return res, time.time() - t0


def gams_bounds(res):
    """Primal/dual bound from a GAMS Pyomo result object."""
    p = res.problem
    return float(p.upper_bound), float(p.lower_bound)


def dump(name, obj):
    with open(RES / name, "w") as f:
        json.dump(obj, f, indent=2, default=float)
