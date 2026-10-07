#!/usr/bin/env python3
"""Parse all runs of the solver campaign into results.csv and results.json.

One row per run directory <runs>/<instance>__<solver>/ (or an archived
attempt <instance>__<solver>__a<k>/). Sources per run:
  run.json   written by driver.py (settings, attempt, validity, wall/CPU time,
             kills, memory)
  trace.trc  GAMS trace record (traceopt=3): statuses, objective, objest, nodes
  gams.log   GAMS + solver log: versions, final bounds, thread evidence
  <inst>.lst GAMS listing: status texts
  m_p.gdx    GAMS savepoint of the returned point (presence only)

Dual bound. GAMS reports the solver's bound as the model attribute objest
(trace field ObjectiveValueEstimate). GAMS/Gurobi leaves it NA for continuous
(NLP) models, so the final bound is also read from each solver's end-of-run
summary in the log: BARON "Best possible = ...", Gurobi "Best objective ...,
best bound ...", SCIP "Dual Bound : ...". These are final solver-reported
values. Globality disclaimers and argument-domain tightening are preserved
separately; the values are not rigorous certificates. dual_bound is objest if available, otherwise
the log summary value; if both exist they must agree (relative 1e-10), else
the row is flagged. A run without a final summary (killed) gets no dual_bound;
its last progress-table value is kept separately in dual_bound_last_logged.
Values with magnitude >= 1e20 are written as "inf"/"-inf".

Precision. dual_bound_text is the decimal string exactly as the source
printed it: the trace prints 15 significant digits, the GUROBI log summary 13
(format %.12e), the BARON and SCIP log summaries 15, BARON's progress table 6.
dual_bound_print_halfunit is half a unit in the last printed digit of
dual_bound_text; the solver's internal value lies within it, assuming
round-to-nearest printing. It is conservative: when the printer drops
trailing zeros (trace, BARON), the true printing error is at most half a unit
in the 15th significant digit. GAMS/Gurobi leaves objest NA for general
nonlinear NLPs, so their GUROBI dual bound comes from the log summary with
only 13 significant digits; such rows get a note. primal_objective is the objective of the point
GAMS returned (trace); the point itself is in m_p.gdx. GAMS can return a point
other than the solver's own final incumbent (seen for SCIP), so
solver_log_primal is reported separately and any difference beyond the
printing precision is noted.

Validity (decided by driver.py, copied from run.json): attempt is the
attempt number of this run, attempts_total the number of attempts made,
valid is true if the attempt ended by its own completion or the hard timeout
and got cpu/wall >= 0.9 (attempts that completed within 60 s, not at the
solver's time limit, are exempt from the cpu/wall test), validity explains the decision, and end_kind says how
the attempt ended. A row with valid false is the best of the allowed
attempts (kept_best) or an archived attempt. Runs from driver version 1 have
no validity fields (empty).

usage: python3 collect.py [--runs DIR] [--out PREFIX]
  defaults: --runs runs  --out results   (relative to this folder)
"""
import argparse
import csv
import json
import math
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path

HERE = Path(__file__).resolve().parent

MODEL_STATUS = {
    1: "Optimal", 2: "Locally Optimal", 3: "Unbounded", 4: "Infeasible", 5: "Locally Infeasible",
    6: "Intermediate Infeasible", 7: "Feasible Solution", 8: "Integer Solution",
    9: "Intermediate Non-Integer", 10: "Integer Infeasible", 11: "Licensing Problem",
    12: "Error Unknown", 13: "Error No Solution", 14: "No Solution Returned", 15: "Solved Unique",
    16: "Solved", 17: "Solved Singular", 18: "Unbounded - No Solution", 19: "Infeasible - No Solution",
}
SOLVER_STATUS = {
    1: "Normal Completion", 2: "Iteration Interrupt", 3: "Resource Interrupt", 4: "Terminated by Solver",
    5: "Evaluation Interrupt", 6: "Capability Problems", 7: "Licensing Problems", 8: "User Interrupt",
    9: "Setup Failure", 10: "Solver Failure", 11: "Internal Solver Failure", 12: "Solve Processing Skipped",
    13: "System Failure",
}
FEASIBLE_MODEL_STATUS = {1, 2, 7, 8, 15, 16, 17}
# solver statuses after which the reported bound is taken as the solver's final bound:
# normal completion, iteration/resource interrupt, terminated by solver, user interrupt
BOUND_SOLVER_STATUS = {1, 2, 3, 4, 8}
INF = 1e20

COLUMNS = [
    "instance", "solver", "solver_version", "gams_version", "model_type", "sense",
    "run_finished", "attempt", "attempts_total", "valid", "validity", "end_kind", "kill_reason", "return_code",
    "model_status", "model_status_text", "solver_status", "solver_status_text", "termination_message",
    "primal_objective", "objective_reported", "solver_log_primal", "dual_bound", "dual_bound_text",
    "dual_bound_print_halfunit", "dual_bound_source", "objest_trace", "dual_bound_log_final",
    "dual_bound_last_logged", "rel_gap", "globality_warning", "scip_argument_bounds_tightened",
    "reported_max_constraint_violation", "loaded_first_batch",
    "wall_time_s", "gams_elapsed_s", "solver_time_s", "cpu_time_s", "cpu_time_wait4_s", "cpu_time_proc_s",
    "cpu_over_wall", "load1_mean", "nodes", "nodes_log",
    "threads_confirmed", "threads_evidence", "peak_group_rss_mb", "peak_group_swap_mb",
    "machine_swap_used_max_gb", "machine_mem_available_min_gb", "savepoint_gdx",
    "generated_counts_match_osil", "reslim", "optcr", "optca", "start_utc", "end_utc", "run_dir", "notes",
]


def num(s):
    """Parse a number from a trace/log token; NA, '-' and empty give None."""
    if s is None:
        return None
    s = s.strip().rstrip("%")
    if s in ("", "NA", "-", "--", "na"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def half_unit(tok):
    """Half a unit in the last printed digit of a decimal token, as a Decimal."""
    e = Decimal(tok.strip()).as_tuple().exponent
    return Decimal(5) * Decimal(10) ** (e - 1)


def differ_beyond_print(a, b):
    """True if decimal tokens a and b differ by more than their printing precision."""
    try:
        return abs(Decimal(a.strip()) - Decimal(b.strip())) > half_unit(a) + half_unit(b)
    except (InvalidOperation, AttributeError):
        return False


def show(v):
    """Value for output: None stays None, |v| >= 1e20 becomes 'inf'/'-inf'."""
    if v is None:
        return None
    if isinstance(v, float) and (math.isinf(v) or abs(v) >= INF):
        return "inf" if v > 0 else "-inf"
    return v


def parse_trace(path):
    """Return the last GamsSolve record of a GAMS trace file as a dict, or {}."""
    path = Path(path)
    if not path.exists():
        return {}
    head, data = [], []
    for ln in path.read_text(errors="replace").splitlines():
        if ln.startswith("*"):
            body = ln[1:].strip()
            if body and body not in ("Trace Record Definition", "GamsSolve"):
                head.append(body)
        elif ln.strip():
            data.append(ln.strip())
    if not head or not data:
        return {}
    fields = "".join(head).split(",")
    vals = data[-1].split(",")
    return dict(zip(fields, vals))


def last(pattern, text, flags=re.M):
    m = None
    for m in re.finditer(pattern, text, flags):
        pass
    return m


def parse_log(text, solver, sense="min"):
    """Versions, final summary values (number and printed token), nodes, last
    progress-table dual bound, thread evidence and error lines of one log."""
    r = {"version": None, "final_dual": None, "final_primal": None, "final_dual_tok": None,
         "final_primal_tok": None, "nodes": None, "termination": None, "last_logged_dual": None,
         "threads_evidence": [], "errors": []}
    m = re.search(r"^--- Job \S+ Start \S+ \S+ (\S+ \S+)", text, re.M)
    r["gams_version"] = m.group(1) if m else None
    m = last(r"^\s+Threads (\d+)\s*$", text)
    if m:
        r["threads_evidence"].append(f"GAMS Threads {m.group(1)}")
        r["gams_threads"] = int(m.group(1))
    if solver == "BARON":
        m = re.search(r"BARON version (\S+?)\.? Built", text)
        r["version"] = m.group(1) if m else None
        m = last(r"^Best possible\s*=\s*(\S+)", text)
        r["final_dual_tok"] = m.group(1) if m else None
        m = last(r"^Solution\s*=\s*(\S+)", text)
        r["final_primal_tok"] = m.group(1) if m else None
        m = last(r"Total no\. of BaR iterations:\s*(\d+)", text)
        r["nodes"] = int(m.group(1)) if m else None
        msgs = [m.group(1).strip() for m in re.finditer(r"^\s*\*\*\* (.+?) \*\*\*\s*$", text, re.M)]
        r["termination"] = " | ".join(msgs) if msgs else None
        # progress row: [*] iteration[+] time mem lower upper progress(% or NA). BARON's lower
        # bound column is the dual bound for minimization, its upper bound column for maximization
        m = last(r"^\s*\*?\s*\d+\+?\s+[\d.]+\s+\d+[KMG]?B\s+(\S+)\s+(\S+)\s+(?:\S+%|NA)\s*$", text)
        r["last_logged_dual"] = num(m.group(1 if sense == "min" else 2)) if m else None
        # BARON's MIP subsolver threads default to GAMS threads (GAMS/BARON docs)
    elif solver == "GUROBI":
        m = re.search(r"Gurobi Optimizer version (\S+) build (\S+)", text)
        r["version"] = f"{m.group(1)} (build {m.group(2)})" if m else None
        m = last(r"Best objective (\S+), best bound (\S+), gap (\S+)", text)
        if m:
            r["final_primal_tok"], r["final_dual_tok"] = m.group(1), m.group(2)
        m = last(r"Explored (\d+) nodes", text)
        r["nodes"] = int(m.group(1)) if m else None
        m = last(r"^\.\.\. Status: (.+)$", text)
        r["termination"] = m.group(1).strip() if m else None
        m = last(r"(\S+)\s+(\S+)\s+(?:\S+%|-)\s+\S+\s+\d+s\s*$", text)
        r["last_logged_dual"] = num(m.group(2)) if m else None
        for pat in (r"using up to (\d+) threads", r"Thread count was (\d+) "):
            m = last(pat, text)
            if m:
                r["threads_evidence"].append(m.group(0).strip())
                r.setdefault("solver_threads", []).append(int(m.group(1)))
    elif solver == "SCIP":
        m = re.search(r"^SCIP version (\S+)(?: \((\w+)\))?", text, re.M)
        r["version"] = (m.group(1) + (f" ({m.group(2)})" if m.group(2) else "")) if m else None
        m = last(r"^Dual Bound\s*:\s*(\S+)", text)
        r["final_dual_tok"] = m.group(1) if m else None
        m = last(r"^Primal Bound\s*:\s*(\S+)", text)
        r["final_primal_tok"] = m.group(1) if m else None
        m = last(r"^Solving Nodes\s*:\s*(\d+)", text)
        r["nodes"] = int(m.group(1)) if m else None
        m = last(r"^SCIP Status\s*:\s*(.+)$", text)
        r["termination"] = m.group(1).strip() if m else None
        # progress table: locate the 'dualbound' column from the header
        hdr = last(r"^ time \|.*$", text)
        if hdr:
            cols = [c.strip() for c in hdr.group(0).split("|")]
            if "dualbound" in cols:
                k = cols.index("dualbound")
                rows = [ln for ln in text.splitlines()
                        if re.match(r"^\S?\s*[\d.]+s\|", ln) and ln.count("|") == len(cols) - 1]
                if rows:
                    r["last_logged_dual"] = num(rows[-1].split("|")[k])
        m = last(r"^lp/threads = (\d+)", text)
        if m:
            r["threads_evidence"].append(m.group(0).strip())
            r.setdefault("solver_threads", []).append(int(m.group(1)))
    r["final_dual"], r["final_primal"] = num(r["final_dual_tok"]), num(r["final_primal_tok"])
    for ln in text.splitlines():
        s = ln.strip()
        if re.search(r"(?i)\berror|cannot|insufficient|not supported|unsupported|capabilit|failure|"
                     r"^\*\*\* no solution|licen[cs]e.*(problem|expired)", s) and s not in r["errors"]:
            r["errors"].append(s)
    m = last(r"^--- Job \S+ Stop .* elapsed (\d+):(\d+):([\d.]+)", text)
    r["gams_elapsed_s"] = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else None
    return r


def parse_lst(text):
    out = {}
    m = last(r"^\*\*\*\* SOLVER STATUS\s+(\d+)\s+(.+?)\s*$", text)
    if m:
        out["solver_status"], out["solver_status_text"] = int(m.group(1)), m.group(2)
    m = last(r"^\*\*\*\* MODEL STATUS\s+(\d+)\s+(.+?)\s*$", text)
    if m:
        out["model_status"], out["model_status_text"] = int(m.group(1)), m.group(2)
    m = re.search(r"^\*\*\*\* (\d+) ERROR\(S\)", text, re.M)
    if m:
        out["gams_errors"] = int(m.group(1))
    return out


def collect_run(d, manifest):
    meta = json.loads((d / "run.json").read_text()) if (d / "run.json").exists() else {}
    inst, solver = d.name.split("__")[:2]
    log = (d / "gams.log").read_text(errors="replace") if (d / "gams.log").exists() else ""
    lstp = d / f"{inst}.lst"
    lst = parse_lst(lstp.read_text(errors="replace")) if lstp.exists() else {}
    tr = parse_trace(d / "trace.trc")
    notes = []
    sense = meta.get("sense") or (manifest.get(inst, {}).get("sense"))
    lg = parse_log(log, solver, sense)
    globality_warning = solver == 'BARON' and 'Globality is therefore not guaranteed' in log
    tightened = solver == 'SCIP' and 'minzerodistance' in log
    violation = re.search(r'max constraint violation \(([^)]+)\) exceeds tolerance', log)
    loaded_first_batch = (meta.get('driver_pid') == 898862
                          and meta.get('start_utc') == '2026-10-03T00:56:09Z')
    if globality_warning:
        notes.append('BARON: globality not guaranteed (inappropriate variable bounds)')
    if tightened:
        notes.append('SCIP: log/pow argument lower bounds tightened to 1e-9; dual is for a slightly tightened model')
    if violation:
        notes.append(f'GUROBI: reported max constraint violation {violation[1]} exceeds its tolerance')
    if loaded_first_batch:
        notes.append('first admitted batch: machine overload and memory pressure; passed measurement validity rule')

    ms = int(num(tr["ModelStatus"])) if tr.get("ModelStatus") not in (None, "NA") else lst.get("model_status")
    ss = int(num(tr["SolverStatus"])) if tr.get("SolverStatus") not in (None, "NA") else lst.get("solver_status")
    if lst.get("model_status") not in (None, ms) or lst.get("solver_status") not in (None, ss):
        notes.append(f"trace status {ms}/{ss} differs from .lst {lst.get('model_status')}/{lst.get('solver_status')}")

    obj_raw = num(tr.get("ObjectiveValue"))
    primal = obj_raw if (ms in FEASIBLE_MODEL_STATUS and obj_raw is not None and abs(obj_raw) < INF) else None
    objest = num(tr.get("ObjectiveValueEstimate"))
    logd = lg["final_dual"]
    dual, src, dual_tok = None, None, None
    if ss not in BOUND_SOLVER_STATUS:
        if objest is not None or logd is not None:
            notes.append(f"solver status {ss} ({SOLVER_STATUS.get(ss)}): reported bound objest={objest!r}, "
                         f"log={logd!r} not used as a final bound")
    elif objest is not None:
        dual, src, dual_tok = objest, "objest (trace)", tr["ObjectiveValueEstimate"].strip()
        if logd is not None:
            both_inf = abs(objest) >= INF and abs(logd) >= INF and (objest > 0) == (logd > 0)
            if not both_inf and abs(objest - logd) > 1e-10 * max(1.0, abs(objest), abs(logd)):
                notes.append(f"objest {objest!r} differs from log final bound {logd!r}")
            else:
                src = "objest (trace), equals log final bound"
    elif logd is not None:
        dual, src, dual_tok = logd, "solver log final summary (objest NA)", lg["final_dual_tok"]
        if solver == "GUROBI" and abs(logd) < INF:
            notes.append(f"dual bound from GUROBI's log summary, printed with 13 significant digits: "
                         f"known only to +-{half_unit(dual_tok)}")
    else:
        notes.append("no final dual bound reported")
    if dual is not None and primal is not None and abs(dual) < INF:
        bad = dual > primal + 1e-6 * max(1.0, abs(primal)) if sense == "min" else \
            dual < primal - 1e-6 * max(1.0, abs(primal))
        if bad:
            notes.append("dual bound on the wrong side of the primal objective (beyond 1e-6 rel.)")
    rel_gap = None
    if dual is not None and primal is not None and abs(dual) < INF:
        rel_gap = abs(primal - dual) / max(abs(primal), abs(dual), 1e-10)
    if lg["final_primal"] is not None and primal is not None and abs(lg["final_primal"]) < INF and \
            differ_beyond_print(lg["final_primal_tok"], tr["ObjectiveValue"]):
        notes.append(f"returned point's objective {tr['ObjectiveValue'].strip()} differs from the solver's "
                     f"final incumbent {lg['final_primal_tok']} beyond printing precision "
                     f"(diff {primal - lg['final_primal']:.3g}); use the savepoint")

    nodes = num(tr.get("NumberOfNodes"))
    nodes = int(nodes) if nodes is not None else lg["nodes"]
    if lg["nodes"] is not None and nodes is not None and lg["nodes"] != nodes:
        notes.append(f"trace nodes {nodes} vs log nodes {lg['nodes']}")

    ratio = meta.get("cpu_over_wall")
    solver_thr = lg.get("solver_threads")
    ev = list(lg["threads_evidence"])
    if ratio is not None:
        ev.append(f"cpu/wall {ratio:.3f}")
    if not meta.get("finished") or not tr:
        thr = None
    elif lg.get("gams_threads") != 1 or (solver_thr and any(t != 1 for t in solver_thr)):
        thr = "no"
    elif ratio is not None and ratio > 1.10:
        thr = "no"
    elif solver == "BARON" or not solver_thr:
        thr = "yes (GAMS threads=1 and cpu/wall <= 1.10; solver log has no thread line)"
    else:
        thr = "yes"

    counts_ok = None
    mf = manifest.get(inst)
    if mf and tr.get("NumberOfEquations"):
        gen = {"rows": tr.get("NumberOfEquations"), "vars": tr.get("NumberOfVariables"),
               "discrete": tr.get("NumberOfDiscreteVariables"), "nz": tr.get("NumberOfNonZeros"),
               "nl": tr.get("NumberOfNonlinearNonZeros")}
        imp = {"rows": mf["osil_implied_rows"], "vars": mf["osil_implied_vars"],
               "discrete": mf["osil_implied_binary"] + mf["osil_implied_integer"],
               "nz": mf["osil_implied_nz"], "nl": mf["osil_implied_nl"]}
        diff = [f"{k} {gen[k]} vs {imp[k]}" for k in gen if num(gen[k]) != imp[k]]
        counts_ok = not diff
        if diff:
            notes.append("generated model counts differ from OSIL-implied: " + ", ".join(diff))
    if tr and tr.get("ModelType") and meta.get("model_type") and tr["ModelType"] != meta["model_type"]:
        notes.append(f"trace model type {tr['ModelType']} != declared {meta['model_type']}")
    if tr and tr.get("SolverName") and tr["SolverName"] != solver:
        notes.append(f"trace solver {tr['SolverName']} != {solver}")
    if meta.get("kill_reason"):
        notes.append(f"driver interrupted the run: {meta['kill_reason']}")
    if not tr and meta.get("finished"):
        notes.append("no trace record (solve did not return to GAMS): no result")
    if meta.get("finished") and "cpu_s_proc" not in meta:
        notes.append("run.json from driver version 1: CPU time from wait4 only, no swap record")
    if meta.get("kept_best"):
        notes.append(f"not a valid measurement: {meta.get('validity')}")
    elif meta.get("valid") is False:
        notes.append(f"archived invalid attempt: {meta.get('validity')}")
    keep = dual is not None and abs(dual) < INF
    if lst.get("gams_errors"):
        notes.append(f"GAMS reported {lst['gams_errors']} error(s)")
    notes += [f"log: {e}" for e in lg["errors"][:5]]

    return {
        "instance": inst, "solver": solver, "solver_version": lg["version"],
        "gams_version": lg.get("gams_version"), "model_type": meta.get("model_type") or tr.get("ModelType"),
        "sense": sense, "run_finished": bool(meta.get("finished")), "attempt": meta.get("attempt"),
        "attempts_total": meta.get("attempts_total"), "valid": meta.get("valid"),
        "validity": meta.get("validity"), "end_kind": meta.get("end_kind"), "kill_reason": meta.get("kill_reason"),
        "return_code": meta.get("return_code"),
        "model_status": ms, "model_status_text": lst.get("model_status_text") or MODEL_STATUS.get(ms),
        "solver_status": ss, "solver_status_text": lst.get("solver_status_text") or SOLVER_STATUS.get(ss),
        "termination_message": lg["termination"],
        "primal_objective": show(primal), "objective_reported": show(obj_raw),
        "solver_log_primal": show(lg["final_primal"]),
        "dual_bound": show(dual), "dual_bound_text": dual_tok if keep else None,
        "dual_bound_print_halfunit": str(half_unit(dual_tok)) if keep else None,
        "dual_bound_source": src, "objest_trace": show(objest),
        "dual_bound_log_final": show(logd), "dual_bound_last_logged": show(lg["last_logged_dual"]),
        "rel_gap": rel_gap,
        "globality_warning": globality_warning, "scip_argument_bounds_tightened": tightened,
        "reported_max_constraint_violation": violation[1] if violation else None,
        "loaded_first_batch": loaded_first_batch,
        "wall_time_s": meta.get("wall_s"), "gams_elapsed_s": lg["gams_elapsed_s"],
        "solver_time_s": num(tr.get("SolverTime")),
        "cpu_time_s": meta.get("cpu_s"), "cpu_time_wait4_s": meta.get("cpu_s_wait4"),
        "cpu_time_proc_s": meta.get("cpu_s_proc"), "cpu_over_wall": ratio,
        "load1_mean": meta.get("load1_mean"), "nodes": nodes, "nodes_log": lg["nodes"],
        "threads_confirmed": thr, "threads_evidence": "; ".join(ev),
        "peak_group_rss_mb": meta.get("peak_group_rss_mb"), "peak_group_swap_mb": meta.get("peak_group_swap_mb"),
        "machine_swap_used_max_gb": meta.get("machine_swap_used_max_gb"),
        "machine_mem_available_min_gb": meta.get("machine_mem_available_min_gb"),
        "savepoint_gdx": (d / "m_p.gdx").exists(),
        "generated_counts_match_osil": counts_ok, "reslim": meta.get("reslim"),
        "optcr": meta.get("optcr"), "optca": meta.get("optca"), "start_utc": meta.get("start_utc"),
        "end_utc": meta.get("end_utc"), "run_dir": str(d.relative_to(HERE)) if d.is_relative_to(HERE) else str(d),
        "notes": "; ".join(notes),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", default="runs", help="directory holding <instance>__<solver> run dirs")
    ap.add_argument("--out", default="results", help="output prefix (writes PREFIX.csv and PREFIX.json)")
    a = ap.parse_args()
    runs = (HERE / a.runs).resolve()
    mpath = HERE / "gms_manifest.json"
    manifest = {r["instance"]: r for r in json.loads(mpath.read_text())} if mpath.exists() else {}
    rows = [collect_run(d, manifest) for d in sorted(runs.iterdir()) if d.is_dir() and "__" in d.name]
    out = (HERE / a.out).resolve()
    with open(out.with_suffix(".csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    out.with_suffix(".json").write_text(json.dumps(rows, indent=1) + "\n")
    fin = sum(r["run_finished"] for r in rows)
    print(f"{len(rows)} run dirs, {fin} finished -> {out.with_suffix('.csv')} and .json")
    for r in rows:
        print(f"{r['instance']:16s} {r['solver']:6s} a{r['attempt']}/{r['attempts_total']} valid={r['valid']} "
              f"cpu/wall={r['cpu_over_wall']} ms={r['model_status']} ss={r['solver_status']} "
              f"primal={r['primal_objective']} dual={r['dual_bound']} [{r['dual_bound_source']}] "
              f"nodes={r['nodes']} wall={r['wall_time_s']} thr={str(r['threads_confirmed'])[:3]} "
              f"{('NOTES: ' + r['notes']) if r['notes'] else ''}")


if __name__ == "__main__":
    main()
