"""Run a separately frozen, matched discovery-correctness supplement."""
from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import signal
import subprocess
import sys
import time

from run_campaign import (HERE, REPO, TOPIC, THREAD_ENV, capture_snapshot,
                          digest, write_json)


def run(args):
    def stop(signum, frame):
        raise SystemExit(128 + signum)

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGHUP, stop)
    previous = args.original.resolve()
    if not (previous / "completion.json").exists():
        raise ValueError("the frozen primary campaign must finish before this sequential supplement")
    plan = json.loads(args.plan.read_text())
    if digest(previous / "records.jsonl") != plan["original_records_sha256"]:
        raise ValueError("the original campaign changed after repair-plan freeze")
    if digest(previous / "source-manifest.json") != plan["original_source_manifest_sha256"]:
        raise ValueError("the original implementation manifest changed")
    jobs = plan["jobs"]
    names = list(dict.fromkeys(job["name"] for job in jobs))
    cases = {}
    for name in names:
        case = json.loads((previous / "cases" / (name + ".json")).read_text())
        if "path" in case:
            original = previous / "snapshot/original-osil" / (name + ".osil")
            if digest(original) != case["source_sha256"]:
                raise ValueError("original archived model hash changed")
            case["path"] = str(original)
        cases[name] = case
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    (out / "cases").mkdir()
    (out / "runs").mkdir()
    for name, case in cases.items():
        write_json(out / "cases" / (name + ".json"), case)
    write_json(out / "jobs.json", jobs)
    write_json(out / "amendment.json", {
        **plan, "original_campaign": str(previous),
        "policy": "Correct sparse expression handling and enforce the existing discovery time budget between units of work. Same model, configuration, phase budgets and seeds; all matched modes included. Original outcomes and unknown cut logs remain in primary results."})
    snapshot = capture_snapshot(out)
    frozen_plan = snapshot / TOPIC.name / "experiments/repair-plan.json"
    frozen_plan.write_bytes(args.plan.read_bytes())
    manifest = json.loads((out / "source-manifest.json").read_text())
    manifest[str(frozen_plan.relative_to(snapshot))] = digest(frozen_plan)
    write_json(out / "source-manifest.json", manifest)
    write_json(out / "environment.json", {
        "python": sys.version, "executable": sys.executable, "platform": platform.platform(),
        "logical_cpus": os.cpu_count(), "load_start": list(os.getloadavg()),
        "thread_environment": THREAD_ENV,
        "packages": {p: importlib.metadata.version(p) for p in
                     ("numpy", "scipy", "sympy", "python-flint", "pyscipopt")},
        "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    worker = snapshot / TOPIC.name / "experiments/worker.py"
    started = time.monotonic()
    with (out / "records.jsonl").open("w", buffering=1) as stream:
        for index, job in enumerate(jobs):
            ident = f"{index:03d}_{job['name']}__{job['mode']}__{job['phase']}"
            output = out / "runs" / (ident + ".json")
            logfile = out / "runs" / (ident + ".log")
            command = [sys.executable, str(worker), "--case", str(out / "cases" / (job["name"] + ".json")),
                       "--source", str(snapshot / TOPIC.name), "--mode", job["mode"],
                       "--time-limit", str(job["time_limit"]), "--seed", str(job["seed"]), "--output", str(output)]
            if job["node_limit"] is not None:
                command += ["--node-limit", str(job["node_limit"])]
            before = time.monotonic()
            with logfile.open("w") as log:
                process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT,
                                           env={**os.environ, **THREAD_ENV}, start_new_session=True)
                try:
                    returncode = process.wait(timeout=job["worker_timeout"])
                    status = "worker_error" if returncode else "worker_no_output"
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    returncode = process.wait()
                    status = "process_timeout"
                except BaseException:
                    if process.poll() is None:
                        os.killpg(process.pid, signal.SIGKILL)
                        process.wait()
                    raise
            if output.exists():
                try:
                    record = json.loads(output.read_text())
                except (ValueError, OSError) as error:
                    damaged = output.with_suffix(".partial-json")
                    output.replace(damaged)
                    record = {"status": "worker_output_parse_error", "cut_log_complete": False,
                              "cut_count": None, "reason": str(error), "partial_output": damaged.name}
            else:
                record = {"status": status, "cut_log_complete": False, "cut_count": None,
                          "reason": "worker ended without complete output; cut count unknown"}
            if returncode:
                record["worker_status"] = status
            record.update(job, run_id=ident, returncode=returncode,
                          outer_wall_seconds=time.monotonic() - before,
                          log=str(logfile.relative_to(out)))
            write_json(output, record)
            stream.write(json.dumps(record, allow_nan=False) + "\n")
            print(json.dumps({"completed": index + 1, "run": ident,
                              "status": record["status"]}), flush=True)
    write_json(out / "completion.json", {"scheduled": len(jobs), "completed": len(jobs),
                                         "wall_seconds": time.monotonic() - started,
                                         "load_end": list(os.getloadavg())})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--original", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--plan", type=Path, required=True)
    run(parser.parse_args())
