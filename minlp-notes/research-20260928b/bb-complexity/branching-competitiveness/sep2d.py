"""2D (and nD) separable exact-alphaBB experiments (alpha = 1).

m(x) = sum_i m_i(x_i), each m_i a 1D polyhedral instance from poly1d (so
m_i + t^2 is piecewise linear convex).  For a box B = prod [l_i,u_i],
    min_B (m - q_B) = sum_i min_{[l_i,u_i]} (m_i - (t-l_i)(u_i-t)),
exactly, and the relaxation minimizer is the vector of 1D minimizers.
A box is pruned iff this value is >= 0.

Rules (split one coordinate unless noted):
  bis    widest side, midpoint
  omega  coordinate maximizing a_i(y) = (y_i-l_i)(u_i-y_i), split at y_i
  omegaW widest coordinate among those with a_i(y) > 0, split at y_i
  multi  split every coordinate with a_i(y) > 0 at y_i (2^k-ary node)
"""
import math
import sys
import numpy as np
from poly1d import Inst, from_function


def node1(I, l, u):
    """Exact min over [l,u] of m_i - (t-l)(u-t) and a minimizer (endpoints included)."""
    v, y = I.node(l, u)
    ml, mu = I.m_at(l), I.m_at(u)
    best = min((v, y) if y is not None else (math.inf, None), (ml, l), (mu, u), key=lambda p: p[0])
    return best


def run(Is, rule, cap=2_000_000):
    n = len(Is)
    stack = [tuple((0.0, 1.0) for _ in range(n))]
    nodes = 0
    while stack:
        box = stack.pop()
        nodes += 1
        if nodes > cap:
            return None
        vals, ys = [], []
        for I, (l, u) in zip(Is, box):
            v, y = node1(I, l, u)
            vals.append(v); ys.append(y)
        tot = sum(vals)
        if tot >= 0:
            continue
        a = [(y - l) * (u - y) for (l, u), y in zip(box, ys)]
        w = [u - l for (l, u) in box]
        if rule == "bis":
            i = int(np.argmax(w)); cuts = [(i, 0.5 * (box[i][0] + box[i][1]))]
        elif rule == "omega":
            i = int(np.argmax(a)); cuts = [(i, ys[i])]
        elif rule == "omegaW":
            cand = [j for j in range(n) if a[j] > 0]
            i = max(cand, key=lambda j: w[j]); cuts = [(i, ys[i])]
        elif rule == "multi":
            cuts = [(j, ys[j]) for j in range(n) if a[j] > 0]
        else:
            raise ValueError(rule)
        boxes = [box]
        for i, s in cuts:
            nb = []
            for b in boxes:
                l, u = b[i]
                b1 = list(b); b1[i] = (l, s)
                b2 = list(b); b2[i] = (s, u)
                nb += [tuple(b1), tuple(b2)]
            boxes = nb
        stack.extend(boxes)
    return nodes


def _m_at(self, t):
    H = np.interp(t, self.x, self.m + self.x ** 2)
    return float(H - t * t)


Inst.m_at = _m_at


def grid_certificate(Is, cuts):
    """Check that the product grid with the given cut lists is a certificate; return #cells or None."""
    cnt = 0
    grids = [[0.0] + sorted(c) + [1.0] for c in cuts]
    import itertools
    for idx in itertools.product(*[range(len(g) - 1) for g in grids]):
        tot = 0.0
        for I, g, k in zip(Is, grids, idx):
            tot += node1(I, g[k], g[k + 1])[0]
        if tot < 0:
            return None
        cnt += 1
    return cnt


FAMILIES = {}


def fam(name):
    def deco(fn):
        FAMILIES[name] = fn
        return fn
    return deco


A = [1.0 / 3.0, math.sqrt(2) - 1, 0.6180339887498949]


@fam("sharp")
def f_sharp(eps, n=2):
    return [from_function(lambda t, a=A[i]: 2 * abs(t - a) - (t - a) ** 2, eps / n, K=2001, extra=[A[i]])
            for i in range(n)], [[A[i]] for i in range(n)]


@fam("sharp_shallow")
def f_sharp_shallow(eps, n=2):
    # slope 0.3 < alpha*width: the relaxation minimizer is not at the kink from far away
    return [from_function(lambda t, a=A[i]: 0.3 * abs(t - a), eps / n, K=2001, extra=[A[i]])
            for i in range(n)], None


@fam("multi_sharp")
def f_multi(eps, n=2):
    # rigid sawtooth breakpoints: m_i = cap on each cell (tight) + floor
    out, cuts = [], []
    rng = np.random.default_rng(5)
    for i in range(n):
        P = np.sort(np.concatenate([[0.0, 1.0], rng.uniform(0.05, 0.95, 3)]))
        def g(t, P=P):
            j = min(np.searchsorted(P, t, side="right") - 1, len(P) - 2)
            return (t - P[j]) * (P[j + 1] - t)
        out.append(from_function(g, eps / n, K=4001, extra=list(P)))
        cuts.append(list(P[1:-1]))
    return out, cuts


@fam("sharp_x_quad_y")
def f_mixed(eps, n=2):
    I1 = from_function(lambda t: 2 * abs(t - A[0]) - (t - A[0]) ** 2, eps / 2, K=2001, extra=[A[0]])
    I2 = from_function(lambda t: (t - A[1]) ** 2, eps / 2, K=20001, extra=[A[1]])
    return [I1, I2], None


@fam("quad")
def f_quad(eps, n=2):
    return [from_function(lambda t, a=A[i]: 0.5 * (t - a) ** 2, eps / n, K=20001, extra=[A[i]])
            for i in range(n)], None


if __name__ == "__main__":
    names = sys.argv[1:] or list(FAMILIES)
    for name in names:
        print("==", name, flush=True)
        for k in (2, 4, 6, 8, 10):
            eps = 10.0 ** (-k)
            Is, cuts = FAMILIES[name](eps)
            row = {r: run(Is, r) for r in ("bis", "omega", "omegaW", "multi")}
            cert = grid_certificate(Is, cuts) if cuts is not None else None
            print(f"eps=1e-{k:<2d}", row, "grid-certificate cells:", cert, flush=True)
