"""Independent completeness/hash and primary-summary audit of a finished campaign.

Does not import the experiment runner or analyzer. Recomputes the primary
solved-count and PAR-2 aggregates from every scheduled raw run.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import itertools
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent / "experiments"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def finite(value):
    return value is not None and math.isfinite(value)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("campaign")
    args = ap.parse_args()
    campaign = EXPERIMENTS / "runs" / args.campaign
    config = json.loads((campaign / "campaign.json").read_text())
    summary = json.loads((campaign / "summary.json").read_text())
    manifest = json.loads((EXPERIMENTS / "frozen/manifest.json").read_text())
    assert digest(EXPERIMENTS / "frozen/manifest.json") == config["manifest_sha256"]
    assert digest(campaign / "campaign.json") == summary["campaign_sha256"]
    for filename, expected in config["source_sha256"].items():
        assert digest(campaign / "source" / filename) == expected, filename
    expected = {(m["name"], seed, arm) for m, seed, arm in
                itertools.product(manifest["models"], manifest["seeds"], manifest["arms"])}
    actual = [(t["name"], t["seed"], t["arm"]) for t in config["tasks"]]
    assert len(actual) == len(set(actual)) and set(actual) == expected
    aggregate = defaultdict(lambda: defaultdict(list))
    over_limit, no_point, unsupported = [], [], []
    statuses = Counter()
    for task in config["tasks"]:
        raw = json.loads((campaign / "raw" / (task["key"] + ".json")).read_text())
        assert raw["process_complete"] and raw["task"] == task
        assert digest(EXPERIMENTS / "frozen" / task["model"]) == task["model_sha256"]
        log = campaign / "logs" / (task["key"] + ".log")
        assert log.is_file()
        elapsed = raw["process_wall_seconds"]
        assert finite(elapsed) and elapsed >= 0
        outcome, validation = raw.get("outcome", {}), raw.get("validation") or {}
        statuses[outcome.get("status", "missing")] += 1
        process_ok = raw.get("process_exitcode") == 0 and not raw.get("hard_timeout") and "error" not in raw
        primal, reported, dual = validation.get("objective_min"), outcome.get("objective"), outcome.get("dual_bound")
        scale = max(1, abs(primal or 0), abs(dual or 0))
        inconsistent = finite(primal) and finite(dual) and dual-primal > 1e-6*scale
        mismatch = finite(primal) and finite(reported) and abs(primal-reported) > 1e-6*max(1, abs(primal), abs(reported))
        solved = process_ok and outcome.get("status") == "optimal" and validation.get("valid", False) and not inconsistent and not mismatch
        assert not validation.get("valid") or finite(primal)
        cost = elapsed if solved else 2*task["time_limit"]
        for group in ("all", task["kind"]):
            aggregate[group][task["arm"]].append((int(solved), cost, elapsed))
        if raw.get("call_wall_seconds", 0) > task["time_limit"]:
            over_limit.append((task["key"], raw["call_wall_seconds"]-task["time_limit"]))
        if outcome.get("solution") is None:
            no_point.append(task["key"])
        if outcome.get("obbt", {}).get("unsupported", 0):
            unsupported.append(task["key"])
    report = {"campaign": args.campaign, "tasks": len(actual), "statuses": dict(statuses),
              "strata": {}, "calls_over_nominal_budget": len(over_limit),
              "maximum_call_overshoot_seconds": max((o for _, o in over_limit), default=0),
              "runs_without_incumbents": len(no_point), "runs_with_unsupported_sidecar_calls": len(unsupported)}
    for group, arms in aggregate.items():
        report["strata"][group] = {}
        for arm, runs in arms.items():
            record = summary["strata"][group][arm]
            solved = sum(r[0] for r in runs)
            par2 = math.fsum(r[1] for r in runs)/len(runs)
            total = math.fsum(r[2] for r in runs)
            assert record["runs"] == len(runs) and record["solved"] == solved
            assert math.isclose(record["mean_par2_seconds"], par2, rel_tol=1e-13)
            assert math.isclose(record["total_process_seconds"], total, rel_tol=1e-13)
            report["strata"][group][arm] = {"runs": len(runs), "solved": solved, "mean_par2_seconds": par2}
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
