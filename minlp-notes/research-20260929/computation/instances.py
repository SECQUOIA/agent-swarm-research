"""Probe3 chain family: definition, derivatives, local optimization, SCIP models.

F(x) = sum_{i<n} (x_i^2 - kappa x_i^4 + c_i x_i) + b sum_{i<n-1} x_i x_{i+1},
x in [-1, 1]^n, c = numpy.random.default_rng(seed).uniform(-0.3, 0.3, n).

This is exactly the objective of research-20260929/scratch/probe3.py after
eliminating the epigraph variables t_i (at an optimum t_i equals its right-hand
side). Default kappa = 0.1, b = 0.8.
"""
import numpy as np
from scipy.optimize import minimize

KAPPA = 0.1
B = 0.8


def coeffs(n, seed, amp=0.3):
    """amp = 0.3 is probe3. Other amplitudes give the same instances scaled by amp/0.3."""
    return np.random.default_rng(seed).uniform(-amp, amp, n)


def F(x, c, kappa=KAPPA, b=B):
    x = np.asarray(x, float)
    return float(np.sum(x * x - kappa * x**4 + c * x) + b * np.sum(x[:-1] * x[1:]))


def grad(x, c, kappa=KAPPA, b=B):
    x = np.asarray(x, float)
    g = 2 * x - 4 * kappa * x**3 + c
    g[:-1] += b * x[1:]
    g[1:] += b * x[:-1]
    return g


def hess_tridiag(x, kappa=KAPPA, b=B):
    """Diagonal and off-diagonal of the (tridiagonal) Hessian at x."""
    x = np.asarray(x, float)
    return 2 - 12 * kappa * x * x, np.full(len(x) - 1, b)


def local_min(x0, c, kappa=KAPPA, b=B, lb=-1.0, ub=1.0):
    n = len(c)
    r = minimize(F, np.clip(x0, lb, ub), jac=grad, args=(c, kappa, b), method="L-BFGS-B",
                 bounds=[(lb, ub)] * n, options=dict(ftol=1e-15, gtol=1e-12, maxiter=10000))
    return r.x, r.fun


# ---------------------------------------------------------------- SCIP models

def build_scip(n, seed, variant="default", kappa=KAPPA, b=B, amp=0.3):
    """Build the probe3 model. variant 'single' uses one nonlinear constraint
    for the whole objective; every other variant uses probe3's formulation."""
    from pyscipopt import Model, quicksum
    c = coeffs(n, seed, amp)
    m = Model()
    m.hideOutput()
    x = [m.addVar(lb=-1, ub=1, name=f"x{i}") for i in range(n)]
    if variant == "single":
        t = m.addVar(lb=None, name="t")
        expr = quicksum(x[i] * x[i] - kappa * x[i] ** 4 for i in range(n))
        expr = expr + quicksum(b * x[i] * x[i + 1] for i in range(n - 1))
        expr = expr + quicksum(float(c[i]) * x[i] for i in range(n))
        m.addCons(t >= expr)
        m.setObjective(t, "minimize")
        tvars = [t]
    else:
        tvars = []
        for i in range(n):
            ti = m.addVar(lb=None, name=f"t{i}")
            expr = x[i] * x[i] - kappa * x[i] ** 4
            if i < n - 1:
                expr = expr + b * x[i] * x[i + 1]
            m.addCons(ti >= expr)
            tvars.append(ti)
        m.setObjective(quicksum(tvars) + quicksum(float(c[i]) * x[i] for i in range(n)), "minimize")
    return m, x, tvars, c


# ------------------------------------------------ chain problem for chain_bb.py

class Probe3Chain:
    """phi_i(x) = x^2 - kappa x^4 + c_i x,  psi_e(x, y) = b x y,  box [-1, 1]^n."""

    def __init__(self, c, kappa=KAPPA, b=B):
        assert kappa >= 0
        self.c = np.asarray(c, float)
        self.n = len(c)
        self.kappa, self.bval = kappa, b
        self.lo, self.hi = -np.ones(self.n), np.ones(self.n)
        self.cert = None

    def F(self, x):
        return F(x, self.c, self.kappa, self.bval)

    def local_opt(self, x0):
        return local_min(x0, self.c, self.kappa, self.bval)

    def pair_grad(self, x):
        return self.bval * x[1:], self.bval * x[:-1]

    def pair_cross(self):
        return np.full(self.n - 1, abs(self.bval))

    def unary_lb(self, i, p, q, Qt, Lt):
        from chain_bb import taylor2_lb
        k, ci = self.kappa, self.c[i] + Lt
        m, r = 0.5 * (p + q), 0.5 * (q - p)
        val = (1 - Qt) * m * m - k * m**4 + ci * m
        g = 2 * (1 - Qt) * m - 4 * k * m**3 + ci
        Hlo = 2 * (1 - Qt) - 12 * k * np.maximum(p * p, q * q)
        return taylor2_lb(val, g, Hlo, r)

    def pair_lb(self, e, p, q, s, t, rhoL, alpha, rhoR, beta):
        from chain_bb import quad_box_min
        return quad_box_min(rhoL, np.full_like(p, self.bval), rhoR, -alpha, -beta, p, q, s, t)

    def hessian_is_pd_on_box(self, lo, hi):
        """Certify that F is strictly convex on the box [lo, hi] inside the open
        box (-1, 1)^n. Hessian = diag(2 - 12 kappa x_i^2) + b (off-diagonal);
        on the box it dominates (Loewner order) the constant tridiagonal matrix
        M with diagonal 2 - 12 kappa max(lo_i^2, hi_i^2)."""
        from scipy.linalg import eigvalsh_tridiagonal
        d = 2 - 12 * self.kappa * np.maximum(lo * lo, hi * hi)
        lmin = float(eigvalsh_tridiagonal(d, np.full(self.n - 1, self.bval),
                                          select="i", select_range=(0, 0))[0])
        interior = bool((lo > -1).all() and (hi < 1).all())
        self.cert = dict(lmin=lmin, interior=interior, hull_maxwidth=float((hi - lo).max()),
                         hull_maxabs=float(np.maximum(abs(lo), abs(hi)).max()))
        return interior and lmin > 1e-8
