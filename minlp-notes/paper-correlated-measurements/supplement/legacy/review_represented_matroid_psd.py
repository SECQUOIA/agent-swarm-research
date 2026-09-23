"""Independent exact audit of the represented-matroid PSD approximation set.

This verifier imports no author or earlier review implementation. It enumerates
tiny matroids for ground truth, constructs determinants by sparse polynomial
arithmetic, and separately checks tensor interpolation on bounded profiles.
Exponential verification routines here are intentionally not the theorem's
polynomial-time solver. All mathematical comparisons use exact arithmetic.
"""

from collections import Counter, defaultdict
from itertools import combinations, permutations, product
import json
from pathlib import Path

import sympy as s


R = s.Rational
STATS = Counter()


def check(condition, name):
    if not condition:
        raise AssertionError(name)
    STATS[name] += 1


def cols(a, indices):
    return a[:, list(indices)]


def bases(a):
    q = a.rank()
    return [b for b in combinations(range(a.cols), q)
            if cols(a, b).rank() == q]


def psd(a):
    return a == a.T and all(a.extract(ix, ix).det() >= 0
                            for k in range(1, a.rows + 1)
                            for ix in combinations(range(a.rows), k))


def factors(a):
    residual = a.copy()
    result = []
    while residual != s.zeros(a.rows):
        pivot = next(i for i in range(a.rows) if residual[i, i] > 0)
        weight = residual[pivot, pivot]
        vector = residual[:, pivot] / weight
        result.append((weight, vector))
        residual -= weight * vector * vector.T
        check(psd(residual), "LDL_PSD_residuals")
    check(sum((w * v * v.T for w, v in result), s.zeros(a.rows)) == a,
          "LDL_reconstructions")
    return result


def dyadic(weight):
    scale = s.Integer(1)
    while scale**2 * weight < 1:
        scale *= 2
    while scale**2 * weight >= 4:
        scale /= 2
    check(1 <= scale**2 * weight < 4, "dyadic_bounds")
    return scale


def padd(a, b):
    out = dict(a)
    for key, value in b.items():
        out[key] = out.get(key, 0) + value
        if out[key] == 0:
            del out[key]
    return out


def pmul(a, b):
    out = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            key = tuple(x + y for x, y in zip(ka, kb))
            out[key] = out.get(key, 0) + va * vb
    return {key: value for key, value in out.items() if value}


def polynomial_det(a, weights, keep=None):
    """Direct Leibniz determinant of the polynomial matrix A diag(y^w) A^T.

    Never drop rows: a rank loss must produce the zero polynomial.
    This computation does not enumerate matroid bases or use squared minors.
    """
    if keep is None:
        keep = tuple(range(a.cols))
    dimension = len(weights[0]) if weights else 1
    zero = (0,) * dimension
    entries = [[{} for _ in range(a.rows)] for _ in range(a.rows)]
    for i, j in product(range(a.rows), repeat=2):
        for e in keep:
            if a[i, e] * a[j, e]:
                entries[i][j] = padd(entries[i][j],
                                     {weights[e]: a[i, e] * a[j, e]})
    total = {}
    for perm in permutations(range(a.rows)):
        sign = (-1) ** sum(perm[i] > perm[j]
                           for i in range(a.rows) for j in range(i + 1, a.rows))
        term = {zero: sign}
        for i, j in enumerate(perm):
            term = pmul(term, entries[i][j])
        total = padd(total, term)
    return total


def sum_profile(b, weights, dimension):
    return tuple(sum(weights[e][i] for e in b) for i in range(dimension))


def minor_coefficients(a, weights):
    """Exhaustive squared-minor ground truth, independent of polynomial_det."""
    coefficients = defaultdict(lambda: s.Integer(0))
    dimension = len(weights[0]) if weights else 1
    for b in combinations(range(a.cols), a.rows):
        det = cols(a, b).det()
        if det:
            coefficients[sum_profile(b, weights, dimension)] += det**2
    return dict(coefficients)


def recover(a, weights, target):
    keep = list(range(a.cols))
    for e in range(a.cols):
        reduced = [j for j in keep if j != e]
        test = polynomial_det(a, weights, reduced)
        rank = cols(a, reduced).rank()
        if rank < a.rows:
            check(not test, "fixed_row_rank_drop_rejections")
        if test.get(target, 0) > 0:
            keep = reduced
        STATS["deletion_coefficient_tests"] += 1
    check(len(keep) == a.rows and cols(a, keep).rank() == a.rows,
          "recovered_actual_bases")
    check(sum_profile(keep, weights, len(target)) == target,
          "recovered_target_profiles")
    return tuple(keep)


def contraction(a, retained, forced):
    extension = list(forced)
    for e in retained:
        if cols(a, extension + [e]).rank() > len(extension):
            extension.append(e)
    d = cols(a, extension)
    check(d.rows == d.cols and d.det() != 0, "contraction_extensions")
    optional = [e for e in retained if e not in forced]
    transformed = d.inv() * cols(a, optional)
    contracted = transformed[len(forced):, :]
    denominator = s.ilcm(*[v.q for v in contracted]) if len(contracted) > 1 else (
        contracted[0].q if len(contracted) else 1)
    integer = denominator * contracted
    check(all(v.q == 1 for v in integer), "integer_contractions")
    if denominator > 1:
        STATS["nontrivial_contraction_denominators"] += 1
    return integer, optional, d.det()**2 / denominator**(2 * contracted.rows)


def sandwich(target, representative, eta, label):
    check(psd(representative - (1 - eta) * target), label + "_lower")
    check(psd((1 + eta) * target - representative), label + "_upper")
    check(target.rank() == representative.rank() == (target + representative).rank(),
          label + "_same_kernel")


def information(prior, matrices, base):
    return prior + sum((matrices[e] for e in base), s.zeros(prior.rows))


def minimum_eigenvalue(a):
    if a.rank() < a.rows:
        return s.Integer(0)
    if a.rows == 1:
        return a[0, 0]
    if a.rows == 2:
        return (s.trace(a) - s.sqrt(s.trace(a)**2 - 4 * a.det())) / 2
    raise AssertionError("Full-rank eigenvalue fixture needs exact extension")


def review_case(name, raw_a, matrices, prior, eta=R(1, 2)):
    before = STATS.copy()
    p = prior.rows
    check(all(psd(v) for v in [prior] + matrices), "PSD_inputs")
    q = raw_a.rank()
    row_indices = raw_a.T.rref()[1]
    a = raw_a[list(row_indices), :]
    original_bases = bases(raw_a)
    check(bases(a) == original_bases, "redundant_row_invariance")
    if q > p:
        STATS["matroid_rank_above_information_dimension"] += 1
    infos = {b: information(prior, matrices, b) for b in original_bases}
    output = set()
    accepted = {}
    labels = [(owner, w, v) for owner, matrix in [(-1, prior)] + list(enumerate(matrices))
              for w, v in factors(matrix)]
    if q == 0:
        output.add(())
        STATS["rank_zero_matroid_cases"] += 1
    else:
        if prior == s.zeros(p):
            zero_elements = [e for e, matrix in enumerate(matrices) if matrix == s.zeros(p)]
            if cols(a, zero_elements).rank() == q:
                output.add(next(b for b in original_bases if set(b) <= set(zero_elements)))
                STATS["zero_information_representatives"] += 1
            elif zero_elements:
                STATS["zero_information_rank_loss_rejections"] += 1
        for r in range(1, p + 1):
            for selected in combinations(range(len(labels)), r):
                v = s.Matrix.hstack(*(labels[j][2] for j in selected))
                if v.rank() != r:
                    continue
                STATS["independent_factor_trials"] += 1
                left = (v.T * v).inv() * v.T
                projector = v * left
                scales = [dyadic(labels[j][1]) for j in selected]
                t = s.diag(*scales) * left
                k = v * s.diag(*(1 / x for x in scales))
                check(t * k == s.eye(r) and k * t == projector, "rectangular_identities")
                h0 = t * prior * t.T
                if projector * prior != prior or any(h0[i, i] > 4 * p for i in range(r)):
                    STATS["prior_filter_rejections"] += 1
                    continue
                transformed = [t * matrix * t.T for matrix in matrices]
                retained = [e for e, matrix in enumerate(matrices)
                            if projector * matrix == matrix
                            and all(transformed[e][i, i] <= 4 * p for i in range(r))]
                STATS["range_deleted_elements"] += sum(projector * m != m for m in matrices)
                STATS["magnitude_deleted_elements"] += sum(
                    projector * m == m and any(transformed[e][i, i] > 4 * p for i in range(r))
                    for e, m in enumerate(matrices))
                forced = sorted({labels[j][0] for j in selected if labels[j][0] >= 0})
                if sum(labels[j][0] >= 0 for j in selected) > len(forced):
                    STATS["repeated_factor_owner_trials"] += 1
                missing = not set(forced) <= set(retained)
                dependent = cols(a, forced).rank() != len(forced)
                rank_loss = cols(a, retained).rank() < q
                STATS["forced_owner_filtered_rejections"] += int(missing)
                STATS["dependent_forced_owner_rejections"] += int(dependent)
                STATS["restriction_rank_loss_rejections"] += int(rank_loss)
                if missing or dependent or rank_loss:
                    continue
                eligible = [b for b in original_bases
                            if set(forced) <= set(b) <= set(retained)]
                check(bool(eligible), "accepted_trial_feasibility")
                accepted[selected] = eligible
                for e in retained:
                    check(k * transformed[e] * k.T == matrices[e], "range_reconstructions")
                    check(all(abs(x) <= 4 * p for x in transformed[e]), "transformed_entry_bounds")
                check(k * h0 * k.T == prior, "prior_reconstructions")
                for b in eligible:
                    hb = information(h0, transformed, b)
                    check(psd(hb - s.eye(r)), "owner_lower_bounds")
                    check(infos[b].rank() == r, "forced_exact_information_rank")
                contracted, optional, coefficient_scale = contraction(a, retained, forced)
                optional_bases = bases(contracted)
                lifted = [tuple(sorted(forced + [optional[j] for j in b])) for b in optional_bases]
                check(set(lifted) == set(eligible), "contraction_lift_equivalence")
                qprime = q - len(forced)
                check(contracted.rows == contracted.rank() == qprime,
                      "contracted_original_rank")
                if qprime == 0:
                    output.add(tuple(forced))
                    STATS["rank_zero_contraction_trials"] += 1
                    continue
                h = eta / (r * q)
                dimension = r * (r + 1) // 2
                upper = [(i, j) for i in range(r) for j in range(i, r)]
                signed = [tuple(int(s.floor(transformed[e][i, j] / h)) for i, j in upper)
                          for e in optional]
                offset = int(s.ceiling(4 * p / h))
                weights = [tuple(z + offset for z in profile) for profile in signed]
                for j, e in enumerate(optional):
                    for ell, (u, v) in enumerate(upper):
                        check(0 <= transformed[e][u, v] - h * signed[j][ell] < h,
                              "signed_floor_residuals")
                        check(0 <= weights[j][ell] <= 2 * offset, "shifted_label_bounds")
                        STATS["negative_rounded_coordinates"] += int(signed[j][ell] < 0)
                coefficients = polynomial_det(contracted, weights)
                check(coefficients == minor_coefficients(contracted, weights),
                      "determinant_squared_coefficients")
                check(all(v > 0 for v in coefficients.values()), "positive_coefficients")
                grouped = defaultdict(list)
                for optional_base, lifted_base in zip(optional_bases, lifted):
                    key = sum_profile(optional_base, weights, dimension)
                    original_key = sum_profile(optional_base, signed, dimension)
                    check(tuple(z - qprime * offset for z in key) == original_key,
                          "signed_profile_shift_invariance")
                    grouped[key].append(lifted_base)
                check(set(coefficients) == set(grouped), "exact_profile_support")
                if len(coefficients) > 1:
                    STATS["trials_with_multiple_profiles"] += 1
                # Independent owner-count construction in the original representation.
                # Forced information is common, so assign zero matrix labels to F.
                optional_index = {e: j for j, e in enumerate(optional)}
                owner_weights = [(0,) * dimension + (1,) if e in forced
                                 else weights[optional_index[e]] + (0,) for e in retained]
                owner_coefficients = polynomial_det(cols(a, retained), owner_weights)
                owner_support = {key[:-1]: value for key, value in owner_coefficients.items()
                                 if key[-1] == len(forced)}
                check(owner_support == {key: coefficient_scale * value
                                        for key, value in coefficients.items()},
                      "owner_count_contraction_coefficient_equivalence")
                if forced:
                    STATS["nonempty_forced_owner_crosschecks"] += 1
                for profile, same_profile_bases in grouped.items():
                    recovered = recover(contracted, weights, profile)
                    representative = tuple(sorted(forced + [optional[j] for j in recovered]))
                    check(representative in same_profile_bases, "lifted_recovered_membership")
                    output.add(representative)
                    for target_base in same_profile_bases:
                        sandwich(infos[target_base], infos[representative], eta, "same_profile_sandwich")
                        delta = t * (infos[representative] - infos[target_base]) * t.T
                        check(all(abs(x) < qprime * h for x in delta), "profile_entry_error")
                    if len(same_profile_bases) > 1:
                        STATS["actual_profile_collisions"] += len(same_profile_bases) - 1
                        STATS["collisions_between_different_information_matrices"] += sum(
                            infos[b] != infos[same_profile_bases[0]] for b in same_profile_bases[1:])
                STATS["accepted_profile_trials"] += 1
        # A rational weighted Gram determinant identifies each target's max-volume witness.
        for b, info in infos.items():
            r = info.rank()
            if not r:
                continue
            owned = [j for j, (owner, _, _) in enumerate(labels) if owner == -1 or owner in b]
            candidates = []
            for selected in combinations(owned, r):
                v = s.Matrix.hstack(*(labels[j][2] for j in selected))
                volume = (v.T * v).det() * s.prod(labels[j][1] for j in selected)
                candidates.append((volume, selected))
            volume, selected = max(candidates)
            check(volume > 0 and selected in accepted and b in accepted[selected],
                  "maximum_volume_target_witnesses")
    check(output <= set(original_bases), "output_original_feasibility")
    for b, target in infos.items():
        representatives = [c for c in output if psd(infos[c] - (1 - eta) * target)
                           and psd((1 + eta) * target - infos[c])]
        check(bool(representatives), "all_target_coverage")
        representative = infos[representatives[0]]
        sandwich(target, representative, eta, "output_sandwich")
        target_inverse, representative_inverse = target.pinv(), representative.pinv()
        check(psd(representative_inverse - target_inverse / (1 + eta)) and
              psd(target_inverse / (1 - eta) - representative_inverse),
              "same_range_pseudoinverse_bounds")
        contrast = target[:, 0]
        check((contrast.T * representative_inverse * contrast)[0] <=
              (contrast.T * target_inverse * contrast)[0] / (1 - eta),
              "estimable_contrast_bound")
        extra = s.diag(*(R(1, i + 1) for i in range(p)))
        sandwich(target + extra, representative + extra, eta, "additional_prior")
        congruence = s.Matrix([[(-1)**(i + j) * (i + j + 1) for j in range(p)]
                               for i in range(p + 1)])
        sandwich(congruence * target * congruence.T,
                 congruence * representative * congruence.T, eta, "common_congruence")
    check(max(infos[b].det() for b in output) >=
          (1 - eta)**p * max(v.det() for v in infos.values()), "D_criterion")
    all_pd = [v for v in infos.values() if v.det() > 0]
    out_pd = [infos[b] for b in output if infos[b].det() > 0]
    check(bool(all_pd) == bool(out_pd), "positive_definite_detection")
    if all_pd:
        check(min(s.trace(v.inv()) for v in out_pd) <=
              min(s.trace(v.inv()) for v in all_pd) / (1 - eta), "A_criterion")
    best_e = max(minimum_eigenvalue(v) for v in infos.values())
    out_e = max(minimum_eigenvalue(infos[b]) for b in output)
    check(bool(out_e >= (1 - eta) * best_e), "E_criterion")
    for epsilon in [R(1, 10), R(2, 3)]:
        check((1 - epsilon / p)**p >= 1 - epsilon, "D_accuracy_constants")
        check(1 / (1 - epsilon / (1 + epsilon)) == 1 + epsilon, "A_accuracy_constants")
    return {"name": name, "matrix_dimension": p, "matroid_rank": q,
            "elements": raw_a.cols, "bases": len(original_bases), "output_bases": len(output),
            "information_ranks": sorted({v.rank() for v in infos.values()}),
            "checks": dict(sorted((STATS - before).items()))}


def interpolated_coefficients(a, weights, degree):
    """Numerical determinant evaluations and independent tensor Vandermonde inversion."""
    dimensions = len(weights[0])
    indices = list(product(range(degree + 1), repeat=dimensions))
    tensor = {}
    for index in indices:
        point = tuple(i + 1 for i in index)
        values = [s.prod(point[j]**weight[j] for j in range(dimensions)) for weight in weights]
        tensor[index] = (a * s.diag(*values) * a.T).det()
    inverse = s.Matrix([[s.Integer(i + 1)**j for j in range(degree + 1)]
                        for i in range(degree + 1)]).inv()
    for axis in range(dimensions):
        updated = {}
        for index in indices:
            updated[index] = sum(inverse[index[axis], t] *
                                 tensor[index[:axis] + (t,) + index[axis + 1:]]
                                 for t in range(degree + 1))
        tensor = updated
    STATS["interpolation_determinant_evaluations"] += len(indices)
    return {key: value for key, value in tensor.items() if value}


def auxiliary_checks():
    # Nontrivial three-variable collision: both bases {0,2} and {1,2}
    # have the same profile, but their minor squares are respectively 1 and 4.
    a = s.Matrix([[1, 2, 0, 1], [0, 0, 1, 1]])
    weights = [(0, 1, 0), (0, 1, 0), (1, 0, 1), (1, 1, 0)]
    direct = polynomial_det(a, weights)
    check(direct == minor_coefficients(a, weights), "auxiliary_support_identity")
    check(direct[(1, 1, 1)] == 5, "positive_collision_addition")
    interpolated = interpolated_coefficients(a, weights, 2)
    check(interpolated == direct, "exact_tensor_interpolation")
    # Deliberately lose a row direction. Retaining the fixed two rows gives zero.
    deficient = a[:, :2]
    check(interpolated_coefficients(deficient, weights[:2], 2) == {},
          "rank_deficient_interpolation_zero")
    check(bool(polynomial_det(deficient[:1, :], weights[:2])),
          "row_rank_recomputation_is_wrong_witness")
    for key in direct:
        recovered = recover(a, weights, key)
        check(set(recovered) in [set(b) for b in bases(a)], "auxiliary_recovery")
    # A positive characteristic-zero support coefficient can vanish modulo a prime.
    check(5 % 5 == 0, "modular_false_zero_witness")
    c1, c2 = s.Matrix([[1, 1]]), s.Matrix([[1, -1]])
    check((c1 * c2.T).det() == 0 and bases(c1) == bases(c2) == [(0,), (1,)],
          "mixed_determinant_cancellation_witness")
    ff = s.Matrix([[1, 1, 0], [1, 0, 1], [0, 1, 1]])
    check(ff.det() == -2 and ff.det() % 2 == 0, "finite_field_lift_witness")
    # The exact two-sided kernel restriction fails for distinct nearly equal ranges.
    v, w = s.Matrix([1, 0]), s.Matrix([1, R(1, 2**80)])
    check(not psd(w * w.T - R(1, 2) * v * v.T)
          and not psd(v * v.T - R(1, 2) * w * w.T), "distinct_singular_range_witness")


def fixtures():
    z2 = s.zeros(2)
    e1, e2 = s.Matrix([1, 0]), s.Matrix([0, 1])
    def outer(v, weight=1):
        return weight * v * v.T
    # Parallel pairs and a loop: dependences are not a cardinality constraint.
    yield ("parallel_owners_signed_collisions", s.Matrix([[1, 2, 0, 0, 0], [0, 0, 1, 3, 0]]),
           [outer(s.Matrix([1, -1]), R(1, 100)), outer(s.Matrix([1, -1]), R(1, 110)),
            outer(s.Matrix([2, 1]), R(1, 200)), outer(s.Matrix([2, 1]), R(1, 210)), s.eye(2)],
           s.eye(2))
    yield ("range_filter_original_rank_loss", s.eye(2), [outer(e1), outer(e2)], z2)
    yield ("magnitude_filter_rank_loss", s.eye(2), [outer(e1), outer(e1, 2**100)], z2)
    yield ("zero_information_filter_rank_loss", s.eye(2), [z2, s.eye(2)], z2)
    yield ("same_owner_two_factors", s.Matrix([[1, 2, 3]]),
           [s.eye(2), s.diag(2, 3), s.Matrix([[2, -1], [-1, 2]])], z2)
    yield ("mixed_zero_and_singular_ranges", s.Matrix([[1, 2, 3, 4]]),
           [z2, outer(e1), outer(s.Matrix([1, R(1, 2**80)])), s.eye(2)], z2)
    # A graphic representation of a triangle with a parallel edge and a loop.
    yield ("graphic_triangle_parallel_edge_loop", s.Matrix([[1, 0, 1, 2, 0], [0, 1, -1, 0, 0]]),
           [outer(e1), outer(e2), outer(s.Matrix([1, -1])), outer(e1, R(101, 100)), z2], z2)
    # Rational contraction requires denominator clearing; an extra row is redundant.
    yield ("rational_representation_and_contraction", s.Matrix([
        [R(1, 2), 0, R(1, 3), R(2, 7)], [0, R(2, 3), R(1, 5), R(1, 11)],
        [1, R(2, 3), R(13, 15), R(51, 77)]]),
        [outer(e1), outer(e2), outer(s.Matrix([1, 1])), outer(s.Matrix([1, 1]), R(101, 100))], z2)
    # q=4 while p=1: the information dimension does not bound matroid rank.
    yield ("variable_matroid_rank", s.Matrix([[1, 0, 0, 0, 1, 2], [0, 1, 0, 0, 1, 3],
                                             [0, 0, 1, 0, 1, 4], [0, 0, 0, 1, 1, 5]]),
           [s.Matrix([[R(100 + i, 100)]]) for i in range(6)], s.Matrix([[1]]))
    yield ("variable_rank_multiple_profiles", s.Matrix([[1, 0, 0, 0, 1, 2], [0, 1, 0, 0, 1, 3],
                                                       [0, 0, 1, 0, 1, 4], [0, 0, 0, 1, 1, 5]]),
           [s.Matrix([[1 + R(i, 2)]]) for i in range(6)], s.Matrix([[1]]))
    yield ("rank_three_mixed_information_ranks", s.Matrix([
        [1, 0, 0, 1, 0, 1], [0, 1, 0, 1, 1, 1], [0, 0, 1, 0, 1, 2]]),
        [outer(e1), outer(e1, R(3, 2)), outer(e1, 2), outer(e2),
         outer(e2, R(5, 3)), outer(s.Matrix([1, -1]), R(2, 3))], z2)
    u, v = s.Matrix([1, 1, 0]), s.Matrix([0, 1, R(1, 2**60)])
    yield ("proper_oblique_singular_range", s.Matrix([[1, 0, 1], [0, 1, 1]]),
           [outer(u), outer(v), outer(u - v, R(1, 100))], s.zeros(3))
    yield ("rank_zero_matroid_nonzero_prior", s.zeros(2, 3), [s.eye(2), z2, outer(e1)], s.eye(2))
    yield ("empty_ground_set", s.zeros(2, 0), [], z2)
    yield ("all_zero_information", s.Matrix([[1, 0, 1], [0, 1, 1]]), [z2, z2, z2], z2)


def main():
    cases = []
    for case in fixtures():
        result = review_case(*case)
        cases.append(result)
        print(json.dumps({key: result[key] for key in
                          ["name", "matroid_rank", "bases", "output_bases"]}), flush=True)
    auxiliary_checks()
    required = ["restriction_rank_loss_rejections", "fixed_row_rank_drop_rejections",
                "dependent_forced_owner_rejections", "repeated_factor_owner_trials",
                "rank_zero_contraction_trials", "nontrivial_contraction_denominators",
                "actual_profile_collisions", "collisions_between_different_information_matrices",
                "negative_rounded_coordinates", "nonempty_forced_owner_crosschecks",
                "zero_information_rank_loss_rejections", "magnitude_deleted_elements",
                "matroid_rank_above_information_dimension", "exact_tensor_interpolation",
                "trials_with_multiple_profiles"]
    for key in required:
        check(STATS[key] > 0, "required_boundary_" + key)
    result = {"status": "all exact checks passed", "implementation": "independent, exhaustive tiny verifier",
              "cases": cases, "totals": dict(sorted(STATS.items())),
              "source": str(Path(__file__).relative_to(Path(__file__).parents[2]))}
    destination = Path(__file__).with_name("results") / "represented-matroid-psd-independent-review.json"
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "totals": result["totals"]}), flush=True)


if __name__ == "__main__":
    main()
