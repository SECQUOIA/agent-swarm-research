"""Restore saved ignored inputs; optionally fetch and verify pinned OSIL models.

    python3 prepare_inputs.py [--download]
Existing files must have the recorded hash. A changed upstream file is rejected.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import tarfile
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true")
    args = parser.parse_args()
    manifest = json.loads((OUT / "manifest.json").read_text())
    archive = manifest["archives"][0]
    path = OUT / archive["path"]
    assert digest(path.read_bytes()) == archive["sha256"], "archive hash differs"
    members = {r["path"]: r for r in json.loads((OUT / archive["members_manifest"]).read_text())}
    restored = 0
    with tarfile.open(path) as tar:
        for member in tar:
            assert member.isfile() and member.name in members, member.name
            dst = (ROOT / member.name).resolve()
            assert dst.is_relative_to(ROOT), member.name
            record = members[member.name]
            data = tar.extractfile(member).read()
            assert digest(data) == record["sha256"], member.name
            if dst.exists():
                assert digest(dst.read_bytes()) == record["sha256"], f"existing file differs: {dst}"
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_bytes(data)
                restored += 1
    missing = []
    models = json.loads((OUT / manifest["osil_manifest"]).read_text())
    for record in models:
        dst = Path(os.path.expanduser(record["path"]))
        if not dst.exists() and args.download:
            request = urllib.request.Request(record["source"], headers={"User-Agent": "minlp-notes reproduction package"})
            with urllib.request.urlopen(request, timeout=300) as response:
                data = response.read()
            assert digest(data) == record["sha256"], f"upstream model differs: {record['name']}"
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(data)
            time.sleep(1)
        if dst.exists():
            assert digest(dst.read_bytes()) == record["sha256"], f"cache model differs: {record['name']}"
        else:
            missing.append(record["name"])
    print(json.dumps(dict(restored=restored, verified_osil=len(models) - len(missing), missing_osil=missing), indent=2))
    if missing:
        raise SystemExit("Missing pinned OSIL inputs; run again with --download.")


if __name__ == "__main__":
    main()
