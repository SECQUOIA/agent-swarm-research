"""Write sections/B-tables.tex from the raw run records of campaigns 3 to 5 (standard library only).

    python make_appendix_tables_v5.py

Extends make_appendix_tables_v4.py, which is kept unchanged:
- tab:partA, tab:partB: maximization models (objective sense from the records)
  are marked (max) in the model column, and the caption names them and says
  that for them a smaller bound is stronger (a sense column would make
  tab:partB wider than the text); tab:partD keeps its sense column and gets
  the same caption remark;
- path family, seeds 0-4: root closures (tab:path-detail) and full runs
  (tab:path-detail-full) of every row of the main-text Table 5, with the
  names of the main text (SCIP, SCIP-nolocks, SCIP-extra, remainder or whole
  row with base or wide limits) and the solved counts;
- path family, seeds 5-9 (Parts 4C3 and 4C4): root closures (tab:path-fresh)
  and full runs (tab:path-fresh-full), adding SCIP-nolocks (Part 5C-a), the
  full runs of SCIP-extra and, for 4C4, the cap-64n root runs of Part 5C-b with
  their distance to the block closure; separate columns for the remainder
  directions with base limits (4C3) and wide limits (4C4);
- star family (Part 5S): root bound as a fraction of the optimum
  (tab:star-detail) and full runs (tab:star-detail-full) of every row of the
  main-text Table tab:stars, with solved counts per k and in total; runs with
  status process_timeout (worker stopped at the hard process limit) are marked
  with a dagger and count as unsolved.
Tables: tab:partA, tab:partB, tab:partD, tab:path-detail, tab:path-detail-full,
tab:path-fresh, tab:path-fresh-full, tab:star-detail, tab:star-detail-full.
Reads experiments/{v3,v3d,v4}/runs/*/records.jsonl and cases/, the Part 5C-a,
5C-b and 5S records and cases in experiments/v5/runs/partC5a, partC5b and
partS5 (not the informational rerun partS5-rerun-spike), the Part B and Part D
selection files and the Part A list in
research-20261003-convexification/experiments/holdout-selection.json.

Definitions (as in make_appendix_tables_v4.py, summarize_v4.py and summarize_v5.py):
- root bound: root_dual; for a run that ended at the root (node limit 1, or at
  most one node) without a finite root_dual, the final dual bound `dual`;
- solved: status optimal or gaplimit and primal_check.passed true; a run whose
  primal check failed is marked with a dagger and explained in the caption;
- time: total_seconds + preparation_seconds;
- root gap closed: (root(mode) - root(baseline)) / (z* - root(baseline)),
  reported only where sign * (z* - root(baseline)) > 0 (sign -1 for
  maximization); z* is the case field known_optimum (path family) or
  reference_primal (MINLPLib best known primal value);
- block closure (Part 4C4): the case field reference_bound_ii; distance of a
  root bound to it: reference_bound_ii - root bound.
The case files of Parts 4C2, 3P, 5C-a and 5C-b must equal those of the part
whose instances they rerun (3C, 4C3, 4C4); the script stops otherwise.
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
SOLVED_CAPTION = ("Solved: number of the runs above it in the column with status optimal or gap limit "
                  "and an incumbent that passed the independent primal check (Section~\\ref{sec:setup}).")


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


def same_cases(cases, directory):
    """Stop unless `directory` has a case file equal to each of `cases`."""
    other = load_cases(directory)
    for name, case in cases.items():
        if other.get(name) != case:
            raise SystemExit(f"case {name} in {directory} differs or is missing")


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


def solved(r):
    return r["status"] in ("optimal", "gaplimit") and (r["primal_check"] or {}).get("passed") is True


def sense(name, records):
    senses = {r["sense"] for r in records}
    if len(senses) != 1:
        raise SystemExit(f"inconsistent objective sense for {name}: {senses}")
    return senses.pop()


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


def num_e4(x):
    """num() of x in units of 1e-4."""
    return num(x * 1e4) if finite(x) else "--"


def and_list(items):
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def model_cell(name, records, maximized):
    """Model name, marked (max) for a maximization model, which is appended to `maximized`."""
    if sense(name, records) != "max":
        return tex_name(name)
    maximized.append(name)
    return tex_name(name) + " (max)"


def sense_caption(maximized):
    """Caption sentence naming the maximization models marked by model_cell()."""
    if not maximized:
        return "All models are minimization models."
    verb = "is a maximization model" if len(maximized) == 1 else "are maximization models"
    return (f"{and_list([tex_name(n) for n in maximized])} {verb}, marked (max), for which a smaller "
            "bound is stronger; all other models are minimization models.")


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

    def full(self, r):
        return self.status(r, seconds(r))

    def root(self, r):
        return self.flag(r, num(root_bound(r)))

    def closed(self, r, base, target):
        return self.flag(r, num(gap_closed(root_bound(r), base, target, "min")))

    def legend(self):
        if not self.letters:
            return None
        known = [f"{k} {STATUS_WORDS[k]}" for k in "ogtn" if k in self.letters]
        other = sorted(self.letters - set(STATUS_WORDS))
        return "Status: " + ", ".join(known + other) + "."

    def caption(self, text, label):
        parts = [p for p in [text, self.legend()] + self.notes if p]
        return "\\caption{" + " ".join(parts) + "}\\label{" + label + "}"


def table(caption, colspec, header, rows, tabcolsep=None):
    sep = [f"\\setlength{{\\tabcolsep}}{{{tabcolsep}}}"] if tabcolsep else []
    return "\n".join(["\\begin{table}[ht]", "\\centering\\scriptsize", *sep, caption,
                      f"\\begin{{tabular}}{{{colspec}}}", "\\toprule", *header, "\\midrule",
                      *rows, "\\bottomrule", "\\end{tabular}", "\\end{table}", ""])


def row(cells):
    return " & ".join(cells) + "\\\\"


def solved_row(lead, columns):
    """Row of solved counts; `columns` holds a list of runs per column, or None for an empty column."""
    return row([lead, *("" if runs is None else str(sum(map(solved, runs))) for runs in columns)])


# ---------------------------------------------------------------- MINLPLib tables

def part_a():
    root, full = load_runs("v3/runs/partA-root"), load_runs("v3/runs/partA-full")
    names = [e["name"] if isinstance(e, dict) else e for e in json.loads(HOLDOUT.read_text())["selected"]]
    t = Table()
    rows, maximized = [], []
    for n in names:
        rb, rd = get(root, n, "root", "baseline"), get(root, n, "root", "all-diag")
        fb, fa = get(full, n, "full", "baseline"), get(full, n, "full", "all")
        rows.append(row([model_cell(n, (rb, rd, fb, fa), maximized), t.root(rb), t.root(rd), str(rd["cuts"]),
                         t.status(fb, seconds(fb)), t.status(fa, seconds(fa)), str(fa["cuts"])]))
    caption = t.caption(
        "Part~3A: the 30 models of campaign~2, in the order of selection. " + sense_caption(maximized) +
        " Root runs (node limit~1, 60\\,s): root bound of the baseline (SCIP default) and of mode "
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
    rows, maximized = [], []
    for n in names:
        fb, fa = get(b, n, "full", "baseline"), get(b, n, "full", "all")
        roots = [get(b, n, "root", "baseline"), get(b, n, "root", "all-diag"),
                 get(b2, n, "root", "baseline-noaggr"), get(b2, n, "root", "all-diag-noaggr"),
                 get(b2, n, "root", "baseline-extra")]
        rows.append(row([model_cell(n, (fb, fa, *roots), maximized), *(t.root(r) for r in roots),
                         t.status(fb, seconds(fb)), t.status(fa, seconds(fa)), str(fa["cuts"])]))
    caption = t.caption(
        "Parts~3B and~4B2: the 30 structure-selected models, in the order of selection. " +
        sense_caption(maximized) +
        " Root bounds (node limit~1, 60\\,s) of the baseline (SCIP default) and "
        "of mode \\code{all-diag} in Part~3B; of the same two with presolve aggregation disabled "
        "(\\code{baseline-noaggr}, \\code{all-diag-noaggr}) and of SCIP with its disabled nonconvex "
        "separators switched on (\\code{baseline-extra}) in Part~4B2. Full runs of Part~3B (seed~0, "
        "300\\,s): status and time in seconds of the baseline and of mode \\code{all}, and the "
        "number of cuts that \\code{all} added.", "tab:partB")
    header = ["& \\multicolumn{2}{c}{Root bound, Part 3B} & \\multicolumn{3}{c}{Root bound, Part 4B2} & "
              "\\multicolumn{3}{c}{Full run, Part 3B, seed 0}\\\\",
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
        rows.append(row([tex_name(n), num(best), sense(n, (rb, rd, rx, *fulls)), t.root(rb), t.root(rd),
                         t.root(rx), str(rd["cuts"]), *(t.status(r, r["dual"]) for r in fulls)]))
    caption = t.caption(
        "Part~4D: the 20 larger models that SCIP did not solve in 60\\,s, in the order "
        "of selection. Best known: best known primal value of the MINLPLib metadata (none for "
        "\\code{mpbp\\_31}); sense: objective sense; for maximization models a smaller bound is "
        "stronger. Root runs (node limit~1, 120\\,s): root bound "
        "of the baseline (SCIP default), of mode \\code{all-diag} and of SCIP with its disabled "
        "nonconvex separators switched on (\\code{baseline-extra}), and the number of cuts that "
        "\\code{all-diag} added. Full runs (seed~0, 300\\,s): status and final dual bound of the "
        "baseline, of mode \\code{all} and of \\code{baseline-extra}.", "tab:partD")
    header = ["& & & \\multicolumn{4}{c}{Root run} & \\multicolumn{3}{c}{Full run: final dual bound}\\\\",
              "\\cmidrule(lr){4-7}\\cmidrule(l){8-10}",
              row(["Model", "Best known", "Sense", "Baseline", "\\code{all-diag}", "Extra", "Cuts",
                   "Baseline", "\\code{all}", "Extra"])]
    return table(caption, "@{}lrlrrrrrrr@{}", header, rows, "3pt")


# ---------------------------------------------------------------- path family

def path_detail():
    """Seeds 0-4: root closures (tab:path-detail) and full runs (tab:path-detail-full)."""
    c3, v3d, c2 = load_runs("v3/runs/partC"), load_runs("v3d/runs/partC-rowdir"), load_runs("v4/runs/partC2")
    cases = load_cases("v3/runs/partC")
    same_cases(cases, "v3d/runs/partC-rowdir")
    same_cases(cases, "v4/runs/partC2")
    # Columns in the order of the main-text Table 5 (part in the comment).
    root_modes = ((c2, "baseline-novarlocks"), (c2, "baseline-extra"),            # 4C2, 4C2
                  (c3, "all-diag-mech"), (c2, "frozen-wide"),                     # 3C, 4C2
                  (v3d, "all-diag-mech"), (v3d, "all-diag-mech-wide"))            # 3P, 3P
    full_modes = ((c3, "baseline"), (c2, "baseline-novarlocks"), (c2, "baseline-extra"),   # 3C, 4C2, 4C2
                  (c2, "gurobi"), (c3, "all-diag-mech"), (c2, "frozen-wide"),              # 4C2, 3C, 4C2
                  (v3d, "all-diag-mech"), (v3d, "all-diag-mech-wide"))                     # 3P, 3P
    tr, tf = Table(), Table()
    root_rows, full_rows = [], []
    columns = [[] for _ in full_modes]
    for n in path_order(cases):
        case = cases[n]
        opt = case["known_optimum"]
        base = get(c3, n, "root", "baseline")
        b = root_bound(base)
        if root_bound(get(v3d, n, "root", "baseline")) != b:
            raise SystemExit(f"{n}: the v3d baseline root bound differs from campaign 3")
        ident = [str(case["mechanism"]["n"]), str(case["mechanism"]["seed"])]
        root_rows.append(row([*ident, num(opt), tr.root(base),
                              *(tr.closed(get(runs, n, "root", m), b, opt) for runs, m in root_modes)]))
        fulls = [get(runs, n, "full", m) for runs, m in full_modes]
        for column, r in zip(columns, fulls):
            column.append(r)
        full_rows.append(row([*ident, *(tf.full(r) for r in fulls)]))

    root_caption = tr.caption(
        "The path family, seeds 0--4 (the instances of Part~3C), root runs (node limit~1, 120\\,s): "
        "number of copies $n$, seed, optimum $z^\\ast$ and SCIP's root bound $z_{\\text{base}}$ "
        "(Part~3C). Root gap closed $(z-z_{\\text{base}})/(z^\\ast-z_{\\text{base}})$, with $z$ the root "
        "bound of SCIP-nolocks and SCIP-extra and of the separator with remainder or whole-row first "
        "directions and base or wide limits (Section~\\ref{sec:blocks}, Table~\\ref{tab:modes}): "
        "remainder with base limits is \\code{all-diag-mech}, remainder with wide limits "
        "\\code{frozen-wide}, and the whole-row columns are the post hoc runs of Part~3P. The row "
        "\\emph{Part} gives the part of each column. Full runs are in Table~\\ref{tab:path-detail-full}.",
        "tab:path-detail")
    root_header = ["& & & SCIP & \\multicolumn{6}{c}{Root gap closed}\\\\",
                   "\\cmidrule(l){5-10}",
                   "& & & root & & & \\multicolumn{2}{c}{Remainder} & \\multicolumn{2}{c}{Whole row}\\\\",
                   "\\cmidrule(lr){7-8}\\cmidrule(l){9-10}",
                   row(["$n$", "Seed", "Optimum", "bound", "SCIP-nolocks", "SCIP-extra", "base", "wide",
                        "base", "wide"]),
                   row(["\\multicolumn{3}{@{}l}{\\emph{Part}}", "3C", "4C2", "4C2", "3C", "4C2", "3P", "3P"])]
    full_caption = tf.caption(
        "The path family, seeds 0--4, full runs (300\\,s): status and time in seconds of SCIP, "
        "SCIP-nolocks, SCIP-extra and Gurobi, and of the separator with remainder or whole-row first "
        "directions and base or wide limits (modes as in Table~\\ref{tab:path-detail}). The row "
        "\\emph{Part} gives the part of each column. " + SOLVED_CAPTION +
        " The solved counts are those of Table~\\ref{tab:mechanism}.", "tab:path-detail-full")
    full_header = ["& & \\multicolumn{8}{c}{Full run: status and time (s)}\\\\",
                   "\\cmidrule(l){3-10}",
                   "& & & & & & \\multicolumn{2}{c}{Remainder} & \\multicolumn{2}{c}{Whole row}\\\\",
                   "\\cmidrule(lr){7-8}\\cmidrule(l){9-10}",
                   row(["$n$", "Seed", "SCIP", "SCIP-nolocks", "SCIP-extra", "Gurobi", "base", "wide",
                        "base", "wide"]),
                   row(["\\multicolumn{2}{@{}l}{\\emph{Part}}", "3C", "4C2", "4C2", "4C2", "3C", "4C2",
                        "3P", "3P"])]
    full_rows += ["\\cmidrule{1-10}", solved_row("\\multicolumn{2}{@{}l}{Solved}", columns)]
    return [table(root_caption, "@{}rrrrrrrrrr@{}", root_header, root_rows, "3pt"),
            table(full_caption, "@{}rrrrrrrrrr@{}", full_header, full_rows, "3pt")]


def path_fresh():
    """Seeds 5-9, Parts 4C3 and 4C4: root closures (tab:path-fresh) and full runs (tab:path-fresh-full)."""
    c5a, c5b = load_runs("v5/runs/partC5a"), load_runs("v5/runs/partC5b")
    tr, tf = Table(), Table()
    root_rows, full_rows = [], []
    parts = (("4C3", "v4/runs/partC3", "coupling row $\\sum_iy_i\\le0.8n$, not binding"),
             ("4C4", "v4/runs/partC4", "coupling row $\\sum_iy_i\\le c$, binding"))
    for part, directory, coupling in parts:
        binding = part == "4C4"
        runs, cases = load_runs(directory), load_cases(directory)
        same_cases(cases, "v5/runs/partC5a")
        if binding:
            same_cases(cases, "v5/runs/partC5b")
        title = f"Part {part}: {coupling} (SCIP-nolocks: Part 5C-a"
        root_title = title + ("; cap $64n$: Part 5C-b)" if binding else ")")
        root_rows += ["\\midrule"] * bool(root_rows)
        root_rows.append(row([f"\\multicolumn{{14}}{{@{{}}l}}{{\\emph{{{root_title}}}}}"]))
        full_rows += ["\\midrule"] * bool(full_rows)
        full_rows.append(row([f"\\multicolumn{{9}}{{@{{}}l}}{{\\emph{{{title})}}}}"]))
        # Full-run columns: SCIP, SCIP-nolocks, SCIP-extra, Gurobi, remainder base, remainder wide, whole row wide.
        columns = [[], [], [], [], [] if not binding else None, [] if binding else None, []]
        for n in path_order(cases):
            case = cases[n]
            opt = case["known_optimum"]
            base = get(runs, n, "root", "baseline")
            b = root_bound(base)
            ident = [str(case["mechanism"]["n"]), str(case["mechanism"]["seed"])]

            def closed(r):
                return tr.closed(r, b, opt)

            nolocks, extra, rowdir = (get(c5a, n, "root", "baseline-novarlocks"),
                                      get(runs, n, "root", "baseline-extra"), get(runs, n, "root", "rowdir-wide"))
            if binding:
                closure = case.get("reference_bound_ii")
                if not finite(closure):
                    raise SystemExit(f"{n}: no block closure (reference_bound_ii)")
                frozen = get(runs, n, "root", "frozen-wide")
                cap = [get(c5b, n, "root", m) for m in ("frozen-cap64", "rowdir-cap64")]
                cells = [num_e4(opt - closure), tr.root(base), closed(nolocks), closed(extra), "", closed(frozen),
                         closed(cap[0]), closed(rowdir), closed(cap[1]),
                         *(tr.flag(r, num_e4(closure - root_bound(r))) for r in cap)]
            else:
                rembase = get(runs, n, "root", "all-diag-mech")
                cells = ["", tr.root(base), closed(nolocks), closed(extra), closed(rembase), "", "", closed(rowdir),
                         "", "", ""]
            root_rows.append(row([*ident, num(opt), *cells]))

            fulls = [get(runs, n, "full", "baseline"), get(c5a, n, "full", "baseline-novarlocks"),
                     get(runs, n, "full", "baseline-extra"), get(runs, n, "full", "gurobi"),
                     None if binding else get(runs, n, "full", "all-diag-mech"),
                     get(runs, n, "full", "frozen-wide") if binding else None,
                     get(runs, n, "full", "rowdir-wide")]
            for column, r in zip(columns, fulls):
                if r is not None:
                    column.append(r)
            full_rows.append(row([*ident, *("" if r is None else tf.full(r) for r in fulls)]))
        full_rows += ["\\cmidrule{1-9}",
                      solved_row("\\multicolumn{2}{@{}l}{Solved}", columns)]

    root_caption = tr.caption(
        "The path family, seeds 5--9, root runs: Part~4C3 with the coupling row of Part~3C, which does "
        "not bind, and Part~4C4 with a binding coupling row. Number of copies $n$, seed, optimum "
        "$z^\\ast$; opt.$-$closure: optimum minus the block closure (Section~\\ref{sec:mechanism}), in "
        "units of $10^{-4}$; SCIP's root bound $z_{\\text{base}}$. Root gap closed "
        "$(z-z_{\\text{base}})/(z^\\ast-z_{\\text{base}})$, with $z$ the root bound of SCIP-nolocks "
        "(nolocks), SCIP-extra (extra) and the separator: remainder directions with base limits "
        "(\\code{all-diag-mech}), wide limits (\\code{frozen-wide}) or the cut cap $64n$ "
        "(\\code{frozen-cap64}); whole-row directions with wide limits (\\code{rowdir-wide}) or the cut "
        "cap $64n$ (\\code{rowdir-cap64}). Closure$-$root: block closure minus the root bound of the "
        "two modes with cut cap $64n$, in units of $10^{-4}$. Root runs: node limit~1, 120\\,s; "
        "Part~5C-b: up to 40 callbacks, 300\\,s (Table~\\ref{tab:modes}). Columns without a stated part "
        "are from the part of the block. Empty cells: not run in that part. Full runs are in "
        "Table~\\ref{tab:path-fresh-full}.", "tab:path-fresh")
    root_header = ["& & & & SCIP & \\multicolumn{7}{c}{Root gap closed} & \\multicolumn{2}{c}{Closure$-$root}\\\\",
                   "\\cmidrule(lr){6-12}\\cmidrule(l){13-14}",
                   "& & & opt.$-$ & root & \\multicolumn{2}{c}{SCIP} & \\multicolumn{3}{c}{Remainder} & "
                   "\\multicolumn{2}{c}{Whole row} & \\multicolumn{2}{c}{cap $64n$}\\\\",
                   "\\cmidrule(lr){6-7}\\cmidrule(lr){8-10}\\cmidrule(lr){11-12}\\cmidrule(l){13-14}",
                   row(["$n$", "Seed", "Optimum", "closure", "bound", "nolocks", "extra", "base", "wide",
                        "$64n$", "wide", "$64n$", "rem.", "row"])]
    full_caption = tf.caption(
        "The path family, seeds 5--9, full runs (300\\,s): status and time in seconds of SCIP, "
        "SCIP-nolocks, SCIP-extra and Gurobi, and of the separator with remainder directions and base "
        "limits (\\code{all-diag-mech}, Part~4C3) or wide limits (\\code{frozen-wide}, Part~4C4) and with "
        "whole-row directions and wide limits (\\code{rowdir-wide}). Columns without a stated part are "
        "from the part of the block. Empty cells: not run in that part. " + SOLVED_CAPTION +
        " The solved counts are those of Table~\\ref{tab:mechanism}.", "tab:path-fresh-full")
    full_header = ["& & \\multicolumn{7}{c}{Full run: status and time (s)}\\\\",
                   "\\cmidrule(l){3-9}",
                   "& & & & & & \\multicolumn{2}{c}{Remainder} & Whole row\\\\",
                   "\\cmidrule(lr){7-8}\\cmidrule(l){9-9}",
                   row(["$n$", "Seed", "SCIP", "SCIP-nolocks", "SCIP-extra", "Gurobi", "base", "wide", "wide"])]
    return [table(root_caption, "@{}rrrrrrrrrrrrrr@{}", root_header, root_rows, "3pt"),
            table(full_caption, "@{}rrrrrrrrr@{}", full_header, full_rows, "3pt")]


# ---------------------------------------------------------------- star family

# Separator modes: whole row with blocks of <=4 variables; block direction, <=4; block direction, stars.
STAR_MODES = ("rowdir-star4", "agg-star4", "agg-star")


def star_table():
    """Part 5S: root bound / optimum (tab:star-detail) and full runs (tab:star-detail-full)."""
    runs, cases = load_runs("v5/runs/partS5"), load_cases("v5/runs/partS5")
    if any(check_failed(r) for r in runs.values()):
        raise SystemExit("partS5: a run failed the primal check; its dagger would clash with process_timeout")
    order = sorted(cases, key=lambda n: tuple(cases[n]["star"][f] for f in ("k", "n", "seed")))
    root_modes = ("baseline", "baseline-novarlocks", "baseline-extra", *STAR_MODES)
    full_modes = ("baseline", "baseline-novarlocks", "baseline-extra", "gurobi", *STAR_MODES)
    tf = Table()

    def full(r):
        if r["status"] == "process_timeout":
            return "--\\textsuperscript{\\dag}"
        return tf.full(r)

    root_rows, full_rows = [], []
    totals = [[] for _ in full_modes]
    for k in sorted({cases[n]["star"]["k"] for n in order}):
        names = [n for n in order if cases[n]["star"]["k"] == k]
        columns = [[get(runs, n, "full", m) for n in names] for m in full_modes]
        root_rows += ["\\midrule"] * bool(root_rows)
        full_rows += ["\\midrule"] * bool(full_rows)
        for i, n in enumerate(names):
            star = cases[n]["star"]
            opt = cases[n]["known_optimum"]
            ident = [str(star["k"]), str(star["n"]), str(star["seed"])]
            fractions = []
            for m in root_modes:
                bound = root_bound(get(runs, n, "root", m))
                fractions.append(num(bound / opt) if finite(bound) else "--")
            root_rows.append(row([*ident, num(opt), *fractions]))
            full_rows.append(row([*ident, *(full(column[i]) for column in columns)]))
        full_rows += ["\\cmidrule{1-10}", solved_row(f"\\multicolumn{{3}}{{@{{}}l}}{{Solved, $k={k}$}}", columns)]
        for total, column in zip(totals, columns):
            total += column
    full_rows += ["\\midrule", solved_row("\\multicolumn{3}{@{}l}{Solved, total}", totals)]

    modes_text = ("SCIP, SCIP-nolocks, SCIP-extra and the separator with blocks of at most four variables "
                  "and whole-row first directions (\\code{rowdir-star4}), with blocks of at most four variables "
                  "and the block direction first (\\code{agg-star4}) and with star blocks and the block "
                  "direction first (\\code{agg-star}); limits in Table~\\ref{tab:modes}")
    root_caption = Table().caption(
        "The star family (Part~5S), root runs (node limit~1, 120\\,s): number $k$ of leaves per star, "
        "number $n$ of stars, seed, optimum $z^\\ast$ and the root bound $z$ as a fraction $z/z^\\ast$ of "
        f"the optimum for {modes_text}. The medians per $k$ are those of Table~\\ref{{tab:stars}}. Full "
        "runs are in Table~\\ref{tab:star-detail-full}.", "tab:star-detail")
    n_timeouts = sum(r["status"] == "process_timeout" for r in runs.values())
    full_caption = tf.caption(
        "The star family (Part~5S), full runs (300\\,s): status and time in seconds of SCIP, "
        "SCIP-nolocks, SCIP-extra, Gurobi and the three separator modes of Table~\\ref{tab:star-detail}. "
        f"\\textsuperscript{{\\dag}}One of the {n_timeouts} runs whose worker process was stopped at the "
        "hard limit of 360\\,s during a load spike on the host (status \\code{process\\_timeout}, "
        "Section~\\ref{sec:star-bench}); such a run recorded no status, time or bound and counts as "
        "unsolved. " + SOLVED_CAPTION + " The solved counts are those of Table~\\ref{tab:stars}.",
        "tab:star-detail-full")
    direction_header = ["& & & & & & & Whole row & \\multicolumn{2}{c}{Block direction}\\\\",
                        "\\cmidrule(lr){8-8}\\cmidrule(l){9-10}"]
    root_header = ["& & & & \\multicolumn{6}{c}{Root bound / optimum}\\\\", "\\cmidrule(l){5-10}",
                   *direction_header,
                   row(["$k$", "$n$", "Seed", "Optimum", "SCIP", "SCIP-nolocks", "SCIP-extra",
                        "$\\le4$ var.", "$\\le4$ var.", "stars"])]
    full_header = ["& & & \\multicolumn{7}{c}{Full run: status and time (s)}\\\\", "\\cmidrule(l){4-10}",
                   *direction_header,
                   row(["$k$", "$n$", "Seed", "SCIP", "SCIP-nolocks", "SCIP-extra", "Gurobi",
                        "$\\le4$ var.", "$\\le4$ var.", "stars"])]
    return [table(root_caption, "@{}rrrrrrrrrr@{}", root_header, root_rows, "3pt"),
            table(full_caption, "@{}rrrrrrrrrr@{}", full_header, full_rows, "3pt")]


INTRO = r"""\paragraph{Per-model and per-instance results.}
Tables~\ref{tab:partA}--\ref{tab:star-detail-full} list the runs behind
Sections~\ref{sec:minlplib}, \ref{sec:mechanism} and~\ref{sec:star-bench}. A
root bound is SCIP's dual bound at the end of the root node; for a run that
ended at the root without reporting one, because the root node was pruned, it
is the final dual bound. Times are the seconds charged to the budget
(Section~\ref{sec:setup}). Numbers have four significant digits; values of at
least 1000 are rounded to integers.
"""


def main():
    parts = [INTRO, part_a(), part_b(), part_d(), *path_detail(), *path_fresh(), *star_table()]
    OUT.write_text("\n".join(parts))
    print(f"wrote {OUT.relative_to(ROOT)}: tab:partA, tab:partB, tab:partD, tab:path-detail, "
          "tab:path-detail-full, tab:path-fresh, tab:path-fresh-full, tab:star-detail, tab:star-detail-full")


if __name__ == "__main__":
    main()
