"""Eight legacy cases x three GAMS big-M baselines, explicit initialization.

Outcome-triggered followup declared from partial legacy results after source
freeze. Only documented initial values change; all solver adapters remain frozen.
Run only after independent review and root allocation of solver slots.
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
from lbesh_research.summarize import assessed
from lbesh_research.validation import capture_witness, validate_witness

LAB = Path(__file__).resolve().parent
TIME_LIMIT, WALL_LIMIT, THREADS = 120.0, 150.0, 1
SOURCE_MANIFEST = LAB / "results/lbesh_development/source_v1_manifest.json"
ADAPTER_SHA256 = "dbfb95a4a9534ec4596a1b3423ac6563b22fac4d86034e5a47dc184707b02f5b"
INSTANCES = tuple("pyomo.farm_layout." + name for name in
                  ("FLay02", "FLay03", "FLay03_alt_1", "FLay03_alt_2", "FLay04", "FLay05", "FLay06"))
INSTANCES += ("gdplib.batch_processing",)
METHODS = tuple(f"gams-{solver}-bigm-initialized" for solver in ("shot", "gurobi", "scip"))


def metadata():
    meta = primary._metadata(legacy=True)
    frozen = json.loads(SOURCE_MANIFEST.read_text())["files"]
    for name, digest in meta["source_sha256"].items():
        if digest != frozen.get("code/minlp_solver_lab/" + name):
            raise RuntimeError("Source differs from the frozen manifest: " + name)
    if meta["source_sha256"]["lbesh_research/benchmark.py"] != ADAPTER_SHA256:
        raise RuntimeError("Frozen benchmark adapter hash mismatch")
    if meta["uv_lock_sha256"] != frozen.get("code/minlp_solver_lab/uv.lock"):
        raise RuntimeError("Frozen dependency lock hash mismatch")
    meta.update(supplementary_wrapper_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                copied_adapter_source_sha256=ADAPTER_SHA256,
                source_manifest_sha256=hashlib.sha256(SOURCE_MANIFEST.read_bytes()).hexdigest(),
                study_role="post-freeze initialization followup triggered by partial legacy results; all seven farms plus batch processing x three GAMS baselines")
    return meta


def initialize_widths(model):
    """Use each existing affine width bound as a domain-valid starting value.

    No variable bounds, equations, disjunctions, or solver options are changed.
    These values are initialization only, not claimed feasible incumbents.
    """
    import math
    import pyomo.environ as pe
    changes = []
    for index in model.plots:
        var, row = model.plot_width[index], model.width_bounds[index]
        if not row.active or row.body is not var:
            raise ValueError("Expected an active direct affine width-bound row")
        lower = pe.value(row.lower)
        if not math.isfinite(lower) or lower <= 0:
            raise ValueError("Width-bound row must establish a finite positive lower bound")
        if var.fixed or (var.lb is not None and lower < pe.value(var.lb)) or (var.ub is not None and lower > pe.value(var.ub)):
            raise ValueError("Width initialization conflicts with the original variable domain")
        changes.append(dict(variable=var.name, old_value=var.value, new_value=lower,
                            source_constraint=row.name, source_lower_bound=lower,
                            original_variable_bounds=list(var.bounds)))
        var.set_value(lower)
    return changes


def initialize_model(name, model):
    if name.startswith("pyomo.farm_layout."):
        return initialize_widths(model)
    if name != "gdplib.batch_processing":
        raise ValueError("No declared initialization for this instance")
    import math
    import pyomo.environ as pe
    from pyomo.gdp import Disjunct
    from pyomo.core.expr.visitor import identify_variables
    last = model.STAGES.last()
    var = model.storageTankSize_log[last]
    if last in model.STAGESExceptLast:
        raise ValueError("Trailing storage stage unexpectedly belongs to tank-selection stages")
    for ctype in (pe.Constraint, pe.Objective, pe.Expression, pe.LogicalConstraint):
        for component in model.component_data_objects(ctype, active=None, descend_into=(pe.Block, Disjunct)):
            if any(v is var for v in identify_variables(component.expr, include_fixed=True)):
                raise ValueError("Trailing tank variable is referenced by " + component.name)
    if any(model.component_data_objects(pe.SOSConstraint, active=None, descend_into=(pe.Block, Disjunct))):
        raise ValueError("Unexpected SOS component prevents the declared unused-variable check")
    lower, upper = var.bounds
    if var.fixed or lower is None or not math.isfinite(lower) or (upper is not None and lower > upper):
        raise ValueError("Trailing tank variable lacks a valid declared lower-bound initialization")
    change = dict(variable=var.name, old_value=var.value, new_value=lower,
                  source_constraint=None, source_lower_bound=lower,
                  original_variable_bounds=list(var.bounds),
                  rationale="Unused trailing tank variable; all algebraic and logical expressions checked including every disjunct")
    var.set_value(lower)
    return [change]


def native_versions(logfile):
    text = logfile.read_text(errors="replace") if logfile.exists() else ""
    patterns = {"gams": r"GAMS (\d+\.\d+\.\d+)",
                "gurobi": r"Gurobi Optimizer version (\d+\.\d+\.\d+)",
                "scip": r"SCIP version (\d+\.\d+\.\d+)",
                "shot": r"SHOT[^\n]*?version[: ]+(\d+\.\d+(?:\.\d+)?)"}
    return {key: match.group(1) if (match := re.search(pattern, text, re.I)) else None
            for key, pattern in patterns.items()}


def run_one(name, method, workdir):
    import pyomo.environ as pe
    start = time.monotonic()
    rec = dict(schema_version=primary.SCHEMA_VERSION, instance=name, method=method,
               solver_time_limit=TIME_LIMIT, threads=THREADS, outcome="error",
               metadata=metadata(), witness=None, validation=None, bound_valid=False)
    try:
        if name not in INSTANCES or method not in METHODS:
            raise ValueError("Followup accepts only the declared eight instances and three methods")
        model = primary._build(name)
        original = model.clone()
        objectives = list(original.component_data_objects(pe.Objective, active=True))
        if len(objectives) != 1:
            raise ValueError("Benchmark requires exactly one objective")
        sense = 1 if objectives[0].sense == pe.minimize else -1
        rec.update(objective_sense="minimize" if sense == 1 else "maximize",
                   instance_metadata={"source": "legacy_gdp_instances"},
                   initialization_changes=initialize_model(name, model))
        solver = method.split("-")[1]
        # The exact same adapter, options, formulation, and limits as primary.
        rec.update(primary._gams(model, solver, "bigm", TIME_LIMIT, THREADS, workdir, sense))
        has_solution = rec.pop("has_solution")
        rec["reported_objective"] = rec["native_gams"].get("OBJVAL")
        rec["native_versions"] = native_versions(workdir / "gams.log")
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


def execute(name, method, directory):
    """Frozen benchmark process-cap pattern with this wrapper's worker target."""
    run_id = hashlib.sha256((name + "\0" + method).encode()).hexdigest()[:16]
    workdir = directory / run_id
    workdir.mkdir(parents=True, exist_ok=False)
    result_path = workdir / "result.json"
    cmd = [sys.executable, str(Path(__file__).resolve()), "--worker", name, method, "--out", str(result_path)]
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
    rec = dict(schema_version=primary.SCHEMA_VERSION, instance=name, method=method,
               outcome="wall_timeout" if timed_out else "crash", bound_valid=False, metadata=metadata())
    if not timed_out and result_path.exists():
        rec = json.loads(result_path.read_text())
    rec.update(wall_time=time.monotonic() - start, wall_limit=WALL_LIMIT, solver_time_limit=TIME_LIMIT,
               threads=THREADS, exit_code=code, artifacts=str(workdir))
    primary._atomic_json(workdir / "final.json", rec)
    return rec


def schedule(parallel, seed):
    return dict(instances=list(INSTANCES), methods=list(METHODS), time_limit=TIME_LIMIT,
                wall_limit=WALL_LIMIT, threads=THREADS, parallel=parallel, order_seed=seed,
                ordered_jobs=primary.ordered_jobs(INSTANCES, METHODS, seed), metadata=metadata(),
                initialization="Farm widths at their affine-row lower bounds; unused trailing batch tank at its own lower bound; initial values only",
                unchanged="all bounds, expressions, disjunctions, big-M computation, solver options, validation",
                validator_tolerances={"absolute": 1e-6, "relative": 1e-7, "integrality": 1e-6})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True)
    parser.add_argument("--parallel", type=int, default=1)
    parser.add_argument("--order-seed", type=int, default=20260927)
    parser.add_argument("--worker", nargs=2, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if not 1 <= args.parallel <= min(6, os.cpu_count() or 1):
        parser.error("Parallelism must be between one and six allocated solver slots")
    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    if args.worker:
        if args.worker[0] not in INSTANCES or args.worker[1] not in METHODS:
            parser.error("Worker must belong to the declared followup schedule")
        if out.exists():
            parser.error("Worker output already exists")
        primary._atomic_json(out, run_one(*args.worker, out.parent))
        return
    directory = out.with_suffix(out.suffix + ".runs")
    if out.exists() or directory.exists():
        parser.error("Output or artifact directory exists; use a new output path")
    plan = schedule(args.parallel, args.order_seed)
    directory.mkdir()
    primary._atomic_json(directory / "schedule.json", plan)
    with out.open("x") as stream, ThreadPoolExecutor(max_workers=args.parallel) as pool:
        futures = [pool.submit(execute, name, method, directory) for name, method in plan["ordered_jobs"]]
        for future in as_completed(futures):
            rec = future.result()
            stream.write(json.dumps(rec, allow_nan=False) + "\n")
            stream.flush()
            print(rec["instance"], rec["method"], rec["outcome"], rec.get("assessment", {}).get("solved"), flush=True)


if __name__ == "__main__":
    main()
