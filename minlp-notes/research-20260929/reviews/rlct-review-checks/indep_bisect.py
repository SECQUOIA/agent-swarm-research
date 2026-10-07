"""Referee's independent re-implementation of uniform 2^n-ary dyadic bisection
with exact alphaBB node bounds, f_B = m - alpha q_B, UBD = f* = 0, prune iff
min_B f_B >= -eps.  Node bounds are computed differently from bisect_bb.py:
  * separable instances: exact 1D minimisation per coordinate (closed form for
    quadratics, Cardano + Newton for y^4 + alpha y^2 - ...), no iterative solver;
  * xy2 (x^2 y^2): closed-form minimisation in x for fixed y, then golden-section
    search on the convex marginal g(y) = min_x F(x, y).
Reports leaves and the number of boxes whose bound lies within 1e-10 of -eps
("near-ties").  Floating point; an independent illustration only.
Usage: python3 indep_bisect.py MODE
"""
import json
import sys

import numpy as np


def quad_min(c2, c1, alpha, l, u):
    """min over [l,u] of c2 x^2 + c1 x - alpha (x-l)(u-x); needs c2 + alpha > 0."""
    a = c2 + alpha
    b = c1 - alpha * (l + u)
    x = np.clip(-b / (2 * a), l, u)
    return a * x * x + b * x + alpha * l * u


def quart_min(alpha, l, u):
    """min over [l,u] of y^4 - alpha (y-l)(u-y) = y^4 + alpha y^2 - alpha(l+u) y + alpha l u."""
    p = alpha / 2.0
    q = -alpha * (l + u) / 4.0
    D = np.sqrt(q * q / 4 + p ** 3 / 27)
    y = np.cbrt(-q / 2 + D) + np.cbrt(-q / 2 - D)
    for _ in range(3):  # Newton polish of 4y^3 + 2 alpha y - alpha(l+u) = 0
        y = y - (4 * y ** 3 + 2 * alpha * y - alpha * (l + u)) / (12 * y * y + 2 * alpha)
    y = np.clip(y, l, u)
    return y ** 4 + alpha * y * y - alpha * (l + u) * y + alpha * l * u


def xy2_min(alpha, l, u, iters=120):
    l1, u1, l2, u2 = l[:, 0], u[:, 0], l[:, 1], u[:, 1]

    def g(y):
        a = y * y + alpha
        x = np.clip(alpha * (l1 + u1) / (2 * a), l1, u1)
        return (x * y) ** 2 - alpha * (x - l1) * (u1 - x) - alpha * (y - l2) * (u2 - y)
    lo, hi = l2.copy(), u2.copy()
    r = (np.sqrt(5) - 1) / 2
    for _ in range(iters):
        c = hi - r * (hi - lo)
        d = lo + r * (hi - lo)
        gc, gd = g(c), g(d)
        left = gc <= gd
        hi = np.where(left, d, hi)
        lo = np.where(left, lo, c)
    ym = 0.5 * (lo + hi)
    return np.minimum(np.minimum(g(ym), g(l2)), g(u2))


def make(kind):
    if kind == "sep24":
        lo, side, alpha = np.array([-0.9, -0.9]), 2.2, 1.0
        fn = lambda l, u: quad_min(1.0, 0.0, alpha, l[:, 0], u[:, 0]) + quart_min(alpha, l[:, 1], u[:, 1])
    elif kind == "bdry":
        lo, side, alpha = np.array([0.0, -0.4]), 0.9, 1.05
        fn = lambda l, u: quad_min(-1.0, 1.0, alpha, l[:, 0], u[:, 0]) + quart_min(alpha, l[:, 1], u[:, 1])
    elif kind == "xy2":
        lo, side, alpha = np.array([-0.9, -0.9]), 2.2, 1.7745
        fn = lambda l, u: xy2_min(alpha, l, u)
    elif kind == "vertex_sharp":   # m = x + y - 0.4(x^2 + y^2) on [0,1]^2, optimal vertex (0,0), all inward partials 1
        lo, side, alpha = np.array([0.0, 0.0]), 1.0, 1.0
        fn = lambda l, u: quad_min(-0.4, 1.0, alpha, l[:, 0], u[:, 0]) + quad_min(-0.4, 1.0, alpha, l[:, 1], u[:, 1])
    elif kind == "vertex_sharp_a8":  # same m, alpha = 8 (valid, >= 0.4): root is not pruned
        lo, side, alpha = np.array([0.0, 0.0]), 1.0, 8.0
        fn = lambda l, u: quad_min(-0.4, 1.0, alpha, l[:, 0], u[:, 0]) + quad_min(-0.4, 1.0, alpha, l[:, 1], u[:, 1])
    elif kind == "vertex_flat":    # m = x - 0.4 x^2 + y^2 on [0,1]^2, optimal vertex (0,0), partial in y is 0
        lo, side, alpha = np.array([0.0, 0.0]), 1.0, 1.0
        fn = lambda l, u: quad_min(-0.4, 1.0, alpha, l[:, 0], u[:, 0]) + quad_min(1.0, 0.0, alpha, l[:, 1], u[:, 1])
    elif kind == "face4d":         # m = x(1-x) + y^4 + z^4 + w^4 on [0,0.9] x [-0.4,0.5]^3
        lo, side, alpha = np.array([0.0, -0.4, -0.4, -0.4]), 0.9, 1.05
        fn = lambda l, u: (quad_min(-1.0, 1.0, alpha, l[:, 0], u[:, 0]) + quart_min(alpha, l[:, 1], u[:, 1])
                           + quart_min(alpha, l[:, 2], u[:, 2]) + quart_min(alpha, l[:, 3], u[:, 3]))
    else:
        raise ValueError(kind)
    return lo, side, fn


def run(kind, eps, max_level=70):
    lo, side, fn = make(kind)
    n = lo.size
    offs = np.array(np.meshgrid(*[[0, 1]] * n, indexing="ij")).reshape(n, -1).T
    corners, s = lo[None, :].copy(), side
    nonpruned, ties = 0, 0
    per_level = []
    for _ in range(max_level):
        if corners.shape[0] == 0:
            break
        keep = np.zeros(corners.shape[0], bool)
        B = 500000
        for a in range(0, corners.shape[0], B):
            l = corners[a:a + B]
            v = fn(l, l + s)
            keep[a:a + B] = v < -eps
            ties += int(np.count_nonzero(np.abs(v + eps) <= 1e-10 * max(eps, 1e-300) + 1e-15))
        k = corners[keep]
        per_level.append(int(k.shape[0]))
        nonpruned += k.shape[0]
        s /= 2
        corners = (k[:, None, :] + s * offs[None, :, :]).reshape(-1, n)
    nodes = 1 + 2 ** n * nonpruned
    return dict(kind=kind, eps=eps, nodes=nodes, leaves=nodes - nonpruned, ties=ties, per_level=per_level)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode in ("sep24", "bdry", "xy2"):
        ref = [json.loads(x) for x in open("../../rlct/logs/sweep.jsonl")]
        ref = sorted([r for r in ref if r["instance"] == mode], key=lambda r: -r["eps"])
        if len(sys.argv) > 2:
            ref = [r for r in ref if r["eps"] >= float(sys.argv[2])]
        mism = 0
        for r in ref:
            o = run(mode, r["eps"])
            flag = "" if o["leaves"] == r["leaves"] else "  MISMATCH"
            mism += bool(flag)
            print(f"{mode:6s} eps={r['eps']:.3e} note_leaves={r['leaves']:9d} referee_leaves={o['leaves']:9d} ties={o['ties']}{flag}", flush=True)
        print(f"{mode}: {len(ref)} eps values, {mism} mismatches")
    else:
        for k in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
            e = float("%.8g" % 10 ** (-k / 2))
            o = run(mode, e)
            print(json.dumps(o), flush=True)
