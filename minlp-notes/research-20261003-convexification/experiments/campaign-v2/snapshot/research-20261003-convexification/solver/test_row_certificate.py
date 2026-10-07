"""Boundary and binding checks for native-row elimination certificates."""

from copy import deepcopy
from dataclasses import replace
from fractions import Fraction as F
import itertools
import math
import sys

import pytest

from row_certificate import AffineSide, certify_row_combination, replay_row_certificate


def problem(**updates):
    result = dict(
        variables=["x0"],
        bounds={"x0": (-2, 7)},
        linear_terms={},
        multipliers=[1.0],
        support_rhs=F(2, 7),
        sides=[AffineSide("row0:upper", [("x0", F(-1, 3))], F(1, 5))],
        support_id="verified-support-digest",
    )
    result.update(updates)
    return result


def test_elimination_orientation_matches_a_valid_nonlinear_example():
    # x^2 + 3y <= 5 and 2x + x^2/2 >= -2 imply 2x - 3y/2 >= -9/2.
    data = problem(
        variables=["x0", "x1"],
        bounds={"x0": (-3, 3), "x1": (-2, 2)},
        linear_terms={"x0": 2.0},
        multipliers=[0.5],
        support_rhs=-2,
        sides=[AffineSide("quadratic:upper", {"x1": 3}, 5)],
    )
    cert = certify_row_combination(**data)
    assert cert.coefficients == (2.0, -1.5)
    assert cert.rhs == -4.5
    for x, y in itertools.product((F(i, 4) for i in range(-12, 13)), repeat=2):
        if -2 <= y <= 2 and x * x + 3 * y <= 5:
            assert 2 * x - F(3, 2) * y >= F(cert.rhs)
    assert replay_row_certificate(cert, **data)


def test_both_rounding_error_signs_use_the_correct_box_endpoints():
    data = problem(
        variables=["x0", "x1"],
        bounds={"x0": (-2, 7), "x1": (-11, 4)},
        sides=[AffineSide("row0", [("x0", F(-1, 3)), ("x1", F(1, 3))], F(1, 5))],
    )
    cert = certify_row_combination(**data)
    exact = [F(1, 3), F(-1, 3)]
    errors = [F(actual) - wanted for actual, wanted in zip(cert.coefficients, exact)]
    assert errors[0] < 0 < errors[1]
    corner_errors = [
        sum(error * coordinate for error, coordinate in zip(errors, point))
        for point in itertools.product((-2, 7), (-11, 4))
    ]
    adjusted = F(2, 7) - F(1, 5) + min(corner_errors)
    assert F(cert.rhs) <= adjusted < F(math.nextafter(cert.rhs, math.inf))
    assert F(cert.to_dict()["exact"]["box_compensation"]) == min(corner_errors)


def test_severe_duplicate_term_cancellation_is_exact():
    huge = 10**400
    side = AffineSide("cancellation", [("x0", huge), ("x0", F(-1, 3)), ("x0", -huge)], 0)
    data = problem(
        sides=[side], support_rhs=0,
        linear_terms=[("x0", 1e16), ("x0", 1.0), ("x0", -1e16)],
    )
    cert = certify_row_combination(**data)
    assert cert.to_dict()["exact"]["coefficients"] == ["4/3"]
    assert len(cert.to_dict()["binding"]["sides"][0]["affine_terms"]) == 3


def test_float_inputs_mean_binary64_values_not_decimal_literals():
    cert = certify_row_combination(**problem(
        linear_terms={"x0": 0.1}, multipliers=[0.1],
        sides=[AffineSide("decimal", {"x0": 0.1}, 0.1)], support_rhs=0.1,
    ))
    record = cert.to_dict()
    expected = F(0.1) - F(0.1) * F(0.1)
    assert F(record["exact"]["coefficients"][0]) == expected
    assert expected != F(9, 100)
    assert F(record["exact"]["eliminated_rhs"]) == expected


def test_exact_unbounded_objective_epigraph_is_admissible():
    data = problem(
        variables=["objective_aux"], bounds={"objective_aux": (-math.inf, math.inf)},
        sides=[AffineSide("objective", {"objective_aux": -1.0}, 0)],
    )
    cert = certify_row_combination(**data)
    assert cert.coefficients == (1.0,)
    assert cert.to_dict()["exact"]["box_compensation"] == "0"
    assert replay_row_certificate(cert.to_dict(), **data)


@pytest.mark.parametrize("interval", [(None, None), (0, None), (None, 1), (-math.inf, 1), (0, math.inf)])
def test_any_unbounded_coordinate_with_rounding_error_is_rejected(interval):
    with pytest.raises(ValueError, match="rounding discrepancy at unbounded"):
        certify_row_combination(**problem(bounds={"x0": interval}))


def test_fixed_coordinate_compensation_can_improve_the_rhs():
    data = problem(bounds={"x0": (-7, -7)})
    cert = certify_row_combination(**data)
    compensation = F(cert.to_dict()["exact"]["box_compensation"])
    assert compensation > 0
    assert compensation == (F(cert.coefficients[0]) - F(1, 3)) * -7


def test_coefficient_underflow_is_compensated_and_rhs_rounds_away_from_zero():
    half_subnormal = F(1, 2**1075)
    cert = certify_row_combination(**problem(
        bounds={"x0": (0, 1)}, support_rhs=0,
        sides=[AffineSide("underflow", {"x0": -half_subnormal}, 0)],
    ))
    assert cert.coefficients == (0.0,)
    assert cert.rhs == -math.ulp(0.0)
    assert F(cert.to_dict()["exact"]["compensated_rhs"]) == -half_subnormal


@pytest.mark.parametrize("exact", [F(1, 10), F(-1, 10), F(1, 2**1075), F(-1, 2**1075), F(0)])
def test_right_hand_side_is_the_greatest_binary64_not_above_exact(exact):
    cert = certify_row_combination(**problem(
        multipliers=[], sides=[], linear_terms={}, support_rhs=exact,
    ))
    assert F(cert.rhs) <= exact < F(math.nextafter(cert.rhs, math.inf))


def test_negative_zero_is_normalized_in_export_and_binding():
    cert = certify_row_combination(**problem(
        linear_terms={"x0": -0.0}, multipliers=[-0.0], support_rhs=-0.0,
    ))
    assert math.copysign(1.0, cert.coefficients[0]) == 1.0
    assert math.copysign(1.0, cert.rhs) == 1.0
    assert cert.to_dict()["binding"]["support"]["multipliers"] == ["0"]


@pytest.mark.parametrize("updates", [
    {"sides": [AffineSide("overflow", {"x0": 10**400}, 0)]},
    {"support_rhs": 10**400},
    {"support_rhs": -(10**400)},
    {"support_rhs": -F(sys.float_info.max) - 1, "sides": [], "multipliers": []},
])
def test_export_overflow_and_nonfinite_downward_rounding_are_rejected(updates):
    with pytest.raises(ValueError, match="finite"):
        certify_row_combination(**problem(**updates))


@pytest.mark.parametrize("value", [-1.0, F(1, 3), math.nan, math.inf, -math.inf, True])
def test_invalid_support_multipliers_are_rejected(value):
    with pytest.raises(ValueError):
        certify_row_combination(**problem(multipliers=[value]))


@pytest.mark.parametrize("interval", [(math.inf, math.inf), (-math.inf, -math.inf), (math.nan, 2), (0, math.nan), (2, 1), (False, 1)])
def test_invalid_bounds_are_rejected(interval):
    with pytest.raises(ValueError):
        certify_row_combination(**problem(bounds={"x0": interval}))


@pytest.mark.parametrize("updates", [
    {"variables": ["x0", "x0"]},
    {"variables": [""]},
    {"bounds": {}},
    {"linear_terms": {"missing": 0}},
    {"linear_terms": {"x0": F(1, 3)}},
    {"multipliers": []},
    {"sides": [AffineSide("", {}, 0)]},
    {"sides": [AffineSide("side", {"missing": 0}, 0)]},
    {"sides": [AffineSide("side", {"x0": math.nan}, 0)]},
    {"sides": [AffineSide("side", {}, math.inf)]},
])
def test_malformed_or_unbound_inputs_are_rejected(updates):
    with pytest.raises(ValueError):
        certify_row_combination(**problem(**updates))


def test_export_is_detached_from_inputs_and_from_each_previous_export():
    terms = [["x0", F(-1, 3)]]
    side = AffineSide("side", terms, 0)
    terms[0][1] = 12
    data = problem(sides=[side])
    cert = certify_row_combination(**data)
    first = cert.to_dict()
    first["binding"]["sides"][0]["affine_terms"][0][1] = "12"
    assert cert.to_dict()["binding"]["sides"][0]["affine_terms"][0][1] == "-1/3"
    assert replay_row_certificate(cert, **data)


@pytest.mark.parametrize("path,value", [
    (("schema",), "different-schema"),
    (("binding", "variables", 0), "other"),
    (("binding", "bounds", 0, 1), "8"),
    (("binding", "support", "support_id"), "different-support"),
    (("binding", "support", "linear_coefficients", 0), "1"),
    (("binding", "support", "multipliers", 0), "2"),
    (("binding", "support", "rhs"), "3"),
    (("binding", "sides", 0, "source_id"), "other-side"),
    (("binding", "sides", 0, "affine_terms", 0, 1), "1/3"),
    (("binding", "sides", 0, "rhs"), "0"),
    (("exact", "coefficients", 0), "1/2"),
    (("exact", "box_compensation"), "0"),
    (("exported", "coefficients", 0), math.nextafter(1 / 3, math.inf)),
    (("exported", "rhs"), 1.0),
    (("exported", "orientation"), "<="),
])
def test_every_binding_and_export_is_checked_during_replay(path, value):
    data = problem()
    cert = certify_row_combination(**data)
    corrupted = deepcopy(cert.to_dict())
    item = corrupted
    for key in path[:-1]:
        item = item[key]
    item[path[-1]] = value
    assert not replay_row_certificate(corrupted, **data)


def test_replay_uses_trusted_inputs_and_checks_public_export_fields():
    data = problem()
    cert = certify_row_combination(**data)
    assert not replay_row_certificate(cert, **problem(bounds={"x0": (-3, 8)}))
    assert not replay_row_certificate(cert, **problem(support_id="different"))
    assert not replay_row_certificate(replace(cert, coefficients=(1.0,)), **data)
    assert not replay_row_certificate(replace(cert, rhs=1.0), **data)
    malformed = cert.to_dict()
    malformed["exported"]["rhs"] = math.nan
    assert not replay_row_certificate(malformed, **data)


def test_zero_variable_constant_cut_and_zero_sides_are_well_defined():
    data = dict(variables=[], bounds={}, linear_terms={}, sides=[], multipliers=[], support_rhs=1)
    cert = certify_row_combination(**data)
    assert cert.coefficients == ()
    assert cert.rhs == 1.0
    assert replay_row_certificate(cert, **data)
