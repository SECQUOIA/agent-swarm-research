#!/usr/bin/env python3
"""Part 5U3 of campaign-v5-protocol.md: a numerical global solve instead of a certificate.

Offline; no SCIP solve. For every recorded cut with an exact certificate
(quadratic polytope, polygon or star oracle) in the given MINLPLib parts, and
for the same random sample of path-family cuts as Part U
(``ablation_uncertified.py``), the support problem

    min a^T u + lambda^T g(u)   over the block box and the affine domain rows

for the recorded binary64 direction (a, lambda) is solved with Gurobi
(gurobipy 13.0.3; NonConvex=2, Threads=1, Seed=0, TimeLimit=10 s,
OutputFlag=0; all tolerances at their defaults: MIPGap 1e-4, MIPGapAbs 1e-10,
FeasibilityTol 1e-6, OptimalityTol 1e-6). The objective is the exact rational
expansion sum_k fl(c_k) g_k(u) (SymPy, domain QQ; every feature must have
total degree <= 2), and each monomial coefficient is then rounded to the
nearest binary64 number. Box bounds and domain rows are rounded the same way
(they are binary64-exact in the records; this is checked and reported). The
expansion is checked against the exact problem stored in the certificate
(``support_witness.proof.quadratic.problem``). Three constants replace the
certified support value:

U3   Gurobi's best bound (ObjBound);
U3p  Gurobi's objective value (ObjVal), the value of its best feasible point;
U3s  U3 - 1e-6*max(1,|U3|), evaluated in binary64 (a fixed safety shift).

Everything else is Part U, imported read-only from ``ablation_uncertified``:
record scanning, the block reconstruction check (the run snapshot's
``solver.certified._prepare`` must reproduce the binding stored in the
support witness), the path-family sample (``random.Random(seed).sample`` over
the same concatenated cut list, same parts in the same order), the exact
comparison of the binary64 constant with ``support_witness.lower_bound``
(invalid: U > value; materially invalid: U - value > 1e-6*max(1,|value|)),
the incumbent pools and the removal test (a recorded feasible point violates
the uncertified row by more than 1e-6*max(1,||c||_1)), with the certified row
as control. A missing or infinite constant (no bound, no feasible point) is
reported as 'no value' and is never counted as invalid.

The selected cuts and the sample indices are compared with the Part U output
(``--part-u-json``) and the result of the comparison is reported.

Usage (the protocol run)::

    export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
    PY=/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python
    E=/workspace/minlp-notes/paper-certified-support-cuts/experiments
    $PY ablation_global_solve.py \\
      --minlplib $E/v3/runs/partA-full $E/v3/runs/partA-root $E/v3/runs/partB \\
                 $E/v3d/runs/partA-root-rowdir $E/v3d/runs/partB-root-rowdir \\
                 $E/v4/runs/partB2 $E/v4/runs/partD-root $E/v4/runs/partD-full \\
      --path $E/v3/runs/partC $E/v3d/runs/partC-rowdir $E/v4/runs/partC2 \\
             $E/v4/runs/partC3 $E/v4/runs/partC4 --workers 6

Worker processes (at most six, each single-threaded, bytecode writing
disabled) import the snapshot code of each run directory read-only.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import ablation_uncertified as U  # noqa: E402  (Part U, read-only; sets the thread variables)

import argparse  # noqa: E402
import collections  # noqa: E402
from concurrent.futures import ThreadPoolExecutor  # noqa: E402
from fractions import Fraction as Q  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import os  # noqa: E402
import random  # noqa: E402
import shlex  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402

MAX_WORKERS = 6
GUROBI_PARAMS = {"NonConvex": 2, "Threads": 1, "Seed": 0, "TimeLimit": 10.0, "OutputFlag": 0}
REPORTED_PARAMS = ("NonConvex", "Threads", "Seed", "TimeLimit", "MIPGap", "MIPGapAbs",
                   "FeasibilityTol", "OptimalityTol", "IntFeasTol", "Presolve", "Method")
SHIFT = 1e-6                     # U3s = U3 - SHIFT*max(1,|U3|)
VARIANTS = ("u3", "u3p", "u3s")
VARIANT_NAMES = {"u3": "U3", "u3p": "U3p", "u3s": "U3s"}
QUANTILES = (("min", 0.0), ("q01", 0.01), ("q05", 0.05), ("q25", 0.25), ("median", 0.5),
             ("q75", 0.75), ("q95", 0.95), ("q99", 0.99), ("max", 1.0))
STATUS = {1: "LOADED", 2: "OPTIMAL", 3: "INFEASIBLE", 4: "INF_OR_UNBD", 5: "UNBOUNDED",
          6: "CUTOFF", 7: "ITERATION_LIMIT", 8: "NODE_LIMIT", 9: "TIME_LIMIT",
          10: "SOLUTION_LIMIT", 11: "INTERRUPTED", 12: "NUMERIC", 13: "SUBOPTIMAL",
          14: "INPROGRESS", 15: "USER_OBJ_LIMIT", 16: "WORK_LIMIT", 17: "MEM_LIMIT"}


# ----------------------------------------------------------------------------
# Worker: block reconstruction, exact expansion, Gurobi solve (one snapshot)
# ----------------------------------------------------------------------------

def monomial_order(d):
    """Constant, x_i, then x_i x_j (i <= j): the order of the certificate's problem."""
    def unit(*indices):
        powers = [0] * d
        for i in indices:
            powers[i] += 1
        return tuple(powers)
    return ([unit()] + [unit(i) for i in range(d)] +
            [unit(i, j) for i in range(d) for j in range(i, d)])


def finite_or_str(x):
    return x if x is None or math.isfinite(x) else str(x)


def worker_main(snapshot):
    # Gurobi's C library writes license messages to fd 1; keep the JSON channel clean.
    channel = os.fdopen(os.dup(1), "w")
    os.dup2(2, 1)
    source = (Path(snapshot) / U.TOPIC).resolve()
    sys.path.insert(0, str(source))
    import gurobipy as gp
    from gurobipy import GRB
    import numpy as np
    import sympy as sp

    from solver.certified import _prepare

    frozen = [m for name, m in list(sys.modules.items())
              if name.split(".")[0] in ("solver", "theory")]
    outside = [m.__file__ for m in frozen if getattr(m, "__file__", None)
               and not Path(m.__file__).resolve().is_relative_to(source.parent)]
    if outside:
        raise RuntimeError(f"modules imported from outside the snapshot: {outside}")

    env = gp.Env(empty=True)
    env.setParam("OutputFlag", 0)
    env.start()

    def new_model():
        m = gp.Model(env=env)
        for name, value in GUROBI_PARAMS.items():
            m.setParam(name, value)
        return m

    probe = new_model()
    meta = {"gurobi_version": ".".join(map(str, gp.gurobi.version())),
            "params": {p: probe.getParamInfo(p)[2] for p in REPORTED_PARAMS}}
    probe.dispose()

    def solve(item):
        res = {"id": item["id"]}
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
        res["reconstruction"] = {
            "binding_matches_witness": binding == item["binding"],
            "feature_strings_roundtrip": [str(f) for f in features] == item["features"],
            "box_binary64_exact": all(Q(b) == q for pair, pairq in zip(box, box_q)
                                      for b, q in zip(pair, pairq)),
            "rows_binary64_exact": all(Q(float(v)) == v for a, r in rows for v in (*a, r)),
        }
        if not all(f.is_polynomial(*syms) and sp.Poly(f, *syms).total_degree() <= 2
                   for f in features):
            res["error"] = "a feature is not a polynomial of total degree <= 2"
            return res

        # Exact expansion of sum_k fl(c_k) g_k, then binary64 rounding per monomial.
        expression = sp.Add(*(sp.Rational(Q(c).numerator, Q(c).denominator) * f
                              for c, f in zip(coefficients, features)))
        terms = {powers: Q(int(c.p), int(c.q))
                 for powers, c in sp.Poly(expression, *syms, domain=sp.QQ).terms() if c != 0}
        order = monomial_order(d)
        if set(terms) - set(order):
            res["error"] = "expansion has a monomial of degree > 2"
            return res
        exact = [terms.get(powers, Q(0)) for powers in order]
        problem = item.get("problem")
        res["matches_certificate_problem"] = None if problem is None else bool(
            [Q(c) for c in problem["coefficients"]] == exact
            and [(Q(lo), Q(hi)) for lo, hi in problem["bounds"]] == box_q
            and [(tuple(Q(v) for v in row[:-1]), Q(row[-1])) for row in problem["rows"]]
            == list(rows))
        rounded = [float(c) for c in exact]
        quad = [(i, j) for i in range(d) for j in range(i, d)]
        hessian = np.zeros((d, d))
        for (i, j), c in zip(quad, rounded[1 + d:]):
            if i == j:
                hessian[i, i] = 2 * c
            else:
                hessian[i, j] = hessian[j, i] = c
        res["size"] = {
            "linear_terms": sum(c != 0 for c in rounded[1:1 + d]),
            "quadratic_terms": sum(c != 0 for c in rounded[1 + d:]),
            "rounded_coefficients": sum(Q(r) != c for r, c in zip(rounded, exact)),
            "min_hessian_eigenvalue": float(np.linalg.eigvalsh(hessian).min()),
            "max_box_width": max(hi - lo for lo, hi in box),
        }

        m = new_model()
        x = [m.addVar(lb=lo, ub=hi, name=f"u{k}") for k, (lo, hi) in enumerate(box)]
        objective = gp.QuadExpr()
        objective.addConstant(rounded[0])
        for i in range(d):
            if rounded[1 + i] != 0:
                objective.addTerms(rounded[1 + i], x[i])
        for (i, j), c in zip(quad, rounded[1 + d:]):
            if c != 0:
                objective.addTerms(c, x[i], x[j])
        m.setObjective(objective, GRB.MINIMIZE)
        for k, (a, rhs) in enumerate(rows):
            m.addLConstr(gp.LinExpr([float(v) for v in a], x), GRB.LESS_EQUAL, float(rhs),
                         name=f"row{k}")
        m.optimize()

        def attr(name):
            try:
                return float(getattr(m, name))
            except (gp.GurobiError, AttributeError):
                return None
        bound = attr("ObjBound")
        value = attr("ObjVal") if m.SolCount > 0 else None
        res["gurobi"] = {
            "status": int(m.Status), "runtime": float(m.Runtime), "nodes": float(m.NodeCount),
            "solutions": int(m.SolCount), "is_mip": int(m.IsMIP), "is_qp": int(m.IsQP),
            "simplex_iterations": float(m.IterCount), "barrier_iterations": int(m.BarIterCount),
            "mip_gap": finite_or_str(attr("MIPGap")) if m.IsMIP else None,
            "obj_bound": None if bound is None else bound.hex(),
            "obj_val": None if value is None else value.hex(),
            "x": [float(v.X) for v in x] if m.SolCount > 0 else None,
        }
        m.dispose()

        # Exact objective at the recorded certified minimizer (as in Part U).
        if item.get("minimizer") is not None:
            point = [Q(v) for v in item["minimizer"]]
            total = sum((c * math.prod(p ** e for p, e in zip(point, powers))
                         for powers, c in terms.items()), Q(0))
            feasible = (all(lo <= v <= hi for v, (lo, hi) in zip(point, box_q)) and
                        all(sum(a_k * v for a_k, v in zip(a, point)) <= r for a, r in rows))
            res["minimizer_check"] = {"value": str(total), "feasible": feasible}
        return res

    items = json.load(sys.stdin)
    results = []
    for item in items:
        try:
            results.append(solve(item))
        except Exception as exc:  # recorded per cut and reported
            results.append({"id": item["id"], "error": f"{type(exc).__name__}: {exc}"})
    env.dispose()
    json.dump({"meta": meta, "results": results}, channel)
    channel.flush()


# ----------------------------------------------------------------------------
# Main process: selection (as Part U), workers, exact comparisons, report
# ----------------------------------------------------------------------------

def select(parts, sample_size, sample_seed):
    """Part U's two passes (ablation_uncertified.main), keeping exact certificates."""
    labels = [p.label for p in parts]
    incumbents, case_witnesses = {}, {}
    contexts, meta_parts, path_refs = [], [], []
    lower_bound_cuts = 0
    for part in parts:
        refs = []
        keep = (lambda i: True) if part.family == "minlplib" else (lambda i: False)
        kept, digest = U.scan(part, keep, refs, incumbents, case_witnesses, None)
        exact = [ctx for ctx in kept if ctx["cut"]["support_stats"]["method"] in U.EXACT_METHODS]
        lower_bound_cuts += len(kept) - len(exact)
        for ctx in exact:
            ctx["family"] = part.family
        contexts.extend(exact)
        if part.family == "path":
            path_refs.extend(refs)
        meta_parts.append({"label": part.label, "family": part.family,
                           "records": str(part.records), "records_sha256": digest,
                           "snapshot": str(part.snapshot),
                           "integration_sha256": part.integration_sha256,
                           "cuts_recorded": len(refs), "cuts_analyzed": len(exact)})
        print(f"[scan] {part.label}: {len(refs)} cuts, {len(exact)} kept", file=sys.stderr,
              flush=True)
    size = min(sample_size, len(path_refs))
    sample = sorted(random.Random(sample_seed).sample(range(len(path_refs)), size))
    wanted = {}
    for i in sample:
        label, line, k = path_refs[i]
        wanted.setdefault(label, set()).add((line, k))
    for part in parts:
        if part.family != "path":
            continue
        refs = []
        chosen = wanted.get(part.label, set())
        kept, _ = U.scan(part, lambda i, refs=refs: (refs[i][1], refs[i][2]) in chosen,
                         refs, None, None, None)
        offset = sum(m["cuts_recorded"] for m in meta_parts
                     if m["family"] == "path" and labels.index(m["label"]) < labels.index(part.label))
        exact = [ctx for ctx in kept if ctx["cut"]["support_stats"]["method"] in U.EXACT_METHODS]
        for ctx in exact:
            ctx["family"] = "path"
            ctx["index"] += offset          # index in the concatenated path list
        contexts.extend(exact)
        next(m for m in meta_parts if m["label"] == part.label)["cuts_analyzed"] = len(exact)
    sample_meta = {"seed": sample_seed, "size": size, "population": len(path_refs),
                   "parts": [p.label for p in parts if p.family == "path"],
                   "call": f"random.Random({sample_seed}).sample(range({len(path_refs)}), {size})",
                   "indices": sample}
    return contexts, meta_parts, sample_meta, incumbents, case_witnesses, lower_bound_cuts


def worker_item(i, ctx):
    cut = ctx["cut"]
    quadratic = (cut["support_witness"].get("proof") or {}).get("quadratic") or {}
    return {"id": i, "symbols": cut["symbols"], "variables": cut["variables"],
            "features": cut["features"], "box": cut["box"], "domain_rows": cut["domain_rows"],
            "coefficients": cut["coefficients"], "binding": cut["support_witness"]["model"],
            "minimizer": cut["support_stats"].get("minimizer"),
            "problem": quadratic.get("problem")}


def run_workers(contexts, parts, workers, chunk):
    by_snapshot = {}
    for i, ctx in enumerate(contexts):
        by_snapshot.setdefault(str(parts[ctx["part"]].snapshot), []).append(i)
    jobs = [(snapshot, ids[start:start + chunk]) for snapshot, ids in by_snapshot.items()
            for start in range(0, len(ids), chunk)]
    env = {**os.environ, **U.THREAD_ENV, "PYTHONDONTWRITEBYTECODE": "1"}
    done_count = [0]

    def run(job):
        snapshot, ids = job
        payload = json.dumps([worker_item(i, contexts[i]) for i in ids])
        done = subprocess.run([sys.executable, "-B", str(Path(__file__).resolve()),
                               "--worker", snapshot], input=payload, capture_output=True,
                              text=True, env=env, cwd="/tmp", check=False)
        if done.returncode != 0:
            raise RuntimeError(f"worker failed ({snapshot}): {done.stderr[-2000:]}")
        out = json.loads(done.stdout)
        done_count[0] += len(ids)
        print(f"[solve] {done_count[0]}/{len(contexts)}", file=sys.stderr, flush=True)
        return out

    results, metas = {}, []
    with ThreadPoolExecutor(max_workers=min(workers, MAX_WORKERS)) as pool:
        for out in pool.map(run, jobs):
            metas.append(out["meta"])
            for result in out["results"]:
                results[result["id"]] = result
    if any(m != metas[0] for m in metas):
        raise RuntimeError(f"workers report different Gurobi versions or parameters: {metas}")
    return results, metas[0], len(jobs)


def constants(gurobi):
    u3 = None if gurobi["obj_bound"] is None else float.fromhex(gurobi["obj_bound"])
    u3p = None if gurobi["obj_val"] is None else float.fromhex(gurobi["obj_val"])
    u3s = (u3 - SHIFT * max(1.0, abs(u3))) if u3 is not None and math.isfinite(u3) else None
    return {"u3": u3, "u3p": u3p, "u3s": u3s}


def analyze(contexts, results, incumbents, case_witnesses, part_u):
    rows = []
    for i, ctx in enumerate(contexts):
        cut, res = ctx["cut"], results.get(i, {"error": "no worker result"})
        certified = Q(cut["support_witness"]["lower_bound"])
        entry = {"part": ctx["part"], "family": ctx["family"], "name": ctx["name"],
                 "run_id": ctx["run_id"], "mode": ctx["mode"], "line": ctx["line"],
                 "cut": ctx["k"], "index": ctx["index"], "method": cut["support_stats"]["method"],
                 "dimension": len(cut["variables"]), "variables": cut["variables"],
                 "domain_rows": len(cut["domain_rows"]), "coefficients": cut["coefficients"],
                 "certified": str(certified), "certified_float": float(certified),
                 "certified_minimizer": cut["support_stats"].get("minimizer")}
        prior = part_u.get((ctx["part"], ctx["line"], ctx["k"]))
        if prior is not None:
            entry["part_u"] = {v: prior.get(f"{v}_material") for v in ("u1", "u2")}
        for key in ("reconstruction", "matches_certificate_problem", "size", "gurobi",
                    "minimizer_check"):
            if key in res:
                entry[key] = res[key]
        if "error" in res:
            entry["error"] = res["error"]
            rows.append(entry)
            continue
        scale = U.MATERIAL * max(Q(1), abs(certified))
        for v, x in constants(res["gurobi"]).items():
            if x is None or not math.isfinite(x):
                entry[f"{v}_none"] = True
                entry[v] = None if x is None else str(x)
                continue
            value = Q(x)
            excess = value - certified
            entry.update({v: x.hex(), f"{v}_float": x, f"{v}_excess": str(excess),
                          f"{v}_excess_float": float(excess),
                          f"{v}_relative_excess_float": float(excess / max(Q(1), abs(certified))),
                          f"{v}_invalid": excess > 0, f"{v}_material": excess > scale})
            if excess > scale:
                points = incumbents.get(ctx["model_key"], [])
                if ctx["model_key"] in case_witnesses:
                    points = points + [case_witnesses[ctx["model_key"]]]
                try:
                    entry[f"{v}_rows"] = U.summarize_rows(U.row_check(cut, value, points))
                except ValueError as exc:
                    entry[f"{v}_rows"] = {"error": str(exc)}
                check = entry.get("minimizer_check")
                if check and check.get("value") is not None:
                    entry[f"{v}_witnessed"] = bool(check["feasible"] and
                                                   Q(check["value"]) < value - scale)
        rows.append(entry)
    return rows


def distinct(selection):
    """Part U's key for a distinct cut: (model, block variables, binary64 direction)."""
    return len({(r["name"], tuple(r["variables"]), tuple(r["coefficients"])) for r in selection})


def distribution(values):
    """Nearest-rank quantiles of exact values, reported as floats."""
    values = sorted(values)
    if not values:
        return None
    n = len(values)
    return {"n": n, **{key: float(values[max(0, math.ceil(q * n) - 1)]) for key, q in QUANTILES}}


def group_summary(group):
    ok = [r for r in group if "error" not in r]
    s = {"cuts": len(group), "analyzed": len(ok), "errors": len(group) - len(ok),
         "distinct": distinct(ok), "models": len({r["name"] for r in ok})}
    for v in VARIANTS:
        valued = [r for r in ok if not r.get(f"{v}_none")]
        excess = [Q(r[f"{v}_excess"]) for r in valued]
        relative = [Q(r[f"{v}_excess"]) / max(Q(1), abs(Q(r["certified"]))) for r in valued]
        material = [r for r in valued if r[f"{v}_material"]]
        checked = [r for r in material if "error" not in r[f"{v}_rows"]]
        removing = [r for r in checked if r[f"{v}_rows"]["removed"]]
        s[v] = {
            "no_value": len(ok) - len(valued),
            "invalid": sum(e > 0 for e in excess),
            "equal": sum(e == 0 for e in excess),
            "below": sum(e < 0 for e in excess),
            "material": len(material), "material_distinct": distinct(material),
            "material_models": sorted({r["name"] for r in material}),
            "witnessed_by_certified_minimizer": sum(bool(r.get(f"{v}_witnessed")) for r in material),
            "row_checks": len(checked), "row_check_errors": len(material) - len(checked),
            "removing": len(removing), "removing_distinct": distinct(removing),
            "removing_models": sorted({r["name"] for r in removing}),
            "removing_known_witness": sum(r[f"{v}_rows"]["removed_known_witness"] for r in removing),
            "control": sum(bool(r[f"{v}_rows"]["certified_row_violated"]) for r in checked),
            "excess": distribution(excess),
            "relative_excess": distribution(relative),
            "abs_excess": distribution([abs(e) for e in excess]),
            "abs_relative_excess": distribution([abs(e) for e in relative]),
        }
    return s


def solver_summary(group):
    ok = [r for r in group if "gurobi" in r]
    if not ok:
        return {}
    runtime = sorted(r["gurobi"]["runtime"] for r in ok)
    nodes = sorted(r["gurobi"]["nodes"] for r in ok)

    def pick(values, q):
        return values[max(0, math.ceil(q * len(values)) - 1)]
    return {"solved": len(ok),
            "status": dict(collections.Counter(STATUS.get(r["gurobi"]["status"], str(r["gurobi"]["status"]))
                                               for r in ok)),
            "spatial_branch_and_bound": sum(r["gurobi"]["is_mip"] for r in ok),
            "no_bound": sum(r["gurobi"]["obj_bound"] is None
                            or not math.isfinite(float.fromhex(r["gurobi"]["obj_bound"])) for r in ok),
            "no_solution": sum(r["gurobi"]["obj_val"] is None for r in ok),
            "runtime": {"total": sum(runtime), "median": pick(runtime, 0.5),
                        "q95": pick(runtime, 0.95), "max": runtime[-1]},
            "nodes": {"total": sum(nodes), "median": pick(nodes, 0.5), "q95": pick(nodes, 0.95),
                      "max": nodes[-1], "with_more_than_one_node": sum(n > 1 for n in nodes)}}


def sanity(group, gap_abs):
    """U3 = ObjBound against the certified value (expected: U3 <= value + MIPGapAbs)."""
    valued = [r for r in group if "error" not in r and not r.get("u3_none")]
    excess = [(r, Q(r["u3_excess"])) for r in valued]
    above = sorted((r for r, e in excess if e > 0), key=lambda r: -r["u3_relative_excess_float"])
    by_model = {}
    for r in above:
        by_model.setdefault(r["name"], []).append(r)
    return {"cuts": len(valued),
            "u3_leq_certified": sum(e <= 0 for _, e in excess),
            "u3_leq_certified_plus_mipgapabs": sum(e <= Q(gap_abs) for _, e in excess),
            "u3_above_certified": len(above),
            "u3_above_certified_plus_mipgapabs": sum(e > Q(gap_abs) for _, e in excess),
            "u3_above_certified_material": sum(r["u3_material"] for r in above),
            "above_by_model": {name: {
                "cuts": len(group), "distinct": distinct(group),
                "dimensions": sorted({r["dimension"] for r in group}),
                "domain_rows": sorted({r["domain_rows"] for r in group}),
                "quadratic_terms": sorted({r["size"]["quadratic_terms"] for r in group}),
                "nonconvex": sum(r["size"]["min_hessian_eigenvalue"] < 0 for r in group),
                "statuses": dict(collections.Counter(STATUS.get(r["gurobi"]["status"]) for r in group)),
                "max_excess": max(r["u3_excess_float"] for r in group),
                "max_relative_excess": max(r["u3_relative_excess_float"] for r in group)}
                for name, group in sorted(by_model.items(), key=lambda kv: (-len(kv[1]), kv[0]))},
            "above": [{"part": r["part"], "name": r["name"], "run_id": r["run_id"],
                       "line": r["line"], "cut": r["cut"], "dimension": r["dimension"],
                       "domain_rows": r["domain_rows"], **r["size"],
                       "status": STATUS.get(r["gurobi"]["status"]),
                       "nodes": r["gurobi"]["nodes"], "runtime": r["gurobi"]["runtime"],
                       "spatial_branch_and_bound": r["gurobi"]["is_mip"],
                       "certified": r["certified"], "certified_float": r["certified_float"],
                       "u3_float": r["u3_float"], "excess": r["u3_excess_float"],
                       "relative_excess": r["u3_relative_excess_float"],
                       "material": r["u3_material"]} for r in above]}


# ----------------------------------------------------------------------------
# Report
# ----------------------------------------------------------------------------

g = U.g
models = U.models


def dm(n, d, m):
    return f"{n} ({d}, {m})"


def write_markdown(path, out):
    meta, summary, rows = out["meta"], out["summary"], out["cuts"]
    params = meta["gurobi"]["params"]
    lines = []
    w = lines.append
    w("# Part 5U3: a numerical global solve (Gurobi) instead of a certificate")
    w("")
    w(f"Generated {meta['generated_utc']} by `verification/ablation_global_solve.py` "
      "(campaign-v5-protocol.md, Part 5U3). Offline: no SCIP solve; Gurobi solves only the "
      "support subproblems. Machine-readable data: `ablation-global-solve.json`. "
      "Part U (`ablation_uncertified.py`) is imported read-only.")
    w("")
    w("## Command")
    w("")
    w("```bash")
    w("export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1")
    w(shlex.join(meta["command"]))
    w("```")
    w("")
    w(f"Elapsed {meta['elapsed_seconds']} s wall time; {meta['worker_jobs']} worker jobs on at most "
      f"{meta['worker_processes']} single-threaded worker processes. Gurobi {meta['gurobi']['gurobi_version']}; "
      "parameter values read back from each model: "
      + ", ".join(f"{k} {v:g}" if isinstance(v, float) else f"{k} {v}" for k, v in params.items()) + ".")
    w("")
    w("## Inputs and selection")
    w("")
    w("| Part | Family | Record file SHA-256 (first 16) | Snapshot integration.py SHA-256 (first 16) | Cuts recorded | Cuts analyzed |")
    w("|---|---|---|---|---|---|")
    for p in meta["parts"]:
        w(f"| {p['label']} | {p['family']} | {p['records_sha256'][:16]} | "
          f"{p['integration_sha256'][:16]} | {p['cuts_recorded']} | {p['cuts_analyzed']} |")
    w("")
    s = meta["sample"]
    x = meta["part_u_crosscheck"]
    w(f"MINLPLib parts: every recorded cut with an exact certificate ({meta['lower_bound_cuts_skipped']} "
      "cuts with lower-bound certificates, Arb and Bernstein, are skipped). Path family: "
      f"`{s['call']}` over the concatenated cut list of {', '.join(s['parts'])} (file order, then cut "
      "order within a record), as in Part U.")
    w("")
    w(f"Cross-check with `{x['file']}`: same exact-certificate cuts in the same order (part, line, "
      f"cut, certified value): **{x['same_cuts']}** ({x['cuts_here']} here, {x['cuts_part_u']} there); "
      f"same sample indices: **{x['same_sample_indices']}**.")
    w("")
    rec = meta["reconstruction"]
    w(f"Reconstruction: {rec['ok']} of {rec['cuts']} cuts reproduce the binding stored in the support "
      "witness with the snapshot's `_prepare`, round-trip their feature strings and have binary64-exact "
      f"boxes; domain rows binary64-exact for {rec['rows_binary64_exact']}; the exact expansion equals "
      f"the certificate's stored problem (coefficients, bounds, rows) for {rec['matches_certificate_problem']} "
      f"of {rec['with_certificate_problem']} cuts. Cuts whose binary64 objective differs from the exact "
      f"expansion (one or more coefficients rounded): {rec['rounded_objective']}. Worker errors: "
      f"{rec['errors']}. Certified value equals `support_stats.exact_support` for "
      f"{rec['certified_is_exact_support']} cuts.")
    w("")
    w("## Method as implemented")
    w("")
    for item in meta["method"]:
        w(f"- {item}")
    w("")

    w("## Key counts")
    w("")
    w("Counts are per recorded cut; '(d, m)' gives distinct cuts (model, block variables, binary64 "
      "direction) and models. inv: constant > certified value; mat: excess > 1e-6*max(1,|value|); "
      "rem: materially invalid cuts whose row is violated by more than 1e-6*max(1,||c||_1) at a "
      "recorded feasible point; KW: rem cuts that remove the known optimal witness; ctl: "
      "row-checked cuts whose certified row is violated at one of the same points.")
    w("")
    names = {"minlplib": "MINLPLib parts", "path": "Path-family sample", "all": "All cuts"}
    for fam in ("minlplib", "path", "all"):
        k = summary["families"].get(fam) if fam != "all" else summary["all"]
        if not k or not k["cuts"]:
            continue
        w(f"- **{names[fam]}** ({k['cuts']} cuts, {k['distinct']} distinct, {models(k['models'])}).")
        for v in VARIANTS:
            c = k[v]
            model_names = (f" ({', '.join(c['removing_models'])})"
                           if c["removing_models"] and fam == "minlplib" else "")
            w(f"  {VARIANT_NAMES[v]}: invalid {c['invalid']}, materially invalid {c['material']} "
              f"({c['material_distinct']} distinct, {models(len(c['material_models']))}), removing "
              f"{c['removing']} ({c['removing_distinct']} distinct, {models(len(c['removing_models']))})"
              f"{model_names}, known witness removed {c['removing_known_witness']}, control "
              f"{c['control']}, no value {c['no_value']}.")
    w("")

    w("## Counts per part")
    w("")
    for v in VARIANTS:
        w(f"### {VARIANT_NAMES[v]}")
        w("")
        w("| Part | Cuts (d, m) | inv | = | < | mat (d, m) | witnessed | rem (d, m) | KW | ctl | no value | max excess | max rel. excess |")
        w("|---|---|---:|---:|---:|---|---:|---|---:|---:|---:|---:|---:|")
        groups = list(summary["parts"].items()) + [
            (f"**all {fam}**", summary["families"][fam]) for fam in ("minlplib", "path")
            if fam in summary["families"]] + [("**all**", summary["all"])]
        for label, k in groups:
            c = k[v]
            e, r = c["excess"] or {}, c["relative_excess"] or {}
            w(f"| {label} | {dm(k['analyzed'], k['distinct'], k['models'])} | {c['invalid']} | "
              f"{c['equal']} | {c['below']} | "
              f"{dm(c['material'], c['material_distinct'], len(c['material_models']))} | "
              f"{c['witnessed_by_certified_minimizer']} | "
              f"{dm(c['removing'], c['removing_distinct'], len(c['removing_models']))} | "
              f"{c['removing_known_witness']} | {c['control']} | {c['no_value']} | "
              f"{g(e.get('max'))} | {g(r.get('max'))} |")
        w("")

    w("## Comparison with Part U (same cuts)")
    w("")
    w("U1 and U2 from `ablation-uncertified.json` (`meta.key_counts`); U3, U3p, U3s from this run.")
    w("")
    w("| Family | Constant | inv | mat (d, m) | rem (d, m) | KW |")
    w("|---|---|---:|---|---|---:|")
    for fam in ("minlplib", "path"):
        prior = meta["part_u_key_counts"].get(f"{fam}/exact")
        k = summary["families"].get(fam)
        if not k:
            continue
        if prior:
            for v in ("u1", "u2"):
                c = prior[v]
                w(f"| {fam} | {v.upper()} (Part U) | {c['invalid']} | "
                  f"{dm(c['material'], c['material_distinct'], len(c['material_models']))} | "
                  f"{dm(c['removing'], c['removing_distinct'], len(c['removing_models']))} | "
                  f"{c['removing_known_witness']} |")
        for v in VARIANTS:
            c = k[v]
            w(f"| {fam} | {VARIANT_NAMES[v]} | {c['invalid']} | "
              f"{dm(c['material'], c['material_distinct'], len(c['material_models']))} | "
              f"{dm(c['removing'], c['removing_distinct'], len(c['removing_models']))} | "
              f"{c['removing_known_witness']} |")
    w("")

    w("## Errors U - certified value")
    w("")
    w("Exact differences between the binary64 constant and the certified value, as floats; "
      "relative = (U - value)/max(1,|value|). Nearest-rank quantiles over the cuts with a value.")
    w("")
    w("| Family | Constant | Kind | n | min | q01 | q05 | q25 | median | q75 | q95 | q99 | max |")
    w("|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for fam in ("minlplib", "path", "all"):
        k = summary["families"].get(fam) if fam != "all" else summary["all"]
        if not k:
            continue
        for v in VARIANTS:
            for kind in ("excess", "relative_excess", "abs_excess"):
                dist = k[v][kind]
                if not dist:
                    continue
                w(f"| {fam} | {VARIANT_NAMES[v]} | {kind.replace('_', ' ')} | {dist['n']} | "
                  + " | ".join(g(dist[key]) for key, _ in QUANTILES) + " |")
    w("")

    w("## Gurobi statuses, times and nodes")
    w("")
    w("| Part | Solved | Statuses | Spatial B&B | No bound | No solution | Runtime total / median / q95 / max (s) | Nodes median / q95 / max | > 1 node |")
    w("|---|---:|---|---:|---:|---:|---|---|---:|")
    solver_groups = list(summary["solver"]["parts"].items()) + [
        (f"**all {fam}**", summary["solver"]["families"][fam]) for fam in ("minlplib", "path")
        if fam in summary["solver"]["families"]] + [("**all**", summary["solver"]["all"])]
    for label, k in solver_groups:
        if not k:
            continue
        rt, nd = k["runtime"], k["nodes"]
        w(f"| {label} | {k['solved']} | "
          + ", ".join(f"{name} {n}" for name, n in sorted(k["status"].items())) +
          f" | {k['spatial_branch_and_bound']} | {k['no_bound']} | {k['no_solution']} | "
          f"{rt['total']:.2f} / {rt['median']:.2g} / {rt['q95']:.2g} / {rt['max']:.2g} | "
          f"{nd['median']:g} / {nd['q95']:g} / {nd['max']:g} | {nd['with_more_than_one_node']} |")
    w("")
    w("'Spatial B&B': models with Gurobi's `IsMIP` = 1 (nonconvex objective, solved by spatial "
      "branch and bound); the others are LPs or convex QPs solved directly (for these, ObjBound is "
      "the dual value of the continuous solve). Runtime is Gurobi's `Runtime`; the host is shared, "
      "times are descriptive.")
    w("")

    sn = out["sanity"]
    w("## Sanity check: U3 = ObjBound against the certified value")
    w("")
    w(f"Gurobi's absolute gap tolerance MIPGapAbs = {params['MIPGapAbs']:g}. Over {sn['all']['cuts']} "
      f"cuts with a bound: U3 <= certified value for {sn['all']['u3_leq_certified']}; "
      f"U3 <= certified value + MIPGapAbs for {sn['all']['u3_leq_certified_plus_mipgapabs']}; "
      f"U3 > certified value for {sn['all']['u3_above_certified']} "
      f"(by more than MIPGapAbs: {sn['all']['u3_above_certified_plus_mipgapabs']}; materially: "
      f"{sn['all']['u3_above_certified_material']}).")
    w("")
    w("| Family | Cuts | U3 <= value | U3 <= value + MIPGapAbs | U3 > value | U3 > value + MIPGapAbs | material |")
    w("|---|---:|---:|---:|---:|---:|---:|")
    for fam in ("minlplib", "path", "all"):
        k = sn.get(fam)
        if k:
            w(f"| {fam} | {k['cuts']} | {k['u3_leq_certified']} | {k['u3_leq_certified_plus_mipgapabs']} | "
              f"{k['u3_above_certified']} | {k['u3_above_certified_plus_mipgapabs']} | "
              f"{k['u3_above_certified_material']} |")
    w("")
    above = sn["all"]["above"]
    if above:
        w("Cuts with U3 > certified value, by model (d: block dimension; rows: domain rows; q: nonzero "
          "quadratic terms; nonconvex: min Hessian eigenvalue < 0):")
        w("")
        w("| Model | Cuts | Distinct | d | rows | q | nonconvex | Statuses | max excess | max rel. excess |")
        w("|---|---:|---:|---|---|---|---:|---|---:|---:|")
        for name, k in sn["all"]["above_by_model"].items():
            w(f"| {name} | {k['cuts']} | {k['distinct']} | {k['dimensions']} | {k['domain_rows']} | "
              f"{k['quadratic_terms']} | {k['nonconvex']} | "
              + ", ".join(f"{s} {n}" for s, n in k["statuses"].items())
              + f" | {g(k['max_excess'])} | {g(k['max_relative_excess'])} |")
        w("")
        shown = above[:40]
        w(f"Individual cuts ({len(shown)} of {len(above)}, largest relative excess first; the full list "
          "is `sanity.all.above` in the JSON):")
        w("")
        w("| Model | Part | Run | Cut | d | rows | q | min eig. | Status | Nodes | Certified value | U3 | Excess | Rel. excess |")
        w("|---|---|---|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|")
        for r in shown:
            w(f"| {r['name']} | {r['part']} | {r['run_id']} | {r['cut']} | {r['dimension']} | "
              f"{r['domain_rows']} | {r['quadratic_terms']} | {g(r['min_hessian_eigenvalue'])} | "
              f"{r['status']} | {r['nodes']:g} | {g(r['certified_float'], 12)} | {g(r['u3_float'], 12)} | "
              f"{g(r['excess'])} | {g(r['relative_excess'])} |")
        w("")

    w("## Notable cases")
    w("")
    for v in VARIANTS:
        material = [r for r in rows if r.get(f"{v}_material")]
        w(f"### {VARIANT_NAMES[v]}: materially invalid cuts ({len(material)})")
        w("")
        if not material:
            w("None.")
            w("")
            continue
        per_model = collections.Counter(r["name"] for r in material)
        w("By model: " + ", ".join(f"{name} {n}" for name, n in per_model.most_common()) + ".")
        w("")
        shown = sorted(material, key=lambda r: -r[f"{v}_relative_excess_float"])[:25]
        w(f"Largest relative excesses ({len(shown)} of {len(material)}):")
        w("")
        w("| Model | Part | Run | Cut | d | rows | q | Status | Nodes | Gap | Certified value | Constant | Excess | Rel. excess | Removes | Part U U1/U2 mat. |")
        w("|---|---|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---|---|")
        for r in shown:
            rc = r.get(f"{v}_rows", {})
            gu = r["gurobi"]
            pu = r.get("part_u", {})
            w(f"| {r['name']} | {r['part']} | {r['run_id']} | {r['cut']} | {r['dimension']} | "
              f"{r['domain_rows']} | {r['size']['quadratic_terms']} | {STATUS.get(gu['status'])} | "
              f"{gu['nodes']:g} | {gu['mip_gap'] if isinstance(gu['mip_gap'], str) else g(gu['mip_gap'])} | "
              f"{g(r['certified_float'], 12)} | {g(r[f'{v}_float'], 12)} | {g(r[f'{v}_excess_float'])} | "
              f"{g(r[f'{v}_relative_excess_float'])} | {len(rc.get('removed', []))}/{rc.get('points', '-')} | "
              f"{pu.get('u1')}/{pu.get('u2')} |")
        w("")
    odd = [r for r in rows if "gurobi" in r and r["gurobi"]["status"] != 2]
    w(f"### Gurobi status other than OPTIMAL ({len(odd)})")
    w("")
    if odd:
        w("| Model | Part | Run | Cut | d | rows | q | Status | Runtime | Nodes | Certified value | U3 | U3p |")
        w("|---|---|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|")
        for r in odd[:40]:
            gu = r["gurobi"]
            w(f"| {r['name']} | {r['part']} | {r['run_id']} | {r['cut']} | {r['dimension']} | "
              f"{r['domain_rows']} | {r['size']['quadratic_terms']} | {STATUS.get(gu['status'])} | "
              f"{gu['runtime']:.3g} | {gu['nodes']:g} | {g(r['certified_float'], 12)} | "
              f"{g(r.get('u3_float'), 12)} | {g(r.get('u3p_float'), 12)} |")
    else:
        w("None.")
    w("")
    errors = [r for r in rows if "error" in r]
    if errors:
        w(f"### Worker errors ({len(errors)})")
        w("")
        for r in errors[:20]:
            w(f"- {r['part']} {r['name']} line {r['line']} cut {r['cut']}: {r['error']}")
        w("")
    path.write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--minlplib", nargs="*", default=[], help="run dirs or records.jsonl (all exact cuts)")
    parser.add_argument("--path", nargs="*", default=[], help="path-family run dirs or records.jsonl (sample)")
    parser.add_argument("--sample-size", type=int, default=1000)
    parser.add_argument("--sample-seed", type=int, default=0)
    parser.add_argument("--workers", type=int, default=MAX_WORKERS)
    parser.add_argument("--chunk", type=int, default=100)
    parser.add_argument("--part-u-json", type=Path,
                        default=HERE.parent / "evidence" / "ablation-uncertified.json")
    parser.add_argument("--out-md", type=Path, default=HERE.parent / "evidence" / "ablation-global-solve.md")
    parser.add_argument("--out-json", type=Path, default=HERE.parent / "evidence" / "ablation-global-solve.json")
    parser.add_argument("--worker", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.worker:
        worker_main(args.worker)
        return
    started = time.time()
    parts = [U.Part(a, "minlplib") for a in args.minlplib] + [U.Part(a, "path") for a in args.path]
    labels = [p.label for p in parts]
    if len(set(labels)) != len(labels):
        raise SystemExit(f"part labels must be unique: {labels}")
    contexts, meta_parts, sample_meta, incumbents, case_witnesses, skipped = select(
        parts, args.sample_size, args.sample_seed)
    print(f"[select] {len(contexts)} cuts to solve", file=sys.stderr, flush=True)

    part_u_data = json.loads(args.part_u_json.read_text())
    part_u_exact = [c for c in part_u_data["cuts"] if c["exact_certificate"]]
    part_u = {(c["part"], c["line"], c["cut"]): c for c in part_u_exact}
    here_keys = [(ctx["part"], ctx["line"], ctx["k"], str(Q(ctx["cut"]["support_witness"]["lower_bound"])))
                 for ctx in contexts]
    crosscheck = {"file": str(args.part_u_json.name),
                  "cuts_here": len(contexts), "cuts_part_u": len(part_u_exact),
                  "same_cuts": here_keys == [(c["part"], c["line"], c["cut"], c["certified"])
                                             for c in part_u_exact],
                  "same_sample_indices": sample_meta["indices"] == part_u_data["meta"]["sample"]["indices"]}

    results, worker_meta, jobs = run_workers(contexts, {p.label: p for p in parts}, args.workers, args.chunk)
    rows = analyze(contexts, results, incumbents, case_witnesses, part_u)
    gap_abs = worker_meta["params"]["MIPGapAbs"]
    families = sorted({r["family"] for r in rows})
    summary = {"parts": {label: group_summary([r for r in rows if r["part"] == label])
                         for label in labels},
               "families": {fam: group_summary([r for r in rows if r["family"] == fam]) for fam in families},
               "all": group_summary(rows),
               "solver": {"parts": {label: solver_summary([r for r in rows if r["part"] == label])
                                    for label in labels},
                          "families": {fam: solver_summary([r for r in rows if r["family"] == fam])
                                       for fam in families},
                          "all": solver_summary(rows)}}
    sanity_out = {fam: sanity([r for r in rows if r["family"] == fam], gap_abs) for fam in families}
    sanity_out["all"] = sanity(rows, gap_abs)
    ok = [r for r in rows if "error" not in r]
    reconstruction = {
        "cuts": len(rows), "errors": len(rows) - len(ok),
        "ok": sum(all(r["reconstruction"][k] for k in ("binding_matches_witness",
                                                      "feature_strings_roundtrip",
                                                      "box_binary64_exact")) for r in ok),
        "rows_binary64_exact": sum(r["reconstruction"]["rows_binary64_exact"] for r in ok),
        "with_certificate_problem": sum(r["matches_certificate_problem"] is not None for r in ok),
        "matches_certificate_problem": sum(r["matches_certificate_problem"] is True for r in ok),
        "rounded_objective": sum(r["size"]["rounded_coefficients"] > 0 for r in ok),
        "certified_is_exact_support": sum(
            ctx["cut"]["support_stats"].get("exact_support") is not None
            and Q(ctx["cut"]["support_stats"]["exact_support"]) == Q(ctx["cut"]["support_witness"]["lower_bound"])
            for ctx in contexts),
    }
    meta = {
        "protocol": "campaign-v5-protocol.md, Part 5U3",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "elapsed_seconds": round(time.time() - started, 1),
        "command": [sys.executable, *sys.argv],
        "worker_processes": min(args.workers, MAX_WORKERS), "worker_jobs": jobs,
        "gurobi": worker_meta, "gurobi_params_set": GUROBI_PARAMS,
        "parts": meta_parts, "sample": sample_meta,
        "lower_bound_cuts_skipped": skipped,
        "part_u_crosscheck": crosscheck,
        "part_u_key_counts": part_u_data["meta"]["key_counts"],
        "reconstruction": reconstruction,
        "incumbents_per_model": {k: len(v) for k, v in incumbents.items()},
        "case_witnesses": {k: v["source"] for k, v in case_witnesses.items()},
        "method": [
            "Selection, incumbents and case witnesses: `ablation_uncertified.scan` and the two passes of "
            "`ablation_uncertified.main`, keeping cuts whose `support_stats.method` is an exact "
            f"certificate ({', '.join(U.EXACT_METHODS)}).",
            "Block: features, symbols, box, domain rows and the binary64 direction (a, lambda) as recorded; "
            "the reconstruction check of Part U (the snapshot's `solver.certified._prepare` reproduces the "
            "support witness's model binding) is repeated in each worker.",
            "Objective: SymPy `Poly(sum_k Rational(fl(c_k)) * g_k, domain=QQ)`; every feature has total "
            "degree <= 2. The exact coefficients (constant, x_i, x_i x_j for i <= j) are compared with the "
            "certificate's `proof.quadratic.problem` and rounded to the nearest binary64 number "
            "(`float(Fraction)`). Box bounds and domain rows are rounded the same way.",
            "Gurobi model: one continuous variable per block variable with the box as bounds, objective "
            "constant + linear terms + quadratic terms (exact zeros omitted) to minimize, one linear row "
            "a.u <= rhs per domain row; parameters "
            + ", ".join(f"{k}={v:g}" if isinstance(v, float) else f"{k}={v}" for k, v in GUROBI_PARAMS.items())
            + ", all others at their defaults. One Gurobi environment per worker job.",
            "Constants: U3 = `ObjBound`, U3p = `ObjVal` (if a solution exists), U3s = U3 - 1e-6*max(1,|U3|) "
            "evaluated in binary64. Missing or infinite constants are 'no value'.",
            "Comparison in exact rational arithmetic between Fraction(constant) and "
            "`support_witness.lower_bound`. Invalid: U > value; materially invalid: "
            "U - value > 1e-6*max(1,|value|).",
            "Removal test (materially invalid cuts only, as in Part U): `ablation_uncertified.row_check` and "
            "`summarize_rows`: the uncertified row c^T v >= r + (U - beta) is evaluated exactly at every "
            "recorded feasible point of the model (pooled by `model_sha256` over all parts given) and the "
            "case file's known witness; removal if the violation exceeds 1e-6*max(1,||c||_1). Control: the "
            "certified row at the same points. Witnessed: the recorded certified minimizer is exactly "
            "feasible and its exact objective lies below the constant by more than the material tolerance.",
        ],
    }
    out = {"meta": meta, "summary": summary, "sanity": sanity_out, "cuts": rows}
    args.out_json.write_text(json.dumps(U.jsonable(out), indent=1, allow_nan=False))
    write_markdown(args.out_md, U.jsonable(out))
    brief = {"crosscheck": crosscheck, "reconstruction": reconstruction,
             "families": {fam: {v: {k: summary["families"][fam][v][k] for k in
                                    ("invalid", "material", "material_distinct", "removing",
                                     "removing_distinct", "removing_known_witness", "control",
                                     "no_value")} for v in VARIANTS} for fam in families},
             "solver": summary["solver"]["all"],
             "sanity": {k: v for k, v in sanity_out["all"].items() if k != "above"}}
    print(json.dumps(U.jsonable(brief), indent=1))


if __name__ == "__main__":
    main()
