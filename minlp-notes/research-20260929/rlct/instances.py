"""Test instances for the RLCT node-complexity note.

Each instance gives m = f - f* >= 0 on a cube X0 = [lo, lo + side]^n with
min m = 0, its gradient, a convexity threshold alpha0 (so that
m - alpha q_B is convex on every box for alpha >= alpha0), a bound on the
largest Hessian eigenvalue on X0 (for gradient steps), and the predicted
RLCT data.

The alpha0 values are analytic bounds; see rlct-node-complexity.md, Section 5.
"""
import numpy as np


def _xy2(y):
    x, z = y[:, 0], y[:, 1]
    v = (x * z) ** 2
    g = np.stack([2 * x * z * z, 2 * x * x * z], axis=1)
    return v, g


def _sep24(y):
    x, z = y[:, 0], y[:, 1]
    v = x * x + z ** 4
    g = np.stack([2 * x, 4 * z ** 3], axis=1)
    return v, g


def _cusp(y):
    x, z = y[:, 0], y[:, 1]
    gg = x * x - z ** 3
    v = gg * gg
    g = np.stack([2 * gg * 2 * x, 2 * gg * (-3 * z * z)], axis=1)
    return v, g


def _xy2z4(y):
    x, z, w = y[:, 0], y[:, 1], y[:, 2]
    v = (x * z) ** 2 + w ** 4
    g = np.stack([2 * x * z * z, 2 * x * x * z, 4 * w ** 3], axis=1)
    return v, g


def _bdry(y):
    x, z = y[:, 0], y[:, 1]
    v = x * (1 - x) + z ** 4
    g = np.stack([1 - 2 * x, 4 * z ** 3], axis=1)
    return v, g


def _make_rrr(delta):
    def f(y):
        x, z = y[:, 0], y[:, 1]
        gg = x * z - delta
        v = gg * gg
        g = np.stack([2 * gg * z, 2 * gg * x], axis=1)
        return v, g
    return f


# ---- instances added in the revision after review ----

def _vsharp(y):
    # m = x + y - 0.4 (x^2 + y^2) on [0,1]^2: optimal vertex, inward slopes 1
    x, z = y[:, 0], y[:, 1]
    v = x + z - 0.4 * (x * x + z * z)
    g = np.stack([1 - 0.8 * x, 1 - 0.8 * z], axis=1)
    return v, g


def _vflat(y):
    # m = x - 0.4 x^2 + y^2 on [0,1]^2: optimal vertex, slope 0 along the edge x = 0
    x, z = y[:, 0], y[:, 1]
    v = x - 0.4 * x * x + z * z
    g = np.stack([1 - 0.8 * x, 2 * z], axis=1)
    return v, g


def _rot(y):
    # m = (x+y)^2 + (x-y)^4 on [0,1]^2: zero at the corner (review item F2)
    x, z = y[:, 0], y[:, 1]
    u, w = x + z, x - z
    v = u * u + w ** 4
    gu, gw = 2 * u, 4 * w ** 3
    g = np.stack([gu + gw, gu - gw], axis=1)
    return v, g


def _face4d(y):
    # m = x(1-x) + y^4 + z^4 + w^4 on [0,0.9] x [-0.4,0.5]^3 (review item F3)
    x = y[:, 0]
    r = y[:, 1:]
    v = x * (1 - x) + np.sum(r ** 4, axis=1)
    g = np.concatenate([(1 - 2 * x)[:, None], 4 * r ** 3], axis=1)
    return v, g


# R = max |coordinate| on [-0.9, 1.3]^n is 1.3.
INSTANCES = {
    # m = x^2 y^2: RLCT (1/2, 2); exponent n/2 - lambda = 1/2, log^1.
    "xy2": dict(fun=_xy2, n=2, lo=-0.9, side=2.2, alpha0=1.69, hmax=6 * 1.69,
                lam=0.5, theta=2),
    # m = x^2 + y^4 (convex; any alpha > 0 is a valid (G^pt) scheme): RLCT (3/4, 1).
    "sep24": dict(fun=_sep24, n=2, lo=-0.9, side=2.2, alpha0=0.0, hmax=12 * 1.69,
                  lam=0.75, theta=1),
    # m = (x^2 - y^3)^2 on [-0.45, 0.65]^2: RLCT (5/12, 1); exponent 7/12.
    "cusp": dict(fun=_cusp, n=2, lo=-0.45, side=1.1, alpha0=2.72, hmax=12.5,
                 lam=5 / 12, theta=1),
    # m = x^2 y^2 + z^4 in 3D: RLCT (3/4, 2); exponent 3/4, log^1.
    "xy2z4": dict(fun=_xy2z4, n=3, lo=-0.9, side=2.2, alpha0=1.69, hmax=12 * 1.69,
                  lam=0.75, theta=2),
    # m = x(1-x) + y^4 on [0, 0.9] x [-0.4, 0.5]: minimizer on the face x = 0.
    # Full-dimensional RLCT (5/4, 1) > n/2; face {x=0}: RLCT (1/4, 1), d = 1.
    "bdry": dict(fun=_bdry, n=2, lo=np.array([0.0, -0.4]), side=0.9, alpha0=1.0,
                 hmax=12 * 0.25 + 2, lam=1.25, theta=1),
    # m = (xy - delta)^2: noisy one-parameter-pair reduced-rank regression toy.
    "rrr0": dict(fun=_make_rrr(0.0), n=2, lo=-0.9, side=2.2, alpha0=1.69,
                 hmax=6 * 1.69 + 1, lam=0.5, theta=2),
    "rrr1e-2": dict(fun=_make_rrr(1e-2), n=2, lo=-0.9, side=2.2, alpha0=1.70,
                    hmax=6 * 1.69 + 1, lam=0.5, theta=1),
    "rrr1e-3": dict(fun=_make_rrr(1e-3), n=2, lo=-0.9, side=2.2, alpha0=1.691,
                    hmax=6 * 1.69 + 1, lam=0.5, theta=1),
    # revision instances
    "vsharp": dict(fun=_vsharp, n=2, lo=0.0, side=1.0, alpha0=0.4, hmax=0.8,
                   lam=2.0, theta=1),
    "vflat": dict(fun=_vflat, n=2, lo=0.0, side=1.0, alpha0=0.4, hmax=2.0,
                  lam=1.5, theta=1),
    "rot": dict(fun=_rot, n=2, lo=0.0, side=1.0, alpha0=0.0, hmax=28.0,
                lam=1.0, theta=1),
    "face4d": dict(fun=_face4d, n=4, lo=np.array([0.0, -0.4, -0.4, -0.4]), side=0.9,
                   alpha0=1.0, hmax=3.0, lam=1.75, theta=1),
}


def get(name, alpha=None):
    d = dict(INSTANCES[name])
    n = d["n"]
    d["lo"] = np.broadcast_to(np.asarray(d["lo"], float), (n,)).copy()
    if alpha is None:
        alpha = max(1.0, 1.05 * d["alpha0"])
    assert alpha >= d["alpha0"], "alpha below the convexity threshold"
    d["alpha"] = alpha
    return d
