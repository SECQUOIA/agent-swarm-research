"""Independently reconcile reported coverage and repair selection.

No optimizer or producer selection/analysis function is called.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from audit_experiments import audit_campaign, is_solved, read, sha


def coverage_class(record):
    if not isinstance(record.get("model_metadata"), dict):
        return "model_not_admitted_or_worker_failed"
    if not isinstance(record.get("cuts"), list) or record.get("cut_log_complete") is not True:
        return "cut_log_incomplete"
    if len(record["cuts"]):
        return "added_cuts"
    if record["mode"] == "baseline":
        return "native_baseline"
    sep, disc = record.get("separation") or {}, record.get("discovery")
    if not sep.get("calls", 0):
        return "solved_without_callback" if is_solved(record) else "unsolved_without_callback"
    if sep.get("discovery_incomplete"):
        return "discovery_stopped_at_budget"
    if disc is None:
        return "callback_without_discovery"
    if not disc.get("blocks", 0):
        return "discovery_without_supported_blocks"
    if record["mode"] == "auto" and not disc.get("auto_eligible", 0):
        return "supported_blocks_but_none_auto_eligible"
    return "eligible_blocks_without_added_cut"


def audit_coverage(campaign):
    records = [json.loads(line) for line in (campaign / "records.jsonl").read_text().splitlines()]
    coverage = read(campaign / "coverage.json")
    errors, verified = [], {}
    if coverage["records_sha256"] != sha(campaign / "records.jsonl"):
        errors.append("Coverage does not identify these records")
    for suite, modes in coverage["suites"].items():
        for mode, reported in modes.items():
            rows = [r for r in records if (r["suite"], r["mode"], r["phase"], r["seed"]) == (suite, mode, "full", 0)]
            counters = Counter()
            classes = Counter()
            for r in rows:
                classes[coverage_class(r)] += 1
                sep, disc = r.get("separation") or {}, r.get("discovery") or {}
                counters["records"] += 1
                counters["solved_with_zero_search_nodes"] += bool(is_solved(r) and r.get("nodes") == 0)
                counters["callback_runs"] += sep.get("calls", 0) > 0
                counters["callback_calls"] += sep.get("calls", 0)
                counters["discovery_runs"] += r.get("discovery") is not None
                counters["supported_blocks"] += disc.get("blocks", 0)
                counters["auto_eligible_blocks"] += disc.get("auto_eligible", 0)
                counters["source_nonlinear_sides"] += disc.get("nonlinear_sides", 0)
                counters["unsupported_source_sides"] += disc.get("unsupported_sides", 0)
                counters["block_cap_cases"] += bool(disc.get("block_cap_reached"))
                counters["budget_exhausted_cases"] += bool(sep.get("budget_exhausted"))
                for output, source in (("callback_seconds", "callback_seconds"), ("discovery_seconds", "discovery_seconds"),
                                       ("certification_seconds", "certification_seconds"), ("candidate_lps", "candidate_lps"),
                                       ("support_calls", "certification_calls"), ("support_failures", "certification_failures"),
                                       ("row_binding_rejections", "row_binding_rejections"), ("row_rounding_rejections", "row_rounding_rejections"),
                                       ("sampling_failures", "sampling_failures"), ("selection_skips", "selection_skips")):
                    counters[output] += sep.get(source, 0)
            for key, actual in {**counters, "outcome_classification": dict(classes)}.items():
                if reported[key] != actual:
                    errors.append(f"Coverage differs: {suite}/{mode}/{key}")
            expected_instances = [{"name": r["name"], "classification": coverage_class(r), "status": r["status"],
                                   "solved": is_solved(r), "nodes": r.get("nodes"),
                                   "cuts": len(r["cuts"]) if isinstance(r.get("cuts"), list) else None,
                                   "discovery": r.get("discovery"), "separation": r.get("separation")} for r in rows]
            if expected_instances != reported["by_instance"]:
                errors.append(f"Coverage instance records differ: {suite}/{mode}")
            verified[suite + "/" + mode] = {**counters, "outcome_classification": dict(classes)}
    return {"passed": not errors, "errors": errors, "records_sha256": sha(campaign / "records.jsonl"), "verified": verified}


def audit_repair_selection(campaign, runner_plan, review_plan):
    records = [json.loads(line) for line in (campaign / "records.jsonl").read_text().splitlines()]
    jobs = read(campaign / "jobs.json")
    errors, trigger_ids, selected_groups = [], [], set()
    for r in records:
        config = r.get("config")
        if config is not None and (config["max_separation_seconds"] != 1.0 or config["separation_budget_fraction"] != 0.05):
            errors.append(f"Recorded configured budget differs from frozen defaults: {r['run_id']}")
        # Constants independently read from the primary snapshot's Config.
        allowed = min(1.0, 0.05 * max(1e-6, r["time_limit"] - r.get("preparation_seconds", 0)))
        too_long = r.get("discovery_seconds", 0) > allowed
        recursion = False
        if r["status"] == "worker_error":
            content = (campaign / r["log"]).read_text()
            recursion = all(word in content for word in ("RecursionError", "split_affine", "sp.Poly"))
        if too_long or recursion:
            trigger_ids.append(r["run_id"])
            selected_groups.add((r["suite"], r["name"], r["phase"], r["seed"], r["node_limit"], r["time_limit"]))
    expected_jobs = []
    for job, record in zip(jobs, records):
        group = tuple(job[k] for k in ("suite", "name", "phase", "seed", "node_limit", "time_limit"))
        if group in selected_groups:
            expected_jobs.append({**job, "original_run_id": record["run_id"]})
    for label, path in (("runner", runner_plan), ("review", review_plan)):
        plan = read(path)
        if plan["original_records_sha256"] != sha(campaign / "records.jsonl"):
            errors.append(f"{label} plan original-record binding differs")
        if label == "runner" and plan["original_source_manifest_sha256"] != sha(campaign / "source-manifest.json"):
            errors.append("Runner plan source-manifest binding differs")
        normalized_jobs = [{k: v for k, v in job.items() if k != "amendment"} for job in plan["jobs"]]
        if normalized_jobs != expected_jobs:
            errors.append(f"{label} plan jobs differ from independently reconstructed selection")
        if [trigger["run_id"] for trigger in plan["triggers"]] != trigger_ids:
            errors.append(f"{label} plan triggers differ from independently reconstructed selection")
    return {"passed": not errors, "errors": errors, "groups": len(selected_groups), "triggers": len(trigger_ids),
            "jobs": len(expected_jobs), "soft_seconds": sum(j["time_limit"] for j in expected_jobs),
            "hard_seconds": sum(j["worker_timeout"] for j in expected_jobs),
            "trigger_ids": trigger_ids, "runner_plan_sha256": sha(runner_plan), "review_plan_sha256": sha(review_plan)}


def audit_repair_results(directory, primary, plan_path):
    """Reconstruct repaired metrics and ensure every original artifact is retained."""
    plan = read(plan_path)
    base = audit_campaign(directory, plan["jobs"])
    errors = []
    summary = read(directory / "repair-summary.json")
    rows = [json.loads(line) for line in (directory / "records.jsonl").read_text().splitlines()]
    if (plan["original_records_sha256"] != sha(primary / "records.jsonl")
            or plan["original_source_manifest_sha256"] != sha(primary / "source-manifest.json")):
        errors.append("Original prospective records or implementation changed during repair")
    top = {"records": len(rows), "status_counts": dict(Counter(r["status"] for r in rows)),
           "recorded_cuts": sum(len(r.get("cuts") or []) for r in rows),
           "primal_checks": base["primal_checked"],
           "unknown_cut_logs": len(base["unknown_or_incomplete_cut_logs"]),
           "records_sha256": sha(directory / "records.jsonl")}
    for key, value in top.items():
        if summary[key] != value:
            errors.append(f"Repair summary differs: {key}")
    old = {r["run_id"]: r for r in (json.loads(line) for line in (primary / "records.jsonl").read_text().splitlines())}
    verified = {}
    for section in summary["sections"]:
        suite, phase = section["suite"], section["phase"]
        for mode, reported in section["modes"].items():
            selected = [r for r in rows if (r["suite"], r["phase"], r["mode"]) == (suite, phase, mode)]
            counts, overshoots = Counter(), []
            for r in selected:
                counts["records"] += 1
                counts["solved"] += is_solved(r)
                counts["cuts"] += len(r.get("cuts") or [])
                counts["complete_cut_logs"] += r.get("cut_log_complete") is True
                counts["primal_checks"] += r.get("primal_check", {}).get("checked", False)
                counts["total_integration_seconds"] += r.get("total_seconds", 0) + r.get("preparation_seconds", 0)
                counts["outer_seconds"] += r.get("outer_wall_seconds", 0)
                sep = r.get("separation") or {}
                for key in ("callback_seconds", "discovery_seconds", "candidate_lps", "row_binding_rejections"):
                    counts[key] += sep.get(key, 0)
                counts["discovery_incomplete"] += bool(sep.get("discovery_incomplete"))
                counts["support_calls"] += sep.get("certification_calls", 0)
                if mode != "baseline" and isinstance(r.get("config"), dict):
                    allowance = min(r["config"]["max_separation_seconds"], r["config"]["separation_budget_fraction"] *
                                    (r["time_limit"] - r.get("preparation_seconds", 0)))
                    if r.get("discovery_seconds", 0) > allowance:
                        overshoots.append({"run_id": r["run_id"], "seconds": r["discovery_seconds"], "budget": allowance,
                                           "excess": r["discovery_seconds"] - allowance,
                                           "discovery_incomplete": sep.get("discovery_incomplete")})
                original = old[r["original_run_id"]]
                if r.get("original_model") is not None and original.get("original_model") is not None and r["original_model"] != original["original_model"]:
                    errors.append(f"Repaired model differs from original parsed input: {r['run_id']}")
                if r.get("config") is not None and original.get("config") is not None and r["config"] != original["config"]:
                    errors.append(f"Repaired configuration changed: {r['run_id']}")
            values = {**counts, "status_counts": dict(Counter(r["status"] for r in selected)),
                      "primal_failures": [r["run_id"] for r in selected if r.get("primal_check", {}).get("passed") is False],
                      "reference_conflicts": [r["run_id"] for r in selected if any(r.get("reference_check", {}).get(k) is False for k in ("dual_consistent", "root_dual_consistent"))],
                      "discovery_soft_overshoots": overshoots}
            for key, value in values.items():
                if reported[key] != value:
                    errors.append(f"Repair section differs: {suite}/{phase}/{mode}/{key}")
            verified[suite + "/" + phase + "/" + mode] = values
        for comparison in section["comparisons"]:
            independent = base["metrics"][suite + "/" + phase]["comparisons"][comparison["mode"]]
            for key, value in independent.items():
                if comparison[key] != value:
                    errors.append(f"Repair paired metric differs: {suite}/{phase}/{comparison['mode']}/{key}")
    return {"passed": base["passed"] and not errors, "errors": errors, "record_audit": base, "summary_audit": verified}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("campaign", type=Path)
    parser.add_argument("--runner-plan", type=Path)
    parser.add_argument("--review-plan", type=Path)
    parser.add_argument("--repair-campaign", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = {"coverage": audit_coverage(args.campaign)}
    if args.runner_plan and args.review_plan:
        output["repair_selection"] = audit_repair_selection(args.campaign, args.runner_plan, args.review_plan)
    if args.repair_campaign:
        output["repair_results"] = audit_repair_results(args.repair_campaign, args.campaign, args.runner_plan)
        output["repair_coverage"] = audit_coverage(args.repair_campaign)
    output["passed"] = all(result["passed"] for result in output.values())
    args.output.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"passed": output["passed"], "output": str(args.output)}))
    raise SystemExit(0 if output["passed"] else 1)
