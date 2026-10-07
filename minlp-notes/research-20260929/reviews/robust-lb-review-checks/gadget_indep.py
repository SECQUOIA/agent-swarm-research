"""Independent re-implementation (referee) of the gadget class bound of robust-lower-bound.md.

Written from the note's formulas only (no import of the authors' code).

Gadget g(x,y,z) = y1^2 x^2 + b x y + c y^2 + u(z) + bp y z on a box B = Bx x By x Bz.
Only y is shared by the two factors (x,y) and (y,z).  For a split class whose space at y is
T (a finite list of test functions containing 1 and y), Lemma 1.2 plus partial minimisation gives

  V_T(B) = min { int H1 dmu1 + int H2 dmu2 : mu1, mu2 prob. on By, int phi dmu1 = int phi dmu2, phi in T }

with H1(y) = min_{x in Bx} (y1^2 x^2 + b x y) + c1 y^2 and H2(y) = min_{z in Bz} (u(z) + bp y z) + c2 y^2,
c1 + c2 = c (the base split of c y^2).  Reduction: given the y-marginal, the cheapest factor measure puts x
(resp. z) at the partial minimiser, which is a continuous function of y.

Computation: column generation over finite y-supports.  Upper bound = value of an explicit consistent pair
(mu1, mu2) (a fooling).  Lower bound = min(H1 + rho) + min(H2 - rho) for rho in span T taken from the LP duals,
with the 1-D minima computed exactly on each piece where H1, H2 are quadratic (critical points by np.roots).
"""
import numpy as np
from scipy.optimize import linprog, brentq


class Gadget:
    def __init__(self, y1=0.38, eta=0.05, epsv=0.02):
        self.y1, self.eta, self.epsv = y1, eta, epsv
        self.b = 2 * y1
        self.bp = 2 * eta + 2 * (1 - eta) * (1 - y1)
        self.c = 1 + eta + epsv
        self.z1 = 2 * eta * y1 / self.bp
        self.k = 2 * (1 - eta) * y1

    # ---- the data, straight from Section 3.1 --------------------------------------------------
    def u(self, z):
        z = np.asarray(z, float)
        inner = self.bp ** 2 * z ** 2 / (4 * self.eta)
        outer = (self.bp * np.abs(z) + self.k) ** 2 / 4 - (1 - self.eta) * self.y1 ** 2
        return np.where(np.abs(z) <= self.z1, inner, outer)

    def du(self, z):
        z = np.asarray(z, float)
        inner = self.bp ** 2 * z / (2 * self.eta)
        outer = np.sign(z) * self.bp * (self.bp * np.abs(z) + self.k) / 2
        return np.where(np.abs(z) <= self.z1, inner, outer)

    def g(self, x, y, z):
        return self.y1 ** 2 * x ** 2 + self.b * x * y + self.c * y ** 2 + self.u(z) + self.bp * y * z

    # ---- partial minimisers --------------------------------------------------------------------
    def xstar(self, y, lx, ux):
        # argmin_x y1^2 x^2 + b x y is -b y / (2 y1^2) = -y / y1; convex in x, so clip.
        return np.clip(-np.asarray(y, float) / self.y1, lx, ux)

    def z0(self, y):
        """Unconstrained minimiser of u(z) + bp y z: solve u'(z) = -bp y (u' increasing, continuous)."""
        y = np.asarray(y, float)
        t = -self.bp * y                      # target slope
        inner = t * 2 * self.eta / self.bp ** 2
        # outer: sign(z) bp (bp |z| + k)/2 = t  ->  |z| = (2|t|/bp - k)/bp
        outer = np.sign(t) * (2 * np.abs(t) / self.bp - self.k) / self.bp
        return np.where(np.abs(inner) <= self.z1, inner, outer)

    def zstar(self, y, lz, uz):
        return np.clip(self.z0(y), lz, uz)

    def H1(self, y, lx, ux):
        y = np.asarray(y, float)
        x = self.xstar(y, lx, ux)
        return self.y1 ** 2 * x ** 2 + self.b * x * y

    def H2(self, y, lz, uz):
        y = np.asarray(y, float)
        z = self.zstar(y, lz, uz)
        return self.u(z) + self.bp * y * z

    def breakpoints(self, box):
        """y-values in By where H1 or H2 changes formula."""
        lx, ux, ly, uy, lz, uz = box
        bps = {ly, uy, -self.y1 * lx, -self.y1 * ux, self.y1, -self.y1}
        for zb in (lz, uz):
            f = lambda y: float(self.z0(y)) - zb
            a, bb = -1.0, 1.0
            if f(a) * f(bb) < 0:
                bps.add(brentq(f, a, bb, xtol=1e-15, rtol=1e-15))
        return np.array(sorted(v for v in bps if ly <= v <= uy))


def exact_min(fun, poly_extra, bps):
    """min over [bps[0], bps[-1]] of fun(y) + polyval(poly_extra, y), where fun is quadratic on each
    [bps[j], bps[j+1]].  poly_extra: numpy.polynomial coefficient array (low to high)."""
    P = np.polynomial.polynomial
    best, arg = np.inf, None
    for a, b in zip(bps[:-1], bps[1:]):
        if b - a <= 0:
            continue
        cands = [a, b]
        if b - a > 1e-9:
            # quadratic piece in local coordinates s = (y - m)/h (well conditioned), then its derivative
            # as a polynomial in y: fun'(y) = (c1 + 2 c2 (y - m)/h)/h
            m, h = 0.5 * (a + b), 0.5 * (b - a)
            s = np.array([-0.5, 0.0, 0.5])
            f0, f1, f2 = fun(m + h * s)
            c2 = (f0 - 2 * f1 + f2) / (2 * 0.25)
            c1 = (f2 - f0) / (2 * 0.5)
            dfun = np.array([c1 / h - 2 * c2 * m / h ** 2, 2 * c2 / h ** 2])
            d = P.polyadd(dfun, P.polyder(poly_extra)) if len(poly_extra) > 1 else dfun
            d = np.trim_zeros(np.asarray(d, float), "b")
            if len(d) >= 2:
                for r in np.roots(d[::-1]):
                    if abs(r.imag) < 1e-9 and a < r.real < b:
                        cands.append(r.real)
        cands = np.array(cands)
        vals = fun(cands) + P.polyval(cands, poly_extra)
        j = int(np.argmin(vals))
        if vals[j] < best:
            best, arg = float(vals[j]), float(cands[j])
    return best, arg


class ClassBound:
    """V_T(B) for T = {1, y, ..., y^d} (class b_d; class a and a0 and b2 are d = 2 for this gadget,
    since c y^2 is the unary term of y) or T = {1, y} with a fixed base split (class env)."""

    def __init__(self, G: Gadget, d=2, c1=None):
        self.G, self.d = G, d
        self.c1 = G.c if c1 is None else c1          # c y^2 share in factor 1
        self.c2 = G.c - self.c1
        self.cache = {}

    def funcs(self, box):
        lx, ux, ly, uy, lz, uz = box
        G = self.G
        F1 = lambda y: G.H1(y, lx, ux) + self.c1 * np.asarray(y) ** 2
        F2 = lambda y: G.H2(y, lz, uz) + self.c2 * np.asarray(y) ** 2
        return F1, F2

    def bound(self, box, tol=1e-12, maxit=200):
        key = tuple(float(v) for v in box)
        if key in self.cache:
            return self.cache[key]
        lx, ux, ly, uy, lz, uz = key
        F1, F2 = self.funcs(key)
        bps = self.G.breakpoints(key)
        Y1 = set(np.linspace(ly, uy, 41).tolist()) | set(bps.tolist())
        Y2 = set(Y1)
        d = self.d
        lower, upper = -np.inf, np.inf
        fool = None
        for it in range(maxit):
            y1a = np.array(sorted(Y1)); y2a = np.array(sorted(Y2))
            m1, m2 = len(y1a), len(y2a)
            V1 = np.vander(y1a, d + 1, increasing=True)   # columns 1, y, ..., y^d
            V2 = np.vander(y2a, d + 1, increasing=True)
            # rows: sum w1 = 1; sum w2 = 1; moments k=1..d: sum w1 y^k - sum w2 y^k = 0
            Aeq = np.zeros((2 + d, m1 + m2))
            Aeq[0, :m1] = 1; Aeq[1, m1:] = 1
            Aeq[2:, :m1] = V1[:, 1:].T; Aeq[2:, m1:] = -V2[:, 1:].T
            beq = np.zeros(2 + d); beq[:2] = 1
            cost = np.concatenate([F1(y1a), F2(y2a)])
            res = linprog(cost, A_eq=Aeq, b_eq=beq, bounds=(0, None), method="highs")
            assert res.status == 0, res.message
            w = res.x
            # explicit fooling: recompute value and residuals
            val = float(cost @ w)
            resid = float(np.max(np.abs(Aeq @ w - beq)))
            if val < upper and resid < 1e-12:
                upper = val
                fool = (y1a[w[:m1] > 0], w[:m1][w[:m1] > 0], y2a[w[m1:] > 0], w[m1:][w[m1:] > 0], resid)
            a = res.eqlin.marginals[2:]                    # multipliers of the moment rows
            # Lagrangian: F1 - a.phi on factor 1, F2 + a.phi on factor 2 (phi = y^k, k>=1)
            rho = np.concatenate([[0.0], -a])             # rho(y) = -sum a_k y^k
            best = -np.inf
            for sgn in (1.0, -1.0):
                m1v, a1 = exact_min(F1, sgn * rho, bps)
                m2v, a2 = exact_min(F2, -sgn * rho, bps)
                if m1v + m2v > best:
                    best, args = m1v + m2v, (a1, a2)
            if best > lower:
                lower = best
            if upper - lower <= tol:
                break
            n_before = len(Y1) + len(Y2)
            Y1.add(args[0]); Y2.add(args[1])
            if len(Y1) + len(Y2) == n_before:
                break
        out = (lower, upper, it + 1, fool)
        self.cache[key] = out
        return out


def bb_product(CB: ClassBound, G, eps, record=None):
    """Widest-side bisection (first index among ties, midpoint) on [-1,1]^{3G}, variable order
    x1,y1,z1,x2,...; delta = 0 so the chain bound is the sum of gadget bounds (see review).
    Prune iff sum of certified lower bounds >= -eps; split iff sum of fooling values < -eps."""
    n = 3 * G
    stack = [(np.full(n, -1.0), np.full(n, 1.0))]
    leaves = nodes = amb = 0
    minmargin_prune, minmargin_split = np.inf, np.inf
    while stack:
        l, u = stack.pop()
        nodes += 1
        lo = up = 0.0
        for g in range(G):
            box = (l[3 * g], u[3 * g], l[3 * g + 1], u[3 * g + 1], l[3 * g + 2], u[3 * g + 2])
            a, b_, _, _ = CB.bound(box)
            lo += a; up += b_
        if lo >= -eps:
            leaves += 1
            minmargin_prune = min(minmargin_prune, lo + eps)
            if record is not None:
                record.append((l.copy(), u.copy()))
            continue
        if up < -eps:
            minmargin_split = min(minmargin_split, -eps - up)
        else:
            amb += 1
        j = int(np.argmax(u - l))
        m = 0.5 * (l[j] + u[j])
        u1 = u.copy(); u1[j] = m
        l2 = l.copy(); l2[j] = m
        stack.append((l, u1)); stack.append((l2, u))
    return dict(leaves=leaves, nodes=nodes, ambiguous=amb, min_prune_margin=minmargin_prune,
                min_split_margin=minmargin_split, distinct_gadget_boxes=len(CB.cache))
