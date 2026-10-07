"""Reviewer's own rigorous homogeneous DP bound for catmix (independent of the authors' code).

Reduction (re-derived in the review): y_0 = Q(u_0) x_0, y_i = M(u_i) y_{i-1} (i = 1..N-1),
x_N = P(u_N)^{-1} y_{N-1}, J = (1,1) x_N - 1, with M = Q adj(P) / det P entrywise >= 0 on [0,1].
V_{N-1}(y) = min_u (1,1) adj(P(u)) y / D(u),  V_{i-1}(y) = min_u V_i(Nm(u) y / D(u)),
J* + 1 = min_{u_0} V_0(Q(u_0) x_0).  V_i concave, positively homogeneous, >= 0 on the quadrant.

Lower bound W_i: chord interpolation of values w_k <= V_i(r_k) on rays r_k = (1-th_k, th_k), i.e.
W(y) = w_k rho(y) + sig_k g_k(y) on cone k, rho = y1 + y2, g_k(y) = (1-th_k) y2 - th_k y1,
sig_k = (w_{k+1}-w_k)/(th_{k+1}-th_k).

Per ray r_j (stage map n(u) = Nm(u) r_j, quadratics): u in [0,1] is cut at the float preimages p of
the cone boundaries (roots of g_k(n(u))), with tiny intervals [p-eps, p+eps]; every interval gets a
cone range [klo, khi] that is VERIFIED rigorously (min g_klo(n(u)) >= 0, max g_{khi+1}(n(u)) <= 0 on
the interval), so f(u) = W(n(u))/D(u) equals one of the rational pieces f_k = p_k/D, k in range.
Each (interval, k) gets either the crude bound (s/D)_min * min(w_k, w_{k+1}) or an exact
Dinkelbach step: t = float min of f_k, then f_k >= t + min(p_k - tD)/D, where the min of the
quadratic p_k - tD over the interval is bounded rigorously.  Interval arithmetic: IEEE double
round-to-nearest + one nextafter step outward per operation.
"""
import json
import sys
import time
from fractions import Fraction as Fr

import numpy as np

import v_catmix_model as vm

INF = np.inf
dn = lambda x: np.nextafter(x, -INF)
up = lambda x: np.nextafter(x, INF)


def fr_iv(F):
    f = float(F)
    G = Fr(f)
    if G == F:
        return (f, f)
    return (float(dn(f)), f) if G > F else (f, float(up(f)))


def iadd(x, y):
    return (dn(x[0] + y[0]), up(x[1] + y[1]))


def isub(x, y):
    return (dn(x[0] - y[1]), up(x[1] - y[0]))


def imul(x, y):
    a, b, c, d = x[0] * y[0], x[0] * y[1], x[1] * y[0], x[1] * y[1]
    return (dn(np.minimum(np.minimum(a, b), np.minimum(c, d))), up(np.maximum(np.maximum(a, b), np.maximum(c, d))))


def ipmul(x, s):
    """interval x times exact point s (arrays, any sign)"""
    a, b = x[0] * s, x[1] * s
    return (dn(np.minimum(a, b)), up(np.maximum(a, b)))


def ineg(x):
    return (-x[1], -x[0])


def mid(x):
    return 0.5 * (x[0] + x[1])


def peval_lo(A, B, C, u):
    """lower bound of A u^2 + B u + C for exact point floats, u >= 0"""
    t1 = np.where(A >= 0, dn(A * dn(u * u)), dn(A * up(u * u)))
    return dn(dn(t1 + dn(B * u)) + C)


def qmin_lb(q, u0, u1):
    """rigorous lower bound of min_{u in [u0,u1]} q(u), q = [q0,q1,q2] intervals, 0 <= u0 <= u1."""
    C, B, A = q[0][0], q[1][0], q[2][0]
    res = np.minimum(peval_lo(A, B, C, u0), peval_lo(A, B, C, u1))
    with np.errstate(all="ignore"):
        v = -B / (2 * A)
        vert = dn(C - up(up(B * B) / dn(4 * A)))
    inside = (A > 0) & (v >= u0 - 1e-12) & (v <= u1 + 1e-12)
    return np.where(inside, np.minimum(res, vert), res)


def qmax_ub(q, u0, u1):
    return -qmin_lb([ineg(c) for c in q], u0, u1)


def fpoly(cm, u):
    return cm[0] + u * (cm[1] + u * cm[2])


def qroots01(c0, c1, c2):
    """float real roots in [0,1] of c0 + c1 u + c2 u^2 (arrays); returns (r1, r2) with nan if absent."""
    with np.errstate(all="ignore"):
        disc = c1 * c1 - 4 * c2 * c0
        sq = np.sqrt(np.where(disc >= 0, disc, np.nan))
        qq = -0.5 * (c1 + np.where(c1 >= 0, 1.0, -1.0) * sq)
        r1 = np.where(c2 != 0, qq / c2, np.nan)
        r2 = np.where(qq != 0, c0 / qq, np.nan)
        lin = (c2 == 0) & (c1 != 0)
        r1 = np.where(lin, -c0 / c1, r1)
        r2 = np.where(lin, np.nan, r2)
    ok = lambda r: np.where((r >= 0) & (r <= 1), r, np.nan)
    return ok(r1), ok(r2)


class Maps:
    def __init__(self, N):
        self.N = N
        m, K, strs = vm.load(N)
        self.K = K
        Pl = vm.polys(K)
        vm.nonneg_checks(Pl)
        iv3 = lambda cs: [tuple(np.float64(v) for v in fr_iv(c)) for c in (cs + [Fr(0)] * 3)[:3]]
        z = [Fr(0)] * 3
        self.stage = dict(N11=iv3(Pl["N11"]), N12=iv3(Pl["N12"]), N21=iv3(Pl["N21"]), N22=iv3(Pl["N22"]),
                          D=iv3(Pl["D"]))
        self.term = dict(T1=iv3(Pl["T1"]), T2=iv3(Pl["T2"]), D=iv3(Pl["D"]))
        self.init = dict(N11=iv3(Pl["Q11"]), N12=iv3(z), N21=iv3(Pl["Q21"]), N22=iv3(z), D=iv3([Fr(1)]))


def ray_polys(S, r1, r2):
    n1 = [iadd(ipmul(S["N11"][d], r1), ipmul(S["N12"][d], r2)) for d in range(3)]
    n2 = [iadd(ipmul(S["N21"][d], r1), ipmul(S["N22"][d], r2)) for d in range(3)]
    return n1, n2


def gk_polys(n1, n2, thk):
    return [isub(ipmul(n2[d], 1.0 - thk), ipmul(n1[d], thk)) for d in range(3)]


def dinkelbach(p, D, u0, u1):
    """rigorous lower bound of min over [u0,u1] of p(u)/D(u) (p, D interval quadratics, D > 0),
    plus the float estimate t."""
    pm = [mid(c) for c in p]
    Dm = [mid(c) for c in D]
    f = lambda u: fpoly(pm, u) / fpoly(Dm, u)
    t = np.minimum(f(u0), f(u1))
    c2 = pm[2] * Dm[1] - pm[1] * Dm[2]
    c1 = 2 * (pm[2] * Dm[0] - pm[0] * Dm[2])
    c0 = pm[1] * Dm[0] - pm[0] * Dm[1]
    for r in qroots01(c0, c1, c2):
        inside = (r > u0) & (r < u1)
        t = np.where(inside, np.minimum(t, f(np.where(inside, r, u0))), t)
    q = [isub(p[d], ipmul(D[d], t)) for d in range(3)]
    m = qmin_lb(q, u0, u1)
    Dlo = qmin_lb(D, u0, u1)
    Dhi = qmax_ub(D, u0, u1)
    assert np.all(Dlo > 0)
    return np.where(m < 0, dn(t + dn(m / Dlo)), dn(t + dn(m / Dhi))), t


def terminal(maps, th):
    S = maps.term
    r1, r2 = 1.0 - th, th
    p = [iadd(ipmul(S["T1"][d], r1), ipmul(S["T2"][d], r2)) for d in range(3)]
    D = [(np.full_like(th, c[0]), np.full_like(th, c[1])) for c in S["D"]]
    z0, z1 = np.zeros_like(th), np.ones_like(th)
    lb, t = dinkelbach(p, D, z0, z1)
    return lb, dict(loss=float(np.max(t - lb)))


EPS = 1e-9


def stage(S, grid, w, th_out, chunk=256):
    """rigorous lower bounds of min_u W(n(u))/D(u) for output rays th_out; W given by (grid, w)."""
    R = len(grid) - 1                     # number of cones
    assert grid[0] == 0 and grid[-1] == 1 and np.all(np.diff(grid) > 0) and np.all(w >= 0)
    dth = np.diff(grid)                   # exact (dyadic grid)
    num = (dn(w[1:] - w[:-1]), up(w[1:] - w[:-1]))
    sig = (dn(num[0] / dth), up(num[1] / dth))
    Dsc = S["D"]
    Dm = [mid(c) for c in Dsc]
    out = np.empty(len(th_out))
    st = dict(intervals=0, pairs=0, refined=0, expand_iters=0, loss=0.0)
    cone = lambda t: np.clip(np.searchsorted(grid, t, "right") - 1, 0, R - 1)
    for c0 in range(0, len(th_out), chunk):
        th = th_out[c0:c0 + chunk]
        m = len(th)
        r1, r2 = 1.0 - th, th
        n1, n2 = ray_polys(S, r1, r2)
        n1m, n2m = [mid(c) for c in n1], [mid(c) for c in n2]
        s = [iadd(n1[d], n2[d]) for d in range(3)]
        sm = [mid(c) for c in s]
        thf = lambda idx, u: fpoly([c[idx] for c in n2m], u) / fpoly([c[idx] for c in sm], u)
        # float theta range: endpoints and roots of the cross polynomial n1 n2' - n2 n1'
        a1, b1, e1 = n1m
        a2, b2, e2 = n2m
        C0, C1, C2 = a1 * b2 - a2 * b1, 2 * (a1 * e2 - a2 * e1), b1 * e2 - b2 * e1
        crs = qroots01(C0, C1, C2)
        idx = np.arange(m)
        cand = [np.zeros(m), np.ones(m)] + [np.where(np.isnan(r), 0.0, r) for r in crs]
        thv = np.stack([thf(idx, u) for u in cand])
        k0, k1 = cone(thv.min(0)), cone(thv.max(0))
        # boundaries strictly inside the range -> float preimages
        nb = k1 - k0
        RI = np.repeat(idx, nb)
        KB = (np.arange(nb.sum()) - np.repeat(np.cumsum(nb) - nb, nb)) + np.repeat(k0, nb) + 1
        tb = grid[KB]
        gc = [(1 - tb) * n2m[d][RI] - tb * n1m[d][RI] for d in range(3)]
        rr = qroots01(gc[0], gc[1], gc[2])
        P_r, P_u = [], []
        for r in rr:
            ok = ~np.isnan(r)
            P_r.append(RI[ok]); P_u.append(r[ok])
        pr, pu = np.concatenate(P_r), np.concatenate(P_u)
        cut_r = np.concatenate([idx, idx, pr, pr])
        cut_u = np.concatenate([np.zeros(m), np.ones(m), np.clip(pu - EPS, 0, 1), np.clip(pu + EPS, 0, 1)])
        o = np.lexsort((cut_u, cut_r))
        cut_r, cut_u = cut_r[o], cut_u[o]
        same = cut_r[1:] == cut_r[:-1]
        IR = cut_r[:-1][same]
        U0, U1 = cut_u[:-1][same], cut_u[1:][same]
        # float cone range per interval (endpoints + interior theta extrema)
        tl = np.minimum(thf(IR, U0), thf(IR, U1))
        th_ = np.maximum(thf(IR, U0), thf(IR, U1))
        for r in crs:
            rI = r[IR]
            ins = ~np.isnan(rI) & (rI > U0) & (rI < U1)
            v = thf(IR, np.where(ins, rI, U0))
            tl = np.where(ins, np.minimum(tl, v), tl)
            th_ = np.where(ins, np.maximum(th_, v), th_)
        klo, khi = cone(tl), cone(th_)
        # rigorous verification (expand until verified)
        n1I = [(c[0][IR], c[1][IR]) for c in n1]
        n2I = [(c[0][IR], c[1][IR]) for c in n2]
        todo = np.ones(len(IR), bool)
        it = 0
        while np.any(todo):
            it += 1
            assert it < 200, "verification does not converge"
            T = np.where(todo)[0]
            n1T = [(c[0][T], c[1][T]) for c in n1I]
            n2T = [(c[0][T], c[1][T]) for c in n2I]
            kl, kh = klo[T], khi[T]
            okl = kl == 0
            gl = gk_polys(n1T, n2T, grid[kl])
            okl |= qmin_lb(gl, U0[T], U1[T]) >= 0
            okh = kh == R - 1
            gh = gk_polys(n1T, n2T, grid[np.minimum(kh + 1, R)])
            okh |= qmax_ub(gh, U0[T], U1[T]) <= 0
            klo[T] = np.where(okl, kl, kl - 1)
            khi[T] = np.where(okh, kh, kh + 1)
            todo[T] = ~(okl & okh)
        st["expand_iters"] = max(st["expand_iters"], it - 1)
        # pairs (interval, cone)
        nk = khi - klo + 1
        PI = np.repeat(np.arange(len(IR)), nk)
        PK = (np.arange(nk.sum()) - np.repeat(np.cumsum(nk) - nk, nk)) + np.repeat(klo, nk)
        PR = IR[PI]
        u0, u1 = U0[PI], U1[PI]
        sP = [(c[0][PR], c[1][PR]) for c in s]
        DP = [(np.full(len(PI), c[0]), np.full(len(PI), c[1])) for c in Dsc]
        smin = np.maximum(qmin_lb(sP, u0, u1), 0.0)
        Dmax = qmax_ub(DP, u0, u1)
        crude = dn(dn(smin / Dmax) * np.minimum(w[PK], w[PK + 1]))
        # float incumbent per ray: f at every cut point
        fcut = np.interp(thf(cut_r, cut_u), grid, w) * fpoly([c[cut_r] for c in sm], cut_u) / fpoly(Dm, cut_u)
        inc = np.full(m, np.inf)
        np.minimum.at(inc, cut_r, fcut)
        ref = crude < inc[PR]
        lbp = crude.copy()
        if np.any(ref):
            F = np.where(ref)[0]
            RF, KF = PR[F], PK[F]
            n1F = [(c[0][RF], c[1][RF]) for c in n1]
            n2F = [(c[0][RF], c[1][RF]) for c in n2]
            gF = gk_polys(n1F, n2F, grid[KF])
            sgF = (sig[0][KF], sig[1][KF])
            pF = [iadd(ipmul((c[0][RF], c[1][RF]), w[KF]), imul(sgF, g)) for c, g in zip(s, gF)]
            DF = [(c[0][F], c[1][F]) for c in DP]
            lbF, tF = dinkelbach(pF, DF, u0[F], u1[F])
            lbp[F] = lbF
            np.minimum.at(inc, RF, tF)
        lbr = np.full(m, np.inf)
        np.minimum.at(lbr, PR, lbp)
        assert np.all(np.isfinite(lbr))
        out[c0:c0 + m] = lbr
        st["intervals"] += len(IR)
        st["pairs"] += len(PI)
        st["refined"] += int(ref.sum())
        st["loss"] = max(st["loss"], float(np.max(inc - lbr)))
    return out, st


def make_grid(fine_exp, F=13 / 128, coarse_exp=7):
    d = 2.0 ** -fine_exp
    g = np.concatenate([np.arange(0, F, d), np.arange(F, 1, 2.0 ** -coarse_exp), [1.0]])
    g = np.unique(g)
    assert np.all(g * 2.0 ** max(fine_exp, coarse_exp) == np.round(g * 2.0 ** max(fine_exp, coarse_exp)))
    return g


def grids_with_window(N, fine_exp, band=None, win=None):
    """per-stage grids: uniform base, optional band (lo, hi, exp), optional window (K, exp) of
    2K+1 rays around the primal trajectory theta_i (authors' controls; any grid is valid)."""
    base = make_grid(fine_exp)
    if band is not None:
        lo, hi, e = band
        d = 2.0 ** -e
        base = np.unique(np.concatenate([base, np.arange(np.ceil(lo / d) * d, hi, d)]))
    if win is None:
        return [base] * N
    Kw, e = win
    d = 2.0 ** -e
    traj = np.load("logs/catmix%d_theta_traj.npy" % N)
    out = []
    for i in range(N):
        c = np.round(traj[i] / d) * d
        wv = c + d * np.arange(-Kw, Kw + 1)
        g = np.unique(np.concatenate([base[(base < wv[0]) | (base > wv[-1])], wv]))
        assert np.all(np.diff(g) > 0) and g[0] == 0 and g[-1] == 1
        out.append(g)
    return out


def run(N, fine_exp, verbose=True, band=None, win=None):
    t0 = time.time()
    maps = Maps(N)
    grids = grids_with_window(N, fine_exp, band, win)
    grid = grids[N - 1]
    w, st = terminal(maps, grid)
    w = np.maximum(w, 0.0)
    tot = dict(pairs=0, refined=0, loss=st["loss"], expand=0)
    for i in range(N - 1, 0, -1):          # compute w for V_{i-1} (grid_{i-1}) from W_i (grid_i)
        w, st = stage(maps.stage, grids[i], w, grids[i - 1])
        grid = grids[i - 1]
        w = np.maximum(w, 0.0)
        tot["pairs"] += st["pairs"]; tot["refined"] += st["refined"]
        tot["loss"] = max(tot["loss"], st["loss"]); tot["expand"] = max(tot["expand"], st["expand_iters"])
        if verbose and (i % max(1, N // 10) == 0):
            print("  N=%d stage %d: pairs %d refined %d loss %.2e (%.0fs)" %
                  (N, i - 1, st["pairs"], st["refined"], st["loss"], time.time() - t0), flush=True)
    w0, st = stage(maps.init, grid, w, np.array([0.0]))
    lb = float(dn(w0[0] - 1.0))
    return dict(N=N, fine_exp=fine_exp, band=band, win=win, rays=int(np.mean([len(g) for g in grids])),
                dual_bound=lb, dual_bound_repr=repr(lb), max_stage_loss=tot["loss"],
                pairs=tot["pairs"], refined=tot["refined"], max_expand_iters=tot["expand"],
                seconds=round(time.time() - t0, 1))


if __name__ == "__main__":
    # usage: v_catmix_dp.py N fine_exp [band_lo band_hi band_exp [win_K win_exp]]
    N, fe = int(sys.argv[1]), int(sys.argv[2])
    band = (float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else None
    win = (int(sys.argv[6]), int(sys.argv[7])) if len(sys.argv) > 7 else None
    print(json.dumps(run(N, fe, band=band, win=win)), flush=True)
