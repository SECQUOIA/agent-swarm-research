#!/usr/bin/env python3
"""Check archive bytes and retained record metadata without experiment imports."""

from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def jsonl_records(path):
    opener = gzip.open if path.name.endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if line.strip():
                try:
                    yield json.loads(line)
                except ValueError as error:
                    raise ValueError(f"{path.name}:{line_number}: invalid JSON") from error


def record_metadata(path):
    if path.name.endswith((".jsonl", ".jsonl.gz")):
        kinds, statuses, count = Counter(), Counter(), 0
        for record in jsonl_records(path):
            count += 1
            if not isinstance(record, dict):
                kinds[type(record).__name__] += 1
                continue
            if "cert" in record:
                kinds["certificate_leaf"] += 1
            elif "facet_start" in record:
                kinds["facet_start"] += 1
            elif "facet_done" in record:
                kinds["facet_done"] += 1
            elif {"inst", "rule", "rounds"}.issubset(record):
                kinds["trajectory"] += 1
            else:
                kinds["other"] += 1
            if "status" in record:
                statuses[str(record["status"])] += 1
        return {"format": "jsonl", "records": count,
                "kinds": dict(sorted(kinds.items())),
                "statuses": dict(sorted(statuses.items()))}
    if path.suffix == ".json":
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        if isinstance(data, list):
            return {"format": "json", "array_items": len(data)}
        if isinstance(data, dict):
            result = {"format": "json", "list_lengths": {
                key: len(value) for key, value in sorted(data.items())
                if isinstance(value, list)}}
            if "status" in data:
                result["status"] = data["status"]
            if "blocks" in data and isinstance(data["blocks"], list):
                result["pieces"] = sum(len(block.get("pieces", []))
                                       for block in data["blocks"])
            return result
        return {"format": "json", "value_type": type(data).__name__}
    return None


def multiround_cohort(root, entries):
    prefix = "source/research-20261001/multiround/"
    paths = [entry["path"] for entry in entries
             if entry["path"].startswith((prefix + "logs/main/",
                                           prefix + "logs/new/"))
             and entry["path"].endswith(".jsonl")]
    caches = {}
    for size in ("4x4", "6x8", "8x12", "10x20"):
        with (root / (prefix + f"data/inst_{size}.json")).open() as handle:
            caches[size] = json.load(handle)["instances"]
    keys, baseline, statuses, rules = set(), set(), Counter(), Counter()
    count = 0
    for relative in paths:
        match = re.match(r"(?:main|new)_(\d+x\d+)_", Path(relative).name)
        if match is None:
            raise ValueError(f"unexpected trajectory name: {relative}")
        size = match.group(1)
        for record in jsonl_records(root / relative):
            key = (size, record["inst"], record["rule"])
            if key in keys:
                raise ValueError(f"duplicate trajectory: {key}")
            keys.add(key)
            count += 1
            statuses[record["status"]] += 1
            rules[record["rule"]] += 1
            cached = caches[size][record["inst"]]
            if (record["zlp"], record["zbil"]) != (cached["zlp"], cached["zbil"]):
                raise ValueError(f"denominator mismatch: {key}")
            if record["rule"] == "scip":
                baseline.add((size, record["inst"]))
    return {"files": len(paths), "trajectories": count,
            "baseline_instances": len(baseline),
            "baseline_by_size": dict(sorted(Counter(size for size, _ in baseline).items())),
            "statuses": dict(sorted(statuses.items())),
            "rules": dict(sorted(rules.items())),
            "cached_denominators_match": True}


def checked_path(root, relative):
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"nonrelative manifest path: {relative}")
    target = root / path
    if target.is_symlink() or not target.is_file():
        raise ValueError(f"missing regular file: {relative}")
    if not target.resolve().is_relative_to(root):
        raise ValueError(f"path outside archive: {relative}")
    return target


def survey_label_mapping(root, entries):
    mapping = json.loads((root / "survey-labels.json").read_text(encoding="utf-8"))
    expected_names = ["adv8_1", "adv8_4", "prop16_v2_1", "prop16_v8",
                      "supp1_1074", "supp1_3437", "supp1_4580", "supp1_5512"]
    records = mapping["records"]
    if [(row["label"], row["source_record_name"]) for row in records] != list(
            zip([f"R{i}" for i in range(1, 9)], expected_names)):
        raise ValueError("survey labels differ from the manuscript mapping")
    inventoried = {entry["path"] for entry in entries}

    def read_reference(reference):
        if reference["path"] not in inventoried:
            raise ValueError("survey reference is not inventoried")
        lines = checked_path(root, reference["path"]).read_text(encoding="utf-8").splitlines()
        line = reference["line"]
        if not isinstance(line, int) or line < 1 or line > len(lines):
            raise ValueError("survey reference has an invalid line number")
        record = json.loads(lines[line - 1])
        if any(record.get(key) != value for key, value in reference["selector"].items()):
            raise ValueError("survey source-record selector differs")
        return record

    total = 0
    for row in records:
        source = read_reference(row["coordinate_source"])
        if row["coordinates"] != {"sbar": source["sbar"], "P": source["P"]}:
            raise ValueError("survey coordinates differ from the retained source row")
        for reference in row["source_records"]:
            if read_reference(reference)["name"] != row["source_record_name"]:
                raise ValueError("survey record name differs")
            total += 1
        definition = row["coordinate_definition"]
        if definition["path"] not in inventoried:
            raise ValueError("coordinate-definition source is not inventoried")
        if "parameter_record" in definition:
            read_reference(definition["parameter_record"])
            if definition["constructor"]["path"] not in inventoried:
                raise ValueError("adversarial constructor is not inventoried")
    return {"labels": len(records), "named_survey_rows": total,
            "saved_coordinate_records_match": True}


def main():
    root = Path(__file__).resolve().parent
    with (root / "manifest.json").open(encoding="utf-8") as handle:
        manifest = json.load(handle)
    entries = manifest["files"]
    names = [entry["path"] for entry in entries]
    if len(names) != len(set(names)):
        raise ValueError("duplicate manifest paths")
    actual = {path.relative_to(root).as_posix()
              for path in root.rglob("*") if path.is_file()}
    if actual != set(names) | {"manifest.json"}:
        raise ValueError("archive file set differs from manifest")
    total_bytes = original_count = original_bytes = 0
    for entry in entries:
        path = checked_path(root, entry["path"])
        size = path.stat().st_size
        if size != entry["bytes"] or sha256(path) != entry["sha256"]:
            raise ValueError(f"byte/hash mismatch: {entry['path']}")
        if record_metadata(path) != entry.get("record_metadata"):
            raise ValueError(f"record metadata mismatch: {entry['path']}")
        if "original_path" in entry:
            original_count += 1
            original_bytes += size
            if entry["sha256"] != entry["original_sha256"]:
                export = entry.get("public_export", {})
                if (export.get("original_sha256") != entry["original_sha256"]
                        or export.get("sha256") != entry["sha256"]
                        or export.get("bytes") != size
                        or export.get("original_bytes") != entry.get("original_bytes")
                        or not isinstance(export.get("reason"), str)
                        or not export["reason"].strip()):
                    raise ValueError(f"original/public-export provenance mismatch: {entry['path']}")
        total_bytes += size
    if {"files": len(entries), "bytes": total_bytes,
        "original_files": original_count, "original_bytes": original_bytes} != manifest["totals"]:
        raise ValueError("manifest totals differ")
    cohort = multiround_cohort(root, entries)
    if cohort != manifest["cohorts"]["multiround_main_new"]:
        raise ValueError("multiround cohort differs")
    if (cohort["files"], cohort["trajectories"], cohort["baseline_instances"],
        cohort["baseline_by_size"], cohort["statuses"]) != (
            74, 5160, 220, {"4x4": 60, "6x8": 60, "8x12": 50, "10x20": 50}, {"ok": 5160}):
        raise ValueError("retained primary cohort does not match audited counts")
    completed = [entry for entry in entries
                 if entry["role"] == "completed-closure-box-certificate"]
    if len(completed) != 5 or any(entry["record_metadata"]["status"] != "complete"
                                or entry["record_metadata"]["list_lengths"]["queue"] != 0
                                for entry in completed):
        raise ValueError("closure completion metadata differs")
    labels = survey_label_mapping(root, entries)
    if labels != manifest["cohorts"]["closure_survey_labels"]:
        raise ValueError("survey-label mapping metadata differs")
    print(f"PASS: {len(entries)} files, {total_bytes} bytes; "
          f"{original_count} original-source files inventoried.")
    print("PASS: 74 primary trajectory files, 5160 trajectories, 220 baseline instances; "
          "cached denominators match.")
    print("PASS: R1–R8 map to 12 named survey rows; saved coordinates and source selectors match.")
    print("Checks cover bytes, record metadata, and cohort consistency; no solver or proof replay ran.")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, ValueError, OSError, TypeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
