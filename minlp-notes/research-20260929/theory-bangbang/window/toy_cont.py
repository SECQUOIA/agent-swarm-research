"""Continuous quantities for the scalar toy (toy.py): one-switch extremal (+1 then -1), switching
function, and the switch data kappa_tau = -k, gamma = sigma'(tau), eta_L, D, F''(tau).
Float (scipy quad on piecewise-polynomial integrands, breakpoints passed explicitly)."""
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq


def xs(toy, t, tau):
    return toy.x0 + t if t <= tau else toy.x0 + 2 * tau - t


def sigma(toy, t, tau):
    a = lambda s: toy.a1 if s < toy.tj else toy.a2
    xT = xs(toy, toy.T, tau)
    psiT = toy.phi1 + toy.phi2 * xT
    f = lambda s: (xs(toy, s, tau) - a(s)) + toy.k * (1.0 if s <= tau else -1.0)
    pts = [p for p in (tau, toy.tj) if t < p < toy.T]
    I = quad(f, t, toy.T, points=pts or None, limit=200, epsabs=1e-14, epsrel=1e-14)[0]
    return toy.k * xs(toy, t, tau) + psiT + I


def switch(toy):
    g = lambda tau: sigma(toy, tau, tau)
    grid = np.linspace(0.01, toy.T - 0.01, 199)
    vals = [g(t) for t in grid]
    roots = [brentq(g, grid[i], grid[i + 1], xtol=1e-15, rtol=1e-15)
             for i in range(len(grid) - 1) if vals[i] * vals[i + 1] < 0]
    out = []
    for tau in roots:
        tt = np.linspace(0, toy.T, 4001)
        s = np.array([sigma(toy, t, tau) for t in tt])
        pmp = float(max(np.max(np.maximum(0, s[tt < tau])), np.max(np.maximum(0, -s[tt > tau]))))
        a_tau = toy.a1 if tau < toy.tj else toy.a2
        gamma = a_tau - xs(toy, tau, tau)              # sigma' = a - x for this toy (u-independent)
        Q = toy.T - tau + toy.phi2                     # last-arc Lyapunov: Q' = -1, Q(T) = phi2
        eta_L = Q + toy.k                              # beta_L = Q b - w, w = -k, b = 1
        D = abs(gamma) * 2.0
        out.append(dict(tau=tau, pmp_viol=pmp, gamma=gamma, kappa_tau=-toy.k, Q_tau=Q, eta_L=eta_L, D=D,
                        Fpp=D + 4 * eta_L, frac_curv=Q,   # b^T Q b = kappa_tau + eta_L: d^2 J / du_s^2 / h^2 in the limit
                        min_sig_ratio=float(np.min(np.abs(s[np.abs(tt - tau) > 1e-3]) /
                                                   np.abs(tt - tau)[np.abs(tt - tau) > 1e-3]))))
    return out


def family_margins(toy, tau, Pfun, dPfun, eps, npts=4001):
    """Global-form inequality of report.md Prop. 3.2 / extension-n2 (A),(G) for a quadratic family in
    this scalar LQ toy (H_xx = 1, g_x = 0, Delta = 2):  min over t != tau of
        M(t) - 2 eps - beta(t)^2 / |sigma(t)|,   M = P' + 1,  beta = P - w = P + k,
    together with min M - 2 eps (condition (A)) and the terminal condition P(T) <= phi2 - 2 eps."""
    tt = np.concatenate([np.linspace(0, tau, npts)[:-1], tau + np.geomspace(1e-9, toy.T - tau, npts)])
    tt = tt[np.abs(tt - tau) > 0]
    G, A = np.inf, np.inf
    for t in tt:
        M = dPfun(t) + 1.0
        beta = Pfun(t) + toy.k
        s = abs(sigma(toy, t, tau))
        A = min(A, M - 2 * eps)
        G = min(G, M - 2 * eps - beta * beta / s)
    term = toy.phi2 - 2 * eps - Pfun(toy.T)
    return dict(min_G=float(G), min_A=float(A), terminal_margin=float(term))
