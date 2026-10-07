"""Independent, read-only reconstruction of the v2 experiment contracts.

This script never invokes an optimizer. It intentionally does not import the
campaign selector, orchestrator, summary, or incumbent checker. The legacy
parser is used only for the syntax filter expressly required by the protocol;
variable bounds/counts are independently read from XML.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import statistics
import sys
import xml.etree.ElementTree as ET

TOPIC = Path(__file__).resolve().parents[1]
REPO = TOPIC.parent
MODES = ("baseline", "all", "auto")
DIAGNOSTICS = ("genpooling_lee2", "syn15m", "cvxnonsep_psig30r", "cvxnonsep_pcon40r",
               "syn10hfsg", "btest14", "ghg_2veh", "chp_partload", "kall_circles_c6b", "waterno2_06")
SYNTHETIC = ("quartic_balance_4", "quartic_balance_8", "cubic_moment", "exp_pair", "log_pair",
             "trig_pair", "simplex_product", "simplex_quadratic_vector", "overlapping_products",
             "star_marginal_inconsistency", "affine_control", "convex_redundant_control",
             "binary_product_control")
ROOT_MECHANISMS = ("quartic_balance_8", "exp_pair", "simplex_quadratic_vector",
                   "overlapping_products", "star_marginal_inconsistency")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def audit_selection():
    """Rebuild the entire eligibility set; do not overwrite the frozen selector."""
    selection_path = TOPIC / "experiments/holdout-selection.json"
    frozen = read(selection_path)
    previous = REPO / "research-20261002-convexification/experiments"
    old = read(previous / "holdout-selection.json")
    excluded = set(old["excluded_names"])
    excluded |= {p.stem for p in (previous / "campaign-v1/cases").glob("*.json")}
    excluded |= {row["name"] for row in old["selected"]}
    errors = []
    if sorted(excluded) != frozen["excluded_names"]:
        errors.append("Exclusion set differs from the named earlier campaigns")
    metadata_path = REPO / "code/minlp_solver_lab/instances/instancedata.csv"
    with metadata_path.open() as stream:
        metadata = {r["name"]: r for r in csv.DictReader(stream, delimiter=";")}
    sys.path.insert(0, str(REPO / "code/univariate_envelopes"))
    from uenv.osil import read_osil
    parser_errors, eligible = [], []
    ns = "{os.optimizationservices.org}"
    for path in sorted((Path.home() / ".cache/minlplib/minlplib/osil").glob("*.osil")):
        name, row = path.stem, metadata.get(path.stem)
        if name in excluded or row is None or path.stat().st_size > 250000:
            continue
        if int(row["nvars"]) > 120 or int(row["ncons"]) > 180:
            continue
        if not any(int(row[k]) for k in ("ngennlfunc", "nquadfunc", "npolynomfunc")):
            continue
        try:
            read_osil(str(path))  # The frozen protocol expressly requires this syntax filter.
        except Exception as exc:
            parser_errors.append({"name": name, "type": type(exc).__name__, "reason": str(exc)})
            continue
        data = ET.parse(path).getroot().find(ns + "instanceData")
        variables = list(data.find(ns + "variables"))
        constraints = data.find(ns + "constraints")
        pairs = [(float(v.get("lb", "0")), float(v.get("ub", "1" if v.get("type") == "B" else "inf")))
                 for v in variables]
        finite = sum(math.isfinite(a) and math.isfinite(b) and a < b for a, b in pairs)
        if finite < 2:
            continue
        convex = row["convex"] == "True"
        integer = int(row["nbinvars"]) + int(row["nintvars"]) > 0
        eligible.append({"name": name,
                         "stratum": "convex" if convex else "nonconvex_integer" if integer else "nonconvex_continuous",
                         "rank": hashlib.sha256(("convexification-holdout-v2:" + name).encode()).hexdigest(),
                         "variables": len(variables), "constraints": len(constraints) if constraints is not None else 0,
                         "finite_nonfixed_variables": finite, "integer": integer, "convex": convex,
                         "bytes": path.stat().st_size, "sha256": sha(path),
                         "reference_primal": row["primalbound"], "reference_dual": row["dualbound"]})
    eligible.sort(key=lambda r: r["rank"])
    selected, used = [], Counter()
    for row in eligible:
        if used[row["stratum"]] < 10:
            selected.append(row)
            used[row["stratum"]] += 1
    comparisons = {
        "eligible_count": len(eligible),
        "stratum_eligible_counts": dict(Counter(r["stratum"] for r in eligible)),
        "eligible_names_in_rank_order": [r["name"] for r in eligible],
        "parser_errors": parser_errors,
        "selected": selected,
    }
    for key, actual in comparisons.items():
        if frozen[key] != actual:
            errors.append(f"Independently reconstructed {key} differs")
    return {"passed": not errors, "errors": errors, "excluded": len(excluded),
            "eligible": len(eligible), "stratum_counts": comparisons["stratum_eligible_counts"],
            "selected": [r["name"] for r in selected], "parser_errors": len(parser_errors),
            "selection_sha256": sha(selection_path), "metadata_sha256": sha(metadata_path)}


def expected_jobs(selected):
    jobs = []
    phases = (("full", "holdout", selected, 30.0, 45.0),
              ("full", "diagnostic", DIAGNOSTICS, 30.0, 45.0),
              ("full", "synthetic", SYNTHETIC, 10.0, 20.0),
              ("root", None, [*selected, *ROOT_MECHANISMS], 5.0, 15.0),
              ("repeat", "holdout", selected[:6], 30.0, 45.0))
    for phase, suite, names, soft, hard in phases:
        for i, name in enumerate(names):
            for shift in range(3):
                mode = MODES[(i + shift) % 3]
                jobs.append({"name": name, "phase": phase, "suite": suite or ("holdout" if name in selected else "synthetic"),
                             "mode": mode, "time_limit": soft, "worker_timeout": hard,
                             "node_limit": 1 if phase == "root" else None, "seed": 1 if phase == "repeat" else 0})
    return jobs


def decode(value):
    if isinstance(value, dict):
        if set(value) == {"binary64"}:
            return float.fromhex(value["binary64"])
        return {k: decode(v) for k, v in value.items()}
    if isinstance(value, list):
        return [decode(v) for v in value]
    return value


def tree_value(tree, x):
    """Use exact binary rational arithmetic until a transcendental is needed."""
    op = tree[0]
    if op == "num":
        return Fraction(tree[1])
    if op == "var":
        return Fraction(x[tree[1]])
    a = [tree_value(child, x) for child in tree[1:]]
    if op == "sum":
        return sum(a)
    if op == "times":
        return math.prod(a)
    if op == "negate":
        return -a[0]
    if op == "divide":
        return a[0] / a[1]
    if op == "square":
        return a[0] * a[0]
    if op == "power":
        exponent = a[1]
        if exponent == int(exponent):
            return a[0] ** int(exponent)
        return float(a[0]) ** float(exponent)
    return {"log": math.log, "exp": math.exp, "sin": math.sin, "cos": math.cos,
            "sqrt": math.sqrt, "abs": abs}[op](a[0])


def independent_primal(model, values, objective, tolerance=1e-5):
    if values is None:
        return {"checked": False}
    if len(values) != len(model["var_lb"]) or not all(math.isfinite(v) for v in values):
        return {"checked": True, "passed": False, "reason": "invalid value vector"}
    violations = []
    for i, (x, lo, hi, kind) in enumerate(zip(values, model["var_lb"], model["var_ub"], model["var_type"])):
        if kind == "B":
            lo, hi = max(0, lo), min(1, hi)
        if math.isfinite(lo):
            violations.append(max(0, lo - x) / max(1, abs(lo)))
        if math.isfinite(hi):
            violations.append(max(0, x - hi) / max(1, abs(hi)))
        if kind in ("B", "I"):
            violations.append(abs(x - round(x)))
    row_values = []
    try:
        for i, row in enumerate(model["rows"]):
            terms = [Fraction(c) * Fraction(values[int(j)]) for j, c in row["lin"].items()]
            terms += [Fraction(c) * Fraction(values[j]) * Fraction(values[k]) for j, k, c in row["quad"]]
            if row["nl"] is not None:
                terms.append(tree_value(row["nl"], values))
            y = float(sum(terms))
            magnitude = float(sum(abs(t) for t in terms))
            if not math.isfinite(y) or not math.isfinite(magnitude):
                raise ValueError("Nonfinite original expression")
            row_values.append(y)
            if i:
                for bound, residual in ((row["lb"], row["lb"] - y), (row["ub"], y - row["ub"])):
                    if math.isfinite(bound):
                        violations.append(max(0, residual) / max(1, magnitude, abs(bound)))
        actual = row_values[0] + model["obj_const"]
        if objective is None or not math.isfinite(objective):
            raise ValueError("Missing or nonfinite returned objective")
        discrepancy = abs(actual - objective) / max(1, abs(actual))
    except (ArithmeticError, ValueError, TypeError, KeyError) as exc:
        return {"checked": True, "passed": False, "reason": str(exc)}
    worst = max(violations, default=0)
    return {"checked": True, "passed": worst <= tolerance and discrepancy <= tolerance,
            "max_scaled_violation": worst, "relative_objective_discrepancy": discrepancy}


def trusted_record(record):
    """Explicit record gates, written independently of summarize.good."""
    checks = record.get("primal_check")
    if not isinstance(checks, dict) or "checked" not in checks:
        return False
    if checks["checked"] and checks.get("passed") is not True:
        return False
    if not checks["checked"] and record.get("primal") is not None:
        return False
    if record.get("returncode", 0) or record.get("worker_status"):
        return False
    if record.get("status") not in {"optimal", "gaplimit", "timelimit", "nodelimit", "stallnodelimit", "totalnodelimit",
                                   "infeasible", "unbounded", "inforunbd", "userinterrupt", "memlimit", "sollimit",
                                   "bestsollimit", "restartlimit"}:
        return False
    reference = record.get("reference_check")
    if not isinstance(reference, dict) or reference.get("checked") not in (True, False):
        return False
    return not reference["checked"] or (reference.get("dual_consistent") is True and reference.get("root_dual_consistent") is True)


def is_solved(record):
    return (trusted_record(record) and record.get("status") in ("optimal", "gaplimit")
            and record.get("primal_check", {}).get("checked") is True
            and record.get("primal_check", {}).get("passed") is True
            and isinstance(record.get("primal"), (int, float)) and math.isfinite(record["primal"]))


def audit_campaign(directory, planned_jobs=None):
    errors, warnings = [], []
    snapshot = directory / "snapshot"
    manifest = read(directory / "source-manifest.json")
    for relative, expected in manifest.items():
        path = snapshot / relative
        if not path.is_file() or sha(path) != expected:
            errors.append(f"Frozen source hash mismatch: {relative}")
    selection = read(snapshot / TOPIC.name / "experiments/holdout-selection.json")
    names = [r["name"] for r in selection["selected"]]
    jobs = expected_jobs(names) if planned_jobs is None else planned_jobs
    if read(directory / "jobs.json") != jobs:
        errors.append("Job schedule differs from independent reconstruction")
    records = [json.loads(line) for line in (directory / "records.jsonl").read_text().splitlines()]
    if len(records) != len(jobs):
        errors.append(f"Expected {len(jobs)} records; found {len(records)}")
    missing_logs, primal_checked, primal_failures, ref_conflicts = [], 0, [], []
    observed, case_model_hashes = {}, {}
    for descriptor in (directory / "cases").glob("*.json"):
        case = read(descriptor)
        archived_descriptor = snapshot / "frozen-cases" / descriptor.name
        if not archived_descriptor.is_file() or descriptor.read_bytes() != archived_descriptor.read_bytes():
            errors.append(f"Active case descriptor differs from snapshot: {descriptor.name}")
        if "path" in case:
            original = snapshot / "original-osil" / (case["name"] + ".osil")
            if not original.is_file() or sha(original) != case["source_sha256"]:
                errors.append(f"Original OSiL hash differs from case: {case['name']}")
    for index, record in enumerate(records):
        if index >= len(jobs):
            break
        job = jobs[index]
        ident = f"{index:03d}_{job['name']}__{job['mode']}__{job['phase']}"
        if record.get("run_id") != ident or any(record.get(k) != v for k, v in job.items()):
            errors.append(f"Job/record mismatch: {ident}")
        if read(directory / "runs" / (ident + ".json")) != record:
            errors.append(f"JSONL and per-run record differ: {ident}")
        key = (job["suite"], job["phase"], job["name"], job["mode"])
        if key in observed:
            errors.append(f"Duplicate experiment key: {key}")
        observed[key] = record
        if not isinstance(record.get("cuts"), list) or record.get("cut_log_complete") is not True:
            missing_logs.append(ident)
        model = record.get("original_model")
        if model is not None:
            actual_hash = hashlib.sha256(json.dumps(model, sort_keys=True).encode()).hexdigest()
            if record.get("model_sha256") != actual_hash:
                errors.append(f"Original-model hash mismatch: {ident}")
            previous_hash = case_model_hashes.setdefault(job["name"], actual_hash)
            if actual_hash != previous_hash:
                errors.append(f"Modes or phases used different original parsed model: {ident}")
            check = independent_primal(decode(model), record.get("original_values"), record.get("primal"))
            if check["checked"]:
                primal_checked += 1
                if not check.get("passed"):
                    primal_failures.append({"run_id": ident, **check})
            declared = record.get("primal_check", {})
            if declared.get("checked", False) != check["checked"] or (check["checked"] and declared.get("passed") != check.get("passed")):
                errors.append(f"Independent primal-check disagreement: {ident}")
        case = read(directory / "cases" / (job["name"] + ".json"))
        reference = case.get("known_optimum")
        if reference is None:
            reference = case.get("reference_primal")
        try:
            reference = float(reference)
        except (ValueError, TypeError):
            reference = math.nan
        if model is not None and math.isfinite(reference):
            tolerance = 1e-5 * max(1, abs(reference))
            for bound_name in ("dual", "root_dual"):
                bound = record.get(bound_name)
                valid = bound is None or (bound <= reference + tolerance if model["obj_sense"] == "min" else bound >= reference - tolerance)
                if not valid:
                    ref_conflicts.append({"run_id": ident, "bound": bound_name, "value": bound, "reference": reference})
                flag = "dual_consistent" if bound_name == "dual" else "root_dual_consistent"
                if record.get("reference_check", {}).get(flag) is not valid:
                    errors.append(f"Missing or incorrect reference flag: {ident}:{bound_name}")
    metrics = {}
    for suite in ("holdout", "diagnostic", "synthetic"):
        for phase in ("full", "root", "repeat"):
            rows = [r for r in records if r["suite"] == suite and r["phase"] == phase]
            if not rows:
                continue
            summary = {mode: {"records": sum(r["mode"] == mode for r in rows),
                              "solved": sum(is_solved(r) for r in rows if r["mode"] == mode)} for mode in MODES}
            comparisons = {}
            for mode in ("all", "auto"):
                counts, ratios = Counter(), []
                for name in sorted({r["name"] for r in rows}):
                    a, b = (observed[(suite, phase, name, m)] for m in (mode, "baseline"))
                    da, db = a.get("dual"), b.get("dual")
                    finite = all(isinstance(v, (int, float)) and math.isfinite(v) for v in (da, db))
                    if not trusted_record(a) or not trusted_record(b) or not finite:
                        counts["unavailable_or_flagged"] += 1
                    else:
                        improvement = (da - db) * (1 if a["sense"] == "min" else -1)
                        tolerance = 1e-6 * max(1, abs(da), abs(db))
                        counts["better" if improvement > tolerance else "worse" if improvement < -tolerance else "tie"] += 1
                    if is_solved(a) and is_solved(b):
                        ratios.append((a["total_seconds"] + a.get("preparation_seconds", 0)) /
                                      max(1e-12, b["total_seconds"] + b.get("preparation_seconds", 0)))
                comparisons[mode] = {"outcomes": dict(counts), "both_solved_count": len(ratios),
                                     "both_solved_median_runtime_ratio": statistics.median(ratios) if ratios else None}
            metrics[suite + "/" + phase] = {"modes": summary, "comparisons": comparisons}
    if (directory / "summary.json").exists():
        producer = read(directory / "summary.json")
        if producer["total_records"] != len(records):
            errors.append("Producer summary record count differs")
        for key, metric in metrics.items():
            suite, phase = key.split("/")
            parent = producer["suites"][suite]
            if phase == "full":
                for mode, counts in metric["modes"].items():
                    if parent["modes"][mode]["solved"] != counts["solved"] or parent["modes"][mode]["instances"] != counts["records"]:
                        errors.append(f"Producer solved denominator differs: {key}/{mode}")
            for comparison in parent[phase + "_comparisons"]:
                for field, actual in metric["comparisons"][comparison["mode"]].items():
                    if comparison[field] != actual:
                        errors.append(f"Producer paired metric differs: {key}/{comparison['mode']}/{field}")
    completion = read(directory / "completion.json")
    if (completion["scheduled"] != len(jobs)
            or ("counts" in completion and completion["counts"] != dict(Counter(r["status"] for r in records)))
            or ("completed" in completion and completion["completed"] != len(records))):
        errors.append("Completion table does not match all records")
    return {"passed": not errors, "errors": errors, "warnings": warnings,
            "source_files_checked": len(manifest), "scheduled": len(jobs), "records": len(records),
            "status_counts": dict(Counter(r["status"] for r in records)),
            "unknown_or_incomplete_cut_logs": missing_logs, "primal_checked": primal_checked,
            "independent_primal_failures": primal_failures, "reference_conflicts": ref_conflicts,
            "recorded_cuts": sum(len(r.get("cuts") or []) for r in records), "metrics": metrics}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign", type=Path)
    parser.add_argument("--repair-plan", type=Path,
                        help="Previously independently checked matched supplement plan")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = {"selection": audit_selection()}
    jobs = expected_jobs(result["selection"]["selected"])
    result["planned_jobs"] = {"count": len(jobs), "soft_seconds": sum(j["time_limit"] for j in jobs),
                              "hard_seconds": sum(j["worker_timeout"] for j in jobs),
                              "groups": dict(Counter(j["suite"] + "/" + j["phase"] for j in jobs))}
    if args.campaign is not None:
        planned = read(args.repair_plan)["jobs"] if args.repair_plan else None
        result["campaign"] = audit_campaign(args.campaign, planned)
    result["passed"] = all(v.get("passed", True) for v in result.values() if isinstance(v, dict))
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"passed": result["passed"], "output": str(args.output),
                      "primary_planned_jobs": len(jobs),
                      "audited_records": result.get("campaign", {}).get("records")}))
    raise SystemExit(0 if result["passed"] else 1)
