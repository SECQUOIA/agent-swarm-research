"""Markdown tables for Section 8 from rules_table_*.jsonl (processed nodes; 'cap' = node cap exceeded;
'-' = not run).  LB row: proved lower bound on LEAVES of any certificate (nodes >= 2*leaves - 1)."""
import json, collections, glob, math
from face_bb import LABEL
rows = collections.OrderedDict()
lbs = {}
for f in sorted(glob.glob("rules_table_*.jsonl")):
    for line in open(f):
        r = json.loads(line)
        rows.setdefault(r["inst"], collections.OrderedDict()).setdefault(r["rule"], {})[r["eps"]] = r["nodes"]
        if r.get("lb_leaves") is not None and not (isinstance(r["lb_leaves"], float) and math.isnan(r["lb_leaves"])):
            lbs[(r["inst"], r["eps"])] = r["lb_leaves"]
E = [1e-2, 1e-3, 1e-4, 1e-5, 1e-6]
ORDER = ["bisect", "xonly", "LP(1,0)w", "LP(1,.2)w", "LP(1,.2)x", "LP(1,.2)sp", "SCIPdef w", "SCIPdef x", "INC w", "SCIP(1,.2)w", "SCIP(1,.2)c", "ANTIG(.75,.1)w", "BARON(.7,.01)w", "COUEN(.25,.2)w",
         "COUEN(.25,.2)c", "SCIP(1,.2)s", "COUEN(.25,.2)s", "SCIP(1,.2)sp", "COUEN(.25,.2)sp"]
for inst, d in rows.items():
    print(f"\n`{inst}` (relative eps for pooling/box QP instances)\n")
    print("| rule | " + " | ".join(f"{e:.0e}" for e in E) + " |")
    print("|---|" + "---|" * len(E))
    if any((inst, e) in lbs for e in E):
        print("| proved LB (leaves) | " + " | ".join(f"{lbs[(inst, e)]:.1f}" if (inst, e) in lbs else "" for e in E) + " |")
    for rule in ORDER:
        if rule not in d:
            continue
        cells = []
        for e in E:
            v = d[rule].get(e, "-")
            cells.append("cap" if v is None else str(v))
        print(f"| {LABEL.get(rule, rule)} | " + " | ".join(cells) + " |")

