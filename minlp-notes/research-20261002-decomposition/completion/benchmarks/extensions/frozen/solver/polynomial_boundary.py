"""Automatic exact implicit boundary output from a certified polynomial grid.

Global grid containment is followed by exact monotonicity reductions and a
uniform positive-definite restricted-Hessian test.  The output describes one
global optimizer as a unique convex polynomial minimizer; it need not have
rational coordinates.  Weak reductions need not preserve every optimizer.
"""

from fractions import Fraction as F
from time import perf_counter

from certified_grid import Budget, BudgetExceeded


def _positive_definite(matrix, check):
    a = [list(row) for row in matrix]
    for k in range(len(a)):
        check()
        pivot = a[k][k]
        if pivot <= 0:
            return False
        for i in range(k + 1, len(a)):
            for j in range(i, len(a)):
                a[i][j] -= a[i][k] * a[k][j] / pivot
                a[j][i] = a[i][j]
    return True


def _retained(problem, grid_certificate, max_table_states, check):
    from verify_polynomial import verify_polynomial
    checked = verify_polynomial(grid_certificate, max_table_states=max_table_states,
                                expected_problem=problem, check=check)
    return checked


def certify_boundary(problem, grid_certificate, *, time_limit=30.0,
                     max_table_states=1000000):
    """Try exact face discovery on a replayed globally valid retained box.

    Returns ``certified`` with a JSON artifact, or ``inconclusive`` if the
    available box does not support the sufficient sign/curvature tests.
    Invalid input certificates raise instead of yielding a success status.
    """
    budget = Budget(time_limit)
    try:
        checked = _retained(problem, grid_certificate, max_table_states,
                            lambda: budget.check(force=True))
        bounds = [tuple(F(x) for x in pair) for pair in checked["retained_bounds"]]
        budget.check(force=True)
        if F(checked["lower"]) == F(checked["upper"]):
            point = tuple(F(x) for x in grid_certificate["point"])
            certificate = {"schema": "polynomial-boundary-v1", "kind": "grid_point",
                           "problem": problem.to_dict(), "grid_certificate": grid_certificate,
                           "point": list(map(str, point)), "value": str(problem.value(point))}
            return {"status": "certified", "certificate": certificate,
                    "elapsed_seconds": perf_counter() - budget.started}
        if any(bounds[i][0] != bounds[i][1] for i in problem.integers):
            return {"status": "inconclusive", "reason": "integer_labels_not_fixed"}
        reductions = []
        while True:
            changed = False
            for i, (lo, hi) in enumerate(bounds):
                budget.check(force=True)
                if lo == hi or i in problem.integers:
                    continue
                lower, upper = problem.derivative_bounds((i,), bounds)
                endpoint = None
                if lo == problem.bounds[i][0] and lower >= 0:
                    endpoint = lo
                elif hi == problem.bounds[i][1] and upper <= 0:
                    endpoint = hi
                if endpoint is not None:
                    reductions.append({"coordinate": i, "endpoint": str(endpoint),
                                       "derivative_lower": str(lower), "derivative_upper": str(upper)})
                    bounds[i] = (endpoint, endpoint)
                    changed = True
            if not changed:
                break
        free = tuple(i for i, (lo, hi) in enumerate(bounds) if lo != hi)
        certificate = {"schema": "polynomial-boundary-v1", "problem": problem.to_dict(),
                       "grid_certificate": grid_certificate, "reductions": reductions,
                       "face_bounds": [[str(lo), str(hi)] for lo, hi in bounds],
                       "free": list(free)}
        if not free:
            point = tuple(lo for lo, _ in bounds)
            certificate.update(kind="point", point=list(map(str, point)),
                               value=str(problem.value(point)))
        else:
            midpoint = tuple((lo + hi) / 2 for lo, hi in bounds)
            hessian = problem.hessian(midpoint)
            matrix = [[hessian[i][j] for j in free] for i in free]
            delta = F(0)
            for row, i in enumerate(free):
                budget.check(force=True)
                error = F(0)
                for column, j in enumerate(free):
                    lower, upper = problem.derivative_bounds((i, j), bounds)
                    error += max(abs(lower - matrix[row][column]), abs(upper - matrix[row][column]))
                delta = max(delta, error)
            shifted = [[value - (delta if i == j else 0) for j, value in enumerate(row)]
                       for i, row in enumerate(matrix)]
            if not _positive_definite(shifted, lambda: budget.check(force=True)):
                return {"status": "inconclusive", "reason": "restricted_hessian_not_certified",
                        "reductions_found": len(reductions)}
            certificate.update(kind="strongly_convex_patch", midpoint=list(map(str, midpoint)),
                               hessian=[list(map(str, row)) for row in matrix],
                               hessian_error=str(delta))
        return {"status": "certified", "certificate": certificate,
                "elapsed_seconds": perf_counter() - budget.started}
    except BudgetExceeded as exc:
        return {"status": "inconclusive", "reason": str(exc),
                "elapsed_seconds": perf_counter() - budget.started}


def discover_boundary(problem, *, max_rounds=16, time_limit=30.0,
                      max_table_states=100000, max_stages=128, **grid_options):
    """Bounded automatic search, replaying finer certified global grid runs.

    The trial accuracies are 1, 1/4, 1/16, ... .  No optimizer, active face,
    growth constant, or derivative margin is supplied.  This straightforward
    restart implementation makes no theorem-level FPT/dovetail work claim.
    """
    from polynomial_grid import solve
    if type(max_rounds) is not int or max_rounds < 1:
        raise ValueError("max_rounds must be a positive integer")
    started = perf_counter()
    attempts = []
    epsilon = F(1)
    for _ in range(max_rounds):
        remaining = time_limit - (perf_counter() - started)
        if remaining <= 0:
            return {"status": "inconclusive", "reason": "time_limit", "attempts": attempts}
        result = solve(problem, epsilon=epsilon, time_limit=remaining,
                       max_table_states=max_table_states, max_stages=max_stages, **grid_options)
        attempt = {"epsilon": str(epsilon), "grid_status": result["status"]}
        attempts.append(attempt)
        remaining = time_limit - (perf_counter() - started)
        if remaining <= 0:
            return {"status": "inconclusive", "reason": "time_limit", "attempts": attempts}
        patch = certify_boundary(problem, result, time_limit=remaining,
                                 max_table_states=max_table_states)
        attempt["patch_status"] = patch["status"]
        attempt["patch_reason"] = patch.get("reason")
        if patch["status"] == "certified":
            patch["attempts"] = attempts
            return patch
        epsilon /= 4
    return {"status": "inconclusive", "reason": "round_limit", "attempts": attempts,
            "elapsed_seconds": perf_counter() - started}
