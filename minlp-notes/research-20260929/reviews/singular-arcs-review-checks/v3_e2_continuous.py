"""Reviewer's check of the E2 continuous extremal (Section 4.1-4.2).
Closed-form bang arc and singular arc; sigma(t) on the bang arc from the
costate integrated backward from the junction (k1 = 0 gauge: sigma is gauge
invariant).  J* for k1 = 0, -1/2, +1/2; roots of sigma = |k|^2."""
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
k2 = 0.25; K = 1 - 2*k2
t1 = brentq(lambda t: 3 - 2*t - 2*np.exp(-t), 0.5, 2.0, xtol=1e-15)
T = 3.0
x1_t1 = 1 - t1
print('t1 = %.10f  u_s(t1) = %.6f' % (t1, -2*x1_t1))
# singular arc x1 = x1_t1 e^{-2(t-t1)}, x2 = -x1; costate (k1=0): psi1 = k2 x1, psi2 = -K x1
def J(k1):
    # bang arc u=-1: x1 = 1-t, x2 = 2 - t - 2e^{-t}
    f = lambda t: 0.5*((1-t)**2 + (2 - t - 2*np.exp(-t))**2) + (k1*(1-t) + k2*(2 - t - 2*np.exp(-t)))*(-1)
    Jb = quad(f, 0, t1, epsabs=1e-14, epsrel=1e-14)[0]
    x1 = lambda t: x1_t1*np.exp(-2*(t - t1))
    fs = lambda t: 0.5*(2*x1(t)**2) + (k1*x1(t) - k2*x1(t))*(-2*x1(t))
    Js = quad(fs, t1, T, epsabs=1e-14, epsrel=1e-14)[0]
    xT = np.array([x1(T), -x1(T)])
    F = np.diag([k2 - k1, K])
    return Jb + Js + 0.5*xT@F@xT
for k1 in (0.0, -0.5, 0.5):
    print('k1 = %+.1f  J* = %.10f' % (k1, J(k1)))
# sigma on the bang arc (k1 = 0): sigma = k2 x2 + psi1; costate backward from t1
def rhs(t, y):
    x1, x2, p1, p2 = y
    uu = -1.0
    return [uu, x1 - x2, -(x1 + p2), -(x2 + k2*uu - p2)]
y1 = [x1_t1, -x1_t1, k2*x1_t1, -K*x1_t1]
s = solve_ivp(rhs, [t1, 0], y1, rtol=1e-13, atol=1e-15, dense_output=True)
print('x(0) back:', s.sol(0)[:2])
sig = lambda t: k2*s.sol(t)[1] + s.sol(t)[2]
ts = np.linspace(1e-9, t1 - 1e-6, 4000)
print('min sigma on (0,t1): %.3e' % min(sig(t) for t in ts))
for ss in (1e-2, 1e-3):
    print('sigma(t1-s)/s^2 at s=%g: %.5f (pred %.5f)' % (ss, sig(t1 - ss)/ss**2, 0.5*K*abs(-1 - (-2*x1_t1))))
for k1 in (-0.5, 0.0):
    thr = k1**2 + k2**2
    tt = brentq(lambda t: sig(t) - thr, 1e-6, t1 - 1e-6)
    print('k1=%+.1f: sigma(t) = |k|^2 = %.4f at t = %.4f' % (k1, thr, tt))
# quantity used for the chattering prediction in 4.3: (1/4) int_0^T (1 - u*^2) and (1/4) int u*^2
us = lambda t: -2*x1_t1*np.exp(-2*(t - t1))
I1 = quad(lambda t: 1 - us(t)**2, t1, T)[0]
I2 = t1 + quad(lambda t: us(t)**2, t1, T)[0]
print('(1/4) int (1-u*^2) = %.4f ; (1/4) int u*^2 = %.4f' % (I1/4, I2/4))
