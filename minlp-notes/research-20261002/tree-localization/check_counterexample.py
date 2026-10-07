"""Targeted floating-point checks of counterexample.md; no solver dependency."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def tree_matrix(depth: int, a: float):
    n = 2 ** (depth + 1) - 1
    H = np.eye(n)
    for v in range(1, n):
        p = (v - 1) // 2
        H[v, p] = H[p, v] = -a
    return H, np.arange(2**depth - 1, n)


def profile(depth: int, a: float):
    s = np.sqrt(1 - 8 * a * a)
    rp, rm = (1 + s) / (4 * a), (1 - s) / (4 * a)
    gamma = rm / rp
    q = (1 + s) / 2 * (1 - gamma ** (depth + 2)) / (
        1 - gamma ** (depth + 1)
    )
    t = 1 / (2 * (q + 1))
    levels = t * (
        rp ** np.arange(1, depth + 2) - rm ** np.arange(1, depth + 2)
    ) / (rp ** (depth + 1) - rm ** (depth + 1))
    return q, t, levels


def h_w(z, width):
    return np.where((0 <= z) & (z <= width), z * (width - z), 0.0)


def run():
    rng = np.random.default_rng(20261002)
    a = 7 / 20
    gap = 1 - 2 * np.sqrt(2) * a
    lp = (1 + np.sqrt(1 - 8 * a * a)) / 2
    b0 = 2 * np.sqrt(2) * a / gap
    c_q = 4 / gap + 4 * (2 * b0 * b0 + 1) / lp
    checked = []

    for depth in range(1, 8):
        H, leaves = tree_matrix(depth, a)
        n, leaf_start = len(H), leaves[0]
        interior = np.arange(leaf_start)
        q, t, levels = profile(depth, a)
        lev = np.floor(np.log2(np.arange(n) + 1)).astype(int)
        target = levels[lev]

        # Check the claimed convex-square plus concave-leaf factorization.
        pivots = np.empty(n)
        pivots[leaves] = 2.0
        for v in range(leaf_start - 1, -1, -1):
            pivots[v] = 1 - a * a / pivots[2 * v + 1] - a * a / pivots[2 * v + 2]
        reconstructed = np.zeros_like(H)
        reconstructed[0, 0] = pivots[0]
        bag_norm = 0.0
        for v in range(1, n):
            p = (v - 1) // 2
            vec = np.array([-a / pivots[v], 1.0])
            local = pivots[v] * np.outer(vec, vec)
            reconstructed[np.ix_([p, v], [p, v])] += local
            bag_norm = max(bag_norm, np.linalg.norm(local, 2))
        reconstructed[leaves, leaves] -= 1
        assert np.max(np.abs(reconstructed - H)) < 1e-14
        assert pivots.min() >= lp - 1e-13
        assert bag_norm < 3

        Hii = H[np.ix_(interior, interior)]
        Hil = H[np.ix_(interior, leaves)]
        B = -np.linalg.solve(Hii, Hil)
        S = H[np.ix_(leaves, leaves)] + Hil.T @ B
        assert np.max(np.abs(S @ np.ones(len(leaves)) - q)) < 1e-12
        offdiag = S - np.diag(np.diag(S))
        assert offdiag.max() < 1e-14
        assert np.max(np.abs(B @ np.full(len(leaves), t) - target[interior])) < 1e-12
        assert np.max(np.abs((H @ target)[interior])) < 1e-12
        assert np.max(np.abs((H @ target)[leaves] - q * t)) < 1e-12
        minimum_eigenvalue = np.linalg.eigvalsh(H)[0]
        assert minimum_eigenvalue >= gap - 1e-12

        # Global auxiliary growth, including points on both sides of the well.
        width = 2 ** (-max(1, int(np.ceil(np.log2(2 * levels.max())))))
        target *= width
        minimum = 0.5 * target @ H @ target - 0.5 * h_w(target[leaves], width).sum()
        assert target.max() <= 0.5 + 1e-12
        for _ in range(50):
            x = rng.uniform(-1, 1, n)
            value = 0.5 * x @ H @ x - 0.5 * h_w(x[leaves], width).sum()
            assert value >= minimum - 1e-12
            assert np.sum((x - target) ** 2) <= c_q * (value - minimum) + 1e-10

        # The scalar global growth bound is the decisive nonlocal-minimum check.
        z = np.linspace(-2, 2, 10001)
        psi = q * z * z / 2 - h_w(z, 1) / 2
        psi_t = -(q + 1) * t * t / 2
        assert np.min(psi - psi_t - q * (z - t) ** 2 / 4) >= -1e-12

        checked.append({
            "depth": depth,
            "vertices": n,
            "minimum_eigenvalue": float(minimum_eigenvalue),
            "max_bag_hessian_norm": float(bag_norm),
            "leaf_schur_row_sum": float(q),
            "root_over_W": float(levels[0]),
            "width_for_domain": float(width),
        })

    growth = []
    for depth in [1, 4, 8, 16, 32, 64, 100]:
        q, _, levels = profile(depth, a)
        growth.append({"depth": depth, "root_over_W": float(levels[0]), "q_d": float(q)})
    assert growth[-1]["root_over_W"] > 1e7

    result = {
        "status": "passed",
        "checks": "factorization; bag norms; spectral gap; Schur signs and row sums; harmonic formula; auxiliary global growth",
        "a": a,
        "uniform_spectral_gap": float(gap),
        "uniform_c_g": float(gap / 2),
        "uniform_M_a": 3,
        "uniform_alpha_prime_A": 0.5,
        "uniform_k_w_Delta": [3, 1, 2],
        "uniform_growth_constant_C_Q": float(c_q),
        "explicit_trees": checked,
        "depth_growth": growth,
        "scope": "floating-point targeted checks; no finite-DP enumeration, project-wide verification, or CI checks",
    }
    output = Path(__file__).with_suffix(".json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run()
