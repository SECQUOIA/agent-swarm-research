"""Certified sparse search with exact changing-active-set convex recourse.

Private blocks are continuous PSD box QPs. Their concave value factors are
queried at retained grid points, with exact KKT witnesses saved for replay.
The global search uses capped unknown-conditioning trials and geometric
incident-node corrections. See completion/convex-recourse.md.
"""

from fractions import Fraction as F
from itertools import product
from math import prod

from certified_grid import (BoxQP, Budget, BudgetExceeded, coordinate_grid,
                            interval_lower_bound, rational)
from decomposition import build_decomposition
from finite_dp import prepare_tree, solve_tree
from rational_optimization import (QPResult, is_psd, solve_convex_box_qp,
                                   verify_convex_box_qp_result)


class ConvexRecourseError(ValueError):
    pass


def _require(condition, message):
    if not condition:
        raise ConvexRecourseError(message)


def _structure(problem, blocks, bags=None, edges=None):
    n = len(problem.b)
    blocks = tuple(tuple(block) for block in blocks)
    private = set()
    for block in blocks:
        _require(block and len(set(block)) == len(block) and all(
            type(i) is int and 0 <= i < n for i in block), "invalid private block")
        _require(not private.intersection(block), "private blocks overlap")
        _require(not problem.integers.intersection(block), "private blocks must be continuous")
        private.update(block)
        _require(is_psd([[problem.A[i][j] for j in block] for i in block]),
                 "private Hessian is not positive semidefinite")
    retained = tuple(i for i in range(n) if i not in private)
    index = {i: j for j, i in enumerate(retained)}
    attachments = []
    for block in blocks:
        _require(all(not problem.A[i][j] for i in block for j in private
                     if j not in block), "different private blocks interact")
        attachments.append(tuple(index[j] for j in retained
                                 if any(problem.A[i][j] for i in block)))
    pairs = tuple((index[i], index[j], problem.A[i][j]) for i in retained
                  for j in retained if i < j and problem.A[i][j])
    scopes = list(attachments) + [(i, j) for i, j, _ in pairs]
    _require((bags is None) == (edges is None), "supply both residual bags and edges")
    if bags is None:
        decomposition = build_decomposition(len(retained), scopes)
        bags, edges = decomposition["bags"], decomposition["edges"]
    layout = prepare_tree(bags, edges, len(retained))
    _require(all(any(set(scope) <= set(bag) for bag in layout.bags)
                 for scope in scopes), "residual factor scope is not covered")
    homes = tuple(next(u for u, bag in enumerate(layout.bags)
                       if set(scope) <= set(bag)) for scope in attachments)
    pair_homes = tuple(next(u for u, bag in enumerate(layout.bags)
                            if i in bag and j in bag) for i, j, _ in pairs)
    return blocks, retained, tuple(attachments), pairs, homes, pair_homes, layout


def _query_data(problem, block, retained, attachment, values):
    H = tuple(tuple(problem.A[i][j] for j in block) for i in block)
    c = tuple(problem.b[i] + sum((problem.A[i][retained[j]] * value
             for j, value in zip(attachment, values)), F(0)) for i in block)
    return H, c, tuple(problem.bounds[i] for i in block)


def _pack_result(t, values, result):
    return {"block": t, "parameters": list(map(str, values)),
            "point": list(map(str, result.x)), "value": str(result.value),
            "lower_multipliers": list(map(str, result.certificate["lower_multipliers"])),
            "upper_multipliers": list(map(str, result.certificate["upper_multipliers"]))}


def _unpack_result(record):
    return QPResult("optimal", tuple(map(rational, record["point"])),
                    rational(record["value"]), {
                        "lower_multipliers": tuple(map(rational, record["lower_multipliers"])),
                        "upper_multipliers": tuple(map(rational, record["upper_multipliers"]))})


def _grids(problem, retained, bounds, center, h, theta, max_states, budget=None,
           limit_reason="table_limit"):
    grids, penalties = [], []
    for j, i in enumerate(retained):
        lo, hi = bounds[j]
        curvature = max(F(0), problem.A[i][i])
        if not curvature or lo == hi:
            grid = tuple(sorted({lo, hi}))
            radii = (F(0),) * len(grid)
        else:
            grid, radii = coordinate_grid(lo, hi, center[j], h, theta,
                                          i in problem.integers, budget,
                                          max_states, limit_reason)
        if len(grid) > max_states:
            raise BudgetExceeded(limit_reason)
        grids.append(grid)
        penalties.append(tuple(curvature * radius * radius / 8 for radius in radii))
    return tuple(grids), tuple(penalties)


def _tables(problem, structure, grids, penalties, value, check):
    blocks, retained, attachments, pairs, homes, pair_homes, layout = structure
    tables = []
    # Each private block is queried only on its actual attachment scope, not
    # on every state of a larger containing bag.
    factors = []
    for t, attachment in enumerate(attachments):
        factor = {}
        for values in product(*(grids[j] for j in attachment)):
            check()
            factor[values] = value(t, values).value
        factors.append(factor)
    for u, bag in enumerate(layout.bags):
        table = {}
        for state in product(*(range(len(grids[j])) for j in bag)):
            check()
            point = {j: grids[j][k] for j, k in zip(bag, state)}
            cost = problem.constant if u == 0 else F(0)
            for j in bag:
                if layout.home[j] == u:
                    i, z = retained[j], point[j]
                    cost += problem.A[i][i] * z * z / 2 + problem.b[i] * z
                    cost -= penalties[j][state[layout.positions[u][j]]]
            for (i, j, a), home in zip(pairs, pair_homes):
                if home == u:
                    cost += a * point[i] * point[j]
            for attachment, factor, home in zip(attachments, factors, homes):
                if home == u:
                    cost += factor[tuple(point[j] for j in attachment)]
            table[state] = cost
        tables.append(table)
    return tables


def _filter(problem, retained, grids, marginals, upper):
    bounds = []
    for i, grid, row in zip(retained, grids, marginals):
        if len(grid) == 1:
            bounds.append((grid[0], grid[0]))
        else:
            kept = [k for k in range(len(grid) - 1)
                    if min(row[k], row[k + 1]) <= upper]
            _require(kept, "all continuous intervals removed")
            bounds.append((grid[kept[0]], grid[kept[-1] + 1]))
    return tuple(bounds)


def solve_convex_recourse(problem, blocks, epsilon=F(1, 1000), max_levels=32,
                          max_table_states=100000, max_faces=10000,
                          max_pivots=10000, time_limit=30.0, *,
                          residual_bags=None, residual_edges=None, exact=False,
                          grid_mode="geometric"):
    """Optimize a BoxQP by eliminating supplied convex private blocks.

    Residual bags use positions in the ordered retained vector. If omitted,
    scope-preserving min-fill constructs a valid decomposition. Caps produce
    certified incomplete results. Exact mode additionally tries rational
    candidates and accepts only with a rational-height separation proof.
    """
    epsilon = rational(epsilon)
    _require(epsilon >= 0 and type(max_levels) is int and max_levels >= 0 and
             type(max_table_states) is int and max_table_states >= 1 and
             type(max_faces) is int and max_faces >= 0 and
             type(max_pivots) is int and max_pivots >= 0 and time_limit >= 0 and
             type(exact) is bool and grid_mode in ("geometric", "uniform"),
             "invalid accuracy or resource limit")
    budget = Budget(time_limit)
    structure = _structure(problem, blocks, residual_bags, residual_edges)
    blocks, retained, attachments, _, _, _, layout = structure
    bounds = tuple(problem.bounds[i] for i in retained)
    step = max((hi - lo for lo, hi in bounds), default=F(1)) or F(1)
    point = tuple(lo for lo, _ in problem.bounds)
    lower, upper = interval_lower_bound(problem), problem.value(point)
    certificate = {"schema": "convex-recourse-qp-v1", "problem": problem.to_dict(),
                   "blocks": list(map(list, blocks)), "retained": list(retained),
                   "bags": list(map(list, layout.bags)), "edges": list(map(list, layout.edges)),
                   "epsilon": str(epsilon), "exact_requested": exact, "grid_mode": grid_mode,
                   "queries": [], "stages": []}
    cache, total_states, faces, pivots = {}, 0, 0, 0
    status, reason = "level_limit", "max_levels"
    exact_proof = None
    trial, trial_stage, restart = 2, 0, True
    center = tuple(point[i] for i in retained)
    target = epsilon or F(1, 16)
    if exact:
        target = min(target, F(1, 16))
    curvature = max((max(F(0), problem.A[i][i]) for i in retained), default=F(0))

    def stage_cap():
        allowance = 7 * curvature * len(retained) * step ** 2 / 8
        result = 0
        while allowance > target:
            allowance /= 4
            result += 1
        return result

    def check():
        budget.check(force=True)

    def query(t, values):
        nonlocal faces, pivots
        key = (t, values)
        if key not in cache:
            check()
            H, c, box = _query_data(problem, blocks[t], retained, attachments[t], values)
            result = solve_convex_box_qp(H, c, box, max_faces=max_faces,
                                         max_pivots=max_pivots, check=check)
            faces += result.faces
            pivots += result.pivots
            if result.status != "optimal":
                raise BudgetExceeded("oracle_" + result.reason)
            cache[key] = result
            certificate["queries"].append(_pack_result(t, values, result))
        return cache[key]

    def exact_gate(candidate):
        nonlocal point, lower, upper, exact_proof
        from exact_output import rational_heights
        if not problem.feasible(candidate):
            return False
        value = problem.value(candidate)
        if value < upper:
            point, upper = candidate, value
        height = rational_heights(problem)["value"]
        separation = F(1, height * upper.denominator)
        if upper - lower < separation:
            exact_proof = {"lower_before": str(lower), "value_height": str(height),
                           "candidate_value_denominator": str(upper.denominator)}
            lower = upper
            return True
        return False

    try:
        check()
        if lower == upper:
            status, reason = "exact", "coincident_bounds"
        elif not exact and upper - lower <= epsilon:
            status, reason = "certified", "requested_gap"
        else:
            for attempt in range(max_levels):
                check()
                if restart:
                    bounds = tuple(problem.bounds[i] for i in retained)
                    center = tuple(point[i] for i in retained)
                h = step / 2 ** trial_stage
                theta = F(1, 2 ** trial) if grid_mode == "geometric" else F(0)
                cap = min(max_table_states, 100 * 2 ** trial * (len(retained) + 1).bit_length())
                try:
                    grids, penalties = _grids(problem, retained, bounds, center, h, theta, cap,
                        budget, "trial_grid_limit" if cap < max_table_states else "table_limit")
                except BudgetExceeded as exc:
                    if str(exc) != "trial_grid_limit":
                        raise
                    trial, trial_stage, restart = trial + 1, 0, True
                    continue
                states = sum(prod(len(grids[i]) for i in bag) for bag in layout.bags)
                if states > max_table_states:
                    raise BudgetExceeded("table_limit")
                tables = _tables(problem, structure, grids, penalties, query, check)
                dp = solve_tree(layout.bags, layout.edges, tuple(map(len, grids)),
                                tables, layout=layout, check=check)
                z = tuple(grid[k] for grid, k in zip(grids, dp["point_indices"]))
                candidate = list(point)
                for i, value in zip(retained, z):
                    candidate[i] = value
                for t, (block, attachment) in enumerate(zip(blocks, attachments)):
                    result = query(t, tuple(z[j] for j in attachment))
                    for i, value in zip(block, result.x):
                        candidate[i] = value
                candidate = tuple(candidate)
                value = problem.value(candidate)
                correction = sum((penalties[j][k] for j, k in enumerate(dp["point_indices"])), F(0))
                _require(problem.feasible(candidate) and value == dp["lower"] + correction,
                         "conditional lift does not match its finite minimum")
                if value < upper:
                    point, upper = candidate, value
                lower = max(lower, dp["lower"])
                bounds = _filter(problem, retained, grids, dp["marginals"], upper)
                total_states += states
                certificate["stages"].append({"level": len(certificate["stages"]),
                    "h": str(h), "theta": str(theta), "restart": restart,
                    "center": list(map(str, center)), "trial": trial, "trial_stage": trial_stage,
                    "grid_minimum": str(dp["lower"]), "lower": str(lower), "upper": str(upper),
                    "point": list(map(str, point)), "table_states": states})
                center, restart = z, False
                if lower == upper:
                    status, reason = "exact", "coincident_bounds"
                    break
                if exact:
                    from exact_output import _candidates, rational_heights
                    for _, proposed in _candidates(problem, point, rational_heights(problem),
                                                   budget, max_pivots):
                        check()
                        if exact_gate(proposed):
                            status, reason = "exact", "rational_separation"
                            break
                    if status == "exact":
                        break
                elif upper - lower <= epsilon:
                    status, reason = "certified", "requested_gap"
                    break
                if exact and upper - lower <= target:
                    target /= 4
                trial_stage += 1
                if trial_stage > stage_cap():
                    trial, trial_stage, restart = trial + 1, 0, True
    except BudgetExceeded as exc:
        reason = str(exc)
        status = "oracle_limit" if reason.startswith("oracle_") else reason
    certificate.update(status=status, reason=reason, lower=str(lower), upper=str(upper),
                       gap=str(upper - lower), point=list(map(str, point)),
                       exact_proof=exact_proof,
                       stats={"retained_variables": len(retained), "private_variables":
                              sum(map(len, blocks)), "max_bag_size": max(map(len, layout.bags)),
                              "local_qp_queries": len(cache), "local_qp_faces": faces,
                              "local_lp_pivots": pivots, "table_states": total_states,
                              "completed_levels": len(certificate["stages"])})
    return certificate


def verify_convex_recourse(certificate, problem=None, *, max_table_states=1000000):
    """Replay local KKT witnesses and every global bound without QP/LP solves.

    The finite-tree minimizations are recomputed from original model factors.
    Passing problem binds the proof to an expected model, including its input
    decomposition. Returns True or raises ConvexRecourseError.
    """
    try:
        _require(certificate["schema"] == "convex-recourse-qp-v1", "unknown schema")
        embedded = BoxQP.from_dict(certificate["problem"])
        _require(problem is None or problem.to_dict() == embedded.to_dict(), "original model mismatch")
        problem = embedded
        structure = _structure(problem, certificate["blocks"], certificate["bags"], certificate["edges"])
        blocks, retained, attachments, _, _, _, layout = structure
        _require(list(retained) == certificate["retained"], "retained map mismatch")
        epsilon = rational(certificate["epsilon"])
        _require(epsilon >= 0 and type(certificate["exact_requested"]) is bool,
                 "invalid requested accuracy")
        cache = {}
        for record in certificate["queries"]:
            t = record["block"]
            _require(type(t) is int and 0 <= t < len(blocks), "invalid query block")
            values = tuple(map(rational, record["parameters"]))
            _require(len(values) == len(attachments[t]) and all(
                problem.bounds[retained[j]][0] <= value <= problem.bounds[retained[j]][1]
                for j, value in zip(attachments[t], values)), "invalid query parameters")
            key = (t, values)
            _require(key not in cache, "duplicate oracle query")
            H, c, box = _query_data(problem, blocks[t], retained, attachments[t], values)
            result = _unpack_result(record)
            _require(verify_convex_box_qp_result(H, c, box, result), "invalid local KKT certificate")
            cache[key] = result

        def query(t, values):
            _require((t, values) in cache, "missing oracle query")
            return cache[t, values]

        bounds = tuple(problem.bounds[i] for i in retained)
        step = max((hi - lo for lo, hi in bounds), default=F(1)) or F(1)
        point = tuple(lo for lo, _ in problem.bounds)
        lower, upper = interval_lower_bound(problem), problem.value(point)
        stages = certificate["stages"]
        center = tuple(point[i] for i in retained)
        for level, stage in enumerate(stages):
            _require(type(stage["level"]) is int and stage["level"] == level, "invalid level ordering")
            _require(type(stage["restart"]) is bool, "invalid restart flag")
            if stage["restart"]:
                bounds = tuple(problem.bounds[i] for i in retained)
            recorded_center = tuple(map(rational, stage["center"]))
            _require(len(recorded_center) == len(retained) and all(
                lo <= z <= hi and (i not in problem.integers or z.denominator == 1)
                for i, z, (lo, hi) in zip(retained, recorded_center, bounds)), "invalid grid center")
            h, theta = rational(stage["h"]), rational(stage["theta"])
            _require(h > 0 and theta >= 0, "invalid grid scale")
            grids, penalties = _grids(problem, retained, bounds, recorded_center, h, theta,
                                      max_table_states)
            states = sum(prod(len(grids[i]) for i in bag) for bag in layout.bags)
            _require(states <= max_table_states, "verifier table limit")
            tables = _tables(problem, structure, grids, penalties, query, lambda: None)
            dp = solve_tree(layout.bags, layout.edges, tuple(map(len, grids)), tables, layout=layout)
            _require(rational(stage["grid_minimum"]) == dp["lower"] and
                     stage["table_states"] == states,
                     "finite bound or correction mismatch")
            proposed = tuple(map(rational, stage["point"]))
            new_upper = rational(stage["upper"])
            raw_minimizer_value = dp["lower"] + sum(
                (penalties[j][k] for j, k in enumerate(dp["point_indices"])), F(0))
            _require(problem.feasible(proposed) and problem.value(proposed) == new_upper and
                     new_upper <= min(upper, raw_minimizer_value), "invalid stage incumbent")
            point, upper = proposed, new_upper
            lower = max(lower, dp["lower"])
            _require(rational(stage["lower"]) == lower and lower <= upper, "invalid stage lower bound")
            bounds = _filter(problem, retained, grids, dp["marginals"], upper)
        final_point = tuple(map(rational, certificate["point"]))
        final_upper = rational(certificate["upper"])
        _require(problem.feasible(final_point) and problem.value(final_point) == final_upper and
                 final_upper <= upper and lower <= final_upper, "invalid final incumbent")
        proof = certificate["exact_proof"]
        if proof is not None:
            from exact_output import rational_heights
            height = rational_heights(problem)["value"]
            _require(rational(proof["lower_before"]) == lower and
                     int(proof["value_height"]) == height and
                     int(proof["candidate_value_denominator"]) == final_upper.denominator and
                     final_upper - lower < F(1, height * final_upper.denominator),
                     "invalid exact rational separation")
            lower = final_upper
        _require(rational(certificate["lower"]) == lower and
                 rational(certificate["gap"]) == final_upper - lower, "final bounds mismatch")
        status = certificate["status"]
        _require(status in {"exact", "certified", "level_limit", "table_limit", "time_limit", "oracle_limit"},
                 "unknown status")
        if status == "exact":
            _require(lower == final_upper, "unsupported exact status")
        if status == "certified":
            _require(not certificate["exact_requested"] and final_upper - lower <= epsilon,
                     "requested gap not certified")
        return True
    except ConvexRecourseError:
        raise
    except (KeyError, TypeError, ValueError, IndexError, ZeroDivisionError, BudgetExceeded) as exc:
        raise ConvexRecourseError("malformed or oversized convex-recourse certificate") from exc
