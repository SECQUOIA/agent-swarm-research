"""Sequential frozen cone references; run only after scheduled solver queues.

Use lbesh_research/conic_reference_env/.venv/bin/python. This driver never
retries or changes tolerances. Outputs are exclusively created JSONL files.
A numerical exception produces an explicit unresolved record and execution
continues. Mathematical formulations and solver code remain frozen.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import itertools
import json
import os
from pathlib import Path
import sys
import time

# Set before importing CVXPY, NumPy or the reference module.
for _key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
             "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "BLIS_NUM_THREADS"):
    os.environ[_key] = "1"

LAB = Path(__file__).resolve().parent
PREFIX = "code/minlp_solver_lab/"
TIME_LIMIT = 300
TOLERANCE = 1e-9


def _digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _metadata(manifest_path):
    expected_env = LAB / "lbesh_research/conic_reference_env/.venv"
    if Path(sys.prefix).resolve() != expected_env.resolve():
        raise RuntimeError(f"Use the pinned interpreter: {expected_env}/bin/python")
    manifest = json.loads(manifest_path.read_text())
    paths = ["lbesh_research/instances.py", "lbesh_research/conic_reference.py",
             "lbesh_research/conic_reference_env/uv.lock",
             "lbesh_research/conic_reference_env/pyproject.toml"]
    for path in paths:
        actual = _digest(LAB/path)
        if actual != manifest["files"][PREFIX+path]:
            raise RuntimeError(f"Frozen source/environment mismatch: {path}")
    versions = {p: importlib.metadata.version(p)
                for p in ("cvxpy", "clarabel", "numpy", "scipy", "pyomo")}
    for package, expected in (("cvxpy", "1.7.3"), ("clarabel", "0.11.1"), ("pyomo", "6.10.1")):
        if versions[package] != expected:
            raise RuntimeError(f"Unexpected {package} version: {versions[package]}")
    return dict(source_sha256={Path(p).name: _digest(LAB/p) for p in paths[:2]},
                environment_lock_sha256=_digest(LAB/paths[2]), versions=versions,
                batch_runner_sha256=_digest(__file__),
                frozen_manifest_sha256=_digest(manifest_path),
                started_at_utc=datetime.now(timezone.utc).isoformat(),
                tolerance=TOLERANCE, time_limit=TIME_LIMIT, threads=1,
                retry_policy="none")


def _run_one(name, modes, solver, metadata):
    start = time.perf_counter()
    try:
        row = solver(name, modes=modes, time_limit=TIME_LIMIT, tolerance=TOLERANCE)
    except Exception as exc:
        row = dict(name=name,
                   method="clarabel_exact_cone_root" if modes is None else "clarabel_fixed_assignment",
                   status="exception", obj=None, lb=None, witness={},
                   modes=None if modes is None else list(modes),
                   relax_integrality=modes is None, bound_certified=False,
                   bound_kind="floating_point_conic_dual_estimate",
                   time=time.perf_counter()-start, error_type=type(exc).__name__,
                   error=str(exc), **metadata)
    row["batch_metadata"] = metadata
    return row


def _enumerate(name, units, solver, metadata):
    start = time.perf_counter()
    rows = [_run_one(name, modes, solver, metadata)
            for modes in itertools.product(range(3), repeat=units)]
    feasible = [r for r in rows if r["status"] == "optimal"]
    unresolved = [r for r in rows if r["status"] not in ("optimal", "infeasible")]
    best = min(feasible, key=lambda r: r["obj"]) if feasible else None
    return dict(name=name, method="clarabel_exhaustive_cone_enumeration",
                status="unresolved" if unresolved else "optimal" if best else "infeasible",
                obj=best["obj"] if best else None,
                lb=min(r["lb"] for r in feasible) if feasible and not unresolved else None,
                bound_certified=False, bound_kind="floating_point_conic_dual_estimate",
                witness=best["witness"] if best else {}, modes=best["modes"] if best else None,
                time=time.perf_counter()-start, assignments=len(rows),
                unresolved_assignments=len(unresolved), rows=rows, batch_metadata=metadata)


def _write(stream, record):
    stream.write(json.dumps(record, allow_nan=False)+"\n")
    stream.flush()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path,
                        default=LAB/"results/lbesh_development/source_v1_manifest.json")
    parser.add_argument("--roots-out", required=True, type=Path)
    parser.add_argument("--enumeration-out", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true", help="Verify environment and print schedule without creating outputs or solving")
    args = parser.parse_args()
    metadata = _metadata(args.manifest)
    from lbesh_research.conic_reference import SUPPORTED_FAMILIES, solve
    from lbesh_research.instances import MANIFEST
    roots = [name for name, info in MANIFEST.items() if info["family"] in SUPPORTED_FAMILIES]
    small = [name for name in roots if MANIFEST[name]["size"] == "small"]
    if len(roots) != 42 or len(small) != 14 or any(MANIFEST[n]["units"] != 3 for n in small):
        raise RuntimeError("Frozen reference schedule must contain 42 roots and 14 three-unit enumerations")
    if args.roots_out.resolve() == args.enumeration_out.resolve():
        raise ValueError("Output paths must differ")
    for path in (args.roots_out, args.enumeration_out):
        if path.exists():
            raise FileExistsError(f"Output already exists; will not replace it: {path}")
    if args.dry_run:
        print(json.dumps(dict(roots=roots, enumerations=small, metadata=metadata), indent=2))
        return
    for path in (args.roots_out, args.enumeration_out):
        path.parent.mkdir(parents=True, exist_ok=True)
    # Open both exclusively before solving; partial runs are never overwritten.
    with args.roots_out.open("x") as root_stream, args.enumeration_out.open("x") as enum_stream:
        for name in roots:
            row = _run_one(name, None, solve, metadata)
            _write(root_stream, row)
            print(name, "root", row["status"], flush=True)
        for name in small:
            row = _enumerate(name, MANIFEST[name]["units"], solve, metadata)
            _write(enum_stream, row)
            print(name, "enumeration", row["status"], row["unresolved_assignments"], flush=True)


if __name__ == "__main__":
    main()
