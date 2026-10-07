"""Round-3 confirmation review of theory-bangbang/singular-arcs.md, item S1.
Independent of the note's revision3_semilinear.py (no shared code).

E2  (symbolic): gauge F = -k1 x1^2/2 - k2 x1 x2; new l0, l1, terminal cost,
     constant; w in the augmented Mayer form; Kelley quantity from the
     closed formula K = b^T l0_xx b + psi^T a_xx[b,b] (valid for b constant,
     l1 = 0; a is linear here, so K = d^2 l0/dx1^2).
E2  (float): continuous costs agree for a random control (ODE), and the
     Euler costs differ by exactly -1/2 h^2 sum g^T F_xx g (quadratic F).
catmix (symbolic): reachable-set boundary, sign of b, xi = int dtheta/b and
     gauge dF/dxi = -theta; new l0; singular-point equation; K = b^2 l0''
     at theta_s (psi_xi = 0 on the arc after the gauge, l0' = 0 there).
catmix (float): C = int(-theta + theta u) equals the gauged cost for random
     controls (ODE), and theta stays in [0, 1/11] for random controls.
"""
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp, quad

rng = np.random.default_rng(12345)

# ---------------- E2 symbolic ----------------
x1, x2, u, k1, k2 = sp.symbols("x1 x2 u k1 k2", real=True)
g = sp.Matrix([u, x1 - x2])
X = sp.Matrix([x1, x2])
l0 = (x1**2 + x2**2) / 2
l1 = k1 * x1 + k2 * x2
Phi = ((k2 - k1) * x1**2 + (1 - 2 * k2) * x2**2) / 2
F = -k1 * x1**2 / 2 - k2 * x1 * x2
gradF = sp.Matrix([sp.diff(F, v) for v in X])
L_new = sp.expand(l0 + l1 * u + (gradF.T * g)[0])
l1n, l0n = sp.expand(L_new.coeff(u, 1)), sp.expand(L_new.coeff(u, 0))
Phin = sp.expand(Phi - F)
print("E2 new l1:", l1n)
print("E2 new l0 - [(x1^2+x2^2)/2 - k2 x1 (x1 - x2)]:", sp.simplify(l0n - ((x1**2 + x2**2) / 2 - k2 * x1 * (x1 - x2))))
print("E2 new terminal - 1/2(k2 x1^2 + 2 k2 x1 x2 + (1-2k2) x2^2):",
      sp.simplify(Phin - (k2 * x1**2 + 2 * k2 * x1 * x2 + (1 - 2 * k2) * x2**2) / 2), "; has k1:", Phin.has(k1))
print("E2 constant F(x0):", F.subs({x1: 1, x2: 0}))
# augmented Mayer form: state (x0c, x1, x2); input column (l1n, 1, 0)
print("E2 augmented input column:", [l1n, 1, 0], "-> state independent:", all(sp.diff(c, v) == 0 for c in [l1n] for v in (x1, x2)))
K_formula = sp.diff(l0n, x1, 2)  # b = e1, a linear, l1 = 0
print("E2 Kelley (closed formula b^T l0_xx b):", sp.factor(K_formula))
print("E2 F_xx:", sp.hessian(F, (x1, x2)))

# ---------------- E2 float ----------------
def e2_cont(k1v, uf, gauge):
    k2v = 0.25
    def rhs(t, y):
        a, b_ = y[0], y[1]
        uu = uf(t)
        if gauge:
            L = (a * a + b_ * b_) / 2 - k2v * a * (a - b_)
        else:
            L = (a * a + b_ * b_) / 2 + (k1v * a + k2v * b_) * uu
        return [uu, a - b_, L]
    s = solve_ivp(rhs, [0, 3], [1.0, 0.0, 0.0], rtol=1e-12, atol=1e-13, max_step=0.01)
    a, b_, c = s.y[:, -1]
    if gauge:
        return c + 0.5 * (k2v * a * a + 2 * k2v * a * b_ + (1 - 2 * k2v) * b_ * b_) - k1v / 2
    return c + 0.5 * ((k2v - k1v) * a * a + (1 - 2 * k2v) * b_ * b_)

coef = rng.uniform(-1, 1, 6)
uf = lambda t: np.clip(np.sum(coef * np.sin(np.arange(1, 7) * t)), -1, 1)
for k1v in (-0.5, 0.0, 0.5):
    print("E2 continuous, k1=%+.1f: J_old - (J_new + F(x0)) = %.2e" % (k1v, e2_cont(k1v, uf, False) - e2_cont(k1v, uf, True)))

def e2_euler(k1v, U, gauge):
    N = len(U); h = 3.0 / N; k2v = 0.25
    x = np.array([1.0, 0.0]); J = 0.0; S = 0.0
    Fxx = np.array([[-k1v, -k2v], [-k2v, 0.0]])
    for t in range(N):
        gg = np.array([U[t], x[0] - x[1]])
        if gauge:
            J += h * ((x @ x) / 2 - k2v * x[0] * (x[0] - x[1]))
        else:
            J += h * ((x @ x) / 2 + (k1v * x[0] + k2v * x[1]) * U[t])
        S += 0.5 * h * h * gg @ Fxx @ gg
        x = x + h * gg
    if gauge:
        J += 0.5 * (k2v * x[0]**2 + 2 * k2v * x[0] * x[1] + (1 - 2 * k2v) * x[1]**2) - k1v / 2
    else:
        J += 0.5 * ((k2v - k1v) * x[0]**2 + (1 - 2 * k2v) * x[1]**2)
    return J, S

for k1v in (-0.5, 0.0, 0.5):
    U = rng.uniform(-1, 1, 100)
    Jo, S = e2_euler(k1v, U, False)
    Jn, _ = e2_euler(k1v, U, True)
    print("E2 Euler N=100, k1=%+.1f: J_new(+F(x0)) - J_old = %.6e, -1/2 h^2 sum g^T F_xx g = %.6e, diff %.1e"
          % (k1v, Jn - Jo, -S, Jn - Jo + S))

# ---------------- catmix symbolic ----------------
th, q = sp.symbols("theta q", real=True)
a = th**2 - th
b = 1 - 10 * th - th**2
print("catmix thetadot at 0:", sp.factor((a + b * u).subs(th, 0)), "; at 1/11:", sp.factor((a + b * u).subs(th, sp.Rational(1, 11))))
print("catmix b(1/11):", b.subs(th, sp.Rational(1, 11)), "; positive root of b:", sp.nsimplify(sp.solve(b, th)[0]), "=",
      float(sp.sqrt(26) - 5), "> 1/11 =", float(sp.Rational(1, 11)))
# xi-formulation: dxi/dtheta = 1/b; xidot = a/b + u; cost l0 = -theta, l1 = theta
# gauge: add dF/dt = F_xi * xidot = -theta (a/b + u)
l0x = sp.simplify(-th + (-th) * (a / b))
l1x = sp.simplify(th - th)
print("catmix xi: l1 =", l1x, "; l0 - theta(11 theta - 1)/b =", sp.simplify(l0x - th * (11 * th - 1) / b))
d1 = sp.factor(sp.numer(sp.together(sp.diff(l0x, th))))
print("catmix xi: numerator of dl0/dtheta:", d1)
ths = (11 - sp.sqrt(10)) / 111
# K = l0_xixi + q A_xixi with q = 0; l0_xixi = b d/dtheta (b dl0/dtheta)
l0xx = b * sp.diff(b * sp.diff(l0x, th), th)
Kval = sp.radsimp(sp.nsimplify(sp.simplify(l0xx.subs(th, ths))))
print("catmix xi: K = l0_xixi at theta_s =", Kval, "=", float(l0xx.subs(th, ths)), "; 2 sqrt 10 =", float(2 * sp.sqrt(10)))
# costate check: in theta, b psi = -theta on the arc; psi_xi = b psi_theta = -theta; after gauge q = psi_xi - F_xi = -theta + theta = 0
print("catmix xi: costate on the arc after gauge = -theta - (-theta) = 0 (hand)")

# ---------------- catmix float ----------------
bf = sp.lambdify(th, b); af = sp.lambdify(th, a); l0f = sp.lambdify(th, l0x)
Ff = lambda T_: -quad(lambda s: s / bf(s), 0, T_, epsabs=1e-14, epsrel=1e-13)[0]  # F(xi(theta)) = -int theta dxi
maxth = 0.0; minth = 1.0
for trial in range(5):
    c = rng.uniform(-3, 3, 6)
    ufc = lambda t: 1.0 / (1 + np.exp(-np.sum(c * np.sin(np.arange(1, 7) * 3 * t))))
    def rhs(t, y):
        tt = y[0]; uu = ufc(t)
        return [af(tt) + bf(tt) * uu, -tt + tt * uu, l0f(tt)]
    s = solve_ivp(rhs, [0, 1], [0.0, 0.0, 0.0], rtol=1e-12, atol=1e-14, max_step=0.002, dense_output=True)
    thT, C, Cn = s.y[:, -1]
    Cg = Cn - Ff(thT) + Ff(0.0)
    maxth = max(maxth, s.y[0].max()); minth = min(minth, s.y[0].min())
    print("catmix random control %d: C = %.12f, gauged cost = %.12f, diff %.1e" % (trial, C, Cg, C - Cg))
# extreme controls for the reachable set
for ucon in (0.0, 1.0):
    s = solve_ivp(lambda t, y: [af(y[0]) + bf(y[0]) * ucon], [0, 50], [0.0], rtol=1e-12, atol=1e-14)
    print("catmix u=%.0f for 50 time units: theta(end) = %.12f" % (ucon, s.y[0, -1]))
    maxth = max(maxth, s.y[0].max())
print("catmix: max theta over runs = %.12f, 1/11 = %.12f; min theta = %.2e" % (maxth, 1 / 11, minth))
