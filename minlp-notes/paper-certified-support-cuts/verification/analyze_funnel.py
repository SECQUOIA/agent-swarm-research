#!/usr/bin/env python3
"""Separator funnel and time decomposition from the archived records.

Standard library only; read-only. Prints Markdown tables to stdout.

    python3 analyze_funnel.py [--repro funnel_repro.jsonl]

Record sets (every cut mode is reported; baseline enters only the time tables):

- campaign 2: research-20261003-convexification/experiments/campaign-v2/records.jsonl
- repair cohort: research-20261003-convexification/experiments/repair-discovery-v1/records.jsonl
- campaign 3: paper-certified-support-cuts/experiments/v3/runs/*/records.jsonl
- post hoc row-direction diagnostic: paper-certified-support-cuts/experiments/v3d/runs/*/records.jsonl

Funnel. The callback (solver/integration.py, RowSeparator.sepaexeclp, identical
in all four snapshots for these steps) ends every support call in exactly one
of: certification failure (no cut; outcome incomplete, unsupported or empty),
rounding rejection, insufficient violation (``violation <= threshold *
max(1, ||c||_1)``, not counted by the callback), stored-row (row-binding)
rejection, or an added cut. Hence

    certified             = certification_calls - certification_failures
    insufficient violation = certified - row_rounding_rejections
                             - row_binding_rejections - cuts

which the script checks to be nonnegative. The split of failures by outcome
and of row-binding rejections by cause is not in the records; it comes from
the reruns of reproduce_funnel.py (``--repro``), whose counters are compared
with the archive run by run.

Time. Per record set, phase and mode, over the (model, seed) pairs solved in
every mode of that phase (full and repeat phases) or completed in every mode
(root phases, node limit 1). Solved = summarize_v3.solved: status optimal or
gaplimit, normal exit, incumbent passing the original-model check.
Total time = total_seconds + preparation_seconds (the paper's time measure).
SCIP time excluding the callback = scip_solve_seconds - callback_seconds;
the callback includes lazy discovery, direction LPs, certification and row
export. Shifted geometric means use shift 1 s.
"""
from __future__ import annotations

from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[2])

import argparse
from collections import Counter, defaultdict
import glob
import json
import math
from pathlib import Path
import statistics

REPO = Path((_PUBLIC_REPO))
R3 = REPO / "research-20261003-convexification/experiments"
PAPER = REPO / "paper-certified-support-cuts"
DEFAULT_REPRO = PAPER / "verification/funnel_repro.jsonl"

FAILURES = ("process_timeout", "worker_error", "worker_no_output", "worker_output_parse_error")
METHODS = ("quadratic_polytope", "quadratic_star", "quadratic_polygon", "bernstein", "arb")
PHASE_ORDER = {"full": 0, "repeat": 1, "root": 2}
MODE_ORDER = {m: i for i, m in enumerate(
    ("baseline", "all", "auto", "all-diag", "all-diag-mech", "all-diag-mech-wide"))}


def record_sets():
    """(campaign label, part label, directory holding snapshot/ and cases/, records path)."""
    sets = [("C2", "", R3 / "campaign-v2"), ("Repair", "", R3 / "repair-discovery-v1")]
    for campaign, root in (("C3", PAPER / "experiments/v3/runs"), ("v3d", PAPER / "experiments/v3d/runs")):
        for path in sorted(glob.glob(str(root / "*/records.jsonl"))):
            directory = Path(path).parent
            part = directory.name.replace("-rowdir", "").replace("part", "")
            sets.append((campaign, part.split("-")[0], directory))
    return [(c, p, d, d / "records.jsonl") for c, p, d in sets]


def load_records():
    out = []
    for campaign, part, directory, path in record_sets():
        for line in path.read_text().splitlines():
            r = json.loads(line)
            label = f"{campaign} {part} {r['suite']}".replace("  ", " ") if campaign in ("C2", "Repair") \
                else f"{campaign} {part}"
            r["_set"], r["_dir"], r["_group"] = campaign, str(directory), f"{label} {r['phase']}"
            r["_key"] = f"{directory.name}/{r['run_id']}"
            out.append(r)
    return out


def failed(r):
    return r.get("status") in FAILURES or bool(r.get("worker_status")) or r.get("returncode", 0) != 0


def solved(r):
    check = r.get("primal_check") or {}
    return (not failed(r) and r.get("status") in ("optimal", "gaplimit")
            and check.get("checked") is True and check.get("passed") is True
            and isinstance(r.get("primal"), (int, float)) and math.isfinite(r["primal"]))


def total_time(r):
    return r["total_seconds"] + r.get("preparation_seconds", 0.0)


def callback(r):
    return (r.get("separation") or {}).get("callback_seconds", 0.0)


def scip_excl(r):
    return r["scip_solve_seconds"] - callback(r)


def sgm(values, shift=1.0):
    return math.exp(statistics.fmean(math.log(v + shift) for v in values)) - shift if values else None


def group_order(g):
    campaign = g.split()[0]
    return (["C2", "Repair", "C3", "v3d"].index(campaign), g.split()[1:-1], PHASE_ORDER[g.split()[-1]])


def pct(a, b):
    return f"{100 * a / b:.1f}%" if b else "-"


def funnel(records):
    rows = defaultdict(Counter)
    models = defaultdict(lambda: defaultdict(Counter))
    for r in records:
        if r["mode"] == "baseline":
            continue
        key = (r["_group"], r["mode"])
        f = rows[key]
        f["runs"] += 1
        f["failed runs"] += failed(r)
        s = r.get("separation")
        if not s:
            continue
        f["runs with callback"] += s["calls"] > 0
        f["callbacks"] += s["calls"]
        f["discovery runs"] += r.get("discovery") is not None
        f["discovery incomplete"] += bool(s.get("discovery_incomplete"))
        f["blocks"] += (r.get("discovery") or {}).get("blocks", 0)
        f["auto-eligible blocks"] += (r.get("discovery") or {}).get("auto_eligible", 0)
        calls, fails = s["certification_calls"], s["certification_failures"]
        rounding, binding, cuts = s["row_rounding_rejections"], s["row_binding_rejections"], s["cuts"]
        if cuts != len(r.get("cuts") or []):
            raise SystemExit(f"cut log mismatch in {r['_key']}")
        insufficient = calls - fails - rounding - binding - cuts
        if insufficient < 0:
            raise SystemExit(f"funnel identity violated in {r['_key']}")
        f.update({"support calls": calls, "failed": fails, "certified": calls - fails,
                  "insufficient violation": insufficient, "rounding": rounding,
                  "row binding": binding, "cuts": cuts})
        f["runs with row binding"] += binding > 0
        models[key][r["name"]].update({"binding": binding, "cuts": cuts})
        f["runs with cuts"] += cuts > 0
        for c in r.get("cuts") or []:
            f["method " + (c.get("support_stats") or {}).get("method", "unknown")] += 1
            f["polytope skipped"] += "polytope_skipped" in (c.get("support_stats") or {})
    for key in rows:
        rows[key]["models with row binding"] = sum(m["binding"] > 0 for m in models[key].values())
        rows[key]["models all rejected"] = sum(m["binding"] > 0 and not m["cuts"] for m in models[key].values())
    return rows


def print_funnel(rows):
    print("### Funnel per record set, phase and mode (cut modes)\n")
    print("Certified = support calls - failed. Insufficient violation, rounding, row binding and "
          "cuts added partition the certified calls. Row-binding share = row binding / (row binding + cuts), "
          "i.e. the share of certified, violated, safely rounded rows that the stored-row check discarded.\n")
    print("Discovery: runs whose discovery completed (in parentheses: stopped at its deadline). Blocks are summed "
          "over runs (auto-eligible in parentheses). Row-binding models: models with at least one rejection; "
          "in brackets, models on which every violated certified row was rejected (no cut added).\n")
    print("| Set / phase | Mode | Runs (failed) | Runs with callback | Discovery (incomplete) | Blocks (auto-eligible) "
          "| Support calls | Certified | Failed | Insufficient violation | Rounding rej. | Row-binding rej. "
          "(runs / models [all rejected]) | Cuts added (runs) | Row-binding share |")
    print("|---|---|" + "---:|" * 12)
    for key in sorted(rows, key=lambda k: (group_order(k[0]), MODE_ORDER[k[1]])):
        f = rows[key]
        print(f"| {key[0]} | {key[1]} | {f['runs']} ({f['failed runs']}) | {f['runs with callback']} "
              f"| {f['discovery runs']} ({f['discovery incomplete']}) | {f['blocks']} ({f['auto-eligible blocks']}) "
              f"| {f['support calls']} "
              f"| {f['certified']} | {f['failed']} | {f['insufficient violation']} | {f['rounding']} "
              f"| {f['row binding']} ({f['runs with row binding']} / {f['models with row binding']} "
              f"[{f['models all rejected']}]) "
              f"| {f['cuts']} ({f['runs with cuts']}) | {pct(f['row binding'], f['row binding'] + f['cuts'])} |")
    print("\n### Oracle method of every added cut\n")
    print("| Set / phase | Mode | Cuts | " + " | ".join(METHODS) + " | polytope budget fallback |")
    print("|---|---|" + "---:|" * (len(METHODS) + 2))
    totals = Counter()
    for key in sorted(rows, key=lambda k: (group_order(k[0]), MODE_ORDER[k[1]])):
        f = rows[key]
        unknown = [k for k in f if k.startswith("method ") and k[7:] not in METHODS]
        if unknown:
            raise SystemExit(f"unexpected oracle methods {unknown}")
        totals.update({k: v for k, v in f.items() if k.startswith("method ") or k in ("cuts", "polytope skipped")})
        print(f"| {key[0]} | {key[1]} | {f['cuts']} | " + " | ".join(str(f["method " + m]) for m in METHODS)
              + f" | {f['polytope skipped']} |")
    print(f"| **all sets** | | {totals['cuts']} | " + " | ".join(str(totals["method " + m]) for m in METHODS)
          + f" | {totals['polytope skipped']} |")


def time_tables(records):
    by_group = defaultdict(lambda: defaultdict(dict))
    for r in records:
        by_group[r["_group"]][(r["name"], r["seed"])][r["mode"]] = r
    print("\n### Time decomposition over runs solved (full, repeat) or completed (root) in every mode\n")
    print("SGM with shift 1 s. SCIP excl. callback = scip_solve_seconds - callback_seconds. "
          "Ratio columns are per-run ratios to baseline over the same pairs (median; geometric mean).\n")
    print("| Set / phase | Pairs | Mode | SGM total | SGM SCIP solve | SGM SCIP excl. callback | SGM callback "
          "| Sum callback (s) | Nodes | SCIP excl. callback / baseline, median; geo. mean | Total / baseline, median |")
    print("|---|---:|---|" + "---:|" * 8)
    summary = {}
    for group in sorted(by_group, key=group_order):
        pairs = by_group[group]
        modes = sorted({m for d in pairs.values() for m in d}, key=MODE_ORDER.__getitem__)
        ok = solved if group.split()[-1] in ("full", "repeat") else (lambda r: not failed(r) and "total_seconds" in r)
        common = sorted(k for k, d in pairs.items() if all(m in d and ok(d[m]) for m in modes))
        for m in modes:
            rs = [pairs[k][m] for k in common]
            base = [pairs[k]["baseline"] for k in common]
            row = {"pairs": len(common), "sgm_total": sgm([total_time(r) for r in rs]),
                   "sgm_scip": sgm([r["scip_solve_seconds"] for r in rs]),
                   "sgm_scip_excl": sgm([scip_excl(r) for r in rs]),
                   "sgm_callback": sgm([callback(r) for r in rs]),
                   "sum_callback": sum(callback(r) for r in rs), "nodes": sum(r["nodes"] for r in rs)}
            if m != "baseline" and common:
                ex = [max(scip_excl(a), 1e-3) / max(scip_excl(b), 1e-3) for a, b in zip(rs, base)]
                tt = [total_time(a) / total_time(b) for a, b in zip(rs, base)]
                row.update(excl_median=statistics.median(ex),
                           excl_geo=math.exp(statistics.fmean(map(math.log, ex))),
                           total_median=statistics.median(tt))
            summary[(group, m)] = row
            fmt = lambda v: "-" if v is None else f"{v:.3f}"
            ratio = (f"{row['excl_median']:.3f}; {row['excl_geo']:.3f}" if "excl_median" in row else "-")
            print(f"| {group} | {len(common)} | {m} | {fmt(row['sgm_total'])} | {fmt(row['sgm_scip'])} "
                  f"| {fmt(row['sgm_scip_excl'])} | {fmt(row['sgm_callback'])} | {row['sum_callback']:.2f} "
                  f"| {row['nodes']:,} | {ratio} | {fmt(row.get('total_median'))} |")
    return summary


def repro_tables(records, path):
    """Failure outcomes and row-binding causes from reproduce_funnel.py reruns."""
    if not path.is_file():
        print(f"\n(No reproduction file {path}; failure outcomes and rejection causes not shown.)")
        return
    archived = {r["_key"]: r for r in records}
    reps = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    rows = defaultdict(Counter)
    causes, outcomes, examples = defaultdict(Counter), defaultdict(Counter), defaultdict(list)
    for rep in reps:
        r = archived[rep["key"]]
        key = (r["_group"], r["mode"])
        f = rows[key]
        f["targets"] += 1
        if rep.get("error"):
            f["errors"] += 1
            continue
        a, b = r["separation"], rep["separation"]
        match = all(a[k] == b[k] for k in ("calls", "certification_calls", "certification_failures",
                                            "row_binding_rejections", "row_rounding_rejections", "cuts"))
        f["matched"] += match
        f["archived failed"] += a["certification_failures"]
        f["archived row binding"] += a["row_binding_rejections"]
        f["rerun failed"] += b["certification_failures"]
        f["rerun row binding"] += b["row_binding_rejections"]
        tag = "matched" if match else "unmatched"
        for o in rep["failed_calls"]:
            outcomes[key][(o["status"], o.get("reason_class"), tag)] += 1
        for rej in rep["rejections"]:
            causes[key][(rej["cause"], tag)] += 1
            if len(examples[rej["cause"]]) < 3:
                examples[rej["cause"]].append((rep["key"], rej))
    order = sorted(rows, key=lambda k: (group_order(k[0]), MODE_ORDER[k[1]]))
    print("\n### Reproduction coverage (reproduce_funnel.py)\n")
    print("Every cut-mode run with a certification failure or a row-binding rejection was rerun in a fresh "
          "process from a copy of its own snapshot, with its recorded Config, seed and time limit. Full runs were "
          "rerun with node limit 1 (the separator runs only at the root). Matched = all six separator counters "
          "equal the archived run's.\n")
    print("| Set / phase | Mode | Runs rerun | Counters matched | Archived failed / rerun | "
          "Archived row binding / rerun |")
    print("|---|---|---:|---:|---:|---:|")
    for key in order:
        f = rows[key]
        print(f"| {key[0]} | {key[1]} | {f['targets']} | {f['matched']} | {f['archived failed']} / "
              f"{f['rerun failed']} | {f['archived row binding']} / {f['rerun row binding']} |")
    print("\n### Outcomes of failed support calls (reruns)\n")
    print("Counts over all reruns; in parentheses the part from runs whose counters matched the archive.\n")
    kinds = sorted({k[:2] for c in outcomes.values() for k in c}, key=str)
    print("| Set / phase | Mode | " + " | ".join(f"{s} ({rc})" for s, rc in kinds) + " |")
    print("|---|---|" + "---:|" * len(kinds))
    for key in order:
        c = outcomes[key]
        if not c:
            continue
        cells = [f"{c[k + ('matched',)] + c[k + ('unmatched',)]} ({c[k + ('matched',)]})" for k in kinds]
        print(f"| {key[0]} | {key[1]} | " + " | ".join(cells) + " |")
    print("\n### Causes of row-binding rejections (reruns)\n")
    print("Each cell: rejections over all reruns (in parentheses: from runs whose counters matched the archive). "
          "presolve: a block variable of the row is no longer an active column (SCIP status AGGREGATED, MULTAGGR, "
          "FIXED or NEGATED), so SCIP stores the row in other columns and with a constant. SCIP: all variables active, "
          "but SCIP stored a coefficient differently (dropped as zero below epsilon 1e-9, or snapped to the nearest "
          "integer within epsilon).\n")
    category = lambda name: ("presolve", "SCIP", "other").index(name.split(":")[0])
    names = sorted({k[0] for c in causes.values() for k in c}, key=lambda n: (category(n), n))
    print("| Set / phase | Mode | Rejections | " + " | ".join(names) + " | Presolve share |")
    print("|---|---|---:|" + "---:|" * (len(names) + 1))
    total = Counter()
    both = lambda c, n: f"{c[(n, 'matched')] + c[(n, 'unmatched')]} ({c[(n, 'matched')]})"
    for key in order + [None]:
        c = total if key is None else causes[key]
        if not c:
            continue
        if key is not None:
            total.update(c)
        n_all = sum(c.values())
        n_pre = sum(v for (n, _), v in c.items() if category(n) == 0)
        label = "| **all reruns** | " if key is None else f"| {key[0]} | {key[1]} "
        print(f"{label}| {n_all} | " + " | ".join(both(c, n) for n in names) + f" | {pct(n_pre, n_all)} |")
    print("\nExamples (first two per cause):\n")
    for cause in names:
        for key, rej in examples[cause][:2]:
            print(f"- {cause}: `{key}` {json.dumps(rej.get('detail'), sort_keys=True)[:300]}")
    return causes, outcomes, rows


def referee_check(rows, causes):
    """The referee's statement on Part B and the analogous shares in every set."""
    print("\n### Stored-row losses as shares of certified rows\n")
    print("Violated = certified rows that passed the violation test and safe rounding (row binding + cuts added). "
          "Presolve-caused = row-binding rejections classified as presolve in the reruns, scaled to the archived "
          "count when the rerun count differs.\n")
    print("| Set / phase | Mode | Certified | Violated | Row binding | Share of violated | Share of certified "
          "| Presolve-caused (rerun) | Presolve-caused share of violated |")
    print("|---|---|---:|---:|---:|---:|---:|---:|---:|")
    for key in sorted(rows, key=lambda k: (group_order(k[0]), MODE_ORDER[k[1]])):
        f = rows[key]
        if not f["row binding"]:
            continue
        violated = f["row binding"] + f["cuts"]
        c = causes.get(key, Counter())
        rerun = sum(c.values())
        pre = sum(v for (n, _), v in c.items() if n.startswith("presolve"))
        scaled = pre * f["row binding"] / rerun if rerun else 0
        print(f"| {key[0]} | {key[1]} | {f['certified']} | {violated} | {f['row binding']} "
              f"| {pct(f['row binding'], violated)} | {pct(f['row binding'], f['certified'])} "
              f"| {pre} of {rerun} | {pct(scaled, violated)} |")


def part_b_models(records, path):
    """Stored-row rejections / cuts added per Part B model and cut mode, with rerun causes."""
    cols = [("C3 B full", "all"), ("C3 B full", "auto"), ("C3 B root", "all"), ("C3 B root", "auto"),
            ("C3 B root", "all-diag")]
    cell = defaultdict(Counter)
    for r in records:
        if (r["_group"], r["mode"]) in cols and r.get("separation"):
            c = cell[(r["name"], (r["_group"], r["mode"]))]
            c["binding"] += r["separation"]["row_binding_rejections"]
            c["cuts"] += r["separation"]["cuts"]
    archived = {r["_key"]: r for r in records}
    cause = defaultdict(Counter)
    for rep in (json.loads(x) for x in path.read_text().splitlines() if x.strip()):
        r = archived[rep["key"]]
        if r["_group"].startswith("C3 B"):
            for rej in rep["rejections"]:
                cause[r["name"]][rej["cause"].split(":")[0]] += 1
    names = sorted({n for (n, _), c in cell.items() if c["binding"]},
                   key=lambda n: (-sum(cell[(n, k)]["binding"] for k in cols), n))
    print("\n### Part B stored-row rejections by model (campaign 3)\n")
    print("Cells: rejections / cuts added, summed over seeds. Causes: rerun classification over all Part B reruns "
          "of the model.\n")
    print("| Model | " + " | ".join(f"{g.split()[-1]} {m}" for g, m in cols) + " | Causes in reruns |")
    print("|---|" + "---:|" * len(cols) + "---|")
    for n in names:
        print(f"| {n} | " + " | ".join(f"{cell[(n, k)]['binding']} / {cell[(n, k)]['cuts']}" for k in cols)
              + " | " + ", ".join(f"{k} {v}" for k, v in sorted(cause[n].items())) + " |")


def paper_tables(rows, causes, outcomes, coverage, time_summary):
    """Compact tables for campaign 3 and the v3d diagnostic (numbers as in the tables above)."""
    print("\n## Paper tables (campaign 3 and post hoc diagnostic)\n")
    print("Failed support calls split by outcome (incomplete / unsupported / empty) and stored-row rejections "
          "split by cause (presolve: variable aggregated, multi-aggregated or fixed by presolve; SCIP: coefficient "
          "dropped below epsilon or snapped to an integer) come from the reruns; a dagger marks rows whose rerun "
          "totals differ from the archive (runs that reached the 1 s callback allowance). Share = stored-row "
          "rejections / (stored-row rejections + cuts added).\n")
    print("| Set / phase | Mode | Support calls | Certified | Failed (inc. / uns. / empty) | Insufficient violation "
          "| Rounding | Stored-row rej. (presolve / SCIP) | Share | Cuts added | Polytope / star / Bernstein / Arb |")
    print("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for key in sorted(rows, key=lambda k: (group_order(k[0]), MODE_ORDER[k[1]])):
        if key[0].split()[0] not in ("C3", "v3d"):
            continue
        f, o, c, cov = rows[key], outcomes.get(key, Counter()), causes.get(key, Counter()), coverage.get(key, Counter())
        count = lambda counter, test: sum(v for k, v in counter.items() if test(k))
        inc, uns, emp = (count(o, lambda k, s=s: k[0] == s) for s in ("incomplete", "unsupported", "empty"))
        pre = count(c, lambda k: k[0].startswith("presolve"))
        sci = count(c, lambda k: k[0].startswith("SCIP"))
        oth = count(c, lambda k: k[0].startswith("other"))
        dagger = "†" if (cov["rerun failed"] != cov["archived failed"]
                         or cov["rerun row binding"] != cov["archived row binding"]) else ""
        other = f" / other {oth}" if oth else ""
        print(f"| {key[0]} | {key[1]} | {f['support calls']} | {f['certified']} | {f['failed']} ({inc} / {uns} / {emp}) "
              f"| {f['insufficient violation']} | {f['rounding']} | {f['row binding']} ({pre} / {sci}{other}){dagger} "
              f"| {pct(f['row binding'], f['row binding'] + f['cuts'])} | {f['cuts']} "
              f"| {f['method quadratic_polytope']} / {f['method quadratic_star']} / {f['method bernstein']} "
              f"/ {f['method arb']} |")
    print("\nTime over pairs solved in every mode (full phases); SGM in seconds, shift 1 s.\n")
    print("| Set | Pairs | Mode | SGM total | SGM SCIP excl. callback | SGM callback | Nodes "
          "| SCIP excl. callback / baseline (median per run) |")
    print("|---|---:|---|---:|---:|---:|---:|---:|")
    for (group, mode), t in time_summary.items():
        if group.split()[0] in ("C2", "C3", "Repair", "v3d") and group.endswith(" full") and t["pairs"]:
            ratio = f"{t['excl_median']:.3f}" if "excl_median" in t else "-"
            print(f"| {group} | {t['pairs']} | {mode} | {t['sgm_total']:.3f} | {t['sgm_scip_excl']:.3f} "
                  f"| {t['sgm_callback']:.3f} | {t['nodes']:,} | {ratio} |")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repro", type=Path, default=DEFAULT_REPRO)
    args = parser.parse_args()
    records = load_records()
    counts = Counter(r["_group"] for r in records)
    print("## Record sets\n")
    for campaign, part, directory, path in record_sets():
        print(f"- {(campaign + ' ' + part).strip()}: `{path.relative_to(REPO)}`")
    print("\n" + ", ".join(f"{g}: {n}" for g, n in sorted(counts.items(), key=lambda x: group_order(x[0])))
          + f" (total {len(records)} records)\n")
    rows = funnel(records)
    print_funnel(rows)
    time_summary = time_tables(records)
    repro = repro_tables(records, args.repro)
    if repro is not None:
        referee_check(rows, repro[0])
        part_b_models(records, args.repro)
        paper_tables(rows, *repro, time_summary)


if __name__ == "__main__":
    main()
