"""Reviewer checks of Section 3 (condition C1 at x*).

For each instance, all N single-wrong-fixing node values
    r_i = min{ ||v_i + B_{-i} u||^2 : u in [0,2]^{N-1} },  v_i = w + 2 b_i,
are computed: NNLS (scipy), and if the NNLS solution leaves the box, BVLS on
[0,2] (scipy lsq_linear).  Reported per instance:
  * min_i (r_i - W)/N versus the first-order law (theta/theta_c - 1)/2 and the
    note's second-order prediction,
  * mean r_i/||v_i||^2 versus 1 - (N-1)/(2M),
  * box inactivity of all nodes, and the largest NNLS coefficient
    (node 0 separately: one fixed node is enough to refute C1).
C1 "holds" here means min_i r_i > W (then x* is the unique optimum).
Written by the reviewer.
Usage: python3 c1_checks.py main > c1_checks.out ;  python3 c1_checks.py tail > nnls_tail.out
"""
import os, sys, json
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import nnls, lsq_linear
from multiprocessing import Pool


def node_values(B, w):
    M, N = B.shape
    W = float(w @ w)
    r = np.empty(N); nv = np.empty(N); umax = np.empty(N); ina = np.empty(N, bool)
    for i in range(N):
        v = w + 2.0 * B[:, i]
        Bf = np.delete(B, i, axis=1)
        u, rn = nnls(Bf, -v, maxiter=100 * N)
        umax[i] = u.max(); ina[i] = umax[i] <= 2.0
        if ina[i]:
            r[i] = rn ** 2
        else:
            res = lsq_linear(Bf, -v, bounds=(0.0, 2.0), method="bvls", tol=1e-13)
            rr = v + Bf @ np.clip(res.x, 0, 2)
            r[i] = rr @ rr
        nv[i] = v @ v
    return W, r, nv, umax, ina


def job(args):
    beta, N, mult, seed = args
    M = int(round(beta * N))
    thc = 1.0 / (4 * (2 * beta - 1))
    theta = mult * thc
    rho = theta * N
    rng = np.random.default_rng(seed)
    H = rng.standard_normal((M, N)); xs = rng.choice([-1.0, 1.0], N); w = rng.standard_normal(M)
    B = np.sqrt(rho / N) * H * xs
    W, r, nv, umax, ina = node_values(B, w)
    first = (theta / thc - 1) / 2
    second = (2 * (2 * beta - 1) * (rho - np.sqrt(2 * rho * np.log(N) / beta)) - N / 2) / N
    return dict(beta=beta, N=N, M=M, mult=mult, theta=theta, seed=seed,
                min_gap=float((r.min() - W) / N), first=first, second=float(second),
                mean_ratio=float(np.mean(r / nv)), law=1 - (N - 1) / (2 * M),
                all_inactive=bool(ina.all()), n_active=int((~ina).sum()),
                umax=float(umax.max()), umax0=float(umax[0]), gap0=float((r[0] - W) / N),
                c1=bool(r.min() > W))


def main():
    jobs = []
    for beta in (1.0, 1.5, 2.0, 3.0):
        mults = (0.5, 0.8, 1.0, 1.2, 1.5, 2.0) if beta == 1.0 else (0.8, 1.0, 1.2, 1.5, 2.0)
        for mult in mults:
            for N, ns in ((200, 4), (400, 4)):
                jobs += [(beta, N, mult, 7000 + 97 * s + N + int(10 * mult) + int(100 * beta)) for s in range(ns)]
    for beta in (1.0, 2.0):
        for mult in (0.8, 1.2, 1.5, 2.0):
            jobs += [(beta, 800, mult, 9000 + s + int(10 * mult) + int(100 * beta)) for s in range(2)]
    jobs.sort(key=lambda a: -a[1] * a[0])  # big jobs first
    with Pool(5) as p, open("c1_checks.jsonl", "w") as f:
        for res in p.imap_unordered(job, jobs):
            f.write(json.dumps(res) + "\n"); f.flush()


def summarize():
    rows = [json.loads(l) for l in open("c1_checks.jsonl")]
    keys = sorted({(r["beta"], r["N"], r["mult"]) for r in rows})
    print("beta N theta/theta_c theta | runs C1-holds | mean min_i(r_i-W)/N  first-order  second-order | "
          "mean r/|v|^2  law | all nodes box-inactive  max NNLS coef (all nodes / node 0) | node0 gap")
    for k in keys:
        R = [r for r in rows if (r["beta"], r["N"], r["mult"]) == k]
        g = np.mean([r["min_gap"] for r in R])
        print(f"{k[0]:.1f} {k[1]} {k[2]:.1f} {R[0]['theta']:.4f} | {len(R)} {sum(r['c1'] for r in R)} | "
              f"{g:+.3f} {R[0]['first']:+.3f} {np.mean([r['second'] for r in R]):+.3f} | "
              f"{np.mean([r['mean_ratio'] for r in R]):.4f} {R[0]['law']:.4f} | "
              f"{sum(r['all_inactive'] for r in R)}/{len(R)}  {max(r['umax'] for r in R):.3f} / {max(r['umax0'] for r in R):.3f} | "
              f"{np.mean([r['gap0'] for r in R]):+.3f}")


def tail_job(args):
    N, T, seed = args
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(T):
        Hs = rng.standard_normal((N, N - 1)) / np.sqrt(N)
        xi = rng.standard_normal(N)
        u, _ = nnls(Hs, xi, maxiter=100 * N)  # law of the node problem: v indep. of the design
        out.append(float(u.max()))
    return N, out


def tail():
    """Conjecture 3.3 reduction.  For beta = 1 the node-i problem has the law of
    min ||v + B' u||, v ~ N(0,(1+4 theta) I_N) independent of B' = sqrt(theta) H'
    (H' N x (N-1) Gaussian).  Its NNLS solution is u = sqrt((1+4theta)/theta) * U/sqrt(N)
    with U = max NNLS coefficient of xi ~ N(0,I_N) on H'/sqrt(N), up to the factor
    ||v||/(sqrt(1+4 theta)||xi||) = 1 + O(N^{-1/2}).  Box inactivity at theta = 1/4:
    U <= sqrt(N/2);  at theta = 1/8: U <= 0.577 sqrt(N)."""
    jobs = [(100, 400, 11 + s) for s in range(5)] + [(200, 200, 21 + s) for s in range(5)] + \
           [(400, 80, 31 + s) for s in range(5)] + [(800, 20, 41 + s) for s in range(5)] + [(1600, 6, 51 + s) for s in range(5)]
    with Pool(5) as p:
        res = p.map(tail_job, jobs)
    for N in (100, 200, 400, 800, 1600):
        U = np.concatenate([np.array(o) for n, o in res if n == N])
        q = np.quantile(U, [0.5, 0.9, 0.99]) if len(U) >= 100 else np.quantile(U, [0.5, 0.9, 1.0])
        print(f"N={N} samples={len(U)}: U median={q[0]:.2f} q90={q[1]:.2f} q99/max={q[2]:.2f} max={U.max():.2f}  "
              f"max U/sqrt(N)={U.max()/np.sqrt(N):.3f}  thresholds U/sqrt(N): theta=1/4 -> 0.707, theta=1/8 -> 0.577; "
              f"frac(U > sqrt(N/2))={np.mean(U > np.sqrt(N/2)):.4f}")


if __name__ == "__main__":
    if sys.argv[1] == "main":
        main(); summarize()
    elif sys.argv[1] == "sum":
        summarize()
    else:
        tail()
