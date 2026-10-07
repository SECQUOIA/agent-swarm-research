"""Check stored EG evidence and a small leaf subset in a disposable relocated copy."""
import hashlib
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time

from eg_evidence import TRACK, REVIEW, CERTIFIER
from finish_paths import ROOT, RESEARCH, OUT

LOGS = OUT / "logs/integration-r1-eg"
RESULTS = OUT / "logs/integration-r1-eg-smoke.json"
CHECKS = [
    ("summary", TRACK, ["summarize.py"],
     ["TOTAL: 1114361 leaves, 0 failures", "RESULT: every leaf of every part certified"]),
    ("chunk-subset", TRACK,
     ["recheck_leaves.py", "rec/rec_disc2_p7.npz", "eg_disc2_s", "5.642100574331458",
      "0", "1024", "smoke-subset.npz"],
     ["coverage: generated == popped multiset: True", "bad reduced boxes 0",
      "certified 29/29; failures 0"]),
    ("unchanged-certifier", REVIEW, ["indep_repro.py", "8"],
     ["total 64 leaves, not reproduced 0;", "differing from recorded 0;"]),
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_saved_results(results_path=RESULTS):
    results_path = Path(results_path)
    results = json.loads(results_path.read_text())
    assert [c["id"] for c in results["checks"]] == [c[0] for c in CHECKS]
    for record, (_, _, _, expected) in zip(results["checks"], CHECKS):
        assert record["exit"] == 0 and record["successful_main_tree_opens"] == 0
        output = results_path.parent / record["output"] if results.get("relative_to_results") else OUT / record["output"]
        trace = results_path.parent / record["trace"] if results.get("relative_to_results") else OUT / record["trace"]
        assert digest(output) == record["output_sha256"]
        assert digest(trace) == record["trace_sha256"]
        assert all(s in output.read_text() for s in expected), record["id"]
        assert not successful_source_opens(trace.read_text()), record["id"]
    subset = results_path.parent / results["subset"]["path"] if results.get("relative_to_results") else OUT / results["subset"]["path"]
    assert digest(subset) == results["subset"]["sha256"]
    import numpy as np
    with np.load(subset) as z:
        assert len(z["sel"]) == 29 and np.all(z["ok"]) and np.all(z["mg"] > 0)
        assert bool(z["cov_ok"]) and int(z["nbad_red"]) == 0
        assert int(z["n_proc"]) == 36521 and int(z["n_leaves"]) == 29093
    return len(results["checks"])


def successful_source_opens(trace):
    return [line for line in trace.splitlines()
            if any(str(p) in line for p in (ROOT, ROOT.with_name("minlp-notes-clean")))
            and re.search(r"= [0-9]+(?:<|$)", line)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path,
                        help="A new output directory; default: a fresh disposable directory in /tmp")
    args = parser.parse_args()
    for command in ("bwrap", "strace"):
        if shutil.which(command) is None:
            parser.error(f"Required command is missing from PATH: {command}")
    logs = args.output_dir.resolve() if args.output_dir else Path(tempfile.mkdtemp(prefix="repro-eg-smoke-output-"))
    if args.output_dir:
        logs.mkdir(parents=True, exist_ok=False)
    results_path = logs / "results.json"
    os.sched_setaffinity(0, sorted(os.sched_getaffinity(0))[:4])
    # All scientific execution uses this copy; it is removed even on failure.
    with tempfile.TemporaryDirectory(prefix="repro-eg-smoke-tree-") as temp:
        run_checks(Path(temp), logs, results_path)
    print(f"PASS: {validate_saved_results(results_path)} relocated EG checks; full recheck not run; outputs: {logs}")


def run_checks(tree, logs, results_path):
    # Copy bytes, never symlink back to the source checkout.
    for scope in (TRACK, REVIEW, CERTIFIER):
        shutil.copytree(RESEARCH / scope, tree / "research-20260929" / scope,
                        ignore=shutil.ignore_patterns("__pycache__"))
    cache = Path("~/.cache/minlplib/minlplib/osil").expanduser()
    isolated = tree / "osil-cache"
    isolated.mkdir()
    model = "eg_disc2_s.osil"
    shutil.copy2(cache / model, isolated / model)
    pin = next(r for r in json.loads((OUT / "inputs/osil-models.json").read_text())
               if r["name"] == "eg_disc2_s")
    assert digest(isolated / model) == pin["sha256"], "OSIL pin mismatch"
    sandbox = ["bwrap", "--dev-bind", "/", "/", "--tmpfs", str(ROOT)]
    old = ROOT.with_name("minlp-notes-clean")
    if old.exists():
        sandbox += ["--tmpfs", str(old)]
    sandbox += ["--tmpfs", str(cache.parent), "--ro-bind", str(isolated), str(cache)]
    for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"):
        sandbox += ["--setenv", key, "1"]
    sandbox += ["--setenv", "PYTHONDONTWRITEBYTECODE", "1"]
    results = dict(tree=str(tree), cpus=sorted(os.sched_getaffinity(0)), checks=[], relative_to_results=True)
    for name, cwd, args, expected in CHECKS:
        local_trace = tree / (name + ".strace")
        argv = sandbox + ["--chdir", str(tree / "research-20260929" / cwd), "--",
                          "strace", "-f", "-yy", "-e", "trace=openat,open", "-o", str(local_trace),
                          "timeout", "180", sys.executable, "-B", "-u"] + args
        start = time.monotonic()
        run = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        output = logs / (name + ".log")
        trace = logs / (name + ".strace")
        output.write_text(run.stdout)
        shutil.copy2(local_trace, trace)
        record = dict(id=name, argv=argv, exit=run.returncode,
                      wall_s=round(time.monotonic() - start, 2),
                      output=output.name, output_sha256=digest(output),
                      trace=trace.name, trace_sha256=digest(trace),
                      successful_main_tree_opens=len(successful_source_opens(trace.read_text())))
        results["checks"].append(record)
        results_path.write_text(json.dumps(results, indent=2) + "\n")
        print(json.dumps({k: record[k] for k in ("id", "exit", "wall_s", "successful_main_tree_opens")}), flush=True)
        assert run.returncode == 0 and all(s in run.stdout for s in expected), run.stdout
        assert record["successful_main_tree_opens"] == 0
    subset = logs / "smoke-subset.npz"
    shutil.copy2(tree / "research-20260929" / TRACK / "smoke-subset.npz", subset)
    results["subset"] = dict(path=subset.name, sha256=digest(subset))
    results_path.write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
