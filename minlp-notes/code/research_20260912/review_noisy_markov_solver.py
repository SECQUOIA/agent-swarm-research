"""Independent bounded audit of the noisy Markov design implementation.

The reference factorization uses explicit selected-subset triangular matrices.
The reference pricing algorithm uses tuples of calendar indices, not bit masks.
No production source is modified. Bounds are numerical, not interval certified.
"""

from __future__ import annotations

from dataclasses import asdict
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

import noisy_markov_design as target


HERE = Path(__file__).resolve().parent
REPORT = HERE / "results/noisy-markov-solver-independent-review.json"


def close(actual, expected, label, atol=2e-8):
    if not np.allclose(actual, expected, atol=atol, rtol=atol):
        raise AssertionError((label, actual, expected))


def ld(J):
    sign, value = np.linalg.slogdet(J)
    assert sign > 0
    return float(value)


def expected_delta(design, L):
    rho, P, noise = abs(design.rho), design.latent_variance, design.nugget_variance
    if rho == 0 or P == 0 or L >= design.n-1:
        return 0.
    direct_tail = 2*P/noise * rho**(L+1)/(1-rho)
    unrefined_row_sum = 2*P/noise * rho**(L+1)*(1-rho**(L+1))/(1-rho)**2
    return direct_tail + P/(P+noise)*(unrefined_row_sum-direct_tail)


class Reference:
    def __init__(self, design, window):
        self.d = design
        self.L = min(window, design.n - 1)
        self.R = np.array([[design.latent_variance * design.rho ** abs(i-j)
                            + (design.nugget_variance if i == j else 0)
                            for j in range(design.n)] for i in range(design.n)])
        self.cache = {}

    def local(self, t, history):
        key = t, history
        if key not in self.cache:
            h = list(history)
            if h:
                b = self.R[t, h] @ np.linalg.inv(self.R[np.ix_(h, h)])
                variance = self.R[t, t] - b @ self.R[h, t]
                f = self.d.F[t] - b @ self.d.F[h]
            else:
                b, variance, f = np.empty(0), self.R[t, t], self.d.F[t]
            self.cache[key] = b, variance, np.outer(f, f) / variance
        return self.cache[key]

    def information(self, selected):
        selected = tuple(sorted(selected))
        size = len(selected)
        A, variances = np.eye(size), np.empty(size)
        for row, t in enumerate(selected):
            positions = [j for j in range(row) if selected[j] >= t - self.L]
            history = tuple(selected[j] for j in positions)
            regression, variance, _ = self.local(t, history)
            A[row, positions] = -regression
            variances[row] = variance
        Q = A.T @ np.diag(1 / variances) @ A
        F = self.d.F[list(selected)]
        R = self.R[np.ix_(selected, selected)]
        residual = A @ R @ A.T
        if size:
            residual /= np.sqrt(variances[:, None] * variances[None, :])
        true = self.d.prior + F.T @ np.linalg.inv(R) @ F
        surrogate = self.d.prior + F.T @ Q @ F
        return true, surrogate, residual

    def price(self, H):
        # A different state representation and independent local-factor code.
        states = {(0, ()): (0., ())}
        for t in range(self.d.n):
            following = {}
            for (count, history), (value, selected) in states.items():
                for take in (False, True):
                    next_count = count + take
                    if not next_count <= self.d.k <= next_count + self.d.n-t-1:
                        continue
                    next_history = tuple(j for j in history if j >= t+1-self.L)
                    candidate = value
                    if take:
                        candidate += float(np.trace(H @ self.local(t, history)[2]))
                        if self.L:
                            next_history += (t,)
                    key = next_count, next_history
                    if key not in following or candidate > following[key][0]:
                        following[key] = candidate, selected + ((t,) if take else ())
            states = following
        return max(states.values(), key=lambda item: item[0])


def inspect_hull(design, result, *, enumerate_designs=True):
    r = asdict(result) if not isinstance(result, dict) else result
    # A refused preflight can intentionally avoid every covariance allocation.
    if r["true_lower_bound"] is None:
        assert r["status"] == "memory_limit"
        assert r["true_upper_bound"] is None
        return {"status": r["status"], "witnesses": 0}
    ref = Reference(design, r["L"])
    selected = tuple(r["selected"])
    assert len(selected) == design.k and len(set(selected)) == len(selected)
    close(r["true_lower_bound"], ld(ref.information(selected)[0]), "feasible lower")
    close(r["full_selection_upper_bound"], ld(ref.information(tuple(range(design.n)))[0]), "full upper")
    assert r["true_upper_bound"] >= r["true_lower_bound"] - 2e-7
    assert r["true_upper_bound"] <= r["full_selection_upper_bound"] + 2e-7
    delta = expected_delta(design, r["L"])
    close(target.spectral_delta(design, r["L"]), delta, "implemented delta formula")
    close(r["delta"], delta, "delta")
    assert r["memory_bound_usable"] == (delta < 1)
    supports = r["hull_support"]
    if supports:
        weights = np.array([s["weight"] for s in supports])
        close(sum(weights), 1, "convex weights")
        assert np.min(weights) >= -1e-12
        matrices = []
        for s in supports:
            path = tuple(s["selected"])
            assert len(path) == design.k and len(set(path)) == len(path)
            matrix = ref.information(path)[1]
            close(s["information"], matrix, "support information")
            matrices.append(matrix)
        mixture = np.einsum("a,aij->ij", weights, matrices)
        close(r["hull_information"], mixture, "mixture information")
        close(r["surrogate_hull_value"], ld(mixture), "mixture objective")
    witnessed = 0
    if r["upper_bound_witness"]:
        w = r["upper_bound_witness"]
        M, H = np.array(w["hull_information"]), np.array(w["gradient"])
        close(H @ M, np.eye(design.p), "surrogate inverse")
        price, _ = ref.price(H)
        close(price, w["linear_price_excluding_prior"], "independent surrogate price")
        path = tuple(w["priced_selection"])
        close(price, np.trace(H @ (ref.information(path)[1]-design.prior)), "surrogate priced path")
        reconstructed = ld(M) - design.p + np.trace(H @ design.prior) + price
        close(reconstructed, w["surrogate_upper_bound"], "surrogate certificate")
        close(reconstructed, r["surrogate_upper_bound"], "saved surrogate upper")
        if delta < 1:
            close(r["transferred_upper_bound"], reconstructed-design.p*math.log1p(-delta), "spectral transfer")
        witnessed += 1
    if r["prior_aware_witness"]:
        w = r["prior_aware_witness"]
        M, N, H = (np.array(w[k]) for k in ("surrogate_hull_information", "N", "arc_gradient"))
        close(N, design.prior+(M-design.prior)/(1-delta), "prior correction")
        close(H @ N, np.eye(design.p)/(1-delta), "prior-aware inverse")
        price, _ = ref.price(H)
        close(price, w["linear_price_excluding_prior"], "independent corrected price")
        path = tuple(w["priced_selection"])
        close(price, np.trace(H @ (ref.information(path)[1]-design.prior)), "corrected priced path")
        reconstructed = ld(N) - design.p + np.trace(np.linalg.inv(N) @ design.prior) + price
        close(reconstructed, w["true_upper_bound"], "prior-aware certificate")
        close(reconstructed, r["prior_aware_upper_bound"], "saved prior-aware upper")
        witnessed += 1
    bounds = [r[key] for key in ("full_selection_upper_bound", "transferred_upper_bound",
                                 "prior_aware_upper_bound") if r[key] is not None]
    close(r["true_upper_bound"], min(bounds), "reported upper equals completed certificates")
    if enumerate_designs:
        infos = [ref.information(s) for s in combinations(range(design.n), design.k)]
        optimum = max(ld(x[0]) for x in infos)
        assert r["true_upper_bound"] >= optimum-2e-7, (r, optimum)
        assert r["true_lower_bound"] <= optimum+2e-7
        if r["surrogate_upper_bound"] is not None:
            assert r["surrogate_upper_bound"] >= max(ld(x[1]) for x in infos)-2e-7
    if r["status"] == "true_optimal_tolerance":
        assert r["true_gap"] <= 1.1e-6
    return {"status": r["status"], "witnesses": witnessed}


def main():
    started = perf_counter()
    source_bytes = Path(target.__file__).read_bytes()
    rng = np.random.default_rng(120926)
    counts = {name: 0 for name in ("subset_factorizations", "spectral_checks", "dp_prices",
                                   "dense_binary_values", "dense_gradient_directions",
                                   "dense_tangent_checks", "hull_solves", "dense_solves",
                                   "saved_hulls", "witnesses", "invalid_inputs",
                                   "root_fractional_tangents")}
    worst = {"factorization": 0., "dp_price": 0., "dense_gradient": 0.}
    statuses = []
    n, p = 7, 3
    for rho, latent, nugget in ((-.75, 1.3, .7), (.45, 1., 2.), (.0, 1., 1.), (.8, 0., .4)):
        F = rng.normal(size=(n, p))
        B = rng.normal(size=(p, p))
        prior = .2 * np.eye(p) + B.T @ B
        for k in (0, 1, 3, n):
            design = target.NoisyDesign(F, rho, latent, nugget, prior, k)
            dense = target.DenseLiuOracle(design)
            subsets = list(combinations(range(n), k))
            for L in (0, 1, 3, n-1, n+5):
                oracle, ref = target.CalendarOracle(design, L), Reference(design, L)
                matrices = []
                for s in subsets:
                    true, surrogate, C = ref.information(s)
                    residual = np.max(abs(oracle.information(s)-surrogate))
                    worst["factorization"] = max(worst["factorization"], float(residual))
                    close(oracle.information(s), surrogate, "local factorization")
                    close(oracle.residual_covariance(s), C, "normalized residual")
                    close(design.true_information(s), true, "true covariance")
                    if s:
                        error = np.max(abs(np.linalg.eigvalsh(C)-1))
                        assert error <= expected_delta(design, L)+2e-8
                        counts["spectral_checks"] += 1
                    if L >= n-1 or rho == 0 or latent == 0:
                        close(surrogate, true, "exact limit")
                    matrices.append(surrogate)
                    counts["subset_factorizations"] += 1
                for _ in range(2):
                    H = rng.normal(size=(p, p))
                    H = (H+H.T)/2  # Includes indefinite and negative arc weights.
                    brute = max(float(np.trace(H @ (M-prior))) for M in matrices)
                    got, chosen = oracle.price(H)
                    other, _ = ref.price(H)
                    close(got, brute, "brute DP price")
                    close(got, other, "tuple-state DP price")
                    close(got, np.trace(H @ (ref.information(chosen)[1]-prior)), "returned DP path")
                    assert len(chosen) == k and tuple(sorted(set(chosen))) == chosen
                    worst["dp_price"] = max(worst["dp_price"], abs(got-brute))
                    counts["dp_prices"] += 1
                if L in (1, n-1):
                    result = target.solve_hull(design, L, time_limit=2, max_rounds=60)
                    audit = inspect_hull(design, result)
                    statuses.append({"rho": rho, "latent": latent, "k": k, "L": L, **audit})
                    counts["hull_solves"] += 1
                    counts["witnesses"] += audit["witnesses"]
            ref = Reference(design, n-1)
            for s in subsets:
                z = np.zeros(n)
                z[list(s)] = 1
                close(dense.value_gradient(z)[0], ld(ref.information(s)[0]), "binary Liu identity")
                counts["dense_binary_values"] += 1
            for _ in range(3):
                z = rng.uniform(.15, .85, size=n)
                value, gradient = dense.value_gradient(z)
                direction = rng.normal(size=n)
                eps = 1e-6
                difference = (dense.value_gradient(z+eps*direction)[0]-dense.value_gradient(z-eps*direction)[0])/(2*eps)
                worst["dense_gradient"] = max(worst["dense_gradient"], abs(difference-gradient@direction))
                close(difference, gradient@direction, "dense finite difference", atol=2e-6)
                counts["dense_gradient_directions"] += 1
                for _ in range(8):
                    point = rng.uniform(size=n)
                    assert dense.value_gradient(point)[0] <= value+gradient@(point-z)+2e-8
                    counts["dense_tangent_checks"] += 1
            dense_result = target.solve_dense_oa(design, time_limit=2, max_rounds=100)
            optimum = max(ld(ref.information(s)[0]) for s in subsets)
            assert dense_result["lower_bound"] <= optimum+2e-7
            assert dense_result["upper_bound"] >= optimum-2e-7
            close(dense_result["lower_bound"], ld(ref.information(dense_result["selected"])[0]), "dense incumbent")
            counts["dense_solves"] += 1
            strengthened = target.solve_dense_oa(design, time_limit=2, max_rounds=100,
                                                 split_fraction=.99, root_rounds=100,
                                                 initial_selected=tuple(reversed(subsets[0])))
            assert strengthened["lower_bound"] <= optimum+2e-7
            assert strengthened["upper_bound"] >= optimum-2e-7
            close(strengthened["initial_lower_bound"], ld(ref.information(subsets[0])[0]), "warm initial value")
            if strengthened["root_upper_bound"] is not None:
                assert strengthened["root_upper_bound"] >= optimum-2e-7
                tighter = target.DenseLiuOracle(design, .99)
                for _ in range(5):
                    w = rng.dirichlet(np.ones(len(subsets)))
                    point = np.zeros(n)
                    for weight, s in zip(w, subsets):
                        point[list(s)] += weight
                    assert tighter.value_gradient(point)[0] <= strengthened["root_upper_bound"]+2e-7
                    counts["root_fractional_tangents"] += 1
            counts["dense_solves"] += 1
            for split in (.01, .99, .999999):
                other = target.DenseLiuOracle(design, split)
                for s in subsets:
                    z = np.zeros(n)
                    z[list(s)] = 1
                    close(other.value_gradient(z)[0], ld(ref.information(s)[0]), "split-independent binary identity")
                    counts["dense_binary_values"] += 1
    design = target.generic_design(n=8, p=2, k=3, rho=.4, seed=17)
    limits = []
    for options in ({"max_rounds": 0}, {"max_rounds": 1}, {"time_limit": 1e-12},
                    {"max_memory_mb": 1e-9}, {"max_correction_iterations": 1}):
        result = target.solve_hull(design, 3, **options)
        audit = inspect_hull(design, result)
        limits.append({"options": options, **audit})
    for options in ({"max_rounds": 0}, {"max_rounds": 1}, {"time_limit": 1e-12}):
        result = target.solve_dense_oa(design, **options)
        optimum = max(ld(Reference(design, 7).information(s)[0]) for s in combinations(range(8), 3))
        assert result["lower_bound"] <= optimum+2e-7 <= result["upper_bound"]+4e-7
        limits.append({"dense_options": options, "status": result["status"]})
    root_only = target.solve_dense_oa(design, max_rounds=0, root_rounds=100, split_fraction=.99)
    close(root_only["lower_bound"], root_only["initial_lower_bound"], "fractional root never becomes true incumbent")
    assert root_only["status"] == "iteration_limit"
    limits.append({"dense_options": {"max_rounds": 0, "root_rounds": 100}, "status": root_only["status"]})
    # Prove that memory refusal occurs before even the seed objective is evaluated.
    with patch.object(target.NoisyDesign, "true_objective", side_effect=AssertionError("allocated before refusal")):
        refused = target.solve_hull(design, 3, max_memory_mb=1e-9)
        assert refused.status == "memory_limit" and refused.true_lower_bound is None
    limits.append({"memory_preflight_skips_objective_evaluation": True})
    oracle = target.CalendarOracle(design, 2)
    ref = Reference(design, 2)
    for size in range(design.n+1):
        for s in combinations(range(design.n), size):
            close(oracle.information(s), ref.information(s)[1], "information outside priced cardinality")
            counts["subset_factorizations"] += 1
    for bad in ((0, 0), (-1,), (8,), (.5,), (1.0,)):
        for method in (design.true_information, oracle.information, oracle.residual_covariance):
            try:
                method(bad)
            except ValueError:
                counts["invalid_inputs"] += 1
            else:
                raise AssertionError(("invalid subset accepted", method.__name__, bad))
    for bad in ((0, 0, 1), (0, 1), (0, 1, 9), (0, 1, 2.0)):
        try:
            target.solve_dense_oa(design, initial_selected=bad)
        except ValueError:
            counts["invalid_inputs"] += 1
        else:
            raise AssertionError(("invalid dense start accepted", bad))
    for split in (0., 1., -1., math.nan):
        try:
            target.DenseLiuOracle(design, split)
        except ValueError:
            counts["invalid_inputs"] += 1
        else:
            raise AssertionError(("invalid split accepted", split))
    with patch.object(target.CalendarOracle, "price", side_effect=target.TimeBudgetExceeded("injected deadline")):
        interrupted = target.solve_hull(design, 3)
        assert interrupted.status == "time_limit" and interrupted.surrogate_upper_bound is None
        inspect_hull(design, interrupted)
    limits.append({"pricing_deadline_preserves_true_baseline": True})
    original_price = target.CalendarOracle.price
    pricing_count = 0

    def interrupt_after_certificate(self, H, **kwargs):
        nonlocal pricing_count
        pricing_count += 1
        if pricing_count >= 2:
            raise target.TimeBudgetExceeded("injected deadline after completed pricing")
        return original_price(self, H, **kwargs)

    with patch.object(target.CalendarOracle, "price", interrupt_after_certificate):
        interrupted = target.solve_hull(design, 3)
        assert interrupted.surrogate_upper_bound is not None
        inspect_hull(design, interrupted)
    limits.append({"later_pricing_deadline_preserves_completed_certificate": True})
    with patch.object(target, "minimize", side_effect=target.TimeBudgetExceeded("injected correction deadline")):
        corrected, success, message = target.correct_weights([np.eye(2), 2*np.eye(2)],
                                                             np.array([.25, .75]), math.inf, 10)
        close(corrected, [.25, .75], "correction preserves feasible mixture")
        assert not success and message == "time_limit"
    limits.append({"correction_deadline_preserves_feasible_weights": True})
    for size in (1, 2, 6):
        for k in sorted(set((0, size//2, size))):
            zero = target.NoisyDesign(np.zeros((size, 2)), -.6, 1., 1., np.eye(2), k)
            result = target.solve_hull(zero, 3, time_limit=2)
            audit = inspect_hull(zero, result)
            assert result.status == "true_optimal_tolerance" and result.true_gap == 0
            counts["hull_solves"] += 1
            counts["witnesses"] += audit["witnesses"]
    saved = HERE / "results/noisy-markov-design-benchmark.json"
    saved_audit = []
    if saved.exists():
        content = json.loads(saved.read_text())
        for row in content["results"]:
            d = target.NoisyDesign(np.array(row["F"]), row["rho"], row["latent_variance"],
                                   row["nugget_variance"], np.array(row["prior"]), row["k"])
            for result in row["hulls"]:
                audit = inspect_hull(d, result, enumerate_designs=math.comb(d.n, d.k)<=1000)
                saved_audit.append({"n": d.n, "k": d.k, "L": result["L"], **audit})
                counts["saved_hulls"] += 1
                counts["witnesses"] += audit["witnesses"]
            for key, dense in row.items():
                if "dense" not in key or not isinstance(dense, dict) or "lower_bound" not in dense:
                    continue
                ref = Reference(d, 0)
                close(dense["lower_bound"], ld(ref.information(dense["selected"])[0]), "saved dense incumbent")
                if "initial_selected" in dense:
                    close(dense["initial_lower_bound"], ld(ref.information(dense["initial_selected"])[0]), "saved dense initial value")
                if "enumerated_true_optimum" in row:
                    optimum = max(ld(ref.information(s)[0]) for s in combinations(range(d.n), d.k))
                    close(optimum, row["enumerated_true_optimum"], "saved enumerated optimum")
                    assert dense["lower_bound"] <= optimum+2e-7 <= dense["upper_bound"]+4e-7
    assert Path(target.__file__).read_bytes() == source_bytes, "Implementation changed during review run; rerun."
    report = {"status": "passed", "seed": 120926, "python": platform.python_version(),
              "numpy": np.__version__, "scipy": scipy.__version__,
              "source_sha256": sha256(source_bytes).hexdigest(),
              "reviewer_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
              "saved_benchmark_sha256": sha256(saved.read_bytes()).hexdigest() if saved.exists() else None,
              "wall_seconds": perf_counter()-started, "counts": counts, "worst_absolute_errors": worst,
              "hull_statuses": statuses, "limit_checks": limits, "saved_audit": saved_audit,
              "limitations": ["Floating point checks, not interval certification.",
                              "Saved dense OA bounds on nonenumerated cases have no retained cut/solver proof.",
                              "Memory checks are preflight estimates; operating-system RSS is not constrained."]}
    REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({k: report[k] for k in ("status", "wall_seconds", "counts", "worst_absolute_errors", "limit_checks")}, indent=2))


if __name__ == "__main__":
    main()
