"""R9 implementation lens: are baseline results reproducible across campaigns?

Compares baseline records of the same (model, phase, seed) between campaign 3
(v3) and the post hoc rerun (v3d), which ran at different times and loads:
root bounds, final status, nodes and time. Read-only.
"""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1] / "experiments"

def load(d, fields=("name", "mode", "node_limit", "seed", "status", "root_dual", "dual", "nodes", "total_seconds", "preparation_seconds")):
    out = {}
    with open(ROOT / d / "records.jsonl") as f:
        for line in f:
            r = json.loads(line)
            if r.get("mode") != "baseline":
                continue
            out[(r["name"], r.get("node_limit"), r.get("seed"))] = {k: r.get(k) for k in fields}
    return out

pairs = [("v3/runs/partC", "v3d/runs/partC-rowdir"), ("v3/runs/partA-root", "v3d/runs/partA-root-rowdir"),
         ("v3/runs/partB", "v3d/runs/partB-root-rowdir")]
for a, b in pairs:
    A, B = load(a), load(b)
    common = sorted(set(A) & set(B), key=str)
    same_root = sum(A[k]["root_dual"] == B[k]["root_dual"] for k in common)
    same_status = sum(A[k]["status"] == B[k]["status"] for k in common)
    same_nodes = sum(A[k]["nodes"] == B[k]["nodes"] for k in common)
    print(f"{a} vs {b}: common {len(common)}, identical root_dual {same_root}, identical status {same_status}, identical nodes {same_nodes}")
    for k in common:
        if A[k]["status"] != B[k]["status"] or A[k]["root_dual"] != B[k]["root_dual"]:
            print("   differs", k, A[k]["status"], B[k]["status"], A[k]["root_dual"], B[k]["root_dual"],
                  round(A[k]["total_seconds"], 1), round(B[k]["total_seconds"], 1))
    if "partC" in a:
        ta = [A[k]["total_seconds"] for k in common if k[1] is None and A[k]["status"] == "optimal"]
        tb = [B[k]["total_seconds"] for k in common if k[1] is None and B[k]["status"] == "optimal"]
        print("   full optimal runs: v3", len(ta), "v3d", len(tb))
