"""R9 implementation lens: separator allowance overruns and soft-budget overruns.

For every cut-mode run of campaigns 3, 3D and 4: allowance = min(s, f * T')
with T' the time_limit passed to run_instance (soft budget minus worker
preparation), callback_seconds versus allowance, and total time
(total_seconds + preparation_seconds) versus the soft budget. Read-only.
"""
import json, collections
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1] / "experiments"
DIRS = ["v3/runs/partA-full", "v3/runs/partA-root", "v3/runs/partB", "v3/runs/partC",
        "v3d/runs/partA-root-rowdir", "v3d/runs/partB-root-rowdir", "v3d/runs/partC-rowdir",
        "v4/runs/partC2", "v4/runs/partC3", "v4/runs/partC4", "v4/runs/partB2",
        "v4/runs/partD-root", "v4/runs/partD-full"]
worst = []
budget_over = []
stopcap = collections.Counter()
for d in DIRS:
    over = collections.Counter(); n = collections.Counter()
    with open(ROOT / d / "records.jsonl") as f:
        for line in f:
            r = json.loads(line)
            sep = r.get("separation")
            soft = r.get("solver_time_limit")
            tot = r.get("total_seconds")
            if tot is not None:
                t = tot + r.get("preparation_seconds", 0.0)
                if t > r["time_limit"] + 1.0:
                    budget_over.append((round(t - r["time_limit"], 2), d, r["run_id"]))
            if not sep:
                continue
            cfg = r["config"]
            allowance = min(cfg["max_separation_seconds"], cfg["separation_budget_fraction"] * soft)
            excess = sep["callback_seconds"] - allowance
            n[r["mode"]] += 1
            if excess > 0.05:
                over[r["mode"]] += 1
            worst.append((round(excess, 3), d, r["run_id"], round(allowance, 3)))
    print(d, "runs", dict(n), "callback > allowance + 0.05 s:", dict(over))
worst.sort(reverse=True)
print("largest allowance overruns:")
for w in worst[:12]:
    print("  ", w)
budget_over.sort(reverse=True)
print("runs whose charged time exceeds the soft budget by > 1 s:", len(budget_over))
for b in budget_over[:12]:
    print("  ", b)
