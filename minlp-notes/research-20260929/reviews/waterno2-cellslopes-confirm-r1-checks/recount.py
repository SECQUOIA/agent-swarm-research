"""Recount the authors' vbb2 cross-checks of cell-slopes.md by distinct record,
and recompute the cost shares of Section 8 and the plan3 gain of Section 6.1.
Run from research-20260929/: python3 reviews/waterno2-cellslopes-confirm-r1-checks/recount.py"""
import collections, json, re

L = "open-instances-wave2/waterno2/cellslopes/logs/"


def load(f):
    return [json.loads(l) for l in open(L + f) if l.strip()]


# Item 2: certB record checks (near file: path + near + 99 random; rand2000 file: 6 path again + 2,000 random)
near, r2k = load("crosscheck_certB_near.jsonl"), load("crosscheck_certB_rand2000.jsonl")
rows = [("near", r) for r in near] + [("r2k", r) for r in r2k]
table_runs = [r for f, r in rows if not (f == "r2k" and r["group"] == "path")]
status = {}
for _, r in rows:
    status.setdefault(r["rid"], set()).add(r["vbb2_status"])
r99 = {r["rid"] for r in near if r["group"] == "random-new"}
r2000 = {r["rid"] for r in r2k if r["group"] == "random-new"}
nearset = {r["rid"] for r in near if r["group"] in ("near", "path")}
print("certB record runs in files", len(rows), "; counted in the 5.4 table", len(table_runs))
print("path records of rand2000 file == path records of near file:",
      {r["rid"] for r in r2k if r["group"] == "path"} == {r["rid"] for r in near if r["group"] == "path"})
print("distinct records", len(status), dict(collections.Counter(tuple(s) for s in status.values())))
print("random 99 & 2000:", len(r99 & r2000), "; random 2000 & near/path:", len(r2000 & nearset),
      "; random 99 & near/path:", len(r99 & nearset))
rand = r99 | r2000
print("random distinct", len(rand), dict(collections.Counter(tuple(status[x]) for x in rand)),
      "; random runs", len(r99) + len(r2000))
src = {}
for _, r in rows:
    src.setdefault(r["rid"], r["src"])
print("origin of distinct records", dict(collections.Counter(src.values())))
a = load("crosscheck_certA_near.jsonl")
print("certA record runs", len(a), "distinct", len({r["rid"] for r in a}))
allv = load("crosscheck_certA_leaf.jsonl") + a + load("crosscheck_certB_leaf.jsonl") + near + r2k
print("vbb2 CPU total %.1f s, longest %.1f s" % (sum(r["time"] for r in allv), max(r["time"] for r in allv)))

# Items 3 and 7: SCIP and rbb CPU from the stats logs
def grab(f, pat):
    return int(re.search(pat, open(L + f).read()).group(1))
planF = grab("stats_planF.log", r"of which new.*?cpu (\d+)s")
certA_new = grab("stats_certA.log", r"of which new.*?cpu (\d+)s")
planG = grab("stats_planG.log", r"of which new.*?cpu (\d+)s")
certB_ref = grab("stats_certB.log", r"of which new.*?cpu (\d+)s")
rbb_runs = grab("stats_certB.log", r"records cellslopes: (\d+) runs")
rbb = grab("stats_certB.log", r"records cellslopes: \d+ runs, cpu (\d+)s")
vbb2 = 8775
scip = certA_new + planG + certB_ref
plan = planF + planG
refr = (certA_new - planF) + certB_ref
tot = scip + rbb + vbb2
print("SCIP %d (%.1f%%), planning %d (%.1f%%), refreshes %d (%.1f%%), rbb %d runs %d s (%.1f%%), total %d"
      % (scip, 100 * scip / tot, plan, 100 * plan / tot, refr, 100 * refr / tot, rbb_runs, rbb, 100 * rbb / tot, tot))

# Item 4: plan3 gain
p3 = open("open-instances-wave2/waterno2/sepbranch/logs/plan3.log").read()
rounds = re.findall(r"round (\d+) t=(\d+)s V_est=([\d.]+) .*?estimates=(\d+)", p3)
(r0, t0, v0, e0), (r1, t1, v1, e1) = rounds[0], rounds[-1]
print("plan3: round %s %s (%s est) -> round %s %s (%s est, %s s): gain %.4f, %d estimates, %.3f per 1,000"
      % (r0, v0, e0, r1, v1, e1, t1, float(v1) - float(v0), int(e1) - int(e0),
         1000 * (float(v1) - float(v0)) / (int(e1) - int(e0))))
