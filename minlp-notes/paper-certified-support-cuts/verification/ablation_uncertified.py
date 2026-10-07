#!/usr/bin/env python3
"""Part U of campaign-v4-protocol.md (Amendment 1): what certification buys.

Offline; no solver is run. For every recorded cut of the MINLPLib parts, and
for a fixed random sample of the path-family cuts, the support constant that
an uncertified binary64 pipeline would use for the recorded binary64 direction
(a, lambda) is computed in two variants and compared exactly with the
certified support value of the cut's certificate:

U1  minimum of a^T u + lambda^T g(u) over the separator's own sample set,
    computed by the snapshot's ``solver.integration._sample`` (the routine
    behind the direction LP ``propose_direction``) with the run's Config:
    a 33-point grid in 1D, 7x7 in 2D, 3^d for d = 3, 4, filtered by the
    affine domain rows, plus the exact domain vertices and their centroid
    for quadratic blocks when the face budget allows. The exchange samples
    that the separator adds later are minimizers returned by the certified
    oracle; an uncertified pipeline does not have them, so they are excluded.
U2  min(U1, SLSQP local minima). scipy.optimize.minimize(method='SLSQP')
    from the three best samples (stable order), on the block box (bounds)
    and the affine domain rows (inequality constraints), default
    tolerances, maxiter 200, analytic gradients (SymPy). A final point is
    clipped to the box and accepted if every domain row holds within
    1e-9*max(1,|rhs|); its value is re-evaluated in binary64 with the
    snapshot's ``_evaluate``.

A cut is invalid if U > certified value, materially invalid if the excess
exceeds 1e-6*max(1,|value|). Only exact certificates (quadratic polytope,
polygon and star oracles, whose value is the true minimum) are counted as
invalid; Bernstein and Arb values are lower bounds and are reported
separately. For each materially invalid cut the eliminated row with the
uncertified constant, c^T v >= U - sum_r lambda_r b_r (the recorded exact
row c^T v >= r with r raised by U - beta, beta the recorded binary64 support
constant), is evaluated exactly at every recorded incumbent of the same
model (records with ``original_values`` that passed the independent primal
check, in all record files given) and at the known optimal witness of the
case file when there is one. A violation above 1e-6*max(1,||c||_1) means
that the uncertified cut would have removed a feasible point. The
certified row is evaluated at the same points as a control.

Also reported for every recorded cut: whether the exported binary64
coefficients differ from the exact eliminated row, and the bound
correction E of Proposition "Safe export" (field
``row_certificate.exact.box_compensation``).

Usage (campaign 3; campaign-4 run directories have the same layout)::

    PY=/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python
    E=/workspace/minlp-notes/paper-certified-support-cuts/experiments
    $PY ablation_uncertified.py \
        --minlplib $E/v3/runs/partA-full $E/v3/runs/partA-root $E/v3/runs/partB \
                   $E/v3d/runs/partA-root-rowdir $E/v3d/runs/partB-root-rowdir \
        --path $E/v3/runs/partC $E/v3d/runs/partC-rowdir

Each argument is a run directory (with ``records.jsonl``, ``snapshot/`` and,
optionally, ``cases/``) or a ``records.jsonl`` inside one. The snapshot code
of each run directory is imported read-only, in worker processes (at most
four, each single-threaded), with bytecode writing disabled.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import os  # noqa: E402

THREAD_ENV = {name: "1" for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS",
                                     "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS",
                                     "BLIS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")}
os.environ.update(THREAD_ENV)
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import argparse  # noqa: E402
import collections  # noqa: E402
from concurrent.futures import ThreadPoolExecutor  # noqa: E402
from fractions import Fraction as Q  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
from pathlib import Path  # noqa: E402
import random  # noqa: E402
import statistics  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402

HERE = Path(__file__).resolve().parent
TOPIC = "research-20261003-convexification"
EXACT_METHODS = ("quadratic_polytope", "quadratic_polygon", "quadratic_star")
MATERIAL = Q(1, 10**6)       # excess and violation tolerances of the protocol
ROW_TOL = 1e-9               # acceptance of a final SLSQP point (relative)
SLSQP_STARTS = 3
SLSQP_MAXITER = 200
MAX_WORKERS = 4


# ----------------------------------------------------------------------------
# Worker: block reconstruction, U1 and U2 (imports one snapshot)
# ----------------------------------------------------------------------------

def worker_main(snapshot):
    source = (Path(snapshot) / TOPIC).resolve()
    sys.path.insert(0, str(source))
    import warnings
    from types import SimpleNamespace

    import numpy as np
    from scipy.optimize import minimize
    import sympy as sp

    from solver.certified import _prepare
    from solver.integration import Config, _evaluate, _sample

    frozen = [m for name, m in list(sys.modules.items())
              if name.split(".")[0] in ("solver", "theory")]
    outside = [m.__file__ for m in frozen if getattr(m, "__file__", None)
               and not Path(m.__file__).resolve().is_relative_to(source.parent)]
    if outside:
        raise RuntimeError(f"modules imported from outside the snapshot: {outside}")

    def analyze(item):
        out = {"id": item["id"]}
        syms = tuple(sp.Symbol(s, real=True) for s in item["symbols"])
        local = {str(s): s for s in syms}
        features = tuple(sp.sympify(f, locals=local) for f in item["features"])
        d = len(syms)
        box_q = [(Q(lo), Q(hi)) for lo, hi in item["box"]]
        box = tuple((float(lo), float(hi)) for lo, hi in box_q)
        rows = tuple((tuple(Q(c) for c in r["coefficients"]), Q(r["rhs"]))
                     for r in item["domain_rows"])
        coefficients = tuple(float(c) for c in item["coefficients"])
        binding = _prepare(features, syms, box, coefficients, rows)[-1]
        out["reconstruction"] = {
            "binding_matches_witness": binding == item["binding"],
            "feature_strings_roundtrip": [str(f) for f in features] == item["features"],
            "box_binary64_exact": all(Q(b) == q for pair, pairq in zip(box, box_q)
                                      for b, q in zip(pair, pairq)),
        }
        quadratic = all(f.is_polynomial(*syms) and sp.Poly(f, *syms).total_degree() <= 2
                        for f in features[d:])
        out["quadratic"] = quadratic
        block = SimpleNamespace(variables=tuple(item["variables"]), symbols=syms,
                                features=features, box=box, rows=rows, quadratic=quadratic,
                                sample=None, sample_points=[], scale=None)
        try:
            _sample(block, Config(**item["config"]))
        except ValueError as exc:
            out["error"] = f"sample routine raised: {exc}"
            return out
        c = np.asarray(coefficients, dtype=float)
        values = block.sample @ c
        best = int(np.argmin(values))
        u1 = float(values[best])
        out.update(sample_size=len(block.sample_points), u1=u1.hex(),
                   u1_point=[float(v) for v in block.sample_points[best]])

        # U2: SLSQP from the three best samples.
        fs = [sp.lambdify(syms, f, "numpy") for f in features]
        gs = [[sp.lambdify(syms, sp.diff(f, s), "numpy") for s in syms] for f in features]

        def fun(u):
            return float(c @ np.array([float(f(*u)) for f in fs]))

        def jac(u):
            return c @ np.array([[float(g(*u)) for g in row] for row in gs])

        lower = np.array([lo for lo, _ in box])
        upper = np.array([hi for _, hi in box])
        if rows:
            A = np.array([[float(v) for v in a] for a, _ in rows])
            b = np.array([float(r) for _, r in rows])
            constraints = [{"type": "ineq", "fun": lambda u: b - A @ u, "jac": lambda u: -A}]
        else:
            constraints = []
        u2, u2_point, runs = u1, out["u1_point"], []
        for start in np.argsort(values, kind="stable")[:SLSQP_STARTS]:
            x0 = np.array([float(v) for v in block.sample_points[int(start)]])
            run = {"start": [float(v) for v in x0]}
            try:
                with warnings.catch_warnings(), np.errstate(all="ignore"):
                    warnings.simplefilter("ignore")
                    res = minimize(fun, x0, jac=jac, method="SLSQP", bounds=box,
                                   constraints=constraints, options={"maxiter": SLSQP_MAXITER})
                x = np.clip(np.asarray(res.x, dtype=float), lower, upper)
                run.update(status=int(res.status), message=str(res.message), nit=int(res.nit))
                violation = float(np.max((A @ x - b) / np.maximum(1., abs(b)))) if rows else 0.
                run["max_relative_row_violation"] = violation
                accepted = bool(np.isfinite(x).all() and violation <= ROW_TOL)
                if accepted:
                    value = float((_evaluate(block, x[None, :]) @ c)[0])
                    accepted = math.isfinite(value)
                if accepted:
                    run.update(value=value.hex(), point=[float(v) for v in x])
                    if value < u2:
                        u2, u2_point = value, [float(v) for v in x]
            except (ValueError, TypeError, ArithmeticError, np.linalg.LinAlgError) as exc:
                run["error"] = str(exc)
                accepted = False
            run["accepted"] = accepted
            runs.append(run)
        out.update(u2=u2.hex(), u2_point=u2_point, slsqp=runs)

        # Exact objective at the recorded certified minimizer (exact oracles).
        if item.get("minimizer") is not None:
            point = [Q(v) for v in item["minimizer"]]
            subs = {s: sp.Rational(v.numerator, v.denominator) for s, v in zip(syms, point)}
            total = Q(0)
            for coefficient, feature in zip(coefficients, features):
                value = feature.xreplace(subs)
                if not value.is_Rational:
                    total = None
                    break
                total += Q(coefficient) * Q(int(value.p), int(value.q))
            feasible = (all(lo <= v <= hi for v, (lo, hi) in zip(point, box_q)) and
                        all(sum(a_k * v for a_k, v in zip(a, point)) <= r for a, r in rows))
            out["minimizer_check"] = {"value": None if total is None else str(total),
                                      "feasible": feasible}
        return out

    items = json.load(sys.stdin)
    results = []
    for item in items:
        try:
            results.append(analyze(item))
        except Exception as exc:  # recorded per cut and reported
            results.append({"id": item["id"], "error": f"{type(exc).__name__}: {exc}"})
    json.dump(results, sys.stdout)


# ----------------------------------------------------------------------------
# Main process: records, sampling, exact comparisons, incumbents, report
# ----------------------------------------------------------------------------

class Part:
    def __init__(self, arg, family):
        path = Path(arg).resolve()
        self.records = path / "records.jsonl" if path.is_dir() else path
        self.run_dir = self.records.parent
        parent = self.run_dir.parent
        self.label = (f"{parent.parent.name}/{self.run_dir.name}" if parent.name == "runs"
                      else self.run_dir.name)
        self.family = family
        self.snapshot = self.run_dir / "snapshot"
        integration = self.snapshot / TOPIC / "solver" / "integration.py"
        if not self.records.is_file() or not integration.is_file():
            raise SystemExit(f"{arg}: need records.jsonl and snapshot/{TOPIC}/solver/integration.py")
        self.integration_sha256 = hashlib.sha256(integration.read_bytes()).hexdigest()


def model_key(record):
    return record.get("model_sha256") or record["name"]


def export_census(cut):
    """Rounding of the eliminated row (Proposition 'Safe export')."""
    cert = cut["row_certificate"]
    exact, exported = cert["exact"], cert["exported"]
    differ = False
    for coefficient, error, value in zip(exact["coefficients"], exact["rounding_errors"],
                                         exported["coefficients"]):
        if error != "0":
            differ = True
        if (value != 0.0 or coefficient != "0") and Q(value) - Q(coefficient) != Q(error):
            raise ValueError("rounding error field disagrees with the exported coefficient")
    r, E = Q(exact["eliminated_rhs"]), Q(exact["box_compensation"])
    safe = (Q(exact["compensated_rhs"]) == r + E and Q(exported["rhs"]) <= r + E)
    return {"differ": differ, "E": E, "r": r, "safe": safe,
            "downward_shift": r + E - Q(exported["rhs"])}


def scan(part, keep, cut_refs, incumbents, case_witnesses, census):
    """Stream one record file; keep cut contexts for which keep(i) is true."""
    digest = hashlib.sha256()
    kept = []
    seen_cases = set()
    with open(part.records, "rb") as handle:
        for line_no, raw in enumerate(handle):
            digest.update(raw)
            if not raw.strip():
                continue
            record = json.loads(raw)
            key = model_key(record)
            if incumbents is not None:
                check = record.get("primal_check") or {}
                if record.get("original_values") is not None and check.get("passed") is True:
                    objective = check.get("objective", record.get("primal"))
                    incumbents.setdefault(key, []).append({
                        "source": f"{part.label}:{record.get('run_id', line_no)}",
                        "name": record["name"], "values": record["original_values"],
                        "objective": objective})
                if (part.label, record["name"]) not in seen_cases:
                    seen_cases.add((part.label, record["name"]))
                    case = part.run_dir / "cases" / (record["name"] + ".json")
                    if case.is_file() and key not in case_witnesses:
                        data = json.loads(case.read_text())
                        if data.get("known_witness_exact") is not None:
                            witness = data["known_witness_exact"]
                            if isinstance(witness, str):
                                witness = json.loads(witness.replace("'", '"'))
                            case_witnesses[key] = {
                                "source": f"{part.label}:cases/{record['name']}.json",
                                "name": record["name"], "values": witness,
                                "objective": data.get("known_optimum_exact")}
            for k, cut in enumerate(record.get("cuts") or []):
                index = len(cut_refs)
                cut_refs.append((part.label, line_no, k))
                if census is not None:
                    census.setdefault(part.label, []).append(export_census(cut))
                if keep(index):
                    kept.append({"index": index, "part": part.label, "line": line_no, "k": k,
                                 "name": record["name"], "model_key": key,
                                 "mode": record.get("mode"), "seed": record.get("seed"),
                                 "phase": record.get("phase"), "run_id": record.get("run_id"),
                                 "config": record["config"], "cut": cut})
    return kept, digest.hexdigest()


def worker_item(i, ctx):
    cut = ctx["cut"]
    return {"id": i, "symbols": cut["symbols"], "variables": cut["variables"],
            "features": cut["features"], "box": cut["box"], "domain_rows": cut["domain_rows"],
            "coefficients": cut["coefficients"], "binding": cut["support_witness"]["model"],
            "config": ctx["config"],
            "minimizer": (cut["support_stats"].get("minimizer")
                          if cut["support_stats"]["method"] in EXACT_METHODS else None)}


def run_workers(contexts, parts, workers, chunk):
    by_snapshot = {}
    for i, ctx in enumerate(contexts):
        by_snapshot.setdefault(str(parts[ctx["part"]].snapshot), []).append(i)
    jobs = []
    for snapshot, ids in by_snapshot.items():
        for start in range(0, len(ids), chunk):
            jobs.append((snapshot, ids[start:start + chunk]))
    env = {**os.environ, **THREAD_ENV, "PYTHONDONTWRITEBYTECODE": "1"}

    def run(job):
        snapshot, ids = job
        payload = json.dumps([worker_item(i, contexts[i]) for i in ids])
        done = subprocess.run([sys.executable, "-B", str(Path(__file__).resolve()),
                               "--worker", snapshot], input=payload, capture_output=True,
                              text=True, env=env, cwd="/tmp", check=False)
        if done.returncode != 0:
            raise RuntimeError(f"worker failed ({snapshot}): {done.stderr[-2000:]}")
        return json.loads(done.stdout)

    results = {}
    with ThreadPoolExecutor(max_workers=min(workers, MAX_WORKERS)) as pool:
        for batch in pool.map(run, jobs):
            for result in batch:
                results[result["id"]] = result
    return results


def column_value(name, incumbent):
    """Value of a row column ('x<i>' or 'objective_epigraph') at an incumbent."""
    if name == "objective_epigraph":
        return None if incumbent["objective"] is None else Q(incumbent["objective"])
    if not name.startswith("x") or not name[1:].isdigit():
        raise ValueError(f"unknown row column {name}")
    index = int(name[1:])
    values = incumbent["values"]
    if index >= len(values) or values[index] is None:
        raise ValueError(f"incumbent lacks column {name}")
    return Q(values[index])


def row_check(cut, uncertified, points):
    """Evaluate certified and uncertified eliminated rows exactly at points."""
    cert = cut["row_certificate"]
    names = cert["binding"]["variables"]
    if cut["column_names"] != ["v" + n[1:] if n.startswith("x") else n for n in names]:
        raise ValueError("row columns do not map to original variables")
    beta = Q(cert["binding"]["support"]["rhs"])
    if beta != Q(float.fromhex(cut["support_witness"]["rhs"])):
        raise ValueError("support constant of the row differs from the witness")
    terms = [(name, Q(c)) for name, c in zip(names, cert["exact"]["coefficients"]) if c != "0"]
    r = Q(cert["exact"]["eliminated_rhs"])
    r_u = r + (uncertified - beta)
    norm = sum(abs(c) for _, c in terms)
    threshold = MATERIAL * max(Q(1), norm)
    checks = []
    for point in points:
        try:
            values = [column_value(name, point) for name, _ in terms]
        except ValueError as exc:
            checks.append({"source": point["source"], "error": str(exc)})
            continue
        if any(v is None for v in values):
            checks.append({"source": point["source"], "error": "no objective value"})
            continue
        activity = sum((c * v for (_, c), v in zip(terms, values)), Q(0))
        checks.append({"source": point["source"],
                       "uncertified_violation": r_u - activity,
                       "certified_violation": r - activity})
    return {"threshold": threshold, "norm": norm, "r": r, "r_uncertified": r_u,
            "points": checks}


def fl(x):
    return None if x is None else float(x)


def summarize_rows(rc):
    evaluated = [p for p in rc["points"] if "error" not in p]
    removed = [p for p in evaluated if p["uncertified_violation"] > rc["threshold"]]
    control = [p for p in evaluated if p["certified_violation"] > rc["threshold"]]
    return {"points": len(rc["points"]), "evaluated": len(evaluated),
            "errors": sorted({p["error"] for p in rc["points"] if "error" in p}),
            "removed": [p["source"] for p in removed],
            "removed_known_witness": any("cases/" in p["source"] for p in removed),
            "certified_row_violated": [p["source"] for p in control],
            "max_uncertified_violation": fl(max((p["uncertified_violation"] for p in evaluated),
                                                default=None)),
            "max_relative_uncertified_violation": fl(max(
                (p["uncertified_violation"] / max(Q(1), rc["norm"]) for p in evaluated),
                default=None)),
            "threshold": fl(rc["threshold"])}


def analyze(contexts, results, incumbents, case_witnesses):
    rows = []
    for i, ctx in enumerate(contexts):
        cut, res = ctx["cut"], results.get(i, {"error": "no worker result"})
        method = cut["support_stats"]["method"]
        certified = Q(cut["support_witness"]["lower_bound"])
        entry = {"part": ctx["part"], "family": ctx["family"], "name": ctx["name"],
                 "run_id": ctx["run_id"], "mode": ctx["mode"], "line": ctx["line"],
                 "cut": ctx["k"], "index": ctx["index"], "method": method,
                 "exact_certificate": method in EXACT_METHODS,
                 "dimension": len(cut["variables"]), "variables": cut["variables"],
                 "sides": [s["source_id"] for s in cut["signed_sides"]],
                 "domain_rows": len(cut["domain_rows"]),
                 "coefficients": cut["coefficients"], "certified": str(certified),
                 "certified_float": float(certified),
                 "certified_minimizer": cut["support_stats"].get("minimizer")}
        if method in EXACT_METHODS:
            exact_support = cut["support_stats"].get("exact_support")
            entry["certified_is_exact_support"] = (exact_support is not None and
                                                   Q(exact_support) == certified)
        if "error" in res:
            entry["error"] = res["error"]
            entry["reconstruction"] = res.get("reconstruction")
            rows.append(entry)
            continue
        entry.update({key: res[key] for key in ("reconstruction", "quadratic", "sample_size",
                                                "u1", "u1_point", "u2", "u2_point", "slsqp")})
        if "minimizer_check" in res:
            entry["minimizer_check"] = res["minimizer_check"]
        scale = MATERIAL * max(Q(1), abs(certified))
        for variant in ("u1", "u2"):
            value = Q(float.fromhex(res[variant]))
            excess = value - certified
            entry[f"{variant}_float"] = float(value)
            entry[f"{variant}_excess"] = str(excess)
            entry[f"{variant}_excess_float"] = float(excess)
            entry[f"{variant}_invalid"] = excess > 0
            entry[f"{variant}_material"] = excess > scale
            if excess > scale:
                points = incumbents.get(ctx["model_key"], [])
                if ctx["model_key"] in case_witnesses:
                    points = points + [case_witnesses[ctx["model_key"]]]
                try:
                    entry[f"{variant}_rows"] = summarize_rows(row_check(cut, value, points))
                except ValueError as exc:
                    entry[f"{variant}_rows"] = {"error": str(exc)}
                check = entry.get("minimizer_check")
                if check and check.get("value") is not None:
                    entry[f"{variant}_witnessed"] = bool(check["feasible"] and
                                                         Q(check["value"]) < value - scale)
        rows.append(entry)
    return rows


def quantile_summary(values):
    values = sorted(values)
    if not values:
        return {"n": 0, "max": None, "median": None}
    return {"n": len(values), "max": float(values[-1]), "median": float(statistics.median(values))}


def part_summary(rows, part_labels):
    summary = {}
    for label in part_labels:
        mine = [r for r in rows if r["part"] == label]
        by_method = {}
        for method in sorted({r["method"] for r in mine}):
            group = [r for r in mine if r["method"] == method and "error" not in r]
            s = {"cuts": len([r for r in mine if r["method"] == method]),
                 "analyzed": len(group),
                 "exact_certificate": method in EXACT_METHODS}
            for v in ("u1", "u2"):
                excess = [Q(r[f"{v}_excess"]) for r in group]
                material = [r for r in group if r[f"{v}_material"]]
                checked = [r for r in material if "error" not in r.get(f"{v}_rows", {})]
                removing = [r for r in checked if r[f"{v}_rows"]["removed"]]
                s[v] = {
                    "exceeds": sum(r[f"{v}_invalid"] for r in group),
                    "material": len(material),
                    "below": sum(e < 0 for e in excess),
                    "equal": sum(e == 0 for e in excess),
                    "max_excess": fl(max(excess, default=None)),
                    "median_positive_excess": fl(statistics.median(
                        sorted(e for e in excess if e > 0))) if any(e > 0 for e in excess) else None,
                    "max_relative_excess": fl(max(
                        (Q(r[f"{v}_excess"]) / max(Q(1), abs(Q(r["certified"]))) for r in group),
                        default=None)),
                    "max_relative_deficit": fl(max(
                        (-Q(r[f"{v}_excess"]) / max(Q(1), abs(Q(r["certified"]))) for r in group
                         if Q(r[f"{v}_excess"]) < 0), default=None)),
                    "witnessed_by_certified_minimizer": sum(bool(r.get(f"{v}_witnessed"))
                                                            for r in material),
                    "row_checks": len(checked),
                    "row_check_errors": len(material) - len(checked),
                    "removing_cuts": len(removing),
                    "removing_models": sorted({r["name"] for r in removing}),
                    "removing_known_witness": sum(r[f"{v}_rows"]["removed_known_witness"]
                                                  for r in checked),
                    "certified_row_violated_cuts": sum(
                        bool(r[f"{v}_rows"]["certified_row_violated"]) for r in checked),
                    "material_models": sorted({r["name"] for r in material}),
                }
            by_method[method] = s
        summary[label] = by_method
    return summary


def family_counts(rows, family, exact):
    """Totals over all parts of one family; 'distinct' identifies a cut by
    (model, block variables, binary64 direction)."""
    group = [r for r in rows if r["family"] == family and r["exact_certificate"] == exact
             and "error" not in r]

    def distinct(selection):
        return len({(r["name"], tuple(r["variables"]), tuple(r["coefficients"])) for r in selection})

    out = {"cuts": len(group), "distinct_cuts": distinct(group),
           "models": len({r["name"] for r in group})}
    for v in ("u1", "u2"):
        material = [r for r in group if r[f"{v}_material"]]
        removing = [r for r in material if r.get(f"{v}_rows", {}).get("removed")]
        out[v] = {"invalid": sum(r[f"{v}_invalid"] for r in group),
                  "material": len(material), "material_distinct": distinct(material),
                  "material_models": sorted({r["name"] for r in material}),
                  "removing": len(removing), "removing_distinct": distinct(removing),
                  "removing_models": sorted({r["name"] for r in removing}),
                  "removing_known_witness": sum(bool(r[f"{v}_rows"].get("removed_known_witness"))
                                                for r in removing),
                  "slsqp_one_iteration": sum(max(x.get("nit", 0) for x in r["slsqp"]) <= 1
                                             for r in material)}
    return out


def census_summary(census):
    out = {}
    for label, entries in census.items():
        differ = [e for e in entries if e["differ"]]
        out[label] = {
            "rows": len(entries), "rows_with_rounded_coefficients": len(differ),
            "safe_export_holds": sum(e["safe"] for e in entries),
            "abs_E_over_rounded_rows": quantile_summary([abs(e["E"]) for e in differ]),
            "relative_abs_E_over_rounded_rows": quantile_summary(
                [abs(e["E"]) / max(Q(1), abs(e["r"])) for e in differ]),
            "nonzero_E_rows": sum(e["E"] != 0 for e in entries),
            "relative_downward_shift": quantile_summary(
                [e["downward_shift"] / max(Q(1), abs(e["r"])) for e in entries]),
        }
    return out


# ----------------------------------------------------------------------------
# Report
# ----------------------------------------------------------------------------

def models(n):
    return f"{n} model" + ("" if n == 1 else "s")


def g(x, digits=3):
    return "-" if x is None else f"{x:.{digits}g}"


def spot_checks(rows):
    """Two MINLPLib cuts and one path-family cut: materially invalid exact
    certificates of distinct models, U2-material first, largest excess first."""
    def pick(family, count):
        def removes(r):
            return any(r.get(f"{v}_rows", {}).get("removed") for v in ("u1", "u2"))
        pool = sorted((r for r in rows if r["family"] == family and r["exact_certificate"]
                       and r.get("u1_material")),
                      key=lambda r: (not r.get("u2_material"), not removes(r),
                                     -r["u2_excess_float" if r.get("u2_material") else "u1_excess_float"]))
        chosen, models = [], set()
        for r in pool:
            if len(chosen) == count:
                break
            if r["name"] not in models:
                chosen.append(r)
                models.add(r["name"])
        return chosen
    return pick("minlplib", 2) + pick("path", 1)


def write_markdown(path, meta, rows, summary, census, contexts):
    lines = []
    w = lines.append
    w("# Part U: what certification buys (offline ablation)")
    w("")
    w(f"Generated {meta['generated_utc']} by `verification/ablation_uncertified.py` "
      "(campaign-v4-protocol.md, Amendment 1, Part U). No solver was run. "
      "Machine-readable data: `ablation-uncertified.json`.")
    w("")
    w("## Inputs")
    w("")
    w("| Part | Family | Record file SHA-256 (first 16) | Snapshot integration.py SHA-256 (first 16) | Cuts recorded | Cuts analyzed |")
    w("|---|---|---|---|---|---|")
    for p in meta["parts"]:
        w(f"| {p['label']} | {p['family']} | {p['records_sha256'][:16]} | "
          f"{p['integration_sha256'][:16]} | {p['cuts_recorded']} | {p['cuts_analyzed']} |")
    w("")
    s = meta["sample"]
    w(f"Path-family sample: `random.Random({s['seed']}).sample(range({s['population']}), "
      f"{s['size']})` over the concatenated cut list of {', '.join(s['parts'])} "
      "(file order, then cut order within a record), processed in sorted order.")
    w("")
    w("## Key counts")
    w("")
    w("Counts are per recorded cut: a cut recorded in several runs (seeds, modes, parts) counts "
      "each time; 'distinct' identifies a cut by (model, block variables, binary64 direction).")
    w("")
    names = {"minlplib": "MINLPLib parts", "path": "Path-family sample"}
    for fam in ("minlplib", "path"):
        k = meta["key_counts"].get(f"{fam}/exact")
        if not k or not k["cuts"]:
            continue
        w(f"- **{names[fam]}, exact certificates** ({k['cuts']} cuts, {k['distinct_cuts']} distinct, "
          f"{k['models']} models).")
        for v in ("u1", "u2"):
            x = k[v]
            names_ = (f": {', '.join(x['removing_models'])}" if fam == "minlplib" and x["removing_models"] else "")
            witness = (f"; {x['removing_known_witness']} of them remove the known optimal witness"
                       if fam == "path" else "")
            w(f"  {v.upper()}: exceeds the certified minimum for {x['invalid']} cuts, materially for "
              f"{x['material']} ({x['material_distinct']} distinct, {models(len(x['material_models']))}). "
              f"{x['removing']} materially invalid cuts ({x['removing_distinct']} distinct) would remove "
              f"a recorded feasible point, in {models(len(x['removing_models']))}{names_}{witness}.")
        w(f"  Of the {k['u2']['material']} U2-materially invalid cuts, {k['u2']['slsqp_one_iteration']} "
          "had every SLSQP run stop after at most one iteration (all runs reported success).")
    k = meta["key_counts"].get("minlplib/lower")
    if k and k["cuts"]:
        w(f"- **MINLPLib parts, lower-bound certificates** (Bernstein, Arb; {k['cuts']} cuts, "
          f"{models(k['models'])}): U1 exceeds the certified bound materially for {k['u1']['material']}, "
          f"U2 for {k['u2']['material']}; not counted as invalid. The uncertified row removes a "
          f"recorded feasible point for {k['u1']['removing']} cuts with U1 "
          f"({', '.join(k['u1']['removing_models']) or 'none'}) and {k['u2']['removing']} with U2; "
          "such a removal shows directly that the uncertified constant exceeds the true minimum.")
    w("")
    w("## Method as implemented")
    w("")
    for item in meta["method"]:
        w(f"- {item}")
    w("")
    errors = [r for r in rows if "error" in r]
    rec_fail = [r for r in rows if "error" not in r and not all(r["reconstruction"].values())]
    w(f"Reconstruction: for {len(rows) - len(errors) - len(rec_fail)} of {len(rows)} analyzed cuts "
      "the reconstructed block (features, symbols, box, domain rows, direction) gives exactly the "
      "model binding stored in the support witness (`_prepare` of the snapshot), the feature "
      "strings round-trip, and the recorded box is binary64-exact. "
      f"Worker errors: {len(errors)}; binding mismatches: {len(rec_fail)}.")
    exact_rows = [r for r in rows if r["exact_certificate"]]
    w(f"For {sum(bool(r.get('certified_is_exact_support')) for r in exact_rows)} of "
      f"{len(exact_rows)} exact-certificate cuts, the certified value (`support_witness.lower_bound`) "
      "equals the recorded exact minimum (`support_stats.exact_support`).")
    if errors:
        w("")
        w("Worker errors:")
        for r in errors[:20]:
            w(f"- {r['part']} {r['name']} line {r['line']} cut {r['cut']}: {r['error']}")
    w("")

    w("## Exact certificates: invalid uncertified constants")
    w("")
    w("Counts of cuts whose uncertified constant exceeds the certified exact minimum "
      "(invalid) and exceeds it by more than 1e-6*max(1,|value|) (materially invalid). "
      "`=`: the constant equals the exact minimum; `<`: it lies below it (binary64 evaluation "
      "rounding at or near the minimizer, or an SLSQP point within the row tolerance); the last "
      "column gives the largest such deficit relative to max(1,|value|).")
    w("")
    w("| Part | Method | Cuts | U1 invalid | U1 material | U1 = | U1 < | U1 max excess | U2 invalid | U2 material | U2 = | U2 < | U2 max excess | max rel. deficit U1 / U2 |")
    w("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    totals = {}
    for label, by_method in summary.items():
        for method, s in by_method.items():
            if not s["exact_certificate"]:
                continue
            fam = next(p["family"] for p in meta["parts"] if p["label"] == label)
            t = totals.setdefault(fam, collections.Counter())
            t["cuts"] += s["analyzed"]
            for v in ("u1", "u2"):
                t[f"{v}_exceeds"] += s[v]["exceeds"]
                t[f"{v}_material"] += s[v]["material"]
            w(f"| {label} | {method} | {s['analyzed']} | {s['u1']['exceeds']} | {s['u1']['material']} | "
              f"{s['u1']['equal']} | {s['u1']['below']} | {g(s['u1']['max_excess'])} | "
              f"{s['u2']['exceeds']} | {s['u2']['material']} | {s['u2']['equal']} | "
              f"{s['u2']['below']} | {g(s['u2']['max_excess'])} | "
              f"{g(s['u1']['max_relative_deficit'])} / {g(s['u2']['max_relative_deficit'])} |")
    for fam, t in totals.items():
        w(f"| **all {fam}** | exact | {t['cuts']} | {t['u1_exceeds']} | {t['u1_material']} | | | | "
          f"{t['u2_exceeds']} | {t['u2_material']} | | | | |")
    w("")
    w("## Exact certificates: would the uncertified cut remove a recorded feasible point?")
    w("")
    w("For each materially invalid cut, the eliminated row with the uncertified constant is "
      "evaluated exactly at every recorded incumbent of the same model (and at the known "
      "optimal witness of the case file, where one exists). `Removing` counts cuts violated "
      "by more than 1e-6*max(1,||c||_1) at one or more of these points. `Witnessed` counts "
      "materially invalid cuts for which the recorded certified minimizer is exactly feasible "
      "and its exact objective value lies below the uncertified constant by more than the "
      "material tolerance (an explicit feasible counterexample to the uncertified support "
      "inequality, independent of the oracle's proof). `Control` counts cuts whose certified "
      "row is violated by more than the tolerance at one of the points.")
    w("")
    w("| Part | Variant | Material | Witnessed | Rows checked | Removing | Models removing / material | Known witness removed | Control |")
    w("|---|---|---|---|---|---|---|---|---|")
    for label, by_method in summary.items():
        for method, s in by_method.items():
            if not s["exact_certificate"]:
                continue
            for v in ("u1", "u2"):
                x = s[v]
                w(f"| {label} | {v.upper()} | {x['material']} | {x['witnessed_by_certified_minimizer']} | "
                  f"{x['row_checks']} | {x['removing_cuts']} | {len(x['removing_models'])} / "
                  f"{len(x['material_models'])} | {x['removing_known_witness']} | "
                  f"{x['certified_row_violated_cuts']} |")
    w("")
    for fam in ("minlplib", "path"):
        for v in ("u1", "u2"):
            removing = sorted({r["name"] for r in rows if r["family"] == fam and r["exact_certificate"]
                               and r.get(f"{v}_material") and r.get(f"{v}_rows", {}).get("removed")})
            ncuts = sum(1 for r in rows if r["family"] == fam and r["exact_certificate"]
                        and r.get(f"{v}_material") and r.get(f"{v}_rows", {}).get("removed"))
            w(f"- {fam}, {v.upper()}: {ncuts} cuts would remove a recorded feasible point, "
              f"in {models(len(removing))}" + (f": {', '.join(removing)}." if removing and fam == "minlplib" else "."))
    w("")
    w("Incumbents available per model with a materially invalid cut:")
    w("")
    per_model = {}
    for r in rows:
        if r["exact_certificate"] and r.get("u1_material") and "error" not in r.get("u1_rows", {"error": 1}):
            per_model.setdefault((r["family"], r["name"]), r["u1_rows"]["points"])
    for fam in ("minlplib", "path"):
        counts = [n for (f, _), n in per_model.items() if f == fam]
        if counts:
            w(f"- {fam}: {len(counts)} models; points per model min {min(counts)}, "
              f"median {statistics.median(counts)}, max {max(counts)}.")
    w("")

    w("## Largest excesses (exact certificates)")
    w("")
    for fam in ("minlplib", "path"):
        for v in ("u1", "u2"):
            pool = sorted((r for r in rows if r["family"] == fam and r["exact_certificate"]
                           and r.get(f"{v}_material")), key=lambda r: -r[f"{v}_excess_float"])[:10]
            if not pool:
                continue
            w(f"**{fam}, {v.upper()}** (top {len(pool)})")
            w("")
            w("| Model | Part | Run | Cut | d | Rows | Sides | Certified value | Uncertified | Excess | Removes incumbent |")
            w("|---|---|---|---|---|---|---|---|---|---|---|")
            for r in pool:
                rc = r.get(f"{v}_rows", {})
                w(f"| {r['name']} | {r['part']} | {r['run_id']} | {r['cut']} | {r['dimension']} | "
                  f"{r['domain_rows']} | {len(r['sides'])} | {g(r['certified_float'], 10)} | "
                  f"{g(r[f'{v}_float'], 10)} | {g(r[f'{v}_excess_float'])} | "
                  f"{len(rc.get('removed', []))}/{rc.get('points', '-')} |")
            w("")

    w("## Lower-bound certificates (Bernstein, Arb)")
    w("")
    w("These values are certified lower bounds, not minima: the separator only asks them "
      "to reach the separation target. An excess is therefore not evidence of invalidity, "
      "and these cuts are not counted as invalid above. The incumbent test is still applied "
      "to cuts with a material excess.")
    w("")
    w("| Part | Method | Cuts | U1 > bound | U1 material | U1 max excess | U1 removing incumbent | U2 > bound | U2 material | U2 max excess | U2 removing incumbent |")
    w("|---|---|---|---|---|---|---|---|---|---|---|")
    for label, by_method in summary.items():
        for method, s in by_method.items():
            if s["exact_certificate"]:
                continue
            w(f"| {label} | {method} | {s['analyzed']} | {s['u1']['exceeds']} | {s['u1']['material']} | "
              f"{g(s['u1']['max_excess'])} | {s['u1']['removing_cuts']} | {s['u2']['exceeds']} | "
              f"{s['u2']['material']} | {g(s['u2']['max_excess'])} | {s['u2']['removing_cuts']} |")
    w("")

    w("## Exported rows and the bound correction E")
    w("")
    w("Over every recorded cut (not only the sample). `Rounded` counts rows whose binary64 "
      "coefficients differ from the exact eliminated rational row. E is the correction "
      "`box_compensation` of Proposition 'Safe export' (E <= 0); `|E|/max(1,|r|)` is relative "
      "to the exact eliminated right-hand side. `Safe` counts rows with exported rhs <= r + E "
      "in exact arithmetic. The last column is the further downward rounding of the exported "
      "right-hand side, relative.")
    w("")
    w("| Part | Rows | Rounded | Nonzero E | Safe | max abs(E) | median abs(E) (rounded rows) | max rel. abs(E) | median rel. abs(E) | max rel. rhs rounding |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    for label, c in census.items():
        a, rel, shift = c["abs_E_over_rounded_rows"], c["relative_abs_E_over_rounded_rows"], c["relative_downward_shift"]
        w(f"| {label} | {c['rows']} | {c['rows_with_rounded_coefficients']} | {c['nonzero_E_rows']} | "
          f"{c['safe_export_holds']} | {g(a['max'])} | {g(a['median'])} | {g(rel['max'])} | "
          f"{g(rel['median'])} | {g(shift['max'])} |")
    w("")

    w("## Spot checks")
    w("")
    for r in spot_checks(rows):
        cut = contexts[r["index_in_contexts"]]["cut"]
        d = r["dimension"]
        w(f"### {r['name']} ({r['part']}, run {r['run_id']}, cut {r['cut']}, {r['method']})")
        w("")
        w(f"- Block variables {cut['symbols']}, box {cut['box']}.")
        w(f"- Features g: {cut['features'][d:]}.")
        w(f"- Signed sides: {[s['source_id'] for s in cut['signed_sides']]}.")
        w(f"- Domain rows (a, rhs; a.u <= rhs): "
          f"{[(row['coefficients'], row['rhs']) for row in cut['domain_rows']] or 'none'}.")
        w(f"- Direction a = {cut['coefficients'][:d]}, lambda = {cut['coefficients'][d:]}.")
        w(f"- U1 (sample minimum over {r['sample_size']} samples) = {r['u1_float']!r} at u = {r['u1_point']}.")
        w(f"- U2 (best of U1 and {len(r['slsqp'])} SLSQP runs) = {r['u2_float']!r} at u = {r['u2_point']}; "
          f"SLSQP statuses {[s.get('status') for s in r['slsqp']]}, accepted {[s['accepted'] for s in r['slsqp']]}.")
        w(f"- Certified minimum = {r['certified']} = {r['certified_float']!r}, "
          f"minimizer {r['certified_minimizer']} = {[float(Q(v)) for v in r['certified_minimizer']]}.")
        mc = r.get("minimizer_check", {})
        w(f"- Exact objective at the certified minimizer = {mc.get('value')}; minimizer exactly feasible: "
          f"{mc.get('feasible')}.")
        w(f"- Excess U1 = {r['u1_excess_float']:.6g}, U2 = {r['u2_excess_float']:.6g} "
          f"(material tolerance {float(MATERIAL * max(Q(1), abs(Q(r['certified'])))):.3g}).")
        for v in ("u1", "u2"):
            rc = r.get(f"{v}_rows")
            if rc and "error" not in rc:
                w(f"- {v.upper()} row: violated beyond {rc['threshold']:.3g} at {len(rc['removed'])} of "
                  f"{rc['evaluated']} points (max violation {g(rc['max_uncertified_violation'])}); "
                  f"certified row violated at {len(rc['certified_row_violated'])}.")
        w("")
    path.write_text("\n".join(lines) + "\n")


def jsonable(x):
    if isinstance(x, Q):
        return str(x)
    if isinstance(x, dict):
        return {k: jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jsonable(v) for v in x]
    return x


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--minlplib", nargs="*", default=[], help="run dirs or records.jsonl (all cuts)")
    parser.add_argument("--path", nargs="*", default=[], help="path-family run dirs or records.jsonl (sample)")
    parser.add_argument("--sample-size", type=int, default=1000)
    parser.add_argument("--sample-seed", type=int, default=0)
    parser.add_argument("--workers", type=int, default=MAX_WORKERS)
    parser.add_argument("--chunk", type=int, default=150)
    parser.add_argument("--out-md", type=Path, default=HERE.parent / "evidence" / "ablation-uncertified.md")
    parser.add_argument("--out-json", type=Path, default=HERE.parent / "evidence" / "ablation-uncertified.json")
    parser.add_argument("--worker", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.worker:
        worker_main(args.worker)
        return
    started = time.time()
    parts = [Part(a, "minlplib") for a in args.minlplib] + [Part(a, "path") for a in args.path]
    labels = [p.label for p in parts]
    if len(set(labels)) != len(labels):
        raise SystemExit(f"part labels must be unique: {labels}")
    by_label = {p.label: p for p in parts}
    incumbents, case_witnesses, census = {}, {}, {}
    contexts, meta_parts = [], []

    # Pass 1: every file; MINLPLib cuts kept, path cuts indexed.
    path_refs = []
    for part in parts:
        refs = []
        keep = (lambda i: True) if part.family == "minlplib" else (lambda i: False)
        kept, digest = scan(part, keep, refs, incumbents, case_witnesses, census)
        for ctx in kept:
            ctx["family"] = part.family
        contexts.extend(kept)
        if part.family == "path":
            path_refs.extend(refs)
        meta_parts.append({"label": part.label, "family": part.family,
                           "records": str(part.records), "records_sha256": digest,
                           "snapshot": str(part.snapshot),
                           "integration_sha256": part.integration_sha256,
                           "cuts_recorded": len(refs), "cuts_analyzed": len(kept)})
        print(f"[scan] {part.label}: {len(refs)} cuts", file=sys.stderr, flush=True)

    # Path-family sample over the concatenated list, then pass 2 to extract.
    size = min(args.sample_size, len(path_refs))
    sample = sorted(random.Random(args.sample_seed).sample(range(len(path_refs)), size))
    wanted = {}
    for i in sample:
        label, line, k = path_refs[i]
        wanted.setdefault(label, set()).add((line, k))
    for part in parts:
        if part.family != "path":
            continue
        refs = []
        chosen = wanted.get(part.label, set())
        kept, _ = scan(part, lambda i, refs=refs: (refs[i][1], refs[i][2]) in chosen,
                       refs, None, None, None)
        offset = sum(m["cuts_recorded"] for m in meta_parts
                     if m["family"] == "path" and labels.index(m["label"]) < labels.index(part.label))
        for ctx in kept:
            ctx["family"] = "path"
            ctx["index"] += offset          # index in the concatenated path list
        contexts.extend(kept)
        next(m for m in meta_parts if m["label"] == part.label)["cuts_analyzed"] = len(kept)
    for i, ctx in enumerate(contexts):
        ctx["index_in_contexts"] = i
    print(f"[sample] {size} path-family cuts of {len(path_refs)}; "
          f"{len(contexts)} cuts to analyze", file=sys.stderr, flush=True)

    results = run_workers(contexts, by_label, args.workers, args.chunk)
    rows = analyze(contexts, results, incumbents, case_witnesses)
    for row, ctx in zip(rows, contexts):
        row["index_in_contexts"] = ctx["index_in_contexts"]
    summary = part_summary(rows, labels)
    census_out = census_summary(census)
    key_counts = {f"{fam}/{'exact' if exact else 'lower'}": family_counts(rows, fam, exact)
                  for fam in ("minlplib", "path") for exact in (True, False)}
    meta = {
        "protocol": "campaign-v4-protocol.md, Amendment 1, Part U",
        "key_counts": key_counts,
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "elapsed_seconds": round(time.time() - started, 1),
        "command": [sys.executable, *sys.argv],
        "parts": meta_parts,
        "sample": {"seed": args.sample_seed, "size": size, "population": len(path_refs),
                   "parts": [p.label for p in parts if p.family == "path"],
                   "call": f"random.Random({args.sample_seed}).sample(range({len(path_refs)}), {size})",
                   "indices": sample},
        "incumbents_per_model": {k: len(v) for k, v in incumbents.items()},
        "case_witnesses": {k: v["source"] for k, v in case_witnesses.items()},
        "method": [
            "Sample set: `solver.integration._sample(block, Config(**record['config']))` of the run's "
            "own snapshot (the routine behind the direction LP `propose_direction`): "
            "`np.linspace` grids with `grid_1d` = 33 points in 1D, `grid_2d` = 7 per axis in 2D and "
            "3 per axis for d = 3, 4, filtered by the domain rows (tolerance 1e-12*max(1,|rhs|)), plus "
            "the exact vertices of box and domain rows (`theory.quadratic_polytope.polytope_vertices`) "
            "and their centroid for quadratic blocks within the face budget. Sample values come from "
            "`solver.integration._evaluate` (SymPy lambdify, NumPy binary64). Exchange samples "
            "(certified minimizers added later by the separator) are excluded.",
            "Block: features, symbols, box, domain rows and the binary64 direction (a, lambda) as "
            "recorded; the reconstruction is accepted only if the snapshot's `solver.certified._prepare` "
            "reproduces the model binding stored in the support witness. `quadratic` is recomputed "
            "as in `discover` (every side polynomial of total degree <= 2).",
            "U1 = min over the sample of `sample @ (a, lambda)` in binary64.",
            f"U2 = min(U1, SLSQP values): `scipy.optimize.minimize(method='SLSQP')` from the "
            f"{SLSQP_STARTS} best samples (stable sort), bounds = block box, inequality constraints "
            f"= domain rows (with their exact Jacobian), analytic objective gradient (SymPy), "
            f"default tolerances, maxiter {SLSQP_MAXITER}; the final point is clipped to the box and "
            f"accepted if every domain row holds within {ROW_TOL:g}*max(1,|rhs|); its value is "
            "re-evaluated with `_evaluate` in binary64.",
            "Comparison in exact rational arithmetic with `support_witness.lower_bound`. Invalid: "
            "U > value; materially invalid: U - value > 1e-6*max(1,|value|). Exact certificates: "
            f"{', '.join(EXACT_METHODS)}; Bernstein and Arb are lower bounds and reported separately.",
            "Uncertified row: c^T v >= r + (U - beta), with c = `row_certificate.exact.coefficients`, "
            "r = `exact.eliminated_rhs` and beta = the recorded binary64 support constant "
            "(`binding.support.rhs`), i.e. exactly U - sum_r lambda_r b_r. Columns `x<i>` map to "
            "`original_values[i]` (the record's `column_names` are checked to be `v<i>` in the same "
            "order); the column `objective_epigraph` takes the incumbent's objective value "
            "(`primal_check.objective`, else `primal`; for a case witness `known_optimum_exact`).",
            "Incumbents: every record (any part, mode, seed) of the same model (same `model_sha256`) "
            "with `original_values` whose `primal_check.passed` is true, plus the case file's "
            "`known_witness_exact` when present. Removal: violation > 1e-6*max(1,||c||_1), exact.",
        ],
    }
    out = {"meta": meta, "summary": summary, "export_census": census_out,
           "spot_checks": [{"part": r["part"], "line": r["line"], "cut": r["cut"]}
                           for r in spot_checks(rows)],
           "cuts": [{k: v for k, v in r.items() if k != "index_in_contexts"} for r in rows]}
    args.out_json.write_text(json.dumps(jsonable(out), indent=1, allow_nan=False))
    write_markdown(args.out_md, meta, rows, summary, census_out, contexts)
    print(json.dumps(jsonable({"summary": summary, "export_census": census_out}), indent=1))


if __name__ == "__main__":
    main()
