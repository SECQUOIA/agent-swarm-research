"""Reference solves for the GDP instance catalog.

Methods:
  loa   : GDPopt LOA, nlp_solver=ipopt, mip_solver=gurobi (2 threads), 120 s;
          subproblems that keep discrete variables after fixing the disjuncts
          are MINLPs and go to GAMS/DICOPT
  baron : core.logical_to_linear + gdp.bigm, then GAMS/BARON, 120 s, 2 threads

Usage:
    uv run python gdp_catalog_solve.py --name NAME --method loa|baron   # one solve, JSON to stdout
    uv run python gdp_catalog_solve.py --all [--jobs 2]                 # all -> gdp_solve_results.json

Requires ipopt and gams on PATH. Each solve runs
in its own subprocess with a hard timeout so a stuck subsolver cannot block
the campaign; with --jobs 4 and 2 threads per solve at most 8 threads are used.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import time
import traceback

SINGLE_THREAD_ENV = {"OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"}
os.environ.update(SINGLE_THREAD_ENV)
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULT_DIR = HERE / "gdp_catalog_results" / "solve"
TIME_LIMIT = 120
THREADS = 2  # per solve; run_all uses 4 parallel solves -> 8 threads total
HARD_TIMEOUT = 600  # build + transform + solve wall clock per subprocess


def _obj_value(m):
    from pyomo.core import Objective
    from pyomo.core.expr.numvalue import value

    objs = list(m.component_data_objects(Objective, active=True, descend_into=True))
    if len(objs) != 1:
        return None, None
    o = objs[0]
    try:
        return value(o, exception=False), ("min" if o.is_minimizing() else "max")
    except Exception:
        return None, ("min" if o.is_minimizing() else "max")


def _finite(x):
    try:
        x = float(x)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def solve_loa(m):
    from pyomo.environ import SolverFactory

    t0 = time.time()
    res = SolverFactory("gdpopt.loa").solve(
        m,
        nlp_solver="ipopt",
        mip_solver="gurobi",
        mip_solver_args={"options": {"Threads": THREADS, "TimeLimit": TIME_LIMIT}},
        nlp_solver_args={"options": {"max_cpu_time": TIME_LIMIT}},
        minlp_solver="gams",
        minlp_solver_args={
            "solver": "dicopt",
            "add_options": [f"option reslim={TIME_LIMIT};", f"option threads={THREADS};"],
        },
        local_minlp_solver="gams",
        local_minlp_solver_args={
            "solver": "dicopt",
            "add_options": [f"option reslim={TIME_LIMIT};", f"option threads={THREADS};"],
        },
        time_limit=TIME_LIMIT,
        tee=False,
    )
    wall = time.time() - t0
    obj, sense = _obj_value(m)
    return {
        "termination": str(res.solver.termination_condition),
        "lower_bound": _finite(res.problem.lower_bound),
        "upper_bound": _finite(res.problem.upper_bound),
        "objective": _finite(obj),
        "sense": sense,
        "iterations": getattr(res.solver, "iterations", None),
        "wall_time": round(wall, 2),
    }


def solve_baron(m):
    from pyomo.environ import SolverFactory, TransformationFactory
    from pyomo.core import LogicalConstraint

    t0 = time.time()
    if any(True for _ in m.component_data_objects(LogicalConstraint, active=True, descend_into=True)):
        TransformationFactory("core.logical_to_linear").apply_to(m)
    transformation = "gdp.bigm"
    try:
        TransformationFactory("gdp.bigm").apply_to(m)
    except Exception as e:  # missing M values: fall back to hull and say so
        transformation = f"gdp.hull (bigm failed: {type(e).__name__}: {str(e)[:120]})"
        TransformationFactory("gdp.hull").apply_to(m)
    t_transform = time.time() - t0
    t0 = time.time()
    res = SolverFactory("gams").solve(
        m,
        solver="baron",
        tee=False,
        load_solutions=False,
        add_options=[
            f"option reslim={TIME_LIMIT};",
            "option optcr=1e-4;",
            "option optca=1e-6;",
            f"option threads={THREADS};",
        ],
    )
    wall = time.time() - t0
    obj = None
    if len(res.solution) > 0:
        try:
            m.solutions.load_from(res)
            obj, _ = _obj_value(m)
        except Exception:
            obj = None
    _, sense = _obj_value(m)
    return {
        "termination": str(res.solver.termination_condition),
        "status": str(res.solver.status),
        "lower_bound": _finite(res.problem.lower_bound),
        "upper_bound": _finite(res.problem.upper_bound),
        "objective": _finite(obj),
        "sense": sense,
        "solver_time": _finite(res.solver.user_time),
        "wall_time": round(wall, 2),
        "transform_time": round(t_transform, 2),
        "transformation": transformation,
    }


def solve_one(name, method):
    import gdp_instances

    t0 = time.time()
    m = gdp_instances.INSTANCES[name]()
    build_time = time.time() - t0
    out = solve_loa(m) if method == "loa" else solve_baron(m)
    out["build_time"] = round(build_time, 2)
    return out


def run_all(jobs, names=None):
    import gdp_instances

    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    names = names or list(gdp_instances.INSTANCES)
    tasks = [(n, meth) for n in names for meth in ("loa", "baron")]

    def work(task):
        name, method = task
        out = RESULT_DIR / f"{name}.{method}.json"
        if out.exists():
            return
        t0 = time.time()
        try:
            p = subprocess.run(
                [sys.executable, __file__, "--name", name, "--method", method],
                capture_output=True, text=True, timeout=HARD_TIMEOUT, cwd=HERE,
                env=dict(os.environ, **SINGLE_THREAD_ENV),
            )
            lines = [l for l in p.stdout.splitlines() if l.startswith("{")]
            if p.returncode == 0 and lines:
                res = json.loads(lines[-1])
            else:
                err = [l for l in p.stderr.strip().splitlines() if l.strip()]
                res = {"error": (err[-1] if err else f"rc={p.returncode}")[:300]}
        except subprocess.TimeoutExpired:
            res = {"error": f"hard timeout {HARD_TIMEOUT}s (killed)"}
        res["total_wall"] = round(time.time() - t0, 1)
        out.write_text(json.dumps(res, indent=1))
        print(f"{name} {method}: {res.get('termination', res.get('error'))} obj={res.get('objective')} "
              f"t={res.get('wall_time')}", flush=True)

    with ThreadPoolExecutor(jobs) as ex:
        list(ex.map(work, tasks))
    merged = {}
    for n in names:
        merged[n] = {}
        for meth in ("loa", "baron"):
            f = RESULT_DIR / f"{n}.{meth}.json"
            if f.exists():
                merged[n][meth] = json.loads(f.read_text())
    (HERE / "gdp_solve_results.json").write_text(json.dumps(merged, indent=1))
    print("wrote gdp_solve_results.json")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--name")
    ap.add_argument("--method", choices=["loa", "baron"])
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    if a.name:
        try:
            print(json.dumps(solve_one(a.name, a.method)))
        except Exception:
            traceback.print_exc()
            sys.exit(1)
    elif a.all:
        run_all(a.jobs, a.only)
