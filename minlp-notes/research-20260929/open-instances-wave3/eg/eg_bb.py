"""Rigorous branch and bound for eg_disc_s / eg_disc2_s / eg_int_s.

Problem (decoded by eg_model):  min_x max_{k in obj rows} (c_k + g_k(x))
    s.t. lb_k <= -g_k(x) <= ub_k (side rows), x in the box, some x integer,
    g_k(x) = sum_m a_km exp( sum_i gamma_kmi (mu_kmi + s_i x_i)^2 ) + linin_k . x.

Integer coordinates are relaxed to their interval while it has more than one
integer and split at integers.  Box bounds: for every row, the natural interval
enclosure (each term's exponent is separable, so each term is enclosed exactly
up to rounding) intersected with the mean-value form.  Lower bound of the
objective = max over obj rows of c_k + lower(g_k).  Boxes where a side row is
provably violated are discarded.  All arithmetic is outward rounded; exp is the
rigorous table/Taylor exp of kan_iv (no libm).

    python3 eg_bb.py <name> [tol_rel] [time_limit_s]
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

import eg_model as em  # noqa: E402

INF = np.inf


def isq(T):
    """exact-range square of an interval, outward rounded."""
    lo2 = T.lo * T.lo
    hi2 = T.hi * T.hi
    pos = T.lo >= 0
    neg = T.hi <= 0
    lo = np.where(pos, lo2, np.where(neg, hi2, 0.0))
    hi = np.maximum(lo2, hi2)
    return NI(np.maximum(dn(lo), 0.0), up(hi))


def iexp_range(E):
    return NI(K.iexp_pt_fast(E.lo).lo, K.iexp_pt_fast(E.hi).hi)


class Prob:
    def __init__(self, name):
        M = em.decode(name)
        self.M = M
        rows = M["rows"]
        self.R = len(rows)
        self.Mt = max(len(r["terms"]) for r in rows)
        assert all(len(r["terms"]) == self.Mt for r in rows)
        d = len(M["dvars"])
        self.d = d
        self.lo0 = np.array([K.frac_iv(v)[0] for v in M["lb"]])
        self.hi0 = np.array([K.frac_iv(v)[1] for v in M["ub"]])
        # inner box (doubles inside the exact box) for candidate points
        self.lo_in = np.array([K.frac_iv(v)[1] for v in M["lb"]])
        self.hi_in = np.array([K.frac_iv(v)[0] for v in M["ub"]])
        self.isint = np.array(M["isint"])
        A = np.zeros((self.R, self.Mt, 2))
        MU = np.zeros((d, self.R, self.Mt, 2))
        GA = np.zeros((d, self.R, self.Mt, 2))
        for k, r in enumerate(rows):
            for m, (a, fac) in enumerate(r["terms"]):
                A[k, m] = K.frac_iv(a)
                for i in range(d):
                    s, mu, g = fac[i]
                    MU[i, k, m] = K.frac_iv(mu)
                    GA[i, k, m] = K.frac_iv(g)
                    assert g < 0
        self.A = NI(A[..., 0], A[..., 1])
        self.MU = [NI(MU[i, ..., 0], MU[i, ..., 1]) for i in range(d)]
        self.GA = [NI(GA[i, ..., 0], GA[i, ..., 1]) for i in range(d)]
        self.S = [K.NIq(s) for s in M["scale"]]
        LI = np.zeros((self.R, d, 2))
        for k, r in enumerate(rows):
            for i, c in r["linin"].items():
                LI[k, i] = K.frac_iv(c)
        self.LI = [NI(LI[:, i, 0], LI[:, i, 1]) for i in range(d)]
        self.objrows = np.array([r["obj"] for r in rows])
        self.c = np.array([K.frac_iv(r["lb"])[0] if r["obj"] else 0.0 for r in rows])   # lower end of c_k
        self.c_hi = np.array([K.frac_iv(r["lb"])[1] if r["obj"] else 0.0 for r in rows])
        # side rows: lb <= -g <= ub  <=>  -ub <= g <= -lb
        self.glo = np.array([(-K.frac_iv(r["ub"])[1] if r["ub"] is not None else -INF) if not r["obj"] else -INF for r in rows])
        self.ghi = np.array([(-K.frac_iv(r["lb"])[0] if r["lb"] is not None else INF) if not r["obj"] else INF for r in rows])
        # for strict feasibility checks of candidate points (inner bounds)
        self.glo_in = np.array([(-K.frac_iv(r["ub"])[0] if r["ub"] is not None else -INF) if not r["obj"] else -INF for r in rows])
        self.ghi_in = np.array([(-K.frac_iv(r["lb"])[1] if r["lb"] is not None else INF) if not r["obj"] else INF for r in rows])

    def geval(self, lo, hi, grad=True):
        """enclosures of g_k over boxes (N, d): value (N, R) and gradient list of (N, R)."""
        N = lo.shape[0]
        E = None
        Ts = []
        for i in range(self.d):
            X = NI(lo[:, i][:, None, None], hi[:, i][:, None, None])
            T = self.MU[i] + self.S[i] * X            # (N, R, Mt)
            Ts.append(T)
            q = self.GA[i] * isq(T)
            E = q if E is None else E + q
        ex = iexp_range(E)
        W = self.A * ex                                 # term values (N, R, Mt)
        g = self._sum(W)   # rigorous summation over the terms
        for i in range(self.d):
            X = NI(lo[:, i][:, None], hi[:, i][:, None])
            g = g + self.LI[i] * X
        if not grad:
            return g, None
        G = []
        for i in range(self.d):
            dT = W * (self.GA[i] * (Ts[i] * (self.S[i] * 2.0)))
            G.append(self._sum(dT) + self.LI[i])
        return g, G

    @staticmethod
    def _sum(W):
        """outward-rounded sum over the last axis (float sum error bound n*u*sum|.|)."""
        n = W.lo.shape[-1]
        slo = W.lo.sum(axis=-1)
        shi = W.hi.sum(axis=-1)
        elo = (n + 2) * 1.2e-16 * np.abs(W.lo).sum(axis=-1)
        ehi = (n + 2) * 1.2e-16 * np.abs(W.hi).sum(axis=-1)
        return NI(dn(slo - elo - 1e-300), up(shi + ehi + 1e-300))

    def bound(self, lo, hi):
        g, G = self.geval(lo, hi)
        c = 0.5 * (lo + hi)
        gc, _ = self.geval(c, c, grad=False)
        mv = gc
        for i in range(self.d):
            D = NI(dn(lo[:, i] - c[:, i]), up(hi[:, i] - c[:, i]))[:, None]
            mv = mv + G[i] * D
        enc = NI(np.maximum(g.lo, mv.lo), np.minimum(g.hi, mv.hi))
        infeas = np.any((enc.hi < self.glo) | (enc.lo > self.ghi), axis=1)
        lbk = np.where(self.objrows, dn(self.c + enc.lo), -INF)
        lb = np.where(infeas, INF, lbk.max(axis=1))
        return lb, G, enc

    def fpoint(self, x):
        """rigorous objective at points x (N, d) and strict feasibility of side rows
        (points outside the exact box count as infeasible)."""
        g, _ = self.geval(x, x, grad=False)
        inbox = np.all((x >= self.lo_in) & (x <= self.hi_in), axis=1)
        feas = np.all((g.lo >= self.glo_in) & (g.hi <= self.ghi_in), axis=1)
        f = np.where(self.objrows, up(self.c_hi + g.hi), -INF).max(axis=1)
        return np.where(feas & inbox, f, INF), g

    # float version for local search
    def ffun(self, x):
        x = np.atleast_2d(x)
        E = 0.0
        dE = []
        for i in range(self.d):
            t = 0.5 * (self.MU[i].lo + self.MU[i].hi) + float(self.M["scale"][i]) * x[:, i][:, None, None]
            ga = 0.5 * (self.GA[i].lo + self.GA[i].hi)
            E = E + ga * t * t
            dE.append(2 * ga * t * float(self.M["scale"][i]))
        W = 0.5 * (self.A.lo + self.A.hi) * np.exp(E)
        g = W.sum(axis=2)
        G = [(W * dE[i]).sum(axis=2) for i in range(self.d)]
        for i in range(self.d):
            li = 0.5 * (self.LI[i].lo + self.LI[i].hi)
            g = g + li * x[:, i][:, None]
            G[i] = G[i] + li
        return g, np.stack(G, axis=2)


def local_minimax(P, x0, fixed_int=True, margin=1e-11):
    """SLSQP on min t s.t. t >= c_k + g_k(x), side rows (with a small margin), box;
    integers fixed at x0.  Returns the point (float); the caller verifies it rigorously."""
    from scipy.optimize import minimize
    cont = ~P.isint if fixed_int else np.ones(P.d, bool)
    ci = np.where(cont)[0]
    cmid = 0.5 * (P.c + P.c_hi)
    obj = P.objrows
    side = np.where(~obj)[0]
    lo_rows = [k for k in side if np.isfinite(P.glo_in[k])]
    hi_rows = [k for k in side if np.isfinite(P.ghi_in[k])]

    def full(z):
        x = x0.copy()
        x[ci] = z[:-1]
        return x

    def cons(z):
        g, G = P.ffun(full(z))
        g = g[0]
        return np.concatenate([z[-1] - (cmid[obj] + g[obj]),
                               g[lo_rows] - P.glo_in[lo_rows] - margin,
                               P.ghi_in[hi_rows] - g[hi_rows] - margin])

    def jcons(z):
        g, G = P.ffun(full(z))
        G = G[0][:, ci]
        J1 = np.hstack([-G[obj], np.ones((obj.sum(), 1))])
        J2 = np.hstack([G[lo_rows], np.zeros((len(lo_rows), 1))])
        J3 = np.hstack([-G[hi_rows], np.zeros((len(hi_rows), 1))])
        return np.vstack([J1, J2, J3])

    g0, _ = P.ffun(x0)
    z0 = np.concatenate([x0[ci], [np.max(cmid[obj] + g0[0][obj])]])
    bnds = [(P.lo_in[i], P.hi_in[i]) for i in ci] + [(None, None)]
    r = minimize(lambda z: z[-1], z0, jac=lambda z: np.eye(len(z))[-1], bounds=bnds,
                 constraints=[dict(type="ineq", fun=cons, jac=jcons)],
                 method="SLSQP", options=dict(maxiter=500, ftol=1e-16))
    z = r.x.copy()
    z[:-1] = np.clip(z[:-1], [b[0] for b in bnds[:-1]], [b[1] for b in bnds[:-1]])
    return full(z)


def branch_and_bound(P, tol_abs, tlim, x_inc=None, batch=400, log=print, polish_every=50):
    t0 = time.time()
    d = P.d
    UB, ubpt = INF, None
    if x_inc is not None:
        f, _ = P.fpoint(x_inc[None, :])
        UB, ubpt = float(f[0]), x_inc.copy()
    lo = P.lo0[None, :].copy()
    hi = P.hi0[None, :].copy()
    key = np.array([-INF])
    fathomed_min = INF
    nproc = 0
    it = 0
    polished = set()
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
        lb, G, enc = P.bound(blo, bhi)
        # candidate points: centers with integers rounded (inside the box)
        c = 0.5 * (blo + bhi)
        c[:, P.isint] = np.clip(np.round(c[:, P.isint]), blo[:, P.isint], bhi[:, P.isint])
        c = np.clip(c, P.lo_in, P.hi_in)
        fc, _ = P.fpoint(c)
        j = int(np.argmin(fc))
        if fc[j] < UB:
            UB, ubpt = float(fc[j]), c[j].copy()
        # occasionally polish the best open candidate with a local minimax solve
        if it % polish_every == 1:
            j = int(np.argmin(lb))
            if np.isfinite(lb[j]):
                cj = c[j].copy()
                keyi = tuple(cj[P.isint].astype(int))
                if keyi not in polished:
                    polished.add(keyi)
                    try:
                        xl = local_minimax(P, cj)
                        f, _ = P.fpoint(xl[None, :])
                        if f[0] < UB:
                            UB, ubpt = float(f[0]), xl.copy()
                    except Exception:
                        pass
        keep = lb < UB - tol_abs
        fath = (~keep) & (lb <= UB)
        if fath.any():
            fathomed_min = min(fathomed_min, float(lb[fath].min()))
        blo, bhi, lbk = blo[keep], bhi[keep], lb[keep]
        if blo.shape[0] == 0:
            continue
        Gm = np.stack([np.maximum(np.abs(g.lo), np.abs(g.hi))[keep].max(axis=1) for g in G], axis=1)
        w = bhi - blo
        smear = Gm * w
        k = np.argmax(smear, axis=1)
        r = np.arange(len(k))
        small = w[r, k] <= 1e-15 * np.maximum(1.0, np.abs(blo[r, k]))
        k = np.where(small, np.argmax(w, axis=1), k)
        tiny = w[r, k] <= 1e-15 * np.maximum(1.0, np.abs(blo[r, k]))
        if tiny.any():
            fathomed_min = min(fathomed_min, float(lbk[tiny].min()))
            blo, bhi, lbk, k = blo[~tiny], bhi[~tiny], lbk[~tiny], k[~tiny]
            r = np.arange(len(k))
        mid = 0.5 * (blo[r, k] + bhi[r, k])
        isi = P.isint[k]
        midlo = np.where(isi, np.floor(mid), mid)
        midhi = np.where(isi, np.floor(mid) + 1, mid)
        lo1, hi1 = blo.copy(), bhi.copy(); hi1[r, k] = midlo
        lo2, hi2 = blo.copy(), bhi.copy(); lo2[r, k] = midhi
        lo = np.concatenate([lo, lo1, lo2]); hi = np.concatenate([hi, hi1, hi2])
        key = np.concatenate([key, lbk, lbk])
        if it % 100 == 0:
            glb = min(fathomed_min, key.min() if key.size else INF, UB)
            log(f"  it {it} processed {nproc} open {lo.shape[0]} UB {UB:.15g} LB {glb:.15g} t {time.time()-t0:.0f}s")
    open_min = key.min() if key.size else INF
    LB = min(fathomed_min, open_min, UB)
    return dict(LB=LB, UB=UB, x=ubpt, processed=nproc, open=lo.shape[0], done=lo.shape[0] == 0, time=time.time() - t0)


def main(name, tol_rel=1e-9, tlim=3600):
    import os
    sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave2/small")
    import ev
    P = Prob(name)
    print(f"== {name}: {P.d} decision vars ({P.isint.sum()} integer), {P.R} rows ({P.objrows.sum()} objective rows)")
    here = os.path.dirname(os.path.abspath(__file__))
    vals = ev.read_sol(os.path.join(here, "..", "sol", f"{name}.p1.sol"))
    x0 = np.array([float(vals.get(n, "0")) for n in P.M["names"]])
    f0, _ = P.fpoint(x0[None, :])
    print(f"listed p1 (double-rounded): rigorous F = {f0[0]!r}")
    xl = local_minimax(P, x0)
    fl, _ = P.fpoint(xl[None, :])
    print(f"polished p1: F = {fl[0]!r} at {xl.tolist()}")
    xi = xl if fl[0] < f0[0] else x0
    UB0 = min(fl[0], f0[0])
    tol_abs = tol_rel * max(1.0, abs(UB0) if np.isfinite(UB0) else 10.0)
    res = branch_and_bound(P, tol_abs, tlim, x_inc=xi)
    print(f"B&B: done={res['done']} processed {res['processed']} open {res['open']} time {res['time']:.0f}s")
    print(f"  min in [{res['LB']!r}, {res['UB']!r}]  tol_abs {tol_abs:.2e}")
    print(f"  best point {res['x'].tolist()}")
    return P, res


if __name__ == "__main__":
    name = sys.argv[1]
    tol = float(sys.argv[2]) if len(sys.argv) > 2 else 1e-9
    tl = float(sys.argv[3]) if len(sys.argv) > 3 else 3600
    main(name, tol, tl)
