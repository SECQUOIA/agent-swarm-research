"""Targeted checks for reference witnesses and the independent primal audit."""
from dataclasses import asdict

from cases import check_primal, instance, row, synthetic_cases
from run_campaign import exact_json
from worker import load_model


def test_frozen_reference_witnesses_and_exact_model_roundtrip():
    for case in synthetic_cases():
        original = case["instance"]
        restored = load_model({"model": exact_json(asdict(original))})
        assert restored == original
        result = check_primal(restored, case["known_witness"], case["known_optimum"])
        assert result["passed"], (original.name, result)


def test_original_row_and_integrality_violation_are_detected():
    cases = {c["instance"].name: c for c in synthetic_cases()}
    simplex = cases["simplex_product"]["instance"]
    assert not check_primal(simplex, [1.0, 1.0], -1)["passed"]
    binary = cases["binary_product_control"]["instance"]
    assert not check_primal(binary, [0.5, 0.5, 0.5, 0.5], -0.5)["passed"]


def test_original_domain_and_objective_mismatch_are_detected():
    cases = {c["instance"].name: c for c in synthetic_cases()}
    assert not check_primal(cases["log_pair"]["instance"], [-1.0])["passed"]
    assert not check_primal(cases["simplex_product"]["instance"], [0.5, 0.5], -0.5)["passed"]
    assert not check_primal(cases["simplex_product"]["instance"], None)["checked"]


def test_nonfinite_objective_is_not_accepted_as_a_feasible_primal_result():
    model = instance("overflow", [(0, 1e308)], row(lin={0: 1e308}))
    assert not check_primal(model, [2.0])["passed"]
    assert not check_primal(model, [0.0], float("inf"))["passed"]
    assert not check_primal(model, [0.0], float("nan"))["passed"]


def test_binary_type_enforces_semantic_bounds_independent_of_declared_box():
    model = instance("binary", [(-10, 10)], row(lin={0: 1}), types=["B"])
    assert check_primal(model, [1.0], 1.0)["passed"]
    assert not check_primal(model, [2.0], 2.0)["passed"]
