"""Second-order + LP bounding for the eg_* minimax problems (rigorous).

For a box X = c + [-r, r] (integers relaxed to their interval) and every row k,
Taylor's theorem with the Lagrange remainder gives, for x = c + d in X,
    g_k(c) + grad g_k(c).d - rho_k  <=  g_k(x)  <=  g_k(c) + grad g_k(c).d + rho_k^+
with explicit remainder bounds built term by term: for a term a e^E,
    d^T Hess(a e^E) d = a e^E ((grad E.d)^2 + d^T Hess E d),
    Hess E = diag(2 gamma_i s_i^2) (negative), so with Emax = max_X E,
    lower part: a > 0: >= -a e^Emax sum 2|gamma_i| s_i^2 r_i^2 ;  a < 0: >= -|a| e^Emax (sum |E_i|max r_i)^2
    upper part: a > 0: <=  a e^Emax (sum |E_i|max r_i)^2 ;       a < 0: <=  |a| e^Emax sum 2|gamma_i| s_i^2 r_i^2
and rho = half of the summed parts.  The objective rows then give the affine minimax
    min_{d in box} max_k (c_k + g_k(c) - rho_k + grad g_k(c).d)
and the side rows give affine constraints (valid relaxation of the feasible set).
Any dual vector (y >= 0 on objective rows, z >= 0 on side rows) gives the rigorous
bound  [sum y_k A_k(d) + sum z_s S_s(d)] / sum y_k minimized over the box in closed
form, evaluated in interval arithmetic; the dual vector comes from an LP solve
(HiGHS).  The natural interval bound of eg_bb.Prob is kept as well (max of both).
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import sys
import time

import numpy as np
from scipy.optimize import linprog

sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave3/kan")
sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave3")
import kan_iv as K  # noqa: E402
from kan_iv import NI, dn, up  # noqa: E402

import eg_bb as eb  # noqa: E402

INF = np.inf


class Prob2(eb.Prob):
    def __init__(self, name):
        super().__init__(name)
        # |2 gamma s^2| upper bounds per (i, k, m)
        self.G2 = [up(np.abs(2.0 * self.GA[i].lo) * (self.S[i].hi ** 2) * (1 + 1e-15)) for i in range(self.d)]
        self.Aabs = np.maximum(np.abs(self.A.lo), np.abs(self.A.hi))
        self.Apos = self.A.lo > 0
        self.Aneg = self.A.hi < 0
        assert np.all(self.Apos | self.Aneg)

    def center_data(self, c):
        """rigorous g_k(c) and grad g_k(c) at float points c (N, d)."""
        N = c.shape[0]
        E = None
        Ts = []
        for i in range(self.d):
            X = NI(c[:, i][:, None, None])
            T = self.MU[i] + self.S[i] * X
            Ts.append(T)
            q = self.GA[i] * eb.isq(T)
            E = q if E is None else E + q
        ex = NI(K.iexp_pt_fast(E.lo).lo, K.iexp_pt_fast(E.hi).hi)
        W = self.A * ex
        g = self._sum(W)
        for i in range(self.d):
            g = g + self.LI[i] * NI(c[:, i][:, None])
        grads = []
        for i in range(self.d):
            dT = W * (self.GA[i] * (Ts[i] * (self.S[i] * 2.0)))
            grads.append(self._sum(dT) + self.LI[i])
        return g, grads

    def remainders(self, lo, hi, r):
        """rho_lo, rho_hi (N, R) upper bounds of the second-order remainders over the boxes."""
        E = None
        Eabs = []
        for i in range(self.d):
            X = NI(lo[:, i][:, None, None], hi[:, i][:, None, None])
            T = self.MU[i] + self.S[i] * X
            q = self.GA[i] * eb.isq(T)
            E = q if E is None else E + q
            dE = self.GA[i] * (T * (self.S[i] * 2.0))
            Eabs.append(np.maximum(np.abs(dE.lo), np.abs(dE.hi)))
        emax = K.iexp_pt_fast(E.hi).hi                       # (N, R, M)
        s1 = None   # sum 2|gamma| s^2 r^2
        s2 = None   # (sum |E_i| r_i)
        for i in range(self.d):
            ri = r[:, i][:, None, None]
            t1 = self.G2[i] * (ri * ri)
            t2 = Eabs[i] * ri
            s1 = t1 if s1 is None else s1 + t1
            s2 = t2 if s2 is None else s2 + t2
        s2 = s2 * s2
        amp = self.Aabs * emax
        lowpart = np.where(self.Apos, amp * s1, amp * s2)
        highpart = np.where(self.Apos, amp * s2, amp * s1)
        f = 1 + 1e-12
        rho_lo = 0.5 * lowpart.sum(axis=2) * f + 1e-300
        rho_hi = 0.5 * highpart.sum(axis=2) * f + 1e-300
        return up(rho_lo), up(rho_hi)

    def bound2(self, lo, hi):
        N = lo.shape[0]
        lb_nat, Gnat, enc = self.bound(lo, hi)          # natural + MVF (eg_bb)
        c = 0.5 * (lo + hi)
        r = up(np.maximum(hi - c, c - lo))
        gc, grads = self.center_data(c)
        rho_lo, rho_hi = self.remainders(lo, hi, r)
        obj = self.objrows
        side = np.where(~obj)[0]
        lb = lb_nat.copy()
        for n in range(N):
            if not np.isfinite(lb[n]) or lb[n] >= self._UB - self._tol:
                continue
            if rho_lo[n, obj].max() > 1e3:
                continue
            # LP data (floats) for the dual vector
            a = self.c[obj] + gc.lo[n, obj] - rho_lo[n, obj]
            B = np.stack([0.5 * (grads[i].lo[n, obj] + grads[i].hi[n, obj]) for i in range(self.d)], axis=1)
            A_ub = [np.hstack([B, -np.ones((obj.sum(), 1))])]
            b_ub = [-a]
            srows = []
            for s in side:
                bs = np.array([0.5 * (grads[i].lo[n, s] + grads[i].hi[n, s]) for i in range(self.d)])
                if np.isfinite(self.ghi[s]):   # g >= gc + b.d - rho_lo must be <= ghi
                    A_ub.append(np.hstack([bs, [0.0]])[None, :]); b_ub.append([self.ghi[s] - gc.lo[n, s] + rho_lo[n, s]])
                    srows.append((s, +1))
                if np.isfinite(self.glo[s]):   # g <= gc + b.d + rho_hi must be >= glo
                    A_ub.append(np.hstack([-bs, [0.0]])[None, :]); b_ub.append([gc.hi[n, s] + rho_hi[n, s] - self.glo[s]])
                    srows.append((s, -1))
            A_ub = np.vstack(A_ub); b_ub = np.concatenate(b_ub)
            bounds = [(lo[n, i] - c[n, i], hi[n, i] - c[n, i]) for i in range(self.d)] + [(None, None)]
            cost = np.zeros(self.d + 1); cost[-1] = 1.0
            res = linprog(cost, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
            if res.status != 0:     # (LP infeasibility is not exploited)
                continue
            dual = -res.ineqlin.marginals                 # >= 0
            y = np.maximum(dual[:obj.sum()], 0.0)
            z = np.maximum(dual[obj.sum():], 0.0)
            if y.sum() <= 0:
                continue
            lbn = self._dual_bound(n, y, z, srows, gc, grads, rho_lo, rho_hi, lo, hi, c)
            lb[n] = max(lb[n], lbn)
        return lb, Gnat, enc

    def _dual_bound(self, n, y, z, srows, gc, grads, rho_lo, rho_hi, lo, hi, c):
        """rigorous value of min_{d in box} [sum_k y_k (c_k + g_k(c) - rho_k + b_k.d) + sum_s z_s S_s(d)] / sum y."""
        obj = np.where(self.objrows)[0]
        Y = NI(y)
        A = NI(dn(self.c[obj] + gc.lo[n, obj] - rho_lo[n, obj]), up(self.c_hi[obj] + gc.hi[n, obj] - rho_lo[n, obj]))
        # sum y_k A_k (lower end suffices since y >= 0 and we need a lower bound)
        tot = (Y * A)
        const = NI(dn(tot.lo.sum() - 1e-15 * np.abs(tot.lo).sum()), up(tot.hi.sum() + 1e-15 * np.abs(tot.hi).sum()))
        coef = []
        for i in range(self.d):
            Bi = NI(grads[i].lo[n, obj], grads[i].hi[n, obj])
            t = Y * Bi
            ci = NI(dn(t.lo.sum() - 1e-15 * np.abs(t.lo).sum()), up(t.hi.sum() + 1e-15 * np.abs(t.hi).sum()))
            coef.append(ci)
        for (s, sgn), zz in zip(srows, z):
            if zz <= 0:
                continue
            Z = NI(zz)
            if sgn > 0:   # z (g_s(c) - rho_lo + b.d - ghi) <= 0 ... we add z*(lower-model - ghi) which is <= 0
                const = const + Z * (NI(gc.lo[n, s]) - rho_lo[n, s] - self.ghi[s])
                for i in range(self.d):
                    coef[i] = coef[i] + Z * NI(grads[i].lo[n, s], grads[i].hi[n, s])
            else:         # z (glo - g_s(c) - rho_hi - b.d) <= 0
                const = const + Z * (NI(self.glo[s]) - gc.hi[n, s] - rho_hi[n, s])
                for i in range(self.d):
                    coef[i] = coef[i] - Z * NI(grads[i].lo[n, s], grads[i].hi[n, s])
        val = const
        for i in range(self.d):
            D = NI(dn(lo[n, i] - c[n, i]), up(hi[n, i] - c[n, i]))
            val = val + coef[i] * D
        ys = NI(dn(y.sum() * (1 - 1e-15)), up(y.sum() * (1 + 1e-15)))
        # lower bound of val / ys with ys > 0
        vl = float(val.lo)
        q = vl / float(ys.hi) if vl >= 0 else vl / float(ys.lo)
        return float(dn(q)) if np.isfinite(q) else -INF
