"""Prototype separator: root cutting loop on McCormick LPs of random bilinear programs.

Each round: solve the LP (HiGHS), take the optimal basis cone, and for every bilinear term
violated by more than 1e-6 add one intersection cut chosen by RULE:
  scip   : Chmiela-Munoz-Serrano Case-4 maximal set (SCIP's construction, default lambda)
  orbit  : best sliced-orbit set C_F for the corner bound (LMI bisection)
  orbitB : the maximal completion C_F^G = cl(C_F -/+ R_+ e_w) of that same F
  corner : the corner-optimal cut w^T lam >= z_K (objective-parallel)
Reports the fraction of the root gap (z_bil - z_LP) closed after each round, where z_bil is
the optimum of the bilinear program (SCIP), and cut nonzeros.
Usage: python3 exp_loop.py SEED NINST ROUNDS OUT.json [p npairs nlin]
"""
import sys, json, time, warnings
import numpy as np
warnings.filterwarnings('ignore')
import pyscipopt as ps
import exp_mccormick as E          # reuse generator / LP helpers (module has no side effects on import? see guard)
from core import corner_bound, qval, best_orbit_bound, bilinear_quadratic
from bilinear import step_A, step_B
from scout_sfree import ms_set, ic_bound

seed = int(sys.argv[1]); NI = int(sys.argv[2]); ROUNDS = int(sys.argv[3]); OUT = sys.argv[4]
p_, npairs_, nlin_ = (int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])) if len(sys.argv) > 7 else (4, 4, 3)
E.rng = np.random.default_rng(seed)


def bilinear_opt(I, timelimit=60):
    m = ps.Model(); m.hideOutput(); m.setParam('limits/time', timelimit)
    n = I['n']; xs = [m.addVar(lb=I['lo'][v], ub=I['hi'][v]) for v in range(n)]
    for k_ in range(len(I['b'])):
        m.addCons(ps.quicksum(I['A'][k_, v] * xs[v] for v in range(n)) <= I['b'][k_])
    for e, (i, j) in enumerate(I['pairs']):
        m.addCons(xs[I['p'] + e] == xs[i] * xs[j])
    m.setObjective(ps.quicksum(I['c'][v] * xs[v] for v in range(n)))
    m.optimize()
    return m.getDualbound(), m.getStatus()


def cut_for(rule, side, sbar, P, w):
    Q, bq, cq = bilinear_quadratic(side)
    wpos = np.maximum(w, 1e-9 * max(1.0, w.max()))
    if rule == 'scip':
        G, cs = ms_set(Q, bq, cq, sbar)
        al = ic_bound(G, sbar, P, w)[1]
    elif rule in ('orbit', 'orbitB'):
        zk = corner_bound(Q, bq, cq, sbar, P, wpos)
        _, _, F = best_orbit_bound(side, sbar, P, wpos, min(zk, 1e6), iters=25)
        if F is None:
            return None
        st = step_A if rule == 'orbit' else step_B
        al = np.array([st(F, side, sbar, P[:, j]) for j in range(P.shape[1])])
    elif rule == 'corner':
        zk = corner_bound(Q, bq, cq, sbar, P, wpos)
        if not np.isfinite(zk) or zk <= 0:
            return None
        return wpos / zk
    return np.array([0.0 if not np.isfinite(t) else 1.0 / t for t in al])


LPFAIL = {}


def run(I, rule, rounds, zbil):
    rows, rhs = [], []
    hist = []; nnz = []
    for r in range(rounds + 1):
        out = E.solve_lp(I, rows, rhs)
        if out is None:
            LPFAIL[rule] = LPFAIL.get(rule, 0) + 1
            break
        h, A, bb = out
        bc = E.basis_cone(I, h, A, bb)
        z = h.getInfo().objective_function_value
        hist.append(z)
        if r == rounds or bc is None:
            break
        x, R, w, Ab, rhsB, _ = bc
        added = 0
        for e, (i, j) in enumerate(I['pairs']):
            idx = [i, j, I['p'] + e]
            sbar = x[idx]
            if abs(sbar[2] - sbar[0] * sbar[1]) < 1e-6:
                continue
            side = '+' if sbar[2] > sbar[0] * sbar[1] else '-'
            a = cut_for(rule, side, sbar, R[idx, :], w)
            if a is None or not np.all(np.isfinite(a)) or not np.any(a > 0):
                continue
            row = a @ Ab; rr = a @ rhsB - 1.0          # row x <= rr
            sc = np.abs(row).max()
            if sc < 1e-12:
                continue
            rows.append(row / sc); rhs.append(rr / sc); added += 1
            nnz.append(int(np.sum(np.abs(row / sc) > 1e-9)))
        if added == 0:
            hist += [z] * (rounds - r)
            break
    return hist, nnz


if __name__ == '__main__':
    res = []
    t0 = time.time()
    for k in range(NI):
        I = E.make_instance(p_, npairs_, nlin_)
        out = E.solve_lp(I)
        if out is None:
            continue
        zlp = out[0].getInfo().objective_function_value
        zbil, st = bilinear_opt(I)
        if st != 'optimal' or zbil - zlp < 1e-6:
            continue
        rec = dict(inst=k, zlp=zlp, zbil=zbil)
        for rule in ('scip', 'orbit', 'orbitB', 'corner'):
            hist, nnz = run(I, rule, ROUNDS, zbil)
            hist = hist + [hist[-1]] * (ROUNDS + 1 - len(hist))
            rec[rule] = [float(min(max((z - zlp) / (zbil - zlp), 0), 1.0 + 1e-9)) for z in hist]
            rec[rule + '_nnz'] = float(np.mean(nnz)) if nnz else 0.0
            rec[rule + '_ncuts'] = len(nnz)
        res.append(rec)
        print(json.dumps({k_: (v if not isinstance(v, list) else [round(t, 3) for t in v[:1] + v[1:2] + v[3:4] + v[-1:]]) for k_, v in rec.items()}), flush=True)
    summ = dict(n=len(res), seconds=time.time() - t0, lp_failures=LPFAIL)
    for rule in ('scip', 'orbit', 'orbitB', 'corner'):
        H = np.array([r[rule] for r in res])
        summ[rule] = dict(mean_closed_by_round=[float(v) for v in H.mean(0)], median_round1=float(np.median(H[:, 1])),
                          median_final=float(np.median(H[:, -1])), mean_nnz=float(np.mean([r[rule + '_nnz'] for r in res])),
                          mean_ncuts=float(np.mean([r[rule + '_ncuts'] for r in res])))
    print('SUMMARY', json.dumps(summ))
    json.dump(dict(summary=summ, records=res), open(OUT, 'w'), indent=1)
