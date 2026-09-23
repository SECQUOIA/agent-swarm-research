"""For every instance solved to optimality by both forms: relative difference of the optimal values."""
import json, sys, collections
by = collections.defaultdict(dict)
for f in sys.argv[1:]:
    for l in open(f):
        r = json.loads(l)
        if "primal" in r:
            by[(r["name"], r["solver"])][r["form"]] = r
diffs = []
for (name, solver), d in by.items():
    o, c = d.get("orig"), d.get("cuts")
    if o and c and o["status"] == "optimal" and c["status"] == "optimal":
        diffs.append(((c["primal"] - o["primal"]) / max(1, abs(o["primal"])), name, solver))
diffs.sort(reverse=True)
print("pairs both optimal:", len(diffs))
print("cuts optimum ABOVE orig optimum by > 1e-4 rel (gap tolerance):", sum(d[0] > 1e-4 for d in diffs))
print("... by > 2e-5:", sum(d[0] > 2e-5 for d in diffs), "; below by > 2e-5:", sum(d[0] < -2e-5 for d in diffs))
for d in diffs[:8]:
    print("  %+.2e %s %s" % d)
