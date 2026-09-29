"""Exact OPT for k = 3 by vectorized enumeration of all triples (k = 3, p <= 2600), and, otherwise, the
perspective C1 status at S* (C1 at S* certifies that S* is the unique optimum).
usage: [PMAX=..] [APPEND=1] opt_check.py mech FILE OUT nproc   |   opt_check.py cmp FILE OUT nproc
(PMAX skips rows with larger p; APPEND=1 appends and skips rows already in OUT)"""
import os, sys, json, itertools
for v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    os.environ[v] = "1"
import numpy as np
from multiprocessing import Pool
from relax import ridge, instance


def opt3(X, y, lam):
    """min over |T| = 3 of y'y - c_T'(G_T + lam I)^{-1} c_T (exact enumeration)."""
    G = X.T @ X; c = X.T @ y; p = X.shape[1]; yy = float(y @ y)
    best, bestT = np.inf, None
    for i in range(p - 2):
        J, L = np.triu_indices(p - i - 1, 1); J = J + i + 1; L = L + i + 1
        a11 = G[i, i] + lam; a22 = G[J, J] + lam; a33 = G[L, L] + lam
        a12 = G[i, J]; a13 = G[i, L]; a23 = G[J, L]
        b1 = c[i]; b2 = c[J]; b3 = c[L]
        # adjugate of symmetric 3x3
        m11 = a22 * a33 - a23 ** 2; m12 = a13 * a23 - a12 * a33; m13 = a12 * a23 - a13 * a22
        m22 = a11 * a33 - a13 ** 2; m23 = a12 * a13 - a11 * a23; m33 = a11 * a22 - a12 ** 2
        det = a11 * m11 + a12 * m12 + a13 * m13
        quad = (b1 * b1 * m11 + b2 * b2 * m22 + b3 * b3 * m33 + 2 * (b1 * b2 * m12 + b1 * b3 * m13 + b2 * b3 * m23)) / det
        t = int(np.argmax(quad))
        v = yy - quad[t]
        if v < best:
            best, bestT = v, (i, int(J[t]), int(L[t]))
    return float(best), bestT


def job(args):
    kind, r = args
    if kind == 'mech':
        from exp_mech import make
        X, y, lam, S = make(r['n'], r['k'], 2560 if r['n'] == 20 else 3200, r['p'], r['seed'])   # pmax of the series
    else:
        X, y, lam, S = instance(r['n'], r['p'], r['k'], seed=r['seed'], tau0=1.5)
    out = dict(p=r['p'], seed=r['seed'], n=r['n'], alpha=r.get('alpha'))
    fS = ridge(X, y, lam, S)[0]
    if r['k'] == 3 and r['p'] <= 2600:
        opt, T = opt3(X, y, lam)
        # refine with the exact ridge value
        opt = min(opt, ridge(X, y, lam, T)[0])
        out.update(OPT=opt, OPT_support=T, Sstar_opt=bool(fS <= opt * (1 + 1e-9)), how='enum')
    else:
        from exp_cmp import failing_nodes
        fails, status, solved = failing_nodes(X, y, lam, r['k'], S, max_solves=3000)
        c1 = (status == 'complete' and not fails)
        out.update(c1_persp=c1, Sstar_opt=True if c1 else None, how='C1', n_fail=len(fails), c1_status=status)
    return out


if __name__ == '__main__':
    kind, fn, OUT, nproc = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    rows = [json.loads(l) for l in open(fn)]
    pmax = int(os.environ.get('PMAX', '100000'))
    done = set()
    if os.path.exists(OUT) and os.environ.get('APPEND'):
        done = {(json.loads(l)['p'], json.loads(l)['seed']) for l in open(OUT)}
    rows = [r for r in rows if r['p'] <= pmax and (r['p'], r['seed']) not in done]
    with Pool(nproc) as pool, open(OUT, 'a' if os.environ.get('APPEND') else 'w') as f:
        for res in pool.imap_unordered(job, [(kind, r) for r in rows]):
            f.write(json.dumps(res) + '\n'); f.flush(); print(res, flush=True)
