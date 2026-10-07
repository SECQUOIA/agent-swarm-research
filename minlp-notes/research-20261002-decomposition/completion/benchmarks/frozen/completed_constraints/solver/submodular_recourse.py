"""Certified mixed concave/convex box-QP recourse by exact cutting planes.

The value function on endpoint labels is submodular after checked sign flips.
Greedy-base cuts minimize its Lovasz extension. This implementation has a finite
factorial cut bound, not a polynomial running-time guarantee. Every returned
bound, including capped runs, has a certificate requiring no optimization.
"""
from __future__ import annotations

from fractions import Fraction as F
from math import isfinite
from time import perf_counter

from certified_grid import BoxQP, BudgetExceeded, interval_lower_bound, rational
from rational_optimization import is_psd, solve_convex_box_qp, solve_lp


class _Limit(Exception):
    pass


def _recognize(problem, concave, flips, check):
    active = tuple(i for i, (lo, hi) in enumerate(problem.bounds) if lo < hi)
    if concave is None:
        D = tuple(i for i in active if problem.A[i][i] <= 0)
    else:
        D = tuple(concave)
        if (len(set(D)) != len(D) or any(type(i) is not int or i not in active for i in D)):
            raise ValueError("concave indices must be distinct, active coordinates")
    C = tuple(i for i in active if i not in D)
    if any(problem.A[i][i] > 0 for i in D):
        return None, "positive_concave_diagonal"
    if any(i in problem.integers for i in C):
        return None, "integer_convex_coordinate"
    if not is_psd([[problem.A[i][j] for j in C] for i in C], check):
        return None, "nonconvex_continuous_block"
    if flips is None:
        signs = {}
        for root in active:
            if root in signs:
                continue
            signs[root] = 1
            pending = [root]
            for i in pending:
                check()
                for j in active:
                    coefficient = problem.A[i][j]
                    if j == i or not coefficient:
                        continue
                    sign = -signs[i] if coefficient > 0 else signs[i]
                    if j in signs and signs[j] != sign:
                        return None, "inconsistent_edge_signs"
                    if j not in signs:
                        signs[j] = sign
                        pending.append(j)
    else:
        signs = dict(flips)
        if (set(signs) != set(active) or any(type(i) is not int for i in signs)
                or any(type(v) is not int or v not in (-1, 1) for v in signs.values())):
            raise ValueError("flips must map every active coordinate to -1 or 1")
        if any(signs[i] * signs[j] * problem.A[i][j] > 0
               for i in active for j in active if i != j):
            return None, "inconsistent_edge_signs"
    return (D, C, signs), ""


def solve_submodular(problem, epsilon=0, exact=False, concave=None, flips=None,
                     max_cuts=100, max_queries=10000, max_faces=10000,
                     max_pivots=10000, time_limit=None, check=None):
    """Minimize a supported BoxQP, with rational witnesses and explicit caps.

    D (``concave``) uses endpoints, including effective native-integer endpoints;
    the remaining nonfixed coordinates must be continuous with a PSD Hessian.
    Automatic recognition chooses every nonpositive diagonal for D. Supplied D
    can use any order. Fixed coordinates are substituted in each query. Edge
    signs are found by graph propagation unless supplied as an index/sign map.

    max_queries counts uncached convex-QP calls; max_cuts counts greedy bases;
    max_faces is per QP; max_pivots is cumulative across all LP/QP calls.
    Time checks are cooperative. BudgetExceeded from an external check yields
    the strongest completed certificate; other exceptions propagate.
    """
    epsilon = rational(epsilon)
    if type(exact) is not bool or epsilon < 0:
        raise ValueError("invalid exact-output flag or tolerance")
    if any(type(v) is not int or v < 0 for v in
           (max_cuts, max_queries, max_faces, max_pivots)):
        raise ValueError("caps must be nonnegative integers")
    if time_limit is not None and (isinstance(time_limit, bool)
            or not isinstance(time_limit, (int, float)) or not isfinite(time_limit) or time_limit < 0):
        raise ValueError("time_limit must be finite and nonnegative")
    started = perf_counter()
    stats = {"queries": 0, "cuts": 0, "lp_calls": 0, "pivots": 0, "qp_faces": 0}
    lower = interval_lower_bound(problem)
    point = min((tuple(lo for lo, _ in problem.bounds), tuple(hi for _, hi in problem.bounds)),
                key=problem.value)
    upper = problem.value(point)
    proof, cache, cuts = None, {}, []

    def tick():
        if time_limit is not None and perf_counter() - started >= time_limit:
            raise _Limit("time_limit")
        if check is not None:
            check()

    def finish(status, reason=""):
        if lower == upper:
            status, reason = "exact", ""
        elif status != "unsupported" and not exact and upper - lower <= epsilon:
            status, reason = "epsilon_optimal", ""
        stats["elapsed_seconds"] = perf_counter() - started
        return {"schema": "submodular-recourse-qp-v1", "problem": problem.to_dict(),
                "epsilon": str(epsilon), "exact_requested": exact, "status": status,
                "reason": reason, "point": list(map(str, point)),
                "lower": str(lower), "upper": str(upper), "gap": str(upper - lower),
                "proof": proof, "stats": stats}

    def done():
        return lower == upper or (not exact and upper - lower <= epsilon)

    try:
        tick()
        recognized, reason = _recognize(problem, concave, flips, tick)
        if recognized is None:
            return finish("unsupported", reason)
        D, C, signs = recognized
        proof = {"concave": list(D), "flips": [[i, signs[i]] for i in sorted(signs)],
                 "queries": [], "mixture": []}
        if done():
            return finish("exact" if lower == upper else "epsilon_optimal")
        positions = {i: j for j, i in enumerate(D)}
        H = [[problem.A[i][j] for j in C] for i in C]
        cbox = [problem.bounds[i] for i in C]

        def query(label):
            nonlocal point, upper
            key = tuple(sorted(label))
            if key in cache:
                return cache[key]
            tick()
            if stats["queries"] >= max_queries:
                raise _Limit("query_limit")
            stats["queries"] += 1
            chosen = set(key)
            x = [lo for lo, _ in problem.bounds]
            for i in D:
                high = (i in chosen) == (signs[i] == 1)
                x[i] = problem.bounds[i][int(high)]
            for i in C:
                x[i] = F(0)
            linear = [problem.b[i] + sum((problem.A[i][j] * x[j]
                                         for j in range(len(x)) if j not in C), F(0)) for i in C]
            result = solve_convex_box_qp(H, linear, cbox, constant=problem.value(x),
                max_faces=max_faces, max_pivots=max_pivots - stats["pivots"], check=tick)
            stats["pivots"] += result.pivots
            stats["qp_faces"] += result.faces
            if result.status != "optimal":
                raise _Limit("qp_" + result.reason)
            for i, value in zip(C, result.x):
                x[i] = value
            x = tuple(x)
            if result.value != problem.value(x):
                raise ArithmeticError("conditional QP objective mismatch")
            item = {"label": list(key), "point": list(map(str, x)), "value": str(result.value)}
            cache[key] = (result.value, item)
            proof["queries"].append(item)
            if result.value < upper:
                point, upper = x, result.value
            return cache[key]

        def greedy(permutation):
            label = []
            previous, _ = query(label)
            base = [F(0)] * len(D)
            for i in permutation:
                label.append(i)
                value, _ = query(label)
                base[positions[i]] = value - previous
                previous = value
            return tuple(base)

        def update_mixture(weights):
            nonlocal lower
            w = [sum((weight * base[j] for weight, (_, base) in zip(weights, cuts)), F(0))
                 for j in range(len(D))]
            candidate = cache[()][0] + sum((min(F(0), value) for value in w), F(0))
            if candidate > upper:
                raise ArithmeticError("base certificate exceeds feasible upper bound")
            if candidate > lower or (candidate == lower and not proof["mixture"]):
                lower = candidate
                proof["mixture"] = [{"permutation": list(permutation), "weight": str(weight)}
                                    for weight, (permutation, _) in zip(weights, cuts) if weight]

        if not D:
            value, _ = query(())
            cuts.append(((), ()))
            update_mixture([F(1)])
            return finish("exact")
        if max_cuts == 0:
            raise _Limit("cut_limit")
        permutation = tuple(D)
        cuts.append((permutation, greedy(permutation)))
        stats["cuts"] = len(cuts)
        update_mixture([F(1)])
        while not done():
            tick()
            rows = [list(base) + [F(-1)] for _, base in cuts]
            rhs = [-cache[()][0]] * len(cuts)
            stats["lp_calls"] += 1
            lp = solve_lp([F(0)] * len(D) + [F(1)], A_ub=rows, b_ub=rhs,
                          bounds=[(0, 1)] * len(D) + [(None, None)],
                          max_pivots=max_pivots - stats["pivots"], check=tick)
            stats["pivots"] += lp.pivots
            if lp.status == "limit":
                raise _Limit("lp_pivot_limit")
            if lp.status != "optimal":
                raise ArithmeticError("finite Lovasz master LP must have an optimum")
            weights = tuple(lp.certificate["inequality_multipliers"][:len(cuts)])
            if min(weights) < 0 or sum(weights, F(0)) != 1:
                raise ArithmeticError("invalid greedy-base dual weights")
            update_mixture(weights)
            if done():
                break
            permutation = tuple(sorted(D, key=lambda i: (-lp.x[positions[i]], i)))
            base = greedy(permutation)
            separated = cache[()][0] + sum((b * y for b, y in zip(base, lp.x)), F(0))
            if separated <= lp.value:
                if lower != upper:
                    raise ArithmeticError("closed Lovasz master did not certify a prefix optimum")
                break
            if any(permutation == old for old, _ in cuts):
                raise ArithmeticError("a stored greedy cut cannot violate its master LP")
            if len(cuts) >= max_cuts:
                raise _Limit("cut_limit")
            cuts.append((permutation, base))
            stats["cuts"] = len(cuts)
            # A new single base is itself a valid bound, even if the next LP is capped.
            update_mixture([F(0)] * (len(cuts) - 1) + [F(1)])
        return finish("exact" if lower == upper else "epsilon_optimal")
    except _Limit as exc:
        return finish("resource_limit", str(exc))
    except BudgetExceeded as exc:
        return finish("resource_limit", str(exc) or "external_budget")
