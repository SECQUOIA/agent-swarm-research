"""Exact finite regression checks for the AC section; not a proof certificate.

Uses only the Python standard library. Crossings are compared with a chord's
intersection with the positive ray; cycle winding is independently counted
at a rotated ray. No transcendental angle evaluation or floating point occurs.
"""
from fractions import Fraction as F
from itertools import combinations, permutations, product
import json


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


def crossing(start, end):
    d = det(start, end)
    if start[1] < 0 <= end[1] and d > 0:
        return 1
    if end[1] < 0 <= start[1] and d < 0:
        return -1
    return 0


def chord_crossing(start, end):
    """Independent segment/ray intersection, with the manuscript endpoint rule."""
    if not (start[1] < 0 <= end[1] or end[1] < 0 <= start[1]):
        return 0
    parameter = -start[1] / (end[1] - start[1])
    intersection = start[0] + parameter * (end[0] - start[0])
    if intersection <= 0:
        return 0
    return 1 if end[1] > start[1] else -1


def admissible(a, b):
    return not (det(a, b) == 0 and dot(a, b) < 0)


def scale(a, r):
    return a[0] * r, a[1] * r


def rotated(a):
    # The positive ray in these coordinates has original direction (5,2).
    return 5 * a[0] + 2 * a[1], 5 * a[1] - 2 * a[0]


def cmul(a, b):
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def conjugate(a):
    return a[0], -a[1]


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def sub(a, b):
    return a[0] - b[0], a[1] - b[1]


def vertex_shifts(vertex_count, edges):
    """Solve a[end]-a[start]=k, with one zero root per component.

    Edges are (start, end, k). Return None on an inconsistent cycle.
    The computation uses exact rational arithmetic, not integer rounding.
    """
    adjacency = [[] for _ in range(vertex_count)]
    for start, end, k in edges:
        adjacency[start].append((end, F(k)))
        adjacency[end].append((start, -F(k)))
    shifts = [None] * vertex_count
    for root in range(vertex_count):
        if shifts[root] is not None:
            continue
        shifts[root] = F(0)
        pending = [root]
        while pending:
            start = pending.pop()
            for end, k in adjacency[start]:
                proposed = shifts[start] + k
                if shifts[end] is None:
                    shifts[end] = proposed
                    pending.append(end)
                elif shifts[end] != proposed:
                    return None
    return shifts


def all_cycle_sums_zero(vertex_count, edges):
    """Independent oracle: enumerate simple cycles, without a spanning tree."""
    weights = {}
    for start, end, k in edges:
        weights[start, end] = k
        weights[end, start] = -k
    for length in range(3, vertex_count + 1):
        for vertices in combinations(range(vertex_count), length):
            for tail in permutations(vertices[1:]):
                cycle = (vertices[0],) + tail
                if cycle[1] > cycle[-1]:
                    continue  # Reversals have the same zero-sum outcome.
                steps = list(zip(cycle, cycle[1:] + cycle[:1]))
                if all(edge in weights for edge in steps):
                    if sum(weights[edge] for edge in steps) != 0:
                        return False
    return True


def check_vertex_shifts():
    # Exhaust all simple graphs through four vertices and three-valued edge
    # counts. Missing edges include forests, isolated vertices and components.
    cases = 0
    consistent = 0
    for vertex_count in range(5):
        possible = list(combinations(range(vertex_count), 2))
        for choices in product([None, -1, 0, 1], repeat=len(possible)):
            edges = [(start, end, k) for (start, end), k in zip(possible, choices)
                     if k is not None]
            shifts = vertex_shifts(vertex_count, edges)
            assert (shifts is not None) == all_cycle_sums_zero(vertex_count, edges)
            # Reorienting every edge changes neither feasibility nor shifts.
            assert shifts == vertex_shifts(vertex_count,
                                           [(end, start, -k) for start, end, k in edges])
            if shifts is not None:
                assert all(a.denominator == 1 for a in shifts)
                assert all(shifts[end] - shifts[start] == k for start, end, k in edges)
                consistent += 1
            cases += 1
    assert vertex_shifts(0, []) == []
    assert vertex_shifts(3, []) == [0, 0, 0]
    assert vertex_shifts(5, [(0, 1, 1), (2, 3, -1)]) == [0, 1, 0, -1, 0]
    assert vertex_shifts(3, [(0, 1, 1), (1, 2, -1), (2, 0, 1)]) is None
    return cases, consistent


def main():
    axes = [(F(1), F(0)), (F(0), F(1)), (F(-1), F(0)), (F(0), F(-1))]
    rays = axes + [(sx * F(a, 5), sy * F(b, 5))
                   for a, b in [(3, 4), (4, 3)] for sx, sy in product([-1, 1], repeat=2)]
    assert len(rays) == 12 and all(dot(a, a) == 1 for a in rays)
    scales = [F(1, 3), F(1), F(2), F(7)]
    cosines = [F(-9, 10), F(-4, 5), F(-3, 5), F(0), F(3, 5), F(4, 5), F(1)]
    pairs = 0
    long_arcs = 0
    cosine_checks = 0
    for a, b in product(rays, repeat=2):
        if not admissible(a, b):
            continue
        for ra, rb in product(scales, repeat=2):
            start, end = scale(a, ra), scale(b, rb)
            k = crossing(start, end)
            assert k == chord_crossing(start, end)
            assert crossing(end, start) == -k
            assert k == crossing(a, b)
            pairs += 1
            long_arcs += dot(a, b) < 0
            assert dot(start, start) == ra * ra
            assert dot(end, end) == rb * rb
            for c in cosines:
                assert (dot(start, end) >= c * ra * rb) == (dot(a, b) >= c)
                cosine_checks += 1

    # Legacy e_i+e_j test fails on this >pi/2 short arc with unequal radii.
    start, end = (F(4), F(-3)), (F(-30), F(40))
    assert dot(start, end) < 0 and start[0] + end[0] < 0
    assert crossing(start, end) == chord_crossing(start, end) == 1
    assert not admissible((F(1), F(0)), (F(-1), F(0)))

    permitted = {(i, j): admissible(a, b)
                 for i, a in enumerate(rays) for j, b in enumerate(rays)}
    counts = {(i, j): crossing(a, b)
              for i, a in enumerate(rays) for j, b in enumerate(rays)}
    rotated_counts = {(i, j): chord_crossing(rotated(a), rotated(b))
                      for i, a in enumerate(rays) for j, b in enumerate(rays)}
    cycles = 0
    winding_cycles = 0
    for length in range(2, 6):
        for nodes in product(range(len(rays)), repeat=length):
            edges = list(zip(nodes, nodes[1:] + nodes[:1]))
            if not all(permitted[edge] for edge in edges):
                continue
            winding = sum(counts[edge] for edge in edges)
            assert winding == sum(rotated_counts[edge] for edge in edges)
            cycles += 1
            winding_cycles += winding != 0

    # Independently expand complex currents for rational line/shunt parameters.
    power_cases = 0
    for ui, uj, (g, b), (h, t) in product(
            [scale(a, r) for a in rays[:6] for r in scales[:2]], rays[:6],
            [(F(1), F(0)), (F(2), F(-3, 2)), (F(0), F(2, 3))],
            [(F(0), F(0)), (F(1, 2), F(-2)), (F(0), F(3))]):
        current = add(cmul((h, t), ui), cmul((g, b), sub(ui, uj)))
        actual = cmul(ui, conjugate(current))
        r2, hij, dij = dot(ui, ui), dot(ui, uj), det(uj, ui)
        formula = (h * r2 + g * (r2 - hij) - b * dij,
                   -t * r2 - b * (r2 - hij) - g * dij)
        assert actual == formula
        power_cases += 1

    # Rational four-cycle: P=2, Q=0, winding=1; equal-angle P would be zero.
    assert sum(crossing(axes[k], axes[(k + 1) % 4]) for k in range(4)) == 1
    for k, ui in enumerate(axes):
        current = add(sub(ui, axes[(k - 1) % 4]), sub(ui, axes[(k + 1) % 4]))
        assert cmul(ui, conjugate(current)) == (2, 0)
    winding_edges = [(k, (k + 1) % 4, crossing(axes[k], axes[(k + 1) % 4]))
                     for k in range(4)]
    assert vertex_shifts(4, winding_edges) is None
    assert vertex_shifts(4, winding_edges[:-1]) == [0, 0, 0, 0]
    # A zero-winding cycle whose real lift requires a nonzero integer shift.
    phasors = [axes[3], axes[0], axes[1], axes[0]]
    lift_edges = [(k, (k + 1) % 4, crossing(phasors[k], phasors[(k + 1) % 4]))
                  for k in range(4)]
    assert all(admissible(phasors[k], phasors[(k + 1) % 4]) for k in range(4))
    assert vertex_shifts(4, lift_edges) == [0, 1, 1, 1]
    potential_cases, consistent_potential_cases = check_vertex_shifts()

    # Sum Q=0 for arbitrary rational resistive phasors, before any angle bound.
    phasors = [scale(rays[k], scales[k % 4]) for k in range(6)]
    edges = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 5)]
    reactive = [F(0) for _ in phasors]
    for edge_number, (i, j) in enumerate(edges):
        g = F(edge_number + 1, 3)
        reactive[i] -= g * det(phasors[j], phasors[i])
        reactive[j] -= g * det(phasors[i], phasors[j])
    assert sum(reactive) == 0

    # Rational size-dependent cosines are positive, <1, with quadratic denominator.
    for n in range(2, 101):
        c = 1 - F(1, n * n)
        assert 0 < c < 1 and c.denominator <= n * n

    print(json.dumps({
        'status': 'PASS', 'scaled_short_arc_pairs': pairs,
        'pairs_longer_than_pi_over_2': long_arcs,
        'rational_cosine_checks': cosine_checks,
        'cycles_against_rotated_cut': cycles, 'nonzero_winding_cycles': winding_cycles,
        'complex_power_sign_cases': power_cases,
        'vertex_shift_cases_against_all_cycles': potential_cases,
        'consistent_vertex_shift_cases': consistent_potential_cases,
        'regressions': ['unequal-radius long arc', 'antipodal exclusion',
                        'rational four-cycle', 'reactive sum identity',
                        'empty and disconnected potential systems',
                        'inconsistent cycles', 'integer shifts across the branch cut',
                        'positive polynomial-bit cosine inputs'],
        'scope': 'finite exact regression checks, not proofs of the quantified theorems'
    }, indent=2))


if __name__ == '__main__':
    main()
