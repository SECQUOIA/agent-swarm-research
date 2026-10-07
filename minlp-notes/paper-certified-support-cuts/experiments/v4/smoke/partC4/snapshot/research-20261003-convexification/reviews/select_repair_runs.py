"""Select matched repair runs from observed failures of the existing budget.

Selection uses recorded discovery time and the identified recursion failure,
never objective quality, solved counts, or corrected outcomes. All three modes
are retained for every selected model/phase/seed. Original records are intact.
"""
import argparse
import hashlib
import json
from pathlib import Path


def group(job):
    return tuple(job[key] for key in ("suite", "name", "phase", "seed", "node_limit", "time_limit"))


def select(campaign):
    records = [json.loads(line) for line in (campaign/"records.jsonl").read_text().splitlines() if line]
    jobs = json.loads((campaign/"jobs.json").read_text())
    if len(records) != len(jobs) or not (campaign/"completion.json").exists():
        raise ValueError("the original campaign must finish before repair selection is frozen")
    triggers, selected = [], set()
    for record in records:
        separation, config = record.get("separation"), record.get("config")
        if separation is not None and config is not None:
            worker_budget = max(1e-6, record["time_limit"]-record.get("preparation_seconds", 0))
            budget = min(config["max_separation_seconds"], config["separation_budget_fraction"]*worker_budget)
            if separation["discovery_seconds"] > budget:
                triggers.append({"run_id": record["run_id"], "reason": "discovery exceeded existing separator budget",
                                 "discovery_seconds": separation["discovery_seconds"], "budget_seconds": budget})
                selected.add(group(record))
        if record["status"] == "worker_error":
            log = campaign/record["log"]
            content = log.read_text(errors="replace")
            if "RecursionError" in content and "split_affine" in content and "sp.Poly" in content:
                triggers.append({"run_id": record["run_id"], "reason": "identified original-row polynomial recursion failure",
                                 "log_sha256": hashlib.sha256(log.read_bytes()).hexdigest()})
                selected.add(group(record))
    matched = [{**job, "original_run_id": record["run_id"]}
               for job, record in zip(jobs, records) if group(job) in selected]
    for key in selected:
        modes = [job["mode"] for job in matched if group(job) == key]
        if sorted(modes) != ["all", "auto", "baseline"]:
            raise ValueError("repair group does not contain exactly the three matched modes")
    return {"schema": "matched-discovery-repair-selection-v1", "original_records": len(records),
            "original_records_sha256": hashlib.sha256((campaign/"records.jsonl").read_bytes()).hexdigest(),
            "criterion": "Recorded discovery_seconds exceeds the original configured separator budget after charged preparation, or a saved worker log identifies the split_affine polynomial RecursionError.",
            "groups": len(selected), "jobs": matched, "scheduled": len(matched), "triggers": triggers,
            "trigger_count": len(triggers), "soft_seconds": sum(j["time_limit"] for j in matched),
            "hard_seconds": sum(j["worker_timeout"] for j in matched),
            "scope": "Matched correctness and existing-budget repair supplement; all original outcomes remain and these runs are not a new prospective population comparison."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("campaign", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = select(args.campaign)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
    print(json.dumps({k: result[k] for k in ("original_records", "groups", "scheduled", "trigger_count", "soft_seconds", "hard_seconds")}))
