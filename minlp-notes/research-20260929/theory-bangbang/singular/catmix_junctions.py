"""Continuous catmix (reduced 1-D form): switching times, optimal value, the
bang-side behaviour of sigma at both junctions, and the layer number
eta_L = b (Q(t2+) b - w) of extension-n2.md at the singular-to-bang junction
(Q: Lyapunov solution of the last arc, Q(1) = Phi'' = 0).  Float (scipy,
tight tolerances)."""
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

s10 = np.sqrt(10.0)
ths = (11 - s10) / 111
a = lambda t: t * t - t
b = lambda t: 1 - 10 * t - t * t
us = -a(ths) / b(ths)
psis = -ths / b(ths)
ws = -(1 + (-10 - 2 * ths) * psis)
Ps = ws / b(ths)
K = 2 * s10

# first arc u = 1: thetadot = 1 - 11 theta, theta(0) = 0
t1 = -np.log(1 - 11 * ths) / 11


# last arc u = 0: thetadot = -theta(1-theta); costate psidot = -H_theta = 1 - psi(2 theta - 1), psi(1) = 0
def last_arc(t2):
    # theta(t) with theta(t2) = ths: logistic decay
    def th_of(t):
        c = ths / (1 - ths)
        e = c * np.exp(-(t - t2))
        return e / (1 + e)
    sol = solve_ivp(lambda t, y: [1 - y[0] * (2 * th_of(t) - 1)], [1.0, t2], [0.0], rtol=1e-13, atol=1e-15,
                    dense_output=True)
    return th_of, sol


def mismatch(t2):
    th_of, sol = last_arc(t2)
    return sol.y[0, -1] - psis


t2 = brentq(mismatch, 0.5, 0.95, xtol=1e-15)
th_of, psol = last_arc(t2)
C = -((1 - us) * ths * (t2 - t1) + quad(lambda t: th_of(t), t2, 1, epsabs=1e-15, epsrel=1e-14)[0])
Jstar = np.exp(C) - 1
print("theta_s = %.15f  u_s = %.15f  psi_s = %.15f  w_s = %.12f  P_s = %.12f  K = %.12f" % (ths, us, psis, ws, Ps, K))
print("t1 = %.12f  t2 = %.12f  C* = %.15f  J* = %.15f" % (t1, t2, C, Jstar))

# sigma on the last arc near t2 (should be > 0, ~ c s^2) and on the first arc near t1 (< 0)
tt = t2 + np.array([1e-3, 1e-2, 5e-2, 0.1, 0.2])
sig_last = [th_of(t) + b(th_of(t)) * psol.sol(t)[0] for t in tt]
pred_last = 0.5 * K * abs(0 - us) / 1.0  # sigma ~ (1/2) K |u_b - u_s| s^2 / b^2 ? printed as ratio below
print("last arc sigma(t2+s)/s^2:", [float(sv / (t - t2) ** 2) for sv, t in zip(sig_last, tt)])


# first arc: costate backward from psi(t1) = psi_s with u = 1
def rhs1(t, y):
    th, ps = y
    # H = -theta + theta u + psi (a + b u), u = 1; psidot = -H_theta
    return [a(th) + b(th), -(-1 + 1 + ps * ((2 * th - 1) + (-10 - 2 * th)))]


s1 = solve_ivp(rhs1, [t1, 0.0], [ths, psis], rtol=1e-13, atol=1e-15, dense_output=True)
tt1 = t1 - np.array([1e-3, 1e-2, 5e-2, 0.1])
sig_first = [s1.sol(t)[0] + b(s1.sol(t)[0]) * s1.sol(t)[1] for t in tt1]
print("first arc sigma(t1-s)/s^2:", [float(sv / (t1 - t) ** 2) for sv, t in zip(sig_first, tt1)],
      " theta(0) back =", float(s1.sol(0.0)[0]))
print("  sign check: min sigma on (0, t1) should be < 0 throughout:",
      float(max(s1.sol(t)[0] + b(s1.sol(t)[0]) * s1.sol(t)[1] for t in np.linspace(1e-6, t1 - 1e-6, 2000))))
print("  last arc: min sigma on (t2, 1] should be > 0:",
      float(min(th_of(t) + b(th_of(t)) * psol.sol(t)[0] for t in np.linspace(t2 + 1e-6, 1, 2000))))
# predicted quadratic coefficient: sigma_ddot on bang side = -dsigma_ddot/du (u_b - u_s) ... = K (u_b - u_s) * (-1)
# sign: d^2 sigma/dt^2 = -K (u_b - u_s)  => sigma ~ -K (u_b - u_s) s^2 / 2
print("  predicted sigma/s^2: last arc (u_b=0): %.6f ; first arc (u_b=1): %.6f" % (-K * (0 - us) / 2, -K * (1 - us) / 2))


# Lyapunov Q on the last arc: Qdot = -2 g_theta(u=0) Q - H_thth(u=0),  g_theta = 2 theta - 1, H_thth = 2 psi
def rhsQ(t, y):
    return [-2 * (2 * th_of(t) - 1) * y[0] - 2 * psol.sol(t)[0]]


sQ = solve_ivp(rhsQ, [1.0, t2], [0.0], rtol=1e-13, atol=1e-15)
Q2 = sQ.y[0, -1]
etaL = b(ths) * (Q2 * b(ths) - ws)
print("Q(t2+) = %.10f   P_s = %.10f   eta_L = b(Q b - w) = %.10f" % (Q2, Ps, etaL))
