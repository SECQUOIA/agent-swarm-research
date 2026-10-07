"""Independent small-instance review checks; requires SymPy for the oracle.

Run from any directory. The oracle enumerates integer slices and all
continuous faces, then solves nonsingular stationarity equations in SymPy.
It does not use the solver's candidate generator or rational LP oracle.
"""

from copy import deepcopy
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import random
import sys

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "solver"))
from certified_grid import BoxQP, Budget, solve
from exact_output import _stationary_candidate, rational_heights, solve_exact
from verify_certificate import CertificateError, verify_certificate


def exhaustive_face_minimum(problem):
    """A minimum-dimensional optimal box face has nonsingular free Hessian."""
    integers = sorted(problem.integers)
    continuous = [i for i in range(len(problem.b)) if i not in problem.integers]
    best, witness = None, None
    for labels in product(*(range(int(problem.bounds[i][0]),
                                  int(problem.bounds[i][1]) + 1)
                            for i in integers)):
        for states in product(range(3), repeat=len(continuous)):
            point = [None] * len(problem.b)
            for i, value in zip(integers, labels):
                point[i] = F(value)
            free = []
            for i, state in zip(continuous, states):
                if state == 2:
                    free.append(i)
                else:
                    point[i] = problem.bounds[i][state]
            if free:
                matrix = sp.Matrix([[problem.A[i][j] for j in free] for i in free])
                if matrix.det() == 0:
                    continue
                rhs = sp.Matrix([
                    -problem.b[i] - sum(problem.A[i][j] * point[j]
                                       for j in range(len(point)) if j not in free)
                    for i in free])
                for i, value in zip(free, matrix.inv() * rhs):
                    point[i] = F(int(value.p), int(value.q))
            if problem.feasible(point):
                value = problem.value(point)
                if best is None or value < best:
                    best, witness = value, tuple(point)
    assert best is not None
    return best, witness


def arbitrary_optimal_set_checks():
    # On the fixed slice t=2/5, this is (x+2y-1/3)^2+z(1-z).
    # Integer z in {0,1} gives two disconnected optimal line segments.
    problem = BoxQP([[2, 4, 0, 1], [4, 8, 0, 0], [0, 0, -2, 0], [1, 0, 0, 0]],
                    [-F(16, 15), -F(4, 3), 1, 0],
                    [(0, F(1, 3)), (0, F(1, 6)), (0, 1), (F(2, 5), F(2, 5))],
                    [2], [(0, 1, 3), (2,)], [(0, 1)], constant=F(1, 9))
    heights = rational_heights(problem)
    tau = F(1, 4 * len(problem.b) * heights["coordinate"])
    count = 0
    for label in (F(0), F(1)):
        for position in ("interior", "lower", "upper"):
            x = {"interior": F(1, 7) + F(1, 10000019),
                 "lower": tau / 4, "upper": F(1, 3) - tau / 4}[position]
            optimum = (x, (F(1, 3) - x) / 2, label, F(2, 5))
            point = (optimum[0] + tau / 8, optimum[1] + tau / 8, label, F(2, 5))
            assert problem.feasible(point) and problem.value(optimum) == 0
            assert sum((a - b) ** 2 for a, b in zip(point, optimum)) <= tau ** 2 / 4
            recovered = _stationary_candidate(problem, point, heights, Budget(2), 100)
            assert recovered is not None and problem.feasible(recovered)
            assert problem.value(recovered) == 0 and recovered[2] == label
            if position == "lower":
                assert recovered[:2] == (F(0), F(1, 6))
            if position == "upper":
                assert recovered[:2] == (F(1, 3), F(0))
            count += 1
    # Disable convex presolve and polishing: certification must use the grid.
    continuous = BoxQP([[2, 2, 0], [2, 2, 0], [0, 0, -2]],
                       [-F(2, 3), -F(2, 3), 1], [(0, 1)] * 3,
                       [], [(0, 1), (2,)], [(0, 1)], constant=F(1, 9))
    approximate = solve(continuous, epsilon=F(1, 100), convex_presolve=False,
                        polish_sweeps=0, max_stages=60, max_table_states=10000, time_limit=5)
    assert approximate["status"] == "certified"
    assert F(approximate["lower"]) <= 0 <= F(approximate["upper"])
    assert verify_certificate(approximate)["valid"]
    return {"near_set_recoveries": count, "nonunique_grid_status": approximate["status"],
            "nonunique_grid_gap": approximate["gap"]}


def main():
    rng = random.Random(830162)
    statuses = {}
    for case in range(36):
        n = 1 + case % 3
        matrix = [[F(0)] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                matrix[i][j] = matrix[j][i] = F(rng.randrange(-4, 5), rng.randrange(1, 4))
        linear = [F(rng.randrange(-4, 5), rng.randrange(1, 5)) for _ in range(n)]
        bounds = [(F(-1, 2), F(4, 3))] * n
        integers = [n - 1] if case % 4 == 0 else []
        if case % 7 == 0:
            bounds[0], integers = (F(1, 3), F(1, 3)), []
        problem = BoxQP(matrix, linear, bounds, integers, [tuple(range(n))], [],
                        constant=F(2, 7))
        optimum, witness = exhaustive_face_minimum(problem)
        heights = rational_heights(problem)
        assert optimum.denominator <= heights["value"], case
        assert all(x.denominator <= heights["coordinate"] for x in witness), case
        result = solve_exact(problem, time_limit=0.3, max_stages=40,
                             max_rounds=6, max_table_states=10000)
        assert verify_certificate(result, max_table_states=10000)["valid"], case
        assert F(result["lower"]) <= optimum <= F(result["upper"]), case
        if result["status"] == "exact":
            assert F(result["upper"]) == optimum, case
        statuses[result["status"]] = statuses.get(result["status"], 0) + 1

    # A singular stationary face of (x+y-1/3)^2 + z(1-z).
    problem = BoxQP([[2, 2, 0], [2, 2, 0], [0, 0, -2]],
                    [-F(2, 3), -F(2, 3), 1], [(0, 1)] * 3,
                    [], [(0, 1), (2,)], [(0, 1)], constant=F(1, 9))
    candidate = _stationary_candidate(
        problem, (F(1, 6), F(1, 6), F(0)), rational_heights(problem), Budget(2), 100)
    assert candidate is not None and problem.feasible(candidate)
    assert problem.value(candidate) == 0
    result = solve_exact(problem, max_rounds=2, max_stages=30, time_limit=2,
                         polish_sweeps=0, warm_start=(F(1, 6), F(1, 6), F(0)))
    assert verify_certificate(result)["valid"]
    mutations = [
        lambda c: c["heights"].__setitem__("value", "1"),
        lambda c: c["rounds"][0]["problem"]["b"].__setitem__(0, "0"),
        lambda c: c["feasible_proposals"].append(
            {"after_round": 0, "point": ["2", "0", "0"]}),
        lambda c: c.__setitem__("upper", "-100"),
    ]
    for mutate in mutations:
        corrupted = deepcopy(result)
        mutate(corrupted)
        try:
            verify_certificate(corrupted)
        except CertificateError:
            pass
        else:
            raise AssertionError("corrupted certificate was accepted")
    for options, expected in [
            ({"time_limit": 0}, "time_limit"),
            ({"max_stages": 0, "convex_presolve": False, "polish_sweeps": 0}, "stage_limit"),
            ({"max_table_states": 1, "convex_presolve": False}, "table_limit")]:
        limited = solve_exact(problem, **options)
        assert limited["status"] == expected, (expected, limited["status"])
        assert verify_certificate(limited)["valid"]
    print(json.dumps({"random_cases": 36, "statuses": statuses,
                      "height_checks": 36, "random_certificate_replays": 36,
                      "singular_candidate": list(map(str, candidate)),
                      "singular_wrapper_status": result["status"],
                      "tamper_rejections": len(mutations),
                      "resource_limit_replays": 3,
                      **arbitrary_optimal_set_checks()}, indent=2))


if __name__ == "__main__":
    main()
