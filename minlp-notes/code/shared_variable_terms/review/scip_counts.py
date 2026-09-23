import json, math
from pathlib import Path
D = Path(__file__).resolve().parent.parent
recs = [json.loads(l) for l in open(D / "results_links.jsonl") if l.startswith("{")]
by = {}
for r in recs: by.setdefault(r["name"], {})[r["mode"]] = r
L = sorted(n for n in by if "linked" in by[n] and by[n]["linked"]["links"] > 0)
print("instances with links:", len(L), " in link_instances.txt:", len(open(D / "link_instances.txt").read().split()))
print("set difference vs link_instances.txt:", set(L) ^ set(open(D / "link_instances.txt").read().split()))
def sgm(ts, s=1.0): return math.exp(sum(math.log(t + s) for t in ts) / len(ts)) - s
for label, ok in (("optimal only", ("optimal",)), ("optimal+gaplimit", ("optimal", "gaplimit")), ("optimal+gaplimit+infeasible", ("optimal", "gaplimit", "infeasible"))):
    sn = [n for n in L if by[n]["native"]["status"] in ok]; sl = [n for n in L if by[n]["linked"]["status"] in ok]
    print(label, "native", len(sn), "linked", len(sl), "only native", set(sn) - set(sl), "only linked", set(sl) - set(sn),
          "sgm native %.2f linked %.2f" % (sgm([by[n]["native"]["time"] if n in sn else 60 for n in L]), sgm([by[n]["linked"]["time"] if n in sl else 60 for n in L])))
wrong = [n for n in L for m in ("native", "linked") if n.startswith("waterno2_0") and by[n][m]["status"] == "optimal"]
print("waterno2 'optimal' records:", wrong)
