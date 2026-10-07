"""R9 implementation lens: support methods, block dimensions and first-direction
types of every recorded cut of campaigns 3, 3D and 4, and whether any cut
used the star oracle or the polytope-budget fallback. Read-only.
"""
import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "experiments"
DIRS = ["v3/runs/partA-full", "v3/runs/partA-root", "v3/runs/partB", "v3/runs/partC",
        "v3d/runs/partA-root-rowdir", "v3d/runs/partB-root-rowdir", "v3d/runs/partC-rowdir",
        "v4/runs/partC2", "v4/runs/partC3", "v4/runs/partC4", "v4/runs/partB2",
        "v4/runs/partD-root", "v4/runs/partD-full"]
total = collections.Counter()
for d in DIRS:
    methods, dims, skipped = collections.Counter(), collections.Counter(), 0
    with open(ROOT / d / "records.jsonl") as handle:
        for line in handle:
            r = json.loads(line)
            for cut in r.get("cuts") or []:
                stats = cut.get("support_stats") or {}
                methods[stats.get("method")] += 1
                dims[len(cut["variables"])] += 1
                skipped += "polytope_skipped" in stats
    total.update(methods)
    print(f"{d:30s} methods {dict(methods)} block dims {dict(sorted(dims.items()))} polytope_skipped {skipped}")
print("all:", dict(total))
