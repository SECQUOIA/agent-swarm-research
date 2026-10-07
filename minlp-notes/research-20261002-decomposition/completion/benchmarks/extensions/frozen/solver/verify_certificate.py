"""Replay corrected-grid QP certificates without calling the optimizer.

The verifier shares rational input parsing, decomposition validation, and
objective evaluation with certified_grid. Grid generation, DP, filtering,
initial lower bounds, and PSD/KKT proof checks are independently implemented.
"""

from fractions import Fraction as F
from itertools import product
import argparse
import json
from math import ceil, floor, lcm, prod
from pathlib import Path
import sys

from certified_grid import BoxQP, rational


class CertificateError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise CertificateError(message)


def initial_lower(problem):
    result = problem.constant
    for i, (lo, hi) in enumerate(problem.bounds):
        candidates = [lo, hi]
        a, b = problem.A[i][i], problem.b[i]
        if a > 0:
            vertex = max(lo, min(hi, -b / a))
            candidates.extend([F(floor(vertex)), F(ceil(vertex))]
                              if i in problem.integers else [vertex])
        result += min(a * x * x / 2 + b * x for x in candidates)
    for i in range(len(problem.b)):
        for j in range(i + 1, len(problem.b)):
            if problem.A[i][j]:
                result += min(problem.A[i][j] * x * y
                              for x in problem.bounds[i] for y in problem.bounds[j])
    return result


def check_convex(problem, proof, point):
    n = len(problem.b)
    diagonal = tuple(map(rational, proof["D"]))
    factor = tuple(tuple(map(rational, row)) for row in proof["L"])
    require(len(diagonal) == n and len(factor) == n
            and all(len(row) == n for row in factor), "wrong PSD factor dimensions")
    require(all(d >= 0 for d in diagonal), "negative PSD pivot")
    require(tuple(map(rational, proof["point"])) == point, "inconsistent KKT point")
    for i in range(n):
        for j in range(n):
            require(problem.A[i][j] == sum((factor[i][k] * diagonal[k] * factor[j][k]
                                           for k in range(n)), F(0)), "invalid PSD identity")
        gradient = problem.b[i] + sum((problem.A[i][j] * point[j] for j in range(n)), F(0))
        lo, hi = problem.bounds[i]
        require(not ((lo < point[i] and gradient > 0) or (point[i] < hi and gradient < 0)),
                "KKT sign failure")


def _verify(certificate, max_table_states):
    require(certificate["schema"] == "certified-grid-qp-v1", "unknown certificate schema")
    problem = BoxQP.from_dict(certificate["problem"])
    n = len(problem.b)
    initial = certificate["initial"]
    point = tuple(map(rational, initial["point"]))
    require(problem.feasible(point), "initial point is infeasible")
    upper = problem.value(point)
    require(rational(initial["upper"]) == upper, "incorrect initial upper bound")
    if "convex" in initial:
        check_convex(problem, initial["convex"], point)
        lower = upper
    else:
        lower = initial_lower(problem)
    require(rational(initial["lower"]) == lower, "incorrect initial lower bound")
    bounds = problem.bounds
    total_states = 0
    for number, stage in enumerate(certificate["stages"]):
        require(stage["stage"] == number, "stages out of order")
        if stage.get("restart", False):
            bounds = problem.bounds
        grids = tuple(tuple(map(rational, row)) for row in stage["grids"])
        require(len(grids) == n, "wrong number of coordinate grids")
        penalties = []
        for i, grid in enumerate(grids):
            require(grid and tuple(sorted(set(grid))) == grid, "grid is empty or not strictly sorted")
            require((grid[0], grid[-1]) == bounds[i], "grid does not cover the current domain")
            require(i not in problem.integers or all(x.denominator == 1 for x in grid),
                    "noninteger grid node")
            correction = []
            for k, value in enumerate(grid):
                lengths = []
                if k:
                    lengths.append(value - grid[k - 1])
                if k + 1 < len(grid):
                    lengths.append(grid[k + 1] - value)
                radius = max((length for length in lengths
                              if i not in problem.integers or length > 1), default=F(0))
                correction.append(max(F(0), problem.A[i][i]) * radius ** 2 / 8)
            penalties.append(correction)
        states = sum(prod(len(grids[i]) for i in bag) for bag in problem.bags)
        require(states <= max_table_states, "verification table budget exceeded")
        require(stage["table_states"] == states, "incorrect state count")
        total_states += states
        positions = [{i: k for k, i in enumerate(bag)} for bag in problem.bags]
        separators = {(u, v): tuple(sorted(set(problem.bags[u]) & set(problem.bags[v])))
                      for u, row in enumerate(problem.neighbors) for v in row}
        messages = {}
        for record in stage["messages"]:
            edge = (record["from"], record["to"])
            require(edge in separators and edge not in messages, "invalid or duplicate message edge")
            rows = {}
            for row in record["rows"]:
                state = tuple(row["indices"])
                require(all(type(k) is int for k in state) and state not in rows,
                        "invalid or duplicate message state")
                rows[state] = rational(row["value"])
            expected = set(product(*(range(len(grids[i])) for i in separators[edge])))
            require(set(rows) == expected, "missing or excess separator states")
            messages[edge] = rows
        require(set(messages) == set(separators), "missing directed messages")

        def lookup(u, v, state):
            key = tuple(state[positions[u][i]] for i in separators[u, v])
            return messages[v, u][key]

        tables = []
        for u, bag in enumerate(problem.bags):
            local = {}
            for state in product(*(range(len(grids[i])) for i in bag)):
                assignment = {i: grids[i][state[k]] for k, i in enumerate(bag)}
                value = problem.constant if u == 0 else F(0)
                for i in bag:
                    if next(t for t, other in enumerate(problem.bags) if i in other) == u:
                        x = assignment[i]
                        value += problem.A[i][i] * x * x / 2 + problem.b[i] * x
                        value -= penalties[i][state[positions[u][i]]]
                for i in bag:
                    for j in bag:
                        if i < j and problem.A[i][j] and next(
                                t for t, other in enumerate(problem.bags) if i in other and j in other) == u:
                            value += problem.A[i][j] * assignment[i] * assignment[j]
                local[state] = value
            tables.append(local)
        # Each directed message must satisfy its exact Bellman equality.
        # Tree structure makes these local equations determine the global DP.
        for (u, v), claimed in messages.items():
            computed = {}
            for state, value in tables[u].items():
                value += sum((lookup(u, w, state) for w in problem.neighbors[u] if w != v), F(0))
                key = tuple(state[positions[u][i]] for i in separators[u, v])
                if key not in computed or value < computed[key]:
                    computed[key] = value
            require(computed == claimed, "message Bellman equation failed")
        marginals = [None] * n
        grid_lower = rational(stage["grid_lower"])
        for u, table in enumerate(tables):
            belief = {state: value + sum((lookup(u, v, state) for v in problem.neighbors[u]), F(0))
                      for state, value in table.items()}
            require(min(belief.values()) == grid_lower, "incorrect grid lower bound")
            for i in problem.bags[u]:
                if marginals[i] is not None:
                    continue
                row = [None] * len(grids[i])
                for state, value in belief.items():
                    index = state[positions[u][i]]
                    if row[index] is None or value < row[index]:
                        row[index] = value
                marginals[i] = tuple(row)
        claimed_marginals = tuple(tuple(map(rational, row)) for row in stage["min_marginals"])
        require(tuple(marginals) == claimed_marginals, "incorrect min-marginal")
        grid_point = tuple(map(rational, stage["grid_point"]))
        require(len(grid_point) == n and all(x in grids[i] for i, x in enumerate(grid_point)),
                "grid witness is not on the grid")
        corrected = problem.value(grid_point) - sum(
            (penalties[i][grids[i].index(x)] for i, x in enumerate(grid_point)), F(0))
        require(corrected == grid_lower, "grid witness does not attain its bound")
        point = tuple(map(rational, stage["incumbent"]))
        require(problem.feasible(point), "infeasible incumbent")
        current_upper = problem.value(point)
        require(current_upper == rational(stage["upper"]) and current_upper <= upper,
                "incorrect or increasing upper bound")
        upper = current_upper
        require(grid_lower <= upper, "lower bound exceeds feasible value")
        lower = max(lower, grid_lower)
        require(lower == rational(stage["lower"]), "incorrect cumulative lower bound")
        next_bounds, removed = [], 0
        for grid, row in zip(grids, marginals):
            if len(grid) == 1:
                next_bounds.append((grid[0], grid[0]))
            else:
                retained = [k for k in range(len(grid) - 1) if min(row[k], row[k + 1]) <= upper]
                require(retained, "all intervals removed")
                next_bounds.append((grid[retained[0]], grid[retained[-1] + 1]))
                removed += len(grid) - 1 - len(retained)
        if not certificate["options"]["pruning"]:
            next_bounds, removed = bounds, 0
        require(tuple(tuple(map(rational, pair)) for pair in stage["next_bounds"])
                == tuple(next_bounds), "invalid domain filtering")
        require(stage["removed_intervals"] == removed, "incorrect filtering count")
        bounds = tuple(next_bounds)
    require(rational(certificate["lower"]) == lower and rational(certificate["upper"]) == upper,
            "incorrect final bounds")
    require(tuple(map(rational, certificate["point"])) == point, "incorrect final incumbent")
    require(rational(certificate["gap"]) == upper - lower, "incorrect final gap")
    epsilon = rational(certificate["options"]["epsilon"])
    require(epsilon >= 0, "negative accuracy target")
    require(certificate["status"] in ("certified", "stage_limit", "table_limit", "time_limit"),
            "unknown termination status")
    if certificate["status"] == "certified":
        require(upper - lower <= epsilon, "claimed accuracy is not certified")
    return {"valid": True, "lower": str(lower), "upper": str(upper),
            "gap": str(upper - lower), "stages": len(certificate["stages"]),
            "checked_table_states": total_states}


def _verify_exact(certificate, max_table_states):
    """Check the wrapper using only original bounds and exact rational arithmetic."""
    require(certificate["schema"] == "certified-grid-qp-exact-v1", "unknown exact schema")
    problem = BoxQP.from_dict(certificate["problem"])
    # Independently reproduce the height proof: choose an optimal integer
    # slice and a continuous optimal face of minimum dimension. Its free
    # Hessian is nonsingular. Hadamard bounds every principal determinant.
    denominator = 1
    for value in (problem.constant,) + problem.b + tuple(
            value / 2 for row in problem.A for value in row) + tuple(
            value for bounds in problem.bounds for value in bounds):
        denominator = lcm(denominator, value.denominator)
    continuous = [i for i in range(len(problem.b))
                  if i not in problem.integers and problem.bounds[i][0] < problem.bounds[i][1]]
    determinant = 1
    for i in continuous:
        bound = sum((abs(denominator * problem.A[i][j]) for j in continuous), F(0))
        require(bound.denominator == 1, "height scaling is not integral")
        determinant *= max(1, int(bound))
    coordinate = denominator * determinant
    value_bound = denominator * coordinate ** 2
    expected_heights = {"denominator": denominator, "stationary_det_bound": determinant,
                        "coordinate": coordinate, "value": value_bound}
    require({key: rational(value) for key, value in certificate["heights"].items()}
            == expected_heights, "incorrect rational-height bounds")
    rounds = certificate["rounds"]
    require(isinstance(rounds, list) and rounds, "exact certificate needs a bound proof")
    lower, upper, point, states, stages = None, None, None, 0, 0
    for round_certificate in rounds:
        require(round_certificate["schema"] == "certified-grid-qp-v1", "invalid nested schema")
        other = BoxQP.from_dict(round_certificate["problem"])
        require(other.to_dict() == problem.to_dict(), "bound proof uses a different problem")
        checked = _verify(round_certificate, max_table_states)
        bound, value = rational(checked["lower"]), rational(checked["upper"])
        lower = bound if lower is None else max(lower, bound)
        if upper is None or value < upper:
            upper, point = value, tuple(map(rational, round_certificate["point"]))
        states += checked["checked_table_states"]
        stages += checked["stages"]
    for proposal in certificate.get("feasible_proposals", []):
        require(type(proposal["after_round"]) is int
                and 0 <= proposal["after_round"] < len(rounds), "invalid proposal round")
        candidate = tuple(map(rational, proposal["point"]))
        require(problem.feasible(candidate), "infeasible recovered proposal")
        value = problem.value(candidate)
        if value < upper:
            upper, point = value, candidate
    require(lower <= upper, "inconsistent bound proofs")
    status = certificate["status"]
    require(status in ("exact", "stage_limit", "table_limit", "time_limit", "round_limit"),
            "unknown exact-output status")
    if status == "exact":
        proof = certificate["proof"]
        candidate = tuple(map(rational, proof["point"]))
        require(problem.feasible(candidate), "exact candidate is infeasible")
        value = problem.value(candidate)
        require(value == rational(proof["value"]), "incorrect exact candidate value")
        require(lower <= value <= upper, "candidate contradicts bound proof")
        if proof["kind"] == "equal_bounds":
            require(lower == upper == value, "unequal bounds do not prove exactness")
        else:
            require(proof["kind"] == "rational_value_separation", "unknown exact proof kind")
            # f* has denominator <= V; a distinct rational candidate value
            # with denominator W differs from f* by at least 1/(V W).
            require(value - lower < F(1, value_bound * value.denominator),
                    "rational value separation does not prove exactness")
        lower = upper = value
        point = candidate
    else:
        require("proof" not in certificate, "incomplete result carries an exact proof")
    require(rational(certificate["lower"]) == lower and rational(certificate["upper"]) == upper,
            "incorrect final exact-output bounds")
    final_point = tuple(map(rational, certificate["point"]))
    require(problem.feasible(final_point) and problem.value(final_point) == upper,
            "incorrect final exact-output point")
    require(rational(certificate["gap"]) == upper - lower, "incorrect final exact-output gap")
    return {"valid": True, "exact": status == "exact", "lower": str(lower),
            "upper": str(upper), "gap": str(upper - lower), "stages": stages,
            "rounds": len(rounds), "checked_table_states": states}


def verify_certificate(certificate, max_table_states=1000000):
    try:
        if certificate["schema"] == "certified-grid-qp-exact-v1":
            return _verify_exact(certificate, max_table_states)
        return _verify(certificate, max_table_states)
    except CertificateError:
        raise
    except (ValueError, KeyError, TypeError, IndexError, ZeroDivisionError, StopIteration) as exc:
        raise CertificateError(f"malformed certificate: {exc}") from exc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--max-table-states", type=int, default=1000000)
    args = parser.parse_args()
    try:
        result = verify_certificate(json.loads(args.certificate.read_text()), args.max_table_states)
    except (CertificateError, OSError, json.JSONDecodeError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
