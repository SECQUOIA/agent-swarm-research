"""Condensed node-count table for the note: nodes at eps = 1e-4 / 1e-6 per (instance, rule)."""
import json, collections, glob, math
from face_bb import LABEL   # display labels after the review (SCIP(1,.2) -> LP(1,.2), etc.)
rows, lbs = collections.OrderedDict(), {}
for f in sorted(glob.glob("rules_table_*.jsonl")):
    for line in open(f):
        r = json.loads(line)
        rows.setdefault(r["inst"], {}).setdefault(r["rule"], {})[r["eps"]] = r["nodes"]
        v = r.get("lb_leaves")
        if v is not None and not (isinstance(v, float) and math.isnan(v)):
            lbs[(r["inst"], r["eps"])] = v
RULES = ["bisect", "SCIP(1,.2)w", "SCIP(1,.2)sp", "ANTIG(.75,.1)w", "BARON(.7,.01)w", "COUEN(.25,.2)w",
         "COUEN(.25,.2)sp", "COUEN(.25,.2)s"]
INST = ["kink", "kinkT", "sharp_pt", "iso", "diag", "tilt(0.3)", "tilt(0.03)", "tilt(0.003)", "aligned_quad", "path3",
        "boxqp4s1c", "boxqp4s2c", "haverly3q"]
def cell(inst, rule):
    d = rows.get(inst, {}).get(rule, {})
    f = lambda e: "cap" if (e in d and d[e] is None) else str(d.get(e, "-"))
    return f"{f(1e-4)} / {f(1e-6)}"
print("| instance | LB leaves 1e-4 / 1e-6 | " + " | ".join(LABEL.get(r, r) for r in RULES) + " |")
print("|---|---|" + "---|" * len(RULES))
for inst in INST:
    if inst not in rows:
        continue
    lb = lambda e: f"{lbs[(inst, e)]:.1f}" if (inst, e) in lbs else "–"
    print(f"| {inst} | {lb(1e-4)} / {lb(1e-6)} | " + " | ".join(cell(inst, r) for r in RULES) + " |")

import sys
if len(sys.argv) > 1 and sys.argv[1] == "rev":
    # revision table (Section 8.4): old keys (SCIP(1,.2)...) and new keys (LP(1,.2)...) merged per column
    COLS = [("bisect", ["bisect"]), ("LP(1,.2)w", ["LP(1,.2)w", "SCIP(1,.2)w"]),
            ("LP(1,.2)sp", ["LP(1,.2)sp", "SCIP(1,.2)sp"]), ("SCIPdef w", ["SCIPdef w"]),
            ("INC w", ["INC w"]), ("LP(1,0)w", ["LP(1,0)w"])]
    INST2 = ["kink", "kinkT", "tilt(0.03)", "iso", "diag", "aligned_quad", "box_aligned", "box_alignedK2"]
    print("\n| instance | LB leaves 1e-4 / 1e-6 | " + " | ".join(c for c, _ in COLS) + " |")
    print("|---|---|" + "---|" * len(COLS))
    for inst in INST2:
        if inst not in rows:
            continue
        def cellk(keys):
            for k in keys:
                if k in rows[inst]:
                    return cell(inst, k)
            return "- / -"
        lb = lambda e: f"{lbs[(inst, e)]:.1f}" if (inst, e) in lbs else "–"
        print(f"| {inst} | {lb(1e-4)} / {lb(1e-6)} | " + " | ".join(cellk(k) for _, k in COLS) + " |")
