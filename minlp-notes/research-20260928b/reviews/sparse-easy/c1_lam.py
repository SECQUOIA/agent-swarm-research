"""Does the EXACT C1 threshold depend on lam through log(p lam/n) (Theorem 3.2) rather than log p?
Fixed n = 400, p in {1000, 8000}, k = 10, b = 1; lam in {20 (= sqrt n), 45, 100}; the noise level sigma is set so that
tau_lam^2 is a uniform draw in [1.5, 13].  C1 at S* is decided exactly with the column-generation verifier
(verify_cg.py logic), plus the PWE root certificate and the saturated witness.
usage: python3 c1_lam.py OUT nproc"""
import os, sys, json, time
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"):
    os.environ[v] = "1"
import numpy as np
import verify_cg as V
from common import ridge_on, saturated_witness


def make(n, p, k, lam, tau2, seed, b=1.0):
    bl = b * n / (n + lam)
    sig2 = ((lam * bl) ** 2 / tau2 - k * bl ** 2 * lam ** 2 / n) / n
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, p))
    S = np.sort(rng.choice(p, k, replace=False))
    beta = np.zeros(p); beta[S] = b * rng.choice([-1.0, 1.0], k)
    y = X @ beta + np.sqrt(sig2) * rng.standard_normal(n)
    return X, y, S


def job(args):
    n, p, k, lam, tau2, seed = args
    t0 = time.time()
    X, y, S = make(n, p, k, lam, tau2, seed)
    V.author_instance = lambda *a, **kw: (X, y, float(lam), S)   # feed this instance to the verifier
    out = V.decide(n, p, k, 'custom', seed)
    fS, bS, r = ridge_on(X, y, lam, S)
    a = X.T @ r; nulls = np.setdiff1d(np.arange(p), S); m0 = np.min(np.abs(a[S]))
    wit = False
    for th in np.linspace(0.5, 1.0, 26):
        al, Gam, Vv, _ = saturated_witness(X, y, lam, S, th * m0)
        if len(Vv) > n - k - 1: continue
        c = X.T @ al; m = np.min(np.abs(c[S])); M = np.max(np.abs(c[nulls]))
        if M <= m and (m * m - M * M) / lam > Gam: wit = True; break
    out.update(lam=lam, tau2_lam=tau2, wit=wit, time=time.time() - t0)
    return out


if __name__ == '__main__':
    from multiprocessing import Pool
    OUT, nproc = sys.argv[1], int(sys.argv[2])
    n, k = 400, 10
    rng = np.random.default_rng(2026)
    jobs = []
    for p in (1000, 8000):
        for lam in (20.0, 45.0, 100.0):
            for s in range(70):
                jobs.append((n, p, k, lam, float(rng.uniform(1.5, 13.0)), 77000 + s + int(lam) * 1000 + p))
    with Pool(nproc) as pool, open(OUT, 'w') as f:
        for res in pool.imap_unordered(job, jobs):
            f.write(json.dumps(res) + '\n'); f.flush()
