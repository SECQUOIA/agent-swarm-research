"""Reviewer's independent check of catmix singular data (Section 5.1-5.3).

(1) Reduced 1-D problem: singular point, u_s, psi_s, w, P_s = w/b, K, b*w, c1,
    a_j at both junctions, thresholds.
(2) Cross-check K in the ORIGINAL 2-D Mayer formulation: along the optimal
    path the 2-D switching function is (J*+1) times the reduced one, so the
    2-D Kelley quantity -d_u sigma2_ddot should equal (J*+1) * K_red.
(3) Continuous optimum by direct simulation of the 2-D ODE with the
    bang-singular-bang control (u=1, u_s, 0) and switch times from
    first-order conditions; J*, t1, t2.
(4) eta_L: exact identity eta_L = 1 on catmix (last-arc value function is
    log(1 - theta(1-e^{-tau})), Q = -psi^2).
"""
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

th, u, p = sp.symbols('theta u p', real=True)
a = th**2 - th; b = 1 - 10*th - th**2; l0 = -th; l1 = th
H = l0 + l1*u + p*(a + b*u)
g = a + b*u
D = lambda F: sp.diff(F, th)*g - sp.diff(F, p)*sp.diff(H, th)
s0 = l1 + b*p
sd = sp.expand(D(s0)); sdd = sp.expand(D(sd))
assert sp.diff(sd, u) == 0
# singular point: s0 = 0, sd = 0
sol = sp.solve([s0, sd], [th, p], dict=True)
sols = [s for s in sol if s[th].is_real and 0 < float(s[th]) < 0.1]
S = sols[0]
ths, ps = sp.nsimplify(sp.radsimp(S[th])), sp.radsimp(S[p])
us = sp.radsimp(sp.solve(sdd.subs({th: ths, p: ps}), u)[0])
w = -sp.diff(s0, th)
ws = sp.radsimp(w.subs({th: ths, p: ps}))
bs = sp.radsimp(b.subs(th, ths))
Ps = sp.radsimp(ws/bs)
K = sp.radsimp(-sp.diff(sdd, u).subs({th: ths, p: ps}))
bx = sp.diff(b, th)
c1 = sp.radsimp((b**2*sp.diff(s0, th, 2) + 2*w*bx*b).subs({th: ths, p: ps}))
print('theta_s', ths, float(ths)); print('u_s', us, float(us)); print('psi_s', ps, float(ps))
print('w_s', ws, float(ws)); print('P_s', sp.nsimplify(Ps), float(Ps)); print('K', K, float(K))
print('b w', sp.radsimp(bs*ws), float(bs*ws)); print('c1', c1, float(c1))
# M(u*) on the stationary arc: Pdot = 0
Ms = (2*sp.diff(g, th)*Ps + sp.diff(H, th, 2)).subs({th: ths, p: ps, u: us})
print('b^2 M(u*) - K =', sp.simplify(sp.radsimp(bs**2*Ms - K)))
Kf, c1f, usf = float(K), float(c1), float(us)
print('vertex values K+(u-u_s)c1 at u=0,1: %.6f %.6f' % (Kf - usf*c1f, Kf + (1-usf)*c1f))
print('entry junction (u_b=1,u°=0): a_j = K - c1 = %.4f; threshold -K(1-u_s)/4 = %.4f' % (Kf - c1f, -Kf*(1-usf)/4))
print('exit junction (u_b=0,u°=1): a_j = K + c1 = %.4f; threshold -K u_s/4 = %.4f' % (Kf + c1f, -Kf*usf/4))

# (2) 2-D Mayer Kelley quantity
x1, x2, l1_, l2_ = sp.symbols('x1 x2 lam1 lam2', real=True)
f = sp.Matrix([u*(10*x2 - x1), u*(x1 - 10*x2) - (1 - u)*x2])
X = sp.Matrix([x1, x2]); L = sp.Matrix([l1_, l2_])
H2 = (L.T*f)[0]
def D2(F):
    return sum(sp.diff(F, X[i])*f[i] - sp.diff(F, L[i])*sp.diff(H2, X[i]) for i in range(2))
s2 = sp.diff(H2, u)
s2dd = sp.expand(D2(D2(s2)))
K2 = -sp.diff(s2dd, u)
# on the optimal path lambda = grad_x [ m exp(phi) ] with phi_theta = psi; choose m = 1 at the point:
# V2(x) = m * exp(C(theta)) -> lambda = exp(C) * (1 + (1-theta)... ) ; compute from V2 = m*exp(phi), phi' = psi
m_ = x1 + x2; thx = x2/m_
phi_lin = sp.Symbol('C0') + ps*(thx - ths)  # phi up to first order suffices for lambda at the point
V2 = m_*sp.exp(phi_lin)
lam = [sp.diff(V2, v) for v in (x1, x2)]
pt = {x1: 1 - ths, x2: ths}
C0 = sp.Symbol('C0')
lamv = [sp.simplify(li.subs(pt)) for li in lam]
K2v = sp.simplify(K2.subs({l1_: lamv[0], l2_: lamv[1]}).subs(pt).subs(u, us))
print('2-D Kelley / exp(C0) =', float(sp.simplify(K2v/sp.exp(C0))), ' (reduced K =', float(K), ')')
s2v = sp.simplify(s2.subs({l1_: lamv[0], l2_: lamv[1]}).subs(pt))
print('2-D sigma at the singular point / exp(C0) =', float(sp.simplify(s2v/sp.exp(C0))))

# (3) continuous optimum by 2-D simulation
thsf = float(ths); psf = float(ps)
t1 = -np.log(1 - 11*thsf)/11
def last_arc_psi_end(t2):
    # reduced costate backward on u=0 from psi(1)=0: psi' = -H_theta = 1 - psi(2theta-1)
    def rhs(t, y):
        thv, pv = y
        return [thv**2 - thv, 1 - pv*(2*thv - 1)]
    # integrate theta forward from t2 then costate backward: do shooting by solving theta analytically
    c = thsf/(1 - thsf)
    thf = lambda t: c*np.exp(-(t - t2))/(1 + c*np.exp(-(t - t2)))
    s = solve_ivp(lambda t, y: [1 - y[0]*(2*thf(t) - 1)], [1.0, t2], [0.0], rtol=1e-13, atol=1e-15)
    return s.y[0, -1] - psf
t2 = brentq(last_arc_psi_end, 0.3, 0.99, xtol=1e-15)
def uctl(t):
    return 1.0 if t < t1 else (usf if t < t2 else 0.0)
def f2(t, x):
    uu = uctl(t)
    return [uu*(10*x[1] - x[0]), uu*(x[0] - 10*x[1]) - (1 - uu)*x[1]]
x = np.array([1.0, 0.0])
for (ta, tb) in ((0, t1), (t1, t2), (t2, 1.0)):
    s = solve_ivp(f2, [ta, tb], x, rtol=1e-13, atol=1e-15, method='DOP853')
    x = s.y[:, -1]
    if tb == t1:
        print('theta(t1) - theta_s = %.3e' % (x[1]/(x[0]+x[1]) - thsf))
    if tb == t2:
        print('theta(t2) - theta_s = %.3e' % (x[1]/(x[0]+x[1]) - thsf))
print('t1 = %.12f t2 = %.12f J* (2-D sim) = %.15f' % (t1, t2, x[0] + x[1] - 1))
# (4) eta_L identity: Q(t2+) = -psi_s^2, eta_L = b(Qb - w)
etaL = sp.radsimp(bs*(-ps**2*bs - ws))
print('eta_L (exact) =', sp.simplify(etaL))
