#!/usr/bin/env python3
"""R9 (numbers lens), part 3: independent spot checks of quantitative claims
that R9_numbers_recompute.py / R9_numbers_tables.py do not cover, plus an
independent recomputation of the headline numbers.

Standard library only. Reads records.jsonl, replay.json and cases/*.json under
../experiments, the campaign-1/2 records under research-2026100{2,3}-*, and
evidence/ablation-uncertified.json. Imports no producer code and no other R9
script. Prints one block per claim group.
"""
import glob
import json
import math
import os
import statistics
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
PAPER = os.path.join(HERE, "..")
EXP = os.path.join(PAPER, "experiments")
REPO = os.path.join(PAPER, "..")
C1 = os.path.join(REPO, "research-20261002-convexification/experiments/campaign-v1")
C2 = os.path.join(REPO, "research-20261003-convexification/experiments/campaign-v2")
REP = os.path.join(REPO, "research-20261003-convexification/experiments/repair-discovery-v1")


def jl(path):
    with open(path) as fh:
        return [json.loads(x) for x in fh if x.strip()]


def recs(part):
    return jl(os.path.join(EXP, part, "records.jsonl"))


def cases(part):
    out = {}
    for f in glob.glob(os.path.join(EXP, part, "cases", "*.json")):
        d = json.load(open(f))
        out[d["name"]] = d
    return out


def fin(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def ok(r):
    pc = r.get("primal_check") or {}
    return r.get("status") in ("optimal", "gaplimit") and pc.get("passed") is True


def t(r):
    return r["total_seconds"] + (r.get("preparation_seconds") or 0.0)


def cbs(r):
    return (r.get("separation") or {}).get("callback_seconds") or 0.0


def rb(r):
    if fin(r.get("root_dual")):
        return r["root_dual"]
    if fin(r.get("dual")) and (r.get("nodes") or 0) <= 1:
        return r["dual"]
    return None


def cmpb(a, b, sense, rtol):
    tol = rtol * max(1.0, abs(a), abs(b))
    d = (a - b) if sense == "min" else (b - a)
    return 1 if d > tol else (-1 if d < -tol else 0)


def closed(z, zb, zs, sense):
    s = 1.0 if sense == "min" else -1.0
    den = s * (zs - zb)
    return None if den <= 0 else s * (z - zb) / den


def sgm(xs):
    xs = list(xs)
    return math.exp(sum(math.log(x + 1) for x in xs) / len(xs)) - 1


def nk(name):
    n = int(name.split("_n")[1].split("_")[0])
    s = int(name.split("_s")[-1])
    return n, s


def hdr(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def headline():
    hdr("H. Headline numbers, recomputed independently")
    parts = {"c3": ["v3/runs/partA-full", "v3/runs/partA-root", "v3/runs/partB", "v3/runs/partC"],
             "c3 post hoc": ["v3d/runs/partA-root-rowdir", "v3d/runs/partB-root-rowdir", "v3d/runs/partC-rowdir"],
             "c4": ["v4/runs/partB2", "v4/runs/partC2", "v4/runs/partC3", "v4/runs/partC4",
                    "v4/runs/partD-root", "v4/runs/partD-full"]}
    tot = 0
    distinct = set()
    distinct_path = set()
    per_run_dup = 0
    for g, ps in parts.items():
        s = 0
        for p in ps:
            rp = json.load(open(os.path.join(EXP, p, "replay.json")))
            n = sum(len(r.get("cuts") or []) for r in recs(p))
            assert n == rp["cuts"] == rp["replayed_cuts"] and rp["passed"], p
            tr = rp.get("tamper_rejections")
            ntr = sum(1 for v in tr.values() if v is True) if isinstance(tr, dict) else tr
            s += n
            for r in recs(p):
                for c in r.get("cuts") or []:
                    ex = c["row_certificate"]["exported"]
                    key = (r["model_sha256"], tuple(ex["coefficients"]), ex["rhs"])
                    distinct.add(key)
                    if "partC" in p:
                        distinct_path.add(key)
            print(f"  {p:30s} {n:6d} cuts, tamper controls rejected {ntr}")
        print(f"  -> {g}: {s}")
        tot += s
    print(f"  total {tot}; distinct exported rows (model, binary64 coefficients, rhs): {len(distinct)} "
          f"(path family {len(distinct_path)}, MINLPLib {len(distinct) - len(distinct_path)})")

    # 40 fresh instances
    c3, c4 = recs("v4/runs/partC3"), recs("v4/runs/partC4")
    k3, k4 = cases("v4/runs/partC3"), cases("v4/runs/partC4")
    for lab, R, K in (("C3", c3, k3), ("C4", c4, k4)):
        full = {(r["name"], r["mode"]): r for r in R if r["phase"] == "full"}
        root = {(r["name"], r["mode"]): r for r in R if r["phase"] == "root"}
        names = sorted(K, key=nk)
        cnt = {m: sum(ok(full[(nm, m)]) for nm in names) for m in sorted({k[1] for k in full})}
        g = [closed(rb(root[(nm, "rowdir-wide")]), rb(root[(nm, "baseline")]), K[nm]["known_optimum"], "min")
             for nm in names]
        print(f"  {lab}: solved {cnt}; rowdir-wide root gap closed min {min(g):.5f}")
        if lab == "C3":
            # per-instance ratio rowdir-wide / baseline on baseline-solved
            rows = []
            for nm in names:
                b, w = full[(nm, "baseline")], full[(nm, "rowdir-wide")]
                if ok(b) and ok(w):
                    rows.append((nk(nm), round(t(w) / t(b), 3)))
            print(f"    C3 per-instance total-time ratio rowdir-wide/baseline: {rows}; "
                  f"median {statistics.median(x for _, x in rows):.3f}")


def table5_borderline():
    hdr("T5. Table 5 cells near a rounding boundary (full precision)")
    c3 = recs("v3/runs/partC")
    base = {r["name"]: r for r in c3 if r["phase"] == "root" and r["mode"] == "baseline"}
    K = cases("v3/runs/partC")
    v = sorted((closed(0.0, rb(base[nm]), K[nm]["known_optimum"], "min"), nm) for nm in K if nk(nm)[0] == 40)
    print("  seeds 0-4, n=40, glued pair hulls (bound 0):", [(round(x, 6), nm) for x, nm in v],
          "median", round(v[2][0], 6))
    c3f = recs("v4/runs/partC3")
    K3 = cases("v4/runs/partC3")
    root = {(r["name"], r["mode"]): r for r in c3f if r["phase"] == "root"}
    v = sorted((closed(rb(root[(nm, "all-diag-mech")]), rb(root[(nm, "baseline")]), K3[nm]["known_optimum"], "min"), nm)
               for nm in K3 if nk(nm)[0] == 80)
    print("  seeds 5-9, n=80, remainder mech:", [(round(x, 6), nm) for x, nm in v], "median", round(v[2][0], 6))
    allm = sorted(closed(rb(root[(nm, "all-diag-mech")]), rb(root[(nm, "baseline")]), K3[nm]["known_optimum"], "min")
                  for nm in K3)
    meds = {}
    for n in (10, 20, 40, 80):
        meds[n] = round(statistics.median(closed(rb(root[(nm, "all-diag-mech")]), rb(root[(nm, "baseline")]),
                                                 K3[nm]["known_optimum"], "min") for nm in K3 if nk(nm)[0] == n), 4)
    print(f"  seeds 5-9 remainder mech per-n medians {meds}; range of per-n medians "
          f"{min(meds.values()):.4f}-{max(meds.values()):.4f}")


def native():
    hdr("N. Native SCIP separators: productive runs")

    def prod(r):
        ns = r.get("native_statistics") or {}
        sep = ns.get("separators") or {}
        nl = ns.get("nlhdlrs") or {}

        def fc(name):
            v = (sep.get(name) or {}).get("FoundCuts")
            return isinstance(v, int) and v > 0
        q = (nl.get("quadratic") or {}).get("Cuts")
        return {"intersection(quadratic nlhdlr)": isinstance(q, int) and q > 0,
                "interminor": fc("interminor"), "eccuts": fc("eccuts"), "minor": fc("minor"), "rlt": fc("rlt")}

    for p in ["v4/runs/partB2", "v4/runs/partC2", "v4/runs/partC3", "v4/runs/partC4", "v4/runs/partD-root"]:
        for m in ["baseline-extra", "baseline", "baseline-novarlocks", "baseline-noaggr"]:
            rs = [r for r in recs(p) if r["mode"] == m and r["phase"] == "root"]
            if not rs:
                continue
            c = Counter()
            for r in rs:
                for k, v in prod(r).items():
                    c[k] += v
            print(f"  {p:22s} {m:20s} runs {len(rs):2d}: {dict(c)}")


def b2_extra():
    hdr("B2. baseline-extra closure on Part B models (against reference_primal)")
    b2 = {(r["name"], r["mode"]): r for r in recs("v4/runs/partB2")}
    c3 = {r["name"]: r for r in recs("v3/runs/partB") if r["phase"] == "root" and r["mode"] == "baseline"}
    K = cases("v4/runs/partB2")
    full, gt95 = [], []
    for nm in sorted(c3):
        ref = K[nm].get("reference_primal")
        if ref is None:
            continue
        sense = c3[nm]["sense"]
        g = closed(rb(b2[(nm, "baseline-extra")]), rb(c3[nm]), float(ref), sense)
        if g is None:
            continue
        if g >= 1 - 1e-6 or cmpb(rb(b2[(nm, "baseline-extra")]), float(ref), sense, 1e-4) >= 0:
            full.append((nm, round(g, 4)))
        elif g > 0.95:
            gt95.append((nm, round(g, 4)))
    print(f"  closed completely: {full}")
    print(f"  closed >95%: {gt95}")
    # certified cuts had an effect on: (from Part B root runs) bental4tp, bental4pq, ex3_1_4, pointpack04
    # rejected rows on c1p12
    for p, m in [("v3/runs/partB", "all-diag"), ("v4/runs/partB2", "all-diag-noaggr"), ("v4/runs/partB2", "all-noaggr")]:
        rs = [r for r in recs(p) if r["mode"] == m and r["phase"] == "root"]
        rej = sum((r.get("separation") or {}).get("row_binding_rejections", 0) for r in rs)
        cut = sum((r.get("separation") or {}).get("cuts", 0) for r in rs)
        c1 = [r for r in rs if r["name"] == "kall_circlespolygons_c1p12"][0]
        s = c1["separation"]
        print(f"  {p} {m}: stored-row rejected {rej} of {rej + cut} violated ({100 * rej / (rej + cut):.1f}%); "
              f"c1p12 rejected {s['row_binding_rejections']} of {s['row_binding_rejections'] + s['cuts']}, "
              f"cuts {s['cuts']}, root bound {rb(c1)}, ref {K['kall_circlespolygons_c1p12'].get('reference_primal')}")


def part_d():
    hdr("D. Part D full runs: which models received cuts; bound differences")
    full = {(r["name"], r["mode"]): r for r in recs("v4/runs/partD-full")}
    names = sorted({k[0] for k in full})
    for m in ["all", "auto"]:
        withcuts = [(nm, len(full[(nm, m)]["cuts"])) for nm in names if full[(nm, m)].get("cuts")]
        diffs = []
        for nm in names:
            a, b = full[(nm, m)], full[(nm, "baseline")]
            c = cmpb(a["dual"], b["dual"], a["sense"], 1e-4)
            if c:
                diffs.append((nm, c))
        print(f"  {m}: models with cuts {withcuts}; final-bound differences (1 better, -1 worse) {diffs}")
    root = {(r["name"], r["mode"]): r for r in recs("v4/runs/partD-root")}
    withcuts = [(nm, len(root[(nm, 'all')]['cuts'])) for nm in names if root[(nm, 'all')].get('cuts')]
    print(f"  root runs, mode all: models with cuts {withcuts}")


def gurobi_gaps():
    hdr("G. Gurobi gaps on n=40, 80 (path family, non-binding)")
    for p, lab in [("v4/runs/partC2", "seeds 0-4"), ("v4/runs/partC3", "seeds 5-9")]:
        gs = [r.get("mip_gap") for r in recs(p) if r["mode"] == "gurobi" and r["phase"] == "full"
              and nk(r["name"])[0] in (40, 80)]
        print(f"  {lab}: gap range {min(gs):.3f}-{max(gs):.3f}")
        ns = sorted(nk(r["name"]) for r in recs(p) if r["mode"] == "gurobi" and r["phase"] == "full" and ok(r))
        print(f"    solved {ns}")


def loads():
    hdr("L. One-minute load average at run start")
    groups = {"c3 prospective": ["v3/runs/partA-full", "v3/runs/partA-root", "v3/runs/partB", "v3/runs/partC"],
              "c3 post hoc 3D": ["v3d/runs/partA-root-rowdir", "v3d/runs/partB-root-rowdir", "v3d/runs/partC-rowdir"],
              "c4": ["v4/runs/partB2", "v4/runs/partC2", "v4/runs/partC3", "v4/runs/partC4",
                     "v4/runs/partD-root", "v4/runs/partD-full"]}
    for g, ps in groups.items():
        ls = sorted(r["load_start"][0] for p in ps for r in recs(p) if r.get("load_start"))
        q = lambda f: ls[int(f * (len(ls) - 1))]
        print(f"  {g:16s} n={len(ls)} min {ls[0]:.2f} p5 {q(0.05):.2f} median {q(0.5):.2f} "
              f"p95 {q(0.95):.2f} max {ls[-1]:.2f}")


def campaign2():
    hdr("F2. Campaign 2 (App. F) at the relative tolerance 1e-4")
    R = jl(os.path.join(C2, "records.jsonl"))
    full = {(r["name"], r["mode"]): r for r in R if r["phase"] == "full" and r["suite"] == "holdout"}
    root = {(r["name"], r["mode"]): r for r in R if r["phase"] == "root" and r["suite"] == "holdout"}
    names = sorted({k[0] for k in full})
    for m in ["all", "auto"]:
        for lab, ix, bf in (("final", full, lambda r: r["dual"]), ("root", root, rb)):
            better, worse = [], []
            for nm in names:
                a, b = ix[(nm, m)], ix[(nm, "baseline")]
                za, zb = bf(a), bf(b)
                if not (fin(za) and fin(zb)):
                    continue
                c = cmpb(za, zb, a["sense"], 1e-4)
                (better if c == 1 else worse if c == -1 else []).append(nm)
            print(f"  {m:4s} {lab:5s}: better {better}; worse {worse}")
    solved = [nm for nm in names if all(ok(full[(nm, m)]) for m in ("baseline", "all", "auto"))]
    print(f"  commonly solved {len(solved)}")
    for tf, lab in ((t, "total+prep"), (lambda r: r["total_seconds"], "total")):
        print(f"  SGM ({lab}): " + ", ".join(f"{m} {sgm(tf(full[(nm, m)]) for nm in solved):.3f}"
                                            for m in ("baseline", "all", "auto")))
    slow = [nm for nm in solved if all(t(full[(nm, m)]) > 1.1 * t(full[(nm, "baseline")]) for m in ("all", "auto"))]
    print(f"  both cut modes >10% slower on {len(slow)} of {len(solved)}")
    s = Counter()
    for nm in names:
        for k, v in (full[(nm, "all")].get("separation") or {}).items():
            if fin(v):
                s[k] += v
    print(f"  mode all, 30 full runs: callback {s['callback_seconds']:.2f}, discovery {s['discovery_seconds']:.2f}, "
          f"LPs {s['candidate_seconds']:.2f}, certification {s['certification_seconds']:.2f}")
    for m in ("all", "auto"):
        wc = [(nm, len(full[(nm, m)]["cuts"])) for nm in names if full[(nm, m)].get("cuts")]
        atroot = [nm for nm, _ in wc if all((full[(nm, mm)].get("nodes") or 0) <= 1 for mm in ("baseline", "all", "auto"))]
        print(f"  {m}: models with cuts {len(wc)} ({sum(c for _, c in wc)} cuts) {wc}; solved at root in every mode: {atroot}; "
              f"baseline solved all of them: {all(ok(full[(nm, 'baseline')]) for nm, _ in wc)}")
    diag = {(r["name"], r["mode"]): r for r in R if r["suite"] == "diagnostic"}
    if ("btest14", "baseline") in diag:
        print(f"  btest14 final dual: " + ", ".join(f"{m} {diag[('btest14', m)]['dual']}" for m in ("baseline", "all", "auto")))
    # overrun of the allowance in cut-mode runs
    over = []
    for r in R:
        if r["mode"] in ("all", "auto"):
            s_ = r.get("separation") or {}
            cfg = r.get("config") or {}
            allow = min(cfg.get("max_separation_seconds", 1.0), cfg.get("separation_budget_fraction", 0.05) * r["time_limit"])
            ex = (s_.get("callback_seconds") or 0.0) - allow
            if ex > 1e-3:
                over.append(ex)
    print(f"  cut-mode runs whose callback time exceeded the allowance: {len(over)}, max excess {max(over):.2f} s")
    nchk = sum(1 for r in R if (r.get("primal_check") or {}).get("checked"))
    npass = sum(1 for r in R if (r.get("primal_check") or {}).get("passed"))
    RR = jl(os.path.join(REP, "records.jsonl"))
    nchk2 = sum(1 for r in RR if (r.get("primal_check") or {}).get("checked"))
    npass2 = sum(1 for r in RR if (r.get("primal_check") or {}).get("passed"))
    print(f"  incumbents checked/passed: campaign 2 {nchk}/{npass}; repair cohort {nchk2}/{npass2}; total {nchk + nchk2}")
    rf = {(r["name"], r["mode"]): r for r in RR if r["phase"] == "full"}
    for nm in ("waterno2_06", "waterx"):
        if (nm, "baseline") in rf:
            print(f"  repair {nm}: " + ", ".join(f"{m} {rf[(nm, m)]['dual']:.4g} ({rf[(nm, m)]['status']}, cuts {len(rf[(nm, m)].get('cuts') or [])})"
                                                for m in ("baseline", "all", "auto")))


def campaign1():
    hdr("F1. Campaign 1 (App. F)")
    R = jl(os.path.join(C1, "records.jsonl"))
    full = {(r["name"], r["mode"]): r for r in R if r["phase"] == "full" and r["suite"] == "holdout"}
    names = sorted({k[0] for k in full})
    modes = ("baseline", "control", "all", "auto")
    solved = [nm for nm in names if all(ok(full[(nm, m)]) for m in modes)]
    print(f"  holdout models {len(names)}; solved in every mode {len(solved)}")
    print("  SGM (total+prep): " + ", ".join(f"{m} {sgm(t(full[(nm, m)]) for nm in solved):.3f}" for m in modes))
    print("  SGM (total): " + ", ".join(f"{m} {sgm(full[(nm, m)]['total_seconds'] for nm in solved):.3f}" for m in modes))
    print("  solved per mode: " + ", ".join(f"{m} {sum(ok(full[(nm, m)]) for nm in names)}" for m in modes))
    hist = {(r["name"], r["mode"]): r for r in R if r["suite"] == "historical" and r["phase"] == "full"}
    print("  waterno2_06 final dual: " + ", ".join(f"{m} {hist[('waterno2_06', m)]['dual']:.4g}" for m in modes))


def ablation_path_removal():
    hdr("U. Path-family ablation: removals by incumbents vs by the case witness only")
    d = json.load(open(os.path.join(PAPER, "evidence", "ablation-uncertified.json")))
    cuts = [c for c in d["cuts"] if c.get("family") == "path" or "partC" in c.get("part", "")]
    keys = sorted({k for c in cuts[:1] for k in c})
    print(f"  path cuts in JSON: {len(cuts)}; example keys: {keys}")
    for v in ("u1", "u2"):
        rem = [c for c in cuts if c.get(v + "_material") and (c.get(v + "_rows") or {}).get("removed")]
        print(f"  {v}: removing {len(rem)}; example removed field: {str((rem[0].get(v + '_rows') or {}).get('removed'))[:300] if rem else None}")


def main():
    headline()
    table5_borderline()
    native()
    b2_extra()
    part_d()
    gurobi_gaps()
    loads()
    campaign2()
    campaign1()
    ablation_path_removal()


if __name__ == "__main__":
    main()
