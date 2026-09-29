"""Shared helpers for the recheck.  Nothing is imported from the note's code/.

The generator mirrors the one documented in the note (Section 7; the scout's
bls.py): rng = default_rng(seed); H (M x N) iid N(0,1); A = sqrt(rho/N) H;
x* uniform signs; w ~ N(0, I_M); y = A x* + w.  Error coordinates:
B = A diag(x*), u = 1 - x* o x in [0, 2]^N, y - A x = w + B u.
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import lsq_linear


def make_instance(N, M, rho, seed):
    rng = np.random.default_rng(seed)
    H = rng.standard_normal((M, N))
    A = np.sqrt(rho / N) * H
    xs = rng.choice([-1.0, 1.0], N)
    noise = rng.standard_normal(M)
    y = A @ xs + noise
    return A, y, xs


def box_value(C, v):
    """min ||v + C u||^2 over u in [0,2]^k by BVLS, and a certified lower
    bound (Lagrangian/Frank-Wolfe) at the returned point.  Returns
    (val, lb, u)."""
    k = C.shape[1]
    if k == 0:
        val = float(v @ v)
        return val, val, np.zeros(0)
    r = lsq_linear(C, -v, bounds=(0.0, 2.0), method="bvls", tol=1e-14,
                   max_iter=20 * k + 100)
    u = np.clip(r.x, 0.0, 2.0)
    res = v + C @ u
    val = float(res @ res)
    g = 2.0 * (C.T @ res)
    lb = val + float(np.sum(np.minimum(-g * u, g * (2.0 - u))))
    return val, lb, u
