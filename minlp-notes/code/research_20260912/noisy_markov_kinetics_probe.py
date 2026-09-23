"""Small smooth-sensitivity probe with an explicitly stylized noisy covariance.

The mean is consecutive first-order A -> B -> C kinetics. The covariance is a
specified stationary AR(1) latent process plus independent observation noise;
it is not estimated from, or attributed to, published experimental data.
"""

import argparse
from dataclasses import asdict
import hashlib
import json
import math
import os
from pathlib import Path
from time import perf_counter

import numpy as np

from noisy_markov_design import NoisyDesign, solve_dense_oa, solve_hull


HERE = Path(__file__).resolve().parent
REGIMES = {"fast": (0.7, 0.2), "slow": (0.18, 0.045)}
HORIZON = 12.0


def reaction_mean(times: np.ndarray, log_parameters: np.ndarray) -> np.ndarray:
    A0, k1, k2 = np.exp(log_parameters)
    return A0*k1/(k2-k1) * (np.exp(-k1*times)-np.exp(-k2*times))


def reaction_data(n: int, regime: str) -> tuple[np.ndarray, np.ndarray, dict]:
    """Parameters are log(A0), log(k1), log(k2), in that order."""
    A0 = 1.0
    k1, k2 = REGIMES[regime]
    times = HORIZON * np.arange(1, n+1) / n
    d = k2-k1
    e1, e2 = np.exp(-k1*times), np.exp(-k2*times)
    B = A0*k1/d*(e1-e2)
    derivative_k1 = A0*(k2/d**2*(e1-e2)-k1/d*times*e1)
    derivative_k2 = A0*(-k1/d**2*(e1-e2)+k1/d*times*e2)
    F = np.column_stack((B, k1*derivative_k1, k2*derivative_k2))
    theta = np.log([A0, k1, k2])
    complex_step = np.empty_like(F)
    for j in range(3):
        perturbed = theta.astype(complex)
        perturbed[j] += 1e-25j
        complex_step[:, j] = reaction_mean(times, perturbed).imag / 1e-25
    absolute_error = float(np.max(abs(F-complex_step)))
    normalized_error = float(np.linalg.norm(F-complex_step)/max(1, np.linalg.norm(F)))
    if absolute_error > 1e-10:
        raise ArithmeticError("analytic sensitivities disagree with independent complex-step differentiation")
    return times, F, {
        "regime": regime, "A0": A0, "k1": k1, "k2": k2,
        "parameter_names": ["log(A0)", "log(k1)", "log(k2)"],
        "nominal_peak_time": math.log(k1/k2)/(k1-k2),
        "horizon": HORIZON, "candidate_times": times.tolist(), "mean_B": B.tolist(),
        "analytic_sensitivity_check": {"method": "independent complex step on mean formula",
                                        "step": 1e-25, "max_absolute_error": absolute_error,
                                        "normalized_frobenius_error": normalized_error},
    }


def checkpoint(output: Path, payload: dict) -> None:
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n")
    temporary.replace(output)


def attempt(label: str, operation) -> dict:
    started = perf_counter()
    try:
        result = operation()
    except Exception as error:
        result = {"status": "exception", "exception_type": type(error).__name__,
                  "exception_message": str(error), "wall_seconds": perf_counter()-started}
    print(json.dumps({"run": label, **{key: result[key] for key in (
        "status", "wall_seconds", "true_lower_bound", "true_upper_bound", "true_gap",
        "surrogate_hull_gap", "lower_bound", "upper_bound", "absolute_gap") if key in result}}), flush=True)
    return result


def run_probe(n: int, rho: float, L: int, regimes: tuple[str, ...], time_limit: float,
              output: Path) -> dict:
    if n < 3 or n % 3:
        raise ValueError("n must be a positive multiple of three")
    if not 0 < time_limit <= 30:
        raise ValueError("time_limit must lie in (0,30]")
    payload = {"metadata": {
        "solver_script_sha256": hashlib.sha256((HERE / "noisy_markov_design.py").read_bytes()).hexdigest(),
        "driver_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "numpy_version": np.__version__, "per_invocation_time_limit": time_limit,
        "max_memory_mb": 256, "gurobi_threads": 1,
        "blas_environment": {key: os.environ.get(key) for key in (
            "OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")},
        "mean_model": "B(t)=A0*k1/(k2-k1)*(exp(-k1*t)-exp(-k2*t)), from consecutive first-order A->B->C",
        "time_grid": "t_j=12*(j+1)/n; time zero excluded; fixed horizon 12",
        "covariance_model": "STYLIZED known stationary latent AR(1) covariance plus independent nugget; no claim of measured error covariance",
        "covariance_units": "latent and nugget variances each 0.00125 concentration-units squared; total pointwise noise SD 0.05",
        "rho_interpretation": "correlation of latent errors per candidate-grid interval; holding rho fixed while changing n changes physical correlation scale",
        "prior_interpretation": "fixed 0.01 I in the stated log-parameter coordinates; regularizes the design criterion",
        "statistical_scope": "local mean Fisher information at nominal parameters with fixed known covariance; no parameter-dependent covariance derivatives",
        "exact_certificate_scope": "compatible with certification of the saved decimal sensitivity and covariance data; no claim that floating analytic sensitivities are exact real values",
        "dense_baseline": "ordinary dense Liu evaluator, split .99 and at most 200 root cuts; same cap and disclosed best-hull incumbent start",
        "sweep_complete": False,
    }, "results": []}
    checkpoint(output, payload)
    for regime in regimes:
        times, F, kinetics = reaction_data(n, regime)
        design = NoisyDesign(F, rho, 0.00125, 0.00125, 0.01*np.eye(3), n//3)
        case = {"n": n, "p": 3, "k": n//3, "rho": rho,
                "latent_variance": design.latent_variance,
                "nugget_variance": design.nugget_variance,
                "F": F.tolist(), "prior": design.prior.tolist(),
                "kinetics": kinetics, "hulls": []}
        payload["results"].append(case)
        hull = attempt(f"{regime},n={n},rho={rho},L={L}", lambda: asdict(
            solve_hull(design, L, time_limit=time_limit, max_memory_mb=256)))
        hull.setdefault("L", L)
        if hull.get("selected") is not None:
            hull["selected_times"] = times[list(hull["selected"])].tolist()
        case["hulls"].append(hull)
        checkpoint(output, payload)
        initial = tuple(hull["selected"]) if hull.get("true_lower_bound") is not None else None
        dense = attempt(f"{regime},n={n},rho={rho},dense_strengthened", lambda: solve_dense_oa(
            design, time_limit=time_limit, split_fraction=0.99, root_rounds=200,
            initial_selected=initial))
        dense["initial_incumbent_source"] = "true-evaluated incumbent from same-case calendar hull; its generation time excluded from dense cap"
        if dense.get("selected") is not None:
            dense["selected_times"] = times[list(dense["selected"])].tolist()
        case["dense_oa_strengthened"] = dense
        checkpoint(output, payload)
    payload["metadata"]["sweep_complete"] = True
    checkpoint(output, payload)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=48)
    parser.add_argument("--rho", type=float, default=0.4)
    parser.add_argument("--L", type=int, default=8)
    parser.add_argument("--regime", choices=("fast", "slow", "both"), default="both")
    parser.add_argument("--time-limit", type=float, default=10)
    parser.add_argument("--output", type=Path, default=HERE / "results/noisy-markov-kinetics-probe.json")
    args = parser.parse_args()
    regimes = tuple(REGIMES) if args.regime == "both" else (args.regime,)
    run_probe(args.n, args.rho, args.L, regimes, args.time_limit, args.output)


if __name__ == "__main__":
    main()
