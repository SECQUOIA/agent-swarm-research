#!/usr/bin/env python3
"""Focused checks for nonunique rational recovery and fixed-offset bit bounds.

These are finite exact-arithmetic checks, not an anchor-DP implementation or
a performance benchmark. Run with Python 3.10+ and the standard library.
"""

from fractions import Fraction as Q
from itertools import product
from math import lcm
import json

from exact_box_qp_checks import (
    Case, accept_candidate, check_candidate_height, height_bounds,
    reconstruct_interval, require,
)
from exact_checks import coordinate_grid, penalties


def check_nonunique_recovery(integer, counts):
    k, n, a = 3, 4, Q(2, 5)
    matrix = tuple(tuple(Q((-1 if i < k else 1) if i == j else 0)
                         for j in range(n)) for i in range(n))
    case = Case("mixed_eight_optima" if integer else "continuous_eight_optima",
                matrix, (Q(1),)*k+(-2*a,), a*a, ((Q(0), Q(1)),)*n,
                integer=integer)
    optima = tuple(tuple(map(Q, bits))+(a,) for bits in product((0, 1), repeat=k))
    projection_count = sum(len({point[i] for point in optima}) for i in range(n))
    require(len(optima) == 8 and projection_count == 2*k+1 == 7,
            "finite optimal set and coordinate projection count")
    g, curvature = Q(1), max(2*matrix[i][i] for i in range(n))
    require(curvature == 2 and all(case.feasible(point) and case.value(point) == 0
                                  for point in optima), "analytic optima and coordinate curvature")

    # On [0,1], x(1-x) >= min(x^2,(1-x)^2); the remaining square is exact.
    # These exact probes also compare coordinate distance with distance to S.
    probes = ((Q(0), Q(1, 5), Q(1, 2), Q(4, 5), Q(1)),)*k + (
        (Q(0), Q(1, 5), a, Q(3, 5), Q(1)),)
    domains = [(Q(0), Q(1)) if i in integer else values for i, values in enumerate(probes)]
    for point in product(*domains):
        distance = min(sum((x-s)**2 for x, s in zip(point, optimum)) for optimum in optima)
        projected_distance = sum(min(x*x, (1-x)**2) for x in point[:k])+(point[-1]-a)**2
        require(distance == projected_distance and case.value(point) >= g*distance,
                case.name + ": growth toward the whole finite set")
        counts["growth_probes"] += 1

    bounds = height_bounds(case)
    *_, R, V = bounds
    theta = Q(1, 4)
    require(theta*theta <= g/(4*curvature), "admissible nonunique trial ratio")
    epsilon = min(Q(1, 4*V*V), curvature*theta*theta/(16*R**4))
    rho = Q(1, 4*R*R)
    step = min(rho/(4*n), epsilon/(8*n))
    recovered = []
    for optimum in optima:
        check_candidate_height(case, optimum, (k,), bounds, counts)
        nearby = tuple(x if i in integer else x+(-step if x == 1 else step)
                       for i, x in enumerate(optimum))
        require(case.feasible(nearby) and sum((x-s)**2 for x, s in zip(nearby, optimum)) < rho*rho,
                case.name + ": close feasible point near this optimizer")
        upper = case.value(nearby)
        lower = upper-epsilon
        require(lower <= 0 <= upper and upper-lower <= Q(1, 4*V*V),
                case.name + ": certified analytic optimum interval")
        value = reconstruct_interval(lower, upper, V)
        candidate = tuple(reconstruct_interval(x-rho, x+rho, R) for x in nearby)
        require(value == 0 and candidate == optimum and accept_candidate(case, candidate, value),
                case.name + ": recovery of the same nearby optimizer")
        recovered.append(candidate)
        counts["value_reconstructions"] += 1
        counts["coordinate_reconstructions"] += n
    require(set(recovered) == set(optima), case.name + ": every isolated optimum recovered")
    return {"name": case.name, "integer_coordinates": list(integer), "optima": len(optima),
            "A": projection_count, "g": str(g), "L": str(curvature), "R": str(R), "V": str(V),
            "recovered_optimizers": [[str(x) for x in point] for point in recovered]}


def check_denominator(value, denominator, counts, key):
    require(denominator % value.denominator == 0, key + ": common denominator divisibility")
    counts[key] += 1


def source_offsets(span, h, theta):
    offsets = [Q(0)]
    while offsets[-1] < span:
        offsets.append((1+theta)*offsets[-1]+h)
    require(offsets[-2] < span <= offsets[-1], "least source-step count reaching span")
    return tuple(offsets)


def check_anchor_closure(name, bounds, integer, J, r, counts):
    n, iterations = len(bounds), 128
    # Rational unary and pair factors, with a positive coordinate curvature.
    quadratic = tuple(Q(i+2, i+7) for i in range(n))
    linear = tuple(Q((-1)**i*(i+1), i+11) for i in range(n))
    constants = tuple(Q(1, i+13) for i in range(n))
    pair_weights = tuple(Q(-3, i+17) for i in range(n-1))
    data = [x for interval in bounds for x in interval]
    data += list(quadratic+linear+constants+pair_weights)
    D = lcm(*(x.denominator for x in data))
    span = max(hi-lo for lo, hi in bounds)
    theta, h = Q(1, 2**r), span/2**J
    curvature = max(2*x for x in quadratic)
    require(D % span.denominator == 0 and D % curvature.denominator == 0,
            name + ": common span and curvature denominator")
    offsets = source_offsets(span, h, theta)
    K = len(offsets)-1
    E = J+r*K
    coordinate_denominator = D*2**E
    W = 8*D**3*2**(2*E)
    for offset in offsets:
        check_denominator(offset, coordinate_denominator, counts, "offset_denominator_checks")

    anchors = [lo for lo, _ in bounds]
    retained = [{lo} for lo, _ in bounds]
    unions = [set() for _ in bounds]
    message = Q(0)
    maximum_coordinate_bits = 0
    maximum_value_bits = 0
    changed = 0
    offset_set = set(offsets)
    for iteration in range(iterations):
        grids, corrections = [], []
        for i, (lo, hi) in enumerate(bounds):
            anchor = anchors[i]
            grid, _ = coordinate_grid(lo, hi, anchor, h, theta, i in integer)
            counts["source_grids_built"] += 1
            if i not in integer:
                require(sum(x < anchor for x in grid) <= K and sum(x > anchor for x in grid) <= K,
                        name + ": uniform source-step bound")
            for x in grid:
                check_denominator(x, coordinate_denominator, counts, "grid_coordinate_checks")
                maximum_coordinate_bits = max(maximum_coordinate_bits, x.denominator.bit_length())
                if i in integer:
                    require(x.denominator == 1, name + ": integer source nodes")
                    counts["integer_coordinate_checks"] += 1
                else:
                    require(x in (lo, hi) or abs(x-anchor) in offset_set,
                            name + ": unclipped nodes are fixed source offsets")
            unions[i].update(grid)
            penalty = penalties(grid, i in integer, curvature)
            for value in penalty:
                check_denominator(value, W, counts, "correction_denominator_checks")
                maximum_value_bits = max(maximum_value_bits, value.denominator.bit_length())
            if iteration % 32 == 31:
                union_grid = tuple(sorted(unions[i]))
                for value in penalties(union_grid, i in integer, curvature):
                    check_denominator(value, W, counts, "union_correction_denominator_checks")
            grids.append(grid)
            corrections.append(penalty)

            # Retain all anchors, selecting the next one from this source grid.
            # Prefer unused nodes with large denominators to stress reanchoring.
            unused = [x for x in grid if x not in retained[i]]
            choices = unused or list(grid)
            largest = max(x.denominator for x in choices)
            choices = [x for x in choices if x.denominator == largest]
            selected = choices[(iteration+i) % len(choices)]
            changed += selected != anchor
            require(selected in grid, name + ": next anchor belongs to the current grid")
            retained[i].add(selected)
            anchors[i] = selected
            check_denominator(selected, coordinate_denominator, counts, "anchor_denominator_checks")

        # Small min-sum message samples, not a full decomposition DP. The
        # previous message is carried through all iterations to test depth.
        proposals = []
        for branch in range(2):
            indices = tuple((7*iteration+3*i+branch) % len(grid) for i, grid in enumerate(grids))
            point = tuple(grid[index] for grid, index in zip(grids, indices))
            factors = [quadratic[i]*point[i]**2+linear[i]*point[i]+constants[i] for i in range(n)]
            factors += [pair_weights[i]*point[i]*point[i+1] for i in range(n-1)]
            for value in factors:
                check_denominator(value, W, counts, "factor_denominator_checks")
                maximum_value_bits = max(maximum_value_bits, value.denominator.bit_length())
            terms = factors + [-corrections[i][indices[i]] for i in range(n)]
            candidate_message = message
            for term in terms:
                candidate_message += term
                check_denominator(candidate_message, W, counts, "message_denominator_checks")
            proposals.append(candidate_message)
        message = min(proposals)
        check_denominator(message, W, counts, "message_denominator_checks")
        counts["anchor_rounds"] += 1

    require(all(len(retained[i]) >= 100 for i in range(n) if i not in integer),
            name + ": at least 100 distinct continuous anchors per coordinate")
    require(iterations >= 100, name + ": repeated-anchor stress depth")
    return {"name": name, "iterations": iterations, "integer_coordinates": list(integer),
            "J": J, "r": r, "K": K, "E": E, "D": str(D),
            "coordinate_denominator_bits": coordinate_denominator.bit_length(),
            "value_denominator_bound_bits": W.bit_length(),
            "maximum_observed_coordinate_denominator_bits": maximum_coordinate_bits,
            "maximum_observed_factor_or_correction_denominator_bits": maximum_value_bits,
            "distinct_anchors_by_coordinate": [len(values) for values in retained],
            "union_nodes_by_coordinate": [len(values) for values in unions],
            "anchor_changes": changed,
            "denominator_bounds_independent_of_iteration": True}


def main():
    counts = dict.fromkeys(("growth_probes", "candidate_height_checks", "value_reconstructions",
                           "coordinate_reconstructions", "offset_denominator_checks",
                           "source_grids_built", "grid_coordinate_checks", "integer_coordinate_checks",
                           "correction_denominator_checks", "union_correction_denominator_checks",
                           "anchor_denominator_checks", "factor_denominator_checks",
                           "message_denominator_checks", "anchor_rounds"), 0)
    recovery = [check_nonunique_recovery(integer, counts) for integer in ((), (0, 2))]
    closure = [
        check_anchor_closure("rational_negative_clipping",
                             ((Q(-2, 7), Q(11, 9)), (Q(1, 5), Q(17, 10))), (), 4, 1, counts),
        check_anchor_closure("mixed_integer_clipping",
                             ((Q(-5, 6), Q(7, 4)), (Q(2, 9), Q(13, 7)), (Q(-2), Q(3))),
                             (2,), 7, 2, counts),
        check_anchor_closure("small_nondyadic_box",
                             ((Q(1, 11), Q(5, 13)), (Q(-7, 10), Q(-1, 3))), (), 5, 3, counts),
    ]
    print(json.dumps({
        "command": "python3 research-20261002/geometric-dp/checks/exact_nonunique_qp_checks.py",
        "arithmetic": "fractions.Fraction; no floating-point arithmetic",
        "scope": "Nonunique recovery and denominator closure; not a full anchor-DP or performance test.",
        "counts": counts, "nonunique_recovery": recovery, "anchor_closure": closure, "passed": True,
    }, indent=2))


if __name__ == "__main__":
    main()
