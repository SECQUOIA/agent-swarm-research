"""Write sections/B-tables.tex from the raw run records of campaigns 3 and 4 (standard library only).

    python make_appendix_tables_v4.py

Supersedes make_appendix_tables.py (campaign-3 records only), which is kept.
Tables: tab:partA, tab:partB, tab:partD, tab:path-detail, tab:path-fresh.
Reads experiments/{v3,v3d,v4}/runs/*/records.jsonl and cases/, the Part B and
Part D selection files and the Part A list in
research-20261003-convexification/experiments/holdout-selection.json.

Definitions (as in summarize_v4.py and the campaign-4 digests):
- root bound: root_dual; for a run that ended at the root (node limit 1, or at
  most one node) without a finite root_dual, the final dual bound `dual`;
- solved: status optimal or gaplimit and primal_check.passed true; a run whose
  primal check failed is marked with a dagger and explained in the caption;
- time: total_seconds + preparation_seconds;
- root gap closed: (root(mode) - root(baseline)) / (z* - root(baseline)),
  reported only where sign * (z* - root(baseline)) > 0 (sign -1 for
  maximization); z* is the case field known_optimum (path family) or
  reference_primal (MINLPLib best known primal value).
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments"
OUT = ROOT / "sections" / "B-tables.tex"
HOLDOUT = ROOT.parent / "research-20261003-convexification" / "experiments" / "holdout-selection.json"

KEEP = ("name", "mode", "phase", "seed", "status", "sense", "primal", "dual", "root_dual",
        "nodes", "node_limit", "total_seconds", "preparation_seconds", "primal_check")
STATUS = {"optimal": "o", "gaplimit": "g", "timelimit": "t", "nodelimit": "n"}
STATUS_WORDS = {"o": "optimal", "g": "gap limit", "t": "time limit", "n": "node limit"}


# ---------------------------------------------------------------- data

def load_runs(directory):
    """(name, phase, mode) -> record without the bulky fields; seed 0 only."""
    runs = {}
    with open(EXP / directory / "records.jsonl") as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            if r["seed"] != 0:
                continue
            key = (r["name"], r["phase"], r["mode"])
            if key in runs:
                raise SystemExit(f"duplicate record in {directory}: {key}")
            slim = {k: r.get(k) for k in KEEP}
            slim["cuts"] = len(r["cuts"]) if isinstance(r.get("cuts"), list) else None
            runs[key] = slim
    return runs


def load_cases(directory):
    return {c["name"]: c for c in (json.loads(p.read_text()) for p in (EXP / directory / "cases").glob("*.json"))}


def get(runs, name, phase, mode):
    try:
        return runs[(name, phase, mode)]
    except KeyError:
        raise SystemExit(f"missing record: {name} {phase} {mode}") from None


def finite(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def root_bound(r):
    if finite(r["root_dual"]):
        return r["root_dual"]
    if (r["node_limit"] == 1 or (r["nodes"] is not None and r["nodes"] <= 1)) and finite(r["dual"]):
        return r["dual"]
    return None


def seconds(r):
    return r["total_seconds"] + (r["preparation_seconds"] or 0.0)


def check_failed(r):
    return (r["primal_check"] or {}).get("passed") is False


def gap_closed(value, base, target, sense):
    sign = -1 if sense == "max" else 1
    if not (finite(value) and finite(base) and finite(target)) or not sign * (target - base) > 0:
        return None
    return (value - base) / (target - base)


def path_order(cases):
    return sorted(cases, key=lambda n: (cases[n]["mechanism"]["n"], cases[n]["mechanism"]["seed"]))


# ---------------------------------------------------------------- formatting

def tex_name(name):
    return "\\code{" + name.replace("_", "\\_") + "}"


def num(x):
    """Four significant digits; values of at least 1000 without decimals; math mode."""
    if not finite(x):
        return "--"
    if abs(x) >= 1000:
        s = f"{x:.0f}"
    else:
        s = f"{x:.4g}"
        if "e" in s:
            mantissa, exponent = s.split("e")
            s = f"{mantissa}\\cdot10^{{{int(exponent)}}}"
    return "$0$" if s == "-0" else f"${s}$"


class Table:
    """Collects the status letters used and the notes for runs that failed the primal check."""

    def __init__(self):
        self.letters = set()
        self.notes = []

    def flag(self, r, text):
        if not check_failed(r):
            return text
        check = r["primal_check"]
        self.notes.append(
            f"\\textsuperscript{{\\dag}}The incumbent of the {r['mode']} {r['phase']} run of "
            f"{tex_name(r['name'])} failed the independent primal check: SCIP reports the objective "
            f"value {num(r['primal'])}, the original model gives {num(check.get('objective'))}. "
            "The run is flagged, and its bound is not used in comparisons.")
        return text + "\\textsuperscript{\\dag}"

    def status(self, r, value):
        letter = STATUS.get(r["status"], r["status"].replace("_", "\\_"))
        self.letters.add(letter)
        return self.flag(r, f"{letter} {num(value)}")

    def root(self, r):
        return self.flag(r, num(root_bound(r)))

    def legend(self):
        known = [f"{k} {STATUS_WORDS[k]}" for k in "ogtn" if k in self.letters]
        other = sorted(self.letters - set(STATUS_WORDS))
        return "Status: " + ", ".join(known + other) + "."

    def caption(self, text, label):
        return "\\caption{" + " ".join([text, self.legend()] + self.notes) + "}\\label{" + label + "}"


def table(caption, colspec, header, rows, tabcolsep=None):
    sep = [f"\\setlength{{\\tabcolsep}}{{{tabcolsep}}}"] if tabcolsep else []
    return "\n".join(["\\begin{table}[ht]", "\\centering\\scriptsize", *sep, caption,
                      f"\\begin{{tabular}}{{{colspec}}}", "\\toprule", *header, "\\midrule",
                      *rows, "\\bottomrule", "\\end{tabular}", "\\end{table}", ""])


def row(cells):
    return " & ".join(cells) + "\\\\"


# ---------------------------------------------------------------- tables

def part_a():
    root, full = load_runs("v3/runs/partA-root"), load_runs("v3/runs/partA-full")
    names = [e["name"] if isinstance(e, dict) else e for e in json.loads(HOLDOUT.read_text())["selected"]]
    t = Table()
    rows = []
    for n in names:
        rb, rd = get(root, n, "root", "baseline"), get(root, n, "root", "all-diag")
        fb, fa = get(full, n, "full", "baseline"), get(full, n, "full", "all")
        rows.append(row([tex_name(n), t.root(rb), t.root(rd), str(rd["cuts"]),
                         t.status(fb, seconds(fb)), t.status(fa, seconds(fa)), str(fa["cuts"])]))
    caption = t.caption(
        "Campaign~3, Part~A: the 30 models of campaign~2, in the order of selection. Root runs "
        "(node limit~1, 60\\,s): root bound of the baseline (SCIP default) and of mode "
        "\\code{all-diag}, and the number of cuts that \\code{all-diag} added. Full runs (seed~0, "
        "300\\,s): status and time in seconds of the baseline and of mode \\code{all}, and the "
        "number of cuts that \\code{all} added.", "tab:partA")
    header = ["& \\multicolumn{3}{c}{Root run} & \\multicolumn{3}{c}{Full run, seed 0}\\\\",
              "\\cmidrule(lr){2-4}\\cmidrule(l){5-7}",
              row(["Model", "Baseline", "\\code{all-diag}", "Cuts", "Baseline", "\\code{all}", "Cuts"])]
    return table(caption, "@{}lrrrrrr@{}", header, rows)


def part_b():
    b, b2 = load_runs("v3/runs/partB"), load_runs("v4/runs/partB2")
    names = [e["name"] for e in json.loads((EXP / "v3/scan/partB-selection.json").read_text())["selected"]]
    t = Table()
    rows = []
    for n in names:
        fb, fa = get(b, n, "full", "baseline"), get(b, n, "full", "all")
        roots = [get(b, n, "root", "baseline"), get(b, n, "root", "all-diag"),
                 get(b2, n, "root", "baseline-noaggr"), get(b2, n, "root", "all-diag-noaggr"),
                 get(b2, n, "root", "baseline-extra")]
        rows.append(row([tex_name(n), *(t.root(r) for r in roots),
                         t.status(fb, seconds(fb)), t.status(fa, seconds(fa)), str(fa["cuts"])]))
    caption = t.caption(
        "Campaign~3, Part~B, and campaign~4, Part~B2: the 30 structure-selected models, in the "
        "order of selection. Root bounds (node limit~1, 60\\,s) of the baseline (SCIP default) and "
        "of mode \\code{all-diag} in Part~B; of the same two with presolve aggregation disabled "
        "(\\code{baseline-noaggr}, \\code{all-diag-noaggr}) and of SCIP with its disabled nonconvex "
        "separators switched on (\\code{baseline-extra}) in Part~B2. Full runs of Part~B (seed~0, "
        "300\\,s): status and time in seconds of the baseline and of mode \\code{all}, and the "
        "number of cuts that \\code{all} added.", "tab:partB")
    header = ["& \\multicolumn{2}{c}{Root bound, Part B} & \\multicolumn{3}{c}{Root bound, Part B2} & "
              "\\multicolumn{3}{c}{Full run, Part B, seed 0}\\\\",
              "\\cmidrule(lr){2-3}\\cmidrule(lr){4-6}\\cmidrule(l){7-9}",
              "& & & \\multicolumn{2}{c}{no aggregation} & & & &\\\\",
              "\\cmidrule(lr){4-5}",
              row(["Model", "Baseline", "\\code{all-diag}", "Baseline", "\\code{all-diag}", "Extra",
                   "Baseline", "\\code{all}", "Cuts"])]
    return table(caption, "@{}lrrrrrrrr@{}", header, rows, "3pt")


def part_d():
    root, full = load_runs("v4/runs/partD-root"), load_runs("v4/runs/partD-full")
    cases = load_cases("v4/runs/partD-root")
    names = [e["name"] for e in json.loads((EXP / "v4/scanD/partD-selection.json").read_text())["selected"]]
    t = Table()
    rows = []
    for n in names:
        try:
            best = float(cases[n].get("reference_primal"))
        except (TypeError, ValueError):
            best = None
        rb, rd, rx = (get(root, n, "root", m) for m in ("baseline", "all-diag", "baseline-extra"))
        fulls = [get(full, n, "full", m) for m in ("baseline", "all", "baseline-extra")]
        senses = {r["sense"] for r in (rb, rd, rx, *fulls)}
        if len(senses) != 1:
            raise SystemExit(f"inconsistent objective sense for {n}: {senses}")
        rows.append(row([tex_name(n), num(best), senses.pop(), t.root(rb), t.root(rd), t.root(rx),
                         str(rd["cuts"]), *(t.status(r, r["dual"]) for r in fulls)]))
    caption = t.caption(
        "Campaign~4, Part~D: the 20 larger models that SCIP did not solve in 60\\,s, in the order "
        "of selection. Best known: best known primal value of the MINLPLib metadata (none for "
        "\\code{mpbp\\_31}); sense: objective sense. Root runs (node limit~1, 120\\,s): root bound "
        "of the baseline (SCIP default), of mode \\code{all-diag} and of SCIP with its disabled "
        "nonconvex separators switched on (\\code{baseline-extra}), and the number of cuts that "
        "\\code{all-diag} added. Full runs (seed~0, 300\\,s): status and final dual bound of the "
        "baseline, of mode \\code{all} and of \\code{baseline-extra}.", "tab:partD")
    header = ["& & & \\multicolumn{4}{c}{Root run} & \\multicolumn{3}{c}{Full run: final dual bound}\\\\",
              "\\cmidrule(lr){4-7}\\cmidrule(l){8-10}",
              row(["Model", "Best known", "Sense", "Baseline", "\\code{all-diag}", "Extra", "Cuts",
                   "Baseline", "\\code{all}", "Extra"])]
    return table(caption, "@{}lrlrrrrrrr@{}", header, rows, "3pt")


def path_detail():
    c3, v3d, c2 = load_runs("v3/runs/partC"), load_runs("v3d/runs/partC-rowdir"), load_runs("v4/runs/partC2")
    cases = load_cases("v3/runs/partC")
    t = Table()
    rows = []
    for n in path_order(cases):
        case = cases[n]
        opt = case["known_optimum"]
        base = get(c3, n, "root", "baseline")
        b = root_bound(base)
        if root_bound(get(v3d, n, "root", "baseline")) != b:
            raise SystemExit(f"{n}: the v3d baseline root bound differs from campaign 3")
        modes = [get(c2, n, "root", "baseline-novarlocks"), get(c2, n, "root", "baseline-extra"),
                 get(c3, n, "root", "all-diag-mech"), get(c2, n, "root", "frozen-wide"),
                 get(v3d, n, "root", "all-diag-mech"), get(v3d, n, "root", "all-diag-mech-wide")]
        fulls = [get(c3, n, "full", "baseline"), get(c2, n, "full", "frozen-wide"),
                 get(v3d, n, "full", "all-diag-mech-wide"), get(c2, n, "full", "gurobi")]
        rows.append(row([str(case["mechanism"]["n"]), str(case["mechanism"]["seed"]), num(opt), t.root(base),
                         *(t.flag(r, num(gap_closed(root_bound(r), b, opt, "min"))) for r in modes),
                         *(t.status(r, seconds(r)) for r in fulls)]))
    caption = t.caption(
        "The path family, seeds 0--4 (the instances of campaign~3): number of copies $n$, seed, "
        "optimum $z^\\ast$ and the baseline (SCIP default) root bound $z_{\\text{base}}$ of "
        "campaign~3. Root gap closed $(z-z_{\\text{base}})/(z^\\ast-z_{\\text{base}})$, with $z$ the "
        "root bound of: SCIP with \\code{checkvarlocks} off (\\code{baseline-novarlocks}) and with "
        "its disabled nonconvex separators on (\\code{baseline-extra}), both Part~C2; the separator "
        "with remainder directions and mechanism limits (\\code{all-diag-mech}, campaign~3) or wide "
        "limits (\\code{frozen-wide}, Part~C2); and with whole-row directions and mechanism or wide "
        "limits (post hoc diagnostic). Limits as in Table~\\ref{tab:modes}. Root runs: node "
        "limit~1, 120\\,s. Full runs (300\\,s): status and time in seconds of the baseline "
        "(campaign~3), of the separator with remainder directions and wide limits (Part~C2), with "
        "whole-row directions and wide limits (post hoc) and of Gurobi (Part~C2).", "tab:path-detail")
    header = ["& & & Baseline & \\multicolumn{6}{c}{Root gap closed} & "
              "\\multicolumn{4}{c}{Full run: status and time (s)}\\\\",
              "\\cmidrule(lr){5-10}\\cmidrule(l){11-14}",
              "& & & root & \\multicolumn{2}{c}{SCIP} & \\multicolumn{2}{c}{Remainder} & "
              "\\multicolumn{2}{c}{Whole row} & & Remainder & Whole row &\\\\",
              "\\cmidrule(lr){5-6}\\cmidrule(lr){7-8}\\cmidrule(lr){9-10}",
              row(["$n$", "Seed", "Optimum", "bound", "locks off", "extra", "mech.", "wide", "mech.",
                   "wide", "Baseline", "wide", "wide", "Gurobi"])]
    return table(caption, "@{}rrrrrrrrrrrrrr@{}", header, rows, "3pt")


def path_fresh():
    t = Table()
    blocks = []
    parts = (("v4/runs/partC3", "all-diag-mech",
              "Part C3: coupling row $\\sum_iy_i\\le0.8n$, not binding; rem.: \\code{all-diag-mech}"),
             ("v4/runs/partC4", "frozen-wide",
              "Part C4: coupling row $\\sum_iy_i\\le c$, binding; rem.: \\code{frozen-wide}"))
    for directory, remainder, title in parts:
        runs, cases = load_runs(directory), load_cases(directory)
        rows = [f"\\multicolumn{{12}}{{@{{}}l}}{{\\emph{{{title}}}}}\\\\"]
        for n in path_order(cases):
            case = cases[n]
            opt = case["known_optimum"]
            bound_ii = case.get("reference_bound_ii")
            base = get(runs, n, "root", "baseline")
            b = root_bound(base)
            modes = [get(runs, n, "root", m) for m in ("baseline-extra", remainder, "rowdir-wide")]
            fulls = [get(runs, n, "full", m) for m in ("baseline", remainder, "rowdir-wide", "gurobi")]
            rows.append(row([str(case["mechanism"]["n"]), str(case["mechanism"]["seed"]), num(opt),
                             num(opt - bound_ii) if finite(bound_ii) else "--", t.root(base),
                             *(t.flag(r, num(gap_closed(root_bound(r), b, opt, "min"))) for r in modes),
                             *(t.status(r, seconds(r)) for r in fulls)]))
        blocks.append(rows)
    caption = t.caption(
        "The path family, seeds 5--9 (campaign~4): Part~C3 with the coupling row of campaign~3, "
        "which does not bind, and Part~C4 with a binding coupling row. Number of copies $n$, seed, "
        "optimum $z^\\ast$; opt.$-$(ii): optimum minus bound~(ii), the best root bound that cuts on "
        "the blocks can give (C4 only); baseline (SCIP default) root bound $z_{\\text{base}}$. Root "
        "gap closed $(z-z_{\\text{base}})/(z^\\ast-z_{\\text{base}})$, with $z$ the root bound of SCIP "
        "with its disabled nonconvex separators on (\\code{baseline-extra}), of the separator with "
        "remainder directions (rem.; mechanism limits in C3, wide limits in C4) and of the separator "
        "with whole-row directions and wide limits (\\code{rowdir-wide}). Root runs: node limit~1, "
        "120\\,s. Full runs (300\\,s): status and time in seconds of the baseline, of the two "
        "separator modes and of Gurobi.", "tab:path-fresh")
    header = ["& & & & Baseline & \\multicolumn{3}{c}{Root gap closed} & "
              "\\multicolumn{4}{c}{Full run: status and time (s)}\\\\",
              "\\cmidrule(lr){6-8}\\cmidrule(l){9-12}",
              row(["$n$", "Seed", "Optimum", "opt.$-$(ii)", "root bound", "extra", "rem.", "whole row",
                   "Baseline", "rem.", "whole row", "Gurobi"])]
    rows = blocks[0] + ["\\midrule"] + blocks[1]
    return table(caption, "@{}rrrrrrrrrrrr@{}", header, rows, "3pt")


INTRO = r"""\paragraph{Per-model and per-instance results.}
Tables~\ref{tab:partA}--\ref{tab:path-fresh} list the runs behind
Sections~\ref{sec:minlplib} and~\ref{sec:mechanism}. A root bound is SCIP's dual
bound at the end of the root node; for a run that ended at the root without
reporting one, because the root node was pruned, it is the final dual bound.
Times are the seconds charged to the budget (Section~\ref{sec:setup}). Numbers
have four significant digits; values of at least 1000 are rounded to integers.
"""


def main():
    parts = [INTRO, part_a(), part_b(), part_d(), path_detail(), path_fresh()]
    OUT.write_text("\n".join(parts))
    print(f"wrote {OUT.relative_to(ROOT)}: tab:partA, tab:partB, tab:partD, tab:path-detail, tab:path-fresh")


if __name__ == "__main__":
    main()
