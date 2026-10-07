#!/usr/bin/env python3
"""R9 (numbers lens): independent standard-library recomputation of the
quantitative claims of the manuscript from the raw run records.

Reads only records.jsonl, replay.json and cases/*.json under ../experiments.
Imports no producer code. Prints one block per claim group; the report
evidence/review2-numbers.md cites these blocks.

Definitions (from Section 8.1 of the manuscript):
  solved      status optimal or gaplimit, returncode 0, primal_check passed
  time        total_seconds + preparation_seconds
  SCIP excl.  scip_solve_seconds - separation.callback_seconds
  root bound  root_dual if finite, else dual for a run that ended at the root
  gap closed  (z_mode - z_base) / (z* - z_base)  (sign-adjusted for max)
  SGM         exp(mean(log(t + 1))) - 1
"""
import glob
import json
import math
import os
import statistics
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.join(HERE, "..", "experiments")


def load(part):
    path = os.path.join(EXP, part, "records.jsonl")
    with open(path) as fh:
        return [json.loads(line) for line in fh]


def cases(part):
    out = {}
    for f in glob.glob(os.path.join(EXP, part, "cases", "*.json")):
        d = json.load(open(f))
        out[d["name"]] = d
    return out


def finite(x):
    return isinstance(x, (int, float)) and math.isfinite(x)


def solved(r):
    pc = r.get("primal_check") or {}
    return (r.get("status") in ("optimal", "gaplimit") and r.get("returncode", 0) == 0
            and not r.get("worker_status") and pc.get("passed") is True)


def ttime(r):
    return r["total_seconds"] + (r.get("preparation_seconds") or 0.0)


def cb(r):
    s = r.get("separation") or {}
    return s.get("callback_seconds") or 0.0


def scip_time(r):
    return r.get("scip_solve_seconds") if r.get("scip_solve_seconds") is not None else r.get("solver_runtime_seconds")


def root_bound(r):
    if finite(r.get("root_dual")):
        return r["root_dual"]
    if finite(r.get("dual")) and (r.get("node_limit") == 1 or (r.get("nodes") or 0) <= 1):
        return r["dual"]
    return None


def sgm(xs):
    xs = list(xs)
    if not xs:
        return float("nan")
    return math.exp(sum(math.log(x + 1.0) for x in xs) / len(xs)) - 1.0


def cmp_bound(a, b, sense, rtol=1e-4):
    """+1 if a better than b, -1 worse, 0 tie."""
    tol = rtol * max(1.0, abs(a), abs(b))
    s = 1.0 if sense == "min" else -1.0
    d = s * (a - b)
    if d > tol:
        return 1
    if d < -tol:
        return -1
    return 0


def gap_closed(zm, zb, zs, sense):
    s = 1.0 if sense == "min" else -1.0
    den = s * (zs - zb)
    if den <= 0:
        return None
    return s * (zm - zb) / den


def r2(x, d=2):
    return f"{x:.{d}f}"


def hdr(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


# ---------------------------------------------------------------- replay
def replay_totals():
    hdr("1. Replay totals (replay.json) and duplicate cut lists")
    groups = {
        "c3 prospective": ["v3/runs/partA-full", "v3/runs/partA-root", "v3/runs/partB", "v3/runs/partC"],
        "c3 post hoc (v3d)": ["v3d/runs/partA-root-rowdir", "v3d/runs/partB-root-rowdir", "v3d/runs/partC-rowdir"],
        "c4": ["v4/runs/partB2", "v4/runs/partC2", "v4/runs/partC3", "v4/runs/partC4",
               "v4/runs/partD-root", "v4/runs/partD-full"],
    }
    grand = 0
    path_total = 0
    minl_total = 0
    for g, parts in groups.items():
        tot = 0
        for p in parts:
            rp = json.load(open(os.path.join(EXP, p, "replay.json")))
            assert rp["passed"] and rp["cuts"] == rp["replayed_cuts"], p
            assert rp.get("missing_cut_logs", 0) == 0
            tr = rp["tamper_rejections"]
            # count recorded cuts directly
            recs = load(p)
            n_rec = sum(len(r.get("cuts") or []) for r in recs)
            assert n_rec == rp["cuts"], (p, n_rec, rp["cuts"])
            print(f"  {p:32s} cuts {rp['cuts']:6d} replayed {rp['replayed_cuts']:6d} "
                  f"tamper {tr.get('rejected', tr) if isinstance(tr, dict) else tr}")
            tot += rp["cuts"]
            if "partC" in p:
                path_total += rp["cuts"]
            else:
                minl_total += rp["cuts"]
        print(f"  -> {g}: {tot}")
        grand += tot
    print(f"  GRAND TOTAL {grand}; path family {path_total}; MINLPLib {minl_total}")

    # duplicates: path-family root and full runs of the same instance and mode
    print("  Path family: are root-run and full-run cut lists identical?")
    distinct_total = 0
    for p in ["v3/runs/partC", "v3d/runs/partC-rowdir", "v4/runs/partC2", "v4/runs/partC3", "v4/runs/partC4"]:
        recs = load(p)
        by = defaultdict(dict)
        for r in recs:
            if r.get("cuts"):
                key = [(tuple(c.get("coefficients") or []), json.dumps(c.get("signed_sides"), sort_keys=True),
                        c.get("block")) for c in r["cuts"]]
                by[(r["name"], r["mode"])][r["phase"]] = key
        same = diff = 0
        dist = 0
        for k, v in by.items():
            if "root" in v and "full" in v:
                if v["root"] == v["full"]:
                    same += 1
                    dist += len(v["root"])
                else:
                    diff += 1
                    dist += len(v["root"]) + len(v["full"])
            else:
                dist += sum(len(x) for x in v.values())
        distinct_total += dist
        print(f"    {p:28s} pairs identical {same}, different {diff}; cut records after removing "
              f"duplicated root/full lists: {dist}")
    print(f"    path-family cuts without the root/full duplication: {distinct_total}")


# ---------------------------------------------------------------- MINLPLib
def minlplib_table():
    hdr("2. Table 2 (full runs on MINLPLib) and Section 8.3 text")
    specs = [("A", "v3/runs/partA-full", ["baseline", "all", "auto"]),
             ("B", "v3/runs/partB", ["baseline", "all", "auto"]),
             ("D", "v4/runs/partD-full", ["baseline", "all", "auto", "baseline-extra"])]
    for label, part, modes in specs:
        recs = [r for r in load(part) if r["phase"] == "full"]
        by = {(r["name"], r["seed"], r["mode"]): r for r in recs}
        keys = sorted({(r["name"], r["seed"]) for r in recs})
        print(f"  Part {label}: {len(keys)} model-seed pairs")
        common = [k for k in keys if all(solved(by[k + (m,)]) for m in modes)]
        print(f"    solved by every mode: {len(common)}")
        for m in modes:
            rs = [by[k + (m,)] for k in keys]
            ns = sum(solved(r) for r in rs)
            ncut = sum(len(r.get("cuts") or []) for r in rs)
            nrun = sum(1 for r in rs if r.get("cuts"))
            nmod = len({r["name"] for r in rs if r.get("cuts")})
            t = sgm(ttime(by[k + (m,)]) for k in common)
            te = sgm(max(0.0, scip_time(by[k + (m,)]) - cb(by[k + (m,)])) for k in common)
            # ratio: pairwise solved with baseline, and all-mode common
            pair = [k for k in keys if solved(by[k + (m,)]) and solved(by[k + ("baseline",)])]
            rat_pair = statistics.median(ttime(by[k + (m,)]) / ttime(by[k + ("baseline",)]) for k in pair) if pair else float("nan")
            rat_comm = statistics.median(ttime(by[k + (m,)]) / ttime(by[k + ("baseline",)]) for k in common) if common else float("nan")
            bet = wor = 0
            for k in keys:
                a, b = by[k + (m,)], by[k + ("baseline",)]
                if m == "baseline":
                    continue
                if finite(a.get("dual")) and finite(b.get("dual")):
                    c = cmp_bound(a["dual"], b["dual"], a["sense"])
                    bet += c == 1
                    wor += c == -1
            print(f"    {m:15s} solved {ns}/{len(keys)} cuts {ncut} (runs {nrun}, models {nmod}) "
                  f"SGM {t:.3f} SCIPexcl {te:.3f} ratio(pair {len(pair)}) {rat_pair:.3f} "
                  f"ratio(common) {rat_comm:.3f} bounds {bet}/{wor}")
        # all modes same solved set per seed?
        same = True
        for seed in sorted({k[1] for k in keys}):
            sets = [frozenset(k[0] for k in keys if k[1] == seed and solved(by[k + (m,)])) for m in modes if m != "baseline-extra"]
            same &= len(set(sets)) == 1
        print(f"    all cut modes and baseline solved the same models in each seed: {same}")
        # SGM slowdowns
        base_t = sgm(ttime(by[k + ("baseline",)]) for k in common)
        for m in modes[1:]:
            mt = sgm(ttime(by[k + (m,)]) for k in common)
            print(f"    SGM slowdown {m}: {100*(mt/base_t-1):.1f}%")
        # node sums over commonly solved runs
        nb = sum(by[k + ("baseline",)]["nodes"] for k in common)
        for m in modes[1:]:
            nm = sum(by[k + (m,)]["nodes"] for k in common)
            print(f"    node sum {m} vs baseline over common: {nm} vs {nb} ({100*(nm/nb-1):+.2f}%)")
        # median SCIP time of baseline
        print(f"    median baseline SCIP time over all runs: {statistics.median(scip_time(by[k + ('baseline',)]) for k in keys):.3f} s")
        if label in ("A", "B"):
            # baseline seed variation
            seeds = sorted({k[1] for k in keys})
            names = sorted({k[0] for k in keys})
            diffs = 0
            comps = 0
            for n in names:
                for i in range(len(seeds)):
                    for j in range(i + 1, len(seeds)):
                        a, b = by[(n, seeds[i], "baseline")], by[(n, seeds[j], "baseline")]
                        comps += 1
                        if cmp_bound(a["dual"], b["dual"], a["sense"]) != 0:
                            diffs += 1
            # also only seed 0 vs others
            d0 = 0
            c0 = 0
            for n in names:
                for s in seeds[1:]:
                    a, b = by[(n, seeds[0], "baseline")], by[(n, s, "baseline")]
                    c0 += 1
                    d0 += cmp_bound(a["dual"], b["dual"], a["sense"]) != 0
            models_diff = sorted({n for n in names if len({round(by[(n, s, 'baseline')]['dual'], 12) for s in seeds}) > 1
                                  and any(cmp_bound(by[(n, s, 'baseline')]['dual'], by[(n, seeds[0], 'baseline')]['dual'], 'min') != 0 for s in seeds)})
            print(f"    baseline final-bound differences between seeds: {diffs} of {comps} seed pairs; "
                  f"seed 0 vs others {d0} of {c0}; models {models_diff}")
            # SCIP excl SGM difference vs baseline
            bt = sgm(scip_time(by[k + ("baseline",)]) for k in common)
            for m in modes[1:]:
                et = sgm(max(0.0, scip_time(by[k + (m,)]) - cb(by[k + (m,)])) for k in common)
                print(f"    SCIP-excl SGM {m} vs baseline SCIP SGM: {et:.4f} vs {bt:.4f} ({100*(et/bt-1):+.2f}%)")
            # callback per run
            for m in modes[1:]:
                c = [cb(by[k + (m,)]) for k in keys]
                print(f"    callback {m}: total {sum(c):.2f} s, per run {sum(c)/len(c):.3f} s")


def minlplib_root():
    hdr("3. MINLPLib root runs (Part A, B, B2, D)")
    for part in ["v3/runs/partA-root", "v3/runs/partB"]:
        recs = [r for r in load(part) if r["phase"] == "root"]
        cs = cases(part)
        by = {(r["name"], r["mode"]): r for r in recs}
        names = sorted({r["name"] for r in recs})
        print(f"  {part}")
        for m in ["all", "auto", "all-diag"]:
            better, worse = [], []
            ncut = 0
            for n in names:
                a, b = by[(n, m)], by[(n, "baseline")]
                ncut += len(a.get("cuts") or [])
                za, zb = root_bound(a), root_bound(b)
                if za is None or zb is None:
                    continue
                c = cmp_bound(za, zb, a["sense"])
                if c == 1:
                    better.append((n, zb, za))
                if c == -1:
                    worse.append((n, zb, za))
            print(f"    {m:9s} cuts {ncut}; better {[(n, round(zb,4), round(za,4)) for n,zb,za in better]}")
            print(f"    {'':9s} worse {[(n, round(zb,4), round(za,4)) for n,zb,za in worse]}")
        # solved at root by baseline
        print(f"    solved at root (status optimal/gaplimit) baseline: "
              f"{sum(solved(by[(n,'baseline')]) for n in names)}")
    # B2
    part = "v4/runs/partB2"
    recs = load(part)
    by = {(r["name"], r["mode"]): r for r in recs}
    c3 = {r["name"]: r for r in load("v3/runs/partB") if r["phase"] == "root" and r["mode"] == "baseline"}
    names = sorted({r["name"] for r in recs})
    print(f"  {part}")
    for m, ref in [("all-noaggr", "baseline-noaggr"), ("all-diag-noaggr", "baseline-noaggr"),
                   ("all-diag-rowdir-noaggr", "baseline-noaggr")]:
        b = w = 0
        for n in names:
            c = cmp_bound(root_bound(by[(n, m)]), root_bound(by[(n, ref)]), by[(n, m)]["sense"])
            b += c == 1
            w += c == -1
        print(f"    {m} vs {ref}: better {b} worse {w}")
    for m in ["baseline-noaggr", "baseline-extra"]:
        b = w = 0
        for n in names:
            c = cmp_bound(root_bound(by[(n, m)]), root_bound(c3[n]), c3[n]["sense"])
            b += c == 1
            w += c == -1
        print(f"    {m} vs c3 baseline: better {b} worse {w}; solved at root {sum(solved(by[(n,m)]) for n in names)} "
              f"vs c3 baseline {sum(solved(c3[n]) for n in names)}")
    # identical cuts all-diag vs all-diag-rowdir (noaggr)
    same_lists = 0
    for n in names:
        a = [tuple(c["coefficients"]) for c in by[(n, "all-diag-noaggr")].get("cuts") or []]
        b = [tuple(c["coefficients"]) for c in by[(n, "all-diag-rowdir-noaggr")].get("cuts") or []]
        same_lists += a == b
    print(f"    all-diag-noaggr vs all-diag-rowdir-noaggr: identical cut direction lists on {same_lists}/30 models")


# ---------------------------------------------------------------- funnel
def funnel():
    hdr("4. Table 5 (funnel), sums over runs")
    rows = [("3A full", "v3/runs/partA-full", "full", "all"),
            ("3B full", "v3/runs/partB", "full", "all"),
            ("3B root", "v3/runs/partB", "root", "all-diag"),
            ("4B2 root", "v4/runs/partB2", "root", "all-diag-noaggr"),
            ("4D root", "v4/runs/partD-root", "root", "all"),
            ("4D root", "v4/runs/partD-root", "root", "all-diag"),
            ("3C", "v3/runs/partC", "root", "all-diag-mech"),
            ("4C2", "v4/runs/partC2", "root", "frozen-wide"),
            ("4C3", "v4/runs/partC3", "root", "rowdir-wide"),
            ("4C4", "v4/runs/partC4", "root", "frozen-wide"),
            ("4C4", "v4/runs/partC4", "root", "rowdir-wide")]
    for lab, part, ph, m in rows:
        rs = [r for r in load(part) if r["phase"] == ph and r["mode"] == m]
        s = Counter()
        for r in rs:
            for k, v in (r.get("separation") or {}).items():
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    s[k] += v
        cert = s["certification_calls"] - s["certification_failures"]
        below = cert - s["row_rounding_rejections"] - s["row_binding_rejections"] - s["cuts"]
        viol = s["row_binding_rejections"] + s["cuts"]
        print(f"  {lab:8s} {m:16s} runs {len(rs):3d} calls {s['certification_calls']:6d} fail {s['certification_failures']:4d} "
              f"below {below:5d} ({100*below/cert:.1f}% of certified) stored-rej {s['row_binding_rejections']:4d} "
              f"({100*s['row_binding_rejections']/viol:.1f}% of violated) round-rej {s['row_rounding_rejections']} "
              f"cuts {s['cuts']:6d} | cb {s['callback_seconds']:.1f} disc {s['discovery_seconds']:.1f} "
              f"LP {s['candidate_seconds']:.1f} cert {s['certification_seconds']:.1f}")


# ---------------------------------------------------------------- path family
def path_family():
    hdr("5. Path family (Table 4, Tables 11-12, Section 8.5 text)")

    def grp(name):
        n = int(name.split("_n")[1].split("_")[0])
        s = int(name.split("_s")[-1])
        return n, s

    sets = {}
    c3 = load("v3/runs/partC")
    v3d = load("v3d/runs/partC-rowdir")
    c2 = load("v4/runs/partC2")
    c3f = load("v4/runs/partC3")
    c4 = load("v4/runs/partC4")
    cs_old = cases("v3/runs/partC")
    cs_c3 = cases("v4/runs/partC3")
    cs_c4 = cases("v4/runs/partC4")

    def idx(recs, ph):
        return {(r["name"], r["mode"]): r for r in recs if r["phase"] == ph}

    # ---- seeds 0-4
    base = idx(c3, "root")
    roots = {"checkvarlocks off": (idx(c2, "root"), "baseline-novarlocks"),
             "extra": (idx(c2, "root"), "baseline-extra"),
             "remainder mech (c3)": (base, "all-diag-mech"),
             "remainder wide": (idx(c2, "root"), "frozen-wide"),
             "whole row mech (v3d)": (idx(v3d, "root"), "all-diag-mech"),
             "whole row wide (v3d)": (idx(v3d, "root"), "all-diag-mech-wide")}
    names = sorted({r["name"] for r in c3}, key=grp)
    print("  seeds 0-4: root gap closed, median per n (exact value, 2-decimal rounding)")
    pair_hull = defaultdict(list)
    for nm in names:
        zb = root_bound(base[(nm, "baseline")])
        zs = cs_old[nm]["known_optimum"]
        pair_hull[grp(nm)[0]].append(gap_closed(0.0, zb, zs, "min"))
    print("    glued pair hulls:", {n: (round(statistics.median(v), 4), r2(statistics.median(v))) for n, v in pair_hull.items()})
    for lab, (ix, m) in roots.items():
        per = defaultdict(list)
        for nm in names:
            zb = root_bound(base[(nm, "baseline")])
            zs = cs_old[nm]["known_optimum"]
            per[grp(nm)[0]].append(gap_closed(root_bound(ix[(nm, m)]), zb, zs, "min"))
        print(f"    {lab:22s}", {n: (round(statistics.median(v), 4), r2(statistics.median(v))) for n, v in per.items()})
    # v3d baseline equal to c3 baseline?
    vb = idx(v3d, "root")
    eq = sum(1 for nm in names if root_bound(vb[(nm, "baseline")]) == root_bound(base[(nm, "baseline")]))
    print(f"    v3d baseline root bound equals c3 baseline on {eq}/20")
    # per-copy baseline root bound
    pc = [root_bound(base[(nm, "baseline")]) / grp(nm)[0] for nm in names]
    print(f"    baseline root bound per copy: min {min(pc):.4f} max {max(pc):.4f}")
    nv = [root_bound(idx(c2, 'root')[(nm, 'baseline-novarlocks')]) for nm in names]
    print(f"    novarlocks root bounds: min {min(nv):.6f} max {max(nv):.6f}")
    fw = idx(c2, "root")
    above = [nm for nm in names if root_bound(fw[(nm, "frozen-wide")]) > 0]
    print(f"    frozen-wide root bound above 0 (pair-hull level) on {len(above)}: {above}")

    # solved counts seeds 0-4
    full_sets = {"SCIP default": (idx(c3, "full"), "baseline"),
                 "checkvarlocks off": (idx(c2, "full"), "baseline-novarlocks"),
                 "extra": (idx(c2, "full"), "baseline-extra"),
                 "Gurobi": (idx(c2, "full"), "gurobi"),
                 "remainder mech (c3)": (idx(c3, "full"), "all-diag-mech"),
                 "remainder wide": (idx(c2, "full"), "frozen-wide"),
                 "whole row mech (v3d)": (idx(v3d, "full"), "all-diag-mech"),
                 "whole row wide (v3d)": (idx(v3d, "full"), "all-diag-mech-wide")}
    print("  seeds 0-4: solved within 300 s")
    for lab, (ix, m) in full_sets.items():
        sv = [nm for nm in names if solved(ix[(nm, m)])]
        print(f"    {lab:22s} {len(sv)}")
    # c3 sep vs baseline on 9 commonly solved
    fb = idx(c3, "full")
    com = [nm for nm in names if solved(fb[(nm, "baseline")]) and solved(fb[(nm, "all-diag-mech")])]
    print(f"    c3 baseline vs all-diag-mech on {len(com)} common: SGM {sgm(ttime(fb[(n,'baseline')]) for n in com):.2f} -> "
          f"{sgm(ttime(fb[(n,'all-diag-mech')]) for n in com):.2f}; nodes sum {sum(fb[(n,'baseline')]['nodes'] for n in com)} -> "
          f"{sum(fb[(n,'all-diag-mech')]['nodes'] for n in com)}; median nodes "
          f"{statistics.median(fb[(n,'baseline')]['nodes'] for n in com)} -> {statistics.median(fb[(n,'all-diag-mech')]['nodes'] for n in com)}; "
          f"fewer nodes on {sum(fb[(n,'all-diag-mech')]['nodes'] < fb[(n,'baseline')]['nodes'] for n in com)}")
    # root runs improved on all 20 by c3 separator
    imp = sum(cmp_bound(root_bound(base[(nm, 'all-diag-mech')]), root_bound(base[(nm, 'baseline')]), 'min') == 1 for nm in names)
    print(f"    c3 separator improved root bound on {imp}/20")
    # frozen-wide extra solved instances and times
    fwf = idx(c2, "full")
    extra_inst = [(nm, round(ttime(fwf[(nm, 'frozen-wide')]), 2)) for nm in names
                  if solved(fwf[(nm, 'frozen-wide')]) and not solved(fb[(nm, 'baseline')])]
    print(f"    frozen-wide solved beyond baseline: {extra_inst}")
    # v3d wide: solved at root node in root runs; full-run nodes
    vr = idx(v3d, "root")
    vf = idx(v3d, "full")
    print(f"    v3d whole-row wide: root runs solved at root {sum(solved(vr[(nm,'all-diag-mech-wide')]) for nm in names)}; "
          f"full runs with 1 node {sum(1 for nm in names if vf[(nm,'all-diag-mech-wide')]['nodes'] <= 1)}")
    # cut caps in four cells
    def capped(ix, m):
        return sum(1 for nm in names if len(ix[(nm, m)].get("cuts") or []) >= ix[(nm, m)]["config"]["max_cuts"])
    print(f"    cut cap reached: c3 mech {capped(base,'all-diag-mech')}, frozen-wide {capped(fw,'frozen-wide')}, "
          f"v3d mech {capped(vr,'all-diag-mech')}, v3d wide {capped(vr,'all-diag-mech-wide')} (root runs, of 20)")
    # Gurobi C2 gaps
    gi = idx(c2, "full")
    for n in (10, 20, 40, 80):
        gs = [gi[(nm, 'gurobi')].get('mip_gap') for nm in names if grp(nm)[0] == n]
        print(f"    Gurobi C2 n={n} mip_gap {[round(g,3) if g is not None else None for g in gs]}")

    # ---- seeds 5-9 non-binding (C3)
    names3 = sorted({r["name"] for r in c3f}, key=grp)
    b3 = idx(c3f, "root")
    print("  seeds 5-9 (C3): root gap closed, median per n")
    ph = defaultdict(list)
    for nm in names3:
        ph[grp(nm)[0]].append(gap_closed(0.0, root_bound(b3[(nm, "baseline")]), cs_c3[nm]["known_optimum"], "min"))
    print("    glued pair hulls:", {n: (round(statistics.median(v), 4), r2(statistics.median(v))) for n, v in ph.items()})
    for m in ["baseline-extra", "all-diag-mech", "rowdir-wide"]:
        per = defaultdict(list)
        mins = []
        for nm in names3:
            g = gap_closed(root_bound(b3[(nm, m)]), root_bound(b3[(nm, "baseline")]), cs_c3[nm]["known_optimum"], "min")
            per[grp(nm)[0]].append(g)
            mins.append(g)
        print(f"    {m:16s}", {n: (round(statistics.median(v), 4), r2(statistics.median(v))) for n, v in per.items()},
              f"min {min(mins):.4f}")
    dev = [root_bound(b3[(nm, 'rowdir-wide')]) - cs_c3[nm]['known_optimum'] for nm in names3]
    print(f"    rowdir-wide root bound - optimum in [{min(dev):.2e}, {max(dev):.2e}]")
    f3 = idx(c3f, "full")
    for m in ["baseline", "baseline-extra", "gurobi", "all-diag-mech", "rowdir-wide"]:
        sv = [nm for nm in names3 if solved(f3[(nm, m)])]
        print(f"    solved {m:16s} {len(sv)}")
    rw = [f3[(nm, 'rowdir-wide')] for nm in names3]
    print(f"    rowdir-wide full: times {min(ttime(r) for r in rw):.2f}-{max(ttime(r) for r in rw):.2f}, "
          f"median nodes {statistics.median(r['nodes'] for r in rw)}, max {max(r['nodes'] for r in rw)}; "
          f"callback share over 20 runs {sum(cb(r) for r in rw)/sum(ttime(r) for r in rw):.4f}")
    com = [nm for nm in names3 if solved(f3[(nm, 'baseline')]) and solved(f3[(nm, 'rowdir-wide')])]
    rat = statistics.median(ttime(f3[(n, 'rowdir-wide')]) / ttime(f3[(n, 'baseline')]) for n in com)
    srat = statistics.median((scip_time(f3[(n, 'rowdir-wide')]) - cb(f3[(n, 'rowdir-wide')])) / scip_time(f3[(n, 'baseline')]) for n in com)
    print(f"    on {len(com)} baseline-solved: median total ratio {rat:.3f}, median SCIP-excl/baseline SCIP {srat:.4f}")
    gi = idx(c3f, "full")
    for n in (10, 20, 40, 80):
        gs = [gi[(nm, 'gurobi')].get('mip_gap') for nm in names3 if grp(nm)[0] == n]
        print(f"    Gurobi C3 n={n} mip_gap {[round(g,3) if g is not None else None for g in gs]}")

    # ---- C4
    names4 = sorted({r["name"] for r in c4}, key=grp)
    b4 = idx(c4, "root")
    f4 = idx(c4, "full")
    print("  seeds 5-9 binding row (C4): root gap closed vs optimum, median per n")
    allmed = {}
    for m in ["baseline-extra", "frozen-wide", "rowdir-wide"]:
        per = defaultdict(list)
        al = []
        for nm in names4:
            g = gap_closed(root_bound(b4[(nm, m)]), root_bound(b4[(nm, "baseline")]), cs_c4[nm]["known_optimum"], "min")
            per[grp(nm)[0]].append(g)
            al.append(g)
        allmed[m] = statistics.median(al)
        print(f"    {m:16s}", {n: (round(statistics.median(v), 4), r2(statistics.median(v), 3)) for n, v in per.items()},
              f"all-20 median {statistics.median(al):.4f} min {min(al):.4f}")
    eqopt = sum(1 for nm in names4 if cs_c4[nm]["known_optimum"] - cs_c4[nm]["reference_bound_ii"] <= 1e-12)
    mx = max(cs_c4[nm]["known_optimum"] - cs_c4[nm]["reference_bound_ii"] for nm in names4)
    print(f"    bound (ii) equals optimum (float) on {eqopt}/20; max opt-(ii) {mx:.3e}")
    d80 = [cs_c4[nm]["reference_bound_ii"] - root_bound(b4[(nm, "rowdir-wide")]) for nm in names4 if grp(nm)[0] == 80]
    print(f"    n=80 rowdir-wide distance to bound (ii): {min(d80):.4f}-{max(d80):.4f}")
    reached = sum(1 for nm in names4 for m in ("frozen-wide", "rowdir-wide")
                  if root_bound(b4[(nm, m)]) >= cs_c4[nm]["reference_bound_ii"] - 1e-9)
    print(f"    root runs reaching bound (ii) (within 1e-9): {reached}")
    for m in ["baseline", "baseline-extra", "gurobi", "frozen-wide", "rowdir-wide"]:
        sv = [nm for nm in names4 if solved(f4[(nm, m)])]
        ts = [ttime(f4[(nm, m)]) for nm in sv]
        print(f"    solved {m:16s} {len(sv)}  times {min(ts):.2f}-{max(ts):.2f}  n80 solved "
              f"{sum(1 for nm in sv if grp(nm)[0]==80)}")
    for m in ["frozen-wide", "rowdir-wide"]:
        com = [nm for nm in names4 if solved(f4[(nm, 'baseline')]) and solved(f4[(nm, m)])]
        rat = statistics.median(ttime(f4[(n, m)]) / ttime(f4[(n, 'baseline')]) for n in com)
        print(f"    {m}: on {len(com)} baseline-solved (n<=20: {all(grp(n)[0]<=20 for n in com)}) median ratio {rat:.3f}")
        capped4 = sum(1 for nm in names4 for ph_ in ("root", "full")
                      if len(idx(c4, ph_)[(nm, m)].get("cuts") or []) == 16 * grp(nm)[0])
        print(f"    {m}: runs at 16n cap {capped4}/40")

    # ---- the 19/22/11 claim and 97%
    hdr("6. Headline: 40 fresh instances")
    tot = Counter()
    for m in ["baseline", "baseline-extra", "gurobi", "rowdir-wide"]:
        tot[m] = sum(solved(f3[(nm, m)]) for nm in names3) + sum(solved(f4[(nm, m)]) for nm in names4)
    print(f"    solved of 40: {dict(tot)}")
    allg = [gap_closed(root_bound(b3[(nm, 'rowdir-wide')]), root_bound(b3[(nm, 'baseline')]), cs_c3[nm]['known_optimum'], 'min') for nm in names3] + \
           [gap_closed(root_bound(b4[(nm, 'rowdir-wide')]), root_bound(b4[(nm, 'baseline')]), cs_c4[nm]['known_optimum'], 'min') for nm in names4]
    print(f"    rowdir-wide root gap closed on 40: min {min(allg):.4f}")
    mx = max(max(ttime(f3[(nm, 'rowdir-wide')]) for nm in names3), max(ttime(f4[(nm, 'rowdir-wide')]) for nm in names4))
    print(f"    rowdir-wide max solve time over 40: {mx:.1f} s")
    # summary 'at most two thirds' across all path families and comparators
    worst = []
    for lab, ix, m, nn in [("C2 extra", idx(c2, 'full'), 'baseline-extra', names), ("C2 novar", idx(c2, 'full'), 'baseline-novarlocks', names),
                           ("C2 gurobi", idx(c2, 'full'), 'gurobi', names), ("C3 base", f3, 'baseline', names3),
                           ("C3 extra", f3, 'baseline-extra', names3), ("C3 gurobi", f3, 'gurobi', names3),
                           ("C4 base", f4, 'baseline', names4), ("C4 extra", f4, 'baseline-extra', names4),
                           ("C4 gurobi", f4, 'gurobi', names4)]:
        worst.append((lab, sum(solved(ix[(n, m)]) for n in nn)))
    print(f"    comparator solved counts (of 20): {worst}")


# ---------------------------------------------------------------- incumbents and loads
def incumbents_and_loads():
    hdr("7. Primal checks, loads, time limits")
    parts = ["v3/runs/partA-full", "v3/runs/partA-root", "v3/runs/partB", "v3/runs/partC",
             "v3d/runs/partA-root-rowdir", "v3d/runs/partB-root-rowdir", "v3d/runs/partC-rowdir",
             "v4/runs/partB2", "v4/runs/partC2", "v4/runs/partC3", "v4/runs/partC4",
             "v4/runs/partD-root", "v4/runs/partD-full"]
    fails = []
    ninc = 0
    for p in parts:
        recs = load(p)
        loads = [r["load_start"][0] for r in recs if r.get("load_start")]
        tl = Counter(r.get("time_limit") for r in recs)
        for r in recs:
            pc = r.get("primal_check") or {}
            if pc.get("checked"):
                ninc += 1
                if not pc.get("passed"):
                    fails.append((p, r["name"], r["mode"], r["phase"], pc.get("relative_objective_discrepancy")))
        print(f"  {p:28s} 1-min load at start: min {min(loads):5.2f} median {statistics.median(loads):5.2f} "
              f"max {max(loads):5.2f}; time limits {dict(tl)}")
    print(f"  incumbents checked {ninc}; failures {fails}")


def main():
    replay_totals()
    minlplib_table()
    minlplib_root()
    funnel()
    path_family()
    incumbents_and_loads()


if __name__ == "__main__":
    main()
