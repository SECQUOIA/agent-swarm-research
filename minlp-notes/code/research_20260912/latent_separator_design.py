"""Exact latent-separator pattern hull for noisy scalar AR(1) design.

Latent anchors make conditional observation blocks independent. Each block's
complete selection patterns contribute additive augmented information; eliminating
the anchor nuisance variables recovers the true selected marginal information.
The concave logdet-Schur objective yields numerical support-price upper bounds.
This isolated prototype does not change the reviewed calendar or dense solvers.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import combinations
import json
import math
import os
from pathlib import Path
from time import perf_counter

import numpy as np
from scipy.optimize import minimize

from noisy_markov_design import NoisyDesign, TimeBudgetExceeded, check_time, logdet


HERE = Path(__file__).resolve().parent


def integer(value, name, lower=0):
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)) or value < lower:
        raise ValueError(f"{name} must be an integer >= {lower}")
    return int(value)


def subset(selected, n):
    selected = tuple(selected)
    if len(set(selected)) != len(selected) or any(
        isinstance(i, bool) or not isinstance(i, (int, np.integer)) or not 0 <= i < n
        for i in selected
    ):
        raise ValueError("A subset must contain distinct valid integer indices")
    return tuple(sorted(int(i) for i in selected))


def one_minus_even_power(rho, distance):
    if distance == 0:
        return 0.
    if rho == 0:
        return 1.
    return -math.expm1(2*distance*math.log(abs(rho)))


def schur_value_gradient(M, p):
    """Return f(M), its Schur information, nuisance minimizer, and PSD gradient."""
    M = (np.asarray(M)+np.asarray(M).T)/2
    if M.shape[0] == p:
        nuisance = np.empty((0, p))
        information = M.copy()
    else:
        nuisance = -np.linalg.solve(M[p:, p:], M[p:, :p])
        information = M[:p, :p]+M[:p, p:]@nuisance
    information = (information+information.T)/2
    value = logdet(information)
    inverse = np.linalg.solve(information, np.eye(p))
    E = np.vstack((np.eye(p), nuisance))
    gradient = E@inverse@E.T
    return value, information, nuisance, (gradient+gradient.T)/2


@dataclass
class Block:
    times: tuple[int, ...]
    anchor_columns: tuple[int, ...]
    columns: np.ndarray
    H: np.ndarray
    D: np.ndarray
    patterns: np.ndarray
    counts: np.ndarray


def layout(design, block_size):
    b = min(integer(block_size, "block_size", 1), design.n)
    blocks = tuple(tuple(range(t, min(t+b, design.n))) for t in range(0, design.n, b))
    anchors = tuple(times[-1] for times in blocks[:-1]) if (
        design.latent_variance > 0 and design.rho != 0) else ()
    return b, blocks, anchors


def workspace_estimate(design, block_size, max_paths):
    b, blocks, anchors = layout(design, block_size)
    # This is a workspace estimate, not a process-RSS guarantee.
    patterns = sum(1 << len(times) for times in blocks)
    dimension = design.p+len(anchors)
    pattern_bytes = 8*patterns*(design.p+2)**2+16*patterns
    hull_bytes = 16*max_paths*dimension**2+64*max_paths**2+64*max_paths*design.n
    ancillary = 64*design.n**2+32*design.n*b+64*dimension**2
    return {"block_size": b, "block_count": len(blocks), "anchor_count": len(anchors),
            "pattern_count": patterns, "augmented_dimension": dimension,
            "estimated_workspace_bytes": pattern_bytes+hull_bytes+ancillary}


class SeparatorOracle:
    def __init__(self, design, block_size, *, deadline=math.inf,
                 max_memory_mb=256, max_paths=101):
        integer(design.k, "cardinality")
        integer(max_paths, "max_paths", 1)
        if not math.isfinite(max_memory_mb) or max_memory_mb <= 0:
            raise ValueError("Positive finite memory limit required")
        self.design = design
        self.estimate = workspace_estimate(design, block_size, max_paths)
        if self.estimate["estimated_workspace_bytes"] > max_memory_mb*2**20:
            raise MemoryError("Latent separator workspace estimate exceeds the memory limit")
        self.block_size, times_by_block, self.anchors = layout(design, block_size)
        self.dimension = design.p+len(self.anchors)
        self.prior = np.zeros((self.dimension, self.dimension))
        self.prior[:design.p, :design.p] = design.prior
        if self.anchors:
            precision = np.zeros((len(self.anchors), len(self.anchors)))
            precision[0, 0] = 1/design.latent_variance
            for i in range(1, len(self.anchors)):
                gap = self.anchors[i]-self.anchors[i-1]
                a = design.rho**gap
                variance = design.latent_variance*one_minus_even_power(design.rho, gap)
                precision[i-1, i-1] += a*a/variance
                precision[i, i] += 1/variance
                precision[i, i-1] = precision[i-1, i] = -a/variance
            self.prior[design.p:, design.p:] = precision
        self.blocks = []
        for block_index, times in enumerate(times_by_block):
            check_time(deadline)
            left = block_index-1 if self.anchors and block_index else None
            right = block_index if self.anchors and block_index < len(self.anchors) else None
            anchor_columns = tuple(i for i in (left, right) if i is not None)
            H, D = self.conditional_block(times, left, right)
            T = np.hstack((design.F[list(times)], H))
            columns = np.array(tuple(range(design.p))
                               +tuple(design.p+i for i in anchor_columns), dtype=int)
            patterns = np.zeros((1 << len(times), len(columns), len(columns)))
            counts = np.array([mask.bit_count() for mask in range(1 << len(times))], dtype=int)
            for mask in range(1, 1 << len(times)):
                if mask % 64 == 0:
                    check_time(deadline)
                rows = [i for i in range(len(times)) if mask >> i & 1]
                Ts = T[rows]
                contribution = Ts.T@np.linalg.solve(D[np.ix_(rows, rows)], Ts)
                patterns[mask] = (contribution+contribution.T)/2
            self.blocks.append(Block(times, anchor_columns, columns, H, D, patterns, counts))

    def conditional_block(self, times, left_column, right_column):
        design = self.design
        rho, P, r = design.rho, design.latent_variance, design.nugget_variance
        left = self.anchors[left_column] if left_column is not None else None
        right = self.anchors[right_column] if right_column is not None else None
        columns = [x for x in (left, right) if x is not None]
        H = np.zeros((len(times), len(columns)))
        if not self.anchors and (P == 0 or rho == 0):
            return H, (P+r)*np.eye(len(times))
        for i, t in enumerate(times):
            if left is None and right is not None:
                H[i, 0] = rho**(right-t)
            elif right is None and left is not None:
                H[i, 0] = rho**(t-left)
            elif left is not None and right is not None:
                denominator = one_minus_even_power(rho, right-left)
                H[i, 0] = rho**(t-left)*one_minus_even_power(rho, right-t)/denominator
                H[i, 1] = rho**(right-t)*one_minus_even_power(rho, t-left)/denominator
        D = np.zeros((len(times), len(times)))
        for i, t in enumerate(times):
            for j in range(i, len(times)):
                s = times[j]
                value = P*rho**(s-t)
                if left is not None:
                    value *= one_minus_even_power(rho, t-left)
                if right is not None:
                    value *= one_minus_even_power(rho, right-s)
                if left is not None and right is not None:
                    value /= one_minus_even_power(rho, right-left)
                D[i, j] = D[j, i] = value
            D[i, i] += r
        return H, D

    def matrix(self, selected):
        selected = set(subset(selected, self.design.n))
        M = self.prior.copy()
        for block in self.blocks:
            mask = sum(1 << i for i, t in enumerate(block.times) if t in selected)
            M[np.ix_(block.columns, block.columns)] += block.patterns[mask]
        return (M+M.T)/2

    def price(self, gradient, *, deadline=math.inf):
        """Exact-count combinatorial pricing in floating-point arc arithmetic."""
        gradient = np.asarray(gradient)
        if gradient.shape != (self.dimension, self.dimension) or not np.isfinite(gradient).all():
            raise ValueError("Invalid augmented gradient")
        k = self.design.k
        values = np.full(k+1, -np.inf)
        values[0] = 0.
        predecessors = []
        for block in self.blocks:
            check_time(deadline)
            local = gradient[np.ix_(block.columns, block.columns)]
            scores = np.einsum("ij,mji->m", local, block.patterns)
            choices = []
            for count in range(min(len(block.times), k)+1):
                masks = np.flatnonzero(block.counts == count)
                mask = int(masks[np.argmax(scores[masks])])
                choices.append((count, mask, float(scores[mask])))
            following = np.full(k+1, -np.inf)
            previous = np.full((k+1, 2), -1, dtype=int)
            for used in range(k+1):
                if not math.isfinite(values[used]):
                    continue
                for count, mask, score in choices:
                    if used+count <= k and values[used]+score > following[used+count]:
                        following[used+count] = values[used]+score
                        previous[used+count] = (used, mask)
            values = following
            predecessors.append(previous)
        if not math.isfinite(values[k]):
            raise ArithmeticError("Cardinality DP has no feasible terminal state")
        count, selected, masks = k, [], []
        for block, previous in zip(reversed(self.blocks), reversed(predecessors)):
            count, mask = map(int, previous[count])
            if count < 0 or mask < 0:
                raise ArithmeticError("Invalid DP predecessor")
            masks.append(mask)
            selected.extend(t for i, t in enumerate(block.times) if mask >> i & 1)
        selected = tuple(sorted(selected))
        if len(selected) != k or count != 0:
            raise ArithmeticError("DP reconstruction violated cardinality")
        return float(values[k]), selected, tuple(reversed(masks))


def correct_weights(matrices, weights, p, deadline, max_iterations):
    blocks = np.array(matrices)
    best = np.asarray(weights).copy()
    best_value = schur_value_gradient(np.einsum("a,aij->ij", best, blocks), p)[0]

    def objective(w):
        nonlocal best, best_value
        check_time(deadline)
        M = np.einsum("a,aij->ij", w, blocks)
        value, _, _, gradient = schur_value_gradient(M, p)
        feasible = np.maximum(w, 0)
        if feasible.sum() <= 0:
            raise ArithmeticError("No positive simplex correction weight")
        feasible /= feasible.sum()
        feasible_value = schur_value_gradient(np.einsum("a,aij->ij", feasible, blocks), p)[0]
        if feasible_value > best_value:
            best, best_value = feasible.copy(), feasible_value
        return -value, -np.einsum("ij,aji->a", gradient, blocks)

    try:
        result = minimize(objective, weights, jac=True, method="SLSQP",
                          bounds=[(0., 1.)]*len(weights),
                          constraints={"type": "eq", "fun": lambda w: w.sum()-1,
                                       "jac": lambda w: np.ones(len(w))},
                          options={"ftol": 1e-11, "maxiter": max_iterations})
        return best, bool(result.success), str(result.message)
    except TimeBudgetExceeded:
        return best, False, "time_limit"


def solve_separator(design, block_size, *, time_limit=30., true_gap=1e-6,
                    hull_gap=1e-6, max_rounds=100, max_correction_iterations=200,
                    max_memory_mb=256., initial_selected=None):
    integer(max_rounds, "max_rounds", 1)
    integer(max_correction_iterations, "max_correction_iterations", 1)
    if not math.isfinite(time_limit) or not 0 < time_limit <= 30:
        raise ValueError("Time limit must be in (0,30]")
    if any(not math.isfinite(v) or v <= 0 for v in (true_gap, hull_gap, max_memory_mb)):
        raise ValueError("Gap tolerances and memory limit must be positive and finite")
    integer(design.k, "cardinality")
    started, status = perf_counter(), "iteration_limit"
    deadline = started+time_limit
    estimate = workspace_estimate(design, block_size, max_rounds+1)
    result = {"status": status, "n": design.n, "p": design.p, "k": design.k,
              "block_size": estimate["block_size"], "workspace_estimate": estimate,
              "numerical_bound_scope": "Floating-point algebra and pricing; exact certificates are separate",
              "true_lower_bound": None, "true_upper_bound": None, "true_gap": None,
              "selected": None, "hull_value": None, "hull_gap": None,
              "pricing_rounds": 0, "generated_paths": 0, "correction_failures": 0,
              "setup_seconds": 0., "pricing_seconds": 0., "correction_seconds": 0.,
              "best_tangent_witness": None, "hull_matrix": None, "hull_support": []}
    if estimate["estimated_workspace_bytes"] > max_memory_mb*2**20:
        result.update(status="memory_limit", wall_seconds=perf_counter()-started)
        return result
    seed = (tuple(np.linspace(0, design.n-1, design.k, dtype=int))
            if initial_selected is None else subset(initial_selected, design.n))
    seed = subset(seed, design.n)
    if len(seed) != design.k:
        raise ValueError("Initial selection must satisfy the exact cardinality")
    lower, selected = design.true_objective(seed), seed
    upper = design.true_objective(tuple(range(design.n)))
    full_upper = upper
    paths, matrices, weights = [], [], np.empty(0)
    hull_value, message, oracle = None, None, None
    try:
        oracle = SeparatorOracle(design, block_size, deadline=deadline,
                                 max_memory_mb=max_memory_mb, max_paths=max_rounds+1)
        result["setup_seconds"] = perf_counter()-started
        paths, matrices, weights = [seed], [oracle.matrix(seed)], np.ones(1)
        for _ in range(max_rounds):
            check_time(deadline)
            M = np.einsum("a,aij->ij", weights, np.array(matrices))
            hull_value, J, nuisance, gradient = schur_value_gradient(M, design.p)
            price_start = perf_counter()
            price, path, masks = oracle.price(gradient, deadline=deadline)
            result["pricing_seconds"] += perf_counter()-price_start
            result["pricing_rounds"] += 1
            prior_trace = float(np.einsum("ij,ji", gradient, oracle.prior))
            candidate_upper = hull_value-design.p+prior_trace+price
            if result["best_tangent_witness"] is None or candidate_upper < result["best_tangent_witness"]["upper_bound"]:
                result["best_tangent_witness"] = {"matrix": M.tolist(), "schur_information": J.tolist(),
                    "nuisance_minimizer": nuisance.tolist(), "logdet_schur": hull_value,
                    "prior_trace": prior_trace, "linear_price_excluding_prior": price,
                    "priced_selection": path, "priced_block_masks": masks, "upper_bound": candidate_upper}
            upper = min(upper, candidate_upper)
            value = design.true_objective(path)
            if value > lower:
                lower, selected = value, path
            if upper < max(lower, hull_value)-1e-7*max(1., abs(lower), abs(hull_value)):
                status = "numerical_bound_inconsistency"
                break
            if upper-lower <= true_gap:
                status = "true_optimal_tolerance"
                break
            if upper-hull_value <= hull_gap:
                status = "hull_optimal_tolerance"
                break
            if path not in paths:
                paths.append(path)
                matrices.append(oracle.matrix(path))
                weights = np.append(weights, 0.)
            correction_start = perf_counter()
            previous = hull_value
            weights, success, message = correct_weights(matrices, weights, design.p, deadline,
                                                        max_correction_iterations)
            result["correction_seconds"] += perf_counter()-correction_start
            result["correction_failures"] += int(not success)
            hull_value = schur_value_gradient(np.einsum("a,aij->ij", weights, np.array(matrices)), design.p)[0]
            if message == "time_limit":
                status = "time_limit"
                break
            if hull_value <= previous+1e-12:
                status = "correction_stalled"
                break
    except TimeBudgetExceeded:
        status = "time_limit"
        if oracle is None:
            result["setup_seconds"] = perf_counter()-started
    except np.linalg.LinAlgError as error:
        status, message = "numerical_linear_algebra_failure", str(error)
        upper = full_upper
    if matrices:
        final_M = np.einsum("a,aij->ij", weights, np.array(matrices))
        result["hull_matrix"] = final_M.tolist()
        result["hull_support"] = [{"selected": path, "weight": float(w)} for path, w in zip(paths, weights)]
        if status not in ("numerical_bound_inconsistency", "numerical_linear_algebra_failure"):
            try:
                final_value, final_J, _, _ = schur_value_gradient(final_M, design.p)
                hull_value = final_value
                result["hull_schur_information"] = final_J.tolist()
            except np.linalg.LinAlgError as error:
                status, message = "numerical_linear_algebra_failure", str(error)
    if status in ("numerical_bound_inconsistency", "numerical_linear_algebra_failure"):
        # The augmented Schur calculation is unreliable. Preserve the separately
        # evaluated marginal-covariance endpoints and only raw mixture diagnostics.
        hull_value, upper = None, full_upper
        result["hull_schur_information"] = None
        result["best_tangent_witness"] = None
    if oracle is not None:
        result["anchors"] = oracle.anchors
        result["block_layout"] = [{"times": b.times, "anchor_columns": b.anchor_columns} for b in oracle.blocks]
    result.update(status=status, wall_seconds=perf_counter()-started, true_lower_bound=lower,
                  true_upper_bound=upper, true_gap=upper-lower, selected=selected,
                  full_selection_upper_bound=full_upper, hull_value=hull_value,
                  hull_gap=None if hull_value is None else upper-hull_value,
                  generated_paths=len(paths), last_correction_message=message)
    return result


def validate():
    rng = np.random.default_rng(958173)
    counts = {key: 0 for key in ("covariance_reconstruction", "selected_schur_identities",
              "gradient_directional_checks", "concavity_checks", "count_dp_checks", "exhaustive_upper_checks")}
    max_information_error = max_gradient_error = 0.
    for n in (1, 2, 5, 8):
        for rho, latent in ((-.7, 1.), (0., 1.), (.4, 0.), (.8, 1.)):
            design = NoisyDesign(rng.normal(size=(n, 3)), rho, latent, .7, .1*np.eye(3), min(2, n))
            for b in sorted(set((1, 3, n))):
                oracle = SeparatorOracle(design, b)
                H, D = np.zeros((n, len(oracle.anchors))), np.zeros((n, n))
                for block in oracle.blocks:
                    D[np.ix_(block.times, block.times)] = block.D
                    if block.anchor_columns:
                        H[np.ix_(block.times, block.anchor_columns)] = block.H
                if oracle.anchors:
                    aa = np.array(oracle.anchors)
                    K = latent*rho**np.abs(aa[:, None]-aa)
                    assert np.allclose(oracle.prior[3:, 3:]@K, np.eye(len(aa)), atol=1e-10)
                    R = D+H@K@H.T
                else:
                    R = D
                assert np.allclose(R, design.covariance(), atol=1e-10)
                counts["covariance_reconstruction"] += 1
                paths = []
                for k in range(n+1):
                    for selected in combinations(range(n), k):
                        value, J, _, _ = schur_value_gradient(oracle.matrix(selected), 3)
                        expected = design.true_information(selected)
                        error = np.max(np.abs(J-expected))
                        max_information_error = max(max_information_error, float(error))
                        assert np.allclose(J, expected, atol=2e-9, rtol=2e-10)
                        counts["selected_schur_identities"] += 1
                        if k == design.k:
                            paths.append(selected)
                M0, M1 = oracle.matrix(paths[0]), oracle.matrix(paths[-1])
                M = .37*M0+.63*M1
                value, _, _, gradient = schur_value_gradient(M, 3)
                expected = .37*schur_value_gradient(M0, 3)[0]+.63*schur_value_gradient(M1, 3)[0]
                assert value >= expected-1e-9
                counts["concavity_checks"] += 1
                direction = M1-M0
                h = 1e-5
                numeric = (schur_value_gradient(M+h*direction, 3)[0]
                           -schur_value_gradient(M-h*direction, 3)[0])/(2*h)
                exact_formula = float(np.einsum("ij,ji", gradient, direction))
                max_gradient_error = max(max_gradient_error, abs(numeric-exact_formula))
                assert np.isclose(numeric, exact_formula, rtol=2e-5, atol=2e-7)
                assert np.isclose(np.einsum("ij,ji", gradient, M), 3, atol=1e-8)
                counts["gradient_directional_checks"] += 1
                price, path, _ = oracle.price(gradient)
                expected_price = max(float(np.einsum("ij,ji", gradient, oracle.matrix(s)-oracle.prior)) for s in paths)
                assert np.isclose(price, expected_price, atol=1e-8)
                assert len(path) == design.k
                counts["count_dp_checks"] += 1
                upper = value-3+float(np.einsum("ij,ji", gradient, oracle.prior))+price
                assert upper >= max(design.true_objective(s) for s in paths)-1e-8
                counts["exhaustive_upper_checks"] += 1
    design = NoisyDesign(rng.normal(size=(9, 3)), .85, 1., .2, .1*np.eye(3), 3)
    optimum = max(design.true_objective(s) for s in combinations(range(9), 3))
    solves = []
    for b in (2, 3, 9):
        result = solve_separator(design, b, time_limit=5.)
        assert result["true_lower_bound"] <= optimum+1e-8 <= result["true_upper_bound"]+2e-8
        solves.append({k: result[k] for k in ("block_size", "status", "true_gap", "hull_gap")})
    return {"status": "passed", "counts": counts, "solver_checks": solves,
            "max_information_error": max_information_error, "max_gradient_error": max_gradient_error,
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--n", type=int, default=48, choices=(48, 96, 192))
    parser.add_argument("--blocks", type=int, nargs="+", default=[4, 6, 8])
    parser.add_argument("--time-limit", type=float, default=30.)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    threads = {key: os.environ.get(key) for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")}
    if any(value != "1" for value in threads.values()):
        raise RuntimeError("Set all BLAS/OpenMP thread variables to one")
    if args.validate:
        report = validate()
        output = args.output or HERE/"results/latent-separator-validation.json"
        output.write_text(json.dumps(report, indent=2)+"\n")
        print(json.dumps(report, indent=2))
        return
    from noisy_markov_kinetics_probe import reaction_data
    _, F, kinetics = reaction_data(args.n, "fast")
    rho = Fraction(4, 5)**(192//args.n)
    design = NoisyDesign(F, float(rho), .00125, .00125, .01*np.eye(3), 16)
    report = {"metadata": {"source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "thread_environment": threads, "per_solver_time_limit": args.time_limit,
               "scope": "Isolated latent-separator runs; seed generation/setup included in each cap"},
              "problem_data": {"F": F.tolist(), "prior": design.prior.tolist(), "rho": str(rho),
                               "latent_variance": "1/800", "nugget_variance": "1/800", "k": 16},
              "kinetics": kinetics, "results": []}
    output = args.output or HERE/f"results/latent-separator-n{args.n}-probe.json"
    for b in args.blocks:
        result = solve_separator(design, b, time_limit=args.time_limit)
        report["results"].append(result)
        temporary = output.with_suffix(output.suffix+".tmp")
        temporary.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
        temporary.replace(output)
        print(json.dumps({key: result[key] for key in ("block_size", "status", "wall_seconds", "pricing_rounds",
                                                       "true_lower_bound", "true_upper_bound", "true_gap", "hull_gap")}))


if __name__ == "__main__":
    main()
