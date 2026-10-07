"""Exact minima, affine coupling, and shared-moment regression tests."""

from copy import deepcopy
from fractions import Fraction as F
from itertools import product
import random

import pytest

from quadratic_polygon import support_quadratic
from quadratic_star import replay_star, support_star


def test_sharp_pair_hull_obstruction():
    # Variable order (y,x,z). The two pair measures agree on y and y squared.
    c = {(0, 0, 0): F(1, 16), (1, 0, 0): F(-1, 2), (2, 0, 0): 2,
         (0, 1, 0): F(5, 4), (0, 2, 0): F(-3, 4), (1, 1, 0): -1,
         (0, 0, 1): 1, (0, 0, 2): F(-39, 64), (1, 0, 1): F(-5, 4)}
    moments = {(0, 0, 0): 1, (1, 0, 0): F(1, 2), (2, 0, 0): F(5, 16),
               (0, 1, 0): F(1, 2), (0, 2, 0): F(1, 2), (1, 1, 0): F(3, 8),
               (0, 0, 1): F(4, 5), (0, 0, 2): F(4, 5), (1, 0, 1): F(1, 2)}
    assert sum(value * moments[exponent] for exponent, value in c.items()) == 0
    result = support_star(((0, 1),) * 3, (), c)
    assert F(result["bound"]) == F(1, 128)
    assert list(map(F, result["minimizer"])) == [F(11, 16), 1, 1]
    assert replay_star(((0, 1),) * 3, (), c, 0, result)


def test_pairwise_rows_improve_the_box_support():
    c = {(1, 1, 0): -1, (1, 0, 1): -1}
    rows = [((1, 1, 0), 1), ((1, 0, 1), 1)]
    constrained = support_star(((0, 1),) * 3, rows, c)
    assert F(constrained["bound"]) == F(-1, 2)
    assert list(map(F, constrained["minimizer"])) == [F(1, 2)] * 3
    assert F(support_star(((0, 1),) * 3, (), c)["bound"]) == -2


def test_random_one_leaf_matches_independent_polygon_candidate_enumeration():
    rng = random.Random(6317)
    exponents = [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2)]
    for _ in range(120):
        c = [F(rng.randint(-11, 11), rng.randint(1, 5)) for _ in exponents]
        rows = [tuple(F(rng.randint(-3, 3)) for _ in range(3)) for _ in range(4)]
        box = ((-2, 3), (-1, 2))
        polygon = support_quadratic(box, rows, c)
        star = support_star(box, [(row[:2], row[2]) for row in rows], dict(zip(exponents, c)))
        assert star["status"] == polygon["status"]
        assert star["bound"] == polygon["bound"]


def test_constructed_joint_convex_quadratics_with_known_minimum():
    rng = random.Random(921)
    for _ in range(30):
        n, y0 = 5, F(1, 3)
        zero = (0,) * n
        c = {zero: y0 * y0, (1, 0, 0, 0, 0): -2 * y0, (2, 0, 0, 0, 0): F(1)}
        expected = [y0]
        rows = []
        for i in range(1, n):
            weight, slope, intercept = rng.randint(1, 5), F(rng.randint(-2, 2), 5), F(1, 2)
            expected.append(intercept + slope * y0)
            linear, square, cross = [0] * n, [0] * n, [0] * n
            linear[i], square[i], cross[i], cross[0] = 1, 2, 1, 1
            c[zero] += weight * intercept * intercept
            c[(1, 0, 0, 0, 0)] += 2 * weight * slope * intercept
            c[(2, 0, 0, 0, 0)] += weight * slope * slope
            c[tuple(linear)] = -2 * weight * intercept
            c[tuple(square)] = weight
            c[tuple(cross)] = -2 * weight * slope
            row = [0] * n
            row[0], row[i] = 1, 1
            rows.append((row, 1))
        result = support_star(((0, 1),) * n, rows, c)
        assert F(result["bound"]) == 0
        assert list(map(F, result["minimizer"])) == expected


def test_nonconvex_box_stars_against_endpoint_enumeration():
    rng = random.Random(8881)
    n = 5
    for _ in range(40):
        center_linear, center_square = F(rng.randint(-7, 7)), F(rng.randint(-3, 5))
        c = {(1, 0, 0, 0, 0): center_linear, (2, 0, 0, 0, 0): center_square}
        terms = []
        for i in range(1, n):
            linear, square, cross = F(rng.randint(-7, 7)), F(-rng.randint(0, 5)), F(rng.randint(-7, 7))
            terms.append((linear, square, cross))
            for degree, value in [(1, linear), (2, square)]:
                exponent = [0] * n
                exponent[i] = degree
                c[tuple(exponent)] = value
            exponent = [0] * n
            exponent[0] = exponent[i] = 1
            c[tuple(exponent)] = cross
        direct = []
        for endpoints in product((F(0), F(1)), repeat=n - 1):
            constant = sum(d * x + a * x * x for x, (d, a, b) in zip(endpoints, terms))
            linear = center_linear + sum(b * x for x, (d, a, b) in zip(endpoints, terms))
            candidates = [F(0), F(1)]
            if center_square > 0 and 0 < -linear / (2 * center_square) < 1:
                candidates.append(-linear / (2 * center_square))
            direct.extend(constant + linear * y + center_square * y * y for y in candidates)
        assert F(support_star(((0, 1),) * n, (), c)["bound"]) == min(direct)


def test_center_projection_singleton_and_incompatible_projections():
    c = {(1, 0, 0): 1, (0, 1, 0): 2, (0, 0, 1): 3}
    rows = [((1, 1, 0), F(1, 2)), ((-1, 0, 1), F(-1, 2))]
    result = support_star(((0, 1),) * 3, rows, c)
    assert result["center_interval"] == ["1/2", "1/2"]
    assert result["bound"] == "1/2"
    assert result["minimizer"] == ["1/2", "0", "0"]
    assert support_star(((0, 1),) * 3, rows + [((1, 0, 0), F(1, 3))], c)["status"] == "empty"


def test_nonzero_center_index_and_no_leaves():
    result = support_star(((0, 1),) * 3, [((1, 1, 0), 1), ((0, 1, 1), 1)], {(1, 1, 0): -1, (0, 1, 1): -1}, center=1)
    assert F(result["bound"]) == F(-1, 2)
    singleton = support_star(((0, 1),), (), {(0,): F(1, 9), (1,): F(-2, 3), (2,): 1})
    assert singleton["bound"] == "0"
    assert singleton["minimizer"] == ["1/3"]


def test_certificate_rejects_missing_domain_rows_and_piece_tampering():
    bounds, rows, c = ((0, 1),) * 3, [((1, 1, 0), 1)], {(1, 1, 0): -1, (1, 0, 1): -1}
    result = support_star(bounds, rows, c)
    assert not replay_star(bounds, (), c, 0, result)
    forged = deepcopy(result)
    forged["pieces"][0]["bound"] = "100"
    assert not replay_star(bounds, rows, c, 0, forged)
    forged = deepcopy(result)
    forged["pieces"].pop()
    assert not replay_star(bounds, rows, c, 0, forged)


def test_unsupported_coupling_is_rejected():
    with pytest.raises(ValueError, match="mixed quadratic"):
        support_star(((0, 1),) * 3, (), {(0, 1, 1): 1})
    with pytest.raises(ValueError, match="affine row"):
        support_star(((0, 1),) * 3, [((0, 1, 1), 1)], {})
    with pytest.raises(ValueError, match="quadratic monomial"):
        support_star(((0, 1),) * 3, (), {(0, 3, 0): 1})
