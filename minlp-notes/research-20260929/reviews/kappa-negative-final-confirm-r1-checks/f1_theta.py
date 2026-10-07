"""Independent check (final confirmation, round 1) of note Section 15 Check 4 / Section 16 N2.

Own code; float. Rebuilds, for the 42 strong-drop grids (kappa 1 -> 0; (t1, t2) = (0.5, 1.5), (0.55, 1.45),
(0.45, 1.55); N = 1000 ... 16000), every KKT point of the Euler toy of the shape
    +1 ... +1 | u_{s1} (vertex -1 or fractional) | -1 ... -1 | u_{s2} (vertex +1 or fractional) | +1 ... +1
with s1, s2 within +-W stages of the logged switching stages.  Problem (from the note / ktoy docstring):
    J(u) = h sum_t [ (x_t - a_t)^2/2 + k_t x_t u_t ] + phi1 x_N + phi2 x_N^2/2,  x_{t+1} = x_t + h u_t,
    x_0 = 0, T = 2, a = 4 on [0,t1), -4 on [t1,t2), 4 on [t2,2]; k = -1 on [0,tk), 0 after; phi1 = -3, phi2 = 1.
Gradient derived by hand: dJ/du_s = h k_s x_s + h [ sum_{t=s+1}^{N-1} h (x_t - a_t + k_t u_t) + Phi'(x_N) ].
Hessian on the free stages from gradient differences (J is exactly quadratic).
Read from the author's log only: tk (problem datum) and the logged s1, s2 (window centre and pattern match).
Then theta_1 by the corrected rule t_s1 + h (1 + u)/2 and the round-2 rule t_s1 + h (1 - u)/2 (vertex: t_s1),
and theta_1(N) - theta_1(16000) in stages of grid N for the 20 grids with fractional s1 and N < 16000.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import json
import sys
import time
from fractions import Fraction as Fr

import numpy as np

SWEEP = (_PUBLIC_REPO + '/research-20260929/theory-bangbang/kneg/logs/sweep.json')
OUT = (_PUBLIC_REPO + '/research-20260929/reviews/kappa-negative-final-confirm-r1-checks/logs/f1_theta.json')
T = 2
W = 10
PHI1, PHI2 = -3.0, 1.0


def piecewise(N, pts):
    # value at t h, with t h >= t_i decided exactly (t_i read as its decimal repr)
    v = np.empty(N + 1)
    for t in range(N + 1):
        val = pts[0][1]
        for ti, vi in pts:
            if Fr(repr(ti)) * N <= Fr(t) * T:
                val = vi
        v[t] = val
    return v


def grad(u, h, a, k):
    N = len(u)
    x = np.concatenate([[0.0], np.cumsum(h * u)])
    inc = h * (x[:N] - a[:N] + k[:N] * u)          # direct partial dJ/dx_t, t < N
    tail = np.concatenate([np.cumsum(inc[::-1])[::-1], [0.0]])  # tail[t] = sum_{t' >= t} inc[t']
    phid = PHI1 + PHI2 * x[N]
    # dJ/du_s = h k_s x_s + h (sum_{t > s} inc_t + Phi'(x_N))
    return h * k[:N] * x[:N] + h * (tail[1:N + 1] + phid)


def J(u, h, a, k):
    N = len(u)
    x = np.concatenate([[0.0], np.cumsum(h * u)])
    return h * np.sum((x[:N] - a[:N]) ** 2 / 2 + k[:N] * x[:N] * u) + PHI1 * x[N] + PHI2 * x[N] ** 2 / 2


def kkt_points(N, t1, t2, tk, c1, c2):
    h = T / N
    a = piecewise(N, ((0.0, 4.0), (t1, -4.0), (t2, 4.0)))
    k = piecewise(N, ((0.0, -1.0), (tk, 0.0)))
    found = []
    for s1 in range(c1 - W, c1 + W + 1):
        for s2 in range(c2 - W, c2 + W + 1):
            if s2 <= s1 + 1:
                continue
            for f1 in (False, True):
                for f2 in (False, True):
                    u = np.ones(N)
                    u[s1:s2] = -1.0
                    free = [s for s, f in ((s1, f1), (s2, f2)) if f]
                    if free:
                        u0 = u.copy()
                        u0[free] = 0.0
                        g0 = grad(u0, h, a, k)
                        H = np.empty((len(free), len(free)))
                        for j, s in enumerate(free):
                            e = u0.copy()
                            e[s] = 1.0
                            H[:, j] = (grad(e, h, a, k) - g0)[free]
                        v = np.linalg.solve(H, -g0[free])
                        if np.any(np.abs(v) >= 1 - 1e-12):
                            continue
                        u = u0
                        u[free] = v
                    g = grad(u, h, a, k)
                    tol = 1e-12 * h
                    fixed = np.ones(N, bool)
                    fixed[free] = False
                    up = fixed & (u == 1.0)
                    dn = fixed & (u == -1.0)
                    if np.all(g[up] <= tol) and np.all(g[dn] >= -tol):
                        viol = max([0.0] + [abs(g[s]) / h for s in free])
                        found.append(dict(s1=s1, s2=s2, frac=free, u_s1=float(u[s1]), u_s2=float(u[s2]),
                                          stat_viol=viol, J=float(J(u, h, a, k))))
    return found


def main():
    sweep = json.load(open(SWEEP))
    rows = [r for r in sweep if r.get("kappa1") == 1.0]
    res = []
    t0 = time.time()
    for r in rows:
        pts = kkt_points(r["N"], r["t1"], r["t2"], r["tk"], r["s1"], r["s2"])
        h = T / r["N"]
        match = [p for p in pts if p["s1"] == r["s1"] and p["s2"] == r["s2"] and sorted(p["frac"]) == sorted(r["frac"])]
        rec = dict(t1=r["t1"], t2=r["t2"], N=r["N"], n_kkt=len(pts), kkt=pts, matches_log=len(match) == 1)
        if len(match) == 1:
            p = match[0]
            fr = p["s1"] in p["frac"]
            ts = p["s1"] * h
            rec.update(s1_frac=fr, u_s1=p["u_s1"], du_vs_log=abs(p["u_s1"] - r["u_s1"]),
                       th_corr=ts + h * (1 + p["u_s1"]) / 2 if fr else ts,
                       th_r2=ts + h * (1 - p["u_s1"]) / 2 if fr else ts)
        res.append(rec)
        print(r["t1"], r["N"], len(pts), rec["matches_log"], rec.get("u_s1"), flush=True)
    # Check 4 tallies
    summ = {}
    allr = []
    for (t1, t2) in ((0.5, 1.5), (0.55, 1.45), (0.45, 1.55)):
        rr = [x for x in res if x["t1"] == t1 and x["t2"] == t2]
        ref = [x for x in rr if x["N"] == 16000][0]
        for x in rr:
            if x["N"] < 16000 and x["s1_frac"]:
                hN = T / x["N"]
                allr.append(dict(cfg=[t1, t2], N=x["N"], u_s1=x["u_s1"],
                                 corr=(x["th_corr"] - ref["th_corr"]) / hN,
                                 r2_vs_corr_ref=(x["th_r2"] - ref["th_corr"]) / hN,
                                 r2_vs_own_ref=(x["th_r2"] - ref["th_r2"]) / hN))
        summ[str((t1, t2))] = dict(ref_frac=ref["s1_frac"], ref_u_s1=ref["u_s1"])
    for key in ("corr", "r2_vs_corr_ref", "r2_vs_own_ref"):
        lo = min(allr, key=lambda d: d[key])
        hi = max(allr, key=lambda d: d[key])
        summ[key] = dict(min=lo[key], argmin=[lo["cfg"], lo["N"]], max=hi[key], argmax=[hi["cfg"], hi["N"]])
    summ["n_rows"] = len(allr)
    summ["max_n_kkt"] = max(x["n_kkt"] for x in res)
    summ["all_match_log"] = all(x["matches_log"] for x in res)
    summ["max_du_vs_log"] = max(x["du_vs_log"] for x in res)
    summ["max_stat_viol"] = max(p["stat_viol"] for x in res for p in x["kkt"])
    summ["time_s"] = time.time() - t0
    print(json.dumps(summ, indent=1))
    json.dump(dict(summary=summ, rows=allr, grids=res), open(OUT, "w"), indent=1)


if __name__ == "__main__":
    main()
