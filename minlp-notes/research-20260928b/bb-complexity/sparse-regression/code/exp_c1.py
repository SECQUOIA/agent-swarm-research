"""C1 / root-exactness / witness experiment for perspective B&B in sparse ridge regression.
usage: python3 exp_c1.py OUT p k LAMRULE alphas seeds nproc [b sigma]
LAMRULE: 'sqrtn' (lam = sqrt n) or a number tau0 (lam = tau0*sigma*sqrt(2 n log p)/b).
For each instance records: root gap at S*, PWE root certificate at S*, best saturated-witness
margin (certificate for C1), and an exact C1 decision at S* (node relaxations solved by Clarabel,
ordered by witness bound, early stop at the first node whose certified bound < f(S*))."""
import os, sys, json, time
os.environ["OMP_NUM_THREADS"] = "1"; os.environ["OPENBLAS_NUM_THREADS"] = "1"; os.environ["RAYON_NUM_THREADS"] = "1"; os.environ["MKL_NUM_THREADS"] = "1"
import numpy as np
from multiprocessing import Pool
from core import instance, ridge, solve_node, solve_node_cg, best_saturated, saturated_witness, single_fixing_bounds
MAXEX = int(os.environ.get('MAXEX', '300'))

def job(args):
    n, p, k, rule, seed, b, sigma = args
    t0 = time.time()
    if rule == 'sqrtn':
        X, y, lam, S = instance(n, p, k, b=b, sigma=sigma, seed=seed)
    else:
        X, y, lam, S = instance(n, p, k, b=b, sigma=sigma, seed=seed, tau0=float(rule))
    fS, bS, r = ridge(X, y, lam, S)
    a = np.abs(X.T @ r); Ss = set(S)
    nulls = np.array([j for j in range(p) if j not in Ss])
    m0 = lam * np.abs(bS).min()
    pwe = bool(a[nulls].max() <= m0)
    if p > 800:
        LBr, vr, zr, ar, _ = solve_node_cg(X, y, lam, k, init=tuple(S))
    else:
        LBr, vr, zr, ar = solve_node(X, y, lam, k)
    marg, th, info = best_saturated(X, y, lam, k, S)
    out = dict(n=n, p=p, k=k, rule=rule, seed=seed, lam=lam, fS=fS, gap=fS - LBr, pwe=pwe,
               tau=m0 / np.linalg.norm(r), nviol=int((a[nulls] > m0).sum()),
               wit_margin=marg, wit_th=th, wit=bool(marg > 0))
    if marg > 0:
        out.update(c1=True, c1_how='witness', n_exact=0)
    else:
        alpha, _ = saturated_witness(X, y, lam, S, th * m0)
        rem, frc = single_fixing_bounds(X, y, lam, k, S, alpha)
        nodes = [((S[t],), (), rem[t]) for t in range(k)] + [((), (int(nulls[t]),), frc[t]) for t in range(len(nulls))]
        nodes.sort(key=lambda z: z[2])
        c1 = True; cnt = 0; fail = None; minm = np.inf
        for S0, S1, wb in nodes:
            if wb >= fS * (1 + 1e-9):
                continue  # already certified by the witness
            if p > 800:
                LB, val, z, aa, _ = solve_node_cg(X, y, lam, k, S0, S1, init=tuple(S) + tuple(np.nonzero(zr > 1e-6)[0]))
            else:
                LB, val, z, aa = solve_node(X, y, lam, k, S0, S1)
            cnt += 1
            if cnt > MAXEX:
                c1 = 'capped'; break
            minm = min(minm, LB - fS)
            if val < fS * (1 - 1e-7):  # primal value below f(S*): node not prunable (certainly)
                c1 = False; fail = 'rem' if S0 else 'frc'; break
            if LB < fS * (1 - 1e-7):
                c1 = None  # undecided numerically (should not happen with IPM)
        out.update(c1=c1, c1_how='exact', n_exact=cnt, fail=fail)
    out['time'] = time.time() - t0
    return out

if __name__ == '__main__':
    OUT, p, k, rule = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    alphas = [float(v) for v in sys.argv[5].split(',')]; seeds = int(sys.argv[6]); nproc = int(sys.argv[7])
    b = float(sys.argv[8]) if len(sys.argv) > 8 else 1.0
    sigma = float(sys.argv[9]) if len(sys.argv) > 9 else 0.5
    jobs = []
    for a in alphas:
        n = max(k + 2, int(round(a * k * np.log(p))))
        for s in range(seeds):
            jobs.append((n, p, k, rule, 1000 + s, b, sigma))
    with Pool(nproc) as pool, open(OUT, 'a') as f:
        for res in pool.imap_unordered(job, jobs):
            res['alpha'] = res['n'] / (res['k'] * np.log(res['p']))
            f.write(json.dumps(res) + '\n'); f.flush()
