"""Targeted floating-point checks for star-short-arc-uniform-review.md.

These checks detect formula errors; they do not certify the theorem or novelty.
Only the short-arc construction is checked, with exhaustive signs for N <= 12.
"""

from itertools import product

import numpy as np


def perimeter(points):
    """Points are one half of the circularly ordered symmetric vertices."""
    if len(points) == 1:
        return 4 * np.linalg.norm(points[0])
    return 2 * (
        np.linalg.norm(points[0] + points[-1])
        + np.linalg.norm(np.diff(points, axis=0), axis=1).sum()
    )


def check(n):
    beta = np.pi / 12
    h = beta / (n - 1)
    angles = np.linspace(-beta, beta, n)
    rotation_angle = -np.pi / 3
    rotation = np.array(
        [
            [np.cos(rotation_angle), -np.sin(rotation_angle)],
            [np.sin(rotation_angle), np.cos(rotation_angle)],
        ]
    )
    points = np.column_stack((np.cos(angles), np.sin(angles))) @ rotation.T
    midpoints = (angles[:-1] + angles[1:]) / 2
    tangents = np.vstack(
        ([1, 0], np.column_stack((-np.sin(midpoints), np.cos(midpoints))), [-1, 0])
    ) @ rotation.T
    g = tangents[:-1] - tangents[1:]
    w = -g[:, 1]
    assert np.all(w > 0)
    np.testing.assert_allclose(g.sum(axis=0), [1, -np.sqrt(3)], atol=1e-13)
    p = perimeter(points)
    np.testing.assert_allclose(np.sum(g * points), p / 2, atol=1e-13)
    if n <= 12:
        signs = np.array(list(product((-1, 1), repeat=n)))
        maximum = np.linalg.norm(signs @ g, axis=1).max()
        np.testing.assert_allclose(maximum, 2, atol=1e-13)

    s_scale = np.cos(beta) + (n - 1) * np.sin(h)
    d = 2 * np.sin(h) * (1 - np.cos(h)) if n >= 3 else s_scale - 1
    largest_deleted_scale = s_scale - d if n >= 3 else 1
    if n <= 12:
        deleted = [perimeter(np.delete(points, i, axis=0)) / 4 for i in range(n)]
        np.testing.assert_allclose(max(deleted), largest_deleted_scale, atol=1e-13)
    eta = (1 / s_scale + 1 / largest_deleted_scale) / 2
    assert 0 < eta < 1
    gap = d / largest_deleted_scale
    if n <= 128:
        np.testing.assert_allclose(eta * p / 2 - 2, gap, atol=1e-13)

    z = (1 + eta * points[:, 1]) / 2
    s = eta * points[:, 0] / 2
    r = (1 - eta * points[:, 1]) / 2
    b = np.sqrt(w)
    a = 1 + w.sum() / 2
    y = -b * s - z * g[:, 0] / b
    reduced_q = np.array([[a, np.linalg.norm(b)], [np.linalg.norm(b), 1]])
    eigenvalues = np.linalg.eigvalsh(reduced_q)
    assert eigenvalues[0] > 1 / 24 and eigenvalues[-1] < 3
    assert z.min() >= (1 - np.cos(beta)) / 2
    assert z.max() < 0.5
    assert np.sum(y * y) <= np.sqrt(3) * (0.5 + 1 / np.tan(np.pi / 24)) ** 2

    constant = np.dot(g[:, 1], z) - (2 + g[:, 1].sum()) / 2
    linear_candidate = a + np.dot(-2 * g[:, 0], s) - np.dot(w, r)
    if n <= 128:
        np.testing.assert_allclose(constant - linear_candidate, gap, atol=1e-13)

    # An unrelated perturbation checks the full tangent identity algebra.
    rng = np.random.default_rng(n)
    shifted_s = s + rng.normal(size=n)
    shifted_r = r + rng.normal(size=n)
    shifted_v = 1.37

    def objective(v, moment_s, moment_r):
        return a * v + np.sum((y + b * moment_s) ** 2 / z - w * moment_r)

    lhs = objective(shifted_v, shifted_s, shifted_r) - objective(1, s, r)
    rhs = (
        a * (shifted_v - 1)
        + np.dot(-2 * g[:, 0], shifted_s - s)
        - np.dot(w, shifted_r - r)
        + np.sum(w / z * (shifted_s - s) ** 2)
    )
    np.testing.assert_allclose(lhs, rhs, atol=1e-10)
    return gap, (n - 1) ** 3 * gap, np.linalg.norm(y)


if __name__ == "__main__":
    print("N   certified_gap       (N-1)^3_gap       norm_y")
    for n in [*range(2, 13), 32, 128, 512]:
        gap, scaled_gap, mean_norm = check(n)
        print(f"{n:3d} {gap:18.11e} {scaled_gap:18.11e} {mean_norm:12.8f}")
    print("All targeted checks passed; floating-point checks are not proof certificates.")
