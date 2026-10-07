"""Reduced-space rigorous branch and bound for the KAN instances.

Minimizes the ideal network function  f~(u) = A (beta0 + sum_j psi~_j(h~_j(u))) + B,
h~_j(u) = beta_j + sum_i phi~_ij(u_i), over the input box U intersected with
{ h~_j(u) in [L_j - eta_j, U_j + eta_j] } (see kan_model / report for why this is a
relaxation of the OSIL model up to the explicit error Delta).

Lower bounds per box: natural interval extension (with the h-constraints
intersected) and the mean-value form; monotonicity test on fully feasible boxes.
All arithmetic is outward rounded (kan_iv / ia.NI).

    python3 kan_bb.py <name> [tol_rel] [time_limit_s]
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import sys
import time
from fractions import Fraction as Fr

import numpy as np

import kan_iv as K
import kan_model as km
from kan_iv import NI, dn, up

INF = np.inf


# ----------------------------------------------------------------------------
def _q_endpoint(g, m, d):
    """rigorous lower bound of g*d + m*d^2/2 at float d (g, m, d floats; each product
    carries at most two roundings, covered by a 1e-15 relative margin)."""
    v1 = g * d
    v2 = 0.5 * m * d * d
    return (v1 - 1e-15 * np.abs(v1)) + (v2 - 1e-15 * np.abs(v2)) - 1e-15 * (np.abs(v1) + np.abs(v2)) - 1e-300


def _qmin(glo, ghi, m, a, b):
    """rigorous lower bound, for every g in [glo, ghi], of min over d in [a, b] (a <= 0 <= b)
    of g d + m d^2/2.  For d >= 0, g d >= glo d; for d <= 0, g d >= ghi d."""
    out = np.full(np.shape(glo), np.inf)
    for g, lo_, hi_ in ((glo, np.zeros_like(a), b), (ghi, a, np.zeros_like(b))):
        ends = np.minimum(_q_endpoint(g, m, lo_), _q_endpoint(g, m, hi_))
        pos = m > 0
        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            vtx = -g / np.where(pos, m, 1.0)
            vval = -up(up(g * g) / dn(2.0 * np.where(pos, m, 1.0)))     # global min of the convex quadratic
        tol = 1e-12 * (np.abs(lo_) + np.abs(hi_) + 1e-300)
        certainly_out = (vtx < lo_ - tol) | (vtx > hi_ + tol)
        val = np.where(pos & ~certainly_out, vval, ends)
        out = np.minimum(out, val)
    return out


def _ivmatmul3(V, Hm):
    """rigorous enclosure (lo, hi) of V^T Hm V for float batches V, Hm (N, d, d) (midpoint-radius:
    |fl(sum) - sum| <= gamma_n sum|terms|, applied twice)."""
    n = V.shape[1]
    g = (2 * n + 2) * 2.0 ** -53 / (1 - (2 * n + 2) * 2.0 ** -53)
    T = np.einsum("nki,nkl->nil", V, Hm)                  # V^T Hm
    Terr = g * np.einsum("nki,nkl->nil", np.abs(V), np.abs(Hm))
    B = np.einsum("nil,nlj->nij", T, V)
    Berr = g * np.einsum("nil,nlj->nij", np.abs(T), np.abs(V)) + np.einsum("nil,nlj->nij", Terr, np.abs(V)) * (1 + 2 * g)
    Berr = up(Berr * (1 + 1e-12)) + 1e-300
    return dn(B - Berr), up(B + Berr)


class Pieces:
    """Arrays (n_edges, P) describing ideal spline pieces of a group of edges.
    For piece p of edge e: argument interval [kl, kr] (outward), shift tau (double),
    and coefficient enclosures of S(tau+s), S'(tau+s), S''(tau+s) in powers of s."""

    def __init__(self, polys_list, knots_list, pieces_list, zero_outside):
        n = len(polys_list)
        P = max(len(pl) for pl in pieces_list)
        self.n, self.P = n, P
        self.kl = np.full((n, P), INF)
        self.kr = np.full((n, P), -INF)
        self.tau = np.zeros((n, P))
        self.C = [[np.zeros((n, P, 2)) for _ in range(4 - d)] for d in range(3)]  # C[d][m] lo/hi
        self.t0 = np.zeros((n, 2))
        self.tK = np.zeros((n, 2))
        self.zero_outside = zero_outside
        for e in range(n):
            t, St, pcs = knots_list[e], polys_list[e], pieces_list[e]
            self.t0[e] = K.frac_iv(t[0])
            self.tK[e] = K.frac_iv(t[-1])
            for p, k in enumerate(pcs):
                self.kl[e, p] = K.frac_iv(t[k])[0]
                self.kr[e, p] = K.frac_iv(t[k + 1])[1]
                tau = float(t[k])
                self.tau[e, p] = tau
                q = km.pshift(St[k], Fr(tau))
                q = q + [Fr(0)] * (4 - len(q))
                assert len(q) == 4
                qs = [q, km.ptrim(km.pder(q)), km.ptrim(km.pder(km.pder(q)))]
                for d in range(3):
                    qq = qs[d] + [Fr(0)] * (4 - d - len(qs[d]))
                    for m in range(4 - d):
                        self.C[d][m][e, p] = K.frac_iv(qq[m])

    def eval(self, Z, need=(0, 1, 2)):
        """Z: NI broadcastable to (N, n).  Returns dict d -> NI (N, n) enclosing S^(d) over Z."""
        out = {}
        shape = np.broadcast_shapes(Z.lo.shape, (self.n,))
        for d in need:
            out[d] = NI(np.full(shape, INF), np.full(shape, -INF))
        for p in range(self.P):
            kl, kr, tau = self.kl[:, p], self.kr[:, p], self.tau[:, p]
            slo = np.maximum(Z.lo, kl)
            shi = np.minimum(Z.hi, kr)
            valid = slo <= shi
            if not valid.any():
                continue
            slo = np.where(valid, slo, tau)
            shi = np.where(valid, shi, tau)
            S = NI(dn(slo - tau), up(shi - tau))
            for d in need:
                C = [NI(self.C[d][m][:, p, 0], self.C[d][m][:, p, 1]) for m in range(4 - d)]
                R = K.poly_range(C, S)
                o = out[d]
                out[d] = NI(np.where(valid, np.minimum(o.lo, R.lo), o.lo), np.where(valid, np.maximum(o.hi, R.hi), o.hi))
        if self.zero_outside:
            outside = (Z.lo < self.t0[:, 1]) | (Z.hi > self.tK[:, 0])
            for d in need:
                o = out[d]
                out[d] = NI(np.where(outside, np.minimum(o.lo, 0.0), o.lo), np.where(outside, np.maximum(o.hi, 0.0), o.hi))
        for d in need:
            assert np.all(out[d].lo <= out[d].hi), "argument outside every piece"
        return out

    def feval(self, z):
        """float evaluation (for local search): z shape (N, n) -> S, S' (N, n)."""
        z = np.broadcast_to(z, np.broadcast_shapes(z.shape, (self.n,)))
        val = np.zeros(z.shape)
        der = np.zeros(z.shape)
        done = np.zeros(z.shape, dtype=bool)
        for p in range(self.P):
            m = (z >= self.kl[:, p]) & (z <= self.kr[:, p]) & ~done
            s = z - self.tau[:, p]
            c = [0.5 * (self.C[0][k][:, p, 0] + self.C[0][k][:, p, 1]) for k in range(4)]
            v = ((c[3] * s + c[2]) * s + c[1]) * s + c[0]
            dv = (3 * c[3] * s + 2 * c[2]) * s + c[1]
            val = np.where(m, v, val)
            der = np.where(m, dv, der)
            done |= m
        return val, der


class Net:
    def __init__(self, name):
        M = km.decode(name)
        self.M = M
        E = M["edges"]
        self.d = len(M["inputs"])
        self.n = len(M["hidden"])
        # input box (outward doubles)
        self.ulo = np.array([K.frac_iv(a)[0] for a, b in M["input_box"]])
        self.uhi = np.array([K.frac_iv(b)[1] for a, b in M["input_box"]])
        # error bounds (exact rationals) ---------------------------------
        eps1 = {}
        self.L1 = []
        for i in range(self.d):
            polys, knots, pcs, ws, wb = [], [], [], [], []
            for j, Hd in enumerate(M["hidden"]):
                (k,) = [k for k in Hd["edges"] if E[k]["src"] == i]
                Ed = E[k]
                a, b = M["input_box"][i]
                err, allowed, t, St = km.spline_error(M, Ed, a, b)
                eps1[(i, j)] = abs(Ed["ws"]) * err
                pc = [kk for kk in range(len(t) - 1) if t[kk] <= b and t[kk + 1] >= a]
                polys.append(St); knots.append(t); pcs.append(pc)
                ws.append(Ed["ws"]); wb.append(Ed["wb"])
            self.L1.append(dict(P=Pieces(polys, knots, pcs, False), ws=K.NIarr(ws), wb=K.NIarr(wb)))
        self.eta = [sum(eps1[(i, j)] for i in range(self.d)) for j in range(self.n)]
        polys, knots, pcs, ws, wb = [], [], [], [], []
        self.delta2 = []
        for j, Hd in enumerate(M["hidden"]):
            (k,) = [k for k in M["out"]["edges"] if E[k]["src"] == j]
            Ed = E[k]
            a, b = Hd["box"]
            err, allowed, t, St = km.spline_error(M, Ed, a, b)
            self.delta2.append(abs(Ed["ws"]) * err)
            polys.append(St); knots.append(t); pcs.append(list(range(len(t) - 1)))
            ws.append(Ed["ws"]); wb.append(Ed["wb"])
        self.L2 = dict(P=Pieces(polys, knots, pcs, True), ws=K.NIarr(ws), wb=K.NIarr(wb))
        self.beta = K.NIarr([Hd["bias"] for Hd in M["hidden"]])
        self.beta0 = K.NIq(M["out"]["bias"])
        self.A = K.NIq(M["A"])
        self.B = K.NIq(M["B"])
        self.hlo = np.array([K.frac_iv(Hd["box"][0] - self.eta[j])[0] for j, Hd in enumerate(M["hidden"])])
        self.hhi = np.array([K.frac_iv(Hd["box"][1] + self.eta[j])[1] for j, Hd in enumerate(M["hidden"])])
        self.hlo_exact = np.array([K.frac_iv(Hd["box"][0])[1] for Hd in M["hidden"]])   # inner, for primal checks
        self.hhi_exact = np.array([K.frac_iv(Hd["box"][1])[0] for Hd in M["hidden"]])
        # Lipschitz constants of psi~_j on [L_j - eta_j, U_j + eta_j] (fine subdivision)
        Hs = []
        for j in range(self.n):
            g = np.linspace(self.hlo[j], self.hhi[j], 4001)
            Hs.append((g[:-1], g[1:]))
        lo = np.stack([h[0] for h in Hs], axis=1)
        hi = np.stack([h[1] for h in Hs], axis=1)
        Z = NI(lo, hi)
        S = self.L2["P"].eval(Z, need=(1,))[1]
        D = self.L2["ws"] * S + self.L2["wb"] * K.dsilu_range(Z)
        lip = np.maximum(np.abs(D.lo), np.abs(D.hi)).max(axis=0)
        self.lip = [Fr(float(up(x))) for x in lip]
        absA = abs(M["A"])
        self.Apos = M["A"] > 0
        self.Delta = absA * sum(self.delta2[j] + self.lip[j] * self.eta[j] for j in range(self.n))

    # ---- interval evaluation ------------------------------------------------
    def layer1(self, lo, hi, need=(0, 1)):
        """per input i: Phi (N, n) and Phi' (N, n) over boxes."""
        res = []
        for i in range(self.d):
            Z = NI(lo[:, i:i + 1], hi[:, i:i + 1])
            L = self.L1[i]
            S = L["P"].eval(Z, need=need)
            out = {}
            if 0 in need:
                out[0] = L["ws"] * S[0] + L["wb"] * K.silu_range(Z)
            if 1 in need:
                out[1] = L["ws"] * S[1] + L["wb"] * K.dsilu_range(Z)
            if 2 in need:
                out[2] = L["ws"] * S[2] + L["wb"] * K.d2silu_range(Z)
            res.append(out)
        return res

    def layer2(self, H, need=(0, 1)):
        L = self.L2
        S = L["P"].eval(H, need=need)
        out = {}
        if 0 in need:
            out[0] = L["ws"] * S[0] + L["wb"] * K.silu_range(H)
        if 1 in need:
            out[1] = L["ws"] * S[1] + L["wb"] * K.dsilu_range(H)
        if 2 in need:
            out[2] = L["ws"] * S[2] + L["wb"] * K.d2silu_range(H)
        return out

    def hsum(self, Phis):
        H = self.beta + Phis[0][0]
        for i in range(1, self.d):
            H = H + Phis[i][0]
        return H

    def fval_box(self, H):
        """A (beta0 + sum_j psi(H_j)) + B for NI H (N, n)."""
        Ps = self.layer2(H, need=(0,))[0]
        s = self.beta0 + Ps[:, 0]
        for j in range(1, self.n):
            s = s + Ps[:, j]
        return self.A * s + self.B

    def point(self, c):
        """rigorous enclosure of f~(c) and h~(c) at float points c (N, d)."""
        Ph = self.layer1(c, c, need=(0,))
        H = self.hsum(Ph)
        return self.fval_box(H), H

    def _hessians(self, Pd1, Pd2, D1, D2):
        """interval Hessian  A sum_j [psi_j'' g_j g_j^T + psi_j' diag(phi_ij'')]  (N, d, d) as (lo, hi)."""
        d = self.d
        Hlo = [[None] * d for _ in range(d)]
        Hhi = [[None] * d for _ in range(d)]
        for i in range(d):
            for k in range(i, d):
                t = D2 * (Pd1[i] * Pd1[k])                # (N, n)
                if i == k:
                    t = t + D1 * Pd2[i]
                ssum = t[:, 0]
                for j in range(1, self.n):
                    ssum = ssum + t[:, j]
                ssum = ssum * self.A
                Hlo[i][k] = Hlo[k][i] = ssum.lo
                Hhi[i][k] = Hhi[k][i] = ssum.hi
        return (np.stack([np.stack(r, axis=1) for r in Hlo], axis=1),
                np.stack([np.stack(r, axis=1) for r in Hhi], axis=1))

    def _hess_bound(self, lo, hi, c, fc, hc, H, Ph, Ph2, Phc12, D1c, L2):
        N, d = lo.shape
        # point Hessian and gradient at c (intervals)
        D2c = self.layer2(hc, need=(2,))[2]
        HcL, HcH = self._hessians([Phc12[i][1] for i in range(d)], [Phc12[i][2] for i in range(d)], D1c, D2c)
        gl, gh = [], []
        for i in range(d):
            t = D1c * Phc12[i][1]
            ssum = t[:, 0]
            for j in range(1, self.n):
                ssum = ssum + t[:, j]
            ssum = ssum * self.A
            gl.append(ssum.lo); gh.append(ssum.hi)
        gl = np.stack(gl, axis=1); gh = np.stack(gh, axis=1)
        # box Hessian (intervals)
        HbL, HbH = self._hessians([Ph[i][1] for i in range(d)], [Ph2[i][2] for i in range(d)], L2[1], L2[2])
        Hm = 0.5 * (HcL + HcH)
        Hm = 0.5 * (Hm + np.transpose(Hm, (0, 2, 1)))
        # R >= |H(xi) - Hm| for xi in the box (the box Hessian contains the center Hessian)
        R = up(np.maximum(np.abs(up(HbH - Hm)), np.abs(up(Hm - HbL))))
        gm = 0.5 * (gl + gh)
        grad_rad = up(np.maximum(gh - gm, gm - gl))
        a = dn(lo - c); b = up(hi - c)
        r = np.maximum(-a, b)
        out = np.full(N, -np.inf)
        # rigorous positive definiteness of Hm via congruence with float eigenvectors + Gershgorin
        try:
            w, V = np.linalg.eigh(Hm)
        except np.linalg.LinAlgError:
            return out
        B = _ivmatmul3(V, Hm)                 # V^T Hm V (interval, lo/hi)
        Blo, Bhi = B
        offmax = np.maximum(np.abs(Blo), np.abs(Bhi))
        idx = np.arange(d)
        offmax[:, idx, idx] = 0.0
        gersh = dn(Blo[:, idx, idx] - up(offmax.sum(axis=2) * (1 + 1e-15)))
        pd = np.all(gersh > 0, axis=1)
        if not pd.any():
            return out
        # approximate box-QP minimizer y of gm.d + d^T Hm d / 2 (projected Newton steps)
        y = np.zeros((N, d))
        with np.errstate(all="ignore"):
            Hinv_g = np.linalg.solve(np.where(pd[:, None, None], Hm, np.eye(d)[None]), gm[:, :, None])[:, :, 0]
        y = np.clip(-Hinv_g, a, b)
        diag = np.maximum(Hm[:, idx, idx], 1e-300)
        for _ in range(30):     # coordinate descent on the box QP
            for i in range(d):
                gi = gm[:, i] + np.einsum("nk,nk->n", Hm[:, i, :], y) - Hm[:, i, i] * y[:, i]
                y[:, i] = np.clip(-gi / diag[:, i], a[:, i], b[:, i])
        # q(d) >= q(y) + rho.(d - y), rho = gm + Hm y   (convexity of q, Hm psd)
        Y = NI(y)
        Hq = NI(Hm)
        HY = None
        for k in range(d):
            t = Hq[:, :, k] * Y[:, k:k + 1]
            HY = t if HY is None else HY + t                    # (N, d)
        rho = HY + NI(gm)
        qy = None
        for i in range(d):
            t = Y[:, i] * (NI(gm[:, i]) + HY[:, i] * 0.5)
            qy = t if qy is None else qy + t
        lin = qy
        for i in range(d):
            Di = NI(a[:, i], b[:, i]) - Y[:, i]
            lin = lin + rho[:, i] * Di
        # penalties: gradient radius and Hessian deviation
        pen = (grad_rad * r).sum(axis=1) + 0.5 * np.einsum("ni,nik,nk->n", r, R, r)
        pen = up(pen * (1 + 1e-12)) + 1e-300
        val = dn(dn(fc.lo + lin.lo) - pen)
        return np.where(pd, val, -np.inf)

    def bound(self, lo, hi):
        """returns dict with lb, feasible mask, fully-feasible mask, gradient enclosure."""
        N = lo.shape[0]
        Ph = self.layer1(lo, hi, need=(0, 1))
        H = self.hsum(Ph)
        infeas = np.any((H.hi < self.hlo) | (H.lo > self.hhi), axis=1)
        full = np.all((H.lo >= self.hlo) & (H.hi <= self.hhi), axis=1)
        Hc = K.meet(H, self.hlo, self.hhi)
        Hc = NI(np.where(Hc.lo <= Hc.hi, Hc.lo, H.lo), np.where(Hc.lo <= Hc.hi, Hc.hi, H.hi))
        nat = self.fval_box(Hc).lo
        # mean-value form
        c = 0.5 * (lo + hi)
        Phc = self.layer1(c, c, need=(0,))
        hc = self.hsum(Phc)
        fc = self.fval_box(hc)
        L2 = self.layer2(H, need=(1, 2))
        D2 = L2[1]                                    # psi'(H) (N, n)
        G = []
        for i in range(self.d):
            g = D2 * Ph[i][1]                          # (N, n)
            gs = g[:, 0]
            for j in range(1, self.n):
                gs = gs + g[:, j]
            G.append(self.A * gs)
        acc = fc
        for i in range(self.d):
            acc = acc + G[i] * NI(dn(lo[:, i] - c[:, i]), up(hi[:, i] - c[:, i]))
        mvf = acc.lo
        # second-order form with affine splitting of the psi-curvature:
        #   psi_j(h) >= psi_j(hc) + psi_j'(hc) s_j + M_j s_j^2/2,  s_j = h_j - hc_j in S_j = H_j - hc_j,
        #   M_j <= min psi_j'' on H_j.  M_j s^2/2 >= mu_j s + kappa_j on S_j  (tangent if M_j > 0, secant if M_j <= 0),
        #   s_j = sum_i (phi_ij(u_i) - phi_ij(c_i)), so the bound separates over inputs:
        #   f >= f(c) + A [sum_j kappa_j + sum_i min_d (gt_i d + mt_i d^2/2)],
        #   gt_i = sum_j (psi_j'(hc) + mu_j) phi_ij'(c_i),  mt_i <= min_{U_i} sum_j (psi_j'(hc) + mu_j) phi_ij''.
        # mu_j (any value is valid) comes from the minimizer of the quadratic model.
        if self.Apos:
            D1c = self.layer2(hc, need=(1,))[1]            # psi'(hc)  (N, n)
            Ph2 = self.layer1(lo, hi, need=(2,))
            Phc12 = self.layer1(c, c, need=(1, 2))
            M = L2[2].lo                                    # (N, n) lower bounds of psi''
            slo = dn(H.lo - hc.hi); shi = up(H.hi - hc.lo)  # S_j
            A_ = float(0.5 * (self.A.lo + self.A.hi))
            # --- choose mu from the quadratic model (floats) ---
            Jm = np.stack([0.5 * (Phc12[i][1].lo + Phc12[i][1].hi) for i in range(self.d)], axis=2)   # (N, n, d)
            psi1 = 0.5 * (D1c.lo + D1c.hi)
            gm = A_ * np.einsum("nj,nji->ni", psi1, Jm)
            m0 = A_ * np.stack([np.einsum("nj,nj->n", psi1, 0.5 * (Phc12[i][2].lo + Phc12[i][2].hi)) for i in range(self.d)], axis=1)
            Mp = np.maximum(M, 0.0)
            Hq = A_ * np.einsum("nji,nj,njk->nik", Jm, Mp, Jm)
            Hq[:, np.arange(self.d), np.arange(self.d)] += np.maximum(m0, 0.0) + 1e-9 * (1 + np.abs(Hq[:, np.arange(self.d), np.arange(self.d)]))
            try:
                dstar = -np.linalg.solve(Hq, gm[:, :, None])[:, :, 0]
            except np.linalg.LinAlgError:
                dstar = np.zeros((N, self.d))
            dstar = np.where(np.isfinite(dstar), dstar, 0.0)
            dstar = np.clip(dstar, lo - c, hi - c)
            sstar = np.einsum("nji,ni->nj", Jm, dstar)
            sstar = np.clip(sstar, slo, shi)
            convex = M > 0
            mu = np.where(convex, M * sstar, 0.5 * M * (slo + shi))
            # kappa_j (rigorous lower bounds): tangent: -M s0^2/2 ; secant: -M slo shi/2
            kt = -(0.5 * M * sstar * sstar) * (1 + 1e-15) - 1e-300
            ks = -(0.5 * M * slo * shi)
            ks = ks - 1e-15 * np.abs(ks) - 1e-300
            kap = np.where(convex, kt, ks)
            # tangent validity: M s^2/2 >= mu s - M s0^2/2 holds for all s when M > 0 (mu = M s0 exactly
            # up to rounding: the rounding of mu is absorbed because we recompute the minorant check below)
            # --- rigorous separable evaluation ---
            MU = NI(mu)
            coef = D1c + MU                                 # (N, n) intervals psi'(hc) + mu
            total = fc.lo.copy()
            qsum = np.zeros(N)
            for i in range(self.d):
                gi = coef * Phc12[i][1]
                gs = gi[:, 0]
                for j in range(1, self.n):
                    gs = gs + gi[:, j]
                gs = gs * self.A
                mi = coef * Ph2[i][2]
                ms = mi[:, 0]
                for j in range(1, self.n):
                    ms = ms + mi[:, j]
                ms = (ms * self.A).lo
                a = dn(lo[:, i] - c[:, i]); b = up(hi[:, i] - c[:, i])
                qsum = qsum + _qmin(gs.lo, gs.hi, ms, a, b)
            # exact minorant constant: min over s in S_j of (M s^2/2 - mu s) >= kappa'_j (computed rigorously)
            kap2 = _qmin(-mu, -mu, M, np.minimum(slo, 0.0), np.maximum(shi, 0.0))
            ksum = kap2.sum(axis=1)
            ksum = ksum - 1e-12 * np.abs(kap2).sum(axis=1) - 1e-300
            Ahi = float(self.A.hi); Alo = float(self.A.lo)
            kobj = np.where(ksum >= 0, ksum * Alo, ksum * Ahi)
            kobj = kobj - 1e-15 * np.abs(kobj)
            sep = total + qsum * (1 + 1e-12 * np.sign(-qsum)) + kobj
            sep = sep - 1e-13 * (np.abs(total) + np.abs(qsum) + np.abs(kobj)) - 1e-300
            mvf = np.maximum(mvf, sep)
            # third-order form: exact (interval) Hessian at c plus Hessian variation over the box.
            h3 = self._hess_bound(lo, hi, c, fc, hc, H, Ph, Ph2, Phc12, D1c, L2)
            mvf = np.maximum(mvf, h3)
        lb = np.maximum(nat, mvf)
        lb = np.where(infeas, INF, lb)
        cfeas = np.all((hc.lo >= self.hlo) & (hc.hi <= self.hhi), axis=1)
        ub = np.where(cfeas, fc.hi, INF)
        return dict(lb=lb, full=full & ~infeas, G=G, ub=ub, c=c)

    # ---- float model for local search -------------------------------------
    def ffun(self, u):
        u = np.atleast_2d(u)
        H = np.tile(0.5 * (self.beta.lo + self.beta.hi), (u.shape[0], 1))
        dH = []
        for i in range(self.d):
            z = u[:, i:i + 1]
            L = self.L1[i]
            S, dS = L["P"].feval(z)
            ws = 0.5 * (L["ws"].lo + L["ws"].hi); wb = 0.5 * (L["wb"].lo + L["wb"].hi)
            sg = 1 / (1 + np.exp(-z))
            H = H + ws * S + wb * z * sg
            dH.append(ws * dS + wb * sg * (1 + z * (1 - sg)))
        L = self.L2
        S, dS = L["P"].feval(H)
        ws = 0.5 * (L["ws"].lo + L["ws"].hi); wb = 0.5 * (L["wb"].lo + L["wb"].hi)
        sg = 1 / (1 + np.exp(-H))
        psi = ws * S + wb * H * sg
        dpsi = ws * dS + wb * sg * (1 + H * (1 - sg))
        A = float(self.M["A"]); B = float(self.M["B"]); b0 = float(self.M["out"]["bias"])
        f = A * (b0 + psi.sum(axis=1)) + B
        g = np.stack([A * (dpsi * dH[i]).sum(axis=1) for i in range(self.d)], axis=1)
        return f, g, H


def local_search(net, starts, seed=0):
    from scipy.optimize import minimize
    best = (INF, None)
    lo_h, hi_h = net.hlo_exact, net.hhi_exact
    bnds = list(zip(net.ulo, net.uhi))

    def fun(u):
        f, g, H = net.ffun(u)
        return f[0], g[0]

    def cons(u):
        f, g, H = net.ffun(u)
        return np.concatenate([H[0] - lo_h, hi_h - H[0]]) - 1e-12

    for u0 in starts:
        try:
            r = minimize(fun, u0, jac=True, bounds=bnds, method="SLSQP",
                         constraints=[dict(type="ineq", fun=cons)], options=dict(maxiter=500, ftol=1e-15))
        except Exception:
            continue
        u = np.clip(r.x, net.ulo, net.uhi)
        f, g, H = net.ffun(u)
        if np.all(H[0] >= lo_h) and np.all(H[0] <= hi_h) and f[0] < best[0]:
            best = (f[0], u)
    return best


def branch_and_bound(net, tol_abs, tlim, u_inc=None, batch=4096, log=print, maxboxes=30_000_000):
    t0 = time.time()
    d = net.d
    UB, ubpt = INF, None
    if u_inc is not None:
        fc, hc = net.point(u_inc[None, :])
        if np.all((hc.lo >= net.hlo) & (hc.hi <= net.hhi)):
            UB, ubpt = float(fc.hi[0]), u_inc.copy()
    lo = net.ulo[None, :].copy()
    hi = net.uhi[None, :].copy()
    key = np.array([-INF])
    fathomed_min = INF
    nproc = 0
    it = 0
    while lo.shape[0] > 0:
        it += 1
        if time.time() - t0 > tlim or nproc > maxboxes:
            break
        m = min(batch, lo.shape[0])
        if lo.shape[0] > m:
            idx = np.argpartition(key, m - 1)[:m]
            rest = np.ones(lo.shape[0], bool); rest[idx] = False
            blo, bhi = lo[idx], hi[idx]
            lo, hi, key = lo[rest], hi[rest], key[rest]
        else:
            blo, bhi = lo, hi
            lo, hi, key = lo[:0], hi[:0], key[:0]
        nproc += blo.shape[0]
        R = net.bound(blo, bhi)
        # incumbent from centers
        j = np.argmin(R["ub"])
        if R["ub"][j] < UB:
            UB, ubpt = float(R["ub"][j]), R["c"][j].copy()
        lb = R["lb"]
        keep = lb < UB - tol_abs
        fath = (~keep) & (lb <= UB)
        if fath.any():
            fathomed_min = min(fathomed_min, float(lb[fath].min()))
        blo, bhi, lbk = blo[keep], bhi[keep], lb[keep]
        G = [g[keep] for g in R["G"]]
        full = R["full"][keep]
        # monotonicity test on fully feasible boxes: collapse to the minimizing face;
        # collapsed boxes are re-queued and re-bounded (their lb is stale)
        mod = np.zeros(blo.shape[0], bool)
        for i in range(d):
            pos = full & (G[i].lo > 0) & (bhi[:, i] > blo[:, i])
            neg = full & (G[i].hi < 0) & (bhi[:, i] > blo[:, i])
            bhi[pos, i] = blo[pos, i]
            blo[neg, i] = bhi[neg, i]
            mod |= pos | neg
        if mod.any():
            lo = np.concatenate([lo, blo[mod]]); hi = np.concatenate([hi, bhi[mod]])
            key = np.concatenate([key, lbk[mod]])
            blo, bhi, lbk = blo[~mod], bhi[~mod], lbk[~mod]
            G = [g[~mod] for g in G]
        w = bhi - blo
        if w.shape[0] == 0:
            continue
        smear = np.stack([np.maximum(np.abs(G[i].lo), np.abs(G[i].hi)) * w[:, i] for i in range(d)], axis=1)
        k = np.argmax(smear, axis=1)
        r = np.arange(len(k))
        small = w[r, k] <= 1e-15 * np.maximum(1.0, np.abs(blo[r, k]))
        k = np.where(small, np.argmax(w, axis=1), k)
        tiny = w[r, k] <= 1e-15 * np.maximum(1.0, np.abs(blo[r, k]))
        if tiny.any():
            # (numerically) a point whose bound was computed in this pass: record it
            fathomed_min = min(fathomed_min, float(lbk[tiny].min()))
            blo, bhi, lbk, k = blo[~tiny], bhi[~tiny], lbk[~tiny], k[~tiny]
        r = np.arange(len(k))
        mid = 0.5 * (blo[r, k] + bhi[r, k])
        lo1, hi1 = blo.copy(), bhi.copy(); hi1[r, k] = mid
        lo2, hi2 = blo.copy(), bhi.copy(); lo2[r, k] = mid
        lo = np.concatenate([lo, lo1, lo2]); hi = np.concatenate([hi, hi1, hi2])
        key = np.concatenate([key, lbk, lbk])
        if it % 200 == 0:
            glb = min(fathomed_min, key.min() if key.size else INF, UB)
            log(f"  it {it} processed {nproc} open {lo.shape[0]} UB {UB:.15g} LB {glb:.15g} t {time.time()-t0:.0f}s")
    open_min = key.min() if key.size else INF
    LB = min(fathomed_min, open_min, UB)
    done = lo.shape[0] == 0
    return dict(LB=LB, UB=UB, u=ubpt, processed=nproc, open=lo.shape[0], done=done, time=time.time() - t0)


def main(name, tol_rel=1e-10, tlim=3600.0, nstarts=40):
    print(f"== {name}")
    net = Net(name)
    M = net.M
    print(f"inputs {net.d}, hidden {net.n}, A = {float(M['A'])}, B = {float(M['B'])}")
    print(f"eta_j = {[float(x) for x in net.eta]}")
    print(f"delta2_j = {[float(x) for x in net.delta2]}, Lip_j = {[float(x) for x in net.lip]}")
    print(f"Delta (model vs ideal objective) <= {float(net.Delta):.3e}")
    rng = np.random.default_rng(0)
    starts = [net.ulo + (net.uhi - net.ulo) * rng.random(net.d) for _ in range(nstarts)]
    t0 = time.time()
    fbest, ubest = local_search(net, starts)
    print(f"local search: {fbest!r} at {ubest.tolist() if ubest is not None else None} ({time.time()-t0:.1f}s)")
    tol_abs = tol_rel * max(1.0, abs(fbest))
    res = branch_and_bound(net, tol_abs, tlim, u_inc=ubest)
    Delta_f = float(up(float(net.Delta)))
    lb_cert = float(dn(res["LB"] - Delta_f))
    print(f"B&B: done={res['done']} processed {res['processed']} open {res['open']} time {res['time']:.0f}s")
    print(f"  min f~ in [{res['LB']!r}, {res['UB']!r}]   tol_abs {tol_abs:.2e}")
    print(f"  certified dual bound for the OSIL model: {lb_cert!r}")
    print(f"  best point u = {res['u'].tolist()}")
    return net, res, lb_cert


if __name__ == "__main__":
    name = sys.argv[1]
    tol = float(sys.argv[2]) if len(sys.argv) > 2 else 1e-10
    tl = float(sys.argv[3]) if len(sys.argv) > 3 else 3600
    main(name, tol, tl)


def make_bound_fn(net):
    """adapter for bbcore.run (monotonicity test on fully feasible boxes)."""
    def fn(lo, hi):
        R = net.bound(lo, hi)
        G = R["G"]
        d = lo.shape[1]
        w = hi - lo
        smear = np.stack([np.maximum(np.abs(G[i].lo), np.abs(G[i].hi)) * w[:, i] for i in range(d)], axis=1)
        nlo, nhi = lo.copy(), hi.copy()
        mod = np.zeros(lo.shape[0], bool)
        full = R["full"]
        for i in range(d):
            pos = full & (G[i].lo > 0) & (hi[:, i] > lo[:, i])
            neg = full & (G[i].hi < 0) & (hi[:, i] > lo[:, i])
            nhi[pos, i] = lo[pos, i]
            nlo[neg, i] = hi[neg, i]
            mod |= pos | neg
        return dict(lb=R["lb"], ub=R["ub"], x=R["c"], smear=smear, newlo=nlo, newhi=nhi, mod=mod)
    return fn


def main2(name, tol_rel=1e-10, tlim=3600.0, nstarts=40):
    sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave3")
    import bbcore
    print(f"== {name}")
    net = Net(name)
    M = net.M
    print(f"inputs {net.d}, hidden {net.n}, A = {float(M['A'])}, B = {float(M['B'])}")
    print(f"eta_j = {[float(x) for x in net.eta]}")
    print(f"delta2_j = {[float(x) for x in net.delta2]}, Lip_j = {[float(x) for x in net.lip]}")
    print(f"Delta (model vs ideal objective) <= {float(net.Delta):.3e}")
    rng = np.random.default_rng(0)
    starts = [net.ulo + (net.uhi - net.ulo) * rng.random(net.d) for _ in range(nstarts)]
    t0 = time.time()
    fbest, ubest = local_search(net, starts)
    print(f"local search: {fbest!r} at {ubest.tolist() if ubest is not None else None} ({time.time()-t0:.1f}s)")
    tol_abs = tol_rel * max(1.0, abs(fbest))
    UB = INF
    if ubest is not None:
        fc, hc = net.point(ubest[None, :])
        if np.all((hc.lo >= net.hlo) & (hc.hi <= net.hhi)):
            UB = float(fc.hi[0])
    res = bbcore.run(make_bound_fn(net), net.ulo, net.uhi, tol_abs, tlim, UB=UB, xbest=ubest)
    res["u"] = res["x"]
    Delta_f = float(up(float(net.Delta)))
    lb_cert = float(dn(res["LB"] - Delta_f))
    print(f"B&B: done={res['done']} processed {res['processed']} open {res['open']} time {res['time']:.0f}s")
    print(f"  min f~ in [{res['LB']!r}, {res['UB']!r}]   tol_abs {tol_abs:.2e}")
    print(f"  certified dual bound for the OSIL model: {lb_cert!r}")
    print(f"  best point u = {res['u'].tolist()}")
    return net, res, lb_cert
