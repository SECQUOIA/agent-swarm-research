"""Level-wise vectorized version of the ann_cumene_tanh bounding (same mathematics
as ann_bb.Model.bound, faster).

Linear rows of one DAG level are applied as one sparse matrix product in
midpoint-radius form (Rump): for y = W x + b with W = W_mid +- W_rad, x in
[x_mid - x_rad, x_mid + x_rad],
    |y - fl(W_mid x_mid + b_mid)| <= |W_mid| x_rad + W_rad (|x_mid| + x_rad) + b_rad
                                    + gamma_{k+1} (|W_mid| |x_mid| + |b_mid|),
k = max nonzeros per row, gamma_n = n u / (1 - n u).  The computed radius is
inflated by (1 + 4 gamma_{k+3}) and a tiny absolute term to cover its own
rounding.  Everything else as in ann_bb.
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import sys
import time
from fractions import Fraction as Fr

import numpy as np
import scipy.sparse as sp

sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave3/kan")
sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave3")
import kan_iv as K  # noqa: E402
from kan_iv import NI, dn, up  # noqa: E402

import ann_bb as ab  # noqa: E402

INF = np.inf
U = 2.0 ** -53


def gam(n):
    return n * U / (1 - n * U)


class FastModel(ab.Model):
    def __init__(self):
        super().__init__()
        D = self.D
        nv = len(D["names"])
        self.nv = nv
        level = {j: 0 for j in self.inputs}
        for op in D["ops"]:
            if op[0] == "lin":
                level[op[1]] = 1 + max([level[o] for o, a in op[3]], default=0)
            else:
                level[op[1]] = 1 + level[op[2]]
        self.level = level
        L = max(level.values())
        self.levels = []
        for l in range(1, L + 1):
            lin = [op for op in D["ops"] if op[0] == "lin" and level[op[1]] == l]
            th = [op for op in D["ops"] if op[0] == "tanh" and level[op[1]] == l]
            ent = {}
            if lin:
                rows, cols, wm, wr = [], [], [], []
                bm, br = [], []
                tv = []
                kmax = 0
                for r, op in enumerate(lin):
                    _, v, cv, terms, rhs = op
                    tv.append(v)
                    kmax = max(kmax, len(terms))
                    for o, a in terms:
                        q = -a / cv
                        lo_, hi_ = K.frac_iv(q)
                        mid = 0.5 * (lo_ + hi_)
                        rows.append(r); cols.append(o); wm.append(mid); wr.append(up(max(hi_ - mid, mid - lo_)))
                    q = rhs / cv
                    lo_, hi_ = K.frac_iv(q)
                    mid = 0.5 * (lo_ + hi_)
                    bm.append(mid); br.append(float(up(max(hi_ - mid, mid - lo_))))
                used = np.array(sorted(set(cols)), dtype=int)
                pos = {j: q for q, j in enumerate(used)}
                cols = [pos[j] for j in cols]
                shape = (len(lin), len(used))
                Wm = sp.csr_matrix((wm, (rows, cols)), shape=shape)
                ent["lin"] = dict(tv=np.array(tv), used=used, Wm=Wm, Wa=abs(Wm), Wr=sp.csr_matrix((wr, (rows, cols)), shape=shape),
                                  bm=np.array(bm)[:, None], br=np.array(br)[:, None], k=kmax)
            if th:
                ent["tanh"] = dict(tv=np.array([op[1] for op in th]), uv=np.array([op[2] for op in th]))
            self.levels.append(ent)
        self.cons_idx = np.array([j for j in self.cb if j not in self.inputs])
        self.cons_lo = np.array([self.cblo[j] for j in self.cons_idx])[:, None]
        self.cons_hi = np.array([self.cbhi[j] for j in self.cons_idx])[:, None]
        self.cons_lo_in = np.array([self.cblo_in[j] for j in self.cons_idx])[:, None]
        self.cons_hi_in = np.array([self.cbhi_in[j] for j in self.cons_idx])[:, None]

    @staticmethod
    def _affine(E, xlo, xhi, with_b=True):
        xm = 0.5 * (xlo + xhi)
        xr = up(np.maximum(xhi - xm, xm - xlo))
        ym = E["Wm"] @ xm
        if with_b:
            ym = ym + E["bm"]
        g1 = gam(E["k"] + 1)
        R = E["Wa"] @ xr + E["Wr"] @ (np.abs(xm) + xr) + g1 * (E["Wa"] @ np.abs(xm))
        if with_b:
            R = R + E["br"] + g1 * np.abs(E["bm"])
        R = R * (1 + 4 * gam(E["k"] + 3)) + 1e-300
        return dn(ym - R), up(ym + R)

    def fforward(self, lo, hi, grad=True, clip=False):
        """returns Xlo, Xhi (nv, N) and (if grad) Glo, Ghi (nv, N, d), plus infeasibility mask."""
        N = lo.shape[0]
        d = self.d
        Xlo = np.zeros((self.nv, N)); Xhi = np.zeros((self.nv, N))
        for i, j in enumerate(self.inputs):
            Xlo[j] = lo[:, i]; Xhi[j] = hi[:, i]
        if grad:
            Glo = np.zeros((self.nv, N * d)); Ghi = np.zeros((self.nv, N * d))
            for i, j in enumerate(self.inputs):
                e = np.zeros((N, d)); e[:, i] = 1.0
                Glo[j] = e.ravel(); Ghi[j] = e.ravel()
        for ent in self.levels:
            if "lin" in ent:
                E = ent["lin"]
                ylo, yhi = self._affine(E, Xlo[E["used"]], Xhi[E["used"]])
                Xlo[E["tv"]] = ylo; Xhi[E["tv"]] = yhi
                if grad:
                    glo, ghi = self._affine(E, Glo[E["used"]], Ghi[E["used"]], with_b=False)
                    Glo[E["tv"]] = glo; Ghi[E["tv"]] = ghi
            if "tanh" in ent:
                T = ent["tanh"]
                Uu = NI(Xlo[T["uv"]], Xhi[T["uv"]])
                Tt = ab.tanh_range(Uu)
                Xlo[T["tv"]] = Tt.lo; Xhi[T["tv"]] = Tt.hi
                if grad:
                    dT = NI(1.0) - ab.isq(Tt)          # (m, N)
                    dTl = np.repeat(dT.lo, d, axis=1); dTh = np.repeat(dT.hi, d, axis=1)
                    P = NI(Glo[T["uv"]], Ghi[T["uv"]]) * NI(dTl, dTh)
                    Glo[T["tv"]] = P.lo; Ghi[T["tv"]] = P.hi
            if clip:
                ci = self.cons_idx
                nl = np.maximum(Xlo[ci], self.cons_lo); nh = np.minimum(Xhi[ci], self.cons_hi)
                okc = nl <= nh
                Xlo[ci] = np.where(okc, nl, Xlo[ci]); Xhi[ci] = np.where(okc, nh, Xhi[ci])
        ci = self.cons_idx
        infeas = np.any((Xhi[ci] < self.cons_lo) | (Xlo[ci] > self.cons_hi), axis=0)
        if grad:
            return Xlo, Xhi, Glo.reshape(self.nv, N, d), Ghi.reshape(self.nv, N, d), infeas
        return Xlo, Xhi, infeas

    def _dicts(self, Xlo, Xhi, Glo=None, Ghi=None):
        X = _Lazy(lambda j: NI(Xlo[j], Xhi[j]))
        G = _Lazy(lambda j: NI(Glo[j], Ghi[j])) if Glo is not None else None
        return X, G

    def fbound(self, lo, hi):
        N, d = lo.shape
        c = 0.5 * (lo + hi)
        Xclo, Xchi, _ = self.fforward(c, c, grad=False)
        Xc, _ = self._dicts(Xclo, Xchi)
        fc, _ = self.objective(Xc)
        Lc, _ = self.lagr(Xc, fc)
        Xlo, Xhi, Glo, Ghi, infeas = self.fforward(lo, hi, grad=True)
        X, G = self._dicts(Xlo, Xhi, Glo, Ghi)
        f, g = self.objective(X, G)
        Lf, Lg = self.lagr(X, f, G, g)
        D_ = NI(dn(lo - c), up(hi - c))
        acc_f, acc_L = fc, Lc
        for i in range(d):
            acc_f = acc_f + g[:, i] * D_[:, i]
            acc_L = acc_L + Lg[:, i] * D_[:, i]
        # mean-value enclosures of the constrained variables
        ci = self.cons_idx
        Gc = NI(Glo[ci], Ghi[ci])                           # (m, N, d)
        Dm = NI(D_.lo[None, :, :], D_.hi[None, :, :])
        S = Gc * Dm
        slo = S.lo.sum(axis=2); shi = S.hi.sum(axis=2)
        slo = dn(slo - 4 * U * np.abs(S.lo).sum(axis=2)); shi = up(shi + 4 * U * np.abs(S.hi).sum(axis=2))
        mlo = dn(Xclo[ci] + slo); mhi = up(Xchi[ci] + shi)
        infeas |= np.any((mhi < self.cons_lo) | (mlo > self.cons_hi), axis=0)
        Xnlo, Xnhi, inf2 = self.fforward(lo, hi, grad=False, clip=True)
        Xn, _ = self._dicts(Xnlo, Xnhi)
        fn, _ = self.objective(Xn)
        lb = np.maximum(np.maximum(fn.lo, acc_f.lo), acc_L.lo)
        infeas |= inf2
        lb = np.where(infeas, INF, lb)
        ok = np.all((Xclo[ci] >= self.cons_lo_in) & (Xchi[ci] <= self.cons_hi_in), axis=0)
        ok &= np.all((c >= self.lo_in) & (c <= self.hi_in), axis=1)
        ub = np.where(ok, fc.hi, INF)
        Gm = np.maximum(np.maximum(np.abs(g.lo), np.abs(g.hi)), np.maximum(np.abs(Lg.lo), np.abs(Lg.hi)))
        smear = Gm * (hi - lo)
        return dict(lb=lb, ub=ub, x=c, smear=smear)


class _Lazy(dict):
    def __init__(self, f):
        super().__init__()
        self.f = f

    def __missing__(self, j):
        v = self.f(j)
        self[j] = v
        return v


def main(tol_rel=1e-9, tlim=3600, nstarts=30, mode="depth"):
    import bbcore
    M = FastModel()
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
    r = bbcore.run(M.fbound, M.lo0, M.hi0, tol_abs, tlim, UB=best[0], xbest=best[1], batch=2048, log_every=50, mode=mode)
    print(f"B&B: done={r['done']} processed {r['processed']} open {r['open']} time {r['time']:.0f}s")
    print(f"  min f over R in [{r['LB']!r}, {r['UB']!r}]  tol_abs {tol_abs:.2e}")
    print(f"  best point u = {r['x'].tolist()}")
    return M, r


if __name__ == "__main__":
    tol = float(sys.argv[1]) if len(sys.argv) > 1 else 1e-9
    tl = float(sys.argv[2]) if len(sys.argv) > 2 else 3600
    mode = sys.argv[3] if len(sys.argv) > 3 else "depth"
    main(tol, tl, mode=mode)
