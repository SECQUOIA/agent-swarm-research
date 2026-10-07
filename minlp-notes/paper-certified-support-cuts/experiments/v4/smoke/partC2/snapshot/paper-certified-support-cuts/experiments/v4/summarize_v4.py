"""Compute the campaign-4 metrics for one or more output directories.

    summarize_v4.py DIR[=REFERENCE_DIR] [...] --dest DEST

Writes DEST/summary.json and DEST/results.md (derived files, regenerated on
each call). Campaign-3 directories (v3, v3d) are accepted too, so that the
separator funnel and time decomposition can be reported for every cut mode of
campaigns 3 and 4. ``DIR=REFERENCE_DIR`` adds the reference directory's
records of the same (phase, model, seed) as modes ``c3:<mode>``: Part C2 has
no baseline of its own and uses the campaign-3 Part C runs
(``partC2=../v3/runs/partC``); Part B2 uses the campaign-3 Part B root runs.

Every scheduled run is counted; missing records, worker errors and timeouts
are reported, not dropped. Definitions (campaign-v3/v4 protocols, Metrics):

- solved: status optimal or gaplimit, worker exited normally, and an
  incumbent that passed the independent original-model check (1e-5);
- time: total_seconds + preparation_seconds (the time charged to the soft
  budget); SCIP time: SCIP's solving time (Gurobi: Runtime); separator
  callback: separation.callback_seconds (discovery included); SCIP time
  excluding the callback: their difference;
- SGM: shifted geometric mean, shift 1 s, over the (model, seed) pairs that
  every mode of the phase solved (full and screen phases) or completed
  without failure (root phases);
- time ratio: mode / reference per (model, seed), over the pairs that both
  completed in that sense; median and geometric mean;
- reference of a mode: baseline-noaggr for the other -noaggr modes, else
  baseline, else c3:baseline;
- bounds: per (model, seed), mode versus its reference, final dual bound for
  full runs and root bound for root runs, better/worse beyond
  rtol * max(1, |a|, |b|) for rtol 1e-4 and 1e-6; 'unavailable' if either run
  failed or lacks a finite bound, 'flagged' if either failed its primal check
  or conflicts with the reference value;
- root bound: root_dual; for a run that ended at the root (node limit 1 or
  one node) without a finite root_dual, the final dual bound (SCIP reports no
  root bound when the root node is pruned by the cuts);
- path family: pair-hull bound 0 (Theorem 6.2); root gap closed
  (root(m) - root(ref)) / (opt - root(ref)); closure of the residual gap
  (root(m) - 0) / (opt - 0);
- larger and structure models: root gap closed against the best known
  primal bound of the MINLPLib metadata (sign-adjusted for maximization);
- funnel: support calls, certification failures, certified supports,
  row-rounding rejections, certified rows below the violation threshold
  (calls - failures - rounding - binding - cuts), stored-row binding
  rejections (by cause where recorded) and cuts added.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import math
from pathlib import Path
import statistics

TOLERANCES = (1e-4, 1e-6)
FAILURES = ("process_timeout", "worker_error", "worker_no_output", "worker_output_parse_error")
MODE_ORDER = ("baseline", "baseline-noaggr", "baseline-novarlocks", "baseline-extra",
              "all", "all-noaggr", "auto", "all-diag", "all-diag-noaggr", "all-diag-rowdir",
              "all-diag-rowdir-noaggr", "all-diag-mech", "all-diag-mech-wide", "frozen-wide",
              "rowdir-wide", "gurobi")
REFERENCE_PREFIX = "c3:"
FUNNEL_KEYS = ("calls", "certification_calls", "certification_failures", "row_rounding_rejections",
               "row_binding_rejections", "cuts", "candidate_lps", "sampling_failures",
               "selection_skips", "repeat_skips", "exchange_samples")
TIME_KEYS = ("callback_seconds", "discovery_seconds", "candidate_seconds", "certification_seconds",
             "row_seconds")


def mode_rank(mode):
    base = mode[len(REFERENCE_PREFIX):] if mode.startswith(REFERENCE_PREFIX) else mode
    return (mode.startswith(REFERENCE_PREFIX) is False,
            MODE_ORDER.index(base) if base in MODE_ORDER else len(MODE_ORDER), mode)


def reference_mode(mode, modes):
    if mode.endswith("-noaggr") and mode != "baseline-noaggr" and "baseline-noaggr" in modes:
        return "baseline-noaggr"
    for candidate in ("baseline", REFERENCE_PREFIX + "baseline"):
        if candidate in modes and candidate != mode:
            return candidate
    return None


def failed(r):
    return r.get("status") in FAILURES or bool(r.get("worker_status")) or r.get("returncode", 0) != 0


def solved(r):
    check = r.get("primal_check") or {}
    return (not failed(r) and r.get("status") in ("optimal", "gaplimit")
            and check.get("checked") is True and check.get("passed") is True
            and isinstance(r.get("primal"), (int, float)) and math.isfinite(r["primal"]))


def completed(r, phase):
    """Solved (full, screen) or finished without failure with a root bound (root)."""
    if phase == "root":
        return bool(r) and not failed(r) and "total_seconds" in r and root_bound(r) is not None
    return bool(r) and solved(r)


def flags(r):
    out = []
    if (r.get("primal_check") or {}).get("passed") is False:
        out.append("primal_check_failed")
    reference = r.get("reference_check") or {}
    if reference.get("dual_consistent") is False:
        out.append("dual_reference_conflict")
    if reference.get("root_dual_consistent") is False:
        out.append("root_dual_reference_conflict")
    return out


def finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def seconds(r):
    return r["total_seconds"] + r.get("preparation_seconds", 0.0)


def solver_seconds(r):
    value = r.get("scip_solve_seconds", r.get("solver_runtime_seconds"))
    return value if finite(value) else None


def callback(r):
    return (r.get("separation") or {}).get("callback_seconds", 0.0)


def scip_excluding_callback(r):
    value = solver_seconds(r)
    return None if value is None else max(0.0, value - callback(r))


def root_bound(r):
    if not r or failed(r):
        return None
    if finite(r.get("root_dual")):
        return r["root_dual"]
    if (r.get("node_limit") == 1 or r.get("nodes") == 1) and finite(r.get("dual")) and r.get("mode") != "gurobi":
        return r["dual"]
    return None


def sgm(values, shift=1.0):
    values = [v for v in values if v is not None]
    if not values:
        return None
    return math.exp(statistics.fmean(math.log(v + shift) for v in values)) - shift


def cuts(r):
    return r["cuts"] if isinstance(r.get("cuts"), list) else None


def is_cut_mode(rows):
    return any(r.get("separation") is not None for r in rows)


def compare(a, b, key, rtol):
    """Outcome of a against reference b on bound `key` (callable or record key)."""
    get = key if callable(key) else (lambda r: r.get(key) if r and not failed(r) else None)
    if a is None or b is None or failed(a) or failed(b) or not finite(get(a)) or not finite(get(b)):
        return "unavailable"
    if flags(a) or flags(b):
        return "flagged"
    sign = 1 if (a.get("sense") or "min") == "min" else -1
    improvement = sign * (get(a) - get(b))
    tolerance = rtol * max(1.0, abs(get(a)), abs(get(b)))
    return "better" if improvement > tolerance else "worse" if improvement < -tolerance else "tie"


# ---------------------------------------------------------------- tables

def funnel(rows):
    separation = [r.get("separation") or {} for r in rows]
    totals = {key: sum(s.get(key, 0) or 0 for s in separation) for key in FUNNEL_KEYS}
    totals["certified_supports"] = totals["certification_calls"] - totals["certification_failures"]
    totals["below_violation_threshold"] = (totals["certified_supports"] - totals["row_rounding_rejections"]
                                           - totals["row_binding_rejections"] - totals["cuts"])
    causes, statuses, recorded = Counter(), Counter(), 0
    for r in rows:
        info = r.get("row_binding_rejection_causes")
        if info is not None:
            recorded += 1
            causes.update(info.get("causes", {}))
            statuses.update(info.get("variable_statuses", {}))
    totals.update(row_binding_rejection_causes=dict(causes), rejected_row_variable_statuses=dict(statuses),
                  runs_with_cause_records=recorded,
                  runs_with_binding_rejections=sum(bool(s.get("row_binding_rejections")) for s in separation),
                  discovery_incomplete_runs=sum(bool(s.get("discovery_incomplete")) for s in separation),
                  budget_exhausted_runs=sum(bool(s.get("budget_exhausted")) for s in separation))
    return totals


def time_decomposition(rows):
    done = [r for r in rows if not failed(r) and "total_seconds" in r]
    separation = [r.get("separation") or {} for r in done]
    out = {"runs": len(done), "sum_seconds": sum(seconds(r) for r in done),
           "sum_solver_seconds": sum(solver_seconds(r) or 0.0 for r in done),
           "sgm_seconds": sgm([seconds(r) for r in done]),
           "sgm_solver_seconds": sgm([solver_seconds(r) for r in done])}
    for key in TIME_KEYS:
        out["sum_" + key] = sum(s.get(key, 0.0) or 0.0 for s in separation)
    out["sgm_callback_seconds"] = sgm([callback(r) for r in done])
    out["sum_solver_seconds_excluding_callback"] = sum(scip_excluding_callback(r) or 0.0 for r in done)
    out["sgm_solver_seconds_excluding_callback"] = sgm([scip_excluding_callback(r) for r in done])
    return out


def native_separators(rows):
    """Native SCIP separator activity (calls that did not return DIDNOTRUN, cuts found/applied)."""
    totals, recorded = {}, 0
    for r in rows:
        stats = r.get("native_statistics") or {}
        if not stats.get("separators"):
            continue
        recorded += 1
        for name in ("eccuts", "interminor", "minor", "rlt"):
            row = stats["separators"].get(name) or {}
            entry = totals.setdefault(name, Counter())
            entry["runs_with_calls"] += bool(row.get("Calls"))
            for column in ("Calls", "FoundCuts", "Applied"):
                entry[column] += row.get(column, 0) if isinstance(row.get(column), int) else 0
        quadratic = (stats.get("nlhdlrs") or {}).get("quadratic") or {}
        entry = totals.setdefault("nlhdlr quadratic (intersection cuts)", Counter())
        entry["runs_with_cuts"] += bool(quadratic.get("Cuts"))
        for column in ("#Enforce", "Cuts"):
            entry[column] += quadratic.get(column, 0) if isinstance(quadratic.get(column), int) else 0
        status = stats.get("original_variable_status") or {}
        entry = totals.setdefault("original variable status after presolve", Counter())
        entry.update(status)
    return {"runs_with_statistics": recorded, **{k: dict(v) for k, v in totals.items()}}


def mode_table(rows, cut_mode):
    methods = Counter(c.get("support_witness", {}).get("method", "unknown")
                      for r in rows for c in (cuts(r) or []))
    return {
        "runs": len(rows), "solved": sum(map(solved, rows)), "cut_mode": cut_mode,
        "status_counts": dict(Counter(r.get("status") for r in rows)),
        "failures": [{"run_id": r["run_id"], "status": r.get("status"), "worker_status": r.get("worker_status"),
                      "reason": r.get("reason")} for r in rows if failed(r)],
        "model_not_admitted": [r["run_id"] for r in rows if not failed(r) and r.get("mode") != "gurobi"
                               and r.get("model_metadata") is None],
        "flagged": {r["run_id"]: flags(r) for r in rows if flags(r)},
        "cuts": sum(len(cuts(r) or []) for r in rows),
        "runs_with_cuts": sum(bool(cuts(r)) for r in rows),
        "cut_methods": dict(methods),
        "missing_cut_logs": [r["run_id"] for r in rows if cut_mode
                             and (cuts(r) is None or r.get("cut_log_complete") is not True)],
        "no_incumbent": sum((r.get("primal_check") or {}).get("checked") is not True for r in rows),
        "soft_budget_overshoots": [{"run_id": r["run_id"], "seconds": seconds(r)} for r in rows
                                   if "total_seconds" in r and seconds(r) > r["time_limit"] + 0.01],
        "outer_seconds": sum(r.get("outer_wall_seconds", 0.0) for r in rows),
        "load_start_mean": statistics.fmean(r["load_start"][0] for r in rows if "load_start" in r)
        if any("load_start" in r for r in rows) else None,
        "funnel": funnel(rows) if cut_mode else None,
        "time_decomposition": time_decomposition(rows),
        "native_separators": native_separators(rows),
    }


def time_metrics(index, modes, seeds, names, phase, cut_modes):
    per_seed, pooled = {}, {m: [] for m in modes}
    for seed in seeds:
        common = [n for n in names if all(completed(index.get((n, seed, m)), phase) for m in modes)]
        per_seed[seed] = {"common": len(common),
                          "sgm": {m: sgm([seconds(index[(n, seed, m)]) for n in common]) for m in modes}}
        for n in common:
            for m in modes:
                pooled[m].append(index[(n, seed, m)])
    ratios = []
    for m in modes:
        ref = reference_mode(m, modes)
        if ref is None:
            continue
        for seed in seeds:
            for n in names:
                a, b = index.get((n, seed, m)), index.get((n, seed, ref))
                if completed(a, phase) and completed(b, phase):
                    ratios.append({"name": n, "seed": seed, "mode": m, "reference": ref,
                                   "ratio": seconds(a) / max(seconds(b), 1e-9)})
    summary = {}
    for m in modes:
        values = [x["ratio"] for x in ratios if x["mode"] == m]
        if values:
            summary[m] = {"reference": reference_mode(m, modes), "count": len(values),
                          "median": statistics.median(values),
                          "geometric_mean": math.exp(statistics.fmean(map(math.log, values))),
                          "faster_than_reference": sum(x < 1 for x in values)}
    return {"basis": "solved by every mode" if phase != "root" else "completed by every mode",
            "per_seed": per_seed,
            "pooled": {"common_pairs": len(pooled[modes[0]]) if modes else 0,
                       "sgm": {m: sgm([seconds(r) for r in v]) for m, v in pooled.items()},
                       "sgm_solver_seconds": {m: sgm([solver_seconds(r) for r in v]) for m, v in pooled.items()},
                       "sgm_solver_seconds_excluding_callback": {
                           m: sgm([scip_excluding_callback(r) for r in v]) for m, v in pooled.items()
                           if m in cut_modes},
                       "sgm_callback_seconds": {m: sgm([callback(r) for r in v]) for m, v in pooled.items()
                                                if m in cut_modes}},
            "ratio_summary": summary, "per_model_ratios": ratios}


def bound_metrics(index, modes, seeds, names, phase):
    key = root_bound if phase == "root" else "dual"
    result = {}
    for rtol in TOLERANCES:
        table = {}
        for m in modes:
            ref = reference_mode(m, modes)
            if ref is None:
                continue
            rows = []
            for seed in seeds:
                for n in names:
                    a, b = index.get((n, seed, m)), index.get((n, seed, ref))
                    rows.append({"name": n, "seed": seed, "outcome": compare(a, b, key, rtol),
                                 "bound": root_bound(a) if phase == "root" else (a or {}).get("dual"),
                                 "reference_bound": root_bound(b) if phase == "root" else (b or {}).get("dual")})
            table[m] = {"reference": ref, "counts": dict(Counter(r["outcome"] for r in rows)), "rows": rows}
        result[f"{rtol:g}"] = table
    return result


def aa_metrics(index, seeds, names):
    if len(seeds) < 2 or not any(k[2] == "baseline" for k in index):
        return None
    common = [n for n in names if all(solved(index.get((n, s, "baseline")) or {}) for s in seeds)]
    first = seeds[0]
    out = {"seeds": list(seeds), "solved_by_seed": {s: sum(solved(index.get((n, s, "baseline")) or {})
                                                     for n in names) for s in seeds},
           "solved_status_disagreements": [n for n in names if len({solved(index.get((n, s, "baseline")) or {})
                                                                     for s in seeds}) > 1],
           "common_solved": len(common),
           "sgm_by_seed": {s: sgm([seconds(index[(n, s, "baseline")]) for n in common]) for s in seeds},
           "time_ratio_to_first_seed": {}}
    for s in seeds[1:]:
        ratios = [seconds(index[(n, s, "baseline")]) / max(seconds(index[(n, first, "baseline")]), 1e-9)
                  for n in common]
        out["time_ratio_to_first_seed"][s] = {
            "median": statistics.median(ratios) if ratios else None,
            "min": min(ratios, default=None), "max": max(ratios, default=None),
            "outside_0.8_1.25": sum(not 0.8 <= x <= 1.25 for x in ratios)}
    return out


def run_summary(r):
    if r is None:
        return None
    return {"status": r.get("status"), "root_bound": root_bound(r), "root_dual": r.get("root_dual"),
            "dual": r.get("dual"), "primal": r.get("primal"), "nodes": r.get("nodes"),
            "seconds": seconds(r) if "total_seconds" in r else None,
            "callback_seconds": (r.get("separation") or {}).get("callback_seconds"),
            "cuts": len(cuts(r)) if cuts(r) is not None else None,
            "solved": solved(r), "flags": flags(r), "failed": failed(r)}


def gap_rows(index, cases, modes, names, seeds, phase, path_family):
    """Root gap closed per model and mode; path family also the residual-gap closure."""
    rows = []
    for seed in seeds:
        for n in names:
            case = cases[n]
            if path_family:
                target = case["known_optimum"]
            else:
                try:
                    target = float(case.get("reference_primal"))
                except (TypeError, ValueError):
                    target = None
            row = {"name": n, "seed": seed, "target": target,
                   "runs": {m: run_summary(index.get((n, seed, m))) for m in modes}}
            if path_family:
                row.update(n=case["mechanism"]["n"], instance_seed=case["mechanism"]["seed"],
                           optimum_exact=case["known_optimum_exact"], pair_hull_bound=0.0)
            sign = 1
            some = next((index.get((n, seed, m)) for m in modes if index.get((n, seed, m))), None)
            if some and some.get("sense") == "max":
                sign = -1
            closed, residual = {}, {}
            for m in modes:
                value = root_bound(index.get((n, seed, m))) if phase == "root" else None
                ref = reference_mode(m, modes)
                base = root_bound(index.get((n, seed, ref))) if ref and phase == "root" else None
                if finite(value) and finite(base) and finite(target) and sign * (target - base) > 0:
                    closed[m] = (value - base) / (target - base)
                if path_family and finite(value) and target > 0:
                    residual[m] = value / target
            row["root_gap_closed"] = closed
            if path_family:
                row["residual_gap_closed"] = residual
            rows.append(row)
    return rows


def median_by(rows, field, key):
    groups = {}
    for row in rows:
        for m, v in row[field].items():
            groups.setdefault(m, {}).setdefault(row.get(key, "all"), []).append(v)
    return {m: {g: {"median": statistics.median(v), "count": len(v)} for g, v in sorted(d.items(), key=str)}
            for m, d in groups.items()}


# ---------------------------------------------------------------- directories

def load_records(out):
    path = out / "records.jsonl"
    return [json.loads(line) for line in path.read_text().splitlines() if line] if path.exists() else []


def summarize_dir(out, reference=None):
    spec = json.loads((out / "jobs.json").read_text())
    records = load_records(out)
    by_id = {r["run_id"]: r for r in records}
    scheduled = [(job, run) for job in spec["jobs"] for run in job["runs"]]
    cases = {p.stem: json.loads(p.read_text()) for p in (out / "cases").glob("*.json")}
    result = {"part": spec["part"], "directory": str(out), "scheduled_runs": len(scheduled),
              "recorded_runs": len(records),
              "missing_runs": [run["run_id"] for job, run in scheduled if run["run_id"] not in by_id],
              "status_counts": dict(Counter(r.get("status") for r in records)), "phases": {},
              "reference_directory": str(reference) if reference else None}
    ref_index, ref_cases = {}, {}
    if reference:
        for r in load_records(reference):
            ref_index[(r["phase"], r["name"], r["seed"], REFERENCE_PREFIX + r["mode"])] = r
        ref_cases = {p.stem: json.loads(p.read_text()) for p in (reference / "cases").glob("*.json")}
        result["reference_case_mismatches"] = sorted(n for n in cases if n in ref_cases and ref_cases[n] != cases[n])
    for suite, phase in sorted({(job["suite"], job["phase"]) for job in spec["jobs"]}):
        jobs = [job for job in spec["jobs"] if (job["suite"], job["phase"]) == (suite, phase)]
        seeds = sorted({job["seed"] for job in jobs})
        names = list(dict.fromkeys(job["name"] for job in jobs))
        index = {(job["name"], job["seed"], run["mode"]): by_id[run["run_id"]]
                 for job in jobs for run in job["runs"] if run["run_id"] in by_id}
        for (p, n, s, m), r in ref_index.items():
            if p == phase and n in names and s in seeds and n not in result.get("reference_case_mismatches", ()):
                index[(n, s, m)] = r
        modes = sorted({run["mode"] for job in jobs for run in job["runs"]} | {k[2] for k in index}, key=mode_rank)
        rows = {m: [r for (n, s, mm), r in index.items() if mm == m] for m in modes}
        cut_modes = [m for m in modes if is_cut_mode(rows[m])]
        entry = {"suite": suite, "phase": phase, "modes": modes, "cut_modes": cut_modes, "seeds": seeds,
                 "models": len(names), "time_limit": jobs[0]["time_limit"],
                 "worker_timeout": jobs[0]["worker_timeout"], "node_limit": jobs[0]["node_limit"],
                 "references": {m: reference_mode(m, modes) for m in modes},
                 "by_mode": {m: mode_table(rows[m], m in cut_modes) for m in modes},
                 "solved_by_seed": {m: {s: sum(solved(index.get((n, s, m)) or {}) for n in names)
                                        for s in seeds} for m in modes},
                 "bounds": bound_metrics(index, modes, seeds, names, phase),
                 "times": time_metrics(index, modes, seeds, names, phase, cut_modes),
                 "aa_baseline": aa_metrics(index, seeds, names) if phase == "full" else None}
        path_family = suite == "mechanism"
        if phase in ("root", "full"):
            gaps = gap_rows(index, cases, modes, names, seeds, phase, path_family)
            entry["models_table"] = gaps
            if phase == "root":
                key = "n" if path_family else "seed"
                entry["root_gap_closed_median"] = median_by(gaps, "root_gap_closed", key)
                if path_family:
                    entry["residual_gap_closed_median"] = median_by(gaps, "residual_gap_closed", key)
        result["phases"][f"{suite}/{phase}"] = entry
    replay = out / "replay.json"
    if replay.exists():
        data = json.loads(replay.read_text())
        extra = data.get("v4") or data.get("v3") or {}
        result["replay"] = {k: data.get(k) for k in ("passed", "archived_passed", "records", "bound_runs",
                                                     "admitted_runs", "cuts", "replayed_cuts",
                                                     "missing_cut_logs", "tamper_rejections")}
        result["replay"]["failed_runs"] = [r["run_id"] for r in data.get("runs", []) if not r.get("passed")]
        result["replay"]["wrapper"] = {k: extra.get(k) for k in
                                       ("coverage_complete", "config_failures", "gurobi_failures",
                                        "modes_with_cuts", "tamper_controls_cover_all_cut_modes")}
        result["replay"]["tamper_by_mode"] = {m: all(c["rejections"].values()) and c["untampered_first_cut_passed"]
                                              for m, c in extra.get("tamper_controls_by_mode", {}).items()}
    else:
        result["replay"] = None
    return result


# ---------------------------------------------------------------- markdown

def fmt(value, digits=4):
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.{digits}g}"
    return str(value)


def markdown(summary):
    lines = ["# Campaign 4 results", "",
             "Generated by `summarize_v4.py`; definitions are in its docstring and in "
             "`campaign-v4-protocol.md`. Timings are descriptive (shared host, up to six "
             "single-threaded workers). Bounds are numerical solver bounds; only recorded cuts are "
             "certified, and only where the replay passed. Modes `c3:<mode>` are campaign-3 records "
             "of the same models and limits (reference directory).", ""]
    for part in summary["parts"]:
        lines += [f"## {part['part']} (`{part['directory']}`)", "",
                  f"Scheduled runs {part['scheduled_runs']}, recorded {part['recorded_runs']}, "
                  f"missing {len(part['missing_runs'])}. Statuses: "
                  + ", ".join(f"{k} {v}" for k, v in sorted(part["status_counts"].items(), key=str)) + ".", ""]
        if part.get("reference_directory"):
            lines += [f"Reference directory: `{part['reference_directory']}`; case mismatches: "
                      f"{len(part.get('reference_case_mismatches', []))}.", ""]
        replay = part["replay"]
        if replay:
            lines += [f"Replay: passed {replay['passed']}; {replay['replayed_cuts']}/{replay['cuts']} cuts replayed; "
                      f"failed runs {len(replay['failed_runs'])}; config failures "
                      f"{len(replay['wrapper'].get('config_failures') or [])}; Gurobi record failures "
                      f"{len(replay['wrapper'].get('gurobi_failures') or [])}; tampering controls by mode "
                      + (", ".join(f"{m} {'rejected all' if ok else 'NOT all rejected'}"
                                   for m, ok in replay["tamper_by_mode"].items()) or "none") + ".", ""]
        else:
            lines += ["Replay: not run yet.", ""]
        for name, p in part["phases"].items():
            lines += [f"### {name}: {p['models']} models, seeds {p['seeds']}, soft {p['time_limit']:g} s, "
                      f"hard {p['worker_timeout']:g} s, node limit {p['node_limit']}", "",
                      "| Mode | Reference | Runs | Solved | Failures | Not admitted | Flagged | Cuts | Runs with cuts | Missing cut logs | SGM s | SGM SCIP s | SGM SCIP s excl. callback | Sum callback s | Outer s | Mean load |",
                      "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
            for m, t in p["by_mode"].items():
                d = t["time_decomposition"]
                lines.append(f"| {m} | {fmt(p['references'][m])} | {t['runs']} | {t['solved']} | {len(t['failures'])} | "
                             f"{len(t['model_not_admitted'])} | {len(t['flagged'])} | {t['cuts']} | {t['runs_with_cuts']} | "
                             f"{len(t['missing_cut_logs'])} | {fmt(d['sgm_seconds'])} | {fmt(d['sgm_solver_seconds'])} | "
                             f"{fmt(d['sgm_solver_seconds_excluding_callback']) if t['cut_mode'] else '-'} | "
                             f"{d['sum_callback_seconds']:.1f} | {t['outer_seconds']:.1f} | {fmt(t['load_start_mean'], 3)} |")
            lines += ["", "SGM columns here are over all completed runs of the mode; the comparison below uses "
                      "common runs.", ""]
            tm = p["times"]
            lines += [f"Times over runs {tm['basis']} ({tm['pooled']['common_pairs']} model-seed pairs):", "",
                      "| Mode | SGM s | SGM SCIP s | SGM SCIP s excl. callback | SGM callback s | Ratio to reference: median | geometric mean | faster | pairs |",
                      "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
            for m in p["modes"]:
                ratio = tm["ratio_summary"].get(m, {})
                lines.append(f"| {m} | {fmt(tm['pooled']['sgm'][m])} | {fmt(tm['pooled']['sgm_solver_seconds'][m])} | "
                             f"{fmt(tm['pooled']['sgm_solver_seconds_excluding_callback'].get(m))} | "
                             f"{fmt(tm['pooled']['sgm_callback_seconds'].get(m))} | {fmt(ratio.get('median'))} | "
                             f"{fmt(ratio.get('geometric_mean'))} | {fmt(ratio.get('faster_than_reference'))} | "
                             f"{fmt(ratio.get('count'))} |")
            lines += ["", f"Paired {'root' if p['phase'] == 'root' else 'final'} bounds versus the reference mode:", "",
                      "| Mode | Reference | rtol | Better | Tie | Worse | Unavailable | Flagged |",
                      "|---|---|---|---:|---:|---:|---:|---:|"]
            for rtol, table in p["bounds"].items():
                for m, v in table.items():
                    c = v["counts"]
                    lines.append(f"| {m} | {v['reference']} | {rtol} | {c.get('better', 0)} | {c.get('tie', 0)} | "
                                 f"{c.get('worse', 0)} | {c.get('unavailable', 0)} | {c.get('flagged', 0)} |")
            lines.append("")
            if p["cut_modes"]:
                lines += ["Separator funnel (sums over runs):", "",
                          "| Mode | Callbacks | Support calls | Cert. failures | Certified | Rounding rej. | Below threshold | Binding rej. (runs) | Binding causes | Cuts | Discovery incomplete | Budget exhausted |",
                          "|---|---:|---:|---:|---:|---:|---:|---|---|---:|---:|---:|"]
                for m in p["cut_modes"]:
                    f = p["by_mode"][m]["funnel"]
                    causes = ", ".join(f"{k} {v}" for k, v in sorted(f["row_binding_rejection_causes"].items())) or "-"
                    if f["runs_with_cause_records"] == 0 and f["row_binding_rejections"]:
                        causes = "not recorded"
                    lines.append(f"| {m} | {f['calls']} | {f['certification_calls']} | {f['certification_failures']} | "
                                 f"{f['certified_supports']} | {f['row_rounding_rejections']} | {f['below_violation_threshold']} | "
                                 f"{f['row_binding_rejections']} ({f['runs_with_binding_rejections']}) | {causes} | {f['cuts']} | "
                                 f"{f['discovery_incomplete_runs']} | {f['budget_exhausted_runs']} |")
                lines += ["", "Separator time decomposition (sums over completed runs, seconds):", "",
                          "| Mode | Charged | SCIP | SCIP excl. callback | Callback | Discovery | Candidate LPs | Certification | Rows |",
                          "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
                for m in p["cut_modes"]:
                    d = p["by_mode"][m]["time_decomposition"]
                    lines.append(f"| {m} | {d['sum_seconds']:.1f} | {d['sum_solver_seconds']:.1f} | "
                                 f"{d['sum_solver_seconds_excluding_callback']:.1f} | {d['sum_callback_seconds']:.1f} | "
                                 f"{d['sum_discovery_seconds']:.1f} | {d['sum_candidate_seconds']:.1f} | "
                                 f"{d['sum_certification_seconds']:.1f} | {d['sum_row_seconds']:.1f} |")
                lines.append("")
            native = {m: p["by_mode"][m]["native_separators"] for m in p["modes"]
                      if p["by_mode"][m]["native_separators"]["runs_with_statistics"]}
            if native:
                lines += ["Native SCIP separators (runs with a productive call / calls / cuts found / applied; "
                          "intersection cuts: runs / enforcement calls / cuts):", "",
                          "| Mode | Runs | eccuts | interminor | minor | rlt | intersection cuts | Original variables after presolve |",
                          "|---|---:|---|---|---|---|---|---|"]
                for m, v in native.items():
                    cell = lambda k: "/".join(str(v.get(k, {}).get(c, 0)) for c in ("runs_with_calls", "Calls", "FoundCuts", "Applied"))
                    q = v.get("nlhdlr quadratic (intersection cuts)", {})
                    status = ", ".join(f"{k} {c}" for k, c in sorted(v.get("original variable status after presolve", {}).items()))
                    lines.append(f"| {m} | {v['runs_with_statistics']} | {cell('eccuts')} | {cell('interminor')} | "
                                 f"{cell('minor')} | {cell('rlt')} | {q.get('runs_with_cuts', 0)}/{q.get('#Enforce', 0)}/{q.get('Cuts', 0)} | {status} |")
                lines.append("")
            if "models_table" in p:
                lines += models_markdown(p)
    return "\n".join(lines) + "\n"


def models_markdown(p):
    path_family = p["suite"] == "mechanism"
    modes = p["modes"]
    lines = []
    if p["phase"] == "root":
        title = ("Root bounds; pair-hull bound 0 (Theorem 6.2); gap closed vs reference / residual closure root/opt"
                 if path_family else "Root bounds; gap closed against the best known primal bound vs reference")
        lines += [title + ":", "", "| Model | Target | " + " | ".join(modes) + " |", "|---|---:|" + "---|" * len(modes)]
        for row in p["models_table"]:
            cells = []
            for m in modes:
                run = row["runs"][m]
                if run is None:
                    cells.append("-")
                    continue
                text = fmt(run["root_bound"], 6)
                if m in row["root_gap_closed"]:
                    text += f" ({fmt(row['root_gap_closed'][m], 3)})"
                if path_family and m in row.get("residual_gap_closed", {}):
                    text += f" [{fmt(row['residual_gap_closed'][m], 3)}]"
                cells.append(text)
            lines.append(f"| {row['name']} | {fmt(row['target'], 6)} | " + " | ".join(cells) + " |")
        lines.append("")
        for field, label in (("root_gap_closed_median", "Median root gap closed"),
                             ("residual_gap_closed_median", "Median closure of the residual gap (root/opt)")):
            if field in p:
                lines.append(f"{label}: " + "; ".join(
                    f"{m}: " + ", ".join(f"{'n=' + str(g) if path_family else 'seed ' + str(g)} {fmt(v['median'], 3)} ({v['count']})"
                                         for g, v in groups.items()) for m, groups in p[field].items()) + ".")
        lines.append("")
    else:
        lines += ["Full runs (status / seconds / nodes / final dual):", "",
                  "| Model | Target | " + " | ".join(modes) + " |", "|---|---:|" + "---|" * len(modes)]
        for row in p["models_table"]:
            cells = []
            for m in modes:
                run = row["runs"][m]
                cells.append("-" if run is None else
                             f"{fmt(run['status'])} / {fmt(run['seconds'], 3)} / {fmt(run['nodes'])} / {fmt(run['dual'], 6)}")
            lines.append(f"| {row['name']} | {fmt(row['target'], 6)} | " + " | ".join(cells) + " |")
        lines.append("")
    return lines


def parse_directory(text):
    directory, _, reference = text.partition("=")
    return Path(directory).resolve(), Path(reference).resolve() if reference else None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("directories", nargs="+", help="DIR or DIR=REFERENCE_DIR")
    parser.add_argument("--dest", type=Path, required=True)
    args = parser.parse_args()
    summary = {"parts": [summarize_dir(*parse_directory(d)) for d in args.directories]}
    args.dest.mkdir(parents=True, exist_ok=True)
    for name, content in (("summary.json", json.dumps(summary, indent=2, allow_nan=False) + "\n"),
                          ("results.md", markdown(summary))):
        (args.dest / name).write_text(content)  # derived from the raw records; safe to regenerate
    print(json.dumps([{"part": p["part"], "recorded": p["recorded_runs"], "scheduled": p["scheduled_runs"],
                       "statuses": p["status_counts"]} for p in summary["parts"]]))
