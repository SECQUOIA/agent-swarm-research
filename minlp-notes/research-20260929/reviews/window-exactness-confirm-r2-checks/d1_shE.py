"""Confirmation round 2, item 2: isotropic (H3)/(W5) margin of (SH) for [E]'s own continuous
tangential families (cmax, clin, clin.02; eps = 0.02) on [E]'s examples A and A0.

Tested object (read-only import): continuous_family of theory-bangbang/n2/model.py.
Own code: states, costates and sigma as exact piecewise polynomials (sympy), own tau by brentq,
P' by a five-point stencil kept inside each smooth piece, M = P' + A^T P + P A + H_xx, beta = P b - w.
Reports inf lambda_min(M), the ratio Delta |beta|^2 / (2 |sigma|) near T and its sup before
tau - 0.1, the ratio at tau + s (s = 1e-2 ... 1e-8), and the anisotropic residual
lambda_min(M - 2 eps I - (Delta / (2|sigma|)) beta beta^T).
"""
import json
import os
import sys
import warnings

import numpy as np
import sympy as sp
from scipy.optimize import brentq

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "theory-bangbang", "n2"))
from model import Par, continuous_family, find_switch  # noqa: E402

EX = {"A": Par(T=2.0, a=1.0, rho=2.0, k1=-0.3, k2=-0.3, q=0.3, c=1.0, x20=0.5),
      "A0": Par(T=2.0, a=1.0, rho=1.0, k1=-0.3, k2=-0.3, q=0.3, c=0.2, x20=0.5)}
FAM = {"cmax": None, "clin": 0.1, "clin.02": 0.02}
EPS = 0.02
Am = np.array([[0.0, 1.0], [0.0, 0.0]])
b = np.array([0.0, 1.0])
t = sp.symbols("t")


def sigma_pieces(p, tau):
    """Exact polynomial sigma on [0, tau) and (tau, T] for the one-switch control +1 -> -1."""
    ua, ub = p.ua, p.ub
    x2a = p.x20 + ua * t
    x1a = p.x10 + sp.integrate(x2a, (t, 0, t))
    x2s, x1s = x2a.subs(t, tau), x1a.subs(t, tau)
    x2b = x2s + ub * (t - tau)
    x1b = x1s + sp.integrate(x2b, (t, tau, t))
    xT1, xT2 = x1b.subs(t, p.T), x2b.subs(t, p.T)
    psi1T, psi2T = -p.a, p.rho * xT2
    # psi1' = -(q x1 + k1 u), psi2' = -(e - c x2 + k2 u + psi1)
    psi1b = psi1T + sp.integrate(p.q * x1b + p.k1 * ub, (t, t, p.T))
    psi2b = psi2T + sp.integrate(p.e - p.c * x2b + p.k2 * ub + psi1b, (t, t, p.T))
    psi1s, psi2s = psi1b.subs(t, tau), psi2b.subs(t, tau)
    psi1a = psi1s + sp.integrate(p.q * x1a + p.k1 * ua, (t, t, tau))
    psi2a = psi2s + sp.integrate(p.e - p.c * x2a + p.k2 * ua + psi1a, (t, t, tau))
    sa = sp.expand(p.k1 * x1a + p.k2 * x2a + psi2a)
    sb = sp.expand(p.k1 * x1b + p.k2 * x2b + psi2b)
    return sp.lambdify(t, sa, "numpy"), sp.lambdify(t, sb, "numpy")


def own_tau(p):
    f = lambda th: float(sigma_pieces(p, th)[0](th))
    return brentq(f, 0.5, 1.9, xtol=1e-14)


def measures(p, delta1, tau_own):
    Pf, dg = continuous_family(p, EPS, delta1=delta1)
    th = find_switch(p)[0]
    sa, sb = sigma_pieces(p, th)
    sig = lambda s: abs(float(sa(s))) if s < th else abs(float(sb(s)))
    lay = th + (delta1 if delta1 is not None else 0.05)
    segs = [(0.0, th), (th, lay), (lay, p.T)]

    def terms(s, lo, hi):
        hs = min(1e-6, 0.05 * (s - lo), 0.05 * (hi - s))
        P = Pf(s)
        dP = (-Pf(s + 2 * hs) + 8 * Pf(s + hs) - 8 * Pf(s - hs) + Pf(s - 2 * hs)) / (12 * hs)
        M = dP + Am.T @ P + P @ Am + p.Hxx
        M = (M + M.T) / 2
        beta = P @ b - p.w
        sg = sig(s)
        ratio = 2.0 * beta @ beta / (2 * sg)
        an = np.linalg.eigvalsh(M - 2 * EPS * np.eye(2) - (2.0 / (2 * sg)) * np.outer(beta, beta))[0]
        return np.linalg.eigvalsh(M)[0], ratio, an, float(np.linalg.norm(beta))

    g = 1e-4
    rows = []
    for s in np.linspace(g, th - g, 2500):
        rows.append((s, "pre") + terms(s, *segs[0]))
    for s in th + np.geomspace(1e-8, lay - th - g, 2500):
        rows.append((s, "layer") + terms(s, *segs[1]))
    for s in np.linspace(lay + g, p.T - g, 2500):
        rows.append((s, "last") + terms(s, *segs[2]))
    lmin = min(r[2] for r in rows)
    pre = max(r[3] for r in rows if r[0] <= th - 0.1)
    atT = terms(p.T - g, *segs[2])[1]
    near = {f"{s:.0e}": terms(th + s, *segs[1])[1] for s in (1e-2, 1e-4, 1e-6, 1e-8)}
    out_layer = [abs(r[4]) for r in rows if (delta1 is None or r[1] != "layer")]
    return dict(tau_E=th, tau_own=tau_own, inf_lambda_min_M=lmin, ratio_near_T=atT,
                sup_ratio_pre_tau_minus_0p1=pre, ratio_at_tau_plus_s=near,
                sup_ratio_all=max(r[3] for r in rows), aniso_absmax_outside_layer=max(out_layer),
                isotropic_margin_holds=bool(max(r[3] for r in rows) < lmin))


def analytic_T(p, tau):
    """P(T) = Phi_xx - 2 eps I for all three families; ratio at T in closed form."""
    PT = np.diag([0.0, p.rho]) - 2 * EPS * np.eye(2)
    beta = PT @ b - p.w
    sT = abs(float(sigma_pieces(p, tau)[1](p.T)))
    return dict(beta_T=beta.tolist(), sigma_T=sT, ratio_T=float(beta @ beta / sT))


if __name__ == "__main__":
    out = {}
    for name, p in EX.items():
        tau = own_tau(p)
        out[name] = dict(analytic_T=analytic_T(p, tau))
        print(name, "own tau", tau, "analytic at T", out[name]["analytic_T"], flush=True)
        for fam, d1 in FAM.items():
            r = measures(p, d1, tau)
            out[name][fam] = r
            print(name, fam, json.dumps(r), flush=True)
    with open(os.path.join(HERE, "logs", "d1_shE.json"), "w") as f:
        json.dump(out, f, indent=1, default=float)
