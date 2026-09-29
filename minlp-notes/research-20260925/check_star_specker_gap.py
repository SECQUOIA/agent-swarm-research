"""Numerical checks for the regular-family star moment gap.

These floating-point checks do not certify the theorem or SDP optima.
Run from the repository root with:
    python research-20260925/check_star_specker_gap.py
"""

import itertools
import math

import cvxpy as cp
import numpy as np


for n in range(2, 6):
    alpha = math.pi / (2 * n)
    theta = math.pi / 2 + math.pi / (4 * n) + np.arange(n) * math.pi / n
    directions = np.column_stack([np.sin(theta), np.cos(theta)])
    radius = 1 / math.sin(alpha)
    eta = 0.5 * (
        radius / n
        + 1 / ((n - 2) * math.sin(alpha) + math.sin(2 * alpha))
    )
    weights = -np.cos(theta)
    a = (radius + sum(weights)) / 2
    b = np.sqrt(weights)
    z = (1 + eta * np.cos(theta)) / 2
    s = eta * np.sin(theta) / 2
    r = (1 - eta * np.cos(theta)) / 2
    y = -b * s - z * np.sin(theta) / b
    candidate = a + np.sum((y + b * s) ** 2 / z - weights * r)
    margin = n * eta - radius
    gamma = (radius - sum(weights)) / 2
    cut_slack = (
        candidate
        + np.sum(2 * np.sin(theta) * y / b + z / weights)
        + gamma
    )
    max_signed_norm = max(
        np.linalg.norm(np.array(signs) @ directions)
        for signs in itertools.product([-1, 1], repeat=n)
    )
    local_perimeter = 4 * eta * (
        (n - 2) * math.sin(alpha) + math.sin(2 * alpha)
    )
    assert abs(max_signed_norm - radius) < 1e-12
    assert a > sum(weights)
    assert local_perimeter < 4
    assert margin > 0
    assert abs(cut_slack + margin) < 1e-12

    patterns = list(itertools.product([0, 1], repeat=n))
    atoms = [cp.Variable((2, 2), symmetric=True) for _ in patterns]
    total = sum(atoms)
    marginals = [
        sum(atom for atom, pattern in zip(atoms, patterns) if pattern[i])
        for i in range(n)
    ]
    constraints = (
        [atom >> 0 for atom in atoms]
        + [total[0, 0] == 1, total[0, 1] == 0]
        + [marginals[i][0, 0] == z[i] for i in range(n)]
    )
    objective = a * total[1, 1] + sum(
        cp.square(y[i] + b[i] * marginals[i][0, 1]) / z[i]
        - weights[i] * marginals[i][1, 1]
        for i in range(n)
    )
    problem = cp.Problem(cp.Minimize(objective), constraints)
    problem.solve(
        solver="CLARABEL",
        tol_gap_abs=1e-10,
        tol_feas=1e-10,
        tol_gap_rel=1e-10,
    )
    assert problem.status == "optimal"
    assert problem.value - candidate > margin - 1e-7
    print(
        f"N={n}: candidate={candidate:.10f}, full={problem.value:.10f}, "
        f"proved_margin={margin:.10f}"
    )
