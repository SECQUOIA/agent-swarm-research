"""Exact corrected-grid bounds and min-marginal filtering for sparse box QP.

Objective: constant + b'x + x'Ax/2, with rational data and symmetric A.
Only Python's standard library is required. See README.md for the certificate
contract, the convergence schedule, and the scope of the implementation.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
import json
from math import ceil, floor, prod
from pathlib import Path
from time import perf_counter

from finite_dp import prepare_tree, solve_tree


def rational(value):
    if isinstance(value, bool) or not isinstance(value, (str, int, F)):
        raise ValueError("rational data must be integers, strings, or Fractions")
    try:
        return F(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("invalid rational number") from exc


@dataclass
class BoxQP:
    A: object
    b: object
    bounds: object
    integers: object
    bags: object = None
    edges: object = None
    constant: object = 0
    name: str = "box_qp"

    def __post_init__(self):
        self.b = tuple(map(rational, self.b))
        self.A = tuple(tuple(map(rational, row)) for row in self.A)
        self.constant = rational(self.constant)
        n = len(self.b)
        if n == 0 or len(self.A) != n or any(len(row) != n for row in self.A):
            raise ValueError("A must be a nonempty square matrix matching b")
        if any(self.A[i][j] != self.A[j][i] for i in range(n) for j in range(n)):
            raise ValueError("A must be symmetric")
        self.integers = tuple(self.integers)
        if any(type(i) is not int or not 0 <= i < n for i in self.integers):
            raise ValueError("invalid integer coordinate")
        self.integers = frozenset(self.integers)
        self.bounds = tuple(tuple(pair) for pair in self.bounds)
        if len(self.bounds) != n or any(len(pair) != 2 for pair in self.bounds):
            raise ValueError("bounds must have one endpoint pair per coordinate")
        bounds = []
        for i, pair in enumerate(self.bounds):
            lo, hi = map(rational, pair)
            if i in self.integers:
                lo, hi = F(ceil(lo)), F(floor(hi))
            if lo > hi:
                raise ValueError("empty coordinate domain")
            bounds.append((lo, hi))
        self.bounds = tuple(bounds)
        if self.bags is None and self.edges is None:
            from decomposition import decompose_qp
            generated = decompose_qp(self.A)
            self.bags, self.edges = generated["bags"], generated["edges"]
        elif self.bags is None or self.edges is None:
            raise ValueError("supply both decomposition bags and edges, or omit both")
        self.bags = tuple(tuple(bag) for bag in self.bags)
        self.edges = tuple(tuple(edge) for edge in self.edges)
        self.neighbors, self.parents, self.order = self._validate_decomposition()
        self.tree_layout = prepare_tree(self.bags, self.edges, n)
        self.home = tuple(next(t for t, bag in enumerate(self.bags) if i in bag)
                          for i in range(n))
        self.interactions = tuple((i, j, self.A[i][j])
                                  for i in range(n) for j in range(i + 1, n)
                                  if self.A[i][j])
        self.factor_home = tuple(next(t for t, bag in enumerate(self.bags)
                                      if i in bag and j in bag)
                                 for i, j, _ in self.interactions)
        adjacency = [[] for _ in range(n)]
        for i, j, coefficient in self.interactions:
            adjacency[i].append((j, coefficient))
            adjacency[j].append((i, coefficient))
        self.adjacency = tuple(tuple(row) for row in adjacency)

    def _validate_decomposition(self):
        n, count = len(self.b), len(self.bags)
        if not count:
            raise ValueError("a decomposition must contain a bag")
        for bag in self.bags:
            if len(set(bag)) != len(bag) or any(
                    type(i) is not int or not 0 <= i < n for i in bag):
                raise ValueError("invalid bag")
        if len(self.edges) != count - 1:
            raise ValueError("decomposition edges must form a tree")
        neighbors = [[] for _ in self.bags]
        seen_edges = set()
        for edge in self.edges:
            if len(edge) != 2 or any(type(t) is not int or not 0 <= t < count
                                     for t in edge):
                raise ValueError("invalid decomposition edge")
            u, v = edge
            canonical = tuple(sorted(edge))
            if u == v or canonical in seen_edges:
                raise ValueError("decomposition edges must form a simple tree")
            seen_edges.add(canonical)
            neighbors[u].append(v)
            neighbors[v].append(u)
        parents, order = {0: None}, [0]
        for u in order:
            for v in neighbors[u]:
                if v not in parents:
                    parents[v] = u
                    order.append(v)
        if len(order) != count:
            raise ValueError("decomposition tree is disconnected")
        for i in range(n):
            containing = {t for t, bag in enumerate(self.bags) if i in bag}
            if not containing:
                raise ValueError("a coordinate is missing from all bags")
            reached = {next(iter(containing))}
            pending = list(reached)
            for u in pending:
                for v in neighbors[u]:
                    if v in containing and v not in reached:
                        reached.add(v)
                        pending.append(v)
            if reached != containing:
                raise ValueError("decomposition violates running intersection")
        for i in range(n):
            for j in range(i + 1, n):
                if self.A[i][j] and not any(i in bag and j in bag for bag in self.bags):
                    raise ValueError("a quadratic interaction is not covered")
        return neighbors, parents, order

    def value(self, point):
        return self.constant + sum((self.A[i][i] * point[i] ** 2 / 2
                                    + self.b[i] * point[i]
                                    for i in range(len(self.b))), F(0)) + sum(
            (a * point[i] * point[j] for i, j, a in self.interactions), F(0))

    def feasible(self, point, bounds=None):
        bounds = self.bounds if bounds is None else bounds
        return (len(point) == len(self.b)
                and all(lo <= point[i] <= hi for i, (lo, hi) in enumerate(bounds))
                and all(point[i].denominator == 1 for i in self.integers))

    def to_dict(self):
        return {"A": [[str(v) for v in row] for row in self.A],
                "b": list(map(str, self.b)),
                "bounds": [[str(lo), str(hi)] for lo, hi in self.bounds],
                "integers": sorted(self.integers),
                "bags": list(map(list, self.bags)), "edges": list(map(list, self.edges)),
                "constant": str(self.constant), "name": self.name}

    @classmethod
    def from_dict(cls, data):
        return cls(**{key: data[key] for key in
                      ("A", "b", "bounds", "integers")},
                   bags=data.get("bags"), edges=data.get("edges"),
                   constant=data.get("constant", 0), name=data.get("name", "box_qp"))


class BudgetExceeded(Exception):
    pass


class Budget:
    def __init__(self, seconds):
        self.started = perf_counter()
        self.seconds = seconds
        self.ticks = 0

    def check(self, force=False):
        self.ticks += 1
        if (force or self.ticks % 128 == 0) and perf_counter() - self.started >= self.seconds:
            raise BudgetExceeded("time_limit")


def unary_minimum(a, b, lo, hi, integer=False):
    candidates = [lo, hi]
    if a > 0:
        vertex = min(hi, max(lo, -b / a))
        candidates.extend((F(floor(vertex)), F(ceil(vertex))) if integer else (vertex,))
    return min(candidates, key=lambda x: a * x * x / 2 + b * x)


def interval_lower_bound(problem):
    """Exact independent-factor bound, also available before any DP completes."""
    result = problem.constant
    for i, (lo, hi) in enumerate(problem.bounds):
        x = unary_minimum(problem.A[i][i], problem.b[i], lo, hi, i in problem.integers)
        result += problem.A[i][i] * x * x / 2 + problem.b[i] * x
    for i, j, a in problem.interactions:
        result += min(a * x * y for x in problem.bounds[i] for y in problem.bounds[j])
    return result


def polish(problem, point, bounds, sweeps, budget):
    """Feasible exact coordinate descent; no lower-bound claim is made."""
    point = list(point)
    for _ in range(sweeps):
        changed = False
        for i, (lo, hi) in enumerate(bounds):
            budget.check()
            linear = problem.b[i] + sum((coefficient * point[j]
                                        for j, coefficient in problem.adjacency[i]), F(0))
            new = unary_minimum(problem.A[i][i], linear, lo, hi, i in problem.integers)
            changed |= new != point[i]
            point[i] = new
        if not changed:
            break
    return tuple(point)


def convex_certificate(problem, point, budget):
    """Try an exact PSD factorization and a rational KKT point on its active face.

    This bounded presolve handles small convex instances. Failure makes no
    nonconvexity claim; singular systems and an incorrect active face may fail.
    """
    n = len(point)
    if n > 64:
        return None
    matrix = [list(row) for row in problem.A]
    factor = [[F(i == j) for j in range(n)] for i in range(n)]
    diagonal = []
    for k in range(n):
        budget.check(force=True)
        pivot = matrix[k][k]
        if pivot < 0 or (pivot == 0 and any(matrix[i][k] for i in range(k + 1, n))):
            return None
        diagonal.append(pivot)
        if not pivot:
            continue
        for i in range(k + 1, n):
            factor[i][k] = matrix[i][k] / pivot
            for j in range(k + 1, i + 1):
                matrix[i][j] -= factor[i][k] * matrix[j][k]
                matrix[j][i] = matrix[i][j]
    free = [i for i, (lo, hi) in enumerate(problem.bounds) if lo < point[i] < hi]
    fixed = [i for i in range(n) if i not in free]
    system = [[problem.A[i][j] for j in free] + [
        -problem.b[i] - sum((problem.A[i][j] * point[j] for j in fixed), F(0))]
        for i in free]
    pivots, row = [], 0
    for column in range(len(free)):
        budget.check(force=True)
        pivot = next((r for r in range(row, len(free)) if system[r][column]), None)
        if pivot is None:
            continue
        system[row], system[pivot] = system[pivot], system[row]
        divisor = system[row][column]
        system[row] = [x / divisor for x in system[row]]
        for r in range(len(free)):
            if r != row and system[r][column]:
                multiple = system[r][column]
                system[r] = [x - multiple * y for x, y in zip(system[r], system[row])]
        pivots.append((row, column))
        row += 1
    if any(not any(line[:-1]) and line[-1] for line in system):
        return None
    candidate = list(point)
    for i in free:
        candidate[i] = F(0)
    for r, column in pivots:
        candidate[free[column]] = system[r][-1]
    candidate = tuple(candidate)
    if not problem.feasible(candidate):
        return None
    for i, (lo, hi) in enumerate(problem.bounds):
        gradient = problem.b[i] + problem.A[i][i] * candidate[i] + sum(
            (coefficient * candidate[j] for j, coefficient in problem.adjacency[i]), F(0))
        if ((lo < candidate[i] and gradient > 0)
                or (candidate[i] < hi and gradient < 0)):
            return None
    return {"point": list(map(str, candidate)),
            "L": [list(map(str, row)) for row in factor], "D": list(map(str, diagonal))}


def coordinate_grid(lo, hi, center, h, theta, integer, budget=None, max_nodes=100000,
                    limit_reason="table_limit"):
    if not (lo <= center <= hi and h > 0 and theta >= 0):
        raise ValueError("invalid grid parameters")
    nodes = {lo, hi, center}
    for endpoint, sign in ((lo, -1), (hi, 1)):
        point = center
        while point != endpoint:
            if budget is not None:
                budget.check()
            step = h + theta * abs(point - center)
            if integer:
                step = F(max(1, floor(step)))
            point += sign * min(step, abs(endpoint - point))
            nodes.add(point)
            if len(nodes) > max_nodes:
                raise BudgetExceeded(limit_reason)
    nodes = tuple(sorted(nodes))
    radii = []
    for k, node in enumerate(nodes):
        adjacent = []
        if k:
            adjacent.append(node - nodes[k - 1])
        if k + 1 < len(nodes):
            adjacent.append(nodes[k + 1] - node)
        radii.append(max((d for d in adjacent if not integer or d > 1), default=F(0)))
    return nodes, tuple(radii)


def grid_dp(problem, grids, penalties, budget=None, max_table_states=100000):
    """Return exact minimum, witness, unary min-marginals and directed messages."""
    work = sum(prod(len(grids[i]) for i in bag) for bag in problem.bags)
    if work > max_table_states:
        raise BudgetExceeded("table_limit")
    if budget is None:
        budget = Budget(float("inf"))
    positions = problem.tree_layout.positions
    unaries = [[i for i, home in enumerate(problem.home) if home == t]
               for t in range(len(problem.bags))]
    pairs = [[factor for factor, home in zip(problem.interactions, problem.factor_home)
              if home == t] for t in range(len(problem.bags))]
    tables = []
    for t, bag in enumerate(problem.bags):
        # Precompute factors before the Cartesian product: rational products
        # otherwise dominate even on branching trees with very small bags.
        unary = {i: tuple(problem.A[i][i] * x * x / 2 + problem.b[i] * x - d
                          for x, d in zip(grids[i], penalties[i])) for i in unaries[t]}
        pair = {(i, j): tuple(tuple(a * x * y for y in grids[j]) for x in grids[i])
                for i, j, a in pairs[t]}
        local = {}
        for state in product(*(range(len(grids[i])) for i in bag)):
            budget.check()
            cost = problem.constant if t == 0 else F(0)
            cost += sum((row[state[positions[t][i]]] for i, row in unary.items()), F(0))
            cost += sum((row[state[positions[t][i]]][state[positions[t][j]]]
                         for (i, j), row in pair.items()), F(0))
            local[state] = cost
        tables.append(local)
    result = solve_tree(problem.bags, problem.edges, tuple(map(len, grids)), tables,
                        home=problem.home, check=budget.check, layout=problem.tree_layout)
    point = tuple(grids[i][k] for i, k in enumerate(result["point_indices"]))
    return {"lower": result["lower"], "point": point,
            "marginals": result["marginals"], "messages": result["messages"],
            "table_states": result["table_states"]}


def filtered_bounds(grids, marginals, upper):
    bounds, removed = [], 0
    for grid, row in zip(grids, marginals):
        if len(grid) == 1:
            bounds.append((grid[0], grid[0]))
            continue
        keep = [k for k in range(len(grid) - 1) if min(row[k], row[k + 1]) <= upper]
        if not keep:
            raise ArithmeticError("all intervals removed by an invalid bound")
        bounds.append((grid[keep[0]], grid[keep[-1] + 1]))
        removed += len(grid) - 1 - len(keep)
    return tuple(bounds), removed


def solve(problem, epsilon=F(1, 1000), max_stages=24, time_limit=10.0,
          max_table_states=100000, theta=F(1, 8), pruning=True,
          grid_mode="geometric", polish_sweeps=2, slope_decay_period=8,
          convex_presolve=True, schedule="conditioning", warm_start=None):
    """Produce a replayable certificate, including after any explicit limit.

    Default conditioning trials restart from the original box, using slopes
    2^-mu for mu=2,3,..., the proved coordinate cap, and a fixed accuracy-based
    stage cap. ``max_stages`` caps total attempted stages across all trials.
    The optional adaptive schedule halves theta every slope_decay_period
    stages; period=0 keeps its slope fixed. Uniform mode uses slope zero.
    This function certifies an accuracy target; use exact_output.solve_exact
    for rational-height exact recovery. Here epsilon=0 uses the adaptive
    schedule. No growth constant or optimizer is supplied.
    """
    epsilon, theta = rational(epsilon), rational(theta)
    if epsilon < 0 or not 0 <= theta <= F(1, 4):
        raise ValueError("epsilon must be nonnegative and theta in [0,1/4]")
    if (type(max_stages) is not int or max_stages < 0 or time_limit < 0
            or type(max_table_states) is not int or max_table_states < 1
            or type(polish_sweeps) is not int or polish_sweeps < 0
            or type(slope_decay_period) is not int or slope_decay_period < 0
            or grid_mode not in ("geometric", "uniform")
            or schedule not in ("conditioning", "adaptive")):
        raise ValueError("invalid solver limit or grid mode")
    if not epsilon:
        schedule = "adaptive"
    budget = Budget(time_limit)
    bounds = problem.bounds
    initial_point = (tuple(lo for lo, hi in bounds) if warm_start is None
                     else tuple(map(rational, warm_start)))
    if not problem.feasible(initial_point):
        raise ValueError("warm start is not feasible in the original box")
    incumbent, upper = initial_point, problem.value(initial_point)
    lower = interval_lower_bound(problem)
    certificate = {"schema": "certified-grid-qp-v1", "problem": problem.to_dict(),
                   "options": {"epsilon": str(epsilon), "theta": str(theta),
                               "pruning": pruning, "grid_mode": grid_mode,
                               "slope_decay_period": slope_decay_period,
                               "schedule": schedule},
                   "initial": {"lower": str(lower), "upper": str(upper),
                               "point": list(map(str, incumbent))}, "stages": []}
    center = incumbent
    scale = max(hi - lo for lo, hi in bounds)
    curvature = max(max(F(0), problem.A[i][i]) for i in range(len(problem.b)))
    trial_stage_cap = 0
    allowance = 7 * curvature * len(problem.b) * scale ** 2 / 8
    if epsilon:
        while allowance > epsilon:
            allowance /= 4
            trial_stage_cap += 1
    # (n+1).bit_length() is exactly ceil(log2(n+2)).
    logarithm_cap = (len(problem.b) + 1).bit_length()
    trial, trial_stage, restart = 2, 0, True
    table_states = 0
    attempted_stages = 0
    status = "stage_limit"
    try:
        budget.check(force=True)
        starts = [initial_point, tuple(hi for lo, hi in bounds), tuple(
            F(floor((lo + hi) / 2)) if i in problem.integers else (lo + hi) / 2
            for i, (lo, hi) in enumerate(bounds))]
        for start in starts:
            candidate = polish(problem, start, bounds, polish_sweeps, budget)
            value = problem.value(candidate)
            if value < upper:
                incumbent, upper = candidate, value
        # Initial proof may use any feasible point, so only its exact value is needed.
        certificate["initial"].update(upper=str(upper), point=list(map(str, incumbent)))
        if convex_presolve:
            proof = convex_certificate(problem, incumbent, budget)
            if proof is not None:
                incumbent = tuple(map(rational, proof["point"]))
                lower = upper = problem.value(incumbent)
                certificate["initial"].update(lower=str(lower), upper=str(upper),
                                               point=list(map(str, incumbent)), convex=proof)
        center = incumbent
        for attempt in range(max_stages):
            if upper - lower <= epsilon:
                status = "certified"
                break
            budget.check(force=True)
            attempted_stages += 1
            if schedule == "conditioning":
                if restart:
                    bounds, center = problem.bounds, incumbent
                h = (scale or F(1)) / 2 ** trial_stage
                slope = F(1, 2 ** trial)
                coordinate_cap = 100 * 2 ** trial * logarithm_cap
            else:
                h = (scale or F(1)) / 2 ** attempt
                slope = (theta / 2 ** (attempt // slope_decay_period)
                         if slope_decay_period else theta)
                coordinate_cap = max_table_states
            if grid_mode == "uniform":
                slope = F(0)
            try:
                grids, radii = zip(*((tuple(sorted({lo, hi})), (F(0),) * len({lo, hi}))
                                     if problem.A[i][i] <= 0 else
                                     coordinate_grid(lo, hi, center[i], h, slope,
                                                     i in problem.integers, budget,
                                                     min(max_table_states, coordinate_cap),
                                                     "trial_grid_limit" if coordinate_cap < max_table_states
                                                     else "table_limit")
                                     for i, (lo, hi) in enumerate(bounds)))
            except BudgetExceeded as exc:
                if str(exc) != "trial_grid_limit":
                    raise
                trial, trial_stage, restart = trial + 1, 0, True
                continue
            penalties = tuple(tuple(max(F(0), problem.A[i][i]) * ell * ell / 8
                                    for ell in row) for i, row in enumerate(radii))
            result = grid_dp(problem, grids, penalties, budget, max_table_states)
            point = result["point"]
            # Preserve a completed proof even if optional primal polishing times out.
            value = problem.value(point)
            if value < upper:
                incumbent, upper = point, value
            try:
                candidate = polish(problem, point, bounds, polish_sweeps, budget)
            except BudgetExceeded:
                candidate = point
            value = problem.value(candidate)
            if value < upper:
                incumbent, upper = candidate, value
            next_bounds, removed = (filtered_bounds(grids, result["marginals"], upper)
                                    if pruning else (bounds, 0))
            lower = max(lower, result["lower"])
            certificate["stages"].append({
                "stage": len(certificate["stages"]), "h": str(h), "theta": str(slope),
                "restart": schedule == "conditioning" and restart,
                "trial": trial if schedule == "conditioning" else None,
                "trial_stage": trial_stage if schedule == "conditioning" else None,
                "grids": [list(map(str, grid)) for grid in grids],
                "messages": [{"from": u, "to": v,
                              "rows": [{"indices": list(state), "value": str(value)}
                                       for state, value in sorted(rows.items())]}
                             for (u, v), rows in sorted(result["messages"].items())],
                "min_marginals": [list(map(str, row)) for row in result["marginals"]],
                "grid_lower": str(result["lower"]), "lower": str(lower),
                "grid_point": list(map(str, point)), "upper": str(upper),
                "incumbent": list(map(str, incumbent)),
                "next_bounds": [[str(lo), str(hi)] for lo, hi in next_bounds],
                "table_states": result["table_states"], "removed_intervals": removed,
                "elapsed_seconds": perf_counter() - budget.started})
            table_states += result["table_states"]
            center, bounds = point, next_bounds
            restart = False
            if schedule == "conditioning":
                trial_stage += 1
                if trial_stage > trial_stage_cap:
                    trial, trial_stage, restart = trial + 1, 0, True
        if upper - lower <= epsilon:
            status = "certified"
    except BudgetExceeded as exc:
        status = str(exc)
    # A budget interruption during initial polishing may improve upper before
    # the initial record was refreshed; publish that feasible point explicitly.
    if not certificate["stages"]:
        certificate["initial"].update(upper=str(upper), point=list(map(str, incumbent)))
    certificate.update(status=status, lower=str(lower), upper=str(upper),
                       point=list(map(str, incumbent)), gap=str(upper - lower),
                       stats={"elapsed_seconds": perf_counter() - budget.started,
                              "completed_table_states": table_states,
                              "attempted_stages": attempted_stages,
                              "completed_stages": len(certificate["stages"]),
                              "max_bag_size": max(map(len, problem.bags))})
    return certificate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("problem", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--epsilon", default="1/1000")
    parser.add_argument("--exact", action="store_true",
                        help="prove rational exact output using certified value separation")
    parser.add_argument("--max-rounds", type=int, default=8)
    parser.add_argument("--time-limit", type=float, default=10)
    parser.add_argument("--max-stages", type=int, default=24)
    parser.add_argument("--max-table-states", type=int, default=100000)
    parser.add_argument("--uniform", action="store_true")
    parser.add_argument("--no-pruning", action="store_true")
    parser.add_argument("--schedule", choices=("conditioning", "adaptive"), default="conditioning")
    args = parser.parse_args()
    problem = BoxQP.from_dict(json.loads(args.problem.read_text()))
    engine = solve
    extra = {"epsilon": args.epsilon}
    if args.exact:
        from exact_output import solve_exact
        engine, extra = solve_exact, {"max_rounds": args.max_rounds}
    result = engine(problem, **extra, max_stages=args.max_stages,
                   time_limit=args.time_limit, max_table_states=args.max_table_states,
                   pruning=not args.no_pruning,
                   schedule=args.schedule,
                   grid_mode="uniform" if args.uniform else "geometric")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ("status", "lower", "upper", "gap", "stats")}))


if __name__ == "__main__":
    main()
