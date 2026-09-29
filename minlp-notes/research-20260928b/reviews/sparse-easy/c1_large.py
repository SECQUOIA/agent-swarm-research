"""Scalable test of Theorems 3.1 and 3.2 (root exactness and C1 thresholds) at large p.

Exact conditional simulation: given (X_S, w), null columns are x_l = (a_l/||r||^2) r + x_l^perp with
a_l = ||r|| Z_l, Z_l iid N(0,1), x_l^perp ~ N(0, I - r r'/||r||^2) independent of a_l.  Only the M
largest |Z_l| among the p-k nulls are simulated (exact order statistics via exponential spacings);
the remaining p-k-M nulls enter only through exactly-sampled maxima.

Per instance we record
  root   : root relaxation exact at S* (Corollary 2.4; exact decision, uses only the top null),
  wit    : saturated witness (Prop. 2.3, grid of kappa/m0) certifies strict C1 (sufficient for C1),
  fail   : an upper bound on r(emptyset,{j}) (j = top null) or on r({i},emptyset) (i = weakest true
           feature), from the node relaxation restricted to S plus the top-MR nulls, is < f(S*)
           (then C1 at S* fails, or S* is not optimal).
usage: python3 c1_large.py OUT.jsonl nproc
"""
import os, sys, json, time
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"):
    os.environ[v] = "1"
import numpy as np
from scipy.stats import norm
import cvxpy as cp

N_POOL = 400     # simulated top nulls
MR = 200         # nulls used in the restricted node relaxations


def top_order_stats(N, M, rng):
    """Largest M of N iid |N(0,1)|, exactly, in decreasing order."""
    E = rng.standard_exponential(M)
    G = rng.gamma(N + 1 - M)
    U = np.cumsum(E) / (np.sum(E) + G)          # smallest M of N iid U(0,1)
    return norm.isf(U / 2)


def restricted_node(Xw, y, lam, k, fixed1=None, fixed0=None):
    m = Xw.shape[1]
    beta = cp.Variable(m); z = cp.Variable(m); t = cp.Variable(m)
    lo = np.zeros(m); hi = np.ones(m)
    if fixed1 is not None:
        lo[fixed1] = 1.0
    if fixed0 is not None:
        hi[fixed0] = 0.0
    cons = [z >= lo, z <= hi, cp.sum(z) <= k, cp.SOC(t + z, cp.vstack([2 * beta, t - z]), axis=0)]
    prob = cp.Problem(cp.Minimize(cp.sum_squares(y - Xw @ beta) + lam * cp.sum(t)), cons)
    prob.solve(solver="CLARABEL")
    return float(prob.value)


def instance(n, p, k, lam, tau2_target, seed, b=1.0):
    rng = np.random.default_rng(seed)
    bl = b * n / (n + lam)
    A = (lam * bl) ** 2
    sig2 = (A / tau2_target - k * bl ** 2 * lam ** 2 / n) / n
    if sig2 <= 0:
        return None
    sigma = np.sqrt(sig2)
    XS = rng.standard_normal((n, k)); w = rng.standard_normal(n)
    bstar = b * rng.choice([-1.0, 1.0], k)
    y = XS @ bstar + sigma * w
    G = XS.T @ XS
    bS = np.linalg.solve(G + lam * np.eye(k), XS.T @ y)
    r = y - XS @ bS; fS = float(y @ r); R = np.linalg.norm(r)
    aS = lam * bS; m0 = np.min(np.abs(aS))
    N = p - k
    Z = top_order_stats(N, N_POOL, rng) * rng.choice([-1.0, 1.0], N_POOL)
    aP = R * Z
    g = rng.standard_normal((n, N_POOL))
    g -= np.outer(r, r @ g) / R ** 2
    XP = np.outer(r, aP / R ** 2) + g                  # pool columns
    zM = abs(Z[-1])                                     # every non-pool null has |Z| <= zM
    out = dict(n=n, p=p, k=k, lam=lam, tau2_target=tau2_target, seed=seed, sigma=sigma,
               tau2_hat=(m0 / R) ** 2, zmax=abs(Z[0]), zM=zM, root=bool(abs(aP[0]) <= m0))
    # saturated witness over a grid of kappa
    Minv_apply = lambda Bm: Bm - XS @ np.linalg.solve(lam * np.eye(k) + G, XS.T @ Bm)
    best = -np.inf; best_th = None
    for th in np.linspace(0.50, 1.0, 51):
        kappa = th * m0
        V = np.nonzero(np.abs(aP) > kappa)[0]
        if len(V) >= n - k - 1:
            continue
        if len(V):
            XV = XP[:, V]; MXV = Minv_apply(XV); H = XV.T @ MXV
            rhs = aP[V] - kappa * np.sign(aP[V]); u = np.linalg.solve(H, rhs)
            Gam = float(rhs @ u); Delta = MXV @ u
        else:
            Gam = 0.0; Delta = np.zeros(n)
        alpha = r - Delta
        cS = XS.T @ alpha; cP = XP.T @ alpha
        m = np.min(np.abs(cS))
        # non-pool nulls: |c_l| <= zM R |1 - r'Delta/R^2| + max_{rest} |x_perp' Delta|
        s = np.linalg.norm(Delta - r * (r @ Delta) / R ** 2)
        Urest = rng.uniform()
        rest_noise = s * norm.isf((1 - Urest ** (1.0 / (N - N_POOL))) / 2) if s > 0 else 0.0
        Mrest = zM * R * abs(1 - (r @ Delta) / R ** 2) + rest_noise
        Mtot = max(np.max(np.abs(cP)), Mrest)
        if Mtot <= m:
            marg = (m ** 2 - Mtot ** 2) / lam - Gam
            if marg > best:
                best, best_th = marg, th
    out.update(wit=bool(best > 0), wit_margin=best, wit_th=best_th)
    # restricted node relaxations (upper bounds on the full node values)
    Xw = np.hstack([XS, XP[:, :MR]])
    ub_frc = restricted_node(Xw, y, lam, k, fixed1=[k])            # force in the top null
    i0 = int(np.argmin(np.abs(aS)))
    ub_rem = restricted_node(Xw, y, lam, k, fixed0=[i0])           # remove the weakest true feature
    out.update(fS=fS, ub_frc=ub_frc, ub_rem=ub_rem,
               fail=bool(min(ub_frc, ub_rem) < fS * (1 - 1e-7)), fail_frc=bool(ub_frc < fS * (1 - 1e-7)),
               fail_rem=bool(ub_rem < fS * (1 - 1e-7)))
    return out


def job(args):
    t = time.time()
    o = instance(*args)
    if o is not None:
        o['time'] = time.time() - t
    return o


if __name__ == '__main__':
    from multiprocessing import Pool
    OUT, nproc = sys.argv[1], int(sys.argv[2])
    n, k = 800, 10
    jobs = []
    for p in (10 ** 4, 10 ** 6, 10 ** 9):
        for lam in (np.sqrt(n), 90.0, 280.0):
            c1 = 2 * np.log(p * lam / n); rt = 2 * np.log(p)
            grid = sorted(set([round(c1 + d, 2) for d in (-8, -6, -4, -2, 0, 2)] + [round(rt + d, 2) for d in (-4, -2, 0)]))
            for t2 in grid:
                if t2 >= n / k - 1:
                    continue
                for s in range(10):
                    jobs.append((n, p, k, lam, t2, 100000 * s + int(p % 997) + int(lam) * 7 + int(10 * t2)))
    with Pool(nproc) as pool, open(OUT, 'w') as f:
        for res in pool.imap_unordered(job, jobs):
            if res is not None:
                f.write(json.dumps(res) + '\n'); f.flush()
