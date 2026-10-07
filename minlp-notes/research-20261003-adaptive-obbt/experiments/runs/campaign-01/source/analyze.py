"""Aggregate all scheduled runs, retaining failures and unavailable bounds."""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import json
import math
from pathlib import Path
import statistics

HERE = Path(__file__).resolve().parent
ARMS = ("native", "fixed", "adaptive")


def finite(value):
    return isinstance(value, (float, int)) and math.isfinite(value) and abs(value) < 1e19


def row_for(task, raw):
    out = raw.get("outcome", {})
    valid = raw.get("validation") or {}
    has_point = out.get("solution") is not None
    numerical_valid = has_point and valid.get("valid", False)
    failure = (not raw.get("process_complete") or raw.get("hard_timeout", False)
               or raw.get("process_exitcode") != 0 or "error" in raw)
    elapsed = raw.get("process_wall_seconds")
    if not finite(elapsed):
        raise ValueError("Missing finite observed process cost: " + task["key"])
    primal = valid.get("objective_min") if numerical_valid else None
    reported = out.get("objective")
    objective_error = abs(primal-reported)/max(1, abs(primal), abs(reported)) if finite(primal) and finite(reported) else None
    objective_mismatch = objective_error is not None and objective_error > 1e-6
    dual = out.get("dual_bound")
    known_gap = finite(primal) and finite(dual)
    inconsistent = known_gap and dual > primal + 1e-6 * max(1, abs(primal), abs(dual))
    known_gap = known_gap and not inconsistent
    solved = not failure and not inconsistent and not objective_mismatch and out.get("status") == "optimal" and numerical_valid
    gap = max(0, primal-dual)/max(1, abs(primal), abs(dual)) if known_gap else None
    obbt = out.get("obbt") or {}
    return {"name": task["name"], "kind": task["kind"], "family": task["family"],
            "arm": task["arm"], "seed": task["seed"], "key": task["key"],
            "status": out.get("status", "missing"), "failure": failure, "solved": solved,
            "has_incumbent": has_point, "valid_incumbent": numerical_valid,
            "invalid_incumbent": has_point and not numerical_valid,
            "inconsistent_bounds": inconsistent,
            "relative_objective_error": objective_error, "objective_mismatch": objective_mismatch,
            "process_seconds": elapsed, "call_seconds": raw.get("call_wall_seconds"),
            "reported_wall_seconds": out.get("wall_time"),
            "validation_seconds": raw.get("validation_seconds"),
            "time_limit": task["time_limit"],
            "capped_time": min(task["time_limit"], elapsed),
            "par2": elapsed if solved else 2 * task["time_limit"],
            "primal_min": primal, "dual_min": dual if finite(dual) else None,
            "normalized_gap": gap, "gap_score": min(1, gap) if known_gap else 1,
            "max_absolute_violation": valid.get("max_absolute"),
            "max_scaled_violation": valid.get("max_scaled"),
            "nodes": out.get("nodes"),
            "obbt_callbacks": obbt.get("calls", 0),
            "obbt_calls": obbt.get("lp_calls", 0), "obbt_seconds": obbt.get("time", 0),
            "obbt_tightenings": obbt.get("tightened", 0),
            "obbt_nonroot_calls": obbt.get("nonroot_calls", 0),
            "obbt_incumbent_retriggers": obbt.get("incumbent_retriggers", 0),
            "obbt_unsupported": obbt.get("unsupported", 0),
            "obbt_screened": obbt.get("screened", 0)}


def summarize(rows):
    def sgm(field):
        return math.exp(statistics.mean(math.log1p(r[field]) for r in rows))-1
    return {"runs": len(rows), "models": len({r["name"] for r in rows}),
            "solved": sum(r["solved"] for r in rows),
            "no_incumbent": sum(not r["has_incumbent"] for r in rows),
            "invalid_incumbent": sum(r["invalid_incumbent"] for r in rows),
            "inconsistent_bounds": sum(r["inconsistent_bounds"] for r in rows),
            "objective_mismatch": sum(r["objective_mismatch"] for r in rows),
            "failure": sum(r["failure"] for r in rows),
            "statuses": dict(Counter(r["status"] for r in rows)),
            "total_process_seconds": sum(r["process_seconds"] for r in rows),
            "mean_par2_seconds": statistics.mean(r["par2"] for r in rows),
            "sgm_capped_seconds_shift1": sgm("capped_time"),
            "sgm_process_seconds_shift1": sgm("process_seconds"),
            "sgm_par2_seconds_shift1": sgm("par2"),
            "mean_gap_score": statistics.mean(r["gap_score"] for r in rows),
            "finite_valid_gap_runs": sum(r["normalized_gap"] is not None for r in rows),
            "total_obbt_calls": sum(r["obbt_calls"] or 0 for r in rows),
            "total_obbt_tightenings": sum(r["obbt_tightenings"] or 0 for r in rows),
            "total_obbt_seconds": sum(r["obbt_seconds"] or 0 for r in rows),
            "total_obbt_callbacks": sum(r["obbt_callbacks"] or 0 for r in rows),
            "total_obbt_nonroot_calls": sum(r["obbt_nonroot_calls"] or 0 for r in rows),
            "total_obbt_incumbent_retriggers": sum(r["obbt_incumbent_retriggers"] or 0 for r in rows),
            "total_obbt_unsupported": sum(r["obbt_unsupported"] or 0 for r in rows),
            "runs_with_obbt_calls": sum((r["obbt_calls"] or 0) > 0 for r in rows),
            "max_scaled_violation": max((r["max_scaled_violation"] or 0) for r in rows),
            "max_absolute_violation": max((r["max_absolute_violation"] or 0) for r in rows)}


def paired(rows, alternative):
    by_key = {(r["name"], r["seed"], r["arm"]): r for r in rows}
    pairs = [(r, by_key[r["name"], r["seed"], alternative]) for r in rows if r["arm"] == "native"]
    new_solves = [b["key"] for a, b in pairs if b["solved"] and not a["solved"]]
    lost_solves = [b["key"] for a, b in pairs if a["solved"] and not b["solved"]]
    gaps = [(a, b) for a, b in pairs if a["normalized_gap"] is not None and b["normalized_gap"] is not None]
    return {"pairs": len(pairs), "new_solves": new_solves, "lost_solves": lost_solves,
            "par2_wins_5percent": sum(b["par2"] < .95*a["par2"] for a, b in pairs),
            "par2_losses_5percent": sum(b["par2"] > 1.05*a["par2"] for a, b in pairs),
            "mean_paired_par2_delta": statistics.mean(b["par2"]-a["par2"] for a, b in pairs),
            "comparable_finite_gaps": len(gaps),
            "gap_wins_absolute_1e-4": sum(b["normalized_gap"] < a["normalized_gap"]-1e-4 for a, b in gaps),
            "gap_losses_absolute_1e-4": sum(b["normalized_gap"] > a["normalized_gap"]+1e-4 for a, b in gaps)}


def main():
    global HERE
    ap = argparse.ArgumentParser()
    ap.add_argument("campaign")
    ap.add_argument("--experiment-root", type=Path)
    args = ap.parse_args()
    if args.experiment_root is not None:
        HERE = args.experiment_root.resolve()
    campaign = HERE / "runs" / args.campaign
    config = json.loads((campaign / "campaign.json").read_text())
    rows = []
    for task in config["tasks"]:
        path = campaign / "raw" / (task["key"] + ".json")
        if not path.exists():
            raise SystemExit("Campaign is incomplete: " + str(path))
        raw = json.loads(path.read_text())
        if not raw.get("process_complete"):
            raise SystemExit("Campaign task is incomplete: " + str(path))
        rows.append(row_for(task, raw))
    rows.sort(key=lambda r: (r["kind"], r["name"], r["seed"], ARMS.index(r["arm"])))
    summary = {"campaign": args.campaign,
               "campaign_sha256": hashlib.sha256((campaign / "campaign.json").read_bytes()).hexdigest(),
               "source_sha256": config["source_sha256"], "strata": {}, "paired": {}}
    for stratum in ("all", "public", "synthetic"):
        selected = [r for r in rows if stratum == "all" or r["kind"] == stratum]
        summary["strata"][stratum] = {arm: summarize([r for r in selected if r["arm"] == arm]) for arm in ARMS}
        summary["paired"][stratum] = {arm: paired(selected, arm) for arm in ("fixed", "adaptive")}
    (campaign / "summary.json").write_text(json.dumps(summary, sort_keys=True, indent=2)+"\n")
    with (campaign / "outcomes.csv").open("w") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    lines = ["| Cohort | Arm | Solved | No incumbent | Invalid | Failures | PAR-2 mean (s) | Capped shifted mean (s) | Mean gap score | OBBT LPs |",
             "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for stratum in ("all", "public", "synthetic"):
        for arm in ARMS:
            r = summary["strata"][stratum][arm]
            lines.append(f'| {stratum} | {arm} | {r["solved"]}/{r["runs"]} | {r["no_incumbent"]} | {r["invalid_incumbent"]} | {r["failure"]} | {r["mean_par2_seconds"]:.3f} | {r["sgm_capped_seconds_shift1"]:.3f} | {r["mean_gap_score"]:.5f} | {r["total_obbt_calls"]} |')
    (campaign / "table.md").write_text("\n".join(lines)+"\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
