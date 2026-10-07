"""Paths, hashing and no-overwrite file helpers shared by the campaign-5 runner scripts."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parents[1]
REPO = PAPER.parent
V3 = PAPER / "experiments/v3"
V3D = PAPER / "experiments/v3d"
V4 = PAPER / "experiments/v4"
TOPIC_NAME = "research-20261003-convexification"
DEPENDENCY_NAME = "research-20261002-convexification"
SNAPSHOT = HERE / "snapshot"
SNAPSHOT_MANIFEST = SNAPSHOT / "source-manifest.json"
PYTHON = REPO / "code/minlp_solver_lab/.venv/bin/python"
THREAD_ENV = {k: "1" for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS",
                              "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS",
                              "BLIS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")}
GLOBAL_SLOTS = 6
# Runner scripts of campaign 5 that are frozen into the snapshot (listed, not
# globbed: other campaign-5 files in this directory are not part of it).
RUNNER_FILES = ("common.py", "snapshot.py", "make_jobs.py", "mechanism.py", "stars.py", "v5_worker.py",
                "driver.py", "replay_v5.py", "summarize_v5.py", "test_v5.py")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def text(value):
    return json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"


def write_new(path, value):
    """Atomically create a JSON file; never replace an existing one."""
    path = Path(path)
    temporary = path.with_name(path.name + f".tmp{os.getpid()}")
    temporary.write_text(text(value))
    try:
        os.link(temporary, path)
    finally:
        temporary.unlink()


def verify_manifest(root, manifest):
    """Return the relative paths whose bytes differ from the manifest."""
    root = Path(root)
    return [relative for relative, expected in sorted(manifest.items())
            if not (root / relative).is_file() or digest(root / relative) != expected]


def load_snapshot_manifest():
    if not SNAPSHOT_MANIFEST.is_file():
        raise SystemExit(f"no snapshot at {SNAPSHOT}; run snapshot.py first")
    manifest = json.loads(SNAPSHOT_MANIFEST.read_text())
    mismatches = verify_manifest(SNAPSHOT, manifest)
    if mismatches:
        raise SystemExit("snapshot differs from its manifest: " + ", ".join(mismatches))
    return manifest
