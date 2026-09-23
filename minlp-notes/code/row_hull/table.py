import json, sys, collections
rows = [json.loads(l) for f in sys.argv[1:] for l in open(f)]
by = collections.defaultdict(dict)
for r in rows: by[(r["name"], r["solver"])][r["form"]] = r
print(f"{'instance':40s} {'solver':7s} | {'orig: status time nodes gap%':38s} | cuts: status time(cut) nodes gap% | rootgap closed")
for (name, solver), d in sorted(by.items()):
    def fmt(r):
        if r is None or "primal" not in r: return "missing/error".ljust(38)
        gap = 100 * (r["primal"] - r["dual"]) / max(abs(r["primal"]), 1e-9)
        return f"{r['status'][:9]:9s} {r['total_time']:7.1f} {int(r['nodes']):9d} {gap:6.2f}"
    o, c = d.get("orig"), d.get("cuts")
    extra = ""
    if c and "cutinfo" in c:
        ci = c["cutinfo"]; best = min(x["primal"] for x in d.values() if "primal" in x)
        clos = 100 * (ci["bound"] - ci["bound0"]) / max(best - ci["bound0"], 1e-9)
        extra = f"({ci['time']:.1f}s, {ci['ncuts']} cuts) | {clos:5.1f}%"
    print(f"{name:40s} {solver:7s} | {fmt(o)} | {fmt(c)} {extra}")
