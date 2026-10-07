#!/usr/bin/env python3
"""Exact small order-polytope checks for LP forcing and feasible rounding."""
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path


def feasible(x, edges):
    return all(0 <= t <= 1 for t in x) and all(x[i] <= x[j] for i, j in edges)


def optimum(target, gamma, edges):
    n = len(target)
    candidates = set()
    for active in product((0, 1), repeat=len(edges)):
        parent = list(range(n))
        def find(i):
            while parent[i] != i:
                i = parent[i]
            return i
        for (i, j), flag in zip(edges, active):
            if flag:
                parent[find(i)] = find(j)
        groups = {}
        for i in range(n):
            groups.setdefault(find(i), []).append(i)
        blocks = list(groups.values())
        for states in product((-1, 0, 1), repeat=len(blocks)):
            point = [Q(0)]*n
            for block, state in zip(blocks, states):
                value = (sum(target[i]-gamma[i]/2 for i in block)/len(block)
                         if state == -1 else Q(state))
                for i in block:
                    point[i] = value
            if feasible(point, edges):
                candidates.add(tuple(point))
    def objective(x):
        return sum((x[i]-target[i])**2+gamma[i]*x[i] for i in range(n))
    best = min(map(objective, candidates))
    winners = [x for x in candidates if objective(x) == best]
    assert len(winners) == 1
    return winners[0], objective


def proposals(n, edges):
    return ([('edge', i, j) for i, j in edges]+
            [('lower', i, i) for i in range(n)]+
            [('upper', i, i) for i in range(n)])


def active_at(point, proposal):
    kind, i, j = proposal
    return point[i] == point[j] if kind == 'edge' else point[i] == (kind == 'upper')


def violates_vertex(vertex, proposal):
    kind, i, j = proposal
    if kind == 'edge':
        return vertex[i] == 0 and vertex[j] == 1
    return vertex[i] == (kind == 'lower')


def gap(vector, vertices, proposal):
    bad = [v for v in vertices if violates_vertex(v, proposal)]
    if not bad:
        return None
    cost = lambda v: sum(a*b for a, b in zip(vector, v))
    return min(map(cost, bad))-min(map(cost, vertices))


def threshold_law(x, h):
    scaled = [t/h for t in x]
    lower = [t.numerator//t.denominator for t in scaled]
    fractions = [t-k for t, k in zip(scaled, lower)]
    breakpoints = sorted({Q(0), Q(1), *fractions})
    return [(tuple(h*(k+(u < t)) for k, t in zip(lower, fractions)), hi-lo)
            for lo, hi in zip(breakpoints, breakpoints[1:])
            for u in [(lo+hi)/2]]


def main():
    graphs = [('chain', [(0, 1), (1, 2)]),
              ('fork', [(0, 1), (0, 2)]),
              ('cycle', [(0, 1), (1, 0), (1, 2)])]
    target = (Q(3, 4), Q(1, 4), Q(1, 2))
    counts = dict(draws=0, forced_equalities=0, active_gap_tests=0,
                  zero_gap_incidences=0, rounding_atoms=0, gap_lipschitz=0,
                  face_probability_tests=0)
    for _, edges in graphs:
        vertices = [tuple(map(Q, v)) for v in product((0, 1), repeat=3) if feasible(v, edges)]
        checks = proposals(3, edges)
        for M in (2, 3, 4):
            labels = [Q(-1)+Q(2*k, M-1) for k in range(M)]
            events = {}
            for gamma in product(labels, repeat=3):
                a, objective = optimum(target, gamma, edges)
                counts['draws'] += 1
                true_gradient = tuple(2*(v-t)+g for v, t, g in zip(a, target, gamma))
                face = tuple(active_at(a, e) for e in checks)
                for e_index, e in enumerate(checks):
                    true_gap = gap(true_gradient, vertices, e)
                    if face[e_index] and true_gap is not None:
                        assert true_gap >= 0
                        counts['active_gap_tests'] += 1
                        if true_gap == 0:
                            counts['zero_gap_incidences'] += 1
                        for tau in (Q(0), Q(1, 8)):
                            if true_gap <= tau:
                                key = (face, e_index, tau)
                                events[key] = events.get(key, 0)+1
                for radius in (Q(1, 2), Q(1, 8), Q(1, 32)):
                    bounds = [(max(Q(0), v-radius), min(Q(1), v+radius)) for v in a]
                    midpoint = [(lo+hi)/2 for lo, hi in bounds]
                    r = max((hi-lo)/2 for lo, hi in bounds)
                    delta = 2*r
                    gradient = tuple(2*(v-t)+g for v, t, g in zip(midpoint, target, gamma))
                    for e in checks:
                        estimated = gap(gradient, vertices, e)
                        exact = gap(true_gradient, vertices, e)
                        if estimated is None or estimated > 3*delta:
                            assert active_at(a, e)
                            counts['forced_equalities'] += 1
                        if exact is not None:
                            assert abs(estimated-exact) <= 3*max(abs(x-y) for x, y in zip(gradient, true_gradient))
                            counts['gap_lipschitz'] += 1
                for h in (Q(1), Q(1, 2), Q(1, 4)):
                    law = threshold_law(a, h)
                    assert sum(w for _, w in law) == 1
                    assert all(sum(w*y[i] for y, w in law) == a[i] for i in range(3))
                    expected = Q(0)
                    for y, weight in law:
                        assert feasible(y, edges)
                        assert all(abs(t-s) <= h for t, s in zip(y, a))
                        expected += weight*objective(y)
                        counts['rounding_atoms'] += 1
                    assert expected <= objective(a)+Q(3, 4)*h*h  # H=2, n=3.
            for (_, _, tau), number in events.items():
                # D=1. A fixed face/proposal event is bounded before the union.
                assert Q(number, M**3) <= tau+Q(2, M)
                counts['face_probability_tests'] += 1
    result = dict(status='passed', scope='finite exact order forcing/rounding review', counts=counts)
    Path(__file__).with_name('order-polytope-review-check-results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
