"""Replay every recorded cut of a campaign-4 output directory with the archived checker.

    replay_v4.py OUTPUT_DIR [--output OUTPUT_DIR/replay.json]

Copied from the campaign-3 wrapper (v3/replay_v3.py) and extended to the
campaign-4 modes. It runs ``replay_campaign`` of the archived
``research-20261003-convexification/experiments/replay.py`` from the output
directory's verified snapshot copy, with tampering controls applied to the
first cut of the chosen record (every archived mutation edits that cut or a
record-level field).

Campaign-4 checks: each scheduled run has exactly one record; for every SCIP
record the recorded effective Config, solver mode, Config overrides and SCIP
parameters equal those of the mode (``v4_worker.mode_config``), and so do the
parameter values SCIP reported after the solve; every Gurobi record has no
cuts and no original-model block (the archived replay lists it among the
omitted runs) and its Gurobi parameters equal the mode's; the tampering
controls are repeated on the first cut-bearing record of every cut mode.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import importlib.util
import json
from pathlib import Path
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
    worker = load(snapshot / "paper-certified-support-cuts/experiments/v4/v4_worker.py", "v4_worker")

    jobs = json.loads((out / "jobs.json").read_text())["jobs"]
    scheduled = {run["run_id"]: run["mode"] for job in jobs for run in job["runs"]}
    records = [json.loads(line) for line in (out / "records.jsonl").read_text().splitlines() if line]
    ids = [r.get("run_id") for r in records]
    coverage = {"scheduled": len(scheduled), "recorded": len(records),
                "missing": sorted(set(scheduled) - set(ids)),
                "unscheduled": sorted(set(ids) - set(scheduled)),
                "duplicates": sorted({i for i in ids if ids.count(i) > 1})}

    cases, config_failures, gurobi_failures, controls = {}, [], [], {}
    by_run = {r["run_id"]: r for r in result["runs"]}
    for record in records:
        mode = record["mode"]
        if scheduled.get(record["run_id"]) != mode:
            config_failures.append(record["run_id"])
            continue
        if mode == "gurobi":
            if record.get("status") == "worker_error" or "gurobi_params" not in record:
                continue  # a failed run; reported by the summarizer
            params = dict(record["gurobi_params"])
            params.pop("TimeLimit", None)
            if (record.get("cuts") != [] or "original_model" in record or record.get("solver_mode") != "gurobi"
                    or params != {**worker.GUROBI_PARAMS, "Seed": record["seed"]}):
                gurobi_failures.append(record["run_id"])
            continue
        if "config" not in record:
            continue
        case = cases.setdefault(record["name"], json.loads((out / "cases" / (record["name"] + ".json")).read_text()))
        solver_mode, overrides, params = worker.mode_config(mode, case)
        effective = (record.get("native_statistics") or {}).get("scip_params_effective")
        if (record["config"] != asdict(Config(**overrides)) or record.get("solver_mode") != solver_mode
                or record.get("config_overrides") != overrides or record.get("scip_params") != params
                or (effective is not None and effective != params)):
            config_failures.append(record["run_id"])
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
    v4 = {"coverage": coverage, "coverage_complete": coverage_passed,
          "config_checked_runs": sum("config" in r for r in records),
          "config_failures": config_failures,
          "gurobi_checked_runs": sum(r["mode"] == "gurobi" and "gurobi_params" in r for r in records),
          "gurobi_failures": gurobi_failures, "modes_with_cuts": cut_modes,
          "tamper_controls_by_mode": controls,
          "tamper_controls_cover_all_cut_modes": sorted(controls) == cut_modes,
          "tamper_scope": "archived mutations applied to the first cut of the record"}
    archived_passed = result["passed"]
    result.update(archived_passed=archived_passed, v4=v4,
                  passed=bool(archived_passed and not config_failures and not gurobi_failures
                              and controls_passed and sorted(controls) == cut_modes),
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
                     | {"coverage_complete": result["v4"]["coverage_complete"],
                        "config_failures": len(result["v4"]["config_failures"]),
                        "gurobi_failures": len(result["v4"]["gurobi_failures"]),
                        "tamper_modes": sorted(result["v4"]["tamper_controls_by_mode"])}))
    raise SystemExit(0 if result["passed"] else 1)
