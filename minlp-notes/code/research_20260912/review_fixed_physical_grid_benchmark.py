"""Fresh bounded review of the fixed physical grid benchmark.

Saved data are reconstructed with covariance principal blocks and a separate
vectorized count/history recurrence. Tiny tests exercise the real solver;
deterministic clock stubs exercise driver accounting and preserved failures.
This does not rerun the saved 30-second MIPs or issue exact certificates.
"""

from collections import Counter
from contextlib import ExitStack, redirect_stdout
from copy import deepcopy
from dataclasses import dataclass
from fractions import Fraction as Q
import hashlib
from io import StringIO
from itertools import combinations
import json
import math
import os
from pathlib import Path
import platform
import sys
from tempfile import TemporaryDirectory
from time import perf_counter
from unittest.mock import patch

import numpy as np
import scipy
from scipy.integrate import solve_ivp

import fixed_physical_grid_benchmark as producer
import noisy_markov_design as core


HERE = Path(__file__).resolve().parent
INPUT = HERE / "results/fixed-physical-grid-benchmark.json"
OUTPUT = HERE / "results/fixed-physical-grid-independent-review.json"
COUNTS = Counter()
ERRORS = Counter()


def check(condition, label):
    assert condition, label
    COUNTS[label] += 1


def close(actual, expected, label, tolerance=2e-9):
    error = float(np.max(np.abs(np.asarray(actual)-np.asarray(expected))))
    assert error <= tolerance, (label, error, tolerance)
    COUNTS[label] += 1
    ERRORS[label] = max(ERRORS[label], error)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def information(case, selected):
    F = np.asarray(case["F"])[list(selected)]
    rho, latent, nugget = (float(Q(case[key])) for key in
                           ("rho", "latent_variance", "nugget_variance"))
    indices = np.asarray(selected)
    R = latent*rho**np.abs(indices[:, None]-indices)+nugget*np.eye(len(indices))
    return np.asarray(case["prior"])+F.T@np.linalg.solve(R, F)


def objective(case, selected):
    sign, value = np.linalg.slogdet(information(case, selected))
    check(sign > 0, "positive_information_determinant")
    return float(value)


def local_information(case, selected, L):
    rho, latent, nugget = (float(Q(case[key])) for key in
                           ("rho", "latent_variance", "nugget_variance"))
    F = np.asarray(case["F"])
    J = np.array(case["prior"])
    for t in sorted(selected):
        history = np.array([s for s in selected if t-L <= s < t], dtype=int)
        residual, variance = F[t].copy(), latent+nugget
        if len(history):
            R = latent*rho**np.abs(history[:, None]-history)+nugget*np.eye(len(history))
            cov = latent*rho**(t-history)
            beta = np.linalg.solve(R, cov)
            residual -= beta@F[history]
            variance -= cov@beta
        J += np.outer(residual, residual)/variance
    return J


def independent_arc_information(case, L):
    """Stationarity permits one covariance regression per history mask."""
    n, p = case["n"], case["p"]
    rho, latent, nugget = (float(Q(case[key])) for key in
                           ("rho", "latent_variance", "nugget_variance"))
    F = np.asarray(case["F"])
    matrices = np.zeros((n, 1 << L, p, p))
    for mask in range(1 << L):
        distances = np.array([d for d in range(1, L+1) if mask & (1 << (d-1))], dtype=int)
        earliest = max(distances, default=0)
        residual = F[earliest:].copy()
        variance = latent+nugget
        if len(distances):
            R = latent*rho**np.abs(distances[:, None]-distances)+nugget*np.eye(len(distances))
            cov = latent*rho**distances
            beta = np.linalg.solve(R, cov)
            for d, coefficient in zip(distances, beta):
                residual -= coefficient*F[earliest-d:n-d]
            variance -= cov@beta
        matrices[earliest:, mask] = np.einsum("ti,tj->tij", residual, residual)/variance
    return matrices


def independent_price(arc_matrices, H, k):
    """Array recurrence; no production oracle, path cache or backpointers."""
    n, masks = arc_matrices.shape[:2]
    scores = np.einsum("tmij,ji->tm", arc_matrices, H)
    values = np.full((k+1, masks), -np.inf)
    values[0, 0] = 0
    for t in range(n):
        updated = np.full_like(values, -np.inf)
        if masks == 1:
            updated[:] = values
            updated[1:, 0] = np.maximum(updated[1:, 0], values[:-1, 0]+scores[t, 0])
        else:
            half = masks//2
            updated[:, ::2] = np.maximum(values[:, :half], values[:, half:])
            chosen = values[:-1]+scores[t]
            updated[1:, 1::2] = np.maximum(chosen[:, :half], chosen[:, half:])
        values = updated
    return float(values[k].max())


def estimate(n, p, k, L):
    masks = 2**min(L, n-1)
    return (8*n*masks*p*p + 5*n*(k+1)*masks + 16*(k+1)*masks
            + 8*101*p*p + 64*101*n + 64*101*101 + 8*n*masks + 64*n*n)


def core_delta(n, L, rho):
    if L >= n-1:
        return Q(0)
    return 2*rho**(L+1)/(1-rho)*(1+Q(1, 2)*sum(rho**i for i in range(1, L+1)))


def refined_delta(n, L, rho):
    """Independent scalar variance recursion and gap-one pair row sum."""
    latent = nugget = Q(1, 800)
    P = latent
    for _ in range(L):
        P = rho*rho*P*nugget/(P+nugget)+latent*(1-rho*rho)
    if L >= n-1:
        return Q(0)
    pairs = [Q(0)]
    for h in range(1, n):
        pairs.append(latent*rho**h if h > L else
                     latent*Q(1, 4)*rho**h*sum(
                         (rho**(2*d) for d in range(max(1, L+1-h), L+1)), Q(0)))
    prefix = [Q(0)]
    for value in pairs[1:]:
        prefix.append(prefix[-1]+value)
    return max(prefix[t]+prefix[n-1-t] for t in range(n))/(P+nugget)


def check_preflight(case):
    pre = case["preflight"]
    n, p, k, rho = case["n"], case["p"], case["k"], Q(case["rho"])
    cap = 256*2**20
    feasible = max(L for L in range(n) if estimate(n, p, k, L) <= cap)
    check(pre["largest_window_under_workspace_estimate"] == feasible, "largest_estimated_window")
    check(estimate(n, p, k, pre["scheduled_primary_window"]) <= cap, "scheduled_window_estimate")
    first = {}
    for row in pre["evaluated_windows"]:
        L = row["L"]
        check(row["estimated_workspace_bytes"] == estimate(n, p, k, L), "workspace_formula")
        for name, delta in (("core", core_delta(n, L, rho)),
                            ("reviewed_refined", refined_delta(n, L, rho))):
            close(float(delta), row[name+"_delta"], "preflight_"+name, 2e-12)
            if delta >= 1:
                continue
            one = -p*math.log1p(-float(delta))
            two = p*(math.log1p(float(delta))-math.log1p(-float(delta)))
            for criterion, value in (("one_sided_log_correction", one),
                                     ("two_sided_surrogate_optimizer_loss", two)):
                key = name+"_"+criterion
                if value <= .01 and key not in first:
                    first[key] = (L, value)
    check(set(first) == set(pre["first_windows"]), "preflight_criteria_complete")
    for key, (L, value) in first.items():
        check(pre["first_windows"][key]["L"] == L, "first_sufficient_window")
        close(value, pre["first_windows"][key]["bound_component"], "preflight_target_formula")
    check("not necessary" in pre["interpretation"], "sufficiency_caveat")
    return {"n": n, "largest_estimated_window": feasible,
            "first_sufficient_windows": {key: L for key, (L, _) in first.items()}}


def check_model(cases):
    reports = []
    for case in cases:
        n = case["n"]
        check(case["k"] == 16 and case["p"] == 3, "fixed_budget_dimension")
        exact_times = [Q(12*(i+1), n) for i in range(n)]
        check([Q(t) for t in case["kinetics"]["candidate_times"]] == exact_times, "exact_time_grid")
        close(case["prior"], .01*np.eye(3), "fixed_prior", 0)
        check(Q(case["latent_variance"]) == Q(case["nugget_variance"]) == Q(1, 800), "fixed_variances")
        check(Q(case["rho"]) == Q(4, 5)**(192//n), "fixed_covariance_rate")
        # Independent augmented mass balances in concentration coordinates.
        k1, k2 = .7, .2
        A = np.array([[-k1, 0., 0.], [k1, -k2, 0.], [0., k2, 0.]])
        B1 = np.array([[-k1, 0., 0.], [k1, 0., 0.], [0., 0., 0.]])
        B2 = np.array([[0., 0., 0.], [0., -k2, 0.], [0., k2, 0.]])
        def balances(_, y):
            x, s0, s1, s2 = y.reshape(4, 3)
            return np.r_[A@x, A@s0, A@s1+B1@x, A@s2+B2@x]
        y0 = np.zeros(12)
        y0[[0, 3]] = 1
        solution = solve_ivp(balances, (0., 12.), y0, t_eval=list(map(float, exact_times)),
                             method="DOP853", rtol=2e-13, atol=2e-14)
        check(solution.success, "augmented_ode_success")
        close(solution.y[[4, 7, 10]].T, case["F"], "ode_sensitivities", 2e-11)
        close(solution.y[1], case["kinetics"]["mean_B"], "ode_mean", 2e-11)
        reports.append(check_preflight(case))
    for coarse, fine in ((cases[0], cases[1]), (cases[1], cases[2]), (cases[0], cases[2])):
        factor = fine["n"]//coarse["n"]
        indices = [factor*(j+1)-1 for j in range(coarse["n"])]
        close(np.asarray(fine["F"])[indices], coarse["F"], "identical_shared_sensitivities", 0)
        check(Q(fine["rho"])**factor == Q(coarse["rho"]), "exact_nested_covariance")
        # Every covariance entry on a shared grid is equal as a rational.
        for lag in range(coarse["n"]):
            check(Q(coarse["rho"])**lag == Q(fine["rho"])**(factor*lag), "rational_covariance_lag")
    return reports


def valid_selection(case, selected):
    check(len(selected) == len(set(selected)) == 16 and
          all(isinstance(j, int) and 0 <= j < case["n"] for j in selected), "valid_saved_selection")


def check_results(case):
    report = {"n": case["n"], "methods": []}
    shared = case["greedy_exchange"]
    valid_selection(case, shared["selected"])
    lower = objective(case, shared["selected"])
    close(lower, shared["true_lower_bound"], "shared_true_objective")
    close(lower, shared["true_objective_recheck"], "shared_recheck")
    check(shared["status"] == "single_exchange_local_optimum", "completed_shared_exchange")
    # Independently check the claimed single-exchange local optimum.
    improvement = -math.inf
    for dropped in shared["selected"]:
        for added in range(case["n"]):
            if added not in shared["selected"]:
                path = sorted((set(shared["selected"])-{dropped}) | {added})
                improvement = max(improvement, objective(case, path)-lower)
    check(improvement <= 2e-10, "independent_single_exchange_optimum")
    report["best_single_exchange_improvement"] = improvement
    full = objective(case, list(range(case["n"])))
    common = case["common_setup_seconds"]+shared["shared_total_seconds"]
    close(case["common_setup_seconds"], case["data_construction_seconds"]+
          case["preflight"]["preflight_seconds"], "common_setup_accounting", 1e-12)
    check(shared["shared_total_seconds"] >= shared["measured_invocation_seconds"] >=
          shared["wall_seconds"], "shared_full_invocation_charged")
    for result in [*case["hulls"], case["dense_oa"]]:
        hull = "L" in result
        valid_selection(case, result["selected"])
        valid_selection(case, result["combined_selected"])
        own = objective(case, result["selected"])
        close(own, result["true_lower_bound" if hull else "lower_bound"], "method_true_objective")
        combined = objective(case, result["combined_selected"])
        close(combined, result["combined_true_lower_bound"], "combined_true_objective")
        close(combined, max(lower, own), "combined_incumbent_maximum")
        close(result["selected_times"], np.asarray(case["kinetics"]["candidate_times"])[result["combined_selected"]],
              "combined_selected_times", 0)
        upper = result["true_upper_bound" if hull else "upper_bound"]
        close(upper, result["combined_true_upper_bound"], "combined_upper_unchanged", 0)
        gap = upper-combined
        close(gap, result["combined_true_gap"], "combined_gap", 1e-12)
        check(result["target_gap_met_numerically"] == (-1e-7 <= gap <= .01), "target_status")
        close(result["solver_time_limit_seconds"], 30-common, "shared_cost_deducted", 1e-12)
        pipeline = common+result["measured_invocation_seconds"]+result["postprocessing_seconds"]
        close(pipeline, result["pipeline_seconds"], "pipeline_accounting", 1e-12)
        close(max(0, pipeline-30), result["pipeline_cap_overrun_seconds"], "cap_overrun_recorded", 1e-12)
        check(result["measured_invocation_seconds"] >= result["wall_seconds"], "outer_timer_covers_return")
        if hull:
            close(full, result["full_selection_upper_bound"], "full_selection_upper_bound")
            mixture = np.zeros((3, 3))
            weights = [point["weight"] for point in result["hull_support"]]
            close(sum(weights), 1, "support_weights_sum", 1e-12)
            check(min(weights) >= 0, "support_weights_nonnegative")
            for point in result["hull_support"]:
                valid_selection(case, point["selected"])
                J = local_information(case, point["selected"], result["L"])
                close(J, point["information"], "saved_local_information")
                mixture += point["weight"]*J
            close(mixture, result["hull_information"], "saved_hull_mixture")
            close(np.linalg.slogdet(mixture)[1], result["surrogate_hull_value"], "saved_hull_logdet")
            if result["pricing_rounds"] == 0:
                check(result["upper_bound_witness"] is None and result["surrogate_upper_bound"] is None
                      and result["transferred_upper_bound"] is None and result["prior_aware_witness"] is None,
                      "no_price_no_hull_bound")
                close(upper, result["full_selection_upper_bound"], "no_price_uses_full_selection", 0)
                check(result["generated_paths"] == 1, "construction_completed_before_first_price_timeout")
            else:
                arcs = independent_arc_information(case, result["L"])
                prior = np.asarray(case["prior"])
                witness = result["upper_bound_witness"]
                M = np.asarray(witness["hull_information"])
                H = np.linalg.inv(M)
                close(H, witness["gradient"], "witness_gradient")
                price = independent_price(arcs, H, 16)
                close(price, witness["linear_price_excluding_prior"], "independent_global_linear_price", 2e-8)
                close(price, np.trace(H@(local_information(case, witness["priced_selection"], result["L"])-prior)),
                      "priced_path_attains_global_price", 2e-8)
                bound = np.linalg.slogdet(M)[1]+np.trace(H@prior)+price-3
                close(bound, result["surrogate_upper_bound"], "surrogate_upper_reconstructed", 2e-8)
                transferred = bound-3*math.log1p(-result["delta"])
                close(transferred, result["transferred_upper_bound"], "transfer_bound_reconstructed", 2e-8)
                prior_bound = result["prior_aware_upper_bound"]
                if prior_bound is not None:
                    witness = result["prior_aware_witness"]
                    M = np.asarray(witness["surrogate_hull_information"])
                    N = prior+(M-prior)/(1-result["delta"])
                    H = np.linalg.inv(N)/(1-result["delta"])
                    close(N, witness["N"], "prior_aware_N")
                    close(H, witness["arc_gradient"], "prior_aware_gradient")
                    price = independent_price(arcs, H, 16)
                    close(price, witness["linear_price_excluding_prior"], "independent_prior_aware_price", 2e-8)
                    close(price, np.trace(H@(local_information(case, witness["priced_selection"], result["L"])-prior)),
                          "prior_aware_path_attains_price", 2e-8)
                    expected = np.linalg.slogdet(N)[1]-3+np.trace(np.linalg.solve(N, prior))+price
                    close(expected, prior_bound, "prior_aware_upper_reconstructed", 2e-8)
                close(upper, min(full, transferred, prior_bound if prior_bound is not None else math.inf),
                      "hull_upper_minimum", 2e-8)
        else:
            check(result["initial_selected"] == shared["selected"], "dense_uses_shared_incumbent")
            check(result["root_status"] == "iteration_limit" and result["root_gap"] > .01,
                  "dense_continuous_root_unresolved")
            close(result["root_upper_bound"]-result["root_feasible_relaxation_value"],
                  result["root_gap"], "dense_root_gap", 1e-12)
        report["methods"].append({key: result[key] for key in (
            "L", "status", "pricing_rounds", "pipeline_seconds", "pipeline_cap_overrun_seconds",
            "combined_true_lower_bound", "combined_true_upper_bound", "combined_true_gap",
            "target_gap_met_numerically", "process_peak_RSS_MiB_so_far") if key in result})
    return report


def tiny_checks():
    rng = np.random.default_rng(415)
    design = core.NoisyDesign(rng.normal(size=(8, 2)), .64, .00125, .00125, .1*np.eye(2), 3)
    case = {"n": 8, "p": 2, "F": design.F.tolist(), "prior": design.prior.tolist(),
            "rho": "16/25", "latent_variance": "1/800", "nugget_variance": "1/800"}
    paths = list(combinations(range(8), 3))
    optimum = max(objective(case, path) for path in paths)
    for L in (0, 2, 7):
        H = np.array([[2., -.3], [-.3, 1.]])
        direct = max(np.trace(H@(local_information(case, path, L)-design.prior)) for path in paths)
        close(independent_price(independent_arc_information(case, L), H, 3), direct,
              "tiny_price_exhaustive", 2e-8)
    hull = core.solve_hull(design, 7, time_limit=1., true_gap=.01, max_rounds=20)
    check(hull.true_lower_bound <= optimum+1e-8 <= hull.true_upper_bound+2e-8,
          "tiny_hull_brackets_enumeration")
    dense = core.solve_dense_oa(design, time_limit=1., absolute_gap=.01, max_rounds=3,
                               root_rounds=10, split_fraction=.99)
    check(dense["lower_bound"] <= optimum+1e-8 <= dense["upper_bound"]+2e-8,
          "tiny_dense_brackets_enumeration")
    with patch.object(core, "CalendarOracle", side_effect=AssertionError("must preflight before construction")):
        refused = core.solve_hull(design, 7, time_limit=1., max_memory_mb=.00001)
    check(refused.status == "memory_limit" and refused.selected is None and refused.true_upper_bound is None,
          "tiny_memory_refusal_preserved")
    return {"n": 8, "k": 3, "enumerated_optimum": optimum,
            "hull_status": hull.status, "dense_status": dense["status"], "refusal_status": refused.status}


def check_refined_transfer(cases):
    path = HERE/"results/fixed-physical-grid-refined-transfer.json"
    artifact = json.loads(path.read_text())
    check(artifact["status"] == "complete", "refined_artifact_complete")
    for key, source in (("source_sha256", INPUT),
                        ("reviewed_bound_sha256", HERE/"noisy_markov_spacing_bound.py"),
                        ("driver_sha256", HERE/"fixed_physical_grid_refined_transfer.py")):
        check(artifact[key] == sha256(source), "refined_source_hash_matches")
    check(len(artifact["results"]) == sum(len(case["hulls"]) for case in cases), "refined_all_rows_retained")
    for row in artifact["results"]:
        case = next(case for case in cases if case["n"] == row["n"])
        hull = case["hulls"][row["hull_index"]]
        check(row["L"] == hull["L"] and row["original_status"] == hull["status"], "refined_field_routing")
        for key, original in (("true_lower_bound", "combined_true_lower_bound"),
                              ("original_true_upper_bound", "combined_true_upper_bound"),
                              ("original_true_gap", "combined_true_gap")):
            close(row[key], hull[original], "refined_original_values_retained", 0)
        close(row["pipeline_plus_reanalysis_seconds"], hull["pipeline_seconds"]+row["reanalysis_seconds"],
              "refined_time_accounting", 1e-12)
        if hull["surrogate_upper_bound"] is None:
            check(row["status"] == "unavailable" and "combined_true_upper_bound" not in row,
                  "refined_no_price_unavailable")
            continue
        delta = refined_delta(case["n"], hull["L"], Q(case["rho"]))
        check(delta == Q(row["refined_delta_exact"]) and delta < 1, "refined_exact_delta")
        close(float(delta), row["refined_delta"], "refined_float_delta", 0)
        close(hull["surrogate_upper_bound"], row["surrogate_upper_bound"], "refined_stored_surrogate_used", 0)
        transferred = hull["surrogate_upper_bound"]-case["p"]*math.log1p(-float(delta))
        upper = min(transferred, hull["combined_true_upper_bound"])
        close(transferred, row["transferred_upper_bound"], "refined_transfer_formula", 0)
        close(upper, row["combined_true_upper_bound"], "refined_upper_minimum", 0)
        close(upper-hull["combined_true_lower_bound"], row["combined_true_gap"], "refined_gap", 0)
        check(row["target_gap_met_numerically"] == (row["combined_true_gap"] <= .01), "refined_target_status")
    return {"artifact_sha256": sha256(path), "driver_sha256": artifact["driver_sha256"],
            "rows": [{key: value for key, value in row.items() if key != "refined_delta_exact"}
                     for row in artifact["results"]]}


@dataclass
class StubHull:
    status: str
    selected: tuple
    true_upper_bound: float
    pricing_rounds: int = 1


def driver_stubs(cases):
    reports = []
    for mode in ("cleanup_overrun", "failure", "shared_exhaustion"):
        clock = [0.]
        calls, cleanups = [], []
        def now():
            return clock[0]
        def construct(n):
            case = deepcopy(next(c for c in cases if c["n"] == n))
            case.update(common_setup_seconds=1., greedy_exchange=None, hulls=[], dense_oa=None)
            clock[0] += 1.
            design = core.NoisyDesign(np.array(case["F"]), float(Q(case["rho"])),
                                     .00125, .00125, np.array(case["prior"]), 16)
            return design, case
        def robust(*args):
            clock[0] += .125
            return args[0][0]
        def greedy(design, **kwargs):
            check(kwargs["time_limit"] == 5., "stub_greedy_cap")
            clock[0] += 35. if mode == "shared_exhaustion" else 2.
            return {"status": "stub_greedy", "selected": tuple(range(16))}
        def operation(kind, design, time_limit):
            calls.append((kind, design.n, time_limit))
            close(time_limit, 26.875, "stub_correct_remaining_budget", 1e-12)
            try:
                clock[0] += time_limit
                if mode == "failure":
                    raise MemoryError("review injected failure")
                upper = design.true_objective(tuple(range(design.n)))
                if kind == "hull":
                    return StubHull("stub_completed", tuple(range(16)), upper)
                return {"status": "stub_completed", "selected": tuple(range(16)), "upper_bound": upper}
            finally:
                clock[0] += .25
                cleanups.append((kind, design.n))
        def hull(design, L, **kwargs):
            return operation("hull", design, kwargs["time_limit"])
        def dense(design, **kwargs):
            return operation("dense", design, kwargs["time_limit"])
        with TemporaryDirectory() as temporary, ExitStack() as stack:
            output = Path(temporary)/"result.json"
            for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
                stack.enter_context(patch.dict(os.environ, {key: "1"}))
            for name, replacement in (("perf_counter", now), ("construct_case", construct),
                                      ("RobustDesign", robust), ("greedy_exchange", greedy),
                                      ("solve_hull", hull), ("solve_dense_oa", dense)):
                stack.enter_context(patch.object(producer, name, replacement))
            stack.enter_context(patch.object(sys, "argv", ["review-driver", "--output", str(output)]))
            stack.enter_context(redirect_stdout(StringIO()))
            producer.main()
            saved = json.loads(output.read_text())
        check(saved["metadata"]["complete"], "stub_checkpoint_complete")
        check([(a, b) for a, b, _ in calls] == cleanups, "stub_cleanup_all_invocations")
        for case in saved["results"]:
            for result in [*case["hulls"], case["dense_oa"]]:
                if mode == "shared_exhaustion":
                    check(result["status"] == "shared_cost_exhausted_pipeline_budget", "stub_exhaustion_status")
                    check(not calls, "stub_no_solver_after_shared_exhaustion")
                else:
                    close(result["pipeline_seconds"], 30.25, "stub_cleanup_charged", 1e-12)
                    close(result["pipeline_cap_overrun_seconds"], .25, "stub_cleanup_overrun_visible", 1e-12)
                if mode == "failure":
                    check(result["status"] == "exception" and result["exception_type"] == "MemoryError",
                          "stub_failure_details_retained")
                    check(result["combined_true_upper_bound"] is None and result["combined_true_gap"] is None
                          and not result["target_gap_met_numerically"], "stub_failure_no_invented_bound")
                check(result["combined_selected"] == list(range(16)), "stub_shared_incumbent_retained")
        reports.append({"mode": mode, "solver_calls": len(calls), "cleanup_calls": len(cleanups)})
    return reports


def main():
    started = perf_counter()
    payload = json.loads(INPUT.read_text())
    metadata = payload["metadata"]
    check(metadata["complete"] and metadata["cores_unchanged_during_run"], "completed_unchanged_record")
    for name, digest in metadata["source_hashes"].items():
        check(sha256(HERE/name) == digest == metadata["final_source_hashes"][name], "source_hash_matches")
    check(all(value == "1" for value in metadata["thread_environment"].values()), "saved_single_thread_settings")
    check("cumulative" in metadata["memory_scope"] and "numerical" in metadata["bound_scope"], "scope_caveats")
    cases = payload["results"]
    model = check_model(cases)
    results = []
    for case in cases:
        results.append(check_results(case))
        print(json.dumps({"reviewed_n": case["n"], "elapsed_seconds": perf_counter()-started}), flush=True)
    tiny = tiny_checks()
    stubs = driver_stubs(cases)
    refined = check_refined_transfer(cases)
    report = {"status": "passed", "reviewer": "/root/physical_grid_review",
              "input_sha256": sha256(INPUT), "review_script_sha256": sha256(Path(__file__)),
              "source_hashes": metadata["source_hashes"], "python": platform.python_version(),
              "numpy": np.__version__, "scipy": scipy.__version__,
              "scope": "Independent rational nesting, mass-balance sensitivities, memory formulas, saved objectives, local support matrices, global linear prices, tiny real solvers and deterministic accounting/failure stubs. No saved 30-second MIP replay or exact certificate.",
              "limitations": ["Saved dense solver upper bounds have no retained cut log or independently replayable dual certificate; only reported arithmetic, assumptions and tiny solver behavior were checked.",
                              "Historical wall time and cumulative RSS cannot be recreated from this result file. Accounting and labels are checked, with controlled timing stubs.",
                              "One recorded run per case, unresolved dense root relaxations and an adaptive separate n96 L12 diagnostic do not establish universal solver superiority.",
                              "The original small stipulated kinetic model remains a scaling probe, without fitted covariance or consequential operational constraints."],
              "counts": dict(COUNTS), "maximum_absolute_errors": dict(ERRORS),
              "model_and_preflight": model, "saved_results": results, "tiny": tiny, "driver_stubs": stubs,
              "refined_transfer": refined,
              "wall_seconds": perf_counter()-started}
    OUTPUT.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"status": "passed", "output": str(OUTPUT), "seconds": report["wall_seconds"]}))


if __name__ == "__main__":
    main()
