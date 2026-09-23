"""Independent exact integration review of latent-separator certificates.

The oracle constructs dense rational conditional covariances and inverses. It
does not call the producer's conditional-variance, quadratic, information, or
logarithm helpers to compute expected results. Large incumbent information is
checked by a separate tridiagonal latent-precision solve.
"""

import argparse
from copy import deepcopy
from fractions import Fraction as Q
from functools import lru_cache
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
from time import perf_counter

import sympy as sp

import certify_latent_separator as producer
from integer_interval_scores import IntegerIntervalScores


HERE = Path(__file__).resolve().parent
COUNTS = {}


def checked(name, condition=True):
    assert condition, name
    COUNTS[name] = COUNTS.get(name, 0) + 1


def rational(value):
    if isinstance(value, sp.Rational):
        return Q(int(value.p), int(value.q))
    return Q(value)


def mat(rows):
    return sp.Matrix([[sp.Rational(rational(x).numerator, rational(x).denominator)
                       for x in row] for row in rows])


def rows(matrix):
    return tuple(tuple(rational(x) for x in matrix.row(i)) for i in range(matrix.rows))


@lru_cache(None)
def independent_log(value):
    """An atanh-series enclosure using dyadic mantissa endpoints."""
    value = rational(value)
    assert value > 0
    exponent = value.numerator.bit_length() - value.denominator.bit_length()
    scale = Q(2) ** exponent
    while value < scale:
        exponent -= 1
        scale /= 2
    while value >= 2 * scale:
        exponent += 1
        scale *= 2
    mantissa = value / scale
    grid = 2 ** 96
    scaled = mantissa * grid
    floor = scaled.numerator // scaled.denominator
    ceiling = -((-scaled.numerator) // scaled.denominator)

    def series(x):
        z = (x - 1) / (x + 1)
        low = sum((2 * z ** (2 * j + 1) / (2 * j + 1) for j in range(32)), Q(0))
        return low, low + 2 * z ** 65 / (65 * (1 - z * z))

    a, b = series(Q(floor, grid))[0], series(Q(ceiling, grid))[1]
    c, d = series(Q(2))
    return (a + exponent * (c if exponent >= 0 else d),
            b + exponent * (d if exponent >= 0 else c))


def principal(matrix, indices):
    return matrix.extract(indices, indices)


def dense_information(F, prior, covariance, selected):
    if not selected:
        return prior
    FS = F.extract(selected, range(F.cols))
    return prior + FS.T * principal(covariance, selected).inv() * FS


def independent_selected_information(record, selected):
    """Solve selected latent precision plus diagonal observation precision.

    The exact Thomas solve is independent of the producer's Kalman information
    recursion and avoids a large dense rational inverse for the saved cases.
    """
    F, J = mat(record["F"]), mat(record["prior"])
    rho, latent, nugget = [rational(record[key]) for key in
                           ("rho", "latent_variance", "nugget_variance")]
    selected = sorted(selected)
    m, p = len(selected), F.cols
    if not m:
        return J
    FS = [[rational(F[t, j]) for j in range(p)] for t in selected]
    if not latent or not rho:
        X = mat(FS)
        return J + X.T * X / (latent + nugget)
    diagonal = [Q(0)] * m
    off = [Q(0)] * (m - 1)
    diagonal[0] = 1 / latent
    for t in range(1, m):
        a = rho ** (selected[t] - selected[t - 1])
        precision = 1 / (latent * (1 - a * a))
        diagonal[t] += precision
        diagonal[t - 1] += a * a * precision
        off[t - 1] = -a * precision
    diagonal = [x + 1 / nugget for x in diagonal]
    rhs = [list(row) for row in FS]
    for t in range(1, m):
        factor = off[t - 1] / diagonal[t - 1]
        diagonal[t] -= factor * off[t - 1]
        rhs[t] = [x - factor * y for x, y in zip(rhs[t], rhs[t - 1])]
    solution = [[Q(0)] * p for _ in range(m)]
    for t in range(m - 1, -1, -1):
        solution[t] = [(rhs[t][j] - (off[t] * solution[t + 1][j] if t + 1 < m else 0))
                       / diagonal[t] for j in range(p)]
    X, Y = mat(FS), mat(solution)
    return J + X.T * X / nugget - X.T * Y / (nugget * nugget)


class CapturePatterns:
    def prepare(self, ages, coefficients, variance):
        return ages, coefficients, variance


def fixture(n, p, b, rho, latent):
    prior = sp.eye(p) / 3 + sp.ones(p) / 17
    source = sp.eye(p) * 3 + sp.ones(p) / 7
    # An asymmetric source tests the deliberate averaging before rounding.
    if p > 1:
        source[0, 1] += sp.Rational(3, 5)
        source[1, 0] -= sp.Rational(3, 5)
    F = [[Q(((t + 2) * (j + 3) + t * t) % 13 - 6, 7 + j)
          for j in range(p)] for t in range(n)]
    effective_b = min(n, b)
    anchor_count = (n - 1) // effective_b if rho and latent else 0
    G = [[Q(((a + 1) * (j + 2)) % 7 - 3, 9 + j)
          for j in range(p)] for a in range(anchor_count)]
    return ({"F": F, "prior": rows(prior), "k": n // 2, "rho": rho,
             "latent_variance": latent, "nugget_variance": Q(2, 5)},
            {"block_size": b, "selected": list(range(n // 2)),
             "best_tangent_witness": {"schur_information": rows(source),
                                      "nuisance_minimizer": G}})


def check_tiny(record, proposal, grids):
    n, p = len(record["F"]), len(record["prior"])
    rho, latent, nugget = [rational(record[key]) for key in
                           ("rho", "latent_variance", "nugget_variance")]
    F, prior = mat(record["F"]), mat(record["prior"])
    K = sp.Matrix(n, n, lambda i, j: latent * rho ** abs(i - j))
    R = K + nugget * sp.eye(n)
    first = producer.certify(record, proposal, **grids)
    anchors, blocks = list(first["anchors"]), first["blocks"]
    N = mat(first["tangent_reference"])
    W = N.inv()
    source = mat(proposal["best_tangent_witness"]["schur_information"])
    symmetric = (source + source.T) / 2
    checked("rounded_reference_distance", all(abs(N[i, j] - symmetric[i, j])
            <= sp.Rational(1, 2 * grids["reference_grid"]) for i in range(p) for j in range(p)))
    if anchors:
        KA = principal(K, anchors)
        H = K.extract(range(n), anchors) * KA.inv()
        G = mat(first["nuisance_witness"])
        D = R - H * KA * H.T
        adjusted = F + H * G
        anchor_trace = sp.trace(W * G.T * KA.inv() * G)
    else:
        H, G = sp.zeros(n, 0), sp.zeros(0, p)
        D, adjusted, anchor_trace = R, F, sp.Rational(0)
    checked("prior_trace", rational(sp.trace(W * prior)) == first["prior_trace"])
    checked("anchor_precision_trace", rational(anchor_trace) == first["anchor_prior_trace"])
    checked("conditional_block_diagonal", all(D[i, j] == 0 for a, block in enumerate(blocks)
            for other in blocks[a + 1:] for i in block for j in other))
    scorer = IntegerIntervalScores(rows(adjusted), rows(W), **{key: grids[key]
                                   for key in ("coefficient_grid", "feature_grid", "score_grid")})
    integer_scores, exact_scores = [], []
    for index, block in enumerate(blocks):
        length, origin = len(block), block[0]
        left = -1 if anchors and index else None
        right = length - 1 if anchors and index < len(anchors) else None
        prepared = producer.bridge_patterns(length, left, right, rho, latent, nugget, CapturePatterns())
        checked("bridge_pattern_count", len(prepared) == 2 ** length - 1)
        seen, integers, exact = set(), {0: 0}, {0: Q(0)}
        for previous, mask, local_t, (ages, coefficients, variance) in prepared:
            t = origin + local_t
            history = [t - age for age in ages]
            checked("pattern_structure", mask not in seen and previous in integers
                    and mask == previous | (1 << local_t)
                    and history == [origin + j for j in range(length) if previous & (1 << j)])
            seen.add(mask)
            if history:
                expected = D.extract([t], history) * principal(D, history).inv()
                expected_variance = D[t, t] - (expected * D.extract(history, [t]))[0, 0]
            else:
                expected, expected_variance = sp.zeros(1, 0), D[t, t]
            checked("exact_bridge_coefficients", tuple(rational(x) for x in expected) == coefficients)
            checked("exact_bridge_variance", rational(expected_variance) == variance)
            residual = adjusted.row(t)
            if history:
                residual -= expected * adjusted.extract(history, range(p))
            arc = rational((residual * W * residual.T)[0, 0] / expected_variance)
            integer_arc = scorer.upper(t, scorer.prepare(ages, coefficients, variance))
            checked("outward_arc_integration", Q(integer_arc, grids["score_grid"]) >= arc)
            integers[mask] = integers[previous] + integer_arc
            exact[mask] = exact[previous] + arc
            indices = [origin + j for j in range(length) if mask & (1 << j)]
            X = adjusted.extract(indices, range(p))
            direct = rational(sp.trace(W * X.T * principal(D, indices).inv() * X))
            checked("all_pattern_scores_dense_inverse", direct == exact[mask])
        integer_scores.append(integers)
        exact_scores.append(exact)
    count_best = {k: (-1, ()) for k in range(n + 1)}
    all_info = {}
    for size in range(n + 1):
        for selected in combinations(range(n), size):
            masks = tuple(sum(1 << j for j, t in enumerate(block) if t in selected) for block in blocks)
            candidate = sum(scores[mask] for scores, mask in zip(integer_scores, masks)), masks
            count_best[size] = max(count_best[size], candidate)
            J = dense_information(F, prior, R, selected)
            checked("independent_precision_information", J == independent_selected_information(record, selected))
            true_trace = rational(sp.trace(W * J))
            separated = rational(sp.trace(W * prior) + anchor_trace) + sum(
                scores[mask] for scores, mask in zip(exact_scores, masks))
            checked("arbitrary_G_majorization", separated >= true_trace)
            all_info[selected] = J
    for k in sorted(set((0, n // 2, n))):
        case, witness = deepcopy(record), deepcopy(proposal)
        case["k"], witness["selected"] = k, list(reversed(range(k)))
        result = producer.certify(case, witness, **grids)
        checked("global_count_exhaustive_price", (result["integer_price"], result["priced_block_masks"])
                == count_best[k])
        checked("priced_selection_cardinality", len(result["priced_selection"]) == k
                and len(set(result["priced_selection"])) == k)
        for block, scores, local in zip(blocks, integer_scores, result["local_count_choices"]):
            checked("local_count_keys", set(local) == {str(c) for c in range(min(len(block), k) + 1)})
            for count, entry in local.items():
                expected = max((score, mask) for mask, score in scores.items() if mask.bit_count() == int(count))
                checked("local_count_exhaustive_price", expected == (entry["integer_score"], entry["mask"]))
        lo_ref, hi_ref = independent_log(rational(N.det()))
        checked("reference_log_upper", result["logdet_reference_upper"] >= hi_ref)
        exact_fixed = rational(sp.trace(W * prior) + anchor_trace) - p
        support_upper = hi_ref + exact_fixed + Q(count_best[k][0], grids["score_grid"])
        checked("global_tangent_log_upper", result["upper_bound"] >= support_upper)
        incumbent = tuple(range(k))
        checked("incumbent_sorted", result["selected"] == incumbent)
        checked("incumbent_log_lower", result["lower_bound"] <= independent_log(rational(all_info[incumbent].det()))[0])
        for selected, J in all_info.items():
            if len(selected) == k:
                checked("exhaustive_true_log_upper", result["upper_bound"] >= independent_log(rational(J.det()))[1])
        checked("gap_identity", result["gap"] == result["upper_bound"] - result["lower_bound"])
        saved = json.loads(json.dumps(result, default=str))
        replay = producer.certify(saved["problem_data"], {
            "block_size": saved["block_size"], "selected": saved["selected"],
            "best_tangent_witness": {"schur_information": saved["tangent_reference"],
                                     "nuisance_minimizer": saved["nuisance_witness"]}}, **grids)
        checked("tiny_serialization_replay", canonical(result) == canonical(replay))


def canonical(value):
    ignored = {"wall_seconds", "input_file", "input_case_index", "input_sha256",
               "source_sha256", "dependency_sha256", "incumbent_source",
               "incumbent_source_sha256"}
    return json.loads(json.dumps({k: v for k, v in value.items() if k not in ignored}, default=str))


def malformed_checks():
    record, proposal = fixture(5, 2, 2, Q(-1, 2), Q(3, 4))
    cases = []
    for name in ("reference_grid", "coefficient_grid", "feature_grid", "score_grid", "log_grid", "max_patterns"):
        for value in (0, -1, True, 1.5, "10"):
            cases.append(("invalid_" + name, record, proposal, {name: value}))
    for key, values in {"k": [-1, 6, True, "2", 1.5], "rho": [1, -1, "nan", "inf", 0.2, True],
                        "latent_variance": [-1, True], "nugget_variance": [0, -1, True],
                        "F": [[], [[]], [[1, 2], [3]], [[1]], [[True, 2]]],
                        "prior": [[], [[0, 0], [0, 1]], [[1, 1], [0, 1]], [[1, 2]], [[1]]]}.items():
        for value in values:
            bad = deepcopy(record)
            bad[key] = value
            cases.append(("invalid_record_" + key, bad, proposal, {}))
    for key, values in {"block_size": [0, -1, True, "2", 1.5],
                        "selected": [[0], [0, 0], [0, 5], [True, 2], [0, "2"], [[0], 1]]}.items():
        for value in values:
            bad = deepcopy(proposal)
            bad[key] = value
            cases.append(("invalid_proposal_" + key, record, bad, {}))
    for key, values in {"schur_information": [[], [[1]], [[0, 0], [0, 0]], [[1, 2], [2, 1]], [[True, 0], [0, 1]]],
                        "nuisance_minimizer": [[], [[0, 0]], [[0], [0]], [[0, 0], [0, True]]]}.items():
        for value in values:
            bad = deepcopy(proposal)
            bad["best_tangent_witness"][key] = value
            cases.append(("invalid_witness_" + key, record, bad, {}))
    cases.append(("variance_floor_rejection", record, proposal, {"coefficient_grid": 1}))
    cases.append(("pattern_total_cap_rejection", record, proposal, {"max_patterns": 9}))
    for name, case, witness, grids in cases:
        try:
            producer.certify(case, witness, **grids)
        except (ValueError, TypeError, MemoryError, ZeroDivisionError):
            checked(name)
        else:
            raise AssertionError("Malformed input accepted: " + name)
    # The preflight must reject an enormous exponent before forming 2**b.
    bad = deepcopy(proposal)
    bad["block_size"] = 10 ** 100
    result = producer.certify(record, {**bad, "best_tangent_witness": {
        **bad["best_tangent_witness"], "nuisance_minimizer": []}}, max_patterns=32)
    checked("oversized_block_clamps_to_n", result["block_size"] == 5 and result["pattern_count"] == 32)
    try:
        producer.certify(record, proposal, max_patterns=3)
    except MemoryError:
        checked("pattern_exponent_cap_rejection")
    else:
        raise AssertionError("Pattern exponent cap not enforced")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay_saved(path, benchmark):
    saved = json.loads(path.read_text(), parse_float=str)
    source = HERE / saved["input_file"]
    checked("saved_input_hash", saved["input_sha256"] == digest(source))
    checked("saved_certifier_hash", saved["source_sha256"] == digest(HERE / "certify_latent_separator.py"))
    if "incumbent_source_sha256" in saved:
        checked("saved_incumbent_source_hash", saved["incumbent_source_sha256"]
                == digest(HERE / "results/fixed-physical-grid-benchmark.json"))
    for name, sha in saved["dependency_sha256"].items():
        checked("saved_dependency_hash", sha == digest(HERE / name))
    upstream = json.loads(source.read_text(), parse_float=str)
    proposal = deepcopy(upstream["results"][saved["input_case_index"]])
    proposal["selected"] = saved["selected"]
    grids = {key: saved[key] for key in ("reference_grid", "coefficient_grid", "feature_grid", "score_grid", "log_grid")}
    rerun = producer.certify(upstream["problem_data"], proposal, **grids)
    # parse_float=str preserves the authoritative rational inputs, while the
    # display-only floats are compared numerically outside the exact payload.
    exact_saved, exact_rerun = canonical(saved), canonical(rerun)
    for key in ("display_lower_bound", "display_upper_bound", "display_gap"):
        checked("saved_display_consistency", float(exact_saved.pop(key)) == exact_rerun.pop(key))
    checked("saved_proposal_replay", exact_saved == exact_rerun)
    frozen = producer.certify(saved["problem_data"], {
        "block_size": saved["block_size"], "selected": saved["selected"],
        "best_tangent_witness": {"schur_information": saved["tangent_reference"],
                                 "nuisance_minimizer": saved["nuisance_witness"]}}, **grids)
    checked("saved_self_contained_replay", canonical(frozen) == canonical(rerun))
    N, prior = mat(saved["tangent_reference"]), mat(saved["problem_data"]["prior"])
    W = N.inv()
    checked("saved_prior_trace", Q(saved["prior_trace"]) == rational(sp.trace(W * prior)))
    anchors = saved["anchors"]
    if anchors:
        rho = Q(saved["problem_data"]["rho"])
        latent = Q(saved["problem_data"]["latent_variance"])
        KA = sp.Matrix(len(anchors), len(anchors), lambda i, j:
                       latent * rho ** abs(anchors[i] - anchors[j]))
        G = mat(saved["nuisance_witness"])
        anchor = rational(sp.trace(W * G.T * KA.inv() * G))
    else:
        anchor = Q(0)
    checked("saved_dense_anchor_prior_trace", Q(saved["anchor_prior_trace"]) == anchor)
    log_reference = independent_log(rational(N.det()))
    checked("saved_reference_log_upper", Q(saved["logdet_reference_upper"]) >= log_reference[1])
    checked("saved_global_sum_upper", Q(saved["upper_bound"]) >= log_reference[1]
            - saved["p"] + Q(saved["prior_trace"]) + anchor + Q(saved["integer_price"], saved["score_grid"]))
    J = independent_selected_information(saved["problem_data"], saved["selected"])
    independent_lower, independent_upper = independent_log(rational(J.det()))
    checked("saved_independent_incumbent_lower", Q(saved["lower_bound"]) <= independent_lower)
    checked("saved_independent_incumbent_below_upper", independent_upper <= Q(saved["upper_bound"]))
    shared = next(case for case in benchmark["results"] if case["n"] == saved["n"])
    if saved["n"] >= 96:
        checked("shared_greedy_incumbent", saved["selected"] == shared["greedy_exchange"]["selected"])
    checked("shared_benchmark_exact_problem", all(
        mat(saved["problem_data"][key]) == mat(shared[key]) for key in ("F", "prior")) and all(
        Q(saved["problem_data"][key]) == Q(shared[key]) for key in
        ("rho", "latent_variance", "nugget_variance")) and saved["k"] == shared["k"])
    return {"file": str(path.relative_to(HERE)), "sha256": digest(path), "n": saved["n"],
            "block_size": saved["block_size"], "gap": saved["gap"],
            "display_gap": float(saved["display_gap"]), "source_sha256": saved["source_sha256"],
            "incumbent_determinant_sha256": hashlib.sha256(str(rational(J.det())).encode()).hexdigest()}


def review_author_note():
    comparison = json.loads((HERE / "results/latent-separator-fixed-physical-comparison.json").read_text())
    refined = json.loads((HERE / "results/fixed-physical-grid-refined-transfer.json").read_text())
    note = (HERE.parent.parent / "notes/research-20260912-latent-separator-certificates.md").read_text()
    totals = {}
    for row in comparison["rows"]:
        n, b = row["n"], row["block_size"]
        path = HERE / f"results/latent-separator-n{n}-b{b}-certificate.json"
        if not path.exists():
            continue
        cert = json.loads(path.read_text())
        for field in ("lower_bound", "upper_bound", "gap"):
            checked("author_note_exact_bound_table", f"{float(Q(cert[field])):.12f}" in note)
        if n >= 96:
            total = row["accounted_total_seconds"] + cert["wall_seconds"]
            totals[f"n{n}_b{b}"] = total
            checked("author_note_accounted_runtime", f"{total:.3f}" in note)
        if n == 192:
            checked("author_note_n192_upper_comparison", float(Q(cert["upper_bound"]))
                    < row["dense_oa_upper_bound"] and float(Q(cert["upper_bound"]))
                    < row["best_saved_calendar_upper_bound"])
        if n == 96:
            checked("author_note_n96_upper_comparison", row["best_refined_calendar_upper_bound"]
                    < float(Q(cert["upper_bound"])))
    checked("author_note_total_above_30", totals["n192_b16"] > 30)
    refined96 = next(row for row in refined["results"] if row["n"] == 96 and "combined_true_gap" in row)
    checked("author_note_refined_gap", f"{refined96['combined_true_gap']:.5f}" in note)
    return totals


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-saved", action="store_true")
    args = parser.parse_args()
    started = perf_counter()
    fixture_specs = [(1, 1, 1, Q(1, 2), Q(3, 4)), (5, 2, 2, Q(1, 2), Q(3, 4)),
                     (7, 2, 3, Q(-2, 3), Q(3, 4)), (6, 3, 1, Q(-1, 2), Q(3, 4)),
                     (4, 2, 9, Q(-1, 2), Q(3, 4)), (5, 2, 2, Q(0), Q(3, 4)),
                     (5, 2, 2, Q(-1, 2), Q(0)), (5, 1, 3, Q(999, 1000), Q(3, 4)),
                     (5, 2, 3, Q(-999, 1000), Q(3, 4))]
    grids = [{"reference_grid": 7, "coefficient_grid": 31, "feature_grid": 3,
              "score_grid": 7, "log_grid": 11},
             {"reference_grid": 10 ** 8, "coefficient_grid": 100003,
              "feature_grid": 1009, "score_grid": 10007, "log_grid": 10 ** 12}]
    for spec, grid in product(fixture_specs, grids):
        check_tiny(*fixture(*spec), grid)
    malformed_checks()
    reports = []
    totals = {}
    benchmark_path = HERE / "results/fixed-physical-grid-benchmark.json"
    if not args.skip_saved:
        benchmark = json.loads(benchmark_path.read_text(), parse_float=str)
        files = sorted((HERE / "results").glob("latent-separator-n*-b*-certificate.json"))
        assert len(files) >= 5, "Expected the five planned saved certificates"
        for path in files:
            print("Reviewing", path.name, flush=True)
            reports.append(replay_saved(path, benchmark))
        totals = review_author_note()
    result = {"status": "passed", "scope": "Exact latent-separator certifier integration",
              "checks": COUNTS, "total_checks": sum(COUNTS.values()), "saved_certificates": reports,
              "reviewed_accounted_generation_plus_certificate_seconds": totals,
              "reviewer_sha256": digest(Path(__file__)),
              "certifier_sha256": digest(HERE / "certify_latent_separator.py"),
              "shared_benchmark_sha256": digest(benchmark_path), "wall_seconds": perf_counter() - started}
    output = HERE / "results/latent-separator-certificate-independent-review.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "checks": result["total_checks"],
                      "saved_certificates": len(reports), "wall_seconds": result["wall_seconds"]}))


if __name__ == "__main__":
    main()
