"""Replay every recorded cut of a campaign-5 output directory with the archived checker.

    replay_v5.py OUTPUT_DIR [--output OUTPUT_DIR/replay.json]

Copied from the campaign-4 wrapper (v4/replay_v4.py) and extended to the
campaign-5 modes. It runs ``replay_campaign`` of the archived
``research-20261003-convexification/experiments/replay.py`` from the output
directory's verified snapshot copy (star cuts are replayed there by the
inherited ``replay_support``, method ``quadratic_star``), with tampering
controls applied to the first cut of the chosen record (every archived
mutation edits that cut or a record-level field).

Campaign-4 checks, kept: each scheduled run has exactly one record; for every
SCIP record the recorded effective Config, solver mode, Config overrides and
SCIP parameters equal those of the mode (``v5_worker.mode_config``), and so do
the parameter values SCIP reported after the solve; every Gurobi record has no
cuts and no original-model block and its Gurobi parameters equal the mode's;
the tampering controls are repeated on the first cut-bearing record of every
cut mode.

Campaign-5 checks: for every cut mode with star cuts (certificate method
``quadratic_star``), the first star cut of the first passing record with one
gets the archived mutations and four star-specific mutations (star certificate
bound, a piece polynomial, the star center, the exported lower bound); each
must be rejected. Every record's ``cut_methods`` must equal the methods of its
cut witnesses.
"""
from __future__ import annotations

import argparse
from collections import Counter
import copy
from dataclasses import asdict
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from pathlib import Path
import time

STAR = "quadratic_star"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def first_cut_only(record):
    return {**record, "cuts": record["cuts"][:1]}


def only_cut(record, index):
    return {**record, "cuts": [record["cuts"][index]]}


def bump(value):
    return str(Q(value) + 1)


STAR_MUTATIONS = {
    "star_certificate_bound": lambda w: w["proof"]["star"].__setitem__("bound", bump(w["proof"]["star"]["bound"])),
    "star_piece_polynomial": lambda w: w["proof"]["star"]["pieces"][0]["polynomial"].__setitem__(
        0, bump(w["proof"]["star"]["pieces"][0]["polynomial"][0])),
    "star_center": lambda w: w["proof"].__setitem__("center", (w["proof"]["center"] + 1) % w["model"]["dimension"]),
    "support_lower_bound": lambda w: w.__setitem__("lower_bound", bump(w["lower_bound"])),
}


def star_tamper_checks(archived, full_tamper_checks, record, expected, replay_support):
    """Archived mutations plus star-certificate mutations on a one-cut record; True = rejected."""
    results = dict(full_tamper_checks(record, expected, replay_support))
    for name, mutate in STAR_MUTATIONS.items():
        data = copy.deepcopy(record)
        mutate(data["cuts"][0]["support_witness"])
        results[name] = not archived.check_run(data, expected, replay_support)["passed"]
    return results


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
    worker = load(snapshot / "paper-certified-support-cuts/experiments/v5/v5_worker.py", "v5_worker")

    jobs = json.loads((out / "jobs.json").read_text())["jobs"]
    scheduled = {run["run_id"]: run["mode"] for job in jobs for run in job["runs"]}
    records = [json.loads(line) for line in (out / "records.jsonl").read_text().splitlines() if line]
    ids = [r.get("run_id") for r in records]
    coverage = {"scheduled": len(scheduled), "recorded": len(records),
                "missing": sorted(set(scheduled) - set(ids)),
                "unscheduled": sorted(set(ids) - set(scheduled)),
                "duplicates": sorted({i for i in ids if ids.count(i) > 1})}

    cases, config_failures, gurobi_failures, method_failures = {}, [], [], []
    controls, star_controls = {}, {}
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
        methods = [c["support_witness"]["method"] for c in record.get("cuts") or []]
        if record.get("cut_methods") != dict(Counter(methods)):
            method_failures.append(record["run_id"])
        if not record.get("cuts") or not by_run.get(record["run_id"], {}).get("passed"):
            continue
        expected = None
        if mode not in controls:
            expected = archived.load_expected_model(case, snapshot)
            trimmed = first_cut_only(record)
            controls[mode] = {"run_id": record["run_id"], "cuts_in_record": len(record["cuts"]),
                              "first_cut_method": methods[0],
                              "untampered_first_cut_passed": archived.check_run(trimmed, expected, replay_support)["passed"],
                              "rejections": full_tamper_checks(trimmed, expected, replay_support)}
        if mode not in star_controls and STAR in methods:
            expected = expected or archived.load_expected_model(case, snapshot)
            index = methods.index(STAR)
            trimmed = only_cut(record, index)
            star_controls[mode] = {"run_id": record["run_id"], "cut_index": index,
                                   "block_dimension": len(record["cuts"][index]["variables"]),
                                   "untampered_cut_passed": archived.check_run(trimmed, expected, replay_support)["passed"],
                                   "rejections": star_tamper_checks(archived, full_tamper_checks, trimmed,
                                                                    expected, replay_support)}
    controls_passed = all(c["untampered_first_cut_passed"] and all(c["rejections"].values())
                          for c in controls.values())
    star_passed = all(c["untampered_cut_passed"] and all(c["rejections"].values()) for c in star_controls.values())
    coverage_passed = not (coverage["missing"] or coverage["unscheduled"] or coverage["duplicates"])
    cut_modes = sorted({r["mode"] for r in records if r.get("cuts")})
    star_modes = sorted({r["mode"] for r in records
                         if any(c["support_witness"]["method"] == STAR for c in r.get("cuts") or [])})
    v5 = {"coverage": coverage, "coverage_complete": coverage_passed,
          "config_checked_runs": sum("config" in r for r in records),
          "config_failures": config_failures, "cut_method_failures": method_failures,
          "gurobi_checked_runs": sum(r["mode"] == "gurobi" and "gurobi_params" in r for r in records),
          "gurobi_failures": gurobi_failures, "modes_with_cuts": cut_modes, "modes_with_star_cuts": star_modes,
          "cuts_by_method": dict(Counter(c["support_witness"]["method"] for r in records for c in r.get("cuts") or [])),
          "tamper_controls_by_mode": controls,
          "tamper_controls_cover_all_cut_modes": sorted(controls) == cut_modes,
          "star_tamper_controls_by_mode": star_controls,
          "star_tamper_controls_cover_all_star_modes": sorted(star_controls) == star_modes,
          "tamper_scope": "archived mutations applied to the first cut of the record; star controls: the "
                          "first star cut of the record, archived and star-certificate mutations"}
    archived_passed = result["passed"]
    result.update(archived_passed=archived_passed, v5=v5,
                  passed=bool(archived_passed and not config_failures and not gurobi_failures
                              and not method_failures and controls_passed and star_passed
                              and sorted(controls) == cut_modes and sorted(star_controls) == star_modes),
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
                     | {"coverage_complete": result["v5"]["coverage_complete"],
                        "config_failures": len(result["v5"]["config_failures"]),
                        "cut_method_failures": len(result["v5"]["cut_method_failures"]),
                        "gurobi_failures": len(result["v5"]["gurobi_failures"]),
                        "cuts_by_method": result["v5"]["cuts_by_method"],
                        "tamper_modes": sorted(result["v5"]["tamper_controls_by_mode"]),
                        "star_tamper_modes": sorted(result["v5"]["star_tamper_controls_by_mode"])}))
    raise SystemExit(0 if result["passed"] else 1)
