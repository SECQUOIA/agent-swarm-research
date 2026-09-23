"""Post-freeze, all-nine-trig GAMS/Gurobi feasibility-tolerance sensitivity.

Run only when the study coordinator has allocated solver slots. This separate
adapter changes only FeasibilityTol to 1e-8; frozen primary code is untouched.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time
import traceback

from lbesh_research import benchmark as primary
from lbesh_research.instances import MANIFEST, build
from lbesh_research.summarize import assessed
from lbesh_research.validation import capture_witness, finite, validate_witness

METHOD = "gams-gurobi-bigm-feas1e8"
TIME_LIMIT, WALL_LIMIT, THREADS = 120.0, 150.0, 1
FEASIBILITY_TOLERANCE = 1e-8
COPIED_ADAPTER_SHA256 = "dbfb95a4a9534ec4596a1b3423ac6563b22fac4d86034e5a47dc184707b02f5b"
INSTANCES = tuple(sorted(name for name, item in MANIFEST.items() if item["family"] == "trig"))


def metadata():
    meta = primary._metadata()
    if meta["source_sha256"]["lbesh_research/benchmark.py"] != COPIED_ADAPTER_SHA256:
        raise RuntimeError("Frozen benchmark source differs from the reviewed adapter source")
    meta["supplementary_wrapper_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    meta["copied_adapter_source_sha256"] = COPIED_ADAPTER_SHA256
    meta["study_role"] = "post-freeze sensitivity triggered by partial primary results; all nine trig instances"
    return meta


def native_versions(logfile):
    text = logfile.read_text(errors="replace") if logfile.exists() else ""
    versions = {}
    for key, pattern in (("gams", r"GAMS (\d+\.\d+\.\d+)"),
                         ("gurobi", r"Gurobi Optimizer version (\d+\.\d+\.\d+)")):
        match = re.search(pattern, text)
        versions[key] = match.group(1) if match else None
    return versions


def solve_gams(model, workdir, sense):
    """Narrow copy of frozen benchmark._gams for big-M Gurobi only.

    Preserves transformation, native DAT parsing, status/load gates, and raw
    bounds. Only solver change: write gurobi.opt and enable optfile=1.
    """
    import pyomo.environ as pe
    pe.TransformationFactory("gdp.bigm").apply_to(model)
    opt = pe.SolverFactory("gams", solver_io="shell")
    if not opt.available(exception_flag=False):
        raise primary.SolverUnavailable("GAMS executable unavailable")
    native = {}
    parse = opt._parse_dat_results
    def capture(*args):
        solution, stats = parse(*args)
        native.update({k: finite(v) for k, v in stats.items()})
        return solution, stats
    opt._parse_dat_results = capture
    options = [f"option reslim={TIME_LIMIT};", f"option threads={THREADS};",
               "option optcr=0.0001;", "option optca=0.000001;", "GAMS_MODEL.optfile=1;"]
    solver_options = {"feasibilitytol": FEASIBILITY_TOLERANCE}
    gamsdir = workdir / "gams"
    gamsdir.mkdir(parents=True, exist_ok=True)
    option_file = gamsdir / "gurobi.opt"
    option_file.write_text("feasibilitytol 1e-8\n")
    result = opt.solve(model, solver="gurobi", load_solutions=False, tee=False,
                       logfile=str(workdir / "gams.log"), tmpdir=str(gamsdir),
                       keepfiles=True, io_options={"put_results_format": "dat"}, add_options=options)
    log = (workdir / "gams.log").read_text(errors="replace")
    effective = re.search(r"(?m)^\s*FeasibilityTol\s+([0-9.eE+-]+)\s*$", log)
    if effective is None or float(effective.group(1)) != FEASIBILITY_TOLERANCE:
        raise RuntimeError("Native Gurobi log does not confirm FeasibilityTol=1e-8")
    record = primary._raw_results(result, sense)
    native_status = native.get("MODELSTAT")
    has_solution = native_status in (1, 2, 7, 8) and len(result.solution) > 0
    if has_solution:
        model.solutions.load_from(result)
    record.update(native_gams=native,
                  options=dict(solver="gurobi", formulation="bigm", add_options=options,
                               solver_options=solver_options, hull_initialization="nu=lambda*x",
                               initialized_disaggregates=0),
                  dual_bound=native.get("OBJEST"),
                  bound_valid=native.get("OBJEST") is not None and native_status in (1, 7, 8),
                  bound_source="GAMS native OBJEST", has_solution=has_solution,
                  effective_feasibilitytol=float(effective.group(1)),
                  native_versions=native_versions(workdir / "gams.log"),
                  option_file_sha256=hashlib.sha256(option_file.read_bytes()).hexdigest())
    return record


def run_one(name, workdir):
    import pyomo.environ as pe
    start = time.monotonic()
    rec = dict(schema_version=primary.SCHEMA_VERSION, instance=name, method=METHOD,
               solver_time_limit=TIME_LIMIT, threads=THREADS, outcome="error",
               metadata=metadata(), witness=None, validation=None, bound_valid=False)
    try:
        if name not in INSTANCES:
            raise ValueError("Sensitivity worker accepts only declared trig instances")
        model = build(name)
        original = model.clone()
        objectives = list(original.component_data_objects(pe.Objective, active=True))
        if len(objectives) != 1:
            raise ValueError("Benchmark requires exactly one objective")
        sense = 1 if objectives[0].sense == pe.minimize else -1
        rec.update(objective_sense="minimize" if sense == 1 else "maximize",
                   instance_metadata=MANIFEST[name])
        rec.update(solve_gams(model, workdir, sense))
        has_solution = rec.pop("has_solution")
        rec["reported_objective"] = rec["native_gams"].get("OBJVAL")
        if has_solution:
            full, wanted = capture_witness(model), capture_witness(original)
            witness = {kind: {key: full[kind].get(key) for key in wanted[kind]} for kind in wanted}
            rec["witness"] = witness
            rec["validation"] = validate_witness(original, witness, reported_objective=rec["reported_objective"])
        rec["outcome"] = "completed"
        rec["assessment"] = assessed(rec)
    except primary.SolverUnavailable as exc:
        rec.update(outcome="unavailable", error=str(exc))
    except Exception as exc:
        rec.update(outcome="error", error_type=type(exc).__name__, error=str(exc), traceback=traceback.format_exc())
    finally:
        rec["worker_time"] = time.monotonic() - start
    return rec


def execute(name, directory):
    """Frozen execute process-cap pattern; worker target is this separate module."""
    run_id = hashlib.sha256((name + "\0" + METHOD).encode()).hexdigest()[:16]
    workdir = directory / run_id
    workdir.mkdir(parents=True, exist_ok=False)
    result_path = workdir / "result.json"
    cmd = [sys.executable, str(Path(__file__).resolve()), "--worker", name, "--out", str(result_path)]
    env = os.environ.copy()
    for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
        env[key] = str(THREADS)
    start = time.monotonic()
    with (workdir / "stdout.log").open("w") as stdout, (workdir / "stderr.log").open("w") as stderr:
        process = subprocess.Popen(cmd, stdout=stdout, stderr=stderr, env=env, start_new_session=True)
        try:
            code = process.wait(timeout=WALL_LIMIT)
            timed_out = False
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            code = process.wait()
            timed_out = True
    elapsed = time.monotonic() - start
    rec = dict(schema_version=primary.SCHEMA_VERSION, instance=name, method=METHOD,
               outcome="wall_timeout" if timed_out else "crash", bound_valid=False,
               metadata=metadata())
    if not timed_out and result_path.exists():
        rec = json.loads(result_path.read_text())
    rec.update(wall_time=elapsed, wall_limit=WALL_LIMIT, solver_time_limit=TIME_LIMIT,
               threads=THREADS, exit_code=code, artifacts=str(workdir))
    primary._atomic_json(workdir / "final.json", rec)
    return rec


def schedule(parallel, order_seed):
    return dict(instances=list(INSTANCES), methods=[METHOD], time_limit=TIME_LIMIT,
                wall_limit=WALL_LIMIT, threads=THREADS, parallel=parallel,
                order_seed=order_seed, ordered_jobs=primary.ordered_jobs(INSTANCES, [METHOD], order_seed),
                metadata=metadata(), solver_options={"feasibilitytol": FEASIBILITY_TOLERANCE},
                primary_results_unchanged=True,
                validator_tolerances={"absolute": 1e-6, "relative": 1e-7, "integrality": 1e-6})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True)
    parser.add_argument("--parallel", type=int, default=1)
    parser.add_argument("--order-seed", type=int, default=20260926)
    parser.add_argument("--worker", choices=INSTANCES, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if not 1 <= args.parallel <= min(6, os.cpu_count() or 1):
        parser.error("Parallelism must be between one and six allocated solver slots")
    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    if args.worker:
        if out.exists():
            parser.error("Worker output already exists")
        primary._atomic_json(out, run_one(args.worker, out.parent))
        return
    directory = out.with_suffix(out.suffix + ".runs")
    if out.exists() or directory.exists():
        parser.error("Output or artifact directory exists; use a new output path")
    plan = schedule(args.parallel, args.order_seed)
    directory.mkdir()
    primary._atomic_json(directory / "schedule.json", plan)
    with out.open("x") as stream, ThreadPoolExecutor(max_workers=args.parallel) as pool:
        futures = [pool.submit(execute, name, directory) for name, _ in plan["ordered_jobs"]]
        for future in as_completed(futures):
            rec = future.result()
            stream.write(json.dumps(rec, allow_nan=False) + "\n")
            stream.flush()
            print(rec["instance"], METHOD, rec["outcome"], rec.get("assessment", {}).get("solved"), flush=True)


if __name__ == "__main__":
    main()
