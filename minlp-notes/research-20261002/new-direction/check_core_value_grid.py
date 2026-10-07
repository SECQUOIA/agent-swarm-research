"""Exact grid diagnostics for the core-only-noise value-oracle review.

This preserves the diagnostic previously run inline. It tests quadratic
cores with a convex residual y**2 and deliberately inexact feasible
recourse certificates; it is not an implementation of the general oracle.
"""

from fractions import Fraction as Q
from itertools import product

stages = 0
cells_checked = 0
pruned = 0
for k in (1, 2):
    centers = [
        (Q(0),) * k,
        (Q(1),) * k,
        tuple(Q(i + 1, 2 * i + 3) for i in range(k)),
    ]
    for center in centers:
        for g in (Q(1, 2), Q(1, 32), Q(1, 1024)):
            retained = None
            U = None
            for j in range(6):
                size = 2**j
                h = Q(1, size)
                e = Q(k, 8) * h * h
                ys = e / (1 + e)
                residual = ys * ys
                assert residual <= e
                if j == 0:
                    cells = [(0,) * k]
                else:
                    cells = [
                        tuple(2 * i + b for i, b in zip(cell, bits))
                        for cell in retained
                        for bits in product((0, 1), repeat=k)
                    ]
                labels = {
                    tuple(Q(i + b, size) for i, b in zip(cell, bits))
                    for cell in cells
                    for bits in product((0, 1), repeat=k)
                }
                values = {
                    v: g * sum((x - a) ** 2 for x, a in zip(v, center))
                    for v in labels
                }
                upper = {v: values[v] + residual for v in labels}
                lower = {v: upper[v] - e for v in labels}
                stageU = min(upper.values())
                U = stageU if U is None else min(U, stageU)
                assert U <= 2 * e
                if k == 1:
                    assert len(cells) ** 2 <= Q(512**2) * (1 + 1 / g)
                else:
                    assert len(cells) <= Q(512) * (1 + 1 / g)
                keep = []
                lbs = []
                for cell in cells:
                    vertices = [
                        tuple(Q(i + b, size) for i, b in zip(cell, bits))
                        for bits in product((0, 1), repeat=k)
                    ]
                    witness = min(vertices, key=lower.get)
                    lb = lower[witness] - e
                    true = g * sum(
                        (max(Q(i, size), min(Q(i + 1, size), a)) - a) ** 2
                        for i, a in zip(cell, center)
                    )
                    assert lb <= true
                    contains = all(
                        Q(i, size) <= a <= Q(i + 1, size)
                        for i, a in zip(cell, center)
                    )
                    if lb <= U:
                        keep.append(cell)
                        lbs.append(lb)
                        assert values[witness] <= 4 * e
                    else:
                        assert not contains and true > U
                        pruned += 1
                    cells_checked += 1
                assert keep
                Lb = min(U, min(lbs))
                assert Lb <= 0 <= U and U - Lb <= 2 * e
                retained = keep
                stages += 1

print(
    f"PASS: {stages} exact stages, {cells_checked} cell lower bounds, "
    f"{pruned} safe prunes; gaps, feasible residual witnesses, growth "
    "packing, and optimizer containment verified."
)
