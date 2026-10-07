"""Report a selected repair cohort without replacing prospective outcomes."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from summarize import compare, solved


def analyze(directory):
    records_path = directory / "records.jsonl"
    records = [json.loads(line) for line in records_path.read_text().splitlines()]
    completion = json.loads((directory / "completion.json").read_text())
    if len(records) != completion["scheduled"]:
        raise ValueError("repair campaign is incomplete")
    sections = []
    for phase in ("full", "root", "repeat"):
        for suite in ("holdout", "diagnostic", "synthetic"):
            selected = [r for r in records if r["phase"] == phase and r["suite"] == suite]
            if not selected:
                continue
            modes = {}
            for mode in ("baseline", "all", "auto"):
                rows = [r for r in selected if r["mode"] == mode]
                sep = [r.get("separation") or {} for r in rows]
                overshoots = []
                for r in rows:
                    if mode == "baseline" or not isinstance(r.get("config"), dict):
                        continue
                    budget = min(r["config"]["max_separation_seconds"],
                                 r["config"]["separation_budget_fraction"] *
                                 (r["time_limit"] - r.get("preparation_seconds", 0)))
                    elapsed = r.get("discovery_seconds", 0)
                    if elapsed > budget:
                        overshoots.append({"run_id": r["run_id"], "seconds": elapsed,
                                           "budget": budget, "excess": elapsed - budget,
                                           "discovery_incomplete": (r.get("separation") or {}).get("discovery_incomplete")})
                modes[mode] = {"records": len(rows), "solved": sum(map(solved, rows)),
                               "status_counts": dict(Counter(r["status"] for r in rows)),
                               "cuts": sum(len(r.get("cuts") or []) for r in rows),
                               "complete_cut_logs": sum(r.get("cut_log_complete") is True for r in rows),
                               "primal_checks": sum(r.get("primal_check", {}).get("checked", False) for r in rows),
                               "primal_failures": [r["run_id"] for r in rows if r.get("primal_check", {}).get("passed") is False],
                               "reference_conflicts": [r["run_id"] for r in rows if any(r.get("reference_check", {}).get(k) is False for k in ("dual_consistent", "root_dual_consistent"))],
                               "total_integration_seconds": sum(r.get("total_seconds", 0) + r.get("preparation_seconds", 0) for r in rows),
                               "outer_seconds": sum(r.get("outer_wall_seconds", 0) for r in rows),
                               "callback_seconds": sum(s.get("callback_seconds", 0) for s in sep),
                               "discovery_seconds": sum(s.get("discovery_seconds", 0) for s in sep),
                               "discovery_incomplete": sum(bool(s.get("discovery_incomplete")) for s in sep),
                               "discovery_soft_overshoots": overshoots,
                               "candidate_lps": sum(s.get("candidate_lps", 0) for s in sep),
                               "support_calls": sum(s.get("certification_calls", 0) for s in sep),
                               "row_binding_rejections": sum(s.get("row_binding_rejections", 0) for s in sep)}
            sections.append({"phase": phase, "suite": suite, "modes": modes,
                             "comparisons": [compare(records, suite, phase, mode) for mode in ("all", "auto")]})
    return {"scope": "selected correctness-regression cohort; original prospective results remain unchanged",
            "records": len(records), "status_counts": dict(Counter(r["status"] for r in records)),
            "recorded_cuts": sum(len(r.get("cuts") or []) for r in records),
            "primal_checks": sum(r.get("primal_check", {}).get("checked", False) for r in records),
            "unknown_cut_logs": sum(r.get("cut_log_complete") is not True for r in records),
            "sections": sections,
            "analysis_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "records_sha256": hashlib.sha256(records_path.read_bytes()).hexdigest(),
            "source_manifest": "source-manifest.json", "selection": "amendment.json"}


def markdown(data):
    lines = ["# Corrected discovery: matched regression results", "",
             "This cohort was selected because the original campaign exposed a discovery error "
             "or exceeded its existing discovery budget. It is not a new prospective holdout. "
             "All original records remain in campaign-v2, including the four failed workers and "
             "their unknown cut logs. The corrected implementation has its own source snapshot, "
             "matched baselines, unchanged models, seeds and budgets.", "",
             "| Phase | Population | Mode | Numerically solved | Recorded cuts | Integration seconds | Discovery seconds | Incomplete discovery |",
             "|---|---|---|---:|---:|---:|---:|---:|"]
    for section in data["sections"]:
        for mode, d in section["modes"].items():
            lines.append(f"| {section['phase']} | {section['suite']} | {mode} | "
                         f"{d['solved']}/{d['records']} | {d['cuts']} | {d['total_integration_seconds']:.3f} | "
                         f"{d['discovery_seconds']:.3f} | {d['discovery_incomplete']} |")
    lines += ["", "| Phase | Population | Mode versus matched baseline | Better final dual | Tie | Worse | Unavailable or flagged |",
              "|---|---|---|---:|---:|---:|---:|"]
    for section in data["sections"]:
        for c in section["comparisons"]:
            o = c["outcomes"]
            lines.append(f"| {section['phase']} | {section['suite']} | {c['mode']} | {o.get('better', 0)} | "
                         f"{o.get('tie', 0)} | {o.get('worse', 0)} | {o.get('unavailable_or_flagged', 0)} |")
    lines += ["", "Discovery now stops at deadline checks between units of work. An incomplete "
              "discovery is discarded, and native SCIP continues. A single nonpreemptive operation "
              "can still overshoot a soft deadline; every measured excess is listed in repair-summary.json. "
              "These checks provide a bounded fallback, not a hard real-time guarantee.", "",
              f"There are {data['records']} records, {data['recorded_cuts']} recorded cuts, "
              f"{data['primal_checks']} returned-incumbent checks and {data['unknown_cut_logs']} unknown cut logs. "
              "Independent replay and metric audit are separate artifacts; numerical incumbent checks "
              "and cut certificates do not certify the complete SCIP solve."]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    result = analyze(args.directory)
    (args.directory / "repair-summary.json").write_text(json.dumps(result, indent=2) + "\n")
    (args.directory / "results.md").write_text(markdown(result))
    print(json.dumps({k: result[k] for k in ("records", "status_counts", "recorded_cuts", "primal_checks", "unknown_cut_logs")}, indent=2))
