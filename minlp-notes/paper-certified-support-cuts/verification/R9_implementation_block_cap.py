"""R9 implementation lens: how often did discovery hit the block cap?

Discovery keeps the first max_blocks groups in the order (-size, variable
indices), so when the cap binds, the blocks examined are the largest groups
with the smallest variable indices. For every cut-mode run with completed
discovery, report whether the cap was reached, by part and mode, and the
number of distinct models affected. Read-only.
"""
import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "experiments"
DIRS = ["v3/runs/partA-full", "v3/runs/partA-root", "v3/runs/partB", "v3/runs/partC",
        "v4/runs/partB2", "v4/runs/partD-root", "v4/runs/partD-full"]
for d in DIRS:
    stats = collections.defaultdict(lambda: [0, 0, set(), 0])
    with open(ROOT / d / "records.jsonl") as handle:
        for line in handle:
            r = json.loads(line)
            sep = r.get("separation")
            if not sep:
                continue
            s = stats[r["mode"]]
            disc = r.get("discovery")
            if disc is None:
                s[3] += 1          # discovery not completed (stopped or not reached)
                continue
            s[0] += 1
            if disc.get("block_cap_reached"):
                s[1] += 1
                s[2].add(r["name"])
    print(d, {m: f"discovered {a}, cap reached {b} ({len(c)} models), no discovery {e}"
              for m, (a, b, c, e) in stats.items()})
