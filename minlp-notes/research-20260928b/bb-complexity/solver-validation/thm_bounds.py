"""Theorem B lower bounds for instances where SCIP's relaxation has the
(G_alpha) form with known per-coordinate constants alpha_i:

  #leaves >= (n/pi^2)^(n/2) prod_i alpha_i^(1/2) * integral (f - f* + eps)^(-n/2) dx

alpha_i is the secant coefficient of the concave quadratic term in x_i as
SCIP sees it after simplification (see transformed/*.cip); other terms
(outer approximation of convex parts, McCormick of x1*x2 in linediag2,
secant of 2 y^4 in lineaxis2) only add nonnegative gap. Quadrature is
floating-point (scipy.quad), not certified.

Usage: python3 thm_bounds.py > results/thm_bounds.json
"""
import json
import math
import sys

from scipy.integrate import quad

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from instances import INSTANCES  # noqa: E402
from sweep import EPS  # noqa: E402


def hc(c):
    return lambda s: (s - 1) ** 2 * ((s + 1) ** 2 + c)


def q1d(g, lo, hi, pts, eps, power):
    pts = [p for p in pts if lo < p < hi]
    return quad(lambda x: (g(x) + eps) ** (-power), lo, hi, points=pts or None,
                limit=1000, epsabs=0, epsrel=1e-9)[0]


def sep2(g1, g2, b1, b2, p1, p2, eps):
    inner = lambda x1: q1d(lambda x2: g1(x1) + g2(x2), b2[0], b2[1], [p2], eps, 1.0)  # noqa: E731
    pts = [p for p in [p1] if b1[0] < p < b1[1]]
    return quad(inner, b1[0], b1[1], points=pts, limit=1000, epsabs=0, epsrel=1e-7)[0]


def integral(name, eps):
    b = INSTANCES[name]["bounds"]
    if name == "qflat1":
        return q1d(lambda x: 2 * x ** 4, *b[0], [0.0], eps, 0.5)
    if name in ("iso2", "iso2c"):
        if name == "iso2":
            return sep2(hc(0.5), hc(0.7), b[0], b[1], 1.0, 1.0, eps)
        g = lambda x1, x2: hc(0.5)(x1) + hc(0.7)(x2) + 0.5 * (x1 - x2) ** 4  # noqa: E731
        inner = lambda x1: quad(lambda x2: 1 / (g(x1, x2) + eps), *b[1], points=[1.0],  # noqa: E731
                                limit=1000, epsabs=0, epsrel=1e-9)[0]
        return quad(inner, *b[0], points=[1.0], limit=1000, epsabs=0, epsrel=1e-7)[0]
    if name == "linediag2":
        (l1, u1), (l2, u2) = b
        width = lambda s: max(0.0, min(u2, u1 - s) - max(l2, l1 - s))  # noqa: E731
        g = hc(0.5)
        return quad(lambda s: width(s) / (g(s) + eps), l1 - u2, u1 - l2,
                    points=[1.0, l1 - l2, u1 - u2], limit=1000, epsabs=0, epsrel=1e-9)[0]
    if name == "lineaxis2":
        return (b[1][1] - b[1][0]) * q1d(hc(0.5), *b[0], [1.0], eps, 1.0)
    if name == "qflat2a":
        return sep2(hc(0.5), lambda y: 2 * y ** 4, b[0], b[1], 1.0, 0.0, eps)
    if name == "qflat2b":
        return sep2(lambda y: 2 * y ** 4, lambda y: 2 * y ** 4, b[0], b[1], 0.0, 0.0, eps)
    raise KeyError(name)


ALPHA = {"qflat1": [1.6875], "iso2": [1.5, 1.3], "iso2c": [1.5, 1.3],
         "linediag2": [1.5, 1.5], "lineaxis2": [1.5, 1.6875],
         "qflat2a": [1.5, 1.6875], "qflat2b": [1.6875, 3.0]}

if __name__ == "__main__":
    out = {}
    for name, al in ALPHA.items():
        n = len(al)
        const = (n / math.pi ** 2) ** (n / 2) * math.prod(a ** 0.5 for a in al)
        out[name] = {repr(e): const * integral(name, e) for e in EPS}
        print(name, {f"{e:.0e}": round(v, 2) for e, v in zip(EPS, out[name].values())},
              file=sys.stderr)
    print(json.dumps(out, indent=0))
