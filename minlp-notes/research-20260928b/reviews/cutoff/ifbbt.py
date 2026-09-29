"""Reviewer's independent interval propagation (HC4-type) on a factorable DAG.

Written for the review of cutoff-propagation.md; it does not import the
author's code. Floating point, no outward rounding: an illustration, not a
certificate.

Nodes (topological order, children before parents; last node = root):
  ('x', i)                      variable x_i
  ('sum', ch, co, b)            b + sum co[j] * w[ch[j]]   (children distinct)
  ('mul', a, b)                 w[a] * w[b]   (a != b)
  ('pow', a, k)                 w[a] ** k, integer k >= 2
  ('up', a, coeffs)             univariate polynomial phi(w[a]) = sum coeffs[i] t^i,
                                a general (possibly non-monotone) unary node

Every revise below is the exact revise rho_E of one elementary constraint E:
all nodes of E get the hull of the projection of E ∩ Z (in real arithmetic).
Schedules:
  hc4      : rounds of (forward images, cutoff, exact revises in reverse order)
  chaotic  : rounds of exact revises of all constraints (and the cutoff) in a
             random order
"""
import math
import random
import numpy as np
from numpy.polynomial import polynomial as P

INF = math.inf


class Empty(Exception):
    pass


def cap(a, b):
    lo, hi = max(a[0], b[0]), min(a[1], b[1])
    if lo > hi:
        # tolerate rounding-level inversions
        if lo - hi <= 1e-13 * (1.0 + abs(lo)):
            m = 0.5 * (lo + hi)
            return (m, m)
        raise Empty
    return (lo, hi)


def hull(pieces):
    pieces = [p for p in pieces if p is not None]
    if not pieces:
        raise Empty
    return (min(p[0] for p in pieces), max(p[1] for p in pieces))


def clip(p, a):
    lo, hi = max(p[0], a[0]), min(p[1], a[1])
    return (lo, hi) if lo <= hi else None


# ---------- images ----------
def i_mul(a, b):
    c = [a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1]]
    c = [0.0 if x != x else x for x in c]
    return (min(c), max(c))


def i_pow(a, k):
    lo, hi = a
    if k % 2:
        return (lo ** k, hi ** k)
    if lo >= 0:
        return (lo ** k, hi ** k)
    if hi <= 0:
        return (hi ** k, lo ** k)
    return (0.0, max(-lo, hi) ** k)


def real_roots(coeffs, lo, hi):
    c = np.trim_zeros(np.asarray(coeffs, float), 'b')
    if len(c) <= 1:
        return []
    r = P.polyroots(c)
    out = []
    d = P.polyder(c)
    scale = 1.0 + max(abs(lo), abs(hi))
    for z in r:
        if abs(z.imag) > 1e-7 * scale:
            continue
        x = z.real
        for _ in range(3):  # Newton polish
            dv = P.polyval(x, d)
            if dv == 0:
                break
            x = x - P.polyval(x, c) / dv
        if lo - 1e-12 * scale <= x <= hi + 1e-12 * scale:
            out.append(min(max(x, lo), hi))
    return sorted(out)


def i_up(a, coeffs):
    lo, hi = a
    pts = [lo, hi] + real_roots(P.polyder(np.asarray(coeffs, float)), lo, hi)
    v = [P.polyval(p, coeffs) for p in pts]
    return (min(v), max(v))


# ---------- projections onto one argument ----------
def proj_div(W, V, U):
    """hull{u in U : exists v in V with u*v in W}."""
    vl, vh = V
    wl, wh = W
    if vl > 0 or vh < 0:
        q = [wl / vl, wl / vh, wh / vl, wh / vh]
        return cap(U, (min(q), max(q)))
    if wl <= 0 <= wh:
        return U
    pieces = []
    if wl > 0:
        if vh > 0:
            pieces.append(clip((wl / vh, INF), U))
        if vl < 0:
            pieces.append(clip((-INF, wl / vl), U))
    else:
        if vl < 0:
            pieces.append(clip((wh / vl, INF), U))
        if vh > 0:
            pieces.append(clip((-INF, wh / vh), U))
    return hull(pieces)


def proj_pow(W, k, Z):
    wl, wh = W
    if k % 2:
        rt = lambda v: math.copysign(abs(v) ** (1.0 / k), v)
        return cap(Z, (rt(wl), rt(wh)))
    if wh < 0:
        raise Empty
    r = wh ** (1.0 / k)
    s = max(wl, 0.0) ** (1.0 / k)
    return hull([clip((-r, -s), Z), clip((s, r), Z)])


def proj_up(W, coeffs, Z):
    """hull{z in Z : phi(z) in W} via breakpoints (roots of phi - wl, phi - wh)."""
    lo, hi = Z
    wl, wh = W
    tol = 1e-11 * (1.0 + max(abs(wl), abs(wh)))
    c = np.asarray(coeffs, float)
    bps = [lo, hi]
    for lev in (wl, wh):
        if math.isfinite(lev):
            cc = c.copy()
            cc[0] -= lev
            bps += real_roots(cc, lo, hi)
    bps = sorted(set(bps))
    inside = lambda z: wl - tol <= P.polyval(z, c) <= wh + tol
    first = last = None
    for i, b in enumerate(bps):
        ok = inside(b)
        if not ok and i + 1 < len(bps):
            ok = inside(0.5 * (b + bps[i + 1]))
        if ok:
            first = b
            break
    for i in range(len(bps) - 1, -1, -1):
        b = bps[i]
        ok = inside(b)
        if not ok and i > 0:
            ok = inside(0.5 * (b + bps[i - 1]))
        if ok:
            last = b
            break
    if first is None or last is None or first > last:
        raise Empty
    return (first, last)


# ---------- the DAG ----------
class DAG:
    def __init__(self, nvar):
        self.nodes = [('x', i) for i in range(nvar)]
        self.nvar = nvar

    def add(self, nd):
        self.nodes.append(nd)
        return len(self.nodes) - 1

    def sum(self, ch, co, b=0.0):
        acc = {}
        for c, a in zip(ch, co):
            acc[c] = acc.get(c, 0.0) + float(a)
        ch = [c for c in acc if acc[c] != 0.0]
        return self.add(('sum', tuple(ch), tuple(acc[c] for c in ch), float(b)))

    def mul(self, a, b):
        if a == b:
            return self.pow(a, 2)
        return self.add(('mul', a, b))

    def pow(self, a, k):
        return self.add(('pow', a, int(k)))

    def up(self, a, coeffs):
        return self.add(('up', a, tuple(float(c) for c in coeffs)))

    # value of every node at a point
    def values(self, x):
        v = []
        for nd in self.nodes:
            t = nd[0]
            if t == 'x':
                v.append(float(x[nd[1]]))
            elif t == 'sum':
                v.append(nd[3] + sum(a * v[c] for c, a in zip(nd[1], nd[2])))
            elif t == 'mul':
                v.append(v[nd[1]] * v[nd[2]])
            elif t == 'pow':
                v.append(v[nd[1]] ** nd[2])
            else:
                v.append(float(P.polyval(v[nd[1]], nd[2])))
        return v

    def f(self, x):
        return self.values(x)[-1]

    def image(self, k, Z):
        nd = self.nodes[k]
        t = nd[0]
        if t == 'sum':
            lo = hi = nd[3]
            for c, a in zip(nd[1], nd[2]):
                if a >= 0:
                    lo += a * Z[c][0]; hi += a * Z[c][1]
                else:
                    lo += a * Z[c][1]; hi += a * Z[c][0]
            return (lo, hi)
        if t == 'mul':
            return i_mul(Z[nd[1]], Z[nd[2]])
        if t == 'pow':
            return i_pow(Z[nd[1]], nd[2])
        if t == 'up':
            return i_up(Z[nd[1]], nd[2])
        return None

    def forward_box(self, box):
        Z = []
        for k, nd in enumerate(self.nodes):
            Z.append(tuple(box[nd[1]]) if nd[0] == 'x' else self.image(k, Z))
        return Z

    def revise(self, k, Z):
        """Exact revise of the elementary constraint defining node k (in place)."""
        nd = self.nodes[k]
        t = nd[0]
        if t == 'x':
            return
        W = cap(Z[k], self.image(k, Z))
        if t == 'sum':
            ch, co, b = nd[1], nd[2], nd[3]
            terms = [(a * Z[c][0], a * Z[c][1]) if a >= 0 else (a * Z[c][1], a * Z[c][0])
                     for c, a in zip(ch, co)]
            slo = sum(x[0] for x in terms); shi = sum(x[1] for x in terms)
            new = []
            for (c, a), tr in zip(zip(ch, co), terms):
                lo = W[0] - b - (shi - tr[1])
                hi = W[1] - b - (slo - tr[0])
                cand = (lo / a, hi / a) if a > 0 else (hi / a, lo / a)
                new.append(cap(Z[c], cand))
            for c, v in zip(ch, new):
                Z[c] = v
        elif t == 'mul':
            a, bb = nd[1], nd[2]
            U, V = Z[a], Z[bb]
            Z[a] = proj_div(W, V, U)
            Z[bb] = proj_div(W, U, V)
        elif t == 'pow':
            Z[nd[1]] = proj_pow(W, nd[2], Z[nd[1]])
        elif t == 'up':
            Z[nd[1]] = proj_up(W, nd[2], Z[nd[1]])
        Z[k] = W

    def propagate(self, box, cut, max_rounds=100000, schedule='hc4', rtol=1e-14, seed=0,
                  start=None):
        """Returns (status, Z, rounds); status in {'empty', 'fixed', 'limit'}."""
        rng = random.Random(seed)
        try:
            Z = list(start) if start is not None else self.forward_box(box)
        except Empty:
            return 'empty', None, 0
        root = len(self.nodes) - 1
        cons = [k for k, nd in enumerate(self.nodes) if nd[0] != 'x']
        for r in range(1, max_rounds + 1):
            old = list(Z)
            try:
                if schedule == 'hc4':
                    for k in cons:
                        Z[k] = cap(Z[k], self.image(k, Z))
                    Z[root] = cap(Z[root], (-INF, cut))
                    for k in reversed(cons):
                        self.revise(k, Z)
                else:
                    order = cons + ['cut']
                    rng.shuffle(order)
                    for k in order:
                        if k == 'cut':
                            Z[root] = cap(Z[root], (-INF, cut))
                        else:
                            self.revise(k, Z)
            except Empty:
                return 'empty', None, r
            if all(abs(a[0] - b[0]) <= rtol * (1 + abs(a[0])) and
                   abs(a[1] - b[1]) <= rtol * (1 + abs(a[1])) for a, b in zip(old, Z)):
                return 'fixed', Z, r
        return 'limit', Z, max_rounds

    def xbox(self, Z):
        out = [None] * self.nvar
        for k, nd in enumerate(self.nodes):
            if nd[0] == 'x':
                out[nd[1]] = Z[k]
        return out

    def pi(self, box, hi=None, iters=45, max_rounds=20000, schedule='hc4'):
        """Bisection estimate of pi_D(box); a round limit counts as nonempty,
        so the returned value can only be too low."""
        lo = self.forward_box(box)[-1][0]
        if hi is None:
            hi = self.f([0.5 * (a + b) for a, b in box])
        for _ in range(iters):
            mid = 0.5 * (lo + hi)
            st, _, _ = self.propagate(box, mid, max_rounds=max_rounds, schedule=schedule)
            if st == 'empty':
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)
