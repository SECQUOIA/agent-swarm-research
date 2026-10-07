"""Confirmation check (item 5): isotropic (H3)/(W5) margin of (SH) for the Section 7.5 family.

Inputs (read-only): [E]'s continuous_family (the P(t) being tested) and find_switch (tau).
Own code: the continuous state/costate by solve_ivp, sigma = k1 x1 + k2 x2 + psi2, P' by a
five-point difference, M = P' + A^T P + P A + H_xx, beta = P b - w.
Reports inf lambda_min(M), sup Delta |beta|^2 / (2 |sigma|), and the anisotropic margin
lambda_min(M - 2 eps I - (Delta/(2|sigma|)) beta beta^T) on the last arc after the layer.
Also the scalar toy families (verifier linear rate, zero kink): M = P' + 1, beta = P + k.
"""
import json
import os
import sys

import numpy as np
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "theory-bangbang", "n2"))
from model import Par, continuous_family, find_switch  # noqa: E402

EX = {"A": Par(rho=2, k1=-.3, k2=-.3, q=.3, c=1, x20=.5),
      "Aminus": Par(rho=2, k1=-.3, k2=.3, q=.3, c=1, x20=.5),
      "Azero": Par(rho=2, k1=-.3, k2=0.0, q=.3, c=1, x20=.5)}
A = np.array([[0.0, 1.0], [0.0, 0.0]])
b = np.array([0.0, 1.0])


def sigma_fun(p, th):
    u = lambda t: p.ua if t < th else p.ub

    def rhs(t, y):
        x1, x2, s1, s2 = y
        uu = u(t)
        return [x2, uu, -(p.q * x1 + p.k1 * uu), -(p.e - p.c * x2 + p.k2 * uu + s1)]
    # forward states, then backward costates (two passes, piecewise)
    fx = solve_ivp(lambda t, y: rhs(t, list(y) + [0, 0])[:2], [0, p.T], [p.x10, p.x20], dense_output=True,
                   rtol=1e-12, atol=1e-13, max_step=1e-3)
    xT = fx.sol(p.T)
    psiT = [-p.a, p.rho * xT[1] + p.nu * xT[1] ** 3]

    def rhs_b(t, y):
        x1, x2 = fx.sol(t)
        uu = u(t)
        s1, s2 = y
        return [-(p.q * x1 + p.k1 * uu), -(p.e - p.c * x2 + p.k2 * uu + s1)]
    bx = solve_ivp(rhs_b, [p.T, 0], psiT, dense_output=True, rtol=1e-12, atol=1e-13, max_step=1e-3)
    return lambda t: p.k1 * fx.sol(t)[0] + p.k2 * fx.sol(t)[1] + bx.sol(t)[1]


def n2(name, eps, delta1=0.1, npts=3000, hs=1e-5):
    p = EX[name]
    th = find_switch(p)[0]
    Pf, _ = continuous_family(p, eps, delta1=delta1)
    sg = sigma_fun(p, th)
    Delta = 2.0
    g = 1e-4
    tt = np.concatenate([np.linspace(g, th - g, npts), np.linspace(th + g, p.T - g, 2 * npts)])
    lmin, ratio, an_last = [], [], []
    for t in tt:
        P = Pf(t)
        dP = (-Pf(t + 2 * hs) + 8 * Pf(t + hs) - 8 * Pf(t - hs) + Pf(t - 2 * hs)) / (12 * hs)
        M = dP + A.T @ P + P @ A + p.Hxx
        M = (M + M.T) / 2
        beta = P @ b - p.w
        s = abs(sg(t))
        lmin.append(np.linalg.eigvalsh(M)[0])
        ratio.append(Delta * beta @ beta / (2 * s))
        if t > th + delta1 + 1e-3:
            an_last.append(np.linalg.eigvalsh(M - 2 * eps * np.eye(2) - Delta / (2 * s) * np.outer(beta, beta))[0])
    i = int(np.argmax(ratio))
    return dict(example=name, eps=eps, tau=th, inf_lmin_M=float(min(lmin)), sup_ratio=float(max(ratio)),
                t_sup=float(tt[i]), sup_ratio_last_arc=float(max(r for t, r in zip(tt, ratio) if t > th)),
                sup_ratio_pre=float(max(r for t, r in zip(tt, ratio) if t < th)),
                aniso_last_absmax=float(np.max(np.abs(an_last))))


def toy(name):
    # scalar toys: sigma from the closed forms quoted by the review (continuous extremal)
    # verifier: k = -0.5, a = 2 | -2, Phi = 0;  zero: k = 0, a = 2 | -1, Phi = x + x^2/4
    from math import isclose
    if name == "verifier":
        k, a2, phi1, phi2, c = -0.5, -2.0, 0.0, 0.0, 0.3
        P0 = 0.5
    else:
        k, a2, phi1, phi2, c = 0.0, -1.0, 1.0, 0.5, 0.3
        P0 = 0.0
    T = 2.0
    # continuous extremal: u = +1 on [0, tau), -1 after; find tau with sigma(tau) = 0 by bisection
    def sig_of(tau):
        x = lambda t: t if t < tau else 2 * tau - t
        xT = x(T)
        a = lambda t: 2.0 if t < 1 else a2
        # psi' = -(x - a + k u), psi(T) = phi1 + phi2 xT; sigma = k x + psi
        ts = np.linspace(0, T, 200001)
        u = np.where(ts < tau, 1.0, -1.0)
        xs = np.where(ts < tau, ts, 2 * tau - ts)
        av = np.where(ts < 1, 2.0, a2)
        f = xs - av + k * u
        # psi(t) = psi(T) + int_t^T f
        cum = np.concatenate([[0], np.cumsum((f[1:] + f[:-1]) / 2 * np.diff(ts))])
        psi = phi1 + phi2 * xT + (cum[-1] - cum)
        return ts, k * xs + psi
    lo, hi = 0.05, 0.95
    for _ in range(60):
        mid = (lo + hi) / 2
        ts, s = sig_of(mid)
        v = np.interp(mid, ts, s)
        lo, hi = (mid, hi) if v < 0 else (lo, mid)
    tau = (lo + hi) / 2
    ts, s = sig_of(tau)
    Pf = lambda t: P0 if t <= tau else P0 - c * (t - tau)
    dP = np.where(ts <= tau, 0.0, -c)
    M = dP + 1.0
    beta = np.array([Pf(t) for t in ts]) + k
    msk = np.abs(ts - tau) > 1e-3
    ratio = 2.0 * beta[msk] ** 2 / (2 * np.abs(s[msk]))
    return dict(toy=name, tau=tau, inf_M=float(M.min()), sup_ratio=float(ratio.max()), t_sup=float(ts[msk][ratio.argmax()]))


if __name__ == "__main__":
    out = []
    for nm in ("verifier", "zero"):
        r = toy(nm)
        print(json.dumps(r), flush=True)
        out.append(r)
    for nm, eps in (("A", 0.02), ("Aminus", 0.02), ("Azero", 0.02), ("Azero", 0.1)):
        r = n2(nm, eps)
        print(json.dumps(r), flush=True)
        out.append(r)
    with open(os.path.join(HERE, "logs", "c2_sh.json"), "w") as f:
        json.dump(out, f, indent=1)
