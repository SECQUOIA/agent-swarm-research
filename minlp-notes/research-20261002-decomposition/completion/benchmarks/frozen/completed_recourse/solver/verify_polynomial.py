"""Independent Bellman and interval-arithmetic replay of polynomial grids.

Shares input parsing and exact objective evaluation, but does not call grid
construction, the optimizer, its derivative bounds, or finite_dp.solve_tree.
"""

from fractions import Fraction as F
from itertools import product
from math import prod, lcm
import argparse
import json
from pathlib import Path

from certified_grid import rational
from polynomial_grid import PolynomialBox
from verify_certificate import CertificateError


def require(condition, message):
    if not condition:
        raise CertificateError(message)


def polynomial_interval(problem, bounds, derivatives=()):
    """Direct monomial calculation, independently of the model derivative API."""
    low, high = F(0), F(0)
    for factor in problem.factors:
        for coefficient, original_powers in factor.terms:
            powers, coefficient = list(original_powers), F(coefficient)
            for coordinate in derivatives:
                if coordinate not in factor.scope:
                    coefficient = F(0)
                    break
                position = factor.scope.index(coordinate)
                coefficient *= powers[position]
                if not coefficient:
                    break
                powers[position] -= 1
            if not coefficient:
                continue
            a = b = F(1)
            for coordinate, power in zip(factor.scope, powers):
                left, right = bounds[coordinate]
                if not power:
                    c = d = F(1)
                elif power % 2:
                    c, d = left ** power, right ** power
                else:
                    c = F(0) if left <= 0 <= right else min(left ** power, right ** power)
                    d = max(left ** power, right ** power)
                endpoints = (a * c, a * d, b * c, b * d)
                a, b = min(endpoints), max(endpoints)
            low += min(coefficient * a, coefficient * b)
            high += max(coefficient * a, coefficient * b)
    return low, high


def _verify(certificate, max_table_states, check):
    check()
    require(certificate["schema"] == "polynomial-grid-v1", "unknown polynomial certificate schema")
    problem = PolynomialBox.from_dict(certificate["problem"])
    n, layout = problem.n, problem.tree_layout
    curvature = certificate["curvature"]
    require(curvature["method"] == "monomial-interval-v1", "unknown curvature proof")
    require(tuple(tuple(map(rational, pair)) for pair in curvature["box"]) == problem.bounds,
            "curvature bound uses a different box")
    intervals = tuple(polynomial_interval(problem, problem.bounds, (i, i)) for i in range(n))
    require(tuple(tuple(map(rational, pair)) for pair in curvature["diagonal_bounds"]) == intervals,
            "incorrect derivative interval bounds")
    caps = tuple(max(F(0), hi) for lo, hi in intervals)
    require(tuple(map(rational, curvature["caps"])) == caps, "invalid curvature caps")
    require(type(certificate["options"]["pruning"]) is bool, "invalid pruning option")
    initial = certificate["initial"]
    point = tuple(map(rational, initial["point"]))
    require(problem.feasible(point), "infeasible initial point")
    upper = problem.value(point)
    lower = polynomial_interval(problem, problem.bounds)[0]
    require(rational(initial["upper"]) == upper and rational(initial["lower"]) == lower,
            "incorrect initial bounds")
    bounds, total_states = problem.bounds, 0
    for number, stage in enumerate(certificate["stages"]):
        check()
        require(type(stage["stage"]) is int and stage["stage"] == number, "stages out of order")
        require(type(stage["restart"]) is bool, "invalid restart marker")
        if stage["restart"]:
            bounds = problem.bounds
        grids = tuple(tuple(map(rational, row)) for row in stage["grids"])
        require(len(grids) == n, "wrong number of coordinate grids")
        penalties = []
        for i, grid in enumerate(grids):
            require(grid and tuple(sorted(set(grid))) == grid, "grid must be nonempty and strictly sorted")
            require((grid[0], grid[-1]) == bounds[i], "grid does not cover the retained domain")
            require(i not in problem.integers or all(x.denominator == 1 for x in grid), "fractional integer node")
            row = []
            for k in range(len(grid)):
                lengths = ([grid[k] - grid[k - 1]] if k else [])
                if k + 1 < len(grid):
                    lengths.append(grid[k + 1] - grid[k])
                radius = max((d for d in lengths if i not in problem.integers or d > 1), default=F(0))
                row.append(caps[i] * radius ** 2 / 8)
            penalties.append(row)
        work = sum(prod(len(grids[i]) for i in bag) for bag in problem.bags)
        require(work <= max_table_states, "verification table budget exceeded")
        require(type(stage["table_states"]) is int and stage["table_states"] == work, "incorrect table size")
        total_states += work
        messages = {}
        for record in stage["messages"]:
            edge = (record["from"], record["to"])
            require(all(type(u) is int for u in edge) and edge in layout.separators and edge not in messages,
                    "invalid or duplicate directed message")
            rows = {}
            for row in record["rows"]:
                key = tuple(row["indices"])
                require(all(type(k) is int for k in key) and key not in rows, "invalid message state")
                rows[key] = rational(row["value"])
            expected = set(product(*(range(len(grids[i])) for i in layout.separators[edge])))
            require(set(rows) == expected, "message omits or adds separator states")
            messages[edge] = rows
        require(set(messages) == set(layout.separators), "missing directed messages")

        def incoming(u, v, state):
            return messages[v, u][tuple(state[layout.positions[u][i]] for i in layout.separators[u, v])]

        tables = []
        for u, bag in enumerate(problem.bags):
            local = {}
            for state in product(*(range(len(grids[i])) for i in bag)):
                check()
                assignment = {i: grids[i][k] for i, k in zip(bag, state)}
                value = sum((factor.value(assignment) for factor in problem.factors
                             if next(t for t, other in enumerate(problem.bags)
                                     if set(factor.scope) <= set(other)) == u), F(0))
                value -= sum((penalties[i][k] for i, k in zip(bag, state)
                              if next(t for t, other in enumerate(problem.bags) if i in other) == u), F(0))
                local[state] = value
            tables.append(local)
        for (u, v), claimed in messages.items():
            computed = {}
            for state, value in tables[u].items():
                check()
                value += sum((incoming(u, w, state) for w in layout.neighbors[u] if w != v), F(0))
                key = tuple(state[layout.positions[u][i]] for i in layout.separators[u, v])
                if key not in computed or value < computed[key]:
                    computed[key] = value
            require(computed == claimed, "message Bellman equality failed")
        grid_lower = rational(stage["grid_lower"])
        marginals = [None] * n
        for u, table in enumerate(tables):
            beliefs = {state: value + sum((incoming(u, v, state) for v in layout.neighbors[u]), F(0))
                       for state, value in table.items()}
            require(min(beliefs.values()) == grid_lower, "incorrect grid lower bound")
            for i in problem.bags[u]:
                if marginals[i] is not None:
                    continue
                row = [None] * len(grids[i])
                for state, value in beliefs.items():
                    k = state[layout.positions[u][i]]
                    if row[k] is None or value < row[k]:
                        row[k] = value
                marginals[i] = tuple(row)
        require(tuple(marginals) == tuple(tuple(map(rational, row)) for row in stage["min_marginals"]),
                "incorrect min-marginals")
        grid_point = tuple(map(rational, stage["grid_point"]))
        require(len(grid_point) == n and all(x in grids[i] for i, x in enumerate(grid_point)), "invalid grid witness")
        corrected = problem.value(grid_point) - sum((penalties[i][grids[i].index(x)]
                                                     for i, x in enumerate(grid_point)), F(0))
        require(corrected == grid_lower, "grid witness does not attain the claimed bound")
        point = tuple(map(rational, stage["incumbent"]))
        require(problem.feasible(point), "infeasible incumbent")
        value = problem.value(point)
        require(value <= upper and value == rational(stage["upper"]), "incorrect or increasing upper bound")
        upper, lower = value, max(lower, grid_lower)
        require(grid_lower <= upper and rational(stage["lower"]) == lower, "incorrect cumulative lower bound")
        retained, removed = [], 0
        for coordinate, (grid, row) in enumerate(zip(grids, marginals)):
            if len(grid) == 1:
                retained.append((grid[0], grid[0]))
            else:
                keep = [k for k in range(len(grid) - 1) if min(row[k], row[k + 1]) <= upper]
                require(keep, "all intervals were removed")
                retained.append((grid[keep[0]], grid[keep[-1] + 1]))
                removed += len(grid) - 1 - len(keep)
            if coordinate in problem.integers:
                labels = [x for x, margin in zip(grid, row) if margin <= upper]
                for k in range(len(grid) - 1):
                    if grid[k + 1] - grid[k] >= 2 and min(row[k], row[k + 1]) <= upper:
                        labels.extend([grid[k] + 1, grid[k + 1] - 1])
                require(labels, "all integer labels removed")
                retained[-1] = (min(labels), max(labels))
        if not certificate["options"]["pruning"]:
            retained, removed = bounds, 0
        require(tuple(tuple(map(rational, pair)) for pair in stage["next_bounds"]) == tuple(retained),
                "incorrect retained domain")
        require(type(stage["removed_intervals"]) is int and stage["removed_intervals"] == removed,
                "incorrect filtering count")
        bounds = tuple(retained)
    require(tuple(tuple(map(rational, pair)) for pair in certificate["retained_bounds"]) == bounds,
            "incorrect final retained box")
    if "integer_lattice" in certificate:
        require(all(i in problem.integers or lo == hi for i, (lo, hi) in enumerate(problem.bounds)),
                "integer lattice proof has a varying continuous coordinate")
        denominator = 1
        for factor in problem.factors:
            for coefficient, powers in factor.terms:
                substituted = F(coefficient)
                for i, exponent in zip(factor.scope, powers):
                    if problem.bounds[i][0] == problem.bounds[i][1]:
                        substituted *= problem.bounds[i][0] ** exponent
                denominator = lcm(denominator, substituted.denominator)
        lattice = certificate["integer_lattice"]
        require(type(lattice["denominator"]) is int and lattice["denominator"] == denominator,
                "incorrect integer value-lattice denominator")
        require(rational(lattice["lower_before"]) == lower, "incorrect pre-lattice lower bound")
        require(0 <= upper - lower < F(1, denominator), "integer value separation is insufficient")
        lower = upper
    require(rational(certificate["lower"]) == lower and rational(certificate["upper"]) == upper,
            "incorrect final bounds")
    require(tuple(map(rational, certificate["point"])) == point, "incorrect final point")
    require(rational(certificate["gap"]) == upper - lower, "incorrect final gap")
    epsilon = rational(certificate["options"]["epsilon"])
    require(epsilon >= 0, "negative accuracy target")
    status = certificate["status"]
    require(status in ("exact", "certified", "stage_limit", "table_limit", "time_limit"), "invalid termination status")
    if status == "exact":
        require(upper == lower, "exact output requires a zero gap")
    if status == "certified":
        require(upper - lower <= epsilon, "uncertified accuracy claim")
    return {"valid": True, "lower": str(lower), "upper": str(upper), "gap": str(upper - lower),
            "retained_bounds": [[str(lo), str(hi)] for lo, hi in bounds],
            "stages": len(certificate["stages"]), "checked_table_states": total_states}


def verify_polynomial(certificate, max_table_states=1000000, *, check=None, expected_problem=None):
    if type(max_table_states) is not int or max_table_states < 1:
        raise CertificateError("invalid verification table budget")
    try:
        if expected_problem is not None:
            require(isinstance(expected_problem, PolynomialBox), "invalid expected polynomial model")
            require(PolynomialBox.from_dict(certificate["problem"]).to_dict() == expected_problem.to_dict(),
                    "certificate describes a different problem")
        return _verify(certificate, max_table_states, (lambda: None) if check is None else check)
    except CertificateError:
        raise
    except (KeyError, TypeError, ValueError, IndexError, ArithmeticError, AttributeError) as exc:
        raise CertificateError("malformed polynomial certificate: " + str(exc)) from exc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--max-table-states", type=int, default=1000000)
    args = parser.parse_args()
    print(json.dumps(verify_polynomial(json.loads(args.certificate.read_text()), args.max_table_states)))


if __name__ == "__main__":
    main()
