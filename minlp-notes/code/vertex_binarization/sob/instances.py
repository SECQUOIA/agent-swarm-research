"""Seeded instance families with separable nonconvex objectives and few linking rows."""
from __future__ import annotations

import numpy as np
import sympy as sp

from .functions import X, Univariate
from .model import SeparableProblem


def jeroslow(n: int) -> SeparableProblem:
    """min sum x_i(1-x_i), sum x_i = floor(n/3) + 1/2: the repository's lower-bound family."""
    funcs = [Univariate(X * (1 - X), 0.0, 1.0) for _ in range(n)]
    return SeparableProblem(f"jeroslow-{n}", funcs, np.ones((1, n)), ["=="], np.array([n // 3 + 0.5]))


def jeroslow_weighted(n: int) -> SeparableProblem:
    """Asymmetric variant: costs c_i x_i(1-x_i) with distinct c_i, so symmetry handling cannot help.

    The optimal value is min_i c_i / 4 = 1/4.
    """
    funcs = [Univariate((1 + sp.Rational(i, n)) * X * (1 - X), 0.0, 1.0) for i in range(n)]
    return SeparableProblem(f"jeroslow_w-{n}", funcs, np.ones((1, n)), ["=="], np.array([n // 3 + 0.5]))


def concave_knapsack(n: int, m: int, seed: int) -> SeparableProblem:
    """Concave quadratic costs (More-Vavasis style) with m random equality rows."""
    rng = np.random.default_rng(seed)
    funcs = []
    for _ in range(n):
        q, c = rng.uniform(0.5, 2.0), rng.uniform(-1.0, 1.0)
        funcs.append(Univariate(-q * X**2 + c * X, 0.0, 1.0))
    A = rng.integers(1, 21, size=(m, n)).astype(float)
    b = np.round(A @ rng.uniform(0.2, 0.8, n), 3)
    return SeparableProblem(f"cknap-n{n}-m{m}-s{seed}", funcs, A, ["=="] * m, b)


def power_cost(n: int, m: int, seed: int) -> SeparableProblem:
    """Economies-of-scale costs c_i x^p_i with m covering rows."""
    rng = np.random.default_rng(seed)
    funcs = [Univariate(rng.uniform(1, 5) * X ** sp.Float(round(rng.uniform(0.4, 0.8), 2)), 0.0, 10.0)
             for _ in range(n)]
    A = rng.integers(1, 10, size=(m, n)).astype(float)
    b = np.round(A @ rng.uniform(1.0, 4.0, n), 2)
    return SeparableProblem(f"power-n{n}-m{m}-s{seed}", funcs, A, [">="] * m, b)


def sigmoid_allocation(n: int, m: int, seed: int) -> SeparableProblem:
    """Udell-Boyd style: maximize a sum of logistic utilities under m budget rows.

    Stated as minimization of -w/(1+exp(-(a x - c))), which is concave then convex.
    """
    rng = np.random.default_rng(seed)
    funcs = []
    for _ in range(n):
        w, a, c = rng.uniform(1, 3), rng.uniform(1.0, 3.0), rng.uniform(2.0, 6.0)
        infl = c / a
        funcs.append(Univariate(-w / (1 + sp.exp(-(a * X - c))), 0.0, 6.0))
        assert 0.0 < infl < 6.0
    A = np.ones((1, n)) if m == 1 else np.vstack([np.ones(n), rng.uniform(0.5, 2.0, size=(m - 1, n))])
    b = np.round(A @ np.full(n, 1.2), 3)
    return SeparableProblem(f"sigmoid-n{n}-m{m}-s{seed}", funcs, A, ["<="] * m, b)


def quartic_allocation(n: int, m: int, seed: int) -> SeparableProblem:
    """Random univariate quartics (several monomials in the same variable) with m equality rows."""
    rng = np.random.default_rng(seed)
    funcs = []
    for _ in range(n):
        r = np.sort(rng.uniform(-2.0, 2.0, 3))          # derivative roots: two wells
        poly = sp.expand(sp.integrate((X - r[0]) * (X - r[1]) * (X - r[2]), X)) * rng.uniform(0.5, 2.0)
        funcs.append(Univariate(poly, -2.5, 2.5))
    A = np.ones((1, n)) if m == 1 else np.vstack([np.ones(n), rng.uniform(0.5, 2.0, size=(m - 1, n))])
    b = np.round(A @ rng.uniform(-0.5, 0.5, n), 3)
    return SeparableProblem(f"quartic-n{n}-m{m}-s{seed}", funcs, A, ["=="] * m, b)


FAMILIES = {"quartic": quartic_allocation, "jeroslow": lambda n, m, seed: jeroslow(n),
            "jeroslow_w": lambda n, m, seed: jeroslow_weighted(n), "cknap": concave_knapsack,
            "power": power_cost, "sigmoid": sigmoid_allocation}
