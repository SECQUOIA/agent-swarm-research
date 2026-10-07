#!/usr/bin/env python3
"""Targeted exact checks; optionally exercise automatic floating LP proposals."""

import argparse
import json
from fractions import Fraction as Q
from time import perf_counter

from certificates import (
    Box,
    Model,
    ProtectedBox,
    Row,
    check_tail_majorant,
    cutoff_frontier,
    current_round_ceilings,
    discover_protected_box,
    mix_for_cutoff,
    scipy_proposal,
    verify_protected_box,
)


def rejected(function, *args):
    try:
        function(*args)
    except (ValueError, TypeError):
        return
    raise AssertionError("Invalid proposed certificate was accepted")


def squares(n, coupled=False):
    row = tuple([1] * n + [0] * n)
    rows = (Row(row, 0), Row(tuple(-v for v in row), 0)) if coupled else ()
    return Model(n, tuple((i, i) for i in range(n)), rows, tuple([0] * n + [1] * n))


def stall_witnesses(radius=Q(1), n=2, coupled=False):
    points = []
    for i in range(n):
        for sign in (-1, 1):
            x = [Q(0)] * n
            x[i] = sign * radius
            if coupled:
                x[(i + 1) % n] = -sign * radius
            w = [radius**2 if value else -radius**2 for value in x]
            points.append(tuple(x + w))
    points.append(tuple([Q(0)] * n + [-radius**2] * n))
    return tuple(points)


def quadratic_stall():
    """Strongly convex objective; stall persists with exact convex squares."""
    products = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))
    rows = []
    for i in range(3):
        coefficients = [0] * 9
        coefficients[3 + i] = -1
        rows.append(Row(tuple(coefficients), 0))
    return Model(3, products, tuple(rows), (0, 0, 0, 1, 1, 1, 1, 1, 1))


def exact_checks():
    checks = []

    # Mixed signs and repeated product indices use the same four valid rows.
    model = Model(2, ((0, 1), (0, 0)), (), (0, 0, 0, 0))
    box = Box((-2, -1), (3, 2))
    for x in (Q(-2), Q(-1, 3), Q(0), Q(3)):
        for y in (Q(-1), Q(0), Q(1, 7), Q(2)):
            assert model.feasible(box, (x, y, x * y, x * x), 0)
    checks.append("bilinear_and_square_rows_at_exact_graph_points")

    # Feasibility on the old box does not certify retention after rebuilding.
    square = squares(1)
    outer = Box((0,), (1,))
    candidates = ((Q(0), Q(0)), (Q(1, 2), Q(0)))
    assert current_round_ceilings(square, outer, 0, candidates) == ((Q(0),), (Q(1, 2),))
    rejected(verify_protected_box, square, outer, Box((0,), (Q(1, 2),)), 0, candidates)
    rejected(ProtectedBox, square, Box((0,), (Q(1, 2),)), candidates)
    assert all(Q(1, 2**k) > 0 for k in range(1, 20))
    checks.append("old_relaxation_witness_rejected_after_rebuilding")

    # An LP fixed box can remain wide despite a unique original optimum at 0.
    model = squares(2)
    protected = Box((-1, -1), (1, 1))
    outer = Box((-2, -4), (3, 2))
    cert = verify_protected_box(model, outer, protected, 0, stall_witnesses())
    assert cert.ceilings(model, outer, 0) == ((Q(1), Q(3)), (Q(2), Q(1)))
    assert cert.objective_ceiling == -2 and cert.required_cutoff == 0
    for enclosing in (outer, Box((-1, -2), (2, 1)), protected):
        assert all(model.feasible(enclosing, w, 0) for w in cert.witnesses)
    checks.append("protected_box_coordinate_and_objective_ceilings")

    # Constant rows, including exact equalities, are part of the identity.
    model4 = squares(4, coupled=True)
    box4 = Box((-1,) * 4, (1,) * 4)
    cert4 = verify_protected_box(model4, box4, box4, 0, stall_witnesses(n=4, coupled=True))
    assert cert4.objective_ceiling == -4
    changed = Model(4, model4.products, model4.rows + (Row((1, 0, 0, 0, 0, 0, 0, 0), 0),), model4.objective)
    assert not cert4.reusable(changed, box4, 0)
    checks.append("coupled_rows_and_model_identity")

    linear = Model(1, (), (), (1,))
    unit = Box((0,), (1,))
    cert = verify_protected_box(linear, unit, unit, 1, ((0,), (1,)))
    assert cert.reusable(linear, Box((-1,), (2,)), 2)
    assert not cert.reusable(linear, unit, Q(1, 2))
    assert not cert.reusable(linear, Box((0,), (Q(3, 4),)), 1)
    rejected(cert.ceilings, linear, unit, Q(1, 2))
    checks.append("tightened_cutoff_and_child_domain_invalidate_cache")

    # The same retained witnesses can survive a genuine cutoff reduction.
    half = Box((0,), (Q(1, 2),))
    half_cert = verify_protected_box(linear, unit, half, 1, ((0,), (Q(1, 2),)))
    assert half_cert.reusable(linear, unit, Q(1, 2))
    assert half_cert.ceilings(linear, Box((0,), (Q(3, 4),)), Q(1, 2)) == ((Q(0),), (Q(1, 4),))
    checks.append("cutoff_and_domain_reuse_with_verified_threshold")

    # Convex mixing adapts current witnesses but does not establish a new P.
    symmetric = Box((-1,), (1,))
    mixed = tuple(mix_for_cutoff(square, symmetric, (s, 1), (0, 0), Q(1, 4)) for s in (-1, 1))
    assert mixed == ((Q(-1, 4), Q(1, 4)), (Q(1, 4), Q(1, 4)))
    assert current_round_ceilings(square, symmetric, Q(1, 4), mixed) == ((Q(3, 4),), (Q(3, 4),))
    rejected(verify_protected_box, square, symmetric, Box((Q(-1, 4),), (Q(1, 4),)), Q(1, 4), mixed)
    rejected(mix_for_cutoff, square, symmetric, (1, 1), (0, 0), -1)
    checks.append("cutoff_mixing_valid_only_in_frozen_domain")

    # The best pooled witness may mix the expensive point with a non-incumbent.
    linear2 = Model(2, (), (), (0, 1))
    pool_box = Box((0, 0), (2, 3))
    pool = ((0, 0), (2, 3), (1, 1))
    frontier = cutoff_frontier(linear2, pool_box, pool, 2)
    assert (Q(4, 3), Q(2)) in frontier and (Q(3, 2), Q(2)) in frontier
    assert current_round_ceilings(linear2, pool_box, 2, frontier)[1][0] == Q(1, 2)
    assert cutoff_frontier(linear2, pool_box, pool, -1) == ()
    checks.append("exact_pairwise_cutoff_frontier_of_cached_pool")

    zero = Box((0,), (0,))
    assert verify_protected_box(square, outer=unit, candidate=zero, cutoff=0, witnesses=((0, 0),)).box == zero
    rejected(Row, (0.1,), 0)
    checks.append("degenerate_boxes_and_exact_input_contract")

    # Matrix majorants are checked exactly; the uniform M remains a hypothesis.
    matrix = ((Q(1, 2), Q(1, 4)), (Q(0), Q(1, 3)))
    residual = (Q(1, 4), Q(1, 3))
    majorant = (Q(3, 4), Q(1, 2))
    assert check_tail_majorant(matrix, residual, majorant)
    assert not check_tail_majorant(matrix, residual, (Q(1, 2), Q(1, 2)))
    term, total = residual, (Q(0), Q(0))
    for _ in range(20):
        total = tuple(a + b for a, b in zip(total, term))
        assert all(t <= e for t, e in zip(total, majorant))
        term = tuple(sum((a * b for a, b in zip(row, term)), Q(0)) for row in matrix)
    assert check_tail_majorant(((1, 0), (0, Q(1, 2))), (0, Q(1, 2)), (0, 1))
    checks.append("matrix_tail_and_noncontracting_inactive_direction")

    # Rebuilt square LP: max x = (u^2+r^2)/(2u) for u>=r>0.
    radius, upper = Q(1), Q(2)
    cutoff = radius**2
    new_upper = (upper**2 + cutoff) / (2 * upper)
    assert square.feasible(Box((0,), (upper,)), (new_upper, cutoff), cutoff)
    residual = upper - new_upper
    q = (1 - radius**2 / upper**2) / 2
    e = residual / (1 - q)
    assert e == Q(6, 5) and upper - radius <= e
    assert check_tail_majorant(((q,),), (residual,), (e,))
    for u in (Q(1), Q(5, 4), Q(3, 2), Q(2)):
        derivative = (1 - cutoff / u**2) / 2
        assert 0 <= derivative <= q
    checks.append("finite_uniform_bound_for_rebuilt_square_lp")

    # A fitted residual ratio can underestimate the entire remaining change.
    def changing_slope(s):
        return 3 * s / 4 if s <= Q(1, 2) else s / 4 + Q(1, 4)

    p0 = Q(1)
    p1, p2 = changing_slope(p0), changing_slope(changing_slope(p0))
    observed_q = (p1 - p2) / (p0 - p1)
    assert observed_q == Q(1, 4)
    assert (p1 - p2) / (1 - observed_q) == Q(1, 6) < p1
    checks.append("empirical_residual_ratio_is_not_a_certificate")
    return checks


def automatic_checks():
    fixtures = []
    fixtures.append(("quadratic_stall_with_nonnegative_squares", quadratic_stall(), Box((-1,) * 3, (1,) * 3), Q(0), True))
    for radius in (Q(1), Q(1, 2)):
        fixtures.append((f"square_stall_radius_{radius}", squares(2), Box((-radius,) * 2, (radius,) * 2), Q(0), True))
    fixtures.append(("coupled_square_stall", squares(4, True), Box((-1,) * 4, (1,) * 4), Q(0), True))
    fixtures.append(("linear_cutoff", Model(1, (), (), (1,)), Box((0,), (1,)), Q(3, 4), True))
    linear_rows = (Row((-1, -1), -1), Row((1, -1), 0), Row((-1, 1), 0))
    fixtures.append(("linear_coupled", Model(2, (), linear_rows, (0, 0)), Box((0, 0), (2, 2)), Q(0), True))
    fixtures.append(("contracting_zero_cutoff", squares(1), Box((0,), (1,)), Q(0), False))
    fixtures.append(("contracting_positive_cutoff", squares(1), Box((0,), (2,)), Q(1), False))
    outcomes = []
    for name, model, box, cutoff, expected in fixtures:
        calls = 0

        def counted(*args):
            nonlocal calls
            calls += 1
            return scipy_proposal(*args)

        started = perf_counter()
        cert = discover_protected_box(model, box, cutoff, counted, improve_objective=True)
        elapsed = perf_counter() - started
        assert (cert is not None) == expected, name
        if cert is not None:
            # Independent replay through the exact public verifier.
            replay = verify_protected_box(model, box, cert.box, cutoff, cert.witnesses)
            assert replay == cert
            if name == "quadratic_stall_with_nonnegative_squares":
                assert cert.objective_ceiling == -3
        outcomes.append({
            "fixture": name,
            "certified": cert is not None,
            "proposal_lp_calls_including_objective": calls,
            "seconds_including_exact_checks": elapsed,
            "protected_lower": [str(v) for v in cert.box.lower] if cert else None,
            "protected_upper": [str(v) for v in cert.box.upper] if cert else None,
            "objective_ceiling": str(cert.objective_ceiling) if cert else None,
        })
    return outcomes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--with-lp-proposals", action="store_true")
    args = parser.parse_args()
    report = {"exact_checks": exact_checks()}
    if args.with_lp_proposals:
        report["automatic_discovery"] = automatic_checks()
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
