"""Reproducible exact path experiments, with an independent numerical KKT MILP.

Run: python code/bilevel_reopened/quadratic_benchmarks.py
Results are synthetic prototype evidence, not a solver superiority claim.
"""
import json
import platform
import random
import time
from fractions import Fraction as F
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import Bounds, LinearConstraint, milp

from quadratic_solver import Problem, exhaustive_path, optimize_path, solve_response_path, verify_path


def instance(n, k, seed):
    rng = random.Random(seed)
    return Problem(
        tuple(F(rng.randint(6, 12), 8) for _ in range(n)),
        tuple(tuple(rng.randint(-2, 2) for _ in range(k)) for _ in range(n)),
        tuple(tuple(F(int(i == j), max(1, 4 * n)) for j in range(k)) for i in range(k)),
        tuple(F(rng.randint(-14, 2), 8) for _ in range(n)),
        tuple(F(rng.randint(1, 16), 8) for _ in range(n)),
    )


def kkt_milp(p, objective_x, objective_z, constraints=()):
    """Independent big-M KKT formulation; floating point comparison only."""
    n, size = len(p.d), 1 + 3 * len(p.d)
    q = np.diag(np.array(p.d, float))
    if p.H:
        u = np.array(p.U, float)
        q += u @ np.array(p.H, float) @ u.T
    c, C = np.array(p.c, float), np.array(p.C, float)
    max_x = max(abs(float(p.lo)), abs(float(p.hi)))
    M = np.abs(c) + np.abs(C) * max_x + np.abs(q).sum(axis=1) + 1
    rows, lower, upper = [], [], []

    def add(row, lo=-np.inf, hi=np.inf):
        rows.append(row)
        lower.append(lo)
        upper.append(hi)

    for i in range(n):
        # z_i <= 1-y_lower_i; z_i >= y_upper_i.
        row = np.zeros(size)
        row[1 + i], row[1 + n + i] = 1, 1
        add(row, hi=1)
        row = np.zeros(size)
        row[1 + i], row[1 + 2 * n + i] = 1, -1
        add(row, lo=0)
        row = np.zeros(size)
        row[1 + n + i], row[1 + 2 * n + i] = 1, 1
        add(row, hi=1)
        # -M*y_upper <= Q_i*z+c_i+C_i*x <= M*y_lower.
        row = np.zeros(size)
        row[0], row[1:1 + n], row[1 + n + i] = C[i], q[i], -M[i]
        add(row, hi=-c[i])
        row = np.zeros(size)
        row[0], row[1:1 + n], row[1 + 2 * n + i] = C[i], q[i], M[i]
        add(row, lo=-c[i])
    for cx, cz, rhs in constraints:
        row = np.zeros(size)
        row[0], row[1:1 + n] = float(cx), np.array(cz, float)
        add(row, hi=float(rhs))
    objective = np.zeros(size)
    objective[0], objective[1:1 + n] = float(objective_x), np.array(objective_z, float)
    lb, ub = np.zeros(size), np.ones(size)
    lb[0], ub[0] = float(p.lo), float(p.hi)
    integrality = np.zeros(size)
    integrality[1 + n:] = 1
    return milp(objective, integrality=integrality, bounds=Bounds(lb, ub),
                constraints=LinearConstraint(np.array(rows), lower, upper),
                options={"time_limit": 30, "mip_rel_gap": 0})


def run_case(p, seed, compare_exhaustive=False, compare_milp=True):
    n, stats = len(p.d), {}
    start = time.perf_counter()
    segments = solve_response_path(p, stats=stats)
    path_time = time.perf_counter() - start
    assert verify_path(p, segments)
    rng = random.Random(seed + 30000)
    oz = tuple(F(rng.randint(-8, 8), 8) for _ in range(n))
    ox = F(rng.randint(-4, 4), 8)
    # Response-dependent service floor, chosen feasible at x=0.
    z0 = next(s.response(p.lo) for s in segments if s.lo <= p.lo <= s.hi)
    floor = sum(z0, F(0)) * F(1, 2)
    constraints = [(0, (-1,) * n, -floor)]
    start = time.perf_counter()
    solution = optimize_path(p, segments, ox, oz, constraints)
    upper_time = time.perf_counter() - start
    row = {"n": n, "k": len(p.H), "seed": seed, "segments": len(segments),
           "path_seconds": path_time, "upper_seconds": upper_time, "stats": stats,
           "x": str(solution["x"]), "objective": str(solution["objective"]),
           "exact_certificate_passed": True}
    if compare_exhaustive:
        reference = optimize_path(p, exhaustive_path(p), ox, oz, constraints)
        assert reference["objective"] == solution["objective"]
        row["exhaustive_objective_equal"] = True
    if compare_milp:
        start = time.perf_counter()
        reference = kkt_milp(p, ox, oz, constraints)
        row["milp_seconds"] = time.perf_counter() - start
        row["milp_status"] = int(reference.status)
        if reference.status == 0:
            error = abs(reference.fun - float(solution["objective"]))
            assert error <= 1e-6 * (1 + abs(reference.fun)), (error, row)
            row["milp_objective_abs_difference"] = error
    return row


def boundary_checks():
    # Every coordinate switches at the same point; exact feasible singleton.
    p = Problem((1, 1, 1), ((), (), ()), (), (0, 0, 0), (-2, -2, -2))
    path = solve_response_path(p)
    constraints = [(1, (0, 0, 0), F(1, 2)), (-1, (0, 0, 0), F(-1, 2))]
    answer = optimize_path(p, path, 0, (1, 1, 1), constraints)
    assert answer["x"] == F(1, 2) and answer["z"] == (1, 1, 1)
    assert optimize_path(p, path, 0, (1, 1, 1), [(0, (1, 0, 0), -1)]) is None
    # Response equality defines an isolated feasible point inside a response cell.
    answer = optimize_path(p, path, 0, (1, 1, 1),
                           [(0, (1, 0, 0), F(1, 3)), (0, (-1, 0, 0), F(-1, 3))])
    assert answer["x"] == F(1, 6)
    # Indefinite aggregate H is allowed if the full Q is positive definite.
    negative = Problem((2, 2), ((1,), (1,)), ((F(-1, 2),),), (-1, -1), (1, 1))
    assert verify_path(negative, solve_response_path(negative))
    singleton = Problem((1,), ((),), (), (-1,), (1,), F(1, 3), F(1, 3))
    assert verify_path(singleton, solve_response_path(singleton))
    # A coordinate persistently at a bound with zero multiplier.
    degenerate = Problem((1, 1), ((), ()), (), (0, -1), (0, 2))
    assert verify_path(degenerate, solve_response_path(degenerate))
    try:
        Problem((1,), ((1,),), ((-2,),), (0,), (1,))
    except ValueError:
        pass
    else:
        raise AssertionError("Non-SPD input was accepted")
    return {"simultaneous_switches": True, "isolated_leader_feasibility": True,
            "isolated_response_feasibility": True, "infeasibility": True,
            "indefinite_H_with_SPD_Q": True, "singleton_domain": True,
            "persistent_zero_multiplier": True, "reject_non_SPD": True}


def main():
    output = {"description": "Synthetic exact scalar-leader box-QP prototype; timings are environment-specific",
              "python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
              "boundary_checks": boundary_checks(), "cases": []}
    for seed in range(12):
        row = run_case(instance(4, 1 + seed % 2, seed), seed, compare_exhaustive=True)
        output["cases"].append(row)
        print(json.dumps(row), flush=True)
    for n in (10, 30, 60, 120):
        for k in (1, 2):
            seed = 1000 + n + k
            row = run_case(instance(n, k, seed), seed, compare_milp=n <= 60)
            output["cases"].append(row)
            print(json.dumps(row), flush=True)
    target = Path(__file__).with_name("quadratic_benchmark_results.json")
    target.write_text(json.dumps(output, indent=2) + "\n")


if __name__ == "__main__":
    main()
