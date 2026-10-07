"""Round-3 confirmation check of kappa-negative.md, item P1 (phase position theta_1).  Float.

Own code; does not import the author's code.  Problem data from the note (Section 9):
  x' = u, |u| <= 1, x(0) = 0, T = 2, a = 4 on [0, t1), -4 on [t1, t2), 4 on [t2, 2],
  Phi = (x - 3)^2 / 2 (phi1 = -3, phi2 = 1), k = k1 on [0, tk), k2 on [tk, 2];
  Euler: J = h sum_t [(x_t - a_t)^2/2 + k_t x_t u_t] + Phi(x_N), x_{t+1} = x_t + h u_t, a_t = a(t h).
Reads from the author's logs only: tk (a problem datum), the logged pattern (s1, s2, frac) for matching,
and break_minus_s1 (cross-checked against the round-1 referee's own sweep logs).

For each strong-drop grid: enumerate all KKT points of the form +1 | (vertex or fractional) | -1 |
(vertex or fractional) | +1 with switching stages within +-W of the logged ones, solving exactly for the
fractional controls (J is quadratic), then checking the sign conditions.  Then theta_1 by
t_{s1} + h (1 + u_{s1}) / 2 (fractional) or t_{s1} (vertex), and break time - theta_1.
"""
import json
import math
import os
import sys
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
KLOG = os.path.join(HERE, "..", "..", "theory-bangbang", "kneg", "logs")
R1LOG = os.path.join(HERE, "..", "kappa-negative-confirm-r1-checks", "logs")
T = 2
CFG = {(0.5, 1.5): "m590", (0.55, 1.45): "m690", (0.45, 1.55): "m490"}
W = 12


def stage_data(N, t1, t2, tk, k1, k2):
    h = Fr(T, N)
    T1, T2, TK = Fr(str(t1)), Fr(str(t2)), Fr(tk)
    a = np.array([4.0 if t * h < T1 else (-4.0 if t * h < T2 else 4.0) for t in range(N)])
    k = np.array([k1 if t * h < TK else k2 for t in range(N)])
    return a, k


def grad(u, h, a, k):
    """dJ/du_t / h = k_t x_t + p_{t+1}; p_t = p_{t+1} + h (x_t - a_t + k_t u_t), p_N = -3 + x_N."""
    N = len(u)
    x = np.concatenate([[0.0], np.cumsum(h * u)])
    inc = h * (x[:N] - a + k * u)
    p = np.empty(N + 1)
    p[N] = -3.0 + x[N]
    p[:N] = p[N] + np.cumsum(inc[::-1])[::-1]
    return k * x[:N] + p[1:], x


def hess(F, N, h, k):
    """d^2 J / du_i du_j = h^2 [h (N - 1 - max) + phi2 + k_max (1 - delta_ij)], derived by hand."""
    H = np.empty((len(F), len(F)))
    for i, a_ in enumerate(F):
        for j, b_ in enumerate(F):
            m = max(a_, b_)
            H[i, j] = h * h * (h * (N - 1 - m) + 1.0 + (k[m] if a_ != b_ else 0.0))
    return H


def kkt_points(N, a, k, c1, c2):
    h = T / N
    out = []
    for m1 in range(c1 - W, c1 + W + 1):
        for m2 in range(c2 - W, c2 + W + 1):
            for f1 in (False, True):
                for f2 in (False, True):
                    u = np.ones(N)
                    u[m1:m2] = -1.0
                    F = ([m1] if f1 else []) + ([m2] if f2 else [])
                    if F:
                        u[F] = 0.0
                        g, _ = grad(u, h, a, k)
                        uF = np.linalg.solve(hess(F, N, h, k), -h * g[F])
                        if np.any(np.abs(uF) >= 1 - 1e-12):
                            continue
                        u[F] = uF
                    s, x = grad(u, h, a, k)
                    tol = 1e-9
                    bad = np.any((u == 1.0) & (s > tol)) or np.any((u == -1.0) & (s < -tol))
                    if bad:
                        continue
                    J = h * np.sum((x[:N] - a) ** 2 / 2 + k * x[:N] * u) - 3 * x[N] + x[N] ** 2 / 2
                    viol = max(np.max(np.where(u == 1.0, np.maximum(s, 0), 0)),
                               np.max(np.where(u == -1.0, np.maximum(-s, 0), 0)),
                               np.max(np.abs(s[F])) if F else 0.0)
                    out.append(dict(s1=m1, s2=m2, frac=F, u_s1=float(u[m1]), u_s2=float(u[m2]), J=float(J),
                                    kkt_viol=float(viol)))
    return out


def main():
    sweep = json.load(open(os.path.join(KLOG, "sweep.json")))
    old = json.load(open(os.path.join(KLOG, "pre_revision", "sweep_r2.json")))
    recs = []
    for (t1, t2), tag in CFG.items():
        r1 = {json.loads(l)["N"]: json.loads(l) for l in open(os.path.join(R1LOG, f"sweep_{tag}.log"))}
        rows = [r for r in sweep if r.get("kappa1") == 1.0 and r.get("t1") == t1 and r.get("t2") == t2]
        for r in rows:
            N = r["N"]
            h = T / N
            a, k = stage_data(N, t1, t2, r["tk"], -1.0, 0.0)
            pts = kkt_points(N, a, k, r["s1"], r["s2"])
            match = [p for p in pts if p["s1"] == r["s1"] and p["s2"] == r["s2"] and sorted(p["frac"]) == sorted(r["frac"])]
            assert len(match) == 1, (t1, N, pts)
            p = match[0]
            br = r["break_minus_s1"]
            assert r1[N]["break_minus_s1"] == br and r1[N]["s1"] == p["s1"], (t1, N)
            fr1 = p["s1"] in p["frac"]
            corr = br * h - (h * (1 + p["u_s1"]) / 2 if fr1 else 0.0)
            r2form = br * h - (h * (1 - p["u_s1"]) / 2 if fr1 else 0.0)
            th_c = p["s1"] * h + (h * (1 + p["u_s1"]) / 2 if fr1 else 0.0)
            th_o = p["s1"] * h + (h * (1 - p["u_s1"]) / 2 if fr1 else 0.0)
            o = [q for q in old if q.get("kappa1") == 1.0 and q.get("t1") == t1 and q.get("N") == N][0]
            rec = dict(cfg=[t1, t2], N=N, n_kkt_in_window=len(pts), other_J=[q["J"] - p["J"] for q in pts if q is not p],
                       s1=p["s1"], s2=p["s2"], frac=p["frac"], s1_frac=fr1, s2_frac=p["s2"] in p["frac"],
                       u_s1=p["u_s1"], u_s1_r1referee=r1[N]["v"][0] if r1[N]["frac"] and r1[N]["frac"][0] == p["s1"] else None,
                       kkt_viol=p["kkt_viol"], break_minus_s1=br, corrected=corr, round2_formula=r2form,
                       logged_new=r["break_time_minus_theta1"], logged_old=o["break_time_minus_theta1"],
                       dev_new=corr - r["break_time_minus_theta1"], dev_old=r2form - o["break_time_minus_theta1"],
                       u_s1_logged=r["u_s1"], theta1_corr=th_c, theta1_r2=th_o)
            print(json.dumps(rec), flush=True)
            recs.append(rec)
    json.dump(recs, open(os.path.join(HERE, "logs", "phase3.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
