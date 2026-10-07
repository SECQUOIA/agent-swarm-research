"""Driver for the catmix400/800 recheck. It reuses the previous verifier's rigorous routines
(v_catmix_dp.stage / terminal / Maps, unchanged) and adds only grid construction and a float
forward pass. Validity of the bound does not depend on the grid or on anything computed in
float here: any dyadic grid containing 0 and 1 gives a valid bound.

Grid: base = v_catmix_dp.make_grid(fine_exp) (dyadic, 2^-fine_exp on [0, 13/128], 2^-7 above),
plus bands (lo, hi, exp) at spacing 2^-exp (optionally only on stages s_lo..s_hi), plus windows
of 2K+1 rays at spacing 2^-exp around per-stage trajectories theta_i read from .npy files
(optionally skipped on stages s_lo..s_hi).

Float diagnostics (heuristic only, they do not enter the bound):
- tree_support: pushes the weights of the chord values that the bound depends on forward from
  x_0 and records, per stage, the theta range they occupy (used to design grids);
- forward: the DP policy's controls, evaluated as a primal point (60-digit interval simulation
  with the exact OSIL constants).

usage: recheck_dp.py N fine_exp [--band lo hi exp] [--sband lo hi exp s_lo s_hi]
       [--win K exp traj.npy] [--win-skip s_lo s_hi] [--tree out.json]
       [--save-traj out.npy] [--save-u out.npy]          (--band/--sband/--win repeatable)
"""
import argparse
import json
import time

import mpmath as mp
import numpy as np

import v_catmix_dp as D
import v_catmix_model as vm


def band_rays(lo, hi, e):
    d = 2.0 ** -e
    return np.arange(np.ceil(lo / d) * d, hi, d)


def build_grids(N, fine_exp, bands, wins, sbands=(), win_skip=None):
    base = D.make_grid(fine_exp)
    for lo, hi, e in bands:
        base = np.unique(np.concatenate([base, band_rays(lo, hi, e)]))
    sb = [(band_rays(lo, hi, e), s0, s1) for lo, hi, e, s0, s1 in sbands]
    trajs = [(K, e, np.load(path)) for K, e, path in wins]
    for _, _, t in trajs:
        assert t.shape == (N,)
    out = []
    for i in range(N):
        parts = [base] + [r for r, s0, s1 in sb if s0 <= i <= s1]
        for K, e, t in trajs:
            if win_skip is not None and win_skip[0] <= i <= win_skip[1]:
                continue
            d = 2.0 ** -e
            c = np.round(t[i] / d) * d
            parts.append(np.clip(c + d * np.arange(-K, K + 1), 0.0, 1.0))
        g = np.unique(np.concatenate(parts))
        # every ray must be dyadic with at most 30 fractional bits (so 1 - theta is exact)
        assert g[0] == 0 and g[-1] == 1 and np.all(np.diff(g) > 0)
        assert np.all(g * 2.0 ** 30 == np.round(g * 2.0 ** 30))
        out.append(g)
    return out


def backward(maps, grids, verbose=True):
    N = len(grids)
    t0 = time.time()
    ws = [None] * N
    w, st = D.terminal(maps, grids[N - 1])
    w = np.maximum(w, 0.0)
    ws[N - 1] = w
    tot = dict(pairs=0, refined=0, loss=st["loss"], expand=0)
    for i in range(N - 1, 0, -1):
        w, st = D.stage(maps.stage, grids[i], w, grids[i - 1])
        w = np.maximum(w, 0.0)
        ws[i - 1] = w
        tot["pairs"] += st["pairs"]; tot["refined"] += st["refined"]
        tot["loss"] = max(tot["loss"], st["loss"]); tot["expand"] = max(tot["expand"], st["expand_iters"])
        if verbose and (i % max(1, N // 10) == 0):
            print("  N=%d stage %d: rays %d pairs %d loss %.2e (%.0fs)" %
                  (N, i - 1, len(grids[i - 1]), st["pairs"], st["loss"], time.time() - t0), flush=True)
    w0, st = D.stage(maps.init, grids[0], ws[0], np.array([0.0]))
    tot["loss"] = max(tot["loss"], st["loss"])
    lb = float(D.dn(w0[0] - 1.0))
    return lb, ws, tot, time.time() - t0


def forward(maps, grids, ws, nu=4001):
    """float policy pass: returns controls u_0..u_N and theta_i = theta(y_i), i = 0..N-1."""
    N = len(grids)
    mid = lambda S: {k: [D.mid(c) for c in v] for k, v in S.items()}
    Si, Ss, St = mid(maps.init), mid(maps.stage), mid(maps.term)
    ev = lambda cs, u: cs[0] + u * (cs[1] + u * cs[2])

    def best_u(f):
        u = np.linspace(0, 1, nu)
        k = int(np.argmin(f(u)))
        uu = np.linspace(max(0, u[k] - 2.0 / nu), min(1, u[k] + 2.0 / nu), 4001)
        return float(uu[np.argmin(f(uu))])

    def Wval(i, n1, n2):
        s = n1 + n2
        return s * np.interp(n2 / s, grids[i], ws[i])

    us, ths = [], []
    n = lambda S, u, y: (ev(S["N11"], u) * y[0] + ev(S["N12"], u) * y[1],
                         ev(S["N21"], u) * y[0] + ev(S["N22"], u) * y[1])
    y = (1.0, 0.0)
    u0 = best_u(lambda u: Wval(0, *n(Si, u, y)) / ev(Si["D"], u))
    us.append(u0)
    n1, n2 = n(Si, u0, y)
    y = (n1 / (n1 + n2), n2 / (n1 + n2))
    ths.append(y[1])
    for i in range(1, N):
        ui = best_u(lambda u: Wval(i, *n(Ss, u, y)) / ev(Ss["D"], u))
        us.append(ui)
        n1, n2 = n(Ss, ui, y)
        y = (n1 / (n1 + n2), n2 / (n1 + n2))
        ths.append(y[1])
    uN = best_u(lambda u: (ev(St["T1"], u) * y[0] + ev(St["T2"], u) * y[1]) / ev(St["D"], u))
    us.append(uN)
    return np.array(us), np.array(ths)


def tree_support(maps, grids, ws, nu=2001, tol=1e-12):
    """float diagnostic: the bound is (approximately) a positive combination of the stored chord
    values; push these weights forward from x_0 through the float argmin controls and chord
    splits. Returns per-stage [theta_min, theta_max] of rays with weight > tol, the weight-quantile
    range (1e-9, 1 - 1e-9), and the number of support rays."""
    N = len(grids)
    Ss = {k: [D.mid(c) for c in v] for k, v in maps.stage.items()}
    Si = {k: [D.mid(c) for c in v] for k, v in maps.init.items()}
    ev = lambda cs, u: cs[0] + u * (cs[1] + u * cs[2])

    def argmin_img(S, i, r1, r2):
        u = np.linspace(0, 1, nu)[None, :]
        def val(u):
            n1 = ev(S["N11"], u) * r1[:, None] + ev(S["N12"], u) * r2[:, None]
            n2 = ev(S["N21"], u) * r1[:, None] + ev(S["N22"], u) * r2[:, None]
            s = n1 + n2
            return s * np.interp(n2 / s, grids[i], ws[i]) / ev(S["D"], u), n1, n2
        f, _, _ = val(u)
        k = np.argmin(f, axis=1)
        lo = np.maximum(u[0, k] - 1.0 / (nu - 1), 0)
        uu = lo[:, None] + np.linspace(0, 2.0 / (nu - 1), nu)[None, :]
        uu = np.minimum(uu, 1.0)
        f, n1, n2 = val(uu)
        kk = np.argmin(f, axis=1)
        idx = np.arange(len(r1))
        ub = uu[idx, kk]
        a1, a2 = n1[idx, kk], n2[idx, kk]
        return ub, (a1 + a2) / ev(S["D"], ub), a2 / (a1 + a2)

    def split(i, th, mass):
        g = grids[i]
        k = np.clip(np.searchsorted(g, th, "right") - 1, 0, len(g) - 2)
        lam = (th - g[k]) / (g[k + 1] - g[k])
        c = np.zeros(len(g))
        np.add.at(c, k, mass * (1 - lam))
        np.add.at(c, k + 1, mass * lam)
        return c

    _, rho, th = argmin_img(Si, 0, np.array([1.0]), np.array([0.0]))
    c = split(0, th, rho)
    out = []
    for i in range(N):
        g = grids[i]
        sup = np.where(c > tol)[0]
        cs = np.cumsum(c) / c.sum()
        q0, q1 = np.searchsorted(cs, 1e-9), min(np.searchsorted(cs, 1 - 1e-9), len(g) - 1)
        out.append([i, float(g[sup.min()]), float(g[sup.max()]), float(g[q0]), float(g[q1]), int(len(sup)),
                    float(c.sum())])
        if i == N - 1:
            break
        r2 = g[sup]
        _, rho, th = argmin_img(Ss, i + 1, 1.0 - r2, r2)
        c = split(i + 1, th, c[sup] * rho)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("N", type=int)
    ap.add_argument("fine_exp", type=int)
    ap.add_argument("--band", nargs=3, action="append", default=[])
    ap.add_argument("--sband", nargs=5, action="append", default=[])
    ap.add_argument("--win", nargs=3, action="append", default=[])
    ap.add_argument("--win-skip", nargs=2, type=int, help="no windows on stages s_lo..s_hi")
    ap.add_argument("--save-traj")
    ap.add_argument("--save-u")
    ap.add_argument("--tree")
    a = ap.parse_args()
    bands = [(float(lo), float(hi), int(e)) for lo, hi, e in a.band]
    sbands = [(float(lo), float(hi), int(e), int(s0), int(s1)) for lo, hi, e, s0, s1 in a.sband]
    wins = [(int(K), int(e), p) for K, e, p in a.win]
    t0 = time.time()
    maps = D.Maps(a.N)
    grids = build_grids(a.N, a.fine_exp, bands, wins, sbands, a.win_skip)
    lb, ws, tot, secs = backward(maps, grids)
    res = dict(N=a.N, fine_exp=a.fine_exp, bands=bands, sbands=sbands, wins=wins, win_skip=a.win_skip,
               rays_mean=int(np.mean([len(g) for g in grids])), rays_max=int(max(len(g) for g in grids)),
               dual_bound=lb, dual_bound_repr=repr(lb), max_stage_loss=tot["loss"], pairs=tot["pairs"],
               refined=tot["refined"], max_expand_iters=tot["expand"], seconds_bound=round(secs, 1))
    print(json.dumps(res), flush=True)
    if a.tree:
        tt = time.time()
        tr = tree_support(maps, grids, ws)
        json.dump(tr, open(a.tree, "w"))
        print("tree support written (%.0fs); stages where support leaves [0.0695, 0.0717] while "
              "touching it: %s" % (time.time() - tt, [t[0] for t in tr if (t[1] < 0.0695 < t[2]) or (t[1] < 0.0717 < t[2])][:40]),
              flush=True)
    if a.save_traj or a.save_u:
        u, th = forward(maps, grids, ws)
        u = np.clip(u, 0.0, 1.0)
        m, K, strs = vm.load(a.N)
        J = vm.simulate_iv(strs, [mp.mpf(float(v)) for v in u])
        mp.mp.dps = 60
        Jlo, Jhi = mp.mpf(J.a.a), mp.mpf(J.b.b)
        out = dict(policy_J_lo=mp.nstr(Jlo, 22), policy_J_hi=mp.nstr(Jhi, 22),
                   policy_gap_to_bound=float(Jlo - lb), seconds_total=round(time.time() - t0, 1))
        print(json.dumps(out), flush=True)
        if a.save_traj:
            np.save(a.save_traj, th)
        if a.save_u:
            np.save(a.save_u, u)
