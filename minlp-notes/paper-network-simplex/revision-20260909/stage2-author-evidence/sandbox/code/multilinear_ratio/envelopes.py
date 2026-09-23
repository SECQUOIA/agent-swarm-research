"""Envelopes of positive multilinear functions on [0,1]^n and the term-by-term gap ratio.

Notation follows Luedtke, Namazifar, Linderoth (Math. Program. 136, 2012):

    phi(x) = sum_{t in T} a_t prod_{j in t} x_j,   a_t > 0,  x in H = [0,1]^n.

    cav_H[phi](x), vex_H[phi](x)  : concave / convex envelope, LPs (7)-(8) over the 2^n vertices.
    chgap(x)  = cav_H[phi](x) - vex_H[phi](x)                         (convex-hull gap)
    tbt_u(x)  = sum_t a_t cav_H[f_t](x) = sum_t a_t min_{j in t} x_j    (term-by-term upper bound)
    tbt_l(x)  = sum_t a_t vex_H[f_t](x) = sum_t a_t max(0, sum_{j in t} x_j - |t| + 1)
    tbtgap(x) = tbt_u(x) - tbt_l(x)                                   (term-by-term gap;
                                                                       = mcgap for bilinear phi)
    ratio(x)  = tbtgap(x) / chgap(x).

Theorem 4 of the paper gives cav_H[phi] = tbt_u for positive coefficients, so
tbtgap - chgap = vex_H[phi] - tbt_l >= 0 and ratio(x) >= 1.
"""
from __future__ import annotations

from fractions import Fraction
import itertools
import math

import numpy as np
from scipy.optimize import linprog


class Multilinear:
    """Multilinear function with positive coefficients on [0,1]^n."""

    def __init__(self, n, terms):
        self.n = n
        self.terms = []
        for a, t in terms:
            t = tuple(sorted(set(int(j) for j in t)))
            if not (0 <= t[0] and t[-1] < n):
                raise ValueError("term index out of range")
            if a <= 0:
                raise ValueError("coefficients must be positive (Conjecture 1 setting)")
            self.terms.append((float(a), t))
        codes = np.arange(2 ** n)
        self.V = ((codes[:, None] >> np.arange(n)[None, :]) & 1).astype(float)  # 2^n x n
        self.phi_v = np.zeros(2 ** n)
        for a, t in self.terms:
            self.phi_v += a * self.V[:, list(t)].prod(axis=1)
        # equality matrix of LP (8): sum_v lam_v v = x, sum_v lam_v = 1
        self.A_eq = np.vstack([self.V.T, np.ones((1, 2 ** n))])

    # ---- closed forms -------------------------------------------------
    def phi(self, x):
        x = np.asarray(x, float)
        return sum(a * x[list(t)].prod() for a, t in self.terms)

    def cav(self, x):
        """Concave envelope = term-by-term upper bound (Theorem 4)."""
        x = np.asarray(x, float)
        return sum(a * x[list(t)].min() for a, t in self.terms)

    def tbt_l(self, x):
        """Term-by-term lower bound: sum of convex envelopes of the monomials."""
        x = np.asarray(x, float)
        return sum(a * max(0.0, x[list(t)].sum() - len(t) + 1) for a, t in self.terms)

    # ---- LP envelopes --------------------------------------------------
    def vex(self, x, return_lp=False):
        """Convex envelope via LP (8): min sum lam_v phi(v), sum lam_v v = x, lam in simplex."""
        x = np.asarray(x, float)
        b = np.append(x, 1.0)
        res = linprog(self.phi_v, A_eq=self.A_eq, b_eq=b, bounds=(0, None), method="highs")
        if res.status != 0:
            raise RuntimeError(f"vex LP failed: {res.message}")
        return (res.fun, res) if return_lp else res.fun

    def cav_lp(self, x):
        """Concave envelope via LP (7); used only to check Theorem 4 numerically."""
        x = np.asarray(x, float)
        b = np.append(x, 1.0)
        res = linprog(-self.phi_v, A_eq=self.A_eq, b_eq=b, bounds=(0, None), method="highs")
        return -res.fun

    def gaps(self, x):
        """Return (tbtgap, chgap)."""
        c = self.cav(x)
        return c - self.tbt_l(x), c - self.vex(x)

    def ratio(self, x, tol=1e-9):
        """tbtgap/chgap; returns 1.0 when both gaps vanish (limit is finite, see README)."""
        g_t, g_h = self.gaps(x)
        if g_h <= tol:
            return 1.0 if g_t <= tol else math.inf
        return g_t / g_h

    # ---- exact rational certificate --------------------------------------
    def phi_exact(self, x):
        x = [Fraction(v) for v in x]
        tot = Fraction(0)
        for a, t in self.terms:
            p = Fraction(a)
            for j in t:
                p *= x[j]
            tot += p
        return tot

    def exact_gaps(self, x, tol=1e-7):
        """Exact (Fraction) tbtgap, chgap, ratio at a rational point x.

        vex is certified by an exact primal solution (lambda on the numerically optimal
        support, re-solved in rational arithmetic) and an exact dual solution
        (affine minorant pi.v + pi0 <= phi(v) checked on all 2^n vertices) with equal value.
        """
        import sympy

        x = [Fraction(v) for v in x]
        n = self.n
        if any(v < 0 or v > 1 for v in x):
            raise ValueError("x outside box")
        xf = np.array([float(v) for v in x])
        val, res = self.vex(xf, return_lp=True)
        lam = res.x
        # exact primal: solve restricted system on the support in rationals
        S = np.where(lam > tol)[0]
        Vq = sympy.Matrix([[sympy.Integer(int(self.V[v, j])) for j in range(n)] + [1] for v in S]).T
        rhs = sympy.Matrix([sympy.Rational(v.numerator, v.denominator) for v in x] + [1])
        sol = Vq.gauss_jordan_solve(rhs)
        lam_q = sol[0]
        if sol[1].shape[0] > 0:  # free parameters (degenerate support): set them to 0
            lam_q = lam_q.subs({p: 0 for p in sol[1]})
        lam_q = [Fraction(int(sympy.fraction(v)[0]), int(sympy.fraction(v)[1])) for v in lam_q]
        if any(l < 0 for l in lam_q):
            raise RuntimeError("exact primal not nonnegative; increase support tolerance")
        phi_q = [self.phi_exact(self.V[v]) for v in S]
        primal_val = sum(l * p for l, p in zip(lam_q, phi_q))
        # exact dual: active vertices of the numerically optimal affine minorant
        duals = res.eqlin.marginals  # d(obj)/d(b_eq): (pi, pi0)
        pi = np.array(duals[:n]);  pi0 = duals[n]
        slack = self.phi_v - (self.V @ pi + pi0)
        act = np.where(slack < 1e-6)[0]
        A = sympy.Matrix([[sympy.Integer(int(self.V[v, j])) for j in range(n)] + [1] for v in act])
        bq = sympy.Matrix([sympy.Rational(self.phi_exact(self.V[v])) for v in act])
        dsol = A.gauss_jordan_solve(bq)
        pq = dsol[0]
        if dsol[1].shape[0] > 0:
            pq = pq.subs({p: 0 for p in dsol[1]})
        pq = [Fraction(int(sympy.fraction(v)[0]), int(sympy.fraction(v)[1])) for v in pq]
        # dual feasibility on all vertices, exactly
        for v in range(2 ** n):
            lhs = sum(pq[j] * int(self.V[v, j]) for j in range(n)) + pq[n]
            if lhs > self.phi_exact(self.V[v]):
                raise RuntimeError("exact dual infeasible; certificate failed")
        dual_val = sum(pq[j] * x[j] for j in range(n)) + pq[n]
        if dual_val != primal_val:
            raise RuntimeError(f"primal/dual mismatch {primal_val} vs {dual_val}")
        vex_q = primal_val
        cav_q = sum(Fraction(a) * min(x[j] for j in t) for a, t in self.terms)
        tbtl_q = sum(Fraction(a) * max(Fraction(0), sum(x[j] for j in t) - len(t) + 1) for a, t in self.terms)
        tbtgap = cav_q - tbtl_q
        chgap = cav_q - vex_q
        return {"cav": cav_q, "vex": vex_q, "tbt_l": tbtl_q, "tbtgap": tbtgap, "chgap": chgap,
                "ratio": tbtgap / chgap if chgap else None}

    def describe(self):
        return f"n={self.n}, |T|={len(self.terms)}, degrees={sorted(set(len(t) for _, t in self.terms))}"
