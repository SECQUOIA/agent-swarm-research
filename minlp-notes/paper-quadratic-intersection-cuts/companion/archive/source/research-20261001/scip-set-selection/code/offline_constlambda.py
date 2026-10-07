"""Offline check: how much does a free direction lambda in SCIP's own (constant-lambda)
family gain on the McCormick corners of the sfree note (Section 9.2)?

For each LP corner of the generator of research-20260928b/sfree/code/exp_mccormick.py
(same seeds and sizes), compare one intersection cut from
  scip   : Chmiela-Munoz-Serrano Case-4 set with SCIP's lambda = xhat(sbar)/|xhat(sbar)|,
  lamK   : the same family with lambda (a point of the unit circle) chosen to maximize the
           single-cut corner bound min_j w_j alpha_j  (grid of 2000 angles + golden refinement),
  lamE   : the same family with lambda chosen to maximize the Euclidean efficacy of the cut
           in the structural space (1/||Ab^T a||),
  orbit  : best set of the sliced orbit family (A) (LMI bisection, from the note),
and the corner bound z_K.  Reported: corner increments and LP re-solve gains as fractions of
the single-constraint gap, as in the note.

Usage: python3 offline_constlambda.py SEED NTRIALS OUT.json [p npairs nlin]
"""
import sys, os, json, warnings
import numpy as np
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
SFREE = os.path.join(HERE, '..', '..', '..', 'research-20260928b', 'sfree', 'code')
sys.path.insert(0, SFREE)
import exp_mccormick as em                      # noqa: E402
from core import corner_bound, qval, best_orbit_bound, bilinear_quadratic   # noqa: E402
from scout_sfree import ms_set, ic_bound       # noqa: E402
from bilinear import step_A                    # noqa: E402


def lam_family_eval(Q, b, c, sbar, P, w, Ab, theta):
    lam = np.array([np.cos(theta), np.sin(theta)])
    G, _ = ms_set(Q, b, c, sbar, lam=lam)
    if not G(sbar) < -1e-12:
        return None
    z, al = ic_bound(G, sbar, P, w)
    a = np.array([0.0 if not np.isfinite(t) else 1.0 / t for t in al])
    eff = 1.0 / max(np.linalg.norm(Ab.T @ a), 1e-300)
    return z, eff, a


def best_theta(Q, b, c, sbar, P, w, Ab, crit, ngrid=400):
    ths = np.linspace(-np.pi, np.pi, ngrid, endpoint=False)
    vals = []
    for t in ths:
        r = lam_family_eval(Q, b, c, sbar, P, w, Ab, t)
        vals.append(-np.inf if r is None else (r[0] if crit == 'K' else r[1]))
    vals = np.array(vals)
    k = int(np.argmax(vals))
    lo, hi = ths[k] - 2 * np.pi / ngrid, ths[k] + 2 * np.pi / ngrid
    f = lambda t: (lambda r: -np.inf if r is None else (r[0] if crit == 'K' else r[1]))(
        lam_family_eval(Q, b, c, sbar, P, w, Ab, t))
    gr = (np.sqrt(5) - 1) / 2
    for _ in range(40):
        m1 = hi - gr * (hi - lo); m2 = lo + gr * (hi - lo)
        if f(m1) >= f(m2):
            hi = m2
        else:
            lo = m1
    tb = 0.5 * (lo + hi)
    if f(tb) < vals[k]:
        tb = ths[k]
    return tb, lam_family_eval(Q, b, c, sbar, P, w, Ab, tb)


if __name__ == '__main__':
    seed = int(sys.argv[1]); T = int(sys.argv[2]); OUT = sys.argv[3]
    SIZE = tuple(int(a) for a in sys.argv[4:7]) if len(sys.argv) > 6 else (4, 4, 3)
    em.rng = np.random.default_rng(seed)          # the generator uses the module-level rng
    res = []
    for trial in range(T):
        I = em.make_instance(*SIZE)
        out = em.solve_lp(I)
        if out is None:
            continue
        h, A, bb = out
        bc = em.basis_cone(I, h, A, bb)
        if bc is None:
            continue
        x, R, w, Ab, rhs, zlp = bc
        p = I['p']
        viol = [(abs(x[p + e] - x[i] * x[j]), e) for e, (i, j) in enumerate(I['pairs'])]
        vmax, e = max(viol)
        if vmax < 1e-4:
            continue
        i, j = I['pairs'][e]; idx = [i, j, p + e]
        sbar = x[idx]
        side = '+' if sbar[2] > sbar[0] * sbar[1] else '-'
        Q, bq, cq = bilinear_quadratic(side)
        P = R[idx, :]
        wpos = np.maximum(w, 1e-9 * max(1.0, w.max()))
        z1 = em.single_constraint_bound(I, e) - zlp
        if z1 < 1e-6:
            continue
        G, cs = ms_set(Q, bq, cq, sbar)
        zms, al_ms = ic_bound(G, sbar, P, wpos)
        a_ms = np.array([0.0 if not np.isfinite(t) else 1.0 / t for t in al_ms])
        eff_ms = 1.0 / np.linalg.norm(Ab.T @ a_ms)
        zk = corner_bound(Q, bq, cq, sbar, P, wpos)
        thK, rK = best_theta(Q, bq, cq, sbar, P, wpos, Ab, 'K')
        thE, rE = best_theta(Q, bq, cq, sbar, P, wpos, Ab, 'E')
        zorb, _, F = best_orbit_bound(side, sbar, P, wpos, min(zk, 1e6), iters=30)
        al_orb = np.array([step_A(F, side, sbar, P[:, jj]) for jj in range(P.shape[1])]) if F is not None else None
        a_orb = None if al_orb is None else np.array([0.0 if not np.isfinite(t) else 1.0 / t for t in al_orb])
        lp = lambda a: None if a is None else em.lp_with_cut(I, Ab, rhs, a)
        fr = lambda v: None if v is None else float(min(max(v, 0.0), z1) / z1)
        lpf = lambda a: (lambda v: None if v is None else fr(v - zlp))(lp(a))
        rec = dict(trial=trial, side=side, gap=z1, zK=zk,
                   scip_incr=fr(min(zms, zk)), lamK_incr=fr(min(rK[0], zk)), lamE_incr=fr(min(rE[0], zk)),
                   orbit_incr=fr(min(zorb, zk)), corner_incr=fr(zk),
                   scip_lp=lpf(a_ms), lamK_lp=lpf(rK[2]), lamE_lp=lpf(rE[2]), orbit_lp=lpf(a_orb),
                   scip_eff=float(eff_ms), lamK_eff=float(rK[1]), lamE_eff=float(rE[1]),
                   orbit_eff=None if a_orb is None else float(1.0 / np.linalg.norm(Ab.T @ a_orb)),
                   scip_over_zK=float(min(zms, zk) / zk), lamK_over_zK=float(min(rK[0], zk) / zk),
                   orbit_over_zK=float(min(zorb, zk) / zk))
        res.append(rec)
        print(json.dumps(rec), flush=True)
    keys = ['scip_incr', 'lamK_incr', 'lamE_incr', 'orbit_incr', 'corner_incr',
            'scip_lp', 'lamK_lp', 'lamE_lp', 'orbit_lp', 'scip_over_zK', 'lamK_over_zK', 'orbit_over_zK']
    summ = {'n': len(res)}
    for k in keys:
        v = np.array([r[k] for r in res if r[k] is not None], float)
        summ[k] = dict(mean=float(v.mean()), median=float(np.median(v)), min=float(v.min()), n=len(v))
    for a, b_ in [('lamK_lp', 'scip_lp'), ('lamE_lp', 'scip_lp'), ('orbit_lp', 'scip_lp'), ('lamK_lp', 'orbit_lp')]:
        d = np.array([r[a] - r[b_] for r in res if r[a] is not None and r[b_] is not None])
        summ['%s_minus_%s' % (a, b_)] = dict(mean=float(d.mean()), better=int((d > 0.01).sum()), worse=int((d < -0.01).sum()), n=len(d))
    summ['lamK_reaches_zK'] = int(sum(r['lamK_over_zK'] > 0.9999 for r in res))
    summ['scip_reaches_zK'] = int(sum(r['scip_over_zK'] > 0.9999 for r in res))
    print('SUMMARY', json.dumps(summ))
    json.dump(dict(summary=summ, records=res), open(OUT, 'w'), indent=1)
