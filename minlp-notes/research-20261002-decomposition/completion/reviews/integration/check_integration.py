"""Small independent cross-caller checks; not a project-wide test runner."""
from copy import deepcopy
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "solver"))

from certified_grid import BoxQP
from exact_output import solve_exact
from recourse import solve_with_recourse
from verify_certificate import verify_certificate
from verify_recourse import RecourseCertificateError, verify_pipeline
from constrained_grid import ConstrainedQP, solve as solve_constrained
from verify_constrained import verify as verify_constrained
from optimal_sets import solve_endpoint_set
from verify_optimal_sets import verify_certificate as verify_set, contains


def gaussian(matrix, rhs):
    n = len(rhs)
    rows = [list(row) + [b] for row, b in zip(matrix, rhs)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if rows[i][j]), None)
        if pivot is None:
            return None
        rows[j], rows[pivot] = rows[pivot], rows[j]
        a = rows[j][j]
        rows[j] = [v / a for v in rows[j]]
        for i in range(n):
            if i != j:
                a = rows[i][j]
                rows[i] = [v - a * w for v, w in zip(rows[i], rows[j])]
    return [row[-1] for row in rows]


def reference(problem):
    """Enumerate original faces; a minimum-dimensional optimum face is nonsingular."""
    labels = [tuple(range(int(lo), int(hi) + 1)) if i in problem.integers
              else ((lo,) if lo == hi else (lo, None, hi))
              for i, (lo, hi) in enumerate(problem.bounds)]
    best = None
    for state in product(*labels):
        free = [i for i, v in enumerate(state) if v is None]
        fixed = [i for i, v in enumerate(state) if v is not None]
        candidate = list(map(lambda x: F(x) if x is not None else None, state))
        values = gaussian([[problem.A[i][j] for j in free] for i in free],
                          [-problem.b[i] - sum(problem.A[i][j] * candidate[j] for j in fixed)
                           for i in free])
        if values is None:
            continue
        for i, v in zip(free, values):
            candidate[i] = v
        if problem.feasible(candidate):
            value = problem.value(candidate)
            best = value if best is None else min(best, value)
    assert best is not None
    return best


def restored(value):
    return json.loads(json.dumps(value))


def bounded(cert, optimum):
    assert F(cert["lower"]) <= optimum <= F(cert["upper"]), (cert, optimum)
    if cert["status"] == "exact":
        assert F(cert["lower"]) == optimum == F(cert["upper"])


def expect_reject(call):
    try:
        call()
    except (ValueError, AssertionError):
        return
    raise AssertionError("invalid certificate was accepted")


def run():
    summary = {"exact_runs": 0, "pipeline_runs": 0, "mutations_rejected": 0,
               "constrained_runs": 0, "set_memberships": 0}
    cases = [
        BoxQP([[2, -2], [-2, 2]], [F(-2, 3), F(2, 3)], [(0, 1)] * 2, (), constant=F(1, 9)),
        BoxQP([[2, -2], [-2, F(-1, 2)]], [0, 1], [(0, 1), (0, 2)], [1]),
        BoxQP([[2, 3, 4], [3, -1, -1], [4, -1, 2]], [1, 2, -2],
              [(2, 2), (0, 1), (F(1, 2), F(1, 2))], [0]),
        BoxQP([[2, -1], [-1, 2]], [F(-2, 3), -2], [(F(-1, 3), F(4, 3)), (0, 2)], [1]),
        BoxQP([[-2, 1, 0], [1, 0, -1], [0, -1, 0]], [1, 0, 1], [(0, 1)] * 3, [1]),
        BoxQP([[2]], [3], [(F(1, 3), F(1, 3))], ()),
    ]
    for problem in cases:
        optimum = reference(problem)
        for options in ({"time_limit": 0}, {"time_limit": 2, "max_stages": 32}):
            cert = restored(solve_exact(problem, **options))
            assert verify_certificate(cert)["valid"]
            bounded(cert, optimum)
            summary["exact_runs"] += 1
        for backend in ("grid", "auto", "mincut", "submodular"):
            cert = restored(solve_with_recourse(problem, backend=backend, exact=True,
                                               time_limit=2, max_stages=32))
            # Replays must consume witnesses only, never re-run optimization.
            with patch("rational_optimization.solve_lp", side_effect=AssertionError("LP during replay")), \
                 patch("rational_optimization.solve_convex_box_qp", side_effect=AssertionError("QP during replay")), \
                 patch("certified_grid.solve", side_effect=AssertionError("grid during replay")):
                assert verify_pipeline(cert, problem)["valid"]
            bounded(cert, optimum)
            summary["pipeline_runs"] += 1
            altered = BoxQP(problem.A, problem.b, problem.bounds, problem.integers,
                            problem.bags, problem.edges, problem.constant + 1)
            expect_reject(lambda: verify_pipeline(cert, altered))
            bad = deepcopy(cert)
            bad["point"][0] = str(F(bad["point"][0]) + 1)
            expect_reject(lambda: verify_pipeline(bad, problem))
            summary["mutations_rejected"] += 2

    clipped = BoxQP([[6, -4], [-4, 2]], [0, 0], [(0, 1)] * 2, ())
    cert = restored(solve_with_recourse(clipped, backend="convex", blocks=[[1]],
                                       epsilon=F(1, 64), max_stages=16, time_limit=3))
    assert verify_pipeline(cert, clipped)["valid"]
    bounded(cert, reference(clipped))
    expect_reject(lambda: verify_pipeline(cert, clipped, max_table_states=1))
    summary["pipeline_runs"] += 1
    summary["mutations_rejected"] += 1

    # A caller's incumbent belongs to the original coordinates even when
    # fixed and affine variables disappear before entering the grid engine.
    warm_model = BoxQP([[F(7, 4), -2, -2], [-2, 2, 2], [-2, 2, 2]],
                      [0, 0, 0], [(0, 2), (0, 1), (0, 1)], ())
    for exact in (False, True):
        cert = restored(solve_with_recourse(warm_model, backend="grid", exact=exact,
                                           warm_start=[F(2), F(1), F(1)], max_stages=4))
        assert verify_pipeline(cert, warm_model)["valid"]
        bounded(cert, F(-1, 2))
        summary["pipeline_runs"] += 1

    # Constraint-only edges must be represented even with no objective edge.
    constrained = ConstrainedQP([[2, 0, 0], [0, 2, 0], [0, 0, 0]],
                  [F(-2, 3), F(-4, 3), 0], [(0, 1), (0, 1), (0, 2)], {2: [0, 2]},
                  [[1, 1, 0]], [1], ["=="], [(0, 1), (2,)], [(0, 1)],
                  {"kind": "network"}, constant=F(5, 9))
    for unions, exact, cap in ((False, False, 1), (False, True, 32), (True, True, 32)):
        cert = restored(solve_constrained(constrained, exact=exact, retain_unions=unions,
                                           max_stages=cap, time_limit=3))
        assert verify_constrained(cert)["valid"]
        assert cert["lower"] is None or F(cert["lower"]) <= 0 <= F(cert["upper"])
        if cert["status"] == "exact":
            assert cert["lower"] == cert["upper"] == "0"
        summary["constrained_runs"] += 1

    endpoints = BoxQP([[-2, 0], [0, 0]], [1, 0], [(0, 1), (-2, 2)], [1])
    result = solve_endpoint_set(endpoints)
    cert = restored(result["certificate"])
    assert verify_set(cert, endpoints)
    for x, z in product((F(0), F(1, 3), F(1)), range(-2, 3)):
        assert contains(cert, [x, F(z)], endpoints) == (x in (0, 1))
        summary["set_memberships"] += 1
    expect_reject(lambda: verify_set(cert, cases[0]))
    summary["mutations_rejected"] += 1
    return summary


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
