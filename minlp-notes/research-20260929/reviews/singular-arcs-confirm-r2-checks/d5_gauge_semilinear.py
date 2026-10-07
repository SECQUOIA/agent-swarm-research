"""Confirmation check d5 (sympy, exact).  Remark 3.5 (new bullet), Section 6
and Section 10 say that E2 is outside Felgenhauer's semilinear class
(min k(x(1)), xdot = f(t,x) + B(t)u) "in every gauge", because the k2 part of
l1 = k1 x1 + k2 x2 "is not a null Lagrangian".

(1) E2: the gauge of Remark 3.5 (add dF/dt = grad F . g to the integrand,
    compensate with F(x0) - F(xT)) with F = -k1 x1^2/2 - k2 x1 x2 gives
    l1 = 0; b = e1 is constant, so the problem is in the class and w = 0.
(2) catmix, reduced 1-D model: theta stays in [0, 1/11] for every admissible
    control, and b(theta) >= 10/121 > 0 there, so y = int dtheta/b is a global
    change of state; then ydot = a/b + u (constant input column) and the
    gauge F(y) = -int l1 dy removes l1."""
import sympy as sp

x1, x2, u, k1, k2 = sp.symbols("x1 x2 u k1 k2", real=True)
g = sp.Matrix([u, x1 - x2])
l0 = (x1 ** 2 + x2 ** 2) / 2
l1 = k1 * x1 + k2 * x2
F = -k1 * x1 ** 2 / 2 - k2 * x1 * x2
dF = (sp.Matrix([F]).jacobian([x1, x2]) * g)[0]
new = sp.expand(l0 + l1 * u + dF)
l1_new = sp.expand(new).coeff(u, 1)
l0_new = sp.expand(new - l1_new * u)
print("E2: new l1 =", sp.simplify(l1_new), "; new l0 =", sp.factor(l0_new))
b = sp.Matrix([1, 0])
# w = -(grad l1 + b_x^T psi) with b constant -> w = -grad l1
w_new = -sp.Matrix([sp.diff(l1_new, x1), sp.diff(l1_new, x2)])
print("E2: w in the new gauge =", list(w_new))
print("E2: Kelley quantity in the new gauge, b^T l0_xx b =", sp.simplify(sp.diff(l0_new, x1, 2)),
      "(note: K = 1 - 2 k2)")
Phi = (k2 - k1) * x1 ** 2 / 2 + (1 - 2 * k2) * x2 ** 2 / 2
print("E2: new terminal cost Phi - F(x_T) =", sp.factor(sp.expand(Phi - F)), "(k1-free); constant F(x0) =",
      F.subs({x1: 1, x2: 0}))

th, y = sp.symbols("theta y", real=True)
a = th ** 2 - th
bb = 1 - 10 * th - th ** 2
print("catmix: thetadot at theta = 1/11:", sp.factor((a + bb * u).subs(th, sp.Rational(1, 11))),
      "(<= 0 for u <= 1); thetadot at theta = 0:", (a + bb * u).subs(th, 0), "(>= 0)")
print("catmix: b on [0, 1/11]: b(0) =", bb.subs(th, 0), ", b(1/11) =", bb.subs(th, sp.Rational(1, 11)),
      ", b decreasing there (b' =", sp.diff(bb, th), "); positive root of b:", [r for r in sp.solve(bb, th) if r > 0][0],
      "=", sp.N([r for r in sp.solve(bb, th) if r > 0][0], 6), "> 1/11 =", sp.N(sp.Rational(1, 11), 6))
print("catmix: with y' (theta) = 1/b: ydot = thetadot / b = a/b + u, input column 1; l1 = theta(y) removed by "
      "F(y) = -int theta dy (1-D), so w = 0 in (y, gauge) coordinates")
