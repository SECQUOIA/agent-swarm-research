"""Root exactness and C1 under stronger relaxations, on the note's instance family
(b = 1, sigma = 0.5, lam = 1.5 sigma sqrt(2 n log p)/b, n = round(alpha k log p); generator core.instance).

Per instance:
  root: f(S*), perspective root (certified dual bound), PWE ratio max|a_l|/m0;
        exact root values of sdp1 / sdp2 / zb where affordable (see limits);
        certified upper bounds on the L_1 and L_2 root values (cbound.best_small_F_bound).
  C1:   all failing single-fixing nodes of the perspective relaxation (exact: dual pool + column
        generation; a node fails if a feasible point has value < f(S*)(1 - 1e-7));
        for the (up to NF weakest) failing nodes: certified L_1 / L_2 upper bounds at that node, and
        for the NF2 weakest: exact sdp1 (Clarabel p <= P1, SCS p <= P1S) and sdp2 (p <= P2) node values.
  A relaxation R satisfies C1 iff all single-fixing R-bounds are >= f(S*); nodes where the perspective
  passes also pass for R (R >= perspective).
usage: exp_cmp.py OUT p k alphas seeds nproc [P1 P1S P2 PZB NF NF2]
"""
import os, sys, json, time
for v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    os.environ[v] = "1"
import numpy as np
from multiprocessing import Pool
from relax import instance, ridge, sdp1, sdp2, zb, persp
from cbound import best_small_F_bound, delta_opt_persp
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "code"))
from core import solve_node_cg, saturated_witness, all_single_bounds

TOLF, TOLP = 1e-7, 1e-9


def failing_nodes(X, y, lam, k, S, max_solves=4000):
    """All single-fixing perspective nodes with a feasible value < f(S)(1-TOLF).
    Returns (fails: list of (S0, S1, value)), status ('complete' or 'capped'), number of solves."""
    n, p = X.shape
    S = np.array(sorted(S)); Ss = set(S.tolist())
    nulls = np.array([j for j in range(p) if j not in Ss])
    fS, bS, r = ridge(X, y, lam, list(S))
    m0 = lam * np.abs(bS).min()
    rem = np.full(len(S), -np.inf); frc = np.full(len(nulls), -np.inf)
    done = np.zeros(len(S) + len(nulls), bool)

    def absorb(a):
        rr, ff = all_single_bounds(X, y, lam, k, a, S, nulls)
        np.maximum(rem, rr, out=rem); np.maximum(frc, ff, out=frc)
    absorb(r)
    for th in np.linspace(0.5, 1.0, 11):
        al, info = saturated_witness(X, y, lam, list(S), th * m0)
        if info['nV'] <= n - k - 1:
            absorb(al)
    LBr, vr, zr, ar, _ = solve_node_cg(X, y, lam, k, init=tuple(S), maxrounds=200, add=40)
    absorb(ar)
    init = tuple(S) + tuple(np.nonzero(zr > 1e-6)[0])
    fails, solved, status = [], 0, 'complete'
    while True:
        allb = np.concatenate([rem, frc]); allb[done] = np.inf
        idx = int(np.argmin(allb))
        if allb[idx] >= fS * (1 + TOLP):
            break
        if solved >= max_solves:
            status = 'capped'; break
        node = ((int(S[idx]),), ()) if idx < len(S) else ((), (int(nulls[idx - len(S)]),))
        LB, val, z, a, rounds = solve_node_cg(X, y, lam, k, node[0], node[1], init=init,
                                              target=fS * (1 + TOLP), maxrounds=200, add=40)
        solved += 1; done[idx] = True
        absorb(a)
        if val < fS * (1 - TOLF):
            fails.append((node[0], node[1], float(val)))
        elif LB < fS * (1 + TOLP) and val - LB > 1e-8 * max(1.0, abs(val)):
            status = 'undecided-node'
    fails.sort(key=lambda t: t[2])
    return fails, status, solved


def job(args):
    p, k, alpha, seed, lim = args
    P1, P1S, P2, PZB, NF, NF2 = lim
    n = max(k + 2, int(round(alpha * k * np.log(p))))
    X, y, lam, S = instance(n, p, k, seed=seed, tau0=1.5)
    t0 = time.time()
    fS, bS, r = ridge(X, y, lam, S)
    a = np.abs(X.T @ r); a[list(S)] = -1.0
    m0 = lam * np.abs(bS).min()
    cand = [int(j) for j in np.argsort(-a)[:20]]
    delta = delta_opt_persp(X, lam)
    out = dict(p=p, k=k, n=n, alpha=alpha, seed=seed, lam=lam, fS=fS, P=persp(X, y, lam, k)[0],
               maxratio=float(a.max() / m0), nviol=int((a > m0).sum()), delta=delta)
    L1ub, L2ub, info = best_small_F_bound(X, y, lam, k, S, cand, hs=(1, 2, 3, 5, 8, 12, 20), delta=delta)
    out.update(L1_ub=L1ub, L2_ub=L2ub, ub_info=info)
    if p <= P1: out['sdp1'] = sdp1(X, y, lam, k)
    elif p <= P1S: out['sdp1'] = sdp1(X, y, lam, k, solver='SCS')
    if p <= P2: out['sdp2'] = sdp2(X, y, lam, k)
    if p <= PZB: out['zb'] = zb(X, y, lam, k, solver='SCS')
    fails, status, solved = failing_nodes(X, y, lam, k, S)
    out.update(c1_status=status, c1_solves=solved, n_fail=len(fails), fails=fails[:50])
    nodes = []
    for (S0, S1, val) in fails[:NF]:
        c = [int(j) for j in np.argsort(-a)[:21] if j not in S1][:20]
        b1, b2, inf2 = best_small_F_bound(X, y, lam, k, S, c, hs=(1, 2, 3, 5, 8, 12, 20), S0=S0, S1=S1, delta=delta)
        d = dict(S0=S0, S1=S1, persp=val, L1_ub=b1, L2_ub=b2)
        if len(nodes) < NF2:
            if p <= P1: d['sdp1'] = sdp1(X, y, lam, k, S0, S1)
            elif p <= P1S: d['sdp1'] = sdp1(X, y, lam, k, S0, S1, solver='SCS')
            if p <= P2: d['sdp2'] = sdp2(X, y, lam, k, S0, S1)
        nodes.append(d)
    out['fail_nodes'] = nodes
    out['time'] = time.time() - t0
    return out


if __name__ == '__main__':
    OUT, p, k = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    alphas = [float(v) for v in sys.argv[4].split(',')]; seeds = int(sys.argv[5]); nproc = int(sys.argv[6])
    lim = [int(v) for v in sys.argv[7:13]] if len(sys.argv) > 7 else [100, 400, 100, 100, 30, 3]
    jobs = [(p, k, al, 1000 + s, lim) for al in alphas for s in range(seeds)]
    with Pool(nproc) as pool, open(OUT, 'a') as f:
        for res in pool.imap_unordered(job, jobs):
            f.write(json.dumps(res, default=float) + '\n'); f.flush()
            print(res['p'], res['alpha'], res['seed'], '%.1fs' % res['time'], flush=True)
