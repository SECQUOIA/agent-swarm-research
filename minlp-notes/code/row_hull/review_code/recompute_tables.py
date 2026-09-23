"""Independent recomputation of the numbers quoted in notes/row-hull-experiments.md."""
import json, math, re, collections, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1] / "results"
TL = 300.0


def load(f):
    return [json.loads(l) for l in open(R / f)]


def sgm(v, s=1.0):
    return math.exp(sum(math.log(x + s) for x in v) / len(v)) - s if v else float("nan")


def analyse(fname, solvers):
    allrows = load(fname)
    err = [r for r in allrows if "primal" not in r]
    rows = [r for r in allrows if "primal" in r]
    print(f"\n===== {fname}: {len(allrows)} lines, {len(err)} without result")
    for r in err:
        print("   no result:", r["name"], r["solver"], r["form"], str(r.get("status"))[:80])
    best = collections.defaultdict(lambda: math.inf)
    for r in rows:
        best[r["name"]] = min(best[r["name"]], r["primal"])
    statuses = collections.Counter((r["solver"], r["form"], r["status"]) for r in rows)
    print("   statuses:", dict(statuses))
    for solver in solvers:
        pairs = collections.defaultdict(dict)
        for r in rows:
            if r["solver"] == solver:
                pairs[r["name"]][r["form"]] = r
        pairs = {k: d for k, d in pairs.items() if "orig" in d and "cuts" in d}
        def bad(r):
            tol = 2e-4 * max(1, abs(best[r["name"]]))
            return r["dual"] > best[r["name"]] + tol or (r["status"] == "optimal" and r["primal"] > best[r["name"]] + tol)
        def ok(r):
            return r["status"] in ("optimal", "gaplimit") and not bad(r)
        so = sum(ok(d["orig"]) for d in pairs.values()); sc = sum(ok(d["cuts"]) for d in pairs.values())
        only_c = [k for k, d in pairs.items() if ok(d["cuts"]) and not ok(d["orig"])]
        only_o = [k for k, d in pairs.items() if ok(d["orig"]) and not ok(d["cuts"])]
        to = sgm([d["orig"]["total_time"] if ok(d["orig"]) else TL for d in pairs.values()])
        tc = sgm([d["cuts"]["total_time"] if ok(d["cuts"]) else TL for d in pairs.values()])
        both = [d for d in pairs.values() if ok(d["orig"]) and ok(d["cuts"])]
        faster = sum(d["cuts"]["total_time"] < d["orig"]["total_time"] for d in both)
        easy = [d for d in pairs.values() if ok(d["orig"]) and d["orig"]["total_time"] < 10]
        slower_easy = sum((not ok(d["cuts"])) or d["cuts"]["total_time"] > d["orig"]["total_time"] for d in easy)
        print(f" {solver}: pairs {len(pairs)}; solved orig {so}, cuts {sc}; only cuts {len(only_c)}, only orig {len(only_o)} {only_o}")
        print(f"   sgm time orig {to:.1f} cuts {tc:.1f}; both solved {len(both)}, cuts faster on {faster}; orig<10s: {len(easy)}, cuts slower on {slower_easy}")
        over = [(k, d["cuts"]["total_time"]) for k, d in pairs.items() if d["cuts"]["total_time"] > TL + 5]
        overo = [(k, d["orig"]["total_time"]) for k, d in pairs.items() if d["orig"]["total_time"] > TL + 5]
        print(f"   runs over {TL+5}s total: cuts {len(over)} (max {max([t for _, t in over], default=0):.0f}), orig {len(overo)} (max {max([t for _, t in overo], default=0):.0f})")
        # closure by family
        fam = collections.defaultdict(list); famall = collections.defaultdict(list)
        for k, d in pairs.items():
            ci = d["cuts"]["cutinfo"]
            clos = 100 * (ci["bound"] - ci["bound0"]) / max(best[k] - ci["bound0"], 1e-9)
            fam[re.sub(r"-s\d+$", "", k)].append(clos)
        for kind in ("transport-", "netflow-", "transportfc-"):
            m = [sum(v) / len(v) for f, v in fam.items() if f.startswith(kind)]
            ind = [x for f, v in fam.items() if f.startswith(kind) for x in v]
            if m:
                print(f"   closure {kind}: family means {min(m):.1f}..{max(m):.1f}; single instances {min(ind):.1f}..{max(ind):.1f}")
        # is the 'best known' proven?  closure uses best primal over all runs
        unproven = [k for k, d in pairs.items() if not any(ok(r) for r in d.values())]
        print(f"   instances whose best-known value is not proven optimal by either form (this solver): {len(unproven)}")
        # status 13 and gaps
        for k, d in pairs.items():
            for f, r in d.items():
                if r["status"] not in ("optimal", "timelimit"):
                    print(f"   status {r['status']}: {k} {f} relgap {(r['primal']-r['dual'])/abs(r['primal']):.2e} time {r['total_time']:.0f}")
                if bad(r):
                    print(f"   INCONSISTENT: {k} {f} status {r['status']} primal {r['primal']:.4f} dual {r['dual']:.4f} best {best[k]:.4f}")
    return rows


g = analyse("main_gurobi.jsonl", ["gurobi"])
# specific quotes
by = collections.defaultdict(dict)
for r in g:
    by[r["name"]][r["form"]] = r
fam = "transport-random-quad-10x15"
d = [v for k, v in by.items() if k.startswith(fam)]
print(f"\n{fam}: node ratio sgm {sgm([x['orig']['nodes'] for x in d])/sgm([x['cuts']['nodes'] for x in d]):.2f}, "
      f"time ratio {sgm([x['cuts']['total_time'] for x in d])/sgm([x['orig']['total_time'] for x in d]):.2f}")
ct = [v["cuts"]["cutinfo"]["time"] for k, v in by.items() if "cuts" in v and v["cuts"]["cutinfo"]["rows_closed_form"] < v["cuts"]["cutinfo"]["nrows"]]
print(f"cut loop time, unequal widths: min {min(ct):.1f} median {sorted(ct)[len(ct)//2]:.1f} max {max(ct):.1f}; share in 2..6 s: {sum(2<=t<=6 for t in ct)}/{len(ct)}")
fams = collections.defaultdict(list)
for k, v in by.items():
    if "cuts" in v:
        fams[re.sub(r"-s\d+$", "", k)].append(v["cuts"]["cutinfo"]["time"])
for k, v in sorted(fams.items()):
    print(f"   cutloop mean {sum(v)/len(v):5.1f}s max {max(v):5.1f}s  {k}")
analyse("main_fc_gurobi.jsonl", ["gurobi"])
analyse("main_others.jsonl", ["scip", "baron"])
