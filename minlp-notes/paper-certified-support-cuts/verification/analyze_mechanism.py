"""Per-instance table of the mechanism family: campaign v3 Part C and the row-direction diagnostic.

Reads only the archived records; standard library only.
Usage: python analyze_mechanism.py
"""
import json, collections, statistics, math
from fractions import Fraction
from pathlib import Path
HERE = Path(__file__).resolve().parents[1] / "experiments"
def load(p):
    return [json.loads(l) for l in open(p)]
def index(recs):
    by = collections.defaultdict(dict)
    for r in recs:
        by[(r["name"], r["phase"])][r["mode"]] = r
    return by
orig = index(load(HERE / "v3/runs/partC/records.jsonl"))
diag = index(load(HERE / "v3d/runs/partC-rowdir/records.jsonl"))
cases = {}
for p in (HERE / "v3/runs/partC/cases").glob("*.json"):
    c = json.loads(p.read_text())
    cases[c["name"]] = c
def opt(name):
    c = cases[name]
    return float(Fraction(c["known_optimum_exact"])) if "known_optimum_exact" in c else c["known_optimum"]
def gap_closed(base, mode, o):
    if base is None or mode is None: return None
    return (mode - base) / (o - base)
rows = []
names = sorted(cases, key=lambda n: (int(n.split("_n")[1].split("_")[0]), n))
print("| n | seed | optimum | root base | closed: v3 mech | closed: rowdir mech | closed: rowdir wide | full base status/nodes/s | v3 mech | rowdir wide |")
summary = collections.defaultdict(list)
for name in names:
    o = opt(name); n = int(name.split("_n")[1].split("_")[0]); s = int(name.split("_s")[-1])
    rb = orig[(name, "root")]["baseline"]; rm = orig[(name, "root")]["all-diag-mech"]
    db = diag[(name, "root")]["baseline"]; dm = diag[(name, "root")]["all-diag-mech"]; dw = diag[(name, "root")]["all-diag-mech-wide"]
    def rd(r):
        return r["root_dual"] if r.get("root_dual") is not None else r["dual"]
    g1 = gap_closed(rd(rb), rd(rm), o); g2 = gap_closed(rd(db), rd(dm), o); g3 = gap_closed(rd(db), rd(dw), o)
    fb = orig[(name, "full")]["baseline"]; fm = orig[(name, "full")]["all-diag-mech"]; fw = diag[(name, "full")]["all-diag-mech-wide"]; fdb = diag[(name, "full")]["baseline"]
    f = lambda r: f"{r['status']}/{r['nodes']}/{r['total_seconds']:.1f}"
    print(f"| {n} | {s} | {o:.6g} | {rd(rb):.4g} | {g1:.2f} | {g2:.2f} | {g3:.2f} | {f(fb)} | {f(fm)} | {f(fw)} |")
    summary[n].append((g1, g2, g3, fb, fm, fw, fdb))
print()
for n, vals in sorted(summary.items()):
    med = lambda i: statistics.median(v[i] for v in vals)
    solved = lambda i: sum(v[i]["status"] in ("optimal", "gaplimit") for v in vals)
    print(f"n={n}: median gap closed v3 {med(0):.2f}, rowdir {med(1):.2f}, rowdir-wide {med(2):.2f}; full solved base {solved(3)}/5 (rerun {solved(6)}/5), v3 mech {solved(4)}/5, rowdir-wide {solved(5)}/5")
def sgm(ts, shift=1.0):
    return math.exp(sum(math.log(t + shift) for t in ts) / len(ts)) - shift
allv = [v for vals in summary.values() for v in vals]
both = [v for v in allv if v[6]["status"] in ("optimal","gaplimit") and v[5]["status"] in ("optimal","gaplimit")]
print("rowdir-wide vs rerun baseline: common solved", len(both), "SGM base", round(sgm([v[6]["total_seconds"] for v in both]),2), "SGM wide", round(sgm([v[5]["total_seconds"] for v in both]),2))
print("solved: rerun baseline", sum(v[6]["status"] in ("optimal","gaplimit") for v in allv), "rowdir-wide", sum(v[5]["status"] in ("optimal","gaplimit") for v in allv), "v3 baseline", sum(v[3]["status"] in ("optimal","gaplimit") for v in allv), "v3 mech", sum(v[4]["status"] in ("optimal","gaplimit") for v in allv))
