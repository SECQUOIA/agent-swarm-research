#!/usr/bin/env python3
"""Exact-rational stress checks for the geometric-grid tree DP.

This is a small independent experiment, not a general optimization solver.
Run with Python 3.10+; it has no third-party dependencies.
"""

from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
from math import prod
from random import Random
import json
import time


def require(condition, message):
    if not condition:
        raise AssertionError(message)


@dataclass(frozen=True)
class Case:
    name: str
    bounds: tuple
    integer: tuple
    optimum: tuple
    quadratic: tuple
    quartic: tuple
    linear: tuple
    edges: tuple  # (parent, child, nonnegative coupling weight)
    center: tuple
    theta: Q
    stages: int
    offset: Q = Q(-17, 5)

    @property
    def n(self):
        return len(self.bounds)

    def unary(self, i, x):
        z = x - self.optimum[i]
        return self.quadratic[i] * z*z - self.quartic[i] * z**4 + self.linear[i] * z

    def pair(self, i, j, weight, x, y):
        return weight * ((x-self.optimum[i]) - (y-self.optimum[j]))**2

    def value(self, x):
        return self.offset + sum(self.unary(i, v) for i, v in enumerate(x)) + sum(
            self.pair(i, j, w, x[i], x[j]) for i, j, w in self.edges
        )

    def constants(self):
        """Algebraic certificates valid throughout the whole continuous box.

        a*z^2-k*z^4 >= (a-k*R^2)*z^2, where |z|<=R.
        Every linear term and edge square is nonnegative at feasible points.
        The coordinate second derivative is at most 2*a+2*weighted_degree.
        """
        degree = [Q(0)] * self.n
        parents = [0] * self.n
        for i, j, w in self.edges:
            require(0 <= i < j < self.n and w >= 0, self.name + ": ordered tree edges")
            degree[i] += w
            degree[j] += w
            parents[j] += 1
        require(parents == [0] + [1] * (self.n-1), self.name + ": rooted tree")
        local_growth = []
        for i, ((lo, hi), s, a, k, m) in enumerate(zip(
            self.bounds, self.optimum, self.quadratic, self.quartic, self.linear
        )):
            require(lo <= s <= hi and lo <= self.center[i] <= hi, self.name + ": feasible centers")
            require(k >= 0 and m*(lo-s) >= 0 and m*(hi-s) >= 0, self.name + ": sign certificate")
            if self.integer[i]:
                require(all(v.denominator == 1 for v in (lo, hi, s, self.center[i])),
                        self.name + ": integral box, optimum, and center")
            radius = max(abs(lo-s), abs(hi-s))
            local_growth.append(a-k*radius**2)
        cg = min(local_growth)
        L = max(2*a+2*d for a, d in zip(self.quadratic, degree))
        require(cg > 0 and L > 0, self.name + ": positive certified constants")
        require(self.theta > 0 and self.theta**2 <= min(Q(1, 4), cg/(8*L)),
                self.name + ": theta restriction")
        require(self.value(self.optimum) == self.offset, self.name + ": attained optimum")
        return cg, L


def coordinate_grid(lo, hi, center, h, theta, integer):
    """Walk outward on each side, clipping only the final step."""
    require(lo <= center <= hi and h > 0 and theta > 0, "grid inputs")
    sides = []
    clipped = 0
    for direction, endpoint in ((-1, lo), (1, hi)):
        values = []
        current = center
        while current != endpoint:
            nominal = h + theta*abs(current-center)
            step = Q(max(1, nominal.numerator // nominal.denominator)) if integer else nominal
            remaining = abs(endpoint-current)
            clipped += remaining < step
            current += direction * min(step, remaining)
            values.append(current)
        sides.append(values)
    grid = tuple(reversed(sides[0])) + (center,) + tuple(sides[1])
    require(grid[0] == lo and grid[-1] == hi and all(a < b for a, b in zip(grid, grid[1:])),
            "grid order and endpoints")
    if integer:
        require(all(v.denominator == 1 for v in grid), "integer grid")
    return grid, clipped


def penalties(grid, integer, L):
    result = [Q(0)] * len(grid)
    for i, (left, right) in enumerate(zip(grid, grid[1:])):
        gap = right-left
        if integer and gap == 1:
            continue
        penalty = L*gap**2/8
        result[i] = max(result[i], penalty)
        result[i+1] = max(result[i+1], penalty)
    return tuple(result)


def tree_dp(case, grids, d):
    """Min-sum elimination; retain choices to reconstruct a full assignment."""
    children = [[] for _ in grids]
    for i, j, w in case.edges:
        children[i].append((j, w))
    tables, choices = {}, {}
    for i in reversed(range(case.n)):
        row = [case.unary(i, x)-d[i][k] for k, x in enumerate(grids[i])]
        for j, w in children[i]:
            edge_choices = []
            for k, x in enumerate(grids[i]):
                best, chosen = min((tables[j][r]+case.pair(i, j, w, x, y), r)
                                   for r, y in enumerate(grids[j]))
                row[k] += best
                edge_choices.append(chosen)
            choices[i, j] = edge_choices
        tables[i] = row
    root_value, root_choice = min((v, k) for k, v in enumerate(tables[0]))
    chosen = [None] * case.n
    chosen[0] = root_choice
    for i in range(case.n):
        for j, _ in children[i]:
            chosen[j] = choices[i, j][chosen[i]]
    point = tuple(grid[k] for grid, k in zip(grids, chosen))
    correction = sum(p[k] for p, k in zip(d, chosen))
    return case.offset+root_value, point, correction


def brute_grid(case, grids, d):
    """Enumerate full assignments independently of the elimination order."""
    local = [[case.unary(i, x)-d[i][k] for k, x in enumerate(grid)]
             for i, grid in enumerate(grids)]
    pairs = [(i, j, [[case.pair(i, j, w, x, y) for y in grids[j]] for x in grids[i]])
             for i, j, w in case.edges]
    best = None
    for indices in product(*(range(len(g)) for g in grids)):
        value = case.offset + sum(local[i][k] for i, k in enumerate(indices))
        value += sum(table[indices[i]][indices[j]] for i, j, table in pairs)
        best = value if best is None else min(best, value)
    return best


def rounding_law(x, grid):
    """Unbiased neighboring-endpoint law for one feasible coordinate."""
    for i, value in enumerate(grid):
        if x == value:
            return ((i, Q(1)),)
    for i, (left, right) in enumerate(zip(grid, grid[1:])):
        if left < x < right:
            return ((i, (right-x)/(right-left)), (i+1, (x-left)/(right-left)))
    raise AssertionError("probe outside box")


def check_rounding(case, grids, d, point, L, lower):
    laws = [rounding_law(x, g) for x, g in zip(point, grids)]
    for i, law in enumerate(laws):
        require(sum(p for _, p in law) == 1, "rounding normalization")
        require(sum(p*grids[i][k] for k, p in law) == point[i], "rounding mean")
    expected_f = Q(0)
    expected_d = Q(0)
    variance = Q(0)
    for outcomes in product(*laws):
        probability = prod(p for _, p in outcomes)
        rounded = tuple(grids[i][k] for i, (k, _) in enumerate(outcomes))
        expected_f += probability*case.value(rounded)
        expected_d += probability*sum(d[i][k] for i, (k, _) in enumerate(outcomes))
        variance += probability*sum((a-b)**2 for a, b in zip(rounded, point))
    require(expected_f-case.value(point) <= L*variance/2, "semiconcavity rounding inequality")
    require(expected_d >= L*variance/2, "endpoint penalties cover rounding loss")
    require(lower <= expected_f-expected_d <= case.value(point), "independent lower certificate")


def probes(case, rng):
    points = [case.optimum, case.center]
    for repetition in range(5):
        point = []
        for i, (lo, hi) in enumerate(case.bounds):
            if case.integer[i]:
                point.append(Q(rng.randint(int(lo), int(hi))))
            else:
                denominator = (3, 7, 11, 13, 17)[repetition]
                point.append(lo+(hi-lo)*Q(rng.randrange(denominator+1), denominator))
        points.append(tuple(point))
    return points


def squared_distance(x, y):
    return sum((a-b)**2 for a, b in zip(x, y))


def check_case(case, seed):
    cg, L = case.constants()
    B = max(Q(1), 4*L/(11*cg))
    scale = max(hi-lo for lo, hi in case.bounds)
    center = case.center
    previous_error = squared_distance(center, case.optimum)
    rows = []
    total_assignments = clipped = rounding_checks = 0
    integer_threshold_stage = None
    rng = Random(seed)
    for stage in range(case.stages):
        h = scale / 2**stage
        grids = []
        for i, (lo, hi) in enumerate(case.bounds):
            grid, clips = coordinate_grid(lo, hi, center[i], h, case.theta, case.integer[i])
            grids.append(grid)
            clipped += clips
        d = [penalties(g, integer, L) for g, integer in zip(grids, case.integer)]
        for i, (grid, correction) in enumerate(zip(grids, d)):
            for v, dv in zip(grid, correction):
                require(dv <= L*(h+case.theta*abs(v-center[i]))**2/8,
                        case.name + ": vertex penalty bound")
        lower, point, correction = tree_dp(case, grids, d)
        exhaustive = brute_grid(case, grids, d)
        require(lower == exhaustive, case.name + ": DP equals exhaustive enumeration")
        value = case.value(point)
        error = squared_distance(point, case.optimum)
        require(value-lower == correction, case.name + ": reconstructed DP assignment")
        require(lower <= case.offset <= value, case.name + ": analytic optimum bracket")
        require(value-case.offset >= cg*error, case.name + ": QG consequence")
        require(correction <= L*(case.n*h*h+case.theta**2*squared_distance(point, center))/4,
                case.name + ": correction distance bound")
        require(error <= 4*L*case.n*h*h/(15*cg)+previous_error/15,
                case.name + ": stage contraction recurrence")
        require(error <= B*case.n*h*h, case.name + ": halving invariant")
        require(correction <= 7*L*case.n*h*h/8, case.name + ": final correction bound")
        for probe in probes(case, rng):
            check_rounding(case, grids, d, probe, L, lower)
            rounding_checks += 1
        assignments = prod(len(g) for g in grids)
        total_assignments += assignments
        if all(case.integer) and B*case.n*h*h < 1:
            require(point == case.optimum, case.name + ": integer identification threshold")
            if integer_threshold_stage is None:
                integer_threshold_stage = stage
            elif stage == integer_threshold_stage+1:
                require(lower == value == case.offset and correction == 0,
                        case.name + ": exact certificate one stage after integer identification")
        rows.append({
            "stage": stage, "h": str(h), "grid_sizes": [len(g) for g in grids],
            "lower": str(lower), "upper": str(value), "squared_error": str(error),
            "correction": str(correction), "assignments": assignments,
        })
        center, previous_error = point, error
    if all(case.integer):
        require(integer_threshold_stage is not None and case.stages > integer_threshold_stage+1,
                case.name + ": integer test reaches the extra certification stage")
    require(clipped > 0, case.name + ": clipped endpoints exercised")
    return {
        "name": case.name, "n": case.n, "cg": str(cg), "L": str(L), "B": str(B),
        "theta": str(case.theta), "stages": rows, "exhaustive_assignments": total_assignments,
        "rounding_checks": rounding_checks, "clipped_steps": clipped,
        "integer_threshold_stage": integer_threshold_stage,
    }


def cases():
    zero3 = (Q(0),)*3
    return (
        Case("boundary_large_linear_chain", ((Q(-1), Q(1)), (Q(-2), Q(1)), (Q(0), Q(2))),
             (False,)*3, (Q(-1), Q(1), Q(0)), (Q(1), Q(3, 2), Q(2)), zero3,
             (Q(1000), Q(-500), Q(750)), ((0, 1, Q(1, 8)), (1, 2, Q(1, 8))),
             (Q(1, 3), Q(-4, 3), Q(7, 5)), Q(1, 8), 4),
        Case("nonconvex_quartic_chain", ((Q(-1), Q(1)),)*3, (False,)*3, zero3,
             (Q(1),)*3, (Q(3, 4),)*3, zero3,
             ((0, 1, Q(1, 16)), (1, 2, Q(1, 16))),
             (Q(2, 3), Q(-3, 5), Q(1, 7)), Q(1, 16), 5),
        Case("pure_integer_exact_stopping", ((Q(-9), Q(10)),)*3, (True,)*3,
             (Q(-2), Q(1), Q(4)), (Q(1), Q(3, 2), Q(2)), zero3, zero3,
             ((0, 1, Q(1, 4)), (1, 2, Q(1, 4))), (Q(8), Q(-7), Q(-5)), Q(1, 8), 8),
        Case("large_integer_compressed_stopping", ((Q(-10000), Q(10000)),)*2, (True,)*2,
             (Q(-2), Q(3)), (Q(1),)*2, (Q(0),)*2, (Q(0),)*2,
             ((0, 1, Q(1, 4)),), (Q(9001), Q(-7001)), Q(1, 8), 17),
        Case("mixed_chain", ((Q(-1), Q(1)), (Q(-3), Q(4)), (Q(0), Q(2))),
             (False, True, False), (Q(1, 3), Q(1), Q(7, 6)),
             (Q(1), Q(3, 2), Q(2)), zero3, zero3,
             ((0, 1, Q(1, 8)), (1, 2, Q(1, 8))), (Q(-2, 3), Q(-2), Q(1, 5)), Q(1, 8), 5),
        Case("branching_nondyadic_centers", ((Q(-1), Q(1)),)*5, (False,)*5,
             (Q(1, 7), Q(-2, 9), Q(3, 11), Q(-4, 13), Q(5, 17)),
             (Q(1),)*5, (Q(0),)*5, (Q(0),)*5,
             ((0, 1, Q(1, 8)), (0, 2, Q(1, 8)), (0, 3, Q(1, 8)), (2, 4, Q(1, 8))),
             (Q(-1, 3), Q(2, 5), Q(-3, 7), Q(4, 9), Q(-5, 11)), Q(1, 8), 3),
    )


def check_integer_unit_intervals():
    """Adjacent integers require no random rounding and no correction."""
    grid = (Q(-1), Q(0), Q(1))
    require(penalties(grid, True, Q(2)) == (Q(0),)*3, "unit integer intervals omitted")
    require(penalties(grid, False, Q(2)) == (Q(1, 4),)*3, "continuous unit intervals retained")
    uneven = (Q(-2), Q(0), Q(1))
    require(penalties(uneven, True, Q(2)) == (Q(1), Q(1), Q(0)), "only unit interval omitted")


def check_sharp_scalar_rounding():
    """The 1/8 coefficient is necessary, even for one quadratic variable."""
    for integer in (False, True):
        case = Case("sharp_scalar_rounding", ((Q(-1), Q(1)),), (integer,), (Q(0),),
                    (Q(1),), (Q(0),), (Q(0),), (), (Q(0),), Q(1, 4), 1)
        cg, L = case.constants()
        require(cg == 1 and L == 2, "sharp scalar constants")
        grids = ((Q(-1), Q(1)),)
        d = (penalties(grids[0], integer, L),)
        lower, _, _ = tree_dp(case, grids, d)
        require(lower == case.offset, "midpoint quadratic lower bound is sharp")
        check_rounding(case, grids, d, (Q(0),), L, lower)
        # A smaller penalty would make the alleged lower bound exceed the optimum.
        insufficient = ((Q(7, 8), Q(7, 8)),)
        bad_lower, _, _ = tree_dp(case, grids, insufficient)
        require(bad_lower > case.offset, "fixture detects a deficient correction coefficient")


def main():
    started = time.monotonic()
    check_integer_unit_intervals()
    check_sharp_scalar_rounding()
    reports = [check_case(case, 7301+i) for i, case in enumerate(cases())]
    large_integer = next(r for r in reports if r["name"] == "large_integer_compressed_stopping")
    require(all(size < 20001 for size in large_integer["stages"][-1]["grid_sizes"]),
            "large integer exact stopping retains compressed grids")
    # The quartic example really is nonconvex: at x_0=1, F_00=2-9+1/8<0.
    require(Q(2)-12*Q(3, 4)+2*Q(1, 16) < 0, "nonconvex test has negative curvature")
    result = {
        "status": "PASS", "arithmetic": "fractions.Fraction throughout all certificate checks",
        "cases": reports, "case_count": len(reports),
        "stage_count": sum(len(r["stages"]) for r in reports),
        "exhaustive_assignments": sum(r["exhaustive_assignments"] for r in reports),
        "rounding_checks": sum(r["rounding_checks"] for r in reports),
        "additional_sharp_scalar_rounding_cases": 2,
        "elapsed_seconds": round(time.monotonic()-started, 3),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
