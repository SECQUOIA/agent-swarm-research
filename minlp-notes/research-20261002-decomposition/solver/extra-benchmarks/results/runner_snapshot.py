"""Bounded, sequential comparison of the sparse box-QP prototype.

Use --run to regenerate results. Each method runs in a fresh subprocess,
with one thread and an outer wall limit in addition to the solver limit.
The bundled QPLIB cases are not sliced, sparsified, or relaxed.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import gzip
import hashlib
import importlib
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
from time import perf_counter

HERE = Path(__file__).resolve().parent
SOLVER = HERE.parent
sys.path.insert(0, str(SOLVER))

from corpus import exact_face_minimum, instances, minimum_degree_decomposition, value


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def worker(args, problem=None):
    # The driver explicitly overwrites these too; this supports direct workers.
    for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
        os.environ[key] = "1"
    started = perf_counter()
    p = instances()[args.case] if problem is None else problem
    prep_started = perf_counter()
    bags, edges = minimum_degree_decomposition(p)
    preprocessing_seconds = perf_counter() - prep_started
    metadata = {"case": p.name, "method": args.method, "epsilon": args.epsilon,
                "n": len(p.b), "integer_variables": len(p.integers),
                "decomposition_width": max(map(len, bags)) - 1,
                "decomposition_bags": len(bags),
                "decomposition_seconds": preprocessing_seconds,
                "decomposition_method": "greedy minimum degree; width is an upper bound",
                "time_limit_seconds": args.time_limit,
                "max_table_states": args.max_table_states}
    if args.method == "scip":
        result = run_scip(p, args)
    else:
        import certified_grid
        constructed = perf_counter()
        problem = certified_grid.BoxQP(p.A, p.b, p.bounds, p.integers,
                                       bags, edges, constant=p.c, name=p.name)
        metadata["validation_seconds"] = perf_counter() - constructed
        solve_started = perf_counter()
        certificate = certified_grid.solve(
            problem, epsilon=F(args.epsilon), time_limit=args.time_limit,
            max_stages=24, max_table_states=args.max_table_states,
            pruning=args.method == "geometric_pruned",
            grid_mode="uniform" if args.method == "uniform_unpruned" else "geometric")
        metadata["solve_wall_seconds"] = perf_counter() - solve_started
        point = tuple(map(F, certificate["point"]))
        assert problem.feasible(point)
        assert value(p, point) == F(certificate["upper"])
        assert F(certificate["upper"]) - F(certificate["lower"]) == F(certificate["gap"])
        result = {key: certificate[key] for key in ("status", "lower", "upper", "gap", "stats")}
        result.update(certification="rational corrected-grid certificate",
                      maximum_completed_table_states=max(
                          (stage["table_states"] for stage in certificate["stages"]), default=0),
                      removed_intervals=sum(stage["removed_intervals"] for stage in certificate["stages"]))
        certificate_path = args.output.with_suffix(".certificate.json.gz")
        with gzip.open(certificate_path, "wt") as stream:
            json.dump(certificate, stream)
        result["certificate_file"] = certificate_path.name
        result["certificate_bytes_gzip"] = certificate_path.stat().st_size
        # The separately written checker may not exist during development.
        # Published runs require it and retain its actual result, never infer it.
        checker_path = SOLVER / "verify_certificate.py"
        if checker_path.exists():
            checker = importlib.import_module("verify_certificate")
            check_started = perf_counter()
            checked = checker.verify_certificate(certificate)
            result["certificate_check"] = checked
            result["certificate_check_seconds"] = perf_counter() - check_started
        else:
            result["certificate_check"] = "checker not available in this run"
    metadata.update(result)
    metadata["worker_wall_seconds"] = perf_counter() - started
    metadata["rusage_maxrss_kib"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # /proc reports this executable's high-water mark. Some launch paths
    # preserve an ancestor's earlier ru_maxrss across exec, so retain both.
    process_status = Path("/proc/self/status")
    if process_status.exists():
        metadata["peak_process_rss_kib"] = int(next(
            line.split()[1] for line in process_status.read_text().splitlines()
            if line.startswith("VmHWM:")))
    else:
        metadata["peak_process_rss_kib"] = metadata["rusage_maxrss_kib"]
    write_json(args.output, metadata)


def run_scip(p, args):
    import pyscipopt
    from pyscipopt import Model, quicksum

    model = Model(p.name)
    model.hideOutput()
    model.setIntParam("parallel/maxnthreads", 1)
    model.setIntParam("lp/threads", 1)
    model.setRealParam("limits/time", args.time_limit)
    model.setRealParam("limits/memory", 256)
    model.setRealParam("limits/absgap", float(F(args.epsilon)))
    model.setRealParam("limits/gap", 0.0)
    x = [model.addVar(f"x{i}", lb=float(lo), ub=float(hi),
                      vtype="I" if i in p.integers else "C")
         for i, (lo, hi) in enumerate(p.bounds)]
    z = model.addVar("objective_epigraph", lb=-model.infinity())
    expression = float(p.c) + quicksum(float(p.b[i]) * x[i] for i in range(len(x)))
    expression += quicksum(float(p.A[i][i] / 2) * x[i] * x[i]
                           for i in range(len(x)) if p.A[i][i])
    expression += quicksum(float(p.A[i][j]) * x[i] * x[j]
                           for i in range(len(x)) for j in range(i) if p.A[i][j])
    model.addCons(z >= expression)
    model.setObjective(z, "minimize")
    started = perf_counter()
    model.optimize()
    result = {"status": str(model.getStatus()),
              "certification": "floating point SCIP bounds, not exact certificates",
              "numerical_lower": model.getDualbound(),
              "numerical_upper": model.getPrimalbound(),
              "solve_wall_seconds": perf_counter() - started,
              "scip_seconds": model.getSolvingTime(), "nodes": model.getNNodes(),
              "scip_version": f"{model.getMajorVersion()}.{model.getMinorVersion()}.{model.getTechVersion()}",
              "pyscipopt_version": pyscipopt.__version__}
    result["numerical_gap"] = result["numerical_upper"] - result["numerical_lower"]
    if model.getNSols():
        raw = [F(str(model.getVal(xi))) for xi in x]
        # Repair only domain tolerance drift; a box permits this directly.
        point = tuple(min(hi, max(lo, F(round(v)) if i in p.integers else v))
                      for i, (v, (lo, hi)) in enumerate(zip(raw, p.bounds)))
        result["recomputed_feasible_upper"] = str(value(p, point))
        result["recomputed_feasible_point"] = list(map(str, point))
        result["repaired_coordinates"] = sum(a != b for a, b in zip(raw, point))
    model.freeProb()
    return result


def run_suite(args):
    args.output.mkdir(parents=True, exist_ok=True)
    cases = instances()
    exact = {name: exact_face_minimum(p) for name, p in cases.items() if len(p.b) <= 8}
    write_json(args.output / "exact_references.json", exact)
    import numpy as np
    case_metadata = {}
    for name, p in cases.items():
        eigenvalues = np.linalg.eigvalsh(np.array(p.A, dtype=float))
        case_metadata[name] = {
            "description": p.description, "source": p.source,
            "n": len(p.b), "integer_variables": len(p.integers),
            "max_positive_diagonal": str(max(F(0), max(p.A[i][i] for i in range(len(p.b))))),
            "numerical_minimum_eigenvalue": float(eigenvalues[0]),
            "numerical_maximum_eigenvalue": float(eigenvalues[-1]),
            "spectral_statistics_are_not_certificates": True}
    write_json(args.output / "cases.json", case_metadata)
    tracked_paths = [Path(__file__), HERE / "corpus.py", SOLVER / "certified_grid.py",
                     SOLVER / "verify_certificate.py"]
    tracked_paths += sorted((HERE / "data").glob("*.qplib"))
    tracked_paths += sorted((HERE / "data").glob("*.sol"))
    tracked_hashes = {str(path): digest(path) for path in tracked_paths}
    for name, path in (("runner", Path(__file__)), ("corpus", HERE / "corpus.py"),
                       ("solver", SOLVER / "certified_grid.py"),
                       ("checker", SOLVER / "verify_certificate.py")):
        (args.output / (name + "_snapshot.py")).write_bytes(path.read_bytes())
    metadata = {"python": sys.version, "platform": platform.platform(),
                "time_limit_seconds_per_solver": args.time_limit,
                "outer_wall_limit_seconds_per_worker": args.time_limit + 12,
                "max_table_states": args.max_table_states, "threads": 1,
                "solver_sha256": digest(SOLVER / "certified_grid.py"),
                "corpus_sha256": digest(HERE / "corpus.py"),
                "runner_sha256": digest(Path(__file__)),
                "checker_sha256": digest(SOLVER / "verify_certificate.py"),
                "external_inputs": {p.name: {"source": p.source,
                    "qplib_sha256": digest(HERE / "data" / (p.name + ".qplib")),
                    "sol_sha256": digest(HERE / "data" / (p.name + ".sol"))}
                    for p in cases.values() if p.source.startswith("https")}}
    write_json(args.output / "environment.json", metadata)
    configurations = [(name, "1/50") for name in cases]
    configurations += [(name, "1/1000") for name in
                       ("random_path", "near_convex_scale1", "near_convex_scale256")]
    methods = ("geometric_pruned", "geometric_unpruned", "uniform_unpruned", "scip")
    env = dict(os.environ)
    for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
        env[key] = "1"
    rows = []
    for name, epsilon in configurations:
        for method in methods:
            tag = f"{name}__eps{epsilon.replace('/', '_')}__{method}"
            output = args.output / (tag + ".json")
            command = [sys.executable, str(Path(__file__).resolve()), "--worker",
                       "--case", name, "--epsilon", epsilon, "--method", method,
                       "--time-limit", str(args.time_limit), "--max-table-states",
                       str(args.max_table_states), "--output", str(output)]
            started = perf_counter()
            try:
                process = subprocess.run(command, env=env, capture_output=True, text=True,
                                         timeout=args.time_limit + 12)
                if process.returncode:
                    row = {"case": name, "epsilon": epsilon, "method": method,
                           "status": "worker_failed", "stderr": process.stderr[-3000:]}
                else:
                    row = json.loads(output.read_text())
            except subprocess.TimeoutExpired:
                row = {"case": name, "epsilon": epsilon, "method": method,
                       "status": "outer_wall_limit"}
            row["subprocess_wall_seconds"] = perf_counter() - started
            if name in exact and "lower" in row:
                optimum = F(exact[name]["objective"])
                assert F(row["lower"]) <= optimum <= F(row["upper"]), tag
                row["exact_reference_enclosed"] = True
                row["exact_reference"] = str(optimum)
            if name in exact and "numerical_lower" in row:
                optimum = float(F(exact[name]["objective"]))
                row["numerical_reference_enclosed_with_1e_6_tolerance"] = (
                    row["numerical_lower"] <= optimum + 1e-6 and
                    row["numerical_upper"] >= optimum - 1e-6)
            write_json(output, row)
            rows.append(row)
            write_json(args.output / "results.json", rows)
            print(name, epsilon, method, row["status"],
                  f"{row['subprocess_wall_seconds']:.3f}s", flush=True)
    assert {str(path): digest(path) for path in tracked_paths} == tracked_hashes, (
        "A source or input changed while benchmarking; rerun after it is stable")
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--case")
    parser.add_argument("--method", choices=("geometric_pruned", "geometric_unpruned", "uniform_unpruned", "scip"))
    parser.add_argument("--epsilon", default="1/50")
    parser.add_argument("--time-limit", type=float, default=2)
    parser.add_argument("--max-table-states", type=int, default=20000)
    parser.add_argument("--output", type=Path, default=HERE / "results")
    args = parser.parse_args()
    if args.worker:
        worker(args)
    elif args.run:
        run_suite(args)
    else:
        parser.error("choose --run or --worker")


if __name__ == "__main__":
    main()
