"""Freeze the solver, checker and runner sources for campaign v3.

Copies the live sources into ``v3/snapshot/`` (same relative layout as the
repository, as campaign v2 did) and writes ``source-manifest.json`` with the
SHA-256 of every copied file. Refuses to overwrite an existing snapshot.
"""
from __future__ import annotations

import importlib.metadata
import json
import os
import platform
import shutil
import sys
import time

from common import (DEPENDENCY_NAME, HERE, PAPER, REPO, SNAPSHOT, SNAPSHOT_MANIFEST,
                    TOPIC_NAME, digest, write_new)

INTEGRATION_SHA256_PREFIX = "128fe10b"  # campaign-v3-protocol.md, Code


def sources():
    topic, dependency = REPO / TOPIC_NAME, REPO / DEPENDENCY_NAME
    paths = []
    for directory in (topic / "solver", topic / "theory", topic / "reviews",
                      dependency / "solver", dependency / "theory",
                      REPO / "code/univariate_envelopes/uenv"):
        paths += [p for p in directory.rglob("*") if p.is_file() and p.suffix in (".py", ".c")
                  and "__pycache__" not in p.parts]
    paths += [topic / "experiments" / name for name in
              ("cases.py", "worker.py", "replay.py", "run_campaign.py", "summarize.py",
               "holdout-selection.json", "protocol.md")]
    paths += [dependency / "requirements.txt",
              REPO / "code/minlp_solver_lab/instances/instancedata.csv",
              PAPER / "experiments/campaign-v3-protocol.md",
              PAPER / "experiments/mechanism-protocol.md"]
    paths += sorted(HERE.glob("*.py"))
    return sorted(set(paths))


def main():
    integration = REPO / TOPIC_NAME / "solver/integration.py"
    if not digest(integration).startswith(INTEGRATION_SHA256_PREFIX):
        raise SystemExit(f"{integration} hash does not match the protocol ({INTEGRATION_SHA256_PREFIX}...)")
    SNAPSHOT.mkdir(exist_ok=False)
    hashes = {}
    for source in sources():
        relative = source.relative_to(REPO)
        target = SNAPSHOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        hashes[str(relative)] = digest(target)
        if hashes[str(relative)] != digest(source):
            raise SystemExit(f"{source} changed while it was copied")
    write_new(SNAPSHOT / "snapshot-info.json", {
        "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "python": sys.version, "executable": sys.executable, "platform": platform.platform(),
        "logical_cpus": os.cpu_count(),
        "packages": {p: importlib.metadata.version(p) for p in
                     ("numpy", "scipy", "sympy", "python-flint", "pyscipopt")},
        "integration_sha256": hashes[f"{TOPIC_NAME}/solver/integration.py"],
        "files": len(hashes)})
    write_new(SNAPSHOT_MANIFEST, hashes)
    print(json.dumps({"snapshot": str(SNAPSHOT), "files": len(hashes),
                      "integration_sha256": hashes[f"{TOPIC_NAME}/solver/integration.py"]}))


if __name__ == "__main__":
    main()
