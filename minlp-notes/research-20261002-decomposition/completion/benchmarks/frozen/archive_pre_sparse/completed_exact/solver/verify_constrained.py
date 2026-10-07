"""Independent Bellman/history replay for TU constrained-grid certificates.

Shares input, TU/curvature checks and objective evaluation with the model. It
does not call the optimizer, its grid filter, or the finite-tree DP routine.
"""
from fractions import Fraction as F
from itertools import product
from math import prod

from certified_grid import rational
from constrained_grid import ConstrainedQP, height_bound


class CertificateError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise CertificateError(message)


def _optional(value):
    return None if value is None else rational(value)


def verify(certificate, *, max_table_states=100000, max_total_states=10000000,
           max_tu_minors=100000):
    """Return checked status/bounds; raise CertificateError for invalid evidence.

    Limits are local checker policy. They cannot be raised by certificate data.
    A limit result can carry valid completed-stage bounds, or no bounds at all.
    """
    try:
        return _verify(certificate, max_table_states, max_total_states, max_tu_minors)
    except CertificateError:
        raise
    except (ValueError, TypeError, KeyError, IndexError, ZeroDivisionError, OverflowError) as exc:
        raise CertificateError(str(exc)) from exc


def _verify(certificate, max_table_states, max_total_states, max_tu_minors):
    require(certificate["schema"] == "tu-constrained-grid-v1", "unknown constrained certificate schema")
    problem = ConstrainedQP.from_dict(certificate["problem"], max_tu_minors)
    epsilon = rational(certificate["request"]["epsilon"])
    require(epsilon >= 0 and type(certificate["request"]["exact"]) is bool, "invalid request")
    state = tuple(problem.labels[i] if i in problem.labels else problem.bounds[i]
                  for i in range(problem.n))
    lower = upper = None
    incumbent = None
    total_states = 0
    infeasible = False
    neighbors = problem.box.neighbors
    positions = [{i: k for k, i in enumerate(bag)} for bag in problem.bags]
    separators = {(u, v): tuple(sorted(set(problem.bags[u]) & set(problem.bags[v])))
                  for u in range(len(problem.bags)) for v in neighbors[u]}
    for level, stage in enumerate(certificate["stages"]):
        require(not infeasible, "stages after infeasibility")
        require(type(stage["level"]) is int and stage["level"] == level, "missing or reordered stage")
        h = F(1, 2**level)
        grids = tuple(tuple(map(rational, row)) for row in stage["grids"])
        require(len(grids) == problem.n, "wrong grid count")
        sizes = []
        for i in range(problem.n):
            if i in problem.labels:
                expected = tuple(state[i])
            else:
                lo, hi = state[i]
                require((lo/h).denominator == (hi/h).denominator == 1, "unaligned retained bounds")
                count = int((hi-lo)/h) + 1
                require(count <= max_table_states, "coordinate grid budget exceeded")
                expected = tuple(h*k for k in range(int(lo/h), int(hi/h)+1))
            require(grids[i] == expected, "grid differs from retained common mesh")
            sizes.append(len(expected))
        states = sum(prod(sizes[i] for i in bag) for bag in problem.bags)
        require(states <= max_table_states, "stage table budget exceeded")
        total_states += states
        require(total_states <= max_total_states, "total verification budget exceeded")
        require(stage["table_states"] == states, "incorrect table state count")
        messages = {}
        for record in stage["messages"]:
            edge = record["from"], record["to"]
            require(all(type(t) is int for t in edge) and edge in separators and edge not in messages,
                    "invalid or duplicate message direction")
            rows = {}
            for row in record["rows"]:
                indices = tuple(row["indices"])
                require(all(type(i) is int for i in indices) and indices not in rows, "invalid message state")
                rows[indices] = _optional(row["value"])
            expected_keys = set(product(*(range(sizes[i]) for i in separators[edge])))
            require(set(rows) == expected_keys, "missing or excess separator message states")
            messages[edge] = rows
        require(set(messages) == set(separators), "missing directed messages")
        computed = {edge: {key: None for key in rows} for edge, rows in messages.items()}
        marginals = [[None] * sizes[i] for i in range(problem.n)]
        global_value = None
        # For each local assignment, compute the finite sum and infeasible
        # count once. Excluding one incoming message is then constant work.
        for u, bag in enumerate(problem.bags):
            bag_minimum = None
            local_marginals = {i: [None] * sizes[i] for i in bag}
            for indices in product(*(range(sizes[i]) for i in bag)):
                assignment = {i: grids[i][k] for i, k in zip(bag, indices)}
                local = problem.local_value(u, assignment)
                incoming = {}
                finite_sum = F(0) if local is None else local
                bad_count = int(local is None)
                for v in neighbors[u]:
                    key = tuple(indices[positions[u][i]] for i in separators[u, v])
                    value = messages[v, u][key]
                    incoming[v] = value
                    bad_count += int(value is None)
                    if value is not None:
                        finite_sum += value
                for v in neighbors[u]:
                    if bad_count - int(incoming[v] is None):
                        continue
                    value = finite_sum - (incoming[v] if incoming[v] is not None else F(0))
                    key = tuple(indices[positions[u][i]] for i in separators[u, v])
                    previous = computed[u, v][key]
                    if previous is None or value < previous:
                        computed[u, v][key] = value
                if bad_count:
                    continue
                value = finite_sum
                if bag_minimum is None or value < bag_minimum:
                    bag_minimum = value
                for i, index in zip(bag, indices):
                    previous = local_marginals[i][index]
                    if previous is None or value < previous:
                        local_marginals[i][index] = value
            if u == 0:
                global_value = bag_minimum
            else:
                require(bag_minimum == global_value, "inconsistent calibrated bag minimum")
            for i, values in local_marginals.items():
                if problem.box.home[i] == u:
                    marginals[i] = values
                else:
                    # Home is first-containing; this row was already checked.
                    require(marginals[i] == values, "inconsistent repeated-coordinate marginal")
        require(computed == messages, "Bellman recurrence failed")
        if global_value is None:
            require(level == 0 and stage.get("infeasible") is True, "invalid empty-grid claim")
            infeasible = True
            continue
        require(not stage.get("infeasible", False), "false infeasibility claim")
        claimed_marginals = [[_optional(v) for v in row] for row in stage["min_marginals"]]
        require(claimed_marginals == marginals, "incorrect min-marginal")
        point = tuple(map(rational, stage["point"]))
        require(len(point) == problem.n and all(x in grids[i] for i, x in enumerate(point)), "point off grid")
        require(problem.feasible(point) and problem.value(point) == global_value, "invalid attaining grid point")
        require(rational(stage["grid_value"]) == global_value, "incorrect grid value")
        if upper is None or global_value < upper:
            upper, incumbent = global_value, point
        error = len(problem.continuous)*problem.L*h*h/8
        require(rational(stage["error"]) == error, "incorrect TU rounding error")
        lower = max(global_value-error, lower) if lower is not None else global_value-error
        require(rational(stage["lower"]) == lower and rational(stage["upper"]) == upper,
                "incorrect accumulated bounds")
        retained = []
        for i, grid in enumerate(grids):
            good = [v is not None and v-error <= upper for v in marginals[i]]
            if i in problem.labels:
                keep = tuple(v for v, passed in zip(grid, good) if passed)
            elif len(grid) == 1:
                keep = (grid[0], grid[0]) if good[0] else ()
            else:
                intervals = [(grid[k], grid[k+1]) for k in range(len(grid)-1) if good[k] or good[k+1]]
                keep = (intervals[0][0], intervals[-1][1]) if intervals else ()
            require(bool(keep), "empty retained coordinate")
            retained.append(keep)
        state = tuple(retained)
        require(tuple(tuple(map(rational, row)) for row in stage["retained"]) == state,
                "incorrect pruning or omitted original-domain history")
    proof = certificate["exact_proof"]
    if proof is not None:
        require(not infeasible and lower is not None, "exact proof lacks original-domain bound")
        require(proof["kind"] == "rational_separation", "unknown exact proof")
        height = height_bound(problem)
        require(proof["height"] == height, "incorrect original-polytope denominator bound")
        require(rational(proof["comparison_lower"]) == lower, "incorrect exact comparison lower bound")
        point = tuple(map(rational, proof["point"]))
        require(problem.feasible(point), "exact point infeasible")
        value = problem.value(point)
        require(value >= lower and value-lower < F(1, value.denominator*height["V"]),
                "rational separation is not strict enough")
        lower = upper = value
        incumbent = point
    status = certificate["status"]
    require(status in ("exact", "epsilon", "infeasible", "limit"), "invalid final status")
    require((status == "infeasible") == infeasible, "incorrect final infeasibility status")
    if status == "exact":
        require(lower is not None and lower == upper, "exact status without exact bounds")
    elif status == "epsilon":
        require(not certificate["request"]["exact"] and lower is not None and upper-lower <= epsilon,
                "requested gap was not proved")
    if proof is not None:
        require(status == "exact", "exact proof without exact status")
    require(_optional(certificate["lower"]) == lower and _optional(certificate["upper"]) == upper,
            "incorrect final bounds")
    claimed_point = None if certificate["point"] is None else tuple(map(rational, certificate["point"]))
    require(claimed_point == incumbent, "incorrect final incumbent")
    return {"valid": True, "status": status, "lower": None if lower is None else str(lower),
            "upper": None if upper is None else str(upper), "stages": len(certificate["stages"]),
            "total_table_states": total_states}
