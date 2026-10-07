"""Behavior and adversarial checks for original affine bound certificates."""

import copy
from fractions import Fraction as Q
import json
import math
import random
from types import SimpleNamespace

import pytest

from solver.bounds import propagate_bounds, replay_bounds


def row(lin, lb=-math.inf, ub=math.inf, *, nl=None, quad=()):
    return {"lin": lin, "lb": lb, "ub": ub, "nl": nl, "quad": list(quad)}


def instance(lower, upper, rows=(), types=None):
    return SimpleNamespace(var_lb=lower, var_ub=upper,
                           var_type=types or ["C"] * len(lower),
                           rows=[row({}, lb=None, ub=None), *rows])


def checked(model, **kwargs):
    result = propagate_bounds(model, **kwargs)
    # A JSON round trip is the real persistence boundary.
    assert replay_bounds(model, json.loads(json.dumps(result.certificate)))
    return result


def test_upper_and_lower_sides_with_both_coefficient_signs():
    model = instance([0, 2], [10, 4], [row({0: -2, 1: 3}, lb=2, ub=4)])
    result = checked(model)
    assert result.lower == (Q(1), Q(2))
    assert result.upper == (Q(5), Q(4))
    assert result.status == "fixed_point"


def test_nonrepresentable_equality_has_outward_bounds():
    model = instance([-math.inf], [math.inf], [row({0: 3}, lb=1, ub=1)])
    result = checked(model)
    assert result.lower == result.upper == (Q(1, 3),)
    assert Q(result.float_lower[0]) < Q(1, 3) < Q(result.float_upper[0])
    assert math.nextafter(result.float_lower[0], math.inf) == result.float_upper[0]
    assert not result.infeasible


def test_negative_nonrepresentable_bounds_round_outward():
    model = instance([-math.inf], [math.inf], [row({0: -3}, lb=1, ub=1)])
    result = checked(model)
    assert result.lower == result.upper == (Q(-1, 3),)
    assert Q(result.float_lower[0]) < Q(-1, 3) < Q(result.float_upper[0])


def test_one_infinite_coordinate_can_be_bounded_but_two_cannot():
    model = instance([-math.inf, 2], [math.inf, math.inf], [row({0: 1, 1: 1}, ub=5)])
    result = checked(model)
    assert result.upper == (Q(3), math.inf)
    assert result.lower == (-math.inf, Q(2))
    unbounded = instance([-math.inf, -math.inf], [math.inf, math.inf],
                         [row({0: 1, 1: 1}, ub=5)])
    assert checked(unbounded).certificate["steps"] == []


def test_objective_and_nonlinear_and_quadratic_rows_are_not_used():
    model = instance([0], [10], [row({0: 1}, ub=-1, nl=("var", 0)),
                                row({0: 1}, ub=-2, quad=[(0, 0, 1)])])
    model.rows[0] = row({0: 1}, ub=-3)
    result = checked(model)
    assert result.lower == (Q(0),) and result.upper == (Q(10),)
    assert result.certificate["steps"] == []
    assert result.certificate["binding"]["rows"] == []


def test_reverse_order_chain_needs_multiple_passes():
    model = instance([0, 0, 0], [math.inf] * 3,
                     [row({0: 1, 1: -1}, ub=0), row({1: 1, 2: -1}, ub=0), row({2: 1}, ub=2)])
    short = checked(model, max_passes=1)
    assert short.upper == (math.inf, math.inf, Q(2))
    assert short.status == "budget"
    full = checked(model)
    assert full.upper == (Q(2),) * 3
    assert full.status == "fixed_point"


def test_step_budget_preserves_only_completed_deductions():
    model = instance([-10, -10], [10, 10], [row({0: 1}, lb=2, ub=3), row({1: 1}, lb=4, ub=5)])
    result = checked(model, max_steps=1)
    assert len(result.certificate["steps"]) == 1
    assert result.status == "budget"
    assert result.lower == (Q(-10), Q(-10))
    assert result.upper == (Q(3), Q(10))
    zero = checked(model, max_steps=0)
    assert zero.certificate["steps"] == [] and zero.status == "budget"


def test_binary_and_integer_semantics_are_exact():
    model = instance([-math.inf, 0.2], [math.inf, 4.8],
                     [row({1: 2}, ub=7)], types=["B", "I"])
    result = checked(model)
    assert result.lower == (Q(0), Q(1)) and result.upper == (Q(1), Q(3))
    assert {s["kind"] for s in result.certificate["steps"]} == {"binary", "integer", "affine"}
    unrounded = checked(model, round_integers=False)
    assert unrounded.lower == (Q(0), Q(0.2))
    assert unrounded.upper == (Q(1), Q(7, 2))


def test_integer_infeasibility_and_initial_bound_contradiction():
    integer = instance([0.2], [0.8], types=["I"])
    assert checked(integer).infeasible
    original = instance([2], [1])
    result = checked(original)
    assert result.infeasible and result.certificate["steps"] == []


@pytest.mark.parametrize("constraint", [row({}, ub=-1), row({}, lb=1), row({0: 2}, ub=1)])
def test_exact_affine_activity_contradiction(constraint):
    model = instance([1], [2], [constraint])
    result = checked(model)
    assert result.infeasible
    assert result.certificate["steps"][-1]["kind"] == "contradiction"


def test_binary64_inputs_are_not_decimal_rationals():
    model = instance([0], [1], [row({0: 0.1}, ub=0.03)])
    result = checked(model)
    assert result.upper == (Q(0.03) / Q(0.1),)
    assert result.upper != (Q(3, 10),)


def test_outward_export_handles_overflow_and_underflow():
    tiny = math.ulp(0.0)
    huge = float.fromhex("0x1.fffffffffffffp+1023")
    for rhs, coefficient in ((huge, tiny), (-huge, tiny), (tiny, huge), (-tiny, huge)):
        model = instance([-math.inf], [math.inf], [row({0: coefficient}, lb=rhs, ub=rhs)])
        result = checked(model)
        exact = Q(rhs) / Q(coefficient)
        assert result.lower == result.upper == (exact,)
        assert result.float_lower[0] <= exact <= result.float_upper[0]


@pytest.mark.parametrize("field,value", [("new", "0"), ("old", "3"), ("side", "lower"),
                                         ("row", 1), ("variable", -1), ("bound", "lower")])
def test_mutated_affine_deduction_is_rejected(field, value):
    model = instance([0], [10], [row({0: 3}, ub=1)])
    certificate = copy.deepcopy(checked(model).certificate)
    certificate["steps"][0][field] = value
    assert not replay_bounds(model, certificate)


def test_reordered_or_missing_chain_premise_is_rejected():
    model = instance([0, 0], [math.inf, math.inf],
                     [row({0: 1}, ub=2), row({0: -1, 1: 1}, ub=0)])
    certificate = checked(model).certificate
    broken = copy.deepcopy(certificate)
    broken["steps"].reverse()
    assert not replay_bounds(model, broken)
    broken = copy.deepcopy(certificate)
    broken["steps"].pop(0)
    assert not replay_bounds(model, broken)


def test_changed_original_model_is_rejected():
    model = instance([0], [10], [row({0: 3}, ub=1)])
    certificate = checked(model).certificate
    for mutate in (lambda m: m.rows[1]["lin"].update({0: 2}),
                   lambda m: m.var_lb.__setitem__(0, -1),
                   lambda m: m.var_type.__setitem__(0, "I"),
                   lambda m: m.rows[1].update(nl=("var", 0))):
        changed = copy.deepcopy(model)
        mutate(changed)
        assert not replay_bounds(changed, certificate)


def test_final_box_float_export_and_completion_claim_are_bound():
    model = instance([0], [10], [row({0: 3}, ub=1)])
    certificate = checked(model).certificate
    for mutate in (lambda c: c["result"]["upper"].__setitem__(0, "0"),
                   lambda c: c["result"]["float_upper"].__setitem__(0, float(Q(1, 3)).hex()),
                   lambda c: c["result"].update(infeasible=True)):
        changed = copy.deepcopy(certificate)
        mutate(changed)
        assert not replay_bounds(model, changed)
    empty = checked(model, max_steps=0).certificate
    empty["result"]["status"] = "fixed_point"
    assert not replay_bounds(model, empty)


@pytest.mark.parametrize("bad", [None, {}, {"schema": "unknown"}, [], "bad"])
def test_malformed_certificates_return_false(bad):
    assert not replay_bounds(instance([0], [1]), bad)


def test_known_feasible_rational_points_survive_propagation():
    rng = random.Random(811)
    for _ in range(60):
        point = [Q(rng.randint(-8, 8), 2) for _ in range(3)]
        constraints = []
        for _ in range(5):
            coefficients = {j: rng.randint(-4, 4) for j in range(3)}
            value = sum(coefficients[j] * point[j] for j in range(3))
            constraints.append(row(coefficients, lb=float(value - rng.randint(0, 3)),
                                   ub=float(value + rng.randint(0, 3))))
        model = instance([-10] * 3, [10] * 3, constraints)
        result = checked(model)
        assert not result.infeasible
        assert all(lo <= x <= hi for lo, x, hi in zip(result.lower, point, result.upper))


@pytest.mark.parametrize("kwargs", [{"max_passes": -1}, {"max_steps": 1.5},
                                    {"max_passes": True}, {"round_integers": 1}])
def test_invalid_budgets_and_options_are_rejected(kwargs):
    with pytest.raises(ValueError):
        propagate_bounds(instance([0], [1]), **kwargs)
