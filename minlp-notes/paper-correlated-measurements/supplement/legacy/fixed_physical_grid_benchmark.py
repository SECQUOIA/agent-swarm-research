"""Matched fixed-physical-covariance, fixed-budget kinetic design benchmark.

Reuses reviewed solvers without altering their implementations. All three
grids sample one exponential latent covariance, and each design selects 16
observations. Memory refusal and construction timeout are retained results.
"""

import argparse
from dataclasses import asdict
from fractions import Fraction
import hashlib
from importlib.metadata import version
import json
import math
import os
from pathlib import Path
import platform
import resource
from time import perf_counter

import numpy as np
import scipy

from noisy_markov_design import NoisyDesign, memory_estimate, solve_dense_oa, solve_hull, spectral_delta
from noisy_markov_kinetics_probe import reaction_data
from noisy_markov_spacing_bound import spacing_bound
from robust_kinetic_design import RobustDesign, greedy_exchange


HERE = Path(__file__).resolve().parent
RHO = {48: Fraction(256, 625), 96: Fraction(16, 25), 192: Fraction(4, 5)}
WINDOWS = {48: 8, 96: 14, 192: 13}
PIPELINE_CAP = 30.
GREEDY_CAP = 5.
TARGET_GAP = .01
MEMORY_MB = 256
CORE_FILES = ("noisy_markov_design.py", "noisy_markov_kinetics_probe.py",
              "noisy_markov_spacing_bound.py", "robust_kinetic_design.py")


def hashes():
    return {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
            for name in (*CORE_FILES, Path(__file__).name)}


def checkpoint(path, payload):
    temporary = path.with_suffix(path.suffix+".tmp")
    temporary.write_text(json.dumps(payload, indent=2, allow_nan=False)+"\n")
    temporary.replace(path)


def attempt(label, operation):
    started = perf_counter()
    try:
        result = operation()
    except Exception as error:
        result = {"status": "exception", "exception_type": type(error).__name__,
                  "exception_message": str(error)}
    result["measured_invocation_seconds"] = perf_counter()-started
    result["process_peak_RSS_MiB_so_far"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
    print(json.dumps({"run": label, **{key: result[key] for key in
            ("status", "measured_invocation_seconds", "true_lower_bound", "true_upper_bound",
             "true_gap", "lower_bound", "upper_bound", "absolute_gap", "pricing_rounds")
            if key in result}}), flush=True)
    return result


def preflight(design, rho):
    started = perf_counter()
    largest = max(L for L in range(design.n)
                  if memory_estimate(design, L)["array_and_path_estimate_bytes"] <= MEMORY_MB*2**20)
    first = {}
    rows = []
    for L in range(design.n):
        core = spectral_delta(design, L)
        refined = float(spacing_bound(design.n, L, 1, rho, Fraction(1, 800), Fraction(1, 800),
                                      refined_pairs=True)["delta"])
        estimate = memory_estimate(design, L)
        row = {"L": L, "core_delta": core, "reviewed_refined_delta": refined,
               "estimated_workspace_bytes": estimate["array_and_path_estimate_bytes"]}
        rows.append(row)
        for name, delta in (("core", core), ("reviewed_refined", refined)):
            if delta >= 1:
                continue
            measures = {"one_sided_log_correction": -design.p*math.log1p(-delta),
                        "two_sided_surrogate_optimizer_loss": design.p*(math.log1p(delta)-math.log1p(-delta))}
            for criterion, value in measures.items():
                key = name+"_"+criterion
                if key not in first and value <= TARGET_GAP:
                    first[key] = {**row, "bound_component": value}
        if len(first) == 4 and L >= max(largest+1, WINDOWS[design.n]):
            break
    return {"largest_window_under_workspace_estimate": largest,
            "scheduled_primary_window": WINDOWS[design.n], "target_loggap": TARGET_GAP,
            "first_windows": first, "evaluated_windows": rows,
            "preflight_seconds": perf_counter()-started,
            "interpretation": "Sufficient bounds for stated approximation components, not necessary memory requirements or a guarantee that the discrete optimization gap reaches the target.",
            "resource_scope": "Core estimate is a preflight estimate of workspace, not a hard bound on process RSS or elapsed construction time."}


def construct_case(n):
    started = perf_counter()
    times, F, kinetics = reaction_data(n, "fast")
    design = NoisyDesign(F, float(RHO[n]), .00125, .00125, .01*np.eye(3), 16)
    data_seconds = perf_counter()-started
    pre = preflight(design, RHO[n])
    return design, {"n": n, "p": 3, "k": 16, "rho": str(RHO[n]),
                    "latent_variance": "1/800", "nugget_variance": "1/800",
                    "F": F.tolist(), "prior": design.prior.tolist(), "kinetics": kinetics,
                    "data_construction_seconds": data_seconds, "preflight": pre,
                    "common_setup_seconds": data_seconds+pre["preflight_seconds"],
                    "greedy_exchange": None, "hulls": [], "dense_oa": None}


def nested_grid_check(cases):
    by_n = {case["n"]: case for case in cases}
    results = []
    for coarse, fine in ((48, 96), (96, 192), (48, 192)):
        multiplier = fine//coarse
        indices = [multiplier*(i+1)-1 for i in range(coarse)]
        assert RHO[fine]**multiplier == RHO[coarse]
        coarse_F, fine_F = np.array(by_n[coarse]["F"]), np.array(by_n[fine]["F"])[indices]
        assert np.array_equal(coarse_F, fine_F)
        coarse_t = np.array(by_n[coarse]["kinetics"]["candidate_times"])
        fine_t = np.array(by_n[fine]["kinetics"]["candidate_times"])[indices]
        assert np.array_equal(coarse_t, fine_t)
        results.append({"coarse_n": coarse, "fine_n": fine,
                        "index_map": "fine_index=(fine_n/coarse_n)*(coarse_index+1)-1",
                        "exact_covariance_consistency": True,
                        "identical_saved_mean_sensitivities_at_shared_times": True})
    return results


def remaining_budget(case):
    return PIPELINE_CAP-case["common_setup_seconds"]-case["greedy_exchange"]["shared_total_seconds"]


def add_shared_incumbent(result, design, case, method):
    started = perf_counter()
    shared = case["greedy_exchange"]
    candidates = []
    if shared.get("selected") is not None:
        path = tuple(shared["selected"])
        candidates.append((design.true_objective(path), path, "shared greedy/exchange"))
    if result.get("selected") is not None:
        path = tuple(result["selected"])
        candidates.append((design.true_objective(path), path, method))
    lower, selected, source = max(candidates)
    upper = result.get("true_upper_bound" if method == "calendar hull" else "upper_bound")
    result["combined_true_lower_bound"] = lower
    result["combined_selected"] = selected
    result["combined_incumbent_source"] = source
    result["combined_true_upper_bound"] = upper
    result["combined_true_gap"] = None if upper is None else upper-lower
    result["target_gap_met_numerically"] = upper is not None and -1e-7 <= upper-lower <= TARGET_GAP
    result["solver_time_limit_seconds"] = remaining_budget(case)
    result["selected_times"] = np.array(case["kinetics"]["candidate_times"])[list(selected)].tolist()
    result["postprocessing_seconds"] = perf_counter()-started
    result["pipeline_seconds"] = (case["common_setup_seconds"]+shared["shared_total_seconds"]
                                   +result["measured_invocation_seconds"]+result["postprocessing_seconds"])
    result["pipeline_cap_overrun_seconds"] = max(0., result["pipeline_seconds"]-PIPELINE_CAP)


def run_hull(design, case, L, label):
    budget = remaining_budget(case)
    if budget <= 0:
        result = {"status": "shared_cost_exhausted_pipeline_budget", "measured_invocation_seconds": 0.}
    else:
        result = attempt(label, lambda: asdict(solve_hull(design, L, time_limit=budget,
                          true_gap=TARGET_GAP, hull_gap=1e-6, max_memory_mb=MEMORY_MB)))
    result["requested_L"] = L
    result.setdefault("L", L)
    add_shared_incumbent(result, design, case, "calendar hull")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--output", type=Path, default=HERE/"results/fixed-physical-grid-benchmark.json")
    args = parser.parse_args()
    threads = {key: os.environ.get(key) for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")}
    if any(value != "1" for value in threads.values()):
        raise RuntimeError("Set BLAS/OpenMP thread variables to one")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    started = perf_counter()
    payload = {"metadata": {"source_hashes": hashes(), "python": platform.python_version(),
               "numpy": np.__version__, "scipy": scipy.__version__, "gurobipy": version("gurobipy"),
               "thread_environment": threads, "logical_cpu_count": os.cpu_count(),
               "gurobi_threads": 1, "pipeline_cap_seconds": PIPELINE_CAP, "shared_greedy_cap_seconds": GREEDY_CAP,
               "target_loggap": TARGET_GAP, "workspace_estimate_limit_MiB": MEMORY_MB,
               "budget_accounting": "Each hull or dense pipeline is charged its data/preflight setup and the same measured shared greedy/exchange generation, then receives the remaining part of 30 seconds. Solver construction and internal seed evaluation are inside its own timer.",
               "mean_model": "Same stipulated fast consecutive A->B->C model: A0=1,k1=.7,k2=.2; log-parameter sensitivities; B observed.",
               "physical_covariance": "R(t,u)=.00125*exp(-lambda*abs(t-u))+.00125*1(t=u), lambda=-16*log(4/5); all grids share this fixed kernel.",
               "rational_covariance_rule": "rho192=4/5,rho96=(4/5)^2,rho48=(4/5)^4; exact rational rho strings retained.",
               "design_family": "Exactly 16 distinct selected times, t_j=12*(j+1)/n; no additional spacing or installation constraint.",
               "scope": "Local nominal mean-information design with stipulated covariance. No experimental covariance fit or global parameter-identifiability claim.",
               "bound_scope": "Solver upper bounds are numerical, subject to the reviewed floating-point implementation limits. This benchmark does not itself produce exact certificates.",
               "memory_scope": "RSS is the cumulative process high-water mark, not an isolated per-method peak.",
               "complete": False}, "results": []}
    designs = {}
    for n in RHO:
        design, case = construct_case(n)
        designs[n] = design
        payload["results"].append(case)
        checkpoint(args.output, payload)
    payload["nested_grid_checks"] = nested_grid_check(payload["results"])
    checkpoint(args.output, payload)
    if args.preflight_only:
        print(json.dumps({"preflight_saved": str(args.output)}), flush=True)
        return
    for case in payload["results"]:
        n, design = case["n"], designs[case["n"]]
        shared_started = perf_counter()
        shared = RobustDesign((design,), np.zeros(1))
        case["greedy_exchange"] = attempt(f"n{n}-shared-greedy", lambda: greedy_exchange(shared, time_limit=GREEDY_CAP))
        greedy = case["greedy_exchange"]
        if greedy.get("selected") is None:
            seed = tuple(np.linspace(0, n-1, 16, dtype=int).tolist())
            greedy.update(selected=seed, true_lower_bound=design.true_objective(seed), fallback_seed=True)
        greedy["true_objective_recheck"] = design.true_objective(tuple(greedy["selected"]))
        greedy["shared_total_seconds"] = perf_counter()-shared_started
        greedy["pipeline_seconds"] = case["common_setup_seconds"]+greedy["shared_total_seconds"]
        checkpoint(args.output, payload)
        case["hulls"].append(run_hull(design, case, WINDOWS[n], f"n{n}-primary-hull-L{WINDOWS[n]}"))
        checkpoint(args.output, payload)
        budget = remaining_budget(case)
        if budget <= 0:
            dense = {"status": "shared_cost_exhausted_pipeline_budget", "measured_invocation_seconds": 0.}
        else:
            dense = attempt(f"n{n}-dense-OA", lambda: solve_dense_oa(design, time_limit=budget,
                        absolute_gap=TARGET_GAP, split_fraction=.99, root_rounds=200,
                        initial_selected=tuple(greedy["selected"])))
        dense["initial_incumbent_source"] = "Shared greedy/exchange, fully charged to this pipeline"
        add_shared_incumbent(dense, design, case, "dense OA")
        case["dense_oa"] = dense
        checkpoint(args.output, payload)
        if n == 96 and case["hulls"][0].get("pricing_rounds", 0) == 0:
            diagnostic = run_hull(design, case, 12, "n96-diagnostic-hull-L12")
            diagnostic["role"] = "Separate construction-versus-bound diagnostic after primary L14 produced no completed price; not a replacement for the primary run. It has its own 30-second pipeline cap."
            case["hulls"].append(diagnostic)
            checkpoint(args.output, payload)
    payload["metadata"]["complete"] = True
    payload["metadata"]["final_source_hashes"] = hashes()
    payload["metadata"]["cores_unchanged_during_run"] = all(
        payload["metadata"]["source_hashes"][name] == payload["metadata"]["final_source_hashes"][name]
        for name in CORE_FILES)
    payload["metadata"]["total_experiment_seconds"] = perf_counter()-started
    checkpoint(args.output, payload)
    print(json.dumps({"complete": True, "output": str(args.output),
                      "total_experiment_seconds": payload["metadata"]["total_experiment_seconds"]}), flush=True)


if __name__ == "__main__":
    main()
