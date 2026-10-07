"""Distinct exact contracts for general bounded quadratic block support."""

from copy import deepcopy
from fractions import Fraction as F
from itertools import product
import random

import pytest

from theory.quadratic_polytope import (
    EnumerationLimitError, coefficient_pairs, enumeration_size, polytope_vertices,
    quadratic_value, replay_quadratic, support_quadratic,
)
from theory.quadratic_polygon import support_quadratic as polygon_support


def diagonal_objective(center, weights):
    d = len(center)
    return (sum(w * x * x for w, x in zip(weights, center)),
            *(-2 * w * x for w, x in zip(weights, center)),
            *(weights[i] if i == j else 0 for i, j in coefficient_pairs(d)))


@pytest.mark.parametrize("dimension", [1, 2, 3, 4])
def test_exact_interior_minimizer_in_each_dimension(dimension):
    center = tuple(F(i + 1, dimension + 2) for i in range(dimension))
    coefficients = diagonal_objective(center, tuple(range(1, dimension + 1)))
    bounds = ((0, 1),) * dimension
    result = support_quadratic(bounds, (), coefficients)
    assert result["bound"] == "0"
    assert tuple(map(F, result["minimizer"])) == center
    assert replay_quadratic(bounds, (), coefficients, result)


@pytest.mark.parametrize("dimension", [2, 3, 4])
def test_coupled_simplex_boundary_minimum(dimension):
    # Sum x_i^2 subject to sum x_i = 1 has the unique minimizer (1/d,...,1/d).
    bounds = ((0, 1),) * dimension
    rows = ((*([1] * dimension), 1), (*([-1] * dimension), -1))
    coefficients = diagonal_objective((0,) * dimension, (1,) * dimension)
    result = support_quadratic(bounds, rows, coefficients)
    assert F(result["bound"]) == F(1, dimension)
    assert tuple(map(F, result["minimizer"])) == (F(1, dimension),) * dimension
    assert replay_quadratic(bounds, rows, coefficients, result)


def test_lower_dimensional_singular_objective_moves_to_boundary():
    # Objective (x+y-1)^2 is flat on a plane, and z is completely absent.
    coefficients = (1, -2, -2, 0, 1, 2, 0, 1, 0, 0)
    rows = ((1, -1, 0, 0), (-1, 1, 0, 0))
    result = support_quadratic(((0, 1),) * 3, rows, coefficients)
    assert result["bound"] == "0"
    assert tuple(map(F, result["minimizer"])) == (F(1, 2), F(1, 2), F(0))


def test_vertices_of_a_segment_point_and_empty_domain():
    bounds = ((0, 1),) * 3
    diagonal = ((1, -1, 0, 0), (-1, 1, 0, 0), (0, 1, -1, 0), (0, -1, 1, 0))
    assert polytope_vertices(bounds, diagonal) == ((F(0),) * 3, (F(1),) * 3)
    assert polytope_vertices(((F(1, 3), F(1, 3)),) * 3) == ((F(1, 3),) * 3,)
    assert polytope_vertices(bounds, ((0, 0, 0, -1),)) == ()


@pytest.mark.parametrize("bounds,rows", [
    (((0, 1),) * 3, ((0, 0, 0, -1),)),
    (((1, 0), (0, 1), (0, 1)), ()),
    (((0, 1),) * 3, ((1, 1, 1, F(1, 3)), (-1, -1, -1, F(-1, 2)))),
])
def test_empty_domain_is_certified_by_complete_vertex_coverage(bounds, rows):
    result = support_quadratic(bounds, rows, (0,) * 10)
    assert result["status"] == "empty"
    assert result["bound"] is None
    assert replay_quadratic(bounds, rows, (0,) * 10, result)


def test_arbitrary_quadratics_match_geometric_polygon_oracle():
    rng = random.Random(2601003)
    for _ in range(25):
        rows = tuple((rng.randint(-3, 3), rng.randint(-3, 3), rng.randint(-1, 4))
                     for _ in range(3))
        coefficients = tuple(F(rng.randint(-8, 8), rng.randint(1, 5)) for _ in range(6))
        result = support_quadratic(((-1, 1),) * 2, rows, coefficients)
        geometric = polygon_support(((-1, 1),) * 2, rows, coefficients)
        assert result["status"] == geometric["status"]
        assert result["bound"] == geometric["bound"]


def test_indefinite_multilinear_four_cycle_matches_boolean_enumeration():
    # All vertices must be considered; this objective has no star center.
    coefficients = (0, -1, 2, -3, 4, 0, -7, 2, 3, 0, 5, -6, 0, 8, 0)
    expected = min(quadratic_value(coefficients, point) for point in product((0, 1), repeat=4))
    result = support_quadratic(((0, 1),) * 4, (), coefficients)
    assert F(result["bound"]) == expected


def test_binary_float_meaning_and_no_rank_tolerance():
    tiny = F(1, 10**100)
    result = support_quadratic(((0.1, 0.1), (0, 1), (0, 1)), (),
                               (0, 1, 0, 0, 0, 0, 0, -tiny, 0, 0))
    assert F(result["bound"]) == F(0.1) - tiny
    assert F(result["bound"]) != F("0.1") - tiny


def test_duplicate_rows_change_witness_but_not_answer():
    bounds = ((0, 1),) * 3
    coefficients = diagonal_objective((0,) * 3, (1,) * 3)
    rows = ((-1, -1, -1, -1),)
    original = support_quadratic(bounds, rows, coefficients)
    duplicated = support_quadratic(bounds, rows * 2 + ((0, 0, 0, 0),), coefficients)
    assert original["bound"] == duplicated["bound"] == "1/3"
    assert original["enumeration"] != duplicated["enumeration"]


def test_budget_failure_cannot_be_mistaken_for_a_bound():
    bounds, coefficients = ((0, 1),) * 3, (0,) * 10
    required = enumeration_size(3, 0)
    with pytest.raises(EnumerationLimitError):
        support_quadratic(bounds, (), coefficients, max_faces=required - 1)
    result = support_quadratic(bounds, (), coefficients, max_faces=required)
    assert replay_quadratic(bounds, (), coefficients, result, max_faces=required)
    assert not replay_quadratic(bounds, (), coefficients, result, max_faces=required - 1)


def test_replay_rejects_omitted_candidates_and_altered_model():
    bounds, rows = ((0, 1),) * 3, ((-1, -1, -1, -1),)
    coefficients = diagonal_objective((0,) * 3, (1,) * 3)
    result = support_quadratic(bounds, rows, coefficients)
    for field, value in [("bound", "0"), ("status", "empty"), ("candidates", []),
                         ("minimizer", ["0"] * 3), ("enumeration", {})]:
        forged = deepcopy(result)
        forged[field] = value
        assert not replay_quadratic(bounds, rows, coefficients, forged)
    assert not replay_quadratic(bounds, (), coefficients, result)
    assert not replay_quadratic(((0, 2),) * 3, rows, coefficients, result)
    assert not replay_quadratic(bounds, rows, (1,) + coefficients[1:], result)


@pytest.mark.parametrize("invalid", [True, float("inf"), float("nan"), "1/0"])
def test_non_rational_input_is_rejected(invalid):
    with pytest.raises(ValueError):
        support_quadratic(((0, 1),), (), (0, invalid, 0))
