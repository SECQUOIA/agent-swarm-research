"""Targeted soundness regressions; sampled agreement is never a certificate."""
from copy import deepcopy
from fractions import Fraction as Q
import json
import math

import pytest
import sympy as sp

from solver.certified import (bernstein_lower, certify_support, downward_float,
                              elementary_interval, feature_intervals, replay_support)

x, y = sp.symbols("x y", real=True)


def replay(args, result, rows=()):
    return replay_support(*args, rows, json.loads(json.dumps(result.witness)))


def test_interior_minimum_requires_complete_subdivision():
    args = ((x*x,), (x,), ((-1, 1),), (1,))
    result = certify_support(*args, target=0, max_cells=3)
    assert result.status == "complete"
    assert result.cut.rhs_exact == 0
    assert result.stats["cells"] == 3
    assert replay(args, result)
    failed = certify_support(*args, target=0, max_cells=2)
    assert failed.status == "incomplete" and failed.cut is None
    assert failed.witness is None  # A partial covering is never exported.


def test_tensor_bernstein_joint_cancellation():
    # Tensor bounds retain cancellation in the whole scalar direction.
    terms = {(2, 0): Q(1), (1, 1): Q(-2), (0, 2): Q(1)}
    assert bernstein_lower(terms, ((Q(0), Q(1)), (Q(0), Q(1)))) == Q(-1, 2)
    args = ((x*x, x*y, y*y), (x, y), ((0, 1), (0, 1)), (1, -2, 1))
    result = certify_support(*args, quadratic_fast_path=False, target=Q(-1, 8), max_cells=255)
    assert result.status == "complete" and result.cut.rhs_exact >= Q(-1, 8)
    assert replay(args, result)


def test_exact_clipped_quadratic_and_stationary_point():
    args = ((x, y, x*x, x*y, y*y), (x, y), ((0, 1), (0, 1)), (0, 0, 0, -1, 0))
    rows = (((1, 1), 1),)
    result = certify_support(*args, rows=rows, target=Q(-1, 4))
    assert result.cut.rhs_exact == Q(-1, 4)
    assert result.stats["method"] == "quadratic_polygon"
    assert replay(args, result, rows)
    assert not replay_support(*args, (), result.witness)


def test_exact_binary_coefficients_and_downward_rounding():
    # 1/10 as a float is above 1/10 as a rational. The exported coefficient
    # must therefore be certified anew, rather than carrying a rational cut.
    args = ((x,), (x,), ((Q(-1, 3), Q(-1, 3)),), (0.1,))
    result = certify_support(*args)
    exact = Q.from_float(0.1) * Q(-1, 3)
    assert result.cut.rhs_exact <= exact
    assert Q.from_float(math.nextafter(result.cut.rhs, math.inf)) > exact
    assert replay(args, result)
    assert downward_float(Q(1, 10)) < 0.1
    assert downward_float(Q(-1, 10)) == -0.1


def test_float_expression_constant_is_exact_binary_value():
    c = sp.Float(0.1)
    args = ((c*x,), (x,), ((1, 1),), (1,))
    result = certify_support(*args)
    assert result.cut.rhs_exact == Q.from_float(0.1)
    assert replay(args, result)


def test_forged_float_rhs_is_rejected():
    args = ((x,), (x,), ((Q(1, 3), 1),), (1,))
    result = certify_support(*args)
    forged = deepcopy(result.witness)
    forged["rhs"] = math.nextafter(result.cut.rhs, math.inf).hex()
    assert not replay_support(*args, (), forged)


def test_forged_leaf_bound_is_rejected():
    args = ((x*x,), (x,), ((-1, 1),), (1,))
    result = certify_support(*args)
    forged = deepcopy(result.witness)
    forged["proof"]["lower"] = "1"
    forged["lower_bound"] = "1"
    forged["rhs"] = 1.0.hex()
    assert not replay_support(*args, (), forged)


def test_omitted_half_and_wrong_split_rejected():
    args = ((x*x,), (x,), ((-1, 1),), (1,))
    result = certify_support(*args, target=0)
    forged = deepcopy(result.witness)
    forged["proof"]["children"].pop()
    assert not replay_support(*args, (), forged)
    forged = deepcopy(result.witness)
    forged["proof"]["split"] = True  # bool is not a valid dimension index.
    assert not replay_support(*args, (), forged)


@pytest.mark.parametrize("part", ["feature", "box", "coefficient"])
def test_certificate_bound_to_expected_model(part):
    args = ((x*x,), (x,), ((-1, 1),), (1,))
    result = certify_support(*args)
    changed = list(args)
    if part == "feature":
        changed[0] = (x*x-2,)
    elif part == "box":
        changed[2] = ((-2, 2),)
    else:
        changed[3] = (-1,)
    assert not replay_support(*changed, (), result.witness)


def test_strict_affine_exclusion_keeps_boundary():
    args = ((x,), (x,), ((0, 1),), (1,))
    rows = (((-1,), Q(-1, 2)),)
    result = certify_support(*args, rows=rows, target=Q(7, 16), max_cells=30)
    assert result.status == "complete" and result.cut.rhs_exact <= Q(1, 2)
    assert replay(args, result, rows)
    bad = deepcopy(result.witness)
    bad["proof"] = {"excluded_by": 0}
    bad["status"] = "empty"
    bad.pop("rhs")
    bad.pop("lower_bound")
    assert not replay_support(*args, rows, bad)


def test_empty_domain_has_no_cut_and_exact_certificate():
    args = ((x,), (x,), ((0, 1),), (1,))
    rows = (((1,), -1),)
    result = certify_support(*args, rows=rows)
    assert result.status == "empty" and result.cut is None
    assert replay(args, result, rows)


def test_no_separation_is_not_membership():
    args = ((x*x,), (x,), ((-1, 1),), (1,))
    result = certify_support(*args, target=1, max_cells=10, max_depth=3)
    assert result.status == "incomplete" and result.cut is None


def test_source_strings_are_not_evaluated():
    with pytest.raises(ValueError, match="source strings"):
        certify_support(("__import__('os').abort()",), (x,), ((0, 1),), (1,))


def test_general_functions_use_arb_and_replay():
    pytest.importorskip("flint")
    args = ((sp.exp(x), sp.log(x)), (x,), ((1, 2),), (1, 1))
    result = certify_support(*args)
    assert result.status == "complete" and result.stats["method"] == "arb"
    assert 2 < result.cut.rhs_exact < 3
    assert replay(args, result)


@pytest.mark.parametrize("expr", [sp.sqrt(x), x**sp.Rational(3, 5)])
def test_singular_derivative_endpoint_kept_and_enclosed(expr):
    pytest.importorskip("flint")
    args = ((expr,), (x,), ((0, 1),), (1,))
    result = certify_support(*args)
    assert result.cut.rhs_exact == 0
    assert replay(args, result)


@pytest.mark.parametrize("expr", [sp.log(x), sp.sqrt(x)])
def test_invalid_tiny_endpoint_sliver_is_never_discarded(expr):
    pytest.importorskip("flint")
    args = ((expr,), (x,), ((-Q(1, 2**100), 1),), (1,))
    result = certify_support(*args, max_depth=8, max_cells=50)
    assert result.status == "incomplete" and result.cut is None


def test_zero_weight_feature_domain_still_checked():
    pytest.importorskip("flint")
    args = ((x, sp.log(x)), (x,), ((-1, 1),), (1, 0))
    result = certify_support(*args, max_depth=5)
    assert result.status == "incomplete" and result.cut is None


def test_unevaluated_cancellation_does_not_erase_domain():
    pytest.importorskip("flint")
    expr = sp.Mul(x, sp.Pow(x, -1, evaluate=False), evaluate=False)
    args = ((expr,), (x,), ((0, 1),), (1,))
    result = certify_support(*args, max_depth=5)
    assert result.status == "incomplete" and result.cut is None


def test_trig_interval_covers_interior_extremum_and_huge_arguments():
    pytest.importorskip("flint")
    lo, hi = elementary_interval(sp.sin(x), x, (Q(0), Q(4)))
    assert lo <= 0 and hi >= 1
    lo, hi = elementary_interval(sp.cos(x), x, (Q(10**40), Q(10**40+100)))
    assert lo <= -1 and hi >= 1


def test_exact_samples_and_transcendental_samples():
    values = feature_intervals((x, x*x, x*y), (x, y), (Q(1, 3), Q(2, 7)))
    assert values == ((Q(1, 3),)*2, (Q(1, 9),)*2, (Q(2, 21),)*2)
    pytest.importorskip("flint")
    exp = feature_intervals((sp.exp(x),), (x,), (0,))
    assert exp == ((Q(1), Q(1)),)


def test_star_support_and_model_bound_replay():
    z = sp.Symbol("z", real=True)
    args = ((x, y, z, x*x, x*y, x*z, y*y, z*z), (x, y, z),
            ((0, 1),)*3, (0, 0, 0, 2, -2, -2, 1, 1))
    result = certify_support(*args, target=0)
    assert result.status == "complete" and result.cut.rhs_exact == 0
    assert result.stats["method"] == "quadratic_star"
    assert replay(args, result)
    forged = deepcopy(result.witness)
    forged["proof"]["center"] = 1
    assert not replay_support(*args, (), forged)
    failed = certify_support(*args, target=1)
    assert failed.cut is None and failed.stats["exact_support"] == "0"
    assert failed.stats["minimizer"] == ["0", "0", "0"]


def test_nonstar_multivariate_support_is_unsupported():
    z = sp.Symbol("z", real=True)
    result = certify_support((x*y, x*z, y*z), (x, y, z), ((0, 1),)*3, (1, 1, 1))
    assert result.status == "unsupported" and result.cut is None


def test_rigorous_curvature_bound_resolves_convex_interior_minimum():
    pytest.importorskip("flint")
    args = ((x, sp.exp(x)), (x,), ((-1, 1),), (-1, 1))
    # min(exp(x)-x)=1. Tightness here requires handling the full interval
    # around the interior minimizer, rather than just checking endpoints.
    result = certify_support(*args, target=Q(99, 100), max_cells=15)
    assert result.status == "complete"
    assert Q(99, 100) <= result.cut.rhs_exact <= 1
    assert replay(args, result)


def test_combined_scalar_cancellation_preserves_original_domains():
    pytest.importorskip("flint")
    args = ((sp.exp(x), sp.exp(x)), (x,), ((-10, 10),), (1, -1))
    result = certify_support(*args, target=0, max_cells=1)
    assert result.status == "complete" and result.cut.rhs_exact == 0
    assert replay(args, result)
    invalid = certify_support((sp.log(x), sp.log(x)), (x,), ((-1, 1),), (1, -1), max_depth=3)
    assert invalid.status == "incomplete" and invalid.cut is None


def test_generator_cannot_exceed_replay_resource_limits():
    args = ((x,), (x,), ((0, 1),), (1,))
    for budget in ({"max_depth": 257}, {"max_cells": 1000001}, {"precision": 128.0}):
        with pytest.raises(ValueError, match="budget or precision"):
            certify_support(*args, **budget)
