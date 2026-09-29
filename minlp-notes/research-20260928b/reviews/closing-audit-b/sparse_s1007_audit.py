"""Closing audit (b), item 1: forced-in node values at p = 3200, seed 1007 (and 1000), lam = sqrt n,
k = 5, alpha = 3 (n = 121), b = 1, sigma = 0.5, of phase-transition.md Section 6.3.

Own code.  The instance generator mirrors the note's documented generator (core.instance):
rng = default_rng(seed); X = N(0,1)^{n x p}; S = sorted rng.choice(p, k, replace=False);
beta_S = b * rng.choice([-1, 1], k); y = X beta + sigma * N(0, I_n).

Node value r(emptyset, {j}) = min { g(z) : z_j = 1, 0 <= z <= 1, sum_{i != j} z_i <= k - 1 },
g(z) = y'(I + X diag(z) X'/lam)^{-1} y, solved by accelerated projected gradient (FISTA with
backtracking and adaptive restart) on the FULL z in R^p -- no column generation, no conic solver.
Certification: primal value g(z) at a feasible z (upper bound), and the Lemma 1.1 dual bound
L(a) = 2a'y - |a|^2 - (1/lam)[c_j^2 + top_{k-1}{c_i^2 : i != j}], c = X'a, at a = M_z^{-1} y
(lower bound, valid for any a).  The bracket [L, g] decides the sign of r - f(S*).
Usage: python3 sparse_s1007_audit.py SEED J [J ...]
"""
import os, sys, time, json
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"):
    os.environ[v] = "1"
import numpy as np

n, p, k, b, sigma = 121, 3200, 5, 1.0, 0.5


def instance(seed):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, p))
    S = np.sort(rng.choice(p, k, replace=False))
    beta = np.zeros(p)
    beta[S] = b * rng.choice([-1.0, 1.0], k)
    y = X @ beta + sigma * rng.standard_normal(n)
    return X, y, np.sqrt(n), S


def proj_capped(v, K):
    """Euclidean projection onto {0 <= u <= 1, sum u <= K}."""
    u = np.clip(v, 0.0, 1.0)
    if u.sum() <= K:
        return u
    lo, hi = 0.0, float(v.max())
    for _ in range(200):
        th = 0.5 * (lo + hi)
        if np.clip(v - th, 0.0, 1.0).sum() > K:
            lo = th
        else:
            hi = th
    return np.clip(v - hi, 0.0, 1.0)


def g_and_a(X, y, lam, z):
    idx = np.nonzero(z > 0)[0]
    Xs = X[:, idx] * np.sqrt(z[idx])
    M = np.eye(len(y)) + Xs @ Xs.T / lam
    a = np.linalg.solve(M, y)
    return float(y @ a), a


def dual_bound(X, y, lam, a, j, kk):
    c2 = (X.T @ a) ** 2
    cj = c2[j]
    c2[j] = -1.0
    top = np.sort(c2)[::-1][:kk - 1].sum()
    return float(2 * a @ y - a @ a - (cj + top) / lam)


def solve_forced_in(X, y, lam, j, S, iters=20000, tol=1e-7, log_every=500):
    kk = k
    others = np.ones(p, bool); others[j] = False
    z = np.zeros(p); z[S] = (kk - 1) / kk; z[j] = 1.0
    zprev = z.copy(); t = 1.0; Lc = 1.0
    best = (np.inf, None, None); lbbest = -np.inf
    gz, az = g_and_a(X, y, lam, z)
    for it in range(1, iters + 1):
        # extrapolated point
        w = z + ((t - 1) / (t + 1)) * (z - zprev) if it > 1 else z.copy()
        w[j] = 1.0
        gw, aw = g_and_a(X, y, lam, w)
        grad = -((X.T @ aw) ** 2) / lam
        while True:
            znew = w - grad / Lc
            zz = proj_capped(znew[others], kk - 1)
            znew = np.empty(p); znew[others] = zz; znew[j] = 1.0
            gn, an = g_and_a(X, y, lam, znew)
            d = znew - w
            if gn <= gw + grad @ d + 0.5 * Lc * (d @ d) + 1e-12:
                break
            Lc *= 2.0
        if gn > gz:          # adaptive restart
            t = 1.0; zprev = z.copy()
        else:
            zprev, z, gz, az = z, znew, gn, an
            t = 0.5 * (1 + np.sqrt(1 + 4 * t * t))
        Lc *= 0.9
        if gz < best[0]:
            best = (gz, z.copy(), az.copy())
        if it % log_every == 0 or it == iters:
            lb = dual_bound(X, y, lam, best[2], j, kk)
            lbbest = max(lbbest, lb)
            if best[0] - lbbest <= tol * max(1.0, abs(best[0])):
                break
    return best[0], lbbest, best[1], it


if __name__ == "__main__":
    seed = int(sys.argv[1]); js = [int(v) for v in sys.argv[2:]]
    X, y, lam, S = instance(seed)
    XS = X[:, S]
    bS = np.linalg.solve(XS.T @ XS + lam * np.eye(k), XS.T @ y)
    r = y - XS @ bS
    fS = float(y @ r)
    a = X.T @ r
    m0 = float(np.min(np.abs(a[S])))
    nul = np.array([i for i in range(p) if i not in set(S)])
    order = nul[np.argsort(-np.abs(a[nul]))]
    rank = {int(jj): int(i + 1) for i, jj in enumerate(order)}
    nviol = int(np.sum(np.abs(a[nul]) > m0))
    satgain = float(np.sum(np.maximum(np.abs(a[nul]) - m0, 0) ** 2) / n)
    info = dict(seed=seed, S=S.tolist(), fS=fS, lam=lam, price=m0 ** 2 / lam, tau2=(m0 / np.linalg.norm(r)) ** 2,
                violators=nviol, satgain=satgain)
    print(json.dumps(info), flush=True)
    for jj in js:
        t0 = time.time()
        up, lo, z, its = solve_forced_in(X, y, lam, jj, S)
        print(json.dumps(dict(seed=seed, j=jj, rank=rank.get(jj), zj=float(abs(a[jj]) / np.linalg.norm(r)),
                              ownfit=float(a[jj] ** 2 / (n + lam)), upper_minus_f=up - fS, lower_minus_f=lo - fS,
                              gap=up - lo, iters=its, nnz=int(np.sum(z > 1e-9)), secs=round(time.time() - t0, 1))),
              flush=True)
