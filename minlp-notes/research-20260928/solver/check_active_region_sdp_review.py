#!/usr/bin/env python3
"""Independent numerical challenge of the regular recourse sharp example.

Exact Dirac checks validate matrix assembly. Floating-point SDP solves are
diagnostics, not certificates of either the theorem or the sharp gap.
"""

from fractions import Fraction as F
import json
import math

import cvxpy as cp
import numpy as np


def shifted(poly, shared, private):
    return {(a + shared, b + private): c for (a, b), c in poly.items()}


def evaluate(poly, u, y):
    return sum(c * u**a * y**b for (a, b), c in poly.items())


def moment(poly, values):
    return sum(float(c) * values[a, b] for (a, b), c in poly.items())


def block_polynomials(r, recourse):
    result = []
    for weighted in (0, 1):
        weight = {(0, 0): F(1)}
        if weighted:
            weight[(2, 0)] = F(-1)
        basis = [(a, b) for b in (0, 1) for a in range(r - weighted + 1)]
        result.append([
            [shifted(weight, a + c, b + d) for c, d in basis]
            for a, b in basis
        ])
        private_bound = dict(weight)
        private_bound.update({(a, 2): -c for (a, _), c in weight.items()})
        basis = range(r - weighted + 1)
        result.append([
            [shifted(private_bound, a + b, 0) for b in basis]
            for a in basis
        ])
        if recourse:
            # z=(1+y)/2 >= u, including the shared weight if present.
            affine = {(0, 0): F(1, 2), (0, 1): F(1, 2), (1, 0): F(-1)}
            localizer = {}
            for (a, b), c in weight.items():
                for (d, e), h in affine.items():
                    key = (a + d, b + e)
                    localizer[key] = localizer.get(key, F(0)) + c * h
            basis = range(r - weighted)
            result.append([
                [shifted(localizer, a + b, 0) for b in basis]
                for a in basis
            ])
    return result


def main():
    rows = []
    dirac_checks = 0
    first_cost = {
        (0, 0): F(1, 4), (0, 1): F(1, 2), (0, 2): F(1, 4),
        (1, 0): F(-1), (1, 1): F(-1),
    }
    second_cost = {(0, 0): F(1, 4), (0, 1): F(1, 2), (0, 2): F(1, 4)}
    for r in (2, 3, 4):
        blocks = [block_polynomials(r, flag) for flag in (False, True)]
        # Actual feasible optimizers have x=z=max(u,0) and objective zero.
        for u in (F(-1), F(-1, 3), F(0), F(2, 5), F(1)):
            y = 2 * max(u, F(0)) - 1
            exact = {(a, b): u**a * y**b for a in range(2 * r + 1) for b in range(3)}
            assert evaluate(first_cost, u, y) + evaluate(second_cost, u, y) == 0
            for recourse, bag in zip((False, True), blocks):
                expected = []
                for weighted in (0, 1):
                    g = (1 - u * u) ** weighted
                    vector = [u**a * y**b for b in (0, 1) for a in range(r - weighted + 1)]
                    expected.append([[g * v * w for w in vector] for v in vector])
                    vector = [u**a for a in range(r - weighted + 1)]
                    expected.append([[g * (1 - y * y) * v * w for w in vector] for v in vector])
                    if recourse:
                        vector = [u**a for a in range(r - weighted)]
                        expected.append([[g * ((1 + y) / 2 - u) * v * w for w in vector] for v in vector])
                for matrix, rank_one in zip(bag, expected):
                    for row, rank_one_row in zip(matrix, rank_one):
                        for poly, target in zip(row, rank_one_row):
                            assert sum(c * exact[a, b] for (a, b), c in poly.items()) == target
                            dirac_checks += 1
                    # Numerical eigenvalues are only a secondary assembly check.
                    mat = np.array([[float(evaluate(p, u, y)) for p in row] for row in matrix])
                    assert np.linalg.eigvalsh(mat).min() >= -1e-12

        values = [cp.Variable((2 * r + 1, 3)) for _ in range(2)]
        constraints = [values[0][0, 0] == 1, values[1][0, 0] == 1,
                       values[0][:, 0] == values[1][:, 0]]
        psd = []
        for bag, data in zip(blocks, values):
            for matrix in bag:
                expr = cp.bmat([[moment(p, data) for p in row] for row in matrix])
                psd.append(expr)
                constraints.append(expr >> 0)
        problem = cp.Problem(cp.Minimize(moment(first_cost, values[0]) + moment(second_cost, values[1])), constraints)
        problem.solve(solver="CLARABEL", tol_gap_abs=1e-10, tol_gap_rel=1e-10,
                      tol_feas=1e-10, max_iter=1000)
        assert all(v.value is not None for v in values)
        denominator = 2 * r * r + 1
        variance = 3 * (4 * r - 3) / (2 * r * denominator)
        rows.append({
            "r": r, "status": problem.status, "objective": problem.value,
            "minimum_psd_eigenvalue": min(float(np.linalg.eigvalsh(p.value).min()) for p in psd),
            "maximum_equality_residual": max(
                abs(float(values[0].value[0, 0]) - 1),
                abs(float(values[1].value[0, 0]) - 1),
                float(np.max(np.abs(values[0].value[:, 0] - values[1].value[:, 0])))),
            "proved_gap_lower": 2 / (27 * math.pi * (2 * r + 2)**2),
            "theorem_2_gap_upper": 12 / denominator + 2 * variance,
        })
    print(json.dumps({"exact_dirac_entry_checks": dirac_checks,
                      "cvxpy_version": cp.__version__, "results": rows}, indent=2))


if __name__ == "__main__":
    main()
