#!/usr/bin/env python3
"""Inspect only the submitted archive wrapper, member hashes, and exclusions."""

import hashlib
import json
from pathlib import Path
import tarfile


base = Path(__file__).resolve().parent
archive = base / "evidence-companion.tar.gz"
digest = hashlib.sha256(archive.read_bytes()).hexdigest()
if digest != (base / "SHA256SUMS").read_text().split()[0]:
    raise ValueError("compressed archive checksum differs")
prefix = "quadratic-intersection-evidence/"
with tarfile.open(archive, "r:gz") as handle:
    members = handle.getmembers()
    manifest = json.load(handle.extractfile(prefix + "manifest.json"))
    entries = {entry["path"]: entry for entry in manifest["files"]}
    names = [member.name for member in members]
    if len(names) != len(set(names)) or set(names) != {prefix + name for name in entries} | {prefix + "manifest.json"}:
        raise ValueError("archive member set differs from manifest")
    for member in members:
        if not member.isfile() or (member.uid, member.gid, member.mtime, member.uname, member.gname) != (0, 0, 0, "", ""):
            raise ValueError(f"nonneutral member metadata: {member.name}")
        if not member.name.startswith(prefix) or ".." in Path(member.name).parts:
            raise ValueError("nonrelative archive member")
        if (member.name.endswith((".cip", ".osil", ".sol", ".solu", ".pdf", ".pyc"))
                or "/sources/" in member.name or "/old_solver/" in member.name
                or ("/scip-rule-fidelity/logs/runs_" in member.name and member.name.endswith(".jsonl.gz"))):
            raise ValueError(f"excluded asset class present: {member.name}")
        relative = member.name.removeprefix(prefix)
        if relative == "manifest.json":
            continue
        entry = entries[relative]
        if member.size != entry["bytes"] or hashlib.sha256(handle.extractfile(member).read()).hexdigest() != entry["sha256"]:
            raise ValueError(f"submitted member differs: {relative}")
print(f"PASS: {len(members)} neutral regular tar members; all submitted hashes match; excluded asset classes absent.")
print(f"PASS: compressed archive SHA-256 {digest}; {archive.stat().st_size} bytes.")
