"""Float screening of stage-wise calibration families for COPS catmix (the
trapezoidal transcription), in the reduced projective form of catmix_trap.py,
at a given control vector (default: the chattering optimum from the COPS
logs; option 'smooth' uses the smooth saddle KKT point saved by
catmix_trap.py).

Families, phi_i(theta) = q_i (theta - thbar_i) + P_i (theta - thbar_i)^2 / 2,
with q the discrete costates:
  A   affine, P_i = 0;
  Q   maximal quadratic-model recursion (1-D analogue of Lemma 10 of
      extension-n2.md, with a margin eps), backward from the terminal stage;
      if it breaks (m <= 0) the stage is recorded and the recursion restarts
      from P = 0 there (the family is then still defined, and the break stage
      is expected to fail).
Stage residuals rho_i(theta, u) = L(theta, u) + phi_i(F(theta, u)) - phi_{i-1}(theta)
are minimized over theta in [0, 1] and u in [0, 1] by a grid (dense near the
trajectory) plus local refinement; loss_i = rho_i(zbar) - min.  All float.
Usage: python3 catmix_calib.py N [chatter|smooth] [eps] [band]
(band: restrict theta to |theta - thbar| <= band; default the full range [0, 1])
"""
import json
import sys
import time

import numpy as np
from scipy.optimize import minimize

import catmix_trap as C


def second_partials(R, th, u, e=1e-5):
    """F, L second partials by central differences of the analytic first partials."""
    def fp(t, v):
        F, Ft, Fu, L, Lt, Lu, _, _ = R._an(t, v)
        return np.array([Ft, Fu, Lt, Lu])
    dt = (fp(th + e, u) - fp(th - e, u)) / (2 * e)
    du = (fp(th, u + e) - fp(th, u - e)) / (2 * e)
    F, Ft, Fu, L, Lt, Lu, Tt, Tu = R._an(th, u)
    return dict(F=F, Ft=Ft, Fu=Fu, Lt=Lt, Lu=Lu, Ftt=dt[0], Ftu=du[0], Fuu=du[1],
                Ltt=dt[2], Ltu=du[2], Luu=du[3])


def term_partials(R, th, u, e=1e-5):
    def tp(t, v):
        out = R._an(t, v)
        return np.array([out[6], out[7]])
    dt = (tp(th + e, u) - tp(th - e, u)) / (2 * e)
    du = (tp(th, u + e) - tp(th, u - e)) / (2 * e)
    out = R._an(th, u)
    return dict(Tt=out[6], Tu=out[7], Ttt=dt[0], Ttu=du[0], Tuu=du[1])


def costates(R, u, th):
    N = R.N
    q = np.zeros(N)
    out = R._an(th[N - 1], u[N])
    q[N - 1] = out[6]
    for i in range(N - 1, 0, -1):
        F, Ft, Fu, L, Lt, Lu, _, _ = R._an(th[i - 1], u[i])
        q[i - 1] = Lt + q[i] * Ft
    return q


def status_of(v, g, tol=1e-9):
    if v <= tol:
        return "lo"
    if v >= 1 - tol:
        return "hi"
    return "free"


def maximal_recursion(R, u, th, q, eps):
    N = R.N
    P = np.zeros(N)
    breaks = []
    # terminal stage N: rho = T - phi_{N-1}
    tp = term_partials(R, th[N - 1], u[N])
    st = status_of(u[N], tp["Tu"])
    m = (2 * abs(tp["Tu"]) + tp["Tuu"]) if st != "free" else tp["Tuu"]
    if m > 0:
        P[N - 1] = tp["Ttt"] - tp["Ttu"] ** 2 / m - eps
    else:
        breaks.append(N)
        P[N - 1] = 0.0
    for i in range(N - 1, 0, -1):
        sp_ = second_partials(R, th[i - 1], u[i])
        Lt_tt = sp_["Ltt"] + q[i] * sp_["Ftt"]
        Lt_tu = sp_["Ltu"] + q[i] * sp_["Ftu"]
        Lt_uu = sp_["Luu"] + q[i] * sp_["Fuu"]
        sig = sp_["Lu"] + q[i] * sp_["Fu"]
        r_tu = Lt_tu + P[i] * sp_["Ft"] * sp_["Fu"]
        r_uu = Lt_uu + P[i] * sp_["Fu"] ** 2
        st = status_of(u[i], sig)
        # feasible omega range length: vertex -> 1 (u in [0,1]); interior -> both signs
        m = (2 * abs(sig) / 1.0 + r_uu) if st != "free" else r_uu
        if m > 0:
            P[i - 1] = Lt_tt + P[i] * sp_["Ft"] ** 2 - r_tu ** 2 / m - eps
        else:
            breaks.append(i)
            P[i - 1] = 0.0
    return P, breaks


def stage_losses(R, u, th, q, P, band=None):
    N = R.N
    losses = np.zeros(N + 1)
    # theta grid: global + dense near trajectory
    base = np.linspace(0, 1, 401)
    uu = np.linspace(0, 1, 201)
    for i in range(1, N + 1):
        tb = th[i - 1]
        offs = np.concatenate([-np.geomspace(1e-7, 0.5, 60), [0.0], np.geomspace(1e-7, 0.5, 60)])
        tg = np.unique(np.clip(np.concatenate([base, tb + offs]), 0, 1))
        tlo, thi = 0.0, 1.0
        if band is not None:
            tlo, thi = max(0.0, tb - band), min(1.0, tb + band)
            tg = tg[(tg >= tlo) & (tg <= thi)]
        ug = np.unique(np.concatenate([uu, [u[i]]]))
        TT, UU = np.meshgrid(tg, ug, indexing="ij")
        if i < N:
            F, Lc = R.step(TT, UU)
            rho = Lc + q[i] * (F - th[i]) + 0.5 * P[i] * (F - th[i]) ** 2 \
                - q[i - 1] * (TT - tb) - 0.5 * P[i - 1] * (TT - tb) ** 2
            F0, L0 = R.step(tb, u[i])
            rho0 = L0 + q[i] * (F0 - th[i]) + 0.5 * P[i] * (F0 - th[i]) ** 2
            def fun(z):
                Fz, Lz = R.step(z[0], z[1])
                return (Lz + q[i] * (Fz - th[i]) + 0.5 * P[i] * (Fz - th[i]) ** 2
                        - q[i - 1] * (z[0] - tb) - 0.5 * P[i - 1] * (z[0] - tb) ** 2)
        else:
            Tv = R.term(TT, UU)
            rho = Tv - q[N - 1] * (TT - tb) - 0.5 * P[N - 1] * (TT - tb) ** 2
            rho0 = R.term(tb, u[N])
            def fun(z):
                return R.term(z[0], z[1]) - q[N - 1] * (z[0] - tb) - 0.5 * P[N - 1] * (z[0] - tb) ** 2
        k = np.argmin(rho)
        best = rho.flat[k]
        z0 = np.array([TT.flat[k], UU.flat[k]])
        r = minimize(fun, z0, method="L-BFGS-B", bounds=[(tlo, thi), (0, 1)],
                     options=dict(ftol=1e-18, gtol=1e-16, maxiter=200))
        best = min(best, r.fun)
        losses[i] = rho0 - best
    # initial stage: phi_0(h u0 / 2) over u0 in [0, 1] (linear + quadratic in u0)
    ug = np.linspace(0, 1, 2001)
    tg = R.h / 2 * ug
    v = q[0] * (tg - th[0]) + 0.5 * P[0] * (tg - th[0]) ** 2
    losses[0] = 0.0 - v.min()
    return losses


def main():
    N = int(sys.argv[1])
    which = sys.argv[2] if len(sys.argv) > 2 else "chatter"
    eps = float(sys.argv[3]) if len(sys.argv) > 3 else 1e-10
    band = float(sys.argv[4]) if len(sys.argv) > 4 else None
    R = C.Red(N)
    if which == "chatter":
        u = np.load(C.COPS % N)
    else:
        u = np.load("logs/catmix%d_smooth_u.npy" % N)
    th, cost = R.simulate(u)
    q = costates(R, u, th)
    t0 = time.time()
    res = dict(N=N, point=which, J=float(np.exp(cost) - 1), eps=eps, band=band)
    fams = {"A": np.zeros(N)}
    Pq, breaks = maximal_recursion(R, u, th, q, eps)
    fams["Q"] = Pq
    res["Q_breaks"] = breaks[:50]
    res["Q_n_breaks"] = len(breaks)
    for name, P in fams.items():
        ls = stage_losses(R, u, th, q, P, band)
        tol = 1e-14
        fail = np.where(ls > tol)[0]
        tot = float(np.sum(np.maximum(ls, 0)))
        # classify failing stages by control status and time
        stat = ["lo" if u[i] <= 1e-9 else ("hi" if u[i] >= 1 - 1e-9 else "free") for i in range(N + 1)]
        res[name] = dict(n_fail=int(len(fail)),
                         fail_time_range=[float(fail.min() / N), float(fail.max() / N)] if len(fail) else None,
                         n_fail_free=int(sum(1 for i in fail if stat[i] == "free")),
                         n_fail_lo=int(sum(1 for i in fail if stat[i] == "lo")),
                         n_fail_hi=int(sum(1 for i in fail if stat[i] == "hi")),
                         loss_logJ=tot, loss_J_approx=tot * (np.exp(cost)),
                         max_stage_loss=float(ls.max()),
                         P_range_arc=[float(P[int(0.2 * N):int(0.7 * N)].min()), float(P[int(0.2 * N):int(0.7 * N)].max())])
    res["seconds"] = time.time() - t0
    print(json.dumps(res), flush=True)


if __name__ == "__main__":
    main()
