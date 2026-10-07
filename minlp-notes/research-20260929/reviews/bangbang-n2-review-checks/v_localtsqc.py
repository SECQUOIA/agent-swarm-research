"""Numerical instance of Theorem 2 (local TSQC) for example C (eta_L = +0.20, global model fails), and example A.

Construction (N = 0 data, so G_m = G° and v = phi'(s) beta_1):
  P = Q_eps on [tau + d1, T];  layer (tau, tau + d1]: beta = phi(s) beta_1 with phi = s / d1 when
  lambda := min(1, 1/(4 kbar eta_1)) = 1 (as here), else the report's log/linear profile;
  P' = G°(P, t) + y y^T / (b.y), y = v - G° b;  before tau: P' = G°(P, t) on [tau - d0, tau), P' = G* before.
For quadratic S and LQ data the residual is exact:
  r(t, x* + d, u) = sigma omega + omega beta.d + 1/2 d^T M d,   M = P' + A^T P + P A + Hxx  (independent of u).
Checks: min b.y in the layer; max |P|; min eigenvalue of M - 2 eps I (condition (A)); min eigenvalue of
M - 2 eps I - (Delta/(2|sigma|)) beta beta^T on |t - tau| <= d0 (condition (G-local));
uniform tube radius r1 = min_t sup{rho : r(t, x*+d, u°) >= (eps/2)|d|^2 for |d| <= rho};
the [R, (H3)] margin min_t (|sigma| - Delta |beta|^2 / (2 mu)), mu = lambda_min(M);
far region: min over the continuous reachable box D_t and u in U of r(t, x, u).
"""
import itertools
import json
import sys

import numpy as np
from scipy.integrate import solve_ivp

import v_riccati as R

A = R.A
b = R.b
Delta = 2.0
T = 2.0


def build(name, eps, d1, d0=None):
    d0 = d1 if d0 is None else d0
    tau, siga, sigb, par, rec = R.sigma_funcs(name)
    w = -np.array([par["k1"], par["k2"]])
    Hxx = np.diag([par["q"], -par["c"]])
    I2 = np.eye(2)

    def Gstar(P):
        return -(A.T @ P + P @ A + Hxx) + 2 * eps * I2

    def Gdeg(P, t, sig):
        beta = P @ b - w
        return Gstar(P) + Delta / (2 * abs(sig(t))) * np.outer(beta, beta)

    kw = dict(method="DOP853", rtol=1e-11, atol=1e-13, dense_output=True)
    PT = np.diag([0.0, par["rho"]]) - 2 * eps * I2
    r1 = solve_ivp(lambda t, y: Gstar(y.reshape(2, 2)).ravel(), (T, tau + d1), PT.ravel(), **kw)
    P1 = r1.y[:, -1].reshape(2, 2)
    beta1 = P1 @ b - w
    eta1 = b @ beta1
    ss = np.linspace(1e-9, d1, 2001)
    kbar = max(Delta * s / (2 * abs(sigb(tau + s))) for s in ss)
    lam = min(1.0, 1.0 / (4 * kbar * eta1))
    if lam < 1:
        d2 = d1 * np.exp(-(1 / lam - 1) / (2 * kbar * eta1))
    else:
        d2 = d1

    def phi_d(s):
        if s <= d2:
            return lam / d2
        L = np.log(d1 / s)
        ph = 1 / (1 + 2 * kbar * eta1 * L)
        return 2 * kbar * eta1 * ph ** 2 / s

    by_min = [np.inf]

    def lay(t, y):
        P = y.reshape(2, 2)
        s = t - tau
        G = Gdeg(P, t, sigb)
        yv = phi_d(s) * beta1 - G @ b
        by = b @ yv
        by_min[0] = min(by_min[0], by)
        return (G + np.outer(yv, yv) / by).ravel()

    r2 = solve_ivp(lay, (tau + d1, tau + 1e-12), P1.ravel(), **kw)
    Ptau = r2.y[:, -1].reshape(2, 2)
    r3 = solve_ivp(lambda t, y: Gdeg(y.reshape(2, 2), t, siga).ravel(), (tau - 1e-12, tau - d0), Ptau.ravel(), **kw)
    r4 = solve_ivp(lambda t, y: Gstar(y.reshape(2, 2)).ravel(), (tau - d0, 0.0), r3.y[:, -1], **kw)

    def P_and_M(t):
        if t >= tau + d1:
            P = r1.sol(t).reshape(2, 2); Pd = Gstar(P)
        elif t > tau:
            P = r2.sol(t).reshape(2, 2); Pd = lay(t, P.ravel()).reshape(2, 2)
        elif t >= tau - d0:
            P = r3.sol(t).reshape(2, 2); Pd = Gdeg(P, t, siga)
        else:
            P = r4.sol(t).reshape(2, 2); Pd = Gstar(P)
        M = Pd + A.T @ P + P @ A + Hxx
        return P, M

    info = dict(tau=tau, eta1=float(eta1), beta1=beta1.tolist(), kbar=kbar, lam=lam, d2=d2,
                Ptau=Ptau.tolist(), beta_tau=(Ptau @ b - w).tolist(), status=[r1.status, r2.status, r3.status, r4.status])
    return P_and_M, siga, sigb, tau, w, info, by_min


def box_min_2d(c0, g, H, lo, hi):
    best = np.inf
    for pat in itertools.product(range(3), repeat=2):
        z = np.array([lo[i] if pat[i] == 0 else hi[i] for i in range(2)], float)
        free = [i for i in range(2) if pat[i] == 2]
        if free:
            fixed = [i for i in range(2) if pat[i] != 2]
            Af = H[np.ix_(free, free)]
            rhs = -(g[free] + (H[np.ix_(free, fixed)] @ z[fixed] if fixed else 0))
            try:
                zf = np.linalg.solve(Af, rhs)
            except np.linalg.LinAlgError:
                continue
            if np.any(zf < lo[free] - 1e-14) or np.any(zf > hi[free] + 1e-14):
                continue
            z[free] = zf
        best = min(best, c0 + g @ z + 0.5 * z @ H @ z)
    return best


def check(name, eps, d1):
    P_and_M, siga, sigb, tau, w, info, by_min = build(name, eps, d1)
    x20 = R.V.EX[name]["x20"]
    x20 = float(x20)
    th = np.linspace(0, 2 * np.pi, 721)[:-1]
    E = np.stack([np.cos(th), np.sin(th)], 1)
    ts = np.concatenate([np.linspace(1e-4, tau - 1e-6, 1500), tau + np.geomspace(1e-7, 2 - tau, 1500)])
    res = dict(minA=np.inf, minG=np.inf, r1=np.inf, margin_H3=np.inf, far_min=np.inf, far_min_outside_tube=np.inf,
               maxP=0.0, n_margin_viol=0)
    for t in ts:
        P, M = P_and_M(t)
        before = t < tau
        sig = siga(t) if before else sigb(t)
        ustar = 1.0 if before else -1.0
        uo = -ustar
        om = uo - ustar
        beta = P @ b - w
        res["maxP"] = max(res["maxP"], np.abs(P).max())
        res["minA"] = min(res["minA"], np.linalg.eigvalsh(M - 2 * eps * np.eye(2))[0])
        if abs(t - tau) <= d1:
            res["minG"] = min(res["minG"], np.linalg.eigvalsh(M - 2 * eps * np.eye(2) - Delta / (2 * abs(sig)) * np.outer(beta, beta))[0])
        # tube radius at u°: f(theta e) = |sig| Delta + theta om beta.e + 1/2 theta^2 e^T (M - eps) e
        qa = 0.5 * np.einsum("ni,ij,nj->n", E, M - eps * np.eye(2), E)
        qb = om * (E @ beta)
        qc = abs(sig) * Delta
        disc = qb ** 2 - 4 * qa * qc
        roots = np.where((disc >= 0) & (qb < 0), (-qb - np.sqrt(np.maximum(disc, 0))) / (2 * qa), np.inf)
        res["r1"] = min(res["r1"], roots.min())
        mu = np.linalg.eigvalsh(M)[0]
        mg = abs(sig) - Delta * (beta @ beta) / (2 * mu)
        res["margin_H3"] = min(res["margin_H3"], mg)
        res["n_margin_viol"] += int(mg <= 0)
        # far region over the continuous reachable box D_t (x0 = (0, x20), |u| <= 1)
        # x*(t): recompute from the extremal
        if before:
            xs = np.array([x20 * t + t * t / 2, x20 + t])
        else:
            x1s, x2s = x20 * tau + tau * tau / 2, x20 + tau
            s = t - tau
            xs = np.array([x1s + x2s * s - s * s / 2, x2s - s])
        lo = np.array([x20 * t - t * t / 2, x20 - t]) - xs
        hi = np.array([x20 * t + t * t / 2, x20 + t]) - xs
        for u in (1.0, -1.0):
            omu = u - ustar
            v = box_min_2d(sig * omu, omu * beta, M, lo, hi)
            res["far_min"] = min(res["far_min"], v)
    res["min_by_layer"] = by_min[0]
    res.update(info)
    return res


if __name__ == "__main__":
    out = []
    for name, eps, d1 in (("C", 0.02, 0.02), ("C", 0.01, 0.01), ("A", 0.02, 0.02)):
        r = check(name, eps, d1)
        r.update(example=name, eps=eps, d1=d1)
        print(json.dumps(r, default=float), flush=True)
        out.append(r)
    json.dump(out, open("logs/v_localtsqc.json", "w"), indent=1, default=float)
