"""Exact discovery and compact certificates for two box-QP optimal-set classes.

``solve_endpoint_set`` covers coordinatewise concave mixed boxes.  Discovery
of a diagonal Lagrangian certificate covers continuous boxes, including
nonunique/disconnected optima.  A failed discovery run is inconclusive.
Neither function takes an optimizer or a growth constant as input.
"""

from fractions import Fraction as F
from itertools import product
from math import isqrt, lcm
from time import perf_counter

from certified_grid import (BoxQP, Budget, BudgetExceeded, coordinate_grid,
                            grid_dp, rational)


def _active(problem):
    return tuple(i for i, (lo, hi) in enumerate(problem.bounds) if lo != hi)


def _local(problem, t, state, grids):
    values = {i: grids[i][k] for i, k in zip(problem.bags[t], state)}
    cost = problem.constant if t == 0 else F(0)
    for i, home in enumerate(problem.home):
        if home == t:
            cost += problem.A[i][i] * values[i] ** 2 / 2 + problem.b[i] * values[i]
    for (i, j, coefficient), home in zip(problem.interactions, problem.factor_home):
        if home == t:
            cost += coefficient * values[i] * values[j]
    return cost


def solve_endpoint_set(problem, *, time_limit=30.0, max_table_states=100000):
    """Return every optimizer through nonnegative local support equations.

    Fixed coordinates may have any diagonal.  Nonfixed integer coordinates
    need only their two bounds, regardless of the interval's numerical width.
    ``certificate`` is JSON serializable and is replayed by the separate
    ``verify_optimal_sets`` module.  Resource failure returns no certificate.
    """
    if any(problem.A[i][i] > 0 for i in _active(problem)):
        raise ValueError("endpoint class requires nonpositive active diagonals")
    budget = Budget(time_limit)
    grids = tuple(tuple(dict.fromkeys(pair)) for pair in problem.bounds)
    try:
        result = grid_dp(problem, grids, tuple(tuple(F(0) for _ in grid)
                                                for grid in grids), budget,
                         max_table_states)
        messages, residuals = [], []
        for t, bag in enumerate(problem.bags):
            budget.check(force=True)
            parent = problem.parents[t]
            separator = tuple(sorted(set(bag) & set(problem.bags[parent]))) if parent is not None else ()
            message = result["messages"][t, parent] if parent is not None else {(): result["lower"]}
            messages.append([{"state": list(s), "value": str(v)} for s, v in sorted(message.items())])
            rows = []
            for state in product(*(range(len(grids[i])) for i in bag)):
                budget.check()
                labels = dict(zip(bag, state))
                cost = _local(problem, t, state, grids)
                for child in problem.neighbors[t]:
                    if problem.parents.get(child) == t:
                        child_sep = tuple(sorted(set(bag) & set(problem.bags[child])))
                        cost += result["messages"][child, t][tuple(labels[i] for i in child_sep)]
                residual = cost - message[tuple(labels[i] for i in separator)]
                rows.append({"state": list(state), "value": str(residual)})
            residuals.append(rows)
        certificate = {"schema": "box-qp-optimal-set-v1", "kind": "endpoint",
                       "problem": problem.to_dict(), "minimum": str(result["lower"]),
                       "point": list(map(str, result["point"])),
                       "messages": messages, "residuals": residuals}
        return {"status": "certified", "certificate": certificate,
                "table_states": result["table_states"],
                "elapsed_seconds": perf_counter() - budget.started}
    except BudgetExceeded as exc:
        return {"status": "resource_limit", "reason": str(exc),
                "elapsed_seconds": perf_counter() - budget.started}


def diagonal_certificate(problem, point, *, check=None):
    """Construct and independently validate a certificate at a supplied point.

    This is an optional certification API, separate from automatic discovery.
    Fixed integer variables are allowed; all nonfixed variables must be real.
    A failed test returns None and makes no local/global optimality claim.
    """
    from verify_optimal_sets import CertificateError, verify_certificate
    if problem.integers & set(_active(problem)):
        raise ValueError("diagonal class requires continuous active variables")
    point = tuple(map(rational, point))
    if not problem.feasible(point):
        return None
    active = _active(problem)
    diagonal = []
    for i in active:
        if check is not None:
            check()
        lo, hi = problem.bounds[i]
        gradient = problem.b[i] + sum((problem.A[i][j] * point[j]
                                        for j in range(len(point))), F(0))
        if point[i] == lo and gradient >= 0:
            diagonal.append(2 * gradient / (hi - lo))
        elif point[i] == hi and gradient <= 0:
            diagonal.append(-2 * gradient / (hi - lo))
        elif lo < point[i] < hi and gradient == 0:
            diagonal.append(F(0))
        else:
            return None
    certificate = {"schema": "box-qp-optimal-set-v1", "kind": "diagonal",
                   "problem": problem.to_dict(), "minimum": str(problem.value(point)),
                   "point": list(map(str, point)), "active": list(active),
                   "diagonal": list(map(str, diagonal))}
    try:
        verify_certificate(certificate, problem, check=check)
    except CertificateError:
        return None
    return certificate


def recovery_radius(problem):
    """Return the exact stationary-polytope height radius, after substitution."""
    active = _active(problem)
    if not active:
        return F(1)
    fixed = {i: lo for i, (lo, hi) in enumerate(problem.bounds) if lo == hi}
    q = [[problem.A[i][j] / 2 for j in active] for i in active]
    b = [problem.b[i] + sum((problem.A[i][j] * v for j, v in fixed.items()), F(0))
         for i in active]
    base = [lo for lo, _ in problem.bounds]
    for i in active:
        base[i] = F(0)
    data = [v for row in q for v in row] + b + [problem.value(base)]
    data += [v for i in active for v in problem.bounds[i]]
    denominator = lcm(*(v.denominator for v in data))
    coefficient = max([1] + [abs(denominator * v) for row in q for v in row])
    determinant = (2 * len(active) * coefficient) ** len(active)
    return F(1, 4 * len(active) * denominator * int(determinant))


def _recover(problem, point, tau, *, max_lp_pivots, check):
    """Solve the original selected-face stationarity LP; no guessed LB is used."""
    from rational_optimization import solve_lp
    active = _active(problem)
    chosen = {}
    for i, (lo, hi) in enumerate(problem.bounds):
        if lo == hi or point[i] - lo <= tau:
            chosen[i] = lo
        elif hi - point[i] <= tau:
            chosen[i] = hi
    free = tuple(i for i in active if i not in chosen)
    if not free:
        return tuple(chosen[i] for i in range(len(point)))
    matrix = [[problem.A[i][j] for j in free] for i in free]
    rhs = [-problem.b[i] - sum((problem.A[i][j] * v for j, v in chosen.items()), F(0))
           for i in free]
    # The exact LP helper returns only verified rational primal solutions.
    result = solve_lp([F(0)] * len(free), A_eq=matrix, b_eq=rhs,
                      bounds=[problem.bounds[i] for i in free], max_pivots=max_lp_pivots,
                      check=check)
    if result.status == "limit":
        raise BudgetExceeded("lp_pivot_limit")
    if result.status != "optimal":
        return None
    answer = dict(chosen)
    answer.update(zip(free, result.x))
    return tuple(answer[i] for i in range(len(point)))


def discover_diagonal_set(problem, *, max_trials=8, max_stages=256,
                          time_limit=30.0, max_table_states=100000,
                          early_accept=True, max_lp_pivots=10000):
    """Search finite proximal trials K=1,2,4,... without assuming their validity.

    Only exact original KKT plus a PSD diagonal certificate authorizes success.
    ``max_stages`` bounds each trial, and a limit returns ``inconclusive``.
    On the stated certificate class the unlimited schedule eventually succeeds.
    Outside it, failure is neither nonmembership nor a global bound.
    """
    if type(max_trials) is not int or max_trials < 1 or type(max_stages) is not int or max_stages < 1:
        raise ValueError("trial and stage limits must be positive integers")
    active = _active(problem)
    if problem.integers & set(active):
        raise ValueError("diagonal discovery requires continuous active variables")
    budget = Budget(time_limit)
    history = []
    if not active:
        cert = diagonal_certificate(problem, tuple(lo for lo, _ in problem.bounds))
        return {"status": "certified", "certificate": cert, "trials": [],
                "elapsed_seconds": perf_counter() - budget.started}
    n = len(active)
    curvature = max(F(1), *(problem.A[i][i] for i in active))
    tau = recovery_radius(problem)
    scale = max(hi - lo for lo, hi in problem.bounds)
    try:
        for trial in range(max_trials):
            conditioning = 2 ** trial
            theta = F(1, 4)
            while theta * theta * conditioning > F(1, 8):
                theta /= 2
            root = isqrt(conditioning * n)
            rho = 2 * (root if root * root == conditioning * n else root + 1)
            lam = curvature * theta * theta / 4
            target = min(F(1), curvature * tau * tau / (4 * conditioning))
            epsilon = F(1)
            while epsilon > target:
                epsilon /= 2
            final_stage, final_h = 0, scale
            while curvature * n * final_h * final_h / 2 > epsilon:
                final_stage += 1
                final_h /= 2
            entry = {"K": conditioning, "required_stages": final_stage + 1,
                     "completed_stages": 0, "table_states": 0,
                     "rejected_candidates": 0}
            history.append(entry)
            center = tuple(lo for lo, _ in problem.bounds)
            h = scale
            for stage in range(min(final_stage + 1, max_stages)):
                budget.check(force=True)
                grids, penalties = [], []
                for i, (lo, hi) in enumerate(problem.bounds):
                    if i not in active:
                        grid, lengths = (lo,), (F(0),)
                    else:
                        grid, lengths = coordinate_grid(max(lo, center[i] - rho * h),
                                                        min(hi, center[i] + rho * h),
                                                        center[i], h, theta, False, budget,
                                                        max_nodes=max_table_states)
                    grids.append(grid)
                    penalties.append(tuple(curvature * length ** 2 / 8 - lam * (x - center[i]) ** 2
                                           for x, length in zip(grid, lengths)))
                result = grid_dp(problem, grids, penalties, budget, max_table_states)
                center = result["point"]
                entry["completed_stages"] += 1
                entry["table_states"] += result["table_states"]
                if early_accept or stage == final_stage:
                    budget.check(force=True)
                    candidate = _recover(problem, center, tau, max_lp_pivots=max_lp_pivots,
                                         check=lambda: budget.check(force=True))
                    cert = diagonal_certificate(problem, candidate, check=lambda: budget.check(force=True)) if candidate is not None else None
                    if cert is not None:
                        return {"status": "certified", "certificate": cert,
                                "trials": history, "recovery_radius": str(tau),
                                "elapsed_seconds": perf_counter() - budget.started}
                    entry["rejected_candidates"] += 1
                h /= 2
            if final_stage + 1 > max_stages:
                return {"status": "inconclusive", "reason": "stage_limit", "trials": history,
                        "elapsed_seconds": perf_counter() - budget.started}
        reason = "trial_limit"
    except BudgetExceeded as exc:
        reason = str(exc)
    return {"status": "inconclusive", "reason": reason, "trials": history,
            "elapsed_seconds": perf_counter() - budget.started}
