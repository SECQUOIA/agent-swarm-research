"""Record the research environment and exercise licensed solver interfaces.

Run from the solver lab with ``uv run --frozen --no-sync python -m
lbesh_research.environment --out results/lbesh_development/environment.json``.
License files, identifiers, and credentials are deliberately not recorded.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.metadata
import io
import json
import math
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time


def probe():
    import pyomo.environ as pyo
    import gurobipy as gp

    lab = Path(__file__).resolve().parents[1]
    result = {
        "python": sys.version,
        "platform": platform.platform(),
        "cpu_count": os.cpu_count(),
        "packages": {},
        "executables": {name: shutil.which(name) for name in ("uv", "gams", "ipopt")},
        "gurobi_version": list(gp.gurobi.version()),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "uv_lock_sha256": hashlib.sha256((lab / "uv.lock").read_bytes()).hexdigest(),
        "thread_policy": "One solver thread per run; root coordinates at most six concurrent experiment workers.",
        "probes": {},
    }
    for name in ("pyomo", "gurobipy", "numpy", "scipy", "sympy", "gamsapi", "gdplib", "highspy", "pyscipopt"):
        try:
            result["packages"][name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            result["packages"][name] = None
    # Silence license banners without retaining their contents.
    with contextlib.redirect_stdout(io.StringIO()):
        try:
            with gp.Env(params={"OutputFlag": 0}) as env, gp.Model(env=env) as m:
                m.Params.Threads = 1
                x = m.addVar(lb=0, ub=3)
                m.addConstr(x >= 1)
                m.setObjective(x)
                m.optimize()
                result["probes"]["gurobipy"] = {"status": m.Status, "objective": m.ObjVal, "passed": m.Status == gp.GRB.OPTIMAL and abs(m.ObjVal - 1) < 1e-8}
        except Exception as exc:
            result["probes"]["gurobipy"] = {"passed": False, "error_type": type(exc).__name__}
    for solver in ("ipopt", "shot", "scip", "gurobi", "baron"):
        start = time.monotonic()
        m = pyo.ConcreteModel()
        m.x = pyo.Var(bounds=(0, 2), initialize=0.5)
        m.y = pyo.Var(domain=pyo.Binary, initialize=0)
        m.c = pyo.Constraint(expr=pyo.exp(m.x) <= 2)
        m.o = pyo.Objective(expr=-m.x + m.y)
        if solver == "ipopt":
            m.y.fix(0)
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                if solver == "ipopt":
                    res = pyo.SolverFactory("ipopt").solve(m, options={"max_cpu_time": 15, "tol": 1e-9})
                else:
                    res = pyo.SolverFactory("gams").solve(m, solver=solver, add_options=["option threads=1;", "option reslim=15;", "option optcr=1e-8;", "option optca=1e-8;"])
            obj = float(pyo.value(m.o))
            result["probes"][solver] = {
                "termination": str(res.solver.termination_condition),
                "objective": obj,
                "expected": -math.log(2),
                "passed": abs(obj + math.log(2)) <= 1e-6 and abs(pyo.value(m.y)) <= 1e-6 and math.exp(pyo.value(m.x)) <= 2 + 1e-6,
                "seconds": time.monotonic() - start,
            }
        except Exception as exc:
            result["probes"][solver] = {"passed": False, "error_type": type(exc).__name__, "seconds": time.monotonic() - start}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = probe()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0 if all(p["passed"] for p in result["probes"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
