"""Integral lower bounds and RLCT asymptotics for the test instances.

For each instance and eps, compute
  I_d(eps) = integral over a face (or X0) of (m + eps)^(-d/2)
by nested adaptive quadrature, the proved lower bound
  (alpha d / pi^2)^(d/2) I_d(eps)            (Theorem 3.1 of the note),
and the ratio of I_d(eps) to its predicted leading term
  c_V Gamma(1+lam) Gamma(d/2-lam)/Gamma(d/2) eps^(lam-d/2) log(1/eps)^(theta-1)
(Lemma 2.2 of the note), where V(t) ~ c_V t^lam log(1/t)^(theta-1).
Usage: python3 integrals.py > logs/integrals.log
"""
import math

import numpy as np
from scipy.integrate import quad

import instances

Q = dict(limit=400, epsabs=0.0, epsrel=1e-9)


def I_xy2(e, a=0.9, b=1.3):
    se = math.sqrt(e)

    def h(x):
        ax = abs(x)
        if ax < 1e-14:
            return (a + b) / e
        return (math.atan(b * ax / se) + math.atan(a * ax / se)) / (ax * se)
    return quad(h, -a, 0, **Q)[0] + quad(h, 0, b, **Q)[0]


def I_rrr(e, delta, a=0.9, b=1.3):
    se = math.sqrt(e)

    def h(x):
        if abs(x) < 1e-12:
            return (a + b) / (delta * delta + e)
        return abs(math.atan((b * x - delta) / se) - math.atan((-a * x - delta) / se)) / (abs(x) * se)
    pts = sorted(set([0.0, delta, -delta, math.sqrt(e), -math.sqrt(e)]))
    grid = [-a] + [p for p in pts if -a < p < b] + [b]
    return sum(quad(h, grid[i], grid[i + 1], **Q)[0] for i in range(len(grid) - 1))


def I_sep24(e, a=0.9, b=1.3):
    def h(y):
        B = y ** 4 + e
        sB = math.sqrt(B)
        return (math.atan(b / sB) + math.atan(a / sB)) / sB
    s = e ** 0.25
    return quad(h, -a, -s, **Q)[0] + quad(h, -s, 0, **Q)[0] + quad(h, 0, s, **Q)[0] + quad(h, s, b, **Q)[0]


def I_cusp(e, lo=-0.45, hi=0.65):
    def inner(y):
        c = y ** 3

        def h(x):
            g = x * x - c
            return 1.0 / (g * g + e)
        pts = [lo, hi]
        if c > 0:
            r = math.sqrt(c)
            pts += [p for p in (-r, r) if lo < p < hi]
        w = math.sqrt(e) ** 0.5
        pts += [p for p in (-w, w, 0.0) if lo < p < hi]
        pts = sorted(set(pts))
        return sum(quad(h, pts[i], pts[i + 1], **Q)[0] for i in range(len(pts) - 1))
    s = e ** (1 / 6)
    pts = sorted(set([lo, -s, 0.0, s, hi] + [p for p in (s * 10, s / 10) if lo < p < hi]))
    return sum(quad(inner, pts[i], pts[i + 1], **Q)[0] for i in range(len(pts) - 1))


_G_cache = {}


def G(T):
    """integral_0^T (1+u^4)^(-3/2) du."""
    return quad(lambda u: (1 + u ** 4) ** -1.5, 0, T, limit=200)[0]


def I_xy2z4(e, a=0.9, b=1.3):
    # integrate z in closed form through G, then (y, x) by quadrature
    Tgrid = np.concatenate([[0.0], np.logspace(-4, 6, 400)])
    Gv = np.array([G(t) for t in Tgrid])

    def Gi(T):
        return float(np.interp(T, Tgrid, Gv)) if T <= Tgrid[-1] else Gv[-1]

    def fz(A):
        q = A ** -0.25
        return A ** -1.25 * (Gi(b * q) + Gi(a * q))

    def inner(x):
        def h(y):
            return fz(x * x * y * y + e)
        s = math.sqrt(e) / max(abs(x), 1e-300)
        pts = sorted(set([-a, 0.0, b] + [p for p in (-s, s) if -a < p < b]))
        return sum(quad(h, pts[i], pts[i + 1], **Q)[0] for i in range(len(pts) - 1))
    s = math.sqrt(e)
    pts = sorted(set([-a, -s, 0.0, s, b]))
    return sum(quad(inner, pts[i], pts[i + 1], limit=400, epsrel=1e-7)[0] for i in range(len(pts) - 1))


def I_bdry2(e):
    def inner(y):
        return quad(lambda x: 1.0 / (x * (1 - x) + y ** 4 + e), 0, 0.9, points=[min(0.9, 10 * e)], **Q)[0]
    s = e ** 0.25
    return quad(inner, -0.4, 0, points=[-s], **Q)[0] + quad(inner, 0, 0.5, points=[s], **Q)[0]


def I_bdry_edge(e):
    s = e ** 0.25
    h = lambda y: (y ** 4 + e) ** -0.5
    return quad(h, -0.4, 0, points=[-s], **Q)[0] + quad(h, 0, 0.5, points=[s], **Q)[0]


def lead(cV, lam, theta, d, e):
    if lam < d / 2:
        return cV * math.gamma(1 + lam) * math.gamma(d / 2 - lam) / math.gamma(d / 2) \
            * e ** (lam - d / 2) * math.log(1 / e) ** (theta - 1)
    raise ValueError


K4 = quad(lambda w: math.sqrt(1 - w ** 4), -1, 1)[0]          # area constant
A_cusp = (quad(lambda y: 2 * math.sqrt(y ** 3 + 1), -1, 1)[0]
          + quad(lambda y: 2 * (math.sqrt(y ** 3 + 1) - math.sqrt(y ** 3 - 1)), 1, math.inf, limit=400)[0])
W4 = quad(lambda w: (1 + w ** 4) ** -0.5, -math.inf, math.inf)[0]


def table(name, f, d, alpha, cV, lam, theta, eps_list):
    print(f"\n== {name}: d = {d}, alpha = {alpha:.4g}, predicted (lam, theta) = ({lam:.4g}, {theta}), "
          f"exponent d/2 - lam = {d / 2 - lam:.4g}, c_V = {cV:.5g}")
    print(f"{'eps':>9} {'I(eps)':>13} {'lower bound':>12} {'local slope':>11} {'I/lead':>8}")
    prev = None
    for e in eps_list:
        I = f(e)
        lb = (alpha * d / math.pi ** 2) ** (d / 2) * I
        slope = "" if prev is None else f"{math.log(I / prev[1]) / math.log(prev[0] / e):11.4f}"
        ratio = I / lead(cV, lam, theta, d, e) if cV else float("nan")
        print(f"{e:9.1e} {I:13.6g} {lb:12.5g} {slope:>11} {ratio:8.4f}")
        prev = (e, I)


def main():
    E2 = [10.0 ** (-k / 2) for k in range(2, 17)]
    print(f"constants: K4 = int_-1^1 sqrt(1-w^4) = {K4:.6f}; A_cusp = area{{|x^2-y^3|<=1}} = {A_cusp:.6f}; "
          f"W4 = int (1+w^4)^(-1/2) = {W4:.6f}")
    a = instances.get("xy2")["alpha"]
    table("xy2  m = x^2 y^2", I_xy2, 2, a, 2.0, 0.5, 2, E2)
    a = instances.get("sep24")["alpha"]
    table("sep24  m = x^2 + y^4", I_sep24, 2, a, 2 * K4, 0.75, 1, E2)
    a = instances.get("cusp")["alpha"]
    table("cusp  m = (x^2 - y^3)^2", I_cusp, 2, a, A_cusp, 5 / 12, 1, E2[:13])
    a = instances.get("xy2z4")["alpha"]
    table("xy2z4  m = x^2 y^2 + z^4", I_xy2z4, 3, a, 2 * K4, 0.75, 2, [10.0 ** (-k / 2) for k in range(2, 13)])
    a = instances.get("bdry")["alpha"]
    print("\n== bdry  m = x(1-x) + y^4 on [0,0.9]x[-0.4,0.5]: full-dimensional integral (d = 2) and edge {x=0} (d = 1)")
    print(f"{'eps':>9} {'I_2(eps)':>11} {'LB_2':>9} {'I_edge(eps)':>12} {'LB_edge':>9} {'edge slope':>10} {'I_edge*eps^(1/4)/W4':>20}")
    prev = None
    for e in [10.0 ** (-k) for k in range(1, 13)]:
        I2, I1 = I_bdry2(e), I_bdry_edge(e)
        sl = "" if prev is None else f"{math.log(I1 / prev[1]) / math.log(prev[0] / e):10.4f}"
        print(f"{e:9.1e} {I2:11.5g} {(a * 2 / math.pi ** 2) * I2:9.4g} {I1:12.6g} "
              f"{math.sqrt(a / math.pi ** 2) * I1:9.4g} {sl:>10} {I1 * e ** 0.25 / W4:20.4f}")
        prev = (e, I1)
    print("\n== rrr  m = (xy - delta)^2: I(eps) * sqrt(eps) (the log factor freezes for eps << delta^2)")
    print(f"{'eps':>9} " + " ".join(f"{'delta=' + d:>13}" for d in ["0", "1e-2", "1e-3"]) + f" {'pi*log(1/eps)':>14}")
    for e in [10.0 ** (-k / 2) for k in range(2, 19)]:
        vals = [I_rrr(e, dl) * math.sqrt(e) for dl in (0.0, 1e-2, 1e-3)]
        print(f"{e:9.1e} " + " ".join(f"{v:13.5f}" for v in vals) + f" {math.pi * math.log(1 / e):14.5f}")


if __name__ == "__main__":
    main()
