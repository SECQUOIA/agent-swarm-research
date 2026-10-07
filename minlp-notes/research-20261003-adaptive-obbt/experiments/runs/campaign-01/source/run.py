"""Run the frozen experiment with fresh workers and preserve every attempt.

Example (from repository root):
  OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 code/minlp_solver_lab/.venv/bin/python \
    research-20261003-adaptive-obbt/experiments/run.py --campaign campaign-01

A campaign snapshots source before executing any held-out model. It is never
overwritten. To resume a partial campaign, pass --resume; the frozen source and
already completed results remain unchanged.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import random
import shutil
import subprocess
import sys
import time
import traceback

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def strict(data):
    """JSON output contains no nonstandard NaN/Infinity tokens."""
    import math
    if isinstance(data, dict):
        return {str(k): strict(v) for k, v in data.items()}
    if isinstance(data, (list, tuple)):
        return [strict(v) for v in data]
    if isinstance(data, float) and not math.isfinite(data):
        return None
    if hasattr(data, "item"):
        return strict(data.item())
    return data


def save(path, data):
    path = Path(path)
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(strict(data), sort_keys=True, indent=2, allow_nan=False)+"\n")
    temp.replace(path)


def worker(campaign, task_index):
    started = time.perf_counter()
    source = campaign / "source"
    sys.path.insert(0, str(source))
    from models import read_problem
    from adaptive_obbt import solve_problem
    config = json.loads((campaign / "campaign.json").read_text())
    task = config["tasks"][task_index]
    result = {"task": task, "started_utc": datetime.now(timezone.utc).isoformat()}
    try:
        model_path = HERE / "frozen" / task["model"]
        if sha(model_path) != task["model_sha256"]:
            raise ValueError("Frozen model hash changed")
        problem = read_problem(model_path)
        call_start = time.perf_counter()
        outcome = solve_problem(problem, policy=task["arm"], time_limit=task["time_limit"],
                                seed=task["seed"], config=config["policy_config"], show_output=True)
        result["call_wall_seconds"] = time.perf_counter()-call_start
        result["outcome"] = outcome
        point = outcome.get("solution")
        validate_start = time.perf_counter()
        result["validation"] = None if point is None else problem.validation(point)
        result["validation_seconds"] = time.perf_counter()-validate_start
    except Exception as exc:
        result["error"] = {"type": type(exc).__name__, "message": str(exc),
                           "traceback": traceback.format_exc()}
        traceback.print_exc()
    result["worker_wall_seconds"] = time.perf_counter()-started
    save(campaign / "raw" / (task["key"] + ".json"), result)


def main():
    global HERE
    ap = argparse.ArgumentParser()
    ap.add_argument("--campaign", required=True)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--worker", type=int)
    ap.add_argument("--experiment-root", type=Path, help=argparse.SUPPRESS)
    ap.add_argument("--policy-config", help="JSON configuration; default null uses frozen solver defaults")
    args = ap.parse_args()
    if args.experiment_root is not None:
        HERE = args.experiment_root.resolve()
    if Path(args.campaign).name != args.campaign:
        raise SystemExit("Campaign must be a simple directory name")
    campaign = HERE / "runs" / args.campaign
    if args.worker is not None:
        worker(campaign, args.worker)
        return
    if campaign.exists() and not args.resume:
        raise SystemExit("Campaign exists; use --resume or a distinct name")
    if args.resume:
        config = json.loads((campaign / "campaign.json").read_text())
        for name, digest in config["source_sha256"].items():
            if sha(campaign / "source" / name) != digest:
                raise SystemExit("Campaign source changed: " + name)
        if config["manifest_sha256"] != sha(HERE / "frozen/manifest.json"):
            raise SystemExit("Frozen manifest changed")
    else:
        manifest = json.loads((HERE / "frozen/manifest.json").read_text())
        (campaign / "source").mkdir(parents=True)
        (campaign / "raw").mkdir()
        (campaign / "logs").mkdir()
        for path in (HERE.parent / "solver").glob("*.py"):
            shutil.copy2(path, campaign / "source" / path.name)
        for name in ("models.py", "run.py", "analyze.py", "PROTOCOL.md"):
            shutil.copy2(HERE / name, campaign / "source" / name)
        if not (campaign / "source/adaptive_obbt.py").is_file():
            raise SystemExit("Solver implementation is not ready")
        tasks = []
        for model in manifest["models"]:
            for seed in manifest["seeds"]:
                for arm in manifest["arms"]:
                    tasks.append({**model, "seed": seed, "arm": arm,
                                  "time_limit": manifest["time_limit_seconds"],
                                  "key": f'{model["name"]}__{arm}__{seed}'})
        random.Random(manifest["task_order_seed"]).shuffle(tasks)
        import numpy, scipy, pyscipopt
        version_model = pyscipopt.Model()
        scip_version = ".".join(str(getattr(version_model, name)()) for name in
                                ("getMajorVersion", "getMinorVersion", "getTechVersion"))
        version_model.freeProb()
        config = {"created_utc": datetime.now(timezone.utc).isoformat(),
                  "manifest_sha256": sha(HERE / "frozen/manifest.json"),
                  "source_sha256": {p.name: sha(p) for p in (campaign / "source").iterdir()},
                  "python": sys.version, "platform": platform.platform(),
                  "logical_cpu_count": os.cpu_count(),
                  "load_average_at_start": list(os.getloadavg()),
                  "numpy": numpy.__version__, "scipy": scipy.__version__,
                  "pyscipopt": pyscipopt.__version__,
                  "scip": scip_version,
                  "policy_config": json.loads(args.policy_config) if args.policy_config else None,
                  "workers": manifest["workers"], "tasks": tasks,
                  "hard_process_limit_seconds": 30,
                  "thread_environment": {k: "1" for k in
                       ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                        "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")}}
        save(campaign / "campaign.json", config)
    env = dict(os.environ, **config["thread_environment"])
    def execute(index, task):
        path = campaign / "raw" / (task["key"] + ".json")
        if path.exists() and json.loads(path.read_text()).get("process_complete"):
            return task["key"], "already complete"
        started = time.perf_counter()
        with (campaign / "logs" / (task["key"] + ".log")).open("w") as log:
            try:
                proc = subprocess.run([sys.executable, str(campaign / "source/run.py"),
                                       "--experiment-root", str(HERE),
                                       "--campaign", args.campaign, "--worker", str(index)],
                                      stdout=log, stderr=subprocess.STDOUT, env=env,
                                      timeout=config["hard_process_limit_seconds"])
                exitcode, hard_timeout = proc.returncode, False
            except subprocess.TimeoutExpired:
                exitcode, hard_timeout = None, True
        elapsed = time.perf_counter()-started
        result = json.loads(path.read_text()) if path.exists() else {"task": task}
        result.update(process_wall_seconds=elapsed, process_exitcode=exitcode,
                      hard_timeout=hard_timeout, process_complete=True)
        save(path, result)
        status = result.get("outcome", {}).get("status", "failed")
        return task["key"], f"{status}, {elapsed:.2f}s"
    started = time.perf_counter()
    with ThreadPoolExecutor(max_workers=config["workers"]) as pool:
        pending = {pool.submit(execute, i, task): task for i, task in enumerate(config["tasks"])}
        for done in as_completed(pending):
            key, status = done.result()
            print(f"{key}: {status}", flush=True)
    save(campaign / "completion.json", {"completed_utc": datetime.now(timezone.utc).isoformat(),
                                       "driver_wall_seconds": time.perf_counter()-started,
                                       "load_average_at_completion": list(os.getloadavg())})


if __name__ == "__main__":
    main()
