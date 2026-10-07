#!/usr/bin/env python3
"""Validate the companion wrapper, then its solver-free evidence metadata."""

import hashlib
import json
from pathlib import Path
import runpy
import sys


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def main():
    root = Path(__file__).resolve().parent
    with (root / "manifest.json").open(encoding="utf-8") as handle:
        manifest = json.load(handle)
    names = [entry["path"] for entry in manifest["files"]]
    actual = {path.name for path in root.iterdir() if path.is_file()}
    if len(names) != len(set(names)) or actual != set(names) | {"manifest.json"}:
        raise ValueError("top-level file set differs from manifest")
    for entry in manifest["files"] + [manifest["payload_manifest"]]:
        relative = Path(entry["path"])
        path = root / relative
        if relative.is_absolute() or ".." in relative.parts or path.is_symlink() or not path.is_file():
            raise ValueError(f"invalid regular-file path: {entry['path']}")
        if path.stat().st_size != entry["bytes"] or digest(path) != entry["sha256"]:
            raise ValueError(f"wrapper hash differs: {entry['path']}")
    payload_path = root / manifest["payload_manifest"]["path"]
    with payload_path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if payload["totals"] != manifest["payload_totals"]:
        raise ValueError("payload totals differ from wrapper")
    print(f"PASS: {len(names)} companion wrapper files and payload-manifest hash.")
    # This entry point is the standalone stdlib metadata checker, not source code.
    runpy.run_path(str(payload_path.parent / "check_manifest.py"), run_name="__main__")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, ValueError, OSError, TypeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
