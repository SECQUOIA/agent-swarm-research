"""Independent re-certification of the leaves of a recorded retry B&B tree (review check).

Shares no code with egfast / egtm / egbb / kan_iv / ia.  Model data come from the GAMS files
(gms_model.py).  For a box X and a target value theta*, it proves that no point x of X that
satisfies the side rows has F(x) = max_k (c_k + g_k(x)) < theta*.

Enclosures (numpy float64 with deliberately generous a-posteriori error bounds; u = 2^-53):
  * natural: exact t-ranges widened by 1e-15 (|mu| + |s x| + |t|) (>= 4u needed), exponent
    sums widened by 1e-14 sum|gamma| t^2 (>= (d+2)u needed), libm exp assumed accurate to a
    relative 1e-14 (about 90 ulp; checked by sampling in check_libm_exp), term products
    widened by 1e-14 relative, 97-term sums by 1e-13 sum|.| (>= 96u needed).
  * Taylor model at the box centre c with signed moment sums (cancellation kept) and a
    remainder derived independently of the retry: for one term w exp(L(d) + Q(d)), set
    phi(tau) = exp(tau a + tau^2 b) with a = L(d), |a| <= l, b = Q(d) in [-q, 0].  Then
        phi''' = phi p (p^2 + 6b),  phi'''' = phi (p^4 + 12 b p^2 + 12 b^2),  p = a + 2 b tau,
    |p| <= l + 2q, phi <= e^l on [0, 1], so
        order 2:  phi(1) = 1 + a + a^2/2 + b + R2,  |R2| <= e^l [(l+2q)^3/6 + q (l+2q)]
        order 3:  phi(1) = 1 + a + a^2/2 + b + (a^3/6 + a b) + R4,
                  |R4| <= e^l [(l+2q)^4 + 12 q (l+2q)^2 + 12 q^2] / 24,
    with the signed cubic sum_m w_m (L^3/6 + L Q) bounded through the moment tensors.
    The quadratic part is bounded elementwise over the box.  This gives affine minorants
    and majorants  aL_k + beta_k . d <= g_k(c + d) <= aU_k + beta_k . d.
Certificates (checked in exact rational arithmetic, fractions.Fraction, from the float data):
  row bound, side-row infeasibility, LP dual (weak duality with multipliers from scipy's
  HiGHS LP), Farkas test (phase-1 LP with the objective cuts c_k + minorant_k <= theta*).
If no certificate is found, the box is bisected (integer coordinates split at integers) and
the pieces are certified recursively, up to a depth limit.
"""
import os
import sys
import time
from fractions import Fraction as Fr

import numpy as np
from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gms_model import GmsModel  # noqa: E402

INF = np.inf
SLK = 1e-12


class Model:
    def __init__(self, name):
        G = GmsModel(name)
        T = G.terms()
        self.vars = [v for v in G.vars if v != "objvar"]
        dv = self.vars
        self.d = d = len(dv)
        self.R = R = len(T)
        self.Mt = Mt = len(T[0]["terms"])
        self.isint = np.array([v in G.ints for v in dv])
        self.qlb = [G.lb[v] for v in dv]
        self.qub = [G.ub[v] for v in dv]
        self.lb = np.array([float(v) for v in self.qlb])
        self.ub = np.array([float(v) for v in self.qub])
        # (box ends such as 0.3 are not floats; the B&B root box must contain the exact box: checked in verify_tree)
        self.A = np.zeros((R, Mt)); self.MU = np.zeros((R, Mt, d)); self.GA = np.zeros((R, d))
        self.S = np.array([float(T[0]["terms"][0][1][v][0]) for v in dv])
        self.LIN = np.zeros((R, d))
        self.qLIN = []
        self.obj = np.array([t["objc"] == 1 for t in T])
        assert self.obj[:24].all() and not self.obj[24:].any()
        self.qc = [t["rhs"] for t in T[:24]]
        self.qglo, self.qghi = [], []
        for t in T[24:]:
            if t["sense"] == "=G=":
                self.qghi.append(-t["rhs"]); self.qglo.append(None)
            else:
                self.qglo.append(-t["rhs"]); self.qghi.append(None)
        for k, t in enumerate(T):
            g0 = None
            for m, (a, fac) in enumerate(t["terms"]):
                self.A[k, m] = float(a)
                g = [fac[v][2] for v in dv]
                assert g0 is None or g == g0
                g0 = g
                assert all(gi < 0 for gi in g)
                for i, v in enumerate(dv):
                    assert float(fac[v][0]) == self.S[i]
                    self.MU[k, m, i] = float(fac[v][1])
            self.GA[k] = [float(gi) for gi in g0]
            self.LIN[k] = [float(t["lin"].get(v, 0)) for v in dv]
            self.qLIN.append([t["lin"].get(v, Fr(0)) for v in dv])
        assert np.all(self.S > 0)
        self.K1 = 2.0 * self.GA * self.S[None, :]            # 2 gamma s
        self.KD = 2.0 * self.GA * (self.S * self.S)[None, :]  # 2 gamma s^2
        self.c = np.array([float(q) for q in self.qc])
        self.glo = np.array([float(q) if q is not None else -INF for q in self.qglo])
        self.ghi = np.array([float(q) if q is not None else INF for q in self.qghi])

    # ------------------------------------------------------------------ natural enclosure
    def natural(self, lo, hi):
        S, MU, GA, A = self.S, self.MU, self.GA, self.A
        tl = MU[None] + (S * lo)[:, None, None, :]
        th = MU[None] + (S * hi)[:, None, None, :]
        dt = 1e-15 * (np.abs(MU)[None] + (S * np.maximum(np.abs(lo), np.abs(hi)))[:, None, None, :]
                      + np.maximum(np.abs(tl), np.abs(th))) + 1e-300
        tl, th = tl - dt, th + dt
        sqmin = np.where((tl <= 0) & (th >= 0), 0.0, np.minimum(tl * tl, th * th))
        sqmax = np.maximum(tl * tl, th * th)
        Elo = (GA[None, :, None, :] * sqmax).sum(-1)
        Ehi = (GA[None, :, None, :] * sqmin).sum(-1)
        err = 1e-14 * (np.abs(GA)[None, :, None, :] * sqmax).sum(-1) + 1e-300
        Elo, Ehi = Elo - err, Ehi + err
        with np.errstate(under="ignore"):
            elo = np.where(Elo < -700, 0.0, np.exp(Elo) * (1 - 1e-14))
            ehi = np.exp(np.minimum(Ehi, 700)) * (1 + 1e-14) + 1e-300
        a = A[None]
        tlo = np.where(a > 0, a * elo, a * ehi)
        thi = np.where(a > 0, a * ehi, a * elo)
        tlo = tlo - 1e-14 * np.abs(tlo) - 1e-300
        thi = thi + 1e-14 * np.abs(thi) + 1e-300
        glo = tlo.sum(-1) - 1e-13 * np.abs(tlo).sum(-1) - 1e-300
        ghi = thi.sum(-1) + 1e-13 * np.abs(thi).sum(-1) + 1e-300
        L = self.LIN[None]
        llo = np.minimum(L * lo[:, None, :], L * hi[:, None, :])
        lhi = np.maximum(L * lo[:, None, :], L * hi[:, None, :])
        glo = glo + llo.sum(-1) - 1e-13 * (np.abs(llo).sum(-1) + np.abs(glo)) - 1e-300
        ghi = ghi + lhi.sum(-1) + 1e-13 * (np.abs(lhi).sum(-1) + np.abs(ghi)) + 1e-300
        return glo, ghi

    # ------------------------------------------------------------------ Taylor model
    def taylor(self, lo, hi):
        N, d = lo.shape
        S, MU, GA, A = self.S, self.MU, self.GA, self.A
        c = np.clip(0.5 * (lo + hi), lo, hi)
        r = np.where(hi == lo, 0.0, np.maximum(hi - c, c - lo) * (1 + 1e-15))
        dims = [i for i in range(d) if np.any(r[:, i] > 0)]
        n = len(dims)
        t = MU[None] + (S * c)[:, None, None, :]                                   # (N,R,M,d)
        dt = 1e-15 * (np.abs(MU)[None] + np.abs(S * c)[:, None, None, :] + np.abs(t)) + 1e-300
        E0 = (GA[None, :, None, :] * t * t).sum(-1)
        dE = (np.abs(GA)[None, :, None, :] * ((2 * np.abs(t) + dt) * dt + 1e-14 * t * t)).sum(-1) + 1e-300
        assert np.all(dE < 1e-6)
        with np.errstate(under="ignore"):
            ex = np.where(E0 < -700, 0.0, np.exp(np.maximum(E0, -745)))
        w = A[None] * ex
        dw = np.abs(w) * (1.02 * dE + 1.1e-14) + np.where(E0 < -699, np.abs(A)[None] * 1e-300, 0.0) + 1e-300
        aw = np.abs(w)
        AW = aw + dw
        S0 = w.sum(-1)
        e0 = dw.sum(-1) + 1e-13 * aw.sum(-1)
        linc = (self.LIN[None] * c[:, None, :])
        G = S0 + linc.sum(-1)
        eG = e0 + 1e-13 * (np.abs(S0) + np.abs(linc).sum(-1)) + 1e-300
        beta = np.zeros((N, self.R, d))
        egrad = np.zeros((N, self.R, d))
        QL = np.zeros((N, self.R)); QU = np.zeros((N, self.R)); P = np.zeros((N, self.R))
        if n:
            tm = t[..., dims]
            dtm = dt[..., dims]
            tau = (np.abs(tm) + dtm).max(-1)
            dtau = dtm.max(-1)
            k1 = self.K1[:, dims]; kd = self.KD[:, dims]
            ak1 = np.abs(k1) * (1 + 1e-14)
            S1 = np.einsum("nrm,nrmi->nri", w, tm)
            e1 = (dw * tau + aw * dtau + 1e-13 * aw * tau).sum(-1)
            S2 = np.einsum("nrm,nrmi,nrmj->nrij", w, tm, tm)
            e2 = (dw * tau ** 2 + 2 * aw * tau * dtau + 1e-13 * aw * tau ** 2).sum(-1)
            e3 = (dw * tau ** 3 + 3 * aw * tau ** 2 * dtau + 1e-13 * aw * tau ** 3).sum(-1)
            lin = self.LIN[None][..., dims]
            gr = k1[None] * S1 + lin
            beta[..., dims] = gr
            egrad[..., dims] = ak1[None] * e1[..., None] + 1e-13 * (np.abs(k1[None] * S1) + np.abs(lin) + np.abs(gr)) + 1e-300
            H = k1[None, :, :, None] * k1[None, :, None, :] * S2
            eH = (ak1[:, :, None] * ak1[:, None, :])[None] * e2[..., None, None] + 1e-13 * np.abs(H)
            ii = np.arange(n)
            H[..., ii, ii] += kd[None] * S0[..., None]
            eH[..., ii, ii] += np.abs(kd)[None] * (1 + 1e-14) * e0[..., None] + 1e-13 * np.abs(kd[None] * S0[..., None])
            eH = eH * (1 + 1e-12) + 1e-300
            rn = r[:, dims]
            rr = rn[:, :, None] * rn[:, None, :]
            Hl, Hh = H - eH, H + eH
            Hm = np.maximum(np.abs(Hl), np.abs(Hh))
            diag_l = 0.5 * (np.minimum(np.diagonal(Hl, axis1=2, axis2=3), 0.0) * (rn * rn)[:, None, :]).sum(-1)
            diag_h = 0.5 * (np.maximum(np.diagonal(Hh, axis1=2, axis2=3), 0.0) * (rn * rn)[:, None, :]).sum(-1)
            off = np.zeros((N, self.R))
            for a_ in range(n):
                for b_ in range(a_ + 1, n):
                    off = off + Hm[..., a_, b_] * rr[:, None, a_, b_]
            QL = (diag_l - off) * (1 + 1e-12) - 1e-300
            QU = (diag_h + off) * (1 + 1e-12) + 1e-300
            # remainders
            ell = ((ak1[None, :, None, :] * (np.abs(tm) + dtm)) * rn[:, None, None, :]).sum(-1) * (1 + 1e-13)
            q = ((np.abs(GA[:, dims]) * (self.S[dims] ** 2))[None] * (rn * rn)[:, None, :]).sum(-1) * (1 + 1e-13)
            q = q[..., None]
            p = ell + 2 * q
            big = ell > 600
            el = np.exp(np.where(big, 0.0, ell)) * (1 + 1e-14)
            R2 = el * (p ** 3 / 6 + q * p)
            R4 = el * (p ** 4 + 12 * q * p ** 2 + 12 * q * q) / 24
            P2 = (AW * R2).sum(-1) * (1 + 1e-12)
            P4 = (AW * R4).sum(-1) * (1 + 1e-12)
            # signed cubic: (1/6) sum_ijk |T_ijk| r_i r_j r_k + sum_ij |U_ij| r_i r_j^2 (ordered triples)
            cub = np.zeros((N, self.R))
            for a_ in range(n):
                for b_ in range(n):
                    wt2 = w * tm[..., a_] * tm[..., b_]
                    for c_ in range(n):
                        s3 = np.abs((wt2 * tm[..., c_]).sum(-1)) + e3
                        cub = cub + ak1[None, :, a_] * ak1[None, :, b_] * ak1[None, :, c_] * s3 * \
                            (rn[:, a_] * rn[:, b_] * rn[:, c_])[:, None]
            cub = cub / 6
            U1 = (ak1[None] * (np.abs(S1) + e1[..., None]) * rn[:, None, :]).sum(-1)
            U2 = ((np.abs(GA[:, dims]) * (self.S[dims] ** 2) * (1 + 1e-14))[None] * (rn * rn)[:, None, :]).sum(-1)
            P3 = (cub + U1 * U2) * (1 + 1e-12) + P4
            P = np.where(big.any(-1), INF, np.minimum(P2, P3) * (1 + 1e-12) + 1e-300)
        LE = (egrad * r[:, None, :]).sum(-1) * (1 + 1e-12)
        tot = np.abs(G) + eG + P + np.abs(QL) + np.abs(QU) + LE
        with np.errstate(invalid="ignore"):
            aL = G - eG - P + QL - LE - SLK * tot - 1e-300
            aU = G + eG + P + QU + LE + SLK * tot + 1e-300
        aL = np.where(np.isfinite(aL), aL, -INF)
        aU = np.where(np.isfinite(aU), aU, INF)
        return c, r, beta, aL, aU


# ---------------------------------------------------------------------- exact checks
def F(x):
    return Fr(float(x)) if not isinstance(x, Fr) else x


def lin_min_exact(coef, dl, dh):
    """exact min over the box of sum coef_i d_i (coef, dl, dh Fractions)."""
    return sum((ci * a if ci >= 0 else ci * b) for ci, a, b in zip(coef, dl, dh))


class Certifier:
    def __init__(self, name, theta, max_depth=24, max_pieces=10**7):
        self.M = Model(name)
        self.theta = Fr(theta)
        self.max_depth = max_depth
        self.max_pieces = max_pieces
        self.stats = dict(row=0, side=0, lp=0, farkas=0, split=0, fail=0, pieces=0, empty=0)
        self.min_margin = None      # smallest certified (bound - theta) over LP/row certificates

    def _margin(self, v):
        m = v - self.theta
        if self.min_margin is None or m < self.min_margin:
            self.min_margin = m

    def certify_batch(self, lo, hi):
        """returns a boolean array: True where the box was certified (possibly after splitting)."""
        ok = self._batch(lo, hi, 0)
        self.stats["fail"] += int((~ok).sum())
        return ok

    def _batch(self, lo, hi, depth):
        M = self.M
        N = len(lo)
        self.stats["pieces"] += N
        ok = np.zeros(N, bool)
        todo = []
        for s in range(0, N, 64):
            l_, h_ = lo[s:s + 64], hi[s:s + 64]
            c, r, beta, aL, aU = M.taylor(l_, h_)
            nlo, nhi = M.natural(l_, h_)
            for j in range(len(l_)):
                if self._one(l_[j], h_[j], c[j], beta[j], aL[j], aU[j], nlo[j], nhi[j]):
                    ok[s + j] = True
                else:
                    todo.append(s + j)
        if todo and depth < self.max_depth and self.stats["pieces"] < self.max_pieces:
            clo, chi, owner = [], [], []
            for n in todo:
                for a, b in self._split(lo[n], hi[n]):
                    clo.append(a); chi.append(b); owner.append(n)
                self.stats["split"] += 1
            sub = self._batch(np.array(clo), np.array(chi), depth + 1)
            owner = np.array(owner)
            for n in todo:
                ok[n] = bool(sub[owner == n].all())
        return ok

    def _split(self, lo, hi):
        M = self.M
        w = (hi - lo) / (M.ub - M.lb)
        w = np.where(M.isint & (hi - lo < 1), -1.0, w)
        k = int(np.argmax(w))
        if M.isint[k]:
            m = np.floor(0.5 * (lo[k] + hi[k]))
            a_hi, b_lo = m, m + 1
        else:
            a_hi = b_lo = 0.5 * (lo[k] + hi[k])
        h1 = hi.copy(); h1[k] = a_hi
        l2 = lo.copy(); l2[k] = b_lo
        return [(lo.copy(), h1), (l2, hi.copy())]

    def _one(self, lo, hi, c, beta, aL, aU, nlo, nhi):
        """try the certificates on one box; exact rational arithmetic."""
        M = self.M
        th = self.theta
        if np.any(lo > hi):
            self.stats["empty"] += 1
            return True
        dl = [F(a) - F(b) for a, b in zip(lo, c)]
        dh = [F(a) - F(b) for a, b in zip(hi, c)]
        Bq = [[F(v) for v in beta[k]] for k in range(28)]
        # lower / upper bounds of each row over the box (affine or natural)
        rmin, rmax = [], []
        for k in range(28):
            lo_k = F(aL[k]) + lin_min_exact(Bq[k], dl, dh) if np.isfinite(aL[k]) else None
            hi_k = F(aU[k]) - lin_min_exact([-b for b in Bq[k]], dl, dh) if np.isfinite(aU[k]) else None
            nl, nh = F(nlo[k]) if np.isfinite(nlo[k]) else None, F(nhi[k]) if np.isfinite(nhi[k]) else None
            rmin.append(max([v for v in (lo_k, nl) if v is not None], default=None))
            rmax.append(min([v for v in (hi_k, nh) if v is not None], default=None))
        for k in range(24):
            if rmin[k] is not None and M.qc[k] + rmin[k] >= th:
                self.stats["row"] += 1
                return True
        for j in range(4):
            k = 24 + j
            if M.qghi[j] is not None and rmin[k] is not None and rmin[k] > M.qghi[j]:
                self.stats["side"] += 1
                return True
            if M.qglo[j] is not None and rmax[k] is not None and rmax[k] < M.qglo[j]:
                self.stats["side"] += 1
                return True
        # LP over the affine models (float data only proposes multipliers)
        rows, rhs, tags = [], [], []
        for k in range(24):
            if np.isfinite(aL[k]):
                rows.append(list(beta[k]) + [-1.0]); rhs.append(-(M.c[k] + aL[k])); tags.append(("obj", k))
        for j in range(4):
            k = 24 + j
            if M.qghi[j] is not None and np.isfinite(aL[k]):
                rows.append(list(beta[k]) + [0.0]); rhs.append(M.ghi[j] - aL[k]); tags.append(("up", k))
            if M.qglo[j] is not None and np.isfinite(aU[k]):
                rows.append(list(-beta[k]) + [0.0]); rhs.append(aU[k] - M.glo[j]); tags.append(("lo", k))
        if not any(t[0] == "obj" for t in tags):
            return False
        bounds = [(float(a), float(b)) for a, b in zip(dl, dh)] + [(None, None)]
        cost = np.zeros(M.d + 1); cost[-1] = 1.0
        res = linprog(cost, A_ub=np.array(rows), b_ub=np.array(rhs), bounds=bounds, method="highs")
        if res.status == 0:
            y = np.maximum(-np.asarray(res.ineqlin.marginals), 0.0)
            v = self._dual_value(y, tags, Bq, aL, aU, dl, dh)
            if v is not None and v >= th:
                self._margin(v)
                self.stats["lp"] += 1
                return True
            return False
        if res.status == 2:
            # Farkas: side rows and objective cuts c_k + aL_k + beta_k . d <= theta*
            rows2, rhs2, tags2 = [], [], []
            for k in range(24):
                if np.isfinite(aL[k]):
                    rows2.append(list(beta[k]) + [-1.0]); rhs2.append(float(th) - M.c[k] - aL[k]); tags2.append(("cut", k))
            for (kind, k), row, b in zip(tags, rows, rhs):
                if kind != "obj":
                    rows2.append(row[:-1] + [-1.0]); rhs2.append(b); tags2.append((kind, k))
            res2 = linprog(cost, A_ub=np.array(rows2), b_ub=np.array(rhs2), bounds=bounds, method="highs")
            if res2.status == 0:
                z = np.maximum(-np.asarray(res2.ineqlin.marginals), 0.0)
                if self._farkas(z, tags2, Bq, aL, aU, dl, dh):
                    self.stats["farkas"] += 1
                    return True
        return False

    def _combine(self, mult, tags, Bq, aL, aU):
        M = self.M
        const = Fr(0)
        coef = [Fr(0)] * M.d
        for (kind, k), mu in zip(tags, mult):
            if not mu > 0:
                continue
            mu = Fr(float(mu))
            if kind == "obj":
                const += mu * (M.qc[k] + F(aL[k]))
                coef = [a + mu * b for a, b in zip(coef, Bq[k])]
            elif kind == "cut":
                const += mu * (M.qc[k] + F(aL[k]) - self.theta)
                coef = [a + mu * b for a, b in zip(coef, Bq[k])]
            elif kind == "up":
                const += mu * (F(aL[k]) - M.qghi[k - 24])
                coef = [a + mu * b for a, b in zip(coef, Bq[k])]
            else:
                const += mu * (M.qglo[k - 24] - F(aU[k]))
                coef = [a - mu * b for a, b in zip(coef, Bq[k])]
        return const, coef

    def _dual_value(self, y, tags, Bq, aL, aU, dl, dh):
        ys = sum(Fr(float(v)) for v, t in zip(y, tags) if t[0] == "obj" and v > 0)
        if ys <= 0:
            return None
        const, coef = self._combine(y, tags, Bq, aL, aU)
        return (const + lin_min_exact(coef, dl, dh)) / ys

    def _farkas(self, z, tags, Bq, aL, aU, dl, dh):
        if not np.any(z > 0):
            return False
        const, coef = self._combine(z, tags, Bq, aL, aU)
        return const + lin_min_exact(coef, dl, dh) > 0


def check_libm_exp(n=20000, seed=3):
    """sampling check of the libm-exp assumption (relative error <= 1e-14) against mpmath."""
    import mpmath as mp
    rng = np.random.default_rng(seed)
    x = np.concatenate([rng.uniform(-700, 1, n), rng.uniform(-1, 1, n // 4) * 10.0 ** rng.uniform(-20, 0, n // 4)])
    e = np.exp(x)
    mp.mp.dps = 40
    worst = max(float(abs(mp.mpf(float(a)) / mp.exp(mp.mpf(float(b))) - 1)) for a, b in zip(e, x))
    return worst
