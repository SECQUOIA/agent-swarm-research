"""Reduced-space rigorous branch and bound for ann_cumene_tanh over its 5 inputs.

Per box (all outward rounded, rigorous tanh from the table exp of kan_iv):
  * forward pass of the decoded DAG (ann_model) giving natural enclosures of every
    determined variable and interval gradients w.r.t. the 5 inputs;
  * feasibility pruning with the finite variable bounds and x772 >= 0.999, using
    the natural enclosure and the mean-value enclosure of each constrained variable;
  * lower bound = max of
      - natural enclosure of f (constrained variables intersected with their bounds),
      - mean-value form of f,
      - mean-value form of the Lagrangian  f - sum_k lam_k (g_k - bound_k)  for the
        active constraints at the incumbent (lam_k >= 0 from the KKT system); on
        feasible points  f >= Lagrangian.

    python3 ann_bb.py [tol_rel] [time_limit_s]
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import sys
import time
from fractions import Fraction as Fr

import numpy as np

sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave3/kan")
import kan_iv as K  # noqa: E402
from kan_iv import NI, dn, up  # noqa: E402

import ann_model as am  # noqa: E402

INF = np.inf


def tanh_pt(z):
    """rigorous tanh at float points z (array)."""
    z = np.asarray(z, dtype=np.float64)
    a = np.minimum(np.abs(z), 300.0)
    E = K.iexp_pt_fast(2.0 * a)                       # e^{2|z|}
    Q = NI(2.0) / (E + 1.0)                           # 2/(e^{2|z|}+1)
    T = NI(1.0) - Q                                   # tanh|z|
    big = np.abs(z) >= 300.0
    lo = np.where(big, 1.0 - 1e-200, T.lo)
    hi = np.where(big, 1.0, np.minimum(T.hi, 1.0))
    lo = np.minimum(lo, hi)
    neg = z < 0
    return NI(np.where(neg, -hi, lo), np.where(neg, -lo, hi))


def tanh_range(U):
    return NI(tanh_pt(U.lo).lo, tanh_pt(U.hi).hi)


def isq(T):
    lo2 = T.lo * T.lo
    hi2 = T.hi * T.hi
    lo = np.where(T.lo >= 0, lo2, np.where(T.hi <= 0, hi2, 0.0))
    return NI(np.maximum(dn(lo), 0.0), up(np.maximum(lo2, hi2)))


class Model:
    def __init__(self):
        D = am.decode()
        self.D = D
        self.d = 5
        self.lo0 = np.array([K.frac_iv(a)[0] for a, b in D["box"]])
        self.hi0 = np.array([K.frac_iv(b)[1] for a, b in D["box"]])
        self.lo_in = np.array([K.frac_iv(a)[1] for a, b in D["box"]])
        self.hi_in = np.array([K.frac_iv(b)[0] for a, b in D["box"]])
        self.ops = []
        for op in D["ops"]:
            if op[0] == "lin":
                _, v, cv, terms, rhs = op
                self.ops.append(("lin", v, K.NIq(Fr(1) / cv), [(o, K.NIq(a)) for o, a in terms], K.NIq(rhs),
                                 float(1 / cv), [(o, float(a)) for o, a in terms], float(rhs)))
            else:
                self.ops.append(op)
        self.cb = {j: (lo, hi) for j, lo, hi in D["cbounds"]}
        self.cblo = {j: (K.frac_iv(lo)[0] if lo is not None else -INF) for j, (lo, hi) in self.cb.items()}
        self.cbhi = {j: (K.frac_iv(hi)[1] if hi is not None else INF) for j, (lo, hi) in self.cb.items()}
        self.cblo_in = {j: (K.frac_iv(lo)[1] if lo is not None else -INF) for j, (lo, hi) in self.cb.items()}
        self.cbhi_in = {j: (K.frac_iv(hi)[0] if hi is not None else INF) for j, (lo, hi) in self.cb.items()}
        self.inputs = D["inputs"]
        self.lag = []     # list of (var j, lam (Fraction >= 0), bound (Fraction), sign): term -lam*sign*(x_j - bound)

    # ---------------- interval forward pass with AD ----------------------
    def forward(self, lo, hi, grad=True, clip=False):
        """values (dict j -> NI (N,)) and gradients (dict j -> NI (N, d)).
        clip=True intersects constrained variables with their bounds (natural values
        only; never used together with grad)."""
        N = lo.shape[0]
        X, G = {}, {}
        for i, j in enumerate(self.inputs):
            X[j] = NI(lo[:, i], hi[:, i])
            if grad:
                g = np.zeros((N, self.d)); g[:, i] = 1.0
                G[j] = NI(g, g.copy())
        infeas = np.zeros(N, bool)
        for op in self.ops:
            if op[0] == "lin":
                _, v, inv, terms, rhs = op[:5]
                acc = rhs
                for o, a in terms:
                    acc = acc - a * X[o]
                X[v] = acc * inv
                if grad:
                    ga = None
                    for o, a in terms:
                        t = G[o] * a
                        ga = t if ga is None else ga + t
                    G[v] = ga * (-inv) if ga is not None else NI(np.zeros((N, self.d)), np.zeros((N, self.d)))
            else:
                _, v, u = op
                T = tanh_range(X[u])
                X[v] = T
                if grad:
                    dT = NI(1.0) - isq(T)
                    G[v] = G[u] * NI(dT.lo[:, None], dT.hi[:, None])
            if v in self.cb:
                infeas |= (X[v].hi < self.cblo[v]) | (X[v].lo > self.cbhi[v])
                if clip:
                    nl = np.maximum(X[v].lo, self.cblo[v]); nh = np.minimum(X[v].hi, self.cbhi[v])
                    nl = np.where(nl <= nh, nl, X[v].lo); nh = np.where(nl <= nh, nh, X[v].hi)
                    X[v] = NI(nl, nh)
        return X, G, infeas

    def objective(self, X, G=None):
        """f and (optionally) its gradient from the forward values."""
        D = self.D

        def P(key):
            if key == D["key793"]:
                v766, k792 = D["special793"]
                pv, pg = P(k792)
                val = X[v766] - pv
                gr = (G[v766] - pg) if G is not None else None
                return val, gr
            val, gr = None, None
            for p, r, c in D["prod"][key]:
                cc = K.NIq(c)
                if p == r:
                    t = isq(X[p]) * cc
                else:
                    t = X[p] * X[r] * cc
                val = t if val is None else val + t
                if G is not None:
                    Xp = NI(X[p].lo[:, None], X[p].hi[:, None]); Xr = NI(X[r].lo[:, None], X[r].hi[:, None])
                    tg = (G[p] * Xr + G[r] * Xp) * cc
                    gr = tg if gr is None else gr + tg
            return val, gr

        f = K.NIq(D["objconst"])
        g = None
        for j, a in D["objlin"]:
            aa = K.NIq(a)
            f = f + X[j] * aa
            if G is not None:
                t = G[j] * aa
                g = t if g is None else g + t
        for key, c in D["objprod"]:
            cc = K.NIq(c)
            pv, pg = P(key)
            f = f + pv * cc
            if G is not None:
                t = pg * cc
                g = t if g is None else g + t
        return f, g

    def lagr(self, X, f, G=None, g=None):
        """Lagrangian value/gradient: f - sum lam*s*(x_j - b)."""
        L, Lg = f, g
        for j, lam, b, s in self.lag:
            ls = K.NIq(lam * s)
            L = L - (X[j] - K.NIq(b)) * ls
            if G is not None:
                Lg = Lg - G[j] * ls
        return L, Lg

    def bound(self, lo, hi):
        N = lo.shape[0]
        c = 0.5 * (lo + hi)
        Xc, _, _ = self.forward(c, c, grad=False)
        fc, _ = self.objective(Xc)
        Lc, _ = self.lagr(Xc, fc)
        X, G, infeas = self.forward(lo, hi, grad=True)
        f, g = self.objective(X, G)
        D_ = NI(dn(lo - c), up(hi - c))
        # mean-value forms (sum over inputs, outward)
        acc_f, acc_L = fc, Lc
        L, Lg = self.lagr(X, f, G, g)
        for i in range(self.d):
            Di = D_[:, i]
            acc_f = acc_f + g[:, i] * Di
            acc_L = acc_L + Lg[:, i] * Di
        # constraint pruning with mean-value enclosures of constrained variables
        for j in self.cb:
            if j in self.inputs:
                continue
            m = Xc[j]
            for i in range(self.d):
                m = m + G[j][:, i] * D_[:, i]
            infeas |= (m.hi < self.cblo[j]) | (m.lo > self.cbhi[j])
        Xn, _, inf2 = self.forward(lo, hi, grad=False, clip=True)
        fn, _ = self.objective(Xn)
        lb = np.maximum(np.maximum(fn.lo, acc_f.lo), acc_L.lo)
        infeas |= inf2
        lb = np.where(infeas, INF, lb)
        # candidate: center, if strictly feasible
        ok = np.ones(N, bool)
        for j in self.cb:
            if j in self.inputs:
                continue
            ok &= (np.broadcast_to(Xc[j].lo, (N,)) >= self.cblo_in[j]) & (np.broadcast_to(Xc[j].hi, (N,)) <= self.cbhi_in[j])
        ok &= np.all((c >= self.lo_in) & (c <= self.hi_in), axis=1)
        ub = np.where(ok, fc.hi, INF)
        Gm = np.maximum(np.maximum(np.abs(g.lo), np.abs(g.hi)), np.maximum(np.abs(Lg.lo), np.abs(Lg.hi)))
        return lb, ub, c, Gm, Lg

    def point_value(self, u):
        """rigorous (feasible?, upper bound of f) at a single point u."""
        if not np.all((u >= self.lo_in) & (u <= self.hi_in)):
            return False, INF
        Xc, _, _ = self.forward(u[None, :], u[None, :], grad=False)
        fc, _ = self.objective(Xc)
        ok = all(np.all(np.atleast_1d(Xc[j].lo) >= self.cblo_in[j]) and np.all(np.atleast_1d(Xc[j].hi) <= self.cbhi_in[j])
                 for j in self.cb if j not in self.inputs)
        return ok, float(np.atleast_1d(fc.hi)[0])

    # ---------------- float model for local search -------------------------
    def ffwd(self, u):
        X = {j: u[i] for i, j in enumerate(self.inputs)}
        G = {j: np.eye(self.d)[i] for i, j in enumerate(self.inputs)}
        for op in self.ops:
            if op[0] == "lin":
                v, inv, terms, rhs = op[1], op[5], op[6], op[7]
                s = rhs - sum(a * X[o] for o, a in terms)
                X[v] = s * inv
                G[v] = -inv * sum(a * G[o] for o, a in terms) if terms else np.zeros(self.d)
            else:
                _, v, u_ = op
                X[v] = np.tanh(X[u_])
                G[v] = (1 - X[v] ** 2) * G[u_]
        return X, G

    def ffun(self, u):
        X, G = self.ffwd(u)
        D = self.D

        def P(key):
            if key == D["key793"]:
                v766, k792 = D["special793"]
                pv, pg = P(k792)
                return X[v766] - pv, G[v766] - pg
            val, gr = 0.0, np.zeros(self.d)
            for p, r, c in D["prod"][key]:
                val += float(c) * X[p] * X[r]
                gr = gr + float(c) * (G[p] * X[r] + G[r] * X[p])
            return val, gr
        f = float(D["objconst"]); g = np.zeros(self.d)
        for j, a in D["objlin"]:
            f += float(a) * X[j]; g = g + float(a) * G[j]
        for key, c in D["objprod"]:
            pv, pg = P(key)
            f += float(c) * pv; g = g + float(c) * pg
        return f, g, X, G


def local_opt(M, u0, margin=1e-9):
    from scipy.optimize import minimize
    tanh_out = {op[1] for op in M.ops if op[0] == "tanh"}
    # constraints that can bind (tanh outputs lie in (-1,1); |bounds| >= 1e5 are checked rigorously afterwards)
    cj = [j for j in M.cb if j not in M.inputs and j not in tanh_out
          and max(abs(M.cblo_in[j]) if np.isfinite(M.cblo_in[j]) else 0, abs(M.cbhi_in[j]) if np.isfinite(M.cbhi_in[j]) else 0) < 1e5]

    def cons(u):
        f, g, X, G = M.ffun(u)
        out = []
        for j in cj:
            if np.isfinite(M.cblo_in[j]):
                out.append(X[j] - M.cblo_in[j] - margin)
            if np.isfinite(M.cbhi_in[j]):
                out.append(M.cbhi_in[j] - X[j] - margin)
        return np.array(out)

    def jac(u):
        f, g, X, G = M.ffun(u)
        out = []
        for j in cj:
            if np.isfinite(M.cblo_in[j]):
                out.append(G[j])
            if np.isfinite(M.cbhi_in[j]):
                out.append(-G[j])
        return np.array(out)

    r = minimize(lambda u: M.ffun(u)[:2], u0, jac=True, bounds=list(zip(M.lo_in, M.hi_in)), method="SLSQP",
                 constraints=[dict(type="ineq", fun=cons, jac=jac)], options=dict(maxiter=500, ftol=1e-16))
    return np.clip(r.x, M.lo_in, M.hi_in)


def kkt_multipliers(M, u, act_tol=1e-7):
    """nonnegative multipliers of the (nearly) active constraints at u by NNLS on
    grad f = sum lam_k s_k grad x_j (s = +1 for lower bounds, -1 for upper bounds);
    input-box bounds are handled by the B&B box itself."""
    from scipy.optimize import nnls
    f, g, X, G = M.ffun(u)
    act = []
    tanh_out = {op[1] for op in M.ops if op[0] == "tanh"}
    for j in M.cb:
        if j in M.inputs or j in tanh_out:     # tanh outputs are strictly inside [-1, 1]
            continue
        if np.isfinite(M.cblo_in[j]) and X[j] - M.cblo_in[j] < act_tol:
            act.append((j, +1, M.cb[j][0]))
        if np.isfinite(M.cbhi_in[j]) and M.cbhi_in[j] - X[j] < act_tol:
            act.append((j, -1, M.cb[j][1]))
    free = [i for i in range(M.d) if M.lo_in[i] + 1e-9 < u[i] < M.hi_in[i] - 1e-9]
    if not act:
        return [], g
    A = np.array([s * G[j] for j, s, b in act]).T[free]
    lam, res = nnls(A, g[free])
    return [(j, Fr(float(l)), b, s) for (j, s, b), l in zip(act, lam) if l > 0], res


def branch_and_bound(M, tol_abs, tlim, u_inc=None, batch=512, log=print):
    t0 = time.time()
    d = M.d
    UB, ubpt = INF, None
    if u_inc is not None:
        ok, fv = M.point_value(u_inc)
        if ok:
            UB, ubpt = fv, u_inc.copy()
    lo = M.lo0[None, :].copy(); hi = M.hi0[None, :].copy()
    key = np.array([-INF])
    fathomed_min = INF
    nproc = 0; it = 0
    scale = M.hi0 - M.lo0
    while lo.shape[0] > 0:
        it += 1
        if time.time() - t0 > tlim:
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
        lb, ub, c, Gm, _ = M.bound(blo, bhi)
        j = int(np.argmin(ub))
        if ub[j] < UB:
            UB, ubpt = float(ub[j]), c[j].copy()
        keep = lb < UB - tol_abs
        fath = (~keep) & (lb <= UB)
        if fath.any():
            fathomed_min = min(fathomed_min, float(lb[fath].min()))
        blo, bhi, lbk, Gm = blo[keep], bhi[keep], lb[keep], Gm[keep]
        if blo.shape[0] == 0:
            continue
        w = bhi - blo
        smear = Gm * w
        k = np.argmax(smear, axis=1)
        r = np.arange(len(k))
        small = w[r, k] <= 1e-15 * np.maximum(1.0, np.abs(blo[r, k]))
        k = np.where(small, np.argmax(w / scale, axis=1), k)
        tiny = w[r, k] <= 1e-15 * np.maximum(1.0, np.abs(blo[r, k]))
        if tiny.any():
            fathomed_min = min(fathomed_min, float(lbk[tiny].min()))
            blo, bhi, lbk, k = blo[~tiny], bhi[~tiny], lbk[~tiny], k[~tiny]
            r = np.arange(len(k))
        mid = 0.5 * (blo[r, k] + bhi[r, k])
        lo1, hi1 = blo.copy(), bhi.copy(); hi1[r, k] = mid
        lo2, hi2 = blo.copy(), bhi.copy(); lo2[r, k] = mid
        lo = np.concatenate([lo, lo1, lo2]); hi = np.concatenate([hi, hi1, hi2])
        key = np.concatenate([key, lbk, lbk])
        if it % 50 == 0:
            glb = min(fathomed_min, key.min() if key.size else INF, UB)
            log(f"  it {it} processed {nproc} open {lo.shape[0]} UB {UB:.15g} LB {glb:.15g} t {time.time()-t0:.0f}s")
    open_min = key.min() if key.size else INF
    LB = min(fathomed_min, open_min, UB)
    return dict(LB=LB, UB=UB, u=ubpt, processed=nproc, open=lo.shape[0], done=lo.shape[0] == 0, time=time.time() - t0)


def main(tol_rel=1e-9, tlim=3600, nstarts=30):
    M = Model()
    rng = np.random.default_rng(1)
    best = (INF, None)
    t0 = time.time()
    for k in range(nstarts):
        u0 = M.lo_in + (M.hi_in - M.lo_in) * rng.random(5)
        u = local_opt(M, u0, margin=1e-12)
        ok, fv = M.point_value(u)
        if ok and fv < best[0]:
            best = (fv, u)
    print(f"local search: best rigorous feasible f = {best[0]!r} at {best[1].tolist()} ({time.time()-t0:.0f}s)")
    lag, res = kkt_multipliers(M, best[1])
    M.lag = lag
    print("Lagrangian terms:", [(M.D['names'][j], float(l), float(b), s) for j, l, b, s in lag], "KKT residual", res)
    tol_abs = tol_rel * abs(best[0])
    r = branch_and_bound(M, tol_abs, tlim, u_inc=best[1])
    print(f"B&B: done={r['done']} processed {r['processed']} open {r['open']} time {r['time']:.0f}s")
    print(f"  min f over R in [{r['LB']!r}, {r['UB']!r}]  tol_abs {tol_abs:.2e}")
    print(f"  best point u = {r['u'].tolist()}")
    return M, r


if __name__ == "__main__":
    tol = float(sys.argv[1]) if len(sys.argv) > 1 else 1e-9
    tl = float(sys.argv[2]) if len(sys.argv) > 2 else 3600
    main(tol, tl)
