"""Exact sublevel-ball and weak-coordinate-bound fixtures.

These are interval/diagonal-polytope fixtures with known extrema, not
an implementation of GLS or the general algebraic fallback.
"""

from fractions import Fraction as Q
from itertools import product

fixtures = extrema_checks = ball_checks = hull_checks = 0
for k, curvature, q, thin in product(
    (1, 2, 5), (Q(1), Q(1, 1024)), (0, 3, 40), (False, True)
):
    # P has k equal core coordinates t. Relative coordinate is w=t-center.
    lower = Q(1, 4)
    side = Q(1, 2**100) if thin else Q(1, 2)
    upper = lower + side
    center = (lower + upper) / 2
    epsilon = Q(1, 2**q)
    growth = curvature / k
    g0 = growth / 2
    delta = min(epsilon / 4, g0 * epsilon**2 / (128 * k))
    zeta = epsilon / (8 * k)
    # The incumbent is exactly the midpoint optimizer, U=0. The chosen
    # constants make the untruncated sublevel radius rational.
    sublevel_radius = epsilon / (16 * k)
    assert curvature * sublevel_radius**2 == delta
    true_lower = max(lower, center - sublevel_radius)
    true_upper = min(upper, center + sublevel_radius)

    W = max(Q(1), curvature * side**2)
    lam = min(Q(1, 2), delta / (8 * W))
    relative_radius = side / 2
    inner_radius = lam * relative_radius
    for relative_point in (-inner_radius, Q(0), inner_radius):
        t = center + relative_point
        assert lower <= t <= upper
        assert curvature * (t - center) ** 2 <= delta / 4
        ball_checks += 1

    # The coordinate objectives +/-t have norm one in relative coordinates.
    eta = min(inner_radius / 2, zeta / (2 + 1 / inner_radius))
    assert eta > 0
    assert true_upper - true_lower >= 2 * eta
    enclosures = {}
    for sign in (-1, 1):
        maximum = true_upper if sign == 1 else -true_lower
        eroded_maximum = maximum - eta
        # Both endpoints of an adversarial interval of weak answers are
        # tested, including a slightly infeasible upper answer.
        for reported in (eroded_maximum - eta, maximum, maximum + eta):
            assert reported >= eroded_maximum - eta
            assert reported <= maximum + eta
            bound = reported + eta * (1 + 1 / inner_radius)
            assert maximum <= bound <= maximum + zeta
            extrema_checks += 1
        enclosures[sign] = maximum + eta + eta * (1 + 1 / inner_radius)
    hull_lower = max(Q(0), -enclosures[-1])
    hull_upper = min(Q(1), enclosures[1])
    assert hull_lower <= true_lower <= center <= true_upper <= hull_upper
    diameter_sq = k * (hull_upper - hull_lower) ** 2
    assert diameter_sq <= epsilon**2 / 4
    hull_checks += 1
    fixtures += 1

print(
    f"PASS: {fixtures} fixtures, {ball_checks} sublevel-ball points, "
    f"{extrema_checks} weak-extremum enclosures, {hull_checks} core hulls; "
    "includes 100-bit thin diagonal polytopes and 40-bit queries."
)
