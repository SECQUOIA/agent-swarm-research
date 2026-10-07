"""R9 implementation lens: do full and root runs of the path family have the
same separator funnel (Section 8.3 claim)? Compares the separator counters of
the full run and the root run of each (instance, cut mode). Read-only.
"""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1] / "experiments"
KEYS = ("calls", "certification_calls", "certification_failures", "row_binding_rejections",
        "row_rounding_rejections", "cuts")
for d in ["v3/runs/partC", "v3d/runs/partC-rowdir", "v4/runs/partC2", "v4/runs/partC3", "v4/runs/partC4"]:
    runs = {}
    with open(ROOT / d / "records.jsonl") as f:
        for line in f:
            r = json.loads(line)
            if not r.get("separation"):
                continue
            runs[(r["name"], r["mode"], r.get("node_limit"))] = tuple(r["separation"][k] for k in KEYS)
    same = diff = 0
    examples = []
    for (name, mode, nl), v in runs.items():
        if nl is None and (name, mode, 1) in runs:
            if runs[(name, mode, 1)] == v:
                same += 1
            else:
                diff += 1
                examples.append((name, mode, v, runs[(name, mode, 1)]))
    print(d, "identical", same, "different", diff)
    for e in examples[:4]:
        print("   ", e)
