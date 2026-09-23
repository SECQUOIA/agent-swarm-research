"""Compare Gurobi 60 s results: native, linked (reference = smallest magnitude), linked2 (positive
exponent closest to 1).  Trigonometric-only instances are identical in the two rules."""
import collections, json, math
by = collections.defaultdict(dict)
for f, m in (("results_gurobi_60.jsonl", None), ("results_gurobi_60_linked2.jsonl", None)):
    for l in open(f):
        r = json.loads(l); by[r["name"]][r["mode"]] = r
ok = lambda r: r["status"] == 2
sg = lambda v: math.exp(sum(math.log(x + 1) for x in v) / len(v)) - 1
rows = [(n, d) for n, d in sorted(by.items()) if all(k in d for k in ("native", "linked", "linked2"))]
print("instances", len(rows))
for mode in ("native", "linked", "linked2"):
    R = [d[mode] for _, d in rows]
    print(f"{mode:8s} solved {sum(map(ok, R)):2d}  sgm time {sg([r['time'] if ok(r) else 60 for r in R]):5.2f}")
print("\ninstances where the rules differ (status, time, dual, primal):")
for n, d in rows:
    a, b = d["linked"], d["linked2"]
    if abs(a["dual"] - b["dual"]) > 1e-6 * max(1, abs(a["dual"])) or a["status"] != b["status"] or abs(a["time"] - b["time"]) > 3:
        s = 1 if a["sense"] == "min" else -1
        print(f"{n:18s} native st{d['native']['status']} {d['native']['time']:5.1f}s dual {d['native']['dual']:.6g} | "
              f"linked st{a['status']} {a['time']:5.1f}s dual {a['dual']:.6g} | linked2 st{b['status']} {b['time']:5.1f}s dual {b['dual']:.6g} primal {b['primal']}")
