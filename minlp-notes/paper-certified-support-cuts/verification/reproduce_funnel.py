#!/usr/bin/env python3
"""Rerun archived cut-mode runs to classify failed support calls and stored-row rejections.

Needs PySCIPOpt (the minlp_solver_lab venv). Each target run executes in a
fresh, single-threaded process from a scratch copy of its own snapshot under
/tmp/funnel-repro (the archived directories are not written). The callback is
unchanged. Two functions are wrapped to observe it:

- solver.support.certify_support: status, method and reason of every call
  that returned no cut;
- solver.integration._audit_inserted_row: when the audit rejects a row, why
  SCIP's stored row differs from the certified row.

Targets: every cut-mode run whose record has certification_failures > 0 or
row_binding_rejections > 0 (record sets of analyze_funnel.py). Root runs are
rerun as recorded. Full and repeat runs are rerun with node limit 1 and their
own seed, Config and solver time limit, because the separator runs only at
depth 0. analyze_funnel.py compares the rerun counters with the archive.

    $PY reproduce_funnel.py [--jobs 3] [--out funnel_repro.jsonl] [--only SUBSTRING]
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import threading
import time

HERE = Path(__file__).resolve().parent
SCRATCH = Path("/tmp/funnel-repro")
THREAD_ENV = {k: "1" for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                               "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")}
COUNTERS = ("calls", "certification_calls", "certification_failures", "row_binding_rejections",
            "row_rounding_rejections", "cuts")
ACTIVE = ("COLUMN", "LOOSE")
CLASSIFIER = 4  # version of classify(); rows from other versions are rerun


def reason_class(status, reason):
    reason = reason or ""
    if status == "empty":
        return "empty domain"
    if status == "unsupported":
        return "unsupported expression"
    if reason.startswith("requested separation target"):
        return "target not certified"
    if reason.startswith("cell budget"):
        return "cell budget"
    if reason.startswith("depth budget"):
        return "depth budget or unresolved domain/target"
    return "other: " + reason[:60]


def classify(model, row, variables, coefficients, rhs):
    """Why the stored row differs from the certified row (mirrors _audit_inserted_row)."""
    removed, expected, alias = [], {}, False
    for variable, coefficient in zip(variables, coefficients):
        if not coefficient:
            continue
        transformed = model.getTransformedVar(variable)
        status = transformed.getStatus()
        if status not in ACTIVE:
            removed.append([variable.name, status])
        alias |= transformed.name in expected
        expected[transformed.name] = expected.get(transformed.name, Q(0)) + Q(float(coefficient))
    expected = {k: v for k, v in expected.items() if v}
    actual = {c.getVar().name: Q(float(v)) for c, v in zip(row.getCols(), row.getVals()) if v}
    lhs, upper, constant = float(row.getLhs()), float(row.getRhs()), float(row.getConstant())
    changed = [[n, float(expected.get(n, 0)), float(actual.get(n, 0))]
               for n in sorted(set(expected) | set(actual)) if expected.get(n) != actual.get(n)]
    epsilon = model.epsilon()
    dropped = [c for c in changed if c[2] == 0 and abs(c[1]) <= epsilon]
    rounded = [c for c in changed if c[1] and c[2] and c[2] == round(c[1]) and abs(c[1] - c[2]) <= epsilon]
    if alias:
        cause = "other: two source variables share one column"
    elif removed:
        cause = "presolve: " + "+".join(sorted({s for _, s in removed}))
    elif changed and len(dropped) + len(rounded) < len(changed):
        cause = "SCIP: coefficient changed (other)"
    elif dropped and rounded:
        cause = "SCIP: coefficient below epsilon dropped and coefficient rounded to integer"
    elif dropped:
        cause = "SCIP: coefficient below epsilon dropped"
    elif rounded:
        cause = "SCIP: coefficient rounded to integer"
    elif Q(lhs) - Q(constant) != Q(float(rhs)):
        cause = "other: left side differs"
    elif not upper >= model.infinity() or row.isLocal():
        cause = "other: finite right side or local row"
    else:
        cause = "other: infinite left side"
    return {"cause": cause, "detail": {"removed": removed[:8], "changed": changed[:8],
                                       "constant": constant, "lhs": lhs, "certified_rhs": float(rhs)}}


def child(spec):
    sys.dont_write_bytecode = True
    source = Path(spec["source"])
    sys.path[:0] = [str(source), str(source / "experiments")]
    from worker import load_model
    import solver.integration as integ
    import solver.support as support
    for module in (integ, support):
        if not Path(module.__file__).resolve().is_relative_to(source):
            raise RuntimeError(f"{module.__name__} imported from outside the snapshot copy")
    failed_calls, rejections = [], []
    original_support, original_audit = support.certify_support, integ._audit_inserted_row

    def certify(*args, **kwargs):
        result = original_support(*args, **kwargs)
        if result.cut is None:
            reason = result.stats.get("reason")
            failed_calls.append({"status": result.status, "method": result.stats.get("method"),
                                 "reason": reason, "reason_class": reason_class(result.status, reason),
                                 "polytope_skipped": "polytope_skipped" in result.stats})
        return result

    def audit(model, row, variables, coefficients, rhs):
        result = original_audit(model, row, variables, coefficients, rhs)
        if result is None:
            rejections.append(classify(model, row, variables, coefficients, rhs))
        return result

    support.certify_support, integ._audit_inserted_row = certify, audit
    case = json.loads(Path(spec["case"]).read_text())
    if "path" in case:
        case = {**case, "path": str(source.parent / "original-osil" / (case["name"] + ".osil"))}
    result = integ.run_instance(load_model(case), spec["solver_mode"], time_limit=spec["time_limit"],
                                seed=spec["seed"], node_limit=spec["node_limit"],
                                config=integ.Config(**spec["config"]))
    sep = result["separation"]
    if len(rejections) != sep["row_binding_rejections"] or len(failed_calls) != sep["certification_failures"]:
        raise RuntimeError("wrapper counts disagree with the callback counters")
    return {"classifier": CLASSIFIER, "separation": {k: sep[k] for k in COUNTERS}, "status": result["status"],
            "nodes": result["nodes"], "failed_calls": failed_calls, "rejections": rejections}


def scratch_copy(directory):
    target = SCRATCH / directory.name
    if not target.exists():
        tmp = SCRATCH / (directory.name + ".partial")
        shutil.rmtree(tmp, ignore_errors=True)
        shutil.copytree(directory / "snapshot", tmp / "snapshot", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(directory / "cases", tmp / "cases")
        tmp.rename(target)
    name = "snapshot/research-20261003-convexification/solver/integration.py"
    if hashlib.sha256((target / name).read_bytes()).digest() != hashlib.sha256((directory / name).read_bytes()).digest():
        raise RuntimeError(f"scratch copy differs from {directory}")
    return target


def targets(only):
    sys.path.insert(0, str(HERE))
    from analyze_funnel import load_records
    out = []
    for r in load_records():
        s = r.get("separation")
        if r["mode"] == "baseline" or not s or not (s["certification_failures"] or s["row_binding_rejections"]):
            continue
        if only and only not in r["_key"]:
            continue
        limit = r.get("solver_time_limit", r["time_limit"] - r.get("preparation_seconds", 0.0))
        out.append({"key": r["_key"], "dir": r["_dir"], "name": r["name"], "solver_mode": r.get("solver_mode", r["mode"]),
                    "config": r["config"], "seed": r["seed"], "time_limit": limit,
                    "node_limit": 1 if r["phase"] in ("full", "repeat") else r["node_limit"]})
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", type=int, default=3)
    parser.add_argument("--out", type=Path, default=HERE / "funnel_repro.jsonl")
    parser.add_argument("--only", default="")
    parser.add_argument("--child", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.child:
        print(json.dumps(child(json.loads(args.child.read_text()))))
        return
    done = set()
    if args.out.is_file():
        rows = [json.loads(line) for line in args.out.read_text().splitlines() if line.strip()]
        stale = [r for r in rows if r.get("classifier") != CLASSIFIER]
        if stale:
            print(f"dropping {len(stale)} rows from another classifier version", flush=True)
            kept = [r for r in rows if r.get("classifier") == CLASSIFIER]
            args.out.write_text("".join(json.dumps(r) + "\n" for r in kept))
            rows = kept
        done = {r["key"] for r in rows}
    todo = [t for t in targets(args.only) if t["key"] not in done]
    print(f"{len(todo)} runs to rerun ({len(done)} already done)", flush=True)
    SCRATCH.mkdir(exist_ok=True)
    copies = {d: scratch_copy(Path(d)) for d in sorted({t["dir"] for t in todo})}
    lock = threading.Lock()
    env = {**os.environ, **THREAD_ENV, "PYTHONDONTWRITEBYTECODE": "1"}

    def run(t):
        copy = copies[t["dir"]]
        spec = {**t, "source": str(copy / "snapshot/research-20261003-convexification"),
                "case": str(copy / "cases" / (t["name"] + ".json"))}
        spec_path = SCRATCH / ("spec-" + hashlib.sha256(t["key"].encode()).hexdigest()[:16] + ".json")
        spec_path.write_text(json.dumps(spec))
        started = time.perf_counter()
        try:
            proc = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--child", str(spec_path)],
                                  capture_output=True, text=True, timeout=900, env=env, cwd=str(SCRATCH))
            if proc.returncode:
                out = {"error": proc.stderr[-2000:]}
            else:
                out = json.loads(proc.stdout.strip().splitlines()[-1])
        except subprocess.TimeoutExpired:
            out = {"error": "timeout 900 s"}
        finally:
            spec_path.unlink(missing_ok=True)
        out.update(key=t["key"], node_limit=t["node_limit"], seconds=time.perf_counter() - started)
        with lock:
            with args.out.open("a") as handle:
                handle.write(json.dumps(out) + "\n")
            print(t["key"], "error" if "error" in out else out["separation"], f"{out['seconds']:.1f}s", flush=True)

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        list(pool.map(run, todo))


if __name__ == "__main__":
    main()
