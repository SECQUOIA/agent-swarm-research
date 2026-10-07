#!/usr/bin/env python3
"""Export all archived campaign ledgers, or verify their compact Git copies."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path

from R10_numbers_extract import extract

EXPERIMENTS = Path(__file__).resolve().parents[1] / "experiments"
DESTINATION = EXPERIMENTS / "compact"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def export():
    DESTINATION.mkdir(exist_ok=True)
    if (DESTINATION / "manifest.json").exists():
        raise SystemExit("compact/manifest.json already exists; preserve it before regenerating")
    entries = []
    for campaign in ("v3", "v3d", "v4", "v5"):
        for source in sorted((EXPERIMENTS / campaign).rglob("records.jsonl")):
            part = source.parent.relative_to(EXPERIMENTS).as_posix()
            output = DESTINATION / (part.replace("/", "_") + ".jsonl.gz")
            if output.exists():
                raise SystemExit(f"refusing to overwrite {output}")
            entry = extract(part, output)
            entry.update(file=output.name, sha256=sha256(output), bytes=output.stat().st_size)
            entries.append(entry)
    manifest = {"schema": "support-cuts-compact-v1",
                "extractor": "verification/R10_numbers_extract.py",
                "extractor_sha256": sha256(Path(__file__).with_name("R10_numbers_extract.py")),
                "scope": "All saved v3/v3d/v4/v5 ledgers, including smoke tests and diagnostic reruns. Full witnesses remain in raw archives.",
                "exports": entries}
    (DESTINATION / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    verify()


def verify():
    manifest = json.loads((DESTINATION / "manifest.json").read_text())
    total_records = total_cuts = total_bytes = 0
    for entry in manifest["exports"]:
        path = DESTINATION / entry["file"]
        if sha256(path) != entry["sha256"] or path.stat().st_size != entry["bytes"]:
            raise SystemExit(f"compact export hash/size mismatch: {path}")
        ids, statuses, cuts, records = set(), Counter(), 0, 0
        with gzip.open(path, "rt", encoding="utf-8") as source:
            for line in source:
                record = json.loads(line)
                identity = record.get("run_id") or record["name"]
                if identity in ids:
                    raise SystemExit(f"duplicate run/model ID in {path}: {identity}")
                ids.add(identity)
                if record["n_cuts"] != len(record["cuts"]):
                    raise SystemExit(f"cut-count mismatch in {path}: {record['run_id']}")
                statuses[str(record.get("status"))] += 1
                cuts += record["n_cuts"]
                records += 1
        if (records, cuts, dict(statuses)) != (entry["records"], entry["cuts"], entry["statuses"]):
            raise SystemExit(f"compact export totals mismatch: {path}")
        total_records += records
        total_cuts += cuts
        total_bytes += entry["bytes"]
    print(f"Verified {len(manifest['exports'])} exports: {total_records} records, {total_cuts} cuts, {total_bytes:,} compressed bytes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="check saved exports without reading raw campaigns")
    arguments = parser.parse_args()
    verify() if arguments.verify else export()
