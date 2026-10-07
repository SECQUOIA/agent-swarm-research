#!/usr/bin/env python3
"""E1: independent audit of the computational evidence of Reports A and B.

Standard library only. The script reads the raw campaign records
(records.jsonl), the frozen job lists, selections, source manifests and replay
outputs, and recomputes every campaign number quoted in

  research-20261002-convexification/document/evidence.tex   (Report A)
  research-20261003-convexification/document/evidence.tex   (Report B)

plus the summary tables in the generated results.md/coverage.md files. It does
not import any producer code (summarize.py, analyze_*.py, replay.py); the
definitions of "solved", "admitted", "flagged" and the bound comparison are
re-implemented here from the wording of the evidence sections.

Usage (from any directory):
  .venv/bin/python E1_audit_experiments.py            # claim checks only
  .venv/bin/python E1_audit_experiments.py --tables   # claim checks + paper tables

Exit status is 1 if any stated number does not match its recomputation.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXP_A = ROOT / "research-20261002-convexification/experiments"
EXP_B = ROOT / "research-20261003-convexification/experiments"
V1 = EXP_A / "campaign-v1"
V2 = EXP_B / "campaign-v2"
REP = EXP_B / "repair-discovery-v1"
METADATA = ROOT / "code/minlp_solver_lab/instances/instancedata.csv"

SCIP_STATUSES = {"optimal", "gaplimit", "timelimit", "nodelimit", "stallnodelimit",
                 "totalnodelimit", "infeasible", "unbounded", "inforunbd", "userinterrupt",
                 "memlimit", "sollimit", "bestsollimit", "restartlimit"}
MODES_A = ("baseline", "control", "all", "auto")
MODES_B = ("baseline", "all", "auto")
TOL_REL = 1e-6  # stated dual-comparison tolerance: 1e-6 times the larger bound scale


# --------------------------------------------------------------------------
# Loading and record-level definitions (independent re-implementation)
# --------------------------------------------------------------------------

def load_jsonl(path):
    with open(path) as stream:
        return [json.loads(line) for line in stream if line.strip()]


def load_json(path):
    with open(path) as stream:
        return json.load(stream)


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fnum(x):
    """Finite float or None."""
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        return None
    return float(x) if math.isfinite(x) else None


def ran_scip(r):
    """The worker returned a SCIP status (no refusal, construction error or crash)."""
    return r["status"] in SCIP_STATUSES and r.get("returncode", 0) == 0 and not r.get("worker_status")


def incumbent_checked(r):
    return (r.get("primal_check") or {}).get("checked") is True


def incumbent_passed(r):
    return incumbent_checked(r) and r["primal_check"].get("passed") is True


def reference_conflict(r):
    ref = r.get("reference_check") or {}
    return ref.get("dual_consistent") is False or ref.get("root_dual_consistent") is False


def flagged(r):
    """Failed incumbent check, unchecked returned incumbent, or reference conflict."""
    if incumbent_checked(r) and not incumbent_passed(r):
        return True
    if fnum(r.get("primal")) is not None and not incumbent_checked(r):
        return True
    return reference_conflict(r)


def solved(r):
    """Evidence wording: optimal/gaplimit, finite incumbent passing the original-model
    numerical check, no reference-bound conflict."""
    return (ran_scip(r) and r["status"] in ("optimal", "gaplimit")
            and fnum(r.get("primal")) is not None and incumbent_passed(r)
            and not reference_conflict(r))


def admitted_a(r):
    """Report A: model reached the solver (not refused by the importer, no construction error)."""
    return r["status"] not in ("source_model_mismatch", "worker_error")


def admitted_b(r):
    """Report B: a complete model record was returned."""
    return isinstance(r.get("model_metadata"), dict)


def cut_count(r, require_complete_flag):
    cuts = r.get("cuts")
    if not isinstance(cuts, list):
        return None
    if require_complete_flag and r.get("cut_log_complete") is not True:
        return None
    return len(cuts)


def time_a(r):
    """Report A in-process time: total_seconds + source_read_seconds."""
    return r["total_seconds"] + r.get("source_read_seconds", 0.0) if "total_seconds" in r else None


def time_b(r):
    """Report B integration time: total_seconds + preparation_seconds."""
    return r["total_seconds"] + r.get("preparation_seconds", 0.0) if "total_seconds" in r else None


def compare_bounds(a, b, field="dual", tol_rel=TOL_REL):
    """Paired bound comparison of mode record a against baseline record b."""
    if a is None or b is None or not ran_scip(a) or not ran_scip(b) or flagged(a) or flagged(b):
        return "unavailable"
    da, db = fnum(a.get(field)), fnum(b.get(field))
    if da is None or db is None:
        return "unavailable"
    improvement = (da - db) if a["sense"] == "min" else (db - da)
    tol = tol_rel * max(1.0, abs(da), abs(db))
    return "better" if improvement > tol else "worse" if improvement < -tol else "tie"


def scip_gap(primal, dual):
    """SCIP-style relative gap |p-d|/min(|p|,|d|); inf if signs differ or one is zero."""
    p, d = fnum(primal), fnum(dual)
    if p is None or d is None:
        return None
    if p == d:
        return 0.0
    if p * d <= 0:
        return math.inf
    return abs(p - d) / min(abs(p), abs(d))


class Index:
    def __init__(self, records):
        self.records = records
        self.by_key = {}
        for r in records:
            key = (r["suite"], r["phase"], r["name"], r["mode"])
            if key in self.by_key:
                raise SystemExit(f"duplicate record key {key}")
            self.by_key[key] = r

    def get(self, suite, phase, name, mode):
        return self.by_key.get((suite, phase, name, mode))

    def select(self, suite=None, phase=None, mode=None, name=None):
        return [r for r in self.records
                if (suite is None or r["suite"] == suite) and (phase is None or r["phase"] == phase)
                and (mode is None or r["mode"] == mode) and (name is None or r["name"] == name)]

    def names(self, suite, phase):
        seen = []
        for r in self.records:
            if r["suite"] == suite and r["phase"] == phase and r["name"] not in seen:
                seen.append(r["name"])
        return seen

    def compare(self, suite, phase, mode, field="dual", baseline="baseline", names=None, tol_rel=TOL_REL):
        counts = Counter()
        rows = {}
        for name in (names or self.names(suite, phase)):
            outcome = compare_bounds(self.get(suite, phase, name, mode),
                                     self.get(suite, phase, name, baseline), field, tol_rel)
            counts[outcome] += 1
            rows[name] = outcome
        return counts, rows


def btwu(counts):
    return (counts.get("better", 0), counts.get("tie", 0), counts.get("worse", 0),
            counts.get("unavailable", 0))


def sep(r):
    return r.get("separation") or {}


def disc(r):
    return r.get("discovery") or {}


# --------------------------------------------------------------------------
# Claim bookkeeping
# --------------------------------------------------------------------------

class Audit:
    def __init__(self):
        self.rows = []

    def _add(self, cid, source, text, expected, computed, ok):
        self.rows.append((cid, source, text, expected, computed, ok))

    def eq(self, cid, source, text, expected, computed):
        self._add(cid, source, text, expected, computed, expected == computed)

    def rounded(self, cid, source, text, expected, computed, decimals):
        ok = computed is not None and f"{computed:.{decimals}f}" == f"{expected:.{decimals}f}"
        shown = None if computed is None else float(f"{computed:.{decimals + 3}f}")
        self._add(cid, source, text, expected, shown, ok)

    def true(self, cid, source, text, condition, detail=""):
        shown = (f"True ({fmt_cell(detail)})" if detail != "" else True) if condition else detail
        self._add(cid, source, text, True, shown, bool(condition))

    def mismatches(self):
        return [row for row in self.rows if not row[5]]

    def report(self):
        lines = ["| ID | Source | Claim | Stated | Recomputed | Result |",
                 "|---|---|---|---|---|---|"]
        for cid, source, text, expected, computed, ok in self.rows:
            lines.append(f"| {cid} | {source} | {text} | {fmt_cell(expected)} | {fmt_cell(computed)} | "
                         f"{'PASS' if ok else '**MISMATCH**'} |")
        bad = self.mismatches()
        lines += ["", f"Checked {len(self.rows)} items (stated values and consistency checks): "
                      f"{len(self.rows) - len(bad)} pass, {len(bad)} mismatch."]
        return "\n".join(lines)


def fmt_cell(value):
    if isinstance(value, (list, tuple, set, frozenset)):
        items = sorted(value) if isinstance(value, (set, frozenset)) else list(value)
        return "[" + ", ".join(str(v) for v in items) + "]"
    return str(value).replace("|", "/")


# --------------------------------------------------------------------------
# Shared checks
# --------------------------------------------------------------------------

def check_records_match_jobs(audit, cid, source, records, jobs):
    keys = ("name", "mode", "phase", "seed", "suite", "time_limit", "node_limit")
    mismatched = [i for i, (r, j) in enumerate(zip(records, jobs))
                  if any(r.get(k) != j.get(k) for k in keys if k in j)]
    audit.eq(cid + ".jobs", source, "records equal frozen jobs (count)", len(jobs), len(records))
    audit.eq(cid + ".joborder", source, "records in job order with identical parameters (mismatching rows)",
             0, len(mismatched))


def check_run_files(audit, cid, source, directory, records):
    """Per-run JSON files agree with records.jsonl on status, bounds and cut counts."""
    bad = []
    for r in records:
        path = directory / "runs" / f"{r['run_id']}.json"
        if not path.exists():
            bad.append(r["run_id"] + ":missing")
            continue
        run = load_json(path)
        for k in ("status", "dual", "primal", "root_dual", "nodes"):
            if run.get(k) != r.get(k):
                bad.append(f"{r['run_id']}:{k}")
        if (len(run["cuts"]) if isinstance(run.get("cuts"), list) else None) != \
                (len(r["cuts"]) if isinstance(r.get("cuts"), list) else None):
            bad.append(r["run_id"] + ":cuts")
    audit.eq(cid + ".runfiles", source, "per-run JSON files that disagree with records.jsonl", 0, len(bad))


def check_manifest(audit, cid, source, directory, stated_count):
    manifest = load_json(directory / "source-manifest.json")
    bad = [k for k, h in manifest.items()
           if not (directory / "snapshot" / k).exists() or sha256_file(directory / "snapshot" / k) != h]
    audit.eq(cid + ".hashes", source, "frozen source/input hashes (manifest entries)", stated_count, len(manifest))
    audit.eq(cid + ".hashok", source, "manifest entries whose snapshot file is missing or has a different SHA256",
             0, len(bad))
    return manifest


def check_replay(audit, cid, source, replay, records, require_complete_flag, stated):
    """stated: dict with cuts, hashes, tamper, missing, bound_runs."""
    rec_cuts = {r["run_id"]: cut_count(r, require_complete_flag) for r in records}
    total = sum(c for c in rec_cuts.values() if c is not None)
    unknown = sorted(rid for rid, c in rec_cuts.items() if c is None)
    audit.eq(cid + ".cuts", source, "recorded added cuts (all phases, from records)", stated["cuts"], total)
    audit.eq(cid + ".replayed", source, "replay: cuts replayed", stated["cuts"], replay["replayed_cuts"])
    run_mismatch = [x["run_id"] for x in replay["runs"]
                    if rec_cuts.get(x["run_id"]) != x["cuts"] or x["replayed_cuts"] != x["cuts"]]
    failed = [x["run_id"] for x in replay["runs"] if not x["passed"] or x["failures"]]
    audit.eq(cid + ".perrun", source, "replay runs whose cut count differs from the record or was not fully replayed",
             0, len(run_mismatch))
    audit.eq(cid + ".passed", source, "replay runs failed (and overall pass flag)", (0, True),
             (len(failed), replay["passed"]))
    audit.eq(cid + ".tamper", source, "tampering controls rejected / total",
             (stated["tamper"], stated["tamper"]),
             (sum(bool(v) for v in replay["tamper_rejections"].values()), len(replay["tamper_rejections"])))
    audit.eq(cid + ".srcfiles", source, "replay: source/input hashes verified", stated["hashes"],
             replay["source_files_verified"])
    audit.eq(cid + ".missing", source, "records with unknown cut count (no complete cut log)",
             stated["missing"], len(unknown))
    audit.eq(cid + ".omitted", source, "replay omitted runs = records with unknown cut count",
             unknown, sorted(x["run_id"] for x in replay["omitted_runs"]))
    audit.eq(cid + ".bound", source, "replay: runs bound to an original model", stated["bound_runs"],
             replay["bound_runs"])
    return total


def decode(x):
    """Plain JSON number or {"binary64": hex} tag."""
    if isinstance(x, dict):
        return float.fromhex(x["binary64"])
    return float(x)


def eval_tree(tree, values):
    tag = tree[0]
    if tag == "num":
        return decode(tree[1])
    if tag == "var":
        return values[int(tree[1])]
    args = [eval_tree(t, values) for t in tree[1:]]
    if tag == "sum":
        out = math.fsum(args)
    elif tag == "times":
        out = math.prod(args)
    elif tag == "negate":
        out = -args[0]
    elif tag == "divide":
        out = args[0] / args[1]
    elif tag == "square":
        out = args[0] * args[0]
    elif tag == "power":
        out = args[0] ** args[1]
    else:
        out = {"log": math.log, "exp": math.exp, "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
               "abs": abs}[tag](args[0])
    if isinstance(out, complex) or not math.isfinite(out):
        raise ValueError(f"{tag} left the real domain")
    return out


def recheck_incumbent(r, tol=1e-5):
    """Independent numerical residual check of a returned original-variable vector against the
    archived original model: bounds, integrality, every row (scaled by max(1, |side|, sum of
    absolute term values)), expression domains, and the reported objective. Returns
    (passed, worst scaled violation, objective discrepancy)."""
    model, x = r["original_model"], [float(v) for v in r["original_values"]]
    worst = 0.0
    for v, lo, hi, kind in zip(x, model["var_lb"], model["var_ub"], model["var_type"]):
        lo, hi = decode(lo), decode(hi)
        if kind == "B":
            lo, hi = max(lo, 0.0), min(hi, 1.0)
        if math.isfinite(lo):
            worst = max(worst, (lo - v) / max(1.0, abs(lo)))
        if math.isfinite(hi):
            worst = max(worst, (v - hi) / max(1.0, abs(hi)))
        if kind in ("B", "I"):
            worst = max(worst, abs(v - round(v)))
    try:
        values = []
        for row in model["rows"]:
            terms = [decode(c) * x[int(i)] for i, c in row["lin"].items()]
            terms += [decode(c) * x[int(i)] * x[int(j)] for i, j, c in row["quad"]]
            if row["nl"] is not None:
                terms.append(eval_tree(row["nl"], x))
            values.append((math.fsum(terms), math.fsum(abs(t) for t in terms)))
    except (ValueError, ArithmeticError, OverflowError):
        return False, math.inf, math.inf
    for (y, mag), row in zip(values[1:], model["rows"][1:]):
        for side, residual in ((decode(row["lb"]), decode(row["lb"]) - y), (decode(row["ub"]), y - decode(row["ub"]))):
            if math.isfinite(side):
                worst = max(worst, residual / max(1.0, abs(side), mag))
    objective = values[0][0] + decode(model["obj_const"])
    discrepancy = abs(objective - r["primal"]) / max(1.0, abs(objective))
    return worst <= tol and discrepancy <= tol, worst, discrepancy


def check_incumbents(audit, cid, source, records, stated_checked):
    checked = [r for r in records if incumbent_checked(r)]
    audit.eq(cid + ".inc", source, "returned incumbents independently checked", stated_checked, len(checked))
    audit.eq(cid + ".incfail", source, "checked incumbents that failed", 0,
             sum(not incumbent_passed(r) for r in checked))
    returned = [r for r in records if isinstance(r.get("original_values"), list) and fnum(r.get("primal")) is not None]
    results = [recheck_incumbent(r) for r in returned]
    audit.eq(cid + ".reeval", source, "incumbents re-evaluated by this script (stdlib evaluator): count, passing at 1e-5",
             (stated_checked, stated_checked), (len(returned), sum(ok for ok, _, _ in results)))
    audit.true(cid + ".reevalmax", source, "largest re-evaluated scaled violation / objective discrepancy <= 1e-5",
               all(ok for ok, _, _ in results),
               (max((w for _, w, _ in results), default=0.0), max((d for _, _, d in results), default=0.0)))
    audit.eq(cid + ".refconf", source, "final or root dual bounds conflicting with reference", 0,
             sum(reference_conflict(r) for r in records))


def check_mode_rotation(records, modes, list_key, global_index=None):
    """Mode order of each (phase list, model) group is the mode tuple rotated by the
    model index. Report B restarts the index in every phase list (holdout, diagnostic and
    synthetic full lists, root list, repeat list); Report A uses the global case index."""
    order = defaultdict(list)
    for r in records:
        order[(list_key(r), r["name"])].append((int(r["run_id"].split("_")[0]), r["mode"]))
    by_list = defaultdict(list)
    for (key, name), entries in order.items():
        entries.sort()
        by_list[key].append((entries[0][0], name, [m for _, m in entries]))
    bad = []
    for key, groups in by_list.items():
        groups.sort()
        for i, (_, name, observed) in enumerate(groups):
            if len(observed) != len(modes):
                continue  # two-mode ablation phases have a fixed order
            j = global_index[name] if global_index is not None else i
            expected = [modes[(j + k) % len(modes)] for k in range(len(modes))]
            if observed != expected:
                bad.append((key, name, observed))
    return bad


def metadata_rows():
    with open(METADATA) as stream:
        return {r["name"]: r for r in csv.DictReader(stream, delimiter=";")}


# --------------------------------------------------------------------------
# Report A (campaign-v1)
# --------------------------------------------------------------------------

def audit_a(audit, recs, meta):
    S = "A ev"
    R = "A results.md"
    ix = Index(recs)
    jobs = load_json(V1 / "jobs.json")
    completion = load_json(V1 / "completion.json")
    environment = load_json(V1 / "environment.json")
    replay = load_json(V1 / "replay.json")
    selection = load_json(EXP_A / "holdout-selection.json")

    check_records_match_jobs(audit, "A.0", S, recs, jobs)
    check_run_files(audit, "A.0", S, V1, recs)
    audit.eq("A.1", S, "completed runs", 316, len(recs))
    audit.rounded("A.2", S, "supervised wall seconds", 443.6, completion["wall_seconds"], 1)
    status = Counter(r["status"] for r in recs)
    audit.eq("A.3", "A completion.json", "status counts",
             {"optimal": 162, "gaplimit": 42, "nodelimit": 56, "timelimit": 12,
              "source_model_mismatch": 36, "worker_error": 8}, dict(status))
    audit.eq("A.4", S, "structured importer refusals, all phases", 36, status["source_model_mismatch"])
    audit.eq("A.5", S, "no hard process timeout / budget exhaustion statuses", 0,
             status["process_timeout"] + status["campaign_budget_exhausted"] + status["worker_no_output"])
    longest = max(r["outer_wall_seconds"] for r in recs)
    audit.true("A.6", S, "every outer worker wall time below the 20 s hard timeout",
               environment["worker_timeout"] == 20.0 and longest < 20.0, longest)

    # Selection (protocol and evidence)
    ranks_ok = all(e["rank"] == hashlib.sha256(("convexification-holdout-v1:" + e["name"]).encode()).hexdigest()
                   for e in selection["eligible"])
    order_ok = [e["rank"] for e in selection["eligible"]] == sorted(e["rank"] for e in selection["eligible"])
    audit.eq("A.7", S, "excluded earlier-campaign names", 123, len(selection["excluded_names"]))
    audit.eq("A.8", S, "eligible models", 279, len(selection["eligible"]))
    audit.true("A.9", S, "ranks recomputed as SHA256(prefix+name) and eligible list sorted by rank",
               ranks_ok and order_ok, (ranks_ok, order_ok))
    audit.eq("A.10", S, "selected = first 24 in rank order",
             [e["name"] for e in selection["eligible"][:24]], [e["name"] for e in selection["selected"]])
    sel = [e["name"] for e in selection["selected"]]
    audit.eq("A.11", S, "selected models with integer variables (instancedata.csv)", 11,
             sum(int(meta[n]["nbinvars"]) + int(meta[n]["nintvars"]) > 0 for n in sel))
    audit.eq("A.12", S, "selected models classified convex (instancedata.csv)", 7,
             sum(meta[n]["convex"] == "True" for n in sel))
    audit.eq("A.13", S, "initial six = first six of the ranking", sel[:6], selection["first_six_subset"])
    audit.eq("A.14", S, "held-out full-run names = selected 24 (in hash order)", sel, ix.names("holdout", "full"))
    audit.eq("A.15", S, "historical diagnostic suite",
             {"btest14", "waterno2_06", "ghg_2veh", "chp_partload"}, set(ix.names("historical", "full")))
    audit.eq("A.16", S, "synthetic mechanism/control cases", 13, len(ix.names("synthetic", "full")))

    # Budgets, seeds, limits
    full_like = [r for r in recs if r["phase"] in ("full", "no_cache", "pairs_only", "repeat")]
    audit.eq("A.17", S, "time limits of full-budget phases (s)", {6.0}, {r["time_limit"] for r in full_like})
    root = ix.select(phase="root")
    audit.eq("A.18", S, "root-only time limit (s) and node limit", {(2.0, 1)},
             {(r["time_limit"], r["node_limit"]) for r in root})
    audit.eq("A.19", S, "root-only cases: 24 held-out + five mechanisms",
             set(sel) | {"quartic_balance_8", "exp_pair", "simplex_quadratic_vector", "overlapping_products",
                         "star_marginal_inconsistency"}, {r["name"] for r in root})
    audit.eq("A.20", "A protocol", "seed-1 repeat subset",
             set(sel[:3]) | {"quartic_balance_8", "exp_pair", "simplex_quadratic_vector"},
             {r["name"] for r in ix.select(phase="repeat")})
    audit.eq("A.21", S, "seeds (non-repeat, repeat)", ({0}, {1}),
             ({r["seed"] for r in recs if r["phase"] != "repeat"}, {r["seed"] for r in ix.select(phase="repeat")}))
    audit.eq("A.22", S, "relative gap limit in every config", {0.0001},
             {r["config"]["gap_limit"] for r in recs if isinstance(r.get("config"), dict)})
    audit.eq("A.23", S, "thread environment set to one", {"1"}, set(environment["thread_environment"].values()))
    case_index = {}
    for r in recs:  # global case order = order of first appearance in the full phase
        if r["phase"] == "full":
            case_index.setdefault(r["name"], len(case_index))
    audit.eq("A.24", "A audit", "mode-order rotation by case index: violations", [],
             check_mode_rotation(recs, MODES_A, lambda r: r["phase"], case_index))

    # Primary table (evidence Table tab:primary) + results.md columns
    table = {
        ("synthetic", "baseline"): (13, 13, 12, 0, 6.57, 0, 16.94),
        ("synthetic", "control"): (13, 13, 13, 0, 1.66, 0, 11.57),
        ("synthetic", "all"): (13, 13, 13, 89, 2.51, 7, 13.18),
        ("synthetic", "auto"): (13, 13, 13, 72, 2.45, 7, 13.14),
        ("holdout", "baseline"): (24, 20, 19, 0, 17.40, 0, 36.66),
        ("holdout", "control"): (24, 20, 19, 0, 20.66, 0, 40.12),
        ("holdout", "all"): (24, 20, 18, 230, 25.41, 12, 45.44),
        ("holdout", "auto"): (24, 20, 18, 106, 23.01, 8, 42.49),
        ("historical", "baseline"): (4, None, 0, 0, 6.22, 0, 9.60),
        ("historical", "control"): (4, None, 0, 0, 6.84, 0, 10.36),
        ("historical", "all"): (4, None, 0, 24, 6.91, 1, 10.41),
        ("historical", "auto"): (4, None, 0, 24, 6.88, 1, 10.26),
    }
    for (suite, mode), (n, adm, sol, cuts, secs, cases, outer) in table.items():
        rows = ix.select(suite, "full", mode)
        src = S if suite != "historical" else R
        tag = f"A.T.{suite}.{mode}"
        audit.eq(tag + ".n", src, f"{suite}/{mode} selected", n, len(rows))
        if adm is not None:
            audit.eq(tag + ".adm", src, f"{suite}/{mode} admitted", adm, sum(map(admitted_a, rows)))
        audit.eq(tag + ".sol", src, f"{suite}/{mode} solved", sol, sum(map(solved, rows)))
        audit.eq(tag + ".cuts", src, f"{suite}/{mode} recorded cuts", cuts,
                 sum(cut_count(r, False) or 0 for r in rows))
        audit.eq(tag + ".cases", R, f"{suite}/{mode} cases with recorded cuts", cases,
                 sum((cut_count(r, False) or 0) > 0 for r in rows))
        audit.rounded(tag + ".time", src, f"{suite}/{mode} summed in-process seconds", secs,
                      sum(t for t in map(time_a, rows) if t is not None), 2)
        audit.rounded(tag + ".outer", R if suite != "holdout" else S, f"{suite}/{mode} summed outer seconds",
                      outer, sum(r["outer_wall_seconds"] for r in rows), 2)

    # Refusals and errors on held-out
    for mode in MODES_A:
        refused = {r["name"] for r in ix.select("holdout", "full", mode) if r["status"] == "source_model_mismatch"}
        audit.eq(f"A.25.{mode}", S, f"held-out refusals ({mode})", {"syn15m", "cvxnonsep_psig30r", "syn10hfsg"},
                 refused)
        audit.true(f"A.26.{mode}", S, f"refusal diagnostics name a log domain ({mode})",
                   all("log" in (r.get("diagnostic") or "") for r in ix.select("holdout", "full", mode)
                       if r["status"] == "source_model_mismatch"))
    errors = sorted(r["run_id"] for r in recs if r["status"] == "worker_error")
    audit.eq("A.27", S, "eight worker errors = cvxnonsep_pcon40r full+root x four modes",
             sorted(f"{x}" for x in errors if "cvxnonsep_pcon40r" in x and ("__full" in x or "__root" in x)),
             errors)
    audit.eq("A.27b", S, "worker errors count", 8, len(errors))
    audit.true("A.28", S, "pcon40r errors are variable-exponent construction failures",
               all("expon" in ((r.get("reason") or "") + (r.get("exception") or "")).lower()
                   or "power" in ((r.get("reason") or "") + (r.get("exception") or "")).lower()
                   for r in recs if r["status"] == "worker_error"),
               [(r.get("exception"), r.get("reason")) for r in recs if r["status"] == "worker_error"][:1])

    # Lost solve and other named cases
    g = {m: ix.get("holdout", "full", "genpooling_lee2", m) for m in MODES_A}
    audit.eq("A.29", S, "genpooling_lee2 statuses (baseline, control, all, auto)",
             (True, True, "timelimit", "timelimit"),
             (solved(g["baseline"]), solved(g["control"]), g["all"]["status"], g["auto"]["status"]))
    audit.rounded("A.30a", S, "genpooling_lee2 baseline seconds", 5.61, time_a(g["baseline"]), 2)
    audit.rounded("A.30b", S, "genpooling_lee2 control seconds", 4.89, time_a(g["control"]), 2)
    audit.eq("A.31", S, "kall_circles_c6b time-limited in every mode", ["timelimit"] * 4,
             [ix.get("holdout", "full", "kall_circles_c6b", m)["status"] for m in MODES_A])
    q = {m: ix.get("synthetic", "full", "quartic_balance_8", m) for m in MODES_A}
    audit.eq("A.32", S, "quartic_balance_8 solved (baseline, control, all, auto)",
             (False, True, True, True), tuple(solved(q[m]) for m in MODES_A))
    st = {m: ix.get("synthetic", "full", "star_marginal_inconsistency", m) for m in MODES_A}
    audit.true("A.33", S, "star case: baseline solved with dual ~ 1/128",
               solved(st["baseline"]) and abs(st["baseline"]["dual"] - 1 / 128) < 1e-5, st["baseline"]["dual"])
    audit.rounded("A.34a", S, "star case baseline seconds", 0.10, time_a(st["baseline"]), 2)
    audit.rounded("A.34b", S, "star case all seconds", 0.50, time_a(st["all"]), 2)
    audit.rounded("A.34c", S, "star case auto seconds", 0.48, time_a(st["auto"]), 2)
    po = {m: ix.get("synthetic", "pairs_only", "star_marginal_inconsistency", m) for m in ("all", "auto")}
    audit.rounded("A.35a", S, "star merging disabled: all seconds", 0.19, time_a(po["all"]), 2)
    audit.rounded("A.35b", S, "star merging disabled: auto seconds", 0.10, time_a(po["auto"]), 2)
    audit.eq("A.35c", S, "star merging disabled: status unchanged",
             (st["all"]["status"], st["auto"]["status"]), (po["all"]["status"], po["auto"]["status"]))
    nc = ix.select(phase="no_cache")
    audit.eq("A.36", S, "no_cache ablation: mechanism runs solved", (10, 10), (len(nc), sum(map(solved, nc))))

    # Historical
    h_adm = {r["name"] for r in ix.select("historical", "full") if admitted_a(r)}
    audit.eq("A.37", S, "historical models passing the importer", {"waterno2_06"}, h_adm)
    w = [ix.get("historical", "full", "waterno2_06", m) for m in MODES_A]
    audit.eq("A.38", S, "waterno2_06 time-limited in every mode", ["timelimit"] * 4, [r["status"] for r in w])
    for m, r, val in zip(MODES_A, w, (26.59, 21.17, 7.05, 2.41)):
        audit.rounded(f"A.39.{m}", S, f"waterno2_06 lower bound ({m})", val, r["dual"], 2)

    # Comparisons
    stated_full = {("synthetic", "control"): (3, 10, 0, 0), ("synthetic", "all"): (2, 9, 2, 0),
                   ("synthetic", "auto"): (2, 9, 2, 0), ("holdout", "control"): (1, 15, 4, 4),
                   ("holdout", "all"): (1, 14, 5, 4), ("holdout", "auto"): (3, 12, 5, 4),
                   ("historical", "control"): (0, 0, 1, 3), ("historical", "all"): (0, 0, 1, 3),
                   ("historical", "auto"): (0, 0, 1, 3)}
    for (suite, mode), expected in stated_full.items():
        audit.eq(f"A.C.full.{suite}.{mode}", R, f"final dual vs baseline B/T/W/U ({suite}, {mode})",
                 expected, btwu(ix.compare(suite, "full", mode)[0]))
    audit.eq("A.C.root.all", S, "held-out root-only vs baseline B/T/W/U (all)", (3, 15, 2, 4),
             btwu(ix.compare("holdout", "root", "all")[0]))
    audit.eq("A.C.root.auto", S, "held-out root-only vs baseline B/T/W/U (auto)", (3, 14, 3, 4),
             btwu(ix.compare("holdout", "root", "auto")[0]))

    # Work counters on primary held-out runs
    hall, hauto = ix.select("holdout", "full", "all"), ix.select("holdout", "full", "auto")
    audit.eq("A.40", S, "candidate LPs (all, auto)", (1073, 323),
             (sum(sep(r).get("candidate_lps", 0) for r in hall), sum(sep(r).get("candidate_lps", 0) for r in hauto)))
    audit.rounded("A.41a", S, "callback seconds (all)", 5.59, sum(sep(r).get("callback_seconds", 0) for r in hall), 2)
    audit.rounded("A.41b", S, "callback seconds (auto)", 3.05, sum(sep(r).get("callback_seconds", 0) for r in hauto), 2)
    audit.rounded("A.42a", S, "certification seconds (all)", 0.70,
                  sum(sep(r).get("certification_seconds", 0) for r in hall), 2)
    audit.rounded("A.42b", S, "certification seconds (auto)", 0.34,
                  sum(sep(r).get("certification_seconds", 0) for r in hauto), 2)
    audit.eq("A.43", S, "unsuccessful support attempts (all, auto)", (95, 14),
             (sum(sep(r).get("certification_failures", 0) for r in hall),
              sum(sep(r).get("certification_failures", 0) for r in hauto)))
    audit.eq("A.44", S, "screen queries and skips, all phases", (506, 2),
             (sum(sep(r).get("screen_queries", 0) for r in recs), sum(sep(r).get("screen_skips", 0) for r in recs)))

    # Replay and incumbents
    check_manifest(audit, "A.45", S, V1, 101)
    check_replay(audit, "A.46", S, replay, recs, False,
                 {"cuts": 1082, "hashes": 101, "tamper": 12, "missing": 8, "bound_runs": 308})
    audit.eq("A.47", S, "records with an original-model output", 308,
             sum(isinstance(r.get("original_model"), dict) for r in recs))
    check_incumbents(audit, "A.48", S, recs, 270)
    return ix


# --------------------------------------------------------------------------
# Report B (campaign-v2)
# --------------------------------------------------------------------------

def audit_b(audit, recs, meta, ix_a, recs_a):
    S = "B ev"
    R = "B results.md"
    C = "B coverage.md"
    ix = Index(recs)
    jobs = load_json(V2 / "jobs.json")
    completion = load_json(V2 / "completion.json")
    environment = load_json(V2 / "environment.json")
    replay = load_json(V2 / "replay.json")
    selection = load_json(EXP_B / "holdout-selection.json")
    a_selection = load_json(EXP_A / "holdout-selection.json")

    # "The earlier result is retained" (numbers about Report A, recomputed from campaign-v1)
    ha = {m: ix_a.select("holdout", "full", m) for m in MODES_A}
    audit.eq("B.0.1", S, "first campaign records", 316, len(recs_a))
    audit.eq("B.0.2", S, "first campaign selected/admitted held-out", (24, 20),
             (len(ha["baseline"]), sum(map(admitted_a, ha["baseline"]))))
    audit.eq("B.0.3", S, "first campaign held-out solved (baseline, control, all, auto)", (19, 19, 18, 18),
             tuple(sum(map(solved, ha[m])) for m in MODES_A))
    audit.eq("B.0.4", S, "first campaign direction LPs (all, auto)", (1073, 323),
             tuple(sum(sep(r).get("candidate_lps", 0) for r in ha[m]) for m in ("all", "auto")))
    audit.eq("B.0.5", S, "first campaign callback seconds (all, auto)", ("5.59", "3.05"),
             tuple(f"{sum(sep(r).get('callback_seconds', 0) for r in ha[m]):.2f}" for m in ("all", "auto")))
    audit.eq("B.0.6", S, "first campaign synthetic solved (control, all, auto, baseline)", (13, 13, 13, 12),
             tuple(sum(map(solved, ix_a.select("synthetic", "full", m))) for m in ("control", "all", "auto", "baseline")))
    audit.eq("B.0.7", S, "first campaign cuts replayed / incumbents checked / construction errors",
             (1082, 270, 8), (load_json(V1 / "replay.json")["replayed_cuts"],
                              sum(map(incumbent_checked, recs_a)),
                              sum(r["status"] == "worker_error" for r in recs_a)))

    # Population
    strata_of = {}
    for name in selection["eligible_names_in_rank_order"]:
        row = meta[name]
        integer = int(row["nbinvars"]) + int(row["nintvars"]) > 0
        strata_of[name] = ("convex" if row["convex"] == "True" else
                           "nonconvex_integer" if integer else "nonconvex_continuous")
    names = selection["eligible_names_in_rank_order"]
    ranks = [hashlib.sha256(("convexification-holdout-v2:" + n).encode()).hexdigest() for n in names]
    audit.true("B.1", S, "eligible list sorted by recomputed SHA256 rank", ranks == sorted(ranks))
    audit.eq("B.2", S, "eligible models", 422, len(names))
    audit.eq("B.2b", S, "eligible count field", 422, selection["eligible_count"])
    audit.eq("B.3", S, "eligible stratum counts recomputed from instancedata.csv (convex, nonconvex cont., nonconvex int.)",
             (85, 208, 129), tuple(sum(s == k for s in strata_of.values())
                                   for k in ("convex", "nonconvex_continuous", "nonconvex_integer")))
    recomputed_sel = []
    for stratum in ("convex", "nonconvex_continuous", "nonconvex_integer"):
        recomputed_sel += [n for n in names if strata_of[n] == stratum][:10]
    recomputed_sel.sort(key=names.index)
    sel = [e["name"] for e in selection["selected"]]
    audit.eq("B.4", S, "selected = first ten per stratum in rank order", recomputed_sel, sel)
    audit.eq("B.5", S, "selected per stratum", (10, 10, 10),
             tuple(sum(e["stratum"] == k for e in selection["selected"])
                   for k in ("convex", "nonconvex_continuous", "nonconvex_integer")))
    previous = set(a_selection["excluded_names"]) | {e["name"] for e in a_selection["selected"]} | \
        {p.stem for p in (V1 / "cases").glob("*.json")}
    audit.eq("B.6", S, "selected models overlapping prior convexification campaign names", set(), set(sel) & previous)
    audit.eq("B.6b", "B protocol", "instancedata.csv SHA256 equals frozen manifest entry",
             load_json(V2 / "source-manifest.json")["code/minlp_solver_lab/instances/instancedata.csv"],
             sha256_file(METADATA))
    audit.eq("B.7", S, "holdout full names = selection order", sel, ix.names("holdout", "full"))

    # Schedule
    check_records_match_jobs(audit, "B.8", S, recs, jobs)
    check_run_files(audit, "B.8", S, V2, recs)
    phases = Counter()
    for r in recs:
        phases[{"holdout": "holdout-full", "diagnostic": "diagnostic-full", "synthetic": "mechanism-full"}[r["suite"]]
               if r["phase"] == "full" else r["phase"]] += 1
    audit.eq("B.9", S, "schedule: holdout full, diagnostic full, mechanism full, root, repeat (total 282)",
             (90, 30, 39, 105, 18, 282),
             (phases["holdout-full"], phases["diagnostic-full"], phases["mechanism-full"], phases["root"],
              phases["repeat"], len(recs)))
    limits = {}
    for r in recs:
        limits.setdefault((r["suite"] if r["phase"] == "full" else r["phase"]), set()).add(
            (r["time_limit"], r["node_limit"], r["worker_timeout"], r["seed"]))
    audit.eq("B.10", S, "(time limit, node limit, hard timeout, seed) per phase",
             {"holdout": {(30.0, None, 45.0, 0)}, "diagnostic": {(30.0, None, 45.0, 0)},
              "synthetic": {(10.0, None, 20.0, 0)}, "root": {(5.0, 1, 15.0, 0)},
              "repeat": {(30.0, None, 45.0, 1)}}, limits)
    audit.eq("B.11", "B protocol", "sum of hard process timeouts (minutes) < 150-minute cap",
             (142.75, 150.0), (sum(r["worker_timeout"] for r in recs) / 60, environment["wall_cap"] / 60))
    audit.eq("B.12", "B protocol", "seed-one repeat = first six hash-ranked holdout models", sel[:6],
             ix.names("holdout", "repeat"))
    audit.eq("B.13", S, "root-only cases = 30 holdout + five mechanisms",
             set(sel) | {"quartic_balance_8", "exp_pair", "simplex_quadratic_vector", "overlapping_products",
                         "star_marginal_inconsistency"}, {r["name"] for r in ix.select(phase="root")})
    audit.eq("B.14", S, "mode-order rotation by model index within each phase list: violations", [],
             check_mode_rotation(recs, MODES_B, lambda r: (r["phase"], r["suite"] if r["phase"] == "full" else "")))
    audit.eq("B.15", S, "relative gap limit in every config", {0.0001},
             {r["config"]["gap_limit"] for r in recs if isinstance(r.get("config"), dict)})

    # Completion
    audit.rounded("B.16", S, "campaign outer wall seconds", 1338.6, completion["wall_seconds"], 1)
    status = Counter(r["status"] for r in recs)
    audit.eq("B.17", S, "status counts", {"optimal": 106, "gaplimit": 74, "timelimit": 31, "nodelimit": 67,
                                          "worker_error": 4}, dict(status))
    audit.true("B.18", S, "no hard timeouts: every outer wall below its process limit",
               all(r["outer_wall_seconds"] < r["worker_timeout"] for r in recs),
               max(r["outer_wall_seconds"] / r["worker_timeout"] for r in recs))

    # Primary holdout table
    H = {m: ix.select("holdout", "full", m) for m in MODES_B}
    for m in MODES_B:
        audit.eq(f"B.19.{m}", S, f"holdout admitted ({m})", 30, sum(map(admitted_b, H[m])))
    solved_sets = {m: {r["name"] for r in H[m] if solved(r)} for m in MODES_B}
    audit.eq("B.20", S, "holdout solved (baseline, all, auto)", (25, 25, 25),
             tuple(len(solved_sets[m]) for m in MODES_B))
    audit.true("B.21", S, "same 25 solved models in every mode",
               solved_sets["baseline"] == solved_sets["all"] == solved_sets["auto"])
    stated = {"baseline": (0, 0, 170.57, 197.30), "all": (38, 7, 187.02, 213.20), "auto": (10, 3, 187.12, 213.56)}
    for m, (cuts, cases, secs, outer) in stated.items():
        audit.eq(f"B.22.{m}", S, f"holdout added cuts ({m})", cuts, sum(cut_count(r, True) or 0 for r in H[m]))
        audit.eq(f"B.23.{m}", S, f"holdout cases with cuts ({m})", cases,
                 sum((cut_count(r, True) or 0) > 0 for r in H[m]))
        audit.rounded(f"B.24.{m}", S, f"holdout summed integration seconds ({m})", secs,
                      sum(time_b(r) for r in H[m]), 2)
        audit.rounded(f"B.24o.{m}", R, f"holdout summed outer seconds ({m})", outer,
                      sum(r["outer_wall_seconds"] for r in H[m]), 2)
    audit.eq("B.25", S, "candidate LPs (all, auto)", (186, 66),
             tuple(sum(sep(r).get("candidate_lps", 0) for r in H[m]) for m in ("all", "auto")))
    audit.eq("B.26", S, "support calls (all, auto)", (138, 51),
             tuple(sum(sep(r).get("certification_calls", 0) for r in H[m]) for m in ("all", "auto")))
    for m, cb, dv in (("all", 27.63, 24.41), ("auto", 27.00, 24.63)):
        audit.rounded(f"B.27.{m}", S, f"callback seconds ({m})", cb, sum(sep(r).get("callback_seconds", 0) for r in H[m]), 2)
        audit.rounded(f"B.28.{m}", S, f"discovery seconds ({m})", dv,
                      sum(sep(r).get("discovery_seconds", 0) for r in H[m]), 2)
        rows = H[m]
        audit.eq(f"B.29.{m}", S, f"discovery runs / no supported blocks / solved without separator call ({m})",
                 (28, 12, 2),
                 (sum(r.get("discovery") is not None for r in rows),
                  sum(r.get("discovery") is not None and disc(r).get("blocks", 0) == 0 for r in rows),
                  sum(sep(r).get("calls", 0) == 0 and solved(r) for r in rows)))
        audit.eq(f"B.30.{m}", S, f"supported blocks / auto-eligible / declined source sides ({m})", (156, 63, 186),
                 (sum(disc(r).get("blocks", 0) for r in rows), sum(disc(r).get("auto_eligible", 0) for r in rows),
                  sum(disc(r).get("unsupported_sides", 0) for r in rows)))

    # Comparisons
    full_cmp = {m: ix.compare("holdout", "full", m) for m in ("all", "auto")}
    audit.eq("B.31.all", S, "final dual vs baseline B/T/W/U (all)", (2, 21, 7, 0), btwu(full_cmp["all"][0]))
    audit.eq("B.31.auto", S, "final dual vs baseline B/T/W/U (auto)", (2, 24, 4, 0), btwu(full_cmp["auto"][0]))
    better = {n for m in ("all", "auto") for n, o in full_cmp[m][1].items() if o == "better"}
    audit.true("B.32", S, "improved final bounds occur only on models solved in all modes",
               better <= (solved_sets["baseline"] & solved_sets["all"] & solved_sets["auto"]), sorted(better))
    unsolved = [n for n in sel if n not in solved_sets["baseline"]]
    audit.eq("B.33", S, "number of common unsolved models", 5, len(unsolved))
    for m in ("all", "auto"):
        audit.eq(f"B.34.{m}", S, f"unsolved five: B/T/W/U ({m})", (0, 1, 4, 0),
                 btwu(ix.compare("holdout", "full", m, names=unsolved)[0]))
        audit.eq(f"B.35.{m}", S, f"cuts on the unsolved five ({m})", 0,
                 sum(cut_count(ix.get("holdout", "full", n, m), True) or 0 for n in unsolved))
    gp = [ix.get("holdout", "full", "graphpart_clique-40", m)["dual"] for m in MODES_B]
    audit.eq("B.36", S, "graphpart_clique-40 final lower bounds (baseline, all, auto)", ("438", "392", "392"),
             tuple(f"{x:.0f}" for x in gp))
    audit.eq("B.37.all", S, "root-only vs baseline B/T/W/U (all)", (1, 26, 3, 0),
             btwu(ix.compare("holdout", "root", "all")[0]))
    audit.eq("B.37.auto", S, "root-only vs baseline B/T/W/U (auto)", (1, 28, 1, 0),
             btwu(ix.compare("holdout", "root", "auto")[0]))
    rep = {m: ix.select("holdout", "repeat", m) for m in MODES_B}
    audit.eq("B.38", S, "seed-one repeats solved (baseline, all, auto)", (6, 6, 6),
             tuple(sum(map(solved, rep[m])) for m in MODES_B))
    for m in ("all", "auto"):
        audit.eq(f"B.39.{m}", S, f"seed-one final dual vs baseline B/T/W/U ({m})", (0, 6, 0, 0),
                 btwu(ix.compare("holdout", "repeat", m)[0]))

    # Synthetic mechanisms
    for m in MODES_B:
        audit.eq(f"B.40.{m}", S, f"synthetic full solved ({m})", 12, sum(map(solved, ix.select("synthetic", "full", m))))
    sq = {m: ix.get("synthetic", "root", "simplex_quadratic_vector", m) for m in MODES_B}
    audit.eq("B.41", S, "root simplex_quadratic_vector: cuts and status (all, auto)",
             ((2, "optimal"), (2, "optimal")),
             tuple((cut_count(sq[m], True), sq[m]["status"]) for m in ("all", "auto")))
    audit.eq("B.42", S, "root simplex_quadratic_vector cut-mode bound ~ -0.50000002",
             ("-0.50000002", "-0.50000002"), tuple(f"{sq[m]['dual']:.8f}" for m in ("all", "auto")))
    audit.eq("B.43", S, "root simplex_quadratic_vector baseline (status, bound)", ("nodelimit", "-0.50027374"),
             (sq["baseline"]["status"], f"{sq['baseline']['dual']:.8f}"))

    # Diagnostics
    D = {m: ix.select("diagnostic", "full", m) for m in MODES_B}
    audit.eq("B.44", S, "diagnostic solved (baseline, all, auto)", (5, 5, 5),
             tuple(sum(map(solved, D[m])) for m in MODES_B))
    errors = sorted(r["run_id"] for r in recs if r["status"] == "worker_error")
    audit.eq("B.45", S, "worker errors: chp_partload and waterno2_06 in both cut modes",
             ["111_chp_partload__all__full", "112_chp_partload__auto__full",
              "118_waterno2_06__all__full", "119_waterno2_06__auto__full"], errors)
    after_build = []
    for rid in errors:
        log = (V2 / "runs" / f"{rid}.log").read_text(errors="replace")
        after_build.append("RecursionError" in log and "split_affine" in log and "sepa.c" in log)
    audit.eq("B.46", S, "error logs show split_affine RecursionError raised inside the separator (after build)",
             [True] * 4, after_build)
    audit.eq("B.47", S, "baseline admits the models of the four errors", (True, True),
             tuple(admitted_b(ix.get("diagnostic", "full", n, "baseline")) for n in ("chp_partload", "waterno2_06")))
    earlier = ("syn15m", "cvxnonsep_psig30r", "cvxnonsep_pcon40r", "syn10hfsg", "btest14", "ghg_2veh", "chp_partload")
    audit.eq("B.48", S, "seven earlier-refused models admitted (baseline)", [True] * 7,
             [admitted_b(ix.get("diagnostic", "full", n, "baseline")) for n in earlier])

    # results.md diagnostic and synthetic rows, comparisons
    rows_md = {("diagnostic", "baseline"): (10, 5, 0, 0, 156.56, 165.67),
               ("diagnostic", "all"): (8, 5, 15, 2, 103.94, 123.81),
               ("diagnostic", "auto"): (8, 5, 5, 1, 103.45, 123.32),
               ("synthetic", "baseline"): (13, 12, 0, 0, 10.69, 22.08),
               ("synthetic", "all"): (13, 12, 13, 4, 10.86, 22.06),
               ("synthetic", "auto"): (13, 12, 2, 1, 10.69, 21.87)}
    for (suite, m), (adm, sol, cuts, cases, secs, outer) in rows_md.items():
        rows = ix.select(suite, "full", m)
        audit.eq(f"B.R.{suite}.{m}", R, f"{suite}/{m}: admitted, solved, cuts, cases with cuts",
                 (adm, sol, cuts, cases),
                 (sum(map(admitted_b, rows)), sum(map(solved, rows)), sum(cut_count(r, True) or 0 for r in rows),
                  sum((cut_count(r, True) or 0) > 0 for r in rows)))
        audit.rounded(f"B.R.{suite}.{m}.t", R, f"{suite}/{m}: integration seconds", secs,
                      sum(t for t in map(time_b, rows) if t is not None), 2)
        audit.rounded(f"B.R.{suite}.{m}.o", R, f"{suite}/{m}: outer seconds", outer,
                      sum(r["outer_wall_seconds"] for r in rows), 2)
    for (suite, m), expected in {("diagnostic", "all"): (1, 5, 2, 2), ("diagnostic", "auto"): (0, 5, 3, 2),
                                 ("synthetic", "all"): (1, 11, 1, 0), ("synthetic", "auto"): (1, 11, 1, 0)}.items():
        audit.eq(f"B.R.cmp.{suite}.{m}", R, f"final dual vs baseline B/T/W/U ({suite}, {m})", expected,
                 btwu(ix.compare(suite, "full", m)[0]))

    # coverage.md
    cov = {("holdout", "all"): (28, 60, 28, 156, 63, 186, 27.633), ("holdout", "auto"): (28, 61, 28, 156, 63, 186, 27.000),
           ("diagnostic", "all"): (8, 11, 8, 136, 37, 188, 29.677),
           ("diagnostic", "auto"): (8, 13, 8, 136, 37, 188, 28.681),
           ("synthetic", "all"): (6, 16, 6, 5, 1, 1, 0.331), ("synthetic", "auto"): (6, 16, 6, 5, 1, 1, 0.078)}
    for (suite, m), (cbr, cbc, dr, blk, elig, uns, cbs) in cov.items():
        rows = ix.select(suite, "full", m)
        audit.eq(f"B.V.{suite}.{m}", C, f"{suite}/{m}: callback runs, calls, discovery runs, blocks, eligible, unsupported",
                 (cbr, cbc, dr, blk, elig, uns),
                 (sum(sep(r).get("calls", 0) > 0 for r in rows), sum(sep(r).get("calls", 0) for r in rows),
                  sum(r.get("discovery") is not None for r in rows), sum(disc(r).get("blocks", 0) for r in rows),
                  sum(disc(r).get("auto_eligible", 0) for r in rows), sum(disc(r).get("unsupported_sides", 0) for r in rows)))
        audit.rounded(f"B.V.{suite}.{m}.cb", C, f"{suite}/{m}: callback seconds", cbs,
                      sum(sep(r).get("callback_seconds", 0) for r in rows), 3)

    # Replay and incumbents
    check_manifest(audit, "B.49", S, V2, 156)
    total = check_replay(audit, "B.50", S, replay, recs, True,
                         {"cuts": 123, "hashes": 156, "tamper": 14, "missing": 4, "bound_runs": 278})
    audit.eq("B.50b", S, "complete model records (admitted runs) = replay admitted runs", (278, 278),
             (sum(map(admitted_b, recs)), replay["admitted_runs"]))
    check_incumbents(audit, "B.51", S, recs, 271)
    return ix, total


# --------------------------------------------------------------------------
# Repair cohort
# --------------------------------------------------------------------------

def discovery_allowance(r):
    c = r["config"]
    return min(c["max_separation_seconds"],
               c["separation_budget_fraction"] * (r["time_limit"] - r.get("preparation_seconds", 0.0)))


def audit_repair(audit, recs, ix_v2, recs_v2, cuts_v2):
    S = "B ev"
    R = "repair results.md"
    ix = Index(recs)
    plan = load_json(EXP_B / "repair-plan.json")
    completion = load_json(REP / "completion.json")
    replay = load_json(REP / "replay.json")

    # Independent reconstruction of the frozen selection rule from campaign-v2
    triggers = []
    for r in recs_v2:
        if r["mode"] == "baseline":
            continue
        if isinstance(r.get("config"), dict) and r.get("discovery_seconds", 0) > discovery_allowance(r):
            triggers.append((r["run_id"], "overrun"))
        elif r["status"] == "worker_error":
            log = (V2 / "runs" / f"{r['run_id']}.log").read_text(errors="replace")
            if "RecursionError" in log and "split_affine" in log:
                triggers.append((r["run_id"], "recursion"))
    kinds = Counter(k for _, k in triggers)
    audit.eq("R.1", "repair-protocol", "triggering records (overrun, recursion, total)", (46, 4, 50),
             (kinds["overrun"], kinds["recursion"], len(triggers)))
    audit.eq("R.1b", "repair-plan", "triggering run ids equal the frozen plan",
             sorted(t["run_id"] for t in plan["triggers"]), sorted(rid for rid, _ in triggers))
    byid = {r["run_id"]: r for r in recs_v2}
    groups = sorted({(byid[rid]["name"], byid[rid]["phase"], byid[rid]["seed"]) for rid, _ in triggers})
    audit.eq("R.2", S, "selected model/phase/seed groups", 25, len(groups))
    audit.eq("R.2b", "repair-plan", "groups equal the frozen plan", sorted((g["name"], g["phase"], g["seed"])
                                                                         for g in plan["groups"]), groups)
    expected_jobs = sorted((r for r in recs_v2 if (r["name"], r["phase"], r["seed"]) in set(groups)),
                           key=lambda r: int(r["run_id"].split("_")[0]))
    audit.eq("R.3", S, "matched jobs = all three original modes per group, original order",
             [r["run_id"] for r in expected_jobs], [r["original_run_id"] for r in recs])
    audit.eq("R.4", "repair-protocol", "soft budget sum / hard limit sum (s)", (1575.0, 2565.0),
             (sum(r["time_limit"] for r in recs), sum(r["worker_timeout"] for r in recs)))
    same_limits = all((r["time_limit"], r["node_limit"], r["seed"], r["worker_timeout"], r["mode"], r["phase"]) ==
                      (byid[r["original_run_id"]]["time_limit"], byid[r["original_run_id"]]["node_limit"],
                       byid[r["original_run_id"]]["seed"], byid[r["original_run_id"]]["worker_timeout"],
                       byid[r["original_run_id"]]["mode"], byid[r["original_run_id"]]["phase"]) for r in recs)
    audit.true("R.5", S, "phase, seed, time, node and process limits unchanged", same_limits)
    check_run_files(audit, "R.5", S, REP, recs)

    # Completion
    audit.eq("R.6", S, "jobs completed", (75, 75), (len(recs), completion["scheduled"]))
    audit.rounded("R.7", S, "outer wall seconds", 754.5, completion["wall_seconds"], 1)
    audit.eq("R.8", S, "worker errors / missing cut logs / hard timeouts", (0, 0, 0),
             (sum(not ran_scip(r) for r in recs), sum(r.get("cut_log_complete") is not True for r in recs),
              sum(r["outer_wall_seconds"] >= r["worker_timeout"] for r in recs)))

    # Table
    sections = {("full", "holdout"): (8, 4, 12, 3), ("full", "diagnostic"): (7, 4, 10, 0),
                ("root", "holdout"): (9, 0, 11, 3), ("repeat", "holdout"): (1, 1, 3, 0)}
    for (phase, suite), (groups_n, solved_n, all_cuts, auto_cuts) in sections.items():
        rows = {m: ix.select(suite, phase, m) for m in MODES_B}
        tag = f"R.T.{phase}.{suite}"
        audit.eq(tag + ".g", S, f"{phase}/{suite}: groups (records per mode)", (groups_n,) * 3,
                 tuple(len(rows[m]) for m in MODES_B))
        audit.eq(tag + ".s", S, f"{phase}/{suite}: solved per mode", (solved_n,) * 3,
                 tuple(sum(map(solved, rows[m])) for m in MODES_B))
        audit.true(tag + ".id", S, f"{phase}/{suite}: same solved identities in all modes",
                   len({frozenset(r["name"] for r in rows[m] if solved(r)) for m in MODES_B}) == 1)
        audit.eq(tag + ".c", S, f"{phase}/{suite}: cuts (baseline, all, auto)", (0, all_cuts, auto_cuts),
                 tuple(sum(cut_count(r, True) or 0 for r in rows[m]) for m in MODES_B))
    cmp_stated = {("full", "holdout", "all"): (0, 5, 3, 0), ("full", "holdout", "auto"): (0, 6, 2, 0),
                  ("full", "diagnostic", "all"): (0, 6, 1, 0), ("full", "diagnostic", "auto"): (0, 6, 1, 0),
                  ("root", "holdout", "all"): (0, 9, 0, 0), ("root", "holdout", "auto"): (0, 9, 0, 0),
                  ("repeat", "holdout", "all"): (0, 1, 0, 0), ("repeat", "holdout", "auto"): (0, 1, 0, 0)}
    for (phase, suite, m), expected in cmp_stated.items():
        audit.eq(f"R.C.{phase}.{suite}.{m}", S, f"final dual vs matched baseline B/T/W/U ({phase}, {suite}, {m})",
                 expected, btwu(ix.compare(suite, phase, m)[0]))
    for m in ("all", "auto"):
        worse = [n for n, o in ix.compare("diagnostic", "full", m)[1].items() if o == "worse"]
        audit.eq(f"R.9.{m}", S, f"worse diagnostic bound ({m})", ["waterno2_06"], worse)
    for m, val in zip(MODES_B, (123.91, 124.86, 124.82)):
        audit.rounded(f"R.10.{m}", S, f"full holdout summed integration seconds ({m})", val,
                      sum(time_b(r) for r in ix.select("holdout", "full", m)), 2)

    # results.md per-row integration/discovery seconds and incomplete discovery
    md_rows = {("full", "holdout"): ((123.913, 0.000, 0), (124.856, 1.332, 0), (124.819, 1.324, 0)),
               ("full", "diagnostic"): ((96.348, 0.000, 0), (95.496, 2.852, 2), (96.718, 2.900, 2)),
               ("root", "holdout"): ((5.854, 0.000, 0), (7.020, 0.981, 1), (7.270, 0.978, 1)),
               ("repeat", "holdout"): ((1.296, 0.000, 0), (1.913, 0.147, 0), (1.450, 0.140, 0))}
    for (phase, suite), triples in md_rows.items():
        for m, (secs, dsecs, inc) in zip(MODES_B, triples):
            rows = ix.select(suite, phase, m)
            audit.rounded(f"R.M.{phase}.{suite}.{m}.t", R, f"{phase}/{suite}/{m}: integration seconds", secs,
                          sum(time_b(r) for r in rows), 3)
            audit.rounded(f"R.M.{phase}.{suite}.{m}.d", R, f"{phase}/{suite}/{m}: discovery seconds", dsecs,
                          sum(sep(r).get("discovery_seconds", 0) for r in rows), 3)
            audit.eq(f"R.M.{phase}.{suite}.{m}.i", R, f"{phase}/{suite}/{m}: incomplete discoveries", inc,
                     sum(bool(sep(r).get("discovery_incomplete")) for r in rows))

    # Soft-budget behaviour
    cut_mode = [r for r in recs if r["mode"] != "baseline"]
    over = [r for r in cut_mode if r["discovery_seconds"] > discovery_allowance(r)]
    audit.eq("R.11", S, "discovery calls crossing the soft deadline / of which incomplete", (6, 6),
             (len(over), sum(bool(sep(r).get("discovery_incomplete")) for r in over)))
    audit.rounded("R.12", S, "largest discovery excess (ms)", 3.618,
                  1e3 * max(r["discovery_seconds"] - discovery_allowance(r) for r in cut_mode), 3)
    audit.rounded("R.13", S, "largest full-callback excess over the separation allowance (ms)", 29.529,
                  1e3 * max(sep(r).get("callback_seconds", 0) - discovery_allowance(r) for r in cut_mode), 3)
    audit.rounded("R.14", S, "largest total soft-budget excess, all 75 records (ms)", 23.611,
                  1e3 * max(time_b(r) - r["time_limit"] for r in recs), 3)
    crashed = [ix.get("diagnostic", "full", n, m) for n in ("chp_partload", "waterno2_06") for m in ("all", "auto")]
    audit.eq("R.15", S, "formerly crashing four: incomplete discovery and a normal SCIP status", [True] * 4,
             [bool(sep(r).get("discovery_incomplete")) and ran_scip(r) for r in crashed])

    # Replay and incumbents
    check_manifest(audit, "R.16", S, REP, 103)
    total = check_replay(audit, "R.17", S, replay, recs, True,
                         {"cuts": 42, "hashes": 103, "tamper": 14, "missing": 0, "bound_runs": 75})
    check_incumbents(audit, "R.18", S, recs, 67)
    audit.eq("R.19", S, "cuts replayed across the two current campaigns", 165, cuts_v2 + total)
    return ix


# --------------------------------------------------------------------------
# Auxiliary Report A evidence (star mechanism, native kernel benchmark)
# --------------------------------------------------------------------------

def audit_aux(audit):
    S = "A ev"
    star = load_json(EXP_A / "star-mechanism.json")
    F = Fraction

    def f(x, y, z):  # objective stated in star-mechanism.json
        return (y - F(1, 4) - x / 2) ** 2 + (y - 5 * z / 8) ** 2 + x * (1 - x) + z * (1 - z)

    left = [(F(w), F(a), F(b)) for w, (a, b) in star["left_measure"]]     # (weight, x, y)
    right = [(F(w), F(a), F(b)) for w, (a, b) in star["right_measure"]]   # (weight, y, z)
    left_obj = sum(w * ((y - F(1, 4) - x / 2) ** 2 + x * (1 - x)) for w, x, y in left)
    right_obj = sum(w * ((y - 5 * z / 8) ** 2 + z * (1 - z)) for w, y, z in right)
    lm = [sum(w * y ** k for w, _, y in left) for k in range(3)]
    rm = [sum(w * y ** k for w, y, _ in right) for k in range(3)]
    audit.eq("A.X.1", S, "pair measures: expected pair objectives (exact)", (F(0), F(0)), (left_obj, right_obj))
    audit.eq("A.X.2", S, "pair measures share center moments 1, 1/2, 5/16", ([F(1), F(1, 2), F(5, 16)],) * 2, (lm, rm))
    pieces = star["certificate"]["pieces"]
    audit.eq("A.X.3", S, "exact center partition has three pieces", 3, len(pieces))
    audit.eq("A.X.4", S, "objective at (1, 11/16, 1) and stated star minimum", (F(1, 128), F(1, 128)),
             (f(F(1), F(11, 16), F(1)), F(star["exact_star_minimum"])))
    # brute-force lower check: piece minima of the stated polynomials over their intervals
    minima = []
    for p in pieces:
        lo, hi = F(p["interval"][0]), F(p["interval"][1])
        c0, c1, c2 = (F(c) for c in p["polynomial"])
        cands = [lo, hi] + ([-c1 / (2 * c2)] if c2 > 0 and lo <= -c1 / (2 * c2) <= hi else [])
        minima.append(min(c0 + c1 * t + c2 * t * t for t in cands))
    audit.eq("A.X.5", S, "minimum over pieces of the piece polynomials", F(1, 128), min(minima))
    audit.eq("A.X.6", S, "pair-hull bound 0; replay accepted; changed objective rejected",
             ("0", True, True), (star["exact_pair_hull_bound"], star["star_certificate_replayed"],
                                 star["changed_objective_rejected"]))

    bench = load_json(EXP_A.parent / "implementation/native-kernel-benchmark.json")
    audit.eq("A.X.7", S, "native benchmark combinations", 35, len(bench["rows"]))
    audit.rounded("A.X.8", S, "native build and load seconds", 0.268, bench["build_seconds"], 3)
    rows = {(r["case"], r["points"]): r for r in bench["rows"]}
    for case, numpy_us, c_us, ratio in (("univariate_square", 5.20, 30.20, 0.17),
                                        ("bivariate_quadratic_5", 30.81, 48.46, 0.64),
                                        ("univariate_quartic", 236.94, 27.76, 8.54),
                                        ("univariate_6", 972.95, 43.51, 22.36),
                                        ("bivariate_24", 6176.34, 390.89, 15.80)):
        r = rows[(case, 4096)]
        audit.eq(f"A.X.9.{case}", S, f"4096-point timings, us and ratio ({case})", (numpy_us, c_us, ratio),
                 (round(r["numpy_seconds"] * 1e6, 2), round(r["native_seconds"] * 1e6, 2),
                  round(r["numpy_seconds"] / r["native_seconds"], 2)))
    grids = {(r["config"]["grid_1d"], r["config"]["grid_2d"]) for r in load_jsonl(V1 / "records.jsonl")
             if isinstance(r.get("config"), dict)}
    audit.true("A.X.12", S, "main separation grids (65 and 13^2 = 169 points) stay below the native threshold",
               grids == {(65, 13)} and max(65, 13 ** 2) < bench["native_minimum_points"],
               (grids, bench["native_minimum_points"]))
    q32 = rows[("univariate_quartic", 32)]
    audit.true("A.X.10", S, "single quartic at 32 points: C slower than NumPy",
               q32["native_seconds"] > q32["numpy_seconds"])
    audit.true("A.X.11", S, "low-degree rows slower in C at 4096 points; dispatch keeps NumPy",
               all(rows[(c, 4096)]["native_seconds"] > rows[(c, 4096)]["numpy_seconds"]
                   and rows[(c, 4096)]["selected_backend"] == "numpy"
                   for c in ("univariate_square", "bivariate_bilinear", "bivariate_quadratic_5")))


# --------------------------------------------------------------------------
# Paper-ready tables
# --------------------------------------------------------------------------

def g8(x):
    v = fnum(x)
    if v is None:
        return "-" if x is None else str(x)
    return f"{v:.8g}"


def t2(x):
    return "-" if x is None else f"{x:.2f}"


def md_table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    out += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(out)


def cut_instance_table(ix, modes, timef, complete_flag, label):
    groups = defaultdict(dict)
    for r in ix.records:
        groups[(r["suite"], r["phase"], r["seed"], r["name"])][r["mode"]] = r
    rows = []
    for key in sorted(groups, key=lambda k: min(int(r["run_id"].split("_")[0]) for r in groups[k].values())):
        g = groups[key]
        if not any((cut_count(r, complete_flag) or 0) > 0 for m, r in g.items() if m not in ("baseline", "control")):
            continue
        for m in modes:
            r = g.get(m)
            if r is None:
                continue
            c = cut_count(r, complete_flag)
            rows.append((label, key[0], key[1], key[2], key[3], m, r["status"], "yes" if solved(r) else "no",
                         g8(r.get("dual")), g8(r.get("root_dual")), r.get("nodes", "-"), t2(timef(r)),
                         "unknown" if c is None else c))
    return md_table(["Campaign", "Suite", "Phase", "Seed", "Instance", "Mode", "Status", "Solved",
                     "Final dual", "Root dual", "Nodes", "Time (s)", "Cuts"], rows)


def time_breakdown(ix, modes, suite_phases, campaign):
    """Sums per suite/phase/mode. Nesting: SCIP solve wall includes callback; callback includes
    direction LPs (candidate), certification and row work (and discovery in campaign-v2)."""
    rows = []
    for suite, phase in suite_phases:
        for m in modes:
            if not ix.select(suite, phase, m):
                continue
            rs = [r for r in ix.select(suite, phase, m) if "total_seconds" in r]
            s = lambda f: sum(f(r) for r in rs)
            read = s(lambda r: r.get("read_seconds", 0) + (r.get("source_read_seconds", 0) if campaign == "A"
                                                           else r.get("preparation_seconds", 0)))
            pre_disc = s(lambda r: r.get("discovery_seconds", 0)) if campaign == "A" else 0.0
            in_cb_disc = s(lambda r: sep(r).get("discovery_seconds", 0)) if campaign != "A" else 0.0
            build = s(lambda r: r.get("build_seconds", 0))
            solve = s(lambda r: r.get("solve_wall_seconds", 0))
            cb = s(lambda r: sep(r).get("callback_seconds", 0))
            cand = s(lambda r: sep(r).get("candidate_seconds", 0))
            cert = s(lambda r: sep(r).get("certification_seconds", 0))
            rowt = s(lambda r: sep(r).get("row_seconds", 0))
            scr = s(lambda r: sep(r).get("screening_seconds", 0))
            total = s(lambda r: time_a(r) if campaign == "A" else time_b(r))
            outer = sum(r["outer_wall_seconds"] for r in ix.select(suite, phase, m))
            rows.append((suite, phase, m, len(ix.select(suite, phase, m)), f"{read:.3f}",
                         f"{pre_disc:.3f}" if campaign == "A" else f"{in_cb_disc:.3f}", f"{build:.3f}",
                         f"{solve:.3f}", f"{cb:.3f}", f"{cand:.3f}", f"{cert:.3f}", f"{rowt:.3f}",
                         f"{scr:.3f}" if campaign == "A" else "n/a", f"{solve - cb:.3f}", f"{total:.3f}",
                         f"{outer:.3f}"))
    disc_label = "Discovery (pre-solve)" if campaign == "A" else "Discovery (inside callback)"
    return md_table(["Suite", "Phase", "Mode", "Runs", "Read/prep", disc_label, "Build", "SCIP solve wall",
                     "Callback", "Direction LPs", "Certification", "Row export", "Screening",
                     "SCIP excl. callback", "Integration total", "Outer wall"], rows)


def sgm(values, shift=1.0):
    return math.exp(sum(math.log(v + shift) for v in values) / len(values)) - shift


def time_summary(ix, suite, modes, timef, label):
    names = ix.names(suite, "full")
    rows = []
    base = {n: timef(ix.get(suite, "full", n, "baseline")) for n in names}
    for m in modes:
        ts = {n: timef(ix.get(suite, "full", n, m)) for n in names}
        avail = [n for n in names if ts[n] is not None and base[n] is not None]
        both = [n for n in avail if solved(ix.get(suite, "full", n, m)) and solved(ix.get(suite, "full", n, "baseline"))]
        faster = sum(ts[n] < 0.9 * base[n] for n in both)
        slower = sum(ts[n] > 1.1 * base[n] for n in both)
        rows.append((label, suite, m, len(avail), f"{sgm([ts[n] for n in avail]):.3f}", len(both),
                     f"{sgm([ts[n] for n in both]):.3f}" if both else "-", faster, slower, len(both) - faster - slower))
    return md_table(["Campaign", "Suite", "Mode", "Runs with time", "SGM time, all (s)", "Both solved",
                     "SGM time, both solved (s)", ">10% faster than baseline", ">10% slower", "Within 10%"], rows)


SYNTHETIC_DESCRIPTIONS = {
    "quartic_balance_4": "min sum_i (x_i^4 - x_i^2), sum_i x_i = 0, x in [-1,1]^4; optimum -1 (separable nonconvex quartic with a linking row)",
    "quartic_balance_8": "same as quartic_balance_4 with 8 variables; optimum -2",
    "cubic_moment": "min x^3 s.t. x^2 >= 1/4, x in [0,1]; optimum 1/8 (shared polynomial curve)",
    "exp_pair": "min e^x + e^-x s.t. e^x + e^-x >= 3, x in [-2,2]; optimum 3 (same exp expression in objective and row)",
    "log_pair": "min log x - (1/2) log(1+2x), x in [1/4,2]; optimum log(1/4) - (1/2) log(3/2) (log curve)",
    "trig_pair": "min sin x + cos x, x in [-pi,pi]; optimum -sqrt(2) (trigonometric curve)",
    "simplex_product": "min -xy on {x+y<=1} in [0,1]^2; optimum -1/4 (box McCormick gives -1/2)",
    "simplex_quadratic_vector": "min x^2 + y^2 - 4xy on {x+y<=1} in [0,1]^2; optimum -1/2 (quadratic vector on a simplex)",
    "overlapping_products": "min -y(x+z), x+y<=1, y+z<=1, [0,1]^3; optimum -1/2 (two overlapping coupled blocks)",
    "star_marginal_inconsistency": "min (y-1/4-x/2)^2 + (y-5z/8)^2 + x(1-x) + z(1-z) on [0,1]^3; optimum 1/128 at (1,11/16,1); exact pair hulls glued on shared center moments give 0",
    "affine_control": "min sum_i (i+1) x_i s.t. sum_i x_i >= 1, [0,1]^8; optimum 1 (no nonlinear structure; neutral control)",
    "convex_redundant_control": "min sum_i (x_i^2 + x_i^4), [-1,1]^8; optimum 0 (convex; unnecessary convexification, adverse control)",
    "binary_product_control": "min -x0 x1 - x2 x3, sum x_i <= 2, binary x; optimum -1 (native integer products; neutral control)",
}


def synthetic_table(ix, modes, timef, complete_flag, phase="full"):
    rows = []
    case_dir = V2 / "cases"
    for name in ix.names("synthetic", phase):
        info = load_json(case_dir / f"{name}.json")
        cells = []
        for m in modes:
            r = ix.get("synthetic", phase, name, m)
            c = cut_count(r, complete_flag)
            cells.append(f"{r['status']}{'' if solved(r) else ' (unsolved)'}; dual {g8(r.get('dual'))}; "
                         f"{t2(timef(r))} s; {('?' if c is None else c)} cuts")
        rows.append((name, info.get("stratum", ""), SYNTHETIC_DESCRIPTIONS[name], g8(float(info["known_optimum"])), *cells))
    return md_table(["Case", "Stratum (cases.py)", "Description", "Known optimum", *modes], rows)


def holdout_table_b(ix, selection):
    rows = []
    for e in selection["selected"]:
        cells = []
        for m in MODES_B:
            r = ix.get("holdout", "full", e["name"], m)
            cells.append(f"{r['status']}{'' if solved(r) else '*'} {t2(time_b(r))}s {cut_count(r, True)}c")
        rows.append((e["name"], e["stratum"], e["variables"], e["constraints"], e["bytes"],
                     "yes" if e["integer"] else "no", e["reference_primal"], *cells))
    return md_table(["Model", "Stratum", "Vars", "Cons", "OSiL bytes", "Integer", "Reference primal",
                     "baseline", "all", "auto"], rows)


def holdout_table_a(ix, selection, meta):
    rows = []
    for e in selection["selected"]:
        cells = []
        for m in MODES_A:
            r = ix.get("holdout", "full", e["name"], m)
            c = cut_count(r, False)
            st = {"source_model_mismatch": "refused", "worker_error": "error"}.get(r["status"], r["status"])
            cells.append(f"{st}{'' if solved(r) else '*'} {t2(time_a(r))}s {('?' if c is None else c)}c")
        row = meta[e["name"]]
        rows.append((e["name"], e["nvars"], e["nrows"], e["bytes"],
                     "yes" if int(row["nbinvars"]) + int(row["nintvars"]) > 0 else "no",
                     "yes" if row["convex"] == "True" else "no", e["reference_primal"], *cells))
    return md_table(["Model", "Vars", "Rows", "OSiL bytes", "Integer", "Convex", "Reference primal",
                     *MODES_A], rows)


def unsolved_table(ix, suite, names, modes, timef, references, label):
    rows = []
    for n in names:
        for m in modes:
            r = ix.get(suite, "full", n, m)
            p, d = fnum(r.get("primal")), fnum(r.get("dual"))
            gap = scip_gap(p, d)
            ref = references.get(n)
            rows.append((label, n, m, r["status"], g8(p), g8(d),
                         "-" if p is None or d is None else g8(abs(p - d)),
                         "-" if gap is None else ("inf" if gap == math.inf else f"{100 * gap:.2f}%"),
                         ref if ref is not None else "-", r.get("nodes", "-"), t2(timef(r)),
                         cut_count(r, label != "v1")))
    return md_table(["Campaign", "Model", "Mode", "Status", "Primal", "Dual", "Abs gap", "SCIP rel. gap",
                     "Archived reference", "Nodes", "Time (s)", "Cuts"], rows)


def comparison_table(ix, label, specs):
    rows = []
    for suite, phase, mode, field, baseline in specs:
        if not ix.select(suite, phase, mode):
            continue
        b, t, w, u = btwu(ix.compare(suite, phase, mode, field=field, baseline=baseline)[0])
        rows.append((label, suite, phase, f"{mode} vs {baseline}", field, b, t, w, u))
    return md_table(["Campaign", "Suite", "Phase", "Comparison", "Bound", "Better", "Tie", "Worse", "Unavailable"], rows)


def tolerance_table(specs):
    rows = []
    for label, ix, suite, phase, mode in specs:
        cells = []
        for tol in (1e-9, 1e-6, 1e-4, 1e-3, 1e-2):
            b, t, w, u = btwu(ix.compare(suite, phase, mode, tol_rel=tol)[0])
            cells.append(f"{b}/{t}/{w}" + (f" (+{u} n/a)" if u else ""))
        rows.append((label, suite, phase, mode, *cells))
    return md_table(["Campaign", "Suite", "Phase", "Mode vs baseline", "tol 1e-9", "tol 1e-6 (stated)",
                     "tol 1e-4", "tol 1e-3", "tol 1e-2"], rows)


def worse_names_table(specs, tol_rel=1e-4):
    rows = []
    for label, ix, suite, phase, mode in specs:
        outcomes = ix.compare(suite, phase, mode, tol_rel=tol_rel)[1]
        for kind in ("better", "worse"):
            names = [n for n, o in outcomes.items() if o == kind]
            if names:
                rows.append((label, suite, phase, mode, kind, ", ".join(names)))
    return md_table(["Campaign", "Suite", "Phase", "Mode vs baseline", f"Outcome at tol {tol_rel:g}", "Models"], rows)


def rerun_table(pairs):
    """A/A comparison: same native baseline configuration run twice (identical model and seed,
    or a different seed). Reports bound outcomes at the stated tolerance and time ratios."""
    rows = []
    for label, first, second, timef in pairs:
        counts = Counter()
        ratios = []
        status_changes = 0
        for a, b in zip(first, second):
            counts[compare_bounds(b, a)] += 1
            ta, tb = timef(a), timef(b)
            if ta and tb and solved(a) and solved(b):
                ratios.append(tb / ta)
            status_changes += a["status"] != b["status"]
        ratios.sort()
        rows.append((label, len(first), *btwu(counts)[:3], status_changes, len(ratios),
                     f"{ratios[0]:.2f}" if ratios else "-", f"{ratios[len(ratios) // 2]:.2f}" if ratios else "-",
                     f"{ratios[-1]:.2f}" if ratios else "-"))
    return md_table(["Rerun pair", "Pairs", "Better", "Tie", "Worse", "Status changes", "Both solved",
                     "Min time ratio", "Median time ratio", "Max time ratio"], rows)


def hardness_table(specs):
    rows = []
    bins = ((0, 0.1), (0.1, 1), (1, 5), (5, math.inf))
    for label, ix, suite, timef, mode in specs:
        rs = ix.select(suite, "full", mode)
        cells = [sum(solved(r) and lo <= timef(r) < hi for r in rs) for lo, hi in bins]
        rows.append((label, suite, mode, len(rs), *cells, sum(not solved(r) for r in rs)))
    return md_table(["Campaign", "Suite", "Mode", "Models", "Solved < 0.1 s", "0.1-1 s", "1-5 s", ">= 5 s",
                     "Unsolved or not admitted"], rows)


def overrun_table(ix_b):
    """Primary campaign-v2: discovery time beyond the configured allowance (the defect repaired
    later), and integration overhead versus baseline inside and outside the repair groups."""
    plan = load_json(EXP_B / "repair-plan.json")
    groups = {(g["name"], g["phase"], g["seed"]) for g in plan["groups"]}
    rows = []
    for suite, phase in (("holdout", "full"), ("holdout", "root"), ("holdout", "repeat"), ("diagnostic", "full"),
                         ("synthetic", "full"), ("synthetic", "root")):
        for m in ("all", "auto"):
            rs = [r for r in ix_b.select(suite, phase, m) if isinstance(r.get("config"), dict)]
            if not rs:
                continue
            over = [r for r in rs if r["discovery_seconds"] > discovery_allowance(r)]
            excess = sum(r["discovery_seconds"] - discovery_allowance(r) for r in over)
            inside, outside = [0.0, 0.0], [0.0, 0.0]
            for r in rs:
                b = ix_b.get(suite, phase, r["name"], "baseline")
                if time_b(b) is None:
                    continue
                target = inside if (r["name"], r["phase"], r["seed"]) in groups else outside
                target[0] += time_b(r)
                target[1] += time_b(b)
            rows.append((suite, phase, m, len(rs), len(over), f"{sum(r['discovery_seconds'] for r in rs):.2f}",
                         f"{excess:.2f}", f"{inside[0]:.2f} vs {inside[1]:.2f}", f"{outside[0]:.2f} vs {outside[1]:.2f}"))
    return md_table(["Suite", "Phase", "Mode", "Runs with record", "Discovery over allowance", "Discovery s",
                     "Excess over allowance s", "Mode vs baseline s (repair groups)",
                     "Mode vs baseline s (other groups)"], rows)


def solved_table(ix, label, specs, modes, admittedf, complete_flag, timef):
    rows = []
    for suite, phase in specs:
        for m in modes:
            rs = ix.select(suite, phase, m)
            if not rs:
                continue
            rows.append((label, suite, phase, m, len(rs), sum(map(admittedf, rs)), sum(map(solved, rs)),
                         dict(sorted(Counter(r["status"] for r in rs).items())),
                         sum(cut_count(r, complete_flag) or 0 for r in rs),
                         sum((cut_count(r, complete_flag) or 0) > 0 for r in rs),
                         sum(cut_count(r, complete_flag) is None for r in rs),
                         f"{sum(t for t in map(timef, rs) if t is not None):.2f}",
                         f"{sum(r['outer_wall_seconds'] for r in rs):.2f}"))
    return md_table(["Campaign", "Suite", "Phase", "Mode", "Runs", "Admitted", "Solved", "Statuses", "Cuts",
                     "Runs with cuts", "Unknown cut logs", "Integration s", "Outer s"], rows)


def overshoot_table(recs, timef, label):
    rows = [(label, r["run_id"], r["time_limit"], f"{timef(r):.4f}", f"{timef(r) - r['time_limit']:.4f}")
            for r in recs if timef(r) is not None and timef(r) > r["time_limit"] + 0.01]
    return md_table(["Campaign", "Run", "Soft budget (s)", "Integration (s)", "Excess (s)"], rows) if rows else "none"


def repair_pairs_table(ix_rep, ix_v2):
    rows = []
    for r in ix_rep.records:
        o = ix_v2.get(r["suite"], r["phase"], r["name"], r["mode"])
        rows.append((r["phase"], r["suite"], r["name"], r["mode"],
                     f"{o['status']} / {r['status']}", f"{g8(o.get('dual'))} / {g8(r.get('dual'))}",
                     f"{t2(time_b(o))} / {t2(time_b(r))}",
                     f"{g8(o.get('discovery_seconds'))} / {g8(r.get('discovery_seconds'))}",
                     f"{cut_count(o, True)} / {cut_count(r, True)}",
                     bool(sep(r).get("discovery_incomplete"))))
    return md_table(["Phase", "Suite", "Model", "Mode", "Status orig/repair", "Dual orig/repair",
                     "Time orig/repair (s)", "Discovery orig/repair (s)", "Cuts orig/repair", "Repair discovery incomplete"],
                    rows)


def tables(ix_a, ix_b, ix_r, meta):
    sel_a = load_json(EXP_A / "holdout-selection.json")
    sel_b = load_json(EXP_B / "holdout-selection.json")
    out = []
    out += ["### (a) Every instance where a cut mode added at least one cut", "",
            "Time is integration time (v1: total+source read; v2/repair: total+preparation). "
            "'unknown' = no complete cut log.", "",
            cut_instance_table(ix_b, MODES_B, time_b, True, "v2"), "",
            cut_instance_table(ix_r, MODES_B, time_b, True, "repair"), "",
            cut_instance_table(ix_a, MODES_A, time_a, False, "v1"), ""]
    out += ["### (b) Time breakdown (seconds, sums over runs)", "",
            "Nesting: SCIP solve wall contains the callback; the callback contains direction LPs, certification, "
            "row export (and, in v2/repair, discovery). 'SCIP excl. callback' = solve wall - callback.", "",
            "Campaign-v2:", "",
            time_breakdown(ix_b, MODES_B, [("holdout", "full"), ("diagnostic", "full"), ("synthetic", "full"),
                                           ("holdout", "root"), ("synthetic", "root"), ("holdout", "repeat")], "B"), "",
            "Repair cohort:", "",
            time_breakdown(ix_r, MODES_B, [("holdout", "full"), ("diagnostic", "full"), ("holdout", "root"),
                                           ("holdout", "repeat")], "B"), "",
            "Campaign-v1:", "",
            time_breakdown(ix_a, MODES_A, [("holdout", "full"), ("historical", "full"), ("synthetic", "full"),
                                           ("holdout", "root"), ("synthetic", "root"), ("holdout", "repeat"),
                                           ("synthetic", "repeat"), ("synthetic", "no_cache"),
                                           ("synthetic", "pairs_only")], "A"), "",
            "Shifted geometric means (shift 1 s) of integration time; paired time ratios on commonly solved models:", "",
            time_summary(ix_b, "holdout", MODES_B, time_b, "v2"), "",
            time_summary(ix_a, "holdout", MODES_A, time_a, "v1"), ""]
    out += ["### (c) The 30 campaign-v2 holdout models (full runs, seed 0)", "",
            "Cell = status, '*' if not numerically solved, integration seconds, recorded cuts. Hash order.", "",
            holdout_table_b(ix_b, sel_b), ""]
    unsolved_b = [e["name"] for e in sel_b["selected"] if not solved(ix_b.get("holdout", "full", e["name"], "baseline"))]
    refs_b = {e["name"]: f"{e['reference_primal']} / {e['reference_dual']}" for e in sel_b["selected"]}
    out += ["### (d) The five unsolved campaign-v2 holdout models: bounds and gaps", "",
            "Archived reference = MINLPLib primal / dual bound. SCIP rel. gap = |p-d|/min(|p|,|d|).", "",
            unsolved_table(ix_b, "holdout", unsolved_b, MODES_B, time_b, refs_b, "v2"), ""]
    out += ["### (e) The 13 synthetic mechanism cases (campaign-v2 full runs, 10 s)", "",
            synthetic_table(ix_b, MODES_B, time_b, True), "",
            "Campaign-v2 root-only mechanism runs (5 s, one node):", "",
            synthetic_table(ix_b, MODES_B, time_b, True, phase="root"), ""]
    out += ["### Campaign-v2: solved counts and paired comparisons by phase", "",
            solved_table(ix_b, "v2", [("holdout", "full"), ("diagnostic", "full"), ("synthetic", "full"),
                                      ("holdout", "root"), ("synthetic", "root"), ("holdout", "repeat")],
                         MODES_B, admitted_b, True, time_b), "",
            comparison_table(ix_b, "v2", [(s, p, m, f, "baseline") for s, p in
                                          [("holdout", "full"), ("diagnostic", "full"), ("synthetic", "full"),
                                           ("holdout", "root"), ("synthetic", "root"), ("holdout", "repeat")]
                                          for m in ("all", "auto") for f in ("dual",)] +
                             [("holdout", "full", m, "root_dual", "baseline") for m in ("all", "auto")]), "",
            "Sensitivity of better/tie/worse counts to the relative comparison tolerance:", "",
            tolerance_table([("v2", ix_b, "holdout", "full", m) for m in ("all", "auto")] +
                            [("v2", ix_b, "holdout", "root", m) for m in ("all", "auto")] +
                            [("repair", ix_r, "holdout", "full", m) for m in ("all", "auto")] +
                            [("v1", ix_a, "holdout", "full", m) for m in ("control", "all", "auto")] +
                            [("v1", ix_a, "holdout", "root", m) for m in ("control", "all", "auto")]), "",
            "Models behind the better/worse outcomes at the stated tolerance 1e-6:", "",
            worse_names_table([("v2", ix_b, "holdout", "full", m) for m in ("all", "auto")] +
                              [("v2", ix_b, "holdout", "root", m) for m in ("all", "auto")] +
                              [("repair", ix_r, "holdout", "full", m) for m in ("all", "auto")] +
                              [("v1", ix_a, "holdout", "full", m) for m in ("control", "all", "auto")],
                              tol_rel=1e-6), "",
            "Models behind the better/worse outcomes that survive a tolerance equal to the 1e-4 gap limit:", "",
            worse_names_table([("v2", ix_b, "holdout", "full", m) for m in ("all", "auto")] +
                              [("v2", ix_b, "holdout", "root", m) for m in ("all", "auto")] +
                              [("repair", ix_r, "holdout", "full", m) for m in ("all", "auto")] +
                              [("v1", ix_a, "holdout", "full", m) for m in ("control", "all", "auto")] +
                              [("v1", ix_a, "holdout", "root", m) for m in ("control", "all", "auto")]), "",
            "Baseline A/A reruns (native SCIP only; quantifies run-to-run and seed variation on the shared host):", "",
            rerun_table([("v2 baseline -> repair baseline, same seed and model (25 groups)",
                          [ix_b.get(r["suite"], r["phase"], r["name"], "baseline") for r in ix_r.select(mode="baseline")],
                          ix_r.select(mode="baseline"), time_b),
                         ("v2 baseline seed 0 -> seed 1 (6 holdout models)",
                          [ix_b.get("holdout", "full", n, "baseline") for n in ix_b.names("holdout", "repeat")],
                          ix_b.select("holdout", "repeat", "baseline"), time_b),
                         ("v1 baseline seed 0 -> seed 1 (6 models)",
                          [ix_a.get(r["suite"], "full", r["name"], "baseline") for r in ix_a.select(phase="repeat", mode="baseline")],
                          ix_a.select(phase="repeat", mode="baseline"), time_a)]), "",
            "Hardness profile of the application populations (integration time of solved runs):", "",
            hardness_table([("v2", ix_b, "holdout", time_b, m) for m in MODES_B] +
                           [("v1", ix_a, "holdout", time_a, m) for m in MODES_A]), "",
            "Primary campaign-v2 discovery overruns (allowance = min(max_separation_seconds, "
            "separation_budget_fraction * (time limit - preparation))) and where the cut-mode overhead arises:", "",
            overrun_table(ix_b), "",
            "Seed-one repeats (campaign-v2):", "",
            md_table(["Model", "Mode", "Seed-0 status / time (s) / cuts", "Seed-1 status / time (s) / cuts"],
                     [(n, m, f"{ix_b.get('holdout', 'full', n, m)['status']} / {t2(time_b(ix_b.get('holdout', 'full', n, m)))} / "
                             f"{cut_count(ix_b.get('holdout', 'full', n, m), True)}",
                       f"{ix_b.get('holdout', 'repeat', n, m)['status']} / {t2(time_b(ix_b.get('holdout', 'repeat', n, m)))} / "
                       f"{cut_count(ix_b.get('holdout', 'repeat', n, m), True)}")
                      for n in ix_b.names("holdout", "repeat") for m in MODES_B]), "",
            "Soft-budget overshoots > 0.01 s (campaign-v2):", "",
            overshoot_table(ix_b.records, time_b, "v2"), ""]
    out += ["### Repair cohort: original versus repaired run, per job", "",
            repair_pairs_table(ix_r, ix_b), "",
            comparison_table(ix_r, "repair", [(s, p, m, "dual", "baseline") for s, p in
                                              [("holdout", "full"), ("diagnostic", "full"), ("holdout", "root"),
                                               ("holdout", "repeat")] for m in ("all", "auto")]), ""]
    unsolved_a = [n for n in ix_a.names("holdout", "full")
                  if admitted_a(ix_a.get("holdout", "full", n, "baseline"))
                  and not all(solved(ix_a.get("holdout", "full", n, m)) for m in MODES_A)]
    refs_a = {e["name"]: f"{e['reference_primal']} / {e['reference_dual']}" for e in sel_a["selected"]}
    out += ["### (f) Campaign-v1 (Report A) analogue", "",
            solved_table(ix_a, "v1", [("synthetic", "full"), ("holdout", "full"), ("historical", "full"),
                                      ("holdout", "root"), ("synthetic", "root"), ("holdout", "repeat"),
                                      ("synthetic", "repeat"), ("synthetic", "no_cache"), ("synthetic", "pairs_only")],
                         MODES_A, admitted_a, False, time_a), "",
            comparison_table(ix_a, "v1", [(s, p, m, "dual", "baseline") for s, p in
                                          [("synthetic", "full"), ("holdout", "full"), ("historical", "full"),
                                           ("holdout", "root"), ("synthetic", "root"), ("holdout", "repeat"),
                                           ("synthetic", "repeat")] for m in ("control", "all", "auto")] +
                             [(s, "full", m, "dual", "control") for s in ("synthetic", "holdout")
                              for m in ("all", "auto")] +
                             [("holdout", "full", m, "root_dual", "baseline") for m in ("control", "all", "auto")]), "",
            "The 24 campaign-v1 held-out models (full runs, 6 s); cell = status ('*' unsolved), seconds, cuts:", "",
            holdout_table_a(ix_a, sel_a, meta), "",
            "Campaign-v1 admitted held-out models not solved in every mode:", "",
            unsolved_table(ix_a, "holdout", unsolved_a, MODES_A, time_a, refs_a, "v1"), "",
            "Campaign-v1 synthetic cases (full runs, 6 s):", "",
            synthetic_table(ix_a, MODES_A, time_a, False), "",
            "Soft-budget overshoots > 0.01 s (campaign-v1):", "",
            overshoot_table(ix_a.records, time_a, "v1"), ""]
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--tables", action="store_true", help="also print paper-ready markdown tables")
    args = parser.parse_args()
    meta = metadata_rows()
    recs_a, recs_b, recs_r = load_jsonl(V1 / "records.jsonl"), load_jsonl(V2 / "records.jsonl"), \
        load_jsonl(REP / "records.jsonl")
    audit = Audit()
    ix_a = audit_a(audit, recs_a, meta)
    audit_aux(audit)
    ix_b, cuts_b = audit_b(audit, recs_b, meta, ix_a, recs_a)
    ix_r = audit_repair(audit, recs_r, ix_b, recs_b, cuts_b)
    print("## Claim-by-claim recomputation\n")
    print("Inputs (SHA256):")
    for path in (V1 / "records.jsonl", V2 / "records.jsonl", REP / "records.jsonl"):
        print(f"- `{path.relative_to(ROOT)}` {sha256_file(path)}")
    print()
    print(audit.report())
    if args.tables:
        print("\n## Paper-ready tables\n")
        print(tables(ix_a, ix_b, ix_r, meta))
    return 1 if audit.mismatches() else 0


if __name__ == "__main__":
    sys.exit(main())
