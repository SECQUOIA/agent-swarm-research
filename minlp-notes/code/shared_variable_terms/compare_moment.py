"""Gurobi 60 s: native / linked / moment (exact hull of (x,x^2,x^3)) / linkmoment, on instances with
the {2,3} power pair (moment adds nothing elsewhere)."""
import collections, json, math
by = collections.defaultdict(dict)
for f in ("results_gurobi_60.jsonl", "results_gurobi_60_moment.jsonl"):
    for l in open(f):
        r = json.loads(l); by[r["name"]][r["mode"]] = r
ok = lambda r: r["status"] == 2
sg = lambda v: math.exp(sum(math.log(x + 1) for x in v) / len(v)) - 1
modes = ("native", "linked", "moment", "linkmoment")
rows = [(n, d) for n, d in sorted(by.items()) if all(m in d for m in modes) and d["moment"]["links"] > 0]
print("instances with a {2,3} pair:", len(rows))
for mode in modes:
    R = [d[mode] for _, d in rows]
    print(f"{mode:10s} solved {sum(map(ok, R)):2d}  sgm time {sg([r['time'] if ok(r) else 60 for r in R]):5.2f}")
print(f"\n{'instance':16s} " + " ".join(f"{m:>22s}" for m in modes) + "   (status time dual)")
for n, d in rows:
    print(f"{n:16s} " + " ".join(f"st{d[m]['status']} {d[m]['time']:5.1f}s {d[m]['dual']:10.4g}" for m in modes))
