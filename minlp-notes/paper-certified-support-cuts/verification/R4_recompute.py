#!/usr/bin/env python3
"""R4-numbers: independent recomputation of the numbers stated in Section 9,
the abstract, the introduction and Appendix B of the manuscript
paper-certified-support-cuts/main.tex, from the raw campaign records.

Standard library only. Does not import any producer code (summarize*.py,
analyze*.py, solver). Definitions are re-implemented from the wording of
Section 9.1 and of the frozen protocols:

  solved   status optimal or gaplimit, worker exited normally, finite primal,
           and primal_check.checked and primal_check.passed are true;
  time     several variants are computed; the one charged to the soft
           budget in v3 is total_seconds + preparation_seconds, in v1/v2
           total_seconds + source_read_seconds;
  SGM      shifted geometric mean, shift 1 s;
  bounds   a better than b if sign*(a-b) > rtol*max(1,|a|,|b|).

Usage:  python R4_recompute.py            (prints a check table and details)
Single-threaded, streaming JSON reader (Part C records are large).
"""
from __future__ import annotations

from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[2])

import collections
import hashlib
import json
import math
import statistics
import sys
from pathlib import Path

ROOT = Path((_PUBLIC_REPO))
PAPER = ROOT / "paper-certified-support-cuts"
EXP = PAPER / "experiments"
V1 = ROOT / "research-20261002-convexification/experiments/campaign-v1"
V2 = ROOT / "research-20261003-convexification/experiments/campaign-v2"
REP = ROOT / "research-20261003-convexification/experiments/repair-discovery-v1"
HOLDOUT2 = ROOT / "research-20261003-convexification/experiments/holdout-selection.json"
V3 = EXP / "v3/runs"
V3D = EXP / "v3d/runs"
SCAN = EXP / "v3/scan"

DROP = ("original_model", "model_metadata", "original_values", "config")
FAIL = ("process_timeout", "worker_error", "worker_no_output", "worker_output_parse_error")

ROWS = []          # (id, where, stated, computed, ok)
DETAILS = []


def check(cid, where, stated, computed, ok=None):
    if ok is None:
        ok = stated == computed
    ROWS.append((cid, where, stated, computed, "PASS" if ok else "MISMATCH"))


def note(*a):
    DETAILS.append(" ".join(str(x) for x in a))


def close(stated, value, digits):
    """stated (a decimal string or number) equals value rounded to `digits` decimals."""
    return value is not None and abs(round(value, digits) - float(stated)) < 0.5 * 10 ** (-digits) + 1e-12


def load(path, keep_config=False):
    out = []
    with open(path) as f:
        for line in f:
            r = json.loads(line)
            cuts = r.get("cuts")
            r["_ncuts"] = len(cuts) if isinstance(cuts, list) else None
            r["_methods"] = collections.Counter(
                ((c.get("support_witness") or {}).get("method") or c.get("method") or "?")
                for c in cuts) if isinstance(cuts, list) else None
            r.pop("cuts", None)
            for k in DROP:
                if k == "config" and keep_config:
                    continue
                r.pop(k, None)
            out.append(r)
    return out


def failed(r):
    return r.get("status") in FAIL or r.get("returncode", 0) not in (0, None)


def finite(x):
    return isinstance(x, (int, float)) and math.isfinite(x)


def solved(r):
    pc = r.get("primal_check") or {}
    return (r is not None and not failed(r) and r.get("status") in ("optimal", "gaplimit")
            and finite(r.get("primal")) and pc.get("checked", True) is True and pc.get("passed") is True)


def t_total(r):
    return r["total_seconds"]


def t_read(r):
    return r["total_seconds"] + r.get("source_read_seconds", 0.0)


def t_prep(r):
    return r["total_seconds"] + r.get("preparation_seconds", 0.0)


def t_outer(r):
    return r["outer_wall_seconds"]


def sgm(vals, shift=1.0):
    vals = list(vals)
    if not vals:
        return None
    return math.exp(statistics.fmean(math.log(v + shift) for v in vals)) - shift


def compare(a, b, key, rtol):
    if a is None or b is None or failed(a) or failed(b) or not finite(a.get(key)) or not finite(b.get(key)):
        return "unavailable"
    sign = 1 if a.get("sense", "min") == "min" else -1
    imp = sign * (a[key] - b[key])
    tol = rtol * max(1.0, abs(a[key]), abs(b[key]))
    return "better" if imp > tol else "worse" if imp < -tol else "tie"


def allowance(r):
    # min(max_separation_seconds, fraction * (time_limit - preparation)); frozen v2/v3 defaults
    prep = r.get("preparation_seconds", 0.0) or 0.0
    return min(1.0, 0.05 * (r["time_limit"] - prep))


def sep(r, key):
    return ((r.get("separation") or {}).get(key) or 0.0)


def has_incumbent(r):
    return finite(r.get("primal"))


def inc_passed(r):
    return (r.get("primal_check") or {}).get("passed") is True


# --------------------------------------------------------------------------------------
# Campaign 1
# --------------------------------------------------------------------------------------
def campaign1():
    recs = load(V1 / "records.jsonl", keep_config=True)
    W = "Sec 9.2"
    check("C1.runs", W + " (total raw records)", 316, len(recs))
    hold = [r for r in recs if r["suite"] == "holdout" and r["phase"] == "full"]
    syn = [r for r in recs if r["suite"] == "synthetic" and r["phase"] == "full"]
    modes = ("baseline", "control", "all", "auto")
    names = sorted({r["name"] for r in hold})
    check("C1.models", W, 24, len(names))
    idx = {(r["name"], r["mode"]): r for r in hold}
    admitted = [n for n in names if all(idx[(n, m)]["status"] not in ("source_model_mismatch", "worker_error") for m in modes)]
    check("C1.admitted", W + " '20 passed the model import in every mode'", 20, len(admitted))
    mism = [n for n in names if all(idx[(n, m)]["status"] == "source_model_mismatch" for m in modes)]
    err = [n for n in names if all(idx[(n, m)]["status"] == "worker_error" for m in modes)]
    check("C1.domain_rejects", W + " 'three rejected (domain)'", 3, len(mism))
    check("C1.varpower", W + " 'one failed (variable power)'", 1, len(err))
    note("C1 domain rejects:", mism, "worker_error:", err)
    for m, st in zip(modes, (19, 19, 18, 18)):
        check(f"C1.solved.{m}", W + " solved of 20", st, sum(solved(idx[(n, m)]) for n in admitted))
    lost = [n for n in admitted if solved(idx[(n, "baseline")]) and not solved(idx[(n, "all")])]
    check("C1.lost", W + " lost model", "genpooling_lee2", ",".join(lost))
    common = [n for n in admitted if all(solved(idx[(n, m)]) for m in modes)]
    note("C1 models solved in every mode:", len(common))
    stated = {"baseline": "0.38", "control": "0.52", "all": "0.57", "auto": "0.46"}
    for tname, tf in (("total+read", t_read), ("total", t_total)):
        for m in modes:
            v = sgm(tf(idx[(n, m)]) for n in common)
            note(f"C1 SGM over {len(common)} common-solved, time={tname}, {m}: {v:.4f}")
    for m in modes:
        v = sgm(t_read(idx[(n, m)]) for n in common)
        check(f"C1.sgm.{m}", W + f" SGM on models solved in every mode ({len(common)})", stated[m], round(v, 3),
              close(stated[m], v, 2))
    # pairwise sets (what the audit computed)
    for m in modes:
        pair = [n for n in admitted if solved(idx[(n, m)]) and solved(idx[(n, "baseline")])]
        v = sgm(t_read(idx[(n, m)]) for n in pair)
        note(f"C1 SGM over models solved by {m} and baseline ({len(pair)}): {v:.4f}")
    sidx = {(r["name"], r["mode"]): r for r in syn}
    snames = sorted({r["name"] for r in syn})
    check("C1.mech.cases", W, 13, len(snames))
    for m, st in zip(modes, (12, 13, 13, 13)):
        check(f"C1.mech.solved.{m}", W, st, sum(solved(sidx[(n, m)]) for n in snames))
    ncuts = sum(r["_ncuts"] or 0 for r in recs)
    check("C1.cuts", W + " recorded cuts", 1082, ncuts)
    rp = json.load(open(V1 / "replay.json"))
    check("C1.replay", W + " cuts passed replay", 1082,
          rp.get("replayed_cuts", rp.get("cuts")) if rp.get("passed") else -1)
    inc = [r for r in recs if has_incumbent(r)]
    check("C1.incumbents", W + " returned incumbents (all phases)", 270, len(inc))
    check("C1.incumbents.passed", W, 270, sum(inc_passed(r) for r in inc))
    tl = sorted({r["time_limit"] for r in hold}), sorted({r["time_limit"] for r in recs if r["phase"] == "root"})
    check("C1.budgets", W + " six-second budget, two-second root", "[6.0] / [2.0]", f"{tl[0]} / {tl[1]}")
    # does the cut changes which models are solved (abstract/intro/9.7)?
    changed = [n for n in admitted if solved(idx[(n, "baseline")]) != solved(idx[(n, "all")])
               or solved(idx[(n, "baseline")]) != solved(idx[(n, "auto")])]
    check("C1.solved_set_unchanged", "Abstract l.23-24; Intro l.107-110; Sec 9.7 l.285-286 "
          "'cuts never changed which models SCIP solved, in any campaign'", "[] (no change)", changed, not changed)
    # campaign 1 vs control: also changed
    changed_c = [n for n in admitted if solved(idx[(n, "control")]) != solved(idx[(n, "all")])]
    note("C1 models whose solved status differs between control and all:", changed_c)
    for m in ("all", "auto", "control"):
        c = collections.Counter(compare(idx[(n, m)], idx[(n, "baseline")], "dual", 1e-4) for n in admitted)
        note(f"C1 holdout full final dual vs baseline at 1e-4, {m}: {dict(c)}")
    cfg = hold[0]["config"]
    note("C1 config:", cfg)
    check("C1.limits.blocks", "App B Tab 6", 64, cfg["max_blocks"])
    check("C1.limits.rounds", "App B Tab 6", 5, cfg["max_rounds"])
    check("C1.limits.cuts", "App B Tab 6", "24 / 6", f"{cfg['max_cuts']} / {cfg['max_cuts_per_round']}")
    check("C1.limits.allow", "App B Tab 6", "min{2 s, 0.15T}",
          f"min{{{cfg['max_separation_seconds']:g} s, {cfg['separation_budget_fraction']:g}T}}")
    check("C1.limits.deg", "App B Tab 6", "8 / 4", f"{cfg['max_degree_1d']} / {cfg['max_degree_2d']}")
    return recs


# --------------------------------------------------------------------------------------
# Campaign 2 and repair cohort
# --------------------------------------------------------------------------------------
def campaign2():
    recs = load(V2 / "records.jsonl", keep_config=True)
    rep = load(REP / "records.jsonl", keep_config=True)
    W = "Sec 9.3"
    check("C2.runs", W + " (282 runs)", 282, len(recs))
    hold = [r for r in recs if r["suite"] == "holdout" and r["phase"] == "full"]
    root = [r for r in recs if r["suite"] == "holdout" and r["phase"] == "root"]
    modes = ("baseline", "all", "auto")
    names = sorted({r["name"] for r in hold})
    check("C2.models", W, 30, len(names))
    idx = {(r["name"], r["mode"]): r for r in hold}
    ridx = {(r["name"], r["mode"]): r for r in root}
    check("C2.budget", W + " 30-second budget", "[30.0]", str(sorted({r["time_limit"] for r in hold})))
    check("C2.mech", W + " 13 mechanism cases", 13, len({r["name"] for r in recs if r["suite"] == "synthetic"}))
    check("C2.diag", W + " ten diagnostic models", 10, len({r["name"] for r in recs if r["suite"] == "diagnostic"}))
    check("C2.repeat", W + " seed-one repeats on six models", 6,
          len({r["name"] for r in recs if r["phase"] == "repeat" and r["seed"] == 1}))
    adm = [n for n in names if all(not failed(idx[(n, m)]) and idx[(n, m)]["status"] != "source_model_mismatch" for m in modes)]
    check("C2.admitted", W, 30, len(adm))
    sol = {m: {n for n in names if solved(idx[(n, m)])} for m in modes}
    same = sol["baseline"] == sol["all"] == sol["auto"]
    check("C2.solved", W + " every mode solved the same 25", "25 same", f"{len(sol['baseline'])} {'same' if same else 'differ'}")
    uns = [n for n in names if n not in sol["baseline"]]
    cut_any = [n for n in uns if any((r["_ncuts"] or 0) > 0 for r in recs if r["name"] == n)]
    check("C2.unsolved_nocut", W + " five unsolved received no cut in any mode", "[]", str(cut_any), not cut_any)
    note("C2 unsolved:", uns)
    for m, (nm, nc) in (("all", (7, 38)), ("auto", (3, 10))):
        withc = [n for n in names if (idx[(n, m)]["_ncuts"] or 0) > 0]
        check(f"C2.cuts.{m}", W + " models with cuts (cuts), holdout full", f"{nm} ({nc})",
              f"{len(withc)} ({sum(idx[(n, m)]['_ncuts'] or 0 for n in names)})")
        note(f"C2 {m} models with cuts:", withc)
    withc = sorted({n for n in names for m in ("all", "auto") if (idx[(n, m)]["_ncuts"] or 0) > 0})
    check("C2.cutmodels_solved", W + " all solved by baseline", True, all(n in sol["baseline"] for n in withc))
    atroot = [n for n in withc if all(idx[(n, m)]["nodes"] == 1 for m in modes)]
    check("C2.atroot", W + " 'four of them were solved at the root in every mode'", 4, len(atroot))
    note("C2 cut models solved at root (nodes==1 in full runs, every mode):", atroot)
    for rtol in (1e-4, 1e-6):
        for m in ("all", "auto"):
            fc = collections.Counter(compare(idx[(n, m)], idx[(n, "baseline")], "dual", rtol) for n in names)
            rc = collections.Counter(compare(ridx[(n, m)], ridx[(n, "baseline")], "dual", rtol) for n in names)
            note(f"C2 rtol={rtol:g} {m}: final {dict(fc)} root {dict(rc)}; root worse: "
                 f"{[n for n in names if compare(ridx[(n, m)], ridx[(n, 'baseline')], 'dual', rtol) == 'worse']}")
            if rtol == 1e-4:
                check(f"C2.better.{m}", W + " no final or root bound better at 1e-4", 0,
                      fc["better"] + rc["better"])
                worse = sorted(n for n in names if compare(idx[(n, m)], idx[(n, "baseline")], "dual", rtol) == "worse")
                check(f"C2.worse.{m}", W + " four time-limited models worse (final)", 4, len(worse))
                note(f"C2 worse final {m}:", worse, [idx[(n, 'baseline')]['status'] for n in worse])
            else:
                note(f"C2 1e-6 {m}: better final {fc['better']} worse final {fc['worse']}; root better {rc['better']} worse {rc['worse']}")
    common = sorted(sol["baseline"] & sol["all"] & sol["auto"])
    for m, st in (("baseline", "0.55"), ("all", "0.99"), ("auto", "0.96")):
        v = sgm(t_read(idx[(n, m)]) for n in common)
        check(f"C2.sgm.{m}", W + " SGM on 25 commonly solved", st, round(v, 3), close(st, v, 2))
        note(f"C2 SGM {m} total only: {sgm(t_total(idx[(n, m)]) for n in common):.4f}, "
             f"total+prep: {sgm(t_prep(idx[(n, m)]) for n in common):.4f}")
    for m in ("all", "auto"):
        slower = sum(t_read(idx[(n, m)]) > 1.1 * t_read(idx[(n, 'baseline')]) for n in common)
        check(f"C2.slower10.{m}", W + " >10% slower on 21 of 25", 21, slower)
    a = [idx[(n, "all")] for n in names]
    cb, dc, cand, cert = (sum(sep(r, k) for r in a) for k in
                          ("callback_seconds", "discovery_seconds", "candidate_seconds", "certification_seconds"))
    check("C2.callback", W + " callback seconds (all)", "27.6", round(cb, 2), close("27.6", cb, 1))
    check("C2.discovery", W + " discovery seconds (all)", "24.4", round(dc, 2), close("24.4", dc, 1))
    check("C2.dirLP", W + " direction LPs (all)", "0.7", round(cand, 2), close("0.7", cand, 1))
    check("C2.cert", W + " certification (all)", "2.4", round(cert, 2), close("2.4", cert, 1))
    werr = [r for r in recs if r["status"] == "worker_error"]
    check("C2.workererr", W + " four worker errors on two diagnostic models", "4 on 2",
          f"{len(werr)} on {len({r['name'] for r in werr})}")
    over = [(r["run_id"], r["discovery_seconds"] - allowance(r)) for r in recs
            if r["mode"] in ("all", "auto") and not failed(r) and finite(r.get("discovery_seconds"))
            and r["discovery_seconds"] > allowance(r)]
    check("C2.overruns", W + " discovery exceeded allowance in 46 cut-mode runs", 46, len(over))
    mx = max(x for _, x in over)
    check("C2.overrun.max", W + " 'by up to 19 s'", "19", round(mx, 2), close("19", mx, 0))
    # repair cohort
    W = "Sec 9.3 (repair)"
    groups = {(r["name"], r["phase"], r["seed"]) for r in rep}
    check("C2R.groups", W, "25 groups, 75 runs", f"{len(groups)} groups, {len(rep)} runs")
    check("C2R.errors", W + " no worker errors", 0, sum(failed(r) for r in rep))
    gi = collections.defaultdict(dict)
    for r in rep:
        gi[(r["name"], r["phase"], r["seed"])][r["mode"]] = r
    diff = [g for g, d in gi.items() if g[1] != "root" and len({solved(d[m]) for m in modes}) > 1]
    check("C2R.samesolved", W + " every mode solved the same models", "[]", str(diff), not diff)
    rov = [max(r["discovery_seconds"] - allowance(r), 0.0) for r in rep if r["mode"] in ("all", "auto")]
    rcb = [max(sep(r, "callback_seconds") - allowance(r), 0.0) for r in rep if r["mode"] in ("all", "auto")]
    check("C2R.overrun", W + " largest remaining overrun of the separator allowance 0.03 s (callback_seconds)",
          "0.03", round(max(rcb), 4), close("0.03", max(rcb), 2))
    note(f"C2R largest discovery-seconds overrun of the allowance: {max(rov):.4f}")
    g = [d for k, d in gi.items() if k[0] == "graphpart_clique-40" and k[1] == "full"]
    if g:
        d = g[0]
        note("C2R graphpart_clique-40 full duals:", {m: d[m]["dual"] for m in modes})
        check("C2R.graphpart", W + " graphpart_clique-40 worse bound disappeared", "tie,tie",
              ",".join(compare(d[m], d["baseline"], "dual", 1e-4) for m in ("all", "auto")))
    nc2, ncr = sum(r["_ncuts"] or 0 for r in recs), sum(r["_ncuts"] or 0 for r in rep)
    check("C2.cuts.total", "Sec 9.3 'All 123 cuts of the prospective campaign'", 123, nc2)
    check("C2R.cuts.total", "Sec 9.3 '42 of the repair cohort'", 42, ncr)
    for path, n in ((V2, 123), (REP, 42)):
        rp = json.load(open(path / "replay.json"))
        check(f"replay.{path.name}", "Sec 9.3 replay", f"passed {n}", f"passed={rp.get('passed')} {rp.get('replayed_cuts')}",
              rp.get("passed") is True and rp.get("replayed_cuts") == n)
    inc = [r for r in recs + rep if has_incumbent(r)]
    check("C2.incumbents", "Sec 9.3 '338 returned incumbents'", 338, len(inc))
    check("C2.incumbents.passed", "Sec 9.3", 338, sum(inc_passed(r) for r in inc))
    # A/A of repair cohort baseline vs original baseline
    oi = {r["run_id"]: r for r in recs}
    aa = collections.Counter()
    for r in rep:
        if r["mode"] == "baseline":
            o = oi.get(r["original_run_id"])
            aa[compare(r, o, "dual", 1e-6)] += 1
    note("C2R A/A baseline rerun vs original at 1e-6:", dict(aa))
    cfg = hold[0]["config"]
    note("C2 config:", cfg)
    for key, st in (("max_blocks", 32), ("max_rows_per_block", 6), ("max_domain_rows", 16), ("max_rounds", 3),
                    ("max_cuts", 12), ("max_cuts_per_round", 4), ("max_support_calls", 24),
                    ("max_exchange_rounds", 3), ("max_faces", 2000), ("max_cells", 128), ("max_depth", 16)):
        check(f"C2.limits.{key}", "App B Tab 6", st, cfg[key])
    check("C2.limits.allow", "App B Tab 6", "min{1 s, 0.05T}",
          f"min{{{cfg['max_separation_seconds']:g} s, {cfg['separation_budget_fraction']:g}T}}")
    return recs, rep


# --------------------------------------------------------------------------------------
# Campaign 3
# --------------------------------------------------------------------------------------
def index(recs):
    return {(r["name"], r["seed"], r["mode"]): r for r in recs}


def part_full(recs, part, seeds, stated, W):
    modes = ("baseline", "all", "auto")
    idx = index(recs)
    names = sorted({r["name"] for r in recs})
    res = {}
    for m in modes:
        rows = [idx[(n, s, m)] for n in names for s in seeds]
        res[m] = rows
    # solved per mode
    for m in modes:
        sv = sum(solved(r) for r in res[m])
        check(f"{part}.solved.{m}", W + " Table 2 Solved", stated[m][0], f"{sv}/{len(res[m])}")
    for m in ("all", "auto"):
        nc = sum(r["_ncuts"] or 0 for r in res[m])
        nr = sum((r["_ncuts"] or 0) > 0 for r in res[m])
        check(f"{part}.cuts.{m}", W + " Table 2 Cuts (runs)", stated[m][1], f"{nc} ({nr})")
    common = [(n, s) for n in names for s in seeds if all(solved(idx[(n, s, m)]) for m in modes)]
    for m in modes:
        v = sgm(t_prep(idx[(n, s, m)]) for n, s in common)
        check(f"{part}.sgm.{m}", W + f" Table 2 SGM time over {len(common)} common-solved runs", stated[m][2],
              round(v, 3), close(stated[m][2], v, 2))
        note(f"{part} SGM {m}: total+prep {v:.4f}, total {sgm(t_total(idx[(n, s, m)]) for n, s in common):.4f}, "
             f"outer {sgm(t_outer(idx[(n, s, m)]) for n, s in common):.4f}")
    ratios = {}
    for m in ("all", "auto"):
        rr = [t_prep(idx[(n, s, m)]) / max(t_prep(idx[(n, s, "baseline")]), 1e-9) for n, s in common]
        ratios[m] = rr
        check(f"{part}.faster.{m}", W + " Table 2 runs faster than baseline", stated[m][3],
              f"{sum(x < 1 for x in rr)}/{len(rr)}")
        note(f"{part} {m}: slower {sum(x > 1 for x in rr)}/{len(rr)}, median ratio {statistics.median(rr):.3f}, "
             f">10% slower {sum(x > 1.1 for x in rr)}")
    return idx, names, common, ratios


def campaign3():
    out = {}
    # ---------------- Part A full
    W = "Sec 9.4 Part A"
    A = load(V3 / "partA-full/records.jsonl", keep_config=True)
    check("A.runs", W, 270, len(A))
    st = {"baseline": ("80/90", None, "1.05", None), "all": ("80/90", "151 (33)", "1.27", "11/80"),
          "auto": ("80/90", "37 (15)", "1.21", "6/80")}
    idx, names, common, ratios = part_full(A, "A", (0, 1, 2), st, W)
    check("A.budget", W + " 300-second budget", "[300.0]", str(sorted({r["time_limit"] for r in A})))
    for s in (0, 1, 2):
        sets = [{n for n in names if solved(idx[(n, s, m)])} for m in ("baseline", "all", "auto")]
        check(f"A.same.s{s}", W + " all modes solved the same models (seed)", True, sets[0] == sets[1] == sets[2])
    g40 = [solved(idx[("graphpart_clique-40", s, "baseline")]) for s in (0, 1, 2)]
    check("A.graphpart", W + " graphpart_clique-40 solved", "[True, True, True]", str(g40))
    tln7 = sum(solved(idx[("tln7", s, m)]) for s in (0, 1, 2) for m in ("baseline", "all", "auto"))
    tln7s = [s for s in (0, 1, 2) if all(solved(idx[("tln7", s, m)]) for m in ("baseline", "all", "auto"))]
    check("A.tln7", W + " tln7 solved in two of three seeds", 2, len(tln7s))
    never = sorted(n for n in names if not any(solved(idx[(n, s, m)]) for s in (0, 1, 2) for m in ("baseline", "all", "auto")))
    check("A.never", W + " unsolved in every mode and seed", "ex5_2_5,ex8_3_4,waterx", ",".join(never))
    for m, k in (("all", 11), ("auto", 5)):
        withc = {n for n in names for s in (0, 1, 2) if (idx[(n, s, m)]["_ncuts"] or 0) > 0}
        check(f"A.cutmodels.{m}", W + " models with cuts (full runs)", k, len(withc))
    for m, (b, w) in (("all", (2, 4)), ("auto", (3, 3))):
        c = collections.Counter(compare(idx[(n, s, m)], idx[(n, s, "baseline")], "dual", 1e-4)
                                for n in names for s in (0, 1, 2))
        check(f"A.bounds.{m}", W + " final bounds better/worse of 90 at 1e-4", f"{b}/{w}", f"{c['better']}/{c['worse']}")
        lst = [(n, s, compare(idx[(n, s, m)], idx[(n, s, "baseline")], "dual", 1e-4)) for n in names for s in (0, 1, 2)
               if compare(idx[(n, s, m)], idx[(n, s, "baseline")], "dual", 1e-4) in ("better", "worse")]
        note(f"A final-bound differences {m}:", lst)
        c6 = collections.Counter(compare(idx[(n, s, m)], idx[(n, s, "baseline")], "dual", 1e-6)
                                 for n in names for s in (0, 1, 2))
        note(f"A final 1e-6 {m}: {dict(c6)}")
    aa1 = collections.Counter(compare(idx[(n, 1, "baseline")], idx[(n, 0, "baseline")], "dual", 1e-4) for n in names)
    aa2 = collections.Counter(compare(idx[(n, 2, "baseline")], idx[(n, 0, "baseline")], "dual", 1e-4) for n in names)
    aa12 = collections.Counter(compare(idx[(n, 2, "baseline")], idx[(n, 1, "baseline")], "dual", 1e-4) for n in names)
    anyd = sum(any(compare(idx[(n, s, "baseline")], idx[(n, t, "baseline")], "dual", 1e-4) in ("better", "worse")
                   for s, t in ((1, 0), (2, 0), (2, 1))) for n in names)
    note(f"A A/A baseline seed1 vs 0: {dict(aa1)}; seed2 vs 0: {dict(aa2)}; seed2 vs 1: {dict(aa12)}; "
         f"models differing in any seed pair: {anyd}")
    d10 = sum(v for k, v in aa1.items() if k in ('better', 'worse'))
    d20 = sum(v for k, v in aa2.items() if k in ('better', 'worse'))
    check("A.aa", W + " 'baseline itself differed in 3 of 30 comparisons'", "3 of 30",
          f"{d10} of 30 (s1 vs s0), {d20} of 30 (s2 vs s0), {d10 + d20} of 60", d10 == 3 or d20 == 3 or anyd == 3)
    for m in ("all", "auto"):
        b = sgm(t_prep(idx[(n, s, 'baseline')]) for n, s in common)
        v = sgm(t_prep(idx[(n, s, m)]) for n, s in common)
        note(f"A {m}: SGM slowdown {100 * (v / b - 1):.1f}%")
    sl = [100 * (sgm(t_prep(idx[(n, s, m)]) for n, s in common) / sgm(t_prep(idx[(n, s, 'baseline')]) for n, s in common) - 1)
          for m in ("all", "auto")]
    check("A.slowdown", W + " slower by 15-21% in SGM", "15-21", f"{min(sl):.1f}-{max(sl):.1f}",
          round(min(sl)) == 15 and round(max(sl)) == 21)
    med = statistics.median(ratios["all"] + ratios["auto"])
    check("A.median", W + " median factor of 1.3 per run (pooled all+auto)", "1.3", round(med, 3), close("1.3", med, 1))
    note(f"A median ratio all {statistics.median(ratios['all']):.3f} auto {statistics.median(ratios['auto']):.3f}")
    out["A"] = A
    # ---------------- Part A root
    AR = load(V3 / "partA-root/records.jsonl")
    out["AR"] = AR
    # ---------------- Part B
    W = "Sec 9.4 Part B"
    B = load(V3 / "partB/records.jsonl", keep_config=True)
    BF = [r for r in B if r["phase"] == "full"]
    BR = [r for r in B if r["phase"] == "root"]
    st = {"baseline": ("52/60", None, "1.33", None), "all": ("52/60", "179 (40)", "1.87", "8/52"),
          "auto": ("52/60", "145 (38)", "1.82", "9/52")}
    idx, names, common, ratios = part_full(BF, "B", (0, 1), st, W)
    check("B.models", W, 30, len(names))
    check("B.admitted", W + " all 30 admitted", 30,
          len({r["name"] for r in B if not failed(r) and r["status"] != "source_model_mismatch"}))
    for s in (0, 1):
        sets = [{n for n in names if solved(idx[(n, s, m)])} for m in ("baseline", "all", "auto")]
        check(f"B.same.s{s}", W + " same 26 solved in every mode", "26 same",
              f"{len(sets[0])} {'same' if sets[0] == sets[1] == sets[2] else 'differ'}")
    uns = sorted({n for n in names for s in (0, 1) if not solved(idx[(n, s, "baseline")])})
    check("B.unsolved", W, "bayes2_20,bayes2_30,bayes2_50,kall_circles_c8a", ",".join(uns))
    st_uns = {(n, s): idx[(n, s, "baseline")]["status"] for n in uns for s in (0, 1)}
    note("B unsolved statuses:", st_uns)
    withc = {n for n in names for s in (0, 1) for m in ("all", "auto") if (idx[(n, s, m)]["_ncuts"] or 0) > 0}
    check("B.cutmodels", W + " cuts added on 20 of 30 models (full runs, any cut mode)", 20, len(withc))
    note("B models with cuts (full, all):", len({n for n in names for s in (0, 1) if (idx[(n, s, 'all')]['_ncuts'] or 0) > 0}),
         "(auto):", len({n for n in names for s in (0, 1) if (idx[(n, s, 'auto')]['_ncuts'] or 0) > 0}))
    for m in ("all", "auto"):
        lst = [(n, s, compare(idx[(n, s, m)], idx[(n, s, "baseline")], "dual", 1e-4)) for n in names for s in (0, 1)]
        c = collections.Counter(x[2] for x in lst)
        bet = sorted({x[0] for x in lst if x[2] == "better"})
        check(f"B.bounds.{m}", W + " final better 2 of 60, both kall_circles_c8a, never worse",
              "2/0 [kall_circles_c8a]", f"{c['better']}/{c['worse']} [{','.join(bet)}]")
    sl = [100 * (sgm(t_prep(idx[(n, s, m)]) for n, s in common) / sgm(t_prep(idx[(n, s, 'baseline')]) for n, s in common) - 1)
          for m in ("all", "auto")]
    check("B.slowdown", W + " about 40% slower in SGM", "about 40", f"{sl[0]:.1f} (all), {sl[1]:.1f} (auto)",
          all(35 <= x <= 45 for x in sl))
    slower = [sum(x > 1 for x in ratios[m]) for m in ("all", "auto")]
    check("B.slower", W + " 'slower on 44 of 52 runs'", "44 of 52", f"{slower[0]} (all), {slower[1]} (auto) of 52",
          slower[0] == 44 and slower[1] == 44)
    # root effects
    rid = {(r["name"], r["mode"]): r for r in BR}
    rmodes = ("all", "auto", "all-diag")
    for m in rmodes:
        c = collections.Counter(compare(rid[(n, m)], rid[(n, "baseline")], "dual", 1e-4) for n in names)
        bet = sorted(n for n in names if compare(rid[(n, m)], rid[(n, "baseline")], "dual", 1e-4) == "better")
        wor = sorted(n for n in names if compare(rid[(n, m)], rid[(n, "baseline")], "dual", 1e-4) == "worse")
        note(f"B root {m}: {dict(c)} better={bet} worse={wor}")
    for n in ("pooling_bental4tp", "pooling_bental4pq", "ex3_1_4", "pointpack04", "pooling_haverly2pq"):
        note(f"B root {n}: sense={rid[(n, 'baseline')]['sense']} " + ", ".join(
            f"{m}={rid[(n, m)]['dual']:.6g} ({rid[(n, m)]['status']}, nodes {rid[(n, m)]['nodes']}, cuts {rid[(n, m)]['_ncuts']})"
            for m in ("baseline",) + rmodes))
    def closed(n, m):
        r = rid[(n, m)]
        return r["status"] in ("optimal", "gaplimit") and solved(r)
    check("B.bental4tp", W + " closed root gap of pooling_bental4tp in every cut mode", "all,auto,all-diag",
          ",".join(m for m in rmodes if closed("pooling_bental4tp", m)))
    check("B.bental4pq", W + " pooling_bental4pq closed in auto and all-diag", "auto,all-diag",
          ",".join(m for m in rmodes if closed("pooling_bental4pq", m)))
    e = {m: rid[("ex3_1_4", m)]["dual"] for m in ("baseline",) + rmodes}
    check("B.ex3_1_4", W + " ex3_1_4 root -6 -> -5.79, -5.69 with raised limits",
          "-6 / -5.79 / -5.69", f"{e['baseline']:.3f} / all {e['all']:.3f}, auto {e['auto']:.3f} / {e['all-diag']:.3f}",
          close("-6", e["baseline"], 2) and (close("-5.79", e["all"], 2) or close("-5.79", e["auto"], 2))
          and close("-5.69", e["all-diag"], 2))
    worse_auto = sorted(n for n in names if compare(rid[(n, "auto")], rid[(n, "baseline")], "dual", 1e-4) == "worse")
    check("B.auto_worse", W + " auto worse root bound (pooling_haverly2pq, pointpack04)",
          "pointpack04,pooling_haverly2pq", ",".join(worse_auto))
    # all-diag added cuts and "one more model"
    for part, recsr, st, extra in (("A", AR, 403, "cvxnonsep_psig20r"), ("B", BR, 358, "pooling_bental4pq")):
        rr = {(r["name"], r["mode"]): r for r in recsr}
        nn = sorted({r["name"] for r in recsr})
        nd = sum(rr[(n, "all-diag")]["_ncuts"] or 0 for n in nn)
        check(f"{part}.diagcuts", "Sec 9.4 all-diag cuts", st, nd)
        b = {m: {n for n in nn if compare(rr[(n, m)], rr[(n, "baseline")], "dual", 1e-4) == "better"} for m in rmodes}
        more = sorted(b["all-diag"] - b["all"])
        more_any = sorted(b["all-diag"] - b["all"] - b["auto"])
        note(f"{part} root better at 1e-4: all={sorted(b['all'])} auto={sorted(b['auto'])} all-diag={sorted(b['all-diag'])}")
        check(f"{part}.diagmore", "Sec 9.4 all-diag improved one more model", extra,
              ",".join(more) + (f" (vs all and auto: {','.join(more_any)})" if more_any != more else ""),
              more == [extra])
        note(f"{part} root cuts by mode:", {m: sum(rr[(n, m)]['_ncuts'] or 0 for n in nn) for m in rmodes})
    out["B"] = B
    # Part B: callback cost
    a = [r for r in BF if r["mode"] == "all"]
    cb, ce, ca, di = (sum(sep(r, k) for r in a) for k in
                      ("callback_seconds", "certification_seconds", "candidate_seconds", "discovery_seconds"))
    W2 = "Sec 9.5"
    check("B.callback", W2 + " Part B callback seconds (all, 60 full runs)", "32.9", round(cb, 2), close("32.9", cb, 1))
    check("B.cert", W2 + " certification", "23.0", round(ce, 2), close("23.0", ce, 1))
    check("B.dirLP", W2 + " direction LPs", "3.9", round(ca, 2), close("3.9", ca, 1))
    check("B.disc", W2 + " discovery", "4.4", round(di, 2), close("4.4", di, 1))
    note(f"B callback per run {cb / len(a):.3f} s over {len(a)} runs")
    # median SCIP time of the baseline in Part B (to judge 'same order as SCIP's whole solving time')
    bt = [r["scip_solve_seconds"] for r in BF if r["mode"] == "baseline"]
    note(f"B baseline scip_solve_seconds median {statistics.median(bt):.3f}")
    # ---------------- incumbents and replay
    inc = [r for r in A + AR + B if has_incumbent(r)]
    check("AB.incumbents", "Sec 9.4 incumbents Parts A and B", 679, len(inc))
    check("AB.incumbents.passed", "Sec 9.4", 679, sum(inc_passed(r) for r in inc))
    check("AB.runs", "Sec 9.4 'Parts A and B together comprise 690 runs'", 690, len(A) + len(AR) + len(B))
    noinc = [r["run_id"] for r in A + AR + B if not has_incumbent(r)]
    note("AB runs without incumbent:", len(noinc), noinc)
    return out


def replay_checks():
    W = "Sec 9.4 replay"
    tot = 0
    for part, st in (("partA-full", 188), ("partA-root", 465), ("partB", 845), ("partC", 6000)):
        rp = json.load(open(V3 / part / "replay.json"))
        n = 0
        with open(V3 / part / "records.jsonl") as f:
            for line in f:
                r = json.loads(line)
                n += len(r["cuts"]) if isinstance(r.get("cuts"), list) else 0
        tam = rp.get("tamper_rejections") or {}
        ok = rp.get("passed") is True and rp.get("replayed_cuts") == st == n and len(tam) == 14 and all(tam.values())
        # v3 wrapper per-mode tamper checks
        v3t = (rp.get("v3") or {})
        check(f"replay.{part}", W, f"{st} cuts, 14 tamper rejected",
              f"records {n}, replayed {rp.get('replayed_cuts')}, passed {rp.get('passed')}, "
              f"tamper {sum(bool(v) for v in tam.values())}/{len(tam)}", ok)
        note(f"replay {part} v3 wrapper keys: {list(v3t.keys())}")
        tot += n
    check("replay.total", W + " 7,498 cuts in Parts A to C", 7498, tot)
    for part in ("partA-root-rowdir", "partB-root-rowdir", "partC-rowdir"):
        p = V3D / part / "replay.json"
        n = 0
        with open(V3D / part / "records.jsonl") as f:
            for line in f:
                r = json.loads(line)
                n += len(r["cuts"]) if isinstance(r.get("cuts"), list) else 0
        if p.exists():
            rp = json.load(open(p))
            note(f"v3d replay {part}: exists, passed={rp.get('passed')}, replayed {rp.get('replayed_cuts')} of {n} recorded")
        else:
            note(f"v3d replay {part}: replay.json MISSING; recorded cuts {n}")
        check(f"v3d.replay.{part}", "Abstract/Intro/Sec 9.7 'every recorded cut passed replay' (diagnostic)",
              "replay passed", "passed" if p.exists() and json.load(open(p)).get("passed") else "no replay.json",
              p.exists() and json.load(open(p)).get("passed") is True)


# --------------------------------------------------------------------------------------
# Scan and selection
# --------------------------------------------------------------------------------------
def scan_and_selection():
    W = "Sec 9.5 scan"
    recs = [json.loads(l) for l in open(SCAN / "records.jsonl")]
    check("S.pool", W, 392, len(recs))
    adm = [r for r in recs if r["status"] == "admitted" and r.get("discovery_completed")]
    check("S.admitted", W, 389, len(adm))
    to = [r for r in recs if r.get("process_timeout")]
    check("S.timeout", W + " three timed out while building", 3, len(to))
    any_b = [r for r in adm if r["blocks"]]
    q2 = [r for r in adm if any(b["quadratic"] and b["dimension"] >= 2 for b in r["blocks"])]
    nr2 = [r for r in adm if any(b["nonlinear_rows"] >= 2 for b in r["blocks"])]
    ns2 = [r for r in adm if any(b["nonlinear_sides"] >= 2 for b in r["blocks"])]
    au = [r for r in adm if any(b["auto_eligible"] for b in r["blocks"])]
    check("S.anyblock", W, 234, len(any_b))
    check("S.quad2", W, 185, len(q2))
    check("S.rows2", W + " 'a block with at least two nonlinear rows'", 110, len(nr2))
    note(f"S blocks with >= 2 nonlinear sides: {len(ns2)}")
    check("S.auto", W, 111, len(au))
    check("S.auto_convex", W + " none of the latter are convex", 0, sum(r["stratum"] == "convex" for r in au))
    ds = [r["discovery_seconds"] for r in adm]
    check("S.median", W + " median discovery 0.04 s", "0.04", round(statistics.median(ds), 4),
          close("0.04", statistics.median(ds), 2))
    check("S.max", W + " at most 4.2 s", "4.2", round(max(ds), 3), close("4.2", max(ds), 1))
    strata = collections.Counter(r["stratum"] for r in recs)
    note("S strata:", dict(strata))
    # selection
    sel = json.load(open(SCAN / "partB-selection.json"))
    ranked = sorted((hashlib.sha256(("convexification-structure-v3:" + r["name"]).encode()).hexdigest(), r["name"])
                    for r in au)
    mine = [n for _, n in ranked[:30]]
    check("S.selection", "Sec 9.4 / App B Part B selection = first 30 by hash",
          True, mine == [x["name"] for x in sel["selected"]])
    # v2 selection
    h = json.load(open(HOLDOUT2))
    check("Sel.eligible", "App B 422 eligible models", 422, h["eligible_count"])
    check("Sel.excluded", "App B 'excluding the 160 names used or excluded by the first campaign'", 160,
          len(h["excluded_names"]))
    check("Sel.strata", "App B strata 85, 208, 129", "85, 208, 129",
          ", ".join(str(h["stratum_eligible_counts"][k]) for k in ("convex", "nonconvex_continuous", "nonconvex_integer")))
    check("Sel.limits", "App B limits 120 vars, 180 cons, 250,000 bytes",
          "120/180/250000", f"{h['limits']['variables']}/{h['limits']['constraints']}/{h['limits']['osil_bytes']}")
    note("Sel parser_errors excluded from 'eligible' (not mentioned in App B):", len(h.get("parser_errors", [])))
    elig = h["eligible_names_in_rank_order"]
    ranks = [hashlib.sha256(("convexification-holdout-v2:" + n).encode()).hexdigest() for n in elig]
    check("Sel.order", "App B hash order", True, ranks == sorted(ranks))
    sel2 = [x["name"] for x in h["selected"]]
    strat = {x["name"]: x["stratum"] for x in h["selected"]}
    check("Sel.v2", "App B first ten per stratum", "10/10/10",
          "/".join(str(sum(v == k for v in strat.values())) for k in ("convex", "nonconvex_continuous", "nonconvex_integer")))
    tex = (PAPER / "sections/B-tables.tex").read_text()
    import re
    m = re.search(r"Models of campaigns 2 and 3 \(Part A\).\}(.*?)\n", tex)
    listed = [x.replace("\\_", "_") for x in re.findall(r"\\code\{([^}]*)\}", m.group(1))] if m else []
    check("Sel.listA", "App B list of Part A models equals v2 selection (order)", True, listed == sel2)
    pool = set(elig) - set(sel2)
    check("S.pool_is_rest", "Sec 9.4 'the 392 eligible models not used in campaign 2'", True,
          pool == {r["name"] for r in recs})


# --------------------------------------------------------------------------------------
# Part C and the v3d diagnostic
# --------------------------------------------------------------------------------------
def mech_cases():
    cases = {}
    for p in sorted((V3 / "partC/cases").glob("*.json")):
        c = json.loads(p.read_text())
        cases[c.get("name", p.stem)] = c
    return cases


def partC():
    W = "Sec 9.6"
    C = load(V3 / "partC/records.jsonl")
    D = load(V3D / "partC-rowdir/records.jsonl")
    cases = mech_cases()
    names = sorted(cases, key=lambda n: (cases[n]["mechanism"]["n"], cases[n]["mechanism"]["seed"]))
    check("C.instances", W, 20, len(names))
    opt = {n: float(cases[n]["known_optimum"]) for n in names}
    nn = {n: cases[n]["mechanism"]["n"] for n in names}
    sd = {n: cases[n]["mechanism"]["seed"] for n in names}
    ci = {(r["phase"], r["name"], r["mode"]): r for r in C}
    di = {(r["phase"], r["name"], r["mode"]): r for r in D}
    # optimum check against the exact formula
    from fractions import Fraction
    bad = []
    for n in names:
        c = cases[n]
        ex = c.get("known_optimum_exact")
        if ex is not None and float(Fraction(ex)) != opt[n]:
            bad.append(n)
    check("C.opt_exact", W + " known optimum stored exactly", "[]", str(bad), not bad)

    def closed(rec_m, rec_b, n, key="dual"):
        b, m = rec_b[key], rec_m[key]
        return (m - b) / (opt[n] - b)

    fr, rd, wd, frr = {}, {}, {}, {}
    for n in names:
        b = ci[("root", n, "baseline")]
        fr[n] = closed(ci[("root", n, "all-diag-mech")], b, n)
        rd[n] = closed(di[("root", n, "all-diag-mech")], b, n)
        wd[n] = closed(di[("root", n, "all-diag-mech-wide")], b, n)
        bd = di[("root", n, "baseline")]
        frr[n] = (closed(di[("root", n, "all-diag-mech")], bd, n), closed(di[("root", n, "all-diag-mech-wide")], bd, n))
        # root_dual vs dual in root runs
        for rr in (b, ci[("root", n, "all-diag-mech")]):
            if finite(rr.get("root_dual")) and abs(rr["root_dual"] - rr["dual"]) > 1e-9 * max(1, abs(rr["dual"])):
                note(f"C root run {rr['run_id']} root_dual {rr['root_dual']} != dual {rr['dual']}")
    tab3 = {10: ("0.35", "0.44", "1.00", 5, 5, 5, 5), 20: ("0.25", "0.44", "1.00", 4, 4, 5, 5),
            40: ("0.19", "0.43", "1.00", 0, 0, 0, 5), 80: ("0.22", "0.46", "1.00", 0, 0, 0, 5)}
    for k, st in tab3.items():
        ns = [n for n in names if nn[n] == k]
        mf = statistics.median(fr[n] for n in ns)
        mr = statistics.median(rd[n] for n in ns)
        mw = statistics.median(wd[n] for n in ns)
        check(f"C.T3.n{k}.frozen", "Table 3 median closed, frozen", st[0], round(mf, 4), close(st[0], mf, 2))
        check(f"C.T3.n{k}.rowdir", "Table 3 median closed, row dir.", st[1], round(mr, 4), close(st[1], mr, 2))
        check(f"C.T3.n{k}.wide", "Table 3 median closed, row dir. wide", st[2], round(mw, 4), close(st[2], mw, 2))
        note(f"C n={k} median closure vs rerun baseline: rowdir {statistics.median(frr[n][0] for n in ns):.4f} "
             f"wide {statistics.median(frr[n][1] for n in ns):.4f}")
        sb = sum(solved(ci[("full", n, "baseline")]) for n in ns)
        sf = sum(solved(ci[("full", n, "all-diag-mech")]) for n in ns)
        sr = sum(solved(di[("full", n, "all-diag-mech")]) for n in ns)
        sw = sum(solved(di[("full", n, "all-diag-mech-wide")]) for n in ns)
        sbr = sum(solved(di[("full", n, "baseline")]) for n in ns)
        check(f"C.T3.n{k}.solved", "Table 3 solved baseline/frozen/rowdir/wide", "/".join(map(str, st[3:])),
              f"{sb}/{sf}/{sr}/{sw}", (sb, sf, sr, sw) == st[3:])
        note(f"C n={k} rerun baseline solved {sbr}")
    # text claims
    allfr = list(fr.values())
    check("C.frozen.improved", W + " frozen improved root bound on all 20", 20, sum(x > 0 for x in allfr))
    meds = [statistics.median(fr[n] for n in names if nn[n] == k) for k in (10, 20, 40, 80)]
    check("C.frozen.medrange", W + " median 19-35%", "19-35", f"{100 * min(meds):.0f}-{100 * max(meds):.0f}",
          round(100 * min(meds)) == 19 and round(100 * max(meds)) == 35)
    note(f"C frozen closure range over instances: {min(allfr):.3f}-{max(allfr):.3f}")
    note(f"C rowdir closure range over instances: {min(rd.values()):.3f}-{max(rd.values()):.3f}; "
         f"wide {min(wd.values()):.6f}-{max(wd.values()):.6f}")
    rmeds = [statistics.median(rd[n] for n in names if nn[n] == k) for k in (10, 20, 40, 80)]
    check("C.rowdir.medrange", W + " row direction alone 43-46%", "43-46",
          f"{100 * min(rmeds):.0f}-{100 * max(rmeds):.0f}", round(100 * min(rmeds)) == 43 and round(100 * max(rmeds)) == 46)
    complete = [n for n in names if abs(wd[n] - 1) <= 1e-4]
    check("C.wide.complete", W + " root gap closed completely on all 20 (|closed-1|<=1e-4)", 20, len(complete))
    # root bound vs optimum for wide, relative 1e-4
    rel = [(n, (opt[n] - di[("root", n, "all-diag-mech-wide")]["dual"])) for n in names]
    note("C wide root gap to optimum (abs):", [(n, f"{g:.2e}") for n, g in rel])
    per_copy = {n: ci[("root", n, "baseline")]["dual"] / nn[n] for n in names}
    lo, hi = min(per_copy.values()), max(per_copy.values())
    by_n = {k: statistics.fmean(per_copy[n] for n in names if nn[n] == k) for k in (10, 20, 40, 80)}
    agg = {k: sum(ci[("root", n, "baseline")]["dual"] for n in names if nn[n] == k) / (5 * k) for k in (10, 20, 40, 80)}
    note(f"C baseline root bound per copy: per instance {lo:.4f}..{hi:.4f}; mean by n {by_n}; ")
    check("C.percopy", W + " root bound 'between -0.031 and -0.022 per copy on average'", "-0.031..-0.022",
          f"per instance {lo:.4f}..{hi:.4f}; mean by n {min(by_n.values()):.4f}..{max(by_n.values()):.4f}",
          (round(lo, 3) == -0.031 and round(hi, 3) == -0.022) or
          (round(min(by_n.values()), 3) == -0.031 and round(max(by_n.values()), 3) == -0.022))
    mind = min(Fraction(cases[n]["known_optimum_exact"]) / nn[n] for n in names)
    note(f"C smallest optimum per copy {mind} = {float(mind):.6g}")
    # each copy contributes at least 1/8192
    # full runs
    both = [n for n in names if solved(ci[("full", n, "baseline")]) and solved(ci[("full", n, "all-diag-mech")])]
    check("C.full.same9", W + " both modes solved the same 9", 9, len(both))
    same = {n for n in names if solved(ci[("full", n, "baseline")])} == {n for n in names if solved(ci[("full", n, "all-diag-mech")])}
    check("C.full.sameset", W + " same instances", True, same)
    for nb, nm in ((30798, 2316), (166693, 69996)):
        hit = [n for n in both if ci[("full", n, "baseline")]["nodes"] == nb and ci[("full", n, "all-diag-mech")]["nodes"] == nm]
        check(f"C.nodes.{nb}", W + f" nodes {nb} -> {nm}", 1, len(hit))
    fewer = sum(ci[("full", n, "all-diag-mech")]["nodes"] < ci[("full", n, "baseline")]["nodes"] for n in both)
    note(f"C full: cuts reduced nodes on {fewer} of {len(both)}")
    for tname, tf in (("total+prep", t_prep), ("total", t_total), ("outer", t_outer)):
        note(f"C full SGM ({tname}) over the 9: baseline {sgm(tf(ci[('full', n, 'baseline')]) for n in both):.3f} "
             f"frozen {sgm(tf(ci[('full', n, 'all-diag-mech')]) for n in both):.3f}")
    vb = sgm(t_prep(ci[("full", n, "baseline")]) for n in both)
    vm = sgm(t_prep(ci[("full", n, "all-diag-mech")]) for n in both)
    check("C.sgm", W + " SGM time 10.3 s -> 6.7 s", "10.3 / 6.7", f"{vb:.2f} / {vm:.2f}", close("10.3", vb, 1) and close("6.7", vm, 1))
    others = [n for n in names if n not in both]
    to = all(ci[("full", n, m)]["status"] == "timelimit" for n in others for m in ("baseline", "all-diag-mech"))
    check("C.others", W + " all other instances timed out in both modes", True, to)
    # diagnostic full runs
    wsolved = [n for n in names if solved(di[("full", n, "all-diag-mech-wide")])]
    check("C.wide.solved", W + " all 20 full runs solved (wide)", 20, len(wsolved))
    ws = [t_prep(di[("full", n, "all-diag-mech-wide")]) for n in names]
    check("C.wide.secs", W + " in 3 to 39 s", "3-39", f"{min(ws):.1f}-{max(ws):.1f}",
          round(min(ws)) == 3 and round(max(ws)) == 39)
    wn = [di[("full", n, "all-diag-mech-wide")]["nodes"] for n in names]
    note(f"C wide full nodes: {wn}; at root (1 node): {sum(x == 1 for x in wn)}")
    rb = sum(solved(di[("full", n, "baseline")]) for n in names)
    check("C.rerun.base", W + " 9 of 20 for a rerun of the baseline", 9, rb)
    rs = sum(solved(di[("full", n, "all-diag-mech")]) for n in names)
    note(f"C rowdir (same limits) full solved {rs} of 20")
    # wide root runs: solved at root node?
    wr = [di[("root", n, "all-diag-mech-wide")]["status"] for n in names]
    note(f"C wide root-run statuses: {collections.Counter(wr)}")
    # cut counts and limits in the mechanism runs
    for lab, idx_, mode in (("frozen", ci, "all-diag-mech"), ("rowdir", di, "all-diag-mech"), ("wide", di, "all-diag-mech-wide")):
        cnt = [(nn[n], idx_[("root", n, mode)]["_ncuts"]) for n in names]
        note(f"C {lab} root cuts (n, cuts): {cnt}")
    # incumbents of Part C
    inc = [r for r in C if has_incumbent(r)]
    check("C.incumbents", "Sec 9.4 '80 in Part C'", 80, len(inc))
    check("C.incumbents.passed", "Sec 9.4", 80, sum(inc_passed(r) for r in inc))
    incd = [r for r in D if has_incumbent(r)]
    note(f"v3d C-rowdir incumbents {len(incd)} of {len(D)}, passed {sum(inc_passed(r) for r in incd)}")
    # Table 7 (mechanism detail)
    T7 = [
        (10, 0, "0.04980", "-0.249", "0.43", "1.00", "o 2562 3", "o 661 2", "o 1 3"),
        (10, 1, "0.01050", "-0.252", "0.28", "1.00", "o 902 1", "o 324 2", "o 1 3"),
        (10, 2, "0.01721", "-0.341", "0.35", "1.00", "o 1521 2", "o 397 2", "o 1 4"),
        (10, 3, "0.01306", "-0.288", "0.38", "1.00", "o 1064 1", "o 400 2", "o 1 3"),
        (10, 4, "0.05310", "-0.236", "0.08", "1.00", "o 792 1", "o 381 2", "o 1 3"),
        (20, 0, "0.07166", "-0.580", "0.25", "1.00", "t 382248 300", "t 402902 300", "o 1 8"),
        (20, 1, "0.03430", "-0.261", "0.22", "1.00", "o 30798 27", "o 2316 6", "o 1 7"),
        (20, 2, "0.06104", "-0.396", "0.33", "1.00", "o 166693 140", "o 69996 50", "o 1 7"),
        (20, 3, "0.06726", "-0.648", "0.28", "1.00", "o 37223 31", "o 6088 10", "o 1 7"),
        (20, 4, "0.04834", "-0.620", "0.08", "1.00", "o 210995 168", "o 202581 161", "o 1 7"),
        (40, 0, "0.07776", "-1.226", "0.27", "1.00", "t 112851 300", "t 159010 300", "o 1 16"),
        (40, 1, "0.09766", "-0.946", "0.19", "1.00", "t 157776 300", "t 160238 300", "o 1 17"),
        (40, 2, "0.08752", "-1.417", "0.33", "1.00", "t 148087 300", "t 123468 300", "o 1 16"),
        (40, 3, "0.08875", "-1.275", "0.15", "1.00", "t 116421 300", "t 131746 300", "o 1 15"),
        (40, 4, "0.09021", "-0.945", "0.19", "1.00", "t 144953 300", "t 131679 300", "o 1 16"),
        (80, 0, "0.16113", "-1.749", "0.17", "1.00", "t 58109 300", "t 53962 300", "o 1 37"),
        (80, 1, "0.21545", "-2.265", "0.33", "1.00", "t 45369 300", "t 54254 300", "o 6 38"),
        (80, 2, "0.13660", "-1.764", "0.22", "1.00", "t 63896 300", "t 59739 300", "o 1 39"),
        (80, 3, "0.17993", "-2.383", "0.33", "1.00", "t 44665 300", "t 69920 300", "o 1 38"),
        (80, 4, "0.22693", "-1.818", "0.20", "1.00", "t 58336 300", "t 56471 300", "o 2 37"),
    ]
    code = {"optimal": "o", "gaplimit": "g", "timelimit": "t"}

    def cell(r):
        return f"{code.get(r['status'], r['status'])} {r['nodes']} {round(t_prep(r)):d}"

    bad7 = []
    for (k, s, o, rb_, cf, cd, cb, cfz, cdg) in T7:
        n = next(x for x in names if nn[x] == k and sd[x] == s)
        comp = (f"{opt[n]:.5f}", f"{ci[('root', n, 'baseline')]['dual']:.3f}", f"{fr[n]:.2f}", f"{wd[n]:.2f}",
                cell(ci[("full", n, "baseline")]), cell(ci[("full", n, "all-diag-mech")]),
                cell(di[("full", n, "all-diag-mech-wide")]))
        stated = (o, rb_, cf, cd, cb, cfz, cdg)
        for col, a, b in zip(("opt", "rootbase", "closed_frozen", "closed_diag", "baseline", "frozen", "diag"), stated, comp):
            if a != b:
                # allow last-digit rounding in seconds (round-half issues) to be listed but separately
                bad7.append(f"n={k} s={s} {col}: stated '{a}' computed '{b}'")
    check("T7", "App B Table 7 (all cells)", "all equal", "; ".join(bad7) if bad7 else "all equal", not bad7)
    # alternative: rerun baseline in diagnostic column?
    alt = []
    for (k, s, *_rest) in T7:
        n = next(x for x in names if nn[x] == k and sd[x] == s)
        alt.append((k, s, cell(di[("full", n, "baseline")]), cell(di[("full", n, "all-diag-mech")])))
    note("C v3d rerun baseline / rowdir(same limits) full cells:", alt)
    return C, D, cases


def diag_AB():
    W = "Sec 9.6 diagnostic on Parts A and B"
    changes_cuts = []
    bound_changes = []
    models = 0
    for orig, var in (("partA-root", "partA-root-rowdir"), ("partB", "partB-root-rowdir")):
        o = [r for r in load(V3 / orig / "records.jsonl") if r["phase"] == "root"]
        v = load(V3D / var / "records.jsonl")
        oi = {(r["name"], r["mode"]): r for r in o}
        vi = {(r["name"], r["mode"]): r for r in v}
        nms = sorted({r["name"] for r in v})
        models += len(nms)
        for n in nms:
            for m in ("baseline", "all", "auto", "all-diag"):
                a, b = vi[(n, m)], oi[(n, m)]
                c = compare(a, b, "dual", 1e-4)
                if c != "tie":
                    bound_changes.append((var, n, m, c, b["dual"], a["dual"]))
                if m != "baseline" and a["_ncuts"] != b["_ncuts"]:
                    changes_cuts.append((var, n, m, b["_ncuts"], a["_ncuts"]))
        for m in ("all", "auto", "all-diag"):
            note(f"{var} cuts {m}: orig {sum(oi[(n, m)]['_ncuts'] or 0 for n in nms)} variant {sum(vi[(n, m)]['_ncuts'] or 0 for n in nms)}")
    check("D.models", W, 60, models)
    check("D.bounds", W + " root bounds unchanged at gap tolerance (rowdir vs original, every mode)", "[]",
          str(bound_changes), not bound_changes)
    check("D.cuts", W + " changed number of cuts in 8 of 180 cut-mode runs", 8, len(changes_cuts))
    note("D cut-count changes:", changes_cuts)


def setup_checks(parts):
    loads = []
    for recs in parts:
        for r in recs:
            for k in ("load_start", "load_end"):
                if isinstance(r.get(k), list):
                    loads.append(r[k][0])
    note(f"one-minute load over v3/v3d records: min {min(loads):.1f} max {max(loads):.1f} "
         f"median {statistics.median(loads):.1f}")
    check("Setup.load", "Sec 9.1 'one-minute load average between about 10 and 17'", "10-17",
          f"{min(loads):.1f}-{max(loads):.1f}", min(loads) >= 9.5 and max(loads) <= 17.5)


def tableB():
    """App B Table (tab:partB): every cell recomputed from v3/runs/partB."""
    tex = (PAPER / "sections/B-tables.tex").read_text()
    body = tex.split("\\label{tab:partB}")[1].split("\\bottomrule")[0].split("\\midrule")[1]
    rows = []
    for line in body.strip().splitlines():
        cells = [c.strip().rstrip("\\").strip() for c in line.split("&")]
        if len(cells) == 6:
            rows.append(cells)
    B = load(V3 / "partB/records.jsonl")
    ri = {(r["name"], r["phase"], r["seed"], r["mode"]): r for r in B}
    code = {"optimal": "o", "gaplimit": "g", "timelimit": "t"}

    def num(x):
        s = f"{x:.4g}"
        return s

    def full(r):
        return f"{code.get(r['status'], r['status'])} {t_total(r):.1f}"  # table uses total_seconds

    bad = []
    sel = json.load(open(SCAN / "partB-selection.json"))["selected"]
    order = [x["name"] for x in sel]
    names_tab = [c[0].replace("\\code{", "").replace("}", "").replace("\\_", "_") for c in rows]
    if names_tab != order:
        bad.append("row order differs from selection order")
    for c, n in zip(rows, names_tab):
        comp = [num(ri[(n, "root", 0, "baseline")]["dual"]), num(ri[(n, "root", 0, "all-diag")]["dual"]),
                full(ri[(n, "full", 0, "baseline")]), full(ri[(n, "full", 0, "all")]),
                str(ri[(n, "full", 0, "all")]["_ncuts"])]
        for col, a, b in zip(("root_base", "root_diag", "baseline", "all", "cuts"), c[1:], comp):
            same = a == b
            if not same:
                try:
                    same = float(a) == float(b)
                except ValueError:
                    pass
            if not same:
                bad.append(f"{n} {col}: stated '{a}' computed '{b}'")
    check("TB", "App B Table (tab:partB), all cells", "all equal", "; ".join(bad) if bad else "all equal", not bad)
    # time-limited and root-closed rows
    for n in ("pooling_bental4tp", "pooling_bental4pq"):
        r = ri[(n, "full", 0, "all")]
        note(f"TB {n} seed-0 full all: status {r['status']} nodes {r['nodes']} cuts {r['_ncuts']}")


def extra_notes():
    """Facts used in the methodology review (not stated in the paper)."""
    for part in ("partA-full", "partA-root", "partB", "partC"):
        agg = collections.defaultdict(collections.Counter)
        for r in load(V3 / part / "records.jsonl"):
            if r["mode"] == "baseline":
                continue
            s = r.get("separation") or {}
            k = (r["phase"], r["mode"])
            agg[k]["runs"] += 1
            agg[k]["cuts"] += r["_ncuts"] or 0
            agg[k]["row_binding_rejections"] += s.get("row_binding_rejections") or 0
            agg[k]["certification_failures"] += s.get("certification_failures") or 0
            agg[k]["budget_exhausted_runs"] += int(bool(s.get("budget_exhausted")))
        for k, c in sorted(agg.items()):
            note(f"sep stats {part} {k}: {dict(c)}")
    # Part B unshifted geometric-mean and median time ratios
    B = [r for r in load(V3 / "partB/records.jsonl") if r["phase"] == "full"]
    A = load(V3 / "partA-full/records.jsonl")
    for lab, recs, seeds in (("A", A, (0, 1, 2)), ("B", B, (0, 1))):
        idx = index(recs)
        names = sorted({r["name"] for r in recs})
        common = [(n, s) for n in names for s in seeds if all(solved(idx[(n, s, m)]) for m in ("baseline", "all", "auto"))]
        for m in ("all", "auto"):
            rr = [t_prep(idx[(n, s, m)]) / t_prep(idx[(n, s, "baseline")]) for n, s in common]
            note(f"{lab} {m}: per-run time ratio median {statistics.median(rr):.3f}, unshifted geometric mean "
                 f"{math.exp(statistics.fmean(map(math.log, rr))):.3f}, quartiles {[round(x, 2) for x in statistics.quantiles(rr, n=4)]}")
        bt = [t_prep(idx[(n, s, "baseline")]) for n, s in common]
        note(f"{lab} baseline time on common-solved runs: median {statistics.median(bt):.3f} s, under 1 s: "
             f"{sum(x < 1 for x in bt)} of {len(bt)}")


def main():
    v1 = campaign1()
    v2, rep = campaign2()
    out = campaign3()
    scan_and_selection()
    C, D, cases = partC()
    diag_AB()
    tableB()
    extra_notes()
    replay_checks()
    AR3 = load(V3D / "partA-root-rowdir/records.jsonl")
    BR3 = load(V3D / "partB-root-rowdir/records.jsonl")
    setup_checks([out["A"], out["AR"], out["B"], C, D, AR3, BR3])
    w = max(len(r[0]) for r in ROWS)
    print("# R4 recomputation: checks")
    print(f"{'id':{w}}  result    stated | computed | where")
    for cid, where, st, comp, res in ROWS:
        print(f"{cid:{w}}  {res:8}  {st} | {comp} | {where}")
    print()
    print(f"{sum(r[4] == 'PASS' for r in ROWS)} PASS, {sum(r[4] != 'PASS' for r in ROWS)} MISMATCH")
    print()
    print("# Details")
    for d in DETAILS:
        print("-", d)


if __name__ == "__main__":
    main()
