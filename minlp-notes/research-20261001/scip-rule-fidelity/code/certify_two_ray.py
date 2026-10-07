"""Exact certificate that the corner bounds z_K stored for some corners of the sfree note's
Section 9.2 runs (exp_mccormick_11_final.json, exp_mccormick_12_big_final.json) are wrong.

The corner is regenerated exactly as research-20260928b/sfree/code/exp_mccormick.py does it
(same seeding, HiGHS basis, most violated product, floor w >= 1e-9 max(1, max w)).  Its
floating-point data (sbar, P, w) are converted exactly to rationals; all checks below are in
exact rational arithmetic on that data.

  upper bound: a rational point lam >= 0 with q(sbar + P lam) <= 0 and w^T lam = z_up;
  lower bound: for every single ray and every pair of rays J, q(sbar + P_J mu) > 0 on the
               triangle {mu >= 0, w_J^T mu <= z_low}.  For bilinear q (rho = 2) Theorem 4 of the
               sfree note says some minimizer uses at most 2 rays (Lemma 3 gives one with P_J
               injective), so z_K >= z_low.
  bug witness: core.two_ray's returned point for the pair core.corner_bound picks, with its
               exact q value (positive = the returned 'minimizer' is infeasible).
Usage: python3 certify_two_ray.py SEED NTRIALS RECORDS.json [p npairs nlin]
"""
import os, sys, json
from fractions import Fraction as Fr
import numpy as np
SFREE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../research-20260928b/sfree/code')
sys.path.insert(0, SFREE)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exp_mccormick as E
import core
from core import bilinear_quadratic
import zk_fast as Z


def fr(x):
    return Fr(float(x))


def qpair(Q, b, c, sb, PJ):
    """q(sbar + PJ mu) = mu^T G mu + 2 m^T mu + g0, exact."""
    k, J = len(sb), len(PJ[0])
    Qs = [sum(Q[i][j] * sb[j] for j in range(k)) for i in range(k)]
    g0 = sum(sb[i] * Qs[i] for i in range(k)) + sum(b[i] * sb[i] for i in range(k)) + c
    QP = [[sum(Q[i][l] * PJ[l][a] for l in range(k)) for a in range(J)] for i in range(k)]
    G = [[sum(PJ[i][a] * QP[i][bb] for i in range(k)) for bb in range(J)] for a in range(J)]
    m = [sum(PJ[i][a] * (Qs[i] + b[i] / 2) for i in range(k)) for a in range(J)]
    return G, m, g0


def min_on_segment(f2, f1, f0):
    """min over t in [0, 1] of f2 t^2 + f1 t + f0, exact."""
    vals = [f0, f2 + f1 + f0]
    if f2 > 0:
        t = -f1 / (2 * f2)
        if 0 < t < 1:
            vals.append(f2 * t * t + f1 * t + f0)
    return min(vals)


def positive_on_triangle(G, m, g0, wJ, z):
    """q > 0 on {mu >= 0, wJ^T mu <= z} (len(wJ) in {1, 2}), exact."""
    if len(wJ) == 1:
        L = z / wJ[0]                          # mu in [0, L]
        return min_on_segment(G[0][0] * L * L, 2 * m[0] * L, g0) > 0
    A = [z / wJ[0], Fr(0)]; B = [Fr(0), z / wJ[1]]
    V = [[Fr(0), Fr(0)], A, B]

    def restr(P0, P1):                         # q(P0 + t (P1 - P0)) coefficients
        d = [P1[0] - P0[0], P1[1] - P0[1]]
        Gd = [G[0][0] * d[0] + G[0][1] * d[1], G[1][0] * d[0] + G[1][1] * d[1]]
        GP = [G[0][0] * P0[0] + G[0][1] * P0[1], G[1][0] * P0[0] + G[1][1] * P0[1]]
        f2 = d[0] * Gd[0] + d[1] * Gd[1]
        f1 = 2 * (P0[0] * Gd[0] + P0[1] * Gd[1]) + 2 * (m[0] * d[0] + m[1] * d[1])
        f0 = P0[0] * GP[0] + P0[1] * GP[1] + 2 * (m[0] * P0[0] + m[1] * P0[1]) + g0
        return f2, f1, f0
    for P0, P1 in ((V[0], V[1]), (V[1], V[2]), (V[2], V[0])):
        if min_on_segment(*restr(P0, P1)) <= 0:
            return False
    det = G[0][0] * G[1][1] - G[0][1] * G[1][0]
    if G[0][0] > 0 and det > 0:                # interior stationary point of a convex q
        mu = [-(G[1][1] * m[0] - G[0][1] * m[1]) / det, -(-G[1][0] * m[0] + G[0][0] * m[1]) / det]
        if mu[0] > 0 and mu[1] > 0 and wJ[0] * mu[0] + wJ[1] * mu[1] < z:
            val = (mu[0] * (G[0][0] * mu[0] + G[0][1] * mu[1]) + mu[1] * (G[1][0] * mu[0] + G[1][1] * mu[1])
                   + 2 * (m[0] * mu[0] + m[1] * mu[1]) + g0)
            if val <= 0:
                return False
    return True


def main():
    seed, T, recf = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    SIZE = tuple(int(a) for a in sys.argv[4:7]) if len(sys.argv) > 6 else (4, 4, 3)
    recs = {r['trial']: r for r in json.load(open(recf))['records']}
    E.rng = np.random.default_rng(seed)
    for trial in range(T):
        I = E.make_instance(*SIZE)
        if trial not in recs:
            continue
        h, A, bb = E.solve_lp(I)
        x, R, w, Ab, rhs, zlp = E.basis_cone(I, h, A, bb)
        p = I['p']
        viol = [(abs(x[p + e] - x[i] * x[j]), e) for e, (i, j) in enumerate(I['pairs'])]
        vmax, e = max(viol)
        i, j = I['pairs'][e]; idx = [i, j, p + e]
        sbar = x[idx]; side = '+' if sbar[2] > sbar[0] * sbar[1] else '-'
        Q, bq, cq = bilinear_quadratic(side); P = R[idx, :]
        wpos = np.maximum(w, 1e-9 * max(1.0, w.max()))
        Qr, br, cr, sr, Pr, rho, _ = Z.reduce_space(Q, bq, cq, sbar, P)
        zf, arg = Z.zK_upto2(Qr, br, cr, sr, Pr, wpos)
        zs = recs[trial]['zK']
        if abs(zf - zs) <= 1e-6 * zf:
            continue
        # exact data
        k, N = 3, P.shape[1]
        Qe = [[fr(Q[a][b_]) for b_ in range(k)] for a in range(k)]
        be = [fr(v) for v in bq]; ce = fr(cq)
        se = [fr(v) for v in sbar]; Pe = [[fr(P[a][b_]) for b_ in range(N)] for a in range(k)]
        we = [fr(v) for v in wpos]
        # upper bound: scale zk_fast's minimizer outward until exactly feasible
        lam = np.zeros(N)
        if len(arg) == 1:
            t, _ = Z.one_ray_vec(Q, bq, cq, sbar, P[:, list(arg)]); lam[arg[0]] = t[0]
        else:
            # pair optimum by a fine theta grid (independent of core.two_ray)
            th = np.linspace(0, 1, 200001)
            Dm = np.outer(P[:, arg[0]] / wpos[arg[0]], th) + np.outer(P[:, arg[1]] / wpos[arg[1]], 1 - th)
            tt, _ = Z.one_ray_vec(Q, bq, cq, sbar, Dm)
            m_ = int(np.argmin(tt))
            lam[arg[0]] = tt[m_] * th[m_] / wpos[arg[0]]; lam[arg[1]] = tt[m_] * (1 - th[m_]) / wpos[arg[1]]
        ok_up = None
        for scale in (1.0, 1 + 1e-12, 1 + 1e-10, 1 + 1e-8, 1 + 1e-6, 1 + 1e-4):
            le = [fr(v * scale) for v in lam]
            pt = [se[a] + sum(Pe[a][b_] * le[b_] for b_ in range(N)) for a in range(k)]
            qv = sum(pt[a] * sum(Qe[a][b_] * pt[b_] for b_ in range(k)) for a in range(k)) + sum(be[a] * pt[a] for a in range(k)) + ce
            if qv <= 0:
                ok_up = sum(we[b_] * le[b_] for b_ in range(N)); break
        # lower bound: all supports of size <= 2
        z_low = fr(zf) * Fr(999, 1000)
        allpos = True
        for a in range(N):
            G, m, g0 = qpair(Qe, be, ce, se, [[Pe[r][a]] for r in range(k)])
            if not positive_on_triangle(G, m, g0, [we[a]], z_low):
                allpos = False
        for a in range(N):
            for b_ in range(a + 1, N):
                G, m, g0 = qpair(Qe, be, ce, se, [[Pe[r][a], Pe[r][b_]] for r in range(k)])
                if not positive_on_triangle(G, m, g0, [we[a], we[b_]], z_low):
                    allpos = False
        # witness of the faulty value: core.corner_bound's pair and core.two_ray's returned point
        zc = core.corner_bound(Q, bq, cq, sbar, P, wpos)
        wit = None
        for a in range(N):
            for b_ in range(a + 1, N):
                v, li, lj = core.two_ray(Q, bq, cq, sbar, P, a, b_, wpos)
                if np.isfinite(v) and abs(v - zc) <= 1e-12 * max(1.0, abs(zc)) and li is not None:
                    pt = [se[r] + Pe[r][a] * fr(li) + Pe[r][b_] * fr(lj) for r in range(k)]
                    qv = sum(pt[r] * sum(Qe[r][t] * pt[t] for t in range(k)) for r in range(k)) + sum(be[r] * pt[r] for r in range(k)) + ce
                    Pn = P[:, [a, b_]] / np.linalg.norm(P[:, [a, b_]], axis=0)
                    wit = dict(pair=(a, b_), value=v, lam=(li, lj), q_exact=float(qv), cos=float(Pn[:, 0] @ Pn[:, 1]),
                               cos_scaled=float(np.dot(P[:, a] / wpos[a], P[:, b_] / wpos[b_]) /
                                                (np.linalg.norm(P[:, a] / wpos[a]) * np.linalg.norm(P[:, b_] / wpos[b_]))))
                    break
            if wit:
                break
        print(json.dumps(dict(seed=seed, trial=trial, zK_stored=zs, zK_core_now=zc, zK_fast=zf, support=list(arg),
                              z_low=float(z_low), lower_bound_certified=allpos,
                              z_up=None if ok_up is None else float(ok_up), upper_bound_certified=ok_up is not None,
                              stored_below_certified_lower=bool(allpos and fr(zs) < z_low), faulty_pair_witness=wit)), flush=True)


if __name__ == '__main__':
    main()
