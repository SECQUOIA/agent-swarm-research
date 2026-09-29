"""Toy spatial branch-and-bound node counts versus tolerance (scout scratch).

Scheme: alphaBB lower bound LB(B) = min_{y in B} f(y) - alpha * q_B(y),
q_B(y) = sum_i (y_i - l_i)(u_i - y_i), with alpha >= max(0, -min eig(Hess f)/2)
on the root box, so the node problem is convex.  The incumbent is fixed at the
known optimum f*, so the set of processed nodes does not depend on node order.
A box is pruned when LB(B) >= f* - eps.

LB is computed as phi(y) + min_{z in B} grad phi(y).(z - y) at an approximate
minimizer y of the convex phi (Frank-Wolfe bound), which is a valid lower bound
up to floating-point error.  This is an uncertified illustration.

Also: exact minimum certificate size in 1D (greedy interval cover, optimal
because validity is inherited by subintervals), and the integral lower bound
(alpha n / pi^2)^{n/2} * int (f - f* + eps)^{-n/2} of the scout report.
"""
import math
import sys
import json
import numpy as np
from scipy.optimize import minimize
from scipy import integrate


class Problem:
    def __init__(self, name, n, lo, hi, f, grad, alpha, fstar, argmin_hint=None):
        self.name, self.n = name, n
        self.lo, self.hi = np.array(lo, float), np.array(hi, float)
        self.f, self.grad, self.alpha, self.fstar = f, grad, alpha, fstar



def lb_1d(phi, dphi, l, u):
    """Valid lower bound (up to rounding) for a convex phi on [l, u], plus a near-minimizer."""
    if dphi(l) >= 0:
        return phi(l), np.array([l])
    if dphi(u) <= 0:
        return phi(u), np.array([u])
    lo_, hi_ = l, u
    for _ in range(200):
        mid = 0.5 * (lo_ + hi_)
        if mid <= lo_ or mid >= hi_:
            break
        if dphi(mid) > 0:
            hi_ = mid
        else:
            lo_ = mid
    # on [lo_, hi_] phi >= each tangent; the minimum over the bracket is at least
    # the smaller of the two tangent values at the opposite end
    b = min(phi(lo_) + dphi(lo_) * (hi_ - lo_), phi(hi_) + dphi(hi_) * (lo_ - hi_))
    b = min(b, phi(lo_), phi(hi_))
    y = lo_ if phi(lo_) <= phi(hi_) else hi_
    return b, np.array([y])

def node_lb(P, l, u):
    a = P.alpha

    def phi(y):
        return P.f(y) - a * np.sum((y - l) * (u - y))

    def dphi(y):
        return P.grad(y) - a * (u + l - 2 * y)

    if P.n == 1:
        return lb_1d(lambda z: phi(np.array([z])), lambda z: dphi(np.array([z]))[0], l[0], u[0])
    if getattr(P, "sep", None) is not None:
        # separable f = sum_i h_i(y_i): phi is separable; solve each coordinate exactly
        tot, ys = 0.0, []
        for i, (h, dh) in enumerate(P.sep):
            li, ui = l[i], u[i]
            v, yi = lb_1d(lambda z: h(z) - a * (z - li) * (ui - z),
                          lambda z: dh(z) - a * (ui + li - 2 * z), li, ui)
            tot += v; ys.append(yi[0])
        return tot, np.array(ys)
    best = None
    starts = [0.5 * (l + u)]
    for y0 in starts:
        r = minimize(phi, y0, jac=dphi, method="L-BFGS-B",
                     bounds=list(zip(l, u)),
                     options={"ftol": 1e-15, "gtol": 1e-13, "maxiter": 500})
        y = np.clip(r.x, l, u)
        g = dphi(y)
        fw = phi(y) + np.sum(np.minimum(g * (l - y), g * (u - y)))
        if best is None or fw > best[0]:
            best = (fw, y)
    return best


def count_nodes(P, eps, rule="bisect", theta=0.02, max_nodes=400000):
    stack = [(P.lo.copy(), P.hi.copy())]
    nodes = 0
    a = P.alpha
    while stack:
        l, u = stack.pop()
        nodes += 1
        if nodes > max_nodes:
            return None
        lb, y = node_lb(P, l, u)
        if lb >= P.fstar - eps:
            continue
        w = u - l
        if rule == "bisect":
            i = int(np.argmax(w))
            s = 0.5 * (l[i] + u[i])
        elif rule == "xonly":          # branch only on coordinate 0 (bisection)
            i = 0
            s = 0.5 * (l[i] + u[i])
        else:
            contrib = (y - l) * (u - y)
            i = int(np.argmax(contrib)) if contrib.max() > 0 else int(np.argmax(w))
            if rule == "omega":        # split at relaxation minimizer, safeguarded
                s = min(max(y[i], l[i] + theta * w[i]), u[i] - theta * w[i])
            elif rule == "mix":        # SCIP-like convex combination
                s = 0.8 * y[i] + 0.2 * 0.5 * (l[i] + u[i])
                s = min(max(s, l[i] + theta * w[i]), u[i] - theta * w[i])
            else:
                raise ValueError(rule)
        l1, u1 = l.copy(), u.copy(); u1[i] = s
        l2, u2 = l.copy(), u.copy(); l2[i] = s
        stack.append((l1, u1)); stack.append((l2, u2))
    return nodes


def valid_interval(P, a, b, eps):
    lb, _ = node_lb(P, np.array([a]), np.array([b]))
    return lb >= P.fstar - eps


def opt_cover_1d(P, eps, tol=1e-13):
    """Minimum number of valid intervals covering [lo, hi] (greedy is optimal)."""
    a, H = P.lo[0], P.hi[0]
    k = 0
    while a < H - 1e-15:
        k += 1
        if valid_interval(P, a, H, eps):
            return k
        lo_b, hi_b = a, H
        # find the largest valid right endpoint by bisection
        while hi_b - lo_b > tol * max(1.0, abs(H)):
            mid = 0.5 * (lo_b + hi_b)
            if valid_interval(P, a, mid, eps):
                lo_b = mid
            else:
                hi_b = mid
        if lo_b <= a + 1e-15:
            return None
        a = lo_b
        if k > 100000:
            return None
    return k


def integral_lb(P, eps, grid=None, pts=None):
    n, al = P.n, P.alpha
    c = (al * n / math.pi ** 2) ** (n / 2)
    if n == 1:
        g = lambda t: (P.f(np.array([t])) - P.fstar + eps) ** (-0.5)
        val, _ = integrate.quad(g, P.lo[0], P.hi[0], points=pts, limit=500)
        return c * val
    # 2D: adaptive nested quadrature with breakpoints
    g = lambda y2, y1: (P.f(np.array([y1, y2])) - P.fstar + eps) ** (-1.0)
    opts = {"limit": 200, "points": pts[1] if pts else None}
    opts0 = {"limit": 200, "points": pts[0] if pts else None}
    val, _ = integrate.nquad(lambda y2, y1: g(y2, y1),
                             [[P.lo[1], P.hi[1]], [P.lo[0], P.hi[0]]],
                             opts=[opts, opts0])
    return c * val


# ---------------------------------------------------------------- problems
A1 = 1.0 / 3.0
A2 = np.array([1.0 / 3.0, 0.4142135623730951])


def p_nondeg1():
    f = lambda y: float((y[0] - A1) ** 2 - 2 * (y[0] - A1) ** 4)
    g = lambda y: np.array([2 * (y[0] - A1) - 8 * (y[0] - A1) ** 3])
    tmax = 2.0 / 3.0
    alpha = max(0.0, -(2 - 24 * tmax ** 2) / 2)
    return Problem("1D nondegenerate t^2-2t^4", 1, [0], [1], f, g, alpha, 0.0)


def p_quartic1():
    f = lambda y: float((y[0] - A1) ** 4 * (1 - (y[0] - A1) ** 2))
    g = lambda y: np.array([4 * (y[0] - A1) ** 3 - 6 * (y[0] - A1) ** 5])
    ts = np.linspace(-A1, 1 - A1, 20001)
    alpha = max(0.0, -np.min(12 * ts ** 2 - 30 * ts ** 4) / 2)
    return Problem("1D quartic t^4(1-t^2)", 1, [0], [1], f, g, alpha, 0.0)


def p_sharp1():
    f = lambda y: float(2 * abs(y[0] - A1) - (y[0] - A1) ** 2)
    g = lambda y: np.array([2 * np.sign(y[0] - A1) - 2 * (y[0] - A1)])
    return Problem("1D sharp 2|t|-t^2", 1, [0], [1], f, g, 1.0, 0.0)


def p_nondeg2():
    def f(y):
        t = y - A2; r2 = t @ t
        return float(r2 - 0.5 * r2 ** 2)

    def g(y):
        t = y - A2; r2 = t @ t
        return 2 * t - 2 * r2 * t
    # Hessian of r2 - 0.5 r2^2: (2 - 2 r2) I - 4 t t^T; min eig 2 - 6 r2
    corners = np.array([[0, 0], [0, 1], [1, 0], [1, 1]]) - A2
    r2max = max(c @ c for c in corners)
    alpha = max(0.0, -(2 - 6 * r2max) / 2)
    return Problem("2D nondegenerate |t|^2-|t|^4/2", 2, [0, 0], [1, 1], f, g, alpha, 0.0)


def p_ring2(r=0.2):
    def f(y):
        t = y - A2; r2 = t @ t
        return float((r2 - r * r) ** 2)

    def g(y):
        t = y - A2; r2 = t @ t
        return 4 * (r2 - r * r) * t
    return Problem("2D ring (|t|^2-r^2)^2, r=0.2", 2, [0, 0], [1, 1], f, g, 2 * r * r, 0.0)


def p_sharp2():
    def f(y):
        t = y - A2
        return float(2 * np.abs(t).sum() - t @ t)

    def g(y):
        t = y - A2
        return 2 * np.sign(t) - 2 * t
    P = Problem("2D sharp 2|t|_1-|t|^2", 2, [0, 0], [1, 1], f, g, 1.0, 0.0)
    P.sep = [(lambda z, c=c: 2 * abs(z - c) - (z - c) ** 2,
              lambda z, c=c: 2 * np.sign(z - c) - 2 * (z - c)) for c in A2]
    return P


def p_mixed2():
    # growth t1^2 + t2^4 near the minimizer; nonconvexity from -2.5 t2^6 away from it
    c0, c1 = A2

    def f(y):
        t = y - A2
        return float(t[0] ** 2 + t[1] ** 4 - 2.5 * t[1] ** 6)

    def g(y):
        t = y - A2
        return np.array([2 * t[0], 4 * t[1] ** 3 - 15.0 * t[1] ** 5])
    ts = np.linspace(-c1, 1 - c1, 20001)
    alpha = max(0.0, -np.min(12 * ts ** 2 - 75.0 * ts ** 4) / 2)
    P = Problem("2D mixed t1^2+t2^4-2.5t2^6", 2, [0, 0], [1, 1], f, g, alpha, 0.0)
    P.sep = [(lambda z: (z - c0) ** 2, lambda z: 2 * (z - c0)),
             (lambda z: (z - c1) ** 4 - 2.5 * (z - c1) ** 6,
              lambda z: 4 * (z - c1) ** 3 - 15.0 * (z - c1) ** 5)]
    return P


PROBLEMS = {"nondeg1": p_nondeg1, "quartic1": p_quartic1, "sharp1": p_sharp1,
            "nondeg2": p_nondeg2, "ring2": p_ring2, "sharp2": p_sharp2,
            "mixed2": p_mixed2}


def main():
    which = sys.argv[1:] or list(PROBLEMS)
    out = {}
    for key in which:
        P = PROBLEMS[key]()
        print(f"== {P.name}: alpha={P.alpha:.4g}", flush=True)
        rows = []
        for k in range(2, 9):
            eps = 10.0 ** (-k)
            row = {"eps": eps}
            for rule in ("bisect", "omega", "mix"):
                row[rule] = count_nodes(P, eps, rule)
            if P.n == 1:
                row["opt_leaves"] = opt_cover_1d(P, eps)
                pts = [A1]
            else:
                pts = [[A2[0]], [A2[1]]]
            try:
                row["int_lb_leaves"] = integral_lb(P, eps, pts=pts)
            except Exception as e:  # noqa
                row["int_lb_leaves"] = None
            rows.append(row)
            print(json.dumps(row), flush=True)
        out[key] = {"name": P.name, "alpha": P.alpha, "rows": rows}
    with open("sbb_toy_results_" + "_".join(which) + ".json", "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
