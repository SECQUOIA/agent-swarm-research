"""Fast rigorous enclosures for the eg_* rows: float arithmetic with explicit error bounds.

Everything here is plain IEEE double arithmetic (round to nearest, no underflow except where
an absolute 1e-300 is added) followed by an explicit bound on the accumulated error.
Unit roundoff u = 2^-53.  Derived quantities (moment sums, Hessian entries, the final affine
constants) get a relative slack SL = 1e-12 (about 9000 u) on top of the bounds below, and
every computed nonnegative error bound is inflated by (1 + SL) plus 1e-300.

(1) fexp(x): lo <= e^x <= hi for float arrays x <= 700.
    x = m ln2/64 + r with m = rint(x 64/ln2); r~ = (x - m L1) - m L2, where L1 has 32
    significant bits (m L1 is exact for |m| < 2^20) and |ln2/64 - L1 - L2| < 1e-27
    (checked exactly with Fractions).  |r~| <= 0.0055 (asserted) and |r~ - r| <= 1e-18:
    x - m L1 is exact by Sterbenz's lemma (0 < L1 < ln2/64, so m L1 lies within a factor 2
    of x when m != 0), the last subtraction adds at most u|r~| < 6.2e-19, and fl(m L2) and
    the split add less than 1e-22.  (Without the exactness of x - m L1, add u|x - m L1|:
    1.3e-18 in total.  Either is far inside the slack below.  check_fexp_r.py.)
    e^r is evaluated by Horner's rule for the degree-6 Taylor polynomial: truncation
    <= |r|^7/7! e^|r| < 1e-19, evaluation error <= gamma_12 e^0.0055 + u < 1.5e-15, so
    |p~ - e^r| <= 2e-15 e^r.  e^x = 2^k T_j e^r with T_j = e^(j ln2/64) enclosed by the
    50-digit table of kan_iv [TLO_j, THI_j].
    Result: lo = 2^k fl(fl(TLO_j p~)(1 - 4e-15)), hi = 2^k fl(fl(THI_j p~)(1 + 4e-15)): the
    needed factors are (1 - u)(1 - 2e-15) and (1 + u)(1 + 2e-15), and the final rounding
    moves them by at most u.  Scaling by 2^k is exact because x >= -700 keeps the result
    normal.  For x < -700 we return [0, 1e-300] (e^-700 < 1e-304).

(2) Term data at a point c.  The float constants mu~, s~, gamma~, a~ are midpoints of the
    one-ulp enclosures of the exact decimals, so each has relative error <= 2u.
    t~ = fl(mu~ + fl(s~ c)):  |t~ - t| <= 2u|mu~| + 2u|s~ c| + 1.01u|s~ c| + u|t~|
    <= DT = 3.1 u (|mu~| + |fl(s~ c)| + |t~|)  (per element).
    E~ = fl(sum_i fl(gamma~_i fl(t~_i^2))):
      |E - E~| <= dE = 1.01 sum_i |gamma~_i| [ (2|t~_i| + DT_i) DT_i + (d + 5) u (|t~_i| + DT_i)^2 ]
    (t error; 2u for gamma~; 2u for the two products and (d - 1) u for the sum, d = 7).
    w = a e^E:  w~ = fl(a~ e~) with e~ the midpoint and de the half-width of the fexp
    enclosure [elo, ehi] of e^E~ (so e^E lies in [elo e^-dE, ehi e^dE]);
      |w - w~| <= dw = |a~| de (1 + 4u) + (1.02 dE + 4u) |w~| + 1e-300.

(4) Taylor model (method taylor).  With L = sum v_i d_i, Q = sum gamma_i s_i^2 d_i^2 <= 0,
    l = sum |v_i| r_i, q = sum |gamma_i| s_i^2 r_i^2 (per term), the part of e^(L+Q) beyond
    second order is bounded in two ways and the smaller total is used per row:
      second order:  |R3| <= l q + q^2/2 + (l + q)^3 e^l / 6   (summed with |w|);
      third order:   C3 + R4 with the signed cubic C3 = sum_m w_m (L^3/6 + L Q) bounded by
        (1/6) sum_ijk |T_ijk| r_i r_j r_k + sum_ij |U_ij| r_i r_j^2,
        T_ijk = sum_m w_m v_mi v_mj v_mk,  U_ij = gamma_j s_j^2 sum_m w_m v_mi,
      and |R4| <= q^2/2 + l^2 q/2 + l q^2/2 + q^3/6 + (l + q)^4 e^l / 24.
    The moment sums carry the error bounds of item (2) and the float summation bound
    (M + 4) u sum |.| for the four-factor products.

(3) Natural enclosure over a box: the float end points tl, th of each t-range are within
    DT of the exact ones; with tmax = max(|tl|, |th|), the exact range of E lies in
    [sum gamma~ sqmax - dE, sum gamma~ sqmin + dE] with
      dE = 1.01 sum_i |gamma~_i| [ (2 tmax_i + DT_i) DT_i + (d + 5) u (tmax_i + DT_i)^2 ].
    Term ranges a [e_lo, e_hi] are widened by 4u relative; sums over the M terms by
    (M + 3) u sum |.| (valid for any summation order).
"""
import os
import sys
from fractions import Fraction as Fr

import mpmath as mp
import numpy as np

import egtm
from egtm import NI

K = egtm.K
INF = np.inf
SL = 1e-12
UR = 2.0 ** -53
ORDER2 = os.environ.get("EG_ORDER") == "2"      # ablation: second-order remainder only

# ---- ln2/64 split (Cody-Waite) and exactness check
with mp.workdps(60):
    _L = mp.log(2) / 64
    _Lq = Fr(mp.nstr(_L, 58, strip_zeros=False))
_L1 = float(np.ldexp(np.floor(np.ldexp(float(_Lq), 38)), -38))   # 32 significant bits (L ~ 2^-6.5)
_L2 = float(_Lq - Fr(_L1))
assert abs(_Lq - Fr(_L1) - Fr(_L2)) < Fr(1, 10**27)     # |ln2/64 - _Lq| < 1e-57
assert Fr(_L1).denominator <= 2 ** 38 and (Fr(_L1) * 2 ** 38).numerator < 2 ** 32
_INV_L = float(64 / mp.log(2))
_C = [1.0, 1.0, 0.5, 1.0 / 6, 1.0 / 24, 1.0 / 120, 1.0 / 720]
_TLO, _THI = K._TLO, K._THI


def fexp(x):
    """(lo, hi) with lo <= e^x <= hi elementwise; x <= 700."""
    x = np.asarray(x, dtype=np.float64)
    assert not np.any(x > 700.0) and not np.any(np.isnan(x))
    small = x < -700.0
    xs = np.where(small, 0.0, x)
    m = np.rint(xs * _INV_L)
    r = (xs - m * _L1) - m * _L2
    assert np.all(np.abs(r) <= 0.0055)
    p = _C[6]
    for j in range(5, -1, -1):
        p = _C[j] + r * p
    mi = m.astype(np.int64)
    k = np.floor_divide(mi, 64)
    j = mi - 64 * k
    lo = np.ldexp((_TLO[j] * p) * (1.0 - 4e-15), k)
    hi = np.ldexp((_THI[j] * p) * (1.0 + 4e-15), k)
    lo = np.where(small, 0.0, lo)
    hi = np.where(small, 1e-300, hi)
    return lo, hi


def infl(x):
    return x * (1.0 + SL) + 1e-300


class Fast(egtm.Model):
    def __init__(self, name):
        super().__init__(name)
        mid = lambda X: 0.5 * (X.lo + X.hi)
        self.am = mid(self.A)                          # (R, M)
        self.mum = mid(self.MU)                        # (R, M, d)
        self.gam = mid(self.GA)                        # (R, d)
        self.sm = mid(self.S)                          # (d,)
        self.k1 = mid(self.TWOGS)                      # 2 gamma s
        self.kd = mid(self.TWOGS2)                     # 2 gamma s^2
        self.lin_m = mid(self.LIN)
        self.hgs2 = 0.5 * np.abs(self.kd)
        assert np.all(np.abs(self.mum) <= 6.0) and np.all(self.A.lo * self.A.hi > 0)
        assert np.all(np.abs(self.sm[None, :] * np.maximum(np.abs(self.lo0), np.abs(self.hi0))) <= 6.0)
        self.agam = np.abs(self.gam)

    def point(self, x):
        """enclosure of g_k at float points x (N, d) by the interval (NI) path of egtm.Model,
        independent of the float error analysis used for the bounds."""
        return egtm.Model.natural(self, x, x)

    # ------------------------------------------------------------ term values at centres
    def _dE(self, tabs, DTe):
        """error bound for E~ = sum_i gamma~_i t~_i^2 given |t~| (or tmax) and its error DTe."""
        d = self.d
        return 1.01 * np.einsum("nrmi,ri->nrm", (2.0 * tabs + DTe) * DTe + (d + 5) * UR * (tabs + DTe) ** 2,
                                self.agam)

    def _terms(self, c):
        """w~, dw (N, R, M), t~ (N, R, M, d) and the per-element bound DT of |t~ - t|."""
        sc = self.sm[None, :] * c                                         # (N, d)
        t = self.mum[None] + sc[:, None, None, :]                         # (N, R, M, d)
        assert np.all(np.abs(t) <= 12.0)
        at = np.abs(t)
        DTe = 3.1 * UR * (np.abs(self.mum)[None] + np.abs(sc)[:, None, None, :] + at)
        E = np.einsum("nrmi,ri->nrm", t * t, self.gam)
        dE = self._dE(at, DTe)
        elo, ehi = fexp(E)
        em = 0.5 * (elo + ehi)
        de = 0.5 * (ehi - elo)
        w = self.am[None] * em
        dw = (np.abs(self.am)[None] * de) * (1.0 + 4 * UR) + (1.02 * dE + 4 * UR) * np.abs(w) + 1e-300
        return w, dw, t, DTe

    # ------------------------------------------------------------ natural enclosure
    def natural(self, lo, hi):
        slo = self.sm[None, :] * lo
        shi = self.sm[None, :] * hi
        tl = self.mum[None] + slo[:, None, None, :]
        th = self.mum[None] + shi[:, None, None, :]
        tl2, th2 = tl * tl, th * th
        sqmin = np.where((tl <= 0) & (th >= 0), 0.0, np.minimum(tl2, th2))
        sqmax = np.maximum(tl2, th2)
        tmax = np.maximum(np.abs(tl), np.abs(th))
        assert np.all(tmax <= 12.0)
        DTe = 3.1 * UR * (np.abs(self.mum)[None] + np.maximum(np.abs(slo), np.abs(shi))[:, None, None, :] + tmax)
        dE = self._dE(tmax, DTe)
        Elo = np.einsum("nrmi,ri->nrm", sqmax, self.gam) - dE
        Ehi = np.einsum("nrmi,ri->nrm", sqmin, self.gam) + dE
        e_lo, _ = fexp(Elo)
        _, e_hi = fexp(Ehi)
        a = self.am[None]
        pos = a > 0
        tlo = np.where(pos, a * e_lo, a * e_hi)
        thi = np.where(pos, a * e_hi, a * e_lo)
        tlo = tlo - 4 * UR * np.abs(tlo) - 1e-300
        thi = thi + 4 * UR * np.abs(thi) + 1e-300
        g = (self.Mt + 3) * UR
        glo = tlo.sum(-1) - g * np.abs(tlo).sum(-1) - 1e-300
        ghi = thi.sum(-1) + g * np.abs(thi).sum(-1) + 1e-300
        L = self.lin_m[None]
        llo = np.minimum(L * lo[:, None, :], L * hi[:, None, :])
        lhi = np.maximum(L * lo[:, None, :], L * hi[:, None, :])
        glo = glo + llo.sum(-1) - SL * (np.abs(llo).sum(-1) + np.abs(glo)) - 1e-300
        ghi = ghi + lhi.sum(-1) + SL * (np.abs(lhi).sum(-1) + np.abs(ghi)) + 1e-300
        return NI(glo, ghi)

    # ------------------------------------------------------------ Taylor model
    def taylor(self, lo, hi, dims=None):
        N, d = lo.shape
        R, Mt = self.R, self.Mt
        c = 0.5 * (lo + hi)
        c = np.minimum(np.maximum(c, lo), hi)
        r = np.maximum(hi - c, c - lo) * (1.0 + 4 * UR)
        r = np.where(hi == lo, 0.0, r)
        if dims is None:
            dims = [i for i in range(d) if np.any(r[:, i] > 0)]
        dims = list(dims)
        n = len(dims)
        w, dw, t, DTe = self._terms(c)
        aw = np.abs(w)
        gam = (Mt + 3) * UR
        S0 = w.sum(-1)
        e0 = infl((dw + gam * aw).sum(-1))
        G = S0 + c @ self.lin_m.T
        eG = infl(e0 + SL * (np.abs(c) @ np.abs(self.lin_m).T + np.abs(G)))
        beta = np.zeros((N, R, d)); rad = np.zeros((N, R, d))
        Hm = np.zeros((N, R, d, d)); He = np.zeros((N, R, d, d))
        P = np.zeros((N, R))
        Vabs = np.zeros((N, R, Mt, d))
        ell = np.zeros((N, R, Mt)); qq = np.zeros((N, R, Mt))
        if n:
            tm = t[..., dims]
            dtm = DTe[..., dims]
            dtau = dtm.max(-1)
            tau = (np.abs(tm) + dtm).max(-1)
            S1 = np.einsum("nrm,nrmi->nri", w, tm)
            S2 = np.einsum("nrm,nrmi,nrmj->nrij", w, tm, tm)
            e1 = infl((dw * tau + aw * dtau + gam * aw * tau).sum(-1))
            e2 = infl((dw * tau * tau + 2.0 * aw * tau * dtau + gam * aw * tau * tau).sum(-1))
            k1 = self.k1[:, dims]
            kd = self.kd[:, dims]
            lm = self.lin_m[None][..., dims]
            g1 = k1[None] * S1 + lm
            eg1 = infl(np.abs(k1)[None] * e1[..., None] + SL * (np.abs(k1[None] * S1) + np.abs(lm) + np.abs(g1)))
            k2 = k1[:, :, None] * k1[:, None, :]
            H = k2[None] * S2
            eH = np.abs(k2)[None] * e2[..., None, None] + SL * np.abs(H)
            ii = np.arange(n)
            Hd = kd[None] * S0[..., None]
            H[..., ii, ii] += Hd
            eH[..., ii, ii] += np.abs(kd)[None] * e0[..., None] + SL * np.abs(Hd)
            eH = infl(eH + SL * np.abs(H))
            beta[..., dims] = g1
            rad[..., dims] = eg1
            ix = np.ix_(range(N), range(R), dims, dims)
            Hm[ix] = H
            He[ix] = eH
            rn = r[:, dims]
            va = infl(np.abs(k1)[None, :, None, :] * (np.abs(tm) + dtm))
            ell = infl((va * rn[:, None, None, :]).sum(-1))
            q1 = infl((self.hgs2[:, dims][None] * (rn * rn)[:, None, :]).sum(-1))       # (N, R)
            qq = np.broadcast_to(q1[..., None], ell.shape)
            uu = ell + qq
            big = ell > 600.0
            _, el = fexp(np.where(big, 0.0, ell))
            R3 = infl(ell * qq + 0.5 * qq * qq + uu * uu * uu * el / 6.0)
            R3 = np.where(big, INF, R3)
            P3 = infl(((aw + dw) * R3).sum(-1))
            # third-order alternative (see module docstring, item 4): signed cubic part + R4
            if ORDER2:
                P = P3
                Vabs[..., dims] = va
        if n and not ORDER2:
            R4 = infl(0.5 * qq * qq + 0.5 * ell * ell * qq + 0.5 * ell * qq * qq + qq * qq * qq / 6.0
                      + (uu * uu) * (uu * uu) * el / 24.0)
            R4 = np.where(big, INF, R4)
            P4 = infl(((aw + dw) * R4).sum(-1))
            gam4 = (Mt + 4) * UR
            e3 = infl((dw * tau ** 3 + 3.0 * aw * tau * tau * dtau + gam4 * aw * tau ** 3).sum(-1))
            ak1 = np.abs(k1)[None]                                                  # (1, R, n)
            cub = np.zeros((N, R))
            for a_ in range(n):
                for b_ in range(a_, n):
                    wt2 = w * tm[..., a_] * tm[..., b_]
                    for c_ in range(b_, n):
                        s3 = np.abs((wt2 * tm[..., c_]).sum(-1)) + e3
                        mult = 6.0 if (a_ < b_ < c_) else (1.0 if a_ == b_ == c_ else 3.0)
                        cub = cub + mult * (ak1[..., a_] * ak1[..., b_] * ak1[..., c_]) * s3 * (
                            rn[:, a_] * rn[:, b_] * rn[:, c_])[:, None]
            cub = cub / 6.0
            cubU = (ak1 * (np.abs(S1) + e1[..., None]) * rn[:, None, :]).sum(-1) * \
                (0.5 * np.abs(kd)[None] * (rn * rn)[:, None, :]).sum(-1)
            P = np.minimum(P3, infl(infl(cub + cubU) * (1.0 + SL) + P4))
            Vabs[..., dims] = va
        Hlo, Hhi = Hm - He, Hm + He
        Hmag = np.maximum(np.abs(Hlo), np.abs(Hhi))
        rr = r * r
        r2 = r[:, :, None] * r[:, None, :]
        dmag = np.diagonal(Hmag, axis1=2, axis2=3)
        dneg = (np.maximum(-np.diagonal(Hlo, axis1=2, axis2=3), 0.0) * rr[:, None, :]).sum(-1)
        dpos = (np.maximum(np.diagonal(Hhi, axis1=2, axis2=3), 0.0) * rr[:, None, :]).sum(-1)
        full = (Hmag * r2[:, None]).sum((-1, -2))
        offd = np.maximum(0.5 * (full - (dmag * rr[:, None, :]).sum(-1)), 0.0)
        offd = infl(offd + SL * full)
        quadlow = -infl(0.5 * dneg + offd)
        quadhigh = infl(0.5 * dpos + offd)
        lin_err = infl((rad * r[:, None, :]).sum(-1))
        with np.errstate(invalid="ignore"):
            tot = np.abs(G) + eG + P + np.abs(quadlow) + np.abs(quadhigh) + lin_err
            aL = G - eG - P + quadlow - lin_err - SL * tot - 1e-300
            aU = G + eG + P + quadhigh + lin_err + SL * tot + 1e-300
        aL = np.where(np.isfinite(aL), aL, -INF)
        aU = np.where(np.isfinite(aU), aU, INF)
        return dict(c=c, r=r, beta=beta, aL=aL, aU=aU, P=P, quadlow=quadlow, Hmag=Hmag,
                    G=NI(G - eG, G + eG), Wabs=aw + dw, Vabs=Vabs, ell=ell, qq=qq)
