"""Tables for the SCIP separator sweep.  python summarize_sepa.py results/scip_sepa_sweep.jsonl"""
import collections, json, math, sys
rows = [json.loads(l) for l in open(sys.argv[1])]
best = collections.defaultdict(lambda: math.inf)
for r in rows:
    if r["primal"] is not None:
        best[r["name"]] = min(best[r["name"]], r["primal"])
ok = lambda r: r["status"] in ("optimal", "gaplimit") and r["dual"] <= best[r["name"]] + 2e-4 * max(1, abs(best[r["name"]]))
sg = lambda v: math.exp(sum(math.log(x + 1) for x in v) / len(v)) - 1 if v else float("nan")
modes = ["native", "root", "tree_d3", "tree_d8", "tree_d1000"]
fam = collections.defaultdict(lambda: collections.defaultdict(list))
for r in rows:
    fam[r["name"].rsplit("-s", 1)[0]][r["mode"]].append(r)
viol = [(r["name"], r["mode"], r["dual"], best[r["name"]]) for r in rows if r["dual"] > best[r["name"]] + 2e-4 * max(1, abs(best[r["name"]]))]
print("records", len(rows), "dual above best primal:", viol)
print(f"{'family':30s} | " + " | ".join(f"{m:>10s}" for m in modes))
print("solved / sgm time (s) / sgm nodes / sgm sepa time (s) / mean end gap % of unsolved")
for f, d in sorted(fam.items()):
    cells = []
    for m in modes:
        R = d.get(m, [])
        if not R:
            cells.append("-"); continue
        s = sum(ok(r) for r in R)
        t = sg([r["total_time"] if ok(r) else 300 for r in R])
        n = sg([r["nodes"] for r in R]); st = sg([r["sepa_time"] for r in R])
        g = [100 * (best[r["name"]] - r["dual"]) / max(abs(best[r["name"]]), 1e-9) for r in R if not ok(r)]
        cells.append(f"{s}/{len(R)} {t:5.0f} {n:6.0f} {st:4.0f} {sum(g)/len(g) if g else 0:4.1f}")
    print(f"{f:30s} | " + " | ".join(f"{c:>10s}" for c in cells))
