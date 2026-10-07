"""Contracts at the rational support to actual binary64 cut boundary."""

from copy import deepcopy
from fractions import Fraction as F

import pytest
import sympy as sp

from solver.support import certify_support, replay_support


X = sp.symbols("x:3")
BOX = ((0, 1),) * 3
ROWS = (((-1, -1, -1), -1),)
FEATURES = tuple(x * x for x in X)


def test_non_star_row_uses_exact_polytope_and_rounds_intercept_down():
    result = certify_support(FEATURES, X, BOX, (1, 1, 1), rows=ROWS)
    assert result.status == "complete"
    assert result.stats["method"] == "quadratic_polytope"
    assert result.stats["exact_support"] == "1/3"
    assert result.cut.rhs_exact <= F(1, 3)
    assert replay_support(FEATURES, X, BOX, (1, 1, 1), ROWS, result.witness)


def test_unreached_target_retains_exact_minimizer_without_cut():
    result = certify_support(FEATURES, X, BOX, (1, 1, 1), rows=ROWS, target=F(1, 3))
    assert result.status == "incomplete"  # 1/3 is not binary64 representable.
    assert result.cut is None and result.witness is None
    assert result.stats["minimizer"] == ["1/3"] * 3
    assert result.stats["exact_support"] == "1/3"


def test_zero_face_budget_falls_back_without_claiming_exact_support():
    result = certify_support(FEATURES, X, BOX, (1, 1, 1), rows=ROWS, max_polytope_faces=0)
    assert result.status == "unsupported"
    assert result.stats["method"] == "bernstein"
    assert "polytope_skipped" in result.stats
    assert result.cut is None and result.witness is None


def test_fallback_can_reuse_generator_rows_and_bounds():
    rows = (((-1, -1), -1),)
    result = certify_support(iter(FEATURES[:2]), iter(X[:2]), (iter(pair) for pair in BOX[:2]),
                             iter((1, 1)), rows=((iter(a), b) for a, b in rows),
                             max_polytope_faces=0)
    assert result.status == "complete"
    assert result.stats["method"] == "quadratic_polygon"
    assert replay_support(FEATURES[:2], X[:2], BOX[:2], (1, 1), rows, result.witness)


def test_empty_affine_domain_has_replayable_empty_witness():
    rows = (((0, 0, 0), -1),)
    result = certify_support(FEATURES, X, BOX, (1, 1, 1), rows=rows)
    assert result.status == "empty" and result.cut is None
    assert replay_support(FEATURES, X, BOX, (1, 1, 1), rows, result.witness)


def test_actual_direction_coefficients_and_symbolic_model_are_bound():
    coefficients = (0.1, 1.0, 1.0)
    result = certify_support(FEATURES, X, BOX, coefficients, rows=ROWS)
    assert result.cut.coefficients[0] == 0.1
    assert F(result.witness["proof"]["quadratic"]["problem"]["coefficients"][4]) == F(0.1)
    assert not replay_support(FEATURES, X, BOX, (0.2, 1, 1), ROWS, result.witness)
    assert not replay_support((X[0], *FEATURES[1:]), X, BOX, coefficients, ROWS, result.witness)
    assert not replay_support(FEATURES, X, BOX, coefficients, (), result.witness)


def test_upward_intercept_or_certificate_mutation_is_rejected():
    result = certify_support(FEATURES, X, BOX, (1, 1, 1), rows=ROWS)
    forged = deepcopy(result.witness)
    forged["rhs"] = float(0.34).hex()
    assert not replay_support(FEATURES, X, BOX, (1, 1, 1), ROWS, forged)
    forged = deepcopy(result.witness)
    forged["proof"]["quadratic"]["candidates"] = []
    assert not replay_support(FEATURES, X, BOX, (1, 1, 1), ROWS, forged)


def test_quadratic_fast_path_can_be_disabled():
    result = certify_support(FEATURES, X, BOX, (1, 1, 1), rows=ROWS, quadratic_fast_path=False)
    assert result.stats["method"] == "bernstein"


@pytest.mark.parametrize("kwargs", [{"max_depth": 257}, {"max_cells": 0},
                                     {"max_polytope_dimension": -1}, {"max_polytope_faces": True}])
def test_invalid_budgets_raise(kwargs):
    with pytest.raises(ValueError):
        certify_support(FEATURES, X, BOX, (1, 1, 1), **kwargs)
