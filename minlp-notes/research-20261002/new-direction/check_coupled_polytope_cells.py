"""Exact coupled-cell, relative-geometry and feasible-repair diagnostics.

P has z=v1+v2, 0<=v_i,z<=1, with optional z=1 or a thin v1 bound.
F_c=(z-1/3)^2-(v1^2+v2^2)/2-c'v. The supplied convexifier is
alpha=1. Every small fixture is solved by complete rational face
enumeration in its two reduced coordinates; this is not the proposed
general LP/GLS implementation or a stochastic performance test.
"""

from fractions import Fraction as Q
from itertools import combinations, product
import json
from pathlib import Path


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Q(0))


def lift(v):
    return v[0], v[1], v[0] + v[1]


def reduced(row):
    return row[0] + row[2], row[1] + row[2]


def vertices(rows):
    out = set()
    inequalities = [(reduced(a), b) for a, b in rows]
    for (a, b), (c, d) in combinations(inequalities, 2):
        det = a[0] * c[1] - a[1] * c[0]
        if not det:
            continue
        v = ((b * c[1] - a[1] * d) / det,
             (a[0] * d - b * c[0]) / det)
        if all(dot(t, v) <= rhs for t, rhs in inequalities):
            out.add(v)
    return sorted(out)


def value(v, hessian, linear, constant):
    return (sum(hessian[i][j] * v[i] * v[j] for i in range(2) for j in range(2)) / 2
            + dot(linear, v) + constant)


def gradient(v, hessian, linear):
    return tuple(linear[i] + dot(hessian[i], v) for i in range(2))


def quadratic_minimum(rows, hessian, linear, constant):
    vs = vertices(rows)
    if not vs:
        return None
    candidates = list(vs)
    for a, b in combinations(vs, 2):
        direction = tuple(b[i] - a[i] for i in range(2))
        curvature = sum(hessian[i][j] * direction[i] * direction[j]
                        for i in range(2) for j in range(2))
        if curvature:
            t = -dot(gradient(a, hessian, linear), direction) / curvature
            if 0 <= t <= 1:
                candidates.append(tuple(a[i] + t * direction[i] for i in range(2)))
    det = hessian[0][0] * hessian[1][1] - hessian[0][1] * hessian[1][0]
    if det:
        stationary = ((-linear[0] * hessian[1][1] + hessian[0][1] * linear[1]) / det,
                      (-hessian[0][0] * linear[1] + linear[0] * hessian[1][0]) / det)
        if all(dot(a, lift(stationary)) <= b for a, b in rows):
            candidates.append(stationary)
    return min((value(v, hessian, linear, constant), v) for v in candidates)


def nullspace(rows, n=3):
    matrix = [[Q(x) for x in a] for a in rows]
    pivots = []
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, len(matrix)) if matrix[i][c]), None)
        if pivot is None:
            continue
        matrix[r], matrix[pivot] = matrix[pivot], matrix[r]
        scale = matrix[r][c]
        matrix[r] = [x / scale for x in matrix[r]]
        for i in range(len(matrix)):
            if i != r:
                scale = matrix[i][c]
                matrix[i] = [matrix[i][j] - scale * matrix[r][j] for j in range(n)]
        pivots.append(c)
        r += 1
    free = [i for i in range(n) if i not in pivots]
    basis = []
    for c in free:
        vector = [Q(0)] * n
        vector[c] = Q(1)
        for i, p in enumerate(pivots):
            vector[p] = -matrix[i][c]
        basis.append(tuple(vector))
    return basis


def relative_geometry(rows, vs, counts):
    points = [lift(v) for v in vs]
    tight, witnesses = [], []
    for a, b in rows:
        slack, point = max((b - dot(a, x), x) for x in points)
        assert slack >= 0
        if slack == 0:
            tight.append(a)
        else:
            witnesses.append(point)
    center = (tuple(sum(x[i] for x in witnesses) / len(witnesses) for i in range(3))
              if witnesses else points[0])
    basis = nullspace(tight)
    radii = []
    for a, b in rows:
        coefficients = [dot(a, vector) for vector in basis]
        norm = sum(map(abs, coefficients))
        slack = b - dot(a, center)
        if norm:
            assert slack > 0
            radii.append(slack / norm)
        else:
            assert slack >= 0
    if basis:
        radius = min(radii)
        assert isinstance(radius, Q)
        assert all(isinstance(x, Q) for vector in basis for x in vector)
        assert radius > 0
        for a, b in rows:
            assert radius * sum(abs(dot(a, vector)) for vector in basis) <= b - dot(a, center)
        counts["positive_relative_ball_checks"] += 1
    else:
        assert len(vs) == 1
        counts["singleton_cells"] += 1
    counts["relative_dimensions"].add(len(basis))


def tangent_dual(rows, g, vbest):
    # First represent -g_reduced using active reduced inequality normals.
    target = (-g[0] - g[2], -g[1] - g[2])
    active = [i for i, (a, b) in enumerate(rows) if dot(a, lift(vbest)) == b]
    solution = None
    if target == (0, 0):
        solution = [Q(0)] * len(rows)
    for size in (1, 2):
        if solution is not None:
            break
        for indices in combinations(active, size):
            vectors = [reduced(rows[i][0]) for i in indices]
            if size == 1:
                a = vectors[0]
                coordinate = next((j for j in range(2) if a[j]), None)
                if coordinate is None:
                    continue
                coeff = target[coordinate] / a[coordinate]
                coeffs = [coeff]
            else:
                a, b = vectors
                det = a[0] * b[1] - b[0] * a[1]
                if not det:
                    continue
                coeffs = [(target[0] * b[1] - b[0] * target[1]) / det,
                          (a[0] * target[1] - target[0] * a[1]) / det]
            if min(coeffs) < 0:
                continue
            if tuple(sum(coeffs[t] * vectors[t][j] for t in range(size)) for j in range(2)) != target:
                continue
            solution = [Q(0)] * len(rows)
            for i, coefficient in zip(indices, coeffs):
                solution[i] = coefficient
            break
    assert solution is not None
    residual = tuple(g[j] + sum(solution[i] * rows[i][0][j] for i in range(len(rows)))
                     for j in range(3))
    # Add one sign of the equality z-v1-v2=0 to finish the ambient dual.
    signed = -residual[2]
    equality = (-Q(1), -Q(1), Q(1))
    assert all(residual[j] + signed * equality[j] == 0 for j in range(3))
    assert dot(g, lift(vbest)) == -sum(solution[i] * rows[i][1] for i in range(len(rows)))
    return abs(signed)  # All final multipliers are nonnegative after choosing its sign.


def original(v, c):
    z = v[0] + v[1]
    return (z - Q(1, 3)) ** 2 - dot(v, v) / 2 - dot(c, v)


def run():
    counts = {key: 0 for key in ["levels", "generated_cells", "empty_cells",
                               "positive_relative_ball_checks", "singleton_cells",
                               "tangent_dual_certificates", "retained_witnesses",
                               "noncorner_oracle_points", "global_intervals", "repair_checks"]}
    counts["relative_dimensions"] = set()
    base = [((-Q(1), Q(0), Q(0)), Q(0)), ((Q(1), Q(0), Q(0)), Q(1)),
            ((Q(0), -Q(1), Q(0)), Q(0)), ((Q(0), Q(1), Q(0)), Q(1)),
            ((Q(0), Q(0), -Q(1)), Q(0)), ((Q(0), Q(0), Q(1)), Q(1)),
            ((-Q(1), -Q(1), Q(1)), Q(0)), ((Q(1), Q(1), -Q(1)), Q(0))]
    domains = [base, base + [((Q(0), Q(0), -Q(1)), -Q(1))],
               base + [((Q(1), Q(0), Q(0)), Q(1, 2 ** 100))]]
    for rows in domains:
        for c in product([Q(-1), Q(0), Q(1)], repeat=2):
            h_true = [[Q(1), Q(2)], [Q(2), Q(1)]]
            linear_true = tuple(-Q(2, 3) - ci for ci in c)
            optimum, exact = quadratic_minimum(rows, h_true, linear_true, Q(1, 9))
            incumbent, retained = None, []
            for j in range(4):
                h = Q(1, 1 << j)
                e = h * h / 4
                masks = list(product((0, 1), repeat=2))
                generated = ([(0, 0)] if j == 0 else
                             [tuple(2 * p[i] + mask[i] for i in range(2))
                              for p in retained for mask in masks])
                records = []
                for index in generated:
                    lo, hi = tuple(i * h for i in index), tuple((i + 1) * h for i in index)
                    cell = list(rows)
                    for i in range(2):
                        a = [Q(0)] * 3
                        a[i] = Q(1)
                        cell.extend([(tuple(a), hi[i]), (tuple(-x for x in a), -lo[i])])
                    vs = vertices(cell)
                    if not vs:
                        counts["empty_cells"] += 1
                        continue
                    relative_geometry(cell, vs, counts)
                    hp = [[Q(2), Q(2)], [Q(2), Q(2)]]
                    lp = tuple(linear_true[i] - (lo[i] + hi[i]) / 2 for i in range(2))
                    cp = Q(1, 9) + dot(lo, hi) / 2
                    phi_star, phi_point = quadratic_minimum(cell, hp, lp, cp)
                    target = max(vs, key=lambda v: sum((v[i] - phi_point[i]) ** 2 for i in range(2)))
                    theta = h * h / 1024
                    while True:
                        w = tuple((1 - theta) * phi_point[i] + theta * target[i] for i in range(2))
                        grad = gradient(w, hp, lp)
                        linear_point = min(vs, key=lambda v: dot(grad, v))
                        phi_w = value(w, hp, lp, cp)
                        ell = phi_w + dot(grad, tuple(linear_point[i] - w[i] for i in range(2)))
                        if phi_w - ell <= e:
                            break
                        theta /= 2
                    assert ell <= phi_star <= phi_w and phi_w - ell <= e
                    gz = 2 * (sum(w) - Q(1, 3))
                    ambient_gradient = (-c[0] - (lo[0] + hi[0]) / 2,
                                        -c[1] - (lo[1] + hi[1]) / 2, gz)
                    tangent_dual(cell, ambient_gradient, linear_point)
                    counts["tangent_dual_certificates"] += 1
                    correction = original(w, c) - phi_w
                    assert 0 <= correction <= e
                    actual_cell_min, _ = quadratic_minimum(cell, h_true, linear_true, Q(1, 9))
                    assert ell <= actual_cell_min
                    upper = original(w, c)
                    incumbent = upper if incumbent is None else min(incumbent, upper)
                    if any(w[i] not in (lo[i], hi[i]) for i in range(2)):
                        counts["noncorner_oracle_points"] += 1
                    records.append((index, ell, upper))
                retained = []
                for index, ell, upper in records:
                    if ell <= incumbent:
                        retained.append(index)
                        assert upper <= optimum + 4 * e
                        counts["retained_witnesses"] += 1
                assert incumbent - 2 * e <= optimum <= incumbent
                assert any(all(index[i] * h <= exact[i] <= (index[i] + 1) * h for i in range(2))
                           for index in retained)
                counts["global_intervals"] += 1
                counts["generated_cells"] += len(generated)
                counts["levels"] += 1

            # One repair primitive supplies simultaneous core and objective accuracy.
            for q in (8, 40, 200):
                epsilon = Q(1, (1 << q) * 24)
                exact_x = lift(exact)
                center = tuple(exact_x[i] + epsilon * (Q(1), -Q(1), Q(1, 2))[i]
                               for i in range(3))
                repair = list(rows)
                for i in range(3):
                    a = [Q(0)] * 3
                    a[i] = Q(1)
                    repair.extend([(tuple(a), center[i] + epsilon),
                                   (tuple(-x for x in a), -center[i] + epsilon)])
                feasible = vertices(repair)
                assert feasible
                y = feasible[0]
                assert max(abs(lift(y)[i] - exact_x[i]) for i in range(3)) <= 2 * epsilon
                assert sum((y[i] - exact[i]) ** 2 for i in range(2)) <= Q(1, 1 << (2 * q))
                assert 0 <= original(y, c) - optimum <= 12 * epsilon
                assert original(y, c) - (optimum - Q(1, 1 << (q + 1))) <= Q(1, 1 << q)
                counts["repair_checks"] += 1

    # Clipping to ambient coordinate bounds alone does not restore the equality.
    p = (Q(1, 4) + Q(1, 100), Q(1, 4), Q(1, 2))
    assert all(0 <= x <= 1 for x in p) and p[2] != p[0] + p[1]
    counts["relative_dimensions"] = sorted(counts["relative_dimensions"])
    result = {"status": "pass", **counts, "ambient_clipping_counterexample": True,
              "thin_domain_denominator_bits": 101,
              "scope": "coupled quadratic fixtures, exact relative geometry, tangent duals and repair; no stochastic or general GLS implementation"}
    Path(__file__).with_name("coupled-polytope-cell-results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run()
