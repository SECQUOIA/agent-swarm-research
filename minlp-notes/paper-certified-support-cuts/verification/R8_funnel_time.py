"""R8: independent check of the campaign-4 separator funnel and time decomposition.

Standard library only. Reads the raw records.jsonl, jobs.json and case files of
the five finished campaign-4 parts (C2, C3, B2, D root, D full) and the
campaign-3 reference directories, recomputes the funnel, cap counts, separator
time parts, SGMs and per-run time ratios, and the native-separator activity,
and compares each number with the value written in
evidence/campaign4-digest.md. Does not import any producer code. Does not read
experiments/v4/runs/partC4.

Definitions (campaign-v4 protocol and v4/README.md):
- failed: returncode != 0, a worker_status, or a failure status;
- solved: status optimal or gaplimit, not failed, primal_check.checked and
  passed, finite primal;
- root bound: root_dual if finite; else, for a run that ended at the root
  (node_limit 1 or nodes <= 1), the final dual bound;
- completed (root phase): not failed, total_seconds present, root bound exists;
  completed (full phase): solved;
- time: total_seconds + preparation_seconds; SCIP time: scip_solve_seconds
  (Gurobi: solver_runtime_seconds); callback: separation.callback_seconds;
  SCIP time excluding the callback: SCIP time - callback;
- SGM: exp(mean(log(t + 1))) - 1 over the runs completed by every compared mode;
- funnel: below threshold = certification_calls - certification_failures -
  row_rounding_rejections - row_binding_rejections - cuts;
- caps per run, from the run's own config: cut cap cuts >= max_cuts; support
  cap certification_calls >= max_support_calls; callback cap calls >=
  max_rounds; time budget (inferred) budget_exhausted without the cut or
  support cap; discovery stopped = discovery_incomplete; none = no cap and not
  budget_exhausted.

Usage: python R8_funnel_time.py [--json OUT]
"""
from __future__ import annotations

import argparse
import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments"
V4 = EXP / "v4" / "runs"
FAILURES = ("process_timeout", "worker_error", "worker_no_output", "worker_output_parse_error")

# (label, directory, reference directory or None)
PARTS = [
    ("C2", V4 / "partC2", EXP / "v3" / "runs" / "partC"),
    ("C3", V4 / "partC3", None),
    ("B2", V4 / "partB2", EXP / "v3" / "runs" / "partB"),
    ("Droot", V4 / "partD-root", None),
    ("Dfull", V4 / "partD-full", None),
]


def load_jsonl(path):
    with open(path) as handle:
        return [json.loads(line) for line in handle if line.strip()]


def finite(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def failed(r):
    return r.get("status") in FAILURES or bool(r.get("worker_status")) or r.get("returncode", 0) != 0


def solved(r):
    pc = r.get("primal_check") or {}
    return (not failed(r) and r.get("status") in ("optimal", "gaplimit")
            and pc.get("checked") is True and pc.get("passed") is True and finite(r.get("primal")))


def root_bound(r):
    if finite(r.get("root_dual")):
        return r["root_dual"]
    at_root = r.get("node_limit") == 1 or (finite(r.get("nodes")) and r["nodes"] <= 1)
    if at_root and finite(r.get("dual")):
        return r["dual"]
    return None


def completed(r, phase):
    if r is None:
        return False
    if phase == "root":
        return not failed(r) and "total_seconds" in r and root_bound(r) is not None
    return solved(r)


def t_total(r):
    return r["total_seconds"] + r.get("preparation_seconds", 0.0)


def t_scip(r):
    if r.get("mode", "").endswith("gurobi"):
        return r["solver_runtime_seconds"]
    return r["scip_solve_seconds"]


def t_callback(r):
    return (r.get("separation") or {}).get("callback_seconds", 0.0)


def t_excl(r):
    return t_scip(r) - t_callback(r)


def sgm(values, shift=1.0):
    values = list(values)
    if not values:
        return None
    return math.exp(sum(math.log(v + shift) for v in values) / len(values)) - shift


def load_part(label, directory, refdir):
    """Return {phase: {mode: {name: record}}} and the scheduled run ids."""
    records = load_jsonl(directory / "records.jsonl")
    jobs = json.loads((directory / "jobs.json").read_text())
    scheduled = {run["run_id"] for job in jobs["jobs"] for run in job["runs"]}
    recorded = Counter(r["run_id"] for r in records)
    by = defaultdict(lambda: defaultdict(dict))
    keys = set()
    for r in records:
        assert r["seed"] == 0
        assert r["name"] not in by[r["phase"]][r["mode"]], (label, r["run_id"])
        by[r["phase"]][r["mode"]][r["name"]] = r
        keys.add((r["phase"], r["name"], r["seed"]))
    if refdir is not None:
        for r in load_jsonl(refdir / "records.jsonl"):
            if (r["phase"], r["name"], r["seed"]) in keys:
                by[r["phase"]]["c3:" + r["mode"]][r["name"]] = r
    cases = {p.stem: json.loads(p.read_text()) for p in (directory / "cases").glob("*.json")}
    return by, {"scheduled": len(scheduled), "recorded": len(records),
                "missing": sorted(scheduled - set(recorded)), "duplicates": [k for k, v in recorded.items() if v > 1],
                "cases": len(cases)}


def funnel(runs):
    out = Counter()
    causes, statuses = Counter(), Counter()
    caps = Counter()
    times = Counter()
    per_model = {}
    classifier_errors = 0
    causes_recorded = True
    for name, r in runs.items():
        s = r["separation"]
        c = r["config"]
        for key in ("calls", "certification_calls", "certification_failures", "row_rounding_rejections",
                    "row_binding_rejections", "cuts", "candidate_lps"):
            out[key] += s[key]
        out["runs"] += 1
        out["runs_with_binding"] += s["row_binding_rejections"] > 0
        out["runs_with_cuts"] += s["cuts"] > 0
        assert s["cuts"] == len(r["cuts"]), (name, r["mode"])
        below = (s["certification_calls"] - s["certification_failures"] - s["row_rounding_rejections"]
                 - s["row_binding_rejections"] - s["cuts"])
        assert below >= 0
        out["below"] += below
        rc = r.get("row_binding_rejection_causes")
        if rc is None:
            causes_recorded = False
        else:
            causes.update(rc.get("causes") or {})
            statuses.update(rc.get("variable_statuses") or {})
            classifier_errors += rc.get("classifier_errors", 0)
            assert sum((rc.get("causes") or {}).values()) == s["row_binding_rejections"]
        cut_cap = s["cuts"] >= c["max_cuts"]
        sup_cap = s["certification_calls"] >= c["max_support_calls"]
        cb_cap = s["calls"] >= c["max_rounds"]
        time_cap = s["budget_exhausted"] and not cut_cap and not sup_cap
        caps["cut_cap"] += cut_cap
        caps["support_cap"] += sup_cap
        caps["callback_cap"] += cb_cap
        caps["time_budget"] += time_cap
        caps["discovery_incomplete"] += bool(s["discovery_incomplete"])
        caps["none"] += not (cut_cap or sup_cap or cb_cap or s["budget_exhausted"])
        caps["max_rounds"] = c["max_rounds"]
        for key in ("callback_seconds", "discovery_seconds", "candidate_seconds", "certification_seconds",
                    "row_seconds"):
            times[key] += s[key]
        per_model[name] = {"support": s["certification_calls"], "fail": s["certification_failures"],
                           "binding": s["row_binding_rejections"], "cuts": s["cuts"], "calls": s["calls"],
                           "causes": dict((rc or {}).get("causes") or {}),
                           "statuses": dict((rc or {}).get("variable_statuses") or {}),
                           "callback": s["callback_seconds"], "discovery": s["discovery_seconds"],
                           "discovery_incomplete": s["discovery_incomplete"],
                           "budget_exhausted": s["budget_exhausted"],
                           "cut_cap": cut_cap, "support_cap": sup_cap, "callback_cap": cb_cap}
    return {"counts": dict(out), "causes": dict(causes) if causes_recorded else None,
            "statuses": dict(statuses) if causes_recorded else None, "caps": dict(caps),
            "times": dict(times), "per_model": per_model, "classifier_errors": classifier_errors}


def time_pair(mode_runs, ref_runs, phase):
    names = sorted(n for n in mode_runs if completed(mode_runs[n], phase) and completed(ref_runs.get(n), phase))
    if not names:
        return None
    m = [mode_runs[n] for n in names]
    f = [ref_runs[n] for n in names]
    ratios = [t_total(a) / t_total(b) for a, b in zip(m, f)]
    excl_ratios = [t_excl(a) / t_scip(b) for a, b in zip(m, f)]
    return {"pairs": len(names), "names": names,
            "sgm_total": sgm(t_total(a) for a in m), "sgm_excl": sgm(t_excl(a) for a in m),
            "sgm_callback": sgm(t_callback(a) for a in m),
            "ref_sgm_total": sgm(t_total(b) for b in f), "ref_sgm_scip": sgm(t_scip(b) for b in f),
            "median_ratio": statistics.median(ratios), "faster": sum(x < 1 for x in ratios),
            "median_excl_ratio": statistics.median(excl_ratios)}


def pooled(by_mode, modes, phase):
    names = sorted(set.intersection(*[{n for n, r in by_mode[m].items() if completed(r, phase)} for m in modes]))
    out = {"names": names}
    for m in modes:
        rs = [by_mode[m][n] for n in names]
        out[m] = {"sgm_total": sgm(t_total(r) for r in rs), "sgm_scip": sgm(t_scip(r) for r in rs),
                  "sgm_excl": sgm(t_excl(r) for r in rs), "sgm_callback": sgm(t_callback(r) for r in rs)}
    return out


def reference(mode, modes):
    if mode.endswith("-noaggr") and mode != "baseline-noaggr" and "baseline-noaggr" in modes:
        return "baseline-noaggr"
    for cand in ("baseline", "c3:baseline"):
        if cand in modes and cand != mode:
            return cand
    return None


def num(x):
    """SCIP statistics tables print '-' for not-applicable entries."""
    return x if isinstance(x, int) and not isinstance(x, bool) else 0


def native(runs):
    """Native separator activity: runs with Calls > 0, sums of Calls, FoundCuts, Applied."""
    seps = defaultdict(Counter)
    quad = Counter()
    for r in runs.values():
        ns = r.get("native_statistics")
        if not ns:
            continue
        for name, row in ns["separators"].items():
            calls = row.get("Calls")
            if not isinstance(calls, int):
                continue
            seps[name]["runs"] += calls > 0
            seps[name]["calls"] += calls
            seps[name]["found"] += num(row.get("FoundCuts"))
            seps[name]["applied"] += num(row.get("Applied"))
        q = (ns.get("nlhdlrs") or {}).get("quadratic") or {}  # sonet23v4 records hold no nlhdlr table
        quad["runs_no_nlhdlr_table"] += ns.get("nlhdlrs") is None
        quad["runs_enforce"] += num(q.get("#Enforce")) > 0
        quad["runs_cuts"] += num(q.get("Cuts")) > 0
        quad["enforce"] += num(q.get("#Enforce"))
        quad["cuts"] += num(q.get("Cuts"))
    return {k: dict(v) for k, v in seps.items()}, dict(quad)


def compute():
    res = {"parts": {}}
    for label, directory, refdir in PARTS:
        by, meta = load_part(label, directory, refdir)
        part = {"meta": meta, "phases": {}}
        for phase, by_mode in by.items():
            modes = sorted(by_mode)
            ph = {"modes": {}, "pooled": None}
            for m in modes:
                runs = by_mode[m]
                entry = {"runs": len(runs), "solved": sum(solved(r) for r in runs.values()),
                         "solved_names": sorted(n for n, r in runs.items() if solved(r)),
                         "load_start_mean": statistics.mean(r["load_start"][0] for r in runs.values())
                         if all(r.get("load_start") for r in runs.values()) else None}
                if any(r.get("separation") for r in runs.values()) and not m.endswith("gurobi") \
                        and not m.split(":")[-1].startswith("baseline"):
                    entry["funnel"] = funnel(runs)
                ref = reference(m, modes)
                if ref:
                    entry["reference"] = ref
                    entry["time"] = time_pair(runs, by_mode[ref], phase)
                entry["native"], entry["quadratic_nlhdlr"] = native(runs)
                over = [(n, t_total(r)) for n, r in runs.items() if r.get("status") == "timelimit"]
                entry["timelimit_charged"] = sorted(over, key=lambda x: x[1])
                entry["all_runs_sgm_total"] = sgm(t_total(r) for r in runs.values())
                entry["all_runs_sgm_excl"] = sgm(t_excl(r) for r in runs.values())
                entry["sum_callback"] = sum(t_callback(r) for r in runs.values())
                entry["sum_total"] = sum(t_total(r) for r in runs.values())
                entry["time_range"] = [min(t_total(r) for r in runs.values()), max(t_total(r) for r in runs.values())]
                ph["modes"][m] = entry
            ph["pooled"] = pooled(by_mode, modes, phase)
            part["phases"][phase] = ph
        part["_by"] = by
        res["parts"][label] = part
    scan = {r["name"]: r for r in load_jsonl(EXP / "v4" / "scanD" / "records.jsonl")}
    res["scan_discovery"] = {n: scan[n].get("discovery_seconds") for n in scan}
    return res


# ---------------------------------------------------------------------------
# Comparison with the digest

def decimals(text):
    text = text.replace(",", "")
    if "e" in text.lower():
        mant, exp = text.lower().split("e")
        d = len(mant.split(".")[1]) if "." in mant else 0
        return d - int(exp)
    return len(text.split(".")[1]) if "." in text else 0


def matches(digest, value):
    if isinstance(value, str) or isinstance(digest, (list, tuple)):
        return str(digest) == str(value)
    text = str(digest)
    d = decimals(text)
    return abs(float(text.replace(",", "")) - value) <= 0.5 * 10 ** (-d) + 1e-12


CHECKS = []


def check(item, digest, value):
    CHECKS.append((item, str(digest), value, matches(digest, value)))


def fmt(v):
    if isinstance(v, float):
        return f"{v:.6g}"
    return str(v)


def run_checks(res):
    P = res["parts"]

    def M(part, phase, mode):
        return P[part]["phases"][phase]["modes"][mode]

    # --- Funnel per part and cut mode (digest table "Funnel per part and cut mode")
    rows = [
        ("C2", "root", "frozen-wide", 20, 122, 13502, 0, 1189, 313, 20, {"column_set_differs_tiny_coefficient_dropped": 313}, 12000, (20, 0, 0, 0, 0)),
        ("C2", "full", "frozen-wide", 20, 122, 13502, 0, 1189, 313, 20, {"column_set_differs_tiny_coefficient_dropped": 313}, 12000, (20, 0, 0, 0, 0)),
        ("C2", "root", "c3:all-diag-mech", 20, 80, 3462, 0, 391, 71, 13, None, 3000, (20, 0, 0, 0, 0)),
        ("C2", "full", "c3:all-diag-mech", 20, 80, 3462, 0, 391, 71, 13, None, 3000, (20, 0, 0, 0, 0)),
        ("C3", "root", "all-diag-mech", 20, 80, 3558, 0, 474, 84, 16, {"column_set_differs_tiny_coefficient_dropped": 84}, 3000, (20, 0, 0, 0, 0)),
        ("C3", "full", "all-diag-mech", 20, 80, 3558, 0, 474, 84, 16, {"column_set_differs_tiny_coefficient_dropped": 84}, 3000, (20, 0, 0, 0, 0)),
        ("C3", "root", "rowdir-wide", 20, 140, 15534, 0, 3181, 353, 20, {"column_set_differs_tiny_coefficient_dropped": 353}, 12000, (20, 0, 0, 0, 0)),
        ("C3", "full", "rowdir-wide", 20, 140, 15534, 0, 3181, 353, 20, {"column_set_differs_tiny_coefficient_dropped": 353}, 12000, (20, 0, 0, 0, 0)),
        ("B2", "root", "all-noaggr", 30, 52, 446, 7, 326, 6, 5, {"coefficient_rounded_to_integer": 4, "column_set_differs_tiny_coefficient_dropped": 1, "column_set_differs_variable_not_column": 1}, 107, (0, 8, 10, 9, 0)),
        ("B2", "root", "all-diag-noaggr", 30, 210, 1572, 17, 1058, 47, 13, {"coefficient_rounded_to_integer": 17, "column_set_differs_tiny_coefficient_dropped": 16, "column_set_differs_variable_not_column": 14}, 450, (0, 0, 13, 0, 0)),
        ("B2", "root", "all-diag-rowdir-noaggr", 30, 210, 1640, 19, 1124, 47, 13, {"coefficient_rounded_to_integer": 17, "column_set_differs_tiny_coefficient_dropped": 16, "column_set_differs_variable_not_column": 14}, 450, (0, 0, 13, 0, 0)),
        ("Droot", "root", "all", 20, 22, 176, 2, 149, 11, 3, {"column_set_differs_variable_not_column": 11}, 14, (0, 6, 1, 14, 12)),
        ("Droot", "root", "all-diag", 20, 115, 6352, 313, 5042, 106, 8, {"column_set_differs_variable_not_column": 99, "coefficient_rounded_to_integer": 7}, 891, (2, 8, 8, 0, 0)),
        ("Droot", "root", "all-diag-rowdir", 20, 107, 6378, 313, 5128, 106, 8, {"column_set_differs_variable_not_column": 99, "coefficient_rounded_to_integer": 7}, 831, (2, 9, 7, 0, 0)),
        ("Dfull", "full", "all", 20, 22, 180, 2, 153, 11, 3, {"column_set_differs_variable_not_column": 11}, 14, (0, 6, 1, 14, 11)),
        ("Dfull", "full", "auto", 20, 24, 170, 0, 145, 11, 3, {"column_set_differs_variable_not_column": 11}, 14, (0, 4, 2, 15, 11)),
    ]
    for part, phase, mode, runs, calls, sup, fail, below, binding, brun, causes, cuts, caps in rows:
        f = M(part, phase, mode)["funnel"]
        c = f["counts"]
        tag = f"funnel {part} {phase} {mode}"
        check(f"{tag} runs", runs, c["runs"])
        check(f"{tag} callbacks", calls, c["calls"])
        check(f"{tag} support calls", sup, c["certification_calls"])
        check(f"{tag} cert failures", fail, c["certification_failures"])
        check(f"{tag} rounding rejections", 0, c["row_rounding_rejections"])
        check(f"{tag} below threshold", below, c["below"])
        check(f"{tag} binding rejections", binding, c["row_binding_rejections"])
        check(f"{tag} runs with binding", brun, c["runs_with_binding"])
        check(f"{tag} cuts", cuts, c["cuts"])
        if causes is not None:
            check(f"{tag} causes", json.dumps(causes, sort_keys=True), json.dumps(f["causes"], sort_keys=True))
        else:
            check(f"{tag} causes not recorded", "None", str(f["causes"]))
        k = f["caps"]
        got = (k["cut_cap"], k["support_cap"], k["callback_cap"], k["time_budget"], k["discovery_incomplete"])
        check(f"{tag} caps cut/support/callback/time/(discovery)", str(caps), str(got))
        check(f"{tag} callback cap value (digest column says 10)", 10, k["max_rounds"])

    # root = full for path family (all counters)
    for part, mode in (("C2", "frozen-wide"), ("C2", "c3:all-diag-mech"), ("C3", "all-diag-mech"), ("C3", "rowdir-wide")):
        a = M(part, "root", mode)["funnel"]["per_model"]
        b = M(part, "full", mode)["funnel"]["per_model"]
        same = all({k: v for k, v in a[n].items() if k not in ("callback", "discovery")} ==
                   {k: v for k, v in b[n].items() if k not in ("callback", "discovery")} for n in a)
        check(f"root and full funnel identical per run {part} {mode}", "True", str(same))

    # B2 extra funnel numbers (B2 table)
    for mode, sup, fail, below, binding, brun, cuts in (("c3:all", 436, 7, 316, 23, 9, 90), ("c3:all-diag", 1618, 19, 1039, 202, 17, 358)):
        c = M("B2", "root", mode)["funnel"]["counts"]
        check(f"B2 {mode} support calls", sup, c["certification_calls"])
        check(f"B2 {mode} cert failures", fail, c["certification_failures"])
        check(f"B2 {mode} below threshold", below, c["below"])
        check(f"B2 {mode} binding (runs)", f"{binding} ({brun})", f"{c['row_binding_rejections']} ({c['runs_with_binding']})")
        check(f"B2 {mode} cuts", cuts, c["cuts"])
        check(f"B2 {mode} causes recorded", "None", str(M("B2", "root", mode)["funnel"]["causes"]))
    shares = {"c3:all": "20.4", "all-noaggr": "5.3", "c3:all-diag": "36.1", "all-diag-noaggr": "9.5", "all-diag-rowdir-noaggr": "9.5"}
    for mode, s in shares.items():
        c = M("B2", "root", mode)["funnel"]["counts"]
        check(f"B2 {mode} share binding/(binding+cuts) %", s, 100 * c["row_binding_rejections"] / (c["row_binding_rejections"] + c["cuts"]))
    check("B2 all-noaggr rejected-row variable statuses", '{"FIXED": 1}', json.dumps(M("B2", "root", "all-noaggr")["funnel"]["statuses"], sort_keys=True))
    check("B2 all-diag-noaggr rejected-row variable statuses", '{"FIXED": 17}', json.dumps(M("B2", "root", "all-diag-noaggr")["funnel"]["statuses"], sort_keys=True))
    check("B2 all-diag-rowdir-noaggr rejected-row variable statuses", '{"FIXED": 17}', json.dumps(M("B2", "root", "all-diag-rowdir-noaggr")["funnel"]["statuses"], sort_keys=True))
    # B2 per-model (binding/cuts c3:all-diag -> all-diag-noaggr)
    pm_c3 = M("B2", "root", "c3:all-diag")["funnel"]["per_model"]
    pm_v4 = M("B2", "root", "all-diag-noaggr")["funnel"]["per_model"]
    pm_rd = M("B2", "root", "all-diag-rowdir-noaggr")["funnel"]["per_model"]
    for name, d in (("kall_circlespolygons_c1p12", "127/25 -> 0/104"), ("pooling_adhya4tp", "17/29 -> 17/29"),
                    ("bayes2_50", "17/8 -> 12/8"), ("bayes2_30", "3/0 -> 3/0"), ("pooling_rt2tp", "4/46 -> 4/46")):
        a, b = pm_c3[name], pm_v4[name]
        check(f"B2 per model binding/cuts {name}", d, f"{a['binding']}/{a['cuts']} -> {b['binding']}/{b['cuts']}")
    check("B2 pooling_adhya4tp all-diag-noaggr causes (14 fixed-variable, 3 integer snaps)",
          json.dumps({"coefficient_rounded_to_integer": 3, "column_set_differs_variable_not_column": 14}, sort_keys=True),
          json.dumps(pm_v4["pooling_adhya4tp"]["causes"], sort_keys=True))
    check("B2 bayes2_50 all-diag-noaggr causes (all tiny)", json.dumps({"column_set_differs_tiny_coefficient_dropped": 12}),
          json.dumps(pm_v4["bayes2_50"]["causes"], sort_keys=True))
    check("B2 bayes2_30 all-diag-noaggr causes (tiny)", json.dumps({"column_set_differs_tiny_coefficient_dropped": 3}),
          json.dumps(pm_v4["bayes2_30"]["causes"], sort_keys=True))
    check("B2 pooling_rt2tp all-diag-noaggr causes (integer snaps)", json.dumps({"coefficient_rounded_to_integer": 4}),
          json.dumps(pm_v4["pooling_rt2tp"]["causes"], sort_keys=True))
    rowdir_same = all((pm_v4[n]["binding"], pm_v4[n]["cuts"], pm_v4[n]["causes"]) == (pm_rd[n]["binding"], pm_rd[n]["cuts"], pm_rd[n]["causes"]) for n in pm_v4)
    check("B2 rowdir per-model binding, cuts, causes equal all-diag-noaggr", "True", str(rowdir_same))

    def fails(part, phase, mode):
        pm = M(part, phase, mode)["funnel"]["per_model"]
        return json.dumps({n: v["fail"] for n, v in sorted(pm.items()) if v["fail"]}, sort_keys=True)
    check("B2 cert failures per model all-noaggr", json.dumps({"ex8_1_7": 7}), fails("B2", "root", "all-noaggr"))
    check("B2 cert failures per model all-diag-noaggr", json.dumps({"ex8_1_7": 9, "tanksize": 8}, sort_keys=True), fails("B2", "root", "all-diag-noaggr"))
    check("B2 cert failures per model all-diag-rowdir-noaggr", json.dumps({"ex8_1_7": 11, "tanksize": 8}, sort_keys=True), fails("B2", "root", "all-diag-rowdir-noaggr"))
    check("B2 cert failures per model c3:all", json.dumps({"ex8_1_7": 7}), fails("B2", "root", "c3:all"))
    check("B2 cert failures per model c3:all-diag", json.dumps({"ex8_1_7": 9, "tanksize": 10}, sort_keys=True), fails("B2", "root", "c3:all-diag"))
    for mode, none in (("all-noaggr", 4), ("all-diag-noaggr", 17), ("all-diag-rowdir-noaggr", 17)):
        check(f"B2 {mode} runs hitting no cap", none, M("B2", "root", mode)["funnel"]["caps"]["none"])

    # --- Part D root funnel extras
    tparts = {"all": (18.4, 15.7, 0.4, 1.8), "all-diag": (188.4, 53.6, 22.8, 69.8), "all-diag-rowdir": (190.8, 53.1, 20.8, 73.1)}
    for mode, (cb, disc, cand, cert) in tparts.items():
        t = M("Droot", "root", mode)["funnel"]["times"]
        check(f"Droot {mode} sum callback s", f"{cb}", t["callback_seconds"])
        check(f"Droot {mode} sum discovery s", f"{disc}", t["discovery_seconds"])
        check(f"Droot {mode} sum candidate-LP s", f"{cand}", t["candidate_seconds"])
        check(f"Droot {mode} sum certification s", f"{cert}", t["certification_seconds"])
    check("Droot all cert failures per model", json.dumps({"kriging_peaks-full100": 2}), fails("Droot", "root", "all"))
    check("Droot all-diag cert failures per model", json.dumps({"kall_ellipsoids_tc02b": 3, "kall_ellipsoids_tc05a": 3, "kriging_peaks-full100": 307}, sort_keys=True), fails("Droot", "root", "all-diag"))
    check("Droot all-diag-rowdir cert failures per model (same models)", fails("Droot", "root", "all-diag"), fails("Droot", "root", "all-diag-rowdir"))
    pm = M("Droot", "root", "all")["funnel"]["per_model"]
    check("Droot all binding per model", json.dumps({"blend718": 5, "kall_circlesrectangles_c6r1": 3, "multiplants_mtg1c": 3}, sort_keys=True),
          json.dumps({n: v["binding"] for n, v in sorted(pm.items()) if v["binding"]}, sort_keys=True))
    check("Droot all cuts per model", json.dumps({"kall_ellipsoids_tc02b": 11, "kriging_peaks-full100": 3}, sort_keys=True),
          json.dumps({n: v["cuts"] for n, v in sorted(pm.items()) if v["cuts"]}, sort_keys=True))
    check("Droot all-diag rejected-row statuses", json.dumps({"AGGREGATED": 85, "FIXED": 109}, sort_keys=True),
          json.dumps(M("Droot", "root", "all-diag")["funnel"]["statuses"], sort_keys=True))
    check("Droot all-diag-rowdir causes (same as all-diag)", json.dumps(M("Droot", "root", "all-diag")["funnel"]["causes"], sort_keys=True),
          json.dumps(M("Droot", "root", "all-diag-rowdir")["funnel"]["causes"], sort_keys=True))
    pmd = M("Droot", "root", "all-diag")["funnel"]["per_model"]
    digest_cuts = {"kall_ellipsoids_tc05a": 200, "kall_ellipsoids_tc02b": 200, "kall_circlespolygons_c1p5b": 143, "hydroenergy2": 133,
                   "pooling_sppa0stp": 54, "pooling_sppa0pq": 42, "multiplants_mtg6": 40, "kall_circlesrectangles_c6r1": 36,
                   "crudeoil_li03": 31, "multiplants_mtg1a": 4, "multiplants_mtg1c": 4, "kriging_peaks-full100": 3, "blend718": 1}
    check("Droot all-diag cuts per model", json.dumps(digest_cuts, sort_keys=True), json.dumps({n: v["cuts"] for n, v in sorted(pmd.items()) if v["cuts"]}, sort_keys=True))
    check("Droot all-diag models with cuts", 13, M("Droot", "root", "all-diag")["funnel"]["counts"]["runs_with_cuts"])
    check("Droot all-diag-rowdir models with cuts", 13, M("Droot", "root", "all-diag-rowdir")["funnel"]["counts"]["runs_with_cuts"])
    check("Droot all-diag-rowdir hydroenergy2 cuts", 73, M("Droot", "root", "all-diag-rowdir")["funnel"]["per_model"]["hydroenergy2"]["cuts"])
    for mode, none in (("all-diag", 2), ("all-diag-rowdir", 2)):
        check(f"Droot {mode} runs hitting no cap", none, M("Droot", "root", mode)["funnel"]["caps"]["none"])
    disc12 = ["blend480", "kall_ellipsoids_tc05a", "pooling_sppa0stp", "ringpack_20_2", "mpbp_31", "hydroenergy2", "pooling_sppa0pq",
              "kall_circlespolygons_c1p5b", "sonet23v4", "ringpack_20_1", "crudeoil_li03", "multiplants_mtg6"]
    inc = sorted(n for n, v in pm.items() if v["discovery_incomplete"])
    check("Droot all discovery-incomplete models", json.dumps(sorted(disc12)), json.dumps(inc))
    slow = sorted(n for n in pm if res["scan_discovery"][n] > 1.0)
    check("Droot all: discovery-incomplete set equals scan discovery > 1 s", "True", str(slow == inc))
    sd = [res["scan_discovery"][n] for n in slow]
    check("scan discovery_seconds of the 12, min", "1.01", min(sd))
    check("scan discovery_seconds of the 12, max", "7.70", max(sd))
    cbs = [pm[n]["callback"] for n in inc]
    check("Droot all: callback on the 12 discovery-stopped, min (digest 1.0)", "1.0", min(cbs))
    check("Droot all: callback on the 12 discovery-stopped, max (digest 1.0)", "1.0", max(cbs))
    check("Droot all: support calls on the 12 discovery-stopped", 0, sum(pm[n]["support"] for n in inc))
    comp = [n for n in pm if not pm[n]["discovery_incomplete"]]
    check("Droot all: models with completed discovery", 8, len(comp))
    check("Droot all: of those, models with cuts", 2, sum(pm[n]["cuts"] > 0 for n in comp))
    nocut = [pm[n]["support"] for n in comp if pm[n]["cuts"] == 0]
    check("Droot all: support calls on completed-discovery models without cuts, min", 21, min(nocut))
    check("Droot all: support calls on completed-discovery models without cuts, max", 24, max(nocut))
    for mode in ("all", "auto"):
        pf = M("Dfull", "full", mode)["funnel"]["per_model"]
        incf = sorted(n for n, v in pf.items() if v["discovery_incomplete"])
        check(f"Dfull {mode} discovery-incomplete = root set minus multiplants_mtg6",
              json.dumps(sorted(set(disc12) - {"multiplants_mtg6"})), json.dumps(incf))
        check(f"Dfull {mode} cuts per model", json.dumps({"kall_ellipsoids_tc02b": 11, "kriging_peaks-full100": 3}, sort_keys=True),
              json.dumps({n: v["cuts"] for n, v in sorted(pf.items()) if v["cuts"]}, sort_keys=True))
        check(f"Dfull {mode} summed callback s", "18.8", M("Dfull", "full", mode)["sum_callback"])
    check("scan discovery multiplants_mtg6", "1.31", res["scan_discovery"]["multiplants_mtg6"])

    # --- Time decomposition table
    trows = [
        ("C2", "root", "c3:all-diag-mech", 20, "4.077", "1.198", "2.913", "1.099", "1.022", "1.18", "3.99"),
        ("C2", "root", "frozen-wide", 20, "10.06", "1.161", "8.956", "1.099", "1.022", "1.19", "9.49"),
        ("C2", "full", "c3:all-diag-mech", 9, "6.661", "4.692", "1.249", "10.27", "10.17", "0.395", "0.773"),
        ("C2", "full", "frozen-wide", 9, "5.166", "1.247", "3.828", "10.27", "10.17", "0.144", "1.171"),
        ("C3", "root", "all-diag-mech", 20, "3.795", "1.140", "2.698", "1.062", "0.990", "1.21", "3.94"),
        ("C3", "root", "rowdir-wide", 20, "10.25", "0.391", "9.863", "1.062", "0.990", "0.330", "10.99"),
        ("C3", "full", "all-diag-mech", 9, "7.267", "5.605", "1.152", "9.379", "9.284", "0.783", "0.858"),
        ("C3", "full", "rowdir-wide", 9, "4.434", "0.1405", "4.252", "9.379", "9.284", "0.0369", "0.860"),
        ("B2", "root", "all-noaggr", 30, "0.6493", "0.1461", "0.4772", "0.1949", "0.1511", "0.997", "3.91"),
        ("B2", "root", "all-diag-noaggr", 30, "1.184", "0.1494", "1.023", "0.1949", "0.1511", "1.005", "7.28"),
        ("B2", "root", "all-diag-rowdir-noaggr", 30, "1.240", "0.1465", "1.082", "0.1949", "0.1511", "0.958", "7.51"),
        ("Droot", "root", "all", 20, "11.09", "9.084", "0.911", "10.07", "9.22", "0.995", "1.106"),
        ("Droot", "root", "all-diag", 20, "17.76", "8.572", "6.838", "10.07", "9.22", "0.996", "2.134"),
        ("Droot", "root", "all-diag-rowdir", 20, "17.92", "8.614", "6.940", "10.07", "9.22", "0.987", "2.161"),
        ("Dfull", "full", "all", 1, "63.70", "62.28", "1.0", "63.36", "62.91", "0.990", "1.005"),
        ("Dfull", "full", "auto", 1, "62.62", "61.14", "1.0", "63.36", "62.91", "0.972", "0.988"),
    ]
    for part, phase, mode, pairs, st, se, sc, rt, rs, mx, mt in trows:
        t = M(part, phase, mode)["time"]
        tag = f"timedec {part} {phase} {mode}"
        check(f"{tag} pairs", pairs, t["pairs"])
        check(f"{tag} SGM total", st, t["sgm_total"])
        check(f"{tag} SGM SCIP excl callback", se, t["sgm_excl"])
        check(f"{tag} SGM callback", sc, t["sgm_callback"])
        check(f"{tag} ref SGM total", rt, t["ref_sgm_total"])
        check(f"{tag} ref SGM SCIP", rs, t["ref_sgm_scip"])
        check(f"{tag} median SCIP-excl / ref SCIP", mx, t["median_excl_ratio"])
        check(f"{tag} median total / ref", mt, t["median_ratio"])

    # --- C2 full times (7 common instances), ratios, 9-pair SGMs
    c2 = P["C2"]["phases"]["full"]
    pool = c2["pooled"]
    check("C2 full: instances solved by all six modes", 7, len(pool["names"]))
    for mode, v in (("c3:baseline", "5.597"), ("c3:all-diag-mech", "3.727"), ("baseline-novarlocks", "2.709"),
                    ("baseline-extra", "4.030"), ("frozen-wide", "4.623"), ("gurobi", "6.321")):
        check(f"C2 full pooled SGM (7) {mode}", v, pool[mode]["sgm_total"])
    for mode, med, pairs, faster in (("c3:all-diag-mech", "0.773", 9, 6), ("baseline-novarlocks", "0.384", 9, 8),
                                     ("baseline-extra", "0.482", 9, 7), ("frozen-wide", "1.171", 9, 4), ("gurobi", "0.256", 7, 4)):
        t = c2["modes"][mode]["time"]
        check(f"C2 full ratio median vs c3:baseline {mode}", med, t["median_ratio"])
        check(f"C2 full ratio (pairs; faster) {mode}", f"({pairs}; {faster})", f"({t['pairs']}; {t['faster']})")
    for mode, v in (("c3:all-diag-mech", "6.661"), ("baseline-novarlocks", "4.817"), ("baseline-extra", "6.531"), ("frozen-wide", "5.166")):
        t = c2["modes"][mode]["time"]
        check(f"C2 full 9-pair SGM {mode}", v, t["sgm_total"])
        check(f"C2 full 9-pair SGM c3:baseline (with {mode})", "10.270", t["ref_sgm_total"])
    t = c2["modes"]["gurobi"]["time"]
    check("C2 full gurobi SGM on its pairs", "6.321", t["sgm_total"])
    check("C2 full c3:baseline SGM on gurobi pairs", "5.597", t["ref_sgm_total"])

    # --- C3 full times
    c3 = P["C3"]["phases"]["full"]
    pool = c3["pooled"]
    check("C3 full: instances solved by all five modes", 5, len(pool["names"]))
    for mode, v, vx, key in (("baseline", "1.698", "1.656", "sgm_scip"), ("all-diag-mech", "2.104", "1.202", "sgm_excl"),
                             ("rowdir-wide", "3.284", "0.1238", "sgm_excl"), ("baseline-extra", "1.061", "1.026", "sgm_scip"),
                             ("gurobi", "0.334", "0.330", "sgm_scip")):
        check(f"C3 full pooled SGM (5) {mode}", v, pool[mode]["sgm_total"])
        check(f"C3 full pooled SGM (5) {mode} {key}", vx, pool[mode][key])
    for mode, med, pairs, faster in (("all-diag-mech", "0.858", 9, 5), ("rowdir-wide", "0.860", 9, 5),
                                     ("baseline-extra", "0.627", 9, 6), ("gurobi", "0.235", 5, 5)):
        t = c3["modes"][mode]["time"]
        check(f"C3 full ratio median vs baseline {mode}", med, t["median_ratio"])
        check(f"C3 full ratio (pairs; faster) {mode}", f"({pairs}; {faster})", f"({t['pairs']}; {t['faster']})")
    for mode, v in (("all-diag-mech", "7.267"), ("rowdir-wide", "4.434"), ("baseline-extra", "7.067")):
        t = c3["modes"][mode]["time"]
        check(f"C3 full 9-pair SGM {mode}", v, t["sgm_total"])
        check(f"C3 full 9-pair SGM baseline (with {mode})", "9.379", t["ref_sgm_total"])
    rw = c3["modes"]["rowdir-wide"]
    check("C3 full rowdir-wide SGM over all 20 runs", "10.19", rw["all_runs_sgm_total"])
    check("C3 full rowdir-wide min time", "3.17", rw["time_range"][0])
    check("C3 full rowdir-wide max time", "33.17", rw["time_range"][1])
    by = P["C3"]["_by"]["full"]["rowdir-wide"]
    n80 = [t_total(r) for n, r in by.items() if "_n80_" in n]
    check("C3 full rowdir-wide n80 min time", "31.7", min(n80))
    check("C3 full rowdir-wide n80 max time", "33.2", max(n80))
    check("C3 full rowdir-wide summed callback", "268.6", rw["sum_callback"])
    check("C3 full rowdir-wide summed time charged", "279.7", rw["sum_total"])
    check("C3 full rowdir-wide max nodes", 38, max(r["nodes"] for r in by.values()))

    # --- D full SGMs
    dfu = P["Dfull"]["phases"]["full"]
    check("Dfull instances solved by all four modes", '["blend480"]', json.dumps(dfu["pooled"]["names"]))
    for mode, v in (("baseline", "63.36"), ("all", "63.70"), ("auto", "62.62"), ("baseline-extra", "49.54")):
        check(f"Dfull pooled (blend480) SGM {mode}", v, dfu["pooled"][mode]["sgm_total"])
    for mode, v, cb in (("all", "62.28", "1.0"), ("auto", "61.14", "1.0")):
        check(f"Dfull pooled (blend480) SCIP excl {mode}", v, dfu["pooled"][mode]["sgm_excl"])
        check(f"Dfull pooled (blend480) callback {mode}", cb, dfu["pooled"][mode]["sgm_callback"])
    for mode, v, vx in (("baseline", "275.8", None), ("all", "276.4", "274.3"), ("auto", "276.2", "274.1"), ("baseline-extra", "274.5", None)):
        check(f"Dfull SGM over all 20 runs {mode}", v, dfu["modes"][mode]["all_runs_sgm_total"])
        if vx:
            check(f"Dfull SGM SCIP excl over all 20 runs {mode}", vx, dfu["modes"][mode]["all_runs_sgm_excl"])

    # --- Non-cut comparators (root median total ratio) and novarlocks
    for part, v in (("C2", "1.196"), ("C3", "1.262"), ("B2", "1.289"), ("Droot", "1.396")):
        t = M(part, "root", "baseline-extra")["time"]
        check(f"{part} root baseline-extra median total ratio vs {M(part, 'root', 'baseline-extra')['reference']}", v, t["median_ratio"])
    check("C2 root novarlocks median total ratio", "0.229", M("C2", "root", "baseline-novarlocks")["time"]["median_ratio"])
    check("C2 full novarlocks median total ratio", "0.384", M("C2", "full", "baseline-novarlocks")["time"]["median_ratio"])
    rp = P["C2"]["phases"]["root"]["pooled"]
    check("C2 root pooled SGM novarlocks", "0.341", rp["baseline-novarlocks"]["sgm_total"])
    check("C2 root pooled SGM c3:baseline", "1.099", rp["c3:baseline"]["sgm_total"])

    # --- Native separators
    ns, q = M("B2", "root", "baseline-extra")["native"], M("B2", "root", "baseline-extra")["quadratic_nlhdlr"]
    for sep, d in (("interminor", (21, 939, 429680, 1985)), ("rlt", (27, 229, 208, 9)), ("minor", (4, 145, 320, 110)),
                   ("eccuts", (0, 0, 0, 0))):
        s = ns[sep]
        check(f"B2 baseline-extra native {sep} runs/calls/found/applied", str(d), str((s["runs"], s["calls"], s["found"], s["applied"])))
    check("B2 baseline-extra intersection (quadratic nlhdlr) runs with cuts/enforce/cuts", str((26, 24141, 6829)),
          str((q["runs_cuts"], q["enforce"], q["cuts"])))
    check("B2 baseline-extra quadratic nlhdlr runs with enforcement calls", 26, q["runs_enforce"])
    ns, q = M("B2", "root", "baseline-noaggr")["native"], M("B2", "root", "baseline-noaggr")["quadratic_nlhdlr"]
    check("B2 baseline-noaggr interminor runs", 0, ns["interminor"]["runs"])
    check("B2 baseline-noaggr intersection cuts", 0, q["cuts"])
    check("B2 baseline-noaggr minor runs/calls/found/applied", str((4, 54, 71, 36)),
          str((ns["minor"]["runs"], ns["minor"]["calls"], ns["minor"]["found"], ns["minor"]["applied"])))
    check("B2 baseline-noaggr rlt runs/calls/found/applied", str((27, 164, 129, 5)),
          str((ns["rlt"]["runs"], ns["rlt"]["calls"], ns["rlt"]["found"], ns["rlt"]["applied"])))
    for part, calls, cuts in (("C2", 29210, 14907), ("C3", 31490, 14875)):
        e = M(part, "root", "baseline-extra")
        ns, q = e["native"], e["quadratic_nlhdlr"]
        check(f"{part} root baseline-extra intersection runs/enforce/cuts", str((20, calls, cuts)), str((q["runs_cuts"], q["enforce"], q["cuts"])))
        check(f"{part} root baseline-extra interminor calls", 0, ns["interminor"]["calls"])
        check(f"{part} root baseline-extra eccuts calls", 0, ns["eccuts"]["calls"])
        check(f"{part} root baseline-extra rlt calls/found", str((200, 0)), str((ns["rlt"]["calls"], ns["rlt"]["found"])))
        check(f"{part} root baseline-extra minor calls", 0, ns["minor"]["calls"])
    nv = M("C2", "root", "baseline-novarlocks")["native"]["minor"]
    check("C2 root novarlocks minor runs/calls/found/applied", str((20, 661, 34061, 17039)), str((nv["runs"], nv["calls"], nv["found"], nv["applied"])))
    others = []
    for part in ("C2", "C3"):
        for phase, ph in P[part]["phases"].items():
            for mode, e in ph["modes"].items():
                if mode == "baseline-novarlocks" or mode.startswith("c3:") or mode == "gurobi":
                    continue
                if e["native"].get("minor", {}).get("runs", 0):
                    others.append(f"{part}/{phase}/{mode}")
    check("minor productive in any other C2/C3 SCIP mode (root or full)", "[]", json.dumps(others))
    check("C2 full novarlocks minor runs productive", 20, M("C2", "full", "baseline-novarlocks")["native"]["minor"]["runs"])
    c3native = any(r.get("native_statistics") for n, r in P["C2"]["_by"]["root"]["c3:baseline"].items())
    check("campaign-3 records hold native statistics", "False", str(c3native))

    # --- Load and overshoots (timing context)
    for part, phase, mode, v in (("C2", "full", "c3:baseline", "16.0"), ("B2", "root", "c3:baseline", "16.3")):
        check(f"{part} {phase} {mode} load_start_mean", v, M(part, phase, mode)["load_start_mean"])
    lo = [M("C2", "full", m)["load_start_mean"] for m in ("baseline-novarlocks", "baseline-extra", "frozen-wide", "gurobi")]
    check("C2 full campaign-4 modes load_start_mean min", "6.49", min(lo))
    check("C2 full campaign-4 modes load_start_mean max", "6.90", max(lo))
    alll = [e["load_start_mean"] for part in P for ph in P[part]["phases"].values() for m, e in ph["modes"].items()
            if not m.startswith("c3:")]
    check("campaign-4 load_start_mean min (digest 3.5)", "3.5", min(alll))
    check("campaign-4 load_start_mean max (digest 7.7)", "7.7", max(alll))
    every = []
    for part, phase, cnt in (("C2", "full", 40), ("C3", "full", 47), ("Dfull", "full", 73)):
        tl = [x for m, e in P[part]["phases"][phase]["modes"].items() if not m.startswith("c3:") for x in e["timelimit_charged"]]
        check(f"{part} 300 s time-limit runs", cnt, len(tl))
        every += [x[1] for x in tl]
    check("300 s time-limit runs (C2, C3, D full): min charged time", "300.19", min(every))
    check("300 s time-limit runs (C2, C3, D full): max charged time", "300.36", max(every))
    tl = [(m, x) for m, e in P["Droot"]["phases"]["root"]["modes"].items() for x in e["timelimit_charged"]]
    check("Droot max charged time of 120 s time-limit runs", "124.49", max(x[1][1] for x in tl))
    top = max(tl, key=lambda y: y[1][1])
    check("Droot max charged run", "baseline-extra kall_circlespolygons_c1p5b", f"{top[0]} {top[1][0]}")
    check("Droot 120 s time-limit runs (mode, model)",
          json.dumps(sorted([["all", "kall_ellipsoids_tc05a"], ["baseline", "kall_ellipsoids_tc05a"],
                             ["baseline-extra", "kall_circlespolygons_c1p5b"], ["baseline-extra", "kall_ellipsoids_tc05a"],
                             ["baseline-extra", "ringpack_20_2"]])),
          json.dumps(sorted([[m, x[0]] for m, x in tl])))
    best = max(((m, x) for m, e in P["Dfull"]["phases"]["full"]["modes"].items() for x in e["timelimit_charged"]), key=lambda y: y[1][1])
    check("Dfull max charged run", "baseline-extra kriging_peaks-full100", f"{best[0]} {best[1][0]}")

    # --- Further funnel statements
    for mode in ("c3:all", "c3:all-diag"):
        check(f"B2 {mode} rounding rejections", 0, M("B2", "root", mode)["funnel"]["counts"]["row_rounding_rejections"])
    for mode, v in (("all-noaggr", 5), ("all-diag-noaggr", 33)):
        ca = M("B2", "root", mode)["funnel"]["causes"]
        check(f"B2 {mode} SCIP coefficient handling (rounded + tiny)", v,
              ca.get("coefficient_rounded_to_integer", 0) + ca.get("column_set_differs_tiny_coefficient_dropped", 0))
    # Solved counts that define the full-run SGM sets
    for part, mode, v in (("C2", "c3:baseline", 9), ("C2", "c3:all-diag-mech", 9), ("C2", "baseline-novarlocks", 10),
                          ("C2", "baseline-extra", 10), ("C2", "frozen-wide", 13), ("C2", "gurobi", 7),
                          ("C3", "baseline", 9), ("C3", "all-diag-mech", 10), ("C3", "rowdir-wide", 20),
                          ("C3", "baseline-extra", 9), ("C3", "gurobi", 5),
                          ("Dfull", "baseline", 2), ("Dfull", "all", 2), ("Dfull", "auto", 2), ("Dfull", "baseline-extra", 1)):
        check(f"{part} full solved {mode}", v, M(part, "full", mode)["solved"])

    # --- Run counts (meta)
    for part, sched in (("C2", 140), ("C3", 180), ("B2", 150), ("Droot", 100), ("Dfull", 80)):
        m = P[part]["meta"]
        check(f"{part} scheduled/recorded/missing", f"{sched}/{sched}/0", f"{m['scheduled']}/{m['recorded']}/{len(m['missing'])}")
    ce = sum(e["funnel"]["classifier_errors"] for part in P for ph in P[part]["phases"].values()
             for e in ph["modes"].values() if "funnel" in e)
    check("classifier_errors in rejection-cause records", 0, ce)


def extras(res):
    """Numbers in the focus area that the digest does not give."""
    P = res["parts"]
    lines = []
    for part, ph in P.items():
        for phase, d in ph["phases"].items():
            for mode, e in d["modes"].items():
                if "funnel" in e:
                    t = e["funnel"]["times"]
                    c = e["funnel"]["counts"]
                    lines.append(f"callback parts {part} {phase} {mode}: callback {t['callback_seconds']:.1f} s, discovery "
                                 f"{t['discovery_seconds']:.1f}, direction LPs {t['candidate_seconds']:.1f} ({c['candidate_lps']} LPs), "
                                 f"certification {t['certification_seconds']:.1f}, row insertion {t['row_seconds']:.2f}, "
                                 f"other {t['callback_seconds'] - t['discovery_seconds'] - t['candidate_seconds'] - t['certification_seconds'] - t['row_seconds']:.1f}")
    for part, phase in (("Droot", "root"), ("Dfull", "full")):
        for mode in ("baseline", "baseline-extra"):
            e = P[part]["phases"][phase]["modes"][mode]
            ns, q = e["native"], e["quadratic_nlhdlr"]
            parts = [f"{k} {ns[k]['runs']}/{ns[k]['calls']}/{ns[k]['found']}/{ns[k]['applied']}" for k in ("interminor", "rlt", "minor", "eccuts")]
            lines.append(f"native {part} {mode} (runs/calls/found/applied): " + "; ".join(parts) +
                         f"; quadratic nlhdlr runs with cuts {q['runs_cuts']}, enforce {q['enforce']}, cuts {q['cuts']}; "
                         f"runs without nlhdlr table {q.get('runs_no_nlhdlr_table', 0)}")
    neg = []
    for part, ph in P.items():
        for phase, by_mode in ph["_by"].items():
            for mode, runs in by_mode.items():
                for n, r in runs.items():
                    if r.get("separation") and not mode.endswith("gurobi") and t_excl(r) < 0:
                        neg.append(f"{part}/{phase}/{mode}/{n}: SCIP {t_scip(r):.4f} s < callback {t_callback(r):.4f} s")
    lines.append("runs with callback > SCIP time: " + ("; ".join(neg) if neg else "none"))
    for part, ph in P.items():
        for phase, d in ph["phases"].items():
            lines.append(f"load_start_mean {part} {phase}: " + ", ".join(
                f"{m} {e['load_start_mean']:.2f}" for m, e in sorted(d["modes"].items()) if e["load_start_mean"] is not None))
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="write computed values to this file")
    args = ap.parse_args()
    res = compute()
    run_checks(res)
    bad = [c for c in CHECKS if not c[3]]
    print(f"checks: {len(CHECKS)}  matching: {len(CHECKS) - len(bad)}  mismatching: {len(bad)}")
    for item, digest, value, ok in CHECKS:
        print(("OK  " if ok else "DIFF"), item, "| digest:", digest, "| recomputed:", fmt(value))
    print("\nNot in the digest (focus area):")
    for line in extras(res):
        print(" ", line)
    if args.json:
        slim = {k: {kk: vv for kk, vv in v.items() if kk != "_by"} for k, v in res["parts"].items()}
        Path(args.json).write_text(json.dumps(slim, indent=1, default=str))


if __name__ == "__main__":
    main()
