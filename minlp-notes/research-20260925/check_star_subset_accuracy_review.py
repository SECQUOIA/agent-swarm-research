"""Targeted independent checks for the quantitative star-gap review.

The symbolic checks are exact identities. The perimeter calculations use
floating point and only check the stated finite cases, not the theorem.
"""

from itertools import combinations, product
from math import cos, pi, sin, sqrt, tan

import sympy as sp


def check_exact_cut_and_candidate():
    # General diagonal leaves, arbitrary total horizontal component C,
    # and radius-two signed-sum bound: this covers both constructions.
    n = 3
    x = sp.symbols("x", real=True)
    y = sp.symbols("y:3", real=True)
    b = sp.symbols("b:3", positive=True)
    d = sp.symbols("d:3", positive=True)
    c = sp.symbols("c:3", real=True)
    w = [b[i] ** 2 / d[i] for i in range(n)]
    total_w = sum(w)
    total_c = sum(c)
    a = 1 + total_w / 2
    gamma = 1 - total_w / 2
    count = 0
    for z in product((0, 1), repeat=n):
        active = [i for i in range(n) if z[i]]
        cost = a * x**2 + sum(
            d[i] * y[i] ** 2 + 2 * b[i] * x * y[i] for i in active
        )
        cut = cost + total_c * x + gamma + sum(
            2 * d[i] * c[i] * y[i] / b[i]
            + w[i]
            + c[i] ** 2 / w[i]
            for i in active
        )
        squares = sum(
            d[i] * (y[i] + b[i] * x / d[i] + c[i] / b[i]) ** 2
            for i in active
        )
        hx = sum((2 * z[i] - 1) * c[i] for i in range(n))
        hz = -sum((2 * z[i] - 1) * w[i] for i in range(n))
        residual = ((2 + hz) * x**2 - 2 * hx * x + 2 - hz) / 2
        assert sp.expand(cut - squares - residual) == 0
        count += 1

    eta = sp.symbols("eta", real=True)
    qx = sp.symbols("qx:3", real=True)
    qz = sp.symbols("qz:3", real=True)
    z = [(1 + eta * qz[i]) / 2 for i in range(n)]
    s = [eta * qx[i] / 2 for i in range(n)]
    r = [(1 - eta * qz[i]) / 2 for i in range(n)]
    means = [-(w[i] * s[i] + z[i] * c[i]) / b[i] for i in range(n)]
    candidate_cost = a + sum(
        d[i] * (means[i] + b[i] * s[i] / d[i]) ** 2 / z[i]
        - w[i] * r[i]
        for i in range(n)
    )
    candidate_cut = candidate_cost + gamma + sum(
        2 * d[i] * c[i] * means[i] / b[i]
        + (w[i] + c[i] ** 2 / w[i]) * z[i]
        for i in range(n)
    )
    desired = 2 - eta * sum(c[i] * qx[i] - w[i] * qz[i] for i in range(n))
    assert sp.cancel(candidate_cut - desired) == 0
    print(f"Exact symbolic identities passed: {count} supports and candidate cut.")


def subset_perimeter(angles):
    if len(angles) == 1:
        return 4.0
    return 4 * (
        cos((angles[-1] - angles[0]) / 2)
        + sum(sin((right - left) / 2) for left, right in zip(angles, angles[1:]))
    )


def check_real_perimeters():
    beta = pi / 12
    s_inf = cos(beta) + beta
    c0 = beta**2 * sin(beta) / (8 * s_inf)
    t0 = sqrt(3) * (2 + 1 / tan(pi / 24) ** 2)
    subset_count = 0
    for k in range(1, 8):
        n = 2 * k
        angles = [-beta + 2 * beta * i / (n - 1) for i in range(n)]
        p = subset_perimeter(angles)
        upper = 4 if k == 1 else 4 * (cos(beta) + (k - 1) * sin(beta / (k - 1)))
        maximum = 0.0
        # Inclusion monotonicity reduces all sizes <= k to size exactly k.
        for indices in combinations(range(n), k):
            maximum = max(maximum, subset_perimeter([angles[i] for i in indices]))
            subset_count += 1
        assert maximum <= upper + 1e-12
        assert p > upper
        delta = (p - upper) / upper
        assert delta >= c0 / k**2
        print(f"k={k}: maximum subset perimeter={maximum:.12f}, certificate={delta:.12g}")
    print(f"Checked {subset_count} subsets; c0={c0:.12g}, T0={t0:.12g}.")


if __name__ == "__main__":
    check_exact_cut_and_candidate()
    check_real_perimeters()
