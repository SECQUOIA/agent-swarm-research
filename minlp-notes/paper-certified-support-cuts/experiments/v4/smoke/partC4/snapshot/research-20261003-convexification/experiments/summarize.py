"""Summarize the frozen campaign without dropping unfavorable records."""
from __future__ import annotations

import argparse
from collections import Counter
import json
import math
from pathlib import Path
import statistics

MODES = ("baseline", "all", "auto")


def good(record):
    if record.get("status") not in ("optimal", "gaplimit", "timelimit", "nodelimit",
                                    "stallnodelimit", "totalnodelimit", "infeasible", "unbounded",
                                    "inforunbd", "userinterrupt", "memlimit", "sollimit",
                                    "bestsollimit", "restartlimit"):
        return False
    if record.get("worker_status") or record.get("returncode", 0) != 0:
        return False
    primal = record.get("primal_check")
    reference = record.get("reference_check")
    if not isinstance(primal, dict) or primal.get("checked") not in (True, False):
        return False
    if primal["checked"] and primal.get("passed") is not True:
        return False
    if not primal["checked"] and record.get("primal") is not None:
        return False
    if not isinstance(reference, dict) or reference.get("checked") not in (True, False):
        return False
    if reference["checked"] and (reference.get("dual_consistent") is not True or
                                 reference.get("root_dual_consistent") is not True):
        return False
    return True


def solved(record):
    return (good(record) and record["status"] in ("optimal", "gaplimit")
            and record.get("primal_check", {}).get("checked") is True
            and record.get("primal_check", {}).get("passed") is True
            and isinstance(record.get("primal"), (float, int)) and math.isfinite(record["primal"]))


def compare(records, suite, phase, mode, baseline="baseline"):
    selected = {r["name"]: r for r in records if r["suite"] == suite and r["phase"] == phase and r["mode"] == mode}
    reference = {r["name"]: r for r in records if r["suite"] == suite and r["phase"] == phase and r["mode"] == baseline}
    outcomes = Counter()
    rows = []
    for name in sorted(selected.keys() & reference.keys()):
        a, b = selected[name], reference[name]
        da, db = a.get("dual"), b.get("dual")
        if not good(a) or not good(b) or not isinstance(da, (int, float)) or not isinstance(db, (int, float)) or not math.isfinite(da) or not math.isfinite(db):
            outcome = "unavailable_or_flagged"
        else:
            sign = 1 if a["sense"] == "min" else -1
            improvement = sign * (da - db)
            tol = 1e-6 * max(1, abs(da), abs(db))
            outcome = "better" if improvement > tol else "worse" if improvement < -tol else "tie"
        outcomes[outcome] += 1
        rows.append({"name": name, "outcome": outcome, "dual": da, "baseline_dual": db,
                     "status": a["status"], "baseline_status": b["status"],
                     "cuts": len(a["cuts"]) if isinstance(a.get("cuts"), list) else None,
                     "solved": solved(a), "baseline_solved": solved(b)})
    both_solved = [(selected[n], reference[n]) for n in selected.keys() & reference.keys()
                   if solved(selected[n]) and solved(reference[n])]
    ratios = [(a["total_seconds"] + a.get("preparation_seconds", 0)) /
              max(1e-12, b["total_seconds"] + b.get("preparation_seconds", 0)) for a, b in both_solved]
    return {"mode": mode, "baseline": baseline, "outcomes": dict(outcomes), "rows": rows,
            "both_solved_count": len(both_solved),
            "both_solved_median_runtime_ratio": statistics.median(ratios) if ratios else None,
            "runtime_interpretation": "descriptive primary-seed bounded runs on a shared host"}


def summarize(directory):
    records = [json.loads(line) for line in (directory / "records.jsonl").read_text().splitlines()]
    suites = {}
    for suite in ("holdout", "diagnostic", "synthetic"):
        subsets = {}
        for mode in MODES:
            rows = [r for r in records if r["suite"] == suite and r["phase"] == "full" and r["mode"] == mode]
            finite_times = [r["total_seconds"] + r.get("preparation_seconds", 0) for r in rows if "total_seconds" in r]
            separation = [r.get("separation") or {} for r in rows]
            discovery = [r.get("discovery") or {} for r in rows]
            subsets[mode] = {
                "instances": len(rows), "solved": sum(map(solved, rows)),
                "model_admitted": sum(isinstance(r.get("model_metadata"), dict) for r in rows),
                "model_rejections": [{"name": r["name"], "status": r["status"],
                                      "diagnostic": r.get("diagnostic", r.get("reason"))}
                                     for r in rows if r.get("model_metadata") is None],
                "status_counts": dict(Counter(r["status"] for r in rows)),
                "cuts": sum(len(r.get("cuts") or []) for r in rows),
                "instances_with_cuts": sum(bool(r.get("cuts")) for r in rows),
                "missing_cut_logs": sum((not isinstance(r.get("cuts"), list) or r.get("cut_log_complete") is not True) and r["mode"] in ("all", "auto") for r in rows),
                "no_incumbent": sum(not r.get("primal_check", {}).get("checked", False) for r in rows),
                "soft_budget_overshoots": [{"name": r["name"], "seconds": r["total_seconds"] + r.get("preparation_seconds", 0)}
                                           for r in rows if r.get("total_seconds", 0) + r.get("preparation_seconds", 0) > r["time_limit"] + 0.01],
                "summed_integration_seconds": sum(finite_times),
                "summed_outer_seconds": sum(r.get("outer_wall_seconds", 0) for r in rows),
                "summed_discovery_seconds": sum(r.get("discovery_seconds", 0) for r in rows),
                "summed_build_seconds": sum(r.get("build_seconds", 0) for r in rows),
                "summed_callback_seconds": sum(s.get("callback_seconds", 0) for s in separation),
                "summed_certification_seconds": sum(s.get("certification_seconds", 0) for s in separation),
                "candidate_lps": sum(s.get("candidate_lps", 0) for s in separation),
                "support_calls": sum(s.get("certification_calls", 0) for s in separation),
                "selection_skips": sum(s.get("selection_skips", 0) for s in separation),
                "certification_failures": sum(s.get("certification_failures", 0) for s in separation),
                "row_binding_rejections": sum(s.get("row_binding_rejections", 0) for s in separation),
                "row_rounding_rejections": sum(s.get("row_rounding_rejections", 0) for s in separation),
                "budget_exhausted_cases": sum(bool(s.get("budget_exhausted")) for s in separation),
                "root_discovery_runs": sum(r.get("discovery") is not None for r in rows),
                "discovered_blocks": sum(d.get("blocks", 0) for d in discovery),
                "auto_eligible_blocks": sum(d.get("auto_eligible", 0) for d in discovery),
                "unsupported_sides": sum(d.get("unsupported_sides", 0) for d in discovery),
                "primal_checks": sum(r.get("primal_check", {}).get("checked", False) for r in rows),
                "primal_failures": [r["name"] for r in rows if r.get("primal_check", {}).get("passed") is False],
                "reference_conflicts": [r["name"] for r in rows if r.get("reference_check", {}).get("dual_consistent") is False],
                "root_reference_conflicts": [r["name"] for r in rows if r.get("reference_check", {}).get("root_dual_consistent") is False],
            }
        suites[suite] = {"modes": subsets,
                         "full_comparisons": [compare(records, suite, "full", mode) for mode in MODES[1:]],
                         "root_comparisons": [compare(records, suite, "root", mode) for mode in MODES[1:]],
                         "repeat_comparisons": [compare(records, suite, "repeat", mode) for mode in MODES[1:]]}
    return {"total_records": len(records), "status_counts": dict(Counter(r["status"] for r in records)),
            "cuts_all_phases": sum(len(r.get("cuts") or []) for r in records), "suites": suites,
            "repeats": [r["run_id"] for r in records if r["phase"] == "repeat"],
            "source_manifest": "source-manifest.json", "protocol": "../protocol.md",
            "claims": "Numerical SCIP bounds; added cut support certificates require the separate replay output."}


def markdown(summary, directory):
    lines = ["# Prospective native-model computational results", "",
             "The new holdout contains 30 models selected before implementation outcomes: "
             "ten convex, ten continuous nonconvex and ten integer nonconvex models. "
             "Previous failures and synthetic mechanisms are reported separately. "
             "All three modes share the same source-faithful model builder; the cut modes "
             "retain native nonlinear constraints and do not introduce feature graph equalities.", "",
             "Application runs use a 30-second total soft budget and mechanism runs ten seconds. "
             "Root-only runs use five seconds and one node. Source loading and integration setup "
             "are charged to the soft budget; interpreter imports and independent checking are "
             "included in outer wall time. Runs are sequential with one solver and BLAS thread. "
             "The host also runs unrelated work, so timings are descriptive.", "",
             "| Suite | Mode | Complete admitted records | Numerically solved | Recorded cuts | Cases with cuts | Integration seconds | Outer seconds |",
             "|---|---|---:|---:|---:|---:|---:|---:|"]
    for suite, data in summary["suites"].items():
        for mode, r in data["modes"].items():
            lines.append(f"| {suite} | {mode} | {r['model_admitted']}/{r['instances']} | {r['solved']}/{r['instances']} | {r['cuts']} | "
                         f"{r['instances_with_cuts']} | {r['summed_integration_seconds']:.2f} | {r['summed_outer_seconds']:.2f} |")
    lines += ["", "Denominators retain every selected case, including importer rejection, "
              "worker failure and timeout. Complete admitted records count returned model metadata, "
              "so a missing record does not establish an importer refusal. The four original "
              "diagnostic worker errors occurred during discovery after successful model construction. "
              "Solved means optimal or gaplimit status with a returned "
              "incumbent that passed the independent numerical original-model checks.", "",
              "| Suite | Mode versus baseline | Better final dual | Tie | Worse | Unavailable or flagged |",
              "|---|---|---:|---:|---:|---:|"]
    for suite, data in summary["suites"].items():
        for c in data["full_comparisons"]:
            o = c["outcomes"]
            lines.append(f"| {suite} | {c['mode']} | {o.get('better',0)} | {o.get('tie',0)} | "
                         f"{o.get('worse',0)} | {o.get('unavailable_or_flagged',0)} |")
    lines += ["", "Dual comparisons use tolerance 1e-6 times the larger bound scale. "
              "Any failed original-model primal check or dual/reference conflict is flagged and "
              "excluded from favorable comparisons; the raw record remains. The original-model "
              "checks use scaled tolerance 1e-5 for every row, variable bound, integrality condition, "
              "domain and objective. These checks do not certify SCIP's complete solve or dual bounds.", "",
              "Independent replay results are reported separately and are required before claiming "
              "any saved added cut is certified. Missing cut logs mean unknown cut counts, not zero. "
              "Detailed statuses, rejected structures, soft-budget overshoots, paired root bounds, "
              "seed-1 repeats and instance-level comparisons are saved in summary.json; raw records, "
              "logs, exact source-model data and implementation snapshots are retained.", "",
              f"All phases contain {summary['total_records']} records and {summary['cuts_all_phases']} recorded added cuts."]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    result = summarize(args.directory)
    (args.directory / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
    (args.directory / "results.md").write_text(markdown(result, args.directory))
    print(json.dumps({"records": result["total_records"], "statuses": result["status_counts"],
                      "cuts": result["cuts_all_phases"]}, indent=2))
