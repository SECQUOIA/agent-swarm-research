"""Breakdown of the vbb2 re-bounding results by period, group and rbb outcome (own code).

usage: python3 breakdown_cs.py cert.pkl.gz sel.json rebound.jsonl
"""
import json
import math
import sys
from collections import Counter, defaultdict

import numpy as np

import load_cs

d = load_cs.load(sys.argv[1])
recs = d["recs"]
sel = {s["key"]: s for s in json.load(open(sys.argv[2]))}
res = {}
for line in open(sys.argv[3]):
    x = json.loads(line)
    res[x["key"]] = x
rec_res = {x["rid"]: x for k, x in res.items() if x["kind"] == "rec"}
print("record tasks by period (certified at the rbb bound / box proved empty / other):")
per = defaultdict(Counter)
for rid, x in rec_res.items():
    per[recs[rid]["t"]][x["vbb2_status"]] += 1
for t in sorted(per):
    print(f"  period {t}: {sum(per[t].values())} = {per[t]['certified']} / {per[t]['infeasible']} / "
          f"{sum(v for k, v in per[t].items() if k not in ('certified', 'infeasible'))}")
print("record tasks by selection group:")
grp = defaultdict(Counter)
for rid, x in rec_res.items():
    grp[sel[f'r{rid}']["group"]][x["vbb2_status"]] += 1
for g, c in grp.items():
    print(f"  {g}: {dict(c)}")
fin_empty = [rid for rid, x in rec_res.items() if x["vbb2_status"] == "infeasible" and math.isfinite(recs[rid]["bound"])]
c = Counter()
for rid in fin_empty:
    r = recs[rid]
    c[("rbb 0 nodes and bound == target" if r["nodes"] == 0 and r["bound"] == r["target"] else "other",
       "target >= 1000" if r["target"] >= 1000 else "target < 1000")] += 1
print(f"finite rbb records that vbb2 proved empty: {len(fin_empty)}: {dict(c)}")
t = np.array([x["time"] for x in rec_res.values()])
print(f"record tasks: {len(t)}, CPU {t.sum():.0f}s, median {np.median(t):.2f}s, p99 {np.percentile(t, 99):.1f}s, "
      f"max {t.max():.1f}s; max nodes {max(x['nodes'] or 0 for x in rec_res.values())}")
leaf = [x for x in res.values() if x["kind"] == "leaf"]
dup = [x for x in leaf if x["key"] not in sel]
nd = [x for x in leaf if x["key"] in sel]
print(f"leaf tasks run: {len(leaf)}; identical to their record task (first run only): {len(dup)}; "
      f"distinct from their record task: {len(nd)} -> {Counter((x['group'], x['vbb2_status']) for x in nd)}")
nsel = sum(1 for s in sel.values() if s["kind"] == "leaf")
print(f"leaf tasks in the selection: {nsel}; all run: {len(nd) == nsel}")
lt = np.array([x["time"] for x in nd])
print(f"distinct leaf tasks: CPU {lt.sum():.0f}s, max {lt.max():.1f}s")
# corrected leaf tasks: size of the correction
