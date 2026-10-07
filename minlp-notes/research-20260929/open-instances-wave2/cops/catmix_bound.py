"""Rigorous dual bound for catmix100/200/400/800 by a homogeneous (projective) DP.

Model (catmix_model.py): P(u_{i+1}) x_{i+1} = Q(u_i) x_i, x_0 = (1,0), objective
c^T x_N - 1 with c = (1,1).  With y_i := Q(u_i) x_i = P(u_{i+1}) x_{i+1}:
  y_0 = Q(u_0) x_0,  y_i = M(u_i) y_{i-1} (i=1..N-1),  x_N = P(u_N)^{-1} y_{N-1},
  M(u) = Q(u) P(u)^{-1} = Nm(u) / D(u),  Nm = Q adj(P) (quadratic), D = det P.
Value functions V_{N-1}(y) = min_u c^T P(u)^{-1} y,  V_{i-1}(y) = min_u V_i(M(u) y),
J* + 1 = min_{u_0} V_0(Q(u_0) x_0).  Each V_i is a minimum of linear functions of y,
hence concave and positively homogeneous; M(u) >= 0 and P(u)^{-1} >= 0 entrywise
(checked below), so every y_i lies in the closed positive quadrant.

Lower bounds: W_i is the chord interpolation of lower-bound values w_k at grid rays
r_k (sorted by angle, covering the quadrant).  For concave homogeneous V_i and
w_k <= V_i(r_k), superadditivity gives V_i(s r_k + t r_{k+1}) >= s w_k + t w_{k+1} =
W_i(.) for s, t >= 0.  Then W_{i-1}(r_j) := rigorous lower bound of
min_{u in [0,1]} W_i(M(u) r_j) <= V_{i-1}(r_j).  The inner minimization is a
vectorized interval branch and bound over u (mean-value forms of the rational
functions l_k^T Nm(u) r_j / D(u) on each chord piece l_k).
All arithmetic on rigorous paths is outward-rounded interval arithmetic (ivx.py).
"""
import json
import sys
import time

import numpy as np

import catmix_model as cmx
import ivx as I

KMAX = 8
DEBUG = False
DEBUG_ROUNDS = ()


class Maps:
    def __init__(self, K):
        a, b, c, ep, em = (I.const(K[k]) for k in ("a", "b", "c", "ep", "em"))
        self.flt = {k: float(K[k]) for k in K}
        m = I.mul
        ab, ac = m(a, b), m(a, c)
        zero = I.pt(0.0)
        one = I.pt(1.0)
        # stage map: Nm = Q adj(P), D = det P
        self.stage = dict(
            N11=[ep, I.sub(c, m(a, ep)), I.sub(ab, ac)],
            N12=[zero, I.add(b, b), zero],
            N21=[zero, m(a, I.add(ep, em)), zero],
            N22=[em, I.sub(m(a, em), c), I.sub(ab, ac)],
            D=[ep, I.add(m(a, ep), c), I.sub(ac, ab)])
        # terminal map: adj(P) / det P
        self.term = dict(N11=[ep, c], N12=[zero, b], N21=[zero, a], N22=[one, a],
                         D=[ep, I.add(m(a, ep), c), I.sub(ac, ab)])
        # initial map: Q (D = 1)
        self.init = dict(N11=[one, I.neg(a)], N12=[zero, b], N21=[zero, a], N22=[em, I.neg(c)], D=[one])

    def check_positive(self):
        """entries of Nm and D nonnegative / positive on [0,1] (rigorous, 64 subintervals)."""
        for name in ("stage", "term", "init"):
            S = getattr(self, name)
            g = np.linspace(0, 1, 65)
            U = (g[:-1], g[1:])
            for key in ("N11", "N12", "N21", "N22"):
                cf = S[key]
                if np.all(cf[0][0] == 0) and np.all(cf[0][1] == 0) and all(np.all(x[0] >= 0) for x in cf[1:]):
                    continue  # zero constant term, nonnegative coefficients: >= 0 for u >= 0
                assert np.all(I.poly(cf, U)[0] > 0), (name, key)
            assert np.all(I.poly(S["D"], U)[0] > 0), (name, "D")
        return True


def deriv(coefs):
    out = []
    for k in range(1, len(coefs)):
        out.append(I.mul(coefs[k], I.pt(float(k))))
    return out if out else [I.pt(0.0)]


def ray_coefs(S, p, q):
    """coefficients of n1(u) = p N11 + q N12, n2(u) = p N21 + q N22 (p, q >= 0 exact floats)."""
    L = max(len(S["N11"]), len(S["N12"]), len(S["N21"]), len(S["N22"]))

    def get(key, k):
        return S[key][k] if k < len(S[key]) else I.pt(0.0)
    n1 = [I.add(I.scale(get("N11", k), p), I.scale(get("N12", k), q)) for k in range(L)]
    n2 = [I.add(I.scale(get("N21", k), p), I.scale(get("N22", k), q)) for k in range(L)]
    return n1, n2


def float_eval_map(S, p, q, u):
    def fp(coefs):
        r = 0.0
        for cf in reversed(coefs):
            r = r * u + 0.5 * (cf[0] + cf[1])
        return r
    D = fp(S["D"])
    z1 = (p * fp(S["N11"]) + q * fp(S["N12"])) / D
    z2 = (p * fp(S["N21"]) + q * fp(S["N22"])) / D
    return z1, z2


def sparse_table(v, op):
    sp = [v.copy()]
    k = 1
    while 2 * k <= len(v):
        prev = sp[-1]
        sp.append(op(prev[:-k], prev[k:]))
        k *= 2
    return sp


def range_query(sp, lo, hi, op):
    """op-reduction of v[lo..hi] inclusive."""
    n = hi - lo + 1
    lv = np.floor(np.log2(n)).astype(int)
    out = np.empty(len(lo))
    for L in np.unique(lv):
        s = lv == L
        tab = sp[L]
        out[s] = op(tab[lo[s]], tab[hi[s] - (1 << L) + 1])
    return out


class Chord:
    """chord interpolation data for one stage: rays (p_k, q_k), values w_k >= 0."""

    def __init__(self, p, q, w):
        self.p, self.q = p, q
        self.w = np.maximum(w, 0.0)  # V >= 0, so max(w, 0) stays a valid lower bound
        self.th = q / (p + q)
        assert np.all(np.diff(self.th) > 0) and self.th[0] == 0 and self.th[-1] == 1
        K = len(p)
        # rays are exactly normalized (p + q == 1, dyadic theta): cancellation-free chord
        # coefficients  W(z) = alpha z1 + beta z2,  alpha = w_k - sig_k th_k,
        # beta = w_k + sig_k (1 - th_k),  sig_k = (w_{k+1} - w_k) / (th_{k+1} - th_k)
        assert np.all(p + q == 1.0)
        th = I.pt(q)
        W0, W1 = I.pt(self.w[:-1]), I.pt(self.w[1:])
        dth = I.sub(I.take(th, slice(1, None)), I.take(th, slice(0, -1)))
        assert np.all(dth[0] > 0)
        sig = I.div_pos(I.sub(W1, W0), dth)
        self.alpha = I.sub(W0, I.mul(sig, I.take(th, slice(0, -1))))
        self.beta = I.add(W0, I.mul(sig, I.pt(p[:-1])))
        self.sig = sig
        self.sp_wmax = sparse_table(self.w, np.maximum)
        self.sp_slo = sparse_table(sig[0], np.minimum)
        self.sp_shi = sparse_table(sig[1], np.maximum)
        self.maxpq = np.max(I.add(I.pt(p), I.pt(q))[1])
        # sparse table for range minimum of w
        self.sp = [self.w.copy()]
        k = 1
        while 2 * k <= K:
            prev = self.sp[-1]
            self.sp.append(np.minimum(prev[:-k], prev[k:]))
            k *= 2

    def range_max_w(self, lo, hi):
        return range_query(self.sp_wmax, lo, hi, np.maximum)

    def range_sig(self, lo, hi):
        return range_query(self.sp_slo, lo, hi, np.minimum), range_query(self.sp_shi, lo, hi, np.maximum)

    def range_min(self, lo, hi):
        """min of w[lo..hi] inclusive (arrays)."""
        n = hi - lo + 1
        lv = np.floor(np.log2(n)).astype(int)
        out = np.empty(len(lo))
        for L in np.unique(lv):
            s = lv == L
            tab = self.sp[L]
            out[s] = np.minimum(tab[lo[s]], tab[hi[s] - (1 << L) + 1])
        return out

    def float_W(self, z1, z2):
        s = z1 + z2
        return s * np.interp(z2 / s, self.th, self.w)


def stage_lb(S, rays_p, rays_q, target, tol, S0=8, max_rounds=80, umin=1e-14):
    """rigorous lower bounds of min_{u in [0,1]} T(Nm(u) r_j / D(u)) for all rays j.
    target: Chord (next-stage W) or the string 'sum' (T(z) = z1 + z2, terminal stage)."""
    n = len(rays_p)
    Dc = S["D"]
    dD = deriv(Dc)
    # --- incumbents from float sampling ---
    inc = np.full(n, np.inf)

    def fval(uu, idx):
        z1, z2 = float_eval_map(S, rays_p[idx], rays_q[idx], uu)
        return (z1 + z2) if target == "sum" else target.float_W(z1, z2)
    allidx = np.arange(n)
    best_u = np.zeros(n)
    for uu in np.linspace(0, 1, 33):
        v = fval(np.full(n, uu), allidx)
        better = v < inc
        inc = np.where(better, v, inc)
        best_u = np.where(better, uu, best_u)
    lo = np.clip(best_u - 1 / 32, 0, 1)
    hi = np.clip(best_u + 1 / 32, 0, 1)
    gr = (np.sqrt(5) - 1) / 2
    x1 = hi - gr * (hi - lo); x2 = lo + gr * (hi - lo)
    f1 = fval(x1, allidx); f2 = fval(x2, allidx)
    for _ in range(50):
        m_ = f1 < f2
        hi = np.where(m_, x2, hi); lo = np.where(m_, lo, x1)
        x2n = np.where(m_, x1, lo + gr * (hi - lo)); x1n = np.where(m_, hi - gr * (hi - lo), x2)
        x1, x2 = x1n, x2n
        f1 = fval(x1, allidx); f2 = fval(x2, allidx)
    inc = np.minimum(inc, np.minimum(f1, f2))
    # --- branch and bound ---
    J = np.repeat(allidx, S0)
    g = np.linspace(0, 1, S0 + 1)
    ul = np.tile(g[:-1], n)
    uh = np.tile(g[1:], n)
    ul[ul < 0] = 0
    leafmin = np.full(n, np.inf)
    stats = dict(rounds=0, evals=0, forced_leaves=0)
    for rnd in range(max_rounds):
        if len(J) == 0:
            break
        stats["rounds"] = rnd + 1
        if DEBUG: print("round", rnd, "active", len(J), flush=True)
        stats["evals"] += len(J)
        p, q = rays_p[J], rays_q[J]
        n1c, n2c = ray_coefs(S, p, q)
        U = (ul, uh)
        um = 0.5 * (ul + uh)
        Um = I.pt(um)
        n1U, n2U, DU = I.poly(n1c, U), I.poly(n2c, U), I.poly(Dc, U)
        assert np.all(DU[0] > 0)
        z1 = I.div_pos(n1U, DU)
        z2 = I.div_pos(n2U, DU)
        # incumbent update at midpoints (float)
        v = fval(um, J)
        np.minimum.at(inc, J, v)
        if target == "sum":
            # single linear functional (1,1)
            LB = mv_lb([n1c[k] for k in range(len(n1c))], [n2c[k] for k in range(len(n2c))],
                       I.pt(np.ones(len(J))), I.pt(np.ones(len(J))), Dc, dD, ul, uh, um)
        else:
            LB = chord_lb(S, n1c, n2c, ul, uh, um, z1, z2, target, Dc, dD)
        if DEBUG and rnd in DEBUG_ROUNDS:
            for t in range(0, len(J), max(1, len(J) // 8)):
                print("   J", J[t], "U", ul[t], uh[t], "LB", repr(LB[t]), "inc", repr(inc[J[t]]), "diff", inc[J[t]] - LB[t])
        done = LB >= inc[J] - tol
        if DEBUG and target != "sum":
            print("  rnd %d active %d done %d width %.2e" % (rnd, len(J), int(np.sum(done)), np.median(uh - ul)), flush=True)
        tiny = (uh - ul) < umin
        leaf = done | tiny
        stats["forced_leaves"] += int(np.sum(tiny & ~done))
        np.minimum.at(leafmin, J[leaf], LB[leaf])
        keep = ~leaf
        J, ul, uh, um = J[keep], ul[keep], uh[keep], um[keep]
        J = np.repeat(J, 2)
        ul, uh = np.stack([ul, um], 1).ravel(), np.stack([um, uh], 1).ravel()
    else:
        # rounds exhausted: remaining intervals become leaves with their last LB
        raise RuntimeError("max rounds reached with %d active intervals" % len(J))
    assert np.all(np.isfinite(leafmin))
    stats["max_loss_vs_incumbent"] = float(np.max(inc - leafmin))
    return leafmin, inc, stats


def candidates(z1, z2, ch):
    th_lo = np.clip(I.dn(z2[0] / I.up(z1[1] + z2[0])), 0, 1)
    th_hi = np.clip(I.up(z2[1] / I.dn(z1[0] + z2[1])), 0, 1)
    nc = len(ch.th) - 1
    kl = np.clip(np.searchsorted(ch.th, th_lo, "right") - 1, 0, nc - 1)
    kh = np.clip(np.searchsorted(ch.th, th_hi, "right") - 1, 0, nc - 1)
    return np.maximum(kl - 1, 0), np.minimum(kh + 1, nc - 1)


def few_lb(n1c, n2c, ul, uh, um, z1, z2, klo, ncand, ch, Dc, dD):
    """min over candidate cones (that may meet the z-box) of the mean-value lower bound
    of the chord functional l_k(z(u)) over [ul, uh]."""
    nc = len(ch.th) - 1
    n = len(ul)
    pi_list, k_list = [], []
    idx = np.arange(n)
    for off in range(KMAX):
        k = np.minimum(klo + off, nc - 1)
        cr_k = I.sub(I.mul(I.pt(ch.p[k]), z2), I.mul(I.pt(ch.q[k]), z1))
        cr_k1 = I.sub(I.mul(I.pt(ch.p[k + 1]), z2), I.mul(I.pt(ch.q[k + 1]), z1))
        valid = (off < ncand) & (cr_k[1] >= 0) & (cr_k1[0] <= 0)
        pi_list.append(idx[valid])
        k_list.append(k[valid])
    PI = np.concatenate(pi_list)
    KK = np.concatenate(k_list)
    n1f = [I.take(cf, PI) for cf in n1c]
    n2f = [I.take(cf, PI) for cf in n2c]
    val = mv_lb(n1f, n2f, I.take(ch.alpha, KK), I.take(ch.beta, KK), Dc, dD, ul[PI], uh[PI], um[PI])
    best = np.full(n, np.inf)
    np.minimum.at(best, PI, val)
    assert np.all(np.isfinite(best)), "no candidate cone"
    return best


def zbox(n1c, n2c, Dc, ul, uh):
    U = (ul, uh)
    n1U, n2U, DU = I.poly(n1c, U), I.poly(n2c, U), I.poly(Dc, U)
    assert np.all(DU[0] > 0)
    return I.div_pos(n1U, DU), I.div_pos(n2U, DU)


def chord_lb(S, n1c, n2c, ul, uh, um, z1, z2, ch, Dc, dD):
    """rigorous lower bound over [ul, uh] of f(u) = W(z(u)), W = chord interpolation."""
    klo, khi = candidates(z1, z2, ch)
    ncand = khi - klo + 1
    LB = np.full(len(ul), -np.inf)
    few = ncand <= KMAX
    sel = lambda cfs, ids: [I.take(cf, ids) for cf in cfs]
    if np.any(few):
        idf = np.where(few)[0]
        LB[idf] = few_lb(sel(n1c, idf), sel(n2c, idf), ul[idf], uh[idf], um[idf],
                         I.take(z1, idf), I.take(z2, idf), klo[idf], ncand[idf], ch, Dc, dD)
    if np.any(~few):
        # f = S(u) PL(Theta(u)), S = (n1+n2)/D, Theta = n2/(n1+n2); f is Lipschitz with
        # f' in S' * [min w, max w] + S * [min sig, max sig] * Theta' (a.e.), so the
        # mean-value bound holds; point values are evaluated rigorously on their cones.
        idm = np.where(~few)[0]
        a1, a2 = sel(n1c, idm), sel(n2c, idm)
        l, h, m = ul[idm], uh[idm], um[idm]
        U = (l, h)
        sc = [I.add(x, y) for x, y in zip(a1, a2)]
        n2U, sU, DU = I.poly(a2, U), I.poly(sc, U), I.poly(Dc, U)
        dn2U, dsU, dDU = I.poly(deriv(a2), U), I.poly(deriv(sc), U), I.poly(dD, U)
        SU = I.div_pos(sU, DU)
        dS = I.div_pos(I.sub(I.mul(dsU, DU), I.mul(sU, dDU)), I.mul(DU, DU))
        dT = I.div_pos(I.sub(I.mul(dn2U, sU), I.mul(n2U, dsU)), I.mul(sU, sU))
        kl, kh = klo[idm], khi[idm]
        nc = len(ch.th) - 1
        wr = (ch.range_min(kl, np.minimum(kh + 1, nc)), ch.range_max_w(kl, np.minimum(kh + 1, nc)))
        sg = ch.range_sig(kl, kh)
        fp = I.add(I.mul(dS, wr), I.mul(I.mul(SU, sg), dT))
        incr = fp[0] >= 0
        decr = fp[1] <= 0
        pts = np.where(incr, l, np.where(decr, h, m))
        pz1, pz2 = zbox(a1, a2, Dc, pts, pts)
        pk_lo, pk_hi = candidates(pz1, pz2, ch)
        pn = pk_hi - pk_lo + 1
        assert np.all(pn <= KMAX)
        pv = few_lb(a1, a2, pts, pts, pts, pz1, pz2, pk_lo, pn, ch, Dc, dD)
        r = I.up(np.maximum(h - m, m - l))
        mag = np.maximum(np.abs(fp[0]), np.abs(fp[1]))
        LB[idm] = np.where(incr | decr, pv, I.dn(pv - I.up(mag * r)))
    return LB


def mv_lb(n1c, n2c, alpha, beta, Dc, dD, ul, uh, um):
    """rigorous lower bound over [ul, uh] of f(u) = (alpha n1(u) + beta n2(u)) / D(u).
    Uses the natural extension, monotonicity (sign of f' on U), and the second-order
    Taylor bound f(u) >= f(um) + f'(um) d + f''(U) d^2 / 2, d = u - um."""
    gc = [I.add(I.mul(alpha, n1c[k]), I.mul(beta, n2c[k])) for k in range(len(n1c))]
    dg = deriv(gc)
    d2g = deriv(dg)
    d2D = deriv(dD)
    U = (ul, uh)
    gU, DU, dgU, dDU = I.poly(gc, U), I.poly(Dc, U), I.poly(dg, U), I.poly(dD, U)
    d2gU, d2DU = I.poly(d2g, U), I.poly(d2D, U)
    fU = I.div_pos(gU, DU)
    num1 = I.sub(I.mul(dgU, DU), I.mul(gU, dDU))
    fp = I.div_pos(num1, I.mul(DU, DU))
    # f'' = [(g'' D - g D'') D - 2 D' (g' D - g D')] / D^3
    num2 = I.sub(I.mul(I.sub(I.mul(d2gU, DU), I.mul(gU, d2DU)), DU), I.mul(I.mul(I.pt(2.0), dDU), num1))
    fpp = I.div_pos(num2, I.mul(I.mul(DU, DU), DU))

    def at(u):
        P = I.pt(u)
        g0, D0 = I.poly(gc, P), I.poly(Dc, P)
        f0 = I.div_pos(g0, D0)
        f1 = I.div_pos(I.sub(I.mul(I.poly(dg, P), D0), I.mul(g0, I.poly(dD, P))), I.mul(D0, D0))
        return f0, f1
    fm, gm = at(um)
    r = I.up(np.maximum(uh - um, um - ul))
    lb = fU[0]
    # second-order Taylor bound: for d in [0, r], f(um + d) >= fm + gm.lo d + h d^2 and
    # for d = -e, e in [0, r], f(um - e) >= fm - gm.hi e + h e^2, where h <= f''(U)/2.
    h = I.dn(0.5 * fpp[0])
    tay = np.full(len(ul), np.inf)
    for gs in (gm[0], -gm[1]):
        e_val = I.add(I.mul(I.pt(gs), I.pt(r)), I.mul(I.pt(h), I.mul(I.pt(r), I.pt(r))))[0]
        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            stat = I.dn(-I.up(I.up(gs * gs) / I.dn(4.0 * h)))      # global min of convex quadratic
        beyond = I.dn(-gs) >= I.up(2.0 * h * r)                     # stationary point at d >= r
        v = np.where(h > 0,
                     np.where(gs >= 0, 0.0, np.where(beyond, e_val, stat)),
                     np.minimum(0.0, e_val))                        # concave or linear: endpoints
        tay = np.minimum(tay, v)
    lb = np.maximum(lb, I.dn(fm[0] + tay))
    # monotone cases: exact endpoint values
    inc_ = fp[0] >= 0
    dec_ = fp[1] <= 0
    if np.any(inc_):
        lb = np.where(inc_, np.maximum(lb, at(ul)[0][0]), lb)
    if np.any(dec_):
        lb = np.where(dec_, np.maximum(lb, at(uh)[0][0]), lb)
    return lb


def compose_check(maps, u):
    """interval composition of the maps used by the DP along controls u:
    J(u) = (1,1) P(u_N)^{-1} M(u_{N-1}) ... M(u_1) Q(u_0) x_0 - 1."""
    def apply(S, y, uu):
        U = I.pt(np.array([uu]))
        n1c, n2c = ray_coefs(S, np.array([1.0]), np.array([0.0]))
        m1c, m2c = ray_coefs(S, np.array([0.0]), np.array([1.0]))
        D = I.poly(S["D"], U)
        c11, c21 = I.poly(n1c, U), I.poly(n2c, U)   # first column
        c12, c22 = I.poly(m1c, U), I.poly(m2c, U)   # second column
        z1 = I.div_pos(I.add(I.mul(c11, y[0]), I.mul(c12, y[1])), D)
        z2 = I.div_pos(I.add(I.mul(c21, y[0]), I.mul(c22, y[1])), D)
        return (z1, z2)
    N = len(u) - 1
    y = apply(maps.init, (I.pt(np.array([1.0])), I.pt(np.array([0.0]))), u[0])
    for i in range(1, N):
        y = apply(maps.stage, y, u[i])
    x = apply(maps.term, y, u[N])
    J = I.sub(I.add(x[0], x[1]), I.pt(np.array([1.0])))
    return float(J[0][0]), float(J[1][0])


# ---------------- grids ----------------
BAND = None  # optional (lo, hi, spacing): extra uniform rays in a band (e.g. around the singular arc)


def make_grids(N, K, ustar, dcoarse, K_win, d_win):
    """per-stage ray grids: uniform on [0, 0.1], coarse on [0.1, 1], plus a window of
    rays around the reference trajectory transported backward by the reference map."""
    fm = cmx.FloatModel(K, N)
    a, b, c, ep, em = fm.a, fm.b, fm.c, fm.ep, fm.em
    J, g, xs = fm.J_grad(ustar)
    ys = np.array([[(1 - a * ustar[i]) * xs[i, 0] + b * ustar[i] * xs[i, 1],
                    a * ustar[i] * xs[i, 0] + (em - c * ustar[i]) * xs[i, 1]] for i in range(N)])
    thstar = ys[:, 1] / ys.sum(1)
    base = np.unique(np.concatenate([np.arange(0, 0.1, dcoarse), np.linspace(0.1, 1, 181)]))
    if BAND is not None:
        base = np.unique(np.concatenate([base, np.arange(BAND[0], BAND[1], BAND[2])]))

    def pre(uu, th):
        P = np.array([[1 + a * uu, -b * uu], [-a * uu, ep + c * uu]])
        Q = np.array([[1 - a * uu, b * uu], [a * uu, em - c * uu]])
        y = P @ np.linalg.solve(Q, np.stack([1 - th, th]))
        return y[1] / (y[0] + y[1])
    grids = [None] * N
    win = thstar[N - 1] + d_win * np.arange(-K_win, K_win + 1) if K_win > 0 else np.array([])
    for i in range(N - 1, -1, -1):
        w_ = win[(win > 0) & (win < 1)]
        if len(w_):
            b_ = base[(base < w_.min()) | (base > w_.max())]   # the window replaces base rays in its span
        else:
            b_ = base
        th = np.unique(np.round(np.concatenate([b_, w_]) * 2.0 ** 40) / 2.0 ** 40)  # dyadic: 1 - th exact
        th = th[np.concatenate([[True], np.diff(th) > 1e-11])]
        th[0], th[-1] = 0.0, 1.0
        grids[i] = th
        if i > 0 and len(win):
            win = pre(ustar[i], win)
    return grids, thstar, J


def rays_of(th):
    p = 1.0 - th
    q = th.copy()
    return p, q


def run(N, dcoarse, K_win, d_win, tol=1e-14, ufile=None, verbose=True):
    t0 = time.time()
    m, K = cmx.extract(N)
    maps = Maps(K)
    maps.check_positive()
    ustar = np.load(ufile or "logs/catmix%d_u.npy" % N)
    grids, thstar, Jref = make_grids(N, K, ustar, dcoarse, K_win, d_win)
    Jmap = compose_check(maps, ustar)
    assert Jmap[0] <= Jref + 1e-12 and Jref - 1e-12 <= Jmap[1], (Jmap, Jref)
    p, q = rays_of(grids[N - 1])
    w, inc, st = stage_lb(maps.term, p, q, "sum", tol)
    chord = Chord(p, q, w)
    total_evals = st["evals"]
    worst_loss = st["max_loss_vs_incumbent"]
    sizes = [len(p)]
    for i in range(N - 1, 0, -1):
        p, q = rays_of(grids[i - 1])
        w, inc, st = stage_lb(maps.stage, p, q, chord, tol)
        chord = Chord(p, q, w)
        total_evals += st["evals"]
        worst_loss = max(worst_loss, st["max_loss_vs_incumbent"])
        sizes.append(len(p))
        if verbose and i % max(1, N // 10) == 0:
            print("  stage %d rays %d rounds %d evals %d loss %.2e (%.0fs)" %
                  (i - 1, len(p), st["rounds"], st["evals"], st["max_loss_vs_incumbent"], time.time() - t0),
                  flush=True)
    # initial stage: single ray x_0 = (1, 0)
    w0, inc0, st = stage_lb(maps.init, np.array([1.0]), np.array([0.0]), chord, tol)
    lb = I.dn(w0[0] - 1.0)
    out = dict(N=N, dcoarse=dcoarse, K_win=K_win, d_win=d_win, tol=tol,
               dual_bound=float(lb), reference_J_float=float(Jref), gap_to_reference=float(Jref - lb),
               avg_rays=float(np.mean(sizes)), total_interval_evals=int(total_evals),
               max_stage_loss_vs_float_incumbent=worst_loss, seconds=time.time() - t0)
    return out


if __name__ == "__main__":
    N = int(sys.argv[1])
    dcoarse, K_win, d_win = float(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
    if len(sys.argv) > 5:
        BAND = tuple(float(v) for v in sys.argv[5:8])
    out = run(N, dcoarse, K_win, d_win)
    out["band"] = BAND
    print(json.dumps(out, indent=1))
    tag = "logs/catmix%d_bound_%g_%d_%g%s.json" % (N, dcoarse, K_win, d_win, "_band%g_%g_%g" % BAND if BAND else "")
    with open(tag, "w") as f:
        json.dump(out, f, indent=1)
