"""Independent checks for the third revision of theory-bangbang/report.md (Remark 3.3 scalar example).

Run from reviews/bangbang-root-fixes-confirm-r2-checks/:
    OMP_NUM_THREADS=1 timeout 300 python3 r2_checks.py > logs/r2_checks.log

Does not reuse revision3_checks.py. Methods differ on purpose:
- exact data from hand-derived closed forms in Fractions (no sympy integration);
  F'(tau), F''(tau) from exact finite differences of the cubic F(theta);
- global-form blow-up with mpmath's Taylor-series ODE solver (odefun, 30 digits) on the
  linearization, plus a direct float integration of P itself (LSODA) to an event P = -1e8;
- local formulation with LSODA in the variable log s.
Problem: x' = u, |u| <= 1 (Delta = 2), cost int x^2/2 dt - phi x(T)^2/2 + k x(T), x(0) = xt + tau,
u = -1 on [0, tau), u = +1 on (tau, T]. Then b = 1, l_1 = 0, w = 0, H_xx = 1, g_x = 0.
"""
from fractions import Fraction as Fr

import mpmath as mp
import numpy as np
from scipy.integrate import solve_ivp


def exact(xt, tau, T, phi):
    xt, tau, T, phi = (Fr(str(v)) for v in (xt, tau, T, phi))
    x0 = xt + tau
    L = T - tau
    xT = xt + L
    int_x_last = xt * L + L * L / 2          # int_tau^T x dt
    k = phi * xT - int_x_last                # makes psi(tau) = 0, psi(T) = -phi x(T) + k
    psiT = -phi * xT + k
    # sigma = psi; psi' = -x.  sigma(tau - s) = xt s + s^2/2, sigma(tau + s) = -(xt s + s^2/2)
    sigdot = -xt
    D = abs(sigdot) * 2
    etaL = -phi + L                          # Q' = -1, Q(T) = -phi

    def F(th):                               # cost with the switch at theta (cubic in theta)
        # first arc: x = x0 - t on [0, th]; int (x0 - t)^2/2 = (x0^3 - (x0 - th)^3)/6
        a = (x0 ** 3 - (x0 - th) ** 3) / 6
        # second arc: x = x0 - 2 th + t on [th, T]; int = ((x0 - 2th + T)^3 - (x0 - th)^3)/6
        xe = x0 - 2 * th + T
        bb = (xe ** 3 - (x0 - th) ** 3) / 6
        return a + bb - phi * xe ** 2 / 2 + k * xe

    h = Fr(1, 8)
    d1 = lambda hh: (F(tau + hh) - F(tau - hh)) / (2 * hh)
    F1 = (4 * d1(h / 2) - d1(h)) / 3          # exact for a cubic
    F2 = (F(tau + h) - 2 * F(tau) + F(tau - h)) / h ** 2   # exact for a cubic
    return dict(x0=x0, k=k, psiT=psiT, sigdot=sigdot, D=D, etaL=etaL, F1=F1, F2=F2,
                formula=D + 4 * etaL)


def blowup_mp(xt, tau, T, phi, eps):
    """Linearization phi'' = a phi/|sigma|, P = -a phi/phi'; blow-up where phi' = 0.
    Reversed time r = T - t so that odefun integrates forward."""
    mp.mp.dps = 30
    xt, tau, T, phi, eps = (mp.mpf(str(v)) for v in (xt, tau, T, phi, eps))
    a = 1 - 2 * eps
    PT = -phi - 2 * eps
    absig = lambda t: xt * (t - tau) + (t - tau) ** 2 / 2
    # z = (phi, dphi/dt) as functions of r; d/dr = -d/dt
    f = mp.odefun(lambda r, z: [-z[1], -a * z[0] / absig(T - r)], 0, [mp.mpf(1), -a / PT])
    dphi = lambda r: f(r)[1]
    # bracket the sign change of phi' on a grid, then refine
    grid = [mp.mpf(i) / 200 for i in range(1, 200 * int((T - tau) * 1) )]
    prev = dphi(grid[0])
    for r in grid[1:]:
        cur = dphi(r)
        if mp.sign(cur) != mp.sign(prev):
            rb = mp.findroot(dphi, (r - mp.mpf(1) / 200, r), solver="anderson")
            return float(T - rb)
        prev = cur
    return None


def blowup_direct(xt, tau, T, phi, eps):
    a = 1.0 - 2 * eps
    absig = lambda t: xt * (t - tau) + (t - tau) ** 2 / 2
    ev = lambda t, P: P[0] + 1e8
    ev.terminal = True
    sol = solve_ivp(lambda t, P: [-a + P[0] ** 2 / absig(t)], [T, tau + 1e-9], [-phi - 2 * eps],
                    events=ev, method="LSODA", rtol=1e-12, atol=1e-12)
    return float(sol.t_events[0][0]) if sol.t_events[0].size else None


def local_layer(xt, tau, T, phi, d0):
    """eps = 0: P = Q on [tau + d0, T]; singular equation on (tau, tau + d0], variable l = log s."""
    absig = lambda s: xt * s + s * s / 2
    P0 = -phi + (T - tau - d0)
    ev = lambda l, P: P[0] + 1e8
    ev.terminal = True
    sol = solve_ivp(lambda l, P: [np.exp(l) * (-1.0 + P[0] ** 2 / absig(np.exp(l)))],
                    [np.log(d0), np.log(1e-12)], [P0], events=ev, method="LSODA",
                    rtol=1e-10, atol=1e-13)
    if sol.t_events[0].size:
        return "blow-up at s = %.3e" % np.exp(sol.t_events[0][0])
    return "bounded, P(tau + 1e-12) = %.5f, min P on layer = %.5f" % (sol.y[0, -1], sol.y[0].min())


for label, pars in [("scalar example, eta_L > 0", (0.01, 1, 2, 0.9)),
                    ("second set, eta_L < 0", (0.5, 1, 2, 1.1))]:
    xt, tau, T, phi = pars
    d = exact(*pars)
    print("==", label, "xt, tau, T, phi =", pars)
    print("  x0 = %s, k = %s, psi(T) = %s" % (d["x0"], d["k"], d["psiT"]))
    print("  sigma_dot(tau) = %s, D = %s, eta_L = %s" % (d["sigdot"], d["D"], d["etaL"]))
    print("  F'(tau) = %s, F''(tau) = %s, D + 4 eta_L = %s" % (d["F1"], d["F2"], d["formula"]))
    for eps in (0.0, 0.01):
        tm = blowup_mp(xt, tau, T, phi, eps)
        td = blowup_direct(float(xt), float(tau), float(T), float(phi), eps)
        print("  global form, eps = %.2f: mpmath linearization t_b = %s; direct LSODA (P = -1e8) t_b = %s"
              % (eps, "%.7f" % tm if tm else None, "%.7f" % td if td else None))
    for d0 in (0.05, 0.2):
        print("  local formulation, delta_0 = %.2f: %s" % (d0, local_layer(float(xt), float(tau),
                                                                           float(T), float(phi), d0)))
