"""Exact small-instance diagnostics for the integer-label isolation lemma.

Enumerates complete finite noise laws, not random samples. This does not
implement the proposed mixed-integer optimizer or prove the general lemma.
"""

from fractions import Fraction as Q
from itertools import combinations, product
import json


def envelope_breakpoints(groups):
    points = set()
    for (t, a), (u, b) in combinations(groups.items(), 2):
        crossing = (b - a) / (t - u)
        value = a + t * crossing
        if all(value <= c + s * crossing for s, c in groups.items()):
            points.add(crossing)
    return points


def check_fixture(labels, costs, bounds, size, sigma, thresholds, counts):
    dimension = len(bounds)
    width_sum = sum(hi - lo for lo, hi in bounds)
    grid = [-sigma + 2 * sigma * j / (size - 1) for j in range(size)]
    sections = {}
    for i, (lo, hi) in enumerate(bounds):
        for other in product(grid, repeat=dimension - 1):
            groups = {}
            for label, cost in zip(labels, costs):
                remainder = tuple(label[j] for j in range(dimension) if j != i)
                value = cost + sum(a * b for a, b in zip(remainder, other))
                slope = label[i]
                if slope not in groups or value < groups[slope]:
                    groups[slope] = value
            points = envelope_breakpoints(groups)
            assert len(points) <= hi - lo
            sections[i, other] = groups, points
            counts['conditional_sections'] += 1

    events = {eps: 0 for eps in thresholds}
    for noise in product(grid, repeat=dimension):
        values = sorted(cost + sum(a * b for a, b in zip(label, noise))
                        for label, cost in zip(labels, costs))
        gap = values[1] - values[0] if len(values) > 1 else None
        if gap == 0:
            counts['tied_draws'] += 1
        for eps in thresholds:
            if gap is not None and gap <= eps:
                events[eps] += 1
                witnesses = 0
                for i in range(dimension):
                    other = tuple(noise[j] for j in range(dimension) if j != i)
                    groups, points = sections[i, other]
                    group_values = sorted(a + t * noise[i] for t, a in groups.items())
                    if len(group_values) > 1 and group_values[1] - group_values[0] <= eps:
                        witnesses += 1
                        assert any(abs(noise[i] - b) <= eps for b in points)
                        counts['breakpoint_witnesses'] += 1
                assert witnesses
        counts['noise_draws'] += 1

    total = size ** dimension
    for eps, events_count in events.items():
        probability = Q(events_count, total)
        upper = width_sum * (eps / sigma + Q(1, size))
        assert probability <= upper, (probability, upper, labels, eps)
        counts['probability_bounds'] += 1
    counts['fixtures'] += 1


def main():
    counts = dict(fixtures=0, noise_draws=0, tied_draws=0,
                  conditional_sections=0, breakpoint_witnesses=0,
                  probability_bounds=0)
    thresholds = [Q(0), Q(1, 128), Q(1, 32), Q(1, 8), Q(1, 2)]
    fixtures = [
        ([(0,), (1,)], [Q(0), Q(0)], [(0, 1)], 17, Q(1)),
        ([(0,), (1,)], [Q(0), Q(-1)], [(0, 1)], 17, Q(1)),
        ([(0,), (2,)], [Q(0), Q(1, 7)], [(0, 2)], 33, Q(1)),
        ([(4,)], [Q(-100)], [(4, 4)], 9, Q(1)),
        ([(0, 0), (0, 2), (2, 0), (1, 1)],
         [Q(0), Q(1, 7), Q(-1, 5), Q(1, 11)], [(0, 2), (0, 2)], 17, Q(1)),
        ([(-1, 0), (0, 1), (1, 0), (0, -1), (0, 0)],
         [Q(0), Q(0), Q(0), Q(0), Q(-1, 3)], [(-1, 1), (-1, 1)], 17, Q(2)),
        ([(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)],
         [Q(0), Q(1, 5), Q(-2, 7), Q(1, 9)], [(0, 1)] * 3, 9, Q(1)),
        (list(product(range(2), repeat=3)),
         [Q(0)] * 8, [(0, 1)] * 3, 9, Q(1)),
    ]
    for fixture in fixtures:
        check_fixture(*fixture, thresholds, counts)
    print(json.dumps(counts, sort_keys=True))


if __name__ == '__main__':
    main()
