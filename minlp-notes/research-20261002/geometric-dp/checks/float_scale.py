#!/usr/bin/env python3
"""Timing-only floating-point prototype. Its output is NOT a certificate."""

import json
import math
import time


def grid(center, h, theta):
    sides = []
    for sign, endpoint in ((-1, -1.0), (1, 1.0)):
        side = []
        current = center
        while current != endpoint:
            current += sign*min(h+theta*abs(current-center), abs(endpoint-current))
            # Assign the endpoint exactly to avoid a final floating-point sliver.
            if abs(current-endpoint) < 1e-14:
                current = endpoint
            side.append(current)
        sides.append(side)
    return list(reversed(sides[0])) + [center] + sides[1]


def solve(n, stages=13):
    # A binary tree quadratic: known minimizer s and minimum zero.
    weight = 0.125
    L = 2.75  # 2 + 2*weight*maximum_degree, maximum_degree=3.
    theta = 0.125
    optimum = [0.45*math.sin(i+1) for i in range(n)]
    center = [1/3]*n
    rows = []
    started = time.perf_counter()
    for stage in range(stages):
        h = 2.0 / 2**stage
        grids = [grid(c, h, theta) for c in center]
        defect = []
        for values in grids:
            lengths = [b-a for a, b in zip(values, values[1:])]
            defect.append([L/8*max(lengths[k-1] if k else 0.0,
                                  lengths[k] if k < len(lengths) else 0.0)**2
                           for k in range(len(values))])
        tables = [[(x-optimum[i])**2-defect[i][k] for k, x in enumerate(values)]
                  for i, values in enumerate(grids)]
        choices = {}
        pair_evaluations = 0
        for child in reversed(range(1, n)):
            parent = (child-1)//2
            child_terms = [(x-optimum[child], value) for x, value in zip(grids[child], tables[child])]
            picks = []
            for k, x in enumerate(grids[parent]):
                z = x-optimum[parent]
                best = math.inf
                pick = None
                for q, (t, value) in enumerate(child_terms):
                    candidate = value+weight*(z-t)**2
                    if candidate < best:
                        best, pick = candidate, q
                tables[parent][k] += best
                picks.append(pick)
            choices[child] = picks
            pair_evaluations += len(grids[parent])*len(grids[child])
        chosen = [min(range(len(tables[0])), key=tables[0].__getitem__)]
        for child in range(1, n):
            chosen.append(choices[child][chosen[(child-1)//2]])
        center = [g[k] for g, k in zip(grids, chosen)]
        residual = [x-s for x, s in zip(center, optimum)]
        upper = sum(z*z for z in residual)+weight*sum(
            (residual[(i-1)//2]-residual[i])**2 for i in range(1, n)
        )
        lower = tables[0][chosen[0]]
        # Sanity check only; floating-point inequalities are not rigorous certificates.
        if not (lower <= 1e-10 and upper >= -1e-10):
            raise AssertionError("numerical bracket sanity check failed")
        rows.append({
            "stage": stage, "h": h, "max_grid_size": max(map(len, grids)),
            "pair_evaluations": pair_evaluations,
            "numerical_lower": lower, "numerical_upper": upper,
            "numerical_gap": upper-lower,
            "theoretical_real_arithmetic_gap_bound": 7*L*n*h*h/8,
        })
    return {"n": n, "elapsed_seconds": round(time.perf_counter()-started, 3), "stages": rows}


if __name__ == "__main__":
    print(json.dumps({
        "certified": False,
        "purpose": "Timing and size observations only; ordinary floating-point arithmetic.",
        "model": "Binary-tree shifted quadratic, continuous box [-1,1]^n, analytic minimum zero.",
        "runs": [solve(n) for n in (16, 64, 128)],
    }, indent=2))
