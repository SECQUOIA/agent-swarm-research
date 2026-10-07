"""Run one campaign-5 case in one mode; a copy of the campaign-4 worker (v4_worker.py).

SCIP modes call the snapshot's ``run_instance`` with the separator mode,
``Config`` overrides and SCIP parameters of the mode table (``mode_config``:
every campaign-4 mode unchanged, plus the campaign-5 modes of
``campaign-v5-protocol.md``); mode ``gurobi`` builds the case model directly in
Gurobi (linear and quadratic rows only), as in campaign 4. Every incumbent,
Gurobi's included, gets the archived independent original-model check
(``cases.check_primal``).

Campaign-5 modes (n stars and k leaves per star of a Part 5S case; n copies
of a path case):

- star-family limits: max_blocks n k, max_cuts 4 n k, max_cuts_per_round n k,
  max_support_calls 10 n k, max_rounds 10, max_separation_seconds 60,
  separation_budget_fraction 0.5; ``rowdir-star4`` adds row_directions,
  ``agg-star4`` adds aggregate_directions and row_directions, ``agg-star``
  adds star_leaves 16 to agg-star4;
- ``frozen-cap32``/``rowdir-cap32``: max_blocks n, max_cuts 32 n,
  max_cuts_per_round 8 n, max_support_calls 80 n, max_rounds 40 (Amendment 1 of
  the protocol; 10 in the original text), max_separation_seconds 150,
  separation_budget_fraction 0.5 (rowdir: plus row_directions);
  ``frozen-cap64``/``rowdir-cap64``: 64 n, 16 n, 160 n.

Three measurements are added without changing the frozen solver code, by
wrapping module-level names of the snapshot for the duration of the run:

- ``certification_log`` (campaign 5): every call of
  ``solver.support.certify_support`` (the separator imports it at each
  callback) as [block dimension, method, status, support certified, seconds];
  ``certification_summary`` aggregates it by method, and ``cut_methods``
  counts the certificate method (``support_witness.method``) of the recorded
  cuts. The run fails if the log does not have one entry per separator
  certification call;
- ``row_binding_rejection_causes``: when the separator's stored-row audit
  (``_audit_inserted_row``) rejects a row, the cause is classified by
  repeating the audit's checks in its order (the audit's return value is
  passed through unchanged);
- ``native_statistics``: just before the model is freed, SCIP's separator and
  nonlinear-handler statistics tables, the effective values of the mode's
  SCIP parameters and the transformed status of every original variable are
  read (``build_model`` is wrapped to hand ``run_instance`` a delegating
  model object whose ``freeProb`` does this first). This happens after
  ``run_instance`` has computed its times. SCIP counts a separator call only
  when the separator did not return DIDNOTRUN.

The run fails unless every solver, checker and case module was imported from
the snapshot.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import tempfile
import time
import traceback

ALL_DIAG = {"max_blocks": 128, "max_cuts": 200, "max_cuts_per_round": 50, "max_rounds": 10,
            "max_support_calls": 500, "max_separation_seconds": 30.0,
            "separation_budget_fraction": 0.5}
# SCIP 10.0.2 parameter names and values (checked by the campaign-4 snapshot.py against
# Model.getParams(); recorded in snapshot/scip-parameters.json, copied unchanged into the
# campaign-5 snapshot, and in every record).
SCIP_PARAMETER_SETS = {
    # No implicit-discreteness presolve of the nonlinear constraint handler.
    "novarlocks": {"constraints/nonlinear/checkvarlocks": "d"},
    # Nonconvex separators that are off by default. The separators run at the
    # root (freq 0), like RLT by default and like the certified separator;
    # separating/rlt/freq is 0 by default, so RLT itself already runs.
    "extra": {"separating/eccuts/freq": 0,
              "nlhdlr/quadratic/useintersectioncuts": True,
              "separating/interminor/freq": 0,
              "separating/rlt/detecthidden": True,
              "separating/rlt/hiddenrlt": True},
    "noaggr": {"presolving/donotaggr": True, "presolving/donotmultaggr": True},
}
GUROBI_PARAMS = {"Threads": 1, "NonConvex": 2, "MIPGap": 1e-4, "OutputFlag": 0}
NOAGGR_MODES = ("baseline-noaggr", "all-noaggr", "all-diag-noaggr", "all-diag-rowdir-noaggr")
SCIP_MODES_V4 = ("baseline", "all", "auto", "all-diag", "all-diag-mech", "frozen-wide", "rowdir-wide",
                 "all-diag-rowdir", "baseline-novarlocks", "baseline-extra") + NOAGGR_MODES
STAR_MODES = ("rowdir-star4", "agg-star4", "agg-star")
CAP_MODES = ("frozen-cap32", "rowdir-cap32", "frozen-cap64", "rowdir-cap64")
SCIP_MODES = SCIP_MODES_V4 + STAR_MODES + CAP_MODES
MODES = SCIP_MODES + ("gurobi",)
FROZEN_PACKAGES = {"solver", "theory", "reviews", "uenv", "cases", "worker", "run_campaign"}
STAR_LEAVES = 16
# Caps of Part 5C-b: (cuts, cuts per round, support calls) per copy.
CAPS = {"32": (32, 8, 80), "64": (64, 16, 160)}


def mechanism_limits(case, cuts, per_round, support):
    n = case["mechanism"]["n"]
    return {"max_blocks": n, "max_cuts": cuts * n, "max_cuts_per_round": per_round * n,
            "max_rounds": 10, "max_support_calls": support * n,
            "max_separation_seconds": 60.0, "separation_budget_fraction": 0.5}


def star_limits(case):
    """Star-family limits of Part 5S: n k blocks, 4 n k cuts, n k per callback, 10 n k support calls."""
    nk = case["star"]["n"] * case["star"]["k"]
    return {"max_blocks": nk, "max_cuts": 4 * nk, "max_cuts_per_round": nk, "max_rounds": 10,
            "max_support_calls": 10 * nk, "max_separation_seconds": 60.0, "separation_budget_fraction": 0.5}


def cap_limits(case, cap):
    """Part 5C-b limits: n blocks, larger cut caps, 40 callbacks (Amendment 1), 150 s separation allowance."""
    cuts, per_round, support = CAPS[cap]
    return {**mechanism_limits(case, cuts, per_round, support), "max_rounds": 40, "max_separation_seconds": 150.0}


def mode_config(mode, case):
    """Return (run_instance mode, Config overrides, SCIP parameters) for a SCIP mode."""
    params = {}
    base = mode
    if mode == "rowdir-star4":
        return "all", {**star_limits(case), "row_directions": True}, params
    if mode == "agg-star4":
        return "all", {**star_limits(case), "aggregate_directions": True, "row_directions": True}, params
    if mode == "agg-star":
        return "all", {**star_limits(case), "aggregate_directions": True, "row_directions": True,
                       "star_leaves": STAR_LEAVES}, params
    if mode in CAP_MODES:
        kind, cap = mode.split("-cap")
        overrides = cap_limits(case, cap)
        return "all", ({**overrides, "row_directions": True} if kind == "rowdir" else overrides), params
    if mode in NOAGGR_MODES:
        base = mode[:-len("-noaggr")]
        params.update(SCIP_PARAMETER_SETS["noaggr"])
    if base in ("baseline", "all", "auto"):
        return base, {}, params
    if base == "all-diag":
        return "all", dict(ALL_DIAG), params
    if base == "all-diag-rowdir":
        return "all", {**ALL_DIAG, "row_directions": True}, params
    if base == "all-diag-mech":  # mechanism: n blocks, 4n cuts, n per callback, 20n support calls
        return "all", mechanism_limits(case, 4, 1, 20), params
    if base == "frozen-wide":  # wide: n blocks, 16n cuts, 4n per callback, 40n support calls
        return "all", mechanism_limits(case, 16, 4, 40), params
    if base == "rowdir-wide":
        return "all", {**mechanism_limits(case, 16, 4, 40), "row_directions": True}, params
    if base == "baseline-novarlocks":
        return "baseline", {}, {**params, **SCIP_PARAMETER_SETS["novarlocks"]}
    if base == "baseline-extra":
        return "baseline", {}, {**params, **SCIP_PARAMETER_SETS["extra"]}
    raise ValueError(f"unknown campaign-5 SCIP mode {mode!r}")


# ---------------------------------------------------------------- SCIP measurements

def statistics_table(text, header):
    lines = text.splitlines()
    start = next((k for k, line in enumerate(lines) if line.startswith(header + " ")), None)
    if start is None:
        return None
    columns = lines[start].split(":", 1)[1].split()
    table = {}
    for line in lines[start + 1:]:
        if not line.startswith("  ") or ":" not in line:
            break
        name, values = line.split(":", 1)
        row = {}
        for column, value in zip(columns, values.split()):
            try:
                row[column] = int(value)
            except ValueError:
                try:
                    row[column] = float(value)
                except ValueError:
                    row[column] = value
        table[name.strip()] = row
    return table


def native_statistics(model, built, params):
    started = time.perf_counter()
    out = {"scip_params_effective": {key: model.getParam(key) for key in params}}
    handle, path = tempfile.mkstemp(suffix=".stats")
    os.close(handle)
    try:
        model.writeStatistics(path)
        text = Path(path).read_text(errors="replace")
    finally:
        os.unlink(path)
    out["separators"] = statistics_table(text, "Separators")
    out["nlhdlrs"] = statistics_table(text, "Nlhdlrs")
    out["original_variable_status"] = dict(Counter(str(model.getTransformedVar(v).getStatus())
                                                   for v in built.xs))
    out["seconds"] = time.perf_counter() - started
    return out


class StatisticsProbe:
    """Delegates every call to the SCIP model; reads statistics before freeing it."""

    def __init__(self, model, built, params, sink):
        self._model, self._built, self._params, self._sink = model, built, params, sink

    def __getattr__(self, name):
        return getattr(self._model, name)

    def freeProb(self):
        try:
            self._sink.update(native_statistics(self._model, self._built, self._params))
        except Exception as error:  # recorded, never hidden; the run itself is unaffected
            self._sink["error"] = f"{type(error).__name__}: {error}"
        finally:
            self._model.freeProb()


def classify_rejection(model, row, variables, coefficients, rhs):
    """First failing check of _audit_inserted_row, in the audit's order."""
    Q = Fraction
    statuses = Counter()
    actual = {column.getVar().name: Q(float(c)) for column, c in zip(row.getCols(), row.getVals()) if c}
    expected = {}
    for variable, coefficient in zip(variables, coefficients):
        if not coefficient:
            continue
        transformed = model.getTransformedVar(variable)
        status = str(transformed.getStatus())
        if status not in ("COLUMN", "LOOSE"):
            statuses[status] += 1
        if transformed.name in expected:
            return "aliased_transformed_column", statuses
        expected[transformed.name] = Q(float(coefficient))
    expected = {name: value for name, value in expected.items() if value}
    lhs, upper, constant = float(row.getLhs()), float(row.getRhs()), float(row.getConstant())
    missing, extra = set(expected) - set(actual), set(actual) - set(expected)
    changed = [name for name in set(actual) & set(expected) if actual[name] != expected[name]]
    if missing or extra:
        if statuses:  # a source variable is aggregated, fixed or otherwise not a column
            cause = "column_set_differs_variable_not_column"
        elif not extra and all(abs(expected[name]) <= model.epsilon() for name in missing):
            cause = "column_set_differs_tiny_coefficient_dropped"
        else:
            cause = "column_set_differs_other"
    elif changed:
        rounded = all(actual[name] == round(expected[name]) for name in changed)
        cause = "coefficient_rounded_to_integer" if rounded else "coefficient_differs_other"
    elif not math.isfinite(lhs) or abs(lhs) >= model.infinity():
        cause = "lhs_infinite"
    elif not math.isfinite(constant):
        cause = "constant_nonfinite"
    elif Q(lhs) - Q(constant) != Q(float(rhs)):
        cause = "bound_differs"
    elif not upper >= model.infinity():
        cause = "finite_upper_side"
    elif row.isLocal():
        cause = "local_row"
    else:
        cause = "unclassified"
    return cause, statuses


def install_measurements(integration, params):
    """Wrap the audit and the model builder of the snapshot's integration module."""
    rejections = {"causes": Counter(), "variable_statuses": Counter(), "classifier_errors": 0}
    statistics = {}
    audit, builder = integration._audit_inserted_row, integration.build_model

    def audited(model, row, variables, coefficients, rhs):
        result = audit(model, row, variables, coefficients, rhs)
        if result is None:
            try:
                cause, statuses = classify_rejection(model, row, variables, coefficients, rhs)
                rejections["causes"][cause] += 1
                rejections["variable_statuses"].update(statuses)
            except Exception:
                rejections["classifier_errors"] += 1
        return result

    def build(inst):
        built = builder(inst)
        built.model = StatisticsProbe(built.model, built, params, statistics)
        return built

    integration._audit_inserted_row = audited
    integration.build_model = build
    return rejections, statistics


CERTIFICATION_FIELDS = ("dimension", "method", "status", "certified", "seconds")


def install_certification_log(support):
    """Wrap support.certify_support; the result is passed through unchanged."""
    log = []
    certify = support.certify_support

    def logged(features, symbols, box, coefficients, **options):
        started = time.perf_counter()
        entry = [len(symbols), None, "exception", False, None]
        try:
            result = certify(features, symbols, box, coefficients, **options)
            entry[1:4] = [result.stats.get("method"), result.status, result.cut is not None]
            return result
        finally:
            entry[4] = time.perf_counter() - started
            log.append(entry)

    support.certify_support = logged
    return log


def certification_summary(log):
    """Per method: calls, statuses, certified supports, seconds (sum, median, max), dimensions."""
    out = {}
    for dimension, method, status, certified, seconds in log:
        entry = out.setdefault(str(method), {"calls": 0, "certified": 0, "statuses": Counter(),
                                             "dimensions": Counter(), "seconds": []})
        entry["calls"] += 1
        entry["certified"] += bool(certified)
        entry["statuses"][status] += 1
        entry["dimensions"][str(dimension)] += 1
        entry["seconds"].append(seconds)
    for entry in out.values():
        times = sorted(entry.pop("seconds"))
        entry.update(statuses=dict(entry["statuses"]), dimensions=dict(entry["dimensions"]),
                     seconds_sum=sum(times), seconds_median=times[len(times) // 2], seconds_max=times[-1])
    return out


# ---------------------------------------------------------------- Gurobi

def gurobi_status_names():
    from gurobipy import GRB
    return {getattr(GRB.Status, name): name for name in dir(GRB.Status) if name.isupper()}


def run_gurobi(model, time_limit, seed):
    """Solve the case model (linear and quadratic rows) with Gurobi; SCIP-like record."""
    import gurobipy as gp
    from gurobipy import GRB
    started = time.perf_counter()
    infinity = lambda v: v if math.isfinite(v) else (GRB.INFINITY if v > 0 else -GRB.INFINITY)
    kinds = {"C": GRB.CONTINUOUS, "B": GRB.BINARY, "I": GRB.INTEGER}
    env = gp.Env(empty=True)
    env.setParam("OutputFlag", 0)
    env.start()
    try:
        g = gp.Model(model.name, env=env)
        x = [g.addVar(lb=infinity(lo), ub=infinity(hi), vtype=kinds[kind], name=f"x{i}")
             for i, (lo, hi, kind) in enumerate(zip(model.var_lb, model.var_ub, model.var_type))]

        def polynomial(row):
            if row["nl"] is not None:
                raise ValueError("mode gurobi supports linear and quadratic rows only")
            expression = gp.QuadExpr()
            for i, c in row["lin"].items():
                expression.add(x[int(i)], c)
            for i, j, c in row["quad"]:
                expression.add(x[i] * x[j], c)
            return expression

        g.setObjective(polynomial(model.rows[0]) + model.obj_const,
                       GRB.MINIMIZE if model.obj_sense == "min" else GRB.MAXIMIZE)
        for row in model.rows[1:]:
            expression = polynomial(row)
            if row["lb"] == row["ub"]:
                g.addConstr(expression == row["ub"])
                continue
            if math.isfinite(row["ub"]):
                g.addConstr(expression <= row["ub"])
            if math.isfinite(row["lb"]):
                g.addConstr(expression >= row["lb"])
        build_seconds = time.perf_counter() - started
        remaining = max(0.0, time_limit - (time.perf_counter() - started))
        params = {**GUROBI_PARAMS, "Seed": seed, "TimeLimit": remaining}
        for key, value in params.items():
            g.setParam(key, value)
        solve_start = time.perf_counter()
        g.optimize()
        solve_wall = time.perf_counter() - solve_start
        code = g.Status
        name = gurobi_status_names().get(code, str(code))
        primal = float(g.ObjVal) if g.SolCount else None
        values = [float(v.X) for v in x] if g.SolCount else None
        try:
            bound = float(g.ObjBound)
        except (AttributeError, gp.GurobiError):
            bound = None
        bound = bound if bound is not None and math.isfinite(bound) and abs(bound) < 1e19 else None
        if code == GRB.OPTIMAL:
            exact = primal is not None and bound is not None and abs(primal - bound) <= 1e-9 * max(1.0, abs(primal))
            status = "optimal" if exact else "gaplimit"
        else:
            status = name.lower().replace("_", "")
        return {"name": model.name, "mode": "gurobi", "sense": model.obj_sense, "status": status,
                "gurobi_status": code, "gurobi_status_name": name,
                "primal": primal, "dual": bound, "root_dual": None, "original_values": values,
                "nodes": int(g.NodeCount), "time_limit": time_limit, "node_limit": None, "seed": seed,
                "build_seconds": build_seconds, "solve_wall_seconds": solve_wall,
                "solver_runtime_seconds": float(g.Runtime), "gurobi_work": float(g.Work),
                "mip_gap": float(g.MIPGap) if g.SolCount else None,
                "total_seconds": time.perf_counter() - started, "remaining_solve_budget": remaining,
                "discovery": None, "coverage": None, "separation": None, "cuts": [],
                "cut_log_complete": True, "model_metadata": None, "gurobi_params": params,
                "gurobi_version": ".".join(map(str, gp.gurobi.version())),
                "bound_status": "Gurobi numerical bounds; no experimental cuts"}
    finally:
        try:
            g.dispose()
        except NameError:
            pass
        env.dispose()


# ---------------------------------------------------------------- worker

def main(args):
    start = time.perf_counter()
    source = args.source.resolve()
    sys.path.insert(0, str(source))
    sys.path.insert(0, str(source / "experiments"))
    from worker import load_model
    from cases import check_primal
    from run_campaign import exact_json
    import solver.integration as integration
    import solver.support as support
    from solver.integration import Config
    preparation_start = time.perf_counter()
    case = json.loads(args.case.read_text())
    if "path" in case:
        archived = source.parent / "original-osil" / (case["name"] + ".osil")
        if not archived.is_file():
            raise FileNotFoundError(f"archived OSiL copy missing: {archived}")
        case = {**case, "path": str(archived)}
    if args.mode != "gurobi":
        solver_mode, overrides, params = mode_config(args.mode, case)
        config = Config(**overrides)
        rejections, statistics = install_measurements(integration, params)
        certifications = install_certification_log(support)
    load_start = time.perf_counter()
    model = load_model(case)
    source_read_seconds = time.perf_counter() - load_start
    encoded = exact_json(asdict(model))
    model_hash = hashlib.sha256(json.dumps(encoded, sort_keys=True).encode()).hexdigest()
    preparation_seconds = time.perf_counter() - preparation_start
    import_seconds = time.perf_counter() - start
    budget = max(1e-6, args.time_limit - preparation_seconds)
    if args.mode == "gurobi":
        if args.node_limit is not None:
            raise ValueError("mode gurobi is run without a node limit")
        result = run_gurobi(model, budget, args.seed)
        result.update(solver_mode="gurobi", model_sha256=model_hash)
    else:
        result = integration.run_instance(model, solver_mode, time_limit=budget, seed=args.seed,
                                          node_limit=args.node_limit, config=config, scip_params=params)
        if result.get("config") != asdict(config) or result.get("scip_params") != params:
            raise RuntimeError("run_instance did not record the effective Config and SCIP parameters")
        result.update(mode=args.mode, solver_mode=solver_mode, config_overrides=overrides,
                      original_model=encoded, model_sha256=model_hash,
                      row_binding_rejection_causes={k: dict(v) if isinstance(v, Counter) else v
                                                    for k, v in rejections.items()},
                      native_statistics=statistics or None)
        separation = result.get("separation") or {}
        if sum(rejections["causes"].values()) + rejections["classifier_errors"] != separation.get(
                "row_binding_rejections", 0):
            raise RuntimeError("row-binding rejection causes do not add up to the separator count")
        if len(certifications) != separation.get("certification_calls", 0):
            raise RuntimeError("certification log does not match the separator's certification calls")
        result.update(cut_methods=dict(Counter(c["support_witness"]["method"] for c in result.get("cuts") or [])),
                      certification_log={"fields": list(CERTIFICATION_FIELDS), "calls": certifications},
                      certification_summary=certification_summary(certifications))
    result.setdefault("cut_log_complete", isinstance(result.get("cuts"), list))
    check_start = time.perf_counter()
    check = check_primal(model, result.get("original_values"), result.get("primal"))
    result.update(primal_check=check, primal_check_seconds=time.perf_counter() - check_start,
                  source_read_seconds=source_read_seconds,
                  preparation_seconds=preparation_seconds,
                  worker_import_and_load_seconds=import_seconds,
                  worker_total_seconds=time.perf_counter() - start)
    result["reference_check"] = {"checked": False, "reason": "no finite archived reference",
                                 "certifies_dual": False}
    reference = case.get("known_optimum", case.get("reference_primal"))
    if reference is not None:
        try:
            reference = float(reference)
            if not math.isfinite(reference):
                raise ValueError("nonfinite archived reference")
            tolerance = 1e-5 * max(1.0, abs(reference))
            dual, root_dual = result.get("dual"), result.get("root_dual")
            minimize = model.obj_sense == "min"
            result["reference_check"] = {
                "checked": True, "value": reference,
                "kind": "analytic optimum" if "known_optimum" in case else "archived feasible bound",
                "tolerance": tolerance,
                "dual_consistent": dual is None or (dual <= reference + tolerance if minimize
                                                     else dual >= reference - tolerance),
                "root_dual_consistent": root_dual is None or (
                    root_dual <= reference + tolerance if minimize else root_dual >= reference - tolerance),
                "certifies_dual": False}
        except (TypeError, ValueError):
            pass
    if case.get("known_witness") is not None:
        result["reference_witness_check"] = check_primal(model, case["known_witness"], case.get("known_optimum"))
    frozen = [m for name, m in list(sys.modules.items()) if name.split(".")[0] in FROZEN_PACKAGES]
    outside = [m.__file__ for m in frozen if getattr(m, "__file__", None)
               and not Path(m.__file__).resolve().is_relative_to(source.parent)]
    if outside:
        raise RuntimeError(f"modules imported from outside the snapshot: {outside}")
    result["snapshot_modules_verified"] = len(frozen)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True,
                        help="snapshot copy of research-20261003-convexification")
    parser.add_argument("--mode", required=True, choices=MODES)
    parser.add_argument("--time-limit", type=float, required=True)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--node-limit", type=int)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = main(args)
    except Exception as error:
        traceback.print_exc()
        result = {"status": "worker_error", "exception": type(error).__name__, "reason": str(error),
                  "cut_log_complete": False, "cut_count": None}
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    temporary.replace(args.output)
