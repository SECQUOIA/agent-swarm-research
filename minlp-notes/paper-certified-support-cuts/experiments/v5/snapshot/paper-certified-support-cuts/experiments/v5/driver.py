"""Run a campaign-5 job list with at most W concurrent single-threaded worker processes.

Copied from the campaign-4 driver (v4/driver.py); only the worker path
(v5_worker.py), the slot directory (v5/.slots) and the texts differ.

    driver.py OUTPUT_DIR [--workers W]

OUTPUT_DIR is created by make_jobs.py. Each job (model, phase, seed) runs its
modes sequentially, one fresh worker process per mode, against the code copy
in OUTPUT_DIR/snapshot. The hard limit is a subprocess timeout followed by
SIGKILL of the worker's own process group. Every finished run, including
worker errors and timeouts, is written once to runs/<run_id>.json and appended
to records.jsonl. Nothing is overwritten: rerunning the driver skips runs
whose result exists, and an interrupted run is retried under a new attempt
number with its earlier log kept in attempts/.

Stop with Ctrl-C or SIGTERM (not SIGKILL): the driver then kills only its own
worker process groups, records nothing for the interrupted runs, and exits.
W is capped by jobs.json (6), and every job also holds one of six slot locks
in v5/.slots shared by all campaign-5 drivers, so concurrent campaign-5
drivers together never exceed six workers. (The campaign-4 drivers use
v4/.slots; do not run both campaigns at the same time.)
"""
from __future__ import annotations

import argparse
import fcntl
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import queue
import shutil
import signal
import socket
import subprocess
import sys
import threading
import time

from common import GLOBAL_SLOTS, HERE, THREAD_ENV, TOPIC_NAME, digest, verify_manifest, write_new

SLOT_DIR = HERE / ".slots"


def kill_group(proc):
    """SIGKILL the process group of one of this driver's own, not yet reaped, workers."""
    if proc.returncode is not None:  # reaped: its pid may belong to someone else now
        return
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


class Driver:
    def __init__(self, out, workers):
        self.out = out
        self.spec = json.loads((out / "jobs.json").read_text())
        self.workers = max(1, min(workers, self.spec["max_workers"], GLOBAL_SLOTS))
        self.stop = threading.Event()
        self.lock = threading.Lock()
        self.children = {}
        self.active = 0
        self.completed = 0
        self.session = f"{utc()}-{os.getpid()}"
        self.started = time.monotonic()
        for name in ("runs", "attempts", "tmp"):
            (out / name).mkdir(exist_ok=True)
        self.worker = out / "snapshot/paper-certified-support-cuts/experiments/v5/v5_worker.py"
        self.source = out / "snapshot" / TOPIC_NAME

    # ------------------------------------------------------------ ledger
    def append(self, record):
        line = (json.dumps(record, allow_nan=False) + "\n").encode()
        with self.lock:
            fd = os.open(self.out / "records.jsonl", os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
            try:
                view = memoryview(line)
                while view:
                    view = view[os.write(fd, view):]
            finally:
                os.close(fd)

    def reconcile(self):
        """Append finished results that a stopped driver did not reach the ledger with."""
        ledger = self.out / "records.jsonl"
        content = ledger.read_text() if ledger.exists() else ""
        if content and not content.endswith("\n"):
            raise SystemExit("records.jsonl ends in a partial line; repair it by hand before resuming")
        known = {json.loads(line)["run_id"] for line in content.splitlines() if line}
        added = 0
        for job in self.spec["jobs"]:
            for run in job["runs"]:
                path = self.out / "runs" / (run["run_id"] + ".json")
                if path.exists() and run["run_id"] not in known:
                    self.append(json.loads(path.read_text()))
                    added += 1
        return added

    def session_event(self, event, **fields):
        line = json.dumps({"event": event, "session": self.session, "pid": os.getpid(),
                           "utc": utc(), "load": list(os.getloadavg()), **fields}) + "\n"
        with self.lock, (self.out / "sessions.jsonl").open("a") as stream:
            stream.write(line)

    # ------------------------------------------------------------ running
    def acquire_slot(self):
        SLOT_DIR.mkdir(exist_ok=True)
        while not self.stop.is_set():
            for k in range(GLOBAL_SLOTS):
                handle = open(SLOT_DIR / f"slot-{k}", "a")
                try:
                    fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    return handle
                except BlockingIOError:
                    handle.close()
            time.sleep(1.0)
        return None

    def run_one(self, job, run):
        run_id = run["run_id"]
        attempt = len(list((self.out / "attempts").glob(f"{run_id}.a*.log")))
        stem = f"{run_id}.a{attempt}"
        log_path = self.out / "attempts" / (stem + ".log")
        output = self.out / "attempts" / (stem + ".worker.json")
        tmpdir = self.out / "tmp" / stem
        tmpdir.mkdir()
        command = [sys.executable, str(self.worker), "--case", str(self.out / "cases" / (job["name"] + ".json")),
                   "--source", str(self.source), "--mode", run["mode"],
                   "--time-limit", str(job["time_limit"]), "--seed", str(job["seed"]),
                   "--output", str(output)]
        if job["node_limit"] is not None:
            command += ["--node-limit", str(job["node_limit"])]
        env = {**os.environ, **THREAD_ENV, "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": str(tmpdir)}
        with self.lock:
            self.active += 1
            active_start = self.active
        load_start, started_utc, outer_start = list(os.getloadavg()), utc(), time.monotonic()
        interrupted = False
        try:
            with log_path.open("w") as logfile:
                proc = subprocess.Popen(command, stdout=logfile, stderr=subprocess.STDOUT, env=env,
                                        cwd=self.out, start_new_session=True)
                with self.lock:
                    self.children[proc.pid] = proc
                if self.stop.is_set():
                    kill_group(proc)
                try:
                    returncode = proc.wait(timeout=job["worker_timeout"])
                    status = "worker_error" if returncode else "worker_no_output"
                except subprocess.TimeoutExpired:
                    kill_group(proc)
                    returncode = proc.wait()
                    status = "process_timeout"
                finally:
                    with self.lock:
                        self.children.pop(proc.pid, None)
                interrupted = self.stop.is_set() and status != "process_timeout" and (
                    returncode < 0 or not output.exists())
        finally:
            outer = time.monotonic() - outer_start
            load_end = list(os.getloadavg())
            with self.lock:
                active_end = self.active
                self.active -= 1
            shutil.rmtree(tmpdir, ignore_errors=True)
        if interrupted:
            return None
        if output.exists():
            try:
                record = json.loads(output.read_text())
            except (ValueError, OSError) as error:
                record = {"status": "worker_output_parse_error", "cut_log_complete": False,
                          "cut_count": None, "reason": str(error),
                          "partial_output": str(output.relative_to(self.out))}
        else:
            record = {"status": status, "cut_log_complete": False, "cut_count": None,
                      "reason": "worker ended before writing result; cut count unknown"}
        if returncode:
            record["worker_status"] = status
        if "time_limit" in record:
            record["solver_time_limit"] = record["time_limit"]
        record.update({key: job[key] for key in ("job_id", "phase", "name", "suite", "seed",
                                                 "time_limit", "worker_timeout", "node_limit")})
        record.update(part=self.spec["part"], mode=run["mode"], position=run["position"], run_id=run_id,
                      attempt=attempt, started_utc=started_utc, ended_utc=utc(),
                      outer_wall_seconds=outer, returncode=returncode,
                      log=str(log_path.relative_to(self.out)), load_start=load_start, load_end=load_end,
                      active_runs_start=active_start, active_runs_end=active_end,
                      driver_workers=self.workers, driver_session=self.session)
        write_new(self.out / "runs" / (run_id + ".json"), record)
        self.append(record)
        if output.exists() and record["status"] != "worker_output_parse_error":
            output.unlink()
        return record

    def run_job(self, job):
        pending = [r for r in job["runs"] if not (self.out / "runs" / (r["run_id"] + ".json")).exists()]
        if not pending:
            return
        slot = self.acquire_slot()
        if slot is None:
            return
        try:
            for run in pending:
                if self.stop.is_set():
                    return
                record = self.run_one(job, run)
                if record is None:
                    return
                with self.lock:
                    self.completed += 1
                    print(json.dumps({"completed": self.completed, "run": run["run_id"],
                                      "status": record["status"],
                                      "cuts": len(record["cuts"]) if isinstance(record.get("cuts"), list) else None,
                                      "outer_seconds": round(record["outer_wall_seconds"], 1),
                                      "elapsed": round(time.monotonic() - self.started, 1)}), flush=True)
        finally:
            slot.close()

    def thread_main(self, jobs):
        while not self.stop.is_set():
            try:
                job = jobs.get_nowait()
            except queue.Empty:
                return
            try:
                self.run_job(job)
            except Exception as error:  # report and continue; the run stays pending
                print(json.dumps({"driver_error": repr(error), "job": job["job_id"]}), flush=True)

    def terminate(self, signum, frame):
        self.stop.set()
        with self.lock:
            children = list(self.children.values())
        for proc in children:
            kill_group(proc)

    def main(self):
        manifest = json.loads((self.out / "source-manifest.json").read_text())
        mismatches = verify_manifest(self.out / "snapshot", manifest)
        if mismatches:
            raise SystemExit("output snapshot differs from source-manifest.json: " + ", ".join(mismatches))
        reconciled = self.reconcile()
        jobs = queue.Queue()
        pending = 0
        for job in self.spec["jobs"]:
            missing = sum(not (self.out / "runs" / (r["run_id"] + ".json")).exists() for r in job["runs"])
            if missing:
                jobs.put(job)
                pending += missing
        for signum in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
            if signal.getsignal(signum) is not signal.SIG_IGN:  # keep nohup's SIGHUP immunity
                signal.signal(signum, self.terminate)
        self.session_event("start", workers=self.workers, pending_runs=pending, reconciled=reconciled,
                           source_manifest_sha256=digest(self.out / "source-manifest.json"),
                           python=sys.version, executable=sys.executable, host=socket.gethostname(),
                           platform=platform.platform(), logical_cpus=os.cpu_count(),
                           thread_environment=THREAD_ENV,
                           packages={p: importlib.metadata.version(p) for p in
                                     ("numpy", "scipy", "sympy", "python-flint", "pyscipopt", "gurobipy")})
        print(json.dumps({"output": str(self.out), "workers": self.workers, "pending_runs": pending}), flush=True)
        threads = [threading.Thread(target=self.thread_main, args=(jobs,), daemon=True)
                   for _ in range(self.workers)]
        for thread in threads:
            thread.start()
        while any(thread.is_alive() for thread in threads):
            for thread in threads:
                thread.join(timeout=0.5)
        records = [json.loads(line) for line in (self.out / "records.jsonl").read_text().splitlines()
                   if line] if (self.out / "records.jsonl").exists() else []
        counts = {}
        for record in records:
            counts[record["status"]] = counts.get(record["status"], 0) + 1
        scheduled = sum(len(j["runs"]) for j in self.spec["jobs"])
        self.session_event("stop" if self.stop.is_set() else "end", completed_this_session=self.completed,
                           recorded=len(records), scheduled=scheduled, status_counts=counts,
                           wall_seconds=time.monotonic() - self.started)
        print(json.dumps({"recorded": len(records), "scheduled": scheduled, "statuses": counts,
                          "stopped": self.stop.is_set()}), flush=True)
        return 130 if self.stop.is_set() else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("output", type=Path)
    parser.add_argument("--workers", type=int, default=GLOBAL_SLOTS)
    args = parser.parse_args()
    out = args.output.resolve()
    if not (out / "jobs.json").is_file():
        raise SystemExit(f"{out} has no jobs.json; create it with make_jobs.py")
    lock = open(out / "driver.lock", "a")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit(f"another driver is running on {out}")
    raise SystemExit(Driver(out, args.workers).main())


if __name__ == "__main__":
    main()
