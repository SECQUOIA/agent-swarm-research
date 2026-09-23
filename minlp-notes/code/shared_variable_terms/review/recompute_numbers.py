"""Recompute the numbers quoted in results/shared-variable-term-links.md from the jsonl files."""
import json, csv, math, sys
from pathlib import Path
D = Path(__file__).resolve().parent.parent
def load(f): return [json.loads(l) for l in open(D / f) if l.startswith("{")]
known = {}
with open(D.parent / "minlp_solver_lab/instances/instancedata.csv") as f:
    for row in csv.DictReader(f, delimiter=";"):
        known[row["name"]] = row
def fl(s):
    try: return float(s)
    except Exception: return None
def sgm(ts, shift=1.0): return math.exp(sum(math.log(t + shift) for t in ts) / len(ts)) - shift

def table(recs, solved, label, tl):
    by = {}
    for r in recs: by.setdefault(r["name"], {})[r["mode"]] = r
    names = sorted(by)
    print(f"== {label}: {len(names)} instances, records {len(recs)}")
    miss = [n for n in names if len(by[n]) < 2]
    print("instances missing a mode:", miss)
    both = [n for n in names if len(by[n]) == 2]
    print("instances with links>0:", sum(1 for n in both if by[n]["linked"]["links"] > 0))
    sn = [n for n in both if solved(by[n]["native"])]; sl = [n for n in both if solved(by[n]["linked"])]
    print("solved native", len(sn), "linked", len(sl)); print(" only native:", sorted(set(sn) - set(sl)), " only linked:", sorted(set(sl) - set(sn)))
    for shift in (1.0, 10.0):
        print(f" sgm(shift {shift}) time, unsolved counted at {tl}: native %.2f linked %.2f" % (
            sgm([by[n]["native"]["time"] if n in sn else tl for n in both], shift), sgm([by[n]["linked"]["time"] if n in sl else tl for n in both], shift)))
        print(f" sgm(shift {shift}) raw time: native %.2f linked %.2f" % (sgm([by[n]["native"]["time"] for n in both], shift), sgm([by[n]["linked"]["time"] for n in both], shift)))
    sb = sorted(set(sn) & set(sl))
    print(" solved by both:", len(sb), " linked faster on", sum(1 for n in sb if by[n]["linked"]["time"] < by[n]["native"]["time"]),
          " (>10%% faster: %d, >10%% slower: %d)" % (sum(1 for n in sb if by[n]["linked"]["time"] < 0.9 * by[n]["native"]["time"]), sum(1 for n in sb if by[n]["linked"]["time"] > 1.1 * by[n]["native"]["time"])))
    # agreement of optimal values
    for n in sb:
        a, b = by[n]["native"]["primal"], by[n]["linked"]["primal"]
        if abs(a - b) > 2e-4 * max(1.0, abs(a), abs(b)): print("  DISAGREE native/linked optimum:", n, a, b)
    # dual bound against best known primal
    for n in both:
        k = fl(known.get(n, {}).get("primalbound")); sense = by[n]["native"]["sense"]
        prim = [by[n][m]["primal"] for m in by[n] if by[n][m]["primal"] is not None] + ([k] if k is not None else [])
        if not prim: continue
        best = min(prim) if sense == "min" else max(prim)
        for m in by[n]:
            d = by[n][m]["dual"]; tol = 1e-4 * max(1.0, abs(best)) * 2
            if (sense == "min" and d > best + tol) or (sense == "max" and d < best - tol):
                print(f"  DUAL EXCEEDS BEST PRIMAL: {n} {m} dual {d} best primal {best} (csv {k}) status {by[n][m]['status']}")
        # reported optimum vs known
        for m in by[n]:
            if solved(by[n][m]) and k is not None and abs(by[n][m]["primal"] - k) > 2e-4 * max(1.0, abs(k)) * 2.5:
                print(f"  SOLVED VALUE differs from csv primal: {n} {m} {by[n][m]['primal']} csv {k}")
    print(" unsolved in at least one mode:")
    for n in both:
        if n not in sn or n not in sl:
            print("   %-18s %s links %4d native: st %s dual %.6g primal %s t %.1f | linked: st %s dual %.6g primal %s t %.1f" % (
                n, by[n]["native"]["sense"], by[n]["linked"]["links"], by[n]["native"]["status"], by[n]["native"]["dual"], by[n]["native"]["primal"], by[n]["native"]["time"],
                by[n]["linked"]["status"], by[n]["linked"]["dual"], by[n]["linked"]["primal"], by[n]["linked"]["time"]))
    return by

g = table(load("results_gurobi_60.jsonl"), lambda r: r["status"] == 2, "Gurobi 60 s", 60)
for n in ("waterno2_03", "waterno2_04", "lnts50", "ex8_4_7", "wastepaper4", "ghg_2veh"):
    print(n, {m: (g[n][m]["status"], round(g[n][m]["time"], 1), g[n][m]["primal"], g[n][m]["dual"]) for m in g[n]})
s = table(load("results_links.jsonl"), lambda r: r["status"] == "optimal", "SCIP 60 s", 60)
for n in ("waterno2_01", "waterno2_02", "waterno2_03", "waterno2_04"):
    print(n, {m: (s[n][m]["status"], round(s[n][m]["time"], 1), s[n][m]["primal"], s[n][m]["dual"]) for m in s[n]}, "gurobi", {m: g[n][m]["primal"] for m in g[n]})
# cross-solver
print("== cross-solver disagreement (both 'solved')")
for n in sorted(set(g) & set(s)):
    for m in ("native", "linked"):
        if m in g[n] and m in s[n] and g[n][m]["status"] == 2 and s[n][m]["status"] == "optimal":
            a, b = g[n][m]["primal"], s[n][m]["primal"]
            if abs(a - b) > 2e-4 * max(1.0, abs(a), abs(b)): print("  ", n, m, "gurobi", a, "scip", b)
print("== 1800 s")
t = table(load("results_gurobi_1800.jsonl"), lambda r: r["status"] == 2, "Gurobi 1800 s", 1800)
