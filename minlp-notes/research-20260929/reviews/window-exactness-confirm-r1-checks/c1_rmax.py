"""Confirmation check (item 3): discrete maximal recursion index in Section 7.6.

Own code: own scalar KKT search for toy plus, own scalar and 2x2 maximal recursions.
For the two-state example A- only the KKT point is taken from [E]'s solver (n2/discrete.py
solve_kkt, read-only input); the recursion, eta values and log law are recomputed here.

Prints, per N: interior stages, break stage (relative to s), b^T Phat_{s+1} b - b^T w (new
definition of eta_hat_1) and b^T (F^T Phat_{s+2} b - w) (old printed formula), and the
leading-order law [1/eta_L + (1/gamma) log(1/h)]^{-1}.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "theory-bangbang")
sys.path.insert(0, os.path.join(ROOT, "n2"))


# ----------------------------------------------------------------- scalar toy plus (own code)
def toy_kkt(N, k=0.5, T=2.0, a1=2.0, a2=-1.0, tj=1.0, phi1=1.0, phi2=0.0):
    h = T / N
    a = np.array([a1 if t * T < tj * N else a2 for t in range(N + 1)])

    def J_of(u):
        x = np.concatenate([[0.0], np.cumsum(h * u)])
        return h * np.sum((x[:N] - a[:N]) ** 2 / 2 + k * x[:N] * u) + phi1 * x[N] + phi2 * x[N] ** 2 / 2, x

    def sig_of(u, x):
        p = np.empty(N + 1)
        p[N] = phi1 + phi2 * x[N]
        for t in range(N - 1, -1, -1):
            p[t] = p[t + 1] + h * (x[t] - a[t] + k * u[t])
        return k * x[:N] + p[1:], p

    best = None
    step = max(1, N // 400)
    coarse = []
    for m in range(1, N - 1, step):
        u = np.where(np.arange(N) < m, 1.0, -1.0)
        coarse.append((J_of(u)[0], m))
    mc = min(coarse)[1]
    for m in range(max(1, mc - 3 * step), min(N - 1, mc + 3 * step + 1)):
        u = np.where(np.arange(N) < m, 1.0, -1.0)
        # J restricted to u_m is an exact quadratic: fit by three evaluations
        vals = []
        for v in (-1.0, 0.0, 1.0):
            u[m] = v
            vals.append(J_of(u)[0])
        c2 = (vals[0] + vals[2] - 2 * vals[1]) / 2
        c1 = (vals[2] - vals[0]) / 2
        cand = [-1.0, 1.0] + ([-c1 / (2 * c2)] if c2 > 0 and abs(c1 / (2 * c2)) < 1 else [])
        for v in cand:
            u[m] = v
            J, _ = J_of(u)
            if best is None or J < best[0]:
                best = (J, m, u.copy())
    J, m, u = best
    _, x = J_of(u)
    sig, p = sig_of(u, x)
    inter = [int(t) for t in np.where(np.abs(u) < 1 - 1e-12)[0]]
    viol = np.where(u > 1 - 1e-12, np.maximum(0, sig), np.where(u < -1 + 1e-12, np.maximum(0, -sig), np.abs(sig)))
    s = inter[0] if inter else int(np.where(u < 0)[0][0])
    return dict(N=N, h=h, u=u, sig=sig, s=s, inter=inter, viol=float(viol.max()), k=k)


def toy_rmax(kk):
    """P_t = h + P_{t+1} - beta^2/m, beta = P_{t+1} + k, m = 2|sig|/(h Delta) + P_{t+1}, Delta = 2, eps = 0."""
    N, h, k = kk["N"], kk["h"], kk["k"]
    P = np.full(N + 1, np.nan)
    P[N] = 0.0
    for t in range(N - 1, -1, -1):
        sg = 0.0 if t in kk["inter"] else abs(kk["sig"][t])
        m = sg / h + P[t + 1]
        if m <= 0:
            return P, t
        beta = P[t + 1] + k
        P[t] = h + P[t + 1] - beta * beta / m
    return P, None


def part_toy():
    out = []
    eta_L, gam = 2.0226, 1.5226
    for k in (0.5, 0.1):
        for N in (500, 1000, 2000, 4000, 8000, 16000, 32000):
            kk = toy_kkt(N, k=k)
            P, brk = toy_rmax(kk)
            s = kk["s"]
            rec = dict(k=k, N=N, s=s, inter=[t - s for t in kk["inter"]], kkt_viol=kk["viol"],
                       brk=None if brk is None else brk - s,
                       eta_new=float(P[s + 1] + k), eta_old=float(P[s + 2] + k))
            if k == 0.5:
                h = kk["h"]
                rec["law"] = 1 / (1 / eta_L + np.log(1 / h) / gam)
            print(json.dumps(rec), flush=True)
            out.append(rec)
    return out


# ----------------------------------------------------------------- two-state A- (own recursion)
def part_aminus():
    from model import Par, find_switch, solve_arcs, switch_quantities, B
    import discrete as dz
    p = Par(rho=2, k1=-.3, k2=.3, q=.3, c=1, x20=.5)
    th = find_switch(p)[0]
    sq = switch_quantities(p, solve_arcs(p, th))
    gam, eta_L = abs(sq["sigdot"]), sq["eta_L"]
    w = p.w
    kap = float(B @ w)
    out = []
    for N in (500, 1000, 2000, 4000, 8000, 16000, 32000):
        kk = dz.solve_kkt(p, N)
        h, s = kk["h"], kk["m"]
        F = np.array([[1.0, h], [0.0, 1.0]])
        Hx = np.diag([p.q, -p.c])
        Pn = np.full((N + 1, 2, 2), np.nan)
        Pn[N] = np.diag([0.0, p.rho + 3 * p.nu * kk["x"][N, 1] ** 2])
        brk = None
        for t in range(N - 1, -1, -1):
            X = Pn[t + 1]
            beta = F.T @ X @ B - w
            sg = 0.0 if t in kk["fracset"] else abs(kk["sig"][t])
            m = 2 * sg / (2 * h) + B @ X @ B
            if m <= 0:
                brk = t
                break
            Pn[t] = h * Hx + F.T @ X @ F - np.outer(beta, beta) / m
        rec = dict(N=N, s=s, inter=sorted(t - s for t in kk["fracset"]), kkt_viol=kk["kkt_viol"],
                   brk=None if brk is None else brk - s, kappa=kap,
                   eta_new=None if np.isnan(Pn[s + 1]).any() else float(B @ Pn[s + 1] @ B - kap),
                   eta_old=None if np.isnan(Pn[s + 2]).any() else float(B @ (F.T @ Pn[s + 2] @ B - w)),
                   law=float(1 / (1 / eta_L + np.log(1 / h) / gam)), T=p.T, gamma=gam, eta_L=eta_L)
        print(json.dumps(rec), flush=True)
        out.append(rec)
    return out


if __name__ == "__main__":
    res = dict(toy=part_toy(), aminus=part_aminus())
    with open(os.path.join(HERE, "logs", "c1_rmax.json"), "w") as f:
        json.dump(res, f, indent=1, default=float)
