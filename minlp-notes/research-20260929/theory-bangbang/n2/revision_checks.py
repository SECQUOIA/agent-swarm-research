"""Targeted checks for the revision of extension-n2.md after reviews/bangbang-n2-review.md.

Usage: python3 revision_checks.py [blowup] [cpre] [localF] [lyapW5] [crmax]   (default: all)
Writes logs/revision_checks_<part>.json; prints a summary to stdout.

Parts
- blowup : continuous blow-up distance s_b (integrator event time, after the fix in
           model.singular_riccati_after) for B (global model and local model, delta0 = .2/.1)
           and B2, with several s_top values; leading-order prediction delta0 exp(-1/(kappa|eta_L|)).
- cpre   : examples C and A.  Largest admissible tangential value at the switch (Proposition 4)
           Pmax = Q_eps(tau+) - beta_eps beta_eps^T / eta_eps.  Integrate the global-model (equality)
           equation backward on [0, tau) from Pmax; record blow-up time and the eigenvalues there.
- localF : examples A and C.  After the layer, Theorem 2's P equals Q_eps (any delta1), so M = 2 eps I.
           On [tau + delta1, T]: the (H3) margin of [R, Theorem 4.1], |sigma| - Delta|beta|^2/(2 mu) with
           mu = 2 eps, and the minimum of r over the continuous reachable box x U.  For LQ data and
           quadratic S, r(t, x*+d, u*+om) = sigma om + om beta.d + eps |d|^2 exactly; the minimum over
           om is at om = 0 (value >= 0) or at the other vertex, and the d-part is separable, so the
           box minimum is computed coordinatewise in closed form.
- lyapW5 : example A, continuous Lyapunov family Q_eps (eps = .02) on [0, T]: (W5) margin and the
           same box minimum of r, to compare with the discrete Lyap failures of Section 6.2.
- crmax  : example C, discrete maximal recursion (discrete.fam_rmax), N = 500 ... 16000, eps = 0, .02:
           fractional stages, break stage, max|P|, m_t at the fractional stages.
"""
import json
import sys

import numpy as np
from scipy.integrate import solve_ivp

from model import A, B, Par, find_switch, solve_arcs, switch_quantities, lyapunov_Q, singular_riccati_after
from discrete import solve_kkt, fam_rmax

EX = {
    "A": Par(T=2.0, a=1.0, rho=2.0, k1=-0.3, k2=-0.3, q=0.3, c=1.0, x20=0.5),
    "B": Par(T=2.0, a=1.0, rho=1.0, k1=0.6, k2=-1.2, c=0.5, q=1.0, x20=0.5, e=0.3),
    "B2": Par(T=2.0, a=1.0, rho=0.5, k1=0.5, k2=-0.6, q=0.3, c=0.2),
    "C": Par(T=2.0, a=1.0, rho=0.5, k1=0.5, k2=-0.2, q=0.3, c=0.2),
}


def setup(name):
    p = EX[name]
    th = find_switch(p)[0]
    sol = solve_arcs(p, th)
    return p, th, sol


def xstar(sol, t):
    arc = sol["a"] if t < sol["th"] else sol["b"]
    return np.array([arc["x1"](t), arc["x2"](t)])


def sigma(sol, t):
    return float((sol["a"] if t < sol["th"] else sol["b"])["sig"](t))


def reach_box(p, t):
    lo = np.array([p.x10 + p.x20 * t - 0.5 * t * t, p.x20 - t])
    hi = np.array([p.x10 + p.x20 * t + 0.5 * t * t, p.x20 + t])
    return lo, hi


def box_min_r(p, sol, t, beta, eps):
    """min over x in the reachable box and u in U of r = sig om + om beta.d + eps |d|^2 (LQ data, M = 2 eps I).
    Returns (value, d at the minimum)."""
    s = sigma(sol, t)
    ustar = p.ua if t < sol["th"] else p.ub
    uo = p.ub if t < sol["th"] else p.ua
    om = uo - ustar
    lo, hi = reach_box(p, t)
    x = xstar(sol, t)
    dlo, dhi = lo - x, hi - x
    if eps > 0:
        d = np.clip(-om * beta / (2 * eps), dlo, dhi)
    else:  # linear in d: pick the endpoint that makes om beta_i d_i smallest
        d = np.where(om * beta > 0, dlo, dhi)
    val = s * om + om * beta @ d + eps * d @ d
    return float(min(val, 0.0)), d  # om = 0 gives eps|d|^2 >= 0, with minimum 0 at d = 0


def part_blowup():
    out = {}
    p, th, sol = setup("B")
    sq = switch_quantities(p, sol)
    kap = sq["Delta"] / (2 * abs(sq["sigdot_b"]))
    recs = []
    for eps in (0.0, 0.02):
        for s_top in (0.19, 0.1, 0.05):
            r = singular_riccati_after(p, sol, eps, s_top=s_top)
            recs.append(dict(ex="B", model="global", eps=eps, s_top=s_top, s_b=r.get("s_blow")))
        for d0 in (0.2, 0.1):
            r = singular_riccati_after(p, sol, eps, delta0=d0, s_top=0.999 * d0)
            pred = d0 * np.exp(-1.0 / (kap * abs(sq["eta_L"])))
            recs.append(dict(ex="B", model="local", delta0=d0, eps=eps, s_b=r.get("s_blow"),
                             pred_leading_order_eps0=float(pred), pred_over_sb=float(pred / r["s_blow"])))
    p2, th2, sol2 = setup("B2")
    for eps in (0.0, 0.02):
        for s_top in (None, 0.05):
            r = singular_riccati_after(p2, sol2, eps, s_top=s_top)
            recs.append(dict(ex="B2", model="global", eps=eps, s_top=s_top, s_b=r.get("s_blow")))
    for rec in recs:
        print(rec, flush=True)
    out["records"] = recs
    out["kappa_B"], out["eta_L_B"] = kap, sq["eta_L"]
    return out


def part_cpre():
    out = []
    for name in ("C", "A"):
        p, th, sol = setup(name)
        Delta = abs(p.ub - p.ua)
        sig_a = sol["a"]["sig"]
        for eps in (0.0, 0.02):
            sq = switch_quantities(p, sol, eps)
            Q, beta, eta = sq["Qplus"], sq["beta_L"], sq["eta_L"]  # at this eps: Q_eps(tau+), beta_eps, eta_eps
            Pmax = Q - np.outer(beta, beta) / eta

            def rhs(t, y):
                P = y.reshape(2, 2)
                bt = P @ B - p.w
                return (-(A.T @ P + P @ A + p.Hxx) + 2 * eps * np.eye(2)
                        + Delta / (2 * abs(sig_a(t))) * np.outer(bt, bt)).ravel()

            ev = lambda t, y: 1e8 - np.abs(y).max()
            ev.terminal = True
            for s0 in (1e-9, 1e-6):
                for method in ("LSODA", "DOP853"):
                    r = solve_ivp(rhs, (th - s0, 0.0), Pmax.ravel(), method=method, rtol=1e-11, atol=1e-13,
                                  events=ev)
                    rec = dict(ex=name, eps=eps, eta_eps=float(eta), Pmax=Pmax.tolist(), s0=s0, method=method,
                               blowup=bool(r.status == 1))
                    if r.status == 1:
                        Pe = r.y_events[0][0].reshape(2, 2)
                        rec["t_blow"] = float(r.t_events[0][0])
                        rec["eig_at_blow"] = np.linalg.eigvalsh(0.5 * (Pe + Pe.T)).tolist()
                    else:
                        rec["P0"] = r.y[:, -1].reshape(2, 2).tolist()
                    out.append(rec)
                    print({k: v for k, v in rec.items() if k != "Pmax"}, flush=True)
    return out


def part_localF():
    out = []
    for name in ("A", "C"):
        p, th, sol = setup(name)
        Delta = abs(p.ub - p.ua)
        for eps in (0.02, 0.01):
            Q = lyapunov_Q(p, sol, eps).sol
            delta1 = 0.02
            tt = np.linspace(th + delta1, p.T, 2001)
            h3, fr = [], []
            for t in tt:
                P = Q(t).reshape(2, 2)
                beta = P @ B - p.w
                h3.append(abs(sigma(sol, t)) - Delta * (beta @ beta) / (2 * 2 * eps))
                fr.append(box_min_r(p, sol, t, beta, eps)[0])
            h3, fr = np.array(h3), np.array(fr)
            i = int(np.argmin(fr))
            rec = dict(ex=name, eps=eps, delta1=delta1, t_range=[float(tt[0]), float(tt[-1])],
                       H3_margin_min=float(h3.min()), H3_fail_fraction=float(np.mean(h3 <= 0)),
                       H3_fail_t=[float(tt[h3 <= 0].min()), float(tt[h3 <= 0].max())] if np.any(h3 <= 0) else None,
                       boxmin_r_min=float(fr.min()), boxmin_r_argmin_t=float(tt[i]),
                       F_fail_fraction=float(np.mean(fr < 0)),
                       F_fail_t=[float(tt[fr < 0].min()), float(tt[fr < 0].max())] if np.any(fr < 0) else None)
            out.append(rec)
            print(rec, flush=True)
    return out


def part_lyapW5():
    p, th, sol = setup("A")
    Delta = abs(p.ub - p.ua)
    eps = 0.02
    QT = p.Phixx(*sol["xT"]) - 2 * eps * np.eye(2)
    f = lambda t, y: (-(A.T @ y.reshape(2, 2) + y.reshape(2, 2) @ A + p.Hxx) + 2 * eps * np.eye(2)).ravel()
    Q = solve_ivp(f, (p.T, 0.0), QT.ravel(), rtol=1e-12, atol=1e-14, dense_output=True).sol
    tt = np.linspace(0.0, p.T, 4001)[1:]
    tt = tt[np.abs(tt - th) > 1e-9]
    w5, fr, nb = [], [], []
    for t in tt:
        P = Q(t).reshape(2, 2)
        beta = P @ B - p.w
        nb.append(float(np.linalg.norm(beta)))
        w5.append(abs(sigma(sol, t)) - Delta * (beta @ beta) / (2 * 2 * eps))
        fr.append(box_min_r(p, sol, t, beta, eps)[0])
    w5, fr, nb = np.array(w5), np.array(fr), np.array(nb)
    last = tt > th
    rec = dict(ex="A", eps=eps, tau=th,
               W5_fail_t=[float(tt[w5 <= 0].min()), float(tt[w5 <= 0].max())],
               W5_fail_contiguous=bool(np.all(w5[(tt >= tt[w5 <= 0].min()) & (tt <= tt[w5 <= 0].max())] <= 0)),
               beta_norm_last_arc=[float(nb[last].min()), float(nb[last].max())],
               beta_norm_at_tau=float(np.linalg.norm(Q(th).reshape(2, 2) @ B - p.w)),
               boxmin_r_fail_t=[float(tt[fr < 0].min()), float(tt[fr < 0].max())],
               boxmin_r_fail_contiguous=bool(np.all(fr[(tt >= tt[fr < 0].min()) & (tt <= tt[fr < 0].max())] < 0)),
               boxmin_r_fail_start_before_tau=float(th - tt[fr < 0].min()),
               boxmin_r_min=float(fr.min()))
    print(rec, flush=True)
    return rec


def part_crmax():
    p = EX["C"]
    out = []
    for N in (500, 1000, 2000, 4000, 8000, 16000):
        kk = solve_kkt(p, N)
        for eps in (0.0, 0.02):
            Ps, brk, ms = fam_rmax(p, kk, eps)
            fr = sorted(kk["fracset"])
            rec = dict(N=N, eps=eps, s=kk["m"], fracset=fr, u_frac=[float(kk["u"][t]) for t in fr],
                       kkt_viol=kk["kkt_viol"], brk=brk, brk_time=None if brk is None else brk * kk["h"],
                       brk_minus_s=None if brk is None else brk - kk["m"],
                       maxabsP=float(np.nanmax(np.abs(Ps))),
                       m_at_frac=[float(ms[t]) for t in fr],
                       min_m=float(np.nanmin(ms)))
            out.append(rec)
            print(rec, flush=True)
    return out


def part_rcheck():
    """Validate box_min_r: (1) r from its definition, l0 + l1 u + S_t + S_x.g with
    S = psi.d + 1/2 d^T Q_eps d (the constant V* is fixed by r(t, x*, u*) = 0), against the closed form
    sig om + om beta.d + eps|d|^2 at random points; (2) closed-form box minimum against a 401 x 401 grid."""
    rng = np.random.default_rng(0)
    out = []
    for name in ("A", "C"):
        p, th, sol = setup(name)
        eps = 0.02
        Q = lyapunov_Q(p, sol, eps).sol
        arc = sol["b"]
        I2 = np.eye(2)

        def rtilde(t, x, u):
            xs = np.array([arc["x1"](t), arc["x2"](t)])
            xsd = np.array([arc["x1"].deriv()(t), arc["x2"].deriv()(t)])
            psi = np.array([arc["psi1"](t), arc["psi2"](t)])
            psid = np.array([arc["psi1"].deriv()(t), arc["psi2"].deriv()(t)])
            P = Q(t).reshape(2, 2)
            Pd = -(A.T @ P + P @ A + p.Hxx) + 2 * eps * I2
            d = x - xs
            St = psid @ d - psi @ xsd - d @ P @ xsd + 0.5 * d @ Pd @ d
            Sx = psi + P @ d
            l0 = p.e * x[1] + 0.5 * p.q * x[0] ** 2 - 0.5 * p.c * x[1] ** 2
            l1 = p.k1 * x[0] + p.k2 * x[1]
            return l0 + l1 * u + St + Sx @ np.array([x[1], u])

        err, gap = 0.0, 0.0
        for _ in range(200):
            t = rng.uniform(th + 0.02, p.T)
            lo, hi = reach_box(p, t)
            x = lo + rng.uniform(size=2) * (hi - lo)
            u = rng.uniform(-1, 1)
            xs = xstar(sol, t)
            d, om = x - xs, u - p.ub
            beta = Q(t).reshape(2, 2) @ B - p.w
            r_def = rtilde(t, x, u) - rtilde(t, xs, p.ub)
            r_cf = sigma(sol, t) * om + om * beta @ d + eps * d @ d
            err = max(err, abs(r_def - r_cf))
        for t in np.linspace(th + 0.02, p.T, 7):
            beta = Q(t).reshape(2, 2) @ B - p.w
            v, _ = box_min_r(p, sol, t, beta, eps)
            lo, hi = reach_box(p, t)
            xs = xstar(sol, t)
            g1, g2 = np.meshgrid(np.linspace(lo[0], hi[0], 401) - xs[0], np.linspace(lo[1], hi[1], 401) - xs[1])
            om = p.ua - p.ub
            grid = sigma(sol, t) * om + om * (beta[0] * g1 + beta[1] * g2) + eps * (g1 ** 2 + g2 ** 2)
            gap = max(gap, float(min(grid.min(), 0.0) - v))  # >= 0; small if the closed form is the minimum
        rec = dict(ex=name, eps=eps, max_abs_r_definition_minus_closed_form=float(err),
                   max_grid_min_minus_closed_form_min=gap)
        out.append(rec)
        print(rec, flush=True)
    return out


PARTS = dict(blowup=part_blowup, cpre=part_cpre, localF=part_localF, lyapW5=part_lyapW5, crmax=part_crmax,
             rcheck=part_rcheck)

if __name__ == "__main__":
    names = sys.argv[1:] or list(PARTS)
    for nm in names:
        print("==", nm, flush=True)
        res = PARTS[nm]()
        json.dump(res, open("logs/revision_checks_%s.json" % nm, "w"), indent=1, default=float)
