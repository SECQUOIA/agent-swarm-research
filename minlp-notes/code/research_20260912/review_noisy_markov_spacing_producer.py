"""Fresh independent audit of the compact minimum-gap numerical producer.

Reference information is formed from an explicit conditional triangular
matrix. Reference dynamic programming stores selected calendar tuples and the
last observation, without production bit masks or capacity pruning.
"""

from hashlib import sha256
from itertools import combinations
import json
import math
from pathlib import Path
import platform
from time import perf_counter
from unittest.mock import patch

import numpy as np
import scipy

import noisy_markov_spacing_design as target


HERE = Path(__file__).resolve().parent
COUNTS = {"mask_checks": 0, "information_checks": 0, "pricing_checks": 0,
          "producer_checks": 0, "support_checks": 0, "witness_checks": 0,
          "invalid_input_checks": 0, "failure_checks": 0}
ERRORS = {"information": 0.0, "pricing": 0.0, "saved_information": 0.0,
          "saved_bound": 0.0}


def close(actual, expected, label, tolerance=3e-9):
    actual, expected = np.asarray(actual), np.asarray(expected)
    difference = float(np.max(np.abs(actual-expected), initial=0))
    if not np.allclose(actual, expected, rtol=tolerance, atol=tolerance):
        raise AssertionError((label, difference, actual, expected))
    return difference


def ld(matrix):
    sign, value = np.linalg.slogdet(matrix)
    assert sign > 0
    return float(value)


def separated(selected, gap):
    return all(b-a >= gap for a, b in zip(selected[:-1], selected[1:]))


class Reference:
    def __init__(self, design, L, gap):
        self.d, self.L, self.gap = design, min(L, design.n-1), gap
        self.R = np.array([[design.latent_variance*design.rho**abs(i-j)
                            + (design.nugget_variance if i == j else 0)
                            for j in range(design.n)] for i in range(design.n)])
        self.local_cache = {}
        self.information_cache = {}

    def local(self, t, history):
        key = t, history
        if key not in self.local_cache:
            indices = list(history)
            if indices:
                regression = self.R[t, indices] @ np.linalg.inv(self.R[np.ix_(indices, indices)])
                variance = self.R[t, t]-regression @ self.R[indices, t]
                sensitivity = self.d.F[t]-regression @ self.d.F[indices]
            else:
                regression, variance, sensitivity = np.empty(0), self.R[t, t], self.d.F[t]
            self.local_cache[key] = regression, variance, np.outer(sensitivity, sensitivity)/variance
        return self.local_cache[key]

    def information(self, selected):
        selected = tuple(sorted(selected))
        if selected not in self.information_cache:
            A = np.eye(len(selected))
            variances = np.empty(len(selected))
            for row, t in enumerate(selected):
                columns = [i for i in range(row) if selected[i] >= t-self.L]
                history = tuple(selected[i] for i in columns)
                regression, variance, _ = self.local(t, history)
                A[row, columns], variances[row] = -regression, variance
            F = self.d.F[list(selected)]
            Q = A.T @ np.diag(1/variances) @ A
            surrogate = self.d.prior+F.T @ Q @ F
            true = self.d.prior+F.T @ np.linalg.inv(self.R[np.ix_(selected, selected)]) @ F
            self.information_cache[selected] = true, surrogate
        return self.information_cache[selected]

    def price(self, H):
        # Keep the last selection even if it has left the information window.
        states = {(0, (), -self.gap): (0., ())}
        for t in range(self.d.n):
            following = {}
            for (count, history, last), (value, selected) in states.items():
                for take in (False, True):
                    if take and (count == self.d.k or t-last < self.gap):
                        continue
                    new_count = count+take
                    if new_count+self.d.n-t-1 < self.d.k:
                        continue
                    new_history = tuple(j for j in history if j >= t+1-self.L)
                    candidate = value
                    if take:
                        candidate += float(np.trace(H @ self.local(t, history)[2]))
                        if self.L:
                            new_history += (t,)
                    new_last = t if take else max(last, t+1-self.gap)
                    key = new_count, new_history, new_last
                    if key not in following or candidate > following[key][0]:
                        following[key] = candidate, selected+((t,) if take else ())
            states = following
        return max(states.values(), key=lambda item: item[0])


def inspect_result(design, result, *, exhaustive=False):
    gap, L = result["minimum_gap"], result["L"]
    ref = Reference(design, L, gap)
    assert result["true_upper_bound"] is None and result["true_gap"] is None
    if result["selected"] is None:
        assert result["status"] == "memory_limit"
        assert result["true_lower_bound"] is None and not result["hull_support"]
        return
    selected = tuple(result["selected"])
    assert len(selected) == design.k and len(set(selected)) == len(selected) and separated(selected, gap)
    close(result["true_lower_bound"], ld(ref.information(selected)[0]), "true incumbent")
    if result["hull_support"]:
        weights, matrices = [], []
        for support in result["hull_support"]:
            path = tuple(support["selected"])
            assert len(path) == design.k and len(set(path)) == len(path) and separated(path, gap)
            matrix = ref.information(path)[1]
            error = close(support["information"], matrix, "saved support")
            ERRORS["saved_information"] = max(ERRORS["saved_information"], error)
            matrices.append(matrix)
            weights.append(support["weight"])
            COUNTS["support_checks"] += 1
        assert min(weights) >= 0
        close(sum(weights), 1., "simplex sum")
        M = np.einsum("a,aij->ij", weights, matrices)
        close(result["hull_information"], M, "saved mixture")
        close(result["surrogate_hull_value"], ld(M), "mixture log determinant")
    witness = result["upper_bound_witness"]
    if witness:
        M, H = np.array(witness["hull_information"]), np.array(witness["gradient"])
        close(H @ M, np.eye(design.p), "tangent inverse")
        price, path = ref.price(H)
        close(price, witness["linear_price_excluding_prior"], "tuple-state tangent price")
        saved_path = tuple(witness["priced_selection"])
        assert len(saved_path) == design.k and separated(saved_path, gap)
        close(price, np.trace(H @ (ref.information(saved_path)[1]-design.prior)), "saved maximizing path")
        upper = ld(M)-design.p+np.trace(H @ design.prior)+price
        error = close(upper, result["surrogate_upper_bound"], "saved upper")
        ERRORS["saved_bound"] = max(ERRORS["saved_bound"], error)
        close(upper, witness["surrogate_upper_bound"], "witness upper")
        assert upper >= result["surrogate_hull_value"]-1e-7
        if exhaustive:
            for selected in combinations(range(design.n), design.k):
                if separated(selected, gap):
                    assert ld(ref.information(selected)[1]) <= upper+1e-7
        COUNTS["witness_checks"] += 1
    COUNTS["producer_checks"] += 1


def rejects(call):
    try:
        call()
    except (ValueError, TypeError):
        COUNTS["invalid_input_checks"] += 1
    else:
        raise AssertionError("Malformed input accepted")


def run():
    started = perf_counter()
    rng = np.random.default_rng(20260912073)
    for width in range(13):
        for gap in range(1, 16):
            expected = tuple(mask for mask in range(1 << width)
                             if separated([j for j in range(width) if mask & (1 << j)], gap))
            assert target.separated_masks(width, gap) == expected
            assert target.spacing_mask_count(width, gap) == len(expected)
            COUNTS["mask_checks"] += 1

    case_number, producer_cases = 0, []
    for n in (1, 2, 4, 6, 8, 9):
        F = rng.normal(size=(n, 2))
        prior = np.array([[.3, .07], [.07, .2]])
        for gap in sorted({1, 2, 3, n, n+2}):
            capacity = (n+gap-1)//gap
            for L in sorted({0, 1, max(0, gap-2), gap-1, n-1, n+2}):
                rho = (-.87, -.2, 0., .4, .95)[case_number % 5]
                latent = (0., .1, 2.)[case_number % 3]
                noise = (.03, .5, 4.)[case_number % 3]
                design = target.NoisyDesign(F, rho, latent, noise, prior, capacity)
                oracle = target.SpacingCalendarOracle(design, L, gap)
                ref = Reference(design, L, gap)
                all_matrices = {}
                for size in range(capacity+1):
                    for selected in combinations(range(n), size):
                        if not separated(selected, gap):
                            continue
                        matrix = ref.information(selected)[1]
                        error = close(oracle.information(selected), matrix, "dense conditional information")
                        ERRORS["information"] = max(ERRORS["information"], error)
                        all_matrices[selected] = matrix
                        COUNTS["information_checks"] += 1
                        if L >= n-1:
                            close(matrix, ref.information(selected)[0], "full history exactness")
                for k in sorted({0, 1, min(2, capacity), capacity}):
                    design_k = target.NoisyDesign(F, rho, latent, noise, prior, k)
                    oracle_k = target.SpacingCalendarOracle(design_k, L, gap)
                    for gradient in (rng.normal(size=(2, 2)), np.zeros((2, 2)), -np.eye(2)):
                        maximum, selected = oracle_k.price(gradient)
                        expected = max(np.trace(gradient @ (matrix-prior)) for path, matrix in all_matrices.items()
                                       if len(path) == k)
                        error = close(maximum, expected, "exhaustive signed pricing")
                        ERRORS["pricing"] = max(ERRORS["pricing"], error)
                        assert len(selected) == k and selected in all_matrices
                        close(maximum, np.trace(gradient @ (all_matrices[selected]-prior)), "selected price")
                        COUNTS["pricing_checks"] += 1
                    if case_number % 13 == 0:
                        result = target.produce_spacing_hull(design_k, L, gap, time_limit=5)
                        inspect_result(design_k, result, exhaustive=True)
                        producer_cases.append({"n": n, "gap": gap, "L": L, "k": k,
                                               "status": result["status"]})
                case_number += 1

    d = target.NoisyDesign(rng.normal(size=(8, 2)), .4, 1., 1., np.eye(2), 3)
    oracle = target.SpacingCalendarOracle(d, 0, 3)
    for selected in ((0, 1), (0, 0), (-1,), (8,), (1.2,), (True,), (np.bool_(False),), ("1",)):
        rejects(lambda selected=selected: oracle.information(selected))
    rejects(lambda: oracle.validate_selection((0,), exact_count=True))
    for L, gap in ((-1, 1), (1.2, 1), (True, 1), (0, 0), (0, -1), (0, 1.2), (0, True), (0, 9)):
        rejects(lambda L=L, gap=gap: target.SpacingCalendarOracle(d, L, gap))
    for value in (0, -1, math.inf, math.nan):
        rejects(lambda value=value: target.produce_spacing_hull(d, 0, 2, max_memory_mb=value))
    for kwargs in ({"time_limit": 0}, {"time_limit": 31}, {"time_limit": math.nan},
                   {"max_rounds": -1}, {"hull_gap": 0}, {"hull_gap": math.inf}):
        rejects(lambda kwargs=kwargs: target.produce_spacing_hull(d, 0, 2, **kwargs))
    with patch.object(target.NoisyDesign, "covariance", side_effect=AssertionError("preflight allocated covariance")), \
         patch.object(target.NoisyDesign, "true_objective", side_effect=AssertionError("preflight evaluated objective")):
        refused = target.produce_spacing_hull(d, 7, 1, max_memory_mb=.000001)
        assert refused["status"] == "memory_limit" and refused["selected"] is None
        COUNTS["failure_checks"] += 1
    for kwargs in ({"max_rounds": 0}, {"time_limit": 1e-12}):
        early = target.produce_spacing_hull(d, 0, 2, **kwargs)
        assert early["status"] in ("iteration_limit", "time_limit")
        inspect_result(d, early)
        COUNTS["failure_checks"] += 1
    with patch.object(target.SpacingCalendarOracle, "price", side_effect=target.TimeBudgetExceeded):
        interrupted = target.produce_spacing_hull(d, 0, 2)
        assert interrupted["status"] == "time_limit"
        inspect_result(d, interrupted)
        COUNTS["failure_checks"] += 1
    for success, message in ((False, "induced correction failure"), (False, "time_limit")):
        with patch.object(target, "correct_weights", side_effect=lambda mats, weights, deadline, iterations:
                          (weights, success, message)):
            interrupted = target.produce_spacing_hull(d, 0, 2)
            assert interrupted["status"] in ("correction_stalled", "time_limit")
            assert interrupted["correction_failures"] == 1
            inspect_result(d, interrupted, exhaustive=True)
            COUNTS["failure_checks"] += 1

    saved_path = HERE / "results/noisy-markov-spacing-kinetics-probe.json"
    saved = json.loads(saved_path.read_text())
    record = saved["results"][0]
    design = target.NoisyDesign(np.array(record["F"]), record["rho"], record["latent_variance"],
                                record["nugget_variance"], np.array(record["prior"]), record["k"])
    for result in record["hulls"]:
        inspect_result(design, result)
    source_hash = sha256(Path(target.__file__).read_bytes()).hexdigest()
    assert saved["metadata"]["source_sha256"] == source_hash
    report = {"status": "passed", "scope": "numerical compact oracle and feasible hull producer; no true global bound audited",
              "counts": COUNTS, "maximum_absolute_errors": ERRORS, "small_model_configurations": case_number,
              "producer_cases": producer_cases, "saved_result": str(saved_path),
              "saved_result_sha256": sha256(saved_path.read_bytes()).hexdigest(),
              "source_hashes": {name: sha256((HERE/name).read_bytes()).hexdigest() for name in
                                ("noisy_markov_spacing_design.py", "noisy_markov_design.py", "noisy_markov_spacing_bound.py",
                                 "noisy_markov_kinetics_probe.py", Path(__file__).name)},
              "versions": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
              "wall_seconds": perf_counter()-started}
    output = HERE / "results/noisy-markov-spacing-producer-independent-review.json"
    output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({k: report[k] for k in ("status", "counts", "maximum_absolute_errors", "wall_seconds")}, indent=2))


if __name__ == "__main__":
    run()
