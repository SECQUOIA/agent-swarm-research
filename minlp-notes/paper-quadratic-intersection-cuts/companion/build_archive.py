#!/usr/bin/env python3
"""Package the approved source selection; do not execute experiment code."""

import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tarfile


HERE = Path(__file__).resolve().parent
ROOT = Path.cwd()
ARCHIVE = HERE / "archive"
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("archive_metadata", ARCHIVE / "check_manifest.py")
metadata = importlib.util.module_from_spec(spec)
spec.loader.exec_module(metadata)


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def original_role(path):
    if "/code/" in path or path.endswith((".py", ".sh", ".set", ".patch", ".diff")):
        return "original-code"
    if "/ratio-bound/logs/" in path and Path(path).name.startswith("leaves_"):
        return "completed-ratio-box-certificate"
    if "/orbit-closure/logs/boxcert_" in path and path.endswith(".json"):
        return "completed-closure-box-certificate"
    if path.endswith(("closure_cert_prop16_A.json", "closure_cert_thm14_A.json",
                      "closure_cert_wcorner_A_A.json", "closure_lower_prop16_cuts.json")):
        return "completed-saved-certificate-data"
    if "/multiround/data/" in path:
        return "generated-instance-and-denominator-cache"
    return "numerical-or-diagnostic-record"


with (HERE / "selected-sources.json").open() as handle:
    selection = json.load(handle)
entries = []
for selected in selection["files"]:
    original = ROOT / selected["path"]
    if original.stat().st_size != selected["bytes"]:
        raise ValueError(f"source size changed: {selected['path']}")
    digest = metadata.sha256(original)
    if digest != selected["sha256"]:
        raise ValueError(f"approved source hash changed: {selected['path']}")
    target = ARCHIVE / "source" / selected["path"]
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        shutil.copyfile(original, target)
    if metadata.sha256(target) != digest:
        raise ValueError(f"copy differs: {selected['path']}")
    record = {"path": target.relative_to(ARCHIVE).as_posix(),
              "original_path": selected["path"], "bytes": selected["bytes"],
              "sha256": digest, "original_sha256": digest,
              "role": original_role(selected["path"])}
    counts = metadata.record_metadata(target)
    if counts is not None:
        record["record_metadata"] = counts
    entries.append(record)

with (ROOT / "artifacts/manifest.json").open() as handle:
    artifacts = json.load(handle)
raw = next(package for package in artifacts["packages"]
           if package["id"] == "scip-fidelity-traces")
references = {
    "description": "Neutral references to omitted source context and optional raw traces.",
    "license_status": "No redistribution license added.",
    "source_context_omitted": [dict(row, sha256=metadata.sha256(ROOT / row["path"]))
                                for row in selection["omitted_context"]],
    "optional_raw_fidelity_archive": {
        key: raw[key] for key in ("id", "archive", "archive_bytes", "archive_sha256",
                                 "assets", "member_count", "uncompressed_bytes")},
    "original_restoration_references": ["artifacts/manifest.json", "artifacts/README.md"],
    "restoration_note": "The repository references give original retrieval sources; "
                        "no author URL is repeated in this wrapper.",
    "exclusions": ["third-party literature PDFs and text", "benchmark inputs and solutions",
                   "solver binaries, licenses, and environments", "raw fidelity traces",
                   "optional full-detail multiround diagnostic trajectories",
                   "incomplete closure checkpoints", "superseded minor old_solver records",
                   "bulky per-run solver logs", "source notes and closeout documents"],
    "identity_note": "Original-byte sources may contain names, URLs, or absolute paths. "
                     "This archive is not certified anonymized."
}
write_json(ARCHIVE / "neutral-reference.json", references)
for name in ("README.md", "check_manifest.py", "neutral-reference.json", "survey-labels.json"):
    target = ARCHIVE / name
    entry = {"path": name, "bytes": target.stat().st_size,
             "sha256": metadata.sha256(target), "role": "archive-wrapper"}
    counts = metadata.record_metadata(target)
    if counts is not None:
        entry["record_metadata"] = counts
    entries.append(entry)
entries.sort(key=lambda entry: entry["path"])
manifest = {"schema_version": 1,
            "description": "Original-byte evidence with file and retained-record metadata.",
            "verification_scope": "Hashes, record metadata, and cohort consistency only; "
                                  "no solver execution or mathematical replay.",
            "files": entries,
            "totals": {"files": len(entries),
                       "bytes": sum(entry["bytes"] for entry in entries),
                       "original_files": len(selection["files"]),
                       "original_bytes": sum(row["bytes"] for row in selection["files"])},
            "cohorts": {"multiround_main_new": metadata.multiround_cohort(ARCHIVE, entries),
                        "closure_survey_labels": metadata.survey_label_mapping(ARCHIVE, entries)}}
write_json(ARCHIVE / "manifest.json", manifest)

# Names, owners, permissions, and timestamps in the tar wrapper are neutral.
target = HERE / "evidence-companion.tar.gz"
with target.open("wb") as raw_handle:
    with gzip.GzipFile(filename="", mode="wb", fileobj=raw_handle, mtime=0) as compressed:
        with tarfile.open(mode="w", fileobj=compressed, format=tarfile.PAX_FORMAT) as bundle:
            for path in sorted(ARCHIVE.rglob("*")):
                if not path.is_file():
                    continue
                name = "quadratic-intersection-evidence/" + path.relative_to(ARCHIVE).as_posix()
                info = bundle.gettarinfo(str(path), arcname=name)
                info.uid = info.gid = info.mtime = 0
                info.uname = info.gname = ""
                info.mode = 0o644
                info.pax_headers = {}
                with path.open("rb") as handle:
                    bundle.addfile(info, handle)
digest = metadata.sha256(target)
(HERE / "SHA256SUMS").write_text(f"{digest}  {target.name}\n", encoding="utf-8")
wrapper = []
for path in sorted(HERE.iterdir()):
    if path.is_file() and path.name != "manifest.json":
        wrapper.append({"path": path.name, "bytes": path.stat().st_size,
                        "sha256": metadata.sha256(path)})
payload_manifest = ARCHIVE / "manifest.json"
write_json(HERE / "manifest.json", {
    "schema_version": 1,
    "description": "Companion wrapper and reference to the original-byte payload inventory.",
    "files": wrapper,
    "payload_manifest": {"path": "archive/manifest.json",
                         "bytes": payload_manifest.stat().st_size,
                         "sha256": metadata.sha256(payload_manifest)},
    "payload_totals": manifest["totals"],
    "verification_scope": "Wrapper hashes and solver-free payload record metadata only."})
print(json.dumps({"original_files": len(selection["files"]),
                  "original_bytes": manifest["totals"]["original_bytes"],
                  "archive_bytes": target.stat().st_size,
                  "archive_sha256": digest}, sort_keys=True))
