"""Exact 1D engine for the exact-gap model (written for this recheck; no author code used).

Instance: m = H - alpha*y^2 on [L, U], where H is piecewise linear through the knots xs.
For a node B = [l, u], phi_B(y) = m(y) - alpha*(y - l)*(u - y) = H(y) - alpha*(l + u)*y + alpha*l*u,
which is linear between consecutive points of {l, u} U (knots inside (l, u)).  So node values,
minimizers, delta-minimizer sets and greedy certificates are exact rationals.

B is valid (pruned) at tolerance eps - d iff min_B phi_B >= d.
"""
from fractions import Fraction as Fr
import bisect


class PL1D:
    def __init__(self, xs, ms, alpha=Fr(1)):
        assert all(a < b for a, b in zip(xs, xs[1:]))
        self.xs = [Fr(x) for x in xs]
        self.alpha = Fr(alpha)
        self.Hs = [Fr(m) + self.alpha * x * x for x, m in zip(self.xs, ms)]
        self.L, self.U = self.xs[0], self.xs[-1]

    def H(self, y):
        xs, Hs = self.xs, self.Hs
        i = bisect.bisect_right(xs, y) - 1
        if i >= len(xs) - 1:
            return Hs[-1]
        t = (y - xs[i]) / (xs[i + 1] - xs[i])
        return Hs[i] + t * (Hs[i + 1] - Hs[i])

    def m(self, y):
        return self.H(y) - self.alpha * y * y

    def phi(self, l, u, y):
        return self.m(y) - self.alpha * (y - l) * (u - y)

    def pts(self, l, u):
        i = bisect.bisect_right(self.xs, l)
        j = bisect.bisect_left(self.xs, u)
        return [l] + self.xs[i:j] + [u]

    def profile(self, l, u):
        p = self.pts(l, u)
        return p, [self.phi(l, u, y) for y in p]

    def minphi(self, l, u):
        return min(self.profile(l, u)[1])

    def minimizer_choices(self, l, u):
        """All exact minimizers among breakpoints, plus the midpoint of every flat minimal segment."""
        p, v = self.profile(l, u)
        mn = min(v)
        ch = [y for y, w in zip(p, v) if w == mn]
        for a, b, va, vb in zip(p, p[1:], v, v[1:]):
            if va == mn and vb == mn:
                ch.append((a + b) / 2)
        return sorted(set(ch))

    def delta_choices(self, l, u, delta, require_negative=False):
        """Interior points y with phi(y) <= min + delta: breakpoints in the sublevel set and the
        endpoints (level crossings) of each sublevel interval.  With require_negative, only points
        with phi < 0 are allowed (Corollary 1(b)); crossings are then taken at a negative level."""
        p, v = self.profile(l, u)
        mn = min(v)
        lev = mn + delta
        if require_negative and lev >= 0:
            lev = mn / 1000          # a negative level inside {phi < 0}
        ch = set(y for y, w in zip(p, v) if w <= lev)
        for a, b, va, vb in zip(p, p[1:], v, v[1:]):
            if (va - lev) * (vb - lev) < 0:
                ch.add(a + (lev - va) * (b - a) / (vb - va))
        ch = [y for y in ch if l < y < u]
        if require_negative:
            ch = [y for y in ch if self.phi(l, u, y) < 0]
        return sorted(ch)

    def greedy(self, d=Fr(0)):
        """Least certificate size at tolerance eps - d (left greedy, exact) and its breakpoints."""
        a, cnt, bps = self.L, 0, []
        while True:
            cnt += 1
            b = self.U
            for k, H in zip(self.xs, self.Hs):
                if a < k < self.U:
                    mk = H - self.alpha * k * k - d
                    assert mk > 0
                    b = min(b, k + mk / (self.alpha * (k - a)))
            if b >= self.U:
                return cnt, bps
            bps.append(b)
            a = b

    def valid(self, l, u, d=Fr(0)):
        return self.minphi(l, u) >= d

    def worst_tree(self, choices, d_valid=Fr(0), cap=10 ** 5):
        """Largest tree over all choice sequences; choices(l, u) lists allowed split points."""
        memo = {}
        count = [0]

        def T(l, u):
            key = (l, u)
            if key in memo:
                return memo[key]
            count[0] += 1
            if count[0] > cap:
                raise RuntimeError("node cap")
            if self.valid(l, u, d_valid):
                r = 1
            else:
                cs = choices(l, u)
                assert cs, (l, u)
                r = 1 + max(T(l, y) + T(y, u) for y in cs)
            memo[key] = r
            return r

        return T(self.L, self.U)


def upper_envelope(lines, L, U):
    """Knots and values of max_k (s_k y + c_k) on [L, U] (exact). lines: list of (slope, intercept)."""
    def val(y):
        return max(s * y + c for s, c in lines)
    cand = {Fr(L), Fr(U)}
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            (s1, c1), (s2, c2) = lines[i], lines[j]
            if s1 != s2:
                y = (c2 - c1) / (s1 - s2)
                if L < y < U:
                    cand.add(y)
    cand = sorted(cand)
    # keep only true kinks (and the ends)
    knots = [cand[0]]
    for a, b, c in zip(cand, cand[1:], cand[2:]):
        # b is a kink iff val is not affine on [a, c] through b
        if (val(b) - val(a)) * (c - b) != (val(c) - val(b)) * (b - a):
            knots.append(b)
    knots.append(cand[-1])
    return knots, [val(y) for y in knots]
