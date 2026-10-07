"""ann_cumene_tanh: adds second-order interval AD (Hessians w.r.t. the 5 inputs) to the
level-wise forward pass and a third-order lower bound (qpbound.third_order_bound) for
the Lagrangian  L = f - sum_k lam_k s_k (x_jk - b_k)  (L <= f on feasible points).

Hessian propagation: linear levels via the same midpoint-radius sparse products;
v = tanh(u):  grad v = t1 grad u,  Hess v = t1 Hess u + t2 grad u grad u^T,
t1 = 1 - tanh^2, t2 = -2 tanh t1 (interval enclosures).  Products x_p x_r in the
objective: Hess = x_p Hess x_r + x_r Hess x_p + grad x_p grad x_r^T + grad x_r grad x_p^T.
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import sys
import time
from fractions import Fraction as Fr

import numpy as np

sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave3/kan")
sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave3")
import kan_iv as K  # noqa: E402
from kan_iv import NI, dn, up  # noqa: E402
import qpbound  # noqa: E402

import ann_bb as ab  # noqa: E402
import ann_fast as af  # noqa: E402

INF = np.inf


class H3Model(af.FastModel):
    def __init__(self):
        super().__init__()
        d = self.d
        self.pairs = [(i, k) for i in range(d) for k in range(i, d)]
        self.T = len(self.pairs)
        self.pidx = np.zeros((d, d), int)
        for p, (i, k) in enumerate(self.pairs):
            self.pidx[i, k] = self.pidx[k, i] = p

    def fforward_h(self, lo, hi):
        N = lo.shape[0]
        d, T = self.d, self.T
        Xlo = np.zeros((self.nv, N)); Xhi = np.zeros((self.nv, N))
        Glo = np.zeros((self.nv, N * d)); Ghi = np.zeros((self.nv, N * d))
        Hlo = np.zeros((self.nv, N * T)); Hhi = np.zeros((self.nv, N * T))
        for i, j in enumerate(self.inputs):
            Xlo[j] = lo[:, i]; Xhi[j] = hi[:, i]
            e = np.zeros((N, d)); e[:, i] = 1.0
            Glo[j] = e.ravel(); Ghi[j] = e.ravel()
        ii = np.array([p[0] for p in self.pairs]); kk = np.array([p[1] for p in self.pairs])
        for ent in self.levels:
            if "lin" in ent:
                E = ent["lin"]
                u = E["used"]
                ylo, yhi = self._affine(E, Xlo[u], Xhi[u])
                Xlo[E["tv"]] = ylo; Xhi[E["tv"]] = yhi
                glo, ghi = self._affine(E, Glo[u], Ghi[u], with_b=False)
                Glo[E["tv"]] = glo; Ghi[E["tv"]] = ghi
                hlo, hhi = self._affine(E, Hlo[u], Hhi[u], with_b=False)
                Hlo[E["tv"]] = hlo; Hhi[E["tv"]] = hhi
            if "tanh" in ent:
                Tn = ent["tanh"]
                m = len(Tn["tv"])
                Uu = NI(Xlo[Tn["uv"]], Xhi[Tn["uv"]])
                Tt = ab.tanh_range(Uu)
                Xlo[Tn["tv"]] = Tt.lo; Xhi[Tn["tv"]] = Tt.hi
                t1 = NI(1.0) - ab.isq(Tt)                      # (m, N)
                t2 = Tt * t1 * (-2.0)
                Gu = NI(Glo[Tn["uv"]].reshape(m, N, d), Ghi[Tn["uv"]].reshape(m, N, d))
                Gv = Gu * NI(t1.lo[:, :, None], t1.hi[:, :, None])
                Glo[Tn["tv"]] = Gv.lo.reshape(m, N * d); Ghi[Tn["tv"]] = Gv.hi.reshape(m, N * d)
                outer = Gu[:, :, ii] * Gu[:, :, kk]            # (m, N, T)
                diagm = ii == kk
                sq = ab.isq(Gu[:, :, ii[diagm]])
                olo = outer.lo.copy(); ohi = outer.hi.copy()
                olo[:, :, diagm] = sq.lo; ohi[:, :, diagm] = sq.hi
                outer = NI(olo, ohi)
                Hu = NI(Hlo[Tn["uv"]].reshape(m, N, T), Hhi[Tn["uv"]].reshape(m, N, T))
                Hv = Hu * NI(t1.lo[:, :, None], t1.hi[:, :, None]) + outer * NI(t2.lo[:, :, None], t2.hi[:, :, None])
                Hlo[Tn["tv"]] = Hv.lo.reshape(m, N * T); Hhi[Tn["tv"]] = Hv.hi.reshape(m, N * T)
        return (Xlo, Xhi, Glo.reshape(self.nv, N, d), Ghi.reshape(self.nv, N, d),
                Hlo.reshape(self.nv, N, T), Hhi.reshape(self.nv, N, T))

    def lagr_h(self, Xlo, Xhi, Glo, Ghi, Hlo, Hhi):
        """value, gradient (N,d), packed Hessian (N,T) enclosures of the Lagrangian."""
        D = self.D
        ii = np.array([p[0] for p in self.pairs]); kk = np.array([p[1] for p in self.pairs])
        X = lambda j: NI(Xlo[j], Xhi[j])
        G = lambda j: NI(Glo[j], Ghi[j])
        Hh = lambda j: NI(Hlo[j], Hhi[j])

        def P(key):
            if key == D["key793"]:
                v766, k792 = D["special793"]
                pv, pg, ph = P(k792)
                return X(v766) - pv, G(v766) - pg, Hh(v766) - ph
            val = gr = hs = None
            for p, r, c in D["prod"][key]:
                cc = K.NIq(c)
                Xp, Xr = X(p), X(r)
                Gp, Gr = G(p), G(r)
                v = (ab.isq(Xp) if p == r else Xp * Xr) * cc
                g = (Gp * NI(Xr.lo[:, None], Xr.hi[:, None]) + Gr * NI(Xp.lo[:, None], Xp.hi[:, None])) * cc
                h = (Hh(p) * NI(Xr.lo[:, None], Xr.hi[:, None]) + Hh(r) * NI(Xp.lo[:, None], Xp.hi[:, None])
                     + Gp[:, ii] * Gr[:, kk] + Gr[:, ii] * Gp[:, kk]) * cc
                val = v if val is None else val + v
                gr = g if gr is None else gr + g
                hs = h if hs is None else hs + h
            return val, gr, hs

        f = K.NIq(D["objconst"]); g = None; h = None
        for j, a in D["objlin"]:
            aa = K.NIq(a)
            f = f + X(j) * aa
            g = G(j) * aa if g is None else g + G(j) * aa
            h = Hh(j) * aa if h is None else h + Hh(j) * aa
        for key, c in D["objprod"]:
            cc = K.NIq(c)
            pv, pg, ph = P(key)
            f = f + pv * cc; g = g + pg * cc; h = h + ph * cc
        for j, lam, bnd, s in self.lag:
            ls = K.NIq(lam * s)
            f = f - (X(j) - K.NIq(bnd)) * ls
            g = g - G(j) * ls
            h = h - Hh(j) * ls
        return f, g, h

    def unpack(self, h):
        idx = self.pidx
        return h.lo[:, idx], h.hi[:, idx]

    def fbound3(self, lo, hi):
        R = self.fbound(lo, hi)
        c = 0.5 * (lo + hi)
        # center (point) and box Hessians of the Lagrangian
        fc, gc, hc = self.lagr_h(*self.fforward_h(c, c))
        _, _, hb = self.lagr_h(*self.fforward_h(lo, hi))
        HcL, HcH = self.unpack(hc)
        HbL, HbH = self.unpack(hb)
        a = dn(lo - c); b = up(hi - c)
        h3 = qpbound.third_order_bound(fc.lo, gc.lo, gc.hi, HcL, HcH, HbL, HbH, a, b)
        R["lb"] = np.where(np.isfinite(R["lb"]), np.maximum(R["lb"], h3), R["lb"])
        return R


def main(tol_rel=1e-9, tlim=3600, nstarts=30, mode="best"):
    import bbcore
    M = H3Model()
    rng = np.random.default_rng(1)
    best = (INF, None)
    t0 = time.time()
    for k in range(nstarts):
        u0 = M.lo_in + (M.hi_in - M.lo_in) * rng.random(5)
        u = ab.local_opt(M, u0, margin=1e-12)
        ok, fv = M.point_value(u)
        if ok and fv < best[0]:
            best = (fv, u)
    print(f"local search: best rigorous feasible f = {best[0]!r} at {best[1].tolist()} ({time.time()-t0:.0f}s)")
    lag, res = ab.kkt_multipliers(M, best[1])
    M.lag = lag
    print("Lagrangian terms:", [(M.D['names'][j], float(l), float(b), s) for j, l, b, s in lag], "KKT residual", res)
    tol_abs = tol_rel * abs(best[0])
    r = bbcore.run(M.fbound3, M.lo0, M.hi0, tol_abs, tlim, UB=best[0], xbest=best[1], batch=512, log_every=20, mode=mode)
    print(f"B&B: done={r['done']} processed {r['processed']} open {r['open']} time {r['time']:.0f}s")
    print(f"  min f over R in [{r['LB']!r}, {r['UB']!r}]  tol_abs {tol_abs:.2e}")
    print(f"  best point u = {r['x'].tolist()}")
    return M, r


if __name__ == "__main__":
    tol = float(sys.argv[1]) if len(sys.argv) > 1 else 1e-9
    tl = float(sys.argv[2]) if len(sys.argv) > 2 else 3600
    mode = sys.argv[3] if len(sys.argv) > 3 else "best"
    main(tol, tl, mode=mode)
