"""Root dual bounds: native vs hybrid, measured against the MINLPLib reference optimum."""
import csv, json, sys
from collections import defaultdict
ref = {}
with open("../minlp_solver_lab/instances/instancedata.csv") as fh:
    for row in csv.DictReader(fh, delimiter=";"):
        try: ref[row["name"]] = float(row["primalbound"])
        except ValueError: pass
by = defaultdict(dict)
for l in open(sys.argv[1]):
    r = json.loads(l); by[r["instance"]][r["mode"]] = r
better = worse = same = skipped = 0
names = {"better": [], "worse": []}
for n, d in sorted(by.items()):
    a, b = d.get("native"), d.get("hybrid")
    if not a or not b or n not in ref or any(r.get("root_dual") is None or abs(r["root_dual"]) >= 1e19 for r in (a, b)):
        skipped += 1; continue
    ga, gb = abs(ref[n] - a["root_dual"]), abs(ref[n] - b["root_dual"])
    scale = max(1e-9, abs(ref[n]))
    if gb < 0.9 * ga - 1e-6 * scale: better += 1; names["better"].append(f"{n} ({ga / scale:.3g} -> {gb / scale:.3g})")
    elif ga < 0.9 * gb - 1e-6 * scale: worse += 1; names["worse"].append(f"{n} ({ga / scale:.3g} -> {gb / scale:.3g})")
    else: same += 1
print(f"root gap to reference, hybrid vs native: smaller by >10% on {better}, larger by >10% on {worse}, similar on {same}; "
      f"not comparable (no root LP bound in a mode) {skipped}")
for k, v in names.items(): print(f"  {k}: " + "; ".join(v))
