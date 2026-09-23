"""Markdown table: SCIP native / hybrid / standalone handler plus Gurobi and BARON baselines on separable families."""
import json, sys
from collections import defaultdict

sep, base = sys.argv[1], sys.argv[2]
by = defaultdict(dict)
for l in open(sep):
    r = json.loads(l); by[(r["family"], r["n"], r["m"], r["seed"])]["scip " + r["mode"]] = r
for l in open(base):
    r = json.loads(l); by[(r["family"], r["n"], r["m"], r["seed"])][r["solver"]] = r
cols = ["scip native", "scip hybrid", "scip uenv", "gurobi", "baron"]
print("| family | n | m | seed | " + " | ".join(cols) + " |\n|" + "---|" * (4 + len(cols)))
summary = defaultdict(lambda: [0, 0])
for k in sorted(by):
    objs = [r["true_obj"] for r in by[k].values() if "true_obj" in r]
    best = min(objs)
    cells = []
    for c in cols:
        r = by[k].get(c)
        if r is None or "time" not in r:
            cells.append("–"); continue
        gap = 100 * abs(best - r["dual"]) / max(1e-9, abs(best))
        done = r["status"] in ("optimal", "gaplimit")
        bad = "!" if r.get("true_obj", best) > best + 1e-3 * max(1, abs(best)) else ""
        cells.append((f"{r['time']:.1f} ({int(r['nodes'])})" if done else f"TL {gap:.2f}%") + bad)
        summary[(k[0], c)][0] += done and not bad; summary[(k[0], c)][1] += 1
    print("| " + " | ".join(map(str, k)) + " | " + " | ".join(cells) + " |")
print("\nSolved within the limit (returned point within 1e-3 of the best known):\n")
for (fam, c), (s, t) in sorted(summary.items()):
    print(f"- {fam}, {c}: {s}/{t}")
