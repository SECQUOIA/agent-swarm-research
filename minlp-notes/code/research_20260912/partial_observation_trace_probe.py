"""Weighted-trace design under two partially observed latent drift modes.

This standalone driver reuses the reviewed CalendarOracle's generic covariance
calculations and one linear price. It does not use its scalar-AR(1) delta or
logdet solver. All bounds in this driver use floating-point arithmetic.
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

from noisy_markov_design import CalendarOracle, TimeBudgetExceeded, check_memory, check_time, memory_estimate
from noisy_markov_kinetics_probe import reaction_data


HERE = Path(__file__).resolve().parent
PROOF_STATUS = "theorem_independently_verified"


def integer(value, name, minimum=0):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return int(value)


def subset(selected, n, count=None):
    selected = tuple(integer(i, "selected index") for i in selected)
    if len(set(selected)) != len(selected) or any(i >= n for i in selected):
        raise ValueError("selected indices must be distinct and in range")
    if count is not None and len(selected) != count:
        raise ValueError("selected must have the requested exact count")
    return tuple(sorted(selected))


def symmetric_psd(matrix, size, name):
    matrix = np.array(matrix, dtype=float, copy=True)
    if matrix.shape != (size, size) or not np.isfinite(matrix).all():
        raise ValueError(f"{name} must be a finite {size}-by-{size} matrix")
    if not np.allclose(matrix, matrix.T, atol=1e-12, rtol=1e-12):
        raise ValueError(f"{name} must be symmetric")
    matrix = (matrix+matrix.T)/2
    if np.linalg.eigvalsh(matrix).min() < -1e-12:
        raise ValueError(f"{name} must be positive semidefinite")
    return matrix


@dataclass
class TwoModeDesign:
    F: np.ndarray
    prior: np.ndarray
    k: int
    variance: float = .00125

    def __post_init__(self):
        self.F = np.array(self.F, dtype=float, copy=True)
        if self.F.ndim != 2 or min(self.F.shape) < 1 or not np.isfinite(self.F).all():
            raise ValueError("F must be a finite nonempty n-by-p array")
        self.n, self.p = self.F.shape
        self.prior = symmetric_psd(self.prior, self.p, "prior")
        self.k = integer(self.k, "k")
        if self.k > self.n:
            raise ValueError("k must not exceed n")
        if not math.isfinite(self.variance) or self.variance <= 0:
            raise ValueError("variance must be positive and finite")

    def covariance(self):
        return self.covariance_subset(range(self.n))

    def covariance_subset(self, selected):
        selected = subset(selected, self.n)
        t = np.array(selected, dtype=int)
        lag = abs(t[:, None]-t)
        return self.variance*(.36*.4**lag+.64*.2**lag+np.eye(len(t)))

    def true_information(self, selected):
        selected = subset(selected, self.n)
        if not selected:
            return self.prior.copy()
        F = self.F[list(selected)]
        R = self.covariance_subset(selected)
        solution = cho_solve(cho_factor(R, lower=True, check_finite=False), F, check_finite=False)
        information = self.prior+F.T @ solution
        return (information+information.T)/2


def trace_score(design, selected, weight):
    return float(np.einsum("ij,ji->", weight, design.true_information(selected)))


def preflight(design, L, max_memory_mb):
    L = min(integer(L, "L"), design.n-1)
    if L > 30:
        raise MemoryError("memory width above 30 refused before covariance allocation")
    estimate = memory_estimate(design, L, max_paths=1)
    # The oracle estimate already includes 64*n^2 dense workspaces. Add the
    # three-column solves and weight matrices of this separate trace driver.
    estimate["array_and_path_estimate_bytes"] += 64*design.n*design.p+64*design.p**2
    check_memory(estimate, max_memory_mb)
    return estimate


def partial_delta(n, L):
    """Partial-observation theorem, gamma=.4 and C/r=B=1 for this model."""
    n, L = integer(n, "n", 1), integer(L, "L")
    if L >= n-1:
        return 0.
    gamma = .4
    far = gamma**(L+1)/(1-gamma)
    near = gamma**(L+2)*(1-gamma**L)*(1-gamma**(L+1))/((1-gamma)*(1-gamma**2))
    return 2*(far+near)


def cap_deadline(time_limit):
    if not math.isfinite(time_limit) or not 0 < time_limit <= 5:
        raise ValueError("time_limit must lie in (0,5]")
    return perf_counter()+time_limit


def evenly_spaced(n, k):
    return tuple(np.linspace(0, n-1, k, dtype=int).tolist()) if k else ()


def solve_trace_dp(design, weight, L, *, time_limit=5, max_memory_mb=256):
    started = perf_counter()
    deadline = cap_deadline(time_limit)
    weight = symmetric_psd(weight, design.p, "weight")
    result = {"status": "not_started", "selected": None, "true_lower_bound": None,
        "true_upper_bound": None, "surrogate_selected": None, "surrogate_optimum": None,
        "transferred_true_upper_bound": None, "time_limit": time_limit, "L": L,
        "proof_status": PROOF_STATUS, "pricing_calls_completed": 0}
    try:
        result["memory"] = preflight(design, L, max_memory_mb)
        check_time(deadline)
        seed = evenly_spaced(design.n, design.k)
        result["selected"] = seed
        result["true_lower_bound"] = trace_score(design, seed, weight)
        result["true_upper_bound"] = trace_score(design, tuple(range(design.n)), weight)
        oracle = CalendarOracle(design, L, deadline=deadline, max_memory_mb=max_memory_mb, max_paths=1)
        result["preprocessing_seconds"] = perf_counter()-started
        priced_at = perf_counter()
        value, selected = oracle.price(weight, deadline=deadline)
        result["pricing_seconds"] = perf_counter()-priced_at
        selected = subset(selected, design.n, design.k)
        result["pricing_calls_completed"] = 1
        result["surrogate_selected"] = selected
        prior_trace = float(np.einsum("ij,ji->", weight, design.prior))
        result["surrogate_optimum"] = prior_trace+value
        independent = float(np.einsum("ij,ji->", weight, oracle.information(selected)))
        result["recovered_surrogate_residual"] = independent-result["surrogate_optimum"]
        true_value = trace_score(design, selected, weight)
        result["surrogate_selected_true_information"] = true_value
        if true_value >= result["true_lower_bound"]:
            result["selected"], result["true_lower_bound"] = selected, true_value
        delta = partial_delta(design.n, L)
        result["delta"] = delta
        if delta < 1:
            result["transferred_true_upper_bound"] = prior_trace+value/(1-delta)
            result["true_upper_bound"] = min(result["true_upper_bound"], result["transferred_true_upper_bound"])
        result["status"] = "surrogate_optimal_numerical"
        result["selected_true_information_matrix"] = design.true_information(result["selected"]).tolist()
        result["selected_surrogate_information_matrix"] = oracle.information(selected).tolist()
        result["selected_arc_trace"] = [float(np.einsum("ij,ji->", weight, oracle.weights[t, sum(
            1 << (t-s-1) for s in selected if t-oracle.L <= s < t)])) for t in selected]
    except (MemoryError, TimeBudgetExceeded) as error:
        result["status"] = "memory_limit" if isinstance(error, MemoryError) else "time_limit"
        result["message"] = str(error)
    if result["true_lower_bound"] is not None and result["true_upper_bound"] is not None:
        gap = result["true_upper_bound"]-result["true_lower_bound"]
        result["true_gap"] = gap
        result["relative_true_gap"] = gap/result["true_lower_bound"] if result["true_lower_bound"] > 0 else None
        if gap < -1e-8*max(1, abs(result["true_lower_bound"])):
            result["status"] = "numerical_bound_inconsistency"
    result["wall_seconds"] = perf_counter()-started
    return result


def greedy_exchange(design, weight, *, time_limit=5, max_memory_mb=256):
    started = perf_counter()
    deadline = cap_deadline(time_limit)
    weight = symmetric_psd(weight, design.p, "weight")
    preflight(design, 0, max_memory_mb)
    incumbent = evenly_spaced(design.n, design.k)
    lower = trace_score(design, incumbent, weight)
    evaluations, exchanges = 1, 0
    greedy_selected = greedy_value = None
    current, current_value = (), float(np.trace(weight @ design.prior))
    status = "time_limit"

    def evaluate(selected):
        nonlocal incumbent, lower, evaluations
        check_time(deadline)
        value = trace_score(design, selected, weight)
        evaluations += 1
        if len(selected) == design.k and value > lower:
            incumbent, lower = selected, value
        return value

    try:
        for _ in range(design.k):
            best, best_value = None, -math.inf
            for t in range(design.n):
                if t in current:
                    continue
                proposed = tuple(sorted((*current, t)))
                value = evaluate(proposed)
                if value > best_value:
                    best, best_value = proposed, value
            current, current_value = best, best_value
        greedy_selected, greedy_value = current, current_value
        while True:
            best, best_value = current, current_value
            for dropped in current:
                for added in range(design.n):
                    if added in current:
                        continue
                    proposed = tuple(sorted((set(current)-{dropped}) | {added}))
                    value = evaluate(proposed)
                    if value > best_value+1e-12*max(1., abs(best_value)):
                        best, best_value = proposed, value
            if best == current:
                status = "single_exchange_local_optimum"
                break
            current, current_value = best, best_value
            exchanges += 1
    except TimeBudgetExceeded:
        pass
    return {"status": status, "selected": incumbent, "true_lower_bound": lower,
        "greedy_selected": greedy_selected, "greedy_information": greedy_value,
        "accepted_exchanges": exchanges, "objective_evaluations": evaluations,
        "time_limit": time_limit, "wall_seconds": perf_counter()-started}


class TraceLiuOracle:
    def __init__(self, design, weight, split_fraction=.99, *, max_memory_mb=256):
        if not math.isfinite(split_fraction) or not 0 < split_fraction < 1:
            raise ValueError("split_fraction must lie in (0,1)")
        preflight(design, 0, max_memory_mb)
        self.design, self.weight = design, symmetric_psd(weight, design.p, "weight")
        R = design.covariance()
        self.a = split_fraction*float(eigh(R, subset_by_index=[0, 0], eigvals_only=True, check_finite=False)[0])
        self.S = R-self.a*np.eye(design.n)

    def value_gradient(self, z):
        z = np.asarray(z, dtype=float)
        if z.shape != (self.design.n,) or not np.isfinite(z).all() or np.any(z < 0) or np.any(z > 1):
            raise ValueError("z must be a finite visit vector in [0,1]")
        q = np.sqrt(z/self.a)
        system = (q[:, None]*self.S)*q[None, :]
        system.flat[::self.design.n+1] += 1
        qF = q[:, None]*self.design.F
        solved = cho_solve(cho_factor(system, lower=True, check_finite=False), qF, check_finite=False)
        information = self.design.prior+qF.T @ solved
        V = self.design.F-self.S @ (q[:, None]*solved)
        gradient = np.einsum("ij,jk,ik->i", V, self.weight, V)/self.a
        return float(np.einsum("ij,ji->", self.weight, information)), gradient


def solve_trace_relaxation(design, weight, *, initial_selected=None, time_limit=5,
                           max_iterations=200, max_memory_mb=256):
    started = perf_counter()
    deadline = cap_deadline(time_limit)
    max_iterations = integer(max_iterations, "max_iterations", 1)
    weight = symmetric_psd(weight, design.p, "weight")
    oracle = TraceLiuOracle(design, weight, max_memory_mb=max_memory_mb)
    initial = subset(initial_selected if initial_selected is not None else evenly_spaced(design.n, design.k), design.n, design.k)
    selected, lower = initial, trace_score(design, initial, weight)
    upper = trace_score(design, tuple(range(design.n)), weight)
    scale = max(1., abs(upper))
    best_value, best_z, witness = -math.inf, None, None
    history = []

    def evaluate(z):
        nonlocal upper, best_value, best_z, witness
        check_time(deadline)
        value, gradient = oracle.value_gradient(z)
        price = float(np.sort(gradient)[-design.k:].sum()) if design.k else 0.
        tangent = float(value-gradient @ z+price)
        if tangent < upper:
            upper = tangent
            witness = {"z": z.tolist(), "value": value, "gradient": gradient.tolist(), "linear_price": price}
        feasible_residual = abs(float(z.sum())-design.k)
        if feasible_residual <= 1e-8 and value > best_value:
            best_value, best_z = value, z.copy()
        history.append({"evaluation": len(history)+1, "value": value, "tangent_upper": tangent,
            "sum_residual": feasible_residual, "wall_seconds": perf_counter()-started})
        return -value/scale, -gradient/scale

    status, message, iterations = "not_started", "", 0
    try:
        result = minimize(evaluate, np.full(design.n, design.k/design.n), method="SLSQP", jac=True,
            bounds=[(0., 1.)]*design.n,
            constraints=[{"type": "eq", "fun": lambda z: z.sum()-design.k, "jac": lambda z: np.ones(design.n)}],
            options={"ftol": 1e-12, "maxiter": max_iterations, "disp": False})
        status = "optimizer_converged" if result.success else "optimizer_stopped"
        message, iterations = str(result.message), int(result.nit)
    except TimeBudgetExceeded as error:
        status, message = "time_limit", str(error)
    rounded = rounded_value = None
    if best_z is not None:
        rounded = tuple(sorted(np.argsort(best_z)[-design.k:].tolist())) if design.k else ()
        rounded_value = trace_score(design, rounded, weight)
        if rounded_value > lower:
            selected, lower = rounded, rounded_value
    continuous_gap = upper-best_value if best_z is not None else None
    if upper < lower-1e-8*scale or (continuous_gap is not None and continuous_gap < -1e-8*scale):
        status = "numerical_bound_inconsistency"
    return {"status": status, "message": message, "selected": selected,
        "true_lower_bound": lower, "true_upper_bound": upper, "true_gap": upper-lower,
        "relative_true_gap": (upper-lower)/lower if lower > 0 else None,
        "continuous_value": best_value if best_z is not None else None,
        "continuous_z": best_z.tolist() if best_z is not None else None,
        "continuous_tangent_gap": continuous_gap, "upper_witness": witness,
        "split_fraction": .99, "split_a": oracle.a, "iterations": iterations,
        "evaluations": len(history), "history": history, "objective_scale": scale,
        "disclosed_initial_selected": initial, "rounded_selected": rounded,
        "rounded_true_information": rounded_value, "time_limit": time_limit,
        "max_iterations": max_iterations, "wall_seconds": perf_counter()-started}


def checkpoint(output, payload):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix+".tmp")
    temporary.write_text(json.dumps(payload, indent=2, allow_nan=False)+"\n")
    temporary.replace(output)


def attempt(label, operation):
    started = perf_counter()
    try:
        result = operation()
    except Exception as error:
        result = {"status": "exception", "exception_type": type(error).__name__,
            "message": str(error), "wall_seconds": perf_counter()-started}
    print(json.dumps({"run": label, **{key: result[key] for key in
        ("status", "true_lower_bound", "true_upper_bound", "relative_true_gap", "wall_seconds") if key in result}}), flush=True)
    return result


def metadata():
    return {"source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "calendar_source_sha256": hashlib.sha256((HERE/"noisy_markov_design.py").read_bytes()).hexdigest(),
        "kinetics_source_sha256": hashlib.sha256((HERE/"noisy_markov_kinetics_probe.py").read_bytes()).hexdigest(),
        "numpy_version": np.__version__, "proof_status": PROOF_STATUS,
        "numeric_scope": "floating-point algebra, optimization, and theorem evaluation; no exact certificate",
        "input_scope": "saved decimal arrays define the numerical model; no claim exact real sensitivities",
        "criterion": "weighted trace of mean Fisher information, W=I in log(A0), log(k1), log(k2) coordinates; not conventional A-optimality",
        "noise_model": "STYLIZED two-dimensional latent drift, scalar partial observation H=(3/5,4/5), known parameter-independent covariance",
        "rational_model": {"A": [["2/5", "0"], ["0", "1/5"]], "H": [["3/5", "4/5"]],
            "P": [["1/800", "0"], ["0", "1/800"]],
            "Q": [["21/20000", "0"], ["0", "3/2500"]], "r": "1/800",
            "prior_diagonal": "1/100", "gamma": "2/5", "C/r": "1", "B": "1"},
        "time_grid_caveat": "fixed horizon 12; holding mode correlations .4/.2 across n changes physical correlation scales",
        "parameter_caveat": "local mean sensitivity only; observing B with unknown A0 leaves the rate-swap global ambiguity",
        "memory_scope": "256 MiB conservative array estimate; not process RSS; checks precede covariance allocation",
        "time_scope": "5 seconds per method; soft between numerical operations",
        "blas_environment": {key: os.environ.get(key) for key in
            ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")}}


def run_probe(output):
    payload = {"metadata": metadata(), "complete": False, "results": []}
    checkpoint(output, payload)
    for n in (48, 96):
        for regime in ("fast", "slow"):
            times, F, kinetics = reaction_data(n, regime)
            design = TwoModeDesign(F, .01*np.eye(3), n//3)
            W = np.eye(3)
            record = {"n": n, "p": 3, "k": design.k, "regime": regime, "F": F.tolist(),
                "prior": design.prior.tolist(), "W": W.tolist(), "variance": design.variance,
                "kinetics": kinetics, "dp": [], "greedy_exchange": None, "liu_continuous": None}
            payload["results"].append(record)
            checkpoint(output, payload)
            for L in ((6, 8) if n == 48 else (8,)):
                result = attempt(f"n{n}-{regime}-L{L}", lambda L=L: solve_trace_dp(design, W, L))
                if result.get("selected") is not None:
                    result["selected_times"] = times[list(result["selected"])].tolist()
                record["dp"].append(result)
                checkpoint(output, payload)
            record["greedy_exchange"] = attempt(f"n{n}-{regime}-greedy", lambda: greedy_exchange(design, W))
            checkpoint(output, payload)
            candidates = [result for result in record["dp"]+[record["greedy_exchange"]] if result.get("true_lower_bound") is not None]
            initial = max(candidates, key=lambda result: result["true_lower_bound"])["selected"] if candidates else None
            record["liu_continuous"] = attempt(f"n{n}-{regime}-liu", lambda: solve_trace_relaxation(design, W, initial_selected=initial))
            checkpoint(output, payload)
    payload["complete"] = True
    checkpoint(output, payload)
    return payload


def validate(output):
    started = perf_counter()
    rng = np.random.default_rng(82739)
    F = rng.integers(-10, 11, size=(10, 3))/10
    design = TwoModeDesign(F, .01*np.eye(3), 3)
    W = np.eye(3)
    R = design.covariance()
    schedules = list(combinations(range(10), 3))
    true = [trace_score(design, s, W) for s in schedules]
    residual = {"latent_covariance": 0., "local_information": 0., "full_history": 0.,
        "spectral_excess": 0., "dp": 0., "liu_binary": 0., "liu_gradient": 0., "liu_tangent_excess": 0.}
    A, H = np.diag([.4, .2]), np.array([[.6, .8]])
    loading = np.eye(20)
    innovations = np.zeros((20, 20))
    for t in range(10):
        innovations[2*t:2*t+2, 2*t:2*t+2] = design.variance*(np.eye(2) if t == 0 else np.eye(2)-A @ A.T)
        if t:
            loading[2*t:2*t+2, :2*t] = A @ loading[2*t-2:2*t, :2*t]
    projection = np.kron(np.eye(10), H)
    latent_R = projection @ loading @ innovations @ loading.T @ projection.T+design.variance*np.eye(10)
    residual["latent_covariance"] = float(np.max(abs(R-latent_R)))
    rows = []
    for L in (0, 2, 6, 9):
        oracle = CalendarOracle(design, L, max_paths=1)
        scores = []
        for chosen in schedules:
            transform, D = np.eye(3), np.zeros(3)
            for row, t in enumerate(chosen):
                history = [s for s in chosen if t-L <= s < t]
                beta = np.linalg.solve(R[np.ix_(history, history)], R[history, t]) if history else np.empty(0)
                for s, b in zip(history, beta):
                    transform[row, chosen.index(s)] = -b
                D[row] = R[t, t]-R[t, history] @ beta
            f = F[list(chosen)]
            independent = design.prior+f.T @ transform.T @ np.diag(1/D) @ transform @ f
            actual = oracle.information(chosen)
            residual["local_information"] = max(residual["local_information"], float(np.max(abs(actual-independent))))
            score = float(np.trace(actual))
            scores.append(score)
            covariance = transform @ R[np.ix_(chosen, chosen)] @ transform.T/np.sqrt(D[:, None]*D)
            error = float(np.max(abs(np.linalg.eigvalsh(covariance)-1)))
            residual["spectral_excess"] = max(residual["spectral_excess"], error-partial_delta(10, L))
            if L == 9:
                residual["full_history"] = max(residual["full_history"], float(np.max(abs(actual-design.true_information(chosen)))))
        price, selected = oracle.price(W)
        residual["dp"] = max(residual["dp"], abs(price+np.trace(design.prior)-max(scores)))
        result = solve_trace_dp(design, W, L)
        assert result["true_lower_bound"] <= max(true)+1e-8 and result["true_upper_bound"] >= max(true)-1e-8
        rows.append({"L": L, "true_enumerated_optimum": max(true), "result": result})
    # A non-diagonal PSD weight checks the general weighted-trace formula.
    mixed = np.array([[1., .3, -.2], [.3, .8, .1], [-.2, .1, .7]])
    oracle = TraceLiuOracle(design, mixed)
    for chosen in schedules:
        z = np.zeros(10)
        z[list(chosen)] = 1
        value, _ = oracle.value_gradient(z)
        residual["liu_binary"] = max(residual["liu_binary"], abs(value-trace_score(design, chosen, mixed)))
    z = rng.uniform(.1, .9, 10)
    value, gradient = oracle.value_gradient(z)
    for j in range(10):
        step = np.zeros(10)
        step[j] = 1e-6
        finite = (oracle.value_gradient(z+step)[0]-oracle.value_gradient(z-step)[0])/2e-6
        residual["liu_gradient"] = max(residual["liu_gradient"], abs(finite-gradient[j]))
    for chosen in schedules:
        residual["liu_tangent_excess"] = max(residual["liu_tangent_excess"],
            trace_score(design, chosen, mixed)-(value-gradient @ z+gradient[list(chosen)].sum()))
    dense = solve_trace_relaxation(design, W)
    assert dense["true_upper_bound"] >= max(true)-1e-8
    assert max(residual.values()) < 2e-6, residual
    boundaries = []
    for n, k, L in ((1, 0, 0), (1, 1, 0), (5, 0, 2), (5, 5, 4)):
        case = TwoModeDesign(F[:n], .01*np.eye(3), k)
        result = solve_trace_dp(case, W, L)
        exact = max(trace_score(case, chosen, W) for chosen in combinations(range(n), k))
        assert abs(result["true_lower_bound"]-exact) < 1e-8 and result["true_upper_bound"] >= exact-1e-8
        boundaries.append({"n": n, "k": k, "L": L, "result": result})
    refusal = solve_trace_dp(design, W, 9, max_memory_mb=1e-9)
    assert refusal["status"] == "memory_limit" and refusal["true_lower_bound"] is None
    cap = solve_trace_dp(design, W, 9, time_limit=1e-12)
    assert cap["status"] == "time_limit" and cap["surrogate_optimum"] is None
    payload = {"status": "passed", "metadata": metadata(), "n": 10, "p": 3, "k": 3,
        "schedule_count": len(schedules), "windows": [0, 2, 6, 9], "residuals": residual,
        "rows": rows, "liu_continuous": dense, "boundary_cases": boundaries,
        "memory_refusal": refusal, "deadline_refusal": cap, "wall_seconds": perf_counter()-started}
    checkpoint(output, payload)
    print(json.dumps({key: payload[key] for key in ("status", "residuals", "wall_seconds")}), flush=True)
    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("validate", "probe"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.mode == "validate":
        validate(args.output)
    else:
        run_probe(args.output)
