"""Descriptive summary of historical records without retained primal witnesses.

These data cannot establish feasibility or optimality. Use
lbesh_research.summarize for new independently validated benchmark records.
"""
import collections
import json
import math
import sys


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "results/gdp_final.jsonl"
    with open(path) as stream:
        records = [json.loads(line) for line in stream if line.strip()]
    by_method = collections.defaultdict(list)
    for record in records:
        by_method[record["method"]].append(record)
    print("HISTORICAL, UNVALIDATED: no primal witnesses; no solved or certified counts.")
    print("Raw optimal/local status labels and consensus objectives are not correctness evidence.")
    print(f"{'method':26s} {'runs':>5s} {'obj_present':>11s} {'errors':>7s} {'mean_all_time':>14s}")
    for method, rows in sorted(by_method.items()):
        times = [r["time"] for r in rows if isinstance(r.get("time"),(int,float)) and math.isfinite(r["time"])]
        errors = sum(r.get("status") in ("error","crash","killed") for r in rows)
        objectives = sum(r.get("obj") is not None for r in rows)
        mean = sum(times)/len(times) if times else float("nan")
        print(f"{method:26s} {len(rows):5d} {objectives:11d} {errors:7d} {mean:14.3f}")
        print("  raw statuses: "+json.dumps(dict(collections.Counter(str(r.get("status")) for r in rows)),sort_keys=True))


if __name__ == "__main__":
    main()
