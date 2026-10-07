#!/usr/bin/env python3
"""Exact finite diagnostics for the all-optimal-flow face certificate.

Flows are exhaustively enumerated on small networks. Core objectives are
at most quadratic, so the tested Taylor differences are minimized exactly.
This is not a convex-flow oracle or a general polynomial-box solver.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product


ZERO = (F(0), F(0), F(0))


def polynomial(coefficients, t):
    a, b, c = coefficients
    return a * t * t + b * t + c


def quadratic_min(a, b, c, lo, hi):
    candidates = [lo, hi]
    if a > 0 and lo <= -b / (2 * a) <= hi:
        candidates.append(-b / (2 * a))
    return min((a * t * t + b * t + c, t) for t in candidates)


@dataclass(frozen=True)
class Fixture:
    name: str
    arcs: tuple
    bounds: tuple
    supply: tuple
    g: tuple
    q: tuple
    potentials: tuple
    potential_slopes: tuple
    width: F
    tangent: tuple = (F(0), F(0))
    center: F = F(0)
    cross: F = F(0)
    base_slope: F = F(1)
    upper_face: bool = False

    def flows(self):
        feasible = []
        for z in product(*(range(lo, hi + 1) for lo, hi in self.bounds)):
            balance = [0] * len(self.supply)
            for (tail, head), flow in zip(self.arcs, z):
                balance[tail] += flow
                balance[head] -= flow
            if tuple(balance) == self.supply:
                feasible.append(z)
        assert feasible
        return feasible

    def potential(self, node, tangent):
        return self.potentials[node] + self.potential_slopes[node] * tangent

    def arc_cost(self, arc, distance, tangent, flow):
        tail, head = self.arcs[arc]
        return (
            polynomial(self.g[arc], flow)
            - (self.potential(tail, tangent) - self.potential(head, tangent)) * flow
            + distance * polynomial(self.q[arc], flow)
        )

    def objective(self, distance, tangent, z):
        return (
            (distance * distance + tangent * tangent) / 2
            + self.cross * distance * tangent
            + self.base_slope * distance
            + sum(self.arc_cost(a, distance, tangent, flow)
                  for a, flow in enumerate(z))
        )


def make_fixtures():
    tie = (F(1), F(-1), F(1, 4))
    square = (F(1), F(0), F(0))
    concave = (F(-1, 4), F(0), F(0))
    linear = (F(0), F(1), F(0))
    cycle = ((0, 1), (1, 2), (2, 0))
    pi = (F(0), F(1, 3), F(-2, 5))
    return [
        Fixture(
            "parallel long flat / upper face", ((0, 1), (0, 1)),
            ((0, 3), (0, 3)), (3, -3), (ZERO, ZERO),
            (square, (F(2), F(-4), F(2))),
            (F(1, 3), F(-2, 5)), (F(1, 7), F(0)), F(1),
            upper_face=True,
        ),
        Fixture(
            "cycle plus parallel / two-point interpolation", cycle + ((0, 1),),
            ((0, 2),) * 4, (0, 0, 0), (tie, ZERO, ZERO, tie),
            (concave, square, square, concave), pi,
            (F(1, 7), F(0), F(-1, 9)), F(1, 16),
            tangent=(F(1, 5), F(2, 5)), center=F(3, 10), cross=F(1, 4),
        ),
        Fixture(
            "cycle sharp distance", cycle, ((0, 2),) * 3, (0, 0, 0),
            (square, ZERO, ZERO),
            (concave, (F(0), F(-1), F(0)), (F(0), F(-1), F(0))),
            pi, (F(0),) * 3, F(1, 6),
        ),
        Fixture(
            "signed cycle intervals", cycle, ((-1, 1),) * 3, (0, 0, 0),
            (square, ZERO, ZERO),
            (concave, linear, (F(0), F(-2), F(0))),
            pi, (F(0),) * 3, F(1, 12),
        ),
        Fixture(
            "parallel arcs plus self-loop", ((0, 1), (0, 1), (0, 0)),
            ((0, 1), (0, 1), (0, 2)), (1, -1), (ZERO, ZERO, square),
            (linear, (F(0), F(2), F(0)), concave),
            (F(1, 3), F(-2, 5)), (F(0), F(0)), F(1, 12),
        ),
    ]


def interval_violation(z, intervals):
    return sum(max(lo - value, 0, value - hi)
               for value, (lo, hi) in zip(z, intervals))


def run_fixture(case, counts):
    flows = case.flows()
    r = len(case.arcs)
    intervals = []
    for arc, (lo, hi) in enumerate(case.bounds):
        values = [(polynomial(case.g[arc], t), t) for t in range(lo, hi + 1)]
        minimum = min(value for value, _ in values)
        winners = [t for value, t in values if value == minimum]
        assert winners == list(range(winners[0], winners[-1] + 1))
        intervals.append((winners[0], winners[-1]))
    tight = [z for z in flows if interval_violation(z, intervals) == 0]
    assert tight
    z0 = tight[0]
    optimum = min(case.objective(F(0), case.center, z) for z in flows)
    assert tight == [z for z in flows if case.objective(F(0), case.center, z) == optimum]
    counts["flow interval classifications"] += len(flows)

    K = F(0)
    for a, ((lo, hi), (ilo, ihi)) in enumerate(zip(case.bounds, intervals)):
        ga, _, _ = case.g[a]
        qa, qb, _ = case.q[a]
        assert min(ga, ga + qa) >= 0  # Native real flow convexity for all inward distances in [0,1].
        K = max(K, abs(2 * qa * lo + qb), abs(2 * qa * hi + qb))
        tail, head = case.arcs[a]
        K = max(K, abs(case.potential_slopes[tail] - case.potential_slopes[head]))
        if ilo == ihi:
            counts["singleton derivative intervals"] += 1
        elif ihi == ilo + 1:
            counts["two-point derivative intervals"] += 1
            slope = polynomial(case.q[a], ihi) - polynomial(case.q[a], ilo)
            for t in (ilo, ihi):
                interpolated = polynomial(case.q[a], ilo) + slope * (t - ilo)
                assert interpolated == polynomial(case.q[a], t)
            if qa < 0:
                midpoint = F(ilo + ihi, 2)
                assert polynomial(case.q[a], midpoint) > (
                    polynomial(case.q[a], ilo) + polynomial(case.q[a], ihi)
                ) / 2
                counts["necessary concave-to-linear interpolations"] += 1
        else:
            assert case.g[a][0] == case.g[a][1] == 0
            assert qa >= 0
            counts["long flat convex derivative intervals"] += 1
        # Reduced costs recover g exactly despite nonzero, varying potentials.
        for tangent in {case.tangent[0], case.center, case.tangent[1]}:
            potential_difference = case.potential(tail, tangent) - case.potential(head, tangent)
            for t in range(lo, hi + 1):
                assert case.arc_cost(a, F(0), tangent, t) + potential_difference * t == polynomial(case.g[a], t)
            for t in range(ilo, ihi + 1):
                assert polynomial(case.g[a], t) == polynomial(case.g[a], z0[a])
        # Exact residual marginal inequalities for the supplied conditional optimizer.
        for neighbor in (z0[a] - 1, z0[a] + 1):
            if lo <= neighbor <= hi:
                assert polynomial(case.g[a], neighbor) >= polynomial(case.g[a], z0[a])

    beta = case.base_slope + case.cross * case.center + min(
        sum(polynomial(q, value) for q, value in zip(case.q, z)) for z in tight
    )
    # Evaluate the convex representations on all tight integer flows independently.
    represented_derivatives = []
    for z in tight:
        value = case.base_slope + case.cross * case.center
        for q, flow, (lo, hi) in zip(case.q, z, intervals):
            if hi == lo + 1:
                value += polynomial(q, lo) + (polynomial(q, hi) - polynomial(q, lo)) * (flow - lo)
            else:
                value += polynomial(q, flow)
        represented_derivatives.append(value)
    assert min(represented_derivatives) == beta
    counts["optimal-flow derivative checks"] += len(tight)

    outside = []
    for g, (lo, hi), (ilo, ihi) in zip(case.g, case.bounds, intervals):
        if ilo > lo:
            outside.append(polynomial(g, ilo - 1) - polynomial(g, ilo))
        if ihi < hi:
            outside.append(polynomial(g, ihi + 1) - polynomial(g, ihi))
    mu = min(outside) if outside else F(0)
    H = 1 + abs(case.cross)  # Exact Hessian norm of the two-core quadratic.
    radius = max(abs(case.tangent[0] - case.center), abs(case.tangent[1] - case.center))
    assert not outside or mu >= r * K * case.width
    coefficient = beta - H * radius - H * case.width / 2
    assert coefficient > 0
    face_arc_optimum = sum(polynomial(g, flow) for g, flow in zip(case.g, z0))
    sharp = False
    for z in flows:
        violation = interval_violation(z, intervals)
        distance = min(sum(abs(a - b) for a, b in zip(z, winner)) for winner in tight)
        assert distance <= r * violation
        sharp |= bool(violation and distance == r * violation)
        counts["nearest-tight-flow bounds"] += 1
        gap = sum(polynomial(g, flow) for g, flow in zip(case.g, z)) - face_arc_optimum
        assert gap >= mu * violation
        slope = case.base_slope + sum(polynomial(q, flow) for q, flow in zip(case.q, z))
        # Each difference is affine in the tangent coordinate, so its box minimum
        # occurs at a tangent endpoint. The remaining univariate quadratic is
        # minimized at its endpoints and any interior stationary point.
        for tangent in set(case.tangent):
            actual_slope = slope + case.cross * tangent
            assert actual_slope >= beta - H * radius - K * distance
            intermediate = quadratic_min(
                (1 + H) / 2,
                actual_slope + r * K * violation - beta + H * radius,
                gap - mu * violation,
                F(0), case.width,
            )[0]
            final = quadratic_min(F(1, 2), actual_slope - coefficient, gap,
                                  F(0), case.width)[0]
            actual = quadratic_min(F(1, 2), actual_slope, gap, F(0), case.width)[0]
            assert intermediate >= 0 and final >= 0 and actual >= 0
            counts["exact Taylor polynomial minima"] += 3
            for distance_inward in (F(0), case.width / 2, case.width):
                face_value = min(case.objective(F(0), tangent, winner) for winner in flows)
                difference = case.objective(distance_inward, tangent, z) - face_value
                assert difference == gap + actual_slope * distance_inward + distance_inward**2 / 2
                # Both lower and upper original faces use the same inward distance.
                original_coordinate = 1 - distance_inward if case.upper_face else distance_inward
                recovered = 1 - original_coordinate if case.upper_face else original_coordinate
                assert recovered == distance_inward
    if case.name == "cycle sharp distance":
        assert sharp
    counts["sharp-distance fixtures"] += int(sharp)
    counts["network fixtures"] += 1


def check_two_arc_boundary(counts):
    flows = ((1, 0), (0, 1))
    gammas = ((F(1, 2), F(1, 2)), (F(1, 2), F(3, 4)), (F(3, 4), F(1)))
    widths = ((F(1, 4), F(1, 3)), (F(3, 4), F(1, 2)), (F(1, 8), F(1, 8)))
    for gamma, width in product(gammas, widths):
        beta = tuple(min(gamma[i] + z[i] for z in flows) for i in range(2))
        assert beta == gamma
        coefficient = min(beta) - max(width) / 2  # H=1, R=0.
        assert coefficient > 0
        for z in flows:
            exact_minimum = sum(quadratic_min(F(1, 2), gamma[i] + z[i] - coefficient,
                                             F(0), F(0), width[i])[0] for i in range(2))
            assert exact_minimum == 0
            counts["two-arc exact polynomial minima"] += 1
        assert width[0] * flows[0][0] > width[0] * flows[1][0]
        assert width[1] * flows[0][1] < width[1] * flows[1][1]
        counts["two-arc boundary boxes"] += 1


def check_losing_threshold_guard(counts):
    # One unit on two parallel arcs. At the face, arc two loses by 1/8.
    # Its inward slope -8 overturns that gap within the proposed width 1/4.
    width, mu, beta, H, K, r = F(1, 4), F(1, 8), F(1), F(1), F(8), 2
    coefficient = beta - H * width / 2
    assert coefficient > 0
    assert mu < r * K * width
    winner_min = quadratic_min(F(1, 2), F(1), F(0), F(0), width)
    loser_min = quadratic_min(F(1, 2), F(-8), mu, F(0), width)
    assert winner_min[0] == 0
    assert loser_min == (F(-59, 32), width)
    assert loser_min[0] < coefficient * loser_min[1]
    # The violated interval is arc two's singleton {0}; changing to the
    # winning flow changes both arcs, attaining the r=2 distance bound.
    assert sum(abs(a - b) for a, b in zip((0, 1), (1, 0))) == r
    counts["losing-flow rejection guards"] += 1


def main():
    from collections import Counter

    counts = Counter()
    for case in make_fixtures():
        run_fixture(case, counts)
    check_two_arc_boundary(counts)
    check_losing_threshold_guard(counts)
    print("PASS: " + "; ".join(f"{value} {name}" for name, value in counts.items()))
    print("Scope: exhaustive small integer flows and exact quadratic core minima; no production flow oracle, binary-search interval routine, or general polynomial minimizer.")


if __name__ == "__main__":
    main()
