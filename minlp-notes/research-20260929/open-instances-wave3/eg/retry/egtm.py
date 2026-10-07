"""Rigorous per-box models of the eg_* rows (outward rounding throughout).

For a box X = [lo, hi] (instance coordinates; integer coordinates either fixed, lo = hi,
or relaxed to an integer interval) with float centre c and radius r >= |x - c|:

  * natural enclosure  g_k(X) in [nat_lo, nat_hi]  (each Gaussian term is separable,
    so each term's exponent range is exact up to rounding);
  * second-order Taylor model with a third-order remainder.  For one term
        T = a exp(E),  E(c + d) = E0 + L(d) + Q(d),
        L = sum_i v_i d_i,  v_i = 2 gamma_i s_i t_i,  t_i = mu_i + s_i c_i,
        Q = sum_i gamma_i s_i^2 d_i^2 <= 0,
    exp(E0 + L + Q) = e^E0 (1 + L + Q + L^2/2 + R) with
        R = L Q + Q^2/2 + u^3 e^(theta u)/6,  u = L + Q,  theta in (0, 1),
        |R| <= l q + q^2/2 + (l + q)^3 e^l / 6,   l = sum |v_i| r_i,  q = sum |gamma_i| s_i^2 r_i^2.
    Summing over the 97 terms (signed, so cancellation between terms is kept):
        g_k(c + d) = G_k + grad_k . d + d' H_k d / 2 + rho_k,   |rho_k| <= P_k,
        G_k = sum w_m + lin.c,  grad_k = sum w_m v_m + lin,
        H_k = sum w_m v_m v_m' + diag(2 gamma s^2) sum w_m,   w_m = a_m e^E0_m.
    The quadratic part is bounded by constants over the box (diagonal: min(H_ii, 0) r_i^2 / 2;
    off-diagonal: -|H_ij| r_i r_j), which gives affine minorants / majorants
        g_k(x) >= aL_k + beta_k . (x - c),   g_k(x) <= aU_k + beta_k . (x - c)   on X.

G, grad, H are interval enclosures (numpy NI, one ulp outward per operation; sums over
the 97 terms by the float sum with the bound (n+2) u sum|.|).  exp is kan_iv.iexp_pt_fast
(table + Taylor + remainder; no libm result is trusted).
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "kan"))
import kan_iv as K  # noqa: E402
from kan_iv import NI, dn, up  # noqa: E402

import egdata  # noqa: E402

INF = np.inf
U = 2.0 ** -52


def ni_arr(q, shape=None):
    a = np.array([K.frac_iv(v) for v in np.ravel(np.array(q, dtype=object))])
    lo, hi = a[:, 0], a[:, 1]
    if shape is not None:
        lo, hi = lo.reshape(shape), hi.reshape(shape)
    return NI(lo, hi)


def isq(T):
    """exact-range square of an interval, outward rounded."""
    lo2 = T.lo * T.lo
    hi2 = T.hi * T.hi
    lo = np.where(T.lo >= 0, lo2, np.where(T.hi <= 0, hi2, 0.0))
    return NI(np.maximum(dn(lo), 0.0), up(np.maximum(lo2, hi2)))


def isum(W, axis=-1):
    """outward-rounded sum over an axis (float sum error <= (n-1) u sum|.|; we use (n+2) u)."""
    n = W.lo.shape[axis]
    e = (n + 2) * U
    slo = W.lo.sum(axis=axis)
    shi = W.hi.sum(axis=axis)
    elo = e * np.abs(W.lo).sum(axis=axis)
    ehi = e * np.abs(W.hi).sum(axis=axis)
    return NI(dn(dn(slo - elo) - 1e-300), up(up(shi + ehi) + 1e-300))


def usum(x, axis=-1):
    """upper bound of the exact sum of nonnegative floats."""
    n = x.shape[axis]
    s = x.sum(axis=axis)
    return up(up(s * (1.0 + (n + 2) * U)) + 1e-300)


def amag(X):
    return np.maximum(np.abs(X.lo), np.abs(X.hi))


def iexp_up(x):
    """upper bound of e^x (inf where x > 700)."""
    return np.where(x > 700.0, INF, K.iexp_pt_fast(np.minimum(x, 700.0)).hi)


class Model:
    def __init__(self, name):
        D = egdata.Data(name)
        self.D = D
        self.name = name
        d, R, Mt = D.d, D.R, D.Mt
        self.d, self.R, self.Mt = d, R, Mt
        self.A = ni_arr(D.qa, (R, Mt))
        self.MU = ni_arr(D.qmu, (R, Mt, d))
        self.GA = ni_arr(D.qga, (R, d))
        self.S = ni_arr(D.qs, (d,))
        self.LIN = ni_arr(D.qlin, (R, d))
        self.TWOGS = (self.GA * 2.0) * self.S[None, :]                     # 2 gamma s     (R, d)
        self.TWOGS2 = self.TWOGS * self.S[None, :]                         # 2 gamma s^2   (R, d)
        self.GS2abs = up(amag(self.TWOGS2) * 0.5)                          # |gamma| s^2 (upper)
        self.isint = D.isint.copy()
        self.lo0 = np.array([K.frac_iv(v)[0] for v in D.qlb])
        self.hi0 = np.array([K.frac_iv(v)[1] for v in D.qub])
        self.lo_in = np.array([K.frac_iv(v)[1] for v in D.qlb])
        self.hi_in = np.array([K.frac_iv(v)[0] for v in D.qub])
        # outer box [lo0, hi0] for bounding; inner box [lo_in, hi_in] for primal points
        obj = D.objrows
        self.obj = obj
        self.nobj = int(obj.sum())
        self.c_lo = np.array([K.frac_iv(v)[0] for v in D.qc[:24]])
        self.c_hi = np.array([K.frac_iv(v)[1] for v in D.qc[:24]])
        # side rows glo <= g <= ghi: relaxed (outer) bounds for pruning, inner bounds for primal checks
        self.side = np.arange(24, 28)
        self.glo = np.array([K.frac_iv(v)[0] if v is not None else -INF for v in D.qglo[24:]])
        self.ghi = np.array([K.frac_iv(v)[1] if v is not None else INF for v in D.qghi[24:]])
        self.glo_in = np.array([K.frac_iv(v)[1] if v is not None else -INF for v in D.qglo[24:]])
        self.ghi_in = np.array([K.frac_iv(v)[0] if v is not None else INF for v in D.qghi[24:]])

    # ------------------------------------------------------------------ natural enclosure
    def natural(self, lo, hi):
        """enclosure of every g_k over each box: NI (N, R)."""
        X = NI(lo[:, None, None, :], hi[:, None, None, :])
        T = self.MU[None] + self.S[None, None, None, :] * X                 # (N, R, M, d)
        E = isum(self.GA[None, :, None, :] * isq(T), axis=-1)              # (N, R, M)
        ex = NI(K.iexp_pt_fast(E.lo).lo, K.iexp_pt_fast(E.hi).hi)
        g = isum(self.A[None] * ex, axis=-1)
        Xl = NI(lo[:, None, :], hi[:, None, :])
        g = g + isum(self.LIN[None] * Xl, axis=-1)
        return g

    def point(self, x):
        """enclosure of g_k at float points x (N, d)."""
        return self.natural(x, x)

    # ------------------------------------------------------------------ Taylor model
    def taylor(self, lo, hi, dims=None):
        """affine minorant/majorant data for every row over each box.

        returns c (N,d), r (N,d), beta (N,R,d) floats, aL, aU (N,R) floats and the
        diagnostics P (N,R), quadlow (N,R), H magnitude (N,R,d,d)."""
        N, d = lo.shape
        c = 0.5 * (lo + hi)
        c = np.minimum(np.maximum(c, lo), hi)
        r = np.maximum(up(hi - c), up(c - lo))
        r = np.where(hi == lo, 0.0, r)
        if dims is None:
            dims = [i for i in range(d) if np.any(r[:, i] > 0)]
        Cc = NI(c[:, None, None, :])
        T = self.MU[None] + self.S[None, None, None, :] * Cc                # (N, R, M, d)
        E0 = isum(self.GA[None, :, None, :] * isq(T), axis=-1)            # (N, R, M)
        ex = NI(K.iexp_pt_fast(E0.lo).lo, K.iexp_pt_fast(E0.hi).hi)
        W = self.A[None] * ex                                              # (N, R, M)
        V = self.TWOGS[None, :, None, :] * T                               # (N, R, M, d)
        G = isum(W, axis=-1) + isum(self.LIN[None] * NI(c[:, None, :]), axis=-1)
        SW = isum(W, axis=-1)
        WV = {}
        grad_lo = np.zeros((N, self.R, d)); grad_hi = np.zeros((N, self.R, d))
        for i in range(d):
            WV[i] = W * V[..., i]
            gi = isum(WV[i], axis=-1) + self.LIN[None, :, i]
            grad_lo[..., i], grad_hi[..., i] = gi.lo, gi.hi
        # Hessian magnitude bounds over the active dims
        Hlo = np.zeros((N, self.R, d, d)); Hhi = np.zeros((N, self.R, d, d))
        for a_, i in enumerate(dims):
            for j in dims[a_:]:
                h = isum(WV[i] * V[..., j], axis=-1)
                if i == j:
                    h = h + self.TWOGS2[None, :, i] * SW
                Hlo[..., i, j], Hhi[..., i, j] = h.lo, h.hi
                Hlo[..., j, i], Hhi[..., j, i] = h.lo, h.hi
        Hmag = np.maximum(np.abs(Hlo), np.abs(Hhi))
        # remainder
        rr = r[:, None, None, :]
        Vabs = amag(V)
        ell = usum(up(Vabs * rr), axis=-1)                                 # (N, R, M)
        qq = usum(up(self.GS2abs[None, :, None, :] * up(rr * rr)), axis=-1)
        uu = up(ell + qq)
        e6 = up(iexp_up(ell) / 6.0)
        R3 = up(up(up(ell * qq) + up(0.5 * up(qq * qq))) + up(up(up(uu * uu) * uu) * e6))
        Wabs = amag(W)
        P = usum(up(Wabs * R3), axis=-1)                                   # (N, R)
        if dims and os.environ.get("EG_ORDER") != "2":
            # third-order alternative (egfast docstring, item 4), all in interval arithmetic:
            # |C3| <= (1/6) sum_ijk |T_ijk| r_i r_j r_k + sum_ij |U_ij| r_i r_j^2, plus R4
            e24 = up(iexp_up(ell) / 24.0)
            u2 = up(uu * uu)
            R4 = up(up(up(up(0.5 * up(qq * qq)) + up(0.5 * up(up(ell * ell) * qq))) +
                       up(up(0.5 * up(ell * up(qq * qq))) + up(up(qq * up(qq * qq)) / 6.0))) +
                    up(up(u2 * u2) * e24))
            P4 = usum(up(Wabs * R4), axis=-1)
            cub = np.zeros((N, self.R))
            for a_, i in enumerate(dims):
                for b_, j in enumerate(dims[a_:]):
                    WVV = WV[i] * V[..., j]
                    for k in dims[a_ + b_:]:
                        T3 = amag(isum(WVV * V[..., k], axis=-1))
                        mult = 6.0 if (i < j < k) else (1.0 if i == j == k else 3.0)
                        cub = up(cub + up(mult * up(T3 * up(up(r[:, None, i] * r[:, None, j]) * r[:, None, k]))))
            cub = up(cub / 6.0)
            g1abs = np.zeros((N, self.R))
            q2 = np.zeros((N, self.R))
            for i in dims:
                g1abs = up(g1abs + up(amag(isum(WV[i], axis=-1)) * r[:, None, i]))
                q2 = up(q2 + up(self.GS2abs[None, :, i] * up(r[:, None, i] * r[:, None, i])))
            cubU = up(g1abs * q2)
            P = np.minimum(P, up(up(cub + cubU) + P4))
        # quadratic part bounds
        r2 = up(r[:, :, None] * r[:, None, :])                             # (N, d, d)
        diag_neg = np.zeros((N, self.R)); diag_pos = np.zeros((N, self.R))
        offd = np.zeros((N, self.R))
        for i in dims:
            diag_neg = up(diag_neg + up(np.maximum(-Hlo[..., i, i], 0.0) * r2[:, None, i, i]))
            diag_pos = up(diag_pos + up(np.maximum(Hhi[..., i, i], 0.0) * r2[:, None, i, i]))
        for a_, i in enumerate(dims):
            for j in dims[a_ + 1:]:
                offd = up(offd + up(Hmag[..., i, j] * r2[:, None, i, j]))
        quadlow = -up(up(0.5 * diag_neg) + offd)                            # <= d'Hd/2
        quadhigh = up(up(0.5 * diag_pos) + offd)
        beta = 0.5 * (grad_lo + grad_hi)
        rad = np.maximum(up(grad_hi - beta), up(beta - grad_lo))
        lin_err = usum(up(rad * r[:, None, :]), axis=-1)
        aL = dn(dn(dn(G.lo - P) + quadlow) - lin_err)
        aU = up(up(up(G.hi + P) + quadhigh) + lin_err)
        return dict(c=c, r=r, beta=beta, aL=aL, aU=aU, P=P, quadlow=quadlow, Hmag=Hmag, G=G,
                    Wabs=Wabs, Vabs=Vabs, ell=ell, qq=qq)


# ---------------------------------------------------------------------------------------
# Fast variant: interval arithmetic only up to the term values w_m = a_m e^E0_m and the
# shifted centres t_mi; the moment sums are then formed in plain floating point (einsum)
# with an explicit a-posteriori error bound:
#   |w t_i t_j - w~ t~_i t~_j| <= dw tau^2 + 2 |w~| tau dtau,   |w t_i - w~ t~_i| <= dw tau + |w~| dtau,
#   float summation of M products (any order, with or without FMA): <= (M + 3) u sum |w~| tau^k,
# where w = w~ +- dw, t_i = t~_i +- dt_i, tau_m = max_i (|t~_mi| + dt_mi), dtau_m = max_i dt_mi.
# Constant factors (2 gamma s etc.) carry relative errors below 10 u; every derived
# quantity is given a relative slack of 1e-12 (> 4000 u), and every computed nonnegative
# bound is inflated by (1 + 1e-12) plus 1e-300 against underflow.
# ---------------------------------------------------------------------------------------
SL = 1e-12          # relative slack
UR = 2.0 ** -53     # unit roundoff


def infl(x):
    return x * (1.0 + SL) + 1e-300


class FastModel(Model):
    def __init__(self, name):
        super().__init__(name)
        mid = lambda X: 0.5 * (X.lo + X.hi)
        self.k1 = mid(self.TWOGS)                      # 2 gamma s        (R, d)
        self.kd = mid(self.TWOGS2)                     # 2 gamma s^2      (R, d)
        self.lin_m = mid(self.LIN)                     # (R, d)
        self.hgs2 = 0.5 * np.abs(self.kd)              # |gamma| s^2      (R, d)

    def taylor(self, lo, hi, dims=None):
        N, d = lo.shape
        R, Mt = self.R, self.Mt
        c = 0.5 * (lo + hi)
        c = np.minimum(np.maximum(c, lo), hi)
        r = np.maximum(up(hi - c), up(c - lo))
        r = np.where(hi == lo, 0.0, r)
        if dims is None:
            dims = [i for i in range(d) if np.any(r[:, i] > 0)]
        dims = list(dims)
        n = len(dims)
        SC = self.S[None, :] * NI(c)                                          # (N, d) small
        T = self.MU[None] + SC[:, None, None, :]                              # (N, R, M, d)
        E0 = isum(self.GA[None, :, None, :] * isq(T), axis=-1)               # (N, R, M)
        ex = NI(K.iexp_pt_fast(E0.lo).lo, K.iexp_pt_fast(E0.hi).hi)
        W = self.A[None] * ex
        wm = 0.5 * (W.lo + W.hi)
        dw = np.maximum(up(W.hi - wm), up(wm - W.lo))
        aw = np.abs(wm)
        gam = (Mt + 3) * UR
        S0 = wm.sum(-1)
        e0 = infl((dw + gam * aw).sum(-1))
        G = S0 + c @ self.lin_m.T
        eG = infl(e0 + SL * (np.abs(c) @ np.abs(self.lin_m).T + np.abs(G)))
        beta = np.zeros((N, R, d))
        rad = np.zeros((N, R, d))
        Hm = np.zeros((N, R, d, d))     # midpoint Hessian
        He = np.zeros((N, R, d, d))     # error bound
        P = np.zeros((N, R))
        Vabs = np.zeros((N, R, Mt, d))
        ell = np.zeros((N, R, Mt)); qq = np.zeros((N, R, Mt))
        if n:
            tm = 0.5 * (T.lo[..., dims] + T.hi[..., dims])                   # (N, R, M, n)
            dt = np.maximum(up(T.hi[..., dims] - tm), up(tm - T.lo[..., dims]))
            tau = (np.abs(tm) + dt).max(-1)
            dtau = dt.max(-1)
            S1 = np.einsum("nrm,nrmi->nri", wm, tm)
            S2 = np.einsum("nrm,nrmi,nrmj->nrij", wm, tm, tm)
            e1 = infl((dw * tau + aw * dtau + gam * aw * tau).sum(-1))
            e2 = infl((dw * tau * tau + 2.0 * aw * tau * dtau + gam * aw * tau * tau).sum(-1))
            k1 = self.k1[:, dims]                                              # (R, n)
            kd = self.kd[:, dims]
            g1 = k1[None] * S1 + self.lin_m[None][..., dims]
            eg1 = infl(np.abs(k1)[None] * e1[..., None] + SL * (np.abs(k1[None] * S1) + np.abs(self.lin_m[None][..., dims]) + np.abs(g1)))
            k2 = k1[:, :, None] * k1[:, None, :]                               # (R, n, n)
            H = k2[None] * S2
            eH = np.abs(k2)[None] * e2[..., None, None] + SL * np.abs(H)
            ii = np.arange(n)
            Hd = kd[None] * S0[..., None]
            H[..., ii, ii] += Hd
            eH[..., ii, ii] += np.abs(kd)[None] * e0[..., None] + SL * np.abs(Hd)
            eH = infl(eH + SL * np.abs(H))
            beta[..., dims] = g1
            rad[..., dims] = eg1
            for a_, i in enumerate(dims):
                for b_, j in enumerate(dims):
                    Hm[..., i, j] = H[..., a_, b_]
                    He[..., i, j] = eH[..., a_, b_]
            # remainder
            rn = r[:, dims]                                                    # (N, n)
            va = infl(np.abs(k1)[None, :, None, :] * (np.abs(tm) + dt))        # |v_mi| upper
            ell = infl((va * rn[:, None, None, :]).sum(-1))
            qq = infl((self.hgs2[:, dims][None] * (rn * rn)[:, None, :]).sum(-1))[..., None] * np.ones((1, 1, Mt))
            uu = ell + qq
            el = K.iexp_pt_fast(np.minimum(ell, 700.0)).hi
            R3 = infl(ell * qq + 0.5 * qq * qq + uu * uu * uu * el / 6.0)
            P = infl(((aw + dw) * R3).sum(-1))
            Vabs[..., dims] = va
        # quadratic part and affine models
        Hlo, Hhi = Hm - He, Hm + He
        Hmag = np.maximum(np.abs(Hlo), np.abs(Hhi))
        r2 = r[:, :, None] * r[:, None, :]
        dneg = (np.maximum(-np.diagonal(Hlo, axis1=2, axis2=3), 0.0) * (r * r)[:, None, :]).sum(-1)
        dpos = (np.maximum(np.diagonal(Hhi, axis1=2, axis2=3), 0.0) * (r * r)[:, None, :]).sum(-1)
        offd = 0.5 * ((Hmag * r2[:, None]).sum((-1, -2)) - (np.diagonal(Hmag, axis1=2, axis2=3) * (r * r)[:, None, :]).sum(-1))
        offd = np.maximum(offd, 0.0)
        # offd computed as (sum_all - diag)/2: bound its rounding by the full sum
        offd = infl(offd + SL * (Hmag * r2[:, None]).sum((-1, -2)))
        quadlow = -infl(0.5 * dneg + offd)
        quadhigh = infl(0.5 * dpos + offd)
        lin_err = infl((rad * r[:, None, :]).sum(-1))
        tot = np.abs(G) + eG + P + np.abs(quadlow) + np.abs(quadhigh) + lin_err
        aL = G - eG - P + quadlow - lin_err - SL * tot - 1e-300
        aU = G + eG + P + quadhigh + lin_err + SL * tot + 1e-300
        return dict(c=c, r=r, beta=beta, aL=aL, aU=aU, P=P, quadlow=quadlow, Hmag=Hmag, G=NI(G - eG, G + eG),
                    Wabs=aw + dw, Vabs=Vabs, ell=ell, qq=qq)
