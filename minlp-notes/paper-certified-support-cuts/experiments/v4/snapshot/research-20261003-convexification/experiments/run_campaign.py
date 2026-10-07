"""One-worker, bounded experiment orchestration; preserves every failure."""
from __future__ import annotations

import argparse
import csv
from dataclasses import asdict
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import shutil
import signal
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
TOPIC = HERE.parent
REPO = TOPIC.parent
sys.path.insert(0, str(HERE))
from cases import synthetic_cases

THREAD_ENV = {k: "1" for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS",
                              "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS",
                              "BLIS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")}
MODES = ("baseline", "all", "auto")
ROOT_SYNTHETIC = ("quartic_balance_8", "exp_pair", "simplex_quadratic_vector",
                  "overlapping_products", "star_marginal_inconsistency")
DIAGNOSTICS = ("genpooling_lee2", "syn15m", "cvxnonsep_psig30r", "cvxnonsep_pcon40r",
               "syn10hfsg", "btest14", "ghg_2veh", "chp_partload",
               "kall_circles_c6b", "waterno2_06")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_json(value):
    if isinstance(value, float):
        return {"binary64": value.hex()}
    if isinstance(value, (tuple, list)):
        return [exact_json(x) for x in value]
    if isinstance(value, dict):
        return {str(k): exact_json(v) for k, v in value.items()}
    return value


def write_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")
    temporary.replace(path)


def capture_snapshot(out):
    snapshot = out / "snapshot"
    paths = []
    dependency = REPO / "research-20261002-convexification"
    for directory in (TOPIC / "solver", TOPIC / "theory", TOPIC / "reviews",
                      dependency / "solver", dependency / "theory",
                      REPO / "code/univariate_envelopes/uenv"):
        if directory.exists():
            paths.extend(p for p in directory.rglob("*") if p.suffix in (".py", ".c"))
    paths.extend(p for p in HERE.iterdir() if p.suffix in (".py", ".md") and p.is_file())
    paths.append(HERE / "holdout-selection.json")
    paths.extend(p for p in (TOPIC / "requirements.txt", dependency / "requirements.txt") if p.exists())
    paths.append(REPO / "code/minlp_solver_lab/instances/instancedata.csv")
    hashes = {}
    for source in sorted(set(paths)):
        relative = source.relative_to(REPO)
        target = snapshot / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        hashes[str(relative)] = digest(target)
    for source in (out / "cases").glob("*.json"):
        relative = Path("frozen-cases") / source.name
        target = snapshot / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        hashes[str(relative)] = digest(target)
        descriptor = json.loads(source.read_text())
        if "path" in descriptor:
            original = Path(descriptor["path"])
            relative = Path("original-osil") / (descriptor["name"] + ".osil")
            target = snapshot / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(original, target)
            hashes[str(relative)] = digest(target)
    write_json(out / "source-manifest.json", hashes)
    return snapshot


def make_jobs(out):
    holdout = json.loads((HERE / "holdout-selection.json").read_text())["selected"]
    with (REPO / "code/minlp_solver_lab/instances/instancedata.csv").open() as stream:
        metadata = {r["name"]: r for r in csv.DictReader(stream, delimiter=";")}
    cases = []
    for entry in synthetic_cases():
        model = entry.pop("instance")
        cases.append({"name": model.name, "suite": "synthetic", **entry,
                      "model": exact_json(asdict(model))})
    for suite, names in (("holdout", [r["name"] for r in holdout]), ("diagnostic", DIAGNOSTICS)):
        for name in names:
            source = Path.home() / ".cache/minlplib/minlplib/osil" / f"{name}.osil"
            entry = next((r for r in holdout if r["name"] == name), {})
            actual_hash = digest(source)
            if entry.get("sha256", actual_hash) != actual_hash:
                raise ValueError(f"held-out OSiL changed after selection freeze: {name}")
            cases.append({"name": name, "suite": suite, "path": str(source),
                          "source_sha256": actual_hash,
                          "reference_primal": entry.get("reference_primal", metadata.get(name, {}).get("primalbound")),
                          "reference_dual": entry.get("reference_dual", metadata.get(name, {}).get("dualbound"))})
    (out / "cases").mkdir()
    for case in cases:
        write_json(out / "cases" / (case["name"] + ".json"), case)
    jobs = []
    # Each phase uses the declared case order, independent of observed results.
    by_name = {case["name"]: case for case in cases}
    phases = (
        ("full", [r["name"] for r in holdout], 30.0, 45.0),
        ("full", list(DIAGNOSTICS), 30.0, 45.0),
        ("full", [c["name"] for c in cases if c["suite"] == "synthetic"], 10.0, 20.0),
        ("root", [r["name"] for r in holdout] + list(ROOT_SYNTHETIC), 5.0, 15.0),
        ("repeat", [r["name"] for r in holdout[:6]], 30.0, 45.0),
    )
    for phase, names, time_limit, timeout in phases:
        for i, name in enumerate(names):
            case = by_name[name]
            modes = MODES[i % len(MODES):] + MODES[:i % len(MODES)]
            for mode in modes:
                jobs.append({"name": name, "suite": case["suite"], "mode": mode, "phase": phase,
                             "time_limit": time_limit, "worker_timeout": timeout,
                             "node_limit": 1 if phase == "root" else None,
                             "seed": 1 if phase == "repeat" else 0})
    write_json(out / "jobs.json", jobs)
    return jobs


def run(args):
    def stop(signum, frame):
        raise SystemExit(128 + signum)

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGHUP, stop)
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    jobs = make_jobs(out)
    snapshot = capture_snapshot(out)
    environment = {"python": sys.version, "executable": sys.executable,
                   "platform": platform.platform(), "logical_cpus": os.cpu_count(),
                   "load_start": list(os.getloadavg()), "thread_environment": THREAD_ENV,
                   "packages": {p: importlib.metadata.version(p) for p in
                                ("numpy", "scipy", "sympy", "python-flint", "pyscipopt")},
                   "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   "wall_cap": args.wall_cap, "worker_timeout": "phase-specific in jobs.json"}
    write_json(out / "environment.json", environment)
    (out / "runs").mkdir()
    worker = snapshot / Path(__file__).relative_to(REPO).parent / "worker.py"
    topic_snapshot = snapshot / TOPIC.name
    start = time.monotonic()
    counts = {}
    with (out / "records.jsonl").open("a", buffering=1) as stream:
        for index, job in enumerate(jobs):
            ident = f"{index:03d}_{job['name']}__{job['mode']}__{job['phase']}"
            path = out / "runs" / (ident + ".json")
            log_path = out / "runs" / (ident + ".log")
            left = args.wall_cap - (time.monotonic() - start)
            if left <= 0:
                record = {**job, "run_id": ident, "status": "campaign_budget_exhausted",
                          "cut_log_complete": False, "cut_count": None}
            else:
                command = [sys.executable, str(worker), "--case", str(out / "cases" / (job["name"] + ".json")),
                           "--source", str(topic_snapshot), "--mode", job["mode"],
                           "--time-limit", str(job["time_limit"]), "--seed", str(job["seed"]),
                           "--output", str(path)]
                if job["node_limit"] is not None:
                    command += ["--node-limit", str(job["node_limit"])]
                outer_start = time.monotonic()
                with log_path.open("w") as logfile:
                    proc = subprocess.Popen(command, stdout=logfile, stderr=subprocess.STDOUT,
                                            env={**os.environ, **THREAD_ENV}, start_new_session=True)
                    try:
                        returncode = proc.wait(timeout=max(0.01, min(job["worker_timeout"], left)))
                        status = "worker_error" if returncode else "worker_no_output"
                    except subprocess.TimeoutExpired:
                        os.killpg(proc.pid, signal.SIGKILL)
                        returncode = proc.wait()
                        status = "process_timeout"
                    except BaseException:
                        if proc.poll() is None:
                            os.killpg(proc.pid, signal.SIGKILL)
                            proc.wait()
                        raise
                if path.exists():
                    try:
                        record = json.loads(path.read_text())
                    except (ValueError, OSError) as error:
                        damaged = path.with_suffix(".partial-json")
                        path.replace(damaged)
                        record = {"status": "worker_output_parse_error", "cut_log_complete": False,
                                  "cut_count": None, "reason": str(error), "partial_output": damaged.name}
                else:
                    record = {"status": status, "cut_log_complete": False,
                              "cut_count": None, "reason": "worker ended before writing result; cut count unknown"}
                if returncode:
                    record["worker_status"] = status
                record.update(job, run_id=ident, outer_wall_seconds=time.monotonic() - outer_start,
                              returncode=returncode, log=str(log_path.relative_to(out)))
            write_json(path, record)
            stream.write(json.dumps(record, allow_nan=False) + "\n")
            counts[record["status"]] = counts.get(record["status"], 0) + 1
            print(json.dumps({"completed": index + 1, "scheduled": len(jobs), "run": ident,
                              "status": record["status"], "cuts": len(record["cuts"]) if "cuts" in record else None,
                              "elapsed": round(time.monotonic() - start, 1)}), flush=True)
    write_json(out / "completion.json", {"counts": counts, "wall_seconds": time.monotonic() - start,
                                        "load_end": list(os.getloadavg()), "scheduled": len(jobs)})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--wall-cap", type=float, default=9000)
    run(parser.parse_args())
