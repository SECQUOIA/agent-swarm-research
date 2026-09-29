"""Independent exact engine for separable exact-gap instances (alpha = 1), written for the
review of separable-omega.md.  Nothing is imported from the author's scripts.

A coordinate provides node(l, u) -> (F, y, w) for the interval J = [l, u]:
    phi_J(t) = m(t) - (t - l)(u - t),  F = min_J phi_J,  y = selected minimizer,
    w = (y - l)(u - y).
Coordinates:
  PL      m = H - t^2 with H piecewise linear through knots (exact Fractions).  phi_J is then
          piecewise linear, so its minimum set is a union of candidate points and flat segments.
  Quad    m = g (t - a)^2 exactly (closed form, unique minimizer).
Minimizer selections (PL only; Quad has a unique minimizer):
  "wmax"  largest w over the WHOLE minimizer set (flat segments included), then leftmost;
  "left"  leftmost minimizer;  "right"  rightmost minimizer;
  "knots" largest w among knots/endpoints only, then leftmost (what the author's code does);
  "center" midpoint of the minimizer segment (interior-point-like); falls back to "wmax".
"""
from fractions import Fraction as Fr
import bisect
import sys

sys.setrecursionlimit(1000000)


class PL:
    def __init__(self, xs, Hs, sel="wmax"):
        xs = [Fr(x) for x in xs]
        Hs = [Fr(h) for h in Hs]
        assert all(xs[k] < xs[k + 1] for k in range(len(xs) - 1))
        self.x, self.Hk = xs, Hs
        self.L, self.U = xs[0], xs[-1]
        self.sel = sel
        self.memo = {}

    @staticmethod
    def from_m(xs, ms, sel="wmax"):
        return PL(xs, [Fr(m) + Fr(x) ** 2 for x, m in zip(xs, ms)], sel)

    @staticmethod
    def from_lines(lines, L=0, U=1, sel="wmax"):
        """H = max of lines (slope, intercept) on [L, U]; knots = envelope kinks."""
        L, U = Fr(L), Fr(U)
        pts = {L, U}
        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                (a1, b1), (a2, b2) = lines[i], lines[j]
                if a1 != a2:
                    t = Fr(b2 - b1) / (a1 - a2)
                    if L < t < U:
                        pts.add(t)
        xs = sorted(pts)
        return PL(xs, [max(a * t + b for a, b in lines) for t in xs], sel)

    def convex(self):
        s = [(self.Hk[k + 1] - self.Hk[k]) / (self.x[k + 1] - self.x[k]) for k in range(len(self.x) - 1)]
        return all(s[k] <= s[k + 1] for k in range(len(s) - 1))

    def H(self, t):
        x = self.x
        k = bisect.bisect_right(x, t) - 1
        if k >= len(x) - 1:
            return self.Hk[-1]
        if k < 0:
            raise ValueError("outside")
        if x[k] == t:
            return self.Hk[k]
        return self.Hk[k] + (self.Hk[k + 1] - self.Hk[k]) * (t - x[k]) / (x[k + 1] - x[k])

    def m(self, t):
        return self.H(t) - t * t

    def node(self, l, u):
        key = (l, u)
        r = self.memo.get(key)
        if r is not None:
            return r
        i = bisect.bisect_right(self.x, l)
        j = bisect.bisect_left(self.x, u)
        cand = [l] + self.x[i:j] + [u]
        s, p = l + u, l * u
        vals = [self.H(cand[0]) - s * cand[0] + p] + \
               [self.Hk[k] - s * self.x[k] + p for k in range(i, j)] + [self.H(u) - s * u + p]
        F = min(vals)
        idx = [k for k, v in enumerate(vals) if v == F]
        if self.sel == "left":
            y = cand[idx[0]]
        elif self.sel == "right":
            y = cand[idx[-1]]
        elif self.sel == "knots":      # largest w among candidate points only, then leftmost
            y = max((cand[k] for k in idx), key=lambda t: ((t - l) * (u - t), -t))
        elif self.sel == "center" and all(vals[k] == F for k in range(idx[0], idx[-1] + 1)):
            y = (cand[idx[0]] + cand[idx[-1]]) / 2   # midpoint of the (single) minimizer segment
        else:
            best = None
            mid = s / 2
            for k in idx:
                pts = [cand[k]]
                if k + 1 < len(cand) and vals[k + 1] == F:   # flat segment [cand[k], cand[k+1]]
                    pts.append(min(max(mid, cand[k]), cand[k + 1]))
                for t in pts:
                    w = (t - l) * (u - t)
                    if best is None or w > best[0] or (w == best[0] and t < best[1]):
                        best = (w, t)
            y = best[1]
        r = (F, y, (y - l) * (u - y))
        self.memo[key] = r
        return r

    def maxvalid(self, a, b, U=None):
        """largest u in (a, U] with F([a, u]) >= -b (exact; b > 0, m >= -b assumed on knots)."""
        U = self.U if U is None else U
        cur = U
        k = bisect.bisect_right(self.x, a)
        while k < len(self.x) and self.x[k] < cur:
            t = self.x[k]
            v = t + (self.Hk[k] - t * t + b) / (t - a)
            if v < cur:
                cur = v
            k += 1
        return cur

    def ncert(self, b, A=None):
        """least number of pieces of A = [l, u] valid at budget b (greedy, exact)."""
        l, u = (self.L, self.U) if A is None else A
        n, a = 0, l
        while True:
            n += 1
            a = self.maxvalid(a, b, u)
            if a >= u:
                return n


class Quad:
    """m = g (t - a)^2 on [L, U], exact node data."""

    def __init__(self, a, g=1, L=0, U=1):
        self.a, self.g, self.L, self.U = Fr(a), Fr(g), Fr(L), Fr(U)
        self.memo = {}

    def m(self, t):
        return self.g * (t - self.a) ** 2

    def phi(self, l, u, t):
        return self.m(t) - (t - l) * (u - t)

    def node(self, l, u):
        key = (l, u)
        r = self.memo.get(key)
        if r is not None:
            return r
        t = (2 * self.g * self.a + l + u) / (2 * (self.g + 1))
        t = min(max(t, l), u)
        r = (self.phi(l, u, t), t, (t - l) * (u - t))
        self.memo[key] = r
        return r

    def valid(self, l, u, b):
        return self.node(l, u)[0] >= -b

    def ncert_bounds(self, b, A=None, bits=80):
        """certified bracket (lo, hi) for the least number of pieces valid at budget b.
        The greedy map a -> max{u : [a,u] valid} is nondecreasing (validity is hereditary).
        Bisection gives u_lo <= u*(a) <= u_hi; iterating u_lo gives a valid partition (hi),
        iterating u_hi dominates the true greedy sequence (lo)."""
        l, u = (self.L, self.U) if A is None else A
        res = []
        for use_hi in (False, True):
            n, a = 0, l
            while True:
                n += 1
                if self.valid(a, u, b):
                    break
                lo_, hi_ = a, u   # lo_ valid (degenerate), hi_ invalid
                for _ in range(bits):
                    md = (lo_ + hi_) / 2
                    if self.valid(a, md, b):
                        lo_ = md
                    else:
                        hi_ = md
                a = hi_ if use_hi else lo_
                if a >= u:
                    break
            res.append(n)
        return res[1], res[0]


def sharp(c, sigma=2, L=0, U=1, sel="wmax"):
    """m = sigma |t - c| - (t - c)^2, H = sigma |t - c| + 2 c t - c^2 (knot at c)."""
    c, sigma, L, U = Fr(c), Fr(sigma), Fr(L), Fr(U)
    xs = [L, c, U] if L < c < U else [L, U]
    return PL(xs, [sigma * abs(x - c) + 2 * c * x - c * c for x in xs], sel)


def dyadic_caps(K, sel="wmax"):
    """g = 0 at 0 and 2^-k (k = 0..K), cap (t - s_{k+1})(s_k - t) on each cell; truncated at K."""
    xs = [Fr(0)] + [Fr(1, 2 ** k) for k in range(K, -1, -1)]
    return PL(xs, [x * x for x in xs], sel)


# ---------------------------------------------------------------- n-dimensional runs
def run(coords, eps, rule="omega", tie="low", cap=10 ** 6, record=False):
    """Simulate a minimizer rule on a separable instance.  Returns dict with nodes, leaves,
    internal = list of (box, split coord, phase id) if record."""
    n = len(coords)
    order = list(range(n)) if tie == "low" else list(range(n - 1, -1, -1))
    rank = {k: order.index(k) for k in range(n)}
    root = tuple((c.L, c.U) for c in coords)
    st = [(root, None, None)]
    nodes = leaves = 0
    internal, leafboxes = [], []
    nph = 0
    while st:
        box, pc, ph = st.pop()
        nodes += 1
        if nodes > cap:
            return None
        d = [c.node(*iv) for c, iv in zip(coords, box)]
        if sum(x[0] for x in d) + eps >= 0:
            leaves += 1
            if record:
                leafboxes.append(box)
            continue
        if rule == "omega":
            i = max(range(n), key=lambda k: (d[k][2], -rank[k]))
        elif rule == "deficit":
            cand = [k for k in range(n) if d[k][2] > 0]
            i = min(cand, key=lambda k: (d[k][0], rank[k]))
        else:
            raise ValueError(rule)
        l, u = box[i]
        y = d[i][1]
        assert l < y < u, (box, i, d)
        if i != pc:
            nph += 1
            ph = nph
        if record:
            internal.append((box, i, ph, tuple(x[1] for x in d)))
        b1 = list(box); b1[i] = (l, y)
        b2 = list(box); b2[i] = (y, u)
        st.append((tuple(b2), i, ph))
        st.append((tuple(b1), i, ph))
    out = dict(nodes=nodes, leaves=leaves, phases=nph)
    if record:
        out["internal"], out["leafboxes"] = internal, leafboxes
    return out


def opt_min2(c1, c2, eps, cap=2 * 10 ** 6):
    """least leaves of any tree that splits every invalid node at its relaxation minimizer
    along a coordinate with w > 0 (offline choice), 2D."""
    memo = {}

    def V(I, J):
        k = (I, J)
        r = memo.get(k)
        if r is not None:
            return r
        if len(memo) > cap:
            raise OverflowError
        a, b = c1.node(*I), c2.node(*J)
        if a[0] + b[0] + eps >= 0:
            memo[k] = 1
            return 1
        best = None
        if a[2] > 0:
            best = V((I[0], a[1]), J) + V((a[1], I[1]), J)
        if b[2] > 0:
            v = V(I, (J[0], b[1])) + V(I, (b[1], J[1]))
            best = v if best is None else min(best, v)
        memo[k] = best
        return best
    try:
        return V((c1.L, c1.U), (c2.L, c2.U))
    except OverflowError:
        return None


# ---------------------------------------------------------------- 1D trees
def rmin_tree(c, A, b, cap=10 ** 6):
    """R_min tree of A stopped at budget b: returns (internal nodes, leaves)."""
    internal, leaves, st = [], [], [A]
    while st:
        J = st.pop()
        F, y, w = c.node(*J)
        if F < -b:
            assert w > 0
            internal.append(J)
            if len(internal) > cap:
                return None
            st += [(J[0], y), (y, J[1])]
        else:
            leaves.append(J)
    return internal, leaves


def pruned_tree(c, A, beta, tau, strict=False, cap=10 ** 6):
    """S(A; beta, tau): split D iff F(D) < -beta and w(D) >= tau (> tau if strict)."""
    S, st = [], [A]
    while st:
        D = st.pop()
        F, y, w = c.node(*D)
        if F < -beta and (w > tau if strict else w >= tau) and w > 0:
            S.append(D)
            if len(S) > cap:
                return None
            st += [(D[0], y), (y, D[1])]
    return S
