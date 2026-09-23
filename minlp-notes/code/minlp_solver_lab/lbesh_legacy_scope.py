"""Structural audit of the fixed legacy set; no optimization or model edits.

Only the 27 names in gdp_final.jsonl define the set. Historical outcomes are
not read. Convexity checks inspect oriented expressions independently of the
solver. ``extract`` is used separately to observe actual bound preprocessing.
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import platform
import warnings

import numpy as np
import pyomo.environ as pe
from pyomo.gdp import Disjunct, Disjunction
from pyomo.repn import generate_standard_repn

from gdp_instances import INSTANCES
from lbesh.structure import extract

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def bounds(v):
    return [None if b is None or not math.isfinite(float(b)) else float(b)
            for b in (v.lb, v.ub)]


def quadratic(expr):
    rep = generate_standard_repn(expr, quadratic=True)
    if rep.nonlinear_expr is not None:
        return None
    ids = {id(v): i for i, v in enumerate(rep.quadratic_vars and
           list({id(v): v for pair in rep.quadratic_vars for v in pair}.values()) or [])}
    q = np.zeros((len(ids), len(ids)))
    for (u, v), c in zip(rep.quadratic_vars, rep.quadratic_coefs):
        i, j = ids[id(u)], ids[id(v)]
        q[i, j] += float(c) / (1 if i == j else 2)
        if i != j:
            q[j, i] += float(c) / 2
    eig = float(np.linalg.eigvalsh(q).min()) if len(q) else 0.0
    # These models are diagonal sums of squares. PSD is verified without
    # relying on an eigenvalue tolerance whenever that exact structure holds.
    diagonal_psd = bool(np.count_nonzero(q - np.diag(np.diag(q))) == 0
                        and np.all(np.diag(q) >= 0))
    return rep, eig, diagonal_psd


def certify(expr):
    """Recognize only the convex forms present here; fail on unknown forms."""
    qr = quadratic(expr)
    if qr is not None:
        rep, eig, diagonal_psd = qr
        if rep.is_linear() or rep.is_fixed():
            return [{"form": "affine"}]
        if not diagonal_psd:
            raise ValueError(f"Quadratic lacks exact diagonal-PSD certificate: {expr}")
        return [{"form": "quadratic_diagonal_psd", "min_eigenvalue": eig}]
    typ = type(expr).__name__
    args = expr.args
    if typ in ("SumExpression", "LinearExpression"):
        return [proof for arg in args for proof in certify(arg)]
    if typ in ("ProductExpression", "MonomialTermExpression"):
        for i in (0, 1):
            if pe.is_fixed(args[i]) and float(pe.value(args[i])) >= 0:
                return certify(args[1 - i])
    if typ == "UnaryFunctionExpression" and expr.getname() == "exp":
        assert generate_standard_repn(args[0]).is_linear()
        return [{"form": "positive_exp_affine"}]
    if typ == "DivisionExpression" and pe.is_fixed(args[0]):
        coefficient = float(pe.value(args[0]))
        denominator = args[1]
        assert coefficient > 0 and denominator.is_variable_type()
        return [{"form": "positive_reciprocal", "denominator": denominator.name,
                 "coefficient": coefficient,
                 "raw_denominator_bounds": bounds(denominator),
                 "domain_condition": "denominator > 0"}]
    if typ == "PowExpression" and pe.is_fixed(args[1]) and pe.value(args[1]) == 0.5:
        qr = quadratic(args[0])
        assert qr is not None
        rep, _, diagonal_psd = qr
        assert diagonal_psd and not rep.linear_vars and rep.constant == 0
        return [{"form": "weighted_euclidean_norm", "smooth_at_origin": False,
                 "variables": sorted({v.name for pair in rep.quadratic_vars for v in pair})}]
    raise ValueError(f"Unrecognized expression {typ}: {expr}")


def source_for(name):
    prefix = HERE / "instances"
    if name.startswith("gdplib."):
        short = name.split(".")[1]
        filename = "gdp_small_batch.py" if short == "small_batch" else short + ".py"
        return prefix / "gdplib_src" / "gdplib" / short / filename
    base = prefix / "pyomo_examples_src" / "examples" / "gdp"
    part = name.split(".")[1]
    file = {"circles": "circles/circles.py", "farm_layout": "farm_layout/farm_layout.py",
            "constrained_layout": "constrained_layout/cons_layout_model.py"}.get(part)
    return base / (file or ("small_lit/" + name.split(".")[2] + ".py"))


def audit(name):
    model = INSTANCES[name]()
    original = list(model.component_data_objects(pe.Var, descend_into=(pe.Block, Disjunct)))
    raw_bounds = {v.name: bounds(v) for v in original}
    disjunctions = list(model.component_data_objects(Disjunction, active=True,
                                                   descend_into=(pe.Block, Disjunct)))
    assert all(d.xor for d in disjunctions)
    rows = []
    for c in model.component_data_objects(pe.Constraint, active=True,
                                          descend_into=(pe.Block, Disjunct)):
        rep = generate_standard_repn(c.body)
        nonlinear = not rep.is_linear() and not rep.is_fixed()
        if not nonlinear:
            continue
        assert (c.lower is None) != (c.upper is None), c.name
        expr = c.body if c.upper is not None else -c.body
        ancestor = c.parent_block()
        in_disjunct = False
        while ancestor is not None:
            in_disjunct |= ancestor.ctype is Disjunct
            ancestor = ancestor.parent_block()
        rows.append({"name": c.name, "in_disjunct": in_disjunct,
                     "proof": certify(expr)})
    objs = list(model.component_data_objects(pe.Objective, active=True))
    assert len(objs) == 1
    obj = objs[0]
    objective_proof = certify(obj.expr if obj.sense == pe.minimize else -obj.expr)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        problem = extract(model)
    after = {v.name: bounds(v) for v in original}
    missing = [n for n, b in after.items() if None in b]
    reciprocal = [p for r in rows for p in r["proof"] if p["form"] == "positive_reciprocal"]
    for p in reciprocal:
        p["preprocessed_denominator_bounds"] = after[p["denominator"]]
        assert after[p["denominator"]][0] > 0
    nonsmooth = any(p["form"] == "weighted_euclidean_norm" for p in objective_proof)
    compact_smooth_original = not missing and not nonsmooth
    # Raw source and actual extracted model are kept distinct. An unbounded
    # epigraph is a further compactness gap even if original variables pass.
    bounded_lift = all(None not in bounds(v) for v in problem.variables)
    source = source_for(name)
    data_files = [source.with_suffix(".dat")] if name == "gdplib.batch_processing" else []
    return {
        "instance": name,
        "source": str(source.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "data_file_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in data_files},
        "original_variable_count": len(original),
        "disjunction_count": len(disjunctions),
        "disjunct_count": sum(len(d.disjuncts) for d in disjunctions),
        "all_disjunctions_xor": True,
        "supported_structure_extraction_passed": True,
        "nonlinear_global_constraint_count": sum(not r["in_disjunct"] for r in rows),
        "nonlinear_disjunct_constraint_count": sum(r["in_disjunct"] for r in rows),
        "original_bounds": raw_bounds,
        "preprocessed_original_bounds": after,
        "original_variables_missing_finite_bounds_after_extraction": missing,
        "nonlinear_constraints": rows,
        "objective_proof": objective_proof,
        "all_oriented_rows_and_objective_convex_on_effective_domain": True,
        "raw_box_has_reciprocal_singularity": any(p["raw_denominator_bounds"][0] == 0 for p in reciprocal),
        "effective_box_reciprocals_strictly_positive": all(p["preprocessed_denominator_bounds"][0] > 0 for p in reciprocal),
        "objective_nonsmooth_at_zero_distance": nonsmooth,
        "original_variables_compact_and_smooth_after_extraction": compact_smooth_original,
        "extracted_lift_has_finite_bounds": bounded_lift,
        "smooth_compact_analytic_scope_as_extracted": compact_smooth_original and bounded_lift,
        "needs_epigraph_compactness_argument": problem.epigraph_var is not None,
        "eligible_for_external_numerical_stress_set": True,
        "scope_group": ("compact_smooth_original_variables" if compact_smooth_original
                        else "broader_numerical_stress"),
        "extraction_runtime_warning_count": len(caught),
    }


def main():
    historical = HERE / "results/gdp_final.jsonl"
    names = sorted({json.loads(line)["instance"] for line in historical.read_text().splitlines()})
    assert len(names) == 27
    records = [audit(name) for name in names]
    result = {
        "audit_kind": "structural, no optimization; historical names only",
        "environment": {"python": platform.python_version(),
                        **{p: importlib.metadata.version(p) for p in ("pyomo", "numpy", "sympy")}},
        "selection_file": str(historical.relative_to(ROOT)),
        "selection_sha256": hashlib.sha256(historical.read_bytes()).hexdigest(),
        "registry_sha256": hashlib.sha256((HERE / "gdp_instances.py").read_bytes()).hexdigest(),
        "scope_flag_limit": "Analytic data assumptions only; anchor, epigraph, solver and separation contracts must also hold. No run is certified by this audit.",
        "summary": {"instances": len(records),
                    "convex_on_effective_domain": sum(r["all_oriented_rows_and_objective_convex_on_effective_domain"] for r in records),
                    "compact_smooth_original_variables": sum(r["original_variables_compact_and_smooth_after_extraction"] for r in records),
                    "smooth_compact_analytic_scope_as_extracted": sum(r["smooth_compact_analytic_scope_as_extracted"] for r in records),
                    "nonsmooth_objectives": sum(r["objective_nonsmooth_at_zero_distance"] for r in records),
                    "raw_reciprocal_box_singularities": sum(r["raw_box_has_reciprocal_singularity"] for r in records)},
        "instances": records,
    }
    destination = HERE / "results/lbesh_development/legacy_scope.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result["summary"], indent=2))
    for r in records:
        print(r["instance"], r["scope_group"],
              "full_lift_box=" + str(r["extracted_lift_has_finite_bounds"]))


if __name__ == "__main__":
    main()
