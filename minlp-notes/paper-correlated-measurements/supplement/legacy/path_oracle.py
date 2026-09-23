"""Count-constrained path pricing and information-hull bounds.

All reported bounds are numerical, not interval-certified.  The upper-bound
formula is valid at every positive definite reference matrix; it does not
depend on successful convergence of the continuous optimizer.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
import heapq
import time

import numpy as np
from scipy.optimize import minimize


@dataclass
class InformationPaths:
    first: np.ndarray
    transition: np.ndarray
    prior: np.ndarray

    @property
    def n(self):
        return len(self.first)

    def information(self, selected):
        selected = tuple(selected)
        result = self.prior.copy()
        if selected:
            result += self.first[selected[0]]
            for i, j in zip(selected, selected[1:]):
                result += self.transition[i, j]
        return result

    def value(self, selected):
        return logdet(self.information(selected))


def logdet(matrix):
    # Cholesky rejects non-positive matrices, unlike a determinant sign check.
    return float(2 * np.log(np.diag(np.linalg.cholesky(matrix))).sum())


def scalar_markov(sensitivity, rho, prior, variance=1.0):
    """Known stationary scalar AR(1) errors, fully observed at selected times."""
    f = np.asarray(sensitivity, dtype=float)
    if (f.ndim != 2 or f.shape[1] == 0 or not np.all(np.isfinite(f))
            or not -1 < rho < 1 or not np.isfinite(variance) or variance <= 0):
        raise ValueError("Require a sensitivity matrix, |rho|<1 and variance>0")
    n, p = f.shape
    prior = np.asarray(prior, dtype=float)
    if prior.shape != (p, p):
        raise ValueError("Prior dimension does not match sensitivities")
    if not np.all(np.isfinite(prior)) or not np.allclose(
            prior, prior.T, rtol=1e-12, atol=1e-14):
        raise ValueError("Prior must be finite and symmetric")
    prior = (prior + prior.T) / 2
    logdet(prior)
    first = np.einsum("ni,nj->nij", f, f) / variance
    transition = np.zeros((n, n, p, p))
    for i in range(n):
        for j in range(i + 1, n):
            phi = rho ** (j - i)
            delta = f[j] - phi * f[i]
            transition[i, j] = np.outer(delta, delta) / (variance * (1 - phi**2))
    return InformationPaths(first, transition, prior)


def price_path(data, count, hessian, required=(), forbidden=()):
    """Maximize trace(H J(path)) over exactly count visits in O(count*n^2).

    Mandatory visits are enforced by prohibiting arcs that skip one.  Return
    None if the requested face contains no path.  H may be any symmetric
    matrix; its positive definiteness is needed only by the logdet bound.
    """
    n = data.n
    req, ban = set(required), set(forbidden)
    if (not isinstance(count, (int, np.integer)) or not 0 <= count <= n
            or any(not isinstance(i, (int, np.integer)) or not 0 <= i < n
                   for i in req | ban)):
        raise ValueError("Invalid count or index")
    if req & ban or len(req) > count or n - len(ban) < count:
        return None
    prior_score = float(np.sum(hessian * data.prior))
    if count == 0:
        return ((), prior_score) if not req else None
    mandatory = np.array([i in req for i in range(n)], dtype=int)
    prefix = np.r_[0, np.cumsum(mandatory)]
    first = np.einsum("ij,nij->n", hessian, data.first)
    edges = np.einsum("ij,nmij->nm", hessian, data.transition)
    dp = np.full((count + 1, n), -np.inf)
    parent = np.full((count + 1, n), -1, dtype=int)
    for j in range(n):
        if j not in ban and prefix[j] == 0:
            dp[1, j] = first[j]
    for k in range(2, count + 1):
        for j in range(k - 1, n):
            if j in ban:
                continue
            candidates = dp[k - 1, :j] + edges[:j, j]
            candidates = np.where(prefix[j] - prefix[1 : j + 1] == 0,
                                  candidates, -np.inf)
            i = int(np.argmax(candidates))
            dp[k, j] = candidates[i]
            parent[k, j] = i
    terminal = np.where(prefix[n] - prefix[1:] == 0, dp[count], -np.inf)
    j = int(np.argmax(terminal))
    if not np.isfinite(terminal[j]):
        return None
    score = float(terminal[j] + prior_score)
    selected = [j]
    for k in range(count, 1, -1):
        j = int(parent[k, j])
        selected.append(j)
    return tuple(reversed(selected)), score


def _correct_weights(matrices, weights):
    """Optimize over accumulated paths; feasibility is checked independently."""
    def objective(w):
        matrix = np.einsum("n,nij->ij", w, matrices)
        inverse = np.linalg.inv(matrix)
        return -logdet(matrix), -np.einsum("ij,nij->n", inverse, matrices)

    result = minimize(objective, weights, jac=True, method="SLSQP",
                      bounds=[(0.0, 1.0)] * len(weights),
                      constraints={"type": "eq", "fun": lambda w: w.sum() - 1,
                                   "jac": lambda w: np.ones(len(w))},
                      options={"ftol": 1e-12, "maxiter": 150})
    candidate = np.maximum(result.x, 0)
    if not np.all(np.isfinite(candidate)) or candidate.sum() <= 0:
        return weights
    candidate /= candidate.sum()
    return candidate if objective(candidate)[0] <= objective(weights)[0] else weights


def hull_bound(data, count, required=(), forbidden=(), warm_paths=(),
               iterations=100, tolerance=1e-8, deadline=float("inf")):
    """Fully corrective conditional gradients for the count-layered hull.

    Every iterate is a convex combination of admissible paths.  Each pricing
    call supplies a dual upper bound.  A time/iteration limit returns the best
    bound obtained, not a claim that the relaxation has been optimized.
    """
    req, ban = set(required), set(forbidden)
    initial = price_path(data, count, np.eye(len(data.prior)), req, ban)
    if initial is None:
        return None
    valid_warm = []
    for path in warm_paths:
        path = tuple(path)
        if (any(not isinstance(i, (int, np.integer)) or not 0 <= i < data.n
                for i in path) or tuple(sorted(set(path))) != path):
            raise ValueError("Warm paths must have sorted, distinct valid indices")
        if len(path) == count and req <= set(path) and not ban.intersection(path):
            valid_warm.append(path)
    paths = list(dict.fromkeys(valid_warm))
    if initial[0] not in paths:
        paths.append(initial[0])
    matrices = np.array([data.information(p) for p in paths])
    weights = np.full(len(paths), 1 / len(paths))
    best_upper, gap = float("inf"), float("inf")
    best_path = max(paths, key=data.value)
    calls = 0
    for _ in range(max(1, iterations)):
        weights = _correct_weights(matrices, weights)
        matrix = np.einsum("n,nij->ij", weights, matrices)
        inverse = np.linalg.inv(matrix)
        priced = price_path(data, count, inverse, req, ban)
        calls += 1
        gap = max(0.0, priced[1] - len(matrix))
        best_upper = min(best_upper, logdet(matrix) + gap)
        if data.value(priced[0]) > data.value(best_path):
            best_path = priced[0]
        if gap <= tolerance or time.perf_counter() >= deadline:
            break
        if priced[0] in paths:
            # The restricted optimizer stalled; the bound remains valid.
            break
        paths.append(priced[0])
        matrices = np.concatenate((matrices, data.information(priced[0])[None]))
        weights = np.r_[weights, 0.0]
    visits = np.zeros(data.n)
    for path, weight in zip(paths, weights):
        visits[list(path)] += weight
    return {"lower": data.value(best_path), "upper": best_upper,
            "path": best_path, "visits": visits, "paths": paths,
            "weights": weights, "relaxation_value": logdet(matrix),
            "relaxation_gap": gap, "pricing_calls": calls}


def solve_branch_bound(data, count, time_limit=30.0, tolerance=1e-6,
                       node_iterations=40):
    """Numerical branch and bound using the path-hull pricing certificate."""
    start = time.perf_counter()
    deadline = start + time_limit
    root = hull_bound(data, count, iterations=node_iterations, deadline=deadline)
    if root is None:
        return {"status": "infeasible", "nodes": 0}
    lower, best = root["lower"], root["path"]
    heap = [(-root["upper"], 0, (), (), root)]
    nodes, pricing_calls, serial = 1, root["pricing_calls"], 0
    unresolved_upper = -float("inf")
    pruned_upper = -float("inf")
    while heap and time.perf_counter() < deadline:
        negative_upper, _, required, forbidden, bound = heapq.heappop(heap)
        if -negative_upper <= lower + tolerance:
            pruned_upper = max(pruned_upper, -negative_upper)
            continue
        free = set(range(data.n)) - set(required) - set(forbidden)
        if not free:
            continue
        branch = min(free, key=lambda i: abs(bound["visits"][i] - 0.5))
        children = [(tuple(sorted((*required, branch))), forbidden),
                    (required, tuple(sorted((*forbidden, branch))))]
        for position, (req, ban) in enumerate(children):
            if time.perf_counter() >= deadline:
                # The parent's bound covers every child not processed.
                unresolved_upper = max(unresolved_upper, -negative_upper)
                break
            child = hull_bound(data, count, req, ban, bound["paths"],
                               node_iterations, deadline=deadline)
            nodes += 1
            if child is None:
                continue
            pricing_calls += child["pricing_calls"]
            if child["lower"] > lower:
                lower, best = child["lower"], child["path"]
            upper = min(child["upper"], -negative_upper)
            if upper > lower + tolerance:
                serial += 1
                heapq.heappush(heap, (-upper, serial, req, ban, child))
            else:
                pruned_upper = max(pruned_upper, upper)
    upper = max(lower, unresolved_upper, pruned_upper,
                -heap[0][0] if heap else lower)
    return {"status": "optimal" if upper <= lower + tolerance else "limit",
            "lower": lower, "upper": upper, "path": best,
            "nodes": nodes, "pricing_calls": pricing_calls,
            "root_upper": root["upper"], "root_lower": root["lower"],
            "seconds": time.perf_counter() - start}


def self_check():
    rng = np.random.default_rng(2197)
    checked = 0
    for n in (4, 6, 8):
        f = rng.normal(size=(n, 3))
        rho = 0.7
        prior = np.eye(3)
        data = scalar_markov(f, rho, prior)
        covariance = rho ** np.abs(np.subtract.outer(np.arange(n), np.arange(n)))
        for count in (0, 1, min(3, n)):
            all_paths = list(combinations(range(n), count))
            for path in all_paths:
                selected = list(path)
                dense = prior.copy()
                if selected:
                    dense += f[selected].T @ np.linalg.solve(
                        covariance[np.ix_(selected, selected)], f[selected])
                np.testing.assert_allclose(data.information(path), dense,
                                           atol=1e-10, rtol=1e-10)
            h = rng.normal(size=(3, 3)); h = h + h.T
            for req, ban in [((), ()), ((1,), (n - 1,)), ((), (0,))]:
                candidates = [p for p in all_paths if set(req) <= set(p)
                              and not set(ban).intersection(p)]
                priced = price_path(data, count, h, req, ban)
                if not candidates:
                    assert priced is None
                else:
                    oracle = max(float(np.sum(h * data.information(p)))
                                 for p in candidates)
                    assert abs(priced[1] - oracle) < 1e-9
                    assert priced[0] in candidates
                checked += 1
            exact = max(data.value(p) for p in all_paths)
            solved = solve_branch_bound(data, count, time_limit=10)
            assert solved["status"] == "optimal", solved
            assert abs(solved["lower"] - exact) < 1e-6, solved
            assert solved["upper"] + 1e-9 >= exact, solved
    print({"oracle_faces_checked": checked, "enumerated_solver_cases": 9,
           "status": "passed"})


if __name__ == "__main__":
    self_check()
