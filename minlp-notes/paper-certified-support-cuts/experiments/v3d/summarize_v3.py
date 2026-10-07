"""Compute the campaign-v3 metrics for one or more v3 output directories.

    summarize_v3.py OUTPUT_DIR [OUTPUT_DIR ...] --dest DIR

Writes DIR/summary.json and DIR/results.md (derived files, regenerated on each call).
Every scheduled run is counted; missing records, worker errors and timeouts
are reported, not dropped. Definitions (campaign-v3-protocol.md, Metrics):

- solved: status optimal or gaplimit, worker exited normally, and an
  incumbent that passed the independent original-model check (1e-5);
- time: total_seconds + preparation_seconds, the time charged to the soft
  budget; shifted geometric mean with shift 1 s over the (model, seed) pairs
  solved by every mode of the phase, per seed and pooled over seeds;
- bounds: per (model, seed), mode versus baseline, final dual bound for full
  runs and root dual bound for root runs; better/worse when the improvement
  exceeds rtol * max(1, |a|, |b|), for rtol 1e-4 and 1e-6. A pair is
  'unavailable' if either run failed or lacks a finite bound and 'flagged' if
  either run failed its primal check or conflicts with the reference value;
- root gap closed (mechanism family):
  (root_dual(all-diag-mech) - root_dual(baseline)) / (opt - root_dual(baseline));
- A/A variation: the baseline across seeds, with the same metrics.
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


def failed(r):
    return r.get("status") in FAILURES or bool(r.get("worker_status")) or r.get("returncode", 0) != 0


def solved(r):
    check = r.get("primal_check") or {}
    return (not failed(r) and r.get("status") in ("optimal", "gaplimit")
            and check.get("checked") is True and check.get("passed") is True
            and isinstance(r.get("primal"), (int, float)) and math.isfinite(r["primal"]))


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


def seconds(r):
    return r["total_seconds"] + r.get("preparation_seconds", 0.0)


def sgm(values, shift=1.0):
    if not values:
        return None
    return math.exp(statistics.fmean(math.log(v + shift) for v in values)) - shift


def finite(value):
    return isinstance(value, (int, float)) and math.isfinite(value)


def cuts(r):
    return r["cuts"] if isinstance(r.get("cuts"), list) else None


def compare(a, b, key, rtol):
    """Outcome of a against reference b on bound `key`."""
    if a is None or b is None or failed(a) or failed(b) or not finite(a.get(key)) or not finite(b.get(key)):
        return "unavailable"
    if flags(a) or flags(b):
        return "flagged"
    sign = 1 if a.get("sense", "min") == "min" else -1
    improvement = sign * (a[key] - b[key])
    tolerance = rtol * max(1.0, abs(a[key]), abs(b[key]))
    return "better" if improvement > tolerance else "worse" if improvement < -tolerance else "tie"


def mode_table(rows):
    separation = [r.get("separation") or {} for r in rows]
    methods = Counter(c.get("support_witness", {}).get("method", "unknown")
                      for r in rows for c in (cuts(r) or []))
    return {
        "runs": len(rows), "solved": sum(map(solved, rows)),
        "status_counts": dict(Counter(r.get("status") for r in rows)),
        "failures": [{"run_id": r["run_id"], "status": r.get("status"), "worker_status": r.get("worker_status"),
                      "reason": r.get("reason")} for r in rows if failed(r)],
        "model_not_admitted": [r["run_id"] for r in rows if not failed(r) and r.get("model_metadata") is None],
        "flagged": {r["run_id"]: flags(r) for r in rows if flags(r)},
        "cuts": sum(len(cuts(r) or []) for r in rows),
        "runs_with_cuts": sum(bool(cuts(r)) for r in rows),
        "cut_methods": dict(methods),
        "missing_cut_logs": [r["run_id"] for r in rows if r["mode"] != "baseline"
                             and (cuts(r) is None or r.get("cut_log_complete") is not True)],
        "no_incumbent": sum((r.get("primal_check") or {}).get("checked") is not True for r in rows),
        "separation_seconds": sum(s.get("callback_seconds", 0.0) for s in separation),
        "support_calls": sum(s.get("certification_calls", 0) for s in separation),
        "separation_budget_exhausted_runs": sum(bool(s.get("budget_exhausted")) for s in separation),
        "soft_budget_overshoots": [{"run_id": r["run_id"], "seconds": seconds(r)} for r in rows
                                   if "total_seconds" in r and seconds(r) > r["time_limit"] + 0.01],
        "outer_seconds": sum(r.get("outer_wall_seconds", 0.0) for r in rows),
        "load_start_mean": statistics.fmean(r["load_start"][0] for r in rows) if rows else None,
        "load_start_max": max((r["load_start"][0] for r in rows), default=None),
    }


def time_metrics(index, modes, seeds, names):
    per_seed = {}
    pooled = {m: [] for m in modes}
    ratios = []
    for seed in seeds:
        common = [n for n in names if all(solved(index.get((n, seed, m)) or {}) for m in modes)]
        per_seed[seed] = {"common_solved": len(common),
                          "sgm": {m: sgm([seconds(index[(n, seed, m)]) for n in common]) for m in modes}}
        for n in common:
            for m in modes:
                pooled[m].append(seconds(index[(n, seed, m)]))
            base = seconds(index[(n, seed, "baseline")])
            ratios += [{"name": n, "seed": seed, "mode": m,
                        "ratio": seconds(index[(n, seed, m)]) / max(base, 1e-9)}
                       for m in modes if m != "baseline"]
    by_mode = {m: [x["ratio"] for x in ratios if x["mode"] == m] for m in modes if m != "baseline"}
    return {"per_seed": per_seed,
            "pooled": {"common_solved_pairs": len(pooled[modes[0]]),
                       "sgm": {m: sgm(v) for m, v in pooled.items()}},
            "ratio_summary": {m: {"median": statistics.median(v) if v else None,
                                  "geometric_mean": math.exp(statistics.fmean(map(math.log, v))) if v else None,
                                  "faster_than_baseline": sum(x < 1 for x in v), "count": len(v)}
                              for m, v in by_mode.items()},
            "per_model_ratios": ratios}


def bound_metrics(index, modes, seeds, names, key):
    result = {}
    for rtol in TOLERANCES:
        table = {}
        for m in modes:
            if m == "baseline":
                continue
            rows = []
            for seed in seeds:
                for n in names:
                    a, b = index.get((n, seed, m)), index.get((n, seed, "baseline"))
                    rows.append({"name": n, "seed": seed, "outcome": compare(a, b, key, rtol),
                                 "bound": (a or {}).get(key), "baseline_bound": (b or {}).get(key)})
            table[m] = {"counts": dict(Counter(r["outcome"] for r in rows)), "rows": rows}
        result[f"{rtol:g}"] = table
    return result


def aa_metrics(index, seeds, names):
    if len(seeds) < 2:
        return None
    common = [n for n in names if all(solved(index.get((n, s, "baseline")) or {}) for s in seeds)]
    first = seeds[0]
    out = {"seeds": list(seeds), "solved_by_seed": {s: sum(solved(index.get((n, s, "baseline")) or {})
                                                     for n in names) for s in seeds},
           "solved_status_disagreements": [n for n in names if len({solved(index.get((n, s, "baseline")) or {})
                                                                     for s in seeds}) > 1],
           "common_solved": len(common),
           "sgm_by_seed": {s: sgm([seconds(index[(n, s, "baseline")]) for n in common]) for s in seeds},
           "time_ratio_to_first_seed": {}, "final_dual_vs_first_seed": {}}
    for s in seeds[1:]:
        ratios = [seconds(index[(n, s, "baseline")]) / max(seconds(index[(n, first, "baseline")]), 1e-9)
                  for n in common]
        out["time_ratio_to_first_seed"][s] = {
            "median": statistics.median(ratios) if ratios else None,
            "min": min(ratios, default=None), "max": max(ratios, default=None),
            "outside_0.8_1.25": sum(not 0.8 <= x <= 1.25 for x in ratios)}
        out["final_dual_vs_first_seed"][s] = {
            f"{rtol:g}": dict(Counter(compare(index.get((n, s, "baseline")), index.get((n, first, "baseline")),
                                              "dual", rtol) for n in names)) for rtol in TOLERANCES}
    return out


def mechanism_metrics(index, cases, names):
    rows = []
    for n in names:
        case = cases[n]
        optimum = case["known_optimum"]
        row = {"name": n, "n": case["mechanism"]["n"], "seed": case["mechanism"]["seed"],
               "optimum": optimum, "optimum_exact": case["known_optimum_exact"]}
        for phase in ("root", "full"):
            for mode in ("baseline", "all-diag-mech"):
                r = index.get((phase, n, mode))
                if r is None:
                    row[f"{phase}_{mode}"] = None
                    continue
                row[f"{phase}_{mode}"] = {
                    "status": r.get("status"), "root_dual": r.get("root_dual"), "dual": r.get("dual"),
                    "primal": r.get("primal"), "nodes": r.get("nodes"),
                    "seconds": seconds(r) if "total_seconds" in r else None,
                    "outer_seconds": r.get("outer_wall_seconds"),
                    "separation_seconds": (r.get("separation") or {}).get("callback_seconds"),
                    "cuts": len(cuts(r)) if cuts(r) is not None else None,
                    "solved": solved(r), "flags": flags(r), "failed": failed(r)}
        base, mech = row.get("root_baseline"), row.get("root_all-diag-mech")
        closed = None
        if base and mech and not base["failed"] and not mech["failed"] and finite(base["root_dual"]) \
                and finite(mech["root_dual"]) and optimum - base["root_dual"] > 0:
            closed = (mech["root_dual"] - base["root_dual"]) / (optimum - base["root_dual"])
        row["root_gap_closed"] = closed
        rows.append(row)
    by_n = {}
    for row in rows:
        by_n.setdefault(row["n"], []).append(row["root_gap_closed"])
    return {"rows": rows,
            "root_gap_closed_by_n": {n: {"values": v, "median": statistics.median([x for x in v if x is not None])
                                         if any(x is not None for x in v) else None}
                                     for n, v in sorted(by_n.items())}}


def summarize_dir(out):
    spec = json.loads((out / "jobs.json").read_text())
    path = out / "records.jsonl"
    records = [json.loads(line) for line in path.read_text().splitlines() if line] if path.exists() else []
    by_id = {r["run_id"]: r for r in records}
    scheduled = [(job, run) for job in spec["jobs"] for run in job["runs"]]
    cases = {p.stem: json.loads(p.read_text()) for p in (out / "cases").glob("*.json")}
    result = {"part": spec["part"], "directory": str(out), "scheduled_runs": len(scheduled),
              "recorded_runs": len(records),
              "missing_runs": [run["run_id"] for job, run in scheduled if run["run_id"] not in by_id],
              "status_counts": dict(Counter(r.get("status") for r in records)), "phases": {}}
    for suite, phase in sorted({(job["suite"], job["phase"]) for job in spec["jobs"]}):
        jobs = [job for job in spec["jobs"] if (job["suite"], job["phase"]) == (suite, phase)]
        modes = sorted({run["mode"] for job in jobs for run in job["runs"]},
                       key=lambda m: ("baseline", "all", "auto", "all-diag", "all-diag-mech", "all-diag-mech-wide").index(m))
        seeds = sorted({job["seed"] for job in jobs})
        names = list(dict.fromkeys(job["name"] for job in jobs))
        index = {(job["name"], job["seed"], run["mode"]): by_id[run["run_id"]]
                 for job in jobs for run in job["runs"] if run["run_id"] in by_id}
        rows = {m: [r for (n, s, mm), r in index.items() if mm == m] for m in modes}
        entry = {"modes": modes, "seeds": seeds, "models": len(names),
                 "time_limit": jobs[0]["time_limit"], "worker_timeout": jobs[0]["worker_timeout"],
                 "node_limit": jobs[0]["node_limit"],
                 "by_mode": {m: mode_table(rows[m]) for m in modes},
                 "solved_by_seed": {m: {s: sum(solved(index.get((n, s, m)) or {}) for n in names)
                                        for s in seeds} for m in modes},
                 "bounds": bound_metrics(index, modes, seeds, names, "dual" if phase == "full" else "root_dual"),
                 "bound_key": "dual" if phase == "full" else "root_dual"}
        if phase == "full":
            entry["times"] = time_metrics(index, modes, seeds, names)
            entry["aa_baseline"] = aa_metrics(index, seeds, names)
        result["phases"][f"{suite}/{phase}"] = dict(entry, suite=suite, phase=phase)
    mech = [n for n, c in cases.items() if c.get("suite") == "mechanism"]
    if mech:
        index = {(job["phase"], job["name"], run["mode"]): by_id[run["run_id"]]
                 for job in spec["jobs"] for run in job["runs"] if run["run_id"] in by_id}
        order = sorted(mech, key=lambda n: (cases[n]["mechanism"]["n"], cases[n]["mechanism"]["seed"]))
        result["mechanism"] = mechanism_metrics(index, cases, order)
    replay = out / "replay.json"
    if replay.exists():
        data = json.loads(replay.read_text())
        result["replay"] = {k: data.get(k) for k in ("passed", "archived_passed", "records", "bound_runs",
                                                     "admitted_runs", "cuts", "replayed_cuts",
                                                     "missing_cut_logs", "tamper_rejections")}
        result["replay"]["failed_runs"] = [r["run_id"] for r in data.get("runs", []) if not r.get("passed")]
        result["replay"]["v3"] = {k: data.get("v3", {}).get(k) for k in
                                  ("coverage_complete", "config_failures", "modes_with_cuts",
                                   "tamper_controls_cover_all_cut_modes")}
        result["replay"]["tamper_by_mode"] = {m: all(c["rejections"].values()) and c["untampered_first_cut_passed"]
                                              for m, c in data.get("v3", {}).get("tamper_controls_by_mode", {}).items()}
    else:
        result["replay"] = None
    return result


def fmt(value, digits=4):
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.{digits}g}"
    return str(value)


def markdown(summary):
    lines = ["# Campaign v3 results", "",
             "Generated by `summarize_v3.py`. Definitions are in its docstring and in "
             "`campaign-v3-protocol.md`; timings are descriptive (shared host, up to six "
             "single-threaded workers). Bounds are SCIP numerical bounds; only recorded cuts are "
             "certified, and only where the replay passed.", ""]
    for part in summary["parts"]:
        lines += [f"## {part['part']} (`{part['directory']}`)", "",
                  f"Scheduled runs {part['scheduled_runs']}, recorded {part['recorded_runs']}, "
                  f"missing {len(part['missing_runs'])}. Statuses: "
                  + ", ".join(f"{k} {v}" for k, v in sorted(part["status_counts"].items(), key=str)) + ".", ""]
        replay = part["replay"]
        if replay:
            lines += [f"Replay: passed {replay['passed']}; {replay['replayed_cuts']}/{replay['cuts']} cuts replayed; "
                      f"failed runs {len(replay['failed_runs'])}; tampering controls by mode "
                      + ", ".join(f"{m} {'rejected all' if ok else 'NOT all rejected'}"
                                  for m, ok in replay["tamper_by_mode"].items()) + ".", ""]
        else:
            lines += ["Replay: not run yet.", ""]
        for phase, p in part["phases"].items():
            lines += [f"### {phase}: {p['models']} models, seeds {p['seeds']}, soft {p['time_limit']:g} s, "
                      f"hard {p['worker_timeout']:g} s, node limit {p['node_limit']}", "",
                      "| Mode | Runs | Solved | Solved by seed | Failures | Not admitted | Flagged | Cuts | Runs with cuts | Cut methods | Missing cut logs | Separation s | Outer s | Mean load |",
                      "|---|---:|---:|---|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|"]
            for m, t in p["by_mode"].items():
                by_seed = " / ".join(str(p["solved_by_seed"][m][s]) for s in p["seeds"])
                methods = ", ".join(f"{k} {v}" for k, v in sorted(t["cut_methods"].items())) or "-"
                lines.append(f"| {m} | {t['runs']} | {t['solved']} | {by_seed} | {len(t['failures'])} | "
                             f"{len(t['model_not_admitted'])} | {len(t['flagged'])} | {t['cuts']} | {t['runs_with_cuts']} | "
                             f"{methods} | {len(t['missing_cut_logs'])} | {t['separation_seconds']:.1f} | "
                             f"{t['outer_seconds']:.1f} | {fmt(t['load_start_mean'], 3)} |")
            lines.append("")
            if "times" in p:
                tm = p["times"]
                header = "| Seeds | Common solved | " + " | ".join(f"SGM {m} (s)" for m in p["modes"]) + " |"
                lines += [header, "|---|---:|" + "---:|" * len(p["modes"])]
                for s, v in tm["per_seed"].items():
                    lines.append(f"| {s} | {v['common_solved']} | " + " | ".join(fmt(v["sgm"][m]) for m in p["modes"]) + " |")
                lines.append(f"| pooled | {tm['pooled']['common_solved_pairs']} | "
                             + " | ".join(fmt(tm["pooled"]["sgm"][m]) for m in p["modes"]) + " |")
                lines.append("")
                for m, v in tm["ratio_summary"].items():
                    lines.append(f"- {m}/baseline time ratio over common solved pairs: median {fmt(v['median'])}, "
                                 f"geometric mean {fmt(v['geometric_mean'])}, faster in {v['faster_than_baseline']}/{v['count']}.")
                lines.append("")
            lines += [f"Paired {'final' if p['bound_key'] == 'dual' else 'root'} dual bounds versus baseline:", "",
                      "| Mode | rtol | Better | Tie | Worse | Unavailable | Flagged |", "|---|---|---:|---:|---:|---:|---:|"]
            for rtol, table in p["bounds"].items():
                for m, v in table.items():
                    c = v["counts"]
                    lines.append(f"| {m} | {rtol} | {c.get('better', 0)} | {c.get('tie', 0)} | {c.get('worse', 0)} | "
                                 f"{c.get('unavailable', 0)} | {c.get('flagged', 0)} |")
            lines.append("")
            aa = p.get("aa_baseline")
            if aa:
                lines += ["A/A baseline variation across seeds: solved " +
                          ", ".join(f"seed {s} {v}" for s, v in aa["solved_by_seed"].items()) +
                          f"; solved-status disagreements {len(aa['solved_status_disagreements'])}; "
                          f"SGM over {aa['common_solved']} models solved in every seed: " +
                          ", ".join(f"seed {s} {fmt(v)}" for s, v in aa["sgm_by_seed"].items()) + "."]
                for s, v in aa["time_ratio_to_first_seed"].items():
                    d = aa["final_dual_vs_first_seed"][s]
                    lines.append(f"- seed {s} vs seed {aa['seeds'][0]}: time ratio median {fmt(v['median'])} "
                                 f"(min {fmt(v['min'])}, max {fmt(v['max'])}, {v['outside_0.8_1.25']} outside [0.8, 1.25]); "
                                 "final dual " + "; ".join(f"rtol {k}: " + ", ".join(f"{o} {c}" for o, c in sorted(x.items()))
                                                           for k, x in d.items()) + ".")
                lines.append("")
        mech = part.get("mechanism")
        if mech:
            lines += ["### Mechanism family", "",
                      "| Instance | Optimum | Root dual baseline | Root dual all-diag-mech | Root gap closed | Root cuts | Full status baseline / mech | Nodes baseline / mech | Seconds baseline / mech | Separation s (full, mech) | Full cuts |",
                      "|---|---:|---:|---:|---:|---:|---|---|---|---:|---:|"]
            for r in mech["rows"]:
                rb, rm = r.get("root_baseline") or {}, r.get("root_all-diag-mech") or {}
                fb, fm = r.get("full_baseline") or {}, r.get("full_all-diag-mech") or {}
                lines.append(f"| {r['name']} | {fmt(r['optimum'], 6)} | {fmt(rb.get('root_dual'), 6)} | {fmt(rm.get('root_dual'), 6)} | "
                             f"{fmt(r['root_gap_closed'], 3)} | {fmt(rm.get('cuts'))} | {fmt(fb.get('status'))} / {fmt(fm.get('status'))} | "
                             f"{fmt(fb.get('nodes'))} / {fmt(fm.get('nodes'))} | {fmt(fb.get('seconds'), 3)} / {fmt(fm.get('seconds'), 3)} | "
                             f"{fmt(fm.get('separation_seconds'), 3)} | {fmt(fm.get('cuts'))} |")
            lines += ["", "Median root gap closed by n: " + ", ".join(
                f"n={n} {fmt(v['median'], 3)}" for n, v in mech["root_gap_closed_by_n"].items()) + ".", ""]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("directories", type=Path, nargs="+")
    parser.add_argument("--dest", type=Path, required=True)
    args = parser.parse_args()
    summary = {"parts": [summarize_dir(d.resolve()) for d in args.directories]}
    args.dest.mkdir(parents=True, exist_ok=True)
    for name, content in (("summary.json", json.dumps(summary, indent=2, allow_nan=False) + "\n"),
                          ("results.md", markdown(summary))):
        (args.dest / name).write_text(content)  # derived from the raw records; safe to regenerate
    print(json.dumps([{"part": p["part"], "recorded": p["recorded_runs"], "scheduled": p["scheduled_runs"],
                       "statuses": p["status_counts"]} for p in summary["parts"]]))
