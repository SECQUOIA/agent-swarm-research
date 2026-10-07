"""Targeted contracts for the exact quadratic polygon support oracle."""

from copy import deepcopy
from fractions import Fraction as F
import random

import pytest

from quadratic_polygon import polygon_vertices, replay_quadratic, support_quadratic


BOX = ((0, 1), (0, 1))


@pytest.mark.parametrize(
    "bounds,rows,objective,bound,minimizer",
    [
        (BOX, (), (0, 0, 0, 0, -1, 0), -1, (1, 1)),
        (BOX, ((1, 1, 1),), (0, 0, 0, 0, -1, 0), F(-1, 4), (F(1, 2), F(1, 2))),
        (BOX, ((1, 1, 1),), (0, 1, 1, -1, -2, -1), 0, (0, 0)),
        (BOX, ((1, 1, 1), (-1, -1, -1)), (0, 0, 0, 0, -1, 0), F(-1, 4), (F(1, 2), F(1, 2))),
        (BOX, ((1, 0, F(1, 3)), (-1, 0, F(-1, 3)), (0, 1, F(2, 5)), (0, -1, F(-2, 5))), (0, 0, 0, 0, 1, 0), F(2, 15), (F(1, 3), F(2, 5))),
        (((2, 2), (-3, 7)), (), (0, 0, 0, 1, 0, 1), 4, (2, 0)),
        (BOX, (), (0, 0, 0, 1, -2, 1), 0, (0, 0)),
        (BOX, (), (F(1, 9), F(-2, 3), 0, 1, 0, 0), 0, (F(1, 3), 0)),
        (BOX, (), (F(1, 4), -1, 1, 1, -2, 1), 0, (F(1, 2), 0)),
    ],
)
def test_known_minima(bounds, rows, objective, bound, minimizer):
    certificate = support_quadratic(bounds, rows, objective)
    assert certificate["status"] == "complete"
    assert F(certificate["bound"]) == bound
    assert tuple(map(F, certificate["minimizer"])) == minimizer
    assert replay_quadratic(bounds, rows, objective, certificate)


@pytest.mark.parametrize("bounds,rows", [
    (BOX, ((0, 0, -1),)),
    (BOX, ((1, 1, -1),)),
    (((1, 0), (0, 1)), ()),
    (BOX, ((1, 1, F(1, 3)), (-1, -1, F(-1, 2)))),
])
def test_empty_domains(bounds, rows):
    certificate = support_quadratic(bounds, rows, (0,) * 6)
    assert certificate["status"] == "empty"
    assert certificate["bound"] is None
    assert replay_quadratic(bounds, rows, (0,) * 6, certificate)


def test_redundant_rows_and_reversed_order_preserve_the_set():
    rows = [(1, 1, 1), (2, 2, 2), (0, 0, 0), (1, 0, 3)]
    expected = ((F(0), F(0)), (F(1), F(0)), (F(0), F(1)))
    assert polygon_vertices(BOX, rows) == expected
    assert polygon_vertices(BOX, list(reversed(rows))) == expected


def test_constructed_positive_definite_quadratics():
    """Known minimizers of (z-z0)'A'(A)(z-z0), including cross terms."""
    rng = random.Random(8017)
    rows = [(1, 1, 1)]
    for _ in range(40):
        x, y = F(rng.randint(1, 9), 20), F(rng.randint(1, 9), 20)
        a, b, d = rng.randint(1, 7), rng.randint(-6, 6), rng.randint(1, 7)
        qxx, qxy, qyy = a * a, 2 * a * b, b * b + d * d
        constant = qxx * x * x + qxy * x * y + qyy * y * y
        c = (constant, -2 * qxx * x - qxy * y, -qxy * x - 2 * qyy * y, qxx, qxy, qyy)
        result = support_quadratic(BOX, rows, c)
        assert F(result["bound"]) == 0
        assert list(map(F, result["minimizer"])) == [x, y]


def test_exact_binary_float_meaning_and_tiny_negative_curvature():
    small = F(1, 10**60)
    result = support_quadratic(BOX, (), (0, 0, 0, -small, 0, 0))
    assert F(result["bound"]) == -small
    result = support_quadratic(((0.1, 0.1), (0, 0)), (), (0, 1, 0, 0, 0, 0))
    assert F(result["bound"]) == F(0.1)
    assert F(result["bound"]) != F("0.1")


def test_cut_and_original_domain_binding_reject_tampering():
    rows, objective = ((1, 1, 1),), (0, 0, 0, 0, -1, 0)
    certificate = support_quadratic(BOX, rows, objective)
    for field, altered in [("bound", "0"), ("status", "empty"), ("vertices", []), ("candidates", []), ("minimizer", ["0", "0"])]:
        forged = deepcopy(certificate)
        forged[field] = altered
        assert not replay_quadratic(BOX, rows, objective, forged)
    assert not replay_quadratic(BOX, (), objective, certificate)
    assert not replay_quadratic(((0, 2), (0, 1)), rows, objective, certificate)
    assert not replay_quadratic(BOX, rows, (0, 0, 0, 0, 1, 0), certificate)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf"), True])
def test_invalid_numbers_are_not_silently_certified(value):
    with pytest.raises(ValueError):
        support_quadratic(BOX, (), (value, 0, 0, 0, 0, 0))
