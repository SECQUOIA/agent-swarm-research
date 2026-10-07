"""Targeted contracts for exact and budgeted graph separation."""

from copy import deepcopy
from fractions import Fraction as Q
import sys
from pathlib import Path

import pytest
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from separation import separate_graph, replay_separation

x, y = sp.symbols("x y")


def test_finite_fallback_finds_cut_beyond_three_support_calls():
    args = ([x, x*x], [x], [(0, 1)], [Q(3, 10), Q(2, 25)])
    short = separate_graph(*args, epsilon=Q(1, 100), proposal_rounds=0, max_directions=3)
    assert short["status"] == "unresolved"
    result = separate_graph(*args, epsilon=Q(1, 100), proposal_rounds=0, complete=True)
    assert result["status"] == "cut"
    assert result["stats"]["support_calls"] > 3
    assert replay_separation(result, *args, epsilon=Q(1, 100))
    assert result["cut"]["binary64"]["separates"]


def test_polynomial_exhaustion_proves_nearness_without_exchange():
    args = ([x**4], [x], [(0, 1)], [Q(2, 5)])
    result = separate_graph(*args, epsilon=Q(1, 4), proposal_rounds=0, complete=True)
    assert result["status"] == "within_tolerance"
    assert result["witness"]["kind"] == "finite_normal_net"
    assert result["stats"]["domain_net_points"] == 33
    assert replay_separation(result, *args, epsilon=Q(1, 4))


def test_quartic_support_interval_contains_analytic_minimum():
    expression = (x - sp.Rational(1, 3))**4 + sp.Rational(1, 7)
    args = ([expression], [x], [(0, 1)], [0])
    result = separate_graph(*args, epsilon=Q(1, 20), complete=True, proposal_rounds=0)
    assert result["status"] == "cut"
    assert result["cut"]["coefficients"] == ["1"]
    lower = Q(result["cut"]["rhs"])
    point = Q(result["witness"]["minimizer"][0])
    upper = (point - Q(1, 3))**4 + Q(1, 7)
    assert lower <= Q(1, 7) <= upper
    assert upper - lower == Q(result["witness"]["error"]) <= Q(1, 40)
    assert replay_separation(result, *args, epsilon=Q(1, 20))


def test_thin_equality_domain_uses_exact_feasible_points():
    args = ([x, y, x*y], [x, y], [(0, 1), (0, 1)], [Q(1, 6), Q(1, 6), Q(1, 24)])
    rows = [(1, 1, Q(1, 3)), (-1, -1, Q(-1, 3))]
    result = separate_graph(*args, rows=rows, epsilon=Q(1, 40), complete=True, proposal_rounds=0)
    assert result["status"] == "cut"
    assert replay_separation(result, *args, rows=rows, epsilon=Q(1, 40))
    assert not replay_separation(result, *args, rows=rows[:-1], epsilon=Q(1, 40))


def test_general_polynomial_on_line_polytope():
    args = ([x**3 + y**3], [x, y], [(0, 1), (0, 1)], [Q(1, 20)])
    rows = [(1, 1, 1), (-1, -1, -1)]
    result = separate_graph(*args, rows=rows, epsilon=Q(1, 10), complete=True, proposal_rounds=0)
    assert result["status"] == "cut"
    assert Q(result["cut"]["rhs"]) <= Q(1, 4)
    assert replay_separation(result, *args, rows=rows, epsilon=Q(1, 10))


def test_convex_combination_is_independent_exact_witness():
    args = ([x, x*x], [x], [(0, 1)], [Q(1, 2), Q(1, 2)])
    result = separate_graph(*args, epsilon=Q(1, 100))
    assert result["status"] == "within_tolerance"
    assert result["witness"]["kind"] == "convex_combination"
    assert Q(result["witness"]["distance"]) == 0
    assert replay_separation(result, *args, epsilon=Q(1, 100))


def test_budget_exhaustion_never_claims_membership():
    args = ([x**4], [x], [(0, 1)], [Q(2, 5)])
    result = separate_graph(*args, epsilon=Q(1, 4), proposal_rounds=0, max_samples=2)
    assert result["status"] == "unresolved"
    assert not replay_separation(result, *args, epsilon=Q(1, 4))


def test_empty_point_and_zero_radius_domains():
    empty_args = ([x], [x], [(0, 1)], [0])
    empty = separate_graph(*empty_args, rows=[(1, -1)], complete=True)
    assert empty["status"] == "empty_domain"
    assert replay_separation(empty, *empty_args, rows=[(1, -1)])
    args = ([x**4], [x], [(Q(1, 3), Q(1, 3))], [Q(1, 81)])
    result = separate_graph(*args, proposal_rounds=0, complete=True)
    assert result["status"] == "within_tolerance"
    assert replay_separation(result, *args)


def test_nonnegative_normals_certify_upper_closure_not_graph():
    args = ([x*x], [x], [(0, 1)], [2])
    graph = separate_graph(*args, complete=True, proposal_rounds=0)
    assert graph["status"] == "cut"
    upper = separate_graph(*args, nonnegative=(0,), epsilon=1, complete=True, proposal_rounds=0)
    assert upper["status"] == "within_tolerance"
    assert replay_separation(upper, *args, nonnegative=(0,), epsilon=1)
    assert not replay_separation(upper, *args, epsilon=1)
    below_args = ([x*x + 1], [x], [(0, 1)], [0])
    below = separate_graph(*below_args, nonnegative=(0,), complete=True)
    assert below["status"] == "cut" and Q(below["cut"]["coefficients"][0]) >= 0
    assert replay_separation(below, *below_args, nonnegative=(0,))


def test_certificate_rejects_changed_query_tolerance_and_cut():
    args = ([x*x + 1], [x], [(0, 1)], [0])
    result = separate_graph(*args, complete=True)
    assert replay_separation(result, *args)
    assert not replay_separation(result, *args[:-1], [Q(1, 10)])
    assert not replay_separation(result, *args, epsilon=Q(1, 20))
    for field, value in [("rhs", "2"), ("coefficients", ["-1"]), ("query_gap", "0")]:
        bad = deepcopy(result)
        bad["cut"][field] = value
        assert not replay_separation(bad, *args)
    bad = deepcopy(result)
    bad["cut"]["binary64"]["rhs"] += 1
    assert not replay_separation(bad, *args)


def test_finite_net_rejects_missing_and_corrupted_witnesses():
    args = ([x**4], [x], [(0, 1)], [Q(2, 5)])
    result = separate_graph(*args, epsilon=Q(1, 4), proposal_rounds=0, complete=True)
    bad = deepcopy(result)
    bad["witness"]["points"].pop()
    assert not replay_separation(bad, *args, epsilon=Q(1, 4))
    bad = deepcopy(result)
    bad["witness"]["points"] = [["2"]] * len(bad["witness"]["points"])
    assert not replay_separation(bad, *args, epsilon=Q(1, 4))
    bad = deepcopy(result)
    bad["witness"]["support_error"] = "1"
    assert not replay_separation(bad, *args, epsilon=Q(1, 4))


def test_nonpolynomial_hidden_domains_and_invalid_data_rejected():
    hidden = sp.Mul(x, sp.Pow(x, -1, evaluate=False), evaluate=False)
    for expression in [hidden, sp.log(x), sp.sqrt(x), sp.sin(x)]:
        with pytest.raises(ValueError):
            separate_graph([expression], [x], [(0, 0)], [1])
    with pytest.raises(ValueError):
        separate_graph([x], [x], [(0, float("inf"))], [0])
    with pytest.raises(ValueError):
        separate_graph([x], [x], [(0, 1)], [0], epsilon=0)
    with pytest.raises(ValueError):
        separate_graph([x], [x], [(0, 1)], [0], nonnegative=(True,))


def test_high_precision_float_binding_and_nonfinite_export():
    constant = sp.Float("1.00000000000000000000000000000001", 60)
    args = ([constant], [x], [(0, 1)], [1])
    result = separate_graph(*args, epsilon=Q(1, 10**40), complete=True, proposal_rounds=0)
    assert result["status"] == "cut"
    assert Q(result["cut"]["rhs"]) == Q(sp.Rational(constant))
    assert replay_separation(result, *args, epsilon=Q(1, 10**40))
    huge_args = ([sp.Integer(10)**400], [x], [(0, 0)], [0])
    huge = separate_graph(*huge_args, epsilon=10**400, complete=True, proposal_rounds=0)
    assert huge["status"] == "cut"
    assert not huge["cut"]["binary64"]["available"]
    assert replay_separation(huge, *huge_args, epsilon=10**400)


def test_rational_cut_remains_valid_when_float_export_loses_gap():
    tiny = Q(1, 10**400)
    args = ([sp.Rational(tiny.numerator, tiny.denominator)], [x], [(0, 0)], [0])
    result = separate_graph(*args, epsilon=tiny, complete=True, proposal_rounds=0)
    assert result["status"] == "cut"
    assert result["cut"]["binary64"]["available"]
    assert not result["cut"]["binary64"]["separates"]
    assert replay_separation(result, *args, epsilon=tiny)


def test_tiny_tolerance_zero_budget_does_not_materialize_normal_net():
    args = ([x], [x], [(0, 1)], [Q(1, 2)])
    result = separate_graph(*args, epsilon=Q(1, 2**100), proposal_rounds=0, max_directions=0)
    assert result["status"] == "unresolved"
    assert result["stats"]["support_calls"] == 0
    assert result["stats"]["normal_grid_size"] > 2**100


def test_large_constant_feature_vector_has_direct_certificate():
    args = ([0] * 1100, [x], [(0, 0)], [0] * 1100)
    result = separate_graph(*args, complete=True, proposal_rounds=0)
    assert result["status"] == "within_tolerance"
    assert result["stats"]["support_calls"] == 0
    assert replay_separation(result, *args)
