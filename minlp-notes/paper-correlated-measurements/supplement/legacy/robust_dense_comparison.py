"""Independent dense robust relaxation and completed exchange polishing.

Uses shared visits in the scalar-split Liu extension. Upper bounds come from
simplex scenario weights and an exact top-k linear support calculation, not
from SLSQP's success flag. All numerical calculations use floating point.
"""

import argparse
import hashlib
from itertools import combinations
import json
import math
import os
from pathlib import Path
from time import perf_counter
import warnings

import numpy as np
from scipy.optimize import OptimizeWarning, linprog, minimize

from noisy_markov_design import DenseLiuOracle, NoisyDesign, TimeBudgetExceeded, check_time
from robust_kinetic_design import (RobustDesign, active_weights, checkpoint, evaluation,
    integer, probability, selection)


HERE = Path(__file__).resolve().parent


def deadline_from(time_limit):
    if not math.isfinite(time_limit) or not 0 < time_limit <= 30:
        raise ValueError("time_limit must lie in (0,30]")
    return perf_counter()+time_limit


def dense_preflight(design, max_memory_mb):
    if not math.isfinite(max_memory_mb) or max_memory_mb <= 0:
        raise ValueError("positive finite memory limit required")
    estimate = 128*design.q*design.n**2+128*design.n*design.q*design.p+128*design.p**2*design.q
    if estimate > max_memory_mb*2**20:
        raise MemoryError("dense array-workspace estimate exceeds memory limit")
    return {"estimated_workspace_bytes": estimate, "limit_mib": max_memory_mb,
            "scope": "conservative array workspaces, not a process RSS cap"}


class RobustDenseOracle:
    def __init__(self, design, *, max_memory_mb=256):
        self.design = design
        self.memory = dense_preflight(design, max_memory_mb)
        self.oracles = [DenseLiuOracle(scenario, .99) for scenario in design.scenarios]

    def values_gradients(self, z):
        z = np.asarray(z, dtype=float)
        if z.shape != (self.design.n,) or not np.isfinite(z).all() or np.any(z < 0) or np.any(z > 1):
            raise ValueError("z must be a finite vector in [0,1]")
        evaluated = [oracle.value_gradient(z) for oracle in self.oracles]
        return np.array([item[0] for item in evaluated])-self.design.offsets, np.array([item[1] for item in evaluated])


def tangent_bound(values, gradients, z, dual, k):
    dual = probability(dual)
    constants = values-gradients @ z
    weighted_gradient = dual @ gradients
    support = float(np.sort(weighted_gradient)[-k:].sum()) if k else 0.
    upper = float(dual @ constants+support)
    return upper, {"dual_weights": dual.tolist(), "z": z.tolist(),
        "scenario_values_minus_offsets": values.tolist(), "scenario_gradients": gradients.tolist(),
        "scenario_constants": constants.tolist(), "weighted_gradient": weighted_gradient.tolist(),
        "top_k_linear_price": support, "upper_bound": upper}


def optimize_tangent_dual(values, gradients, z, k, deadline):
    """Small LP minimizes the top-k support tangent over scenario weights."""
    check_time(deadline)
    q, n = gradients.shape
    # max_{box,sum=k} g*z = min_nu k*nu + sum_i max(g_i-nu,0).
    # Minimize that expression jointly with simplex scenario weights.
    objective = np.r_[values-gradients @ z, float(k), np.ones(n)]
    inequalities = np.column_stack((gradients.T, -np.ones(n), -np.eye(n)))
    equality = np.r_[np.ones(q), np.zeros(n+1)][None, :]
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="Unrecognized options detected.*", category=OptimizeWarning)
        result = linprog(objective, A_ub=inequalities, b_ub=np.zeros(n),
            A_eq=equality, b_eq=np.ones(1), bounds=[(0., None)]*q+[(None, None)]+[(0., None)]*n,
            method="highs", options={"threads": 1, "time_limit": max(1e-5, deadline-perf_counter())})
    if result.x is not None and np.isfinite(result.x[:q]).all() and np.maximum(result.x[:q], 0).max() > 0:
        dual = probability(result.x[:q])
    else:
        dual = active_weights(values)
    # Recompute the support after normalization. The LP objective is never
    # trusted as an upper certificate when its solve or constraints are inexact.
    upper, witness = tangent_bound(values, gradients, z, dual, k)
    witness["dual_lp_status"] = int(result.status)
    witness["dual_lp_message"] = str(result.message)
    return upper, witness


def solve_dense_robust(design, *, initial_selected=None, time_limit=30,
                       max_iterations=1000, max_memory_mb=256):
    started = perf_counter()
    deadline = deadline_from(time_limit)
    max_iterations = integer(max_iterations, "max_iterations", 1)
    memory = dense_preflight(design, max_memory_mb)
    initial = selection(initial_selected if initial_selected is not None else
        (tuple(np.linspace(0, design.n-1, design.k, dtype=int)) if design.k else ()), design.n, design.k)
    initial_value = design.true_score(initial)
    upper = design.true_score(tuple(range(design.n)))
    oracle = RobustDenseOracle(design, max_memory_mb=max_memory_mb)
    best_value, best_z, best_witness = -math.inf, None, None
    cached_z = cached_values = cached_gradients = None
    history = []

    def retain(upper_candidate, witness):
        nonlocal upper, best_witness
        if upper_candidate < upper:
            upper, best_witness = upper_candidate, witness

    def evaluate(z):
        nonlocal cached_z, cached_values, cached_gradients, best_z, best_value
        check_time(deadline)
        if cached_z is not None and np.array_equal(z, cached_z):
            return cached_values, cached_gradients
        values, gradients = oracle.values_gradients(z)
        feasible_error = abs(float(z.sum())-design.k)
        if feasible_error <= 1e-8 and min(values) > best_value:
            best_value, best_z = float(min(values)), z.copy()
        for dual in (active_weights(values), np.ones(design.q)):
            candidate, witness = tangent_bound(values, gradients, z, dual, design.k)
            retain(candidate, witness)
        history.append({"evaluation": len(history)+1, "continuous_value": float(min(values)),
            "sum_residual": feasible_error, "upper_bound": upper, "wall_seconds": perf_counter()-started})
        cached_z, cached_values, cached_gradients = z.copy(), values, gradients
        return values, gradients

    z0 = np.full(design.n, design.k/design.n)
    status, message, iterations, optimizer_dual = "not_started", "", 0, None
    final_z = None
    try:
        values, _ = evaluate(z0)
        def objective(x):
            check_time(deadline)
            return -float(x[-1]), np.r_[np.zeros(design.n), -1.]

        result = minimize(objective, np.r_[z0, min(values)], method="SLSQP", jac=True,
            bounds=[(0., 1.)]*design.n+[(None, None)],
            constraints=[{"type": "eq", "fun": lambda x: x[:-1].sum()-design.k,
                          "jac": lambda x: np.r_[np.ones(design.n), 0.]},
                {"type": "ineq", "fun": lambda x: evaluate(x[:-1])[0]-x[-1],
                 "jac": lambda x: np.column_stack((evaluate(x[:-1])[1], -np.ones(design.q)))}],
            options={"ftol": 1e-11, "maxiter": max_iterations, "disp": False})
        status = "optimizer_converged" if result.success else "optimizer_stopped"
        message, iterations = str(result.message), int(result.nit)
        final_z = result.x[:-1].copy()
        multipliers = np.asarray(getattr(result, "multipliers", []))
        if len(multipliers) == design.q+1 and np.isfinite(multipliers[1:]).all() and np.maximum(multipliers[1:], 0).max() > 0:
            optimizer_dual = probability(multipliers[1:])
    except TimeBudgetExceeded as error:
        status, message = "time_limit", str(error)
    dual_postprocess = []
    # Valid upper bounds survive any optimizer stop. Optimize dual weights at
    # the best feasible fractional point and final optimizer point if time allows.
    for point in (best_z, final_z):
        if point is None:
            continue
        try:
            check_time(deadline)
            values, gradients = oracle.values_gradients(point)
            if optimizer_dual is not None:
                candidate, witness = tangent_bound(values, gradients, point, optimizer_dual, design.k)
                retain(candidate, witness)
            candidate, witness = optimize_tangent_dual(values, gradients, point, design.k, deadline)
            dual_postprocess.append({"status": witness["dual_lp_status"], "upper_bound": candidate})
            retain(candidate, witness)
        except TimeBudgetExceeded:
            dual_postprocess.append({"status": "time_limit"})
            break
    rounded = None if best_z is None else (tuple(sorted(np.argsort(best_z)[-design.k:].tolist())) if design.k else ())
    rounded_value = None if rounded is None else design.true_score(rounded)
    selected, lower = initial, initial_value
    if rounded_value is not None and rounded_value > lower:
        selected, lower = rounded, rounded_value
    continuous_gap = upper-best_value if best_z is not None else None
    if upper < lower-1e-7 or (continuous_gap is not None and continuous_gap < -1e-7):
        status = "numerical_bound_inconsistency"
    return {"status": status, "message": message, "selected": selected,
        "true_lower_bound": lower, "true_upper_bound": upper, "true_gap": upper-lower,
        "continuous_value": best_value if best_z is not None else None,
        "continuous_z": best_z.tolist() if best_z is not None else None,
        "continuous_tangent_gap": continuous_gap, "upper_bound_witness": best_witness,
        "rounded_selected": rounded, "rounded_true_score": rounded_value,
        "disclosed_initial_selected": initial, "disclosed_initial_score": initial_value,
        "initial_incumbent_affects_continuous_search": False,
        "split_fraction": .99, "split_a_by_scenario": [item.a for item in oracle.oracles],
        "iterations": iterations, "evaluations": len(history), "history": history,
        "optimizer_dual": optimizer_dual.tolist() if optimizer_dual is not None else None,
        "dual_postprocess": dual_postprocess, "memory": memory,
        "max_iterations": max_iterations, "time_limit": time_limit,
        "wall_seconds": perf_counter()-started}


def polish_schedule(design, initial_selected, *, time_limit=30):
    """Best single exchanges, with local status tied to the returned path."""
    started = perf_counter()
    deadline = deadline_from(time_limit)
    current = selection(initial_selected, design.n, design.k)
    current_value = design.true_score(current)
    start_value = current_value
    incumbent, incumbent_value = current, current_value
    evaluations, exchanges = 1, 0
    status = "time_limit"
    try:
        while True:
            best, best_value = current, current_value
            for dropped in current:
                for added in range(design.n):
                    if added in current:
                        continue
                    check_time(deadline)
                    path = tuple(sorted((set(current)-{dropped}) | {added}))
                    value = design.true_score(path)
                    evaluations += 1
                    if value > incumbent_value:
                        incumbent, incumbent_value = path, value
                    if value > best_value+1e-11:
                        best, best_value = path, value
            if best == current:
                incumbent, incumbent_value = current, current_value
                status = "single_exchange_local_optimum"
                break
            current, current_value = best, best_value
            exchanges += 1
    except TimeBudgetExceeded:
        pass
    return {"status": status, "initial_selected": initial_selected, "initial_score": start_value,
        "selected": incumbent, "true_lower_bound": incumbent_value,
        "improvement": incumbent_value-start_value, "accepted_exchanges": exchanges,
        "objective_evaluations": evaluations, "time_limit": time_limit,
        "wall_seconds": perf_counter()-started,
        "selected_scenario_logdet": design.true_values(incumbent).tolist()}


def load_case(path):
    payload = json.loads(Path(path).read_text())
    scenarios = tuple(NoisyDesign(np.array(row["F"]), row["rho"], row["latent_variance"],
        row["nugget_variance"], np.array(row["prior"]), row["k"]) for row in payload["scenarios"])
    return payload, RobustDesign(scenarios, np.array(payload["offsets"]))


def attempt(label, operation):
    started = perf_counter()
    try:
        result = operation()
    except Exception as error:
        result = {"status": "exception", "exception_type": type(error).__name__,
            "message": str(error), "wall_seconds": perf_counter()-started}
    print(json.dumps({"run": label, **{key: result[key] for key in ("status", "true_lower_bound",
        "true_upper_bound", "true_gap", "continuous_tangent_gap", "improvement", "wall_seconds") if key in result}}), flush=True)
    return result


def run_comparison(source, output):
    started = perf_counter()
    original, design = load_case(source)
    payload = {"metadata": {"source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "robust_source_sha256": hashlib.sha256((HERE/"robust_kinetic_design.py").read_bytes()).hexdigest(),
        "input_path": str(source), "input_sha256": hashlib.sha256(Path(source).read_bytes()).hexdigest(),
        "numeric_scope": "floating-point dense relaxation bounds and true-covariance feasible scores",
        "dense_incumbent_scope": "supplied incumbent affects reported lower bound only; fractional search starts uniformly",
        "time_limits": {"dense": 30, "each_polish": 30}, "blas_environment": {key: os.environ.get(key) for key in
            ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")}},
        "n": design.n, "p": design.p, "k": design.k, "offsets": design.offsets.tolist(),
        "hull_polish": None, "dense": None, "dense_rounding_polish": None,
        "evaluations": None, "timing": None, "complete": False}
    checkpoint(output, payload)
    payload["hull_polish"] = attempt("hull-incumbent-polish", lambda: polish_schedule(design, original["robust"]["selected"]))
    checkpoint(output, payload)
    candidates = [record for record in (original["robust"], original["greedy_exchange"], payload["hull_polish"])
                  if record.get("true_lower_bound") is not None]
    initial = max(candidates, key=lambda record: record["true_lower_bound"])["selected"]
    payload["dense"] = attempt("dense-robust", lambda: solve_dense_robust(design, initial_selected=initial))
    checkpoint(output, payload)
    if payload["dense"].get("rounded_selected") is not None:
        payload["dense_rounding_polish"] = attempt("dense-rounding-polish", lambda: polish_schedule(design, payload["dense"]["rounded_selected"]))
    checkpoint(output, payload)
    reference_lower = np.array([record["hull"]["true_lower_bound"] for record in original["references"]])
    reference_upper = np.array([record["hull"]["true_upper_bound"] for record in original["references"]])
    payload["evaluations"] = {}
    for label in ("hull_polish", "dense", "dense_rounding_polish"):
        record = payload[label]
        if record is not None and record.get("selected") is not None:
            payload["evaluations"][label] = evaluation(design, record["selected"], reference_lower, reference_upper)
            candidates.append(record)
    best = max(candidates, key=lambda record: record["true_lower_bound"])
    payload["best_shared_incumbent"] = evaluation(design, best["selected"], reference_lower, reference_upper)
    payload["upper_comparison"] = {"shared_hull_true_upper": original["robust"]["true_upper_bound"],
        "dense_true_upper": payload["dense"].get("true_upper_bound"),
        "common_fixed_offset_lower": best["true_lower_bound"]}
    ref = original["reference_wall_seconds"]
    hull = original["robust"]["wall_seconds"]
    greedy = original["greedy_exchange"]["wall_seconds"]
    hp = payload["hull_polish"]["wall_seconds"]
    dense = payload["dense"]["wall_seconds"]
    dp = payload["dense_rounding_polish"]["wall_seconds"] if payload["dense_rounding_polish"] is not None else 0.
    payload["timing"] = {"existing_reference_generation": ref, "existing_hull_generation": hull,
        "existing_greedy_generation": greedy, "hull_polishing": hp, "dense_solver": dense,
        "dense_rounding_polishing": dp,
        "hull_with_reference_and_polishing": ref+hull+hp,
        "standalone_dense_with_references_and_own_polishing": ref+dense+dp,
        "supplied_shared_incumbent_generation": ref+hull+greedy+hp,
        "all_generation_and_new_methods": ref+hull+greedy+hp+dense+dp,
        "new_driver_wall_seconds": perf_counter()-started}
    payload["complete"] = True
    checkpoint(output, payload)
    return payload


def validate(output):
    started = perf_counter()
    rng = np.random.default_rng(28741)
    n, p, k = 10, 2, 3
    scenarios = tuple(NoisyDesign(rng.integers(-9, 10, size=(n, p))/10, .4, 1., 1., .1*np.eye(p), k) for _ in range(3))
    paths = list(combinations(range(n), k))
    raw = np.array([[scenario.true_objective(path) for scenario in scenarios] for path in paths])
    design = RobustDesign(scenarios, raw.max(axis=0))
    oracle = RobustDenseOracle(design)
    residuals = {"binary_identity": 0., "gradient": 0., "tangent_excess": 0.}
    for path, values in zip(paths, raw):
        z = np.zeros(n)
        z[list(path)] = 1
        evaluated, _ = oracle.values_gradients(z)
        residuals["binary_identity"] = max(residuals["binary_identity"], float(np.max(abs(evaluated-(values-design.offsets)))))
    z = rng.uniform(.1, .9, n)
    values, gradients = oracle.values_gradients(z)
    for i in range(n):
        step = np.zeros(n)
        step[i] = 1e-6
        finite = (oracle.values_gradients(z+step)[0]-oracle.values_gradients(z-step)[0])/2e-6
        residuals["gradient"] = max(residuals["gradient"], float(np.max(abs(finite-gradients[:, i]))))
    optimum = float(np.min(raw-design.offsets, axis=1).max())
    for dual in ([1e308, 1e308, 1e308], [1, 0, 0], [.1, .2, .7]):
        upper, _ = tangent_bound(values, gradients, z, dual, k)
        residuals["tangent_excess"] = max(residuals["tangent_excess"], optimum-upper)
    lp_upper, lp_witness = optimize_tangent_dual(values, gradients, z, k, perf_counter()+5)
    assert lp_upper >= optimum-1e-9
    dense = solve_dense_robust(design, time_limit=10)
    assert dense["true_lower_bound"] <= optimum+1e-9 and dense["true_upper_bound"] >= optimum-1e-9
    polished = polish_schedule(design, dense["rounded_selected"], time_limit=10)
    assert polished["status"] == "single_exchange_local_optimum"
    neighbors = []
    for dropped in polished["selected"]:
        for added in range(n):
            if added not in polished["selected"]:
                path = tuple(sorted((set(polished["selected"])-{dropped}) | {added}))
                neighbors.append(design.true_score(path))
    assert max(neighbors) <= polished["true_lower_bound"]+1e-11
    assert max(residuals.values()) < 1e-7, residuals
    # Analytic identical scenarios force a binary optimum with no uncertainty gap.
    single = NoisyDesign(np.array([[1.], [2.]]), 0., 0., 1., np.array([[1.]]), 1)
    analytic = RobustDesign((single, single), np.zeros(2))
    analytic_result = solve_dense_robust(analytic, time_limit=5)
    assert abs(analytic_result["true_upper_bound"]-math.log(5)) < 1e-7
    payload = {"status": "passed", "n": n, "p": p, "k": k,
        "schedules": len(paths), "residuals": residuals, "true_enumerated_optimum": optimum,
        "dual_lp_witness": lp_witness, "dense": dense, "polished": polished,
        "polished_neighbor_checks": len(neighbors), "analytic": analytic_result,
        "wall_seconds": perf_counter()-started,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    checkpoint(output, payload)
    print(json.dumps({key: payload[key] for key in ("status", "residuals", "wall_seconds")}), flush=True)
    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("validate", "compare"))
    parser.add_argument("--source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.mode == "validate":
        validate(args.output)
    else:
        if args.source is None:
            parser.error("--source required for comparison")
        run_comparison(args.source, args.output)
