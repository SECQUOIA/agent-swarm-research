"""Recompute the amp 0.3, n = 1000 row of the verification table at
eps-optimal points (after review: multistart missed the optimum for 4 seeds).

For each seed: prototype (mode quad, eps 1e-6) LB/UB and point x; smallest
Hessian eigenvalue at x; max |x_i|; number of coordinates at the bounds; and
the multistart value from data/verify.jsonl for comparison.
"""
import json
import numpy as np
from scipy.linalg import eigvalsh_tridiagonal
import instances as I
import chain_bb as CB

ms = {r["seed"]: r for r in map(json.loads, open("data/verify.jsonl")) if r["amp"] == 0.3 and r["n"] == 1000}
for seed in range(5):
    c = I.coeffs(1000, seed, 0.3)
    r = CB.chain_bb(I.Probe3Chain(c), 1e-6, mode="quad", unary_sub=16, time_limit=600,
                    max_pairs_iter=60_000_000)
    x = r["x"]
    d, off = I.hess_tridiag(x)
    lmin = float(eigvalsh_tridiagonal(d, off, select="i", select_range=(0, 0))[0])
    rec = dict(amp=0.3, n=1000, seed=seed, status=r["status"], LB=r["LB"], UB=r["UB"], pairs=r["pairs"],
               time=r["time"], lmin_hess_at_x=lmin, max_abs_x=float(abs(x).max()),
               coords_at_bound=int((abs(x) > 1 - 1e-9).sum()),
               multistart_f_best=ms[seed]["f_best"], multistart_minus_UB=ms[seed]["f_best"] - r["UB"])
    print(json.dumps(rec), flush=True)
