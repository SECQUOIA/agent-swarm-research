"""Exact tools for separable exact-gap instances (alpha = 1).

A coordinate is a 1D "knot instance": knots x_0 < ... < x_K (Fractions) and
values H_k of H = m + t^2 at the knots, H piecewise linear between knots.
So m = H - t^2 is a concave cap of curvature -2 on each cell.  If H is convex
the coordinate is in the convex class (f + alpha|y|^2 convex); non-convex H is
allowed (Theorem 1 of the main note does not need convexity).  m is shifted so
that min m = 0 over the root interval (min is attained at a knot).

For J = [l, u]:  phi_J(t) = m(t) - (t-l)(u-t) = H(t) - (l+u) t + l u, piecewise
linear, so min over J is attained at an interior knot or an endpoint.
  F(J) = min_J phi_J,  y_J = a minimizer,  w(J) = (y_J - l)(u - y_J).
Minimizer selection (class attribute Coord.sel; revised after the review):
  "knot": among the minimizing knots and endpoints, the one with the largest w, then the
          leftmost.  This is what all runs before the review used.  When phi_J is constant on
          a segment between knots it returns an end of that segment, not its most central point.
  "proj": the point of the whole minimizer set with the largest w, i.e. the centre of J
          projected onto the minimizer set (flat segments included).  This is the rule the
          note originally stated, and what an interior-point solver's face centre resembles.

Box B = prod J_i valid iff sum_i F_i(J_i) + eps >= 0.
Rules: omega (argmax_i w_i; ties -> lowest index), deficit (argmin_i F_i among w_i > 0).
"""
from fractions import Fraction as Fr
import bisect
import ctypes
import os
import numpy as np


class Coord:
    sel = "knot"

    def __init__(self, xs, Hs, shift=True):
        xs = [Fr(x) for x in xs]
        Hs = [Fr(h) for h in Hs]
        assert all(xs[i] < xs[i + 1] for i in range(len(xs) - 1))
        self.x = xs
        self.H = Hs
        if shift:
            mmin = min(h - x * x for x, h in zip(xs, Hs))
            self.H = [h - mmin for h in Hs]
        self.L, self.U = xs[0], xs[-1]
        self.cache = {}

    @staticmethod
    def from_m(xs, ms, shift=True):
        return Coord(xs, [Fr(m) + Fr(x) * Fr(x) for x, m in zip(xs, ms)], shift)

    def is_convex(self):
        x, H = self.x, self.H
        s = [(H[i + 1] - H[i]) / (x[i + 1] - x[i]) for i in range(len(x) - 1)]
        return all(s[i] <= s[i + 1] for i in range(len(s) - 1))

    def Hat(self, t):
        x = self.x
        i = bisect.bisect_right(x, t) - 1
        if i >= len(x) - 1:
            return self.H[-1]
        if x[i] == t:
            return self.H[i]
        return self.H[i] + (self.H[i + 1] - self.H[i]) * (t - x[i]) / (x[i + 1] - x[i])

    def m(self, t):
        return self.Hat(t) - t * t

    def node(self, l, u):
        """(F, y, w) for J = [l, u]."""
        key = (l, u, self.sel)
        r = self.cache.get(key)
        if r is not None:
            return r
        s = l + u
        lu = l * u
        i = bisect.bisect_right(self.x, l)
        j = bisect.bisect_left(self.x, u)
        best = None
        cands = [(l, self.Hat(l))] + [(self.x[k], self.H[k]) for k in range(i, j)] + [(u, self.Hat(u))]
        vals = [h - s * t + lu for t, h in cands]
        for (t, h), v in zip(cands, vals):
            w = (t - l) * (u - t)
            if best is None or v < best[0] or (v == best[0] and w > best[2]):
                best = (v, t, w)
        if self.sel == "proj":
            # minimizer set = minimizing candidates plus flat segments between consecutive ones
            vmin = best[0]
            c = (l + u) / 2
            pts = []
            for k, ((t, h), v) in enumerate(zip(cands, vals)):
                if v == vmin:
                    pts.append(t)
                    if k + 1 < len(cands) and vals[k + 1] == vmin:
                        t2 = cands[k + 1][0]
                        pts.append(min(max(c, t), t2))
            y = min(pts, key=lambda t: (abs(t - c), t))
            best = (vmin, y, (y - l) * (u - y))
        self.cache[key] = best
        return best

    def F(self, l, u):
        return self.node(l, u)[0]

    def greedy(self, b, l=None, u=None):
        """Least number of pieces of [l,u] with F >= -b (b > 0), exact; returns breakpoints."""
        l = self.L if l is None else l
        u = self.U if u is None else u
        pts = [l]
        a = l
        while True:
            cur = u
            i = bisect.bisect_right(self.x, a)
            ma = None
            while i < len(self.x) and self.x[i] < cur:
                k = self.x[i]
                mk = self.H[i] - k * k
                v = k + (mk + b) / (k - a)
                if v < cur:
                    cur = v
                i += 1
            pts.append(cur)
            if cur >= u:
                return pts
            a = cur


def run(coords, eps, rule="omega", cap=10 ** 6, record=False):
    """Simulate a minimizer rule; returns dict(nodes, leaves, internal=[(box, y, i)] if record)."""
    n = len(coords)
    root = tuple((c.L, c.U) for c in coords)
    stack = [(root, -1, 0)]
    nodes = leaves = 0
    internal = []
    leafboxes = []
    nphase = 0
    while stack:
        box, pcoord, ph = stack.pop()
        nodes += 1
        if nodes > cap:
            return None
        data = [c.node(l, u) for c, (l, u) in zip(coords, box)]
        tot = sum(d[0] for d in data) + eps
        if tot >= 0:
            leaves += 1
            if record:
                leafboxes.append(box)
            continue
        if rule == "omega":
            i = max(range(n), key=lambda k: (data[k][2], -k))
        elif rule == "deficit":
            cand = [k for k in range(n) if data[k][2] > 0]
            i = min(cand, key=lambda k: (data[k][0], k))
        else:
            raise ValueError(rule)
        y = data[i][1]
        l, u = box[i]
        assert l < y < u
        if i != pcoord:
            nphase += 1
            ph = nphase
        if record:
            internal.append((box, tuple(d[1] for d in data), i, ph))
        b1 = list(box); b1[i] = (l, y)
        b2 = list(box); b2[i] = (y, u)
        stack.append((tuple(b2), i, ph)); stack.append((tuple(b1), i, ph))
    out = dict(nodes=nodes, leaves=leaves, phases=nphase)
    if record:
        out["internal"] = internal
        out["leafboxes"] = leafboxes
    return out


_lib = None


def _load():
    global _lib
    if _lib is None:
        here = os.path.dirname(os.path.abspath(__file__))
        _lib = ctypes.CDLL(os.path.join(here, "libgdp_sep.so"))
        _lib.gdp_sep.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p,
                                 ctypes.c_double, ctypes.c_void_p]
        _lib.gdp_sep.restype = ctypes.c_int
    return _lib


def Ftab(c, g):
    G = len(g)
    T = np.full((G, G), -1e300)
    for a in range(G):
        for b in range(a + 1, G):
            T[a, b] = float(c.F(g[a], g[b]))
    return T


def guill_grid(c1, c2, g1, g2, eps, guard=1e-13, certificate=True):
    """Least guillotine certificate with cuts on grid g1 x g2 (lists of Fractions incl. ends).
    Float DP with a conservative guard, then exact verification of the reconstructed
    certificate.  Returns (N, boxes) (N=None if the grid admits no certificate)."""
    lib = _load()
    G1, G2 = len(g1), len(g2)
    assert G1 * G1 * G2 * G2 * 2 < 1.2e9, "grid too large"
    V1, V2 = Ftab(c1, g1), Ftab(c2, g2)
    N = np.zeros(G1 * G1 * G2 * G2, dtype=np.uint16)
    thr = -float(eps) + guard
    r = lib.gdp_sep(G1, G2, V1.ctypes.data, V2.ctypes.data, thr, N.ctypes.data)
    if r >= 65535:
        return None, None
    if not certificate:
        return r, None
    N = N.reshape(G1, G1, G2, G2)
    boxes = []
    st = [(0, G1 - 1, 0, G2 - 1)]
    while st:
        a, b, c, d = st.pop()
        v = N[a, b, c, d]
        if V1[a, b] + V2[c, d] >= thr:
            boxes.append((a, b, c, d))
            continue
        done = False
        for k in range(a + 1, b):
            if int(N[a, k, c, d]) + int(N[k, b, c, d]) == v:
                st += [(a, k, c, d), (k, b, c, d)]; done = True; break
        if not done:
            for k in range(c + 1, d):
                if int(N[a, b, c, k]) + int(N[a, b, k, d]) == v:
                    st += [(a, b, c, k), (a, b, k, d)]; done = True; break
        assert done
    assert len(boxes) == r
    for a, b, c, d in boxes:  # exact verification
        assert c1.F(g1[a], g1[b]) + c2.F(g2[c], g2[d]) + eps >= 0, "float DP accepted an invalid box"
    return r, [((g1[a], g1[b]), (g2[c], g2[d])) for a, b, c, d in boxes]


def product_bound(c1, c2, eps, splits=64):
    """min over eps1 + eps2 = eps (sampled) of N1(eps1) N2(eps2), exact 1D greedy."""
    best = None
    for k in range(1, splits):
        e1 = eps * Fr(k, splits)
        e2 = eps - e1
        v = (len(c1.greedy(e1)) - 1) * (len(c2.greedy(e2)) - 1)
        best = v if best is None else min(best, v)
    return best


def slice_bound(coords, eps):
    return max(len(c.greedy(eps)) - 1 for c in coords)


def opt_min(c1, c2, eps, cap=400000):
    """Least number of leaves of any tree that splits every invalid node at its relaxation
    minimizer along some coordinate i with w_i > 0 (the best 'minimizer rule', offline).
    Memoized DP over pairs of 1D R_min-tree nodes.  Returns None past cap states."""
    import sys
    sys.setrecursionlimit(100000)
    memo = {}

    def V(I, J):
        key = (I, J)
        r = memo.get(key)
        if r is not None:
            return r
        if len(memo) > cap:
            raise OverflowError
        d1, d2 = c1.node(*I), c2.node(*J)
        if d1[0] + d2[0] + eps >= 0:
            memo[key] = 1
            return 1
        best = None
        if d1[2] > 0:
            y = d1[1]
            v = V((I[0], y), J) + V((y, I[1]), J)
            best = v
        if d2[2] > 0:
            y = d2[1]
            v = V(I, (J[0], y)) + V(I, (y, J[1]))
            best = v if best is None else min(best, v)
        memo[key] = best
        return best
    try:
        return V((c1.L, c1.U), (c2.L, c2.U))
    except OverflowError:
        return None


class QuadCoord:
    """Exact coordinate m(t) = g (t - a)^2 on [L, U] (strictly convex phi, unique minimizer)."""

    def __init__(self, a, g=1, L=0, U=1):
        self.a, self.g, self.L, self.U = Fr(a), Fr(g), Fr(L), Fr(U)
        self.cache = {}

    def m(self, t):
        return self.g * (t - self.a) ** 2

    def node(self, l, u):
        key = (l, u)
        r = self.cache.get(key)
        if r is not None:
            return r
        g, a = self.g, self.a
        t = (2 * g * a + l + u) / (2 * (g + 1))
        t = min(max(t, l), u)
        r = (g * (t - a) ** 2 - (t - l) * (u - t), t, (t - l) * (u - t))
        self.cache[key] = r
        return r

    def F(self, l, u):
        return self.node(l, u)[0]

    def _reach(self, l, b, u_max, bits=70):
        """largest u in (l, u_max] with F([l,u]) >= -b, bracketed by bisection: (lo, hi)."""
        if self.F(l, u_max) >= -b:
            return u_max, u_max
        lo, hi = l, u_max
        for _ in range(bits):
            mid = (lo + hi) / 2
            mid = Fr(mid.numerator, mid.denominator)
            if self.F(l, mid) >= -b:
                lo = mid
            else:
                hi = mid
        return lo, hi

    def greedy(self, b, l=None, u=None):
        """Breakpoints of a greedy partition whose pieces are exactly valid at budget b
        (upper bound on N); greedy_count_bracket gives a certified bracket."""
        l = self.L if l is None else l
        u = self.U if u is None else u
        pts = [l]
        a = l
        while a < u:
            lo, _ = self._reach(a, b, u)
            pts.append(lo)
            a = lo
        return pts

    def greedy_count_bracket(self, b):
        """(N_low, N_high): N_high from exactly valid pieces; N_low from pieces extended to the
        invalid side of the bisection bracket (each longer than any valid piece from its start)."""
        n_hi = len(self.greedy(b)) - 1
        a, n_lo = self.L, 0
        while a < self.U:
            _, hi = self._reach(a, b, self.U)
            n_lo += 1
            a = hi
        return n_lo, n_hi
