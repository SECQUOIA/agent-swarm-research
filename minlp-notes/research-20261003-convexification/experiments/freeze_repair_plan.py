"""Freeze matched repeats of observed discovery defects, never performance wins."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import time


def make_plan(directory):
    if not (directory / "completion.json").exists():
        raise ValueError("the original 282-job campaign must be complete")
    records_file = directory / "records.jsonl"
    records = [json.loads(line) for line in records_file.read_text().splitlines()]
    original_jobs = json.loads((directory / "jobs.json").read_text())
    if len(records) != 282 or len(original_jobs) != 282:
        raise ValueError("the original campaign is incomplete")
    groups, triggers = set(), []
    for record in records:
        if record["mode"] == "baseline":
            continue
        config = record.get("config", {})
        budget = min(config.get("max_separation_seconds", 1.0),
                     config.get("separation_budget_fraction", .05) *
                     (record["time_limit"] - record.get("preparation_seconds", 0.0)))
        seconds = record.get("discovery_seconds", 0.0)
        reason = None
        if seconds > budget:
            reason = "discovery_exceeded_existing_callback_budget"
        if record["status"] == "worker_error":
            log = (directory / record["log"]).read_text()
            if "RecursionError" not in log or "split_affine" not in log:
                raise ValueError("unclassified worker error requires review before freezing the repair plan")
            reason = "global_polynomial_generators_exceeded_recursion_depth"
        if reason is not None:
            group = (record["name"], record["phase"], record["seed"])
            groups.add(group)
            triggers.append({"run_id": record["run_id"], "name": record["name"],
                             "suite": record["suite"], "phase": record["phase"], "seed": record["seed"],
                             "reason": reason, "discovery_seconds": seconds if seconds else None,
                             "callback_budget": budget})
    jobs = []
    for index, (job, record) in enumerate(zip(original_jobs, records)):
        if any(record[k] != job[k] for k in ("name", "mode", "phase", "seed")):
            raise ValueError("original jobs and records do not match")
        if (job["name"], job["phase"], job["seed"]) in groups:
            jobs.append({**job, "original_run_id": record["run_id"],
                         "amendment": "discovery_correctness_repair"})
    if len(jobs) != 3 * len(groups):
        raise ValueError("every affected group must have three matched modes")
    return {"frozen_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "criterion": "Any cut-mode record with discovery_seconds > min(config.max_separation_seconds, config.separation_budget_fraction*(nominal time_limit-preparation_seconds)), or an identified global-generator split_affine RecursionError. Repeat every original mode for its model/phase/seed, without changing budget or order.",
            "original_records_sha256": hashlib.sha256(records_file.read_bytes()).hexdigest(),
            "original_source_manifest_sha256": hashlib.sha256((directory / "source-manifest.json").read_bytes()).hexdigest(),
            "groups": [{"name": name, "phase": phase, "seed": seed}
                       for name, phase, seed in sorted(groups)],
            "triggers": triggers, "jobs": jobs,
            "total_soft_seconds": sum(j["time_limit"] for j in jobs),
            "total_hard_seconds": sum(j["worker_timeout"] for j in jobs),
            "interpretation": "A selected correctness-regression cohort, not a new prospective benchmark or a replacement of any original record."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("original", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("repair plan already exists; do not overwrite a frozen selection")
    plan = make_plan(args.original)
    args.output.write_text(json.dumps(plan, indent=2) + "\n")
    print(json.dumps({"groups": len(plan["groups"]), "jobs": len(plan["jobs"]),
                      "triggers": len(plan["triggers"]),
                      "soft_seconds": plan["total_soft_seconds"]}, indent=2))
