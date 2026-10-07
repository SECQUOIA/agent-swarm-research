"""Confirmation recheck of scouting.md, second revision: symbolic checks.
New code, written independently of revision_checks.py, recheck_revision_checks.py and
the earlier reviewers' scripts.

(a) R5: Euler Riccati defect F(P(t+h)) - P(t) for xdot = alpha x + u,
    l = (u^2 + q x^2)/2, F(P) = h q + (1 + alpha h)^2 P / (1 + h P).
    Method: P(t+h) as a Taylor series whose coefficients are total derivatives along
    Pdot = P^2 - 2 alpha P - q, computed with a derivation operator on polynomials in
    the symbols P and E (E = e(t) = eps exp(-lam t), Edot = -lam E).
(b) R2: tilted curvature s = P - 2E: the O(h) term and the O(h^2) term.
(c) R5: alpha = q = 0 exact zero; alpha = 0, q = 1, Phi = 0 (P = tanh(T - t)): the
    exact sign of F(P(t+h)) - P(t) on a grid (not only to leading order).
(d) R8/optional (b): the coercivity identity for n = 3 states, m = 2 controls,
    time-dependent l, random polynomial data, at a general point.
(e) R2: scalar LQ tilt determinant and the Young-inequality sketch bound.
(f) optional (c): U = R identity and last-stage residual.
"""
import json
import os
import random
import time

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
t0 = time.time()
out = {}

h, al, q, lam, T = sp.symbols("h alpha q lambda T", real=True)
P, E = sp.symbols("P E", real=True)
PDOT = P**2 - 2 * al * P - q


def D(expr):
    """Total time derivative along Pdot = PDOT, Edot = -lam E."""
    return sp.expand(sp.diff(expr, P) * PDOT + sp.diff(expr, E) * (-lam * E))


def shifted(expr, order):
    """expr(t + h) as a polynomial in h up to h^order."""
    acc, d = 0, expr
    for k in range(order + 1):
        acc += d * h**k / sp.factorial(k)
        d = D(d)
    return sp.expand(acc)


def F(Pn):
    return h * q + (1 + al * h) ** 2 * Pn / (1 + h * Pn)


def defect_coeffs(s_expr, order=3):
    ser = sp.series(F(shifted(s_expr, order)) - s_expr, h, 0, order + 1).removeO()
    return [sp.factor(sp.simplify(ser.coeff(h, k))) for k in range(order + 1)]


# (a) untilted
c = defect_coeffs(P, 3)
K = (P - al) * (al * P + q)
out["a"] = {
    "h0": str(c[0]), "h1": str(c[1]), "h2": str(c[2]), "h3": str(c[3]),
    "h2_equals_(P-alpha)(alpha P+q)": sp.simplify(c[2] - K) == 0,
    "q0_h2_equals_alpha P (P-alpha)": sp.simplify(c[2].subs(q, 0) - al * P * (P - al)) == 0,
}
# numeric cross-check with the closed-form P of case alpha=-2, q=0, phiT=1
Pc = lambda tt: 1.0 / (-0.25 + 1.25 * np.exp(4.0 * (1.0 - tt)))
num = []
for tt in (0.1, 0.5, 0.9):
    for hh in (1e-2, 1e-3):
        Pn = Pc(tt + hh)
        Fv = (1 - 2 * hh) ** 2 * Pn / (1 + hh * Pn)
        Kv = (Pc(tt) + 2) * (-2 * Pc(tt))
        num.append({"t": tt, "h": hh, "defect_over_h2": (Fv - Pc(tt)) / hh**2, "K": Kv})
out["a"]["numeric_case1"] = num

# (b) tilted
ct = defect_coeffs(P - 2 * E, 2)
out["b"] = {
    "h1": str(ct[1]),
    "h1_equals_4E(lam/2-alpha+P-E)": sp.simplify(ct[1] - 4 * E * (lam / 2 - al + P - E)) == 0,
    "h2_minus_K_vanishes_at_E=0": sp.simplify((ct[2] - K).subs(E, 0)) == 0,
    "h2_minus_K": str(sp.factor(sp.simplify(ct[2] - K))),
}

# (c) exact cases
c_ = sp.symbols("c", positive=True)
tt_ = sp.symbols("t", real=True)
Pex = 1 / (c_ + T - tt_)
Pn = Pex.subs(tt_, tt_ + h)
out["c"] = {"alpha=q=0_exact_zero": sp.simplify(Pn / (1 + h * Pn) - Pex) == 0}
worst = np.inf
for hh in np.geomspace(1e-4, 1.0, 60):
    tt = np.linspace(0.0, 1.0 - hh, 400)
    Pn = np.tanh(1.0 - (tt + hh))
    d = hh + Pn / (1 + hh * Pn) - np.tanh(1.0 - tt)
    worst = min(worst, float(np.min(d / hh**2)))
out["c"]["alpha0_q1_phi0_min_defect_over_h2"] = worst

# (d) coercivity identity, n = 3, m = 2
random.seed(20260930)
xs = sp.symbols("x1:4", real=True)
us = sp.symbols("u1:3", real=True)
ts = sp.symbols("t", real=True)
Z = list(xs) + list(us)
xis = sp.Matrix(sp.symbols("xi1:4", real=True))
ets = sp.Matrix(sp.symbols("eta1:3", real=True))


def rpoly(vars_, deg, nterms):
    mons = []
    for _ in range(nterms):
        m = 1
        for _k in range(random.randint(0, deg)):
            m *= random.choice(vars_)
        mons.append(sp.Rational(random.randint(-5, 5), random.randint(1, 4)) * m)
    return sum(mons)


S = rpoly(list(xs), 4, 8) * (1 + ts) + ts**2 * rpoly(list(xs), 3, 4)
l = rpoly(Z, 3, 10) + sp.sin(ts) * rpoly(Z, 2, 5)
g = sp.Matrix([rpoly(Z, 2, 6) for _ in range(3)])
Sx = sp.Matrix([sp.diff(S, v) for v in xs])
r = l + sp.diff(S, ts) + (Sx.T * g)[0]
pp = sp.symbols("p1:4", real=True)
Hfix = l + sum(pp[i] * g[i] for i in range(3))
HessH = sp.hessian(Hfix, Z).subs({pp[i]: Sx[i] for i in range(3)})
Pm = sp.hessian(S, list(xs))
Pdot = sp.diff(Pm, ts) + sum((sp.diff(Pm, xs[k]) * g[k] for k in range(3)), sp.zeros(3, 3))
xidot = g.jacobian(list(xs)) * xis + g.jacobian(list(us)) * ets
zeta = sp.Matrix(list(xis) + list(ets))
lhs = (zeta.T * sp.hessian(r, Z) * zeta)[0]
rhs = (zeta.T * HessH * zeta)[0] + (xis.T * Pdot * xis)[0] + 2 * (xis.T * Pm * xidot)[0]
out["d"] = {"identity_n3_m2_time_dependent_l": sp.simplify(sp.expand(lhs - rhs)) == 0}

# (e) scalar LQ tilt
d_, v_, e_, Pp, lam_ = sp.symbols("d v e P lam", real=True)
# r_S = v^2/2 + e[(lam - 2 alpha + 2P) d^2 - 2 d v] with v = u - u_f, u_f = -P x
rS = v_**2 / 2 + e_ * ((lam_ - 2 * al + 2 * Pp) * d_**2 - 2 * d_ * v_)
Mq = sp.hessian(rS, [d_, v_]) / 2
out["e"] = {
    "det": str(sp.factor(Mq.det())),
    "det_equals_e(lam/2-alpha+P-e)": sp.simplify(Mq.det() - e_ * (lam_ / 2 - al + Pp - e_)) == 0,
}
# direct derivation of r_S from S = P x^2/2 - e (x - xs)^2, xdot = alpha x + u, l = (u^2 + q x^2)/2
x_, u_, xs_, us_, tsym = sp.symbols("x u xs us t", real=True)
Pt, et, xst = sp.Function("P")(tsym), sp.Function("e")(tsym), sp.Function("xs")(tsym)
Ssym = Pt * x_**2 / 2 - et * (x_ - xst) ** 2
gsym = al * x_ + u_
rsym = (u_**2 + q * x_**2) / 2 + sp.diff(Ssym, tsym) + sp.diff(Ssym, x_) * gsym
rsym = rsym.subs({sp.Derivative(Pt, tsym): Pt**2 - 2 * al * Pt - q,
                  sp.Derivative(et, tsym): -lam_ * et,
                  sp.Derivative(xst, tsym): al * xst - Pt * xst})
target = (u_ + Pt * x_) ** 2 / 2 + et * ((lam_ - 2 * al + 2 * Pt) * (x_ - xst) ** 2 - 2 * (x_ - xst) * (u_ + Pt * x_))
out["e"]["r_S_formula_from_S"] = sp.simplify(sp.expand(rsym - target)) == 0
# Young sketch: L1 = alpha - P, L2 = 1, c_W = 1/2 => bound v^2/4 + e(lam - 2L1 - 4e) d^2
bound = v_**2 / 4 + e_ * (lam_ - 2 * (al - Pp) - 4 * e_) * d_**2
out["e"]["rS_minus_sketch_bound"] = str(sp.factor(sp.expand(rS - bound)))
out["e"]["rS_minus_sketch_bound_is_square"] = sp.simplify(sp.expand(rS - bound - (v_ / 2 - 2 * e_ * d_) ** 2)) == 0

# (f) U = R example
x, u = sp.symbols("x u", real=True)
rr = u**2 / 2 + x**6 + x**2 + sp.diff(-x**4 / 4, x) * u
out["f"] = {
    "identity": sp.expand(rr - (x**2 + u**2) / 4 - (u / 2 - x**3) ** 2 - sp.Rational(3, 4) * x**2) == 0,
    "last_stage_x0": str(sp.factor(sp.expand(h * u**2 / 2 + (-(h * u) ** 4 / 4) - 0))),
}
out["runtime_s"] = time.time() - t0
for k_, v in out.items():
    print(k_, v)
with open(os.path.join(HERE, "logs", "k1_symbolic.json"), "w") as fh:
    json.dump(out, fh, indent=1, default=str)
