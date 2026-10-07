#!/usr/bin/env python3
"""R8: independent recomputation of the campaign-4 MINLPLib numbers (B2, D root, D full).

Standard library only. Reads records.jsonl, jobs.json, cases/ and replay.json of
  experiments/v4/runs/partB2, partD-root, partD-full
and the campaign-3 Part B root runs in experiments/v3/runs/partB (reference
modes "c3:<mode>"). Does not import summarize_v4, summarize_v3, campaign4_digest
or any producer code. Part C4 is not read.

Definitions (campaign-v4 protocol, v4/README.md):
- failed: returncode != 0, a worker_status, or a failure status;
- solved: not failed, status optimal or gaplimit, primal_check.checked and
  primal_check.passed true, finite primal;
- time: total_seconds + preparation_seconds; SCIP time: scip_solve_seconds;
  callback: separation.callback_seconds; SCIP excl. callback: max(0, difference);
- SGM: shifted geometric mean, shift 1 s;
- bounds: sign = +1 (min) / -1 (max); better if sign*(a-b) > rtol*max(1,|a|,|b|),
  worse if < -tol, else tie; a run whose primal check failed is reported as
  'flagged' (and its raw outcome is shown separately);
- root bound: root_dual if finite, else (run ended at the root: node_limit 1 or
  nodes <= 1) the final dual bound if finite;
- root gap closed: (root(m) - root(ref)) / (target - root(ref)), target =
  MINLPLib best known primal bound (case reference_primal, cross-checked with the
  instancedata.csv primalbound); only where sign*(target - root(ref)) > 0;
- reference modes: B2 -noaggr cut modes -> baseline-noaggr; B2 baseline-noaggr,
  baseline-extra and c3:* -> c3:baseline; D: every mode -> baseline.

Usage: R8_minlplib.py [--json OUT]
"""
from __future__ import annotations

import csv
import json
import math
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]
EXP = PAPER / "experiments"
RUNS = EXP / "v4" / "runs"
V3B = EXP / "v3" / "runs" / "partB"
SCAN = EXP / "v4" / "scanD" / "records.jsonl"
CSV_SNAPSHOT = EXP / "v4" / "snapshot" / "code" / "minlp_solver_lab" / "instances" / "instancedata.csv"
CSV_LIVE = PAPER.parent / "code" / "minlp_solver_lab" / "instances" / "instancedata.csv"
FAIL_STATUSES = {"process_timeout", "worker_error", "worker_no_output", "worker_output_parse_error"}
TOLS = (1e-4, 1e-6)


# ------------------------------------------------------------------ basics

def load(d):
    recs = [json.loads(l) for l in (d / "records.jsonl").read_text().splitlines() if l.strip()]
    jobs = json.loads((d / "jobs.json").read_text())
    cases = {p.stem: json.loads(p.read_text()) for p in (d / "cases").glob("*.json")}
    return recs, jobs, cases


def fin(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def failed(r):
    return r.get("returncode", 0) != 0 or bool(r.get("worker_status")) or r.get("status") in FAIL_STATUSES


def check_passed(r):
    pc = r.get("primal_check") or {}
    return pc.get("checked") is True and pc.get("passed") is True


def has_incumbent(r):
    return (r.get("primal_check") or {}).get("checked") is True


def solved(r):
    return (not failed(r) and r.get("status") in ("optimal", "gaplimit") and check_passed(r)
            and fin(r.get("primal")))


def secs(r):
    return r["total_seconds"] + (r.get("preparation_seconds") or 0.0)


def scip_secs(r):
    v = r.get("scip_solve_seconds")
    return v if fin(v) else None


def cb(r):
    return (r.get("separation") or {}).get("callback_seconds", 0.0) or 0.0


def scip_excl(r):
    v = scip_secs(r)
    return None if v is None else max(0.0, v - cb(r))


def root_bound(r):
    if r is None or failed(r):
        return None
    if fin(r.get("root_dual")):
        return r["root_dual"]
    if (r.get("node_limit") == 1 or (r.get("nodes") is not None and r["nodes"] <= 1)) and fin(r.get("dual")):
        return r["dual"]
    return None


def sgm(vals, shift=1.0):
    vals = [v for v in vals if v is not None]
    if not vals:
        return None
    return math.exp(sum(math.log(v + shift) for v in vals) / len(vals)) - shift


def flagged(r):
    return (r.get("primal_check") or {}).get("passed") is False


def outcome(a, b, va, vb, rtol):
    if a is None or b is None or not fin(va) or not fin(vb):
        return "unavailable", None
    sign = 1 if (a.get("sense") or "min") == "min" else -1
    imp = sign * (va - vb)
    tol = rtol * max(1.0, abs(va), abs(vb))
    raw = "better" if imp > tol else "worse" if imp < -tol else "tie"
    return ("flagged" if (flagged(a) or flagged(b)) else raw), raw


def ncuts(r):
    return len(r["cuts"]) if isinstance(r.get("cuts"), list) else 0


def fmt(x, nd=4):
    if x is None:
        return "None"
    if isinstance(x, float):
        return f"{x:.{nd}g}"
    return str(x)


def minmax_med(vals):
    vals = sorted(vals)
    if not vals:
        return "n/a"
    return f"{fmt(statistics.median(vals), 3)} [{fmt(vals[0], 3)}, {fmt(vals[-1], 3)}] (n={len(vals)})"


# ------------------------------------------------------------------ indices

def index_part(d, phase=None, prefix=""):
    recs, jobs, cases = load(d)
    idx = {}
    for r in recs:
        if phase and r["phase"] != phase:
            continue
        if r.get("seed", 0) != 0:
            continue
        idx[(r["name"], prefix + r["mode"])] = r
    return recs, jobs, cases, idx


def csv_primal(path):
    if not path.exists():
        return {}
    with path.open() as s:
        return {row["name"]: row for row in csv.DictReader(s, delimiter=";")}


# ------------------------------------------------------------------ sections

OUT = {}


def section(title):
    print("\n" + "=" * 100 + "\n" + title + "\n" + "=" * 100)


def coverage(name, d):
    recs, jobs, cases = load(d)
    sched = [run["run_id"] for job in jobs["jobs"] for run in job["runs"]]
    ids = [r["run_id"] for r in recs]
    rep = json.loads((d / "replay.json").read_text()) if (d / "replay.json").exists() else {}
    v4 = rep.get("v4") or {}
    out = {
        "scheduled": len(sched), "recorded": len(recs), "missing": sorted(set(sched) - set(ids)),
        "duplicates": [k for k, c in Counter(ids).items() if c > 1],
        "statuses": dict(Counter(r.get("status") for r in recs)),
        "failed": [r["run_id"] for r in recs if failed(r)],
        "returncode_nonzero": sum(r.get("returncode", 0) != 0 for r in recs),
        "worker_status": sum(bool(r.get("worker_status")) for r in recs),
        "missing_cut_logs": [r["run_id"] for r in recs if r.get("separation") is not None
                             and (not isinstance(r.get("cuts"), list) or r.get("cut_log_complete") is not True)],
        "cuts_total": sum(ncuts(r) for r in recs),
        "replay_passed": rep.get("passed"), "replay_cuts": rep.get("cuts"), "replay_replayed": rep.get("replayed_cuts"),
        "replay_config_failures": len(v4.get("config_failures", []) or []),
        "replay_tamper_modes": sorted((v4.get("tamper_controls_by_mode") or {}).keys()),
        "replay_tamper_all_rejected": {m: all(v.get("rejections", {}).values())
                                       for m, v in (v4.get("tamper_controls_by_mode") or {}).items()},
        "classifier_errors": sum(((r.get("row_binding_rejection_causes") or {}).get("classifier_errors") or 0)
                                 for r in recs),
        "cause_sum_mismatch": [r["run_id"] for r in recs if r.get("separation") is not None
                               and "row_binding_rejection_causes" in r   # campaign 3 records no causes
                               and sum(((r.get("row_binding_rejection_causes") or {}).get("causes") or {}).values())
                               != r["separation"].get("row_binding_rejections", 0)],
        "cuts_field_vs_list": [r["run_id"] for r in recs if r.get("separation") is not None
                               and r["separation"].get("cuts") != ncuts(r)],
    }
    section(f"Coverage and replay: {name}")
    for k, v in out.items():
        print(f"  {k}: {v}")
    OUT.setdefault(name, {})["coverage"] = out


def funnel(rows):
    t = Counter()
    causes, statuses = Counter(), Counter()
    runs_bind = 0
    for r in rows:
        s = r.get("separation") or {}
        for k in ("calls", "certification_calls", "certification_failures", "row_rounding_rejections",
                  "row_binding_rejections", "cuts"):
            t[k] += s.get(k, 0) or 0
        for k in ("callback_seconds", "discovery_seconds", "candidate_seconds", "certification_seconds",
                  "row_seconds"):
            t[k] += s.get(k, 0.0) or 0.0
        t["cut_list"] += ncuts(r)
        runs_bind += bool(s.get("row_binding_rejections"))
        info = r.get("row_binding_rejection_causes")
        if info:
            causes.update(info.get("causes") or {})
            statuses.update(info.get("variable_statuses") or {})
    t["below_threshold"] = (t["certification_calls"] - t["certification_failures"] - t["row_rounding_rejections"]
                            - t["row_binding_rejections"] - t["cuts"])
    return dict(t), runs_bind, dict(causes), dict(statuses)


def caps(rows):
    """Per run: which limit was reached (config from the record)."""
    c = Counter()
    per = {}
    for r in rows:
        s = r.get("separation") or {}
        cfg = r.get("config") or {}
        hit = []
        cut_cap = s.get("cuts", 0) >= cfg.get("max_cuts", math.inf)
        sup_cap = s.get("certification_calls", 0) >= cfg.get("max_support_calls", math.inf)
        rnd_cap = s.get("calls", 0) >= cfg.get("max_rounds", math.inf)
        time_b = bool(s.get("budget_exhausted")) and not cut_cap and not sup_cap
        disc = bool(s.get("discovery_incomplete"))
        if cut_cap: hit.append("cut_cap")
        if sup_cap: hit.append("support_cap")
        if rnd_cap: hit.append(f"callback_cap({cfg.get('max_rounds')})")
        if time_b: hit.append("time_budget")
        if disc: hit.append("discovery_stopped")
        for h in hit:
            c[h.split("(")[0]] += 1
        if not (cut_cap or sup_cap or rnd_cap or time_b):
            c["none"] += 1
        per[r["name"]] = hit
    limits = Counter((r.get("config") or {}).get("max_rounds") for r in rows)
    sup = Counter((r.get("config") or {}).get("max_support_calls") for r in rows)
    cutc = Counter((r.get("config") or {}).get("max_cuts") for r in rows)
    sepsec = Counter((r.get("config") or {}).get("max_separation_seconds") for r in rows)
    return dict(c), per, {"max_rounds": dict(limits), "max_support_calls": dict(sup), "max_cuts": dict(cutc),
                          "max_separation_seconds": dict(sepsec)}


def print_funnel(label, rows):
    t, rb, causes, statuses = funnel(rows)
    cc, per, lim = caps(rows)
    print(f"  {label}: runs {len(rows)} callbacks {t['calls']} support_calls {t['certification_calls']} "
          f"cert_fail {t['certification_failures']} rounding {t['row_rounding_rejections']} "
          f"below_thr {t['below_threshold']} binding {t['row_binding_rejections']} ({rb} runs) cuts {t['cuts']} "
          f"(list {t['cut_list']}) share_of_violated "
          f"{t['row_binding_rejections']}/{t['row_binding_rejections'] + t['cuts']}="
          f"{(t['row_binding_rejections'] / max(1, t['row_binding_rejections'] + t['cuts'])):.4f}")
    print(f"      causes {causes} statuses {statuses}")
    print(f"      seconds: callback {t['callback_seconds']:.2f} discovery {t['discovery_seconds']:.2f} "
          f"candidate {t['candidate_seconds']:.2f} certification {t['certification_seconds']:.2f} "
          f"row {t['row_seconds']:.2f}")
    print(f"      caps {cc}  config limits {lim}")
    return t, rb, causes, statuses, cc, per


def per_model_funnel(rows):
    out = {}
    for r in rows:
        s = r.get("separation") or {}
        out[r["name"]] = {"calls": s.get("calls"), "support": s.get("certification_calls"),
                          "fail": s.get("certification_failures"), "bind": s.get("row_binding_rejections"),
                          "cuts": s.get("cuts"), "disc_incomplete": s.get("discovery_incomplete"),
                          "callback_s": s.get("callback_seconds"),
                          "causes": (r.get("row_binding_rejection_causes") or {}).get("causes"),
                          "statuses": (r.get("row_binding_rejection_causes") or {}).get("variable_statuses")}
    return out


def bound_table(idx, names, mode, ref, key, label, targets=None):
    res = {}
    for rtol in TOLS:
        cnt, rows = Counter(), []
        for n in names:
            a, b = idx.get((n, mode)), idx.get((n, ref))
            va = key(a) if a else None
            vb = key(b) if b else None
            o, raw = outcome(a, b, va, vb, rtol)
            cnt[o] += 1
            rows.append((n, o, raw, va, vb))
        res[rtol] = (dict(cnt), rows)
    print(f"  {label}: {mode} vs {ref}: 1e-4 {res[1e-4][0]}  1e-6 {res[1e-6][0]}")
    for n, o, raw, va, vb in res[1e-4][1]:
        o6 = [x for x in res[1e-6][1] if x[0] == n][0][1]
        if o != "tie" or o6 != "tie":
            g = ""
            if targets is not None:
                gc = gap_closed(idx, n, mode, ref, targets)
                g = f" gap_closed {fmt(gc, 4)}"
            print(f"      {n}: 1e-4 {o} (raw {raw}) 1e-6 {o6}: {va!r} vs {vb!r}{g}")
    return res


def gap_closed(idx, n, mode, ref, targets):
    a, b = idx.get((n, mode)), idx.get((n, ref))
    t = targets.get(n)
    va, vb = root_bound(a), root_bound(b)
    if not (fin(va) and fin(vb) and fin(t)):
        return None
    sign = 1 if (b.get("sense") or "min") == "min" else -1
    if sign * (t - vb) <= 0:
        return None
    return (va - vb) / (t - vb)


def time_decomp(idx, names, mode, ref, phase):
    def ok(r):
        if r is None or failed(r):
            return False
        return solved(r) if phase == "full" else ("total_seconds" in r)
    pairs = [n for n in names if ok(idx.get((n, mode))) and ok(idx.get((n, ref)))]
    A = [idx[(n, mode)] for n in pairs]
    B = [idx[(n, ref)] for n in pairs]
    ratio_excl = [scip_excl(a) / max(scip_secs(b), 1e-9) for a, b in zip(A, B)
                  if scip_excl(a) is not None and scip_secs(b)]
    ratio_tot = [secs(a) / max(secs(b), 1e-9) for a, b in zip(A, B)]
    out = {"pairs": len(pairs), "sgm_total": sgm([secs(a) for a in A]), "sgm_excl": sgm([scip_excl(a) for a in A]),
           "sgm_cb": sgm([cb(a) for a in A]), "ref_sgm_total": sgm([secs(b) for b in B]),
           "ref_sgm_scip": sgm([scip_secs(b) for b in B]),
           "median_excl_over_ref_scip": statistics.median(ratio_excl) if ratio_excl else None,
           "median_total_over_ref": statistics.median(ratio_tot) if ratio_tot else None,
           "faster": sum(x < 1 for x in ratio_tot)}
    print(f"  time {phase} {mode} vs {ref}: " + " ".join(f"{k} {fmt(v, 4)}" for k, v in out.items()))
    return out


def native(rows, label):
    tot = defaultdict(Counter)
    for r in rows:
        ns = r.get("native_statistics") or {}
        seps = ns.get("separators") or {}
        for name in ("interminor", "minor", "rlt", "eccuts"):
            row = seps.get(name) or {}
            calls = row.get("Calls") if isinstance(row.get("Calls"), int) else 0
            tot[name]["runs"] += bool(calls)
            for col in ("Calls", "FoundCuts", "Applied"):
                tot[name][col] += row.get(col) if isinstance(row.get(col), int) else 0
        q = (ns.get("nlhdlrs") or {}).get("quadratic") or {}
        cuts_q = q.get("Cuts") if isinstance(q.get("Cuts"), int) else 0
        tot["quadratic"]["runs_with_cuts"] += bool(cuts_q)
        tot["quadratic"]["#Enforce"] += q.get("#Enforce") if isinstance(q.get("#Enforce"), int) else 0
        tot["quadratic"]["Cuts"] += cuts_q
    print(f"  native {label}: " + "; ".join(f"{k} {dict(v)}" for k, v in tot.items()))
    return {k: dict(v) for k, v in tot.items()}


# ------------------------------------------------------------------ B2

def part_b2():
    d = RUNS / "partB2"
    recs, jobs, cases, idx = index_part(d)
    _, _, cases3, idx3 = index_part(V3B, phase="root", prefix="c3:")
    mism = sorted(n for n in cases if n in cases3 and cases3[n] != cases[n])
    idx.update({k: v for k, v in idx3.items() if k[0] not in mism})
    names = [job["name"] for job in jobs["jobs"]]
    section("B2: setup")
    print(f"  models {len(names)}; v3 partB root case mismatches {mism}; c3 modes "
          f"{sorted({k[1] for k in idx3})}")
    snap, live = csv_primal(CSV_SNAPSHOT), csv_primal(CSV_LIVE)
    targets = {}
    for n in names:
        rp = cases[n].get("reference_primal")
        try:
            targets[n] = float(rp)
        except (TypeError, ValueError):
            targets[n] = None
        sp = (snap.get(n) or {}).get("primalbound")
        lp = (live.get(n) or {}).get("primalbound")
        if (sp or None) != (rp or None) or (lp or None) != (rp or None):
            print(f"  reference mismatch {n}: case {rp!r} snapshot csv {sp!r} live csv {lp!r}")
    print(f"  models without reference_primal: {[n for n in names if targets[n] is None]}")
    print(f"  maximization models: {sorted({n for (n, m), r in idx.items() if r.get('sense') == 'max'})}")

    section("B2: funnel per mode (sums over 30 root runs)")
    modes_cut = ["c3:all", "all-noaggr", "c3:all-diag", "all-diag-noaggr", "all-diag-rowdir-noaggr", "c3:auto"]
    fun = {}
    for m in modes_cut:
        rows = [idx[(n, m)] for n in names if (n, m) in idx]
        fun[m] = print_funnel(m, rows)
    section("B2: per-model separator counts (binding/cuts, cert failures)")
    pm = {m: per_model_funnel([idx[(n, m)] for n in names if (n, m) in idx]) for m in modes_cut}
    for n in names:
        parts = []
        for m in ["c3:all", "all-noaggr", "c3:all-diag", "all-diag-noaggr", "all-diag-rowdir-noaggr"]:
            x = pm[m].get(n, {})
            if x.get("bind") or x.get("cuts") or x.get("fail"):
                parts.append(f"{m} {x.get('bind')}/{x.get('cuts')} f{x.get('fail')} {x.get('causes') or ''}"
                             f"{(' st' + str(x.get('statuses'))) if x.get('statuses') else ''}")
        if parts:
            print(f"  {n}: " + " | ".join(parts))

    section("B2: root bounds vs references")
    rb = {}
    for m, ref in [("all-noaggr", "baseline-noaggr"), ("all-diag-noaggr", "baseline-noaggr"),
                   ("all-diag-rowdir-noaggr", "baseline-noaggr"), ("baseline-noaggr", "c3:baseline"),
                   ("baseline-extra", "c3:baseline"), ("c3:all", "c3:baseline"), ("c3:all-diag", "c3:baseline"),
                   ("c3:auto", "c3:baseline"), ("all-diag-rowdir-noaggr", "all-diag-noaggr")]:
        rb[(m, ref)] = bound_table(idx, names, m, ref, root_bound, "root", targets)
    same = [n for n in names if root_bound(idx[(n, "all-diag-rowdir-noaggr")]) != root_bound(idx[(n, "all-diag-noaggr")])]
    print(f"  models where rowdir and all-diag-noaggr root bounds differ exactly: {same}")
    samecuts = [n for n in names if ncuts(idx[(n, "all-diag-rowdir-noaggr")]) != ncuts(idx[(n, "all-diag-noaggr")])]
    print(f"  models where rowdir and all-diag-noaggr cut counts differ: {samecuts}")

    section("B2: root gap closed vs MINLPLib primalbound")
    refs = {"all-noaggr": "baseline-noaggr", "all-diag-noaggr": "baseline-noaggr",
            "all-diag-rowdir-noaggr": "baseline-noaggr", "baseline-noaggr": "c3:baseline",
            "baseline-extra": "c3:baseline", "c3:all": "c3:baseline", "c3:all-diag": "c3:baseline"}
    for m, ref in refs.items():
        vals = {n: gap_closed(idx, n, m, ref, targets) for n in names}
        v = [x for x in vals.values() if x is not None]
        excl = [n for n in names if vals[n] is None]
        print(f"  {m} vs {ref}: median [min,max] {minmax_med(v)}; excluded {excl}; "
              f"exact zeros {sum(x == 0 for x in v)}")
    n = "kall_circlespolygons_c1p12"
    print(f"  {n}: all-diag-noaggr root {root_bound(idx[(n, 'all-diag-noaggr')])} baseline-noaggr "
          f"{root_bound(idx[(n, 'baseline-noaggr')])} target {targets[n]}")

    section("B2: solved at the root, statuses, incumbents")
    for m in ["c3:baseline", "baseline-noaggr", "baseline-extra", "all-noaggr", "all-diag-noaggr",
              "all-diag-rowdir-noaggr", "c3:all", "c3:all-diag"]:
        rows = [idx[(n, m)] for n in names]
        print(f"  {m}: solved {sum(map(solved, rows))} {sorted(r['name'] for r in rows if solved(r))}; "
              f"statuses {dict(Counter(r['status'] for r in rows))}; no incumbent "
              f"{sorted(r['name'] for r in rows if not has_incumbent(r))}; primal check failed "
              f"{[r['name'] for r in rows if flagged(r)]}; root bound missing "
              f"{[r['name'] for r in rows if root_bound(r) is None]}")
    for m in ["baseline-noaggr", "c3:baseline"]:
        pass

    section("B2: times (root, all runs completed)")
    td = {}
    for m, ref in [("all-noaggr", "baseline-noaggr"), ("all-diag-noaggr", "baseline-noaggr"),
                   ("all-diag-rowdir-noaggr", "baseline-noaggr"), ("baseline-extra", "c3:baseline"),
                   ("baseline-noaggr", "c3:baseline"), ("c3:all", "c3:baseline"), ("c3:all-diag", "c3:baseline")]:
        td[(m, ref)] = time_decomp(idx, names, m, ref, "root")
    allm = ["baseline-noaggr", "all-noaggr", "all-diag-noaggr", "all-diag-rowdir-noaggr", "baseline-extra",
            "c3:baseline", "c3:all", "c3:auto", "c3:all-diag"]
    common = [n for n in names if all((n, m) in idx and not failed(idx[(n, m)]) for m in allm)]
    print(f"  pooled over {len(common)} models completed by all modes: " + ", ".join(
        f"{m} {fmt(sgm([secs(idx[(n, m)]) for n in common]), 4)}" for m in allm))

    section("B2: native separators")
    for m in ["baseline-extra", "baseline-noaggr", "all-noaggr", "all-diag-noaggr"]:
        native([idx[(n, m)] for n in names], m)

    section("B2: load at start (mean of 1-min load)")
    for m in allm:
        rows = [idx[(n, m)] for n in names if "load_start" in idx[(n, m)]]
        print(f"  {m}: {statistics.fmean(r['load_start'][0] for r in rows):.2f}")
    OUT["B2"] = {"funnel": {m: fun[m][:4] for m in fun}}


# ------------------------------------------------------------------ D

def part_d():
    dr, df = RUNS / "partD-root", RUNS / "partD-full"
    recs_r, jobs_r, cases_r, R = index_part(dr)
    recs_f, jobs_f, cases_f, F = index_part(df)
    names = [job["name"] for job in jobs_r["jobs"]]
    names_f = [job["name"] for job in jobs_f["jobs"]]
    section("D: setup")
    print(f"  root models {len(names)}, full models {len(names_f)}, same set {set(names) == set(names_f)}; "
          f"cases equal {all(cases_r[n] == cases_f[n] for n in names)}")
    snap, live = csv_primal(CSV_SNAPSHOT), csv_primal(CSV_LIVE)
    targets = {}
    for n in names:
        rp = cases_r[n].get("reference_primal")
        try:
            targets[n] = float(rp)
        except (TypeError, ValueError):
            targets[n] = None
        sp = (snap.get(n) or {}).get("primalbound")
        lp = (live.get(n) or {}).get("primalbound")
        if (sp or None) != (rp or None) or (lp or None) != (rp or None):
            print(f"  reference mismatch {n}: case {rp!r} snapshot csv {sp!r} live csv {lp!r}")
        print(f"  {n}: sense {R[(n, 'baseline')].get('sense')} reference_primal {rp} csv objsense "
              f"{(snap.get(n) or {}).get('objsense')}")
    print(f"  without reference_primal: {[n for n in names if targets[n] is None]}")

    section("D root: per-mode status, cuts, root bounds")
    modes = ["baseline", "all", "all-diag", "all-diag-rowdir", "baseline-extra"]
    for m in modes:
        rows = [R[(n, m)] for n in names]
        per_model = {r["name"]: ncuts(r) for r in rows if ncuts(r)}
        print(f"  {m}: statuses {dict(Counter(r['status'] for r in rows))}; models with cuts "
              f"{sum(ncuts(r) > 0 for r in rows)}; cuts {sum(map(ncuts, rows))}; per model {per_model}")
        print(f"      no incumbent {sorted(r['name'] for r in rows if not has_incumbent(r))}; "
              f"primal check failed {[r['name'] for r in rows if flagged(r)]}; root bound missing "
              f"{[r['name'] for r in rows if root_bound(r) is None]}; root_dual missing "
              f"{[r['name'] for r in rows if not fin(r.get('root_dual'))]}")
        tl = [(r["name"], round(secs(r), 2)) for r in rows if r["status"] == "timelimit"]
        print(f"      timelimit runs {tl}")
        over = [(r["name"], round(secs(r), 2)) for r in rows if secs(r) > r["time_limit"] + 0.01]
        print(f"      soft-budget overshoots (> limit + 0.01 s): {over}")
    for r in recs_r:
        if flagged(r):
            print(f"  FLAGGED {r['run_id']}: primal {r.get('primal')} check {r.get('primal_check')}")

    section("D root: bounds vs baseline")
    for m in ["all", "all-diag", "all-diag-rowdir", "baseline-extra"]:
        bound_table(R, names, m, "baseline", root_bound, "root", targets)
    bound_table(R, names, "all-diag-rowdir", "all-diag", root_bound, "root (rowdir vs all-diag)", None)

    section("D root: root gap closed vs MINLPLib primalbound (reference baseline)")
    for m in ["all", "all-diag", "all-diag-rowdir", "baseline-extra"]:
        vals = {n: gap_closed(R, n, m, "baseline", targets) for n in names}
        v = [x for x in vals.values() if x is not None]
        vnoflag = [x for n, x in vals.items() if x is not None and not flagged(R[(n, m)])]
        print(f"  {m}: {minmax_med(v)}; excluded {[n for n in names if vals[n] is None]}; exact zeros "
              f"{sum(x == 0 for x in v)}; without flagged runs {minmax_med(vnoflag)}")
        for n in names:
            if vals[n] not in (None, 0):
                print(f"      {n}: {vals[n]:.6g} (root {root_bound(R[(n, m)])!r} base "
                      f"{root_bound(R[(n, 'baseline')])!r} target {targets[n]})")

    section("D root: funnel and caps")
    disc_scan = {}
    for l in SCAN.read_text().splitlines():
        if l.strip():
            x = json.loads(l)
            disc_scan[x["name"]] = x.get("discovery_seconds")
    for m in ["all", "all-diag", "all-diag-rowdir"]:
        rows = [R[(n, m)] for n in names]
        t, rb, causes, statuses, cc, per = print_funnel(m, rows)
        pm = per_model_funnel(rows)
        for n in names:
            x = pm[n]
            if x["bind"] or x["fail"] or x["cuts"] or m == "all":
                print(f"      {n}: calls {x['calls']} support {x['support']} fail {x['fail']} bind {x['bind']} "
                      f"cuts {x['cuts']} disc_incomplete {x['disc_incomplete']} cb {fmt(x['callback_s'], 4)} "
                      f"scan_disc {fmt(disc_scan.get(n), 3)} caps {per[n]} causes {x['causes']} st {x['statuses']}")
    rows = [R[(n, "all")] for n in names]
    stopped = [r["name"] for r in rows if (r.get("separation") or {}).get("discovery_incomplete")]
    slow = [n for n in names if disc_scan.get(n) is not None and disc_scan[n] > 1.0]
    nocut = [r["name"] for r in rows if ncuts(r) == 0]
    print(f"  D root all: discovery stopped on {len(stopped)}: {stopped}")
    print(f"  scan discovery > 1 s: {len(slow)} {slow}; range "
          f"{fmt(min(disc_scan[n] for n in slow), 3)}-{fmt(max(disc_scan[n] for n in slow), 3)}; "
          f"sets equal {set(stopped) == set(slow)}")
    print(f"  models with no cuts in mode all: {len(nocut)}; of which discovery stopped "
          f"{len(set(nocut) & set(stopped))}; completed discovery but no cuts "
          f"{sorted(set(nocut) - set(stopped))} with support calls "
          f"{[R[(n, 'all')]['separation']['certification_calls'] for n in sorted(set(nocut) - set(stopped))]}")
    print(f"  stopped runs: support calls {[R[(n, 'all')]['separation']['certification_calls'] for n in stopped]}"
          f" callback s {[round(cb(R[(n, 'all')]), 3) for n in stopped]}")

    section("D root: times")
    for m in ["all", "all-diag", "all-diag-rowdir", "baseline-extra"]:
        time_decomp(R, names, m, "baseline", "root")
    allc = [n for n in names if all(not failed(R[(n, m)]) and root_bound(R[(n, m)]) is not None for m in modes)]
    print(f"  models completed with a root bound in every mode: {len(allc)}")
    for m in modes:
        rows = [R[(n, m)] for n in names if "load_start" in R[(n, m)]]
        print(f"  load {m}: {statistics.fmean(r['load_start'][0] for r in rows):.2f}")

    # ---------------- full
    section("D full: statuses, solved, cuts")
    fmodes = ["baseline", "all", "auto", "baseline-extra"]
    for m in fmodes:
        rows = [F[(n, m)] for n in names_f]
        print(f"  {m}: statuses {dict(Counter(r['status'] for r in rows))}; solved {sum(map(solved, rows))} "
              f"{[(r['name'], r['status']) for r in rows if solved(r)]}; cuts {sum(map(ncuts, rows))} "
              f"{[(r['name'], ncuts(r)) for r in rows if ncuts(r)]}")
        print(f"      no incumbent {sorted(r['name'] for r in rows if not has_incumbent(r))}; primal check failed "
              f"{[r['name'] for r in rows if flagged(r)]}; status optimal/gaplimit but not solved "
              f"{[r['name'] for r in rows if r['status'] in ('optimal', 'gaplimit') and not solved(r)]}")
        over = sorted((round(secs(r), 3), r["name"]) for r in rows if secs(r) > r["time_limit"] + 0.01)
        print(f"      overshoots {len(over)}: min {over[0] if over else None} max {over[-1] if over else None}")
        tlr = [secs(r) for r in rows if r["status"] == "timelimit"]
        print(f"      timelimit runs {len(tlr)} charged {fmt(min(tlr), 6) if tlr else None}-{fmt(max(tlr), 6) if tlr else None}")
    allf = [r for r in recs_f]
    over_all = sorted((round(secs(r), 3), r["run_id"]) for r in allf if secs(r) > r["time_limit"] + 0.01)
    print(f"  D full overshoots total {len(over_all)}; largest {over_all[-1]}; timelimit total "
          f"{sum(r['status'] == 'timelimit' for r in allf)}")

    section("D full: final dual vs baseline")
    for m in ["all", "auto", "baseline-extra"]:
        bound_table(F, names_f, m, "baseline", lambda r: r.get("dual") if r and not failed(r) else None, "final")
    for m in ["all", "auto"]:
        diff = [n for n in names_f if outcome(F[(n, m)], F[(n, "baseline")], F[(n, m)].get("dual"),
                                              F[(n, "baseline")].get("dual"), 1e-4)[0] != "tie"]
        print(f"  {m}: models with 1e-4 difference {diff}; of these with cuts "
              f"{[n for n in diff if ncuts(F[(n, m)])]}")

    section("D full: times")
    common = [n for n in names_f if all(solved(F[(n, m)]) for m in fmodes)]
    print(f"  solved by all four: {common}")
    for m in fmodes:
        A = [F[(n, m)] for n in common]
        print(f"  {m}: SGM total {fmt(sgm([secs(a) for a in A]), 5)} SCIP {fmt(sgm([scip_secs(a) for a in A]), 5)} "
              f"excl {fmt(sgm([scip_excl(a) for a in A]), 5)} cb {fmt(sgm([cb(a) for a in A]), 4)}")
        A = [F[(n, m)] for n in names_f]
        print(f"      all 20: SGM total {fmt(sgm([secs(a) for a in A]), 5)} SCIP {fmt(sgm([scip_secs(a) for a in A]), 5)}"
              f" excl {fmt(sgm([scip_excl(a) for a in A]), 5)} sum cb {sum(cb(a) for a in A):.2f}")
    for m in ["all", "auto", "baseline-extra"]:
        time_decomp(F, names_f, m, "baseline", "full")
    for m in fmodes:
        rows = [F[(n, m)] for n in names_f if "load_start" in F[(n, m)]]
        print(f"  load {m}: {statistics.fmean(r['load_start'][0] for r in rows):.2f}")

    section("D full: funnel and discovery")
    for m in ["all", "auto"]:
        rows = [F[(n, m)] for n in names_f]
        print_funnel(m, rows)
        st = [r["name"] for r in rows if (r.get("separation") or {}).get("discovery_incomplete")]
        print(f"      discovery stopped {len(st)}: {st}")
    rs = {r["name"] for r in [R[(n, "all")] for n in names] if r["separation"].get("discovery_incomplete")}
    for m in ["all", "auto"]:
        fs = {n for n in names_f if F[(n, m)]["separation"].get("discovery_incomplete")}
        print(f"  root-stopped minus full-stopped ({m}): {sorted(rs - fs)}; full minus root {sorted(fs - rs)}")


# ------------------------------------------------------------------ comparison with the digest

def num_match(value, text):
    """True if value rounds to the digest's displayed number (commas ignored)."""
    if value is None:
        return False
    s = text.replace(",", "").strip()
    try:
        float(s)
    except ValueError:
        return False
    if "e" in s.lower():
        mant, exp = s.lower().split("e")
        d = len(mant.split(".")[1]) if "." in mant else 0
        unit = 10 ** (int(exp) - d)
    else:
        d = len(s.split(".")[1]) if "." in s else 0
        unit = 10 ** (-d)
    return abs(value - float(s)) <= 0.5001 * unit + 1e-15


CHECKS = []


def chk(item, digest, value, severity="major", reason="", exact=None):
    """Record one check. `digest` is the digest's text; numbers are compared at its precision."""
    if exact is not None:
        ok = exact
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        ok = num_match(value, digest)
    else:
        ok = str(value) == str(digest)
    CHECKS.append({"item": item, "digest_value": str(digest), "recomputed_value": str(value), "match": bool(ok),
                   "severity": None if ok else severity, "reason": "" if ok else reason})


def compare_with_digest():
    b2 = RUNS / "partB2"
    _, jobs_b, cases_b, IB = index_part(b2)
    _, _, _, I3 = index_part(V3B, phase="root", prefix="c3:")
    IB.update(I3)
    nb = [j["name"] for j in jobs_b["jobs"]]
    tb = {}
    for n in nb:
        try:
            tb[n] = float(cases_b[n].get("reference_primal"))
        except (TypeError, ValueError):
            tb[n] = None
    _, jobs_r, cases_r, R = index_part(RUNS / "partD-root")
    _, jobs_f, _, F = index_part(RUNS / "partD-full")
    nd = [j["name"] for j in jobs_r["jobs"]]
    td_ = {}
    for n in nd:
        try:
            td_[n] = float(cases_r[n].get("reference_primal"))
        except (TypeError, ValueError):
            td_[n] = None

    def rows(I, names, m):
        return [I[(n, m)] for n in names]

    def bc(I, names, m, ref, key, rtol):
        c = Counter(outcome(I[(n, m)], I[(n, ref)], key(I[(n, m)]), key(I[(n, ref)]), rtol)[0] for n in names)
        return c.get("better", 0), c.get("tie", 0), c.get("worse", 0), c.get("flagged", 0)

    dual = lambda r: r.get("dual") if r and not failed(r) else None

    # ---- coverage
    for label, d, sched, st in [("B2", b2, 150, {"optimal": 37, "gaplimit": 6, "nodelimit": 107}),
                                ("D root", RUNS / "partD-root", 100, {"nodelimit": 95, "timelimit": 5}),
                                ("D full", RUNS / "partD-full", 80, {"optimal": 4, "gaplimit": 3, "timelimit": 73})]:
        recs, jobs, _ = load(d)
        rep = json.loads((d / "replay.json").read_text())
        chk(f"{label} scheduled/recorded", f"{sched} / {sched}",
            f"{sum(len(j['runs']) for j in jobs['jobs'])} / {len(recs)}")
        chk(f"{label} status counts", json.dumps(st, sort_keys=True),
            json.dumps(dict(Counter(r["status"] for r in recs)), sort_keys=True))
        chk(f"{label} failures", "0", str(sum(failed(r) for r in recs)))
        chk(f"{label} replay passed; cuts replayed/recorded", f"True {rep['cuts']}/{rep['cuts']}",
            f"{rep['passed']} {rep['replayed_cuts']}/{sum(ncuts(r) for r in recs)}")

    # ---- B2 funnel table
    want = {"c3:all": (436, 7, 316, 23, 9, 90, "20.4%"), "all-noaggr": (446, 7, 326, 6, 5, 107, "5.3%"),
            "c3:all-diag": (1618, 19, 1039, 202, 17, 358, "36.1%"),
            "all-diag-noaggr": (1572, 17, 1058, 47, 13, 450, "9.5%"),
            "all-diag-rowdir-noaggr": (1640, 19, 1124, 47, 13, 450, "9.5%")}
    for m, w in want.items():
        t, rb, causes, statuses = funnel(rows(IB, nb, m))
        got = (t["certification_calls"], t["certification_failures"], t["below_threshold"],
               t["row_binding_rejections"], rb, t["cuts"],
               f"{100 * t['row_binding_rejections'] / (t['row_binding_rejections'] + t['cuts']):.1f}%")
        chk(f"B2 funnel {m} (support, fail, below, binding, runs, cuts, share)", str(w), str(got))
    for m, w in [("all-noaggr", {"coefficient_rounded_to_integer": 4, "column_set_differs_tiny_coefficient_dropped": 1,
                                 "column_set_differs_variable_not_column": 1}),
                 ("all-diag-noaggr", {"coefficient_rounded_to_integer": 17,
                                      "column_set_differs_tiny_coefficient_dropped": 16,
                                      "column_set_differs_variable_not_column": 14}),
                 ("all-diag-rowdir-noaggr", {"coefficient_rounded_to_integer": 17,
                                             "column_set_differs_tiny_coefficient_dropped": 16,
                                             "column_set_differs_variable_not_column": 14})]:
        chk(f"B2 binding causes {m}", json.dumps(w, sort_keys=True),
            json.dumps(funnel(rows(IB, nb, m))[2], sort_keys=True))
    chk("B2 all-diag-noaggr rejected-row variable statuses", "{'FIXED': 17}",
        str(funnel(rows(IB, nb, "all-diag-noaggr"))[3]))
    chk("B2 all-noaggr rejected-row variable statuses", "{'FIXED': 1}", str(funnel(rows(IB, nb, "all-noaggr"))[3]))
    for m, w in [("all-noaggr", 52), ("all-diag-noaggr", 210), ("all-diag-rowdir-noaggr", 210)]:
        chk(f"B2 callbacks {m}", str(w), str(funnel(rows(IB, nb, m))[0]["calls"]))
    for m, w in [("all-noaggr", "cut 0 / support 8 / callback 10 / time 9 / none 4"),
                 ("all-diag-noaggr", "cut 0 / support 0 / callback 13 / time 0 / none 17"),
                 ("all-diag-rowdir-noaggr", "cut 0 / support 0 / callback 13 / time 0 / none 17")]:
        c = caps(rows(IB, nb, m))[0]
        chk(f"B2 caps (run counts) {m}", w, f"cut {c.get('cut_cap', 0)} / support {c.get('support_cap', 0)} / "
            f"callback {c.get('callback_cap', 0)} / time {c.get('time_budget', 0)} / none {c.get('none', 0)}")
    lim = sorted({r["config"]["max_rounds"] for r in rows(IB, nb, "all-noaggr")})
    chk("B2 all-noaggr callback cap value (digest: '10-callback cap')", "10", str(lim[0] if len(lim) == 1 else lim),
        "major", "Frozen Config max_rounds = 3 for modes all/auto/all-noaggr (record field config.max_rounds); "
        "10 is the all-diag/mechanism value. The run count (10) is right; the label is wrong.")
    # per-model binding/cuts
    for n, a, b in [("kall_circlespolygons_c1p12", "127/25", "0/104"), ("pooling_adhya4tp", "17/29", "17/29"),
                    ("bayes2_50", "17/8", "12/8"), ("bayes2_30", "3/0", "3/0"), ("pooling_rt2tp", "4/46", "4/46")]:
        x, y = IB[(n, "c3:all-diag")]["separation"], IB[(n, "all-diag-noaggr")]["separation"]
        chk(f"B2 {n} binding/cuts c3:all-diag -> all-diag-noaggr", f"{a} -> {b}",
            f"{x['row_binding_rejections']}/{x['cuts']} -> {y['row_binding_rejections']}/{y['cuts']}")
    for n, m, w in [("ex8_1_7", "all-noaggr", 7), ("ex8_1_7", "all-diag-noaggr", 9),
                    ("ex8_1_7", "all-diag-rowdir-noaggr", 11), ("tanksize", "all-diag-noaggr", 8),
                    ("tanksize", "all-diag-rowdir-noaggr", 8), ("ex8_1_7", "c3:all", 7),
                    ("tanksize", "c3:all-diag", 10), ("ex8_1_7", "c3:all-diag", 9)]:
        chk(f"B2 cert failures {n} {m}", str(w), str(IB[(n, m)]["separation"]["certification_failures"]))
    # bounds
    for m, ref, w4, w6 in [("all-noaggr", "baseline-noaggr", (3, 27, 0, 0), (4, 25, 1, 0)),
                           ("all-diag-noaggr", "baseline-noaggr", (6, 23, 1, 0), (6, 22, 2, 0)),
                           ("all-diag-rowdir-noaggr", "baseline-noaggr", (6, 23, 1, 0), (6, 22, 2, 0)),
                           ("baseline-noaggr", "c3:baseline", (0, 24, 6, 0), (0, 24, 6, 0)),
                           ("baseline-extra", "c3:baseline", (12, 17, 1, 0), (12, 17, 1, 0))]:
        chk(f"B2 root bound {m} vs {ref} 1e-4 (better, tie, worse, flagged)", str(w4),
            str(bc(IB, nb, m, ref, root_bound, 1e-4)))
        chk(f"B2 root bound {m} vs {ref} 1e-6", str(w6), str(bc(IB, nb, m, ref, root_bound, 1e-6)))
    for m, w in [("c3:all", 3), ("c3:all-diag", 4)]:
        b, t, wo, f = bc(IB, nb, m, "c3:baseline", root_bound, 1e-4)
        chk(f"B2 {m} vs c3:baseline 1e-4 better / worse", f"{w} / 0", f"{b} / {wo}")
    for n, m, ref, dg in [("sep1", "all-noaggr", "baseline-noaggr", "0.0448"),
                          ("ex3_1_4", "all-noaggr", "baseline-noaggr", "0.105"),
                          ("pointpack04", "all-noaggr", "baseline-noaggr", "0.0781"),
                          ("ex8_1_7", "all-noaggr", "baseline-noaggr", "2.8e-6"),
                          ("pooling_bental4tp", "all-diag-noaggr", "baseline-noaggr", "0.731"),
                          ("sep1", "all-diag-noaggr", "baseline-noaggr", "0.114"),
                          ("ex3_1_4", "all-diag-noaggr", "baseline-noaggr", "0.154"),
                          ("tanksize", "all-diag-noaggr", "baseline-noaggr", "0.00149"),
                          ("pooling_bental4pq", "all-diag-noaggr", "baseline-noaggr", "1.0"),
                          ("pointpack04", "all-diag-noaggr", "baseline-noaggr", "0.335"),
                          ("pooling_haverly1tp", "all-diag-noaggr", "baseline-noaggr", "-0.533"),
                          ("pooling_bental4tp", "baseline-extra", "c3:baseline", "1.0"),
                          ("wastewater04m2", "baseline-extra", "c3:baseline", "0.459"),
                          ("pooling_haverly2pq", "baseline-extra", "c3:baseline", "1.0"),
                          ("ex3_1_4", "baseline-extra", "c3:baseline", "1.0"),
                          ("pooling_adhya4tp", "baseline-extra", "c3:baseline", "0.957"),
                          ("tanksize", "baseline-extra", "c3:baseline", "0.00964"),
                          ("kall_congruentcircles_c32", "baseline-extra", "c3:baseline", "0.0763"),
                          ("ex8_1_7", "baseline-extra", "c3:baseline", "0.0123"),
                          ("pooling_bental4pq", "baseline-extra", "c3:baseline", "1.0"),
                          ("pooling_haverly3tp", "baseline-extra", "c3:baseline", "1.0"),
                          ("pooling_rt2tp", "baseline-extra", "c3:baseline", "0.523"),
                          ("pointpack04", "baseline-extra", "c3:baseline", "0.958"),
                          ("sep1", "baseline-extra", "c3:baseline", "-0.87")]:
        chk(f"B2 gap closed {n} {m} vs {ref}", dg, gap_closed(IB, n, m, ref, tb))
    for n, m, dg in [("sep1", "all-noaggr", "-523.8205"), ("sep1", "baseline-noaggr", "-524.4654"),
                     ("pointpack04", "all-noaggr", "1.151211"), ("pointpack04", "baseline-noaggr", "1.164013"),
                     ("ex8_1_7", "all-noaggr", "-5910.599"), ("prob06", "all-noaggr", "1.177099"),
                     ("prob06", "baseline-noaggr", "1.177121"), ("pooling_bental4tp", "all-diag-noaggr", "-462.7154"),
                     ("pooling_bental4tp", "baseline-noaggr", "-497.3265"), ("tanksize", "all-diag-noaggr", "0.8430595"),
                     ("pooling_haverly1tp", "all-diag-noaggr", "-422.2222"),
                     ("pooling_haverly1tp", "baseline-noaggr", "-414.4928"),
                     ("pooling_haverly2pq", "baseline-noaggr", "-857.1429"),
                     ("pooling_haverly2pq", "c3:baseline", "-617.7001"), ("pooling_haverly3tp", "c3:baseline", "-750.7937"),
                     ("wastewater04m2", "baseline-extra", "80.17429"), ("pooling_adhya4tp", "baseline-extra", "-881.9363"),
                     ("pooling_rt2tp", "baseline-extra", "-4933.627"), ("sep1", "baseline-extra", "-533.7662"),
                     ("ex8_1_7", "baseline-extra", "-5837.857"), ("pointpack04", "baseline-extra", "1.006909")]:
        chk(f"B2 root bound value {n} {m}", dg, root_bound(IB[(n, m)]), "minor", "last displayed digit differs from the recorded value (rounding slip); immaterial")
    chk("B2 rowdir-noaggr root bounds identical to all-diag-noaggr (models differing)", "[]",
        str([n for n in nb if root_bound(IB[(n, "all-diag-rowdir-noaggr")]) != root_bound(IB[(n, "all-diag-noaggr")])]))
    for m in ["all-noaggr", "all-diag-noaggr", "all-diag-rowdir-noaggr", "baseline-extra"]:
        ref = "c3:baseline" if m == "baseline-extra" else "baseline-noaggr"
        v = [x for x in (gap_closed(IB, n, m, ref, tb) for n in nb) if x is not None]
        chk(f"B2 median root gap closed {m} (count)", "0 (29)", f"{statistics.median(v):.3g} ({len(v)})",
            "minor", "baseline-extra median is 3.27e-12 (S partB2 structure/root root_gap_closed_median "
            "baseline-extra), not 0; immaterial.", exact=(statistics.median(v) == 0 and len(v) == 29))
    chk("B2 reason for 29 (models without a reference)", "1 model without a reference",
        str([n for n in nb if tb[n] is None]), "minor",
        "All 30 B2 cases have reference_primal. nvs02 is excluded because its reference root bound "
        "(5.96418452307, solved at the root) already reaches the target 5.964184523 (no gap).")
    for m, w in [("c3:baseline", 8), ("baseline-noaggr", 7), ("baseline-extra", 13)]:
        chk(f"B2 solved at the root {m}", str(w), str(sum(map(solved, rows(IB, nb, m)))))
    chk("B2 no incumbent (all five B2 modes)", "['wastewater04m2']",
        str(sorted({r["name"] for m in ["baseline-noaggr", "all-noaggr", "all-diag-noaggr", "all-diag-rowdir-noaggr",
                                        "baseline-extra"] for r in rows(IB, nb, m) if not has_incumbent(r)})))
    # native
    nat = native(rows(IB, nb, "baseline-extra"), "baseline-extra (check)")
    chk("B2 extra interminor runs/calls/found/applied", "21/939/429680/1985",
        f"{nat['interminor']['runs']}/{nat['interminor']['Calls']}/{nat['interminor']['FoundCuts']}/{nat['interminor']['Applied']}")
    chk("B2 extra intersection runs/enforce/cuts", "26/24141/6829",
        f"{nat['quadratic']['runs_with_cuts']}/{nat['quadratic']['#Enforce']}/{nat['quadratic']['Cuts']}")
    chk("B2 extra RLT", "27/229/208/9", f"{nat['rlt']['runs']}/{nat['rlt']['Calls']}/{nat['rlt']['FoundCuts']}/{nat['rlt']['Applied']}")
    chk("B2 extra minor", "4/145/320/110",
        f"{nat['minor']['runs']}/{nat['minor']['Calls']}/{nat['minor']['FoundCuts']}/{nat['minor']['Applied']}")
    chk("B2 extra eccuts runs", "0", str(nat["eccuts"]["runs"]))
    nat0 = native(rows(IB, nb, "baseline-noaggr"), "baseline-noaggr (check)")
    chk("B2 baseline-noaggr interminor/intersection/minor/RLT", "0 / 0 / 4/54/71/36 / 27/164/129/5",
        f"{nat0['interminor']['runs']} / {nat0['quadratic']['Cuts']} / {nat0['minor']['runs']}/{nat0['minor']['Calls']}/"
        f"{nat0['minor']['FoundCuts']}/{nat0['minor']['Applied']} / {nat0['rlt']['runs']}/{nat0['rlt']['Calls']}/"
        f"{nat0['rlt']['FoundCuts']}/{nat0['rlt']['Applied']}")
    # time decomposition B2
    for m, w in [("all-noaggr", ("30", "0.6493", "0.1461", "0.4772", "0.1949", "0.1511", "0.997", "3.91")),
                 ("all-diag-noaggr", ("30", "1.184", "0.1494", "1.023", "0.1949", "0.1511", "1.005", "7.28")),
                 ("all-diag-rowdir-noaggr", ("30", "1.240", "0.1465", "1.082", "0.1949", "0.1511", "0.958", "7.51"))]:
        o = time_decomp(IB, nb, m, "baseline-noaggr", "root")
        vals = (o["pairs"], o["sgm_total"], o["sgm_excl"], o["sgm_cb"], o["ref_sgm_total"], o["ref_sgm_scip"],
                o["median_excl_over_ref_scip"], o["median_total_over_ref"])
        for k, (dg, v) in enumerate(zip(w, vals)):
            chk(f"B2 time {m} field {['pairs', 'sgm_total', 'sgm_excl', 'sgm_cb', 'ref_total', 'ref_scip', 'med_excl', 'med_total'][k]}",
                dg, v)
    chk("B2 baseline-extra median total ratio vs c3:baseline", "1.289",
        time_decomp(IB, nb, "baseline-extra", "c3:baseline", "root")["median_total_over_ref"])
    chk("B2 c3: load_start mean", "16.3",
        statistics.fmean(r["load_start"][0] for m in ["c3:baseline", "c3:all", "c3:auto", "c3:all-diag"]
                         for r in rows(IB, nb, m)), "minor",
        "mean load_start[0] of the 120 campaign-3 Part B root runs is 16.35 (rounds to 16.4); immaterial")

    # ---- D root
    for m, mc, cu, w in [("all", 2, 14, (0, 19, 1, 0)), ("all-diag", 13, 891, (1, 14, 5, 0)),
                         ("all-diag-rowdir", 13, 831, (1, 14, 5, 0)), ("baseline-extra", 0, 0, (8, 8, 3, 1))]:
        rr = rows(R, nd, m)
        chk(f"D root {m} models with cuts / cuts", f"{mc} / {cu}", f"{sum(ncuts(r) > 0 for r in rr)} / {sum(map(ncuts, rr))}")
        chk(f"D root {m} vs baseline 1e-4 (better, tie, worse, flagged)", str(w), str(bc(R, nd, m, "baseline", root_bound, 1e-4)))
    for m, w in [("all", ("0", "-0.00323", "0")), ("all-diag", ("0", "-0.0306", "0.0389")),
                 ("all-diag-rowdir", ("0", "-0.0306", "0.0389")), ("baseline-extra", ("0", "-0.243", "0.344"))]:
        v = [x for x in (gap_closed(R, n, m, "baseline", td_) for n in nd) if x is not None]
        chk(f"D root {m} gap closed count", "19", len(v))
        chk(f"D root {m} gap closed median", w[0], statistics.median(v))
        chk(f"D root {m} gap closed min", w[1], min(v))
        chk(f"D root {m} gap closed max", w[2], max(v))
    chk("D root models without reference_primal", "['mpbp_31']", str([n for n in nd if td_[n] is None]))
    for n, m, dg in [("multiplants_mtg1c", "all-diag", "0.0389"), ("multiplants_mtg1a", "all-diag", "-0.0306"),
                     ("hydroenergy2", "all-diag", "-0.0247"), ("hydroenergy2", "all-diag-rowdir", "-0.0132"),
                     ("kriging_peaks-full100", "all-diag", "-0.00323"), ("crudeoil_li03", "all-diag", "-0.00523"),
                     ("blend718", "all-diag", "-0.00026"), ("blend480", "baseline-extra", "0.0759"),
                     ("pooling_sppa0stp", "baseline-extra", "0.148"), ("camshape100", "baseline-extra", "0.344"),
                     ("kriging_peaks-full100", "baseline-extra", "0.164"), ("multiplants_mtg1c", "baseline-extra", "0.0300"),
                     ("blend718", "baseline-extra", "0.00144"), ("pooling_sppa0pq", "baseline-extra", "0.250"),
                     ("multiplants_mtg6", "baseline-extra", "0.000538"), ("multiplants_mtg1a", "baseline-extra", "-0.0125"),
                     ("hydroenergy2", "baseline-extra", "-0.0132"), ("crudeoil_li03", "baseline-extra", "-0.00754"),
                     ("waternd2", "baseline-extra", "-0.243")]:
        chk(f"D root gap closed {n} {m}", dg, gap_closed(R, n, m, "baseline", td_))
    for n, m, dg in [("kriging_peaks-full100", "all", "-335.418"), ("kriging_peaks-full100", "baseline", "-334.346"),
                     ("multiplants_mtg1c", "all-diag", "8573.751"), ("multiplants_mtg1c", "baseline", "8893.211"),
                     ("multiplants_mtg1a", "all-diag", "1823.402"), ("multiplants_mtg1a", "baseline", "1780.952"),
                     ("hydroenergy2", "all-diag", "379795.09"), ("hydroenergy2", "baseline", "379602.42"),
                     ("hydroenergy2", "all-diag-rowdir", "379704.95"), ("crudeoil_li03", "all-diag", "3577.653"),
                     ("crudeoil_li03", "baseline", "3577.182"), ("blend718", "all-diag", "20.69113"),
                     ("blend718", "baseline", "20.68767"), ("multiplants_mtg6", "all-diag", "6870.1466"),
                     ("multiplants_mtg6", "baseline", "6870.1214"), ("blend480", "baseline-extra", "10.67717"),
                     ("blend480", "baseline", "10.79625"), ("pooling_sppa0stp", "baseline-extra", "-37232.28"),
                     ("pooling_sppa0stp", "baseline", "-37479.54"), ("camshape100", "baseline-extra", "-4.771519"),
                     ("camshape100", "baseline", "-5.027017"), ("kriging_peaks-full100", "baseline-extra", "-279.8305"),
                     ("multiplants_mtg1c", "baseline-extra", "8647.275"), ("blend718", "baseline-extra", "20.66851"),
                     ("pooling_sppa0pq", "baseline-extra", "-37288.49"), ("pooling_sppa0pq", "baseline", "-37780.20"),
                     ("multiplants_mtg6", "baseline-extra", "6869.284"), ("multiplants_mtg1a", "baseline-extra", "1798.335"),
                     ("hydroenergy2", "baseline-extra", "379704.87"), ("crudeoil_li03", "baseline-extra", "3577.861")]:
        chk(f"D root bound value {n} {m}", dg, root_bound(R[(n, m)]), "minor", "last displayed digit differs from the recorded value (rounding slip); immaterial")
    chk("D root all-diag 1e-6 worse adds multiplants_mtg6",
        "(1, 13, 6, 0)", str(bc(R, nd, "all-diag", "baseline", root_bound, 1e-6)))
    chk("D root all-diag cuts per model", "tc05a 200, tc02b 200, c1p5b 143, hydroenergy2 133, sppa0stp 54, sppa0pq 42, "
        "mtg6 40, c6r1 36, li03 31, mtg1a 4, mtg1c 4, kriging 3, blend718 1",
        ", ".join(str(ncuts(R[(n, "all-diag")])) for n in [
            "kall_ellipsoids_tc05a", "kall_ellipsoids_tc02b", "kall_circlespolygons_c1p5b", "hydroenergy2",
            "pooling_sppa0stp", "pooling_sppa0pq", "multiplants_mtg6", "kall_circlesrectangles_c6r1", "crudeoil_li03",
            "multiplants_mtg1a", "multiplants_mtg1c", "kriging_peaks-full100", "blend718"]),
        exact=[ncuts(R[(n, "all-diag")]) for n in [
            "kall_ellipsoids_tc05a", "kall_ellipsoids_tc02b", "kall_circlespolygons_c1p5b", "hydroenergy2",
            "pooling_sppa0stp", "pooling_sppa0pq", "multiplants_mtg6", "kall_circlesrectangles_c6r1", "crudeoil_li03",
            "multiplants_mtg1a", "multiplants_mtg1c", "kriging_peaks-full100", "blend718"]]
        == [200, 200, 143, 133, 54, 42, 40, 36, 31, 4, 4, 3, 1])
    for m, w in [("all", (22, 176, 2, 149, 11, 3, 14)), ("all-diag", (115, 6352, 313, 5042, 106, 8, 891)),
                 ("all-diag-rowdir", (107, 6378, 313, 5128, 106, 8, 831))]:
        t, rb, causes, statuses = funnel(rows(R, nd, m))
        chk(f"D root funnel {m} (callbacks, support, fail, below, binding, runs, cuts)", str(w),
            str((t["calls"], t["certification_calls"], t["certification_failures"], t["below_threshold"],
                 t["row_binding_rejections"], rb, t["cuts"])))
    for m, w in [("all", (18.4, 15.7, 0.4, 1.8)), ("all-diag", (188.4, 53.6, 22.8, 69.8)),
                 ("all-diag-rowdir", (190.8, 53.1, 20.8, 73.1))]:
        t = funnel(rows(R, nd, m))[0]
        for k, dg in zip(("callback_seconds", "discovery_seconds", "candidate_seconds", "certification_seconds"), w):
            chk(f"D root {m} sum {k}", str(dg), t[k])
    chk("D root all-diag causes / statuses",
        "{'column_set_differs_variable_not_column': 99, 'coefficient_rounded_to_integer': 7} {'FIXED': 109, 'AGGREGATED': 85}",
        f"{funnel(rows(R, nd, 'all-diag'))[2]} {funnel(rows(R, nd, 'all-diag'))[3]}",
        exact=funnel(rows(R, nd, "all-diag"))[2] == {"column_set_differs_variable_not_column": 99,
                                                     "coefficient_rounded_to_integer": 7}
        and funnel(rows(R, nd, "all-diag"))[3] == {"FIXED": 109, "AGGREGATED": 85})
    chk("D root all binding per model (mtg1c, blend718, c6r1)", "3, 5, 3",
        ", ".join(str(R[(n, "all")]["separation"]["row_binding_rejections"])
                  for n in ["multiplants_mtg1c", "blend718", "kall_circlesrectangles_c6r1"]))
    chk("D root all-diag cert failures (kriging, tc05a, tc02b)", "307, 3, 3",
        ", ".join(str(R[(n, "all-diag")]["separation"]["certification_failures"])
                  for n in ["kriging_peaks-full100", "kall_ellipsoids_tc05a", "kall_ellipsoids_tc02b"]))
    stopped = [n for n in nd if R[(n, "all")]["separation"]["discovery_incomplete"]]
    disc = {json.loads(l)["name"]: json.loads(l).get("discovery_seconds") for l in SCAN.read_text().splitlines() if l.strip()}
    chk("D root all discovery stopped (count)", "12", len(stopped))
    chk("D root all stopped set == scan discovery > 1 s", "True", str(set(stopped) == {n for n in nd if (disc.get(n) or 0) > 1.0}))
    chk("D root scan discovery range on stopped models", "1.01-7.70",
        f"{min(disc[n] for n in stopped):.2f}-{max(disc[n] for n in stopped):.2f}")
    chk("D root stopped runs: support calls all 0, callback ~1.0 s", "True",
        str(all(R[(n, "all")]["separation"]["certification_calls"] == 0 and 0.99 < cb(R[(n, "all")]) < 1.01
                for n in stopped)))
    done = [n for n in nd if n not in stopped]
    chk("D root all: completed discovery / with cuts / support calls of the rest", "8 / 2 / 21-24",
        f"{len(done)} / {sum(ncuts(R[(n, 'all')]) > 0 for n in done)} / "
        f"{min(R[(n, 'all')]['separation']['certification_calls'] for n in done if not ncuts(R[(n, 'all')]))}-"
        f"{max(R[(n, 'all')]['separation']['certification_calls'] for n in done if not ncuts(R[(n, 'all')]))}")
    for m, w in [("all", "cut 0 / support 6 / callback 1 / time 14 / disc 12"),
                 ("all-diag", "cut 2 / support 8 / callback 8 / time 0 / none 2"),
                 ("all-diag-rowdir", "cut 2 / support 9 / callback 7 / time 0 / none 2")]:
        c = caps(rows(R, nd, m))[0]
        last = f"disc {c.get('discovery_stopped', 0)}" if m == "all" else f"none {c.get('none', 0)}"
        chk(f"D root caps (run counts) {m}", w, f"cut {c.get('cut_cap', 0)} / support {c.get('support_cap', 0)} / "
            f"callback {c.get('callback_cap', 0)} / time {c.get('time_budget', 0)} / {last}")
    lim = sorted({r["config"]["max_rounds"] for r in rows(R, nd, "all")})
    chk("D root mode all callback cap value (digest: '10-callback cap in 1')", "10", str(lim[0]), "major",
        "Mode all uses the frozen max_rounds = 3 (record config.max_rounds); the one run is kall_ellipsoids_tc02b "
        "with 3 callbacks. Same label error in the funnel table rows for D root all, D full all and auto, and B2 all-noaggr.")
    for m, w in [("all", ("20", "11.09", "9.084", "0.911", "10.07", "9.22", "0.995", "1.106")),
                 ("all-diag", ("20", "17.76", "8.572", "6.838", "10.07", "9.22", "0.996", "2.134")),
                 ("all-diag-rowdir", ("20", "17.92", "8.614", "6.940", "10.07", "9.22", "0.987", "2.161"))]:
        o = time_decomp(R, nd, m, "baseline", "root")
        vals = (o["pairs"], o["sgm_total"], o["sgm_excl"], o["sgm_cb"], o["ref_sgm_total"], o["ref_sgm_scip"],
                o["median_excl_over_ref_scip"], o["median_total_over_ref"])
        for k, (dg, v) in enumerate(zip(w, vals)):
            chk(f"D root time {m} field {['pairs', 'sgm_total', 'sgm_excl', 'sgm_cb', 'ref_total', 'ref_scip', 'med_excl', 'med_total'][k]}",
                dg, v)
    chk("D root baseline-extra median total ratio", "1.396",
        time_decomp(R, nd, "baseline-extra", "baseline", "root")["median_total_over_ref"])
    w = R[("waternd2", "baseline-extra")]
    chk("D root waternd2 extra primal / recomputed / discrepancy / violation",
        "3084095.92 / 2297367.49 / 0.342 / 3.4e-11",
        f"{w['primal']:.2f} / {w['primal_check']['objective']:.2f} / "
        f"{w['primal_check']['relative_objective_discrepancy']:.3f} / {w['primal_check']['max_scaled_violation']:.1e}")
    tl = sorted((r["name"], r["mode"]) for m in ["baseline", "all", "all-diag", "all-diag-rowdir", "baseline-extra"]
                for r in rows(R, nd, m) if r["status"] == "timelimit")
    chk("D root timelimit runs", "tc05a baseline/all/extra; ringpack_20_2 extra; c1p5b extra", str(tl),
        exact=tl == sorted([("kall_ellipsoids_tc05a", "baseline"), ("kall_ellipsoids_tc05a", "all"),
                            ("kall_ellipsoids_tc05a", "baseline-extra"), ("ringpack_20_2", "baseline-extra"),
                            ("kall_circlespolygons_c1p5b", "baseline-extra")]))
    chk("D root max charged time (c1p5b extra)", "124.49", secs(R[("kall_circlespolygons_c1p5b", "baseline-extra")]))
    noinc = sorted({r["name"] for m in ["baseline", "all", "all-diag", "all-diag-rowdir", "baseline-extra"]
                    for r in rows(R, nd, m) if not has_incumbent(r)})
    cnt = sum(not has_incumbent(r) for m in ["baseline", "all", "all-diag", "all-diag-rowdir", "baseline-extra"]
              for r in rows(R, nd, m))
    chk("D root runs without incumbent", "blend480, crudeoil_li03, kall_ellipsoids_tc05a (15 runs)",
        f"{', '.join(noinc)} ({cnt} runs)")
    chk("D root other primal check failures (besides waternd2 extra)", "0",
        str(sum(flagged(r) for m in ["baseline", "all", "all-diag", "all-diag-rowdir", "baseline-extra"]
                for r in rows(R, nd, m)) - 1))
    chk("D root rowdir vs all-diag: models with different root bound / cuts", "hydroenergy2 / hydroenergy2 (73 vs 133)",
        f"{[n for n in nd if root_bound(R[(n, 'all-diag')]) != root_bound(R[(n, 'all-diag-rowdir')])]} / "
        f"{[(n, ncuts(R[(n, 'all-diag-rowdir')]), ncuts(R[(n, 'all-diag')])) for n in nd if ncuts(R[(n, 'all-diag')]) != ncuts(R[(n, 'all-diag-rowdir')])]}",
        exact=[n for n in nd if root_bound(R[(n, "all-diag")]) != root_bound(R[(n, "all-diag-rowdir")])] == ["hydroenergy2"])

    # ---- D full
    for m, w in [("baseline", "2 [blend480 optimal, kriging_peaks-full100 gaplimit]"), ("all", "2 same"),
                 ("auto", "2 same"), ("baseline-extra", "1 [blend480]")]:
        s = [(r["name"], r["status"]) for r in rows(F, nd, m) if solved(r)]
        exp = ([("blend480", "optimal")] if m == "baseline-extra"
               else [("blend480", "optimal"), ("kriging_peaks-full100", "gaplimit")])
        chk(f"D full solved {m}", w, str(s), exact=sorted(s) == exp)
    for m, w in [("all", (5, 14, 1, 0)), ("auto", (4, 16, 0, 0)), ("baseline-extra", (7, 6, 7, 0))]:
        chk(f"D full final dual {m} vs baseline 1e-4", str(w), str(bc(F, nd, m, "baseline", dual, 1e-4)))
    for n, m, dg in [("camshape100", "all", "-4.573527"), ("camshape100", "baseline", "-4.574352"),
                     ("multiplants_mtg1c", "all", "6586.358"), ("multiplants_mtg1c", "baseline", "6602.980"),
                     ("blend718", "all", "10.39616"), ("blend718", "baseline", "10.56384"),
                     ("sonet23v4", "all", "-39618.46"), ("sonet23v4", "baseline", "-39633.63"),
                     ("crudeoil_li03", "all", "3560.264"), ("crudeoil_li03", "baseline", "3560.880"),
                     ("multiplants_mtg1a", "all", "859.0551"), ("multiplants_mtg1a", "baseline", "856.8424"),
                     ("multiplants_mtg1a", "auto", "852.1695"), ("blend718", "auto", "10.35299"),
                     ("kall_circlesrectangles_c6r1", "baseline-extra", "0"),
                     ("kall_circlesrectangles_c6r1", "baseline", "0.7848")]:
        chk(f"D full dual {n} {m}", dg, F[(n, m)]["dual"], "minor", "last displayed digit differs from the recorded value (rounding slip); immaterial")
    ex = {n: outcome(F[(n, "baseline-extra")], F[(n, "baseline")], F[(n, "baseline-extra")]["dual"],
                     F[(n, "baseline")]["dual"], 1e-4)[0] for n in nd}
    chk("D full extra better set", "pooling_sppa0stp, camshape100, hydroenergy2, blend718, pooling_sppa0pq, sonet23v4, crudeoil_li03",
        str(sorted(n for n in nd if ex[n] == "better")),
        exact=sorted(n for n in nd if ex[n] == "better") == sorted(
            ["pooling_sppa0stp", "camshape100", "hydroenergy2", "blend718", "pooling_sppa0pq", "sonet23v4", "crudeoil_li03"]))
    chk("D full extra worse set", "multiplants_mtg1a, mpbp_31, waternd2, kriging_peaks-full100, multiplants_mtg1c, "
        "kall_circlesrectangles_c6r1, multiplants_mtg6", str(sorted(n for n in nd if ex[n] == "worse")),
        exact=sorted(n for n in nd if ex[n] == "worse") == sorted(
            ["multiplants_mtg1a", "mpbp_31", "waternd2", "kriging_peaks-full100", "multiplants_mtg1c",
             "kall_circlesrectangles_c6r1", "multiplants_mtg6"]))
    for m in ["all", "auto"]:
        withcuts = {n: ncuts(F[(n, m)]) for n in nd if ncuts(F[(n, m)])}
        chk(f"D full {m} cuts per model", "{'kall_ellipsoids_tc02b': 11, 'kriging_peaks-full100': 3}", str(withcuts))
        diffs = [n for n in nd if outcome(F[(n, m)], F[(n, "baseline")], F[(n, m)]["dual"], F[(n, "baseline")]["dual"],
                                          1e-4)[0] != "tie"]
        chk(f"D full {m}: 1e-4 differences on models with cuts", "[]", str([n for n in diffs if ncuts(F[(n, m)])]))
    common = [n for n in nd if all(solved(F[(n, m)]) for m in ["baseline", "all", "auto", "baseline-extra"])]
    chk("D full solved by all four", "['blend480']", str(common))
    for m, w in [("baseline", ("63.36", None, None)), ("all", ("63.70", "62.28", "1.0")),
                 ("auto", ("62.62", "61.14", "1.0")), ("baseline-extra", ("49.54", None, None))]:
        A = [F[(n, m)] for n in common]
        chk(f"D full SGM common {m}", w[0], sgm([secs(a) for a in A]))
        if w[1]:
            chk(f"D full SGM common {m} SCIP excl", w[1], sgm([scip_excl(a) for a in A]))
            chk(f"D full SGM common {m} callback", w[2], sgm([cb(a) for a in A]))
    for m, w in [("baseline", ("275.8", None)), ("all", ("276.4", "274.3")), ("auto", ("276.2", "274.1")),
                 ("baseline-extra", ("274.5", None))]:
        A = rows(F, nd, m)
        chk(f"D full SGM all 20 {m}", w[0], sgm([secs(a) for a in A]))
        if w[1]:
            chk(f"D full SGM all 20 {m} SCIP excl", w[1], sgm([scip_excl(a) for a in A]))
            chk(f"D full summed callback {m}", "18.8", sum(cb(a) for a in A))
    for m, w in [("all", (22, 180, 2, 153, 11, 3, 14)), ("auto", (24, 170, 0, 145, 11, 3, 14))]:
        t, rb, causes, statuses = funnel(rows(F, nd, m))
        chk(f"D full funnel {m} (callbacks, support, fail, below, binding, runs, cuts)", str(w),
            str((t["calls"], t["certification_calls"], t["certification_failures"], t["below_threshold"],
                 t["row_binding_rejections"], rb, t["cuts"])))
    for m, w in [("all", "cut 0 / support 6 / callback 1 / time 14 / disc 11"),
                 ("auto", "cut 0 / support 4 / callback 2 / time 15 / disc 11")]:
        c = caps(rows(F, nd, m))[0]
        chk(f"D full caps (run counts) {m}", w, f"cut {c.get('cut_cap', 0)} / support {c.get('support_cap', 0)} / "
            f"callback {c.get('callback_cap', 0)} / time {c.get('time_budget', 0)} / disc {c.get('discovery_stopped', 0)}")
    rs = {n for n in nd if R[(n, "all")]["separation"]["discovery_incomplete"]}
    for m in ["all", "auto"]:
        fs = {n for n in nd if F[(n, m)]["separation"]["discovery_incomplete"]}
        chk(f"D full {m} discovery stopped: root set minus full set", "['multiplants_mtg6'] (11 stopped)",
            f"{sorted(rs - fs)} ({len(fs)} stopped)", exact=(sorted(rs - fs) == ["multiplants_mtg6"] and len(fs) == 11
                                                             and not (fs - rs)))
    # time decomposition D full: digest uses the single all-four common run (blend480)
    for m, w in [("all", ("63.70", "62.28", "1.0", "63.36", "62.91", "0.990", "1.005")),
                 ("auto", ("62.62", "61.14", "1.0", "63.36", "62.91", "0.972", "0.988"))]:
        a, b = F[("blend480", m)], F[("blend480", "baseline")]
        vals = (secs(a), scip_excl(a), cb(a), secs(b), scip_secs(b), scip_excl(a) / scip_secs(b), secs(a) / secs(b))
        for k, (dg, v) in enumerate(zip(w, vals)):
            chk(f"D full time {m} (blend480 only) field {['total', 'excl', 'cb', 'ref_total', 'ref_scip', 'ratio_excl', 'ratio_total'][k]}",
                dg, v)
        o = time_decomp(F, nd, m, "baseline", "full")
        chk(f"D full time {m}: pairs solved by both mode and baseline (digest header definition)", "1 (blend480)",
            o["pairs"], "minor",
            "The digest's time-decomposition header defines pairs as runs solved by both the mode and its reference; "
            "for D full that is 2 pairs (blend480, kriging_peaks-full100), giving median total ratio "
            f"{o['median_total_over_ref']:.3f} and median SCIP-excl ratio {o['median_excl_over_ref_scip']:.3f} "
            "(S partD-full larger/full times.ratio_summary: count 2). The digest row uses blend480 only.")
    tl = [secs(r) for m in ["baseline", "all", "auto", "baseline-extra"] for r in rows(F, nd, m) if r["status"] == "timelimit"]
    chk("D full timelimit runs / overshoots", "73 / 73", f"{len(tl)} / "
        f"{sum(secs(r) > r['time_limit'] + 0.01 for m in ['baseline', 'all', 'auto', 'baseline-extra'] for r in rows(F, nd, m))}")
    chk("D full largest charged time (kriging extra)", "300.36", secs(F[("kriging_peaks-full100", "baseline-extra")]))
    chk("D full charged range of timelimit runs", "300.19-300.36", f"{min(tl):.2f}-{max(tl):.2f}", "minor",
        "D full timelimit runs were charged 300.21-300.36 s; the digest's 300.19 lower end comes from other parts "
        "(C2/C3, not checked here).", exact=(min(tl) >= 300.185 and max(tl) < 300.365))
    tc = [(m, F[("kall_ellipsoids_tc05a", m)]["nodes"]) for m in ["baseline", "all", "auto"]]
    chk("D full kall_ellipsoids_tc05a nodes (baseline, all, auto) and incumbent", "1, 1, 1; no incumbent",
        f"{tc}; incumbent {[has_incumbent(F[('kall_ellipsoids_tc05a', m)]) for m in ['baseline', 'all', 'auto', 'baseline-extra']]}",
        exact=all(x[1] == 1 for x in tc) and not any(has_incumbent(F[("kall_ellipsoids_tc05a", m)])
                                                      for m in ["baseline", "all", "auto", "baseline-extra"]))
    loads = {f"{p} {m}": statistics.fmean(r["load_start"][0] for r in rows(I, nd if p != "B2" else nb, m))
             for p, I, ms in [("B2", IB, ["baseline-noaggr", "all-noaggr", "all-diag-noaggr", "all-diag-rowdir-noaggr",
                                         "baseline-extra"]),
                              ("Droot", R, ["baseline", "all", "all-diag", "all-diag-rowdir", "baseline-extra"]),
                              ("Dfull", F, ["baseline", "all", "auto", "baseline-extra"])] for m in ms}
    chk("Campaign-4 load_start mean range (B2, D) within digest's 3.5-7.7", "3.5-7.7",
        f"{min(loads.values()):.2f}-{max(loads.values()):.2f}",
        exact=min(loads.values()) >= 3.45 and max(loads.values()) <= 7.75)

    section("Comparison with the digest")
    for c in CHECKS:
        if not c["match"]:
            print(f"  MISMATCH [{c['severity']}] {c['item']}: digest {c['digest_value']} | recomputed "
                  f"{c['recomputed_value']} | {c['reason']}")
    print(f"  checks run {len(CHECKS)}, matching {sum(c['match'] for c in CHECKS)}")
    return CHECKS


if __name__ == "__main__":
    for name, d in [("B2", RUNS / "partB2"), ("D root", RUNS / "partD-root"), ("D full", RUNS / "partD-full"),
                    ("v3 partB", V3B)]:
        coverage(name, d)
    part_b2()
    part_d()
    checks = compare_with_digest()
    if len(sys.argv) > 2 and sys.argv[1] == "--json":
        Path(sys.argv[2]).write_text(json.dumps(checks, indent=1))
