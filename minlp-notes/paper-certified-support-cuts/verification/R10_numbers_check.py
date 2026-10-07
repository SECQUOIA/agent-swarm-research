#!/usr/bin/env python3
"""R10 (numbers lens): recompute the campaign numbers of the manuscript from
the compact extracts written by R10_numbers_extract.py (which read the raw
records.jsonl), from replay.json and from cases/*.json.

Standard library only; imports no producer code.

Usage: R10_numbers_check.py <extract dir> [section ...]
Sections: replay c5s c5a c5b load path minlplib funnel

Definitions (Section 8.1 of the manuscript):
  solved      status optimal or gaplimit, returncode 0, no worker_status,
              primal_check passed
  time        total_seconds + preparation_seconds (charged time)
  root bound  root_dual if finite, else dual for a run that ended at the root
  gap closed  (z_mode - z_base) / (z* - z_base) (sign-adjusted for max)
  SGM         exp(mean(log(t + 1))) - 1
  bound tie   |a - b| <= 1e-4 max(1, |a|, |b|)
"""
import glob
import gzip
import json
import math
import os
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.join(HERE, "..", "experiments")
EX = sys.argv[1]
SECTIONS = sys.argv[2:] or ["replay", "c5s", "c5a", "c5b", "load", "path", "minlplib", "funnel"]

PARTS = {
    "c3": ["v3/runs/partA-full", "v3/runs/partA-root", "v3/runs/partB", "v3/runs/partC"],
    "c3p": ["v3d/runs/partA-root-rowdir", "v3d/runs/partB-root-rowdir", "v3d/runs/partC-rowdir"],
    "c4": ["v4/runs/partB2", "v4/runs/partC2", "v4/runs/partC3", "v4/runs/partC4",
           "v4/runs/partD-root", "v4/runs/partD-full"],
    "c5": ["v5/runs/partS5", "v5/runs/partC5a", "v5/runs/partC5b"],
}
_cache = {}


def load(part):
    if part not in _cache:
        f = os.path.join(EX, part.replace("/", "_") + ".jsonl")
        opener = open
        if not os.path.exists(f):
            f += ".gz"
            opener = gzip.open
        with opener(f, "rt") as fh:
            _cache[part] = [json.loads(l) for l in fh]
    return _cache[part]


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
    return (r.get("status") in ("optimal", "gaplimit") and (r.get("returncode") or 0) == 0
            and not r.get("worker_status") and pc.get("passed") is True)


def ttime(r):
    return (r.get("total_seconds") or 0.0) + (r.get("preparation_seconds") or 0.0)


def cbs(r):
    return (r.get("separation") or {}).get("callback_seconds") or 0.0


def root_bound(r):
    if finite(r.get("root_dual")):
        return r["root_dual"]
    if finite(r.get("dual")) and (r.get("node_limit") == 1 or (r.get("nodes") or 0) <= 1):
        return r["dual"]
    return None


def sgm(xs):
    xs = list(xs)
    return math.exp(sum(math.log(x + 1.0) for x in xs) / len(xs)) - 1.0 if xs else float("nan")


def gap_closed(zm, zb, zs, sense="min"):
    s = 1.0 if sense == "min" else -1.0
    den = s * (zs - zb)
    if den <= 0 or zm is None:
        return None
    return s * (zm - zb) / den


def cmpb(a, b, sense="min", rtol=1e-4):
    tol = rtol * max(1.0, abs(a), abs(b))
    d = (a - b) if sense == "min" else (b - a)
    return 1 if d > tol else (-1 if d < -tol else 0)


def med(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


def hdr(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)


def utc(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")


# --------------------------------------------------------------------------- replay
def sec_replay():
    hdr("REPLAY: replay.json vs records, totals, distinct rows")
    grand = 0
    all_keys = set()
    keys_by_c = {}
    for c, parts in PARTS.items():
        tot = 0
        ck = set()
        for p in parts:
            recs = load(p)
            n_rec = sum(r["n_cuts"] for r in recs)
            per_run = {r["run_id"]: r["n_cuts"] for r in recs}
            rp_path = os.path.join(EXP, p, "replay.json")
            if os.path.exists(rp_path):
                rp = json.load(open(rp_path))
                tam = rp.get("tamper_rejections")
                tam_ok = None
                if isinstance(tam, dict):
                    flat = []

                    def walk(x):
                        if isinstance(x, dict):
                            for v in x.values():
                                walk(v)
                        elif isinstance(x, list):
                            for v in x:
                                walk(v)
                        else:
                            flat.append(x)
                    walk(tam)
                    tam_ok = all(v is True for v in flat if isinstance(v, bool))
                    n_tam = sum(1 for v in flat if isinstance(v, bool))
                else:
                    n_tam = 0
                run_mismatch = []
                run_fail = []
                for rr in rp.get("runs", []):
                    if rr.get("cuts") != per_run.get(rr["run_id"]) or rr.get("replayed_cuts") != rr.get("cuts"):
                        run_mismatch.append((rr["run_id"], rr.get("cuts"), rr.get("replayed_cuts"), per_run.get(rr["run_id"])))
                    if not rr.get("passed"):
                        run_fail.append(rr["run_id"])
                replay_ids = {rr["run_id"] for rr in rp.get("runs", [])}
                omitted = {o["run_id"] for o in rp.get("omitted_runs", [])}
                not_covered = [k for k in per_run if k not in replay_ids and k not in omitted]
                omitted_with_cuts = [o for o in rp.get("omitted_runs", []) if per_run.get(o["run_id"], 0)]
                print(f"  {p:30s} records {len(recs):4d} cuts(rec) {n_rec:6d} replay.cuts {rp['cuts']:6d} "
                      f"replayed {rp['replayed_cuts']:6d} passed {rp['passed']} missing_logs {rp.get('missing_cut_logs')} "
                      f"tamper_all_rejected {tam_ok} ({n_tam} flags) run_mismatch {len(run_mismatch)} run_fail {len(run_fail)} "
                      f"not_covered {len(not_covered)} omitted {len(omitted)} omitted_with_cuts {len(omitted_with_cuts)}")
                if run_mismatch[:3]:
                    print("     mismatches:", run_mismatch[:5])
            else:
                print(f"  {p:30s} records {len(recs):4d} cuts(rec) {n_rec:6d}  NO replay.json")
            tot += n_rec
            for r in recs:
                for cu in r["cuts"]:
                    ck.add(cu["k"])
            incomplete = [r["run_id"] for r in recs if r.get("cut_log_complete") is False]
            if incomplete:
                print(f"     runs with incomplete cut log: {len(incomplete)} {incomplete}")
        keys_by_c[c] = ck
        all_keys |= ck
        grand += tot
        print(f"  -> {c}: recorded cuts {tot}, distinct rows {len(ck)}")
    print(f"  GRAND TOTAL recorded cuts {grand}; distinct rows (model sha, binary64 coefs, rhs) {len(all_keys)}")
    c34 = keys_by_c["c3"] | keys_by_c["c3p"] | keys_by_c["c4"]
    print(f"  distinct c3-c4: {len(c34)}; distinct c5: {len(keys_by_c['c5'])}; c5 not in c3-4: {len(keys_by_c['c5'] - c34)}")
    # sources of duplication in campaign 5
    for p in ["v5/runs/partS5", "v5/runs/partC5b"]:
        recs = load(p)
        by = defaultdict(dict)
        for r in recs:
            if r["n_cuts"]:
                by[(r["name"], r["mode"])][r["phase"]] = [c["k"] for c in r["cuts"]]
        same = diff = 0
        for k, v in by.items():
            if "root" in v and "full" in v:
                if v["root"] == v["full"]:
                    same += 1
                else:
                    diff += 1
        keys = set()
        for r in recs:
            keys |= {c["k"] for c in r["cuts"]}
        print(f"  {p}: root/full pairs identical {same}, different {diff}; distinct rows {len(keys)} of {sum(r['n_cuts'] for r in recs)}")
        if p.endswith("C5b"):
            idx = {(r["name"], r["mode"]): r for r in recs}
            ident = 0
            tot = 0
            for (nm, md), r in idx.items():
                if md.endswith("cap32"):
                    o = idx.get((nm, md.replace("cap32", "cap64")))
                    tot += 1
                    if o and [c["k"] for c in o["cuts"]] == [c["k"] for c in r["cuts"]]:
                        ident += 1
            print(f"     cap32 vs cap64 identical cut lists: {ident} of {tot}")
            for fam in ("frozen", "rowdir"):
                ks = set()
                for r in recs:
                    if r["mode"].startswith(fam):
                        ks |= {c["k"] for c in r["cuts"]}
                print(f"     distinct rows {fam}: {len(ks)}")
    # rerun cuts
    rr = load("v5/runs/partS5-rerun-spike")
    print(f"  rerun-spike records {len(rr)}, cuts {sum(r['n_cuts'] for r in rr)}, replay.json exists: "
          f"{os.path.exists(os.path.join(EXP, 'v5/runs/partS5-rerun-spike/replay.json'))}")
    # rounding stats by family and campaign
    print("  Rounding (any coefficient changed) and max |E|:")
    fam_parts = {
        "MINLPLib c3-4": PARTS["c3"][:3] + PARTS["c3p"][:2] + ["v4/runs/partB2", "v4/runs/partD-root", "v4/runs/partD-full"],
        "path c3-4": ["v3/runs/partC", "v3d/runs/partC-rowdir", "v4/runs/partC2", "v4/runs/partC3", "v4/runs/partC4"],
        "path c5 (5C-b)": ["v5/runs/partC5b"],
        "path c3-5": ["v3/runs/partC", "v3d/runs/partC-rowdir", "v4/runs/partC2", "v4/runs/partC3", "v4/runs/partC4", "v5/runs/partC5b"],
        "star c5 (5S)": ["v5/runs/partS5"],
    }
    for fam, parts in fam_parts.items():
        n = rnd = 0
        emax = 0.0
        for p in parts:
            for r in load(p):
                for c in r["cuts"]:
                    n += 1
                    rnd += c["r"]
                    if c["E"] is not None:
                        emax = max(emax, abs(c["E"]))
        print(f"    {fam:18s} rows {n:7d} rounded {rnd:7d} ({100*rnd/max(n,1):.1f}%) max|E| {emax:.3g}")


# --------------------------------------------------------------------------- star family
def star_key(name):
    # constrained_star_k16_n10_s0
    parts = name.split("_")
    k = int(parts[2][1:]); n = int(parts[3][1:]); s = int(parts[4][1:])
    return k, n, s


def sec_c5s():
    hdr("PART 5S: star family")
    recs = load("v5/runs/partS5")
    cs = cases("v5/runs/partS5")
    opt = {nm: d["known_optimum"] for nm, d in cs.items()}
    idx = {(r["name"], r["phase"], r["mode"]): r for r in recs}
    modes = ["baseline", "baseline-novarlocks", "baseline-extra", "gurobi", "rowdir-star4", "agg-star4", "agg-star"]
    st = Counter(r["status"] for r in recs)
    print("  statuses:", dict(st), "records", len(recs))
    pt = [r for r in recs if r["status"] == "process_timeout" or r.get("worker_status")]
    print("  process timeouts / worker status:", [(r["run_id"], r["status"], r.get("worker_status")) for r in pt])
    print("  Root bound / optimum (median per k) and solved (full) per k:")
    for m in modes:
        row = []
        for k in (4, 8, 16):
            vals = []
            for nm in opt:
                kk, n, s = star_key(nm)
                if kk != k:
                    continue
                r = idx.get((nm, "root", m))
                if r is None:
                    continue
                z = root_bound(r)
                vals.append(z / opt[nm] if z is not None else None)
            row.append(med(vals))
        sol = []
        for k in (4, 8, 16):
            c = 0
            for nm in opt:
                if star_key(nm)[0] != k:
                    continue
                r = idx.get((nm, "full", m))
                if r is not None and solved(r):
                    c += 1
            sol.append(c)
        print(f"    {m:20s} root/opt " + " ".join(f"{x:.4f}" if x is not None else "  -   " for x in row)
              + f"   solved {sol} total {sum(sol)}")
    # agg-star root within 1e-6 relative
    worst = 0.0
    for nm in opt:
        r = idx[(nm, "root", "agg-star")]
        z = root_bound(r)
        worst = max(worst, abs(z - opt[nm]) / max(1.0, abs(opt[nm])))
    print(f"  agg-star root: max |z - z*| / max(1,|z*|) = {worst:.3g}")
    # per-instance difference of <=4-var blocks over SCIP
    for m in ("rowdir-star4", "agg-star4"):
        diffs = []
        for nm in opt:
            zb = root_bound(idx[(nm, "root", "baseline")])
            zm = root_bound(idx[(nm, "root", m)])
            diffs.append((zm - zb) / opt[nm] * 100)
        print(f"  {m}: per-instance root bound minus SCIP's, in % of optimum: min {min(diffs):.2f} max {max(diffs):.2f} "
              f"median {med(diffs):.2f}; >2 points on {sum(d > 2 for d in diffs)} instances")
    for m in ("rowdir-star4", "agg-star4"):
        md = []
        for k in (4, 8, 16):
            a = med([root_bound(idx[(nm, 'root', m)]) / opt[nm] for nm in opt if star_key(nm)[0] == k])
            b = med([root_bound(idx[(nm, 'root', 'baseline')]) / opt[nm] for nm in opt if star_key(nm)[0] == k])
            md.append(round(100 * (a - b), 2))
        print(f"  {m}: difference of medians to SCIP per k (points): {md}")
    # star oracle calls in root runs
    star_secs = []
    star_dims = Counter()
    star_cert = 0
    poly_by_mode = {}
    for m in ("rowdir-star4", "agg-star4", "agg-star"):
        ps = []
        for nm in opt:
            r = idx[(nm, "root", m)]
            for d, meth, cert, sec in r["cert_calls"]:
                if meth == "quadratic_star":
                    star_secs.append(sec); star_dims[d] += 1; star_cert += bool(cert)
                elif meth == "quadratic_polytope":
                    ps.append(sec)
        poly_by_mode[m] = (len(ps), med(ps))
    print(f"  star oracle (root runs): calls {len(star_secs)}, certified {star_cert}, dims {dict(star_dims)}, "
          f"median {med(star_secs)*1000:.2f} ms, max {max(star_secs):.3f} s")
    print(f"  polytope enumeration (root runs) per mode: " + ", ".join(f"{m}: {n} calls, median {x*1000:.1f} ms" for m, (n, x) in poly_by_mode.items()))
    # full-run star oracle too
    fs = [sec for nm in opt for d, meth, cert, sec in idx[(nm, "full", "agg-star")]["cert_calls"] if meth == "quadratic_star"]
    print(f"  star oracle (full runs agg-star): calls {len(fs)}, median {med(fs)*1000:.2f} ms, max {max(fs):.3f}")
    # star cuts
    for ph in ("root", "full"):
        cm = Counter()
        for nm in opt:
            r = idx.get((nm, ph, "agg-star"))
            for c in r["cuts"]:
                cm[(c["m"], c["d"])] += 1
        print(f"  agg-star {ph} cuts by (method, dim): {dict(cm)}")
    # unsolved agg-star full runs: bound optimal? incumbent gap
    print("  agg-star full runs not solved:")
    for nm in sorted(opt, key=star_key):
        r = idx[(nm, "full", "agg-star")]
        if not solved(r):
            d = r.get("dual"); p = r.get("primal")
            print(f"    {nm:30s} status {r['status']:16s} dual/opt-1 {((d/opt[nm])-1) if finite(d) else None} "
                  f"primal/opt-1 {((p/opt[nm])-1) if finite(p) else None} cb {cbs(r):.1f} budget_exh "
                  f"{(r.get('separation') or {}).get('budget_exhausted')}")
    print("  largest instances (k=16, n=20): incumbents relative to optimum")
    for m in ("agg-star", "gurobi", "baseline"):
        vals = []
        bvals = []
        for nm in opt:
            k, n, s = star_key(nm)
            if k == 16 and n == 20:
                r = idx[(nm, "full", m)]
                vals.append(r["primal"] / opt[nm] - 1 if finite(r.get("primal")) else None)
                bvals.append(1 - r["dual"] / opt[nm] if finite(r.get("dual")) else None)
        print(f"    {m:10s} primal/opt-1: {[round(v,5) if v is not None else None for v in vals]}  1-dual/opt: {[round(v,5) if v is not None else None for v in bvals]}")
    print("  gurobi: incumbent rel. to optimum over all full runs with primal; bound below optimum")
    gp = []; gb = []
    for nm in opt:
        r = idx[(nm, "full", "gurobi")]
        if finite(r.get("primal")):
            gp.append(abs(r["primal"] / opt[nm] - 1))
        if finite(r.get("dual")):
            gb.append(1 - r["dual"] / opt[nm])
    print(f"    max |primal/opt - 1| = {max(gp):.3g}; max (1 - dual/opt) = {max(gb):.4f}")
    # budget exhaustion of separator in full runs
    for m in ("rowdir-star4", "agg-star4", "agg-star"):
        be = [(r.get("separation") or {}).get("budget_exhausted") for nm in opt for r in [idx[(nm, "full", m)]] if r.get("separation")]
        cbl = [cbs(idx[(nm, 'full', m)]) for nm in opt if idx[(nm, 'full', m)].get('separation')]
        print(f"  {m} full: budget_exhausted {sum(bool(x) for x in be)}/{len(be)}, callback s min {min(cbl):.1f} max {max(cbl):.1f}")
    # process timeouts: time window and load
    pts = sorted([r for r in recs if r["status"] == "process_timeout"], key=lambda r: r["started_utc"])
    if pts:
        print("  process_timeout runs:")
        for r in pts:
            print(f"    {r['run_id']:58s} {r['started_utc']} -> {r['ended_utc']} load_start {r['load_start']} load_end {r['load_end']} outer {r.get('outer_wall_seconds')}")
    # rerun
    rr = load("v5/runs/partS5-rerun-spike")
    print("  rerun-spike:")
    for r in rr:
        print(f"    {r['run_id']:58s} status {r['status']:10s} solved {solved(r)} time {ttime(r):.1f} cuts {r['n_cuts']} load {r['load_start'][0]:.1f}")
    # solved counts with rerun substitutions
    sub = {(r["name"], r["mode"]): r for r in rr}
    for m in modes:
        c = 0
        for nm in opt:
            r = sub.get((nm, m)) or idx[(nm, "full", m)]
            c += solved(r)
        print(f"    with reruns, {m:20s} solved {c}")


# --------------------------------------------------------------------------- 5C-a / 5C-b
def path_name(nm):
    p = nm.split("_")
    n = int([x for x in p if x.startswith("n") and x[1:].isdigit()][0][1:])
    s = int([x for x in p if x.startswith("s") and x[1:].isdigit()][0][1:])
    return n, s


def sec_c5a():
    hdr("PART 5C-a: SCIP-nolocks on 4C3 and 4C4 instances")
    a = load("v5/runs/partC5a")
    c3 = load("v4/runs/partC3")
    c4 = load("v4/runs/partC4")
    for fam, ref, tag in (("interleaved_path_n", c3, "4C3"), ("interleaved_path_coupled_n", c4, "4C4")):
        base = {r["name"]: r for r in ref if r["phase"] == "root" and r["mode"] == "baseline"}
        opt = {r["name"]: r["reference_value"] for r in ref if r.get("reference_value") is not None}
        rows = [r for r in a if r["name"].startswith(fam) and r["phase"] == "root"]
        byn = defaultdict(list)
        allv = []
        for r in rows:
            n, s = path_name(r["name"])
            g = gap_closed(root_bound(r), root_bound(base[r["name"]]), opt[r["name"]])
            byn[n].append(g); allv.append(g)
        print(f"  {tag}: root closure medians per n: " + ", ".join(f"n={n}: {med(v):.4f}" for n, v in sorted(byn.items()))
              + f"; range {min(allv):.4f}-{max(allv):.4f}")
        full = [r for r in a if r["name"].startswith(fam) and r["phase"] == "full"]
        sol = [r for r in full if solved(r)]
        times = [ttime(r) for r in sol]
        print(f"  {tag}: full solved {len(sol)}/{len(full)}; time range {min(times):.3g}-{max(times):.4g}; SGM over solved {sgm(times):.3f}")
        # compare with cut modes of 4C4
        if tag == "4C4":
            for m in ("frozen-wide", "rowdir-wide"):
                tm = [ttime(r) for r in ref if r["phase"] == "full" and r["mode"] == m and solved(r)]
                print(f"    4C4 {m}: solved {len(tm)}, SGM {sgm(tm):.2f}, range {min(tm):.3g}-{max(tm):.4g}")
            tb = [ttime(r) for r in ref if r["phase"] == "full" and r["mode"] == "baseline" and solved(r)]
            print(f"    4C4 SCIP: solved {len(tb)}")
            # how many runs at the root node
        # load
        loads = [x for r in a for x in (r["load_start"][0], r["load_end"][0])]
        print(f"  5C-a load (1-min, start/end) min {min(loads):.1f} max {max(loads):.1f}")


def sec_c5b():
    hdr("PART 5C-b: larger cut caps on 4C4")
    b = load("v5/runs/partC5b")
    c4 = load("v4/runs/partC4")
    cs = cases("v5/runs/partC5b")
    bii = {nm: d["reference_bound_ii"] for nm, d in cs.items()}
    opt = {nm: d["known_optimum"] for nm, d in cs.items()}
    base = {r["name"]: r for r in c4 if r["phase"] == "root" and r["mode"] == "baseline"}
    # check that case optimum equals 4C4 reference value
    for nm in opt:
        rv = [r["reference_value"] for r in c4 if r["name"] == nm and r.get("reference_value") is not None]
        if rv and abs(rv[0] - opt[nm]) > 1e-15:
            print("   optimum mismatch", nm, rv[0], opt[nm])
    opt_minus = {nm: opt[nm] - bii[nm] for nm in opt}
    print(f"  block closure = optimum (|diff|<1e-12) on {sum(abs(v) < 1e-12 for v in opt_minus.values())} of {len(opt_minus)}; "
          f"max opt - closure {max(opt_minus.values()):.4g}")
    for m in ("frozen-cap32", "frozen-cap64", "rowdir-cap32", "rowdir-cap64"):
        rows = [r for r in b if r["mode"] == m]
        byn = defaultdict(list)
        dist = []
        calls = []
        cpb = []
        be = []
        cuts = []
        caps = []
        for r in rows:
            n, s = path_name(r["name"])
            z = root_bound(r)
            byn[n].append(gap_closed(z, root_bound(base[r["name"]]), opt[r["name"]]))
            dist.append(bii[r["name"]] - z)
            sp = r.get("separation") or {}
            calls.append(sp.get("calls"))
            cpb.append(r["n_cuts"] / n)
            be.append(sp.get("budget_exhausted"))
            cap = (32 if "32" in m else 64) * n
            caps.append(r["n_cuts"] >= cap)
        print(f"  {m:13s} closure medians per n: " + " ".join(f"{med(v):.4f}" for n, v in sorted(byn.items()))
              + f" | closure-root min {min(dist):.3g} max {max(dist):.3g} | callbacks {min(calls)}-{max(calls)} | cuts/block "
              f"{min(cpb):.1f}-{max(cpb):.1f} | budget_exhausted {sum(bool(x) for x in be)} | at cap {sum(caps)} | statuses {Counter(r['status'] for r in rows)}")
    # cap32 vs cap64 root bounds identical?
    idx = {(r["name"], r["mode"]): r for r in b}
    same_b = same_c = 0
    for (nm, m), r in idx.items():
        if m.endswith("cap32"):
            o = idx[(nm, m.replace("32", "64"))]
            same_b += root_bound(r) == root_bound(o)
            same_c += r["n_cuts"] == o["n_cuts"]
    print(f"  cap32 vs cap64: identical root bounds {same_b}/40, identical cut counts {same_c}/40")
    # 4C4 16n runs: distance to closure, at cap
    for m in ("frozen-wide", "rowdir-wide"):
        rows = [r for r in c4 if r["mode"] == m and r["phase"] == "root"]
        d80 = [bii[r["name"]] - root_bound(r) for r in rows if path_name(r["name"])[0] == 80]
        atcap = sum(r["n_cuts"] >= 16 * path_name(r["name"])[0] for r in rows)
        dall = [bii[r["name"]] - root_bound(r) for r in rows]
        print(f"  4C4 {m} root: at cap 16n {atcap}/{len(rows)}; closure-root n=80 {min(d80):.4f}-{max(d80):.4f}; all {min(dall):.3g}-{max(dall):.3g}")
    loads = [x for r in b for x in (r["load_start"][0], r["load_end"][0])]
    print(f"  5C-b load (1-min, start/end) min {min(loads):.1f} max {max(loads):.1f}")
    # funnel row for rowdir-cap64
    for m in ("rowdir-cap64", "frozen-cap64"):
        rows = [r for r in b if r["mode"] == m]
        S = Counter()
        for r in rows:
            sp = r.get("separation") or {}
            for k in ("certification_calls", "certification_failures", "row_binding_rejections", "cuts", "callback_seconds",
                      "discovery_seconds", "candidate_seconds", "certification_seconds"):
                S[k] += sp.get(k) or 0
        print(f"  funnel {m}: {dict((k, round(v, 1)) for k, v in S.items())}")


# --------------------------------------------------------------------------- load
def sec_load():
    hdr("LOAD: one-minute load average at run start/end per campaign/part")

    def pct(v, q):
        v = sorted(v)
        i = (len(v) - 1) * q
        lo = math.floor(i); hi = math.ceil(i)
        return v[lo] + (v[hi] - v[lo]) * (i - lo)
    groups = {
        "c3 prospective": PARTS["c3"], "c3P": PARTS["c3p"], "c4": PARTS["c4"],
        "c5": PARTS["c5"], "5S": ["v5/runs/partS5"], "5C-a": ["v5/runs/partC5a"], "5C-b": ["v5/runs/partC5b"],
        "4C4": ["v4/runs/partC4"],
    }
    for g, parts in groups.items():
        v = []
        for p in parts:
            for r in load(p):
                for key in ("load_start", "load_end"):
                    if r.get(key):
                        v.append(r[key][0])
        print(f"  {g:16s} n {len(v):4d} min {min(v):6.1f} p5 {pct(v,.05):6.1f} p95 {pct(v,.95):6.1f} max {max(v):6.1f}")
    # 5S: excluding the spike window
    recs = load("v5/runs/partS5")
    hi = sorted([(r["started_utc"], r["load_start"][0], r["ended_utc"], r["load_end"][0], r["run_id"]) for r in recs
                 if max(r["load_start"][0], r["load_end"][0]) > 25], key=lambda x: x[0])
    print(f"  5S runs with a start/end load above 25: {len(hi)}")
    for h in hi[:40]:
        print("    ", h)
    lo = [x for r in recs for x in (r["load_start"][0], r["load_end"][0]) if x <= 25]
    print(f"  5S loads <= 25: min {min(lo):.1f} max {max(lo):.1f}")
    # sessions log
    try:
        with open(os.path.join(EXP, "v5/runs/partS5/sessions.jsonl")) as fh:
            for l in fh:
                d = json.loads(l)
                print("   session", d.get("event"), d.get("utc"), d.get("load"))
    except Exception as e:
        print("   sessions:", e)




# --------------------------------------------------------------------------- path family
def sec_path():
    hdr("PATH FAMILY: Table 5 and the text of Section 8.5")
    P3 = load("v3/runs/partC"); PP = load("v3d/runs/partC-rowdir"); C2 = load("v4/runs/partC2")
    C3 = load("v4/runs/partC3"); C4 = load("v4/runs/partC4"); A5 = load("v5/runs/partC5a"); B5 = load("v5/runs/partC5b")

    def ix(recs):
        return {(r["name"], r["phase"], r["mode"]): r for r in recs}
    i3, iP, i2, iC3, iC4, iA, iB = map(ix, (P3, PP, C2, C3, C4, A5, B5))
    names03 = sorted({r["name"] for r in P3}, key=path_name)
    names59 = sorted({r["name"] for r in C3}, key=path_name)
    names4 = sorted({r["name"] for r in C4}, key=path_name)
    opt = {}
    for recs in (P3, C3, C4):
        for r in recs:
            if r.get("reference_value") is not None:
                opt[r["name"]] = r["reference_value"]
    cs3 = cases("v3/runs/partC"); cs4 = cases("v4/runs/partC3")
    for d in list(cs3.values()) + list(cs4.values()):
        if abs(d["known_optimum"] - opt[d["name"]]) > 1e-12:
            print("   optimum mismatch", d["name"])

    def table_rows(names, rows):
        for label, idx, mode, basei in rows:
            byn = defaultdict(list)
            for nm in names:
                n, s = path_name(nm)
                if mode == "glued":
                    zb = root_bound(basei[(nm, "root", "baseline")])
                    byn[n].append(gap_closed(0.0, zb, opt[nm]))
                    continue
                if mode == "closure":
                    zb = root_bound(basei[(nm, "root", "baseline")])
                    bii = cases("v5/runs/partC5b")[nm]["reference_bound_ii"]
                    byn[n].append(gap_closed(bii, zb, opt[nm]))
                    continue
                r = idx.get((nm, "root", mode))
                if r is None:
                    continue
                zb = root_bound(basei[(nm, "root", "baseline")])
                byn[n].append(gap_closed(root_bound(r), zb, opt[nm]))
            sol = None
            if mode not in ("glued", "closure"):
                full = [idx.get((nm, "full", mode)) for nm in names]
                if any(f is not None for f in full):
                    sol = sum(1 for f in full if f is not None and solved(f))
            print(f"    {label:34s} " + " ".join(f"{med(byn[n]):.4f}" if byn.get(n) else "  -   " for n in (10, 20, 40, 80))
                  + f"  solved {sol}")
    print("  seeds 0-4:")
    table_rows(names03, [
        ("3C SCIP", i3, "baseline", i3), ("4C2 SCIP-nolocks", i2, "baseline-novarlocks", i3),
        ("4C2 SCIP-extra", i2, "baseline-extra", i3), ("4C2 Gurobi", i2, "gurobi", i3),
        ("glued pair hulls", None, "glued", i3), ("3C remainder base", i3, "all-diag-mech", i3),
        ("4C2 remainder wide", i2, "frozen-wide", i3), ("3P whole row base", iP, "all-diag-mech", i3),
        ("3P whole row wide", iP, "all-diag-mech-wide", i3)])
    print("  seeds 5-9:")
    table_rows(names59, [
        ("4C3 SCIP", iC3, "baseline", iC3), ("5C-a SCIP-nolocks", iA, "baseline-novarlocks", iC3),
        ("4C3 SCIP-extra", iC3, "baseline-extra", iC3), ("4C3 Gurobi", iC3, "gurobi", iC3),
        ("glued pair hulls", None, "glued", iC3), ("4C3 remainder base", iC3, "all-diag-mech", iC3),
        ("4C3 whole row wide", iC3, "rowdir-wide", iC3)])
    print("  binding row:")
    table_rows(names4, [
        ("4C4 SCIP", iC4, "baseline", iC4), ("5C-a SCIP-nolocks", iA, "baseline-novarlocks", iC4),
        ("4C4 SCIP-extra", iC4, "baseline-extra", iC4), ("4C4 Gurobi", iC4, "gurobi", iC4),
        ("block closure", None, "closure", iC4), ("4C4 remainder wide", iC4, "frozen-wide", iC4),
        ("4C4 whole row wide", iC4, "rowdir-wide", iC4), ("5C-b remainder cap64", iB, "frozen-cap64", iC4),
        ("5C-b whole row cap64", iB, "rowdir-cap64", iC4)])
    # overall medians at the root for 4C4 cut modes
    for m in ("frozen-wide", "rowdir-wide"):
        v = [gap_closed(root_bound(iC4[(nm, "root", m)]), root_bound(iC4[(nm, "root", "baseline")]), opt[nm]) for nm in names4]
        print(f"  4C4 {m} root closure: median {med(v):.4f}, range {min(v):.4f}-{max(v):.4f}")
    # SCIP's root bound per copy in 3C
    pc = [root_bound(i3[(nm, "root", "baseline")]) / path_name(nm)[0] for nm in names03]
    print(f"  3C SCIP root bound per copy: {min(pc):.4f} to {max(pc):.4f}")
    # nolocks below 0 in 3C (4C2 runs)
    nb = [root_bound(i2[(nm, "root", "baseline-novarlocks")]) for nm in names03]
    print(f"  4C2 SCIP-nolocks root bound: max {max(nb):.3g}, min {min(nb):.3g}; all < 0: {all(x < 0 for x in nb)}")
    nb5 = [root_bound(iA[(nm, "root", "baseline-novarlocks")]) for nm in names59]
    print(f"  5C-a SCIP-nolocks root bound on 4C3: max {max(nb5):.3g}; all < 0: {all(x < 0 for x in nb5)}")
    # minor cuts productive
    def prod(r, sep):
        return ((r.get("native") or {}).get(sep) or {}).get("Applied") or 0
    for lab, recs, mode in (("4C2 nolocks", C2, "baseline-novarlocks"), ("5C-a nolocks", A5, "baseline-novarlocks"),
                            ("c4 default C3", C3, "baseline"), ("c4 default C4", C4, "baseline")):
        rs = [r for r in recs if r["mode"] == mode]
        print(f"  minor cuts applied>0 in {lab}: {sum(prod(r, 'minor') > 0 for r in rs)}/{len(rs)}")
    for lab, recs in (("4C2", C2), ("4C3", C3), ("4C4", C4)):
        rs = [r for r in recs if r["mode"] == "baseline-extra"]
        print(f"  {lab} SCIP-extra: interminor applied>0 {sum(prod(r, 'interminor') > 0 for r in rs)}/{len(rs)}, "
              f"eccuts applied>0 {sum(prod(r, 'eccuts') > 0 for r in rs)}, quadratic nlhdlr cuts>0 "
              f"{sum(((r.get('native') or {}).get('nlhdlr_quadratic') or {}).get('Cuts', 0) not in (0, None, '-') for r in rs)}")
    # Gurobi
    for lab, recs, names in (("4C2", C2, names03), ("4C3", C3, names59), ("4C4", C4, names4)):
        g = {r["name"]: r for r in recs if r["mode"] == "gurobi"}
        solved_g = [nm for nm in names if solved(g[nm])]
        gaps = {}
        for nm in names:
            r = g[nm]
            if finite(r.get("primal")) and finite(r.get("dual")) and not solved(r):
                gaps[nm] = abs(r["primal"] - r["dual"]) / abs(r["primal"])
        g4080 = [v for nm, v in gaps.items() if path_name(nm)[0] >= 40]
        print(f"  Gurobi {lab}: solved {[(path_name(n)) for n in solved_g]}; gap n>=40 {min(g4080)*100:.1f}-{max(g4080)*100:.1f}%; "
              f"unsolved gaps all {[round(100*v,1) for v in gaps.values()]}")
    # 3C separator vs SCIP
    v = [gap_closed(root_bound(i3[(nm, "root", "all-diag-mech")]), root_bound(i3[(nm, "root", "baseline")]), opt[nm]) for nm in names03]
    print(f"  3C remainder base: improved root on {sum(x > 0 for x in v)}/20; medians per n above")
    sb = [nm for nm in names03 if solved(i3[(nm, "full", "baseline")])]
    sm = [nm for nm in names03 if solved(i3[(nm, "full", "all-diag-mech")])]
    print(f"  3C solved baseline {len(sb)}, mech {len(sm)}, same set {set(sb) == set(sm)}")
    common = [nm for nm in sb if nm in sm]
    tb = [ttime(i3[(nm, 'full', 'baseline')]) for nm in common]; tm = [ttime(i3[(nm, 'full', 'all-diag-mech')]) for nm in common]
    nodes_b = sum(i3[(nm, 'full', 'baseline')]['nodes'] for nm in common); nodes_m = sum(i3[(nm, 'full', 'all-diag-mech')]['nodes'] for nm in common)
    print(f"  3C SGM baseline {sgm(tb):.2f} vs mech {sgm(tm):.2f}; nodes {nodes_b} vs {nodes_m}; fewer nodes on "
          f"{sum(i3[(nm,'full','all-diag-mech')]['nodes'] < i3[(nm,'full','baseline')]['nodes'] for nm in common)}/{len(common)}")
    # 3P
    for m in ("all-diag-mech", "all-diag-mech-wide"):
        s = [nm for nm in names03 if solved(iP[(nm, "full", m)])]
        atroot = [nm for nm in s if (iP[(nm, "full", m)].get("nodes") or 0) <= 1]
        print(f"  3P {m}: solved {len(s)}, at root node {len(atroot)}")
    # 4C2 frozen-wide above pair-hull level
    above = [path_name(nm) for nm in names03 if root_bound(i2[(nm, "root", "frozen-wide")]) > 0]
    print(f"  4C2 frozen-wide root bound > 0 on {len(above)}: {above}")
    # caps reached
    for lab, idx, m, capf in (("3C mech", i3, "all-diag-mech", 4), ("3P base", iP, "all-diag-mech", 4),
                              ("3P wide", iP, "all-diag-mech-wide", 16), ("4C2 wide", i2, "frozen-wide", 16),
                              ("4C3 rowdir-wide", iC3, "rowdir-wide", 16), ("4C3 mech", iC3, "all-diag-mech", 4)):
        names = names03 if lab[:2] in ("3C", "3P", "4C2"[:2]) and "4C3" not in lab else names59
        if lab.startswith("4C2"):
            names = names03
        rs = [idx[(nm, "root", m)] for nm in names]
        print(f"  {lab}: at cut cap {sum(r['n_cuts'] >= capf * path_name(r['name'])[0] for r in rs)}/{len(rs)}")
    # 4C3 rowdir-wide details
    rw = [iC3[(nm, "root", "rowdir-wide")] for nm in names59]
    print(f"  4C3 rowdir-wide root: max |z - z*| {max(abs(root_bound(r) - opt[r['name']]) for r in rw):.3g}")
    fw = [iC3[(nm, "full", "rowdir-wide")] for nm in names59]
    print(f"  4C3 rowdir-wide full: solved {sum(solved(r) for r in fw)}, time {min(ttime(r) for r in fw):.2f}-{max(ttime(r) for r in fw):.2f}, "
          f"nodes median {med([r['nodes'] for r in fw])}, max {max(r['nodes'] for r in fw)}")
    for m in ("baseline", "baseline-extra", "all-diag-mech", "gurobi"):
        print(f"    4C3 {m} solved {sum(solved(iC3[(nm, 'full', m)]) for nm in names59)}")
    sb = [nm for nm in names59 if solved(iC3[(nm, "full", "baseline")])]
    rat = [(path_name(nm), ttime(iC3[(nm, 'full', 'rowdir-wide')]) / ttime(iC3[(nm, 'full', 'baseline')])) for nm in sb]
    print("  4C3 ratio rowdir-wide/SCIP on SCIP-solved:", [(n, round(x, 3)) for n, x in rat])
    own = [(iC3[(nm, 'full', 'rowdir-wide')]['scip_solve_seconds'] - cbs(iC3[(nm, 'full', 'rowdir-wide')])) /
           iC3[(nm, 'full', 'baseline')]['scip_solve_seconds'] for nm in sb]
    print(f"  4C3 SCIP own time (excl. callback) / baseline SCIP time on SCIP-solved: median {med(own):.3f}; values {[round(x,3) for x in own]}")
    tot = sum(ttime(r) for r in fw); cb = sum(cbs(r) for r in fw)
    print(f"  4C3 rowdir-wide full: callback share of charged time {cb/tot:.3f}")
    v = [gap_closed(root_bound(iC3[(nm, "root", "all-diag-mech")]), root_bound(iC3[(nm, "root", "baseline")]), opt[nm]) for nm in names59]
    # 4C4
    for m in ("frozen-wide", "rowdir-wide"):
        fw = [iC4[(nm, "full", m)] for nm in names4]
        print(f"  4C4 {m}: solved {sum(solved(r) for r in fw)}, time {min(ttime(r) for r in fw):.2f}-{max(ttime(r) for r in fw):.2f}")
    for m in ("baseline", "baseline-extra", "gurobi"):
        s = [nm for nm in names4 if solved(iC4[(nm, 'full', m)])]
        print(f"    4C4 {m} solved {len(s)}; n of solved {sorted(set(path_name(x)[0] for x in s))}")
    sb = [nm for nm in names4 if solved(iC4[(nm, "full", "baseline")])]
    for m in ("frozen-wide", "rowdir-wide"):
        rat = [ttime(iC4[(nm, 'full', m)]) / ttime(iC4[(nm, 'full', 'baseline')]) for nm in sb]
        print(f"  4C4 {m}/SCIP median ratio on SCIP-solved ({len(sb)}): {med(rat):.3f}")
    # direction classes
    for m in ("frozen-wide", "rowdir-wide"):
        cls = Counter(); ynz = 0; neg = 0; tot = 0
        for nm in names4:
            for c in iC4[(nm, "root", m)]["cuts"]:
                cls[c["c"]] += 1
        n = sum(cls.values())
        print(f"  4C4 {m} root cut classes: {dict(cls)}; 'other' (LP) share {cls['other']/n:.4f}")
    # whole-row cuts alone: sum min d_i = C3 optimum of same triples vs SCIP root bound of C4
    below = 0
    for nm in names4:
        c3n = nm.replace("_coupled", "")
        if opt[c3n] < root_bound(iC4[(nm, "root", "baseline")]):
            below += 1
    print(f"  sum_i min d_i below SCIP root bound on {below} of 20")
    ref = json.load(open(os.path.join(EXP, "v4/c4-references.json")))
    rt = [i["gurobi"]["runtime_seconds"] for i in ref["instances"]]
    print(f"  Gurobi convex reformulation runtime < 1 s on {sum(x < 1 for x in rt)} of {len(rt)}; max {max(rt):.2f}")




# --------------------------------------------------------------------------- MINLPLib
def best_known(part):
    out = {}
    for nm, d in cases(part).items():
        v = d.get("known_optimum")
        if v is None:
            v = d.get("best_known") or d.get("reference_value") or d.get("primal_bound")
        out[nm] = v
    return out


def sec_minlplib():
    hdr("MINLPLIB: Table 3 and Section 8.3")
    A = load("v3/runs/partA-full"); AR = load("v3/runs/partA-root"); B = load("v3/runs/partB")
    AP = load("v3d/runs/partA-root-rowdir"); BP = load("v3d/runs/partB-root-rowdir")
    B2 = load("v4/runs/partB2"); DF = load("v4/runs/partD-full"); DR = load("v4/runs/partD-root")

    def table(recs, modes, label, ph="full"):
        idx = {(r["name"], r["seed"], r["mode"]): r for r in recs if r["phase"] == ph}
        keys = sorted({(r["name"], r["seed"]) for r in recs if r["phase"] == ph})
        common = [k for k in keys if all(idx.get((k[0], k[1], m)) is not None and solved(idx[(k[0], k[1], m)]) for m in modes)]
        for m in modes:
            rs = [idx[(k[0], k[1], m)] for k in keys if (k[0], k[1], m) in idx]
            nsol = sum(solved(r) for r in rs)
            cuts = sum(r["n_cuts"] for r in rs); runs_c = sum(r["n_cuts"] > 0 for r in rs)
            models_c = len({r["name"] for r in rs if r["n_cuts"] > 0})
            t = sgm(ttime(idx[(k[0], k[1], m)]) for k in common) if common else float("nan")
            te = sgm((idx[(k[0], k[1], m)]["scip_solve_seconds"] or 0) - cbs(idx[(k[0], k[1], m)]) for k in common) if common else float("nan")
            if m != modes[0]:
                rat = med([ttime(idx[(k[0], k[1], m)]) / ttime(idx[(k[0], k[1], modes[0])]) for k in common])
                ratx = med([((idx[(k[0], k[1], m)]["scip_solve_seconds"] or 0) - cbs(idx[(k[0], k[1], m)])) /
                            (idx[(k[0], k[1], modes[0])]["scip_solve_seconds"] or 1e-9) for k in common])
                bet = wor = 0
                for k in keys:
                    a = idx.get((k[0], k[1], m)); b = idx.get((k[0], k[1], modes[0]))
                    if a is None or b is None or not finite(a.get("dual")) or not finite(b.get("dual")):
                        continue
                    if (a.get("primal_check") or {}).get("passed") is False and a.get("primal") is not None and m == "baseline-extra":
                        pass
                    c = cmpb(a["dual"], b["dual"], a.get("sense") or "min")
                    bet += c > 0; wor += c < 0
            else:
                rat = ratx = None; bet = wor = None
            print(f"    {label} {m:14s} solved {nsol}/{len(rs)} cuts {cuts} ({runs_c} runs, {models_c} models) SGM {t:.3f} "
                  f"excl {te:.3f} ratio {rat if rat is None else round(rat,3)} excl-ratio {ratx if ratx is None else round(ratx,3)} bounds {bet}/{wor} common {len(common)}")
        return idx, keys
    ia, ka = table(A, ["baseline", "all", "auto"], "3A")
    ib, kb = table([r for r in B if r["phase"] == "full"], ["baseline", "all", "auto"], "3B")
    idf, kd = table(DF, ["baseline", "all", "auto", "baseline-extra"], "4D")
    # same models solved per seed
    for lab, idx, keys, modes in (("3A", ia, ka, ["baseline", "all", "auto"]), ("3B", ib, kb, ["baseline", "all", "auto"])):
        diff = [k for k in keys if len({solved(idx[(k[0], k[1], m)]) for m in modes}) > 1]
        print(f"  {lab}: model-seed pairs where modes differ in solved: {diff}")
    # baseline between seeds (3A): final dual bound comparisons
    names = sorted({k[0] for k in ka})
    for s1, s2 in ((0, 1), (0, 2), (1, 2)):
        d = sum(cmpb(ia[(nm, s1, "baseline")]["dual"], ia[(nm, s2, "baseline")]["dual"], ia[(nm, s1, "baseline")]["sense"] or "min") != 0 for nm in names)
        print(f"  3A baseline final dual differs seed {s1} vs {s2}: {d}/30")
    rat = []
    for nm in names:
        for s1, s2 in ((0, 1), (0, 2), (1, 2)):
            a, b = ia[(nm, s1, "baseline")], ia[(nm, s2, "baseline")]
            if solved(a) and solved(b):
                rat.append(ttime(b) / ttime(a))
    print(f"  3A baseline seed-to-seed per-run ratio: median {med(rat):.3f}, range {min(rat):.2f}-{max(rat):.2f} (n={len(rat)})")
    # nodes summed over commonly solved runs
    for lab, idx, keys in (("3A", ia, ka), ("3B", ib, kb)):
        common = [k for k in keys if all(solved(idx[(k[0], k[1], m)]) for m in ("baseline", "all", "auto"))]
        nb = sum(idx[(k[0], k[1], "baseline")]["nodes"] for k in common)
        for m in ("all", "auto"):
            nm_ = sum(idx[(k[0], k[1], m)]["nodes"] for k in common)
            print(f"  {lab} nodes summed {m} vs baseline: {nm_} vs {nb} ({100*(nm_/nb-1):+.2f}%)")
    # models with cuts in full runs
    for lab, idx, keys in (("3A", ia, ka), ("3B", ib, kb)):
        for m in ("all", "auto"):
            print(f"  {lab} {m}: models with cuts (full) {len({k[0] for k in keys if idx[(k[0], k[1], m)]['n_cuts'] > 0})}")
    # better/worse 3B where
    for m in ("all", "auto"):
        w = [(k, cmpb(ib[(k[0], k[1], m)]["dual"], ib[(k[0], k[1], "baseline")]["dual"], ib[(k[0], k[1], m)]["sense"] or "min")) for k in kb]
        print(f"  3B {m} final bound better on {[k for k, c in w if c > 0]}, worse {[k for k, c in w if c < 0]}")
    # root runs 3A/3B
    for lab, recs, recsP in (("3A", AR, AP), ("3B", [r for r in B if r["phase"] == "root"], BP)):
        idx = {(r["name"], r["mode"]): r for r in recs}
        idxP = {(r["name"], r["mode"]): r for r in recsP}
        nms = sorted({r["name"] for r in recs})
        for m in ("all", "auto", "all-diag"):
            better = [nm for nm in nms if cmpb(root_bound(idx[(nm, m)]), root_bound(idx[(nm, "baseline")]), idx[(nm, m)]["sense"] or "min") > 0]
            worse = [nm for nm in nms if cmpb(root_bound(idx[(nm, m)]), root_bound(idx[(nm, "baseline")]), idx[(nm, m)]["sense"] or "min") < 0]
            cuts = sum(idx[(nm, m)]["n_cuts"] for nm in nms)
            print(f"  {lab} root {m:8s}: cuts {cuts}; better {better}; worse {worse}")
        # 3P differences
        ncd = sum(idxP[(nm, m)]["n_cuts"] != idx[(nm, m)]["n_cuts"] for nm in nms for m in ("all", "auto", "all-diag"))
        nbd = sum(cmpb(root_bound(idxP[(nm, m)]), root_bound(idx[(nm, m)]), idx[(nm, m)]["sense"] or "min") != 0 for nm in nms for m in ("all", "auto", "all-diag"))
        nbd_exact = sum(root_bound(idxP[(nm, m)]) != root_bound(idx[(nm, m)]) for nm in nms for m in ("all", "auto", "all-diag"))
        base_same = sum(root_bound(idxP[(nm, "baseline")]) == root_bound(idx[(nm, "baseline")]) for nm in nms)
        print(f"  {lab} 3P vs 3: cut count differs {ncd}/{3*len(nms)}; root bound differs (tol) {nbd}, exactly {nbd_exact}; baseline identical {base_same}/{len(nms)}")
        if lab == "3B":
            for nm in ("ex3_1_4", "pooling_haverly2pq", "pointpack04", "pooling_bental4tp", "pooling_bental4pq"):
                print(f"    {nm}: " + ", ".join(f"{m} {root_bound(idx[(nm, m)]):.6g}" for m in ("baseline", "all", "auto", "all-diag")))
            # stored-row shares
            for m in ("all", "all-diag"):
                rej = sum((idx[(nm, m)].get("separation") or {}).get("row_binding_rejections", 0) for nm in nms)
                cu = sum(idx[(nm, m)]["n_cuts"] for nm in nms)
                print(f"    3B root {m}: stored-row rejected {rej} of {rej + cu} violated ({100*rej/(rej+cu):.1f}%)")
            r = idx[("kall_circlespolygons_c1p12", "all-diag")]
            rj = (r.get("separation") or {}).get("row_binding_rejections")
            print(f"    c1p12 all-diag 3B: rejected {rj}, cuts {r['n_cuts']}, violated {rj + r['n_cuts']}")
    # 4B2
    idx2 = {(r["name"], r["mode"]): r for r in B2}
    idxB = {(r["name"], r["mode"]): r for r in B if r["phase"] == "root"}
    nms = sorted({r["name"] for r in B2})
    for m in ("all-noaggr", "all-diag-noaggr", "all-diag-rowdir-noaggr"):
        rej = sum((idx2[(nm, m)].get("separation") or {}).get("row_binding_rejections", 0) for nm in nms)
        cu = sum(idx2[(nm, m)]["n_cuts"] for nm in nms)
        better = [nm for nm in nms if cmpb(root_bound(idx2[(nm, m)]), root_bound(idx2[(nm, "baseline-noaggr")]), idx2[(nm, m)]["sense"] or "min") > 0]
        worse = [nm for nm in nms if cmpb(root_bound(idx2[(nm, m)]), root_bound(idx2[(nm, "baseline-noaggr")]), idx2[(nm, m)]["sense"] or "min") < 0]
        print(f"  4B2 {m}: rejected {rej}/{rej+cu} ({100*rej/(rej+cu):.1f}%), cuts {cu}; better {len(better)} {better}; worse {worse}")
    same = all(idx2[(nm, "all-diag-noaggr")]["n_cuts"] == idx2[(nm, "all-diag-rowdir-noaggr")]["n_cuts"] and
               root_bound(idx2[(nm, "all-diag-noaggr")]) == root_bound(idx2[(nm, "all-diag-rowdir-noaggr")]) for nm in nms)
    samek = all([c["k"] for c in idx2[(nm, "all-diag-noaggr")]["cuts"]] == [c["k"] for c in idx2[(nm, "all-diag-rowdir-noaggr")]["cuts"]] for nm in nms)
    print(f"  4B2 all-diag-rowdir same counts and bounds as all-diag: {same}; identical cut lists: {samek}")
    weak = [nm for nm in nms if cmpb(root_bound(idx2[(nm, "baseline-noaggr")]), root_bound(idxB[(nm, "baseline")]), idxB[(nm, "baseline")]["sense"] or "min") < 0]
    print(f"  noaggr baseline weaker than 3B baseline on {len(weak)}: {weak}")
    r = idx2[("kall_circlespolygons_c1p12", "all-diag-noaggr")]
    print(f"  c1p12 4B2 all-diag-noaggr cuts {r['n_cuts']}, root {root_bound(r)}")
    # SCIP-extra on 3B models
    bk = best_known("v3/runs/partB")
    better = []; worse = []; full = []; g95 = []; rootsolved_e = 0; rootsolved_b = 0
    for nm in nms:
        e = idx2[(nm, "baseline-extra")]; b = idxB[(nm, "baseline")]
        sense = b["sense"] or "min"
        c = cmpb(root_bound(e), root_bound(b), sense)
        if c > 0: better.append(nm)
        if c < 0: worse.append(nm)
        z = bk.get(nm)
        if z is not None:
            g = gap_closed(root_bound(e), root_bound(b), z, sense)
            if g is not None and g >= 1 - 1e-4 * max(1, abs(z)) / max(abs(z - root_bound(b)), 1e-12):
                full.append(nm)
            elif g is not None and g > 0.95:
                g95.append((nm, round(g, 4)))
        rootsolved_e += solved(e); rootsolved_b += solved(b)
    print(f"  SCIP-extra vs 3B baseline root: better {len(better)}, worse {worse}; closed fully {full}; >95% {g95}; solved at root {rootsolved_e} vs {rootsolved_b}")
    ext = [idx2[(nm, "baseline-extra")] for nm in nms]
    print(f"  SCIP-extra (4B2): interminor applied>0 on {sum(((r.get('native') or {}).get('interminor') or {}).get('Applied', 0) > 0 for r in ext)}, "
          f"eccuts {sum(((r.get('native') or {}).get('eccuts') or {}).get('Applied', 0) > 0 for r in ext)}, "
          f"intersection (quadratic nlhdlr cuts>0) {sum((((r.get('native') or {}).get('nlhdlr_quadratic') or {}).get('Cuts') or 0) > 0 for r in ext)}")
    # 4D
    idr = {(r["name"], r["mode"]): r for r in DR}
    nmd = sorted({r["name"] for r in DR})
    inc = [nm for nm in nmd if (idr[(nm, "all")].get("separation") or {}).get("discovery_incomplete")]
    inc_full = [nm for nm in nmd if (idf[(nm, 0, "all")].get("separation") or {}).get("discovery_incomplete")]
    print(f"  4D all root: discovery incomplete on {len(inc)}; full {len(inc_full)}; same set {set(inc) == set(inc_full)}")
    other = [nm for nm in nmd if nm not in inc]
    nocut = [nm for nm in other if idr[(nm, "all")]["n_cuts"] == 0]
    rej = {nm: (idr[(nm, "all")].get("separation") or {}).get("row_binding_rejections", 0) for nm in other}
    viol = sum(rej.values()) + sum(idr[(nm, "all")]["n_cuts"] for nm in other)
    print(f"  4D all root: of other {len(other)}, no cut on {len(nocut)}; rejections on {sum(v > 0 for v in rej.values())} models, "
          f"{sum(rej.values())} of {viol} violated; cap reached {sum(bool((idr[(nm,'all')].get('discovery') or {}).get('block_cap_reached')) for nm in other)} of {len(other)}")
    capd = sum(bool((idr[(nm, "all-diag")].get("discovery") or {}).get("block_cap_reached")) for nm in nmd)
    print(f"  4D all-diag: block cap reached on {capd}/20")
    for m in ("all-diag", "all-diag-rowdir", "baseline-extra", "all"):
        better = []; worse = []
        cuts = sum(idr[(nm, m)]["n_cuts"] for nm in nmd); mc = sum(idr[(nm, m)]["n_cuts"] > 0 for nm in nmd)
        for nm in nmd:
            r, b = idr[(nm, m)], idr[(nm, "baseline")]
            if m == "baseline-extra" and (r.get("primal_check") or {}).get("passed") is False:
                pass
            c = cmpb(root_bound(r), root_bound(b), r["sense"] or "min")
            if c > 0: better.append(nm)
            if c < 0: worse.append(nm)
        print(f"  4D root {m}: cuts {cuts} on {mc} models; better {better}; worse {worse}")
    bkd = best_known("v4/runs/partD-root")
    for nm in nmd:
        r, b = idr[(nm, "all-diag")], idr[(nm, "baseline")]
        c = cmpb(root_bound(r), root_bound(b), r["sense"] or "min")
        if c != 0 and bkd.get(nm) is not None:
            print(f"    {nm}: all-diag gap closed {gap_closed(root_bound(r), root_bound(b), bkd[nm], r['sense'] or 'min'):.4f}")
    flagged = [r["run_id"] for recs in (DR, DF) for r in recs if (r.get("primal_check") or {}).get("passed") is False]
    print(f"  4D incumbents failing primal check: {flagged}")
    for r in DR + DF:
        pc = r.get("primal_check") or {}
        if pc.get("passed") is False:
            print(f"    {r['run_id']} rel. objective discrepancy {pc.get('relative_objective_discrepancy')} objective {pc.get('objective')} primal {r.get('primal')}")
    # final-bound differences on models with cuts?
    for m in ("all", "auto"):
        d = [nm for nm in nmd if cmpb(idf[(nm, 0, m)]["dual"], idf[(nm, 0, "baseline")]["dual"], idf[(nm, 0, m)]["sense"] or "min") != 0]
        print(f"  4D full {m}: bound differs on {d}; with cuts: {[nm for nm in d if idf[(nm, 0, m)]['n_cuts'] > 0]}")
    sb = [nm for nm in nmd if solved(idf[(nm, 0, "baseline")])]
    print(f"  4D solved: baseline {sb}; extra {[nm for nm in nmd if solved(idf[(nm, 0, 'baseline-extra')])]}")
    # incumbents in all campaigns failing check
    allfail = []
    for c, parts in PARTS.items():
        for p in parts:
            for r in load(p):
                pc = r.get("primal_check") or {}
                if pc.get("checked") and pc.get("passed") is False:
                    allfail.append(r["run_id"] + "@" + p)
    print(f"  incumbents failing the primal check in campaigns 3-5: {allfail}")


def sec_funnel():
    hdr("FUNNEL: Table 1 rows and Section 8.4")
    rows = [("3A full all", "v3/runs/partA-full", "full", "all"), ("3B full all", "v3/runs/partB", "full", "all"),
            ("3B root all-diag", "v3/runs/partB", "root", "all-diag"), ("4B2 root all-diag-noaggr", "v4/runs/partB2", "root", "all-diag-noaggr"),
            ("4D root all", "v4/runs/partD-root", "root", "all"), ("4D root all-diag", "v4/runs/partD-root", "root", "all-diag"),
            ("3C mech", "v3/runs/partC", "root", "all-diag-mech"), ("4C2 frozen-wide", "v4/runs/partC2", "root", "frozen-wide"),
            ("4C3 rowdir-wide", "v4/runs/partC3", "root", "rowdir-wide"), ("4C4 frozen-wide", "v4/runs/partC4", "root", "frozen-wide"),
            ("4C4 rowdir-wide", "v4/runs/partC4", "root", "rowdir-wide"), ("5C-b rowdir-cap64", "v5/runs/partC5b", "root", "rowdir-cap64"),
            ("5S agg-star4", "v5/runs/partS5", "root", "agg-star4"), ("5S agg-star", "v5/runs/partS5", "root", "agg-star")]
    for lab, p, ph, m in rows:
        rs = [r for r in load(p) if r["phase"] == ph and r["mode"] == m]
        S = Counter()
        below = 0
        for r in rs:
            sp = r.get("separation") or {}
            for k in ("certification_calls", "certification_failures", "row_binding_rejections", "row_rounding_rejections",
                      "callback_seconds", "discovery_seconds", "candidate_seconds", "certification_seconds"):
                S[k] += sp.get(k) or 0
            S["cuts"] += r["n_cuts"]
        below = S["certification_calls"] - S["certification_failures"] - S["row_binding_rejections"] - S["row_rounding_rejections"] - S["cuts"]
        print(f"  {lab:24s} calls {S['certification_calls']:6d} failed {S['certification_failures']:4d} below {below:6d} rej {S['row_binding_rejections']:4d} "
              f"roundrej {S['row_rounding_rejections']} cuts {S['cuts']:6d} | cb {S['callback_seconds']:.1f} disc {S['discovery_seconds']:.1f} "
              f"dir {S['candidate_seconds']:.1f} cert {S['certification_seconds']:.1f} | below/certified {below/max(1,S['certification_calls']-S['certification_failures']):.3f} "
              f"rej/violated {S['row_binding_rejections']/max(1,S['row_binding_rejections']+S['cuts']):.3f}")
        if p.startswith(("v3/runs/partC", "v4/runs/partC", "v5")):
            full = [r for r in load(p) if r["phase"] == "full" and r["mode"] == m]
            if full:
                same = sum(1 for r in full for q in rs if q["name"] == r["name"] and [c["k"] for c in q["cuts"]] == [c["k"] for c in r["cuts"]])
                print(f"      full runs with the same cut list as the root run: {same}/{len(full)}")
    # 4D failures from one model
    rs = [r for r in load("v4/runs/partD-root") if r["mode"] == "all-diag"]
    f = sorted(((r.get("separation") or {}).get("certification_failures", 0), r["name"]) for r in rs)[-3:]
    print(f"  4D all-diag failures by model (top): {f}")
    # SCIP excl. median ratio in 4B2 and 4D
    B2 = load("v4/runs/partB2")
    idx = {(r["name"], r["mode"]): r for r in B2}
    for m in ("all-noaggr", "all-diag-noaggr", "all-diag-rowdir-noaggr"):
        rat = [((idx[(nm, m)]["scip_solve_seconds"] or 0) - cbs(idx[(nm, m)])) / idx[(nm, "baseline-noaggr")]["scip_solve_seconds"]
               for nm in {r["name"] for r in B2}]
        print(f"  4B2 {m}: median SCIP-excl ratio {med(rat):.3f}")
    for p, ph in (("v4/runs/partD-root", "root"), ("v4/runs/partD-full", "full")):
        recs = load(p)
        idx = {(r["name"], r["mode"]): r for r in recs}
        for m in sorted({r["mode"] for r in recs} - {"baseline", "baseline-extra"}):
            rat = [((idx[(nm, m)]["scip_solve_seconds"] or 0) - cbs(idx[(nm, m)])) / idx[(nm, "baseline")]["scip_solve_seconds"]
                   for nm in {r["name"] for r in recs}]
            print(f"  {p} {m}: median SCIP-excl ratio {med(rat):.3f}")
    B = [r for r in load("v3/runs/partB") if r["phase"] == "full"]
    cb = [cbs(r) for r in B if r["mode"] == "all"]
    sc = [r["scip_solve_seconds"] for r in B if r["mode"] == "baseline"]
    print(f"  3B full all: callback per run mean {sum(cb)/len(cb):.3f}, median {med(cb):.3f}; baseline SCIP time median {med(sc):.3f}")


if __name__ == "__main__":
    for s in SECTIONS:
        globals()["sec_" + s]()
