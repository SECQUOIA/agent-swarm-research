"""Targeted exact regression checks and bounded illustrative runs."""

import argparse
from dataclasses import replace
from fractions import Fraction as Q
from itertools import product
import json
from math import ceil, floor
from pathlib import Path
import random
import time

from mincut_recourse import Certificate, Quadratic, adaptive_core, detect_flips, exact_core, solve_recourse, verify_exact, verify_recourse, verify_search


def make_model(k, r, seed, density=Q(1, 2)):
    rng = random.Random(seed)
    signs = {i: rng.choice((-1, 1)) for i in range(k, k + r)}
    diagonal = tuple([Q(1)] * k + [Q(-rng.randrange(4), 8) for _ in range(r)])
    linear = tuple(Q(rng.randrange(-8, 9), 8) for _ in range(k + r))
    edges = []
    for i in range(k + r):
        for j in range(i + 1, k + r):
            if i < k and j < k:
                continue  # exact small-instance comparison uses diagonal core
            if rng.random() >= float(density):
                continue
            coefficient = Q(rng.randrange(1, 5), max(8, r))
            if i >= k:
                coefficient *= -signs[i] * signs[j]
            else:
                coefficient *= rng.choice((-1, 1))
            edges.append((i, j, coefficient))
    return Quadratic(diagonal, linear, tuple(edges)), signs


def exhaustive_recourse(model, core_values, bounds, integers):
    residual = [i for i in range(len(bounds)) if i not in core_values]
    endpoints = []
    for i in residual:
        lo, hi = bounds[i]
        endpoints.append((Q(ceil(lo)), Q(floor(hi))) if i in integers else (lo, hi))
    values = []
    for choices in product(*endpoints):
        point = [Q(0)] * len(bounds)
        for i, value in core_values.items():
            point[i] = value
        for i, value in zip(residual, choices):
            point[i] = value
        values.append(model.value(point))
    return min(values)


def exhaustive_small_global(model, k, bounds):
    """Exact endpoint enumeration plus independent convex core quadratics."""
    best, points = None, []
    for bits in product((0, 1), repeat=len(bounds) - k):
        point = [Q(0)] * k + [bounds[i][b] for i, b in zip(range(k, len(bounds)), bits)]
        for i in range(k):
            slope = model.linear[i]
            for left, right, coefficient in model.edges:
                if left == i:
                    assert right >= k
                    slope += coefficient * point[right]
            point[i] = min(Q(1), max(Q(0), -slope / (2 * model.diagonal[i])))
        value = model.value(point)
        if best is None or value < best:
            best, points = value, [tuple(point)]
        elif value == best:
            points.append(tuple(point))
    return best, points


def switched_dense_model(r):
    """Two tied interior core optimizers and a dense, nonconvex cut residual.

    V(x) = (x-3/4)^2 + min(0,x-1/2), since each nonuniform binary
    residual has at least one cut edge of cost one. Its minima are zero
    at x=1/4 (all residuals one) and x=3/4 (all residuals zero).
    """
    diagonal = (Q(1),) + (Q(0),) * r
    linear = (Q(-3, 2),) + (Q(r - 1) - Q(1, 2 * r),) * r
    edges = [(0, i, Q(1, r)) for i in range(1, r + 1)]
    edges.extend((i, j, Q(-2)) for i in range(1, r + 1) for j in range(i + 1, r + 1))
    return Quadratic(diagonal, linear, tuple(edges), Q(9, 16)), {i: 1 for i in range(1, r + 1)}


def run_checks():
    rng = random.Random(77293)
    oracle_cases, signed_cases, restricted_cases = 0, 0, 0
    for case in range(100):
        k, r = case % 3, 1 + case % 7
        model, flips = make_model(k, r, case, density=Q(3, 4))
        bounds = [(Q(0), Q(1))] * k
        integers = set()
        for i in range(k, k + r):
            if (case + i) % 3 == 0:
                bounds.append((Q(-7, 3), Q(11, 3)))
                integers.add(i)
            else:
                lo = Q(rng.randrange(-8, 9), 8)
                bounds.append((lo, lo + Q(rng.randrange(0, 9), 8)))
        core_values = {i: Q(rng.randrange(9), 8) for i in range(k)}
        cert = solve_recourse(model, core_values, bounds, flips, integers)
        detected = detect_flips(model, core_values)
        detected_cert = solve_recourse(model, core_values, bounds, detected, integers)
        assert detected_cert.value == cert.value
        assert cert.value == exhaustive_recourse(model, core_values, bounds, integers)
        assert verify_recourse(model, core_values, bounds, flips, cert, integers)
        assert not verify_recourse(model, core_values, bounds, flips,
                                  replace(cert, value=cert.value + 1), integers)
        if cert.flow:
            changed = dict(cert.flow)
            edge = next(iter(changed))
            changed[edge] += 1
            assert not verify_recourse(model, core_values, bounds, flips,
                                       replace(cert, flow=changed), integers)
        oracle_cases += 1
        signed_cases += any(sign < 0 for sign in flips.values())
        restricted_cases += any(b != (0, 1) for b in bounds[k:])
    # Every rejection protects a mathematical premise rather than a code shape.
    rejected = 0
    bad_cases = [
        (Quadratic((Q(1),), (Q(0),), ()), {}, [(0, 1)], {0: 1}, ()),
        (Quadratic((Q(0), Q(0)), (Q(0), Q(0)), ((0, 1, Q(1)),)),
         {}, [(0, 1)] * 2, {0: 1, 1: 1}, ()),
        (Quadratic((Q(0),), (Q(0),), ()), {}, [(Q(1, 3), Q(2, 3))], {0: 1}, (0,)),
    ]
    for args in bad_cases:
        try:
            solve_recourse(*args)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError("invalid recourse premise accepted")
    positive_triangle = Quadratic((Q(0),) * 3, (Q(0),) * 3,
                                 ((0, 1, Q(1)), (0, 2, Q(1)), (1, 2, Q(1))))
    try:
        detect_flips(positive_triangle, ())
    except ValueError:
        pass
    else:
        raise AssertionError("contradictory cycle accepted")
    assert len(detect_flips(positive_triangle, (0,))) == 2
    integer_iterator_model = Quadratic((Q(0),), (Q(-1),), ())
    integer_iterator_bounds = [(Q(1, 3), Q(5, 3))]
    iterator_cert = solve_recourse(integer_iterator_model, {}, integer_iterator_bounds,
                                  {0: 1}, iter([0]))
    assert iterator_cert.point == (Q(1),) and iterator_cert.value == -1
    assert verify_recourse(integer_iterator_model, {}, integer_iterator_bounds,
                           {0: 1}, iterator_cert, iter([0]))
    iterator_result = adaptive_core(integer_iterator_model, (), integer_iterator_bounds,
                                    {0: 1}, Q(1, 100), integer_indices=iter([0]))
    assert iterator_result["lower"] == iterator_result["upper"] == -1
    assert verify_search(integer_iterator_model, (), integer_iterator_bounds, {0: 1},
                         Q(1, 100), iterator_result, integer_indices=iter([0]))
    huge = 2**54
    flow_roundoff_model = Quadratic((Q(0), Q(0)), (Q(-1), Q(2 * huge - 1)),
                                   ((0, 1, Q(-2 * (huge - 1))),))
    fake_float_flow = Certificate((Q(0), Q(0)), Q(0),
                                 {(2, 0): float(huge), (0, 2): -float(huge),
                                  (0, 1): Q(huge - 1), (1, 0): Q(1 - huge),
                                  (1, 3): float(huge), (3, 1): -float(huge)}, frozenset({2}))
    assert not verify_recourse(flow_roundoff_model, {}, [(0, 1)] * 2,
                               {0: 1, 1: 1}, fake_float_flow)
    try:
        solve_recourse(flow_roundoff_model, {}, [(0, 1)] * 2, {0: 1.0, 1: 1.0})
    except ValueError:
        pass
    else:
        raise AssertionError("inexact endpoint flips accepted")
    # Ties, empty residual, and zero curvature need no genericity promise.
    zero = Quadratic((Q(0),) * 3, (Q(0),) * 3, ())
    tied = adaptive_core(zero, (0,), [(0, 1)] * 3, {1: 1, 2: -1}, Q(1, 100))
    assert tied["complete"] and tied["lower"] == tied["upper"] == 0
    no_residual = Quadratic((Q(1),), (Q(-2, 3),), ())
    result = adaptive_core(no_residual, (0,), [(0, 1)], {}, Q(1, 1000))
    assert result["lower"] <= Q(-1, 9) <= result["upper"]
    all_residual, flips = make_model(0, 5, 193)
    result = adaptive_core(all_residual, (), [(0, 1)] * 5, flips, Q(1, 1000))
    assert result["complete"] and result["lower"] == result["upper"]
    search_cases, level_checks, verified = 0, 0, 0
    for case in range(20):
        k, r = 1 + case % 2, 3 + case % 4
        model, flips = make_model(k, r, case + 1000)
        bounds = [(Q(0), Q(1))] * (k + r)
        optimum, optimizers = exhaustive_small_global(model, k, bounds)
        result = adaptive_core(model, range(k), bounds, flips, Q(1, 1024), max_levels=12)
        assert result["complete"] and result["upper"] - result["lower"] <= Q(1, 1024)
        assert verify_search(model, range(k), bounds, flips, Q(1, 1024), result)
        altered = dict(result, lower=result["lower"] + 1)
        assert not verify_search(model, range(k), bounds, flips, Q(1, 1024), altered)
        for row in result["trace"]:
            assert row["lower"] <= optimum <= row["upper"]
            denominator = 2 ** row["level"]
            for point in optimizers:
                assert any(all(Q(cell[i], denominator) <= point[i] <= Q(cell[i] + 1, denominator)
                               for i in range(k)) for cell in row["retained_cells"])
            level_checks += 1
        for corner, cert in result["certificates"].items():
            assert verify_recourse(model, dict(zip(range(k), corner)), bounds, flips, cert)
            verified += 1
        search_cases += 1
    bounded = adaptive_core(no_residual, (0,), [(0, 1)], {}, Q(1, 10**12), max_levels=0)
    assert not bounded["complete"] and bounded["lower"] <= Q(-1, 9) <= bounded["upper"]
    assert verify_search(no_residual, (0,), [(0, 1)], {}, Q(1, 10**12), bounded)
    switched, flips = switched_dense_model(6)
    switched_bounds = [(0, 1)] * 7
    switched_result = adaptive_core(switched, (0,), switched_bounds, flips, Q(1, 4096))
    assert switched_result["complete"] and switched_result["lower"] <= 0 <= switched_result["upper"]
    assert verify_search(switched, (0,), switched_bounds, flips, Q(1, 4096), switched_result)
    for row in switched_result["trace"]:
        denominator = 2 ** row["level"]
        for optimum_core in (Q(1, 4), Q(3, 4)):
            assert any(Q(cell[0], denominator) <= optimum_core <= Q(cell[0] + 1, denominator)
                       for cell in row["retained_cells"])
    exact_fixtures = [
        (Quadratic((Q(3),), (Q(-2),), ()), (0,), [(0, 1)], {}, Q(-1, 3)),
        (Quadratic((Q(3), Q(-1)), (Q(-2), Q(1)), ((0, 1, Q(-1)),)),
         (0,), [(0, 1)] * 2, {1: 1}, Q(-3, 4)),
        (Quadratic((Q(0), Q(0)), (Q(-1), Q(0)), ((0, 1, Q(1)),)),
         (0, 1), [(0, 1)] * 2, {}, Q(-1)),
        (Quadratic((Q(1), Q(1)), (Q(-1), Q(-1)), ((0, 1, Q(-2)),)),
         (0, 1), [(0, 1)] * 2, {}, Q(-2)),
    ]
    exact_levels = []
    for model, core, bounds, flips, expected in exact_fixtures:
        exact_result = exact_core(model, core, bounds, flips, max_levels=32)
        assert exact_result["complete"] and exact_result["value"] == expected
        assert verify_exact(model, core, bounds, flips, exact_result)
        assert not verify_exact(model, core, bounds, flips,
                                dict(exact_result, value=exact_result["value"] + 1))
        exact_levels.append(len(exact_result["search"]["trace"]))
    limited_exact = exact_core(exact_fixtures[0][0], (0,), [(0, 1)], {}, max_levels=0)
    assert not limited_exact["complete"] and not verify_exact(exact_fixtures[0][0],
                                                            (0,), [(0, 1)], {}, limited_exact)
    return {"exact_oracle_cases": oracle_cases, "signed_cases": signed_cases,
            "automatic_recognition_cases": oracle_cases, "contradictory_cycle_rejected": True,
            "one_pass_integer_domain_regression": "oracle and full search passed",
            "floating_point_flow_attack_rejected": True,
            "floating_point_signs_rejected": True,
            "exact_output_cases": len(exact_fixtures), "exact_output_levels": exact_levels,
            "restricted_box_cases": restricted_cases, "invalid_premises_rejected": rejected,
            "exact_global_comparisons": search_cases, "optimizer_preserving_levels": level_checks,
            "independently_verified_search_certificates": verified,
            "complete_traces_verified": search_cases, "tampered_traces_rejected": search_cases,
            "special_cases": ["ties", "no residual", "no core", "zero curvature", "bounded unfinished run",
                              "dense switching residual with two interior core optimizers"]}


def run_examples():
    records = []
    for k, r, density in [(1, 8, Q(1, 2)), (1, 32, Q(1, 8)),
                           (1, 64, Q(1, 16)), (2, 16, Q(1, 4)),
                           (2, 32, Q(1, 8)), (1, 32, Q(1))]:
        model, flips = make_model(k, r, 800 + r + k, density=density)
        bounds = [(Q(0), Q(1))] * (k + r)
        start = time.perf_counter()
        result = adaptive_core(model, range(k), bounds, flips, Q(1, 1024), max_levels=12)
        elapsed = time.perf_counter() - start
        start = time.perf_counter()
        assert verify_search(model, range(k), bounds, flips, Q(1, 1024), result)
        verify_elapsed = time.perf_counter() - start
        assert result["complete"]
        records.append({"core": k, "residual": r, "edges": len(model.edges),
                        "complete": result["complete"], "levels": len(result["trace"]),
                        "queries": len(result["certificates"]),
                        "max_retained": max(row["retained"] for row in result["trace"]),
                        "generated_total": sum(row["generated"] for row in result["trace"]),
                        "lower": str(result["lower"]), "upper": str(result["upper"]),
                        "gap": str(result["upper"] - result["lower"]),
                        "search_seconds": round(elapsed, 6), "verify_seconds": round(verify_elapsed, 6)})
    for r in (8, 32):
        model, flips = switched_dense_model(r)
        bounds = [(Q(0), Q(1))] * (r + 1)
        start = time.perf_counter()
        result = adaptive_core(model, (0,), bounds, flips, Q(1, 1024), max_levels=12)
        elapsed = time.perf_counter() - start
        start = time.perf_counter()
        assert verify_search(model, (0,), bounds, flips, Q(1, 1024), result)
        verify_elapsed = time.perf_counter() - start
        assert result["complete"] and result["upper"] == 0
        records.append({"family": "dense_two_modes", "core": 1, "residual": r,
                        "edges": len(model.edges), "complete": result["complete"],
                        "levels": len(result["trace"]), "queries": len(result["certificates"]),
                        "max_retained": max(row["retained"] for row in result["trace"]),
                        "generated_total": sum(row["generated"] for row in result["trace"]),
                        "lower": str(result["lower"]), "upper": str(result["upper"]),
                        "gap": str(result["upper"] - result["lower"]),
                        "search_seconds": round(elapsed, 6), "verify_seconds": round(verify_elapsed, 6)})
    return records


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--examples", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = {"checks": run_checks()}
    if args.examples:
        report["examples"] = run_examples()
    text = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")
