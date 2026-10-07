"""Exact checks for finding C-writing-3 (growth-scope caveat).

(1) Without growth: a box QP with non-unique minimizers still has H_{J0J0} >= 0
    at a minimizer, and its negative curvature lies along an active coordinate.
(2) Example 5.12 block: J0 = {rho}, H_{J0J0} = 2 = 2g with g = 1/2, and the
    negative-curvature direction lies in the active (u, v) coordinates.
(3) Global restriction: kappa >= L*|x'-x*|^2 / (F(x') - OPT). With L = 0 this
    gives nothing: F = -(x-1/2)^2 + eps*x on [0,1] has nearly tied minima at
    distance 1, the largest point-growth constant is eps, and kappa = 1.
"""
import sympy as sp

# (1)
x1, x2 = sp.symbols("x1 x2", real=True)
F = -(x1 - sp.Rational(1, 2)) ** 2
H = sp.hessian(F, (x1, x2))
xs = {x1: 0, x2: sp.Rational(1, 2)}
grad = [sp.diff(F, v).subs(xs) for v in (x1, x2)]
assert F.subs(xs) == F.subs({x1: 1, x2: 0}) == -sp.Rational(1, 4)  # not unique
assert grad[1] == 0 and H[1, 1] >= 0  # J0 = {2}: zeta_J0 = 0, H_J0J0 = [0] PSD
assert H[0, 0] < 0  # negative curvature only along e1, coordinate 1 is at a bound
print("(1) no growth, H_J0J0 =", H[1, 1], ", H_11 =", H[0, 0])

# (2)
u, v, r = sp.symbols("u v rho", real=True)
phi = u**2 + v**2 - 4 * u * v + sp.Rational(1, 4) * (u + v) + (r - u / 2) ** 2
Hb = sp.hessian(phi, (u, v, r))
print("(2) block Hessian eigenvalues:", Hb.eigenvals())
assert Hb[2, 2] == 2  # J0 = {rho}; 2g with g = 1/2
d = sp.Matrix([1, 1, 1])  # (1,1,1): rho moves with u (cancels (rho-u/2)^2 partly)
print("    d^T H d for d=(1,1,1):", (d.T * Hb * d)[0])

# (3)
x, eps, g = sp.symbols("x eps g", positive=True)
F1 = -(x - sp.Rational(1, 2)) ** 2 + eps * x
gap = sp.simplify(F1 - F1.subs(x, 0))
assert sp.simplify(gap - x * (1 + eps - x)) == 0
# gap >= g x^2 on (0,1]  <=>  (1+eps-x)/x >= g; minimum over (0,1] at x = 1
gmax = sp.simplify((1 + eps - x) / x).subs(x, 1)
print("(3) largest g =", gmax, "; L = max(H_11, 0) =", max(sp.diff(F1, x, 2), 0),
      "; kappa = max(1, 0/g) = 1; F(1)-OPT =", sp.simplify(F1.subs(x, 1) - F1.subs(x, 0)))
