#!/usr/bin/env python3
"""Exact rational checks for surrogate-cell screening and dense QP recovery.

Run from the repository root:
    python code/bilevel_reopened/approximate_structure_checks.py

SymPy provides rational linear algebra. Scalar leader LPs are solved by exact
interval intersection, independently of a numerical LP/QP solver. The small
reference method enumerates every true active set; the screened method uses
only the statuses certified from the surrogate ellipsoid. This is an exact
proof-of-concept, not a production implementation of general cell enumeration.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
import time
from dataclasses import dataclass
from pathlib import Path

import sympy as sp


R = sp.Rational


@dataclass
class Cell:
    lo: sp.Rational
    hi: sp.Rational
    intercept: sp.Matrix
    slope: sp.Matrix


def affine_value(intercept, slope, x):
    return intercept + slope * x


def extremes(intercept, slope, lo, hi):
    values = (intercept + slope * lo, intercept + slope * hi)
    return min(values), max(values)


def intersect_leq(lo, hi, intercept, slope):
    """Intersect [lo,hi] with intercept+slope*x <= 0 exactly."""
    if slope > 0:
        hi = min(hi, -intercept / slope)
    elif slope < 0:
        lo = max(lo, -intercept / slope)
    elif intercept > 0:
        return None
    return None if lo > hi else (lo, hi)


def greater_than_half_root(value, square):
    return value > 0 and 4 * value**2 > square


def at_least_half_root(value, square):
    return value >= 0 and 4 * value**2 >= square


def diagonal_cells(diagonal, c, C, lo=R(0), hi=R(1)):
    cuts = {lo, hi}
    for i in range(len(c)):
        if C[i] != 0:
            for target in (R(0), R(1)):
                point = (-diagonal[i] * target - c[i]) / C[i]
                if lo <= point <= hi:
                    cuts.add(point)
    cuts = sorted(cuts)
    intervals = list(zip(cuts[:-1], cuts[1:])) if lo < hi else [(lo, hi)]
    cells = []
    for left, right in intervals:
        middle = (left + right) / 2
        p, q = sp.zeros(len(c), 1), sp.zeros(len(c), 1)
        for i in range(len(c)):
            value = -(c[i] + C[i] * middle) / diagonal[i]
            if value <= 0:
                p[i] = 0
            elif value >= 1:
                p[i] = 1
            else:
                p[i], q[i] = -c[i] / diagonal[i], -C[i] / diagonal[i]
        cells.append(Cell(left, right, p, q))
    return cells


def screen(Q, Qhat, Qinv, c, C, cell):
    E = Q - Qhat
    p0, p1 = E * cell.intercept, E * cell.slope
    eta = max(
        (p.T * Qinv * p)[0]
        for p in (p0 + p1 * cell.lo, p0 + p1 * cell.hi)
    )
    s0 = cell.intercept - Qinv * p0 / 2
    s1 = cell.slope - Qinv * p1 / 2
    t0 = Qhat * cell.intercept + c + p0 / 2
    t1 = Qhat * cell.slope + C + p1 / 2
    status = []
    for i in range(Q.rows):
        smin, smax = extremes(s0[i], s1[i], cell.lo, cell.hi)
        tmin, tmax = extremes(t0[i], t1[i], cell.lo, cell.hi)
        rsq, ssq = Qinv[i, i] * eta, Q[i, i] * eta
        lower = (at_least_half_root(tmin, ssq) and greater_than_half_root(tmax, ssq)) or at_least_half_root(-smax, rsq)
        upper = (at_least_half_root(-tmax, ssq) and greater_than_half_root(-tmin, ssq)) or at_least_half_root(smin - 1, rsq)
        free = (at_least_half_root(smin, rsq) and at_least_half_root(1 - smax, rsq)
                and greater_than_half_root(smax, rsq) and greater_than_half_root(1 - smin, rsq))
        assert sum((bool(lower), bool(upper), bool(free))) <= 1
        status.append("L" if lower else "U" if upper else "F" if free else "?")
    return status, eta


def candidate_response(Q, c, C, status):
    n = Q.rows
    free = [i for i, s in enumerate(status) if s == "F"]
    upper = [i for i, s in enumerate(status) if s == "U"]
    p, q = sp.zeros(n, 1), sp.zeros(n, 1)
    for i in upper:
        p[i] = 1
    if free:
        inverse = Q.extract(free, free).inv()
        offset = c.extract(free, [0])
        if upper:
            offset += Q.extract(free, upper) * sp.ones(len(upper), 1)
        fp = -inverse * offset
        fq = -inverse * C.extract(free, [0])
        for j, i in enumerate(free):
            p[i], q[i] = fp[j], fq[j]
    g0, g1 = Q * p + c, Q * q + C
    constraints = []
    for i, value in enumerate(status):
        if value == "L":
            constraints.append((-g0[i], -g1[i]))
        elif value == "U":
            constraints.append((g0[i], g1[i]))
        else:
            assert g0[i] == 0 and g1[i] == 0
            constraints.extend([(-p[i], -q[i]), (p[i] - 1, q[i])])
    return p, q, constraints


def solve_status(Q, c, C, status, lo, hi, objective, upper_rows, cache):
    key = tuple(status)
    if key not in cache:
        cache[key] = candidate_response(Q, c, C, key)
    p, q, constraints = cache[key]
    for intercept, slope in constraints:
        interval = intersect_leq(lo, hi, intercept, slope)
        if interval is None:
            return None
        lo, hi = interval
    for leader_coeff, response_row, rhs in upper_rows:
        intercept = (response_row.T * p)[0] - rhs
        slope = leader_coeff + (response_row.T * q)[0]
        interval = intersect_leq(lo, hi, intercept, slope)
        if interval is None:
            return None
        lo, hi = interval
    leader_coeff, response_row = objective
    intercept = (response_row.T * p)[0]
    slope = leader_coeff + (response_row.T * q)[0]
    x = lo if slope >= 0 else hi
    return (intercept + slope * x, x, p + q * x, (lo, hi))


def optimize_screened(Q, Qhat, c, C, cells, objective, upper_rows):
    Qinv, cache, best = Q.inv(), {}, None
    ambiguous_counts, completed, feasible = [], 0, 0
    for cell in cells:
        status, eta = screen(Q, Qhat, Qinv, c, C, cell)
        ambiguous = [i for i, value in enumerate(status) if value == "?"]
        ambiguous_counts.append(len(ambiguous))
        for values in itertools.product("LFU", repeat=len(ambiguous)):
            completed += 1
            assignment = list(status)
            for i, value in zip(ambiguous, values):
                assignment[i] = value
            answer = solve_status(Q, c, C, assignment, cell.lo, cell.hi, objective, upper_rows, cache)
            if answer is not None:
                feasible += 1
                if best is None or answer[0] < best[0]:
                    best = answer
    return best, {
        "cells": len(cells),
        "max_ambiguous": max(ambiguous_counts, default=0),
        "ambiguous_histogram": {str(t): ambiguous_counts.count(t) for t in sorted(set(ambiguous_counts))},
        "completed_statuses": completed,
        "distinct_statuses": len(cache),
        "feasible_cell_status_pairs": feasible,
    }


def optimize_exhaustive(Q, c, C, objective, upper_rows, lo=R(0), hi=R(1)):
    best, cache = None, {}
    for status in itertools.product("LFU", repeat=Q.rows):
        answer = solve_status(Q, c, C, status, lo, hi, objective, upper_rows, cache)
        if answer is not None and (best is None or answer[0] < best[0]):
            best = answer
    return best


def check_kkt(Q, c, C, x, z):
    g = Q * z + c + C * x
    for zi, gi in zip(z, g):
        assert 0 <= zi <= 1
        assert (zi == 0 and gi >= 0) or (zi == 1 and gi <= 0) or (0 < zi < 1 and gi == 0)


def dense_family(n, seed=101, scale=10000):
    rng = random.Random(seed)
    A = sp.Matrix(n, n, lambda i, j: rng.randint(-3, 3))
    E = (A + A.T) / (scale * n)
    Qhat = sp.eye(n)
    Q = Qhat + E
    assert all(Q[i, i] > sum(abs(Q[i, j]) for j in range(n) if i != j) for i in range(n))
    c = sp.Matrix([R(-1, 2) + R(13, 4) * R(i, max(n - 1, 1)) for i in range(n)])
    C = sp.Matrix([-3] * n)
    b = sp.Matrix([R((-1) ** i * (i % 3 + 1)) for i in range(n)])
    objective = (R(1, 7), b)
    # A signed response constraint; its feasibility is checked on the true response.
    upper_rows = [(R(-1, 3), sp.Matrix([R(1) if i % 2 == 0 else R(-1, 2) for i in range(n)]), R(n, 5))]
    return Q, Qhat, c, C, objective, upper_rows


def neighborhood_certificate(Q, Qhat, c, C, cells):
    """Corollary's rational radius; scalar intervals already are simplices."""
    n = Q.rows
    infinity_norm = lambda A: max(sum(abs(A[i, j]) for j in range(A.cols)) for i in range(A.rows))
    m, L = 1 / infinity_norm(Qhat.inv()), infinity_norm(Qhat)
    Rdim = math.isqrt(n) + int(math.isqrt(n) ** 2 != n)
    q, margins, unions = 0, [], []
    for cell in cells:
        union = set()
        for x in {cell.lo, cell.hi}:
            y = cell.intercept + cell.slope * x
            g = Qhat * y + c + C * x
            transition = {i for i in range(n) if y[i] in (0, 1) and g[i] == 0}
            q = max(q, len(transition))
            union.update(transition)
        unions.append(union)
        middle = (cell.lo + cell.hi) / 2
        ym = cell.intercept + cell.slope * middle
        for i in range(n):
            if i in union:
                continue
            for x in {cell.lo, cell.hi}:
                y = cell.intercept + cell.slope * x
                g = Qhat * y + c + C * x
                if ym[i] == 0:
                    margins.append(g[i])
                elif ym[i] == 1:
                    margins.append(-g[i])
                else:
                    margins.extend([y[i], 1 - y[i]])
    sigma = min(margins) if margins else R(1)
    assert sigma > 0
    radius = min(m / 2, sigma / (4 * Rdim * max(1 / m, 1 + L / m)))
    eps = infinity_norm(Q - Qhat)
    max_unclassified = None
    if eps <= radius:
        delta = 2 * eps * Rdim / m
        gamma = 2 * eps * Rdim * (1 + L / m)
        assert delta <= sigma / 2 and gamma <= sigma / 2
        max_unclassified = 0
        for cell, union in zip(cells, unions):
            g0, g1 = Qhat * cell.intercept + c, Qhat * cell.slope + C
            unknown = []
            for i in range(n):
                ymin, ymax = extremes(cell.intercept[i], cell.slope[i], cell.lo, cell.hi)
                gmin, gmax = extremes(g0[i], g1[i], cell.lo, cell.hi)
                certified = gmin > gamma or gmax < -gamma or (ymin > delta and ymax < 1 - delta)
                if not certified:
                    unknown.append(i)
            assert set(unknown) <= union
            assert len(unknown) <= 2 * q
            max_unclassified = max(max_unclassified, len(unknown))
    return {"max_vertex_transition_count_q": q, "sigma": str(sigma),
            "guaranteed_radius": str(radius), "actual_infinity_norm_error": str(eps),
            "inside_guaranteed_neighborhood": bool(eps <= radius),
            "norm_certificate_max_ambiguous": max_unclassified}


def upper_half_root(square, denominator=2**24):
    scaled_numerator = int(sp.numer(square)) * denominator**2
    scaled_denominator = int(sp.denom(square))
    numerator = math.isqrt(scaled_numerator // scaled_denominator)
    if numerator**2 * scaled_denominator < scaled_numerator:
        numerator += 1
    answer = R(numerator, 2 * denominator)
    assert 4 * answer**2 >= square
    return answer


def optimize_sandwich(Q, Qhat, c, C, cells, objective, upper_rows):
    Qinv = Q.inv()
    E = Q - Qhat
    outer_best, inner_best = None, None
    for cell in cells:
        p0, p1 = E * cell.intercept, E * cell.slope
        eta = max((p.T * Qinv * p)[0] for p in (p0 + p1 * cell.lo, p0 + p1 * cell.hi))

        def output(row):
            q0 = (row.T * (cell.intercept - Qinv * p0 / 2))[0]
            q1 = (row.T * (cell.slope - Qinv * p1 / 2))[0]
            radius = upper_half_root((row.T * Qinv * row)[0] * eta)
            return q0, q1, radius

        f0, f1, fradius = output(objective[1])
        f1 += objective[0]
        for inner in (False, True):
            lo, hi = cell.lo, cell.hi
            feasible = True
            for leader, row, rhs in upper_rows:
                g0, g1, gradius = output(row)
                interval = intersect_leq(lo, hi, g0 + (gradius if inner else -gradius) - rhs, g1 + leader)
                if interval is None:
                    feasible = False
                    break
                lo, hi = interval
            if feasible:
                x = lo if f1 >= 0 else hi
                value = f0 + f1 * x + (fradius if inner else -fradius)
                if inner and (inner_best is None or value < inner_best[0]):
                    inner_best = (value, x)
                if not inner and (outer_best is None or value < outer_best[0]):
                    outer_best = (value, x)
    return outer_best, inner_best


def run_checks():
    started = time.perf_counter()
    report = {"arithmetic": "exact rational SymPy; scalar LPs by rational interval intersection"}
    small = []
    for seed, scale in [(101, 10000), (207, 100), (319, 10)]:
        Q, Qhat, c, C, objective, rows = dense_family(5, seed, scale)
        cells = diagonal_cells([R(1)] * 5, c, C)
        screened, stats = optimize_screened(Q, Qhat, c, C, cells, objective, rows)
        exhaustive = optimize_exhaustive(Q, c, C, objective, rows)
        assert screened is not None and exhaustive is not None
        assert screened[0] == exhaustive[0]
        check_kkt(Q, c, C, screened[1], screened[2])
        assert all(a * screened[1] + (b.T * screened[2])[0] <= h for a, b, h in rows)
        small.append({"seed": seed, "perturbation_denominator": scale * 5, **stats,
                      "exact_optimum": str(screened[0]), "exact_leader": str(screened[1]),
                      "matches_all_243_true_statuses": True})
    report["exhaustive_comparisons"] = small

    # Check the VI ellipse and signed output bounds at independently enumerated responses.
    Q, Qhat, c, C, objective, rows = dense_family(4, 73, 20)
    Qinv = Q.inv()
    output_count = 0
    for x in [R(i, 12) for i in range(13)]:
        answer = optimize_exhaustive(Q, c, C, (R(0), sp.zeros(4, 1)), [], x, x)
        assert answer is not None
        z = answer[2]
        y = sp.Matrix([min(R(1), max(R(0), -c[i] - C[i] * x)) for i in range(4)])
        e, p = z - y, (Q - Qhat) * y
        assert (e.T * Q * e + p.T * e)[0] <= 0
        for b in [sp.eye(4)[:, i] for i in range(4)] + [Q[:, i] for i in range(4)] + [sp.Matrix([2, -3, 1, -2])]:
            center = (b.T * e + b.T * Qinv * p / 2)[0]
            assert 4 * center**2 <= (b.T * Qinv * b)[0] * (p.T * Qinv * p)[0]
            output_count += 1
    report["exact_directional_enclosures"] = {"leader_points": 13, "signed_outputs_checked": output_count}

    # A zero-gradient bound is not identified by the strict gradient test.
    assert not greater_than_half_root(R(0), R(0))
    Q = sp.diag(1, 2, 3)
    c, C = sp.Matrix([0, -2, R(-3, 2)]), sp.zeros(3, 1)
    singleton = diagonal_cells([1, 2, 3], c, C, R(0), R(0))
    statuses, eta = screen(Q, Q, Q.inv(), c, C, singleton[0])
    assert statuses == ["L", "U", "F"] and eta == 0
    answer, stats = optimize_screened(Q, Q, c, C, singleton, (R(0), sp.Matrix([-1, 2, -3])), [])
    assert answer is not None and answer[2] == sp.Matrix([0, 1, R(1, 2)])
    report["degeneracy"] = {"singleton_cell_statuses": statuses, "zero_gradient_strict_test_rejected": True}

    # Closing an exact surrogate interior cell must not create artificial ambiguity.
    c, C = sp.zeros(6, 1), -sp.ones(6, 1)
    cell = diagonal_cells([1] * 6, c, C)[0]
    closure_statuses, eta = screen(sp.eye(6), sp.eye(6), sp.eye(6), c, C, cell)
    assert closure_statuses == ["F"] * 6
    report["weak_closure_free_certificate"] = {"N": 6, "statuses": closure_statuses,
                                               "all_coordinates_hit_both_clipping_boundaries": True}

    # Shifted switch: surrogate lower threshold at x=1/2, true threshold shifts
    # because the second coordinate is interior and coupled to the first.
    Qhat = sp.eye(2)
    Q = sp.Matrix([[1, R(1, 10)], [R(1, 10), 1]])
    c, C = sp.Matrix([R(1, 2), R(-1, 2)]), sp.Matrix([-1, 0])
    objective, rows = (R(0), sp.Matrix([-1, 0])), [(R(0), sp.Matrix([1, 0]), R(1, 5))]
    cells = diagonal_cells([1, 1], c, C)
    answer, stats = optimize_screened(Q, Qhat, c, C, cells, objective, rows)
    direct = optimize_exhaustive(Q, c, C, objective, rows)
    assert answer[0] == direct[0] == R(-1, 5)
    assert answer[1] == R(187, 250)
    at_surrogate_switch = optimize_exhaustive(Q, c, C, (R(0), sp.zeros(2, 1)), [], R(21, 40), R(21, 40))
    assert at_surrogate_switch[2][0] == 0
    assert R(21, 40) - R(1, 2) > 0  # surrogate is already interior here
    report["shifted_switch"] = {"true_switch": "11/20", "surrogate_switch": "1/2",
                                "exact_constrained_leader": str(answer[1]), **stats}

    # Exact upper equality remains supported; robust inner approximations may be empty.
    equality_rows = rows + [(R(0), sp.Matrix([-1, 0]), R(-1, 5))]
    equality_answer, _ = optimize_screened(Q, Qhat, c, C, cells, objective, equality_rows)
    assert equality_answer is not None and equality_answer[1] == R(187, 250)
    outer_equal, inner_equal = optimize_sandwich(Q, Qhat, c, C, cells, objective, equality_rows)
    assert outer_equal is not None and inner_equal is None
    report["upper_equality"] = {"exact_feasible_leader": str(equality_answer[1]),
                                 "robust_inner_empty_despite_true_feasibility": True}

    outer, inner = optimize_sandwich(Q, Qhat, c, C, cells, objective, rows)
    assert outer is not None and inner is not None
    assert outer[0] <= answer[0] <= inner[0]
    true_inner = optimize_exhaustive(Q, c, C, objective, rows, inner[1], inner[1])
    assert true_inner is not None and true_inner[0] <= inner[0]
    report["signed_objective_sandwich"] = {"lower_bound": str(outer[0]), "true_optimum": str(answer[0]),
                                            "upper_bound": str(inner[0]), "inner_leader_true_feasible": True}

    # An infeasible response-dependent upper inequality.
    impossible_rows = [(R(0), sp.Matrix([1, 0]), R(-1, 10))]
    answer, _ = optimize_screened(Q, Qhat, c, C, cells, objective, impossible_rows)
    assert answer is None
    report["infeasible_upper_constraint_detected"] = True

    # A useful negative example: globally constant radii can obscure easy free statuses.
    n = 6
    Qhat, Q = sp.eye(n), sp.eye(n) + sp.ones(n, n) / (1000 * n)
    c, C = sp.zeros(n, 1), -sp.ones(n, 1)
    cells = diagonal_cells([1] * n, c, C)
    status, eta = screen(Q, Qhat, Q.inv(), c, C, cells[0])
    assert status == ["?"] * n
    p, slope, constraints = candidate_response(Q, c, C, ["F"] * n)
    assert all(max(extremes(a, b, R(0), R(1))) <= 0 for a, b in constraints)
    assert p == sp.zeros(n, 1) and slope == sp.ones(n, 1) * R(1000, 1001)
    report["conservative_screening_negative_example"] = {
        "N": n, "matrix_error_infinity_norm": "1/1000", "ellipsoid_ambiguous": n,
        "true_response": "z_i(x)=1000*x/1001 for all i",
        "all_free_pattern_directly_certified_over_entire_cell": True}

    medium = []
    for n in [8, 12, 20]:
        tick = time.perf_counter()
        Q, Qhat, c, C, objective, rows = dense_family(n)
        cells = diagonal_cells([R(1)] * n, c, C)
        answer, stats = optimize_screened(Q, Qhat, c, C, cells, objective, rows)
        assert answer is not None
        check_kkt(Q, c, C, answer[1], answer[2])
        medium.append({"N": n, **stats, "all_status_enumeration_size": 3**n,
                       "exact_optimum": str(answer[0]), "seconds": round(time.perf_counter() - tick, 3),
                       "exact_returned_KKT": True,
                       "perturbation_neighborhood": neighborhood_certificate(Q, Qhat, c, C, cells)})
    report["dense_scaling_examples"] = medium
    report["total_seconds"] = round(time.perf_counter() - started, 3)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("approximate_structure_checks.json"))
    args = parser.parse_args()
    report = run_checks()
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
