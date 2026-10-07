"""Rigorous best-first branch and bound for eg_int_s / eg_disc_s / eg_disc2_s.

Per box (instance coordinates; integer coordinates relaxed to integer intervals until
split to single values):
  1. affine minorants/majorants of every row from the Taylor model (egfast.Fast.taylor),
     and the natural enclosure on large boxes;
  2. row bound  lb0 = max_k (c_k + min_box minorant_k)  and side-row infeasibility;
  3. domain reduction (interval propagation, 2 rounds) on the linear inequalities
        c_k + minorant_k(x) <= theta  (objective cut, theta = UB - tol)
        minorant_s(x) <= ghi_s,  majorant_s(x) >= glo_s  (side rows);
     integer coordinates are rounded inward;
  4. an LP over the affine models (min t, t >= c_k + minorant_k, side rows, reduced box);
     its dual vector is evaluated in outward-rounded interval arithmetic (weak duality),
     so a poor LP solution can only weaken the bound.  If the LP is infeasible, a phase-1
     LP over the side rows and the objective cuts gives a Farkas vector, again checked in
     interval arithmetic.
Coverage: every feasible point lies in an open box, in a box with lb >= theta (closed),
in a part removed by steps 3-4 (F > theta there, or infeasible), or in a box proved
infeasible.  Certified bound = min(theta_min, open keys, forced-closed boxes, UB).

    python3 egbb.py <name> <tol_rel> <time_s> [save.npz|-] [resume.npz|-] [k K]
(k K: run only part k of K of the integer coordinate with the largest range; the parts
cover the domain, so the minimum of the parts' bounds is a bound for the instance)
"""
import os
import sys
import time

import highspy
import numpy as np

import egfast
import egtm
from egtm import NI, dn, up

INF = np.inf
HINF = highspy.kHighsInf


def lin_min(beta, dl, dh):
    """rigorous lower bound of beta . d over d in [dl, dh]: (N, R)."""
    t = dn(np.minimum(beta * dl[:, None, :], beta * dh[:, None, :]))
    n = t.shape[-1]
    return dn(t.sum(-1) - (n + 2) * egtm.U * np.abs(t).sum(-1) - 1e-300)


def lin_max(beta, dl, dh):
    t = up(np.maximum(beta * dl[:, None, :], beta * dh[:, None, :]))
    n = t.shape[-1]
    return up(t.sum(-1) + (n + 2) * egtm.U * np.abs(t).sum(-1) + 1e-300)


def fbbt(A, b, dl, dh, rounds=2):
    """interval propagation for rows A[n,j,:] . d <= b[n,j] over d in [dl, dh] (outward rounded).
    Returns new dl, dh and an infeasibility flag (N,)."""
    N, J, d = A.shape
    dl = dl.copy(); dh = dh.copy()
    infeas = np.zeros(N, bool)
    for _ in range(rounds):
        tmin = dn(np.minimum(A * dl[:, None, :], A * dh[:, None, :]))       # (N, J, d)
        tmin = np.where(A == 0, 0.0, tmin)
        tot = dn(tmin.sum(-1) - (d + 2) * egtm.U * np.abs(tmin).sum(-1) - 1e-300)   # <= sum
        infeas |= np.any(tot > b, axis=1)
        rest = dn(tot[..., None] - tmin)                                      # <= sum_{j != i}
        with np.errstate(invalid="ignore", over="ignore"):
            num = up(b[..., None] - rest)
        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            qp = up(num / A)                                                  # A > 0: d_i <= qp
            qn = dn(num / A)                                                  # A < 0: d_i >= qn
        ok = np.isfinite(num) & (np.abs(A) > 1e-12)
        dh = np.minimum(dh, np.where(ok & (A > 0), qp, INF).min(axis=1))
        dl = np.maximum(dl, np.where(ok & (A < 0), qn, -INF).max(axis=1))
        infeas |= np.any(dl > dh, axis=1)
    return dl, dh, infeas


class LP:
    """min cost.x s.t. A x <= b, lb <= x <= ub (dense, small) with a reused HiGHS instance.
    Only its dual vector is used, and only after a rigorous re-evaluation."""

    def __init__(self):
        self.h = highspy.Highs()
        self.h.setOptionValue("output_flag", False)
        self.n = 0
        self.t = 0.0

    def solve(self, cost, A, b, lb, ub):
        t0 = time.time()
        m, n = A.shape
        lp = highspy.HighsLp()
        lp.num_col_ = n
        lp.num_row_ = m
        lp.col_cost_ = cost
        lp.col_lower_ = np.where(np.isfinite(lb), lb, -HINF)
        lp.col_upper_ = np.where(np.isfinite(ub), ub, HINF)
        lp.row_lower_ = np.full(m, -HINF)
        lp.row_upper_ = b
        lp.a_matrix_.format_ = highspy.MatrixFormat.kRowwise
        lp.a_matrix_.start_ = np.arange(0, m * n + 1, n, dtype=np.int32)
        lp.a_matrix_.index_ = np.tile(np.arange(n, dtype=np.int32), m)
        lp.a_matrix_.value_ = np.ascontiguousarray(A, dtype=np.float64).ravel()
        self.h.passModel(lp)
        self.h.run()
        st = self.h.getModelStatus()
        sol = self.h.getSolution()
        self.n += 1
        self.t += time.time() - t0
        if st == highspy.HighsModelStatus.kOptimal:
            return "opt", np.maximum(-np.array(sol.row_dual), 0.0)
        if st == highspy.HighsModelStatus.kInfeasible:
            return "inf", None
        return "other", None


class BB:
    def __init__(self, name, tol_abs, natural_rel=1.0 / 16, log=print):
        # EGMODEL=ni selects the slower interval-arithmetic models of egtm.Model (independent
        # of the float error analysis in egfast); default: egfast.Fast
        self.M = egtm.Model(name) if os.environ.get("EGMODEL") == "ni" else egfast.Fast(name)
        self.tol = tol_abs
        self.natural_rel = natural_rel
        self.log = log
        M = self.M
        self.width0 = np.maximum(M.hi0 - M.lo0, 1e-300)
        self.lp = LP()
        self.stats = dict(lp_close=0, farkas=0, fbbt_close=0, row_close=0)

    # ------------------------------------------------------------------ primal
    def fpoint(self, x, fast=False):
        """rigorous objective upper bound at float points x (N, d); inf if not strictly feasible
        (side rows checked against inner-rounded bounds, point in the inner box, integers integral)."""
        M = self.M
        g = M.natural(x, x) if fast else M.point(x)
        inbox = np.all((x >= M.lo_in) & (x <= M.hi_in), axis=1) & np.all(
            (~M.isint) | (np.round(x) == x), axis=1)
        feas = np.all((g.lo[:, 24:] >= M.glo_in) & (g.hi[:, 24:] <= M.ghi_in), axis=1)
        f = up(M.c_hi[None, :] + g.hi[:, :24]).max(axis=1)
        return np.where(inbox & feas, f, INF)

    # ------------------------------------------------------------------ bounding
    def bound(self, lo, hi, theta):
        """returns lb (N,), reduced lo/hi, split scores (N, d)."""
        M = self.M
        N, d = lo.shape
        T = M.taylor(lo, hi)
        c, beta, aL, aU = T["c"], T["beta"], T["aL"], T["aU"]
        fixed = hi == lo                       # then c = lo exactly and d = 0
        dl = np.where(fixed, 0.0, np.minimum(dn(lo - c), 0.0))
        dh = np.where(fixed, 0.0, np.maximum(up(hi - c), 0.0))
        with np.errstate(invalid="ignore"):
            rmin = dn(aL + lin_min(beta, dl, dh))                              # (N, R) lower bounds of g
            rmax = up(aU + lin_max(beta, dl, dh))
        rmin = np.where(np.isnan(rmin), -INF, rmin)
        rmax = np.where(np.isnan(rmax), INF, rmax)
        big = np.any((hi - lo) > self.natural_rel * self.width0, axis=1)
        if big.any():
            nat = M.natural(lo[big], hi[big])
            rmin[big] = np.maximum(rmin[big], nat.lo)
            rmax[big] = np.minimum(rmax[big], nat.hi)
        objlb = dn(M.c_lo[None, :] + rmin[:, :24])
        lb = objlb.max(axis=1)
        sviol = (rmin[:, 24:] > M.ghi[None, :]) | (rmax[:, 24:] < M.glo[None, :])
        infeas = np.any(sviol, axis=1)
        lb = np.where(infeas, INF, lb)
        straddle = (rmax[:, 24:] > M.ghi[None, :]) | (rmin[:, 24:] < M.glo[None, :])
        self.stats["row_close"] += int((lb >= theta).sum())
        newlo, newhi = lo.copy(), hi.copy()
        duals = {}
        act = lb < theta
        ia = np.where(act)[0]
        if len(ia) and not os.environ.get("EG_NOFBBT"):
            # ---- domain reduction on the affine models (rows with infinite constants drop out)
            with np.errstate(invalid="ignore", over="ignore"):
                b_obj = up(up(theta - M.c_lo[None, :]) - aL[ia, :24])
                b_up = up(M.ghi[None, :] - aL[ia, 24:])
                b_lo = up(aU[ia, 24:] - M.glo[None, :])
            A = np.concatenate([beta[ia, :24], beta[ia, 24:], -beta[ia, 24:]], axis=1)
            b = np.concatenate([b_obj, b_up, b_lo], axis=1)
            b = np.where(np.isnan(b), INF, b)
            dl2, dh2, inf2 = fbbt(A, b, dl[ia], dh[ia])
            nlo = np.maximum(lo[ia], dn(c[ia] + dl2))
            nhi = np.minimum(hi[ia], up(c[ia] + dh2))
            isi = M.isint[None, :]
            nlo = np.where(isi, np.ceil(nlo), nlo)
            nhi = np.where(isi, np.floor(nhi), nhi)
            inf2 |= np.any(nlo > nhi, axis=1)
            lb[ia[inf2]] = INF
            self.stats["fbbt_close"] += int(inf2.sum())
            nlo = np.where(inf2[:, None], lo[ia], nlo)
            nhi = np.where(inf2[:, None], hi[ia], nhi)
            newlo[ia], newhi[ia] = nlo, nhi
        if len(ia) and not os.environ.get("EG_NOLP"):
            inf2 = lb[ia] == INF
            # ---- LP over the affine models on the reduced boxes (offsets d = x - c, outward)
            for jj, n in enumerate(ia):
                if inf2[jj]:
                    continue
                fx = (newhi[n] == newlo[n]) & (newlo[n] == c[n])
                dln = np.where(fx, 0.0, np.minimum(dn(newlo[n] - c[n]), 0.0))
                dhn = np.where(fx, 0.0, np.maximum(up(newhi[n] - c[n]), 0.0))
                v, info = self.lp_bound(n, beta, aL, aU, dln, dhn, theta)
                if v > lb[n]:
                    lb[n] = v
                if info is not None:
                    duals[n] = info
        return lb, newlo, newhi, self.scores(T, duals, objlb, straddle)

    def _rows(self, n, beta, aL, aU, theta, with_cut):
        """affine rows a . d <= b (floats, LP data only) with tags: ('obj', k) for t-rows,
        ('cut', k), ('up', s), ('lo', s)."""
        M = self.M
        rows, rhs, tags = [], [], []
        for k in range(24):
            if np.isfinite(aL[n, k]):
                rows.append(beta[n, k]); rhs.append(-(M.c_lo[k] + aL[n, k])); tags.append(("obj", k))
                if with_cut:
                    rows.append(beta[n, k]); rhs.append(theta - M.c_lo[k] - aL[n, k]); tags.append(("cut", k))
        for j, s in enumerate(range(24, 28)):
            if np.isfinite(M.ghi[j]) and np.isfinite(aL[n, s]):
                rows.append(beta[n, s]); rhs.append(M.ghi[j] - aL[n, s]); tags.append(("up", s))
            if np.isfinite(M.glo[j]) and np.isfinite(aU[n, s]):
                rows.append(-beta[n, s]); rhs.append(aU[n, s] - M.glo[j]); tags.append(("lo", s))
        return np.array(rows).reshape(len(tags), -1), np.array(rhs), tags

    def lp_bound(self, n, beta, aL, aU, dl, dh, theta):
        d = self.M.d
        A, b, tags = self._rows(n, beta, aL, aU, theta, with_cut=False)
        isobj = np.array([t[0] == "obj" for t in tags], dtype=bool)
        if not isobj.any():
            return -INF, None
        Ax = np.hstack([A, np.where(isobj, -1.0, 0.0)[:, None]])
        cost = np.zeros(d + 1); cost[-1] = 1.0
        st, y = self.lp.solve(cost, Ax, b, np.append(dl, -INF), np.append(dh, INF))
        if st == "opt":
            val = self.dual_value(n, y, tags, beta, aL, aU, dl, dh, theta)
            if val >= theta:
                self.stats["lp_close"] += 1
            return val, (y, tags)
        if st == "inf":
            # phase 1 with the objective cuts: min s, a . d - s <= b over side rows and cuts
            A2, b2, tags2 = self._rows(n, beta, aL, aU, theta, with_cut=True)
            keep = np.array([t[0] != "obj" for t in tags2], dtype=bool)
            A2, b2 = A2[keep], b2[keep]
            tags2 = [t for t, k in zip(tags2, keep) if k]
            Ax2 = np.hstack([A2, -np.ones((len(tags2), 1))])
            st2, z = self.lp.solve(cost, Ax2, b2, np.append(dl, -INF), np.append(dh, INF))
            if st2 == "opt" and self.farkas(n, z, tags2, beta, aL, aU, dl, dh, theta):
                self.stats["farkas"] += 1
                return INF, None
        return -INF, None

    def _combine(self, n, mult, tags, beta, aL, aU, theta):
        """interval enclosure of sum_j mult_j row_j(d) = const + coef . d, where
        'obj' rows contribute mult (c_k + aL_k + beta_k . d)  (<= mult F for every point), and
        'cut' (c_k + aL_k + beta_k . d - theta), 'up' (aL_s + beta_s . d - ghi_s) and
        'lo' (glo_s - aU_s - beta_s . d) are <= 0 at every feasible point with F <= theta."""
        M = self.M
        const = NI(0.0)
        coef = NI(np.zeros(M.d))
        for (kind, k), mu in zip(tags, mult):
            if not mu > 0:
                continue
            Mu = NI(mu)
            B = NI(beta[n, k])
            if kind == "obj":
                const = const + Mu * (NI(M.c_lo[k]) + aL[n, k])
                coef = coef + Mu * B
            elif kind == "cut":
                const = const + Mu * ((NI(M.c_lo[k]) + aL[n, k]) - theta)
                coef = coef + Mu * B
            elif kind == "up":
                const = const + Mu * (NI(aL[n, k]) - M.ghi[k - 24])
                coef = coef + Mu * B
            else:
                const = const + Mu * (NI(M.glo[k - 24]) - aU[n, k])
                coef = coef - Mu * B
        return const, coef

    def dual_value(self, n, y, tags, beta, aL, aU, dl, dh, theta):
        """For every feasible point x = c + d of the box:
        (sum_obj y_k) F(x) >= sum_obj y_k (c_k + aL_k + beta_k.d) >= that + sum_side z (row <= 0).
        Returns a rigorous lower bound of F over the box (division by sum y > 0 in intervals)."""
        isobj = np.array([t[0] == "obj" for t in tags], dtype=bool)
        y = np.where(isobj | np.array([t[0] in ("up", "lo") for t in tags], dtype=bool), y, 0.0)
        ys = y[isobj]
        if not ys.sum() > 0:
            return -INF
        const, coef = self._combine(n, y, tags, beta, aL, aU, theta)
        val = const + egtm.isum(coef * NI(dl, dh), axis=-1)
        S = egtm.isum(NI(ys), axis=-1)
        vl = float(val.lo)
        if vl >= 0:
            q = vl / float(S.hi)
        elif float(S.lo) > 0:
            q = vl / float(S.lo)
        else:      # sum y not proved > 0: no bound from this dual vector (guard added after review)
            return -INF
        return float(dn(q)) if np.isfinite(q) else -INF

    def farkas(self, n, z, tags, beta, aL, aU, dl, dh, theta):
        """True if sum_j z_j row_j(d) > 0 on the whole box: then no feasible point with F <= theta."""
        assert all(t[0] != "obj" for t in tags)
        if not np.any(z > 0):
            return False
        const, coef = self._combine(n, z, tags, beta, aL, aU, theta)
        val = const + egtm.isum(coef * NI(dl, dh), axis=-1)
        return bool(float(val.lo) > 0)

    def scores(self, T, duals, objlb, straddle):
        """split scores: estimated loss of the affine models per coordinate, weighted by the LP
        multipliers (or the leading objective row) plus the side rows not yet proved satisfied."""
        r = T["r"]
        loss = r[:, None, :] * np.einsum("nkij,nj->nki", T["Hmag"], r)          # (N, R, d)
        with np.errstate(over="ignore", invalid="ignore"):
            sens = np.einsum("nkm,nkmi->nki", T["Wabs"] * 0.5 * (T["ell"] + T["qq"]) ** 2
                             * np.exp(np.minimum(T["ell"], 50.0)), T["Vabs"]) * r[:, None, :]
            tot = loss + sens
        tot = np.where(np.isfinite(tot), tot, 1e300)
        N = r.shape[0]
        w = np.zeros((N, tot.shape[1]))
        w[np.arange(N), np.argmax(objlb, axis=1)] = 1.0
        for n, (y, tags) in duals.items():
            isobj = np.array([t[0] == "obj" for t in tags], dtype=bool)
            ys = max(y[isobj].sum(), 1e-300)
            w[n, :] = 0.0
            for (kind, k), mu in zip(tags, y):
                w[n, k] += mu / ys
        w[:, 24:] += straddle
        return np.einsum("nk,nki->ni", w, tot)

    # ------------------------------------------------------------------ driver
    def run(self, tlim, UB, xbest, lo0=None, hi0=None, init=None, batch=256, log_every=20, save=None,
            polish=None, ncand=4):
        M = self.M
        t0 = time.time()
        if init is not None:
            lo, hi, key = init
        else:
            lo = (M.lo0 if lo0 is None else lo0)[None, :].copy()
            hi = (M.hi0 if hi0 is None else hi0)[None, :].copy()
            key = np.array([-INF])
        theta_min = INF
        forced_min = INF
        nproc = 0
        it = 0
        polished = set()
        while lo.shape[0] > 0 and time.time() - t0 < tlim:
            it += 1
            theta = UB - self.tol
            assert np.isfinite(theta)
            m = min(batch, lo.shape[0])
            if lo.shape[0] > m:
                idx = np.argpartition(key, m - 1)
                sel, rest = idx[:m], idx[m:]
                blo, bhi, bkey = lo[sel], hi[sel], key[sel]
                lo, hi, key = lo[rest], hi[rest], key[rest]
            else:
                blo, bhi, bkey = lo, hi, key
                lo, hi, key = lo[:0], hi[:0], key[:0]
            theta_min = min(theta_min, theta)      # closing at level theta (pre-check, cuts, lb >= theta)
            pre = bkey >= theta
            blo, bhi, bkey = blo[~pre], bhi[~pre], bkey[~pre]
            if blo.shape[0] == 0:
                continue
            nproc += blo.shape[0]
            lb, nlo, nhi, sc = self.bound(blo, bhi, theta)
            lb = np.where(np.isnan(lb), -INF, lb)      # NaN guard: never close a box on a NaN bound
            lb = np.maximum(lb, bkey)
            # primal candidates: centres of the reduced boxes with the lowest bounds, integers rounded
            order = np.argsort(np.where(np.isfinite(lb), lb, INF))[:ncand]
            cand = 0.5 * (nlo[order] + nhi[order])
            cand[:, M.isint] = np.clip(np.round(cand[:, M.isint]), nlo[order][:, M.isint], nhi[order][:, M.isint])
            cand = np.clip(cand, M.lo_in, M.hi_in)
            if len(order):
                fc = self.fpoint(cand, fast=True)
                j = int(np.argmin(fc))
                if fc[j] < UB:
                    f = self.fpoint(cand[j][None])[0]           # confirm on the interval path
                    if f < UB:
                        UB, xbest = float(f), cand[j].copy()
                if polish is not None:
                    ci = tuple(cand[0][M.isint].astype(int))
                    if ci not in polished:
                        polished.add(ci)
                        xp = polish(cand[0])
                        if xp is not None:
                            f = self.fpoint(xp[None])[0]
                            if f < UB:
                                UB, xbest = float(f), xp.copy()
            keep = lb < UB - self.tol
            nlo, nhi, lb, sc = nlo[keep], nhi[keep], lb[keep], sc[keep]
            if nlo.shape[0] == 0:
                continue
            w = nhi - nlo
            sc = np.where(w > 0, sc, -1.0)
            k = np.argmax(sc, axis=1)
            r_ = np.arange(len(k))
            tiny = w[r_, k] <= 1e-13 * np.maximum(1.0, np.abs(nlo[r_, k]))
            if tiny.any():
                forced_min = min(forced_min, float(lb[tiny].min()))
                nlo, nhi, lb, k = nlo[~tiny], nhi[~tiny], lb[~tiny], k[~tiny]
                r_ = np.arange(len(k))
            mid = 0.5 * (nlo[r_, k] + nhi[r_, k])
            isi = M.isint[k]
            mlo = np.where(isi, np.floor(mid), mid)
            mhi = np.where(isi, np.floor(mid) + 1, mid)
            lo1, hi1 = nlo.copy(), nhi.copy(); hi1[r_, k] = mlo
            lo2, hi2 = nlo.copy(), nhi.copy(); lo2[r_, k] = mhi
            lo = np.concatenate([lo, lo1, lo2]); hi = np.concatenate([hi, hi1, hi2])
            key = np.concatenate([key, lb, lb])
            if it % log_every == 0:
                omin = key.min() if key.size else INF
                self.log(f"  it {it} processed {nproc} open {lo.shape[0]} UB {UB:.12g} LB "
                         f"{min(theta_min, omin, forced_min, UB):.12g} lp {self.lp.n} ({self.lp.t:.0f}s) "
                         f"{self.stats} t {time.time()-t0:.0f}s")
                sys.stdout.flush()
                if save is not None and it % (log_every * 10) == 0:
                    np.savez(save, lo=lo, hi=hi, key=key, UB=UB, xbest=xbest,
                             theta_min=min(theta_min, UB - self.tol), forced_min=forced_min)
        omin = key.min() if key.size else INF
        # every box closed so far had a bound >= the cutoff in force at that time, and every
        # cutoff is >= UB - tol for the final UB
        theta_min = min(theta_min, UB - self.tol)
        LB = min(theta_min, omin, forced_min, UB)
        if save is not None:
            np.savez(save, lo=lo, hi=hi, key=key, UB=UB, xbest=xbest, theta_min=theta_min, forced_min=forced_min)
        return dict(LB=LB, UB=UB, x=xbest, processed=nproc, open=lo.shape[0], done=lo.shape[0] == 0,
                    time=time.time() - t0, theta_min=theta_min, omin=omin, forced_min=forced_min)


def make_polish(bb):
    """local minimax solve (SLSQP, integers fixed) followed by a push into the interior of
    nearly active side rows; the caller certifies the point with bb.fpoint."""
    import explore
    D = bb.M.D
    cont = ~D.isint

    def push(x, margin):
        for _ in range(30):
            g, G = D.g(x[None])
            gs = g[0, 24:]
            worst = None
            for j in range(4):
                if np.isfinite(D.ghi[24 + j]) and gs[j] > D.ghi[24 + j] - margin:
                    worst = (j, +1, gs[j] - (D.ghi[24 + j] - margin))
                if np.isfinite(D.glo[24 + j]) and gs[j] < D.glo[24 + j] + margin:
                    worst = (j, -1, (D.glo[24 + j] + margin) - gs[j])
            if worst is None:
                return x
            j, sg, amt = worst
            gr = G[0, 24 + j] * cont
            nrm = float(gr @ gr)
            if nrm == 0:
                return x
            x = np.clip(x - sg * (amt * 1.5 + 1e-16) * gr / nrm, bb.M.lo_in, bb.M.hi_in)
        return x

    def polish(x0):
        try:
            x, f, v = explore.local(D, x0.copy(), cont, margin=1e-9)
        except Exception:
            return None
        x = np.clip(x, bb.M.lo_in, bb.M.hi_in)
        best, fb = None, INF
        for margin in (1e-13, 1e-12, 1e-11, 1e-10):     # smallest push that is certified feasible
            xp = push(x.copy(), margin)
            f = bb.fpoint(xp[None])[0]
            if f < fb:
                best, fb = xp, f
            if np.isfinite(f):
                break
        return best
    return polish


def main():
    name = sys.argv[1]
    tol_rel = float(sys.argv[2])
    tlim = float(sys.argv[3])
    save = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != "-" else None
    resume = sys.argv[5] if len(sys.argv) > 5 and sys.argv[5] != "-" else None
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(here, "..", "..", "..", "open-instances-wave2", "small"))
    import ev
    bb = BB(name, 0.0)
    M = bb.M
    vals = ev.read_sol(os.path.join(here, "..", "..", "sol", f"{name}.p1.sol"))
    x0 = np.array([float(vals.get(n, "0")) for n in M.D.M["names"]])
    pol = make_polish(bb)
    xp = pol(x0)
    f0 = bb.fpoint(x0[None])[0]
    fp = bb.fpoint(xp[None])[0] if xp is not None else INF
    UB, xb = (fp, xp) if fp < f0 else (f0, x0)
    print(f"== {name}: listed p1 rigorous F = {f0!r}; polished F = {fp!r}", flush=True)
    bb.tol = tol_rel * max(1.0, abs(UB) if np.isfinite(UB) else 10.0)
    init = None
    if resume:
        z = np.load(resume)
        init = (z["lo"], z["hi"], z["key"])
        if float(z["UB"]) < UB:
            UB, xb = float(z["UB"]), z["xbest"]
        print(f"resumed {init[0].shape[0]} open boxes from {resume}; previous theta_min {float(z['theta_min'])!r} "
              f"forced_min {float(z['forced_min'])!r}")
    lo0, hi0 = M.lo0.copy(), M.hi0.copy()
    if len(sys.argv) > 7:      # part k of K: split the integer coordinate with the largest range
        k, K = int(sys.argv[6]), int(sys.argv[7])
        ii = np.where(M.isint)[0]
        j = ii[np.argmax(hi0[ii] - lo0[ii])]
        vals_j = np.arange(lo0[j], hi0[j] + 1)
        chunks = np.array_split(vals_j, K)
        lo0[j], hi0[j] = chunks[k][0], chunks[k][-1]
        print(f"part {k} of {K}: {M.D.M['names'][j]} in [{lo0[j]:g}, {hi0[j]:g}]")
    r = bb.run(tlim, UB, xb, lo0=lo0, hi0=hi0, init=init, save=save, polish=pol)
    if resume:     # the closed part of the earlier run(s) still counts
        r["LB"] = min(r["LB"], float(z["theta_min"]), float(z["forced_min"]))
    print(f"B&B: done={r['done']} processed {r['processed']} open {r['open']} time {r['time']:.0f}s "
          f"lp {bb.lp.n} ({bb.lp.t:.0f}s) {bb.stats}")
    print(f"  certified lower bound {r['LB']!r} (theta_min {r['theta_min']!r}, open min {r['omin']!r}, "
          f"forced {r['forced_min']!r}); UB {r['UB']!r} at {np.asarray(r['x']).tolist()}")


if __name__ == "__main__":
    main()
