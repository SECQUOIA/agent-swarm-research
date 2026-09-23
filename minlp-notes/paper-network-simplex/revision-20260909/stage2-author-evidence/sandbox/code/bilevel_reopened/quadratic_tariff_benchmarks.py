"""Exact common-tariff experiments on synthetic quadratic consumption models."""
import json
import random
import time
from fractions import Fraction as F
from pathlib import Path

from quadratic_solver import Problem, optimize_aligned_rank_one, optimize_path, solve_response_path


def tariff_instance(n, seed, coupling_sign=1):
    rng = random.Random(seed)
    return Problem(tuple(F(rng.randint(5, 20), 10) for _ in range(n)), ((1,),) * n,
                   ((F(coupling_sign, 10 * n),),),
                   tuple(-F(rng.randint(1000, 25000), 10000) for _ in range(n)),
                   (1,) * n, 0, 3)


def main():
    result = {"description": "Uncalibrated synthetic common-tariff revenue maximization with a service floor",
              "objective": "maximize x*sum(z); require sum(z)>=N/5; 0<=x<=3", "cases": []}
    for n, sign in [(100, 1), (1000, 1), (10000, 1), (1000, -1)]:
        seed = 50000 + n + sign
        start = time.perf_counter()
        p = tariff_instance(n, seed, sign)
        input_seconds = time.perf_counter() - start
        constraints = [(0, (-1,) * n, -F(n, 5))]
        start = time.perf_counter()
        answer = optimize_aligned_rank_one(p, 0, (0,) * n, constraints, objective_xz=(-1,) * n)
        elapsed = time.perf_counter() - start
        assert answer is not None
        x, z = answer["x"], answer["z"]
        gradient = tuple(qz + ci + Ci * x for qz, ci, Ci in zip(p.qmul(z), p.c, p.C))
        assert all(0 <= zi <= 1 and (gi >= 0 if zi == 0 else gi <= 0 if zi == 1 else gi == 0)
                   for zi, gi in zip(z, gradient))
        assert sum(z, F(0)) >= F(n, 5)
        assert answer["objective"] == -x * sum(z, F(0))
        row = {"n": n, "coupling_sign": sign, "seed": seed,
               "input_validation_seconds": input_seconds, "sweep_seconds": elapsed,
               "distinct_thresholds": answer["thresholds"],
               "response_intervals_visited": answer["response_intervals_visited"],
               "price": str(x), "price_float": float(x),
               "revenue": str(-answer["objective"]), "revenue_float": float(-answer["objective"]),
               "total_consumption": str(sum(z, F(0))), "exact_returned_KKT_passed": True}
        if n == 100:
            start = time.perf_counter()
            path = solve_response_path(p)
            general = optimize_path(p, path, 0, (0,) * n, constraints, objective_xz=(-1,) * n)
            row["general_certified_path_seconds"] = time.perf_counter() - start
            assert general["objective"] == answer["objective"]
            row["general_path_exact_objective_equal"] = True
        result["cases"].append(row)
        print(json.dumps(row), flush=True)
    Path(__file__).with_name("quadratic_tariff_benchmark_results.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
