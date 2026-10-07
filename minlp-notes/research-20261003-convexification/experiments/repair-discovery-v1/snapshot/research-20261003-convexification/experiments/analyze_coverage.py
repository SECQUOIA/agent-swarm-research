"""Describe measured coverage without attributing unobserved causes."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from summarize import solved


def classify(record):
    cuts = record.get("cuts")
    if not isinstance(record.get("model_metadata"), dict):
        return "model_not_admitted_or_worker_failed"
    if not isinstance(cuts, list) or record.get("cut_log_complete") is not True:
        return "cut_log_incomplete"
    if cuts:
        return "added_cuts"
    separation = record.get("separation") or {}
    discovery = record.get("discovery")
    if record["mode"] == "baseline":
        return "native_baseline"
    if separation.get("calls", 0) == 0:
        return ("solved_without_callback" if solved(record) else "unsolved_without_callback")
    if discovery is None:
        return "callback_without_discovery"
    if discovery.get("blocks", 0) == 0:
        return "discovery_without_supported_blocks"
    if record["mode"] == "auto" and discovery.get("auto_eligible", 0) == 0:
        return "supported_blocks_but_none_auto_eligible"
    return "eligible_blocks_without_added_cut"


def analyze(directory):
    records = [json.loads(line) for line in (directory / "records.jsonl").read_text().splitlines()]
    result = {}
    for suite in ("holdout", "diagnostic", "synthetic"):
        modes = {}
        for mode in ("baseline", "all", "auto"):
            rows = [r for r in records if r["suite"] == suite and r["phase"] == "full" and r["mode"] == mode]
            sep = [r.get("separation") or {} for r in rows]
            disc = [r.get("discovery") or {} for r in rows]
            mode_result = {
                "records": len(rows), "outcome_classification": dict(Counter(map(classify, rows))),
                "solved_with_zero_search_nodes": sum(solved(r) and r.get("nodes") == 0 for r in rows),
                "callback_runs": sum(s.get("calls", 0) > 0 for s in sep),
                "callback_calls": sum(s.get("calls", 0) for s in sep),
                "discovery_runs": sum(r.get("discovery") is not None for r in rows),
                "supported_blocks": sum(d.get("blocks", 0) for d in disc),
                "auto_eligible_blocks": sum(d.get("auto_eligible", 0) for d in disc),
                "source_nonlinear_sides": sum(d.get("nonlinear_sides", 0) for d in disc),
                "unsupported_source_sides": sum(d.get("unsupported_sides", 0) for d in disc),
                "block_cap_cases": sum(bool(d.get("block_cap_reached")) for d in disc),
                "callback_seconds": sum(s.get("callback_seconds", 0) for s in sep),
                "discovery_seconds": sum(s.get("discovery_seconds", 0) for s in sep),
                "certification_seconds": sum(s.get("certification_seconds", 0) for s in sep),
                "candidate_lps": sum(s.get("candidate_lps", 0) for s in sep),
                "support_calls": sum(s.get("certification_calls", 0) for s in sep),
                "support_failures": sum(s.get("certification_failures", 0) for s in sep),
                "row_binding_rejections": sum(s.get("row_binding_rejections", 0) for s in sep),
                "row_rounding_rejections": sum(s.get("row_rounding_rejections", 0) for s in sep),
                "sampling_failures": sum(s.get("sampling_failures", 0) for s in sep),
                "selection_skips": sum(s.get("selection_skips", 0) for s in sep),
                "budget_exhausted_cases": sum(bool(s.get("budget_exhausted")) for s in sep),
                "by_instance": [{"name": r["name"], "classification": classify(r),
                                 "status": r["status"], "solved": solved(r), "nodes": r.get("nodes"),
                                 "cuts": len(r["cuts"]) if isinstance(r.get("cuts"), list) else None,
                                 "discovery": r.get("discovery"), "separation": r.get("separation")}
                                for r in rows],
            }
            modes[mode] = mode_result
        result[suite] = modes
    return {"scope": "seed-0 full runs, suites kept separate", "suites": result,
            "analysis_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "records_sha256": hashlib.sha256((directory / "records.jsonl").read_bytes()).hexdigest(),
            "interpretation": "No callback is not itself proof of a presolve solve; zero nodes is reported separately. No cut within the bounded search is not hull membership or proof that native cuts dominate. Block counts overlap and are not unique source-variable counts."}


def markdown(data):
    lines = ["# Measured coverage of the native-model cuts", "",
             "These counts describe the seed-0 full runs. They do not identify the causal "
             "effect of native relaxations, reformulation or a different activation policy.", "",
             "| Suite | Mode | Callback runs | Callback calls | Discovery runs | Supported blocks | Auto-eligible blocks | Unsupported sides | Callback seconds |",
             "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for suite, modes in data["suites"].items():
        for mode in ("all", "auto"):
            d = modes[mode]
            lines.append(f"| {suite} | {mode} | {d['callback_runs']}/{d['records']} | {d['callback_calls']} | "
                         f"{d['discovery_runs']} | {d['supported_blocks']} | {d['auto_eligible_blocks']} | "
                         f"{d['unsupported_source_sides']} | {d['callback_seconds']:.3f} |")
    lines += ["", "| Suite | Mode | Mutually exclusive outcome classifications |",
              "|---|---|---|"]
    for suite, modes in data["suites"].items():
        for mode in ("all", "auto"):
            d = modes[mode]
            categories = "; ".join(f"{key}: {value}" for key, value in sorted(d["outcome_classification"].items()))
            lines.append(f"| {suite} | {mode} | {categories} |")
    lines += ["", "`coverage.json` records instance-level classifications, source-side refusals, "
              "support failures, actual-row binding and rounding rejections, selection skips, "
              "budget exhaustion, callback/discovery/certification time, and zero-node solves. "
              "A model solved without invoking this separator did not need these cuts on that "
              "run; it does not show that the cuts can never help. A supported block without an "
              "added cut can reflect the bounded direction search, insufficient violation, "
              "certification or binding rejection, or the work budget. The recorded counters "
              "do not isolate the causal contribution of these mechanisms.", "",
              data["interpretation"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    output = analyze(args.directory)
    (args.directory / "coverage.json").write_text(json.dumps(output, indent=2) + "\n")
    (args.directory / "coverage.md").write_text(markdown(output))
