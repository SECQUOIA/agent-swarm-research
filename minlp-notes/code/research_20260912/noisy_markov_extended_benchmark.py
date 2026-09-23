"""Bounded extension: n=48/96, seeds=0/1/2, memory L=6/8, strong dense OA.

Each new invocation receives five seconds. JSON is replaced atomically after
every solve, including exception records. Exactly matched original results may
be reused; their provenance remains explicit.
"""

from dataclasses import asdict
import hashlib
import json
from pathlib import Path
from time import perf_counter

import numpy as np

from noisy_markov_design import generic_design, solve_dense_oa, solve_hull


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "results/noisy-markov-extended-benchmark.json"
ORIGINAL = HERE / "results/noisy-markov-design-benchmark.json"
TIME_LIMIT = 5


def checkpoint(payload: dict) -> None:
    temporary = OUTPUT.with_suffix(".tmp")
    temporary.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n")
    temporary.replace(OUTPUT)


def attempt(label: str, operation) -> dict:
    started = perf_counter()
    try:
        result = operation()
    except Exception as error:
        result = {"status": "exception", "exception_type": type(error).__name__,
                  "exception_message": str(error), "wall_seconds": perf_counter()-started}
    print(json.dumps({"run": label, **{key: result[key] for key in (
        "status", "wall_seconds", "true_lower_bound", "true_upper_bound", "true_gap",
        "lower_bound", "upper_bound", "absolute_gap") if key in result}}), flush=True)
    return result


def main() -> None:
    source_hash = hashlib.sha256((HERE / "noisy_markov_design.py").read_bytes()).hexdigest()
    original = json.loads(ORIGINAL.read_text())
    if original["metadata"]["script_sha256"] != source_hash:
        raise ValueError("original results have a different implementation hash")
    payload = {"metadata": {
        "solver_script_sha256": source_hash,
        "driver_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "numpy_version": np.__version__, "new_invocation_time_limit": TIME_LIMIT,
        "gurobi_threads": 1, "blas_threads_in_recorded_run": 1,
        "grid": {"n": [48, 96], "seed": [0, 1, 2], "L": [6, 8], "p": 3,
                 "k": "n/3", "rho": 0.4, "latent_variance": 1, "nugget_variance": 1},
        "dense_configuration": {"split_fraction": 0.99, "root_rounds": 200},
        "dense_start": "best true-evaluated incumbent from the two same-case hull runs; hull cost excluded from dense cap",
        "original_result_file": str(ORIGINAL.relative_to(HERE)),
        "sweep_complete": False,
    }, "results": []}
    checkpoint(payload)
    for n in (48, 96):
        for seed in (0, 1, 2):
            design = generic_design(n=n, k=n//3, rho=0.4, seed=seed)
            case = {"n": n, "p": 3, "k": n//3, "seed": seed, "rho": 0.4,
                    "latent_variance": 1, "nugget_variance": 1,
                    "F": design.F.tolist(), "prior": design.prior.tolist(),
                    "hulls": [], "provenance": {}}
            payload["results"].append(case)
            matches = [row for row in original["results"] if row["n"] == n
                       and np.array_equal(row["F"], design.F)
                       and np.array_equal(row["prior"], design.prior)
                       and row["k"] == design.k and row["rho"] == design.rho
                       and row["latent_variance"] == design.latent_variance
                       and row["nugget_variance"] == design.nugget_variance]
            matched = matches[0] if matches else None
            for L in (6, 8):
                saved = next((h for h in matched["hulls"] if h["L"] == L), None) if matched else None
                if saved is not None and original["metadata"]["per_solver_time_limit"] == TIME_LIMIT:
                    result = saved
                    case["provenance"]["hull_L" + str(L)] = "reused exact input/source/cap match from " + ORIGINAL.name
                else:
                    result = attempt(f"n={n},seed={seed},L={L}",
                                     lambda: asdict(solve_hull(design, L, time_limit=TIME_LIMIT)))
                    result.setdefault("L", L)
                    case["provenance"]["hull_L" + str(L)] = "new five-second-cap invocation"
                case["hulls"].append(result)
                checkpoint(payload)
            available = [h for h in case["hulls"] if h.get("true_lower_bound") is not None]
            initial = tuple(max(available, key=lambda h: h["true_lower_bound"])["selected"]) if available else None
            saved = matched["dense_oa_strengthened"] if matched else None
            if (saved is not None and initial is not None
                    and tuple(saved["initial_selected"]) == initial
                    and saved["split_fraction"] == 0.99
                    and original["metadata"]["per_solver_time_limit"] == TIME_LIMIT):
                dense = saved
                case["provenance"]["dense_oa_strengthened"] = "reused exact input/source/cap/start match from " + ORIGINAL.name
            else:
                dense = attempt(f"n={n},seed={seed},dense_strengthened", lambda: solve_dense_oa(
                    design, time_limit=TIME_LIMIT, split_fraction=0.99,
                    root_rounds=200, initial_selected=initial))
                case["provenance"]["dense_oa_strengthened"] = "new five-second-cap invocation"
            dense = dict(dense)
            dense["initial_incumbent_source"] = "best available true-evaluated incumbent from same-case L6/L8 hulls; their times reported separately"
            case["dense_oa_strengthened"] = dense
            checkpoint(payload)
    payload["metadata"]["sweep_complete"] = True
    checkpoint(payload)


if __name__ == "__main__":
    main()
