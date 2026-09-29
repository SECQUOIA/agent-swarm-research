"""Midpoint-conflict lower bound for CVP / integer least squares.

For f(x) = ||Bx - t||^2 over x in Z^n, any B&B tree that branches on split
disjunctions (any integer direction, e.g. after lattice reduction) and bounds
nodes by the continuous relaxation needs at least
    #{x in Z^n : ||Bx - t||^2 < OPT + lambda_1(L)^2/4 - eps}
leaves, because every two such points have a midpoint of value < OPT - eps.
This script counts that set for random unimodular lattices (Gaussian basis
scaled to det 1) and uniform random targets, and compares with the Gaussian
heuristic prediction  vol(ball of radius sqrt(OPT + lambda1^2/4)).
"""
import os, sys, json, math
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np
from multiprocessing import Pool


def lll(B, delta=0.99):
    B = B.copy().astype(float)
    n = B.shape[1]

    def gs(B):
        Q = np.zeros_like(B); mu = np.zeros((n, n)); nb = np.zeros(n)
        for i in range(n):
            v = B[:, i].copy()
            for j in range(i):
                mu[i, j] = B[:, i] @ Q[:, j] / nb[j]
                v -= mu[i, j] * Q[:, j]
            Q[:, i] = v; nb[i] = v @ v
        return Q, mu, nb
    Q, mu, nb = gs(B)
    k = 1
    while k < n:
        for j in range(k - 1, -1, -1):
            q = round(mu[k, j])
            if q:
                B[:, k] -= q * B[:, j]
                Q, mu, nb = gs(B)
        if nb[k] >= (delta - mu[k, k - 1] ** 2) * nb[k - 1]:
            k += 1
        else:
            B[:, [k - 1, k]] = B[:, [k, k - 1]]
            Q, mu, nb = gs(B)
            k = max(k - 1, 1)
    return B


def enum_ball(R, tt, r2, collect=True, exclude_zero=False):
    """All integer z with ||R z - tt||^2 <= r2, R upper triangular."""
    n = R.shape[0]
    out = []
    z = np.zeros(n)

    def rec(i, partial):
        # coordinate i, contributions from j > i fixed
        c = (tt[i] - R[i, i + 1:] @ z[i + 1:]) / R[i, i]
        rem = r2 - partial
        if rem < 0:
            return
        w = math.sqrt(rem) / abs(R[i, i])
        lo, hi = math.ceil(c - w), math.floor(c + w)
        for v in range(lo, hi + 1):
            z[i] = v
            d = (R[i, i] * (v - c)) ** 2
            if i == 0:
                if partial + d <= r2:
                    if not (exclude_zero and not z.any()):
                        out.append((partial + d, z.copy()))
            else:
                rec(i - 1, partial + d)
        z[i] = 0
    rec(n - 1, 0.0)
    return out


def sample(args):
    n, seed = args
    rng = np.random.default_rng(seed)
    B = rng.standard_normal((n, n))
    B /= abs(np.linalg.det(B)) ** (1.0 / n)
    B = lll(B)
    Q, R = np.linalg.qr(B)
    # lambda_1 by enumeration around 0
    r2 = min(np.sum(B * B, 0))
    pts = enum_ball(R, np.zeros(n), r2 * (1 + 1e-9), exclude_zero=True)
    lam1sq = min(p[0] for p in pts)
    u = rng.random(n)
    t = B @ u
    tt = Q.T @ t
    # Babai upper bound then exact CVP
    z = np.zeros(n)
    for i in range(n - 1, -1, -1):
        z[i] = round((tt[i] - R[i, i + 1:] @ z[i + 1:]) / R[i, i])
    ub = float(np.sum((R @ z - tt) ** 2))
    pts = enum_ball(R, tt, ub * (1 + 1e-12))
    OPT = min(p[0] for p in pts)
    rad2 = OPT + lam1sq / 4
    pts = enum_ball(R, tt, rad2 * (1 - 1e-12))
    cnt = sum(1 for p in pts if p[0] < rad2 * (1 - 1e-12))
    vol = math.pi ** (n / 2) / math.gamma(n / 2 + 1)
    gh = vol ** (-1.0 / n)  # radius of unit-volume ball
    return dict(n=n, seed=seed, count=cnt, OPT=OPT, lam1sq=lam1sq,
                gh_pred=vol * rad2 ** (n / 2), opt_over_gh2=OPT / gh ** 2,
                lam1_over_gh2=lam1sq / gh ** 2)


if __name__ == "__main__":
    ns = [int(v) for v in sys.argv[1].split(",")]
    nseeds = int(sys.argv[2])
    out = sys.argv[3]
    jobs = [(n, s) for n in ns for s in range(nseeds)]
    with Pool(int(sys.argv[4]) if len(sys.argv) > 4 else 8) as pool, open(out, "w") as f:
        for r in pool.imap_unordered(sample, jobs):
            f.write(json.dumps(r) + "\n"); f.flush()
