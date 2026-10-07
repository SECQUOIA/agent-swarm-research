"""Frozen, sequential extension diagnostics with separate bounded proof replay."""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import gzip
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import shutil
import subprocess
import sys
from time import perf_counter

HERE = Path(__file__).resolve().parent
THREADS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")
for key in THREADS:
    os.environ[key] = "1"
sys.path.insert(0, str(HERE))
from corpus import cases, references, objective, feasible


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, data):
    path.write_text(json.dumps(data, sort_keys=True, indent=2, default=str) + "\n")


def rss():
    return int(next(line.split()[1] for line in Path("/proc/self/status").read_text().splitlines()
                    if line.startswith("VmHWM:")))


def freeze():
    target = HERE / "frozen"
    if target.exists():
        raise ValueError("Refusing to overwrite frozen evidence")
    target.mkdir()
    base = HERE.parents[2]
    hashes = {}
    for directory in ("solver", "conditional-messages", "negative-curvature", "degeneracy", "constraints"):
        for source in sorted((base / directory).glob("*.py")):
            if source.name.startswith(("test_", "check_")):
                continue
            destination = target / directory / source.name
            destination.parent.mkdir(exist_ok=True)
            shutil.copy2(source, destination)
            hashes[str(destination.relative_to(target))] = digest(destination)
    for name in ("run_extensions.py", "corpus.py"):
        shutil.copy2(HERE / name, target / name)
        hashes[name] = digest(target / name)
    dump(target / "cases.json", cases())
    dump(target / "references.json", references())
    for name in ("cases.json", "references.json"):
        hashes[name] = digest(target / name)
    dump(target / "manifest.json", {"source_sha256": hashes, "python": sys.version,
         "platform": platform.platform(), "threads": 1, "solver_time_limit_seconds": 2,
         "worker_wall_limit_seconds": 5, "address_space_limit_mib": 512})


def load_case(name):
    # Executed by the copied runner, never the mutable source tree.
    sys.path.insert(0, str(HERE / "solver"))
    spec = json.loads((HERE / "cases.json").read_text())[name]
    model = spec["model"]
    if model["kind"] == "polynomial":
        from polynomial_grid import PolynomialBox, PolynomialFactor
        problem = PolynomialBox(model["bounds"], [PolynomialFactor.from_dict(f) for f in model["factors"]],
                                model["integers"], name=name)
    else:
        from certified_grid import BoxQP
        problem = BoxQP(model["A"], model["b"], model["bounds"], model["integers"],
                        constant=model["constant"], name=name)
    return spec, problem


def loaded_sources():
    """Record every loaded module inside the repository; reject snapshot leaks."""
    out = {}
    project = "minlp-notes"
    for module in tuple(sys.modules.values()):
        path = getattr(module, "__file__", None)
        if not path:
            continue
        path = Path(path).resolve()
        if project not in path.parts:
            continue
        if not path.is_relative_to(HERE):
            raise AssertionError("worker imported mutable repository module: " + str(path))
        if path.is_file() and path.suffix == ".py":
            out[str(path.relative_to(HERE))] = digest(path)
    return out


def analytic_patch_check(name, checked):
    bounds = checked.get("face_bounds")
    if name == "irrational_boundary":
        assert checked["kind"] == "strongly_convex_patch"
        lo, hi = bounds[0]
        assert 0 <= lo < hi and lo * lo <= F(1, 2) <= hi * hi and bounds[1] == (0, 0)
    elif name == "weak_boundary":
        assert checked["kind"] == "strongly_convex_patch"
        assert bounds[0][0] <= F(1, 4) <= bounds[0][1] and bounds[1] == (0, 0)
    else:
        raise AssertionError("unexpected successful boundary case")


def solve_worker(args):
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024**2,) * 2)
    started = perf_counter()
    spec, problem = load_case(args.case)
    method, options = spec["method"], dict(spec["options"])
    metadata = {"case": args.case, "method": method, "n": len(problem.bounds),
                "decomposition_width": max(map(len, problem.bags)) - 1,
                "load_and_preprocessing_seconds": perf_counter() - started}
    solve_started = perf_counter()
    if method == "polynomial":
        from polynomial_grid import solve
        options["epsilon"] = F(options["epsilon"])
        options.setdefault("max_table_states", 30000)
        result = solve(problem, time_limit=2, max_stages=128, **options)
        certificate = result
    elif method == "boundary":
        from polynomial_boundary import discover_boundary
        options.setdefault("max_rounds", 8)
        result = discover_boundary(problem, time_limit=2, max_stages=128, max_table_states=30000, **options)
        certificate = result.get("certificate")
    elif method == "submodular":
        from submodular_recourse import solve_submodular
        result = solve_submodular(problem, exact=True, time_limit=2, max_queries=1000,
                                  max_faces=10000, max_pivots=10000, **options)
        certificate = result
    else:
        raise ValueError(method)
    metadata.update(status=result["status"], solve_seconds=perf_counter() - solve_started)
    for key in ("reason", "attempts", "lower", "upper", "gap", "point", "stats"):
        if key in result:
            metadata[key] = result[key]
    if certificate is not None:
        assert certificate["problem"] == problem.to_dict()
        metadata["certificate_input_bound"] = True
        metadata["certificate_schema"] = certificate["schema"]
        if "point" in certificate:
            point = tuple(map(F, certificate["point"]))
            assert feasible(spec["model"], point)
            value = objective(spec["model"], point)
            assert value == F(certificate.get("upper", certificate.get("value")))
            metadata["independent_objective_checked"] = True
        path = args.output.with_suffix(".certificate.json.gz")
        with gzip.open(path, "wt") as stream:
            json.dump(certificate, stream, sort_keys=True)
        metadata.update(certificate_file=path.name, certificate_bytes_gzip=path.stat().st_size,
                        certificate_sha256=digest(path))
    else:
        metadata["certificate_file"] = None
    metadata.update(worker_seconds=perf_counter() - started, peak_rss_kib=rss(),
                    loaded_source_sha256=loaded_sources())
    dump(args.output, metadata)


def check_worker(args):
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024**2,) * 2)
    started = perf_counter()
    spec, problem = load_case(args.case)
    with gzip.open(args.certificate, "rt") as stream:
        certificate = json.load(stream)
    assert certificate["problem"] == problem.to_dict()
    check_started = perf_counter()
    method = spec["method"]
    if method == "polynomial":
        from verify_polynomial import verify_polynomial
        checked = verify_polynomial(certificate, expected_problem=problem)
        assert checked["valid"]
    elif method == "boundary":
        from verify_polynomial_boundary import verify_certificate
        checked = verify_certificate(certificate, problem)
        assert checked["valid"]
        analytic_patch_check(args.case, checked)
        checked["independent_analytic_optimizer_contained"] = True
    else:
        from verify_submodular_recourse import verify_submodular
        assert verify_submodular(certificate, problem)
        checked = {"valid": True}
    reference = json.loads((HERE / "references.json").read_text())[args.case]
    if "lower" in certificate:
        assert F(certificate["lower"]) <= F(reference["value"]) <= F(certificate["upper"])
        checked["independent_reference_enclosed"] = True
        if certificate["status"] == "exact":
            assert F(certificate["upper"]) == F(reference["value"])
    dump(args.output, {"certificate_check": checked, "check_seconds": perf_counter() - check_started,
          "checker_worker_seconds": perf_counter() - started, "checker_peak_rss_kib": rss(),
          "checker_loaded_source_sha256": loaded_sources()})


def launch(command):
    started = perf_counter()
    try:
        process = subprocess.run(command, capture_output=True, text=True, timeout=5, env=dict(os.environ))
        return {"returncode": process.returncode, "seconds": perf_counter() - started,
                "stderr": process.stderr[-4000:] if process.returncode else ""}
    except subprocess.TimeoutExpired:
        return {"returncode": None, "seconds": perf_counter() - started, "stderr": "hard worker wall limit"}


def run():
    results = HERE / "results"
    if results.exists():
        raise ValueError("Refusing to overwrite published results")
    results.mkdir()
    frozen = HERE / "frozen"
    manifest = json.loads((frozen / "manifest.json").read_text())
    for name, expected in manifest["source_sha256"].items():
        assert digest(frozen / name) == expected, "frozen source mismatch: " + name
    summaries = []
    for name, spec in json.loads((frozen / "cases.json").read_text()).items():
        path = results / (name + ".json")
        worker = launch([sys.executable, str(frozen / "run_extensions.py"), "--solve-worker", "--case", name,
                         "--output", str(path)])
        if worker["returncode"] != 0:
            row = {"case": name, "method": spec["method"], "status": "hard_time_limit" if worker["returncode"] is None
                   else "worker_failure", "solver_subprocess": worker}
        else:
            row = json.loads(path.read_text())
            row["solver_subprocess"] = worker
            if row["certificate_file"]:
                checkpath = results / (name + ".check.json")
                check = launch([sys.executable, str(frozen / "run_extensions.py"), "--check-worker", "--case", name,
                                "--certificate", str(results / row["certificate_file"]), "--output", str(checkpath)])
                row["checker_subprocess"] = check
                if check["returncode"] == 0:
                    row.update(json.loads(checkpath.read_text()))
                else:
                    row["certificate_check"] = {"valid": False, "status": "hard_time_limit" if check["returncode"] is None
                                                else "checker_failure"}
            row["total_subprocess_seconds"] = worker["seconds"] + row.get("checker_subprocess", {}).get("seconds", 0)
        dump(path, row)
        summaries.append(row)
        print(name, row["status"], row.get("certificate_check", {}).get("valid"), flush=True)
    dump(HERE / "summary.json", {"configurations": len(summaries), "results": summaries,
          "valid_certificate_replays": sum(row.get("certificate_check", {}).get("valid") is True for row in summaries),
          "proof_replay_failures": sum("certificate_check" in row and row["certificate_check"].get("valid") is not True for row in summaries)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze", action="store_true")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--solve-worker", action="store_true")
    parser.add_argument("--check-worker", action="store_true")
    parser.add_argument("--case")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--certificate", type=Path)
    args = parser.parse_args()
    if args.freeze:
        freeze()
    elif args.run:
        run()
    elif args.solve_worker:
        solve_worker(args)
    elif args.check_worker:
        check_worker(args)
    else:
        parser.error("choose --freeze, --run, --solve-worker, or --check-worker")


if __name__ == "__main__":
    main()
