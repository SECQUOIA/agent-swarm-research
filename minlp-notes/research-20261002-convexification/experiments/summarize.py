"""Summarize the frozen campaign without dropping unfavorable records."""
from __future__ import annotations

import argparse
from collections import Counter
import json
import math
from pathlib import Path
import statistics

MODES = ("baseline", "control", "all", "auto")


def good(record):
    return (record.get("status") not in ("worker_error", "process_timeout", "campaign_budget_exhausted",
                                         "worker_no_output", "worker_output_parse_error", "ablation_unavailable")
            and not record.get("worker_status") and record.get("returncode", 0) == 0
            and record.get("reference_check", {}).get("dual_consistent", True)
            and record.get("reference_check", {}).get("root_dual_consistent", True)
            and record.get("primal_check", {}).get("passed", True))


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
        if not good(a) or not good(b) or da is None or db is None:
            outcome = "unavailable_or_flagged"
        else:
            sign = 1 if a["sense"] == "min" else -1
            improvement = sign * (da - db)
            tol = 1e-6 * max(1, abs(da), abs(db))
            outcome = "better" if improvement > tol else "worse" if improvement < -tol else "tie"
        outcomes[outcome] += 1
        rows.append({"name": name, "outcome": outcome, "dual": da, "baseline_dual": db,
                     "status": a["status"], "baseline_status": b["status"],
                     "cuts": len(a["cuts"]) if "cuts" in a else None,
                     "solved": solved(a), "baseline_solved": solved(b)})
    both_solved = [(selected[n], reference[n]) for n in selected.keys() & reference.keys()
                   if solved(selected[n]) and solved(reference[n])]
    ratios = [(a["total_seconds"] + a.get("source_read_seconds", 0)) /
              max(1e-12, b["total_seconds"] + b.get("source_read_seconds", 0)) for a, b in both_solved]
    return {"mode": mode, "baseline": baseline, "outcomes": dict(outcomes), "rows": rows,
            "both_solved_count": len(both_solved),
            "both_solved_median_runtime_ratio": statistics.median(ratios) if ratios else None,
            "runtime_interpretation": "descriptive one-seed short runs on a shared host"}


def summarize(directory):
    records = [json.loads(line) for line in (directory / "records.jsonl").read_text().splitlines()]
    suites = {}
    for suite in ("synthetic", "holdout", "historical"):
        subsets = {}
        for mode in MODES:
            rows = [r for r in records if r["suite"] == suite and r["phase"] == "full" and r["mode"] == mode]
            finite_times = [r["total_seconds"] + r.get("source_read_seconds", 0) for r in rows if "total_seconds" in r]
            separation = [r.get("separation") or {} for r in rows]
            subsets[mode] = {
                "instances": len(rows), "solved": sum(map(solved, rows)),
                "status_counts": dict(Counter(r["status"] for r in rows)),
                "cuts": sum(len(r.get("cuts", [])) for r in rows),
                "instances_with_cuts": sum(bool(r.get("cuts")) for r in rows),
                "missing_cut_logs": sum("cuts" not in r and r["mode"] in ("all", "auto") for r in rows),
                "soft_budget_overshoots": [{"name": r["name"], "seconds": r["total_seconds"] + r.get("source_read_seconds", 0)}
                                           for r in rows if r.get("total_seconds", 0) + r.get("source_read_seconds", 0) > r["time_limit"] + 0.01],
                "summed_integration_seconds": sum(finite_times),
                "summed_outer_seconds": sum(r.get("outer_wall_seconds", 0) for r in rows),
                "summed_discovery_seconds": sum(r.get("discovery_seconds", 0) for r in rows),
                "summed_build_seconds": sum(r.get("build_seconds", 0) for r in rows),
                "summed_callback_seconds": sum(s.get("callback_seconds", 0) for s in separation),
                "summed_certification_seconds": sum(s.get("certification_seconds", 0) for s in separation),
                "candidate_lps": sum(s.get("candidate_lps", 0) for s in separation),
                "selection_skips": sum(s.get("selection_skips", 0) for s in separation),
                "certification_failures": sum(s.get("certification_failures", 0) for s in separation),
                "primal_checks": sum(r.get("primal_check", {}).get("checked", False) for r in rows),
                "primal_failures": [r["name"] for r in rows if r.get("primal_check", {}).get("passed") is False],
                "reference_conflicts": [r["name"] for r in rows if r.get("reference_check", {}).get("dual_consistent") is False],
                "root_reference_conflicts": [r["name"] for r in rows if r.get("reference_check", {}).get("root_dual_consistent") is False],
            }
        suites[suite] = {"modes": subsets,
                         "full_comparisons": [compare(records, suite, "full", mode) for mode in MODES[1:]],
                         "full_vs_control": [compare(records, suite, "full", mode, "control") for mode in MODES[2:]],
                         "root_comparisons": [compare(records, suite, "root", mode) for mode in MODES[1:]]}
    return {"total_records": len(records), "status_counts": dict(Counter(r["status"] for r in records)),
            "cuts_all_phases": sum(len(r.get("cuts", [])) for r in records), "suites": suites,
            "repeats": [r["run_id"] for r in records if r["phase"] == "repeat"],
            "ablations": [{k: r.get(k) for k in ("run_id", "name", "mode", "phase", "status", "dual",
                                                "primal", "total_seconds", "separation")}
                          for r in records if r["phase"] in ("no_cache", "pairs_only")],
            "reuse_ablation_scope": "no_cache disables sample caching, support-point exchange, repeat skipping, and automatic screening together; it does not isolate cache speed.",
            "source_manifest": "source-manifest.json", "protocol": "../protocol.md",
            "claims": "Numerical SCIP bounds; added cut support certificates require the separate replay output."}


def markdown(summary, directory):
    lines = ["# Frozen short-run computational results", "",
             "This experiment measures a bounded prototype under default native SCIP handling. "
             "All modes retain native nonlinear constraints. The held-out population was selected "
             "before new optimization outcomes and is separate from the synthetic and historical cases.", "",
             "Each full run has a six-second soft budget including integration setup; root-only runs have two seconds "
             "and one node. Each cold worker is limited to 20 seconds and runs alone with one solver "
             "and BLAS thread. Interpreter startup and independent primal checks are recorded in outer "
             "wall time. Nonpreemptive setup or support calls may overshoot the soft budget; these are "
             "listed in summary.json. Missing worker cut logs mean unknown cut counts. "
             "Unrelated jobs share the host, so small time differences are descriptive.", "",
             "| Suite | Mode | Numerically solved | Recorded cuts | Cases with recorded cuts | Integration seconds | Outer seconds |",
             "|---|---|---:|---:|---:|---:|---:|"]
    for suite, data in summary["suites"].items():
        for mode, r in data["modes"].items():
            lines.append(f"| {suite} | {mode} | {r['solved']}/{r['instances']} | {r['cuts']} | "
                         f"{r['instances_with_cuts']} | {r['summed_integration_seconds']:.2f} | {r['summed_outer_seconds']:.2f} |")
    lines += ["", "Final dual-bound comparisons use tolerance 1e-6 times the larger bound scale. "
              "A record with a failed original-model primal check or a dual/reference conflict is flagged "
              "and excluded from favorable comparisons, while retained in the raw output.", "",
              "| Suite | Mode versus baseline | Better | Tie | Worse | Unavailable or flagged |",
              "|---|---|---:|---:|---:|---:|"]
    for suite, data in summary["suites"].items():
        for c in data["full_comparisons"]:
            o = c["outcomes"]
            lines.append(f"| {suite} | {c['mode']} | {o.get('better',0)} | {o.get('tie',0)} | "
                         f"{o.get('worse',0)} | {o.get('unavailable_or_flagged',0)} |")
    lines += ["", "The independently evaluated original-model checks use scaled tolerance 1e-5. "
              "They test bounds, integrality, domains, objective and every original constraint. "
              "These numerical checks and the added-cut certificates do not certify SCIP's search or dual bounds.", "",
              "Detailed instance comparisons, root results, repeats, negative outcomes, and caching/star "
              "ablations are in `summary.json`; raw records, exact model data, source snapshots and worker "
              "logs are retained in this campaign directory. The separate replay output is required "
              "to assess saved cut validity and model binding.", "",
              "The `no_cache` ablation disables sample caching, support-point exchange, repeated-point "
              "skipping, and automatic screening together. Its outcomes cannot isolate the effect of "
              "caching alone. The optional native sampler has a separate kernel microbenchmark; "
              "these solver workers do not compile or load it.", "",
              f"There are {summary['total_records']} raw records and {summary['cuts_all_phases']} recorded added cuts across all phases."]
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
