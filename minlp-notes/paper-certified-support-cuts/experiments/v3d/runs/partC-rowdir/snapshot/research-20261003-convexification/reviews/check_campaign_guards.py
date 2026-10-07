"""Audit whether post-freeze defensive guards affect recorded campaign cuts."""
import argparse
import hashlib
import json
import math
from pathlib import Path


def audit(campaign):
    records = [json.loads(line) for line in (campaign/"records.jsonl").read_text().splitlines() if line]
    cuts, failed = 0, []
    maximum_ratio = 0.0
    for record in records:
        for i, cut in enumerate(record.get("cuts") or []):
            cuts += 1
            actual = cut["actual_row"]
            infinity = actual["scip_infinity"]
            valid = math.isfinite(infinity) and infinity > 0
            for label, value in (("cut_rhs", cut["rhs"]), ("actual_lhs", actual["lhs"])):
                valid_value = math.isfinite(value) and valid and abs(value) < infinity
                if not valid_value:
                    failed.append({"run_id": record["run_id"], "cut": i, "field": label,
                                   "value": value, "scip_infinity": infinity})
                elif infinity:
                    maximum_ratio = max(maximum_ratio, abs(value)/infinity)
    exceptions = []
    for record in records:
        if record.get("status") == "worker_error":
            log = campaign/"logs"/(record["run_id"]+".log")
            if not log.exists():
                log = campaign/"runs"/(record["run_id"]+".log")
            content = log.read_text(errors="replace") if log.exists() else ""
            exceptions.append({"run_id": record["run_id"], "exception": record.get("exception"),
                               "reason": record.get("reason"), "log": str(log) if log.exists() else None,
                               "mentions_exchange_evaluation": "_evaluate" in content,
                               "log_sha256": hashlib.sha256(content.encode()).hexdigest() if content else None})
    return {"schema": "post-freeze-defensive-guard-audit-v1", "records": len(records),
            "recorded_cuts": cuts, "passed": not failed,
            "infinity_guard_failures": failed, "maximum_abs_rhs_over_scip_infinity": maximum_ratio,
            "worker_errors": exceptions,
            "incomplete_cut_log_runs": [r["run_id"] for r in records
                                         if r.get("cut_log_complete") is not True],
            "scope": "Recorded cut right sides and actual row lower sides versus SCIP infinity; missing logs are unknown, and frozen worker exceptions are retained without replacing outcomes."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("campaign", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.campaign)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
