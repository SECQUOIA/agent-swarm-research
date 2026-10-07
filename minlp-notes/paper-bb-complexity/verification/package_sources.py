#!/usr/bin/env python3
"""Package checked, reachable submission sources with exact SHA256 hashes."""

import argparse
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import zipfile

from check_sources import ROOT, check


def package(root, output):
    root = root.resolve()
    report = check(root)
    build = root / "BUILD.txt"
    if not build.is_file() or build.is_symlink():
        report.errors.append("BUILD.txt: missing regular file with standalone build instructions")
    if report.errors:
        for error in report.errors:
            print(error, file=sys.stderr)
        return 1
    report.files.add("BUILD.txt")
    report.dependencies.append({"from": "submission", "to": "BUILD.txt", "kind": "build instructions"})
    payloads = {name: (root / name).read_bytes() for name in sorted(report.files)}
    payloads["dependencies.json"] = (json.dumps(report.manifest(), indent=2) + "\n").encode("utf-8")
    payloads["SHA256SUMS"] = "".join(
        f"{hashlib.sha256(data).hexdigest()}  {name}\n" for name, data in sorted(payloads.items())
    ).encode("utf-8")
    output = output.resolve()
    if output in {root / name for name in payloads}:
        print("Output would overwrite a submission source", file=sys.stderr)
        return 1
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=output.parent, suffix=".zip", delete=False) as temp:
        temporary = Path(temp.name)
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, data in sorted(payloads.items()):
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, data)
        # Verify the actual ZIP bytes before publishing the archive.
        with zipfile.ZipFile(temporary) as archive:
            for name, expected in payloads.items():
                if archive.read(name) != expected:
                    raise ValueError(f"archive verification failed for {name}")
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    print(f"PACKAGE=ok: {output}, {len(payloads)} members")
    print(f"ARCHIVE_SHA256={hashlib.sha256(output.read_bytes()).hexdigest()}")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="manuscript directory")
    parser.add_argument("--output", type=Path, help="ZIP path; default: ROOT/delivery/bb-complexity-sources.zip")
    args = parser.parse_args()
    output = args.output or args.root / "delivery" / "bb-complexity-sources.zip"
    try:
        return package(args.root, output)
    except (OSError, UnicodeError, ValueError, zipfile.BadZipFile) as exc:
        print(f"Packaging failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
