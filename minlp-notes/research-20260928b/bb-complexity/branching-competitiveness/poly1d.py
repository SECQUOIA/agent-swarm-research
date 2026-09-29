"""Exact-structure 1D simulator for spatial B&B with exact alphaBB (alpha = 1).

Instance class ("polyhedral"): H(y) = m(y) + y^2 is the piecewise-linear
interpolant of knot values (x_j, m_j + x_j^2), convex.  Between knots m is a
concave cap with m'' = -2 (the extreme allowed curvature).  Here m = f - f* + eps
(so min m = eps).  A box [l,u] is pruned iff min_{[l,u]} (m - (y-l)(u-y)) >= 0.
Because H - chord is convex piecewise linear, the minimum is at a knot or an
endpoint, and at endpoints the value is m > 0; so only interior knots matter.

Every alpha-semiconvex m is a limit of such instances, and for rules that only
see (box, relaxation minimizer, relaxation value) the adversary may assume this
form when H is convex (see competitive-branching.md, Section 7.1).
"""
import bisect
import math

import numpy as np

# nodes with relaxation value >= -TOL count as pruned (guards against rounding;
# instances used in searches keep eps >= 1e-9 >> TOL)
TOL = 1e-12


class Inst:
    def __init__(self, xs, ms):
        xs = np.asarray(xs, float)
        ms = np.asarray(ms, float)
        order = np.argsort(xs)
        self.x = xs[order]
        self.m = ms[order]
        H = self.m + self.x ** 2
        sl = np.diff(H) / np.diff(self.x)
        if np.any(np.diff(sl) < -1e-9 * (1 + np.abs(sl[1:]))):
            raise ValueError("H not convex")
        if self.m.min() <= 0:
            raise ValueError("m must be positive")
        self.xl = list(self.x)

    def node(self, l, u):
        """Return (value, minimizer) of min over interior knots of m - (y-l)(u-y)."""
        i = bisect.bisect_right(self.xl, l)
        j = bisect.bisect_left(self.xl, u)
        if j <= i:
            return math.inf, None
        xs = self.x[i:j]
        v = self.m[i:j] - (xs - l) * (u - xs)
        k = int(np.argmin(v))
        return float(v[k]), float(xs[k])

    def valid(self, l, u):
        return self.node(l, u)[0] >= 0

    def nopt(self):
        """Minimum number of valid intervals covering [0,1] (greedy is optimal)."""
        a, cnt = 0.0, 0
        x, m = self.x, self.m
        while True:
            cnt += 1
            b = 1.0
            i = bisect.bisect_right(self.xl, a)
            while i < len(x) and x[i] < b:
                k = x[i]
                b = min(b, k + m[i] / (k - a))
                i += 1
            if b >= 1.0:
                return cnt
            a = b

    def greedy_breakpoints(self):
        """Breakpoints 0 = s_0 < ... < s_N = 1 of the left-greedy (optimal) certificate."""
        a, pts = 0.0, [0.0]
        x, m = self.x, self.m
        while True:
            b = 1.0
            i = bisect.bisect_right(self.xl, a)
            while i < len(x) and x[i] < b:
                k = x[i]
                b = min(b, k + m[i] / (k - a))
                i += 1
            if b >= 1.0:
                pts.append(1.0)
                return pts
            pts.append(b)
            a = b

    def splits(self, rule, cap=10 ** 6):
        """Return the list of (l, u, split point) of all internal nodes."""
        stack, out = [(0.0, 1.0)], []
        while stack:
            l, u = stack.pop()
            v, y = self.node(l, u)
            if v >= -TOL:
                continue
            s = rule(l, u, y, v)
            out.append((l, u, s))
            if len(out) > cap:
                return None
            stack.append((l, s))
            stack.append((s, u))
        return out

    def tree(self, rule, cap=10 ** 6):
        stack = [(0.0, 1.0)]
        nodes = 0
        while stack:
            l, u = stack.pop()
            nodes += 1
            if nodes > cap:
                return None
            v, y = self.node(l, u)
            if v >= -TOL:
                continue
            s = rule(l, u, y, v)
            if not (l < s < u):
                raise RuntimeError(f"bad split {s} in ({l},{u})")
            stack.append((l, s))
            stack.append((s, u))
        return nodes


# ------------------------------------------------------------------ rules
def r_bis(l, u, y, v):
    return 0.5 * (l + u)


def r_min(l, u, y, v):
    return y


def r_clamp(theta):
    def r(l, u, y, v):
        w = u - l
        return min(max(y, l + theta * w), u - theta * w)
    return r


def r_mix(lam, theta=0.2):
    def r(l, u, y, v):
        w = u - l
        s = lam * y + (1 - lam) * 0.5 * (l + u)
        return min(max(s, l + theta * w), u - theta * w)
    return r


RULES = {
    "bis": r_bis,
    "min": r_min,
    "clamp.02": r_clamp(0.02),
    "clamp.2": r_clamp(0.2),
    "mix.8": r_mix(0.8),
}


# ------------------------------------------------------------------ instances
def convexify(xs, ms):
    """Drop knots so that H = m + x^2 is convex (lower hull); keep endpoints."""
    pts = sorted(zip(xs, ms))
    hull = []
    for x, m in pts:
        h = m + x * x
        while len(hull) >= 2:
            (x1, h1), (x2, h2) = hull[-2], hull[-1]
            if (h2 - h1) * (x - x1) >= (h - h1) * (x2 - x1):
                hull.pop()
            else:
                break
        hull.append((x, h))
    X = np.array([p[0] for p in hull])
    M = np.array([p[1] for p in hull]) - X ** 2
    return X, M


def from_function(fun, eps, K=4001, extra=(), geo=True):
    """Polyhedral instance from samples of an alpha-semiconvex m0 >= 0.

    Knots: a uniform grid plus, around each point in `extra`, a geometric grid
    (radii 1e-13..0.5, 60 per decade) so that smooth minima are resolved far
    below sqrt(eps)."""
    pts = [np.linspace(0, 1, K), np.asarray(extra, float)]
    if geo:
        r = np.geomspace(1e-13, 0.5, 60 * 13)
        for a in extra:
            pts += [a - r, a + r]
    xs = np.concatenate(pts)
    xs = np.unique(xs[(xs >= 0) & (xs <= 1)])
    ms = np.array([fun(t) for t in xs]) + eps
    X, M = convexify(xs, ms)
    M = M - M.min() + eps
    return Inst(X, M)


if __name__ == "__main__":
    a = 1.0 / 3.0
    for eps in (1e-2, 1e-5, 1e-8):
        I = from_function(lambda t: 2 * abs(t - a) - (t - a) ** 2, eps, extra=[a])
        print(eps, I.nopt(), {k: I.tree(r) for k, r in RULES.items()})


def from_lines(lines):
    """Instance with H(y) = max_i (s_i y + b_i) on [0,1]; m = H - y^2 (unshifted).

    Returns (xs, ms) of the knots of H (including 0 and 1)."""
    lines = sorted(set((float(s), float(b)) for s, b in lines))
    # upper envelope of lines over [0,1]
    env = []
    for s, b in lines:
        if env and abs(env[-1][0] - s) < 1e-300:
            if b <= env[-1][1]:
                continue
            env.pop()
        while len(env) >= 2:
            (s1, b1), (s2, b2) = env[-2], env[-1]
            # line2 useless if intersection(1,3) <= intersection(1,2)
            if (b - b1) * (s2 - s1) >= (b2 - b1) * (s - s1):
                env.pop()
            else:
                break
        env.append((s, b))
    xs = [0.0]
    for (s1, b1), (s2, b2) in zip(env, env[1:]):
        x = (b1 - b2) / (s2 - s1)
        if 0.0 < x < 1.0:
            xs.append(x)
    xs.append(1.0)
    xs = np.array(sorted(set(xs)))
    H = np.max(np.array([[s * x + b for s, b in env] for x in xs]), axis=1)
    return xs, H - xs ** 2
