"""Ground truth for z_K on LP corners: SCIP global solve of
   min w^T lam  s.t.  lam >= 0,  q(sbar + P lam) <= 0
compared with zk_vec (this stream) and core.corner_bound (sfree note, with a check whether
its minimizer is feasible).  Corners: all violated terms at the root LP vertex and at the
vertices after 1-3 rounds of SCIP-rule cuts (to include cut rows in the basis).
Usage: python3 check_zk_scip.py SEED NINST_PER_SIZE"""
import sys
import numpy as np
import pyscipopt as ps
import mrcore as M
from core import corner_bound, bilinear_quadratic

seed, NI = int(sys.argv[1]), int(sys.argv[2])


def scip_zk(side, sbar, P, w, ub):
    Q, b, c = bilinear_quadratic(side)
    m = ps.Model(); m.hideOutput(); m.setParam('limits/time', 60)
    m.setParam('numerics/feastol', 1e-9)
    N = P.shape[1]
    lam = [m.addVar(lb=0, ub=(1.5 * ub / w[j] if np.isfinite(ub) else 1e4)) for j in range(N)]
    s = [sbar[k] + ps.quicksum(P[k, j] * lam[j] for j in range(N)) for k in range(3)]
    # q = s^T Q s + b^T s  (bilinear: +-(w - x y))
    m.addCons(Q[0, 1] * 2 * s[0] * s[1] + b[2] * s[2] <= 0)
    m.setObjective(ps.quicksum(w[j] * lam[j] for j in range(N)))
    m.optimize()
    if m.getStatus() == 'infeasible':
        return np.inf
    if m.getStatus() != 'optimal':
        return np.nan
    return m.getObjVal()


rows = []
for k, size in enumerate([(4, 4, 3), (6, 8, 4), (8, 12, 5), (10, 20, 6)]):
    M.E.rng = np.random.default_rng(seed + k)
    for inst in range(NI):
        I = M.E.make_instance(*size)
        cuts_r, cuts_b = [], []
        for rnd in range(3):
            out = M.E.solve_lp(I, cuts_r, cuts_b)
            if out is None:
                break
            bc = M.E.basis_cone(I, *out)
            if bc is None:
                break
            x, R, w, Ab, rhs, _ = bc
            wp = M.floor_pos(w)
            newc = []
            for e, (i, j) in enumerate(I['pairs']):
                idx = [i, j, I['p'] + e]; sbar = x[idx]
                if abs(sbar[2] - sbar[0] * sbar[1]) < 1e-6:
                    continue
                side = '+' if sbar[2] > sbar[0] * sbar[1] else '-'
                P = R[idx, :]
                Q, b, c = bilinear_quadratic(side)
                g0 = float(sbar @ Q @ sbar + b @ sbar + c)
                zr, lr = corner_bound(Q, b, c, sbar, P, wp, return_point=True)
                ref_feas = lr is None or (lambda s_: s_ @ Q @ s_ + b @ s_ + c)(sbar + P @ lr) <= 1e-7 * g0
                zv = M.zk_vec(side, sbar, P, wp)
                zs = scip_zk(side, sbar, P, wp, max(zv, zr) if np.isfinite(max(zv, zr)) else np.inf)
                rel = lambda a: 0.0 if (np.isinf(a) and np.isinf(zs)) else abs(a - zs) / max(abs(zs), 1e-12)
                rows.append((size, inst, rnd, e, zs, zv, zr, ref_feas, rel(zv), rel(zr)))
                print('size %s inst %d round %d term %d  scip %.8g  vec %.8g  ref %.8g (ref point feasible: %s)'
                      % (size, inst, rnd, e, zs, zv, zr, ref_feas), flush=True)
                a = M.inv(M.scip_alpha(side, sbar, P))
                if np.any(a > 0):
                    row = a @ Ab; rr = a @ rhs - 1.0; sc = np.abs(row).max()
                    newc.append((row / sc, rr / sc))
            if not newc:
                break
            for r_, b_ in newc:
                cuts_r.append(r_); cuts_b.append(b_)

ok = [r for r in rows if np.isfinite(r[4]) or np.isinf(r[4])]
ok = [r for r in ok if not np.isnan(r[4])]
tolv = 1e-4
print('SUMMARY corners %d (SCIP solved %d)' % (len(rows), len(ok)))
print('  zk_vec : |rel diff| > %g in %d, max %.3e' % (tolv, sum(r[8] > tolv for r in ok), max(r[8] for r in ok)))
print('  core   : |rel diff| > %g in %d (below SCIP: %d, its minimizer infeasible: %d)' % (
    tolv, sum(r[9] > tolv for r in ok), sum(r[9] > tolv and r[6] < r[4] for r in ok), sum(not r[7] for r in ok)))
print('  zk_vec pair candidates rejected as infeasible: %d' % M.ZK_REJECT[0])
