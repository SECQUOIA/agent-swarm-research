"""Bounded integration review of the optional refined residual-pair mode.

Uses earlier independent dense references and the accepted interval component.
Small designs are exhaustively priced. Large artifacts replay the accepted
integer implementation; the earlier all-arc exact component review is reused.
"""

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from time import perf_counter

import certify_spacing_design as certifier
from integer_interval_scores import IntegerIntervalScores
from noisy_markov_spacing_bound import spacing_bound
from review_certify_spacing_design import (Reference, determinant, inverse,
                                          make_record, trace_product)
from review_noisy_markov_exact import independent_log
from review_noisy_markov_pair_refinements import (enumerated_row_bound, is_psd,
                                                 local_floor, phi_values)
from review_noisy_markov_spacing import (DenseReference, enumerated_pair_majorants,
                                        separated_sets)


HERE = Path(__file__).resolve().parent


def canonical(value):
    return json.loads(json.dumps(value, default=str))


def expected_bound(n, L, gap, rho, P, r, refined):
    L = min(L, n-1)
    floor = local_floor(P, r, abs(rho), L, gap)
    if not rho or not P or L >= n-1 or gap >= n:
        return Q(0), floor, Q(0)
    phi = (phi_values(n, L, gap, abs(rho), P, r, True) if refined else
           enumerated_pair_majorants(n, L, gap, rho, P, r))
    row = enumerated_row_bound(phi, gap)
    return row/floor, floor, row


def helper_checks(counts):
    for n in (1, 3, 5):
        for gap in (1, 2, 6):
            for L in sorted({0, 1, 3, n+2}):
                for rho, P, r in ((Q(-2, 3), Q(1), Q(1)),
                                   (Q(3, 4), Q(2), Q(1, 3)),
                                   (Q(0), Q(1), Q(2)),
                                   (Q(1, 2), Q(0), Q(1))):
                    default = spacing_bound(n, L, gap, rho, P, r)
                    assert default == spacing_bound(n, L, gap, rho, P, r, refined_pairs=False)
                    reference = DenseReference(n, rho, P, r)
                    for refined in (False, True):
                        actual = spacing_bound(n, L, gap, rho, P, r, refined_pairs=refined)
                        delta, floor, row = expected_bound(n, L, gap, rho, P, r, refined)
                        assert (actual["delta"], actual["innovation_floor"], actual["row_majorant"]) == (delta, floor, row)
                        assert actual["delta"] <= default["delta"]
                        counts["helper_formula_comparisons"] += 1
                        if refined:
                            for selected in separated_sets(n, gap):
                                covariance, variances = reference.residual_covariance(selected, L)
                                assert all(d >= floor for d in variances)
                                for sign in (-1, 1):
                                    matrix = [[(delta*variances[i] if i == j else 0)
                                              +sign*(covariance[i][j]-(variances[i] if i == j else 0))
                                               for j in range(len(selected))] for i in range(len(selected))]
                                    assert is_psd(matrix)
                                    counts["exact_spectral_matrices"] += 1


def expected_reference(record, hull, delta, grid):
    prior = tuple(tuple(Q(v) for v in row) for row in record["prior"])
    M = tuple(tuple(Q(v) for v in row) for row in hull["hull_information"])
    def nearest(value):
        numerator = value*grid+Q(1, 2)
        return Q(numerator.numerator//numerator.denominator, grid)
    return tuple(tuple(nearest(prior[i][j]+((M[i][j]+M[j][i])/2-prior[i][j])/(1-delta))
                       for j in range(len(prior))) for i in range(len(prior)))


def check_certificate(record, hull, refined, integer_grid, counts):
    result = certifier.certify(record, hull, refined_pairs=refined,
                              integer_grid=integer_grid, score_grid=101, reference_grid=10**5)
    n, k, gap, L = result["n"], result["k"], result["minimum_gap"], result["L"]
    delta = expected_bound(n, L, gap, record["rho"], record["latent_variance"],
                           record["nugget_variance"], refined)[0]
    assert result["delta"] == delta
    N = expected_reference(record, hull, delta, result["reference_grid"])
    assert result["tangent_reference"] == N
    inv_N = inverse(N)
    H = tuple(tuple(v/(1-delta) for v in row) for row in inv_N)
    reference = Reference(record)
    feasible = [s for s in separated_sets(n, gap) if len(s) == k]
    scorer = None if integer_grid is None else IntegerIntervalScores(
        reference.F, H, coefficient_grid=integer_grid, score_grid=result["score_grid"])
    prices = {}
    for selected in feasible:
        exact_rounded, exact_unrounded = reference.price(selected, L, H, result["score_grid"])
        if scorer is None:
            price = exact_rounded
        else:
            price = 0
            for i, t in enumerate(selected):
                ages = tuple(t-j for j in selected[:i] if t-j <= L)
                coefficients, variance = reference.conditional(ages)
                price += scorer.upper(t, scorer.prepare(ages, coefficients, variance))
            assert price >= exact_rounded
        prices[selected] = price
        assert result["upper_bound"] >= independent_log(determinant(reference.true(selected)))[1]
        counts["enumerated_design_bounds_and_prices"] += 1
    assert result["integer_price"] == max(prices.values())
    assert prices[result["priced_selection"]] == result["integer_price"]
    constant = -result["p"]+trace_product(inv_N, reference.prior)+Q(result["integer_price"], result["score_grid"])
    assert result["upper_bound"] >= independent_log(determinant(N))[1]+constant
    assert result["lower_bound"] <= independent_log(determinant(reference.true(result["selected"])))[0]
    assert result["gap"] == result["upper_bound"]-result["lower_bound"]
    assert result["pair_majorant"] == ("fresh-filter refinement" if refined else "original triangle bound")
    if not refined:
        implicit = certifier.certify(record, hull, integer_grid=integer_grid,
                                     score_grid=101, reference_grid=10**5)
        assert {k:v for k,v in implicit.items() if k != "wall_seconds"} == {
            k:v for k,v in result.items() if k != "wall_seconds"}
        counts["implicit_default_equalities"] += 1
    counts["small_certificates"] += 1
    return result


def small_certificates(counts):
    cases = [(1, 0, 2, Q(-2, 3), Q(1), Q(1)),
             (5, 2, 1, Q(1, 2), Q(1), Q(1)),
             (6, 0, 3, Q(-1, 2), Q(1), Q(2)),
             (6, 3, 2, Q(-2, 3), Q(1), Q(1)),
             (5, 8, 1, Q(9, 10), Q(1), Q(1, 3)),
             (5, 2, 2, Q(3, 4), Q(0), Q(1)),
             (5, 1, 7, Q(1, 2), Q(1), Q(1))]
    for n, L, gap, rho, P, r in cases:
        for k in sorted({0, min(2, (n+gap-1)//gap)}):
            record = make_record(n, 2, k, gap, rho, P, r)
            selected = next(s for s in separated_sets(n, gap) if len(s) == k)
            M = Reference(record).true(selected)
            # An antisymmetric source tests the unchanged symmetrization path.
            M = ((M[0][0], M[0][1]+Q(1, 7)), (M[1][0]-Q(1, 7), M[1][1]))
            hull = {"L": L, "selected": selected, "hull_information": M}
            for refined in (False, True):
                for integer_grid in (None, 37, 10**12):
                    check_certificate(record, hull, refined, integer_grid, counts)
    record = make_record(5, 2, 2, 1, Q(3, 4), Q(1), Q(1))
    hull = {"L": 1, "selected": (0, 3), "hull_information": Reference(record).true((0, 3))}
    try:
        certifier.certify(record, hull)
    except ValueError as error:
        assert "no positive relative lower bound" in str(error)
        counts["old_bound_rejection_new_acceptance"] += 1
    else:
        raise AssertionError("Expected old delta >= 1")
    check_certificate(record, hull, True, 10**12, counts)


def flag_and_cli_checks(counts):
    record = make_record(4, 2, 2, 1, Q(1, 4), Q(1), Q(2))
    hull = {"L": 1, "selected": (0, 3), "hull_information": Reference(record).true((0, 3))}
    for invalid in (None, 0, 1, -1, "false", "true", [], {}, Q(1)):
        for call in (lambda: spacing_bound(1, 4, 2, Q(0), Q(0), Q(1), refined_pairs=invalid),
                     lambda: certifier.certify(record, hull, refined_pairs=invalid)):
            try:
                call()
            except TypeError:
                counts["nonboolean_rejections"] += 1
            else:
                raise AssertionError("A nonboolean mode was accepted")
    with TemporaryDirectory(prefix="refined-spacing-review-") as temporary:
        directory = Path(temporary)
        input_path, output_path = directory/"input.json", directory/"output.json"
        data = {"F": [[.1, -.3], [.7, .2], [-.9, .4], [.6, -.8]],
                "prior": [[1., 0], [0, 1.]], "rho": -.25,
                "latent_variance": 1., "nugget_variance": 2., "k": 2, "minimum_gap": 1,
                "hulls": [{}, {"L": 1, "selected": [0, 3], "hull_information": [[2., .1], [.1, 2.]]}]}
        input_path.write_text(json.dumps({"results": [{}, data]}))
        records = []
        for refined in (False, True):
            command = [sys.executable, str(HERE/"certify_spacing_design.py"), str(input_path), str(output_path),
                       "--case", "1", "--hull", "1", "--integer-grid", "1000000000000"]
            if refined:
                command.append("--refined-pairs")
            subprocess.run(command, check=True, capture_output=True, text=True)
            artifact = json.loads(output_path.read_text())
            expected = spacing_bound(4, 1, 1, Q(-1, 4), Q(1), Q(2), refined_pairs=refined)
            assert Q(artifact["delta"]) == expected["delta"]
            assert artifact["pair_majorant"] == ("fresh-filter refinement" if refined else "original triangle bound")
            assert artifact["input_case_index"] == artifact["input_hull_index"] == 1
            assert artifact["input_sha256"] == sha256(input_path.read_bytes()).hexdigest()
            assert artifact["source_sha256"] == sha256((HERE/"certify_spacing_design.py").read_bytes()).hexdigest()
            assert Q(artifact["problem_data"]["F"][0][0]) == Q(1, 10)
            assert artifact["integer_coefficient_grid"] == 10**12
            records.append(artifact)
            counts["cli_modes"] += 1
        assert Q(records[1]["delta"]) < Q(records[0]["delta"])


def large_artifacts(counts):
    names = ("noisy-markov-spacing-kinetics-integer-certificate.json",
             "noisy-markov-spacing-kinetics-refined-certificate.json")
    reports = []
    for refined, name in zip((False, True), names):
        path = HERE/"results"/name
        saved = json.loads(path.read_text())
        input_path = HERE.parents[1]/saved["input_file"]
        assert sha256(input_path.read_bytes()).hexdigest() == saved["input_sha256"]
        record = json.loads(input_path.read_text(), parse_float=str)["results"][saved["input_case_index"]]
        hull = record["hulls"][saved["input_hull_index"]]
        regenerated = canonical(certifier.certify(record, hull, integer_grid=saved["integer_coefficient_grid"],
                                                  refined_pairs=refined))
        for key, value in regenerated.items():
            if key in saved and key != "wall_seconds":
                assert value == saved[key], key
        delta = spacing_bound(saved["n"], saved["L"], saved["minimum_gap"],
                              record["rho"], record["latent_variance"], record["nugget_variance"],
                              refined_pairs=refined)["delta"]
        N = expected_reference(record, hull, delta, saved["reference_grid"])
        assert canonical(N) == saved["tangent_reference"]
        assert Q(saved["delta"]) == delta
        assert saved["integer_scorer_sha256"] == sha256((HERE/"integer_interval_scores.py").read_bytes()).hexdigest()
        if refined:
            assert saved["source_sha256"] == sha256((HERE/"certify_spacing_design.py").read_bytes()).hexdigest()
            assert saved["pair_majorant"] == "fresh-filter refinement"
        inv_N = inverse(N)
        constant = -saved["p"]+trace_product(inv_N, tuple(tuple(Q(v) for v in row) for row in record["prior"]))
        constant += Q(saved["integer_price"], saved["score_grid"])
        assert Q(saved["upper_bound"]) >= independent_log(determinant(N))[1]+constant
        assert Q(saved["gap"]) == Q(saved["upper_bound"])-Q(saved["lower_bound"])
        reports.append({"artifact": name, "sha256": sha256(path.read_bytes()).hexdigest(),
                        "delta": float(delta), "integer_price": saved["integer_price"],
                        "display_gap": saved["display_gap"],
                        "regenerated_wall_seconds": regenerated["wall_seconds"]})
        counts["large_integer_artifact_replays"] += 1
    original = json.loads((HERE/"results"/"noisy-markov-spacing-kinetics-certificate.json").read_text())
    refined = json.loads((HERE/"results"/names[1]).read_text())
    assert original["problem_data"] == refined["problem_data"]
    assert original["selected"] == refined["selected"]
    assert original["lower_bound"] == refined["lower_bound"]
    assert Q(refined["upper_bound"]) < Q(original["upper_bound"])
    accepted = json.loads((HERE/"results"/"integer-interval-scores-independent-review.json").read_text())
    assert accepted["component_sha256"] == refined["integer_scorer_sha256"]
    assert accepted["saved_n96_case"]["all_arcs_verified"] == 31900
    return reports


def main():
    start = perf_counter()
    counts = dict.fromkeys(("helper_formula_comparisons", "exact_spectral_matrices", "enumerated_design_bounds_and_prices",
                           "implicit_default_equalities", "small_certificates", "old_bound_rejection_new_acceptance",
                           "nonboolean_rejections", "cli_modes", "large_integer_artifact_replays"), 0)
    helper_checks(counts)
    small_certificates(counts)
    flag_and_cli_checks(counts)
    artifacts = large_artifacts(counts)
    report = {"status": "passed", "counts": counts, "large_artifacts": artifacts,
              "source_hashes": {name: sha256((HERE/name).read_bytes()).hexdigest() for name in
                                ("noisy_markov_spacing_bound.py", "certify_spacing_design.py", "integer_interval_scores.py",
                                 "review_refined_spacing_integration.py")},
              "wall_seconds": perf_counter()-start,
              "scope": "Optional refined-pair integration. Reuses accepted pricing/logarithm/component proof and independent all-arc review; does not repeat the large exact-rational all-arc run."}
    (HERE/"results"/"refined-spacing-integration-independent-review.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
