"""Certified sparse corrected grids for explicit rational polynomial factors.

The objective is a sum of factors in the monomial basis. Every curvature
constant is derived by exact interval arithmetic on the original box.
Finite table optimization and coordinate geometry are shared with the QP
solver; certificates expose the complete pruning history for independent
replay and boundary-face output.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from math import ceil, floor, prod, isfinite
from time import perf_counter
import argparse
import json
from pathlib import Path

from certified_grid import Budget, BudgetExceeded, coordinate_grid, filtered_bounds, rational
from finite_dp import prepare_tree, solve_tree
from decomposition import build_decomposition


def _power_interval(lo, hi, power):
    if not power:
        return F(1), F(1)
    if power % 2:
        return lo ** power, hi ** power
    return (F(0) if lo <= 0 <= hi else min(lo ** power, hi ** power),
            max(lo ** power, hi ** power))


@dataclass(frozen=True)
class PolynomialFactor:
    scope: object
    terms: object

    def __post_init__(self):
        scope = tuple(self.scope)
        if len(set(scope)) != len(scope) or any(type(i) is not int or i < 0 for i in scope):
            raise ValueError("invalid polynomial factor scope")
        terms = {}
        for term in self.terms:
            if len(term) != 2:
                raise ValueError("terms are (coefficient, exponent tuple) pairs")
            coefficient, powers = rational(term[0]), tuple(term[1])
            if len(powers) != len(scope) or any(type(p) is not int or p < 0 for p in powers):
                raise ValueError("invalid monomial exponents")
            terms[powers] = terms.get(powers, F(0)) + coefficient
        object.__setattr__(self, "scope", scope)
        object.__setattr__(self, "terms", tuple((c, p) for p, c in sorted(terms.items()) if c))

    def value(self, point):
        return sum((coefficient * prod(point[i] ** power for i, power in zip(self.scope, powers))
                    for coefficient, powers in self.terms), F(0))

    def derivative(self, coordinate):
        if coordinate not in self.scope:
            return PolynomialFactor((), ())
        j = self.scope.index(coordinate)
        terms = []
        for coefficient, powers in self.terms:
            if powers[j]:
                reduced = list(powers)
                reduced[j] -= 1
                terms.append((coefficient * powers[j], reduced))
        return PolynomialFactor(self.scope, terms)

    def interval(self, bounds):
        lower, upper = F(0), F(0)
        for coefficient, powers in self.terms:
            lo = hi = coefficient
            for i, power in zip(self.scope, powers):
                a, b = _power_interval(*bounds[i], power)
                endpoints = (lo * a, lo * b, hi * a, hi * b)
                lo, hi = min(endpoints), max(endpoints)
            lower, upper = lower + lo, upper + hi
        return lower, upper

    def to_dict(self):
        return {"scope": list(self.scope),
                "terms": [[str(coefficient), list(powers)] for coefficient, powers in self.terms]}

    @classmethod
    def from_dict(cls, data):
        return cls(data["scope"], data["terms"])


@dataclass
class PolynomialBox:
    bounds: object
    factors: object
    integers: object = ()
    bags: object = None
    edges: object = None
    name: str = "polynomial_box"

    def __post_init__(self):
        raw = tuple(tuple(pair) for pair in self.bounds)
        n = len(raw)
        if not n or any(len(pair) != 2 for pair in raw):
            raise ValueError("a nonempty box requires one endpoint pair per coordinate")
        integers = tuple(self.integers)
        if any(type(i) is not int or not 0 <= i < n for i in integers):
            raise ValueError("invalid integer coordinate")
        self.integers = frozenset(integers)
        bounds = []
        for i, pair in enumerate(raw):
            lo, hi = map(rational, pair)
            if i in self.integers:
                lo, hi = F(ceil(lo)), F(floor(hi))
            if lo > hi:
                raise ValueError("empty coordinate domain")
            bounds.append((lo, hi))
        self.bounds = tuple(bounds)
        self.factors = tuple(self.factors)
        if any(not isinstance(factor, PolynomialFactor) or any(i >= n for i in factor.scope)
               for factor in self.factors):
            raise ValueError("invalid polynomial factor")
        if self.bags is None and self.edges is None:
            layout = build_decomposition(n, (factor.scope for factor in self.factors))
            self.bags, self.edges = layout["bags"], layout["edges"]
        elif self.bags is None or self.edges is None:
            raise ValueError("supply both bags and edges or omit both")
        self.bags = tuple(tuple(bag) for bag in self.bags)
        self.edges = tuple(tuple(edge) for edge in self.edges)
        self.tree_layout = prepare_tree(self.bags, self.edges, n)
        self.home = self.tree_layout.home
        homes = []
        for factor in self.factors:
            containing = [t for t, bag in enumerate(self.bags) if set(factor.scope) <= set(bag)]
            if not containing:
                raise ValueError("factor scope is not covered by a bag")
            homes.append(containing[0])
        self.factor_home = tuple(homes)
        self.n = n
        self.degree = max((sum(powers) for factor in self.factors
                           for coefficient, powers in factor.terms), default=0)

    def value(self, point):
        return sum((factor.value(point) for factor in self.factors), F(0))

    def feasible(self, point, bounds=None):
        bounds = self.bounds if bounds is None else bounds
        return (len(point) == self.n and all(lo <= x <= hi for x, (lo, hi) in zip(point, bounds))
                and all(F(point[i]).denominator == 1 for i in self.integers))

    def derivative_bounds(self, indices=(), bounds=None):
        bounds = self.bounds if bounds is None else bounds
        lower, upper = F(0), F(0)
        for factor in self.factors:
            for i in indices:
                factor = factor.derivative(i)
            lo, hi = factor.interval(bounds)
            lower, upper = lower + lo, upper + hi
        return lower, upper

    def gradient(self, point):
        return tuple(sum((factor.derivative(i).value(point) for factor in self.factors), F(0))
                     for i in range(self.n))

    def hessian(self, point):
        return tuple(tuple(sum((factor.derivative(i).derivative(j).value(point)
                                for factor in self.factors), F(0))
                           for j in range(self.n)) for i in range(self.n))

    def curvature_certificate(self):
        intervals = tuple(self.derivative_bounds((i, i)) for i in range(self.n))
        return {"method": "monomial-interval-v1",
                "box": [[str(lo), str(hi)] for lo, hi in self.bounds],
                "diagonal_bounds": [[str(lo), str(hi)] for lo, hi in intervals],
                "caps": [str(max(F(0), hi)) for lo, hi in intervals]}

    def to_dict(self):
        return {"bounds": [[str(lo), str(hi)] for lo, hi in self.bounds],
                "factors": [factor.to_dict() for factor in self.factors],
                "integers": sorted(self.integers), "bags": list(map(list, self.bags)),
                "edges": list(map(list, self.edges)), "name": self.name}

    @classmethod
    def from_dict(cls, data):
        return cls(data["bounds"], [PolynomialFactor.from_dict(factor) for factor in data["factors"]],
                   data.get("integers", ()), data.get("bags"), data.get("edges"),
                   data.get("name", "polynomial_box"))


def polynomial_grid_dp(problem, grids, penalties, budget=None, max_table_states=100000):
    work = sum(prod(len(grids[i]) for i in bag) for bag in problem.bags)
    if work > max_table_states:
        raise BudgetExceeded("table_limit")
    budget = Budget(float("inf")) if budget is None else budget
    owned = [[factor for factor, home in zip(problem.factors, problem.factor_home) if home == t]
             for t in range(len(problem.bags))]
    tables = []
    for t, bag in enumerate(problem.bags):
        local = {}
        for state in product(*(range(len(grids[i])) for i in bag)):
            budget.check()
            point = {i: grids[i][index] for i, index in zip(bag, state)}
            value = sum((factor.value(point) for factor in owned[t]), F(0))
            value -= sum((penalties[i][index] for i, index in zip(bag, state)
                          if problem.home[i] == t), F(0))
            local[state] = value
        tables.append(local)
    result = solve_tree(problem.bags, problem.edges, tuple(map(len, grids)), tables,
                        home=problem.home, check=budget.check, layout=problem.tree_layout)
    result["point"] = tuple(grids[i][index] for i, index in enumerate(result["point_indices"]))
    return result



def polynomial_filtered_bounds(problem, grids, marginals, upper):
    """Retain continuous cells and actual integer labels, then take each hull."""
    bounds, removed = filtered_bounds(grids, marginals, upper)
    bounds = list(bounds)
    for i in problem.integers:
        grid, row = grids[i], marginals[i]
        kept = [value for value, margin in zip(grid, row) if margin <= upper]
        for k in range(len(grid) - 1):
            if grid[k + 1] - grid[k] > 1 and min(row[k], row[k + 1]) <= upper:
                kept.extend((grid[k] + 1, grid[k + 1] - 1))
        if not kept:
            raise ArithmeticError("integer filtering removed every label")
        bounds[i] = (min(kept), max(kept))
    return tuple(bounds), removed


def solve(problem, epsilon=F(1, 1000), *, max_stages=40, time_limit=10.0,
          max_table_states=100000, theta=F(1, 8), pruning=True,
          schedule="conditioning", grid_mode="geometric", warm_start=None):
    """Return a complete rational bound/pruning certificate, also after limits.

    The conditioning schedule uses capped decreasing-slope trials. Uniform
    grids and adaptive slopes are diagnostic alternatives. All statuses carry
    valid bounds; `certified` means the requested gap was achieved and `exact`
    means a zero gap. Arbitrary-degree input is accepted, without a claim of
    polynomial cost when degree is part of the input.
    """
    epsilon, theta = rational(epsilon), rational(theta)
    if not isinstance(time_limit, (int, float, F)) or isinstance(time_limit, bool):
        raise ValueError("time limit must be a finite nonnegative number")
    try:
        finite_time = isfinite(time_limit)
    except OverflowError:
        finite_time = False
    if not finite_time:
        raise ValueError("time limit must be finite")
    if (epsilon < 0 or not 0 <= theta <= F(1, 4) or type(max_stages) is not int or max_stages < 0
            or type(max_table_states) is not int or max_table_states < 1 or time_limit < 0
            or schedule not in ("conditioning", "adaptive") or grid_mode not in ("geometric", "uniform")
            or type(pruning) is not bool):
        raise ValueError("invalid accuracy, limit, or grid option")
    if not epsilon:
        schedule = "adaptive"
    budget = Budget(time_limit)
    incumbent = tuple(lo for lo, hi in problem.bounds) if warm_start is None else tuple(map(rational, warm_start))
    if not problem.feasible(incumbent):
        raise ValueError("infeasible warm start")
    upper = problem.value(incumbent)
    lower = problem.derivative_bounds()[0]
    curvature = problem.curvature_certificate()
    caps = tuple(map(rational, curvature["caps"]))
    # Feasible proposals affect only the upper bound, and are checked on replay.
    for point in (tuple(hi for lo, hi in problem.bounds), tuple(
            F(floor((lo + hi) / 2)) if i in problem.integers else (lo + hi) / 2
            for i, (lo, hi) in enumerate(problem.bounds))):
        value = problem.value(point)
        if value < upper:
            incumbent, upper = point, value
    certificate = {"schema": "polynomial-grid-v1", "problem": problem.to_dict(),
                   "curvature": curvature,
                   "options": {"epsilon": str(epsilon), "theta": str(theta), "pruning": pruning,
                               "schedule": schedule, "grid_mode": grid_mode},
                   "initial": {"lower": str(lower), "upper": str(upper), "point": list(map(str, incumbent))},
                   "stages": []}
    bounds, center = problem.bounds, incumbent
    scale = max(hi - lo for lo, hi in bounds) or F(1)
    allowance, trial_cap = 7 * max(caps) * problem.n * scale ** 2 / 8, 0
    if epsilon:
        while allowance > epsilon:
            allowance /= 4
            trial_cap += 1
    trial, trial_stage, restart = 2, 0, True
    states, attempted, status = 0, 0, "stage_limit"
    try:
        budget.check(force=True)
        for attempt in range(max_stages):
            if upper - lower <= epsilon:
                break
            budget.check(force=True)
            attempted += 1
            if schedule == "conditioning":
                if restart:
                    bounds, center = problem.bounds, incumbent
                h, slope = scale / 2 ** trial_stage, F(1, 2 ** trial)
                cap = 100 * 2 ** trial * (problem.n + 1).bit_length()
            else:
                h, slope, cap = scale / 2 ** attempt, theta / 2 ** (attempt // 8), max_table_states
            if grid_mode == "uniform":
                slope = F(0)
            try:
                grids, radii = zip(*((tuple(sorted({lo, hi})), (F(0),) * len({lo, hi})) if not caps[i] else
                    coordinate_grid(lo, hi, center[i], h, slope, i in problem.integers,
                                    budget, min(cap, max_table_states),
                                    "trial_grid_limit" if cap < max_table_states else "table_limit")
                    for i, (lo, hi) in enumerate(bounds)))
            except BudgetExceeded as exc:
                if str(exc) != "trial_grid_limit":
                    raise
                trial, trial_stage, restart = trial + 1, 0, True
                continue
            penalties = tuple(tuple(caps[i] * radius ** 2 / 8 for radius in row)
                              for i, row in enumerate(radii))
            result = polynomial_grid_dp(problem, grids, penalties, budget, max_table_states)
            point, value = result["point"], problem.value(result["point"])
            if value < upper:
                incumbent, upper = point, value
            next_bounds, removed = (polynomial_filtered_bounds(problem, grids, result["marginals"], upper)
                                    if pruning else (bounds, 0))
            lower = max(lower, result["lower"])
            certificate["stages"].append({
                "stage": len(certificate["stages"]), "h": str(h), "theta": str(slope),
                "restart": schedule == "conditioning" and restart,
                "trial": trial if schedule == "conditioning" else None,
                "trial_stage": trial_stage if schedule == "conditioning" else None,
                "grids": [list(map(str, row)) for row in grids],
                "messages": [{"from": u, "to": v,
                              "rows": [{"indices": list(key), "value": str(value)} for key, value in sorted(rows.items())]}
                             for (u, v), rows in sorted(result["messages"].items())],
                "min_marginals": [list(map(str, row)) for row in result["marginals"]],
                "grid_point": list(map(str, point)), "grid_lower": str(result["lower"]),
                "incumbent": list(map(str, incumbent)), "upper": str(upper), "lower": str(lower),
                "next_bounds": [[str(lo), str(hi)] for lo, hi in next_bounds],
                "removed_intervals": removed, "table_states": result["table_states"]})
            states += result["table_states"]
            bounds, center, restart = next_bounds, point, False
            if schedule == "conditioning":
                trial_stage += 1
                if trial_stage > trial_cap:
                    trial, trial_stage, restart = trial + 1, 0, True
    except BudgetExceeded as exc:
        status = str(exc)
    # A restart can precede an interrupted stage. The replay domain is the
    # last completed stage's box, not the provisional restarted working box.
    retained = (certificate["stages"][-1]["next_bounds"] if certificate["stages"]
                else [[str(lo), str(hi)] for lo, hi in problem.bounds])
    if upper == lower:
        status = "exact"
    elif upper - lower <= epsilon:
        status = "certified"
    certificate.update(status=status, point=list(map(str, incumbent)), lower=str(lower), upper=str(upper),
                       gap=str(upper - lower), retained_bounds=retained,
                       stats={"elapsed_seconds": perf_counter() - budget.started,
                              "attempted_stages": attempted, "completed_stages": len(certificate["stages"]),
                              "completed_table_states": states, "degree": problem.degree,
                              "max_bag_size": max(map(len, problem.bags))})
    return certificate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("problem", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--epsilon", default="1/1000")
    parser.add_argument("--max-stages", type=int, default=40)
    parser.add_argument("--time-limit", type=float, default=10)
    parser.add_argument("--max-table-states", type=int, default=100000)
    parser.add_argument("--uniform", action="store_true")
    args = parser.parse_args()
    problem = PolynomialBox.from_dict(json.loads(args.problem.read_text()))
    result = solve(problem, args.epsilon, max_stages=args.max_stages, time_limit=args.time_limit,
                   max_table_states=args.max_table_states, grid_mode="uniform" if args.uniform else "geometric")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ("status", "lower", "upper", "gap", "stats")}))


if __name__ == "__main__":
    main()
