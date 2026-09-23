"""Compare envelope cuts with a brute-force lower convex hull on dense samples."""
import numpy as np
import sympy as sp
from uenv.curvature import X
from uenv.envelope import Univariate

CASES = [
    (X**4 - 3 * X**3 + X**2 + X, -1.5, 2.5),
    (X * sp.exp(-X), 0.0, 6.0),
    (-1 / (1 + sp.exp(-(2 * X - 5))), 0.0, 6.0),
    (sp.sin(3 * X) + 0.3 * X**2, -2.0, 3.0),
    (X / (1 + X) ** 2, 0.0, 8.0),
    (sp.log(1 + sp.exp(X)) - 0.2 * X**2, -4.0, 4.0),
    (X**0.6 - 0.1 * X**1.7, 0.5, 9.0),
]


def lower_hull(xs, ys):
    hull = []
    for p in zip(xs, ys):
        while len(hull) >= 2:
            (x1, y1), (x2, y2) = hull[-2], hull[-1]
            if (x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1) > 0:
                break
            hull.pop()
        hull.append(p)
    hx, hy = zip(*hull)
    return lambda t: np.interp(t, hx, hy)


def test_envelopes():
    rng = np.random.default_rng(0)
    for expr, lo, hi in CASES:
        f = Univariate(expr, lo, hi)
        for _ in range(6):
            l, u = np.sort(rng.uniform(lo, hi, 2))
            if u - l < 1e-3:
                continue
            xs = np.linspace(l, u, 20001)
            ys = np.array([f.g(float(t)) for t in xs])
            env, cenv = lower_hull(xs, ys), lower_hull(xs, -ys)
            scale = 1.0 + np.ptp(ys)
            for xstar in rng.uniform(l, u, 5):
                a, c = f.under(l, u, xstar)
                assert np.all(a * xs + c <= ys + 1e-9 * scale), (expr, l, u, "under invalid")
                assert a * xstar + c >= env(xstar) - 2e-4 * scale, (expr, l, u, xstar, "under loose")
                a, c = f.over(l, u, xstar)
                assert np.all(a * xs + c >= ys - 1e-9 * scale), (expr, l, u, "over invalid")
                assert a * xstar + c <= -cenv(xstar) + 2e-4 * scale, (expr, l, u, xstar, "over loose")
            rlo, rhi = f.range(l, u)
            assert rlo <= ys.min() + 1e-9 and rhi >= ys.max() - 1e-9
            assert rlo >= ys.min() - 1e-3 * scale and rhi <= ys.max() + 1e-3 * scale


def test_domain_and_singular_endpoints():
    import pytest
    for expr, lo, hi in [(sp.log(X), -2.0, -1.0), (1 / (X - 1), 0.0, 2.0), (sp.tan(X), 1.0, 2.0)]:
        with pytest.raises((ValueError, NotImplementedError)):
            Univariate(expr, lo, hi)
    f = Univariate((X + 4.5) ** 0.6, -4.5, 3.0)       # singular endpoint away from zero
    xs = np.linspace(-4.5, 3.0, 5001)
    ys = (xs + 4.5) ** 0.6
    for xstar in (-4.5, -4.0, 0.0, 3.0):
        a, c = f.under(-4.5, 3.0, xstar)
        assert np.all(a * xs + c <= ys + 1e-9)
        a, c = f.over(-4.5, 3.0, xstar)
        assert np.all(a * xs + c >= ys - 1e-9)
