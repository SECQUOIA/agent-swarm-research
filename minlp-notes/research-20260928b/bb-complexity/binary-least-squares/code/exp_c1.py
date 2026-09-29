"""E2: condition C1 at x* (every single wrong fixing prunable with incumbent
f(x*)).  For each instance all N single-wrong-fixing nodes are solved; C1 is
certified when every certified lower bound exceeds f(x*) (then x* is the
unique optimum), and refuted when some node value (a primal feasible value)
is below f(x*).
Also records the exact-law check of Theorem 2.3 at the nodes:
node_i / ||v_i||^2 versus 1 - (N-1)/(2M) when the node NNLS is box-inactive.
Usage: python3 exp_c1.py OUT.jsonl N beta thetas nseeds [procs]
"""
import sys, json, os
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np
from multiprocessing import Pool
from core import instance, box_min, single_fixings


def job(args):
    N, beta, th, s = args
    M = int(round(beta * N)); rho = th * N
    A, y, xs, B, w = instance(N, M, rho, s)
    W = float(w @ w)
    R, Rlb, u, ina = box_min(B, w)
    vals, lbs, inas = single_fixings(B, w)
    v2 = np.array([float((w + 2 * B[:, i]) @ (w + 2 * B[:, i])) for i in range(N)])
    c1_cert = bool(np.all(lbs > W))
    c1_refuted = bool(np.any(vals < W))
    # linearized predictor: node_i ~ ||v_i||^2 (1 - G/W)
    G = W - R
    pred = v2 * (1 - G / W)
    zeta = B.T @ w
    return dict(N=N, M=M, beta=beta, theta=th, rho=rho, seed=s, W=W, G=G,
                min_margin=float((vals.min() - W) / N), c1=c1_cert, refuted=c1_refuted,
                frac_node_inactive=float(inas.mean()),
                mean_ratio=float(np.mean(vals / v2)), law_ratio=1 - (N - 1) / (2 * M),
                pred_c1=bool(pred.min() > W),
                argmin_zeta_rank=int(np.argsort(np.argsort(zeta))[int(np.argmin(vals))]),
                umax_root=float(u.max()))


if __name__ == "__main__":
    out = sys.argv[1]; N = int(sys.argv[2]); beta = float(sys.argv[3])
    ths = [float(t) for t in sys.argv[4].split(",")]; ns = int(sys.argv[5])
    procs = int(sys.argv[6]) if len(sys.argv) > 6 else 5
    jobs = [(N, beta, th, s) for th in ths for s in range(ns)]
    with Pool(procs) as pool, open(out, "a") as f:
        for r in pool.imap_unordered(job, jobs):
            f.write(json.dumps(r) + "\n"); f.flush()
