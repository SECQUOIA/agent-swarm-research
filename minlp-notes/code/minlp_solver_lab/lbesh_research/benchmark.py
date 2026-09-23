"""Fresh-process, wall-capped LB-ESH comparison with retained primal witnesses.

Run from code/minlp_solver_lab: python -m lbesh_research.benchmark
--instances all --methods core --out results/lbesh_development/core.jsonl.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import random
import signal
import subprocess
import sys
import time
import traceback

CORE_METHODS = [f"lbesh-{rule}-{form}-{tree}" for rule in ("esh", "ecp")
                for form in ("hull", "bigm") for tree in ("single", "multi")]
BASELINES = ["gdpopt-loa", "gams-shot-bigm", "gams-shot-hull-convex", "conic-hull-gurobi"]
OPTIONAL_BASELINES = ["gams-shot-hull"] + [f"gams-{solver}-{form}" for solver in ("gurobi", "scip")
                      for form in ("bigm", "hull")]
SCHEMA_VERSION = 1


def ordered_jobs(names, methods, seed):
    jobs = [(name,method) for name in names for method in methods]
    random.Random(seed).shuffle(jobs)
    return jobs


def _build(name):
    from . import instances
    if name in instances.MANIFEST:
        return instances.build(name)
    from gdp_instances import INSTANCES
    return INSTANCES[name]()


def _metadata(*, legacy=False):
    lab = Path(__file__).resolve().parents[1]
    versions = {}
    for package in ("pyomo", "gurobipy", "numpy", "scipy", "gamsapi", "pyscipopt"):
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = None
    files = (list((lab / "lbesh").glob("*.py")) + list((lab / "lbesh_research").glob("*.py"))
             + [lab/"gdp_instances.py", lab/"pyproject.toml"])
    if legacy:
        for root in (lab/"instances/gdplib_src", lab/"instances/pyomo_examples_src"):
            files.extend(p for p in root.rglob("*") if p.is_file() and
                         not any(part in (".git", "__pycache__", ".pytest_cache") for part in p.parts)
                         and p.suffix != ".pyc")
    return dict(python=sys.version, platform=platform.platform(), packages=versions,
                source_sha256={str(p.relative_to(lab)): hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in sorted(files)},
                uv_lock_sha256=hashlib.sha256((lab/"uv.lock").read_bytes()).hexdigest())


def _raw_results(result, sense):
    from .validation import finite
    return dict(raw_status=str(result.solver.termination_condition),
                raw_solver_status=str(result.solver.status),
                raw_solver_message=str(result.solver.message),
                dual_bound=finite(result.problem.lower_bound if sense == 1 else result.problem.upper_bound),
                raw_lower_bound=finite(result.problem.lower_bound),
                raw_upper_bound=finite(result.problem.upper_bound))


def _gams(model, solver, form, time_limit, threads, workdir, sense, *, assume_convex=False):
    import pyomo.environ as pe
    from pyomo.gdp import Disjunct
    from .validation import finite
    transformation = pe.TransformationFactory("gdp."+form)
    original_vars = list(model.component_data_objects(pe.Var,active=None,descend_into=(pe.Block,Disjunct)))
    original_disjuncts = list(model.component_data_objects(Disjunct,active=None,descend_into=(pe.Block,Disjunct)))
    transformation.apply_to(model)
    initialized = 0
    if form == "hull":
        # The writer evaluates expression domains at initialization. Pyomo
        # copies x into every nu; for an inactive branch this evaluates x/eps,
        # which can overflow exp or leave a logarithm's domain. A consistent
        # disaggregation nu=lambda*x avoids that artificial writer failure.
        for disjunct in original_disjuncts:
            if disjunct._transformation_block is None:
                continue
            lam = finite(disjunct.binary_indicator_var.value)
            if lam is None:
                continue
            for var in original_vars:
                nu = transformation.get_disaggregated_var(var,disjunct,raise_exception=False)
                x = finite(var.value)
                if nu is not None and nu is not var and x is not None:
                    nu.set_value(lam*x,skip_validation=True)
                    initialized += 1
    opt = pe.SolverFactory("gams", solver_io="shell")
    if not opt.available(exception_flag=False):
        raise SolverUnavailable("GAMS executable unavailable")
    native = {}
    # Preserve native GAMS MODELSTAT, SOLVESTAT and OBJEST before Pyomo maps
    # them into generic statuses. This narrowly wraps its versioned DAT reader.
    parse = opt._parse_dat_results
    def capture(*args):
        solution, stats = parse(*args)
        native.update({k: finite(v) for k,v in stats.items()})
        return solution, stats
    opt._parse_dat_results = capture
    options = [f"option reslim={time_limit};", f"option threads={threads};",
               "option optcr=0.0001;", "option optca=0.000001;"]
    solver_options = {}
    io_options = {"put_results_format": "dat"}
    if solver == "shot":
        solver_options = {"Primal.Tolerance.Integer": 1e-8,
                          "Primal.Tolerance.LinearConstraint": 1e-6,
                          "Primal.Tolerance.NonlinearConstraint": 1e-8,
                          "Primal.Tolerance.TrustLinearConstraintValues": False,
                          "Dual.MIP.Solver": 1,
                          "Dual.MIP.NumberOfThreads": threads}
        if assume_convex:
            solver_options["Model.Convexity.AssumeConvex"] = True
        (workdir/"gams").mkdir(parents=True,exist_ok=True)
        (workdir/"gams"/"shot.opt").write_text("".join(
            f"{key} = {str(value).lower()}\n" for key,value in solver_options.items()))
        options.append("GAMS_MODEL.optfile=1;")
        # SHOT accepts affine instances through its MINLP interface too.
        io_options["mtype"] = "minlp"
    result = opt.solve(model, solver=solver, load_solutions=False, tee=False,
                       logfile=str(workdir/"gams.log"),
                       tmpdir=str(workdir/"gams"), keepfiles=True,
                       io_options=io_options, add_options=options)
    record = _raw_results(result, sense)
    native_status = native.get("MODELSTAT")
    has_solution = native_status in (1,2,7,8) and len(result.solution) > 0
    if has_solution:
        model.solutions.load_from(result)
    record.update(native_gams=native, options=dict(solver=solver, formulation=form,
                  add_options=options,solver_options=solver_options,
                  hull_initialization="nu=lambda*x",initialized_disaggregates=initialized),
                  dual_bound=native.get("OBJEST"),
                  bound_valid=(native.get("OBJEST") is not None and solver in ("shot", "scip", "gurobi")
                               and native_status in (1,7,8)),
                  bound_source="GAMS native OBJEST"+(" with declared convexity" if assume_convex else ""),
                  has_solution=has_solution)
    return record


class SolverUnavailable(RuntimeError):
    pass


def run_one(name, method, time_limit, threads, workdir):
    import pyomo.environ as pe
    from .validation import capture_witness, validate_witness, finite
    from .summarize import assessed
    start = time.monotonic()
    rec = dict(schema_version=SCHEMA_VERSION, instance=name, method=method,
               solver_time_limit=time_limit, threads=threads, outcome="error",
               metadata=_metadata(legacy=not name.startswith("lbesh.")),
               witness=None, validation=None, bound_valid=False)
    try:
        model = _build(name)
        original = model.clone()
        originals = list(original.component_data_objects(pe.Objective, active=True))
        if len(originals) != 1:
            raise ValueError("Benchmark requires exactly one objective")
        sense = 1 if originals[0].sense == pe.minimize else -1
        rec["objective_sense"] = "minimize" if sense == 1 else "maximize"
        try:
            from .instances import MANIFEST
            rec["instance_metadata"] = MANIFEST.get(name, {"source": "legacy_gdp_instances"})
        except ImportError:
            pass
        reported_objective = None
        has_solution = False
        if method.startswith("lbesh-"):
            from lbesh.solver import LBESH
            parts = method.split("-")
            if len(parts) < 4 or parts[1] not in ("esh", "ecp") or parts[2] not in ("hull", "bigm") or parts[3] not in ("single", "multi"):
                raise ValueError("Unknown LB-ESH method: "+method)
            suffix = set(parts[4:])
            if suffix - {"nonlp", "nolp", "usercuts"}:
                raise ValueError("Unknown LB-ESH ablation: "+method)
            options = dict(formulation=parts[2], esh=parts[1] == "esh",
                           nlp_at_integer="nonlp" not in suffix, lp_phase="nolp" not in suffix,
                           user_cuts="usercuts" in suffix, nlp_solver="ipopt", threads=threads,
                           time_limit=time_limit, abs_tol=1e-6, rel_tol=1e-4,
                           feas_tol=1e-6, verbose=False)
            if not pe.SolverFactory("ipopt").available(exception_flag=False):
                raise SolverUnavailable("Ipopt executable unavailable")
            solver = LBESH(model, **options)
            stats = solver.solve(single_tree=parts[3] == "single")
            metrics = {k: (finite(v) if isinstance(v, float) else v) for k,v in stats.as_dict().items()}
            reported_objective = finite(stats.obj)
            rec.update(raw_status=stats.status, solver_metrics=metrics, options=options,
                       metric_semantics="Component times overlap: single-tree time_master includes callback NLP and cut work; do not sum component times.",
                       dual_bound=finite(stats.bound), bound_source="LBESH master global bound",
                       bound_valid=finite(stats.bound) is not None)
            has_solution = solver.incumbent is not None
        elif method == "gdpopt-loa":
            if not pe.SolverFactory("ipopt").available(exception_flag=False):
                raise SolverUnavailable("Ipopt executable unavailable")
            options = dict(nlp_solver="ipopt", mip_solver="gurobi",
                           mip_solver_args=dict(options=dict(Threads=threads, MIPGap=1e-4, MIPGapAbs=1e-6)),
                           time_limit=time_limit, bound_tolerance=1e-6, tee=False)
            result = pe.SolverFactory("gdpopt.loa").solve(model, **options)
            rec.update(_raw_results(result,sense), options=options,
                       bound_source="GDPopt global master bound")
            # GDPopt loads its incumbent directly; finite incumbent bound
            # distinguishes a saved solution from the model's initialization.
            incumbent_bound = finite(result.problem.upper_bound if sense == 1 else result.problem.lower_bound)
            has_solution = incumbent_bound is not None
            reported_objective = incumbent_bound
            rec["bound_valid"] = rec["dual_bound"] is not None
        elif method.startswith("gams-"):
            parts = method.split("-")
            if len(parts) not in (3,4):
                raise ValueError("Unknown GAMS baseline: "+method)
            _, solver, form = parts[:3]
            declared_convex = len(parts) == 4 and parts[3] == "convex"
            if len(parts) == 4 and not declared_convex:
                raise ValueError("Unknown GAMS baseline: "+method)
            if solver not in ("shot", "scip", "gurobi") or form not in ("bigm", "hull"):
                raise ValueError("Unknown GAMS baseline: "+method)
            if declared_convex:
                from .instances import MANIFEST
                if solver != "shot" or name not in MANIFEST:
                    raise ValueError("Declared convexity is restricted to SHOT on verified generated instances")
            rec.update(_gams(model,solver,form,time_limit,threads,workdir,sense,
                             assume_convex=declared_convex))
            has_solution = rec.pop("has_solution")
            reported_objective = rec["native_gams"].get("OBJVAL")
        elif method == "conic-hull-gurobi":
            from .conic import solve, UnsupportedConic
            try:
                result = solve(model,time_limit=time_limit,threads=threads)
            except UnsupportedConic as exc:
                rec.update(outcome="unsupported", error=str(exc))
                return rec
            rec.update(raw_status=result.get("status"), native_status=result.get("raw_status"),
                       options=result.get("options"), solver_metrics={k:v for k,v in result.items()
                       if k not in ("witness", "options")}, dual_bound=finite(result.get("lb")),
                       bound_source="exact quadratic hull Gurobi global bound",
                       bound_valid=finite(result.get("lb")) is not None)
            reported_objective = finite(result.get("obj"))
            if result.get("witness"):
                # GDP disjuncts are not ordinary blocks in Pyomo's traversal.
                from pyomo.gdp import Disjunct
                for v in model.component_data_objects(pe.Var, active=None, descend_into=(pe.Block,Disjunct)):
                    if v.name in result["witness"]:
                        v.set_value(result["witness"][v.name], skip_validation=True)
                from pyomo.core.base.boolean_var import BooleanVarData
                boolean_witness = result.get("boolean_witness", {})
                for v in model.component_data_objects(pe.BooleanVar, active=None, descend_into=(pe.Block,Disjunct)):
                    if v.name in boolean_witness:
                        BooleanVarData.set_value(v,boolean_witness[v.name],skip_validation=True)
                has_solution = True
        else:
            raise ValueError("Unknown method: "+method)
        rec["reported_objective"] = reported_objective
        if has_solution:
            full = capture_witness(model)
            wanted = capture_witness(original)
            witness = {kind: {key: full[kind].get(key) for key in wanted[kind]} for kind in wanted}
            rec["witness"] = witness
            rec["validation"] = validate_witness(original,witness,reported_objective=reported_objective)
        rec["outcome"] = "completed"
        rec["assessment"] = assessed(rec)
    except SolverUnavailable as exc:
        rec.update(outcome="unavailable", error=str(exc))
    except Exception as exc:
        rec.update(outcome="error", error_type=type(exc).__name__, error=str(exc),
                   traceback=traceback.format_exc())
    finally:
        rec["worker_time"] = time.monotonic()-start
    return rec


def _atomic_json(path, value):
    temp = path.with_suffix(path.suffix+".tmp")
    temp.write_text(json.dumps(value,indent=2,allow_nan=False)+"\n")
    temp.replace(path)


def execute(name, method, *, time_limit, wall_limit, threads, directory):
    """Redirect logs to files and kill the entire process group at the wall cap."""
    run_id = hashlib.sha256((name+"\0"+method).encode()).hexdigest()[:16]
    workdir = directory/run_id
    workdir.mkdir(parents=True, exist_ok=False)
    result_path = workdir/"result.json"
    cmd = [sys.executable,"-m","lbesh_research.benchmark","--worker",name,method,
           "--time-limit",str(time_limit),"--threads",str(threads),"--out",str(result_path)]
    env = os.environ.copy()
    for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
        env[key] = str(threads)
    start = time.monotonic()
    with (workdir/"stdout.log").open("w") as stdout, (workdir/"stderr.log").open("w") as stderr:
        process = subprocess.Popen(cmd,stdout=stdout,stderr=stderr,env=env,start_new_session=True)
        try:
            code = process.wait(timeout=wall_limit)
            timed_out = False
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid,signal.SIGKILL)
            except ProcessLookupError:
                pass
            code = process.wait()
            timed_out = True
    elapsed = time.monotonic()-start
    record = dict(schema_version=SCHEMA_VERSION,instance=name,method=method,
                  outcome="wall_timeout" if timed_out else "crash",bound_valid=False)
    if not timed_out and result_path.exists():
        record = json.loads(result_path.read_text())
    record.update(wall_time=elapsed,wall_limit=wall_limit,solver_time_limit=time_limit,
                  threads=threads,exit_code=code,artifacts=str(workdir))
    _atomic_json(workdir/"final.json",record)
    return record


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--instances",default="all")
    p.add_argument("--methods",default="core")
    p.add_argument("--time-limit",type=float,default=300)
    p.add_argument("--wall-limit",type=float,help="Total process cap; default time limit plus 30 seconds")
    p.add_argument("--threads",type=int,default=1)
    p.add_argument("--parallel",type=int,default=1)
    p.add_argument("--order-seed",type=int,default=0,
                   help="Seed for reproducibly shuffled instance/method launch order")
    p.add_argument("--out",required=True)
    p.add_argument("--worker",nargs=2)
    args = p.parse_args()
    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True,exist_ok=True)
    if args.worker:
        _atomic_json(out,run_one(*args.worker,args.time_limit,args.threads,out.parent))
        return
    wall_limit = args.wall_limit if args.wall_limit is not None else args.time_limit+30
    if min(args.time_limit,wall_limit,args.threads,args.parallel) <= 0:
        p.error("Time limits, threads and parallelism must be positive")
    if args.parallel*args.threads > (os.cpu_count() or 1):
        p.error("Requested solver threads exceed available CPU count")
    from .instances import MANIFEST
    names = sorted(MANIFEST) if args.instances == "all" else args.instances.split(",")
    methods = (CORE_METHODS if args.methods == "core" else CORE_METHODS+BASELINES
               if args.methods == "all" else args.methods.split(","))
    if len(set(names)) != len(names) or len(set(methods)) != len(methods):
        p.error("Duplicate instances or methods")
    directory = out.with_suffix(out.suffix+".runs")
    # New output files prevent accidental mixing of protocol versions or reruns.
    if out.exists() or directory.exists():
        p.error("Output or artifact directory exists; use a new output path")
    directory.mkdir()
    jobs = ordered_jobs(names,methods,args.order_seed)
    schedule = dict(instances=names,methods=methods,time_limit=args.time_limit,
                    wall_limit=wall_limit,threads=args.threads,parallel=args.parallel,
                    order_seed=args.order_seed,ordered_jobs=jobs,
                    metadata=_metadata(legacy=any(not name.startswith("lbesh.") for name in names)))
    _atomic_json(directory/"schedule.json",schedule)
    with out.open("x") as stream, ThreadPoolExecutor(max_workers=args.parallel) as pool:
        futures = [pool.submit(execute,name,method,time_limit=args.time_limit,
                   wall_limit=wall_limit,threads=args.threads,directory=directory)
                   for name,method in jobs]
        for future in as_completed(futures):
            record = future.result()
            stream.write(json.dumps(record,allow_nan=False)+"\n")
            stream.flush()
            print(record["instance"],record["method"],record["outcome"],
                  record.get("assessment",{}).get("solved"),round(record["wall_time"],3),flush=True)


if __name__ == "__main__":
    main()
