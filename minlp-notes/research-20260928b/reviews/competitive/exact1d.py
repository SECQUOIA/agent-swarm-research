"""Independent exact 1D simulator for spatial B&B with the exact-gap relaxation.

Reviewer code (does not import the note's scripts).  alpha = 1, root [0, 1].

Instance: knots 0 = x_0 < ... < x_K = 1 (Fractions) and values m_k > 0 with
min_k m_k = eps.  H = m + y^2 is the piecewise-linear interpolant of
(x_k, m_k + x_k^2).  H need NOT be convex: the note claims Theorem 1 needs
only continuity of f, and for piecewise-linear H every node function
phi_B(y) = m(y) - (y-l)(u-y) = H(y) - (l+u) y + l u is linear between knots,
so node values and minimizers are exact minima over the knots.

m(y) between knots is computed from the interpolant of H.
"""
from fractions import Fraction as Fr
import bisect


class Inst:
    def __init__(self, xs, ms):
        pts = sorted(zip(xs, ms))
        self.x = [Fr(p[0]) for p in pts]
        self.m = [Fr(p[1]) for p in pts]
        assert self.x[0] == 0 and self.x[-1] == 1
        assert all(a < b for a, b in zip(self.x, self.x[1:]))
        assert min(self.m) > 0
        self.eps = min(self.m)
        self.H = [mk + xk * xk for xk, mk in zip(self.x, self.m)]

    def convex(self):
        s = [(self.H[i + 1] - self.H[i]) / (self.x[i + 1] - self.x[i]) for i in range(len(self.x) - 1)]
        return all(a <= b for a, b in zip(s, s[1:]))

    def Hat(self, y):
        i = bisect.bisect_right(self.x, y) - 1
        if i >= len(self.x) - 1:
            return self.H[-1]
        x0, x1 = self.x[i], self.x[i + 1]
        return self.H[i] + (self.H[i + 1] - self.H[i]) * (y - x0) / (x1 - x0)

    def mat(self, y):
        return self.Hat(y) - y * y

    def interior(self, l, u):
        i = bisect.bisect_right(self.x, l)
        j = bisect.bisect_left(self.x, u)
        return range(i, j)

    def node(self, l, u, shift=0):
        """min over [l,u] of phi_B - shift, and the list of all minimizing knots.
        Endpoints have phi = m > 0 (they are not candidates when the node is invalid)."""
        best, arg = None, []
        for k in self.interior(l, u):
            v = self.m[k] - shift - (self.x[k] - l) * (u - self.x[k])
            if best is None or v < best:
                best, arg = v, [self.x[k]]
            elif v == best:
                arg.append(self.x[k])
        ends = min(self.mat(l), self.mat(u)) - shift
        if best is None or ends < best:
            return ends, []
        return best, arg

    def valid(self, l, u, shift=0):
        return self.node(l, u, shift)[0] >= 0

    def bmax(self, a, shift=0):
        """largest b <= 1 with [a,b] valid at tolerance eps - shift (exact).
        [a,b] valid iff for every knot k in (a,b): m_k - shift >= (x_k - a)(b - x_k)."""
        b = Fr(1)
        for k in self.interior(a, Fr(1)):
            xk = self.x[k]
            if xk >= b:
                break
            b = min(b, xk + (self.m[k] - shift) / (xk - a))
        return b

    def greedy(self, shift=0):
        """left-greedy certificate breakpoints at tolerance eps - shift (optimal)."""
        a, pts = Fr(0), [Fr(0)]
        while True:
            b = self.bmax(a, shift)
            pts.append(b)
            if b >= 1:
                return pts
            a = b

    def amin(self, b, shift=0):
        """smallest a >= 0 with [a,b] valid (mirror of bmax)."""
        a = Fr(0)
        for k in reversed(self.interior(Fr(0), b)):
            xk = self.x[k]
            if xk <= a:
                break
            a = max(a, xk - (self.m[k] - shift) / (b - xk))
        return a

    def rgreedy(self, shift=0):
        b, pts = Fr(1), [Fr(1)]
        while True:
            a = self.amin(b, shift)
            pts.append(a)
            if a <= 0:
                return sorted(pts)
            b = a

    def run(self, choose, shift_prune=0, cap=10 ** 5):
        """B&B with split rule choose(l, u, value, argmins) -> split point.
        Node pruned iff min phi_B >= shift_prune (shift_prune = incumbent gap g:
        prune iff LB >= U - eps with U = f* + g, i.e. min (m - q) >= g).
        Returns list of internal nodes (l, u, s)."""
        out, stack = [], [(Fr(0), Fr(1))]
        while stack:
            l, u = stack.pop()
            v, arg = self.node(l, u)
            if v >= shift_prune:
                continue
            s = choose(l, u, v, arg)
            assert l < s < u, (l, u, s)
            out.append((l, u, s))
            if len(out) > cap:
                raise RuntimeError("cap")
            stack += [(l, s), (s, u)]
        return out


def per_interval(S, internal):
    """count split points strictly inside each certificate interval, and at breakpoints."""
    N = len(S) - 1
    cnt = [0] * N
    at_bp = 0
    for (l, u, s) in internal:
        j = bisect.bisect_left(S, s)
        if j < len(S) and S[j] == s:
            at_bp += 1
        else:
            cnt[j - 1] += 1
    return cnt, at_bp


def classes(S, internal, j):
    """for interval J_j = [S[j-1], S[j]] (1-based j), split nodes inside it, classified."""
    a, b = S[j - 1], S[j]
    inside = [(l, u, s) for (l, u, s) in internal if a < s < b]
    YL = [n for n in inside if n[0] < a < n[1] and not n[0] < b < n[1]]
    YR = [n for n in inside if n[0] < b < n[1] and not n[0] < a < n[1]]
    YLR = [n for n in inside if n[0] < a < n[1] and n[0] < b < n[1]]
    return inside, YL, YR, YLR
