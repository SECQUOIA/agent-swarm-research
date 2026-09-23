"""Shared-schedule robust D-design across a finite set of kinetic scenarios.

The objective is min_s(logdet(J_s)-offset_s). A common path mixture and
nonnegative scenario weights provide a numerical upper certificate. The
concatenated sensitivity array is only a linear-pricing device: cross-scenario
blocks are never interpreted as the information of a joint statistical model.
"""

import argparse
from dataclasses import asdict, dataclass
import hashlib
from itertools import combinations
import json
import math
import os
from pathlib import Path
from time import perf_counter

import numpy as np
from scipy.optimize import minimize

from noisy_markov_design import (CalendarOracle, NoisyDesign, TimeBudgetExceeded,
    check_memory, check_time, logdet, memory_estimate, solve_hull, spectral_delta)


HERE = Path(__file__).resolve().parent


def integer(value, name, minimum=0):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return int(value)


def selection(path, n, k=None):
    path = tuple(integer(i, "selected time") for i in path)
    if len(set(path)) != len(path) or any(i >= n for i in path) or (k is not None and len(path) != k):
        raise ValueError("invalid schedule indices or exact count")
    return tuple(sorted(path))


def probability(vector):
    vector = np.asarray(vector, dtype=float)
    if vector.ndim != 1 or not len(vector) or not np.isfinite(vector).all():
        raise ValueError("finite nonempty probability vector required")
    vector = np.maximum(vector, 0.)
    maximum = vector.max()
    if maximum <= 0:
        raise ValueError("probability vector has zero positive mass")
    # Finite entries may overflow their sum; scale first so accepted vectors
    # remain actual simplex points even for extreme finite dual multipliers.
    vector = vector/maximum
    return vector/vector.sum()


@dataclass
class RobustDesign:
    scenarios: tuple[NoisyDesign, ...]
    offsets: np.ndarray

    def __post_init__(self):
        self.scenarios = tuple(self.scenarios)
        if not self.scenarios:
            raise ValueError("at least one scenario required")
        self.offsets = np.asarray(self.offsets, dtype=float).copy()
        self.q = len(self.scenarios)
        if self.offsets.shape != (self.q,) or not np.isfinite(self.offsets).all():
            raise ValueError("one finite scalar offset per scenario required")
        first = self.scenarios[0]
        self.n, self.p, self.k = first.n, first.p, first.k
        common = (first.n, first.p, first.k, first.rho, first.latent_variance, first.nugget_variance)
        for scenario in self.scenarios:
            if (scenario.n, scenario.p, scenario.k, scenario.rho,
                    scenario.latent_variance, scenario.nugget_variance) != common:
                raise ValueError("prototype requires matching dimensions, count, and common covariance")

    def true_values(self, path):
        path = selection(path, self.n)
        return np.array([scenario.true_objective(path) for scenario in self.scenarios])

    def true_score(self, path):
        return float(np.min(self.true_values(path)-self.offsets))

    def pricing_container(self):
        p = self.p
        prior = np.zeros((self.q*p, self.q*p))
        for s, scenario in enumerate(self.scenarios):
            prior[s*p:(s+1)*p, s*p:(s+1)*p] = scenario.prior
        first = self.scenarios[0]
        return NoisyDesign(np.concatenate([s.F for s in self.scenarios], axis=1),
            first.rho, first.latent_variance, first.nugget_variance, prior, self.k)


def scenario_blocks(information, q, p):
    return np.array([information[s*p:(s+1)*p, s*p:(s+1)*p] for s in range(q)])


def diagonal_gradient(gradients):
    q, p, _ = gradients.shape
    combined = np.zeros((q*p, q*p))
    for s, gradient in enumerate(gradients):
        combined[s*p:(s+1)*p, s*p:(s+1)*p] = gradient
    return combined


def mixture_information(blocks, weights):
    return np.einsum("a,asij->sij", weights, np.asarray(blocks))


def values_and_gradients(blocks, weights, offsets):
    information = mixture_information(blocks, weights)
    inverses = np.linalg.inv(information)
    values = np.array([logdet(matrix) for matrix in information])-offsets
    gradients = np.einsum("sij,asji->sa", inverses, np.asarray(blocks))
    return values, gradients


def active_weights(values):
    active = values <= min(values)+1e-7
    return active/active.sum()


def correct_mixture(blocks, weights, offsets, deadline, max_iterations=200):
    """Feasible mixture retained even when the epigraph optimizer stops early."""
    weights = probability(weights)
    values, _ = values_and_gradients(blocks, weights, offsets)
    best, best_value = weights.copy(), float(values.min())
    path_count = len(weights)

    def objective(x):
        check_time(deadline)
        return -float(x[-1]), np.r_[np.zeros(path_count), -1.]

    def constraints(x):
        nonlocal best, best_value
        check_time(deadline)
        feasible = probability(x[:-1])
        feasible_values, _ = values_and_gradients(blocks, feasible, offsets)
        if feasible_values.min() > best_value:
            best, best_value = feasible.copy(), float(feasible_values.min())
        # SLSQP bounds keep the weights nonnegative; add the fixed prior through
        # each path matrix. An infeasible sum still leaves these matrices SPD.
        values, _ = values_and_gradients(blocks, x[:-1], offsets)
        return values-x[-1]

    def jacobian(x):
        check_time(deadline)
        _, gradients = values_and_gradients(blocks, x[:-1], offsets)
        return np.column_stack((gradients, -np.ones(len(offsets))))

    dual, success, message, iterations = active_weights(values), False, "not_started", 0
    try:
        output = minimize(objective, np.r_[weights, best_value], jac=True, method="SLSQP",
            bounds=[(0., 1.)]*path_count+[(None, None)],
            constraints=[{"type": "eq", "fun": lambda x: x[:-1].sum()-1,
                          "jac": lambda x: np.r_[np.ones(path_count), 0.]},
                         {"type": "ineq", "fun": constraints, "jac": jacobian}],
            options={"ftol": 1e-11, "maxiter": max_iterations, "disp": False})
        success, message, iterations = bool(output.success), str(output.message), int(output.nit)
        multipliers = np.asarray(getattr(output, "multipliers", []), dtype=float)
        if len(multipliers) == 1+len(offsets) and np.isfinite(multipliers[1:]).all() and np.maximum(multipliers[1:], 0).sum() > 0:
            dual = probability(multipliers[1:])
        else:
            dual = active_weights(values_and_gradients(blocks, best, offsets)[0])
    except TimeBudgetExceeded:
        message = "time_limit"
        dual = active_weights(values_and_gradients(blocks, best, offsets)[0])
    return best, dual, {"success": success, "message": message, "iterations": iterations}


def tangent_price(design, oracle, matrices, dual, *, deadline=math.inf, prior_aware=False):
    """A valid weighted tangent upper bound for any probability vector dual."""
    dual = probability(dual)
    scales = np.ones(design.q)
    references = matrices.copy()
    if prior_aware:
        for s, scenario in enumerate(design.scenarios):
            delta = spectral_delta(scenario, oracle.L)
            if delta >= 1:
                raise ValueError("memory correction unavailable")
            scales[s] = 1/(1-delta)
            references[s] = scenario.prior+(matrices[s]-scenario.prior)*scales[s]
    inverses = np.linalg.inv(references)
    gradient = diagonal_gradient(dual[:, None, None]*scales[:, None, None]*inverses)
    value, path = oracle.price(gradient, deadline=deadline)
    constants = np.array([logdet(references[s])-design.offsets[s]-design.p
        +np.trace(inverses[s] @ scenario.prior) for s, scenario in enumerate(design.scenarios)])
    upper = float(dual @ constants+value)
    return upper, path, {"prior_aware": prior_aware, "dual_weights": dual.tolist(),
        "hull_information": matrices.tolist(), "tangent_reference_information": references.tolist(),
        "scenario_constants": constants.tolist(), "scenario_scales": scales.tolist(),
        "arc_gradient_blocks": (dual[:, None, None]*scales[:, None, None]*inverses).tolist(),
        "priced_selection": path, "linear_price_excluding_prior": value, "upper_bound": upper}


def solve_robust_hull(design, L, *, initial_paths=(), time_limit=30,
                      max_memory_mb=256, max_rounds=100, hull_gap=1e-6):
    started = perf_counter()
    if not math.isfinite(time_limit) or not 0 < time_limit <= 30 or not math.isfinite(hull_gap) or hull_gap <= 0:
        raise ValueError("invalid time limit or hull gap")
    max_rounds = integer(max_rounds, "max_rounds", 1)
    L = integer(L, "L")
    if min(L, design.n-1) > 30:
        raise MemoryError("history width above 30 refused before covariance allocation")
    deadline = started+time_limit
    container = design.pricing_container()
    initial_paths = [selection(path, design.n, design.k) for path in initial_paths]
    seed = tuple(np.linspace(0, design.n-1, design.k, dtype=int).tolist()) if design.k else ()
    initial_paths = list(dict.fromkeys([seed]+initial_paths))
    estimate = memory_estimate(container, L, max_rounds+len(initial_paths))
    result = {"status": "not_started", "selected": None, "true_lower_bound": None,
        "true_upper_bound": None, "surrogate_hull_value": None, "surrogate_upper_bound": None,
        "surrogate_hull_gap": None, "true_gap": None, "L": L, "memory": estimate,
        "time_limit": time_limit, "pricing_rounds": 0, "correction_failures": 0,
        "history": [], "hull_support": [], "hull_information": None,
        "dual_weights": None, "upper_bound_witness": None, "prior_aware_witness": None}
    blocks, paths, weights, dual = [], [], np.empty(0), np.full(design.q, 1/design.q)
    try:
        check_memory(estimate, max_memory_mb)
        check_time(deadline)
        for path in initial_paths:
            value = design.true_score(path)
            if result["true_lower_bound"] is None or value > result["true_lower_bound"]:
                result["selected"], result["true_lower_bound"] = path, value
        full = design.true_score(tuple(range(design.n)))
        result["full_selection_upper_bound"] = full
        result["true_upper_bound"] = full
        oracle = CalendarOracle(container, L, deadline=deadline, max_memory_mb=max_memory_mb,
                                max_paths=max_rounds+len(initial_paths))
        paths = initial_paths.copy()
        blocks = [scenario_blocks(oracle.information(path), design.q, design.p) for path in paths]
        weights = np.full(len(paths), 1/len(paths))
        result["preprocessing_seconds"] = perf_counter()-started
        result["status"] = "iteration_limit"
        correction = None
        for _ in range(max_rounds):
            check_time(deadline)
            weights, dual, correction = correct_mixture(blocks, weights, design.offsets, deadline)
            result["correction_failures"] += int(not correction["success"])
            M = mixture_information(blocks, weights)
            surrogate_value = float(min(logdet(M[s])-design.offsets[s] for s in range(design.q)))
            result["surrogate_hull_value"] = surrogate_value
            if correction["message"] == "time_limit":
                result["status"] = "time_limit"
                break
            upper, path, witness = tangent_price(design, oracle, M, dual, deadline=deadline)
            result["pricing_rounds"] += 1
            if result["surrogate_upper_bound"] is None or upper < result["surrogate_upper_bound"]:
                result["surrogate_upper_bound"], result["upper_bound_witness"] = upper, witness
            value = design.true_score(path)
            if value > result["true_lower_bound"]:
                result["selected"], result["true_lower_bound"] = path, value
            deltas = [spectral_delta(scenario, L) for scenario in design.scenarios]
            if max(deltas) < 1:
                transfer = result["surrogate_upper_bound"]+max(-design.p*math.log1p(-d) for d in deltas)
                result["true_upper_bound"] = min(result["true_upper_bound"], transfer)
            gap = result["surrogate_upper_bound"]-surrogate_value
            result["history"].append({"pricing_round": result["pricing_rounds"],
                "surrogate_value": surrogate_value, "surrogate_upper": result["surrogate_upper_bound"],
                "true_lower": result["true_lower_bound"], "true_upper": result["true_upper_bound"],
                "dual_weights": dual.tolist(), "correction": correction,
                "wall_seconds": perf_counter()-started})
            if gap < -1e-7 or result["true_upper_bound"] < result["true_lower_bound"]-1e-7:
                result["status"] = "numerical_bound_inconsistency"
                break
            if gap <= hull_gap:
                result["status"] = "surrogate_hull_optimal_tolerance"
                break
            if path in paths:
                result["status"] = "pricing_repeated_path"
                break
            paths.append(path)
            blocks.append(scenario_blocks(oracle.information(path), design.q, design.p))
            weights = np.r_[weights, 0.]
        if weights.size and perf_counter() < deadline:
            M = mixture_information(blocks, weights)
            if all(spectral_delta(scenario, L) < 1 for scenario in design.scenarios):
                upper, path, witness = tangent_price(design, oracle, M, dual, deadline=deadline, prior_aware=True)
                result["prior_aware_witness"] = witness
                result["true_upper_bound"] = min(result["true_upper_bound"], upper)
                value = design.true_score(path)
                if value > result["true_lower_bound"]:
                    result["selected"], result["true_lower_bound"] = path, value
    except (TimeBudgetExceeded, MemoryError) as error:
        result["status"] = "time_limit" if isinstance(error, TimeBudgetExceeded) else "memory_limit"
        result["message"] = str(error)
    if weights.size:
        result["hull_information"] = mixture_information(blocks, weights).tolist()
        result["surrogate_hull_value"] = min(logdet(matrix)-offset for matrix, offset in
            zip(mixture_information(blocks, weights), design.offsets))
        result["dual_weights"] = dual.tolist()
        result["hull_support"] = [{"selected": path, "weight": float(weight),
            "scenario_information": block.tolist()} for path, weight, block in zip(paths, weights, blocks)]
    if result["surrogate_upper_bound"] is not None:
        result["surrogate_hull_gap"] = result["surrogate_upper_bound"]-result["surrogate_hull_value"]
    if result["true_lower_bound"] is not None and result["true_upper_bound"] is not None:
        result["true_gap"] = result["true_upper_bound"]-result["true_lower_bound"]
        if result["true_gap"] < -1e-7:
            result["status"] = "numerical_bound_inconsistency"
        result["selected_scenario_logdet"] = design.true_values(result["selected"]).tolist()
        result["selected_raw_worst_logdet"] = min(result["selected_scenario_logdet"])
    result["wall_seconds"] = perf_counter()-started
    return result


def greedy_exchange(design, *, time_limit=30):
    started = perf_counter()
    if not math.isfinite(time_limit) or not 0 < time_limit <= 30:
        raise ValueError("time_limit must lie in (0,30]")
    deadline = started+time_limit
    seed = tuple(np.linspace(0, design.n-1, design.k, dtype=int).tolist()) if design.k else ()
    selected, lower = seed, design.true_score(seed)
    count, exchanges = 1, 0
    current, current_value = (), design.true_score(())
    greedy_path = greedy_value = None
    exchange_start = None
    status = "time_limit"

    def evaluate(path):
        nonlocal count, selected, lower
        check_time(deadline)
        value = design.true_score(path)
        count += 1
        if len(path) == design.k and value > lower:
            selected, lower = path, value
        return value

    try:
        for _ in range(design.k):
            best, best_value = None, -math.inf
            for t in range(design.n):
                if t in current:
                    continue
                path = tuple(sorted((*current, t)))
                value = evaluate(path)
                if value > best_value:
                    best, best_value = path, value
            current, current_value = best, best_value
        greedy_path, greedy_value = current, current_value
        # A retained feasible seed can beat the complete greedy branch. Start
        # exchanges from that incumbent so a local-optimum status describes
        # the path actually returned, not a different completed search.
        if lower > current_value:
            current, current_value = selected, lower
        exchange_start = current
        while True:
            best, best_value = current, current_value
            for dropped in current:
                for added in range(design.n):
                    if added in current:
                        continue
                    path = tuple(sorted((set(current)-{dropped}) | {added}))
                    value = evaluate(path)
                    if value > best_value+1e-11:
                        best, best_value = path, value
            if best == current:
                selected, lower = current, current_value
                status = "single_exchange_local_optimum"
                break
            current, current_value = best, best_value
            exchanges += 1
    except TimeBudgetExceeded:
        pass
    return {"status": status, "selected": selected, "true_lower_bound": lower,
        "selected_scenario_logdet": design.true_values(selected).tolist(),
        "greedy_selected": greedy_path, "greedy_score": greedy_value,
        "exchange_start_selected": exchange_start,
        "exchange_selected": current if exchange_start is not None else None,
        "accepted_exchanges": exchanges, "objective_evaluations": count,
        "wall_seconds": perf_counter()-started, "time_limit": time_limit}


def reaction_sensitivity(n, A0, k1, k2):
    if min(A0, k1, k2) <= 0 or abs(k1-k2) < 1e-6:
        raise ValueError("positive separated nominal parameters required")
    t = 12*np.arange(1, n+1)/n
    difference = k2-k1
    e1, e2 = np.exp(-k1*t), np.exp(-k2*t)
    F = np.column_stack((A0*k1/difference*(e1-e2),
        A0*k1*(k2/difference**2*(e1-e2)-k1/difference*t*e1),
        A0*k2*(-k1/difference**2*(e1-e2)+k1/difference*t*e2)))
    theta = np.log([A0, k1, k2]).astype(complex)
    checked = np.empty_like(F)
    for j in range(3):
        perturbed = theta.copy()
        perturbed[j] += 1e-25j
        a, b, c = np.exp(perturbed)
        checked[:, j] = (a*b/(c-b)*(np.exp(-b*t)-np.exp(-c*t))).imag/1e-25
    error = float(np.max(abs(F-checked)))
    if error > 1e-11:
        raise ArithmeticError("kinetic sensitivity complex-step check failed")
    return F, {"A0": A0, "k1": k1, "k2": k2, "times": t.tolist(),
        "parameter_names": ["log(A0)", "log(k1)", "log(k2)"],
        "complex_step_max_error": error, "horizon": 12.}


def chemical_scenarios(n):
    scenarios, inputs = [], []
    for name, k1, k2 in (("early", .7, .2), ("central", .4, .1), ("late", .18, .045)):
        F, kinetics = reaction_sensitivity(n, 1., k1, k2)
        design = NoisyDesign(F, .4, .00125, .00125, .01*np.eye(3), n//3)
        scenarios.append(design)
        inputs.append({"name": name, "n": n, "p": 3, "k": n//3,
            "F": F.tolist(), "prior": design.prior.tolist(), "rho": design.rho,
            "latent_variance": design.latent_variance, "nugget_variance": design.nugget_variance,
            "kinetics": kinetics})
    return tuple(scenarios), inputs


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
    print(json.dumps({"run": label, **{key: result[key] for key in ("status", "true_lower_bound",
        "true_upper_bound", "true_gap", "surrogate_hull_gap", "wall_seconds") if key in result}}), flush=True)
    return result


def evaluation(design, path, reference_lower, reference_upper):
    values = design.true_values(path)
    return {"selected": path, "scenario_logdet": values.tolist(),
        "fixed_offset_score": float(min(values-design.offsets)), "raw_worst_logdet": float(min(values)),
        "standardized_score_lower": float(min(values-reference_upper)),
        "standardized_score_upper": float(min(values-reference_lower)),
        "scenario_logdet_loss_to_reference": (reference_lower-values).tolist(),
        "scenario_efficiency_lower": np.exp((values-reference_upper)/design.p).tolist(),
        "scenario_efficiency_upper": np.exp((values-reference_lower)/design.p).tolist()}


def run_probe(n, output):
    pipeline_started = perf_counter()
    scenarios, scenario_inputs = chemical_scenarios(n)
    L = 8
    payload = {"metadata": {"source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "reviewed_core_sha256": hashlib.sha256((HERE/"noisy_markov_design.py").read_bytes()).hexdigest(),
        "criterion": "min_s(logdet J_s-offset_s), offsets are feasible individual reference scores",
        "scope": "floating-point numerical bounds; stipulated common AR1+nugget covariance and local reaction sensitivities",
        "normalization": "reference lower/upper intervals bound efficiency relative to each unknown individual optimum",
        "covariance_interpretation": "one common stipulated covariance across scenarios; cross-scenario pricing blocks are not a joint statistical model",
        "time_grid_caveat": "fixed horizon and fixed per-grid rho; n changes physical correlation scale",
        "parameter_caveat": "local Fisher criterion; known covariance; B(t) with unknown A0 has a global rate-swap ambiguity",
        "reference_time_limit": 5, "robust_time_limit": 30, "greedy_time_limit": 30,
        "max_memory_mb": 256, "blas_environment": {key: os.environ.get(key) for key in
            ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")}},
        "n": n, "p": 3, "k": n//3, "L": L, "scenarios": scenario_inputs,
        "references": [], "offsets": None, "robust": None, "greedy_exchange": None,
        "evaluations": None, "complete": False}
    checkpoint(output, payload)
    for scenario, record in zip(scenarios, scenario_inputs):
        reference = attempt(record["name"]+"-reference", lambda scenario=scenario: asdict(solve_hull(scenario, L, time_limit=5)))
        payload["references"].append({"scenario_name": record["name"], "L": L, "hull": reference})
        checkpoint(output, payload)
    if any(item["hull"].get("true_lower_bound") is None or item["hull"].get("true_upper_bound") is None for item in payload["references"]):
        payload["status"] = "reference_failure"
        payload["pipeline_wall_seconds"] = perf_counter()-pipeline_started
        checkpoint(output, payload)
        return payload
    lower = np.array([item["hull"]["true_lower_bound"] for item in payload["references"]])
    upper = np.array([item["hull"]["true_upper_bound"] for item in payload["references"]])
    payload["offsets"] = lower.tolist()
    design = RobustDesign(scenarios, lower)
    paths = [item["hull"]["selected"] for item in payload["references"]]
    payload["robust"] = attempt(f"n{n}-robust", lambda: solve_robust_hull(design, L, initial_paths=paths))
    checkpoint(output, payload)
    payload["greedy_exchange"] = attempt(f"n{n}-greedy", lambda: greedy_exchange(design))
    checkpoint(output, payload)
    payload["evaluations"] = {"individual_designs": [evaluation(design, path, lower, upper) for path in paths],
        "nominal_central": evaluation(design, paths[1], lower, upper)}
    for label in ("robust", "greedy_exchange"):
        if payload[label].get("selected") is not None:
            payload["evaluations"][label] = evaluation(design, payload[label]["selected"], lower, upper)
    payload["reference_wall_seconds"] = sum(item["hull"]["wall_seconds"] for item in payload["references"])
    payload["robust_pipeline_seconds"] = payload["reference_wall_seconds"]+payload["robust"]["wall_seconds"]
    payload["greedy_pipeline_seconds"] = payload["reference_wall_seconds"]+payload["greedy_exchange"]["wall_seconds"]
    payload["pipeline_wall_seconds"] = perf_counter()-pipeline_started
    payload["complete"] = True
    checkpoint(output, payload)
    return payload


def validate(output):
    started = perf_counter()
    rng = np.random.default_rng(9723)
    n, p, k = 10, 2, 3
    scenarios = tuple(NoisyDesign(rng.integers(-8, 9, size=(n, p))/10, .4, 1., 1., .1*np.eye(p), k) for _ in range(3))
    schedules = list(combinations(range(n), k))
    true = np.array([[scenario.true_objective(path) for scenario in scenarios] for path in schedules])
    offsets = true.max(axis=0)
    design = RobustDesign(scenarios, offsets)
    optimum = float(np.min(true-offsets, axis=1).max())
    residuals = {"diagonal_blocks": 0., "weighted_prices": 0., "tangent_excess": 0.,
        "mixture_gradient": 0., "probability_residual": 0.}
    rows = []
    for L in (0, 2, 6, 9):
        joint = CalendarOracle(design.pricing_container(), L)
        singles = [CalendarOracle(scenario, L) for scenario in scenarios]
        path_blocks = []
        for path in schedules:
            block = scenario_blocks(joint.information(path), design.q, design.p)
            independent = np.array([oracle.information(path) for oracle in singles])
            residuals["diagonal_blocks"] = max(residuals["diagonal_blocks"], float(np.max(abs(block-independent))))
            path_blocks.append(block)
        weights = probability(rng.uniform(.1, 1, 5))
        indices = rng.choice(len(schedules), 5, replace=False)
        M = mixture_information(np.array(path_blocks)[indices], weights)
        dual = probability(rng.uniform(.1, 1, design.q))
        bound, path, witness = tangent_price(design, joint, M, dual)
        H = np.array(witness["arc_gradient_blocks"])
        expected = max(float(np.einsum("sij,sji->", H, block-np.array([s.prior for s in scenarios]))) for block in path_blocks)
        residuals["weighted_prices"] = max(residuals["weighted_prices"], abs(witness["linear_price_excluding_prior"]-expected))
        surrogate_best = max(min(logdet(block[s])-offsets[s] for s in range(design.q)) for block in path_blocks)
        residuals["tangent_excess"] = max(residuals["tangent_excess"], surrogate_best-bound)
        result = solve_robust_hull(design, L, time_limit=10)
        assert result["true_lower_bound"] <= optimum+1e-8 and result["true_upper_bound"] >= optimum-1e-8
        if L == 9:
            blocks = np.array(path_blocks)
            w = np.full(len(schedules), 1/len(schedules))
            all_weights, _, closure = correct_mixture(blocks, w, offsets, perf_counter()+10)
            exhaustive_hull = min(logdet(M)-offset for M, offset in zip(mixture_information(blocks, all_weights), offsets))
            assert result["surrogate_upper_bound"] >= exhaustive_hull-1e-7
            assert abs(result["surrogate_hull_value"]-exhaustive_hull) < 2e-6
            result["independent_all_schedule_hull_value"] = exhaustive_hull
        rows.append({"L": L, "true_enumerated_optimum": optimum, "result": result})
    small_blocks = np.array(path_blocks[:4])
    w = np.full(4, .25)
    value, gradient = values_and_gradients(small_blocks, w, offsets)
    for j in range(4):
        step = np.zeros(4)
        step[j] = 1e-6
        finite = (values_and_gradients(small_blocks, w+step, offsets)[0]-values_and_gradients(small_blocks, w-step, offsets)[0])/2e-6
        residuals["mixture_gradient"] = max(residuals["mixture_gradient"], float(np.max(abs(finite-gradient[:, j]))))
    # One scalar information parameter and two scenarios give an analytic hull:
    # paths score (2,1) and (1,2), so the equal mixture has min logdet log(1.5).
    analytic_blocks = np.array([[[[2.]], [[1.]]], [[[1.]], [[2.]]]])
    aw, ad, correction = correct_mixture(analytic_blocks, np.array([.8, .2]), np.zeros(2), perf_counter()+5)
    assert np.max(abs(aw-.5)) < 1e-6 and np.max(abs(ad-.5)) < 1e-6
    assert abs(min(logdet(m) for m in mixture_information(analytic_blocks, aw))-math.log(1.5)) < 1e-8
    for scale in (1e308, 1e-308):
        residuals["probability_residual"] = max(residuals["probability_residual"],
            float(np.max(abs(probability([scale, scale])-.5))))
    identical = NoisyDesign(np.ones((2, 1)), 0., 0., 1., np.array([[2.]]), 1)
    extreme = RobustDesign((identical, identical), np.zeros(2))
    extreme_oracle = CalendarOracle(extreme.pricing_container(), 0)
    centers = scenario_blocks(extreme_oracle.information((0,)), 2, 1)
    extreme_upper, _, _ = tangent_price(extreme, extreme_oracle, centers, [1e308, 1e308])
    assert abs(extreme_upper-math.log(3)) < 1e-12
    seed_case_F = .2*np.array([
        [[-4, 0], [0, 2], [4, 3], [0, 0], [4, 1], [-3, 0], [0, 4]],
        [[0, 0], [-2, 0], [-2, 2], [-3, -3], [-1, 2], [-1, 1], [1, 0]],
        [[4, 0], [2, -1], [-3, 0], [0, 3], [0, 4], [-3, -3], [-1, -2]]])
    seed_case = RobustDesign(tuple(NoisyDesign(f, .5, 1., 1., .1*np.eye(2), 3) for f in seed_case_F),
        np.array([-.8704014586967649, -1.752401402870794, -.8976081574756385]))
    seed_result = greedy_exchange(seed_case, time_limit=5)
    assert seed_result["status"] == "single_exchange_local_optimum"
    assert seed_result["selected"] == seed_result["exchange_selected"]
    for dropped in seed_result["selected"]:
        for added in range(seed_case.n):
            if added not in seed_result["selected"]:
                neighbor = tuple(sorted((set(seed_result["selected"])-{dropped}) | {added}))
                assert seed_case.true_score(neighbor) <= seed_result["true_lower_bound"]+1e-11
    assert max(residuals.values()) < 1e-7, residuals
    # Immediate deadline and memory refusal must not fabricate a path bound.
    cap = solve_robust_hull(design, 9, time_limit=1e-12)
    refusal = solve_robust_hull(design, 9, max_memory_mb=1e-10)
    assert cap["status"] == "time_limit" and cap["true_lower_bound"] is None
    assert refusal["status"] == "memory_limit" and refusal["true_lower_bound"] is None
    chem, _ = chemical_scenarios(12)
    payload = {"status": "passed", "n": n, "p": p, "k": k, "scenarios": 3,
        "enumerated_schedules": len(schedules), "windows": [0, 2, 6, 9],
        "residuals": residuals, "rows": rows, "analytic_dual": ad.tolist(),
        "analytic_mixture": aw.tolist(), "cap": cap, "memory_refusal": refusal,
        "retained_seed_exchange_regression": seed_result,
        "chemical_sensitivity_shapes": [list(s.F.shape) for s in chem],
        "wall_seconds": perf_counter()-started,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    checkpoint(output, payload)
    print(json.dumps({key: payload[key] for key in ("status", "residuals", "wall_seconds")}), flush=True)
    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("validate", "probe"))
    parser.add_argument("--n", type=int, choices=(48, 96), default=48)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.mode == "validate":
        validate(args.output)
    else:
        run_probe(args.n, args.output)
