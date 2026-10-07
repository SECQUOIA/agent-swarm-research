"""COPS catmix (trapezoid), reduced projective form: quadratic calibrations
with windows of L consecutive stages, at the chattering optimum.

Storage phi_j(theta) = q (theta - thbar) + P (theta - thbar)^2 / 2 only at
window boundaries (q = discrete costate).  For a window with entry offset d
and control offsets omega (each in its feasible interval: one-sided at a
bound, two-sided if interior), the window residual is expanded to second
order (analytic first and second partials, chain rule):
    Phi_W - Phi_W(orbit) = g.omega + [d omega] H [d omega]^T / 2,
g_d = 0 by the costates.  Exactness of the quadratic model over d in R and
omega in the box holds iff H_dd > 0 and min over the box of
    g.omega + omega^T S omega / 2,   S = H_ww - H_wd H_dw / H_dd,
is >= 0.  H_dd decreases with the entry curvature P_in, so the largest
admissible P_in is found by bisection; the recursion runs backward over the
windows (the 1-D, windowed analogue of Lemma 10 of extension-n2.md).
L = 1 is the stage-wise recursion.  Float only; the model is local (d in R,
second order), so this is a screening, not a certificate.
Usage: python3 catmix_windows.py N fixed|adaptive L [L ...]
(adaptive: a window that fails is extended backward, up to 6 stages)
"""
import itertools
import json
import sys

import numpy as np
import sympy as sp

import catmix_trap as C


def analytic2(N):
    th, u = sp.symbols("th u")
    h = sp.Rational(1, N)
    A = sp.Matrix([[-u, 10 * u], [u, -1 - 9 * u]])
    P = sp.eye(2) - h / 2 * A
    Q = sp.eye(2) + h / 2 * A
    yv = sp.Matrix([1 - th, th])
    z = P.inv() * (Q * yv)
    c = z[0] + z[1]
    F = sp.simplify(z[1] / c)
    Lc = sp.log(sp.simplify(c))
    wv = P.inv() * yv
    T = sp.log(sp.simplify(wv[0] + wv[1]))
    out = {}
    for nm, ex in (("F", F), ("L", Lc), ("T", T)):
        out[nm] = sp.lambdify((th, u), [ex, sp.diff(ex, th), sp.diff(ex, u), sp.diff(ex, th, 2),
                                         sp.diff(ex, th, u), sp.diff(ex, u, 2)], "numpy")
    return out


def box_qp_min(g, S, lo, hi):
    """exact min of g.w + w'Sw/2 over the box [lo, hi] (small dimension):
    enumerate faces; on each face solve the stationary system if the face
    Hessian is positive definite; include all vertices."""
    n = len(g)
    best = 0.0  # w = 0 is feasible
    for pattern in itertools.product((0, 1, 2), repeat=n):  # 0 free, 1 lo, 2 hi
        fixed = {k: (lo[k] if p == 1 else hi[k]) for k, p in enumerate(pattern) if p}
        fr = [k for k, p in enumerate(pattern) if p == 0]
        w = np.zeros(n)
        for k, v in fixed.items():
            w[k] = v
        if fr:
            Sff = S[np.ix_(fr, fr)]
            if np.linalg.eigvalsh(Sff)[0] <= 0:
                continue
            rhs = -(g[fr] + S[np.ix_(fr, list(fixed))] @ w[list(fixed)]) if fixed else -g[fr]
            wf = np.linalg.solve(Sff, rhs)
            if np.any(wf < np.array(lo)[fr] - 1e-15) or np.any(wf > np.array(hi)[fr] + 1e-15):
                continue
            w[fr] = wf
        val = g @ w + 0.5 * w @ S @ w
        best = min(best, val)
    return best


def window_model(an, th_in, us, q_out, P_out, terminal):
    """gradient and Hessian of the window objective (without -phi_in) in
    z = (d, omega_1..omega_L); terminal=True: last stage uses T instead of
    L + phi_out."""
    Lw = len(us)
    n = 1 + Lw
    th = th_in
    gth = np.zeros(n)
    gth[0] = 1.0
    Hth = np.zeros((n, n))
    gobj = np.zeros(n)
    Hobj = np.zeros((n, n))
    for k, uk in enumerate(us):
        e = np.zeros(n)
        e[1 + k] = 1.0
        last = terminal and k == Lw - 1
        if last:
            T, Tt, Tu, Ttt, Ttu, Tuu = an["T"](th, uk)
            gobj += Tt * gth + Tu * e
            Hobj += (Tt * Hth + Ttt * np.outer(gth, gth) + Ttu * (np.outer(gth, e) + np.outer(e, gth))
                     + Tuu * np.outer(e, e))
            return gobj, Hobj
        L, Lt, Lu, Ltt, Ltu, Luu = an["L"](th, uk)
        gobj += Lt * gth + Lu * e
        Hobj += (Lt * Hth + Ltt * np.outer(gth, gth) + Ltu * (np.outer(gth, e) + np.outer(e, gth))
                 + Luu * np.outer(e, e))
        F, Ft, Fu, Ftt, Ftu, Fuu = an["F"](th, uk)
        Hth = (Ft * Hth + Ftt * np.outer(gth, gth) + Ftu * (np.outer(gth, e) + np.outer(e, gth))
               + Fuu * np.outer(e, e))
        gth = Ft * gth + Fu * e
        th = F
    gobj += q_out * gth
    Hobj += q_out * Hth + P_out * np.outer(gth, gth)
    return gobj, Hobj


def polish(R, u, iters=30):
    """Newton on grad = 0 over the interior stages of u (active set kept)."""
    u = u.copy()
    free = np.where((u > 1e-9) & (u < 1 - 1e-9))[0]

    def gf(v):
        return R.grad_logJ(v)[1][free]

    for it in range(iters):
        g = gf(u)
        if np.max(np.abs(g)) < 1e-16:
            break
        Hm = np.zeros((len(free), len(free)))
        e = 1e-6
        for jj, j in enumerate(free):
            up, um = u.copy(), u.copy()
            up[j] += e
            um[j] -= e
            Hm[:, jj] = (gf(up) - gf(um)) / (2 * e)
        du = np.linalg.solve((Hm + Hm.T) / 2, -g)
        u[free] += du
        if np.max(np.abs(du)) < 1e-15:
            break
    cost, g = R.grad_logJ(u)
    act = np.setdiff1d(np.arange(len(u)), free)
    sgn_ok = all((u[j] <= 1e-9 and g[j] >= 0) or (u[j] >= 1 - 1e-9 and g[j] <= 0) for j in act)
    return u, float(np.max(np.abs(g[free]))), bool(sgn_ok and np.all((u[free] > 0) & (u[free] < 1))), \
        float(min(g[j] for j in act if u[j] <= 1e-9)) if any(u[j] <= 1e-9 for j in act) else None


def run(N, Lw, eps=0.0, do_polish=True, adaptive=False, Lmax=6):
    R = C.Red(N)
    an = analytic2(N)
    u = np.load(C.COPS % N)
    pol = None
    if do_polish:
        u, gmax, kkt_ok, gmin0 = polish(R, u)
        pol = dict(max_grad_free=gmax, kkt_ok=kkt_ok, min_grad_at_0=gmin0)
    th, cost = R.simulate(u)
    # costates q_i = d(cost-to-go)/d theta_i
    q = np.zeros(N)
    q[N - 1] = an["T"](th[N - 1], u[N])[1]
    for i in range(N - 1, 0, -1):
        L_ = an["L"](th[i - 1], u[i])
        F_ = an["F"](th[i - 1], u[i])
        q[i - 1] = L_[1] + q[i] * F_[1]
    def solve_window(a, b, P_out):
        terminal = (b == N)
        us = [u[i] for i in range(a, b + 1)]
        qo = 0.0 if terminal else q[b]
        Po = 0.0 if terminal else P_out
        g, H = window_model(an, th[a - 1], us, qo, Po, terminal)
        gw = g[1:].copy()
        for kk, uk in enumerate(us):
            if 1e-9 < uk < 1 - 1e-9:
                gw[kk] = 0.0
        lo = [(-uk if uk > 1e-9 else 0.0) for uk in us]
        hi = [((1 - uk) if uk < 1 - 1e-9 else 0.0) for uk in us]

        def ok(Pin):
            Hdd = H[0, 0] - Pin
            if Hdd <= 0:
                return False
            S = H[1:, 1:] - np.outer(H[1:, 0], H[0, 1:]) / Hdd
            return box_qp_min(gw, S, lo, hi) >= -1e-22
        hiP = H[0, 0] - 1e-300
        loP = H[0, 0] - 1.0
        k = 0
        while not ok(loP) and k < 60:
            loP = H[0, 0] - 2 * (H[0, 0] - loP)
            k += 1
        if not ok(loP):
            return None, abs(g[0] - q[a - 1])
        for _ in range(80):
            mid = 0.5 * (loP + hiP)
            if ok(mid):
                loP = mid
            else:
                hiP = mid
        return loP - eps, abs(g[0] - q[a - 1])

    breaks = []
    Pval = {}
    windows = []
    gd_max = 0.0
    b = N
    P_out = 0.0
    while b >= 1:
        done = False
        for Lc in range(Lw, (Lmax if adaptive else Lw) + 1):
            a = max(1, b - Lc + 1)
            Pin, gd = solve_window(a, b, P_out)
            gd_max = max(gd_max, gd)
            if Pin is not None:
                done = True
                break
            if a == 1:
                break
        if not done:
            a = max(1, b - Lw + 1)
            breaks.append(a)
            Pin = 0.0
            Pval[a - 1] = None
        else:
            Pval[a - 1] = Pin
        windows.append((a, b))
        P_out = Pin
        b = a - 1
    arc = [Pval[k] for k in Pval if Pval[k] is not None and 0.2 * N <= k <= 0.7 * N]
    lens = [bb - aa + 1 for (aa, bb) in windows]
    long_w = [(aa, bb) for (aa, bb) in windows if bb - aa + 1 > Lw]
    return dict(N=N, L=Lw, adaptive=adaptive, n_windows=len(windows), max_window=max(lens),
                long_windows=long_w[:10], n_breaks=len(breaks), breaks=sorted(breaks)[:40],
                break_times=[b / N for b in sorted(breaks)[:40]],
                P_arc_range=[float(min(arc)), float(max(arc))] if arc else None,
                max_grad_d_mismatch=gd_max, J=float(np.exp(cost) - 1), polish=pol)


if __name__ == "__main__":
    N = int(sys.argv[1])
    adaptive = sys.argv[2] == "adaptive"
    for Lw in [int(v) for v in sys.argv[3:]]:
        print(json.dumps(run(N, Lw, adaptive=adaptive)), flush=True)
