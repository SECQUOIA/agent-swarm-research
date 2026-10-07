"""Runs for kappa-negative.md, Part 2 (several switches, close switches, terminal row).

usage: OMP_NUM_THREADS=1 python3 run_multi.py PART [PART ...]     PART in: two kink close close2 row sweep
Toy (ktoy.py): x' = u, |u| <= 1, x(0) = 0, T = 2, target a = 4 on [0, t1), -4 on [t1, t2), 4 on [t2, 2],
Phi = (x - 3)^2 / 2 (phi1 = -3, phi2 = 1, constant dropped), k(t) piecewise constant.  The optimal
control is +1, -1, +1 (two switches); kappa at switch j is -k(tau_j).
"""
import json
import math
import os
import sys
import time
from fractions import Fraction as Fr

import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ktoy import (KToy, kkt, exact_kkt, fam_const, bound, data, simulate, adjoint, stage_loss,  # noqa: E402
                  window_value, fam_rmax, float_data)
from lifted import certify_multi  # noqa: E402

LOG = os.path.join(HERE, "logs")
OUT = []


def emit(rec):
    print(json.dumps(rec, default=float), flush=True)
    OUT.append(rec)


def dump(name):
    with open(os.path.join(LOG, f"{name}.json"), "w") as f:
        json.dump(OUT, f, indent=1, default=float)
    OUT.clear()


def toy2(k_pts, t1, t2, xT=None):
    return KToy(a_pts=((0.0, 4.0), (t1, -4.0), (t2, 4.0)), k_pts=k_pts, phi1=-3.0, phi2=1.0, R=4.0, xT=xT)


def structure(toy, N=400):
    """Switch times of the kappa-free transcription J - (h^2/2) sum kappa_t u_t^2 (L-BFGS-B; it is convex
    for these data when k is constant); used as the starting guess for the KKT search."""
    h = toy.T / N
    _, kk_ = data(toy, N)

    def f(u):
        x, J = simulate(toy, N, u)
        _, sig = adjoint(toy, N, x, u)
        return J + 0.5 * h * h * np.sum(kk_[:N] * u * u), h * sig + h * h * kk_[:N] * u
    r = minimize(f, np.zeros(N), jac=True, method="L-BFGS-B", bounds=[(-1, 1)] * N,
                 options=dict(maxiter=5000, ftol=1e-15, gtol=1e-12))
    u = r.x
    return [i * h for i in range(1, N) if np.sign(u[i]) != np.sign(u[i - 1])]


def switching_stages(Z):
    """First stage of each new control value (interior stages count as switching stages)."""
    out = []
    u = Z["u"]
    for t in range(1, Z["N"]):
        if t in Z["frac"]:
            out.append(t)
        elif u[t] != u[t - 1] and (t - 1) not in Z["frac"]:
            out.append(t)
    return out


# ---------------------------------------------------------------------------------------------- two
CASES = [(-0.5, 0.5, 1.5), (-0.5, 0.6, 1.4), (0.0, 0.5, 1.5), (0.0, 0.6, 1.4), (0.0, 0.65, 1.35),
         (0.0, 0.7, 1.3), (0.5, 0.5, 1.5), (0.5, 0.7, 1.3), (0.5, 0.75, 1.25)]


def part_two():
    """Two switches with the same kappa (LQ data: kappa = -k at every switch).  Tangential family
    P = -k (beta = 0 at every stage).  kappa > 0 and kappa = 0: exact rational gap of the plain
    calibration (no window).  kappa < 0: exact certificate by branch and bound on the switching-stage
    controls (lifted and fixed node families, certify_box)."""
    for (k, t1, t2) in CASES:
        toy = toy2(((0.0, k),), t1, t2)
        sw = structure(toy)
        for N in (500, 1000, 2000, 4000):
            t0 = time.time()
            kk = kkt(toy, N, sw)
            if kk is None:
                emit(dict(k=k, t1=t1, t2=t2, N=N, kkt="not found"))
                continue
            Z = exact_kkt(toy, kk)
            h = Z["h"]
            P = fam_const(N, -Fr(k))
            B, L, LN = bound(toy, Z, P)
            ss = switching_stages(Z)
            rec = dict(kappa=-k, t1=t1, t2=t2, N=N, switches=sw, ell=sw[1] - sw[0] if len(sw) == 2 else None,
                       switch_stages=ss, frac=Z["frac"], u_frac=[float(Z["u"][t]) for t in Z["frac"]],
                       sig_over_h={t: [round(float(Z["sig"][s] / h), 4) for s in (t - 1, t)] for t in ss},
                       gap_over_h2=float((Z["J"] - B) / h ** 2), exact_gap_zero=(B == Z["J"]),
                       failing=[(t, float(v / h ** 2)) for t, v in L.items() if v > 0], terminal_loss=float(LN))
            if k > 0 and B != Z["J"] and N <= 2000:
                res = certify_multi(toy, Z, P, Z["J"], max_nodes=150)
                inc = res["incumbent"]
                if inc["improved"]:
                    uu = inc["u"]
                    rec.update(incumbent_improved=True, incumbent_J_minus_J_over_h2=float((inc["J"] - Z["J"]) / h ** 2),
                               incumbent_frac=inc["frac"], incumbent_u_frac=[float(uu[t]) for t in inc["frac"]],
                               incumbent_monotone_switches=sum(1 for t in range(1, N) if uu[t] != uu[t - 1] and not (
                                   -1 < uu[t] < 1 or -1 < uu[t - 1] < 1)) + len(inc["frac"]))
                rec.update(cert_ok=res["ok"], cert_nodes=res["n_nodes"], cert_leaves=res.get("n_leaves"),
                           cert_kinds=[(q["kind"], q.get("stages", q.get("stage")), q.get("box")) for q in res["nodes"]])
            rec["time"] = time.time() - t0
            emit(rec)
    dump("two")


# ---------------------------------------------------------------------------------------------- kink
def kink_family(N, T, taus, c):
    """kappa = 0 (k = 0): P(t) = 0 before tau_1, -c dist(t, {tau_1, tau_2}) between and -c (t - tau_2)
    after; tangential (P(tau_j) = 0 = w) but with b^T P_{n+1} b < 0 at the switching stages."""
    t1, t2 = taus
    mid = (t1 + t2) / 2
    out = []
    for i in range(N + 1):
        t = Fr(i) * Fr(T) / N
        if t <= t1:
            v = Fr(0)
        elif t <= mid:
            v = -c * (t - t1)
        elif t <= t2:
            v = -c * (t2 - t)
        else:
            v = -c * (t - t2)
        out.append(v)
    return out


def part_kink():
    """Theorem B with two switches: kappa = 0 at both, family with O(h^3) failures at the switching
    stages; windows {n - K, ..., n + K} around each failing stage (exact rational minima)."""
    for (t1, t2) in ((0.5, 1.5), (0.6, 1.4), (0.65, 1.35), (0.7, 1.3)):
        toy = toy2(((0.0, 0.0),), t1, t2)
        sw = structure(toy)
        # switch times from the phase positions of the KKT point at N = 16000 (error O(h) = O(1e-4)):
        # theta = t_n + h (u_n - u_after) / (u_before - u_after) at a switching stage n
        kf = kkt(toy, 16000, sw)
        hf = kf["h"]
        taus = []
        u = kf["u"]
        t = 1
        while t < 16000 and len(taus) < 2:
            if u[t] != u[t - 1]:
                before = u[t - 1]
                n = t
                after = u[t + 1] if (-1 < u[t] < 1) else u[t]
                taus.append(Fr(n * hf + hf * (u[n] - after) / (before - after)).limit_denominator(10 ** 9))
                t += 2
                continue
            t += 1
        for N in (1000, 2000, 4000):
            t0 = time.time()
            kk = kkt(toy, N, sw)
            Z = exact_kkt(toy, kk)
            h = Z["h"]
            P = kink_family(N, toy.T, taus, Fr(3, 10))
            B, L, LN = bound(toy, Z, P)
            fail = [t for t, v in L.items() if v > 0]
            wins = {}
            for t in fail:
                wins[t] = [float(-window_value(toy, Z, P, t - K, t + K + 1) / h ** 3) for K in (0, 1, 2)]
            emit(dict(t1=t1, t2=t2, N=N, ell=sw[1] - sw[0], taus=[float(v) for v in taus], frac=Z["frac"], failing=[(t, float(L[t] / h ** 3)) for t in fail],
                      terminal_loss=float(LN), window_deficits_over_h3_K012=wins, time=time.time() - t0))
    dump("kink")


# ---------------------------------------------------------------------------------------------- close
def part_close(pairs=((-0.5, 0.0), (0.0, -0.5), (-0.5, -0.3), (-0.3, -0.5)),
               configs=((0.5, 1.5), (0.6, 1.4), (0.65, 1.35)), name="close"):
    """kappa changes between the switches (k(t) jumps at the midpoint t_k of the middle arc).  Necessary
    condition for a tangential calibration with (A) on the middle arc (kappa-negative.md, Prop. 6.2):
    eta^X_1 = kappa_2 - kappa_1 + ell (1 - 2 eps) >= 0 (scalar toy: b = 1, A = 0, H_xx = 1).  Float
    screening: discrete maximal recursion (Lemma 10 of extension-n2.md, eps = 0) and where it breaks."""
    for (k1, k2) in pairs:
        for (t1, t2) in configs:
            base = toy2(((0.0, k1),), t1, t2)
            sw0 = structure(base)
            if len(sw0) != 2:
                emit(dict(k1=k1, k2=k2, t1=t1, t2=t2, base_structure=sw0))
                continue
            tk = round((sw0[0] + sw0[1]) / 2 * 64) / 64          # dyadic midpoint
            toy = toy2(((0.0, k1), (tk, k2)), t1, t2)
            sw = structure(toy)
            if len(sw) != 2:
                emit(dict(k1=k1, k2=k2, t1=t1, t2=t2, structure=sw))
                continue
            ell = sw[1] - sw[0]
            for N in (1000, 2000, 4000, 8000):
                kk = kkt(toy, N, sw)
                if kk is None:
                    emit(dict(k1=k1, k2=k2, t1=t1, t2=t2, N=N, kkt="not found"))
                    continue
                D = float_data(toy, kk)
                P, br = fam_rmax(toy, D, eps=0.0)
                h = kk["h"]
                s1 = [t for t in range(1, N) if kk["u"][t] != kk["u"][t - 1]][0]
                rec = dict(kappa1=-k1, kappa2=-k2, t1=t1, t2=t2, tk=tk, N=N, switches=sw, ell=ell,
                           eta_X_pred=(-k2) - (-k1) + ell, frac=kk["frac"], first_switch_stage=s1,
                           break_stage=br, break_time=None if br is None else br * h,
                           break_minus_tau1=None if br is None else br * h - sw[0],
                           break_minus_s1_stages=None if br is None else br - s1)
                if br is None:
                    # all stages exact over R x U and P_N = phi2: exact certificate (float check of losses)
                    Lmax = max(stage_loss(toy, D, P, t) for t in range(N))
                    rec["max_stage_loss_float"] = float(Lmax)
                emit(rec)
    dump(name)


def part_close2():
    part_close(pairs=((-1.0, 0.0), (0.0, -1.0)), configs=((0.5, 1.5), (0.55, 1.45), (0.45, 1.55)), name="close2")


# ---------------------------------------------------------------------------------------------- sweep
SWEEP_N = (1000, 1500, 2000, 2500, 3000, 3500, 4000, 5000, 6000, 7000, 8000, 10000, 12000, 16000)
SWEEP_CONFIGS = ((-0.5, 0.0, 0.5, 1.5), (-0.5, 0.0, 0.6, 1.4), (-0.5, -0.3, 0.5, 1.5), (-0.5, -0.3, 0.6, 1.4),
                 (-1.0, 0.0, 0.5, 1.5), (-1.0, 0.0, 0.55, 1.45), (-1.0, 0.0, 0.45, 1.55))


def part_sweep(configs=SWEEP_CONFIGS, Ns=SWEEP_N):
    """Revision after review (F1): N-sweep of the maximal recursion for the falling-kappa close-switch
    configurations (k1 -> k2 at the dyadic midpoint, as in part_close).  Float.  Per grid: switching
    stages s1 < s2, fractional stages, |sigma|/h at s1 - 1, s1, s1 + 1, the excess after the first switch
    eta_hat_1 = P_{s1+1} - kappa_1, the excess carried into the middle arc from the second switch
    e_2 = P_{m_k} - kappa_2 - (s2 - m_k) h (m_k = first stage with k = k2), and the break stage."""
    for (k1, k2, t1, t2) in configs:
        base = toy2(((0.0, k1),), t1, t2)
        sw0 = structure(base)
        if len(sw0) != 2:
            emit(dict(k1=k1, k2=k2, t1=t1, t2=t2, base_structure=sw0))
            continue
        tk = round((sw0[0] + sw0[1]) / 2 * 64) / 64
        toy = toy2(((0.0, k1), (tk, k2)), t1, t2)
        sw = structure(toy)
        ell = sw[1] - sw[0]
        for N in Ns:
            t0 = time.time()
            kk = kkt(toy, N, sw)
            if kk is None:
                emit(dict(k1=k1, k2=k2, t1=t1, t2=t2, N=N, kkt="not found"))
                continue
            D = float_data(toy, kk)
            P, br = fam_rmax(toy, D, eps=0.0)
            h = kk["h"]
            u = kk["u"]
            chg = [t for t in range(1, N) if u[t] != u[t - 1]]
            s1 = chg[0]
            s2 = [t for t in chg if t > s1 + 1 and (t - 1) not in kk["frac"]][0]
            mk = int(np.ceil(tk * N / toy.T - 1e-9))
            sg = [round(abs(float(kk["sig"][t])) / h, 3) for t in (s1 - 1, s1, s1 + 1)]
            eta1 = None if (br is not None and br >= s1 + 1) else float(P[s1 + 1] - (-k1))
            e2 = None if (br is not None and br >= mk) else float(P[mk] - (-k2) - (s2 - mk) * h)
            # theta_1: phase position of the first switch (u from +1 to -1, Delta = 2):
            # theta = t_n + h (u_n - u_after) / (u_before - u_after) = t_n + h (1 + u_n) / 2, which tends to
            # t_n (the vertex rule) as u_n -> -1.  Revision after review (round 3): the sign of u_n was wrong.
            n1 = s1
            theta1 = n1 * h + h * (1 + u[n1]) / 2 if n1 in kk["frac"] else n1 * h
            emit(dict(kappa1=-k1, kappa2=-k2, t1=t1, t2=t2, tk=tk, N=N, ell=ell, eta_X_pred=(-k2) - (-k1) + ell,
                      kkt_viol=kk["kkt_viol"], frac=kk["frac"], s1=s1, s2=s2, u_s1=float(u[s1]),
                      sig_over_h_s1m1_s1_s1p1=sg,
                      eta_hat_1=eta1, e2=e2, break_minus_s1=None if br is None else br - s1,
                      break_time_minus_theta1=None if br is None else br * h - theta1, time=time.time() - t0))
    dump("sweep")


# ---------------------------------------------------------------------------------------------- row
def part_row():
    """Terminal row x_N = xT = -63/64 (toy plus data of window-exactness.md, one switch at 0.5078125).  kappa >= 0: the
    tangential family P = -k is exact at every stage and the terminal term is trivial (X_N a point).
    kappa < 0: the same family fails at the fractional stage by kappa h^2 om^2 / 2 (Theorem C does not
    see the row); maximal recursion with P_N = +infinity (row): excess eta_hat_1 and break stage."""
    for k in (-0.5, 0.0, 0.5):
        toy = KToy(a_pts=((0.0, 2.0), (1.0, -1.0)), k_pts=((0.0, k),), phi1=0.0, phi2=0.0, xT=-0.984375, R=2.0)
        free = KToy(a_pts=((0.0, 2.0), (1.0, -1.0)), k_pts=((0.0, k),), phi1=1.0, phi2=0.0, R=2.0)
        for N in (500, 1000, 2000, 4000, 8000, 16000):
            t0 = time.time()
            kk = kkt(toy, N, [0.5078125])
            if kk is None:
                emit(dict(k=k, N=N, kkt="not found"))
                continue
            rec = dict(kappa=-k, N=N, frac=kk["frac"], u_frac=[float(kk["u"][t]) for t in kk["frac"]], nu=kk["nu"])
            D = float_data(toy, kk)
            Pm, br = fam_rmax(toy, D, eps=0.0, PN="inf")
            n = kk["frac"][0] if kk["frac"] else None
            rec.update(rmax_break=br, eta_hat_1=(None if (n is None or Pm[n + 1] is None) else float(Pm[n + 1] + k)))
            # free-end comparison (window-exactness.md Sec. 7.6 quantity) at the same N
            kf = kkt(free, N, [0.4774])
            if kf is not None and kf["frac"]:
                Df = float_data(free, kf)
                Pf, brf = fam_rmax(free, Df, eps=0.0)
                nf = kf["frac"][0]
                rec.update(free_eta_hat_1=float(Pf[nf + 1] + k) if Pf[nf + 1] is not None else None, free_break=brf)
            if N <= 4000:
                Z = exact_kkt(toy, kk)
                P = fam_const(N, -Fr(k))
                B, L, LN = bound(toy, Z, P)
                rec.update(exact_gap_over_h2=float((Z["J"] - B) / Z["h"] ** 2),
                           failing=[(t, float(v / Z["h"] ** 2)) for t, v in L.items() if v > 0])
            rec["time"] = time.time() - t0
            emit(rec)
    dump("row")


if __name__ == "__main__":
    for part in sys.argv[1:]:
        dict(two=part_two, kink=part_kink, close=part_close, close2=part_close2, row=part_row, sweep=part_sweep)[part]()
