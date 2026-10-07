"""Replay every recorded cut of a v3 output directory with the archived checker.

    replay_v3.py OUTPUT_DIR [--output OUTPUT_DIR/replay.json]

Runs ``replay_campaign`` of the archived
``research-20261003-convexification/experiments/replay.py``, loaded from the
output directory's verified snapshot copy, in this fresh process. The output
layout is that of campaign v2, so the archived function runs unchanged, with
one adaptation: its tampering controls are applied to the first cut of the
chosen record only. Every archived mutation edits that cut or a record-level
field, so the controls are the same; the full record has already passed the
untampered replay. This bounds the cost on records with hundreds of cuts.

v3 additions: each scheduled run has exactly one record; the recorded
effective Config equals the one the v3 mode defines (so cuts produced under
the raised all-diag limits are identified as such); and the tampering
controls are repeated on the first cut-bearing record of every mode.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def first_cut_only(record):
    return {**record, "cuts": record["cuts"][:1]}


def replay(out):
    started = time.perf_counter()
    snapshot = out / "snapshot"
    archived = load(snapshot / "research-20261003-convexification/experiments/replay.py", "archived_replay")
    full_tamper_checks = archived.tamper_checks
    archived.tamper_checks = lambda record, expected, support: full_tamper_checks(
        first_cut_only(record), expected, support)
    result = archived.replay_campaign(out)  # verifies the manifest, then imports from the snapshot
    from solver.integration import Config
    from solver.support import replay_support
    v3_worker = load(snapshot / "paper-certified-support-cuts/experiments/v3/v3_worker.py", "v3_worker")

    jobs = json.loads((out / "jobs.json").read_text())["jobs"]
    scheduled = [run["run_id"] for job in jobs for run in job["runs"]]
    records = [json.loads(line) for line in (out / "records.jsonl").read_text().splitlines() if line]
    ids = [r.get("run_id") for r in records]
    coverage = {"scheduled": len(scheduled), "recorded": len(records),
                "missing": sorted(set(scheduled) - set(ids)),
                "unscheduled": sorted(set(ids) - set(scheduled)),
                "duplicates": sorted({i for i in ids if ids.count(i) > 1})}

    cases, config_failures, controls = {}, [], {}
    by_run = {r["run_id"]: r for r in result["runs"]}
    for record in records:
        if "config" not in record:
            continue
        case = cases.setdefault(record["name"], json.loads((out / "cases" / (record["name"] + ".json")).read_text()))
        solver_mode, overrides = v3_worker.mode_config(record["mode"], case)
        if (record["config"] != asdict(Config(**overrides)) or record.get("solver_mode") != solver_mode
                or record.get("config_overrides") != overrides):
            config_failures.append(record["run_id"])
        mode = record["mode"]
        if (mode not in controls and record.get("cuts") and by_run.get(record["run_id"], {}).get("passed")):
            expected = archived.load_expected_model(case, snapshot)
            trimmed = first_cut_only(record)
            untampered = archived.check_run(trimmed, expected, replay_support)["passed"]
            controls[mode] = {"run_id": record["run_id"], "cuts_in_record": len(record["cuts"]),
                              "untampered_first_cut_passed": untampered,
                              "rejections": full_tamper_checks(trimmed, expected, replay_support)}
    controls_passed = all(c["untampered_first_cut_passed"] and all(c["rejections"].values())
                          for c in controls.values())
    coverage_passed = not (coverage["missing"] or coverage["unscheduled"] or coverage["duplicates"])
    cut_modes = sorted({r["mode"] for r in records if r.get("cuts")})
    v3 = {"coverage": coverage, "coverage_complete": coverage_passed,
          "config_checked_runs": sum("config" in r for r in records),
          "config_failures": config_failures, "modes_with_cuts": cut_modes,
          "tamper_controls_by_mode": controls,
          "tamper_controls_cover_all_cut_modes": sorted(controls) == cut_modes,
          "tamper_scope": "archived mutations applied to the first cut of the record"}
    archived_passed = result["passed"]
    result.update(archived_passed=archived_passed, v3=v3,
                  passed=bool(archived_passed and not config_failures and controls_passed
                              and sorted(controls) == cut_modes),
                  wrapper_seconds=time.perf_counter() - started,
                  wrapper_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    out = args.output_dir.resolve()
    target = args.output or out / "replay.json"
    result = replay(out)
    target.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({k: result[k] for k in ("passed", "archived_passed", "records", "bound_runs",
                                              "cuts", "replayed_cuts", "replay_seconds")}
                     | {"coverage_complete": result["v3"]["coverage_complete"],
                        "config_failures": len(result["v3"]["config_failures"]),
                        "tamper_modes": sorted(result["v3"]["tamper_controls_by_mode"])}))
    raise SystemExit(0 if result["passed"] else 1)
