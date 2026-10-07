"""Independent singular-Riccati checks (continuous time) for extension-n2.md, examples A, B, B2, C.

Own implementation: switching functions are exact sympy polynomials (from v_exact_cont), the ODEs are
integrated in plain time t with Radau (the author integrates in log(t - tau)).

1. Global model after the switch: P' = -(A^T P + P A + Hxx) + 2 eps I + (Delta / (2|sigma|)) beta beta^T,
   beta = P b - w, backward from P(T) = Phi_xx - 2 eps I.  Report the blow-up distance s_b = t_b - tau
   (report: B: 5.87e-3 (eps 0), 1.33e-2 (eps .02)); local model with the singular term only on
   (tau, tau + delta0] (report: 4.08e-3 / 2.46e-3 for delta0 = .2 / .1).
2. Global model before the switch, started from the LARGEST admissible tangential value
   Pmax(tau) = Q_eps(tau+) - beta_eps beta_eps^T / eta_eps (Proposition 4).  By Riccati comparison
   every global-model calibration has P <= this solution on [0, tau), so a blow-up here rules out every
   global-model TSQC (report: example C blows up at t ~ .46 from its own, smaller, P(tau)).
"""
import json
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

import v_exact_cont as V

A = np.array([[0.0, 1.0], [0.0, 0.0]])
b = np.array([0.0, 1.0])
Delta = 2.0
T = 2.0


def extremal(name):
    d = V.EX[name]
    r = V.run(name, d)
    # rebuild sigma polynomials (float) from the exact module by re-running the symbolic adjoint
    return r


def sigma_funcs(name):
    """Exact switching-function polynomials of the extremal (re-derived here in sympy)."""
    d = V.EX[name]
    R = sp.Rational
    t = V.t
    rho, k1, k2, q, c, x20, e = (R(d[k]) for k in ("rho", "k1", "k2", "q", "c", "x20", "e"))
    r = V.run(name, d)
    tau = sp.Float(repr(r["tau"]), 30)
    s = sp.symbols("s")
    x2a = x20 + t
    x1a = x20 * t + t ** 2 / 2
    x1s, x2s = x1a.subs(t, tau), x2a.subs(t, tau)
    x2b = x2s - (t - tau)
    x1b = x1s + x2s * (t - tau) - (t - tau) ** 2 / 2
    psi1b = -1 + sp.integrate((q * x1b - k1).subs(t, s), (s, t, 2))
    psi2b = rho * x2b.subs(t, 2) + sp.integrate((e - c * x2b - k2 + psi1b).subs(t, s), (s, t, 2))
    psi1a = psi1b.subs(t, tau) + sp.integrate((q * x1a + k1).subs(t, s), (s, t, tau))
    psi2a = psi2b.subs(t, tau) + sp.integrate((e - c * x2a + k2 + psi1a).subs(t, s), (s, t, tau))
    siga = sp.lambdify(t, sp.expand(k1 * x1a + k2 * x2a + psi2a), "numpy")
    sigb = sp.lambdify(t, sp.expand(k1 * x1b + k2 * x2b + psi2b), "numpy")
    par = dict(rho=float(rho), k1=float(k1), k2=float(k2), q=float(q), c=float(c))
    return float(tau), siga, sigb, par, r


def rhs_factory(par, sig, eps, sing_window=None, tau=None):
    Hxx = np.diag([par["q"], -par["c"]])
    w = -np.array([par["k1"], par["k2"]])

    def f(t, y):
        P = y.reshape(2, 2)
        beta = P @ b - w
        lin = -(A.T @ P + P @ A + Hxx) + 2 * eps * np.eye(2)
        if sing_window is not None and abs(t - tau) > sing_window:
            return lin.ravel()
        return (lin + Delta / (2 * abs(sig(t))) * np.outer(beta, beta)).ravel()
    return f, w


def blowup_event(t, y):
    return 1e7 - np.abs(y).max()


blowup_event.terminal = True


def after_switch(name, eps, delta0=None, smin=1e-10):
    tau, siga, sigb, par, r = sigma_funcs(name)
    f, w = rhs_factory(par, sigb, eps, delta0, tau)
    PT = np.diag([0.0, par["rho"]]) - 2 * eps * np.eye(2)
    sol = solve_ivp(f, (T, tau + smin), PT.ravel(), method="Radau", rtol=1e-10, atol=1e-12, events=blowup_event)
    if sol.status == 1:
        return dict(blowup=True, s_b=float(sol.t[-1] - tau))
    P = sol.y[:, -1].reshape(2, 2)
    beta = P @ b - w
    return dict(blowup=False, beta_end=float(np.linalg.norm(beta)), eta_end=float(b @ beta))


def Qeps_at_tau(name, eps):
    tau, siga, sigb, par, r = sigma_funcs(name)
    f, w = rhs_factory(par, sigb, eps, sing_window=-1.0, tau=tau)  # no singular term
    PT = np.diag([0.0, par["rho"]]) - 2 * eps * np.eye(2)
    sol = solve_ivp(f, (T, tau), PT.ravel(), method="Radau", rtol=1e-12, atol=1e-14)
    Q = sol.y[:, -1].reshape(2, 2)
    beta = Q @ b - w
    eta = b @ beta
    return tau, Q, beta, eta, siga, par, w


def before_switch_from_Pmax(name, eps, s0=1e-9):
    tau, Q, beta, eta, siga, par, w = Qeps_at_tau(name, eps)
    Pmax = Q - np.outer(beta, beta) / eta
    f, _ = rhs_factory(par, siga, eps)
    sol = solve_ivp(f, (tau - s0, 0.0), Pmax.ravel(), method="Radau", rtol=1e-10, atol=1e-12, events=blowup_event)
    return dict(eta_eps=float(eta), Pmax=Pmax.tolist(), beta_check=(Pmax @ b - w).tolist(),
                blowup=bool(sol.status == 1), t_blow=float(sol.t[-1]) if sol.status == 1 else None,
                P0=None if sol.status == 1 else sol.y[:, -1].reshape(2, 2).tolist())


if __name__ == "__main__":
    out = {}
    for name in ("B", "B2", "A", "C"):
        rec = {}
        for eps in (0.0, 0.02):
            rec["after_global_eps%s" % eps] = after_switch(name, eps)
            if name == "B":
                for d0 in (0.2, 0.1):
                    rec["after_local_d%s_eps%s" % (d0, eps)] = after_switch(name, eps, d0)
            if name in ("A", "C"):  # Pmax(tau) is defined only when eta_eps > 0
                rec["before_from_Pmax_eps%s" % eps] = before_switch_from_Pmax(name, eps)
        out[name] = rec
        print(name, json.dumps(rec), flush=True)
    json.dump(out, open("logs/v_riccati.json", "w"), indent=1)
