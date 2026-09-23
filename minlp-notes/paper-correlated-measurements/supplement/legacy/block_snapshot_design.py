"""Numerical full-vector snapshot selection for a stationary noisy Markov model.

Every selected time acquires all channels. The single unknown mean parameter
makes information additive after local conditioning; one count-mask dynamic
program maximizes that surrogate. Bounds here use floating-point arithmetic,
not the exact rational certificate machinery in the other research drivers.
"""

from dataclasses import dataclass
from itertools import combinations
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
from time import perf_counter

import numpy as np
from scipy.linalg import cho_factor, cho_solve, eigh
from scipy.optimize import minimize


class DeadlineExceeded(Exception):
    pass


def check_time(deadline):
    if perf_counter() >= deadline:
        raise DeadlineExceeded("time cap reached between numerical operations")


def integer(value, name, minimum=0):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return int(value)


def subset_indices(selected, n, d):
    selected = tuple(integer(t, "selected time") for t in selected)
    if len(set(selected)) != len(selected) or any(t >= n for t in selected):
        raise ValueError("selected times must be distinct and in range")
    selected = tuple(sorted(selected))
    return selected, np.array([t*d+j for t in selected for j in range(d)], dtype=int)


def solve_spd(matrix, rhs):
    return cho_solve(cho_factor(matrix, lower=True, check_finite=False), rhs, check_finite=False)


@dataclass
class SnapshotDesign:
    F: np.ndarray  # (time, channel), one mean parameter
    A: np.ndarray  # constant latent transition
    rho: float    # promised contraction cap, validated numerically
    prior: float
    k: int

    def __post_init__(self):
        self.F = np.asarray(self.F, dtype=float)
        self.A = np.asarray(self.A, dtype=float)
        if self.F.ndim != 2 or min(self.F.shape) < 1 or not np.isfinite(self.F).all():
            raise ValueError("F must be a nonempty finite time-by-channel array")
        self.n, self.d = self.F.shape
        if self.A.shape != (self.d, self.d) or not np.isfinite(self.A).all():
            raise ValueError("A must be a finite channel-by-channel array")
        if not math.isfinite(self.rho) or not 0 <= self.rho < 1:
            raise ValueError("require 0 <= rho < 1")
        if np.linalg.norm(self.A, 2) > self.rho + 1e-12:
            raise ValueError("A exceeds the stated contraction bound")
        if not math.isfinite(self.prior) or self.prior <= 0:
            raise ValueError("positive finite scalar prior required")
        self.k = integer(self.k, "k")
        if self.k > self.n:
            raise ValueError("k exceeds the number of times")

    def covariance(self):
        """P=I, V=I, Q=I-AA^T; lower covariance block is A**lag."""
        powers = [np.eye(self.d)]
        for _ in range(1, self.n):
            powers.append(self.A @ powers[-1])
        R = np.empty((self.n*self.d, self.n*self.d))
        for t in range(self.n):
            ti = slice(t*self.d, (t+1)*self.d)
            R[ti, ti] = 2*np.eye(self.d)
            for s in range(t):
                si = slice(s*self.d, (s+1)*self.d)
                R[ti, si] = powers[t-s]
                R[si, ti] = powers[t-s].T
        return R

    def true_information(self, selected, R=None):
        selected, indices = subset_indices(selected, self.n, self.d)
        if not selected:
            return self.prior
        if R is None:
            R = self.covariance()
        f = self.F.ravel()[indices]
        return float(self.prior + f @ solve_spd(R[np.ix_(indices, indices)], f))


def memory_estimate(design, L):
    L = min(integer(L, "L"), design.n-1)
    # Refuse before constructing exponentially large arrays, including shifts.
    if L > 30:
        raise MemoryError("history width above 30 refused before allocation")
    n, d, k, masks = design.n, design.d, design.k, 1 << L
    cache = 8*masks*(d*d*(L+1)+L)+512*masks
    dp = 5*(n+1)*(k+1)*masks + 16*(k+1)*masks + 8*n*masks
    # Includes dense covariance/eigensolver/Liu workspaces and largest local
    # factorization; Python/BLAS runtime memory is outside this array estimate.
    dense = 96*(n*d)**2 + 32*((L+1)*d)**2
    return {"L": L, "mask_count": masks,
            "count_layer_state_upper_bound": n*(k+1)*masks,
            "estimated_workspace_bytes": cache+dp+dense,
            "cache_array_upper_bytes": cache, "dp_array_bytes": dp,
            "dense_workspace_bytes": dense}


def preflight(design, L, max_memory_mb):
    if not math.isfinite(max_memory_mb) or max_memory_mb <= 0:
        raise ValueError("positive finite memory limit required")
    estimate = memory_estimate(design, L)
    if estimate["estimated_workspace_bytes"] > max_memory_mb*2**20:
        raise MemoryError(f"array workspace estimate exceeds {max_memory_mb} MiB: {estimate}")
    return estimate


def delta_bounds(design, L):
    """Reviewed block bound with Pbar=rmin=1; no dimension multiplier."""
    L = min(integer(L, "L"), design.n-1)
    rho = design.rho
    if L >= design.n-1 or rho == 0:
        return {"finite_series": 0., "gain_refined": 0., "used": 0.}
    base = 2*rho**(L+1)*(1-rho**(L+1))/(1-rho)**2
    gain = 2*rho**(L+1)/(1-rho)*(1+.5*rho*(1-rho**L)/(1-rho))
    return {"finite_series": base, "gain_refined": gain, "used": min(base, gain)}


class BlockCalendarOracle:
    def __init__(self, design, L, *, deadline=math.inf, max_memory_mb=256, R=None):
        self.design = design
        self.estimate = preflight(design, L, max_memory_mb)
        self.L = self.estimate["L"]
        self.masks = self.estimate["mask_count"]
        self.trim = self.masks-1
        check_time(deadline)
        self.R = design.covariance() if R is None else R
        self.maps = {}
        self.weights = np.full((design.n, self.masks), np.nan)
        for t in range(design.n):
            check_time(deadline)
            for mask in range(1 << min(t, self.L)):
                if mask.bit_count() >= design.k:
                    continue
                if mask % 16 == 0:
                    check_time(deadline)
                ages, beta, factor = self.conditional_map(mask)
                adjusted = design.F[t].copy()
                if ages:
                    adjusted -= beta @ design.F[[t-age for age in ages]].ravel()
                self.weights[t, mask] = adjusted @ cho_solve(factor, adjusted, check_finite=False)

    def conditional_map(self, mask):
        """Stationarity permits one block regression per tuple of history ages."""
        mask = integer(mask, "mask")
        if mask >= self.masks:
            raise ValueError("mask exceeds history width")
        if mask not in self.maps:
            ages = tuple(bit+1 for bit in range(self.L) if mask & (1 << bit))
            t, d = self.L, self.design.d
            # Preserve nearest-to-oldest age order in both beta and F_H.
            hi = np.array([(t-age)*d+j for age in ages for j in range(d)], dtype=int)
            ti = np.arange(t*d, (t+1)*d)
            if ages:
                cross = self.R[np.ix_(ti, hi)]
                beta = solve_spd(self.R[np.ix_(hi, hi)], cross.T).T
                D = 2*np.eye(d)-beta @ cross.T
            else:
                beta, D = np.empty((d, 0)), 2*np.eye(d)
            factor = cho_factor((D+D.T)/2, lower=True, check_finite=False)
            self.maps[mask] = ages, beta, factor
        return self.maps[mask]

    def information(self, selected):
        selected, _ = subset_indices(selected, self.design.n, self.design.d)
        if len(selected) > self.design.k:
            raise ValueError("oracle weights were compiled only for counts up to k")
        total = self.design.prior
        for t in selected:
            mask = sum(1 << (t-s-1) for s in selected if t-self.L <= s < t)
            total += self.weights[t, mask]
        return float(total)

    def maximize(self, *, deadline=math.inf):
        n, k, m = self.design.n, self.design.k, self.masks
        values = np.full((k+1, m), -np.inf)
        values[0, 0] = 0
        previous = np.full((n+1, k+1, m), -1, dtype=np.int32)
        chosen = np.zeros((n+1, k+1, m), dtype=bool)
        visited = 0
        for t in range(n):
            check_time(deadline)
            next_values = np.full_like(values, -np.inf)
            for count, mask in zip(*np.where(np.isfinite(values))):
                visited += 1
                shifted = (int(mask) << 1) & self.trim
                value = values[count, mask]
                if count+n-t-1 >= k and value > next_values[count, shifted]:
                    next_values[count, shifted] = value
                    previous[t+1, count, shifted] = mask
                    chosen[t+1, count, shifted] = False
                if count < k:
                    target = shifted | (1 if self.L else 0)
                    proposed = value+self.weights[t, mask]
                    if proposed > next_values[count+1, target]:
                        next_values[count+1, target] = proposed
                        previous[t+1, count+1, target] = mask
                        chosen[t+1, count+1, target] = True
            values = next_values
        mask = int(np.argmax(values[k]))
        optimum = float(self.design.prior+values[k, mask])
        if not math.isfinite(optimum):
            raise ArithmeticError("no finite exact-count DP solution")
        count, selected = k, []
        for t in range(n, 0, -1):
            was_chosen = chosen[t, count, mask]
            prev_mask = int(previous[t, count, mask])
            if prev_mask < 0:
                raise ArithmeticError("DP predecessor missing")
            if was_chosen:
                selected.append(t-1)
                count -= 1
            mask = prev_mask
        selected = tuple(reversed(selected))
        if len(selected) != k or not np.isclose(self.information(selected), optimum, rtol=1e-12, atol=1e-12):
            raise ArithmeticError("recovered DP schedule disagrees with value")
        return {"selected": selected, "surrogate_optimum": optimum,
                "visited_states": visited, "cached_conditional_maps": len(self.maps)}


def solve_snapshot(design, L, *, time_limit=30, max_memory_mb=256):
    started = perf_counter()
    if not math.isfinite(time_limit) or not 0 < time_limit <= 30:
        raise ValueError("time_limit must lie in (0,30]")
    deadline = started+time_limit
    result = {"status": "not_started", "selected": None, "true_lower_bound": None,
              "true_upper_bound": None, "true_information_gap": None,
              "surrogate_optimum": None, "L": L, "time_limit": time_limit,
              "numerical_scope": "floating-point algebra and DP; no exact certificate"}
    try:
        result["memory"] = preflight(design, L, max_memory_mb)
        check_time(deadline)
        R = design.covariance()
        seed = tuple(np.linspace(0, design.n-1, design.k, dtype=int)) if design.k else ()
        result["selected"] = seed
        result["true_lower_bound"] = design.true_information(seed, R)
        result["true_upper_bound"] = design.true_information(range(design.n), R)
        oracle = BlockCalendarOracle(design, L, deadline=deadline, max_memory_mb=max_memory_mb, R=R)
        result["preprocessing_seconds"] = perf_counter()-started
        dp_started = perf_counter()
        dp = oracle.maximize(deadline=deadline)
        result["dp_seconds"] = perf_counter()-dp_started
        result.update(dp)
        result["true_lower_bound"] = design.true_information(result["selected"], R)
        result["delta"] = delta_bounds(design, L)
        delta = result["delta"]["used"]
        if delta < 1:
            transferred = design.prior+(result["surrogate_optimum"]-design.prior)/(1-delta)
            result["transferred_information_upper_bound"] = transferred
            result["true_upper_bound"] = min(result["true_upper_bound"], transferred)
        result["status"] = "surrogate_optimal_numerical"
        result["selected_arc_information"] = [float(oracle.weights[t, sum(
            1 << (t-s-1) for s in result["selected"] if t-oracle.L <= s < t)])
            for t in result["selected"]]
    except (DeadlineExceeded, MemoryError) as error:
        result["status"] = "time_limit" if isinstance(error, DeadlineExceeded) else "memory_limit"
        result["message"] = str(error)
    if result["true_lower_bound"] is not None and result["true_upper_bound"] is not None:
        gap = result["true_upper_bound"]-result["true_lower_bound"]
        if gap < -1e-9*max(1, abs(result["true_lower_bound"])):
            result["status"] = "numerical_bound_inconsistency"
        result["true_information_gap"] = gap
        result["relative_information_gap"] = gap/result["true_lower_bound"]
        result["true_log_information_gap"] = math.log(result["true_upper_bound"] / result["true_lower_bound"])
    result["wall_seconds"] = perf_counter()-started
    return result


def greedy_exchange(design, *, time_limit=30, max_memory_mb=256):
    started = perf_counter()
    if not math.isfinite(time_limit) or not 0 < time_limit <= 30:
        raise ValueError("time_limit must lie in (0,30]")
    preflight(design, 0, max_memory_mb)
    deadline = started+time_limit
    R = design.covariance()
    seed = tuple(np.linspace(0, design.n-1, design.k, dtype=int)) if design.k else ()
    incumbent, lower = seed, design.true_information(seed, R)
    current, current_value = (), design.prior
    evaluations, exchanges, complete = 1, 0, False
    try:
        for _ in range(design.k):
            best_value, best = -math.inf, None
            for t in range(design.n):
                if t in current:
                    continue
                check_time(deadline)
                proposed = tuple(sorted((*current, t)))
                value = design.true_information(proposed, R)
                evaluations += 1
                if value > best_value:
                    best_value, best = value, proposed
            current, current_value = best, best_value
        greedy_selected, greedy_value = current, current_value
        if current_value > lower:
            incumbent, lower = current, current_value
        while True:
            best_value, best = current_value, current
            for dropped in current:
                for added in range(design.n):
                    if added in current:
                        continue
                    check_time(deadline)
                    proposed = tuple(sorted((set(current)-{dropped}) | {added}))
                    value = design.true_information(proposed, R)
                    evaluations += 1
                    if value > best_value+1e-12*max(1., abs(best_value)):
                        best_value, best = value, proposed
            if best == current:
                complete = True
                break
            current, current_value = best, best_value
            exchanges += 1
            if current_value > lower:
                incumbent, lower = current, current_value
    except DeadlineExceeded:
        pass
    return {"status": "single_exchange_local_optimum" if complete else "time_limit",
            "selected": incumbent, "true_lower_bound": lower,
            "greedy_selected": locals().get("greedy_selected"),
            "greedy_information": locals().get("greedy_value"),
            "objective_evaluations": evaluations, "accepted_exchanges": exchanges,
            "wall_seconds": perf_counter()-started, "time_limit": time_limit}


class BlockLiuOracle:
    """Scalar Liu extension with the same visit variable for every block row."""
    def __init__(self, design, split_fraction=.99, *, max_memory_mb=256):
        if not 0 < split_fraction < 1:
            raise ValueError("split_fraction must lie in (0,1)")
        preflight(design, 0, max_memory_mb)
        self.design, self.split_fraction = design, split_fraction
        self.R = design.covariance()
        minimum = float(eigh(self.R, subset_by_index=[0, 0], eigvals_only=True, check_finite=False)[0])
        self.a = split_fraction*minimum
        self.S = self.R-self.a*np.eye(design.n*design.d)
        self.f = design.F.ravel()

    def value_gradient(self, z):
        z = np.asarray(z, dtype=float)
        if z.shape != (self.design.n,) or not np.isfinite(z).all() or np.any(z < 0) or np.any(z > 1):
            raise ValueError("z must be a finite block visit vector in [0,1]")
        q = np.repeat(np.sqrt(z/self.a), self.design.d)
        matrix = (q[:, None]*self.S)*q[None, :]
        matrix.flat[::len(q)+1] += 1
        v = solve_spd(matrix, q*self.f)
        J = float(self.design.prior+(q*self.f) @ v)
        adjusted = self.f-self.S @ (q*v)
        gradient = np.sum(adjusted.reshape(self.design.n, self.design.d)**2, axis=1)/(self.a*J)
        return math.log(J), gradient


def solve_liu_relaxation(design, *, time_limit=30, max_memory_mb=256, initial_selected=None,
                         split_fraction=.99, max_iterations=200):
    started = perf_counter()
    if not math.isfinite(time_limit) or not 0 < time_limit <= 30:
        raise ValueError("time_limit must lie in (0,30]")
    deadline = started+time_limit
    oracle = BlockLiuOracle(design, split_fraction, max_memory_mb=max_memory_mb)
    selected, _ = subset_indices(initial_selected if initial_selected is not None else
        (np.linspace(0, design.n-1, design.k, dtype=int) if design.k else ()), design.n, design.d)
    if len(selected) != design.k:
        raise ValueError("initial_selected must have exactly k times")
    lower = design.true_information(selected, oracle.R)
    best_upper = math.log(design.true_information(range(design.n), oracle.R))
    best_witness = None
    best_value, best_z, evaluations = -math.inf, None, 0
    history = []

    def evaluate(z):
        nonlocal best_upper, best_witness, best_value, best_z, evaluations
        check_time(deadline)
        value, gradient = oracle.value_gradient(z)
        evaluations += 1
        # The top-k linear maximum is exact for box visits with sum(z)=k.
        price = float(np.sort(gradient)[-design.k:].sum()) if design.k else 0.
        upper = value+price-gradient @ z
        if upper < best_upper:
            best_upper = float(upper)
            best_witness = {"z": z.tolist(), "log_information": value,
                            "gradient": gradient.tolist(), "linear_price": price}
        feasibility = abs(float(z.sum())-design.k)
        if feasibility <= 1e-8 and value > best_value:
            best_value, best_z = value, z.copy()
        history.append({"evaluation": evaluations, "continuous_value": value,
                        "sum_residual": feasibility, "tangent_upper": float(upper),
                        "wall_seconds": perf_counter()-started})
        return -value, -gradient

    z0 = np.full(design.n, design.k/design.n)
    status, message, iterations = "not_started", "", 0
    try:
        output = minimize(evaluate, z0, method="SLSQP", jac=True, bounds=[(0., 1.)]*design.n,
            constraints=[{"type": "eq", "fun": lambda z: z.sum()-design.k,
                          "jac": lambda z: np.ones(design.n)}],
            options={"ftol": 1e-10, "maxiter": max_iterations, "disp": False})
        status = "optimizer_converged" if output.success else "optimizer_stopped"
        message, iterations = str(output.message), int(output.nit)
    except DeadlineExceeded as error:
        status, message = "time_limit", str(error)
    if best_z is not None:
        rounded = tuple(sorted(np.argsort(best_z)[-design.k:].tolist())) if design.k else ()
        rounded_value = design.true_information(rounded, oracle.R)
        if rounded_value > lower:
            selected, lower = rounded, rounded_value
    else:
        rounded, rounded_value = None, None
    continuous_gap = None if best_z is None else best_upper-best_value
    if best_upper < math.log(lower)-1e-8 or (continuous_gap is not None and continuous_gap < -1e-8):
        status = "numerical_bound_inconsistency"
    return {"status": status, "message": message, "selected": selected,
            "true_lower_bound": lower, "true_upper_bound": math.exp(best_upper),
            "true_information_gap": math.exp(best_upper)-lower,
            "true_log_information_gap": best_upper-math.log(lower),
            "continuous_log_information": None if best_z is None else best_value,
            "continuous_z": None if best_z is None else best_z.tolist(),
            "continuous_tangent_gap": continuous_gap,
            "upper_witness": best_witness, "split_fraction": split_fraction,
            "split_a": oracle.a, "evaluations": evaluations, "iterations": iterations,
            "rounded_selected": rounded, "rounded_true_information": rounded_value,
            "disclosed_initial_selected": initial_selected, "history": history,
            "time_limit": time_limit, "max_iterations": max_iterations,
            "wall_seconds": perf_counter()-started,
            "numerical_scope": "floating-point continuous tangent bound; no MIP or exact certificate"}


def transition(d, rho=.4):
    shift = np.roll(np.eye(d), 1, axis=0)
    signs = np.diag([1 if j % 2 == 0 else -1 for j in range(d)])
    return (rho/2)*(shift+signs)


def reaction_spectrum(n, d):
    times = 12*np.arange(1, n+1)/n
    channel = np.linspace(0, 1, d)
    centers, widths = np.array([.15, .50, .85]), np.array([.16, .19, .16])
    profiles = np.exp(-.5*((channel[:, None]-centers)/widths)**2)
    k1, k2, A0 = .7, .2, 1.
    e1, e2, difference = np.exp(-k1*times), np.exp(-k2*times), k2-k1
    concentrations = np.column_stack((A0*e1, A0*k1/difference*(e1-e2),
                                      A0-A0*e1-A0*k1/difference*(e1-e2)))
    dA = -A0*k1*times*e1
    dB = A0*k1*(k2/difference**2*(e1-e2)-k1/difference*times*e1)
    derivatives = np.column_stack((dA, dB, -dA-dB))
    F = derivatives @ profiles.T
    perturbed_k1 = k1*np.exp(1e-25j)
    complex_A = A0*np.exp(-perturbed_k1*times)
    complex_B = A0*perturbed_k1/(k2-perturbed_k1)*(np.exp(-perturbed_k1*times)-e2)
    complex_mean = np.column_stack((complex_A, complex_B, A0-complex_A-complex_B)) @ profiles.T
    error = float(np.max(np.abs(F-complex_mean.imag/1e-25)))
    if error > 1e-11:
        raise ArithmeticError("analytic reaction spectrum sensitivity check failed")
    return F, {"time_grid": times.tolist(), "channel_coordinate": channel.tolist(),
        "profile_centers": centers.tolist(), "profile_widths": widths.tolist(),
        "channel_profiles": profiles.tolist(), "mean_spectra": (concentrations @ profiles.T).tolist(),
        "species_concentrations": concentrations.tolist(), "A0": A0, "k1": k1, "k2": k2,
        "unknown_parameter": "log(k1)", "known_parameters": ["A0", "k2"],
        "complex_step_sensitivity_max_error": error,
        "model_label": "STYLIZED Beer-Lambert spectrum with three fixed Gaussian channel profiles; no measured spectra or calibrated residual covariance"}


def checkpoint(output, payload):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix+".tmp")
    temporary.write_text(json.dumps(payload, indent=2, allow_nan=False)+"\n")
    temporary.replace(output)


def attempt(operation):
    started = perf_counter()
    try:
        return operation()
    except Exception as error:
        return {"status": "exception", "exception_type": type(error).__name__,
                "message": str(error), "wall_seconds": perf_counter()-started}


def application_probe(d, output, time_limit=30):
    n, k, rho, L = 24, 8, .4, 6
    F, kinetics = reaction_spectrum(n, d)
    A = transition(d, rho)
    design = SnapshotDesign(F, A, rho, .01, k)
    Q = np.eye(d)-A @ A.T
    payload = {"metadata": {"driver_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "numpy_version": np.__version__, "time_limit_per_method": time_limit,
        "max_memory_mb": 256, "blas_environment": {key: os.environ.get(key) for key in
        ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")},
        "numerical_scope": "floating point throughout; model is the saved decimal arrays",
        "acquisition_unit": "all d channels at one time, never partial channels",
        "noise_model": "STYLIZED stationary latent VAR(1) with P=I, V=I, Q=I-AA^T; known mean-independent covariance",
        "dimension_comparison": "more channels add observations at unchanged per-channel noise; information values across d are not normalized",
        "spectral_units": "normalized channel coordinate and signal, path length one, model time units",
        "prior": "fixed scalar .01 in log(k1) coordinates",
        "baseline": "greedy plus best single exchange; scalar-split Liu continuous relaxation with shared block visits, split .99 and top-k tangent certificate",
        "complete": False},
        "n": n, "d": d, "p": 1, "k": k, "L": L, "rho": rho, "prior": design.prior,
        "F": F.tolist(), "A": A.tolist(), "Q": Q.tolist(), "kinetics": kinetics,
        "transition_checks": {"operator_norm": float(np.linalg.norm(A, 2)),
            "Q_minimum_eigenvalue": float(np.linalg.eigvalsh(Q).min()),
            "nonnormal_commutator_norm": float(np.linalg.norm(A @ A.T-A.T @ A, 2)),
            "off_diagonal_frobenius_norm": float(np.linalg.norm(A-np.diag(np.diag(A))))},
        "dp": None, "greedy_exchange": None, "liu_continuous": None}
    checkpoint(output, payload)
    payload["dp"] = attempt(lambda: solve_snapshot(design, L, time_limit=time_limit))
    checkpoint(output, payload)
    print(json.dumps({"d": d, "dp": payload["dp"]}), flush=True)
    payload["greedy_exchange"] = attempt(lambda: greedy_exchange(design, time_limit=time_limit))
    checkpoint(output, payload)
    candidates = [record for record in (payload["dp"], payload["greedy_exchange"])
                  if record.get("true_lower_bound") is not None]
    initial = max(candidates, key=lambda record: record["true_lower_bound"])["selected"] if candidates else None
    payload["liu_continuous"] = attempt(lambda: solve_liu_relaxation(
        design, time_limit=time_limit, initial_selected=initial))
    payload["metadata"]["complete"] = True
    checkpoint(output, payload)
    print(json.dumps({"d": d, "greedy": payload["greedy_exchange"],
        "liu": {key: value for key, value in payload["liu_continuous"].items()
                if key not in ("history", "continuous_z", "upper_witness")}}), flush=True)
    return payload


def validation(output):
    started = perf_counter()
    rng = np.random.default_rng(7183)
    F = rng.integers(-10, 11, size=(10, 3))/10
    design = SnapshotDesign(F, transition(3), .4, .01, 3)
    R = design.covariance()
    # Independently reconstruct the state covariance from innovation loadings.
    loading = np.eye(design.n*design.d)
    innovations = np.zeros_like(loading)
    for t in range(design.n):
        ti = slice(t*design.d, (t+1)*design.d)
        innovations[ti, ti] = np.eye(design.d) if not t else np.eye(design.d)-design.A @ design.A.T
        if t:
            loading[ti, :t*design.d] = design.A @ loading[(t-1)*design.d:t*design.d, :t*design.d]
    independent_R = loading @ innovations @ loading.T+np.eye(design.n*design.d)
    covariance_error = float(np.max(abs(R-independent_R)))
    assert covariance_error < 1e-12
    subsets = list(combinations(range(design.n), design.k))
    true = {s: design.true_information(s, R) for s in subsets}
    optimum = max(true.values())
    residuals = {"covariance_recursion": covariance_error, "local_information": 0., "full_history": 0., "price": 0.,
                 "liu_binary": 0., "liu_gradient": 0., "spectral_excess": 0.}
    rows = []
    for L in (0, 2, 6, 9):
        oracle = BlockCalendarOracle(design, L)
        scores = []
        for selected in subsets:
            _, ids = subset_indices(selected, design.n, design.d)
            f = F[list(selected)].ravel()
            transform = np.eye(len(ids))
            blockD = np.zeros((len(ids), len(ids)))
            for row, t in enumerate(selected):
                history = [s for s in selected if t-L <= s < t]
                _, hi = subset_indices(history, design.n, design.d)
                ti = np.arange(t*design.d, (t+1)*design.d)
                beta = solve_spd(R[np.ix_(hi, hi)], R[np.ix_(hi, ti)]).T if history else np.empty((design.d, 0))
                ri = slice(row*design.d, (row+1)*design.d)
                for h, s in enumerate(history):
                    col = selected.index(s)
                    transform[ri, col*design.d:(col+1)*design.d] = -beta[:, h*design.d:(h+1)*design.d]
                blockD[ri, ri] = R[np.ix_(ti, ti)]-beta @ R[np.ix_(hi, ti)]
            precision = transform.T @ solve_spd(blockD, transform)
            independent = float(design.prior+f @ precision @ f)
            score = oracle.information(selected)
            residuals["local_information"] = max(residuals["local_information"], abs(score-independent))
            scores.append(score)
            delta = delta_bounds(design, L)["used"]
            # Generalized spectrum compares the implemented precision to R^-1.
            root = np.linalg.cholesky(R[np.ix_(ids, ids)])
            eig = np.linalg.eigvalsh(root.T @ precision @ root)
            residuals["spectral_excess"] = max(residuals["spectral_excess"], float(np.max(abs(eig-1)))-delta)
            if L == 9:
                residuals["full_history"] = max(residuals["full_history"], abs(score-true[selected]))
        dp = oracle.maximize()
        residuals["price"] = max(residuals["price"], abs(dp["surrogate_optimum"]-max(scores)))
        solved = solve_snapshot(design, L)
        assert solved["true_lower_bound"] <= optimum+1e-10 <= solved["true_upper_bound"]+1e-10
        rows.append({"L": L, "enumerated_surrogate_optimum": max(scores),
                     "true_optimum": optimum, "result": solved})
    dense = BlockLiuOracle(design)
    for selected in subsets:
        z = np.zeros(design.n)
        z[list(selected)] = 1
        value, _ = dense.value_gradient(z)
        residuals["liu_binary"] = max(residuals["liu_binary"], abs(math.exp(value)-true[selected]))
    z = rng.uniform(.1, .9, design.n)
    _, gradient = dense.value_gradient(z)
    for j in range(design.n):
        step = np.zeros(design.n)
        step[j] = 1e-6
        finite = (dense.value_gradient(z+step)[0]-dense.value_gradient(z-step)[0])/2e-6
        residuals["liu_gradient"] = max(residuals["liu_gradient"], abs(finite-gradient[j]))
    relaxation = solve_liu_relaxation(design, time_limit=10)
    assert relaxation["true_upper_bound"] >= optimum-1e-9
    assert max(residuals.values()) < 1e-8, residuals
    boundary = []
    for n, k, L in ((1, 0, 0), (1, 1, 0), (5, 0, 2), (5, 5, 4)):
        case = SnapshotDesign(F[:n], transition(3), .4, .01, k)
        answer = solve_snapshot(case, L)
        assert len(answer["selected"]) == k
        exact = max(case.true_information(s) for s in combinations(range(n), k))
        assert answer["true_lower_bound"] <= exact+1e-10 <= answer["true_upper_bound"]+1e-10
        boundary.append({"n": n, "k": k, "L": L, "status": answer["status"]})
    refusal = solve_snapshot(design, 6, max_memory_mb=1e-8)
    assert refusal["status"] == "memory_limit" and refusal["true_lower_bound"] is None
    _, kinetic = reaction_spectrum(24, 4)
    payload = {"status": "passed", "n": 10, "d": 3, "k": 3,
        "subsets_per_window": len(subsets), "windows": [0, 2, 6, 9],
        "residuals": residuals, "rows": rows, "liu_continuous": relaxation,
        "boundary_cases": boundary, "memory_refusal": refusal,
        "kinetic_derivative_error": kinetic["complex_step_sensitivity_max_error"],
        "wall_seconds": perf_counter()-started,
        "driver_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    checkpoint(output, payload)
    print(json.dumps({key: payload[key] for key in ("status", "residuals", "wall_seconds")}), flush=True)
    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("validate", "probe"))
    parser.add_argument("--d", type=int, choices=(4, 16), default=4)
    parser.add_argument("--time-limit", type=float, default=30)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.mode == "validate":
        validation(args.output)
    else:
        application_probe(args.d, args.output, args.time_limit)
