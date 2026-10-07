"""Symbolic rechecks of the revised Section 5 of theory-calibration/scouting.md.

Independent of the review's and the author's scripts.

(a) Non-strict LQ defect (Remark 5.2(d)): for xdot = alpha x + u, l = (u^2 + q x^2)/2,
    V = P x^2/2 with Pdot = P^2 - 2 alpha P - q, the Euler Riccati map is
    F(P') = h q + (1 + alpha h)^2 P' / (1 + h P').  Expand F(P(t+h)) - P(t) in h.
    The note claims h^2 alpha P (P - alpha) + O(h^3) for q = 0.
(b) Tilt threshold (Remark 5.2(e)): residual of V - e' (x - x*)^2 (e' = eps e^{-lam t})
    for the same LQ problem is a quadratic form in (d, v) = (x - x*, u - u*); positive
    definite iff lam > 2 alpha - 2P + 2e'.
(c) U = R counterexample (Remark 5.2(c)): r = (u - x^3)^2/2 + x^6/2 + x^2 and the exact
    identity r - (x^2 + u^2)/4 = (u/2 - x^3)^2 + 3 x^2/4 >= 0.
(d) Coercivity identity (Remark 5.2(b)) for vector states n = 2, m = 1 and random
    polynomial data: zeta^T D^2 r zeta = zeta^T D^2 H zeta + d/dt(xi^T P xi) along
    xdot = g(x,u), xidot = g_x xi + g_u eta, P = S_xx(t, x), H at p = S_x(t, x).
    This is a pointwise algebraic identity; no optimality is used.
"""
import json
import random

import sympy as sp

out = {}

# ------------------------------------------------------------------ (a)
h, al, q = sp.symbols("h alpha q", real=True)
P0, P1, P2 = sp.symbols("P0 P1 P2", real=True)  # P, Pdot, Pddot at t
Pdot = lambda P: P**2 - 2 * al * P - q
# P(t+h) to O(h^3): P + h Pdot + h^2/2 Pddot with Pddot = d/dt Pdot = (2P - 2 alpha) Pdot
Pd1 = Pdot(P0)
Pd2 = (2 * P0 - 2 * al) * Pd1
Pnext = P0 + h * Pd1 + h**2 / 2 * Pd2
F = h * q + (1 + al * h) ** 2 * Pnext / (1 + h * Pnext)
ser = sp.series(F - P0, h, 0, 3).removeO()
c1 = sp.factor(sp.simplify(ser.coeff(h, 1)))
c2 = sp.factor(sp.simplify(ser.coeff(h, 2)))
c2_q0 = sp.factor(c2.subs(q, 0))
out["a"] = {"order_h_coeff": str(c1), "order_h2_coeff_general_q": str(c2),
            "order_h2_coeff_q0": str(c2_q0),
            "matches_note_q0": bool(sp.simplify(c2_q0 - al * P0 * (P0 - al)) == 0)}
print("a", out["a"])

# ------------------------------------------------------------------ (b)
d, v, P, e, lam = sp.symbols("d v P e lam", real=True)
# field residual (u + P x)^2/2 = (v + P d)^2/2 since u* = -P x*
# tilt adds e [lam d^2 - 2 d (g - g*)], g - g* = alpha d + v
r_tot = (v + P * d) ** 2 / 2 + e * (lam * d**2 - 2 * d * (al * d + v))
M = sp.hessian(r_tot, (d, v)) / 2
det = sp.factor(sp.simplify(M.det()))
out["b"] = {"form_matrix": str(M), "det": str(det),
            "det_equals_e_times_(lam/2 - alpha + P - e)": bool(
                sp.simplify(det - e * (lam / 2 - al + P - e)) == 0)}
print("b", out["b"])

# ------------------------------------------------------------------ (c)
x, u = sp.symbols("x u", real=True)
r = u**2 / 2 + x**6 + x**2 + (-x**3) * u  # l + S_x g with S = -x^4/4, g = u
out["c"] = {
    "r_equals_note_form": bool(sp.expand(r - ((u - x**3) ** 2 / 2 + x**6 / 2 + x**2)) == 0),
    "r_minus_quarter_norm_identity": bool(
        sp.expand(r - (x**2 + u**2) / 4 - ((u / 2 - x**3) ** 2 + sp.Rational(3, 4) * x**2)) == 0),
    "jump_cost_X1000": {str(hh): float(1000.0**2 / (2 * hh) + 1000.0**2 / 2 - 1000.0**4 / 4)
                        for hh in (0.1, 0.01, 0.001)},
}
print("c", out["c"])

# ------------------------------------------------------------------ (d)
random.seed(3)
t = sp.symbols("t", real=True)
x1, x2, uu = sp.symbols("x1 x2 uu", real=True)
xi1, xi2, eta = sp.symbols("xi1 xi2 eta", real=True)
X = sp.Matrix([x1, x2])
monos = [1, x1, x2, uu, x1 * x2, x1**2, x2**2, uu**2, x1 * uu, x2 * uu, x1**3, x2**2 * uu, x1 * x2 * uu]
smonos = [x1, x2, x1 * x2, x1**2, x2**2, x1**3, x1**2 * x2, x2**3, x1 * x2**2, x1**4, x2**4]


def rnd_poly(ms):
    return sum(sp.Rational(random.randint(-5, 5), random.randint(1, 4)) * m for m in ms)


S = sum(sp.Rational(random.randint(-5, 5), 3) * m * (1 + sp.Rational(random.randint(-3, 3), 2) * t
                                                     + sp.Rational(random.randint(-3, 3), 5) * t**2)
        for m in smonos)
l = rnd_poly(monos)
g = sp.Matrix([rnd_poly(monos), rnd_poly(monos)])
Sx = sp.Matrix([sp.diff(S, x1), sp.diff(S, x2)])
rfun = l + sp.diff(S, t) + (Sx.T * g)[0]
Z = [x1, x2, uu]
zeta = sp.Matrix([xi1, xi2, eta])
Hr = sp.hessian(rfun, Z)
# H(x,u,p) with p frozen at S_x(t, x) at the evaluation point
p1, p2 = sp.symbols("p1 p2")
Hfun = l + p1 * g[0] + p2 * g[1]
HH = sp.hessian(Hfun, Z).subs({p1: Sx[0], p2: Sx[1]})
Pm = sp.hessian(S, [x1, x2])
# total time derivative of P along xdot = g
Pdot_m = Pm.diff(t) + Pm.diff(x1) * g[0] + Pm.diff(x2) * g[1]
gx = g.jacobian([x1, x2])
gu = g.jacobian([uu])
xivec = sp.Matrix([xi1, xi2])
xidot = gx * xivec + gu * sp.Matrix([eta])
lhs = (zeta.T * Hr * zeta)[0]
rhs = (zeta.T * HH * zeta)[0] + (xivec.T * Pdot_m * xivec)[0] + 2 * (xivec.T * Pm * xidot)[0]
diff = sp.expand(lhs - rhs)
out["d"] = {"identity_holds_n2_m1_random_polynomials": diff == 0}
print("d", out["d"])

with open("logs/r1_symbolic.json", "w") as fh:
    json.dump(out, fh, indent=1)
