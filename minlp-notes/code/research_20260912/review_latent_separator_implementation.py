"""Independent numerical review of the latent-separator producer and witnesses.

Reference algebra uses dense covariance conditioning, dense selected solves, and
independent enumeration. Producer routines are invoked only as the test target.
This is not an exact certificate and does not recreate benchmark timings.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import replace
from fractions import Fraction
import hashlib
from itertools import combinations
import json
import math
import os
from pathlib import Path
from time import perf_counter
from types import SimpleNamespace
from unittest.mock import patch

for variable in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    if os.environ.get(variable) != "1":
        raise RuntimeError(f"Set {variable}=1 before starting this review")

import numpy as np

import latent_separator_design as producer
from noisy_markov_design import NoisyDesign, TimeBudgetExceeded

HERE = Path(__file__).resolve().parent
COUNTS = Counter()
ERRORS = Counter()


def close(name, actual, expected, atol=2e-8, rtol=2e-9):
    actual, expected = np.asarray(actual), np.asarray(expected)
    error = float(np.max(np.abs(actual-expected), initial=0.))
    ERRORS[name] = max(ERRORS[name], error)
    assert np.allclose(actual, expected, atol=atol, rtol=rtol), (name, error)
    COUNTS[name] += 1


def ld(matrix):
    sign, value = np.linalg.slogdet(matrix)
    assert sign > 0
    return float(value)


def dense_information(design, selected):
    s = list(selected)
    delta = np.abs(np.subtract.outer(s, s))
    covariance = design.latent_variance*design.rho**delta + design.nugget_variance*np.eye(len(s))
    return design.prior + design.F[s].T@np.linalg.solve(covariance, design.F[s])


class DenseReference:
    def __init__(self, design, block_size):
        self.design = design
        self.blocks = [tuple(range(start, min(start+block_size, design.n)))
                       for start in range(0, design.n, block_size)]
        self.anchors = [block[-1] for block in self.blocks[:-1]] if (
            design.rho != 0 and design.latent_variance != 0) else []
        K = design.latent_variance*design.rho**np.abs(np.subtract.outer(np.arange(design.n), np.arange(design.n)))
        KA = K[np.ix_(self.anchors, self.anchors)]
        self.H = np.linalg.solve(KA, K[self.anchors]).T
        self.D = K-self.H@K[self.anchors]+design.nugget_variance*np.eye(design.n)
        self.D = (self.D+self.D.T)/2
        self.prior = np.zeros((design.p+len(self.anchors),)*2)
        self.prior[:design.p, :design.p] = design.prior
        self.prior[design.p:, design.p:] = np.linalg.inv(KA)
        self.T = np.column_stack((design.F, self.H))

    def matrix(self, selected):
        s = list(selected)
        return self.prior+self.T[s].T@np.linalg.solve(self.D[np.ix_(s, s)], self.T[s])


def dense_schur(M, p):
    inverse = np.linalg.inv(M)
    information = np.linalg.inv(inverse[:p, :p])
    C = M[p:, p:]
    gradient = inverse.copy()
    gradient[p:, p:] -= np.linalg.inv(C)
    G = -np.linalg.solve(C, M[p:, :p])
    return ld(M)-ld(C), information, G, gradient


def small_cases():
    rng = np.random.default_rng(92846219)
    cases = []
    for n in (1, 2, 4, 7):
        for rho, latent in ((-.85, 1.3), (0., 1.3), (.65, 0.), (.98, 1.3)):
            A = rng.normal(size=(3, 3))
            design = NoisyDesign(rng.normal(size=(n, 3)), rho, latent, .45,
                                 .2*np.eye(3)+A@A.T, 0)
            for b in sorted({1, 2, 3, n, n+2}):
                reference = DenseReference(design, b)
                oracle = producer.SeparatorOracle(design, b)
                assert tuple(reference.anchors) == oracle.anchors
                assert tuple(reference.blocks) == tuple(block.times for block in oracle.blocks)
                close("anchor_prior", oracle.prior, reference.prior)
                H, D = np.zeros_like(reference.H), np.zeros_like(reference.D)
                for block in oracle.blocks:
                    H[np.ix_(block.times, block.anchor_columns)] = block.H
                    D[np.ix_(block.times, block.times)] = block.D
                close("dense_conditional_mean", H, reference.H)
                close("dense_conditional_covariance", D, reference.D)
                for anchor_column, anchor in enumerate(reference.anchors):
                    close("anchor_endpoint_membership", H[anchor], np.eye(len(reference.anchors))[anchor_column])
                    close("anchor_residual_row", D[anchor], design.nugget_variance*np.eye(n)[anchor])
                schedules = [s for k in range(n+1) for s in combinations(range(n), k)]
                matrices = [reference.matrix(s) for s in schedules]
                for s, expected_M in zip(schedules, matrices):
                    M = oracle.matrix(s)
                    close("all_subset_augmented_matrix", M, expected_M)
                    value, J, _, _ = producer.schur_value_gradient(M, design.p)
                    true_J = dense_information(design, s)
                    close("all_subset_true_information", J, true_J)
                    close("all_subset_true_objective", value, ld(true_J))
                mixture = .23*matrices[0]+.41*matrices[-1]+.36*matrices[len(matrices)//2]
                value, J, G, gradient = producer.schur_value_gradient(mixture, design.p)
                ev, eJ, eG, egradient = dense_schur(mixture, design.p)
                close("dense_schur_value", value, ev)
                close("dense_schur_information", J, eJ)
                close("dense_schur_nuisance", G, eG)
                close("dense_inverse_gradient", gradient, egradient)
                close("gradient_homogeneity", np.sum(gradient*mixture), design.p)
                direction = rng.normal(size=mixture.shape)
                direction = (direction+direction.T)/2
                h = 1e-5/max(1., np.linalg.norm(direction))
                numeric = (dense_schur(mixture+h*direction, design.p)[0]
                           -dense_schur(mixture-h*direction, design.p)[0])/(2*h)
                close("full_symmetric_gradient_difference", np.sum(gradient*direction), numeric, atol=2e-6)
                for k in range(n+1):
                    oracle.design = replace(design, k=k)
                    indices = [i for i, s in enumerate(schedules) if len(s) == k]
                    random_gradient = rng.normal(size=mixture.shape)
                    random_gradient = (random_gradient+random_gradient.T)/2
                    for L in (gradient, random_gradient, np.zeros_like(gradient)):
                        price, chosen, masks = oracle.price(L)
                        scores = [float(np.sum(L*(matrices[i]-reference.prior))) for i in indices]
                        close("exhaustive_cardinality_price", price, max(scores))
                        close("price_reconstruction", price, np.sum(L*(reference.matrix(chosen)-reference.prior)))
                        assert len(chosen) == k and len(set(chosen)) == k
                        assert tuple(sorted(t for block, mask in zip(reference.blocks, masks)
                                            for bit, t in enumerate(block) if mask & (1 << bit))) == chosen
                    tangent = value-design.p+np.sum(gradient*reference.prior)
                    tangent += max(float(np.sum(gradient*(matrices[i]-reference.prior))) for i in indices)
                    optimum = max(ld(dense_information(design, schedules[i])) for i in indices)
                    assert tangent >= optimum-2e-8
                    COUNTS["exhaustive_tangent_upper"] += 1
                cases.append({"n": n, "rho": rho, "latent_variance": latent, "block_size": b})
    return cases


def termination_and_solver_cases():
    rng = np.random.default_rng(537249)
    summaries = []
    for n in (1, 5, 7):
        for k in sorted({0, 1, max(0, n-1), n}):
            d = NoisyDesign(rng.normal(size=(n, 2)), -.8, .9, .3, .2*np.eye(2), k)
            optimum = max(ld(dense_information(d, s)) for s in combinations(range(n), k))
            for b in sorted({1, 3, n}):
                result = producer.solve_separator(d, b, time_limit=2., max_rounds=30)
                selected = tuple(result["selected"])
                assert len(selected) == k and len(set(selected)) == k
                close("solver_dense_lower", result["true_lower_bound"], ld(dense_information(d, selected)))
                assert result["true_lower_bound"] <= optimum+2e-8 <= result["true_upper_bound"]+4e-8
                support = result["hull_support"]
                assert all(row["weight"] >= 0 and len(row["selected"]) == k for row in support)
                close("solver_simplex_sum", sum(row["weight"] for row in support), 1.)
                reference = DenseReference(d, b)
                expected_M = sum(row["weight"]*reference.matrix(row["selected"]) for row in support)
                close("solver_hull_reconstruction", result["hull_matrix"], expected_M)
                close("solver_hull_value", result["hull_value"], dense_schur(expected_M, d.p)[0])
                summaries.append({"n": n, "k": k, "b": b, "status": result["status"]})
    d = NoisyDesign(rng.normal(size=(7, 2)), .8, 1., .3, .2*np.eye(2), 3)
    memory = producer.solve_separator(d, 3, max_memory_mb=1e-9)
    assert memory["status"] == "memory_limit" and memory["selected"] is None
    COUNTS["memory_preflight"] += 1
    timed = producer.solve_separator(d, 3, time_limit=1e-12)
    assert timed["status"] == "time_limit" and len(timed["selected"]) == d.k
    close("timeout_preserves_dense_incumbent", timed["true_lower_bound"], ld(dense_information(d, timed["selected"])))
    assert timed["best_tangent_witness"] is None
    original_price = producer.SeparatorOracle.price
    price_calls = 0
    def second_price_times_out(oracle, gradient, **kwargs):
        nonlocal price_calls
        price_calls += 1
        if price_calls == 2:
            raise TimeBudgetExceeded("injected during second pricing round")
        return original_price(oracle, gradient, **kwargs)
    with patch.object(producer.SeparatorOracle, "price", second_price_times_out):
        interrupted = producer.solve_separator(d, 3, time_limit=2.)
    assert interrupted["status"] == "time_limit" and interrupted["pricing_rounds"] == 1
    assert interrupted["best_tangent_witness"] is not None
    assert interrupted["true_lower_bound"] <= interrupted["true_upper_bound"]+2e-8
    COUNTS["interrupted_pricing_preserves_complete_bound"] += 1
    def stalled_correction(matrices, weights, *args):
        return weights.copy(), False, "injected correction failure"
    with patch.object(producer, "correct_weights", stalled_correction):
        stalled = producer.solve_separator(d, 3, time_limit=2.)
    assert stalled["status"] == "correction_stalled" and stalled["correction_failures"] == 1
    assert stalled["true_lower_bound"] <= stalled["true_upper_bound"]+2e-8
    COUNTS["failed_correction_preserves_bound"] += 1
    blocks, seed = [np.array([[.2]]), np.array([[4.]])], np.array([1., 0.])
    for mode in ("failure", "timeout"):
        def fake_minimize(fun, *args, **kwargs):
            fun(np.array([.4, .6]))
            if mode == "timeout":
                raise TimeBudgetExceeded("injected after feasible improvement")
            return SimpleNamespace(success=False, message="injected correction failure")
        with patch.object(producer, "minimize", fake_minimize):
            weights, success, message = producer.correct_weights(blocks, seed, 1, math.inf, 5)
        close("correction_retains_feasible_improvement", weights, [.4, .6])
        assert not success and (message == "time_limit") == (mode == "timeout")
    # This accepted, ill-conditioned input has a well-defined dense seed/full
    # value. Record whether finalization preserves the numerical-failure status.
    difficult = NoisyDesign(np.ones((4, 2)), .8, 1., 1e-16, .01*np.eye(2), 2)
    failure_case = {"input": {"F": difficult.F.tolist(), "rho": .8, "latent_variance": 1.,
                              "nugget_variance": 1e-16, "prior": difficult.prior.tolist(), "k": 2, "b": 1},
                    "dense_seed_value": ld(dense_information(difficult, (0, 3))),
                    "dense_full_value": ld(dense_information(difficult, range(4)))}
    try:
        numerical = producer.solve_separator(difficult, 1, time_limit=1.)
        failure_case.update(outcome="returned", status=numerical["status"],
                            true_lower_bound=numerical["true_lower_bound"],
                            true_upper_bound=numerical["true_upper_bound"])
        assert numerical["status"] == "numerical_linear_algebra_failure"
        close("numerical_failure_preserves_lower", numerical["true_lower_bound"], failure_case["dense_seed_value"])
        close("numerical_failure_uses_full_upper", numerical["true_upper_bound"], failure_case["dense_full_value"])
        assert numerical["hull_value"] is None and numerical["hull_gap"] is None
        assert numerical["hull_schur_information"] is None
    except np.linalg.LinAlgError as error:
        failure_case.update(outcome="uncaught_LinAlgError", message=str(error))
    near_unit = NoisyDesign(np.ones((4, 1)), np.nextafter(1., 0.), 1., 1e-8,
                            np.eye(1)*1e-8, 2)
    inconsistent = producer.solve_separator(near_unit, 1, time_limit=1.)
    assert inconsistent["status"] == "numerical_bound_inconsistency"
    close("inconsistency_uses_full_upper", inconsistent["true_upper_bound"],
          ld(dense_information(near_unit, range(4))))
    assert inconsistent["true_gap"] >= 0
    assert inconsistent["hull_value"] is None and inconsistent["hull_gap"] is None
    assert inconsistent["hull_schur_information"] is None
    assert inconsistent["best_tangent_witness"] is None
    COUNTS["extreme_conditioning_flags_inconsistency"] += 1
    return {"solver_cases": summaries, "numerical_failure_case": failure_case,
            "extreme_conditioning_inconsistency": {
                "rho": near_unit.rho, "latent_variance": 1., "nugget_variance": 1e-8,
                "F": near_unit.F.tolist(), "prior": near_unit.prior.tolist(), "k": 2, "b": 1,
                "status": inconsistent["status"], "true_lower_bound": inconsistent["true_lower_bound"],
                "true_upper_bound": inconsistent["true_upper_bound"], "true_gap": inconsistent["true_gap"],
                "hull_value": inconsistent["hull_value"], "hull_gap": inconsistent["hull_gap"],
                "best_tangent_witness": inconsistent["best_tangent_witness"]}}


def all_pattern_scores(D, X, W):
    """Enumerate subsets by dense sequential Gaussian conditioning.

    Each recursive node conditions the remaining rows on its selected row.
    This is independent of producer pattern matrices and conditional formulas.
    """
    n = len(D)
    scores = np.zeros(1 << n)
    def recurse(covariance, rows, indices, mask, value):
        for j, index in enumerate(indices):
            variance = covariance[j, j]
            assert variance > 0
            score = value+float(rows[j]@W@rows[j])/variance
            next_mask = mask | (1 << index)
            scores[next_mask] = score
            if j+1 < len(indices):
                regression = covariance[j+1:, j]/variance
                remaining = covariance[j+1:, j+1:]-np.outer(regression, covariance[j, j+1:])
                adjusted = rows[j+1:]-np.outer(regression, rows[j])
                recurse(remaining, adjusted, indices[j+1:], next_mask, score)
    recurse(D, X, tuple(range(n)), 0, 0.)
    return scores


def independent_support(reference, G, W, k):
    values = {0: (0., ())}
    all_scores = []
    for block in reference.blocks:
        X = reference.design.F[list(block)]+reference.H[list(block)]@G
        D = reference.D[np.ix_(block, block)]
        scores = all_pattern_scores(D, X, W)
        all_scores.append(scores)
        options = {}
        for mask, score in enumerate(scores):
            count = mask.bit_count()
            if count <= k and (count not in options or score > options[count][0]):
                options[count] = (score, mask)
        following = {}
        for used, (value, masks) in values.items():
            for count, (score, mask) in options.items():
                total = used+count
                if total <= k and (total not in following or value+score > following[total][0]):
                    following[total] = (float(value+score), masks+(mask,))
        values = following
        # Independently check representative recursive scores by direct solves.
        for mask in {0, 1, (1 << len(block))-1, ((1 << len(block))-1)//3}:
            rows = [i for i in range(len(block)) if mask & (1 << i)]
            direct = float(np.trace(W@X[rows].T@np.linalg.solve(D[np.ix_(rows, rows)], X[rows])))
            close("saved_pattern_direct_solve", scores[mask], direct)
    return values[k], all_scores


def saved_witnesses():
    summaries = []
    names = [f"latent-separator-n{n}-probe.json" for n in (48, 96, 192)]
    names += [f"latent-separator-n{n}-larger-blocks.json" for n in (96, 192)]
    files = [HERE/"results"/name for name in sorted(names)]
    for file in files:
        report = json.loads(file.read_text())
        data = report["problem_data"]
        d = NoisyDesign(np.array(data["F"]), float(Fraction(data["rho"])),
                        float(Fraction(data["latent_variance"])), float(Fraction(data["nugget_variance"])),
                        np.array(data["prior"]), data["k"])
        for result in report["results"]:
            b = result["block_size"]
            reference = DenseReference(d, b)
            assert list(result["anchors"]) == reference.anchors
            assert [list(block) for block in reference.blocks] == [row["times"] for row in result["block_layout"]]
            selected = result["selected"]
            assert len(selected) == d.k and len(set(selected)) == d.k
            lower = ld(dense_information(d, selected))
            close("saved_dense_incumbent", result["true_lower_bound"], lower)
            full = ld(dense_information(d, range(d.n)))
            close("saved_dense_full_upper", result["full_selection_upper_bound"], full)
            support = result["hull_support"]
            assert all(row["weight"] >= 0 and len(row["selected"]) == d.k
                       and len(set(row["selected"])) == d.k for row in support)
            close("saved_simplex_sum", sum(row["weight"] for row in support), 1.)
            mixture = sum(row["weight"]*reference.matrix(row["selected"]) for row in support)
            close("saved_hull_matrix", result["hull_matrix"], mixture, atol=2e-7)
            hull, J, _, _ = dense_schur(mixture, d.p)
            close("saved_hull_value", result["hull_value"], hull)
            close("saved_hull_information", result["hull_schur_information"], J, atol=2e-7)
            witness = result["best_tangent_witness"]
            M = np.array(witness["matrix"])
            value, J, G, gradient = dense_schur(M, d.p)
            W = np.linalg.inv(J)
            close("saved_witness_logdet", witness["logdet_schur"], value)
            close("saved_witness_information", witness["schur_information"], J, atol=2e-7)
            close("saved_witness_nuisance", witness["nuisance_minimizer"], G)
            (price, masks), scores = independent_support(reference, G, W, d.k)
            close("saved_independent_support_price", witness["linear_price_excluding_prior"], price)
            saved_masks = witness["priced_block_masks"]
            close("saved_priced_mask_value", sum(score[mask] for score, mask in zip(scores, saved_masks)), price)
            reconstructed = sorted(t for block, mask in zip(reference.blocks, saved_masks)
                                   for bit, t in enumerate(block) if mask & (1 << bit))
            assert reconstructed == witness["priced_selection"] and len(reconstructed) == d.k
            prior_trace = np.trace(W@d.prior)+np.trace(W@G.T@reference.prior[d.p:, d.p:]@G)
            close("saved_fixed_prior_trace", witness["prior_trace"], prior_trace)
            upper = -ld(W)-d.p+prior_trace+price
            close("saved_tangent_upper", witness["upper_bound"], upper)
            close("saved_final_upper", result["true_upper_bound"], min(full, upper))
            close("saved_true_gap", result["true_gap"], result["true_upper_bound"]-lower)
            close("saved_hull_gap", result["hull_gap"], result["true_upper_bound"]-hull)
            assert lower <= upper+2e-8 and hull <= upper+2e-8
            summaries.append({"file": file.name, "file_sha256": hashlib.sha256(file.read_bytes()).hexdigest(),
                              "producer_sha256": report["metadata"]["source_sha256"], "n": d.n, "b": b,
                              "pattern_count": sum(len(score) for score in scores),
                              "support_count": len(support), "status": result["status"],
                              "reconstructed_lower": lower, "reconstructed_upper": upper,
                              "reconstructed_hull": hull, "true_gap": upper-lower,
                              "hull_gap": upper-hull})
            print(json.dumps({"saved_witness_passed": file.name, "b": b}), flush=True)
    assert len(summaries) == 13
    return summaries


def main():
    started = perf_counter()
    source_sha = hashlib.sha256(Path(producer.__file__).read_bytes()).hexdigest()
    small = small_cases()
    print(json.dumps({"small_configurations_passed": len(small)}), flush=True)
    termination = termination_and_solver_cases()
    witnesses = saved_witnesses()
    outcome = termination["numerical_failure_case"]["outcome"]
    report = {"status": "passed_with_reported_issue" if outcome == "uncaught_LinAlgError" else "passed",
              "scope": "Independent numerical implementation and saved-witness review; no exact arithmetic or timing reproduction",
              "producer_sha256": source_sha, "review_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "thread_environment": {v: os.environ[v] for v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")},
              "small_configurations": small, "counts": dict(COUNTS), "maximum_absolute_errors": dict(ERRORS),
              "termination": termination, "saved_witnesses": witnesses, "review_seconds": perf_counter()-started}
    output = HERE/"results/latent-separator-independent-implementation-checks.json"
    output.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"status": report["status"], "counts": dict(COUNTS), "seconds": report["review_seconds"]}), flush=True)


if __name__ == "__main__":
    main()
