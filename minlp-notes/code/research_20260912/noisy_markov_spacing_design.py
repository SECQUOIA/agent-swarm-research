"""Compact minimum-gap calendar oracle and numerical surrogate hull producer.

The producer reports a true-evaluated feasible incumbent and a SURROGATE upper
bound. It deliberately supplies no transferred true upper bound; independent
gap-aware certification consumes the saved paths and hull matrix separately.
"""

from dataclasses import asdict
from itertools import combinations
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
from time import perf_counter

import numpy as np

from noisy_markov_design import (
    NoisyDesign, TimeBudgetExceeded, check_time, correct_weights, logdet,
    validated_subset,
)
from noisy_markov_kinetics_probe import reaction_data
from noisy_markov_spacing_bound import spacing_mask_count


def shape_estimate(design: NoisyDesign, L: int, gap: int, max_paths: int = 101) -> dict:
    if any(isinstance(v, bool) or not isinstance(v, (int, np.integer)) for v in (L, gap)):
        raise ValueError("integer L and minimum gap required")
    if L < 0 or gap < 1:
        raise ValueError("require L>=0 and minimum_gap>=1")
    if design.k > (design.n+gap-1)//gap:
        raise ValueError("exact count exceeds minimum-gap capacity")
    L = min(int(L), design.n-1)
    width = max(L, min(int(gap)-1, design.n-1))
    masks = spacing_mask_count(width, int(gap))
    states = design.n*(design.k+1)*masks
    arc_bytes = 8*design.n*masks*design.p**2
    dp_bytes = 5*states + 16*(design.k+1)*masks
    workspace = (8*design.n*masks + 64*design.n**2 + 192*masks
                 + 64*max_paths**2 + 64*max_paths*design.n + 8*max_paths*design.p**2)
    return {"information_L": L, "cooldown_width": width, "minimum_gap": int(gap),
            "compact_mask_count": masks, "unrestricted_mask_count": 1 << width,
            "count_layer_state_upper_bound": states,
            "arc_matrix_bytes": arc_bytes, "dp_array_bytes": dp_bytes,
            "estimated_workspace_bytes": arc_bytes+dp_bytes+workspace}


def enforce_memory(estimate: dict, limit_mb: float) -> None:
    if not math.isfinite(limit_mb) or limit_mb <= 0:
        raise ValueError("memory limit must be positive and finite")
    if estimate["estimated_workspace_bytes"] > limit_mb*2**20:
        raise MemoryError("compact-state workspace estimate exceeds limit: " + str(estimate))


def separated_masks(width: int, gap: int) -> tuple[int, ...]:
    """Generate valid masks directly, without scanning a 2**width array."""
    masks = []

    def extend(first: int, mask: int) -> None:
        masks.append(mask)
        for position in range(first, width):
            extend(position+gap, mask | (1 << position))

    extend(0, 0)
    return tuple(sorted(masks))


class SpacingCalendarOracle:
    def __init__(self, design: NoisyDesign, L: int, minimum_gap: int, *,
                 deadline: float = math.inf, max_memory_mb: float = 256,
                 max_paths: int = 101):
        self.design = design
        self.estimate = shape_estimate(design, L, minimum_gap, max_paths)
        enforce_memory(self.estimate, max_memory_mb)
        self.L = self.estimate["information_L"]
        self.width = self.estimate["cooldown_width"]
        self.gap = int(minimum_gap)
        self.masks = separated_masks(self.width, self.gap)
        assert len(self.masks) == self.estimate["compact_mask_count"]
        self.index = {mask: i for i, mask in enumerate(self.masks)}
        self.trim = (1 << self.width)-1
        forbidden_recent = (1 << min(self.width, self.gap-1))-1
        self.skip = np.empty(len(self.masks), dtype=np.int32)
        self.choose = np.full(len(self.masks), -1, dtype=np.int32)
        self.wait = np.empty(len(self.masks), dtype=np.int32)
        for i, mask in enumerate(self.masks):
            shifted = (mask << 1) & self.trim
            self.skip[i] = self.index[shifted]
            if not mask & forbidden_recent:
                target = shifted | (1 if self.width else 0)
                self.choose[i] = self.index[target]
            age = (mask & -mask).bit_length() if mask else self.gap
            self.wait[i] = min(design.n, max(0, self.gap-age))
        check_time(deadline)
        self.R = design.covariance()
        self.weights = np.zeros((design.n, len(self.masks), design.p, design.p))
        for t in range(design.n):
            check_time(deadline)
            valid_prefix = 1 << min(t, self.width)
            for i, mask in enumerate(self.masks):
                if mask >= valid_prefix:
                    break
                if i % 64 == 0:
                    check_time(deadline)
                if self.choose[i] < 0:
                    continue
                history = [j for j in range(max(0, t-self.L), t)
                           if mask & (1 << (t-1-j))]
                adjusted = design.F[t].copy()
                variance = float(self.R[t, t])
                if history:
                    cov = self.R[history, t]
                    regression = np.linalg.solve(self.R[np.ix_(history, history)], cov)
                    variance -= float(cov @ regression)
                    adjusted -= regression @ design.F[history]
                if variance <= 0:
                    raise np.linalg.LinAlgError("nonpositive local conditional variance")
                self.weights[t, i] = np.outer(adjusted, adjusted)/variance
        self.last_pricing = {}

    def validate_selection(self, selected: tuple[int, ...], exact_count: bool = False) -> tuple[int, ...]:
        selected = tuple(sorted(validated_subset(selected, self.design.n)))
        if any(isinstance(i, (bool, np.bool_)) for i in selected):
            raise ValueError("boolean values are not calendar indices")
        if any(b-a < self.gap for a, b in zip(selected[:-1], selected[1:])):
            raise ValueError("selected calendar indices violate minimum gap")
        if exact_count and len(selected) != self.design.k:
            raise ValueError("selected subset must have exactly k entries")
        return selected

    def information(self, selected: tuple[int, ...]) -> np.ndarray:
        selected_set = set(self.validate_selection(selected))
        state = self.index[0]
        J = self.design.prior.copy()
        for t in range(self.design.n):
            if t in selected_set:
                J += self.weights[t, state]
                state = int(self.choose[state])
                if state < 0:
                    raise RuntimeError("validated selection encountered a forbidden transition")
            else:
                state = int(self.skip[state])
        return J

    def price(self, gradient: np.ndarray, *, deadline: float = math.inf) -> tuple[float, tuple[int, ...]]:
        started = perf_counter()
        n, k, count = self.design.n, self.design.k, len(self.masks)
        arc_scores = np.einsum("ij,tsji->ts", gradient, self.weights)
        values = np.full((k+1, count), -np.inf)
        values[0, self.index[0]] = 0
        parents = np.full((n, k+1, count), -1, dtype=np.int32)
        actions = np.full((n, k+1, count), -1, dtype=np.int8)
        visited = 0
        for t in range(n):
            check_time(deadline)
            next_values = np.full_like(values, -np.inf)
            for q in range(min(k, t)+1):
                for state in np.flatnonzero(np.isfinite(values[q])):
                    if int(state) % 128 == 0:
                        check_time(deadline)
                    span = n-t-int(self.wait[state])
                    capacity = max(0, (span+self.gap-1)//self.gap)
                    if q+capacity < k:
                        continue
                    visited += 1
                    value = values[q, state]
                    target = int(self.skip[state])
                    if value > next_values[q, target]:
                        next_values[q, target] = value
                        parents[t, q, target], actions[t, q, target] = state, 0
                    target = int(self.choose[state])
                    if q < k and target >= 0:
                        candidate = value+arc_scores[t, state]
                        if candidate > next_values[q+1, target]:
                            next_values[q+1, target] = candidate
                            parents[t, q+1, target], actions[t, q+1, target] = state, 1
            values = next_values
        state = int(np.argmax(values[k]))
        maximum = float(values[k, state])
        if not math.isfinite(maximum):
            raise RuntimeError("minimum-gap count DP found no feasible path")
        q, selected = k, []
        for t in range(n-1, -1, -1):
            take = int(actions[t, q, state])
            previous = int(parents[t, q, state])
            if take not in (0, 1) or previous < 0:
                raise RuntimeError("invalid compact DP predecessor")
            if take:
                selected.append(t)
            state, q = previous, q-take
        selected = self.validate_selection(tuple(reversed(selected)), exact_count=True)
        self.last_pricing = {"visited_states": visited, "wall_seconds": perf_counter()-started}
        return maximum, selected


def produce_spacing_hull(design: NoisyDesign, L: int, minimum_gap: int, *,
                         time_limit: float = 30, max_memory_mb: float = 256,
                         max_rounds: int = 100, hull_gap: float = 1e-6) -> dict:
    if not 0 < time_limit <= 30 or max_rounds < 0 or not math.isfinite(hull_gap) or hull_gap <= 0:
        raise ValueError("invalid time, round, or gap limit")
    started = perf_counter()
    deadline = started+time_limit
    estimate = shape_estimate(design, L, minimum_gap, max_rounds+1)
    result = {"status": "iteration_limit", "n": design.n, "p": design.p, "k": design.k,
              "L": estimate["information_L"], "minimum_gap": int(minimum_gap),
              "cooldown_width": estimate["cooldown_width"], "memory_estimate": estimate,
              "surrogate_hull_value": None, "surrogate_upper_bound": None,
              "surrogate_hull_gap": None, "true_lower_bound": None,
              "true_upper_bound": None, "true_gap": None, "selected": None,
              "hull_support": [], "hull_information": None, "upper_bound_witness": None,
              "pricing_history": [], "pricing_rounds": 0, "correction_failures": 0,
              "last_correction_message": None,
              "bound_scope": "surrogate hull bound only; independent minimum-gap true certificate pending"}
    paths, matrices, weights = [], [], np.empty(0)
    try:
        enforce_memory(estimate, max_memory_mb)
        seed = tuple(int(t) for t in np.linspace(0, design.n-1, design.k))
        if any(b-a < minimum_gap for a, b in zip(seed[:-1], seed[1:])):
            raise RuntimeError("evenly spaced seed violates the minimum gap")
        result["selected"], result["true_lower_bound"] = seed, design.true_objective(seed)
        oracle = SpacingCalendarOracle(design, L, minimum_gap, deadline=deadline,
                                       max_memory_mb=max_memory_mb, max_paths=max_rounds+1)
        oracle.validate_selection(seed, exact_count=True)
        paths, matrices, weights = [seed], [oracle.information(seed)], np.ones(1)
        result["surrogate_hull_value"] = logdet(matrices[0])
        for iteration in range(max_rounds):
            check_time(deadline)
            M = np.einsum("a,aij->ij", weights, np.array(matrices))
            value = logdet(M)
            gradient = np.linalg.solve(M, np.eye(design.p))
            price, selected = oracle.price(gradient, deadline=deadline)
            candidate_upper = value-design.p+float(np.trace(gradient @ design.prior))+price
            if result["surrogate_upper_bound"] is None or candidate_upper < result["surrogate_upper_bound"]:
                result["surrogate_upper_bound"] = candidate_upper
                result["upper_bound_witness"] = {
                    "hull_information": M.tolist(), "gradient": gradient.tolist(),
                    "hull_logdet": value, "linear_price_excluding_prior": price,
                    "priced_selection": selected, "surrogate_upper_bound": candidate_upper}
            oracle.validate_selection(selected, exact_count=True)
            true_value = design.true_objective(selected)
            if true_value > result["true_lower_bound"]:
                result["true_lower_bound"], result["selected"] = true_value, selected
            result["surrogate_hull_value"] = value
            result["pricing_rounds"] += 1
            result["pricing_history"].append({
                "round": iteration+1, "elapsed_seconds": perf_counter()-started,
                "surrogate_hull_value": value, "surrogate_upper_bound": result["surrogate_upper_bound"],
                "true_lower_bound": result["true_lower_bound"], **oracle.last_pricing})
            if result["surrogate_upper_bound"] < value-1e-7*max(1, abs(value)):
                result["status"] = "numerical_surrogate_bound_inconsistency"
                break
            if result["surrogate_upper_bound"]-value <= hull_gap:
                result["status"] = "surrogate_hull_optimal_tolerance"
                break
            if selected not in paths:
                paths.append(selected)
                matrices.append(oracle.information(selected))
                weights = np.append(weights, 0.0)
            weights, success, message = correct_weights(matrices, weights, deadline, 100)
            result["last_correction_message"] = message
            result["correction_failures"] += int(not success)
            corrected = logdet(np.einsum("a,aij->ij", weights, np.array(matrices)))
            result["surrogate_hull_value"] = corrected
            if message == "time_limit":
                result["status"] = "time_limit"
                break
            if corrected <= value+1e-12:
                result["status"] = "correction_stalled"
                break
    except TimeBudgetExceeded:
        result["status"] = "time_limit"
    except MemoryError as error:
        result["status"], result["exception_message"] = "memory_limit", str(error)
    if len(weights):
        result["hull_information"] = np.einsum("a,aij->ij", weights, np.array(matrices)).tolist()
        result["hull_support"] = [{"selected": path, "weight": float(weight), "information": matrix.tolist()}
                                  for path, weight, matrix in zip(paths, weights, matrices)]
    if result["surrogate_upper_bound"] is not None:
        result["surrogate_hull_gap"] = max(0, result["surrogate_upper_bound"]-result["surrogate_hull_value"])
    result["wall_seconds"] = perf_counter()-started
    return result


def validate() -> dict:
    rng = np.random.default_rng(17)
    cases = [(8, 2, 0, 3), (8, 2, 3, 3), (9, 3, 1, 3), (10, 3, 4, 3),
             (8, 1, 2, 3), (6, 6, 0, 1), (8, 2, 7, 4), (8, 2, 0, 0)]
    matrix_error = price_error = 0.0
    checks = []
    for n, gap, L, k in cases:
        design = NoisyDesign(rng.normal(size=(n, 3)), -0.4, 1, 1, 0.1*np.eye(3), k)
        oracle = SpacingCalendarOracle(design, L, gap)
        R = design.covariance()
        allowed = []
        for size in range((n+gap-1)//gap+1):
            for selected in combinations(range(n), size):
                if any(b-a < gap for a, b in zip(selected[:-1], selected[1:])):
                    continue
                A, variances = np.eye(size), np.empty(size)
                for i, t in enumerate(selected):
                    history = [j for j in range(i) if t-selected[j] <= L]
                    variances[i] = R[t, t]
                    if history:
                        indices = [selected[j] for j in history]
                        b = np.linalg.solve(R[np.ix_(indices, indices)], R[indices, t])
                        A[i, history] = -b
                        variances[i] -= float(R[t, indices] @ b)
                reference = design.prior.copy()
                if selected:
                    transformed = A @ design.F[list(selected)]
                    reference += transformed.T @ (transformed/variances[:, None])
                actual = oracle.information(selected)
                matrix_error = max(matrix_error, float(np.max(abs(actual-reference))))
                if size == k:
                    allowed.append((selected, actual))
        for _ in range(3):
            gradient = rng.normal(size=(3, 3))
            gradient = (gradient+gradient.T)/2  # Include indefinite linear prices.
            price, selected = oracle.price(gradient)
            exact = max(float(np.trace(gradient @ (J-design.prior))) for _, J in allowed)
            price_error = max(price_error, abs(price-exact))
            oracle.validate_selection(selected, exact_count=True)
        produced = produce_spacing_hull(design, L, gap, time_limit=5)
        assert produced["surrogate_upper_bound"] >= max(logdet(J) for _, J in allowed)-1e-7
        assert produced["true_upper_bound"] is None and produced["true_gap"] is None
        oracle.validate_selection(produced["selected"], exact_count=True)
        checks.append({"n": n, "gap": gap, "L": L, "k": k,
                       "compact_masks": len(oracle.masks), "feasible_size_k_subsets": len(allowed),
                       "producer_status": produced["status"]})
    assert matrix_error < 1e-10 and price_error < 1e-9
    refused = produce_spacing_hull(NoisyDesign(np.ones((96, 3)), 0.4, 1, 1, np.eye(3), 32),
                                  30, 2, max_memory_mb=1)
    assert refused["status"] == "memory_limit" and refused["true_lower_bound"] is None
    try:
        oracle.validate_selection((0, 1))
    except ValueError:
        pass
    else:
        raise AssertionError("minimum-gap violation accepted")
    return {"status": "passed", "max_information_error": matrix_error,
            "max_linear_pricing_error": price_error, "cases": checks,
            "memory_refusal": refused["status"]}


def first_case(output: Path) -> None:
    n, gap, L = 96, 2, 13
    times, F, kinetics = reaction_data(n, "fast")
    design = NoisyDesign(F, math.sqrt(0.4), 0.00125, 0.00125, 0.01*np.eye(3), 32)
    payload = {"metadata": {
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "numpy_version": np.__version__, "time_limit": 30, "max_memory_mb": 256,
        "blas_environment": {key: os.environ.get(key) for key in (
            "OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")},
        "scope": "surrogate hull producer with validated minimum-gap paths; transferred true upper bound intentionally omitted",
        "physical_grid_relation": "rho=sqrt(.4) at spacing .125 matches rho=.4 at spacing .25 up to floating-point representation; gap2 means physical gap .25",
        "noise_model": "stylized stationary latent AR1 plus nugget; not measured source covariance",
    }, "results": []}
    record = {"n": n, "p": 3, "k": 32, "minimum_gap": gap,
              "rho": design.rho, "latent_variance": design.latent_variance,
              "nugget_variance": design.nugget_variance,
              "F": F.tolist(), "prior": design.prior.tolist(), "kinetics": kinetics, "hulls": []}
    payload["results"].append(record)
    started = perf_counter()
    try:
        result = produce_spacing_hull(design, L, gap, time_limit=30, max_memory_mb=256)
    except Exception as error:
        result = {"status": "exception", "L": L, "minimum_gap": gap,
                  "exception_type": type(error).__name__, "exception_message": str(error),
                  "wall_seconds": perf_counter()-started}
    if result.get("selected") is not None:
        result["selected_times"] = times[list(result["selected"])].tolist()
    record["hulls"].append(result)
    temporary = output.with_suffix(output.suffix+".tmp")
    temporary.write_text(json.dumps(payload, indent=2, allow_nan=False)+"\n")
    temporary.replace(output)
    print(json.dumps({key: result[key] for key in (
        "status", "wall_seconds", "pricing_rounds", "surrogate_hull_value", "surrogate_upper_bound",
        "surrogate_hull_gap", "true_lower_bound", "memory_estimate") if key in result}), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "first-case"))
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("results") / "noisy-markov-spacing-kinetics-probe.json")
    args = parser.parse_args()
    if args.command == "validate":
        print(json.dumps(validate(), indent=2))
    else:
        first_case(args.output)


if __name__ == "__main__":
    main()
