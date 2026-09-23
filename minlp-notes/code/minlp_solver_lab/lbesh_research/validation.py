"""Evaluate a witness against a fresh, untransformed Pyomo GDP model.

This checks numerical primal feasibility, not convexity or global optimality.
The caller must supply the original model, before any solver preprocessing.
"""
from __future__ import annotations

import math
import pyomo.environ as pe
from pyomo.core.base.boolean_var import BooleanVarData
from pyomo.gdp import Disjunct, Disjunction

DESCEND = (pe.Block, Disjunct)


def finite(value):
    try:
        value = float(value)
        return value if math.isfinite(value) and abs(value) < 1e300 else None
    except (TypeError, ValueError, OverflowError):
        return None


def capture_witness(model):
    """Extract numeric variables and Boolean truth from solver binary values.

    Pyomo's transformed standalone Booleans may retain their initialization
    while only their associated binary is updated. Resolve that association
    here; validation of externally supplied witnesses remains strict.
    """
    def truth(v):
        binary = v.get_associated_binary()
        if binary is None:
            return None if v.value is None else bool(v.value)
        x = finite(binary.value)
        return bool(round(x)) if x is not None and min(abs(x),abs(x-1)) <= 1e-6 else None
    return {
        "variables": {v.name: finite(v.value) for v in model.component_data_objects(
            pe.Var, active=None, descend_into=DESCEND)},
        "booleans": {v.name: truth(v)
                     for v in model.component_data_objects(
                         pe.BooleanVar, active=None, descend_into=DESCEND)},
    }


def validate_witness(model, witness, *, abs_tol=1e-6, rel_tol=1e-7,
                     integer_tol=1e-6, reported_objective=None):
    """Check domains, fixed values, selected rows, disjunctions and logical rows.

    All numeric variables must be present. Row residuals use the scale of the
    evaluated body and bound. The maximum raw and tolerance-normalized residual
    are retained so that the numerical tolerance remains auditable.
    """
    issues = []
    max_raw = max_scaled = 0.0
    rows_checked = 0
    vals = witness.get("variables", {})
    bools = witness.get("booleans", {})
    fixed_booleans = {v.name: v.value for v in model.component_data_objects(
        pe.BooleanVar, active=None, descend_into=DESCEND) if v.fixed}

    def issue(kind, name, **kw):
        issues.append(dict(kind=kind, name=name, **kw))

    def residual(kind, name, amount, scale=1.0, tolerance=None):
        nonlocal max_raw, max_scaled
        tol = abs_tol + rel_tol * max(1.0, scale) if tolerance is None else tolerance
        amount = max(0.0, amount)
        max_raw = max(max_raw, amount)
        max_scaled = max(max_scaled, amount / tol)
        if amount > tol:
            issue(kind, name, violation=amount, tolerance=tol)

    for v in model.component_data_objects(pe.Var, active=None, descend_into=DESCEND):
        x = finite(vals.get(v.name))
        if x is None:
            issue("missing_or_nonfinite_variable", v.name)
            v.set_value(None)
            continue
        if v.fixed:
            expected = finite(v.value)
            if expected is None:
                issue("undefined_fixed_value", v.name)
            else:
                residual("fixed_value", v.name, abs(x - expected), abs(expected))
        v.set_value(x, skip_validation=True)
        for bound, sign, label in ((v.lb, -1, "lower_bound"), (v.ub, 1, "upper_bound")):
            if bound is not None:
                b = finite(pe.value(bound, exception=False))
                if b is None:
                    issue("nonfinite_bound", v.name)
                else:
                    residual(label, v.name, sign * (x - b), max(abs(x), abs(b)))
        if v.is_integer():
            residual("integrality", v.name, abs(x - round(x)), tolerance=integer_tol)
        elif x not in v.domain:
            # Real interval domains are already checked through lb/ub. Other
            # domains (for example finite sets) require exact membership.
            try:
                continuous = v.domain.get_interval()[2] == 0
            except (AttributeError, TypeError):
                continuous = False
            if not continuous:
                issue("domain", v.name, value=x)

    for v in model.component_data_objects(pe.BooleanVar, active=None, descend_into=DESCEND):
        associated = v.get_associated_binary()
        x = finite(vals.get(associated.name)) if associated is not None else None
        supplied = bools.get(v.name)
        if supplied is not None and not isinstance(supplied, bool):
            issue("invalid_boolean", v.name)
            supplied = None
        # Solvers commonly update only the associated binary. Derive Boolean
        # truth from it, but check a supplied Boolean for consistency.
        inferred = bool(round(x)) if x is not None and abs(x-round(x)) <= integer_tol else None
        truth = inferred if associated is not None else supplied
        if supplied is not None and inferred is not None and supplied != inferred:
            issue("boolean_binary_mismatch", v.name)
        if truth is None:
            issue("missing_boolean", v.name)
        if v.name in fixed_booleans and truth != fixed_booleans[v.name]:
            issue("fixed_boolean", v.name)
        # AutoLinkedBooleanVar.set_value also overwrites its binary. Keep the
        # exact supplied numeric witness for objective and row evaluation.
        BooleanVarData.set_value(v, truth, skip_validation=True)

    def enabled(component):
        if not component.active:
            return False
        block = component.parent_block()
        while block is not None:
            if not block.active:
                return False
            if block.ctype is Disjunct and block.indicator_var.value is not True:
                return False
            block = block.parent_block()
        return True

    for c in model.component_data_objects(pe.Constraint, active=None, descend_into=DESCEND):
        if not enabled(c):
            continue
        rows_checked += 1
        try:
            body = finite(pe.value(c.body, exception=False))
            if body is None:
                raise ValueError("nonfinite body")
            for bound, sign in ((c.lower, -1), (c.upper, 1)):
                if bound is not None:
                    b = finite(pe.value(bound, exception=False))
                    if b is None:
                        raise ValueError("nonfinite bound")
                    residual("constraint", c.name, sign*(body-b), max(abs(body), abs(b)))
        except Exception as exc:
            issue("constraint_evaluation", c.name, error=str(exc))

    for dj in model.component_data_objects(Disjunction, active=None, descend_into=DESCEND):
        if enabled(dj):
            truths = [d.indicator_var.value for d in dj.disjuncts]
            if any(t is None for t in truths) or (sum(t is True for t in truths) != 1
                    if dj.xor else not any(t is True for t in truths)):
                issue("disjunction", dj.name, values=truths, xor=dj.xor)
    for c in model.component_data_objects(pe.LogicalConstraint, active=None, descend_into=DESCEND):
        if enabled(c):
            try:
                if pe.value(c.expr, exception=False) is not True:
                    issue("logical_constraint", c.name)
            except Exception as exc:
                issue("logical_evaluation", c.name, error=str(exc))

    objectives = [o for o in model.component_data_objects(pe.Objective, active=True,
                  descend_into=DESCEND) if enabled(o)]
    objective = None
    sense = None
    if len(objectives) != 1:
        issue("objective_count", "model", count=len(objectives))
    else:
        sense = "minimize" if objectives[0].sense == pe.minimize else "maximize"
        try:
            objective = finite(pe.value(objectives[0].expr, exception=False))
            if objective is None:
                raise ValueError("nonfinite objective")
            if reported_objective is not None:
                reported = finite(reported_objective)
                if reported is None:
                    issue("nonfinite_reported_objective", objectives[0].name)
                else:
                    residual("objective_mismatch", objectives[0].name,
                             abs(objective-reported), max(abs(objective), abs(reported)))
        except Exception as exc:
            issue("objective_evaluation", objectives[0].name, error=str(exc))
    return dict(feasible=not issues, objective=objective, objective_sense=sense,
                issues=issues, rows_checked=rows_checked, max_violation=max_raw,
                max_normalized_violation=max_scaled,
                tolerances=dict(absolute=abs_tol, relative=rel_tol, integrality=integer_tol))
