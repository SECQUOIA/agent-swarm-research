"""Independent 1D check of Theorem B (reviewer script, not the scout's code).

For exact alphaBB (f_B = f - alpha q_B) a box is prunable at tolerance eps iff
condition (V) holds on it, so the minimum alpha-valid family equals the minimum
certificate N_opt.  In 1D the minimum is computed by the greedy cover (validity
passes to subintervals).  Validity of [a,b] is decided from the critical points
of the piecewise polynomial g = f - f* + eps - alpha (y-a)(b-y).

Checks:
  * N_opt >= (alpha/pi^2)^(1/2) * int (f-f*+eps)^(-1/2)  on the scout's
    instances, on random degree-6 polynomials and at random eps;
  * a sawtooth instance on which the ratio N_opt / bound tends to 1, so the 1D
    constant cannot be improved.
"""
import math
import sys
import numpy as np
from numpy.polynomial import Polynomial as Poly
import mpmath as mp

mp.mp.dps = 30


class PWPoly:
    """Continuous piecewise polynomial on [0,1] with breakpoints."""

    def __init__(self, pieces):
        # pieces: list of (lo, hi, Poly)
        self.pieces = pieces

    def __call__(self, y):
        for lo, hi, p in self.pieces:
            if lo <= y <= hi:
                return p(y)
        raise ValueError(y)

    def min_on(self, a, b, extra=None):
        """min over [a,b] of self(y) + extra(y) (extra: Poly or None)."""
        best = math.inf
        for lo, hi, p in self.pieces:
            l, u = max(lo, a), min(hi, b)
            if l > u:
                continue
            q = p if extra is None else p + extra
            cands = [l, u]
            d = q.deriv()
            if d.degree() >= 1 or abs(d.coef[0]) > 0:
                for r in d.roots():
                    if abs(r.imag) < 1e-12 and l < r.real < u:
                        cands.append(r.real)
            best = min(best, min(q(c) for c in cands))
        return best

    def breakpoints(self):
        return sorted({lo for lo, _, _ in self.pieces} | {hi for _, hi, _ in self.pieces})


def valid(F, fstar, alpha, eps, a, b):
    # g(y) = f(y) - f* + eps - alpha (y-a)(b-y);  -(y-a)(b-y) = y^2 - (a+b) y + a b
    extra = Poly([alpha * a * b - fstar + eps, -alpha * (a + b), alpha])
    return F.min_on(a, b, extra) >= -1e-15


def opt_cover(F, fstar, alpha, eps, tol=1e-14):
    x, k = 0.0, 0
    while x < 1.0:
        k += 1
        if valid(F, fstar, alpha, eps, x, 1.0):
            return k
        lo, hi = x, 1.0
        while hi - lo > tol:
            mid = 0.5 * (lo + hi)
            if valid(F, fstar, alpha, eps, x, mid):
                lo = mid
            else:
                hi = mid
        if lo <= x:
            raise RuntimeError("no progress")
        x = lo
        if k > 10 ** 6:
            raise RuntimeError("too many")
    return k


def bound(F, fstar, alpha, eps, pts):
    g = lambda t: (mp.mpf(F(float(t))) - fstar + eps) ** mp.mpf(-0.5)
    pts = sorted(set([0.0, 1.0] + [p for p in pts if 0 < p < 1]))
    val = mp.quad(g, pts, maxdegree=10)
    return float(mp.sqrt(alpha) / mp.pi * val)


def poly_instance(coefs_about_a, a):
    """f(y) = sum c_k (y-a)^k on [0,1]."""
    p = Poly([0.0])
    shift = Poly([-a, 1.0])
    for k, c in enumerate(coefs_about_a):
        p = p + c * shift ** k
    return PWPoly([(0.0, 1.0, p)]), p


def alpha_for(p):
    d2 = p.deriv(2)
    cands = [0.0, 1.0] + [r.real for r in d2.deriv().roots() if abs(r.imag) < 1e-12 and 0 < r.real < 1]
    m = min(d2(c) for c in cands)
    return max(0.0, -m / 2.0)


def fmin(F):
    best, arg = math.inf, None
    for lo, hi, p in F.pieces:
        cands = [lo, hi] + [r.real for r in p.deriv().roots() if abs(r.imag) < 1e-12 and lo < r.real < hi]
        for c in cands:
            v = p(c)
            if v < best:
                best, arg = v, c
    return best, arg


def report(name, F, alpha, pts, epss):
    fstar, arg = fmin(F)
    rows = []
    for eps in epss:
        n_opt = opt_cover(F, fstar, alpha, eps)
        lb = bound(F, fstar, alpha, eps, pts + [arg])
        rows.append((eps, n_opt, lb, n_opt / lb))
        print(f"{name:28s} alpha={alpha:.4g} eps={eps:.1e} N_opt={n_opt:5d} ThmB={lb:9.3f} ratio={n_opt/lb:.3f}", flush=True)
    return rows


def main():
    A = 1.0 / 3.0
    epss = [1e-2, 1e-5, 1e-8]
    worst = math.inf
    # scout instances
    F, p = poly_instance([0, 0, 1, 0, -2], A)
    alpha = -(2 - 24 * (2 / 3) ** 2) / 2
    for r in report("nondeg t^2-2t^4", F, alpha, [], epss):
        worst = min(worst, r[3])
    F, p = poly_instance([0, 0, 0, 0, 1, 0, -1], A)
    alpha = alpha_for(p)
    for r in report("quartic t^4(1-t^2)", F, alpha, [], epss):
        worst = min(worst, r[3])
    # sharp: 2|t| - t^2 with t = y - A
    left = Poly([2 * A, -2]) - Poly([-A, 1]) ** 2
    right = Poly([-2 * A, 2]) - Poly([-A, 1]) ** 2
    F = PWPoly([(0.0, A, left), (A, 1.0, right)])
    for r in report("sharp 2|t|-t^2", F, 1.0, [A], epss):
        worst = min(worst, r[3])
    # sawtooth: f = alpha * (y - k h)((k+1) h - y) on each of N cells: N_opt/bound -> 1
    for N in (3, 7):
        h = 1.0 / N
        pieces = [(k * h, (k + 1) * h, Poly([-(k * h) * ((k + 1) * h), (2 * k + 1) * h, -1.0]) * 1.0) for k in range(N)]
        F = PWPoly(pieces)
        for r in report(f"sawtooth N={N} (alpha=1)", F, 1.0, [k * h for k in range(N + 1)], [1e-3, 1e-6, 1e-9, 1e-12]):
            worst = min(worst, r[3])
    # random polynomials, random eps
    rng = np.random.default_rng(20260928)
    rmin = math.inf
    for trial in range(int(sys.argv[1]) if len(sys.argv) > 1 else 40):
        a = rng.uniform(0.05, 0.95)
        c = rng.normal(size=7)
        c[0] = 0.0
        c[1] = 0.0          # stationary point at a
        c[2] = abs(c[2]) * rng.choice([0.0, 1.0])   # sometimes degenerate
        F, p = poly_instance(c, a)
        alpha = alpha_for(p) + rng.uniform(0, 1)
        if alpha <= 0:
            continue
        eps = 10 ** rng.uniform(-9, -1)
        fstar, arg = fmin(F)
        n_opt = opt_cover(F, fstar, alpha, eps)
        lb = bound(F, fstar, alpha, eps, [arg, a])
        rmin = min(rmin, n_opt / lb)
        print(f"random#{trial:02d} a={a:.3f} alpha={alpha:.3g} eps={eps:.1e} N_opt={n_opt} ThmB={lb:.3f} ratio={n_opt/lb:.3f}", flush=True)
    print(f"min ratio N_opt/ThmB: named instances {worst:.4f}, random {rmin:.4f}")


if __name__ == "__main__":
    main()
