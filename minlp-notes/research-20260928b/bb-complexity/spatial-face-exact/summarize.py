"""Summarize rules_table*.jsonl into a node-count table (nodes; '-' = not run, 'cap' = cap exceeded)."""
import json, collections, glob, sys
files = sys.argv[1:] or sorted(glob.glob("rules_table_*.jsonl"))
tab, lbs, order = collections.OrderedDict(), {}, []
for f in files:
    for line in open(f):
        r = json.loads(line)
        key = (r["inst"], r["rule"])
        tab.setdefault(key, {})[r["eps"]] = r["nodes"]
        lbs[(r["inst"], r["eps"])] = r["lb_leaves"]
E = [1e-2, 1e-3, 1e-4, 1e-5, 1e-6]
last = None
for (inst, rule), d in tab.items():
    if inst != last:
        print(f"\n{inst:12s} {'LB(leaves)':16s}", " ".join(f"{lbs.get((inst, e), float('nan')):>7.1f}" for e in E))
        last = inst
    cells = []
    for e in E:
        v = d.get(e, "-")
        cells.append(f"{'cap' if v is None else str(v):>7s}")
    print(f"{'':12s} {rule:16s}", " ".join(cells))
