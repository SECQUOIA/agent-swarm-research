"""Verifier's own rigorous interval certifier for eg_disc2_s leaves (eg-recheck review r1).

Own code, written for this review.  Shares nothing with indep_cert.py, the certificate author's
modules or the eg-recheck scripts.  Model data: own_model.py (cached OSIL file, exact decimals).

Arithmetic: numpy float64 interval arithmetic with outward rounding after EVERY operation:
    dn(v) = nextafter(v, -inf) - 1e-300,  up(v) = nextafter(v, +inf) + 1e-300.
Assumptions (standard IEEE-754 facts, nothing about libm): numpy's +, -, *, / on float64 are
correctly rounded to nearest (|error| <= half an ulp, so the neighbours enclose the exact value;
the 1e-300 pad also covers a possible flush of subnormal results), np.nextafter is exact,
np.ldexp is exact for normal results.  exp is NOT taken from libm: exp(x) = 2^k exp(r),
r = x - k ln2 with ln2 enclosed by its two neighbouring doubles, exp(r) by the degree-14 Taylor
polynomial evaluated in interval Horner form plus the Lagrange remainder
|r|^15/15! e^|r| <= 1.6e-19 for |r| <= 0.35 (bound used: 1e-18).  For x < -700, exp(x) is
enclosed by [0, 1e-300].  Every decimal datum of the OSIL file is enclosed by the two doubles
around it (exact Fraction comparison).

Bounds over a box X (integer coordinates relaxed to their interval):
    natural interval extension of h_k, and the mean-value form
    h_k(X) in h_k(c) + sum_i dh_k/dx_i(X) (X_i - c_i), with dh_k/dx_i(X) enclosed by
    sum_m a_m exp(E_m(X)) 2 g_ki s_i (mu_kmi + s_i X_i) + l_ki;  the two are intersected.
Certificate for a box: max_k<24 (lb_k + h_k(X)).lo >= theta*  (row bound), or a side row that
cannot be satisfied anywhere in X.  Otherwise the box is bisected (integer coordinates at
integers) up to a piece limit per leaf.  The final comparison with theta* uses a double that is
>= theta* (exact Fraction check).
"""
import os
import sys
import time
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from own_model import OsilModel  # noqa: E402

NINF, PINF = -np.inf, np.inf
PAD = 1e-300


def dn(v):
    return np.nextafter(v, NINF) - PAD


def up(v):
    return np.nextafter(v, PINF) + PAD


def encl(q):
    """two doubles around the exact rational q."""
    f = float(q)
    lo = f if Fr(f) <= q else float(np.nextafter(f, NINF))
    hi = f if Fr(f) >= q else float(np.nextafter(f, PINF))
    assert Fr(lo) <= q <= Fr(hi)
    return lo, hi


def iadd(al, ah, bl, bh):
    return dn(al + bl), up(ah + bh)


def imul(al, ah, bl, bh):
    p1, p2, p3, p4 = al * bl, al * bh, ah * bl, ah * bh
    return dn(np.minimum(np.minimum(p1, p2), np.minimum(p3, p4))), up(np.maximum(np.maximum(p1, p2), np.maximum(p3, p4)))


def isqr(al, ah):
    l2, h2 = al * al, ah * ah
    lo = np.where(al >= 0, l2, np.where(ah <= 0, h2, 0.0))
    hi = np.maximum(l2, h2)
    return np.where((al >= 0) | (ah <= 0), dn(lo), 0.0), up(hi)


LN2_LO, LN2_HI = encl(Fr("0.693147180559945309417232121458176568075500134360255254120680009493393621969694715605863326996418687542001481021"))
NTAY = 14
REM = 1e-18


def _exp_bound(x, upper):
    """rigorous lower (upper=False) or upper (upper=True) bound of exp(x), x a float array <= 1."""
    x = np.asarray(x, float)
    assert np.all(x <= 1.0) and not np.any(np.isnan(x))
    small = x < -700
    xs = np.where(small, 0.0, x)
    k = np.rint(xs / 0.6931471805599453)
    pl, ph = imul(k, k, LN2_LO, LN2_HI)
    rl, rh = dn(xs - ph), up(xs - pl)
    assert np.all(np.abs(rl) <= 0.35) and np.all(np.abs(rh) <= 0.35)
    yl, yh = np.ones_like(xs), np.ones_like(xs)
    for j in range(NTAY, 0, -1):
        tl, th = imul(rl, rh, yl, yh)
        tl, th = dn(tl / j), up(th / j)
        yl, yh = iadd(1.0, 1.0, tl, th)
    ki = k.astype(np.int64)
    if upper:
        v = np.ldexp(up(yh + REM), ki)
        return np.where(small, 1e-300, v)
    v = np.ldexp(dn(yl - REM), ki)
    return np.where(small, 0.0, np.maximum(v, 0.0))


def iexp(al, ah):
    return _exp_bound(al, False), _exp_bound(ah, True)


class IAModel:
    def __init__(self):
        O = OsilModel()
        self.O = O
        R, Mt, d = 28, 97, 7
        self.vint = np.array(O.vint[:7])
        A = np.zeros((2, R, Mt)); MU = np.zeros((2, R, Mt, d)); G = np.zeros((2, R, d)); S = np.zeros((2, d))
        LIN = np.zeros((2, R, d))
        for k, r in enumerate(O.rows):
            assert len(r["terms"]) == Mt
            for m, (a, facs) in enumerate(r["terms"]):
                A[:, k, m] = encl(a)
                for i in range(d):
                    sc, mu, g = facs[i]
                    MU[:, k, m, i] = encl(mu)
                    if m == 0:
                        G[:, k, i] = encl(g)
                        S[:, i] = encl(sc)
                    else:
                        assert (Fr(G[0, k, i]) <= g <= Fr(G[1, k, i])) and encl(g) == tuple(G[:, k, i])
                        assert encl(sc) == tuple(S[:, i])
            for i in range(d):
                LIN[:, k, i] = encl(r["lin"].get(i, Fr(0)))
        assert np.all(G[1] < 0) and np.all(S[0] > 0)
        self.A, self.MU, self.G, self.S, self.LIN = A, MU, G, S, LIN
        # 2 g s (gradient factor)
        self.K = imul(2 * G[0], 2 * G[1], S[0][None, :], S[1][None, :])   # 2*g exact (power of two)
        self.c = np.array([encl(O.clb[k]) for k in range(24)]).T            # (2, 24)
        # side rows: -h in [clb, cub]  ->  h <= -clb (if clb) and h >= -cub (if cub)
        self.side = []
        for k in range(24, 28):
            hmax = None if O.clb[k] is None else encl(-O.clb[k])
            hmin = None if O.cub[k] is None else encl(-O.cub[k])
            self.side.append((k, hmax, hmin))

    def rows(self, lo, hi, ridx, order):
        """interval enclosures over boxes [lo, hi] (N,7) of the rows ridx (N,r):
        order 0: h; order 1: h and gradient (N,r,7); order 2: h, gradient and Hessian (N,r,7,7)."""
        A, MU, G, S = self.A, self.MU, self.G, self.S
        sxl, sxh = imul(S[0][None], S[1][None], lo, hi)                                   # (N,7)
        tl, th = iadd(MU[0][ridx], MU[1][ridx], sxl[:, None, None, :], sxh[:, None, None, :])  # (N,r,97,7)
        ql, qh = isqr(tl, th)
        # g < 0, q >= 0: g*q in [g_lo * q_hi, g_hi * q_lo]
        gl, gh = G[0][ridx][:, :, None, :], G[1][ridx][:, :, None, :]
        el_, eh_ = dn(gl * qh), up(gh * ql)
        El, Eh = el_[..., 0], eh_[..., 0]
        for i in range(1, 7):
            El, Eh = iadd(El, Eh, el_[..., i], eh_[..., i])
        xl, xh = iexp(El, Eh)                                                   # (N,r,97), >= 0
        al, ah = A[0][ridx], A[1][ridx]
        wl = np.where(al >= 0, dn(al * xl), dn(al * xh))
        wh = np.where(ah >= 0, up(ah * xh), up(ah * xl))
        hl, hh = wl[..., 0], wh[..., 0]
        for m in range(1, wl.shape[-1]):
            hl, hh = iadd(hl, hh, wl[..., m], wh[..., m])
        LINl, LINh = self.LIN[0][ridx], self.LIN[1][ridx]                       # (N,r,7)
        Ll, Lh = imul(LINl, LINh, lo[:, None, :], hi[:, None, :])
        for i in range(7):
            hl, hh = iadd(hl, hh, Ll[..., i], Lh[..., i])
        if order == 0:
            return hl, hh
        # u_mi = 2 g_i s_i t_mi  (derivative of the exponent);  dh/dx_i = sum_m w_m u_mi + l_i
        Kl, Kh = self.K[0][ridx][:, :, None, :], self.K[1][ridx][:, :, None, :]
        ul, uh = imul(Kl, Kh, tl, th)                                           # (N,r,97,7)
        pl, ph = imul(wl[..., None], wh[..., None], ul, uh)
        sl, sh = pl[:, :, 0, :], ph[:, :, 0, :]
        for m in range(1, pl.shape[2]):
            sl, sh = iadd(sl, sh, pl[:, :, m, :], ph[:, :, m, :])
        gl2, gh2 = iadd(sl, sh, LINl, LINh)
        if order == 1:
            return hl, hh, gl2, gh2
        # d2h/dx_i dx_j = sum_m w_m (u_mi u_mj + [i == j] 2 g_i s_i^2)
        vl, vh = imul(ul[..., :, None], uh[..., :, None], ul[..., None, :], uh[..., None, :])   # (N,r,97,7,7)
        ii = np.arange(7)
        dgl, dgh = imul(self.K[0][ridx], self.K[1][ridx], S[0][None, None, :], S[1][None, None, :])  # 2 g s^2 (N,r,7)
        vdl, vdh = iadd(vl[..., ii, ii], vh[..., ii, ii], dgl[:, :, None, :], dgh[:, :, None, :])
        vl[..., ii, ii] = vdl
        vh[..., ii, ii] = vdh
        ql2, qh2 = imul(wl[..., None, None], wh[..., None, None], vl, vh)
        Hl, Hh = ql2[:, :, 0], qh2[:, :, 0]
        for m in range(1, ql2.shape[2]):
            Hl, Hh = iadd(Hl, Hh, ql2[:, :, m], qh2[:, :, m])
        return hl, hh, gl2, gh2, Hl, Hh

    def bounds(self, lo, hi, ridx):
        """enclosure of h_k (rows ridx) over the boxes: natural extension, first-order mean-value
        form and second-order Taylor form with interval Hessian, intersected."""
        hl, hh, gl, gh, Hl, Hh = self.rows(lo, hi, ridx, 2)
        c = 0.5 * (lo + hi)
        c = np.minimum(np.maximum(c, lo), hi)
        cl, ch, cgl, cgh = self.rows(c, c, ridx, 1)
        dl, dh = dn(lo - c), up(hi - c)                       # d = x - c in [dl, dh], dl <= 0 <= dh
        ml, mh = cl, ch
        tl_, th_ = cl, ch
        for i in range(7):
            pl, ph = imul(gl[..., i], gh[..., i], dl[:, None, i], dh[:, None, i])
            ml, mh = iadd(ml, mh, pl, ph)
            pl, ph = imul(cgl[..., i], cgh[..., i], dl[:, None, i], dh[:, None, i])
            tl_, th_ = iadd(tl_, th_, pl, ph)
        # 1/2 sum_ij H_ij d_i d_j
        sq_hi = up(np.maximum(dl * dl, dh * dh))
        ql_, qh_ = np.zeros_like(cl), np.zeros_like(cl)
        for i in range(7):
            for j in range(7):
                if i == j:
                    pdl, pdh = np.zeros_like(sq_hi[:, i]), sq_hi[:, i]
                else:
                    pdl, pdh = imul(dl[:, i], dh[:, i], dl[:, j], dh[:, j])
                pl, ph = imul(Hl[..., i, j], Hh[..., i, j], pdl[:, None], pdh[:, None])
                ql_, qh_ = iadd(ql_, qh_, pl, ph)
        tl_, th_ = iadd(tl_, th_, 0.5 * ql_, 0.5 * qh_)
        return (np.maximum(np.maximum(hl, ml), tl_), np.minimum(np.minimum(hh, mh), th_), gl, gh)


class Cert:
    def __init__(self, theta, nobj=4):
        self.M = IAModel()
        self.theta = Fr(theta)
        self.th_up = encl(self.theta)[1]       # double >= theta*
        self.nobj = nobj
        # float data for choosing rows (heuristic only; any subset of rows gives a valid bound)
        M = self.M
        A = 0.5 * (M.A[0] + M.A[1]); MU = 0.5 * (M.MU[0] + M.MU[1]); G = 0.5 * (M.G[0] + M.G[1]); S = 0.5 * (M.S[0] + M.S[1])
        self._f = (A, MU, G, S, 0.5 * (M.LIN[0] + M.LIN[1]), 0.5 * (M.c[0] + M.c[1]))

    def _pick_rows(self, lo, hi):
        A, MU, G, S, LIN, c = self._f
        x = 0.5 * (lo + hi)
        t = MU[None] + (S * x)[:, None, None, :]
        h = (A[None] * np.exp((G[None, :, None, :] * t * t).sum(-1))).sum(-1) + x @ LIN.T
        top = np.argsort(-(c[None] + h[:, :24]), axis=1)[:, :self.nobj]
        return np.concatenate([top, np.tile(np.arange(24, 28), (len(lo), 1))], 1)

    def test(self, lo, hi):
        """per box: status 0 = certified by row bound, 1 = side infeasible, -1 = undecided;
        margin (float lower bound of max over the chosen objective rows of c_k + h_k, minus th_up)
        and a split coordinate."""
        M = self.M
        ridx = self._pick_rows(lo, hi)
        no = self.nobj
        hl, hh, gl, gh = M.bounds(lo, hi, ridx)
        fl = dn(M.c[0][ridx[:, :no]] + hl[:, :no])          # lower bounds of c_k + h_k, chosen rows
        flb = fl.max(1)
        st = np.where(flb >= self.th_up, 0, -1)
        inf = np.zeros(len(lo), bool)
        for j, (k, hmax, hmin) in enumerate(M.side):
            col = no + j
            assert np.all(ridx[:, col] == k)
            if hmax is not None:
                inf |= hl[:, col] > hmax[1]
            if hmin is not None:
                inf |= hh[:, col] < hmin[0]
        st = np.where((st < 0) & inf, 1, st)
        # split coordinate: width x gradient magnitude of the best row
        kb = fl.argmax(1)
        gm = np.maximum(np.abs(gl), np.abs(gh))[np.arange(len(lo)), kb]   # (N,7)
        w = hi - lo
        sc = w * gm
        sc = np.where(M.vint & (w < 1), -1.0, sc)
        sc = np.where(~M.vint & (w <= 0), -1.0, sc)
        return st, flb - self.th_up, sc.argmax(1), sc.max(1)

    def certify(self, LO, HI, max_pieces=4000, batch=96, log=None):
        """certify leaves [LO, HI] (n,7) by recursive bisection; returns per leaf: status
        (1 certified, 0 piece limit / unsplittable), pieces used, min margin over row-certified
        pieces (inf if none), pieces proved infeasible, max depth."""
        n = len(LO)
        pieces = np.zeros(n, int); minmg = np.full(n, np.inf); ninf = np.zeros(n, int)
        maxd = np.zeros(n, int); failed = np.zeros(n, bool)
        q_lo, q_hi, q_id, q_dep = [LO.copy()], [HI.copy()], [np.arange(n)], [np.zeros(n, int)]
        qlo, qhi, qid, qdep = LO.copy(), HI.copy(), np.arange(n), np.zeros(n, int)
        t0 = time.time()
        done_boxes = 0
        while len(qlo):
            blo, bhi, bid, bdep = qlo[:batch], qhi[:batch], qid[:batch], qdep[:batch]
            qlo, qhi, qid, qdep = qlo[batch:], qhi[batch:], qid[batch:], qdep[batch:]
            alive = ~failed[bid]
            blo, bhi, bid, bdep = blo[alive], bhi[alive], bid[alive], bdep[alive]
            if not len(blo):
                continue
            st, mg, k, smax = self.test(blo, bhi)
            done_boxes += len(blo)
            np.add.at(pieces, bid, 1)
            np.maximum.at(maxd, bid, bdep)
            r = st == 0
            np.minimum.at(minmg, bid[r], mg[r])
            np.add.at(ninf, bid[st == 1], 1)
            und = np.flatnonzero(st < 0)
            # undecided: split, unless the leaf exceeded its budget or the box cannot be split
            bad = (pieces[bid[und]] >= max_pieces) | (smax[und] < 0)
            failed[bid[und[bad]]] = True
            und = und[~bad]
            if len(und):
                lo_, hi_, kk = blo[und], bhi[und], k[und]
                ii = np.arange(len(und))
                isint = self.M.vint[kk]
                mid = 0.5 * (lo_[ii, kk] + hi_[ii, kk])
                a_hi = np.where(isint, np.floor(mid), mid)
                b_lo = np.where(isint, np.floor(mid) + 1, mid)
                h1 = hi_.copy(); h1[ii, kk] = a_hi
                l2 = lo_.copy(); l2[ii, kk] = b_lo
                # depth-first per leaf keeps the queue short: put children in front
                qlo = np.concatenate([lo_, l2, qlo]); qhi = np.concatenate([h1, hi_, qhi])
                qid = np.concatenate([bid[und], bid[und], qid]); qdep = np.concatenate([bdep[und] + 1, bdep[und] + 1, qdep])
            if log and done_boxes % (batch * 200) < batch:
                print(f"      boxes {done_boxes}, queue {len(qlo)}, failed leaves {int(failed.sum())}, {time.time() - t0:.0f}s",
                      file=log, flush=True)
        return (~failed).astype(int), pieces, minmg, ninf, maxd


def verify_ln2_enclosure(n=60):
    """exact rational check that LN2_LO < ln 2 < LN2_HI: with S_n(q) = sum_{j<=n} q^j/j! and
    0 < q < 1, S_n(q) <= exp(q) <= S_n(q) + 3 q^(n+1)/(n+1)!.  Proves exp(LN2_LO) < 2 < exp(LN2_HI)."""
    def S(q):
        s, t = Fr(0), Fr(1)
        for j in range(n + 1):
            s += t
            t = t * q / (j + 1)
        return s, 3 * t          # t = q^(n+1)/(n+1)! here
    sl, rl = S(Fr(LN2_LO))
    sh, _ = S(Fr(LN2_HI))
    return sl + rl < 2 and sh > 2


assert verify_ln2_enclosure(), "ln2 enclosure not verified"
