"""Numerical check of Theorem 12 (second-order tangent expansion of composite
McCormick relaxations), see ../../proofs-12-11.md.

Implements
  * the composite McCormick relaxation of a factorable function (natural
    interval arithmetic with exact univariate ranges; sums and scalings exact;
    the product rule of Mitsos, Chachuat and Barton (2009); the univariate
    composition rule h^cv(mid(cv, cc, zmin)), h^cc(mid(cv, cc, zmax)) with the
    exact convex/concave envelopes of h on the interval), and
  * the recursion for ell^{L,U}, E^cv, E^cc proved in proofs-12-11.md,
and compares (cv_k(x) - v_k(x))/w^2 with -E_k^cv and (cc_k(x) - v_k(x))/w^2 with
E_k^cc at x = x* + w xi on B = x* + w D(d), for every factor k, as w -> 0.
It also reports max (v_k^L - cv_k)^+/w^2 and (cc_k - v_k^U)^+/w^2 (Lemma P).

Run with ~/miniconda3/envs/exact-quadratic-hull/bin/python mccormick_expansion.py
"""
import math
import numpy as np

pos = lambda t: max(t, 0.0)
neg = lambda t: max(-t, 0.0)


# ---------------------------------------------------------------- univariates
def _points(L, U, base, period):
    """Points base + k*period inside [L, U]."""
    k0 = math.ceil((L - base) / period)
    out = []
    while base + k0 * period <= U:
        out.append(base + k0 * period)
        k0 += 1
    return out


class Uni:
    def __init__(self, name, f, df, d2f, crit, infl):
        self.name, self.f, self.df, self.d2f = name, f, df, d2f
        self.crit = crit    # (L, U) -> critical points of f in [L, U]
        self.infl = infl    # (L, U) -> sign changes of f'' in (L, U)

    def neg(self):
        return Uni("-" + self.name, lambda t: -self.f(t), lambda t: -self.df(t),
                   lambda t: -self.d2f(t), self.crit, self.infl)


UNI = {
    "exp": Uni("exp", math.exp, math.exp, math.exp, lambda L, U: [], lambda L, U: []),
    "log": Uni("log", math.log, lambda t: 1 / t, lambda t: -1 / t ** 2,
               lambda L, U: [], lambda L, U: []),
    "sqr": Uni("sqr", lambda t: t * t, lambda t: 2 * t, lambda t: 2.0,
               lambda L, U: [0.0] if L <= 0 <= U else [], lambda L, U: []),
    "sin": Uni("sin", math.sin, math.cos, lambda t: -math.sin(t),
               lambda L, U: _points(L, U, math.pi / 2, math.pi),
               lambda L, U: [s for s in _points(L, U, 0.0, math.pi) if L < s < U]),
    "cos": Uni("cos", math.cos, lambda t: -math.sin(t), lambda t: -math.cos(t),
               lambda L, U: _points(L, U, 0.0, math.pi),
               lambda L, U: [s for s in _points(L, U, math.pi / 2, math.pi) if L < s < U]),
}


def _bisect(F, a, b, it=200):
    """Root of an increasing function F on [a, b] with F(a) < 0 <= F(b)."""
    for _ in range(it):
        m = 0.5 * (a + b)
        if F(m) < 0:
            a = m
        else:
            b = m
    return 0.5 * (a + b)


def cv_env(h, L, U, y):
    """Convex envelope of h on [L, U] at y (h has at most one inflection there)."""
    if U - L <= 0:
        return h.f(y)
    f, df = h.f, h.df
    sec = lambda y: f(L) + (f(U) - f(L)) / (U - L) * (y - L)
    infl = h.infl(L, U)
    if not infl:
        return f(y) if h.d2f(0.5 * (L + U)) >= 0 else sec(y)
    if len(infl) > 1:
        raise ValueError("more than one inflection point in the interval")
    s = infl[0]
    if h.d2f(0.5 * (L + s)) >= 0:      # convex on [L, s], concave on [s, U]
        F = lambda t: df(t) * (U - t) - (f(U) - f(t))   # increasing on [L, s]
        if F(L) >= 0:
            return sec(y)
        t = _bisect(F, L, s)
        return f(y) if y <= t else f(t) + (f(U) - f(t)) / (U - t) * (y - t)
    else:                               # concave on [L, s], convex on [s, U]
        G = lambda t: df(t) * (t - L) - (f(t) - f(L))   # increasing on [s, U]
        if G(U) <= 0:
            return sec(y)
        t = _bisect(G, s, U)
        return f(y) if y >= t else f(L) + (f(t) - f(L)) / (t - L) * (y - L)


def cc_env(h, L, U, y):
    return -cv_env(h.neg(), L, U, y)


def uni_range(h, L, U):
    """Exact range of h on [L, U] and a minimizer / maximizer."""
    cand = [L, U] + h.crit(L, U)
    vals = [h.f(t) for t in cand]
    i, j = int(np.argmin(vals)), int(np.argmax(vals))
    return vals[i], vals[j], cand[i], cand[j]


def mid(a, b, c):
    return sorted((a, b, c))[1]


# ---------------------------------------------------------------- expressions
class Node:
    def __init__(self, op, *args):
        self.op, self.args = op, args

    def __add__(s, o): return Node("add", s, _n(o))
    __radd__ = __add__
    def __mul__(s, o): return Node("scale", o, s) if isinstance(o, (int, float)) else Node("mul", s, o)
    __rmul__ = lambda s, o: Node("scale", o, s)
    def __neg__(s): return Node("scale", -1.0, s)
    def __sub__(s, o): return s + (-_n(o))


def _n(o):
    return o if isinstance(o, Node) else Node("const", float(o))


def var(i): return Node("var", i)
def uni(name, a): return Node("uni", name, a)


def topo(root):
    order, seen = [], set()
    def visit(n):
        if id(n) in seen:
            return
        seen.add(id(n))
        for a in n.args:
            if isinstance(a, Node):
                visit(a)
        order.append(n)
    visit(root)
    return order


# ------------------------------------------------ composite McCormick relaxation
def relax(root, x, lo, hi):
    """Return {id(node): (value, L, U, cv, cc)} for all factors."""
    R = {}
    for n in topo(root):
        op = n.op
        if op == "var":
            i = n.args[0]
            R[id(n)] = (x[i], lo[i], hi[i], x[i], x[i])
        elif op == "const":
            c = n.args[0]
            R[id(n)] = (c, c, c, c, c)
        elif op == "add":
            A, B = R[id(n.args[0])], R[id(n.args[1])]
            R[id(n)] = tuple(A[k] + B[k] for k in range(5))
        elif op == "scale":
            c, A = n.args[0], R[id(n.args[1])]
            if c >= 0:
                R[id(n)] = (c * A[0], c * A[1], c * A[2], c * A[3], c * A[4])
            else:
                R[id(n)] = (c * A[0], c * A[2], c * A[1], c * A[4], c * A[3])
        elif op == "mul":
            (a, aL, aU, acv, acc) = R[id(n.args[0])]
            (b, bL, bU, bcv, bcc) = R[id(n.args[1])]
            prods = [aL * bL, aL * bU, aU * bL, aU * bU]
            # Mitsos, Chachuat, Barton (2009) product rule
            al1 = min(bL * acv, bL * acc); al2 = min(aL * bcv, aL * bcc)
            be1 = min(bU * acv, bU * acc); be2 = min(aU * bcv, aU * bcc)
            cv = max(al1 + al2 - aL * bL, be1 + be2 - aU * bU)
            ga1 = max(bL * acv, bL * acc); ga2 = max(aU * bcv, aU * bcc)
            de1 = max(bU * acv, bU * acc); de2 = max(aL * bcv, aL * bcc)
            cc = min(ga1 + ga2 - aU * bL, de1 + de2 - aL * bU)
            R[id(n)] = (a * b, min(prods), max(prods), cv, cc)
        elif op == "uni":
            h = UNI[n.args[0]]
            (a, aL, aU, acv, acc) = R[id(n.args[1])]
            vL, vU, zmin, zmax = uni_range(h, aL, aU)
            cv = cv_env(h, aL, aU, mid(acv, acc, zmin))
            cc = cc_env(h, aL, aU, mid(acv, acc, zmax))
            R[id(n)] = (h.f(a), vL, vU, cv, cc)
    return R


# ------------------------------------------------------- tangent recursion (E)
def tangent(root, xs, dm, dp, xi):
    """Return {id(node): (v*, p, ellL, ellU, Ecv, Ecc)} (recursion of Theorem 12)."""
    T = {}
    for n in topo(root):
        op = n.op
        if op == "var":
            i = n.args[0]
            T[id(n)] = (xs[i], xi[i], -dm[i], dp[i], 0.0, 0.0)
        elif op == "const":
            T[id(n)] = (n.args[0], 0.0, 0.0, 0.0, 0.0, 0.0)
        elif op == "add":
            A, B = T[id(n.args[0])], T[id(n.args[1])]
            T[id(n)] = tuple(A[k] + B[k] for k in range(6))
        elif op == "scale":
            c, (v, p, lL, lU, Ev, Ec) = n.args[0], T[id(n.args[1])]
            if c >= 0:
                T[id(n)] = (c * v, c * p, c * lL, c * lU, c * Ev, c * Ec)
            else:
                T[id(n)] = (c * v, c * p, c * lU, c * lL, -c * Ec, -c * Ev)
        elif op == "mul":
            (a, pa, aL, aU, Eva, Eca) = T[id(n.args[0])]
            (b, pb, bL, bU, Evb, Ecb) = T[id(n.args[1])]
            lL = min(b * aL, b * aU) + min(a * bL, a * bU)
            lU = max(b * aL, b * aU) + max(a * bL, a * bU)
            Ecv = (pos(b) * Eva + neg(b) * Eca + pos(a) * Evb + neg(a) * Ecb
                   + min((pa - aL) * (pb - bL), (aU - pa) * (bU - pb)))
            Ecc = (pos(b) * Eca + neg(b) * Eva + pos(a) * Ecb + neg(a) * Evb
                   + min((aU - pa) * (pb - bL), (pa - aL) * (bU - pb)))
            T[id(n)] = (a * b, b * pa + a * pb, lL, lU, Ecv, Ecc)
        elif op == "uni":
            h = UNI[n.args[0]]
            (a, pa, aL, aU, Eva, Eca) = T[id(n.args[1])]
            h1, h2 = h.df(a), h.d2f(a)
            s = (pa - aL) * (aU - pa)
            Ecv = neg(h2) / 2 * s + pos(h1) * Eva + neg(h1) * Eca
            Ecc = pos(h2) / 2 * s + pos(h1) * Eca + neg(h1) * Eva
            T[id(n)] = (h.f(a), h1 * pa, min(h1 * aL, h1 * aU), max(h1 * aL, h1 * aU), Ecv, Ecc)
    return T


# ------------------------------------------------------------------- the check
def check(name, root, xs, nsamp=300, ws=(1e-1, 1e-2, 1e-3, 1e-4), seed=0):
    rng = np.random.default_rng(seed)
    xs = np.asarray(xs, float)
    nv = len(xs)
    samples = []
    for _ in range(nsamp):
        dm, dp = rng.uniform(0.2, 1.5, nv), rng.uniform(0.2, 1.5, nv)
        dm[rng.random(nv) < 0.1] = 0.0          # degenerate shapes
        dp[rng.random(nv) < 0.1] = 0.0
        xi = rng.uniform(-dm, dp)
        r = rng.random(nv)                       # put some coordinates on faces
        xi[r < 0.2] = -dm[r < 0.2]
        xi[r > 0.8] = dp[r > 0.8]
        samples.append((dm, dp, xi))
    nodes = topo(root)
    errs, lemP = [], []
    for w in ws:
        e = p = 0.0
        for dm, dp, xi in samples:
            R = relax(root, xs + w * xi, xs - w * dm, xs + w * dp)
            T = tangent(root, xs, dm, dp, xi)
            for n in nodes:
                v, L, U, cv, cc = R[id(n)]
                Ecv, Ecc = T[id(n)][4], T[id(n)][5]
                e = max(e, abs((cv - v) / w ** 2 + Ecv), abs((cc - v) / w ** 2 - Ecc))
                p = max(p, (L - cv) / w ** 2, (cc - U) / w ** 2)
        errs.append(e); lemP.append(p)
    # size of the predicted E at the root, for scale
    Emax = max(max(tangent(root, xs, dm, dp, xi)[id(root)][4:6]) for dm, dp, xi in samples)
    print(f"{name:34s} x*={np.array2string(xs, precision=3):24s} max E_root={Emax:7.3f}")
    print("   w        : " + "  ".join(f"{w:8.0e}" for w in ws))
    print("   max|err| : " + "  ".join(f"{e:8.1e}" for e in errs))
    print("   Lemma P  : " + "  ".join(f"{p:8.1e}" for p in lemP))
    return errs


if __name__ == "__main__":
    x, y, z = var(0), var(1), var(2)
    xy = x * y
    cases = [
        ("x*y*z", x * y * z, [(0.5, -0.7, 1.2), (0.0, 0.0, 1.0), (0.0, 0.0, 0.0)]),
        ("exp(x)*y", uni("exp", x) * y, [(0.3, -0.4), (0.3, 0.0)]),
        ("sin(x+y)*x", uni("sin", x + y) * x,
         [(0.4, 0.3), (0.2, -0.2), (0.0, 0.0), (math.pi / 4, math.pi / 4), (1.0, 2.0)]),
        ("(x*y)^2 [sqr]", uni("sqr", xy), [(0.0, 0.0), (1.0, -0.5)]),
        ("(x*y)*(x*y) [product]", xy * xy, [(0.0, 0.0), (1.0, -0.5)]),
        ("log(1+x^2)*y", uni("log", 1.0 + uni("sqr", x)) * y,
         [(0.0, 0.7), (0.5, -1.0), (0.0, 0.0)]),
        ("exp(-x*y)*z", uni("exp", -xy) * z, [(0.6, 0.8, -1.1), (0.0, 0.5, 0.0)]),
        ("sin(x*y+z)", uni("sin", xy + z), [(0.5, 0.5, math.pi - 0.25), (0.3, -0.2, 1.0)]),
        ("cos(x)*cos(y)-x*y", uni("cos", x) * uni("cos", y) - xy, [(0.0, 0.0), (1.2, -0.4)]),
    ]
    worst = 0.0
    for name, expr, points in cases:
        for xs in points:
            errs = check(name, expr, xs)
            worst = max(worst, errs[-1])
    print(f"\nworst error at w = 1e-4 over all cases and factors: {worst:.2e}")
