"""Part C4 metrics (campaign-v4-protocol.md, Amendment 1).

    summarize_c4.py runs/partC4 [--dest DIR]

Writes DIR/c4-results.md and DIR/c4-summary.json (derived, regenerated on each call; DIR
defaults to this directory). Run after ``replay_v4.py runs/partC4`` has passed.

Definitions shared with campaign 4 come from ``summarize_v4`` (unchanged): solved (status
optimal or gaplimit, normal worker exit, incumbent passed the independent primal check), time
charged (total_seconds + preparation_seconds), SGM with shift 1 s over the instances that every
mode solved (full) or completed with a root bound (root), per-run time ratios to baseline over
the instances both solved/completed (median, geometric mean), root bound (root_dual, or the
final dual bound of a run that ended at the root without one), separator funnel.

C4 additions: for ref in {optimum, bound (ii)} the root gap closed of mode m is
(root(m) - root(baseline)) / (ref - root(baseline)) when ref > root(baseline); the optimum and
bound (ii) are the case fields ``known_optimum`` and ``reference_bound_ii`` (mechanism_c4.py).
Nodes: median node count per mode over the commonly solved full runs and over all full runs.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import statistics

import summarize_v4 as sv

HERE = Path(__file__).resolve().parent
REFS = (("optimum", "known_optimum"), ("bound_ii", "reference_bound_ii"))


def median(values):
    values = [v for v in values if v is not None]
    return statistics.median(values) if values else None


def gap_tables(phase, cases):
    rows = []
    for row in phase["models_table"]:
        case = cases[row["name"]]
        base = (row["runs"].get("baseline") or {}).get("root_bound")
        out = {"name": row["name"], "n": case["mechanism"]["n"], "instance_seed": case["mechanism"]["seed"],
               "optimum": case["known_optimum"], "bound_ii": case["reference_bound_ii"], "baseline_root": base,
               "root": {m: (r or {}).get("root_bound") for m, r in row["runs"].items()},
               "closed": {}}
        for label, key in REFS:
            target = case[key]
            out["closed"][label] = {
                m: (v - base) / (target - base) for m, v in out["root"].items()
                if m != "baseline" and sv.finite(v) and sv.finite(base) and target - base > 0}
        rows.append(out)
    medians = {}
    for label, _ in REFS:
        modes = sorted({m for r in rows for m in r["closed"][label]}, key=sv.mode_rank)
        medians[label] = {m: {"all": median([r["closed"][label].get(m) for r in rows]),
                              **{f"n={n}": median([r["closed"][label].get(m) for r in rows if r["n"] == n])
                                 for n in sorted({r["n"] for r in rows})}}
                          for m in modes}
    return rows, medians


def node_table(phase):
    modes = phase["modes"]
    rows = phase["models_table"]
    common = [r for r in rows if all((r["runs"].get(m) or {}).get("solved") for m in modes)]
    return {m: {"median_nodes_common_solved": median([r["runs"][m]["nodes"] for r in common]),
                "median_nodes_all": median([(r["runs"].get(m) or {}).get("nodes") for r in rows]),
                "common_solved": len(common)} for m in modes}


def summarize(out):
    part = sv.summarize_dir(out)
    cases = {p.stem: json.loads(p.read_text()) for p in (out / "cases").glob("*.json")}
    result = {"part": part["part"], "directory": str(out), "scheduled_runs": part["scheduled_runs"],
              "recorded_runs": part["recorded_runs"], "missing_runs": part["missing_runs"],
              "status_counts": part["status_counts"], "replay": part["replay"], "phases": {}}
    for name, phase in part["phases"].items():
        entry = {"phase": phase["phase"], "modes": phase["modes"], "cut_modes": phase["cut_modes"],
                 "time_limit": phase["time_limit"], "worker_timeout": phase["worker_timeout"],
                 "node_limit": phase["node_limit"], "models": phase["models"],
                 "by_mode": {m: {k: t[k] for k in ("runs", "solved", "status_counts", "failures", "flagged",
                                                     "cuts", "runs_with_cuts", "missing_cut_logs",
                                                     "soft_budget_overshoots", "funnel")}
                             for m, t in phase["by_mode"].items()},
                 "times": {"basis": phase["times"]["basis"], "common_pairs": phase["times"]["pooled"]["common_pairs"],
                           "sgm": phase["times"]["pooled"]["sgm"],
                           "sgm_solver_seconds": phase["times"]["pooled"]["sgm_solver_seconds"],
                           "ratio_summary": phase["times"]["ratio_summary"]},
                 "bounds": phase["bounds"], "models_table": phase["models_table"]}
        if phase["phase"] == "root":
            entry["gap_rows"], entry["gap_closed_median"] = gap_tables(phase, cases)
        else:
            entry["nodes"] = node_table(phase)
        result["phases"][name] = entry
    result["references"] = [{"name": c["name"], "n": c["mechanism"]["n"], "seed": c["mechanism"]["seed"],
                             "c": c["mechanism"]["coupling"]["c"], "sum_y_star": c["mechanism"]["coupling"]["sum_y_star"],
                             "optimum": c["known_optimum"], "optimum_exact": c["known_optimum_exact"],
                             "bound_ii": c["reference_bound_ii"],
                             "optimum_minus_bound_ii": c["known_optimum"] - c["reference_bound_ii"]}
                            for c in sorted(cases.values(), key=lambda c: (c["mechanism"]["n"], c["mechanism"]["seed"]))]
    return result


def fmt(value, digits=4):
    return sv.fmt(value, digits)


def markdown(s):
    lines = ["# Campaign 4, Part C4 results (path family with a binding coupling row)", "",
             f"Generated by `summarize_c4.py` from `{s['directory']}`; definitions are in its docstring. "
             "Timings are descriptive (shared host, at most six single-threaded workers). Bounds are numerical "
             "solver bounds; only recorded cuts are certified, and only where the replay passed.", "",
             f"Scheduled runs {s['scheduled_runs']}, recorded {s['recorded_runs']}, missing {len(s['missing_runs'])}. "
             "Statuses: " + ", ".join(f"{k} {v}" for k, v in sorted(s["status_counts"].items(), key=str)) + ".", ""]
    replay = s["replay"]
    if replay:
        lines += [f"Replay: passed {replay['passed']}; {replay['replayed_cuts']}/{replay['cuts']} cuts replayed; "
                  f"failed runs {len(replay['failed_runs'])}; config failures "
                  f"{len(replay['wrapper'].get('config_failures') or [])}; Gurobi record failures "
                  f"{len(replay['wrapper'].get('gurobi_failures') or [])}; tampering controls: "
                  + (", ".join(f"{m} {'all rejected' if ok else 'NOT all rejected'}"
                               for m, ok in replay["tamper_by_mode"].items()) or "none") + ".", ""]
    else:
        lines += ["Replay: not run yet.", ""]
    lines += ["## Reference values", "",
              "Optimum: Gurobi 13.0.3 on the perspective MISOCP, re-solved exactly for the chosen pairs and "
              "certified by the Lagrangian dual (`c4-references.json`). Bound (ii): "
              "min sum_i conv(phi_i)(y_i) s.t. the coupling row, by bisection on the multiplier.", "",
              "| Instance | c | sum y* | Optimum | Bound (ii) | Optimum - (ii) |", "|---|---:|---:|---:|---:|---:|"]
    for r in s["references"]:
        lines.append(f"| {r['name']} | {r['c']} | {r['sum_y_star']} | {r['optimum']:.12g} | {r['bound_ii']:.12g} | "
                     f"{r['optimum_minus_bound_ii']:.3g} |")
    lines.append("")
    for name, p in s["phases"].items():
        lines += [f"## {name}: {p['models']} instances, soft {p['time_limit']:g} s, hard {p['worker_timeout']:g} s, "
                  f"node limit {p['node_limit']}", "",
                  "| Mode | Runs | Solved | Statuses | Failures | Flagged | Cuts | Runs with cuts | Missing cut logs | Soft overshoots |",
                  "|---|---:|---:|---|---:|---:|---:|---:|---:|---:|"]
        for m, t in p["by_mode"].items():
            statuses = ", ".join(f"{k} {v}" for k, v in sorted(t["status_counts"].items(), key=str))
            lines.append(f"| {m} | {t['runs']} | {t['solved']} | {statuses} | {len(t['failures'])} | {len(t['flagged'])} | "
                         f"{t['cuts']} | {t['runs_with_cuts']} | {len(t['missing_cut_logs'])} | "
                         f"{len(t['soft_budget_overshoots'])} |")
        tm = p["times"]
        lines += ["", f"Times over the instances {tm['basis']} ({tm['common_pairs']}); per-run ratios to baseline over "
                  "the instances both solved/completed:", "",
                  "| Mode | SGM s | SGM solver s | Ratio median | Ratio geometric mean | Faster than baseline | Pairs |"
                  + (" Median nodes (common solved) | Median nodes (all) |" if "nodes" in p else ""),
                  "|---|---:|---:|---:|---:|---:|---:|" + ("---:|---:|" if "nodes" in p else "")]
        for m in p["modes"]:
            ratio = tm["ratio_summary"].get(m, {})
            line = (f"| {m} | {fmt(tm['sgm'][m])} | {fmt(tm['sgm_solver_seconds'][m])} | {fmt(ratio.get('median'))} | "
                    f"{fmt(ratio.get('geometric_mean'))} | {fmt(ratio.get('faster_than_reference'))} | {fmt(ratio.get('count'))} |")
            if "nodes" in p:
                line += f" {fmt(p['nodes'][m]['median_nodes_common_solved'])} | {fmt(p['nodes'][m]['median_nodes_all'])} |"
            lines.append(line)
        lines += ["", "Paired bounds versus baseline (root bound for root runs, final dual bound for full runs):", "",
                  "| Mode | rtol | Better | Tie | Worse | Unavailable | Flagged |", "|---|---|---:|---:|---:|---:|---:|"]
        for rtol, table in p["bounds"].items():
            for m, v in table.items():
                c = v["counts"]
                lines.append(f"| {m} | {rtol} | {c.get('better', 0)} | {c.get('tie', 0)} | {c.get('worse', 0)} | "
                             f"{c.get('unavailable', 0)} | {c.get('flagged', 0)} |")
        lines.append("")
        if p["cut_modes"]:
            lines += ["Separator funnel (sums over runs):", "",
                      "| Mode | Callbacks | Support calls | Cert. failures | Rounding rej. | Binding rej. | Binding causes | Cuts |",
                      "|---|---:|---:|---:|---:|---:|---|---:|"]
            for m in p["cut_modes"]:
                f = p["by_mode"][m]["funnel"]
                causes = ", ".join(f"{k} {v}" for k, v in sorted(f["row_binding_rejection_causes"].items())) or "-"
                lines.append(f"| {m} | {f['calls']} | {f['certification_calls']} | {f['certification_failures']} | "
                             f"{f['row_rounding_rejections']} | {f['row_binding_rejections']} | {causes} | {f['cuts']} |")
            lines.append("")
        if p["phase"] == "root":
            modes = p["modes"]
            lines += ["Root bounds; in parentheses the root gap closed relative to the optimum / relative to bound (ii):", "",
                      "| Instance | Optimum | Bound (ii) | " + " | ".join(modes) + " |",
                      "|---|---:|---:|" + "---:|" * len(modes)]
            for r in p["gap_rows"]:
                cells = []
                for m in modes:
                    text = fmt(r["root"].get(m), 6)
                    if m in r["closed"]["optimum"]:
                        text += f" ({fmt(r['closed']['optimum'][m], 3)} / {fmt(r['closed']['bound_ii'].get(m), 3)})"
                    cells.append(text)
                lines.append(f"| {r['name']} | {r['optimum']:.6g} | {r['bound_ii']:.6g} | " + " | ".join(cells) + " |")
            lines.append("")
            for label, title in (("optimum", "relative to the optimum"), ("bound_ii", "relative to bound (ii)")):
                med = p["gap_closed_median"][label]
                groups = sorted({g for v in med.values() for g in v}, key=lambda g: (g != "all", len(g), g))
                lines += [f"Median root gap closed {title}:", "", "| Mode | " + " | ".join(groups) + " |",
                          "|---|" + "---:|" * len(groups)]
                for m, v in med.items():
                    lines.append(f"| {m} | " + " | ".join(fmt(v.get(g), 3) for g in groups) + " |")
                lines.append("")
        else:
            modes = p["modes"]
            lines += ["Full runs (status / seconds / nodes / final dual):", "",
                      "| Instance | Optimum | " + " | ".join(modes) + " |", "|---|---:|" + "---|" * len(modes)]
            for row in p["models_table"]:
                cells = ["-" if row["runs"].get(m) is None else
                         f"{fmt(row['runs'][m]['status'])} / {fmt(row['runs'][m]['seconds'], 3)} / "
                         f"{fmt(row['runs'][m]['nodes'])} / {fmt(row['runs'][m]['dual'], 6)}" for m in modes]
                lines.append(f"| {row['name']} | {fmt(row['target'], 6)} | " + " | ".join(cells) + " |")
            lines.append("")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--dest", type=Path, default=HERE)
    args = parser.parse_args()
    summary = summarize(args.directory.resolve())
    args.dest.mkdir(parents=True, exist_ok=True)
    (args.dest / "c4-summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n")
    (args.dest / "c4-results.md").write_text(markdown(summary))
    print(json.dumps({"recorded": summary["recorded_runs"], "scheduled": summary["scheduled_runs"],
                      "statuses": summary["status_counts"], "replay_passed": (summary["replay"] or {}).get("passed")}))
