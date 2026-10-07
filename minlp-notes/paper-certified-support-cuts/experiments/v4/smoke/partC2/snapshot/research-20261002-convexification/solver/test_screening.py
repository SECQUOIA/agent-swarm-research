"""Targeted checks for the graph-witness trust boundary and dual norm."""

from copy import deepcopy
from fractions import Fraction as F
import math

import pytest

from screening import (
    Interval,
    SampleCache,
    bind_samples,
    normalize_weights,
    replay_screen,
    screen_convex_combination,
    upper_float,
)


def line(point):
    return point[0], point[0]


def parabola(point):
    return point[0], point[0] ** 2


def test_exact_dual_norm_distinction_at_line_hull():
    samples = bind_samples([(0,), (1,)], bounds=[(0, 1)], evaluate=line)
    infinity = screen_convex_combination((1, 0), samples, [1, 1], threshold=F(1, 2))
    one = screen_convex_combination((1, 0), samples, [1, 1], threshold=F(1, 2), norm="1")
    # The line hull has support zero in directions (1,-1) and (1/2,-1/2).
    assert infinity.upper_bound == F(1, 2)
    assert one.upper_bound == 1
    assert infinity.can_skip
    assert not one.can_skip


def test_interval_bound_uses_far_endpoint_not_distance_to_enclosure():
    samples = bind_samples([(0,)], bounds=[(0, 0)], evaluate=lambda _: [Interval(1, 2)])
    result = screen_convex_combination([1], samples, [1])
    assert result.upper_bound == 1
    assert not result.can_skip


def test_normalized_floating_weights_repair_negative_mass_exactly():
    weights = normalize_weights([-1e-14, 0.1, 0.2])
    assert all(w >= 0 for w in weights)
    assert sum(weights) == 1
    assert weights == (0, F(1, 3), F(2, 3))
    samples = bind_samples([(0,), (F(1, 2),), (1,)], bounds=[(0, 1)], evaluate=parabola)
    result = screen_convex_combination([F(5, 6), F(3, 4)], samples, [-1e-14, 0.1, 0.2])
    assert result.upper_bound == 0
    assert result.can_skip


def test_positive_scaling_changes_normalization_and_is_exact():
    samples = bind_samples([(0,), (1,)], bounds=[(0, 1)], evaluate=line)
    result = screen_convex_combination([1, 0], samples, [1, 1], scales=[2, F(1, 2)], norm="1")
    assert result.upper_bound == F(5, 4)
    result = screen_convex_combination([1, 0], samples, [1, 1], scales=[2, F(1, 2)])
    assert result.upper_bound == 1


def test_exact_row_equalities_accept_rational_points_and_reject_near_feasible_float():
    rows = [(1, 1, 1), (-1, -1, -1)]
    cache = SampleCache(bounds=[(0, 1), (0, 1)], rows=rows, evaluate=lambda p: (*p, p[0] * p[1]))
    samples = cache.bind([(F(1, 10), F(9, 10))])
    result = screen_convex_combination([F(1, 10), F(9, 10), F(9, 100)], samples, [1])
    assert result.can_skip
    with pytest.raises(ValueError, match="affine row"):
        cache.bind([(0.1, 0.9)])


def test_cache_checks_domain_before_calling_evaluator_and_reuses_values():
    calls = []

    def evaluate(point):
        calls.append(point)
        return parabola(point)

    cache = SampleCache(bounds=[(0, 1)], rows=[(1, F(3, 4))], evaluate=evaluate)
    first = cache.bind([(0,), (F(1, 2),)])
    second = cache.bind([(F(1, 2),), (F(3, 4),), (0,)])
    assert len(calls) == 3
    assert first.values[1] is second.values[0]
    with pytest.raises(ValueError, match="affine row"):
        cache.bind([(1,)])
    with pytest.raises(ValueError, match="box"):
        cache.bind([(-1,)])
    assert len(calls) == 3


def test_positive_tolerance_does_not_imply_membership():
    samples = bind_samples([(0,)], bounds=[(0, 0)], evaluate=lambda _: [0])
    result = screen_convex_combination([F(1, 100)], samples, [1], threshold=F(1, 100))
    assert result.can_skip and result.upper_bound > 0


def test_floating_threshold_is_interpreted_as_actual_binary_value():
    samples = bind_samples([(0,)], bounds=[(0, 0)], evaluate=lambda _: [0])
    assert screen_convex_combination([F(1, 10)], samples, [1], threshold=0.1).can_skip
    assert not screen_convex_combination([F(3, 10)], samples, [1], threshold=0.3).can_skip


def _certificate():
    samples = bind_samples([(0,), (1,)], bounds=[(0, 1)], evaluate=parabola)
    return screen_convex_combination([F(1, 2), F(1, 2)], samples, [1, 1]).to_dict()


def test_replay_binds_original_graph_query_scale_domain_policy_and_norm():
    certificate = _certificate()
    args = dict(bounds=[(0, 1)], evaluate=parabola)
    point = [F(1, 2), F(1, 2)]
    assert replay_screen(point, certificate, **args)
    assert not replay_screen(point, certificate, bounds=[(F(1, 2), 1)], evaluate=parabola)
    assert not replay_screen(point, certificate, bounds=[(0, 1)], evaluate=lambda p: (p[0], p[0] ** 2 + 1))
    assert not replay_screen([F(1, 2), 0], certificate, **args)
    assert not replay_screen(point, certificate, scales=[2, 1], **args)
    assert not replay_screen(point, certificate, threshold=1, **args)
    assert not replay_screen(point, certificate, norm="1", **args)
    assert not replay_screen(point, certificate, rows=[(1, F(3, 4))], **args)


@pytest.mark.parametrize("mutate", [
    lambda c: c.update(upper_bound="-1"),
    lambda c: c.update(can_skip=False),
    lambda c: c.update(weights=["0", "0"]),
    lambda c: c["weights"].__setitem__(0, "-1"),
    lambda c: c["samples"][0]["point"].__setitem__(0, "-1"),
    lambda c: c["samples"][0]["values"][1].__setitem__(1, "1"),
    lambda c: c["combination"][1].__setitem__(0, "0"),
    lambda c: c["bounds"][0].__setitem__(1, "2"),
    lambda c: c.update(norm="1"),
    lambda c: c.update(schema="other"),
    lambda c: c.update(samples=[]),
])
def test_serialized_certificate_mutations_fail_replay(mutate):
    certificate = deepcopy(_certificate())
    mutate(certificate)
    assert not replay_screen([F(1, 2), F(1, 2)], certificate, bounds=[(0, 1)], evaluate=parabola)


@pytest.mark.parametrize("weights", [[], [0], [-1], [float("nan")], [float("inf")], [True]])
def test_invalid_weight_proposals_do_not_produce_screen(weights):
    samples = bind_samples([(0,)], bounds=[(0, 0)], evaluate=lambda _: [0])
    with pytest.raises(ValueError):
        screen_convex_combination([0], samples, weights)


@pytest.mark.parametrize("kwargs", [
    {"scales": [0]}, {"scales": [-1]}, {"scales": [float("inf")]},
    {"scales": [1, 1]}, {"threshold": -1}, {"threshold": float("nan")},
    {"norm": "2"},
])
def test_invalid_policy_arguments_rejected(kwargs):
    samples = bind_samples([(0,)], bounds=[(0, 0)], evaluate=lambda _: [0])
    with pytest.raises(ValueError):
        screen_convex_combination([0], samples, [1], **kwargs)


def test_invalid_domain_or_feature_data_rejected():
    for bounds in ([], [(1, 0)], [(0, float("inf"))], [(0, 1, 2)]):
        with pytest.raises(ValueError):
            bind_samples([(0,)], bounds=bounds, evaluate=lambda _: [0])
    with pytest.raises(ValueError):
        bind_samples([], bounds=[(0, 1)], evaluate=line)
    with pytest.raises(ValueError):
        bind_samples([(0,)], bounds=[(0, 1)], evaluate=lambda _: [(2, 1)])
    with pytest.raises(ValueError):
        bind_samples([(0,)], bounds=[(0, 1)], evaluate=lambda _: [float("nan")])
    with pytest.raises(ValueError):
        bind_samples([(0,)], bounds=[(0, 1)], evaluate=lambda _: [])


def test_outward_float_bound_includes_underflow_and_overflow():
    for bound in [F(0), F(1, 10), F(3, 10), F(1, 2**1100), F(2**2000)]:
        exported = upper_float(bound)
        assert math.isinf(exported) or F(exported) >= bound
    assert upper_float(0) == 0
    with pytest.raises(ValueError):
        upper_float(-1)


def test_existing_direction_lp_marginals_are_usable_without_second_lp():
    optimize = pytest.importorskip("scipy.optimize")
    result = optimize.linprog(
        [1, 1, 0], A_ub=[[-1, 0, 0], [-1, -1, -1]], b_ub=[0, 0],
        bounds=[(None, None), (-1, 1), (-1, 1)], method="highs",
    )
    assert result.success
    samples = bind_samples([(0,), (1,)], bounds=[(0, 1)], evaluate=line)
    certificate = screen_convex_combination(
        [1, 0], samples, -result.ineqlin.marginals, norm="1", threshold=F(1, 2)
    )
    assert certificate.upper_bound == 1
    assert not certificate.can_skip


def test_cached_mixture_is_recomputed_at_each_query():
    samples = bind_samples([(0,), (1,)], bounds=[(0, 1)], evaluate=line)
    first = screen_convex_combination([F(1, 2), F(1, 2)], samples, [1, 1], norm="1")
    later = screen_convex_combination([F(1, 2), 0], samples, first.weights, norm="1")
    assert first.can_skip
    assert later.upper_bound == F(1, 2)
    assert not later.can_skip
