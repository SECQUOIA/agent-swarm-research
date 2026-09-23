"""Summaries and consistency checks.  python summarize.py results/a.jsonl [results/b.jsonl ...]"""
import collections, json, math, re, sys

rows = [json.loads(l) for f in sys.argv[1:] for l in open(f)]
rows = [r for r in rows if "primal" in r]
TL = max(r.get("tl", 300) for r in rows)
SOLVED = {"optimal", "gaplimit"}

# ---- consistency: no dual bound above the best primal value of the same instance
best = collections.defaultdict(lambda: math.inf)
for r in rows:
    best[r["name"]] = min(best[r["name"]], r["primal"])
bad = []
for r in rows:
    tol = 2e-4 * max(1.0, abs(best[r["name"]]))
    if r["dual"] > best[r["name"]] + tol:
        bad.append((r["name"], r["solver"], r["form"], r["dual"], best[r["name"]]))
    if r["status"] in SOLVED and r["primal"] > best[r["name"]] + tol:
        bad.append((r["name"], r["solver"], r["form"], "claims optimal at", r["primal"], "best", best[r["name"]]))
print(f"consistency: {len(rows)} records, {len(bad)} violations")
for b in bad:
    print("  VIOLATION", b)
badset = {(b[0], b[1], b[2]) for b in bad}


def sgm(vals, shift=1.0):
    return math.exp(sum(math.log(v + shift) for v in vals) / len(vals)) - shift if vals else float("nan")


groups = collections.defaultdict(lambda: collections.defaultdict(dict))
for r in rows:
    fam = re.sub(r"-s\d+$", "", r["name"])
    groups[(r["solver"], fam)][r["name"]][r["form"]] = r
print(f"\n{'solver':7s} {'family':34s} {'n':>2s} | solved o/c | time o   c (sgm, s) | nodes o   c (both solved) | closed% | endgap% o  c (unsolved)")
for (solver, fam), inst in sorted(groups.items()):
    forms = sorted({f for d in inst.values() for f in d})
    o = [d.get("orig") for d in inst.values()]; c = [d.get("cuts") for d in inst.values()]
    pairs = [(a, b) for a, b in zip(o, c) if a and b]
    def ok(r): return r["status"] in SOLVED and (r["name"], r["solver"], r["form"]) not in badset
    so, sc = sum(ok(a) for a, _ in pairs), sum(ok(b) for _, b in pairs)
    to = sgm([a["total_time"] if ok(a) else TL for a, _ in pairs]); tc = sgm([b["total_time"] if ok(b) else TL for _, b in pairs])
    both = [(a, b) for a, b in pairs if ok(a) and ok(b)]
    no, nc = sgm([a["nodes"] for a, _ in both]), sgm([b["nodes"] for _, b in both])
    clos = [100 * (b["cutinfo"]["bound"] - b["cutinfo"]["bound0"]) / max(best[b["name"]] - b["cutinfo"]["bound0"], 1e-9) for _, b in pairs]
    gap = lambda r: 100 * (best[r["name"]] - r["dual"]) / max(abs(best[r["name"]]), 1e-9)
    go = [gap(a) for a, _ in pairs if not ok(a)]; gc = [gap(b) for _, b in pairs if not ok(b)]
    mean = lambda v: sum(v) / len(v) if v else float("nan")
    print(f"{solver:7s} {fam:34s} {len(pairs):2d} | {so:3d} {sc:3d}    | {to:7.1f} {tc:7.1f}     | {no:9.0f} {nc:9.0f}       | {mean(clos):5.1f}   | {mean(go):5.2f} {mean(gc):5.2f}")
