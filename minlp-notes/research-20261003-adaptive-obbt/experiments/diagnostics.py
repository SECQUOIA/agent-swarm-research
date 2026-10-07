"""Descriptive trace/provenance audit after primary frozen analysis.

This does not select runs or change the predeclared performance metrics.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    campaign = HERE / "runs" / sys.argv[1]
    config = json.loads((campaign / "campaign.json").read_text())
    artifacts = {}
    for name, expected in config["source_sha256"].items():
        path = campaign / "source" / name
        assert digest(path) == expected, name
        artifacts[str(path.relative_to(campaign))] = digest(path)
    records = []
    for task in config["tasks"]:
        model = HERE / "frozen" / task["model"]
        assert digest(model) == task["model_sha256"], task["key"]
        raw = campaign / "raw" / (task["key"]+".json")
        log = campaign / "logs" / (task["key"]+".log")
        data = json.loads(raw.read_text())
        assert data["process_complete"], task["key"]
        artifacts[str(raw.relative_to(campaign))] = digest(raw)
        artifacts[str(log.relative_to(campaign))] = digest(log)
        records.append(data)
    output = {"completed_records": len(records), "arms": {}}
    for arm in ("native", "fixed", "adaptive"):
        selected = [r for r in records if r["task"]["arm"] == arm]
        stops, errors, unsupported = Counter(), Counter(), Counter()
        for r in selected:
            obbt = r["outcome"]["obbt"]
            stops.update(e["stop"] for e in obbt["events"])
            errors.update(obbt["errors"])
            if obbt["unsupported"]:
                unsupported[r["task"]["name"]] += obbt["unsupported"]
        output["arms"][arm] = {
            "event_stop_counts": dict(stops), "exception_messages": dict(errors),
            "unsupported_models": dict(unsupported),
            "lp_attempts_without_usable_bound": sum(r["outcome"]["obbt"]["lp_failures"] for r in selected),
            "screened_directions": sum(r["outcome"]["obbt"]["screened"] for r in selected),
            "total_call_seconds": sum(r["call_wall_seconds"] for r in selected),
            "total_solver_seconds": sum(r["outcome"]["solving_time"] for r in selected),
            "max_call_seconds": max(r["call_wall_seconds"] for r in selected),
            "max_process_seconds": max(r["process_wall_seconds"] for r in selected),
            "calls_exceeding_nominal_budget": sum(r["call_wall_seconds"] > r["task"]["time_limit"] for r in selected),
            "no_incumbent_keys": [r["task"]["key"] for r in selected if r["outcome"]["solution"] is None]}
    (campaign / "diagnostics.json").write_text(json.dumps(output, indent=2, sort_keys=True)+"\n")
    (campaign / "artifact_hashes.json").write_text(json.dumps(artifacts, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"records": len(records), "hashed_source_raw_log_files": len(artifacts)}))


if __name__ == "__main__":
    main()
