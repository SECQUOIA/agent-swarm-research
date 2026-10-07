"""Record statistics of a cell-slope certificate, for comparison with the note's
tables (own code; pickle via stub).

usage: python3 record_stats.py cert.pkl.gz ind_verify.json
"""
import json
import math
import sys
from collections import Counter

import numpy as np

import load_cs


def main():
    d = load_cs.load(sys.argv[1])
    R = json.load(open(sys.argv[2]))
    used = set(R["used_records"])
    recs = d["recs"]
    groups = {}
    for rid, r in enumerate(recs):
        src = r["src"][0] if r["src"][0] == "cert3" else r["src"][1]
        groups.setdefault(src, []).append(rid)
    for src, rids in groups.items():
        rs = [recs[i] for i in rids]
        inf = sum(1 for r in rs if r["bound"] == math.inf)
        below = [r for r in rs if r["bound"] < r["target"]]
        at = sum(1 for r in rs if r["bound"] != math.inf and r["bound"] >= r["target"])
        times = np.array([r["time"] for r in rs])
        nodes = sum(int(r["nodes"]) for r in rs)
        retries = [r for r in rs if r.get("retry") is not None]
        print(f"{src}: {len(rs)} records; at/above target {at}, +inf {inf}, below target {len(below)}; "
              f"used by the DP {sum(1 for i in rids if i in used)}")
        print(f"   time sum {times.sum():.0f}s max {times.max():.1f}s median {np.median(times):.2f}s "
              f"p99 {np.percentile(times, 99):.1f}s; nodes {nodes}")
        print(f"   statuses {Counter(r['status'] for r in rs)}")
        for r in below:
            print(f"   below target: t={r['t']} target {r['target']:.4f} bound {r['bound']:.4f} nodes {r['nodes']} "
                  f"status {r['status']}")
        ok = sum(1 for r in retries if r["bound"] >= r["target"])
        print(f"   records with an rc=False retry: {len(retries)}; of these at target after retry: {ok}")


if __name__ == "__main__":
    main()
