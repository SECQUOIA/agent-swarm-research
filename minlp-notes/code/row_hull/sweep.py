"""Parallel sweep.  python sweep.py out.jsonl --sizes 8x12 10x15 --seeds 0 1 2 --caps uniform random uncap
       --costs quad sqrt --forms orig cuts --solvers gurobi --tl 300 --workers 8"""
import argparse, itertools, json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("out")
ap.add_argument("--sizes", nargs="+", default=["8x12"])
ap.add_argument("--seeds", nargs="+", type=int, default=[0])
ap.add_argument("--caps", nargs="+", default=["uniform", "random", "uncap"])
ap.add_argument("--costs", nargs="+", default=["quad", "sqrt"])
ap.add_argument("--forms", nargs="+", default=["orig", "cuts"])
ap.add_argument("--solvers", nargs="+", default=["gurobi"])
ap.add_argument("--tl", type=float, default=300)
ap.add_argument("--workers", type=int, default=8)
a = ap.parse_args()
here = Path(__file__).resolve().parent
done = set()
if Path(a.out).exists():
    for ln in open(a.out):
        r = json.loads(ln); done.add((r["name"], r["form"], r["solver"]))


def cell(c):
    size, seed, cap, cost, form, solver = c
    if size.startswith("g"):
        m, n = size.split("d")[0].split("n")
        name = f"netflow-{cap}-{cost}-{m[1:]}n{n}d-s{seed}"
    elif size.startswith("f"):
        m, n = size.split("x")
        name = f"transportfc-{cap}-{cost}-{m[1:]}x{n}-s{seed}"
    else:
        m, n = size.split("x")
        name = f"transport-{cap}-{cost}-{m}x{n}-s{seed}"
    if (name, form, solver) in done:
        return None
    cmd = [sys.executable, str(here / "run_one.py"), m, n, str(seed), cap, cost, form, solver, "--tl", str(a.tl)]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=a.tl + 900).stdout
        line = [ln for ln in out.splitlines() if ln.startswith("{")][-1]
    except Exception as e:  # noqa: BLE001
        line = json.dumps({"name": name, "form": form, "solver": solver, "status": f"error: {e!r}"})
    return line


cells = list(itertools.product(a.sizes, a.seeds, a.caps, a.costs, a.forms, a.solvers))
with ThreadPoolExecutor(a.workers) as ex, open(a.out, "a") as fh:
    for line in ex.map(cell, cells):
        if line:
            fh.write(line + "\n"); fh.flush()
