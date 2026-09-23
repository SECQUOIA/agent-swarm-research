#!/usr/bin/env python3
"""Exact signed-subset circuit oracle, checked against a separate LP solver.

This validates the finite oracle used after flat-chain profile elimination;
the independent reviewer checks the original graph-to-profile reduction.
"""

from fractions import Fraction as F
from itertools import combinations, product
from math import gcd, lcm
import json
import numpy as np
import sympy as sp
from scipy.optimize import linprog


def circuits(d):
    normals = [tuple(sign * x for x in row)
               for row in product([0, 1], repeat=d) if any(row)
               for sign in [-1, 1]]
    found = []
    for size in range(2, d + 2):
        for inds in combinations(range(len(normals)), size):
            mat = sp.Matrix([normals[i] for i in inds]).T
            kernel = mat.nullspace()
            if len(kernel) != 1:
                continue
            ray = kernel[0]
            if all(v < 0 for v in ray):
                ray = -ray
            if not all(v > 0 for v in ray):
                continue
            scale = lcm(*[int(v.q) for v in ray])
            ints = [int(v * scale) for v in ray]
            divisor = gcd(*ints)
            ints = tuple(v // divisor for v in ints)
            assert mat * sp.Matrix(ints) == sp.zeros(d, 1)
            found.append((inds, ints))
    return normals, found


def main():
    rng = np.random.default_rng(20260909)
    report = []
    for d in [1, 2, 3]:
        normals, rays = circuits(d)
        bound = 1 if d <= 2 else 2
        assert all(max(weights) <= bound for _, weights in rays)
        feasible = infeasible = 0
        for case in range(200):
            present = {i for i in range(len(normals)) if rng.random() < 0.7}
            if case % 2 == 0:
                point = [F(int(rng.integers(-5, 6)), 7) for _ in range(d)]
                rhs = {i: sum(F(v) * w for v, w in zip(normals[i], point))
                          + F(int(rng.integers(0, 8)), 11) for i in present}
            else:
                rhs = {i: F(int(rng.integers(-8, 9)), 11) for i in present}
            accepted = all(sum(F(weight) * rhs[i] for i, weight in zip(inds, weights)) >= 0
                           for inds, weights in rays if set(inds) <= present)
            order = sorted(present)
            lp = linprog(np.zeros(d),
                         A_ub=np.array([normals[i] for i in order]) if order else None,
                         b_ub=np.array([float(rhs[i]) for i in order]) if order else None,
                         bounds=[(None, None)] * d, method="highs")
            assert lp.success == accepted, (d, case, lp.message)
            feasible += int(accepted)
            infeasible += int(not accepted)
        report.append({"states": d, "normals": len(normals), "circuits": len(rays),
                       "maximum_ray_entry": max(max(w) for _, w in rays),
                       "feasible": feasible, "infeasible": infeasible})
    print(json.dumps({"passed": True, "cases": report}, indent=2))


if __name__ == "__main__":
    main()
