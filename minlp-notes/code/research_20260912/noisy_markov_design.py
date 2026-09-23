"""Calendar-memory design bounds for stationary scalar AR(1) plus nugget noise.

The path hull is a surrogate relaxation. Its closure does not establish a
discrete optimum. A uniform spectral correction transfers its upper bound to
the true likelihood. Every feasible lower bound uses the true covariance.
All numerical bounds rely on floating-point linear algebra and solver tolerances.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
from itertools import combinations
import json
import math
from pathlib import Path
from time import perf_counter

import numpy as np
from scipy.optimize import minimize


class TimeBudgetExceeded(RuntimeError):
    pass


def check_time(deadline: float) -> None:
    if perf_counter() >= deadline:
        raise TimeBudgetExceeded("wall-time budget exhausted")


def logdet(matrix: np.ndarray) -> float:
    return float(2 * np.log(np.diag(np.linalg.cholesky((matrix + matrix.T) / 2))).sum())


def validated_subset(selected: tuple[int, ...], n: int) -> tuple[int, ...]:
    selected = tuple(selected)
    if len(set(selected)) != len(selected) or any(
        not isinstance(i, (int, np.integer)) or not 0 <= i < n for i in selected
    ):
        raise ValueError("selected must contain distinct integer indices in [0,n)")
    return selected


@dataclass(frozen=True)
class NoisyDesign:
    F: np.ndarray
    rho: float
    latent_variance: float
    nugget_variance: float
    prior: np.ndarray
    k: int

    def __post_init__(self) -> None:
        F = np.array(self.F, dtype=float, copy=True)
        prior = np.array(self.prior, dtype=float, copy=True)
        if F.ndim != 2 or min(F.shape) < 1 or not np.isfinite(F).all():
            raise ValueError("F must be a finite nonempty n-by-p matrix")
        if not math.isfinite(self.rho) or abs(self.rho) >= 1:
            raise ValueError("rho must satisfy abs(rho) < 1")
        if not math.isfinite(self.latent_variance) or self.latent_variance < 0:
            raise ValueError("latent_variance must be nonnegative and finite")
        if not math.isfinite(self.nugget_variance) or self.nugget_variance <= 0:
            raise ValueError("nugget_variance must be positive and finite")
        if prior.shape != (F.shape[1], F.shape[1]) or not np.isfinite(prior).all():
            raise ValueError("prior must be finite and p-by-p")
        if not np.allclose(prior, prior.T, atol=1e-14, rtol=1e-12):
            raise ValueError("prior must be symmetric")
        prior = (prior + prior.T) / 2
        np.linalg.cholesky(prior)
        if not isinstance(self.k, (int, np.integer)) or not 0 <= self.k <= len(F):
            raise ValueError("k must be an integer in [0,n]")
        F.setflags(write=False)
        prior.setflags(write=False)
        object.__setattr__(self, "F", F)
        object.__setattr__(self, "prior", prior)

    @property
    def n(self) -> int:
        return len(self.F)

    @property
    def p(self) -> int:
        return self.F.shape[1]

    def covariance(self) -> np.ndarray:
        times = np.arange(self.n)
        return (self.latent_variance * self.rho ** np.abs(times[:, None] - times)
                + self.nugget_variance * np.eye(self.n))

    def true_information(self, selected: tuple[int, ...]) -> np.ndarray:
        selected = validated_subset(selected, self.n)
        if not selected:
            return self.prior.copy()
        F = self.F[list(selected)]
        t = np.array(selected)
        R = (self.latent_variance * self.rho ** np.abs(t[:, None] - t)
             + self.nugget_variance * np.eye(len(t)))
        J = self.prior + F.T @ np.linalg.solve(R, F)
        return (J + J.T) / 2

    def true_objective(self, selected: tuple[int, ...]) -> float:
        return logdet(self.true_information(selected))


def spectral_delta(design: NoisyDesign, L: int) -> float:
    """Reviewed finite-series/gain bound; complete calendar history is exact."""
    if not isinstance(L, (int, np.integer)) or L < 0:
        raise ValueError("L must be a nonnegative integer")
    rho = abs(design.rho)
    if rho == 0 or design.latent_variance == 0 or L >= design.n - 1:
        return 0.0
    gain = design.latent_variance / (design.latent_variance + design.nugget_variance)
    return (2 * design.latent_variance / design.nugget_variance * rho**(L+1) / (1-rho)
            * (1 + gain*rho*(1-rho**L)/(1-rho)))


def memory_estimate(design: NoisyDesign, L: int, max_paths: int = 101) -> dict:
    if not isinstance(L, (int, np.integer)) or L < 0:
        raise ValueError("L must be a nonnegative integer")
    effective = min(L, design.n - 1)
    masks = 1 << effective
    states = design.n * (design.k + 1) * masks
    # Arc matrices, DP predecessors/actions, two DP value layers, and hull data.
    arc_bytes = 8 * design.n * masks * design.p**2
    dp_bytes = 5 * states + 16 * (design.k + 1) * masks
    hull_bytes = 8 * max_paths * design.p**2 + 64 * max_paths * design.n + 64 * max_paths**2
    # Include covariance construction/solve temporaries and the cached covariance.
    ancillary_bytes = 8 * design.n * masks + 64 * design.n**2
    return {"requested_L": L, "effective_L": effective, "mask_count": masks,
            "count_layer_state_upper_bound": states,
            "array_and_path_estimate_bytes": arc_bytes + dp_bytes + hull_bytes + ancillary_bytes,
            "arc_matrix_bytes": arc_bytes, "dp_array_bytes": dp_bytes}


def check_memory(estimate: dict, max_memory_mb: float) -> None:
    if not math.isfinite(max_memory_mb) or max_memory_mb <= 0:
        raise ValueError("max_memory_mb must be positive and finite")
    if estimate["array_and_path_estimate_bytes"] > max_memory_mb * 2**20:
        raise MemoryError("calendar/count and covariance workspace estimate exceeds max_memory_mb: "
                          + str(estimate))


class CalendarOracle:
    """Local conditional information, indexed by preceding calendar bits."""

    def __init__(self, design: NoisyDesign, L: int, *, deadline: float = math.inf,
                 max_memory_mb: float = 256, max_paths: int = 101):
        self.design = design
        self.estimate = memory_estimate(design, L, max_paths)
        check_memory(self.estimate, max_memory_mb)
        self.L = self.estimate["effective_L"]
        self.masks = 1 << self.L
        self.R = design.covariance()
        self.weights = np.zeros((design.n, self.masks, design.p, design.p))
        for t in range(design.n):
            check_time(deadline)
            for mask in range(1 << min(t, self.L)):
                if mask.bit_count() >= design.k:
                    continue  # No size-k path can choose with this many recent visits.
                if mask % 64 == 0:
                    check_time(deadline)
                history, regression, variance = self.local_conditional(t, mask)
                adjusted = design.F[t].copy()
                if history:
                    adjusted -= regression @ design.F[history]
                self.weights[t, mask] = np.outer(adjusted, adjusted) / variance

    def local_conditional(self, t: int, mask: int) -> tuple[list[int], np.ndarray, float]:
        history = [j for j in range(max(0, t-self.L), t) if mask & (1 << (t-1-j))]
        if not history:
            return history, np.empty(0), float(self.R[t, t])
        cov = self.R[history, t]
        regression = np.linalg.solve(self.R[np.ix_(history, history)], cov)
        variance = float(self.R[t, t] - cov @ regression)
        if variance <= 0:
            raise np.linalg.LinAlgError("nonpositive local conditional variance")
        return history, regression, variance

    def information(self, selected: tuple[int, ...]) -> np.ndarray:
        """Compute for any subset, including cardinalities absent from priced paths."""
        selected = validated_subset(selected, self.design.n)
        J = self.design.prior.copy()
        selected_set = set(selected)
        mask = 0
        for t in range(self.design.n):
            choose = t in selected_set
            if choose:
                history, regression, variance = self.local_conditional(t, mask)
                adjusted = self.design.F[t].copy()
                if history:
                    adjusted -= regression @ self.design.F[history]
                J += np.outer(adjusted, adjusted) / variance
            mask = ((mask << 1) | choose) & (self.masks - 1)
        return J

    def residual_covariance(self, selected: tuple[int, ...]) -> np.ndarray:
        selected = tuple(sorted(validated_subset(selected, self.design.n)))
        A = np.eye(len(selected))
        variances = np.empty(len(selected))
        positions = {t: i for i, t in enumerate(selected)}
        for i, t in enumerate(selected):
            mask = sum(1 << (t-1-j) for j in selected[:i] if t-j <= self.L)
            history, regression, variance = self.local_conditional(t, mask)
            for j, coefficient in zip(history, regression):
                A[i, positions[j]] = -coefficient
            variances[i] = variance
        residual = A @ self.R[np.ix_(selected, selected)] @ A.T
        return residual / np.sqrt(variances[:, None] * variances[None, :])

    def price(self, gradient: np.ndarray, *, deadline: float = math.inf) -> tuple[float, tuple[int, ...]]:
        """Exact-count longest path; returned value excludes fixed prior information."""
        n, k, masks = self.design.n, self.design.k, self.masks
        arc_values = np.einsum("ij,tmji->tm", gradient, self.weights)
        values = np.full((k+1, masks), -np.inf)
        values[0, 0] = 0
        parent_mask = np.full((n, k+1, masks), -1, dtype=np.int32)
        action = np.full((n, k+1, masks), -1, dtype=np.int8)
        for t in range(n):
            check_time(deadline)
            next_values = np.full_like(values, -np.inf)
            for q in range(min(k, t)+1):
                for mask in np.flatnonzero(np.isfinite(values[q])):
                    if int(mask) % 256 == 0:
                        check_time(deadline)
                    value = values[q, mask]
                    shifted = (int(mask) << 1) & (masks-1)
                    if q + n-t-1 >= k and value > next_values[q, shifted]:
                        next_values[q, shifted] = value
                        parent_mask[t, q, shifted], action[t, q, shifted] = mask, 0
                    if q < k:
                        target = shifted | (1 if self.L else 0)
                        candidate = value + arc_values[t, mask]
                        if candidate > next_values[q+1, target]:
                            next_values[q+1, target] = candidate
                            parent_mask[t, q+1, target], action[t, q+1, target] = mask, 1
            values = next_values
        mask = int(np.argmax(values[k]))
        maximum, q, selected = float(values[k, mask]), k, []
        if not math.isfinite(maximum):
            raise RuntimeError("count-layer DP has no feasible path")
        for t in range(n-1, -1, -1):
            take = int(action[t, q, mask])
            previous = int(parent_mask[t, q, mask])
            if take not in (0, 1) or previous < 0:
                raise RuntimeError("invalid DP predecessor")
            if take:
                selected.append(t)
            mask, q = previous, q-take
        selected.reverse()
        return maximum, tuple(selected)


def correct_weights(matrices: list[np.ndarray], weights: np.ndarray, deadline: float,
                    max_iterations: int) -> tuple[np.ndarray, bool, str]:
    """Simplex correction; any returned weights give a feasible hull matrix."""
    blocks = np.array(matrices)
    best = weights.copy()
    best_value = logdet(np.einsum("a,aij->ij", best, blocks))

    def objective(w: np.ndarray) -> tuple[float, np.ndarray]:
        nonlocal best, best_value
        check_time(deadline)
        J = np.einsum("a,aij->ij", w, blocks)
        value = logdet(J)
        gradient = np.einsum("ij,aji->a", np.linalg.solve(J, np.eye(len(J))), blocks)
        feasible = np.maximum(w, 0)
        feasible /= feasible.sum()
        feasible_value = logdet(np.einsum("a,aij->ij", feasible, blocks))
        if feasible_value > best_value:
            best, best_value = feasible.copy(), feasible_value
        return -value, -gradient

    try:
        result = minimize(objective, weights, jac=True, method="SLSQP",
                          bounds=[(0, 1)] * len(weights),
                          constraints={"type": "eq", "fun": lambda w: w.sum()-1,
                                       "jac": lambda w: np.ones(len(w))},
                          options={"ftol": 1e-11, "maxiter": max_iterations, "disp": False})
        return best, bool(result.success), str(result.message)
    except TimeBudgetExceeded:
        return best, False, "time_limit"


@dataclass
class HullResult:
    status: str
    n: int
    p: int
    k: int
    L: int
    delta: float
    memory_bound_usable: bool
    wall_seconds: float
    pricing_rounds: int
    generated_paths: int
    correction_failures: int
    surrogate_hull_value: float | None
    surrogate_upper_bound: float | None
    surrogate_hull_gap: float | None
    true_lower_bound: float | None
    true_upper_bound: float | None
    true_gap: float | None
    selected: tuple[int, ...] | None
    full_selection_upper_bound: float | None
    transferred_upper_bound: float | None
    memory_estimate: dict
    last_correction_message: str | None
    hull_support: list[dict]
    hull_information: list[list[float]] | None
    upper_bound_witness: dict | None
    prior_aware_upper_bound: float | None
    prior_aware_witness: dict | None


def solve_hull(design: NoisyDesign, L: int, *, time_limit: float = 30,
               hull_gap: float = 1e-6, true_gap: float = 1e-6, max_rounds: int = 100,
               max_correction_iterations: int = 100, max_memory_mb: float = 256) -> HullResult:
    if (not 0 < time_limit <= 30 or not math.isfinite(hull_gap) or hull_gap <= 0
            or not math.isfinite(true_gap) or true_gap <= 0 or max_rounds < 0
            or max_correction_iterations < 1):
        raise ValueError("invalid time, gap, or iteration limit")
    started = perf_counter()
    deadline = started + time_limit
    estimate = memory_estimate(design, L, max_rounds+1)
    delta = spectral_delta(design, L)
    try:
        check_memory(estimate, max_memory_mb)
    except MemoryError as error:
        return HullResult(
            status="memory_limit", n=design.n, p=design.p, k=design.k,
            L=estimate["effective_L"], delta=delta, memory_bound_usable=delta < 1,
            wall_seconds=perf_counter()-started, pricing_rounds=0, generated_paths=0,
            correction_failures=0, surrogate_hull_value=None, surrogate_upper_bound=None,
            surrogate_hull_gap=None, true_lower_bound=None, true_upper_bound=None,
            true_gap=None, selected=None, full_selection_upper_bound=None,
            transferred_upper_bound=None, memory_estimate=estimate,
            last_correction_message=str(error), hull_support=[], hull_information=None,
            upper_bound_witness=None, prior_aware_upper_bound=None, prior_aware_witness=None)
    seed = tuple(int(i) for i in np.linspace(0, design.n-1, design.k))
    lower = design.true_objective(seed)
    full = design.true_objective(tuple(range(design.n)))
    upper, selected = full, seed
    surrogate_upper = surrogate_value = transferred = None
    rounds, failures, generated = 0, 0, 0
    status, correction_message = "iteration_limit", None
    paths, matrices, weights = [], [], np.empty(0)
    witness = None
    prior_aware = prior_witness = None
    try:
        oracle = CalendarOracle(design, L, deadline=deadline,
                                max_memory_mb=max_memory_mb, max_paths=max_rounds+1)
        paths, matrices, weights = [seed], [oracle.information(seed)], np.ones(1)
        generated = 1
        surrogate_value = logdet(matrices[0])
        for _ in range(max_rounds):
            check_time(deadline)
            J = np.einsum("a,aij->ij", weights, np.array(matrices))
            surrogate_value = logdet(J)
            gradient = np.linalg.solve(J, np.eye(design.p))
            price, path = oracle.price(gradient, deadline=deadline)
            rounds += 1
            candidate_upper = surrogate_value + float(np.trace(gradient @ design.prior)) + price - design.p
            if surrogate_upper is None or candidate_upper < surrogate_upper:
                witness = {"hull_information": J.tolist(), "gradient": gradient.tolist(),
                           "hull_logdet": surrogate_value, "priced_selection": path,
                           "linear_price_excluding_prior": price,
                           "prior_trace": float(np.trace(gradient @ design.prior)),
                           "surrogate_upper_bound": candidate_upper}
            surrogate_upper = (candidate_upper if surrogate_upper is None
                               else min(surrogate_upper, candidate_upper))
            if surrogate_upper < surrogate_value-1e-7*max(1, abs(surrogate_value)):
                status = "numerical_hull_bound_inconsistency"
                break
            feasible_value = design.true_objective(path)
            if feasible_value > lower:
                lower, selected = feasible_value, path
            if delta < 1:
                transferred = surrogate_upper - design.p * math.log1p(-delta)
                upper = min(full, transferred)
            if upper < lower - 1e-7 * max(1, abs(lower)):
                status = "numerical_bound_inconsistency"
                break
            if upper-lower <= true_gap:
                status = "true_optimal_tolerance"
                break
            if surrogate_upper-surrogate_value <= hull_gap:
                status = "hull_optimal_tolerance"
                break
            if path not in paths:
                paths.append(path)
                matrices.append(oracle.information(path))
                weights = np.append(weights, 0.0)
                generated += 1
            previous = surrogate_value
            weights, success, correction_message = correct_weights(
                matrices, weights, deadline, max_correction_iterations)
            failures += int(not success)
            surrogate_value = logdet(np.einsum("a,aij->ij", weights, np.array(matrices)))
            if correction_message == "time_limit":
                status = "time_limit"
                break
            if surrogate_value <= previous + 1e-12:
                status = "correction_stalled"
                break
    except TimeBudgetExceeded:
        status = "time_limit"
    except MemoryError as error:
        status, correction_message = "memory_limit", str(error)
    if len(weights) and delta < 1 and perf_counter() < deadline:
        # Apply the tangent after retaining the unscaled prior. This is a true
        # objective upper bound, separate from the surrogate hull certificate.
        try:
            M = np.einsum("a,aij->ij", weights, np.array(matrices))
            N = design.prior + (M-design.prior)/(1-delta)
            inverse_N = np.linalg.solve(N, np.eye(design.p))
            H = inverse_N/(1-delta)
            price, path = oracle.price(H, deadline=deadline)
            prior_trace = float(np.trace(inverse_N @ design.prior))
            prior_aware = logdet(N)-design.p+prior_trace+price
            prior_witness = {"surrogate_hull_information": M.tolist(), "N": N.tolist(),
                             "arc_gradient": H.tolist(), "logdet_N": logdet(N),
                             "prior_trace": prior_trace, "priced_selection": path,
                             "linear_price_excluding_prior": price,
                             "true_upper_bound": prior_aware}
            upper = min(upper, prior_aware)
            feasible_value = design.true_objective(path)
            if feasible_value > lower:
                lower, selected = feasible_value, path
            if upper < lower-1e-7*max(1, abs(lower)):
                status = "numerical_bound_inconsistency"
            elif upper-lower <= true_gap and not status.startswith("numerical_"):
                status = "true_optimal_tolerance"
        except TimeBudgetExceeded:
            pass  # Earlier fully completed pricing certificates remain valid.
    return HullResult(
        status=status, n=design.n, p=design.p, k=design.k, L=estimate["effective_L"],
        delta=delta, memory_bound_usable=delta < 1,
        wall_seconds=perf_counter()-started, pricing_rounds=rounds,
        generated_paths=generated, correction_failures=failures,
        surrogate_hull_value=surrogate_value, surrogate_upper_bound=surrogate_upper,
        surrogate_hull_gap=(None if surrogate_upper is None or surrogate_value is None
                            else max(0.0, surrogate_upper-surrogate_value)),
        true_lower_bound=lower, true_upper_bound=upper, true_gap=max(0.0, upper-lower),
        selected=selected, full_selection_upper_bound=full, transferred_upper_bound=transferred,
        memory_estimate=estimate, last_correction_message=correction_message,
        hull_support=[{"selected": path, "weight": float(w), "information": matrix.tolist()}
                      for path, w, matrix in zip(paths, weights, matrices)],
        hull_information=(np.einsum("a,aij->ij", weights, np.array(matrices)).tolist()
                          if len(weights) else None),
        upper_bound_witness=witness,
        prior_aware_upper_bound=prior_aware, prior_aware_witness=prior_witness,
    )


class DenseLiuOracle:
    def __init__(self, design: NoisyDesign, split_fraction: float = 0.5):
        if not 0 < split_fraction < 1:
            raise ValueError("split_fraction must lie strictly between zero and one")
        self.design = design
        R = design.covariance()
        self.a = split_fraction * float(np.linalg.eigvalsh(R)[0])
        self.S = R - self.a * np.eye(design.n)

    def value_gradient(self, z: np.ndarray) -> tuple[float, np.ndarray]:
        d = z / self.a
        V = np.linalg.solve(np.eye(self.design.n) + self.S * d[None, :], self.design.F)
        J = self.design.prior + self.design.F.T @ (d[:, None] * V)
        J = (J + J.T) / 2
        gradient = np.einsum("ij,ji->i", V, np.linalg.solve(J, V.T)) / self.a
        return logdet(J), gradient


def solve_dense_oa(design: NoisyDesign, *, time_limit: float = 30,
                   absolute_gap: float = 1e-6, max_rounds: int = 500,
                   split_fraction: float = 0.5, root_rounds: int = 0,
                   initial_selected: tuple[int, ...] | None = None) -> dict:
    """Standalone same-covariance binary OA comparator; Gurobi uses one thread."""
    import gurobipy as gp

    if (not 0 < time_limit <= 30 or not math.isfinite(absolute_gap) or absolute_gap <= 0
            or max_rounds < 0 or root_rounds < 0):
        raise ValueError("invalid time, gap, or iteration limit")
    started = perf_counter()
    deadline = started + time_limit
    oracle = DenseLiuOracle(design, split_fraction)
    selected = (tuple(int(i) for i in np.linspace(0, design.n-1, design.k))
                if initial_selected is None else validated_subset(initial_selected, design.n))
    if len(selected) != design.k:
        raise ValueError("initial_selected must have exactly k entries")
    lower = design.true_objective(selected)
    initial_point, initial_value = selected, lower
    upper = design.true_objective(tuple(range(design.n)))
    status, master_status, rounds, nodes = "iteration_limit", None, 0, 0.0
    root_iterations, root_status = 0, "not_requested"
    root_value = root_upper = None
    with gp.Env(empty=True) as env:
        env.setParam("OutputFlag", 0)
        env.start()
        with gp.Model("noisy_dense_oa", env=env) as model:
            model.Params.Threads = 1
            model.Params.Seed = 0
            model.Params.MIPGap = 0
            model.Params.MIPGapAbs = min(1e-9, absolute_gap/10)
            model.Params.FeasibilityTol = 1e-9
            model.Params.IntFeasTol = 1e-9
            model.Params.OptimalityTol = 1e-9
            z = list(model.addVars(design.n, lb=0, ub=1,
                                  vtype=gp.GRB.CONTINUOUS if root_rounds else gp.GRB.BINARY).values())
            t = model.addVar(lb=logdet(design.prior), ub=upper)
            model.addConstr(gp.quicksum(z) == design.k)
            model.setObjective(t, gp.GRB.MAXIMIZE)

            def cut(point: np.ndarray) -> None:
                value, gradient = oracle.value_gradient(point)
                model.addConstr(t <= value-float(gradient @ point)
                                + gp.LinExpr(gradient.tolist(), z))

            point = np.zeros(design.n)
            point[list(selected)] = 1
            cut(np.ones(design.n))
            cut(point)
            if root_rounds:
                root_status = "iteration_limit"
                for _ in range(root_rounds):
                    if perf_counter() >= deadline:
                        root_status = "time_limit"
                        break
                    model.Params.TimeLimit = deadline-perf_counter()
                    model.optimize()
                    root_iterations += 1
                    master_status = model.Status
                    if model.Status == gp.GRB.OPTIMAL:
                        upper = min(upper, float(model.ObjVal))
                        root_upper = upper
                    if not model.SolCount:
                        root_status = "master_status_" + str(model.Status)
                        break
                    fractional = np.clip([v.X for v in z], 0, 1)
                    fractional_value = oracle.value_gradient(fractional)[0]
                    root_value = (fractional_value if root_value is None
                                  else max(root_value, fractional_value))
                    if root_upper is not None and root_upper < root_value-1e-7*max(1, abs(root_value)):
                        root_status = status = "numerical_root_bound_inconsistency"
                        break
                    if root_upper is not None and root_upper-root_value <= absolute_gap:
                        root_status = "optimal_tolerance"
                        break
                    if model.Status != gp.GRB.OPTIMAL:
                        root_status = "master_status_" + str(model.Status)
                        break
                    cut(fractional)
                for variable in z:
                    variable.VType = gp.GRB.BINARY
            for variable, value in zip(z, point):
                variable.Start = float(value)
            t.Start = lower
            for _ in range(0 if root_status.startswith("numerical_") else max_rounds):
                if upper < lower-1e-7*max(1, abs(lower)):
                    status = "numerical_bound_inconsistency"
                    break
                if upper-lower <= absolute_gap:
                    status = "optimal_tolerance"
                    break
                if perf_counter() >= deadline:
                    status = "time_limit"
                    break
                model.Params.TimeLimit = deadline-perf_counter()
                model.optimize()
                rounds += 1
                nodes += model.NodeCount
                master_status = model.Status
                if math.isfinite(model.ObjBound):
                    upper = min(upper, float(model.ObjBound))
                point = None
                if model.SolCount:
                    values = np.array([v.X for v in z])
                    point = np.rint(values)
                    if int(point.sum()) != design.k or np.max(abs(point-values)) > 1e-6:
                        status = "invalid_integer_incumbent"
                        break
                    candidate = tuple(int(i) for i in np.flatnonzero(point))
                    value = design.true_objective(candidate)
                    if value > lower:
                        lower, selected = value, candidate
                if upper < lower-1e-7*max(1, abs(lower)):
                    status = "numerical_bound_inconsistency"
                    break
                if upper-lower <= absolute_gap:
                    status = "optimal_tolerance"
                    break
                if model.Status == gp.GRB.TIME_LIMIT or perf_counter() >= deadline:
                    status = "time_limit"
                    break
                if model.Status != gp.GRB.OPTIMAL or point is None:
                    status = "master_status_" + str(model.Status)
                    break
                cut(point)
    point = np.zeros(design.n)
    point[list(selected)] = 1
    return {"status": status, "wall_seconds": perf_counter()-started,
            "n": design.n, "p": design.p, "k": design.k,
            "lower_bound": lower, "upper_bound": upper, "absolute_gap": max(0.0, upper-lower),
            "selected": selected, "oa_rounds": rounds, "master_nodes": nodes,
            "master_status": master_status,
            "objective_residual": abs(oracle.value_gradient(point)[0]-lower),
            "split_fraction": split_fraction, "root_oa_rounds": root_iterations,
            "root_status": root_status, "root_feasible_relaxation_value": root_value,
            "root_upper_bound": root_upper,
            "root_gap": None if root_value is None or root_upper is None else max(0, root_upper-root_value),
            "initial_selected": initial_point, "initial_lower_bound": initial_value}


def generic_design(n: int = 12, p: int = 3, k: int = 4, rho: float = 0.4,
                   seed: int = 0, nugget_variance: float = 1) -> NoisyDesign:
    return NoisyDesign(np.random.default_rng(seed).normal(size=(n, p)), rho, 1,
                       nugget_variance, 0.1*np.eye(p), k)


def enumerate_optimum(design: NoisyDesign) -> tuple[float, tuple[int, ...]]:
    if math.comb(design.n, design.k) > 100_000:
        raise ValueError("enumeration is limited to 100,000 subsets")
    return max((design.true_objective(s), s) for s in combinations(range(design.n), design.k))


def validate() -> dict:
    checks = []
    rng = np.random.default_rng(31)
    for rho, L in ((0.4, 0), (0.4, 4), (0.6, 6), (-0.4, 3), (0.4, 11)):
        design = generic_design(n=12, k=4, rho=rho, seed=2)
        oracle = CalendarOracle(design, L)
        delta, worst_spectral = spectral_delta(design, L), 0.0
        for size in range(1, design.n+1):
            for selected in combinations(range(design.n), size):
                C = oracle.residual_covariance(selected)
                error = float(np.max(abs(np.linalg.eigvalsh(C)-1)))
                worst_spectral = max(worst_spectral, error)
                assert error <= delta+1e-10, (rho, L, selected, error, delta)
        subsets = list(combinations(range(design.n), design.k))
        infos = np.array([oracle.information(s) for s in subsets])
        gradient = rng.normal(size=(design.p, design.p))
        gradient = gradient @ gradient.T
        price, chosen = oracle.price(gradient)
        brute_price = float(np.einsum("ij,aji->a", gradient, infos-design.prior).max())
        assert abs(price-brute_price) < 1e-8, (price, brute_price)
        assert abs(price-float(np.trace(gradient @ (oracle.information(chosen)-design.prior)))) < 1e-8
        true_optimum, _ = enumerate_optimum(design)
        surrogate_optimum = max(logdet(J) for J in infos)
        result = solve_hull(design, L, time_limit=5)
        assert result.true_upper_bound >= true_optimum-1e-7, result
        assert result.true_lower_bound <= true_optimum+1e-7, result
        assert result.surrogate_upper_bound >= surrogate_optimum-1e-7, result
        dense = DenseLiuOracle(design)
        for selected in subsets:
            z = np.zeros(design.n)
            z[list(selected)] = 1
            assert abs(dense.value_gradient(z)[0]-design.true_objective(selected)) < 1e-8
        checks.append({"rho": rho, "L": L, "delta": delta,
                       "worst_subset_spectral_error": worst_spectral,
                       "true_optimum": true_optimum, "surrogate_discrete_optimum": surrogate_optimum,
                       "result": asdict(result)})
    tiny = generic_design(n=8, k=3, rho=0.4, seed=4)
    optimum, _ = enumerate_optimum(tiny)
    dense = solve_dense_oa(tiny, time_limit=5)
    assert dense["status"] == "optimal_tolerance", dense
    assert abs(dense["lower_bound"]-optimum) < 1e-7, dense
    strengthened = solve_dense_oa(tiny, time_limit=5, split_fraction=0.99, root_rounds=200)
    assert strengthened["status"] == "optimal_tolerance", strengthened
    assert abs(strengthened["lower_bound"]-optimum) < 1e-7, strengthened
    for k in (0, 1, 6):
        design = generic_design(n=6, k=k)
        oracle = CalendarOracle(design, 2)
        price, selected = oracle.price(np.eye(design.p))
        assert len(selected) == k
        expected = max(np.trace(oracle.information(s)-design.prior)
                       for s in combinations(range(design.n), k))
        assert abs(price-expected) < 1e-9
    cap = solve_hull(tiny, 3, max_rounds=0)
    assert cap.status == "iteration_limit" and cap.surrogate_upper_bound is None
    timed = solve_hull(tiny, 3, time_limit=1e-9)
    assert timed.status == "time_limit" and timed.true_lower_bound is not None
    refused = solve_hull(generic_design(n=48, k=16), 20, max_memory_mb=1)
    assert refused.status == "memory_limit" and refused.true_lower_bound is None, refused
    for bad in ((0, 0), (-1,), (12,), (1.0,)):
        for evaluate in (tiny.true_information, CalendarOracle(tiny, 2).information):
            try:
                evaluate(bad)
            except ValueError:
                pass
            else:
                raise AssertionError(("invalid subset accepted", bad))
    return {"status": "passed", "cases": checks, "dense_tiny": dense,
            "dense_tiny_strengthened": strengthened,
            "cap_status": cap.status, "time_cap_status": timed.status,
            "memory_refusal_status": refused.status}


def benchmark(time_limit: float = 5) -> dict:
    """Small reproducible comparison; each solver invocation gets its own cap."""
    results = []
    for n in (12, 24, 48):
        design = generic_design(n=n, k=n//3, rho=0.4, seed=0)
        record = {"n": n, "p": design.p, "k": design.k, "rho": design.rho,
                  "latent_variance": design.latent_variance,
                  "nugget_variance": design.nugget_variance,
                  "F": design.F.tolist(), "prior": design.prior.tolist(),
                  "hulls": [asdict(solve_hull(design, L, time_limit=time_limit)) for L in (4, 6)],
                  "dense_oa": solve_dense_oa(design, time_limit=time_limit)}
        best_hull = max(record["hulls"], key=lambda r: r["true_lower_bound"])
        record["dense_oa_strengthened"] = solve_dense_oa(
            design, time_limit=time_limit, split_fraction=0.99, root_rounds=200,
            initial_selected=tuple(best_hull["selected"]))
        record["dense_oa_strengthened"]["initial_incumbent_source"] = (
            "best true-evaluated path from the two hull runs; their preprocessing times are reported separately")
        if n <= 12:
            optimum, selected = enumerate_optimum(design)
            record["enumerated_true_optimum"] = optimum
            record["enumerated_selected"] = selected
            for hull in record["hulls"]:
                assert hull["true_lower_bound"] <= optimum+1e-7 <= hull["true_upper_bound"]+2e-7
            dense = record["dense_oa"]
            assert dense["lower_bound"] <= optimum+1e-7 <= dense["upper_bound"]+2e-7
            dense = record["dense_oa_strengthened"]
            assert dense["lower_bound"] <= optimum+1e-7 <= dense["upper_bound"]+2e-7
        results.append(record)
    thresholds = []
    for rho in (0.4, 0.6):
        design = generic_design(n=48, k=16, rho=rho)
        thresholds.extend({"rho": rho, "L": L, "delta": spectral_delta(design, L),
                           **memory_estimate(design, L)} for L in range(15))
    return {"metadata": {"numpy_version": np.__version__, "seed": 0,
                         "per_solver_time_limit": time_limit, "gurobi_threads": 1,
                         "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                         "delta_rule": "reviewed finite-series bound with gain P/(P+r)",
                         "claim": "solver-numerical bounds; hull closure does not imply a discrete optimum"},
            "results": results, "thresholds": thresholds}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("solve", "validate", "thresholds", "benchmark"))
    parser.add_argument("--n", type=int, default=24)
    parser.add_argument("--p", type=int, default=3)
    parser.add_argument("--k", type=int, default=8)
    parser.add_argument("--rho", type=float, default=0.4)
    parser.add_argument("--L", type=int, default=4)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--time-limit", type=float, default=10)
    parser.add_argument("--max-rounds", type=int, default=100)
    parser.add_argument("--max-memory-mb", type=float, default=256)
    parser.add_argument("--dense", action="store_true")
    parser.add_argument("--split-fraction", type=float, default=0.5)
    parser.add_argument("--root-rounds", type=int, default=0)
    args = parser.parse_args()
    design = generic_design(args.n, args.p, args.k, args.rho, args.seed)
    if args.command == "validate":
        print(json.dumps(validate(), indent=2))
    elif args.command == "benchmark":
        print(json.dumps(benchmark(args.time_limit), indent=2))
    elif args.command == "thresholds":
        print(json.dumps([{"L": L, "delta": spectral_delta(design, L),
                           **memory_estimate(design, L)} for L in range(min(args.n, 15))], indent=2))
    else:
        result = (solve_dense_oa(design, time_limit=args.time_limit, max_rounds=args.max_rounds,
                                split_fraction=args.split_fraction, root_rounds=args.root_rounds)
                  if args.dense else asdict(solve_hull(
                      design, args.L, time_limit=args.time_limit, max_rounds=args.max_rounds,
                      max_memory_mb=args.max_memory_mb)))
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
