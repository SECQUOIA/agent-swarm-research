"""Independent dense rational checks of the latent-separator derivation.

This reviewer script imports no producer or certificate code. SymPy forms and
inverts the original dense covariances; every assertion uses exact arithmetic,
including rational enclosures of the few logarithms used in bound checks.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import time

import sympy as s


Q = s.Rational
COUNTS: Counter[str] = Counter()
P = Q(3, 2)
R_NOISE = Q(2, 5)
J0 = s.Matrix([[3, Q(1, 3)], [Q(1, 3), 2]])
W = s.Matrix([[Q(2, 3), Q(1, 7)], [Q(1, 7), Q(3, 5)]])


def equal(left, right, label):
    assert left == right, (label, left, right)
    COUNTS[label] += 1


def psd(matrix, label):
    assert matrix == matrix.T
    for size in range(1, matrix.rows + 1):
        for indices in combinations(range(matrix.rows), size):
            assert matrix.extract(indices, indices).det() >= 0, (label, matrix)
    COUNTS[label] += 1


def subsets(indices):
    for size in range(len(indices) + 1):
        yield from combinations(indices, size)


def covariance(n, rho):
    return s.Matrix(n, n, lambda i, j: P * rho ** abs(i - j))


def sensitivities(n):
    return s.Matrix(n, 2, lambda i, j: Q(((-1) ** (i + j)) * (i + j + 1), j + 2))


def schur(matrix, retained):
    removed = tuple(i for i in range(matrix.rows) if i not in retained)
    aa = matrix.extract(retained, retained)
    if not removed:
        return aa
    ab = matrix.extract(retained, removed)
    return aa - ab * matrix.extract(removed, removed).inv() * ab.T


def representation(k, anchors):
    n = k.rows
    if not anchors:
        return s.zeros(n, 0), k + R_NOISE * s.eye(n), s.zeros(0, 0)
    ka_inverse = k.extract(anchors, anchors).inv()
    h = k.extract(range(n), anchors) * ka_inverse
    d = k - h * k.extract(anchors, range(n)) + R_NOISE * s.eye(n)
    return h, d, ka_inverse


def augmented(f, h, d, precision, selected):
    base = s.diag(J0, precision)
    if not selected:
        return base
    design = f.row_join(h).extract(selected, range(f.cols + h.cols))
    return base + design.T * d.extract(selected, selected).inv() * design


def original_information(f, r, selected):
    if not selected:
        return J0
    fs = f.extract(selected, range(f.cols))
    return J0 + fs.T * r.extract(selected, selected).inv() * fs


def log_bounds(q):
    """Exact log enclosure by binary rescaling and the atanh series."""
    assert q > 0
    power = 0
    while q < 1:
        q *= 2
        power -= 1
    while q > 2:
        q /= 2
        power += 1

    def series(x):
        t = (x - 1) / (x + 1)
        terms = 32
        low = 2 * sum(t ** (2 * j + 1) / (2 * j + 1) for j in range(terms))
        remainder = 2 * t ** (2 * terms + 1) / ((2 * terms + 1) * (1 - t * t))
        return low, low + remainder

    low, high = series(q)
    low2, high2 = series(s.Integer(2))
    if power >= 0:
        return low + power * low2, high + power * high2
    return low + power * high2, high + power * low2


def upper_log_check(q, rational_upper, label):
    _, high = log_bounds(q)
    assert high <= rational_upper, (label, q, rational_upper)
    COUNTS[label] += 1


def closed_loadings(n, anchors, rho):
    h = s.zeros(n, len(anchors))
    for i in range(n):
        if i in anchors:
            h[i, anchors.index(i)] = 1
        elif anchors:
            before = [a for a in anchors if a < i]
            after = [a for a in anchors if a > i]
            if not before:
                h[i, 0] = rho ** (anchors[0] - i)
            elif not after:
                h[i, len(anchors) - 1] = rho ** (i - anchors[-1])
            else:
                a, c = before[-1], after[0]
                ell, u = i - a, c - i
                h[i, anchors.index(a)] = rho ** ell * (1 - rho ** (2 * u)) / (1 - rho ** (2 * (ell + u)))
                h[i, anchors.index(c)] = rho ** u * (1 - rho ** (2 * ell)) / (1 - rho ** (2 * (ell + u)))
    return h


def arbitrary_g(m):
    return s.Matrix(m, 2, lambda i, j: Q((i + 2) * ((-1) ** (i + j)), 7 + j))


def block_checks(n, b, rho):
    k = covariance(n, rho)
    r = k + R_NOISE * s.eye(n)
    f = sensitivities(n)
    blocks = [tuple(range(start, min(start + b, n))) for start in range(0, n, b)]
    anchors = tuple(block[-1] for block in blocks[:-1])
    h, d, precision = representation(k, anchors)
    equal(h, closed_loadings(n, anchors, rho), "stationary_loadings")
    for left, right in combinations(blocks, 2):
        equal(d.extract(left, right), s.zeros(len(left), len(right)), "cross_block_zeros")
    assert all(d[:j, :j].det() > 0 for j in range(1, n + 1))
    COUNTS["residual_spd"] += 1
    g = arbitrary_g(len(anchors))
    e = s.eye(2).col_join(g)
    prior = s.diag(J0, precision)
    dense_anchor_score = s.trace(W * g.T * precision * g)
    sparse_anchor_score = s.Integer(0)
    if anchors:
        sparse_anchor_score = (g[0, :] * W * g[0, :].T)[0] / P
        for j in range(1, len(anchors)):
            c = rho ** (anchors[j] - anchors[j - 1])
            difference = g[j, :] - c * g[j - 1, :]
            sparse_anchor_score += (difference * W * difference.T)[0] / (P * (1 - c * c))
    equal(dense_anchor_score, sparse_anchor_score, "anchor_precision_quadratic")

    tables = []
    for block in blocks:
        scores = {}
        for pattern in subsets(block):
            increment = augmented(f, h, d, precision, pattern) - prior
            scores[pattern] = s.trace(W * e.T * increment * e)
            assert scores[pattern] >= 0
        tables.append(scores)

    brute_by_count = {}
    matrices = {}
    for number, selected in enumerate(subsets(tuple(range(n)))):
        matrix = augmented(f, h, d, precision, selected)
        matrices[selected] = matrix
        information = original_information(f, r, selected)
        equal(schur(matrix, (0, 1)), information, "all_subset_information")
        selected_set = set(selected)
        additive = prior.copy()
        score = s.Integer(0)
        for block, table in zip(blocks, tables):
            pattern = tuple(i for i in block if i in selected_set)
            additive += augmented(f, h, d, precision, pattern) - prior
            score += table[pattern]
        equal(additive, matrix, "block_additive_augmented")
        equal(score, s.trace(W * e.T * (matrix - prior) * e), "block_scalar_scores")
        brute_by_count[len(selected)] = max(brute_by_count.get(len(selected), score), score)

        c = matrix[2:, 2:]
        g_star = -c.inv() * matrix[2:, :2] if anchors else s.zeros(0, 2)
        projected = e.T * matrix * e
        equal(projected - information, (g - g_star).T * c * (g - g_star), "completion_of_square")
        psd(projected - information, "arbitrary_g_psd_gap")
        if number % 7 == 0:
            # Rearrange certificate as log(det J det W) <= tr(W Q) - p.
            upper_log_check(information.det() * W.det(), s.trace(W * projected) - 2, "arbitrary_w_g_log_certificate")

    # Count compression followed by max-plus convolution; brute above uses
    # direct globally selected dense matrices, not this recurrence.
    best = {0: s.Integer(0)}
    for table in tables + [{(): s.Integer(0)}]:
        local = {}
        for pattern, value in table.items():
            local[len(pattern)] = max(local.get(len(pattern), value), value)
        next_best = {}
        for count, value in best.items():
            for local_count, local_value in local.items():
                total = count + local_count
                candidate = value + local_value
                next_best[total] = max(next_best.get(total, candidate), candidate)
        best = next_best
    equal(best, brute_by_count, "all_cardinality_dp")
    equal(best[0], 0, "empty_blocks_and_zero_count")
    equal(s.trace(W * e.T * prior * e), s.trace(W * J0) + dense_anchor_score, "prior_added_once")

    # Anchor residual noise is independent, so reassigning it to the other
    # neighboring block must preserve exact block additivity.
    if anchors:
        right_blocks = [tuple(range(0, anchors[0]))]
        right_blocks += [tuple(range(a, c)) for a, c in zip(anchors, anchors[1:])]
        right_blocks += [tuple(range(anchors[-1], n))]
        for left, right in combinations(right_blocks, 2):
            equal(d.extract(left, right), s.zeros(len(left), len(right)), "anchor_reassignment_zeros")
    COUNTS["stationary_model_cases"] += 1


def generic_concavity_checks():
    for nuisance in range(4):
        dimension = 2 + nuisance
        for seed in range(1, 5):
            u = s.Matrix(dimension, dimension, lambda i, j: ((i + 1) * (j + seed + 2)) % 7 - 3)
            v = s.Matrix(dimension, dimension, lambda i, j: ((i + seed + 3) * (j + 1)) % 5 - 2)
            first = u.T * u + (seed + 1) * s.eye(dimension)
            second = v.T * v + (seed + 2) * s.eye(dimension)
            half = (first + second) / 2
            j1, j2, jhalf = (schur(m, (0, 1)) for m in (first, second, half))
            psd(jhalf - (j1 + j2) / 2, "schur_concavity")
            assert jhalf.det() ** 2 >= j1.det() * j2.det()
            COUNTS["logdet_schur_concavity"] += 1
            c = first[2:, 2:]
            ci = c.inv() if nuisance else s.zeros(0, 0)
            g = -ci * first[2:, :2]
            e = s.eye(2).col_join(g)
            gradient = e * j1.inv() * e.T
            # Independent derivative of log det M - log det C.
            equal(gradient, first.inv() - s.diag(s.zeros(2, 2), ci), "gradient_inverse_identity")
            equal(gradient.rank(), 2, "gradient_rank_p")
            equal(s.trace(gradient * first), 2, "gradient_trace_p")
            psd(gradient, "gradient_psd")
            upper_log_check(j2.det() / j1.det(), s.trace(gradient * (second - first)), "tangent_certificate")
            direction = u + u.T
            second_derivative = -s.trace(first.inv() * direction * first.inv() * direction)
            if nuisance:
                dc = direction[2:, 2:]
                second_derivative += s.trace(ci * dc * ci * dc)
            assert second_derivative <= 0
            COUNTS["arbitrary_direction_hessian"] += 1


def nested_anchor_checks():
    n = 5
    chain = [(), (1,), (1, 3), (0, 1, 2, 3, 4)]
    for rho in (Q(-2, 3), Q(0), Q(1, 2)):
        k, f = covariance(n, rho), sensitivities(n)
        families = {}
        for anchors in chain:
            h, d, precision = representation(k, anchors)
            families[anchors] = {
                selected: augmented(f, h, d, precision, selected)
                for selected in subsets(tuple(range(n)))
            }
        for a, b in combinations(chain, 2):
            retained = (0, 1) + tuple(2 + b.index(anchor) for anchor in a)
            for selected in families[a]:
                equal(families[a][selected], schur(families[b][selected], retained), "nested_single_schedule_identity")
            selections = list(combinations(range(n), 2))
            denominator = sum(range(1, len(selections) + 1))
            mean_a = s.zeros(2 + len(a), 2 + len(a))
            mean_b = s.zeros(2 + len(b), 2 + len(b))
            for weight, selected in enumerate(selections, 1):
                mean_a += Q(weight, denominator) * families[a][selected]
                mean_b += Q(weight, denominator) * families[b][selected]
            eliminated_b = schur(mean_b, retained)
            psd(eliminated_b - mean_a, "nested_augmented_mixture_order")
            ja, jb = schur(mean_a, (0, 1)), schur(mean_b, (0, 1))
            psd(jb - ja, "nested_parameter_mixture_order")
            assert jb.det() >= ja.det()
            COUNTS["nested_logdet_order"] += 1


def singleton_baseline_checks():
    n = 5
    weights = [Q(0), Q(1, 3), Q(1), Q(2, 3), Q(0)]
    selected = tuple(i for i, z in enumerate(weights) if z)
    for rho in (Q(-2, 3), Q(0), Q(1, 2)):
        k, f = covariance(n, rho), sensitivities(n)
        r = k + R_NOISE * s.eye(n)
        for anchors in (tuple(range(n)), tuple(range(n - 1))):
            h, d, precision = representation(k, anchors)
            assert d.is_diagonal()
            expected = [R_NOISE] * n
            if len(anchors) == n - 1:
                expected[-1] += P * (1 - rho * rho)
            equal(list(d.diagonal()), expected, "singleton_residual_diagonal")
            mean = s.diag(J0, precision)
            for i, z in enumerate(weights):
                mean += z * (augmented(f, h, d, precision, (i,)) - s.diag(J0, precision))
            virtual = r.extract(selected, selected) + s.diag(*(d[i, i] * (1 - weights[i]) / weights[i] for i in selected))
            fs = f.extract(selected, range(2))
            equal(schur(mean, (0, 1)), J0 + fs.T * virtual.inv() * fs, "singleton_virtual_noise_identity")
    for rho in (Q(-2, 3), Q(0), Q(1, 2)):
        _, d, _ = representation(covariance(1, rho), ())
        equal(d, s.Matrix([[P + R_NOISE]]), "one_candidate_no_anchor_residual")


def nonstationary_checks():
    n = 6
    transitions = [Q(-1, 2), Q(0), Q(2, 3), Q(-3, 4), Q(1, 3)]
    innovations = [Q(5, 3), Q(1, 4), Q(2, 5), Q(3, 7), Q(1, 6), Q(2, 9)]
    loading = s.eye(n)
    for i in range(1, n):
        loading[i, :i] = transitions[i - 1] * loading[i - 1, :i]
    k = loading * s.diag(*innovations) * loading.T
    f = sensitivities(n)
    h, d, precision = representation(k, (1, 3))
    blocks = ((0, 1), (2, 3), (4, 5))
    for left, right in combinations(blocks, 2):
        equal(d.extract(left, right), s.zeros(2, 2), "nonstationary_cross_block_zeros")
    for selected in subsets(tuple(range(n))):
        matrix = augmented(f, h, d, precision, selected)
        equal(schur(matrix, (0, 1)), original_information(f, k + R_NOISE * s.eye(n), selected), "nonstationary_all_subset_information")


def irregular_anchor_checks():
    anchors = (1, 2, 6)
    n = 8
    for rho in (Q(-2, 3), Q(0), Q(1, 2)):
        k = covariance(n, rho)
        h, _, precision = representation(k, anchors)
        equal(h, closed_loadings(n, anchors, rho), "irregular_anchor_loadings")
        innovation_map = s.eye(len(anchors))
        inverse_variances = [1 / P]
        for j in range(1, len(anchors)):
            c = rho ** (anchors[j] - anchors[j - 1])
            innovation_map[j, j - 1] = -c
            inverse_variances.append(1 / (P * (1 - c * c)))
        equal(precision, innovation_map.T * s.diag(*inverse_variances) * innovation_map, "irregular_anchor_full_precision")


def bridge_checks():
    n = 7
    for rho in (Q(-2, 3), Q(0), Q(1, 2)):
        k = covariance(n, rho)
        for left, right in ((None, None), (None, 5), (1, None), (1, 5)):
            anchors = tuple(a for a in (left, right) if a is not None)
            h, d, _ = representation(k, anchors)
            conditional = d - R_NOISE * s.eye(n)
            first = left if left is not None else 0
            last = right if right is not None else n - 1
            points = tuple(range(first, last + 1))

            def variance(t):
                value = P
                if left is not None:
                    value *= 1 - rho ** (2 * (t - left))
                if right is not None:
                    value *= 1 - rho ** (2 * (right - t))
                if left is not None and right is not None:
                    value /= 1 - rho ** (2 * (right - left))
                return value

            def transition(before, after):
                value = rho ** (after - before)
                if right is not None:
                    assert before < right
                    value *= (1 - rho ** (2 * (right - after))) / (1 - rho ** (2 * (right - before)))
                return value

            for t in points:
                equal(conditional[t, t], variance(t), "bridge_marginal_variance")
            for before, after in combinations(points, 2):
                a = transition(before, after)
                equal(conditional[after, before], a * variance(before), "bridge_transition_covariance")
                q = variance(after) - a * a * variance(before)
                assert q >= 0
                COUNTS["bridge_gap_innovation_nonnegative"] += 1

            # Verify the information from scalar noisy bridge innovations
            # directly against the dense conditional covariance for all sparse
            # subsets. Use arbitrary augmented sensitivities [F,H], not only F.
            design = sensitivities(n).row_join(h)
            dimension = design.cols
            for selected in subsets(points):
                info = s.zeros(dimension, dimension)
                state_information = s.zeros(1, dimension)
                posterior_variance = s.Integer(0)
                previous = None
                for t in selected:
                    if previous is None:
                        predicted_variance = variance(t)
                    else:
                        a = transition(previous, t)
                        predicted_variance = variance(t) - a * a * variance(previous) + a * a * posterior_variance
                        state_information *= a
                    innovation_variance = predicted_variance + R_NOISE
                    innovation_sensitivity = design[t, :] - state_information
                    info += innovation_sensitivity.T * innovation_sensitivity / innovation_variance
                    gain = predicted_variance / innovation_variance
                    state_information += gain * innovation_sensitivity
                    posterior_variance = predicted_variance * R_NOISE / innovation_variance
                    previous = t
                dense = s.zeros(dimension, dimension)
                if selected:
                    selected_design = design.extract(selected, range(dimension))
                    dense = selected_design.T * d.extract(selected, selected).inv() * selected_design
                equal(info, dense, "bridge_all_subset_kalman_information")


def main():
    started = time.monotonic()
    for n, b in ((1, 1), (1, 3), (2, 1), (2, 2), (4, 2), (5, 2), (5, 3), (5, 5), (6, 4)):
        for rho in (Q(-2, 3), Q(0), Q(1, 2)):
            block_checks(n, b, rho)
    generic_concavity_checks()
    nested_anchor_checks()
    singleton_baseline_checks()
    nonstationary_checks()
    irregular_anchor_checks()
    bridge_checks()
    report = {
        "status": "all exact assertions passed",
        "scope": "independent theory tests; no producer implementation imported or reviewed",
        "arithmetic": "SymPy rational matrices and rational logarithm enclosures",
        "counts": dict(sorted(COUNTS.items())),
        "seconds": time.monotonic() - started,
    }
    output = Path(__file__).parent / "results" / "latent-separator-independent-theory-checks.json"
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
