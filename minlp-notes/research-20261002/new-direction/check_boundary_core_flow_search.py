#!/usr/bin/env python3
"""End-to-end exact diagnostic of dyadic search plus boundary flow faces.

This is the two-core, two-parallel-arc toy only. It enumerates both flows
and uses closed-form quadratic minima for independent verification and the
same-draw cutoff fallback. It is not a general flow or polynomial solver.
"""

from collections import Counter
from fractions import Fraction as F
from itertools import product


FLOWS = ((1, 0), (0, 1))
UNIT_BOX = ((F(0), F(1)), (F(0), F(1)))
FACE_PATTERNS = tuple(product((None, 0, 1), repeat=2))
MAX_LEVEL = 8


def value(gamma, v, z):
    return sum(v[i] ** 2 / 2 + (gamma[i] + z[i]) * v[i] for i in range(2))


def fixed_flow_minimum(gamma, z, box=UNIT_BOX):
    point = tuple(min(hi, max(lo, -gamma[i] - z[i]))
                  for i, (lo, hi) in enumerate(box))
    return value(gamma, point, z), point


def true_minimum(gamma, box=UNIT_BOX):
    answers = [(cost, point, z) for z in FLOWS
               for cost, point in [fixed_flow_minimum(gamma, z, box)]]
    optimum = min(answer[0] for answer in answers)
    return optimum, tuple(answer for answer in answers if answer[0] == optimum)


def corners(box):
    return tuple(product(*(tuple(set(interval)) for interval in box)))


def quadratic_minimum(a, b, c, interval):
    lo, hi = interval
    points = [lo, hi]
    if a > 0 and lo <= -b / (2 * a) <= hi:
        points.append(-b / (2 * a))
    return min(a * t * t + b * t + c for t in points)


def inside(point, box):
    return all(lo <= t <= hi for t, (lo, hi) in zip(point, box))


def certify_face(gamma, box, face, counts):
    counts["face patterns examined"] += 1
    active = [i for i in range(2) if face[i] is not None]
    if not active:
        # The all-free pattern belongs to the separate uniform-flow test.
        # Do not let that shortcut bypass boundary-face testing here.
        counts["all-free patterns not used"] += 1
        return None
    for i in active:
        if (face[i] == 0 and box[i][0] != 0) or (face[i] == 1 and box[i][1] != 1):
            counts["faces not touching hull"] += 1
            return None
    face_box = tuple((F(face[i]), F(face[i])) if i in active else box[i]
                     for i in range(2))
    center = tuple((lo + hi) / 2 for lo, hi in face_box)
    pivot = min(range(2), key=lambda i: center[i])
    # Arc costs are v_a*z_a. Set pi_source-pi_sink=-v_pivot on the face.
    # Its value at the center is an exact residual-potential certificate.
    intervals = []
    for i in range(2):
        reduced = [(center[i] - center[pivot]) * t for t in (0, 1)]
        minimum = min(reduced)
        labels = tuple(t for t in (0, 1) if reduced[t] == minimum)
        assert labels in ((0,), (1,), (0, 1))
        intervals.append(labels)
    tight = tuple(z for z in FLOWS if all(z[i] in intervals[i] for i in range(2)))
    conditional = min(value(gamma, center, z) for z in FLOWS)
    assert tight == tuple(z for z in FLOWS if value(gamma, center, z) == conditional)
    assert tight
    counts["exact potential interval checks"] += 1
    z0 = tight[0]
    face_corners = corners(face_box)

    # The reduced-cost equalities are affine on this face. Corner tests are exact.
    equalities_hold = all(
        (w[i] - w[pivot]) * (t - z0[i]) == 0
        for w in face_corners for i in range(2) for t in intervals[i]
    )
    if not equalities_hold:
        counts["uniform face equality failures"] += 1
        return None
    for w in face_corners:
        assert all(value(gamma, w, z) == value(gamma, w, z0) for z in tight)

    widths = {i: box[i][1] if face[i] == 0 else 1 - box[i][0] for i in active}
    total_width = sum(widths.values())
    max_width = max(widths.values())
    # H=1 and K=1. Sum of half-widths is a rational Euclidean radius bound.
    radius = sum((hi - lo) / 2 for i, (lo, hi) in enumerate(face_box) if i not in active)
    threshold = 2 * total_width  # r*K*T1 for two arcs.
    outside = []
    for i, labels in enumerate(intervals):
        for t in (0, 1):
            if t not in labels:
                boundary_label = min(labels, key=lambda label: abs(t - label))
                outside.append(min((w[i] - w[pivot]) * (t - boundary_label)
                                   for w in face_corners))
    if outside and min(outside) < threshold:
        counts["outside threshold failures"] += 1
        return None
    beta_components = tuple(
        min((1 if face[i] == 0 else -1) * (center[i] + gamma[i] + z[i]) for z in tight)
        for i in active
    )
    beta = min(beta_components)
    coefficient = beta - radius - max_width / 2
    if coefficient <= 0:
        counts["inward Taylor margin failures"] += 1
        return None

    # Verify the claimed global-on-hull inequality independently. Uniform face
    # optimality makes V(projection(v)) equal to F(projection(v),z0). The
    # difference minus coefficient*inward_distance is a separable quadratic.
    for z in FLOWS:
        minimum = F(0)
        for i in range(2):
            if face[i] == 0:
                a, b, c = F(1, 2), gamma[i] + z[i] - coefficient, F(0)
            elif face[i] == 1:
                a = F(1, 2)
                b = gamma[i] + z[i] + coefficient
                c = -F(1, 2) - gamma[i] - z0[i] - coefficient
            else:
                a, b, c = F(0), F(z[i] - z0[i]), F(0)
            minimum += quadratic_minimum(a, b, c, box[i])
        assert minimum >= 0
        counts["successful-face exact inequality minima"] += 1
    counts["successful boundary certificates"] += 1
    return face, z0, len(tight), coefficient


def run_draw(gamma, counts):
    reference_value, reference_answers = true_minimum(gamma)
    optimal_cores = {answer[1] for answer in reference_answers}
    cache = {}
    incumbent = None
    retained = [(0, 0)]
    for level in range(MAX_LEVEL + 1):
        if level:
            retained = [(2 * i + di, 2 * j + dj)
                        for i, j in retained for di, dj in product((0, 1), repeat=2)]
        spacing = F(1, 2**level)
        evaluated = []
        for i, j in retained:
            box = ((i * spacing, (i + 1) * spacing),
                   (j * spacing, (j + 1) * spacing))
            candidates = []
            for v in corners(box):
                if v not in cache:
                    cache[v] = min((value(gamma, v, z), v, z) for z in FLOWS)
                    counts["distinct conditional core evaluations"] += 1
                candidates.append(cache[v])
            best_corner = min(candidates)
            incumbent = best_corner if incumbent is None else min(incumbent, best_corner)
            lower = best_corner[0] - spacing**2 / 4
            # Independent exact cell minimum validates every corrected lower bound.
            cell_minimum, _ = true_minimum(gamma, box)
            assert lower <= cell_minimum <= best_corner[0]
            counts["corrected cells checked"] += 1
            evaluated.append(((i, j), box, lower))
        retained_records = [record for record in evaluated if record[2] <= incumbent[0]]
        retained = [record[0] for record in retained_records]
        assert retained
        hull = tuple((min(record[1][i][0] for record in retained_records),
                      max(record[1][i][1] for record in retained_records)) for i in range(2))
        assert all(inside(point, hull) for point in optimal_cores)
        assert min(record[2] for record in retained_records) <= reference_value <= incumbent[0]
        counts["search levels"] += 1
        successes = [certificate for face in FACE_PATTERNS
                     for certificate in [certify_face(gamma, hull, face, counts)]
                     if certificate is not None]
        if successes:
            # Every successful certificate must work, not merely the chosen one.
            for face, z0, tied_flow_count, coefficient in successes:
                assert all(all(face[i] is None or point[i] == face[i] for i in range(2))
                           for point in optimal_cores)
                cost, point = fixed_flow_minimum(gamma, z0, UNIT_BOX)
                assert cost == reference_value
                assert value(gamma, point, z0) == reference_value
                counts["whole-core fixed-flow completions checked"] += 1
            chosen = successes[0]
            counts["certified draws"] += 1
            counts[f"draws closed at level {level}"] += 1
            if chosen[2] == 2:
                counts["draws closed through both tied flows"] += 1
            else:
                counts["draws closed through singleton optimal flow"] += 1
            return "certificate", level, chosen[0]

    # Same gamma, exact two-label fallback. No redraw, probabilistic budget,
    # uniform-label shortcut, or theorem-sized sampling law is used.
    fallback = min((cost, point, z) for z in FLOWS
                   for cost, point in [fixed_flow_minimum(gamma, z, UNIT_BOX)])
    assert fallback[0] == reference_value
    counts["same-draw analytic fallbacks"] += 1
    return "fallback", MAX_LEVEL, None


def main():
    atoms = tuple(-F(1) + F(2 * i, 7) for i in range(8))
    counts = Counter()
    remaining = []
    for gamma in product(atoms, repeat=2):
        result, level, face = run_draw(gamma, counts)
        if result == "fallback":
            remaining.append(gamma)
    assert len(atoms) ** 2 == counts["certified draws"] + counts["same-draw analytic fallbacks"]
    assert remaining == [(t, t) for t in atoms if t < 0]
    assert counts["draws closed through both tied flows"] == 16
    print("PASS: all 64 core-noise draws; " + "; ".join(f"{value} {name}" for name, value in counts.items()))
    print("Fallback atoms: " + ", ".join(f"({a},{b})" for a, b in remaining))
    print(f"Scope: exact two-label toy, levels 0..{MAX_LEVEL}; all nine face patterns examined, all-free pattern not used to bypass boundary testing; no general flow oracle or sampling-law theorem.")


if __name__ == "__main__":
    main()
