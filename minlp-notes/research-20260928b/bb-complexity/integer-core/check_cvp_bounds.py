"""Checks for the random-CVP theorems (Section 3 of relaxation-intrinsic-bounds.md).

For each instance: lattice L = B Z^n of determinant 1 (Goldstein-Mayer 'gm',
approximately Haar; or Gaussian basis 'gauss'), target t uniform mod L,
phi(z) = ||Bz - t||^2.  Units: squared lengths are divided by GH^2.

Reported per instance:
  OPT, lam1^2                                  (normalized by GH^2)
  clique test (Theorem 3.4), rho = 4/3:
    N43   = #{z : phi(z) < (4/3) OPT}
    M43   = #unordered non-conflicting pairs inside that ball
    lb43  = N43 - M43  (deletion lower bound on the clique; proof of Theorem 3.4)
    om43  = exact clique number of the conflict graph restricted to the ball
  class test (Theorem 3.5):
    Nc    = #{z : phi(z) < OPT + lam1^2/2}; the theorem gives kappa >= Nc/(n+1)
  upper-bound test (proof of Proposition 3.6(c)):
    N2    = #{z : phi(z) < 2 OPT}
    omg   = greedy clique among all points with phi < 2.5 OPT and number of its
            members with phi >= 2.2 OPT (must be <= 12)
Conflict: phi((a+b)/2) < OPT (eps = 0, strict, relative tolerance 1e-10).
"""
import os
import sys
import json
import math
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from multiprocessing import Pool
from lattice_tools import lll, enum_ball, gm_basis, gauss_basis, gh_radius, max_clique, greedy_clique


def instance(args):
    n, kind, seed = args
    rng = np.random.default_rng(10_000 * n + seed + (0 if kind == "gm" else 5_000_000))
    B = gm_basis(n, rng) if kind == "gm" else gauss_basis(n, rng)
    B = lll(B)
    GH2 = gh_radius(n) ** 2
    Q, R = np.linalg.qr(B)
    # lambda_1
    r2 = min(np.sum(B * B, 0))
    lam1sq = min(p[0] for p in enum_ball(R, np.zeros(n), r2 * (1 + 1e-9), exclude_zero=True))
    t = B @ rng.random(n)
    tt = Q.T @ t
    # Babai upper bound then exact CVP
    z = np.zeros(n)
    for i in range(n - 1, -1, -1):
        z[i] = round((tt[i] - R[i, i + 1:] @ z[i + 1:]) / R[i, i])
    ub = float(np.sum((R @ z - tt) ** 2))
    # exact CVP: grow the radius from 0.8 GH^2 until a point is found (never above Babai)
    r2 = min(0.8 * GH2, ub)
    while True:
        cand = enum_ball(R, tt, min(r2, ub) * (1 + 1e-12))
        if cand:
            break
        r2 *= 1.15
    OPT = min(p[0] for p in cand)
    big = n <= 20
    rad2 = (2.5 if big else 1.55) * OPT
    pts = enum_ball(R, tt, rad2, limit=200000)
    U = np.array([R @ p[1] - tt for p in pts])
    f = np.einsum("ij,ij->i", U, U)
    thr = 4 * OPT * (1 - 1e-10)  # conflict iff |u+w|^2 < 4 OPT

    def conflict_matrix(idx):
        V = U[idx]
        s = V @ V.T
        sq = np.diag(s)
        summ = sq[:, None] + sq[None, :] + 2 * s
        A = summ < thr
        np.fill_diagonal(A, False)
        return A

    out = dict(n=n, kind=kind, seed=seed, OPT=OPT / GH2, lam1sq=lam1sq / GH2)
    # clique test at rho = 4/3
    i43 = np.where(f < (4 / 3) * OPT)[0]
    A43 = conflict_matrix(i43)
    N43 = len(i43)
    M43 = int((~A43).sum() - N43) // 2
    out.update(N43=N43, M43=M43, lb43=N43 - M43)
    out["om43"] = max_clique(A43.tolist()) if N43 <= 150 else greedy_clique(A43)
    out["om43_exact"] = N43 <= 150
    # class test
    out["Nc"] = int((f < OPT + lam1sq / 2).sum())
    out["class_lb"] = out["Nc"] / (n + 1)
    # upper-bound test (only for n <= 20, where all points below 2.5 OPT are listed)
    if not big:
        out["npts"] = len(f)
        return out
    out["N2"] = int((f < 2 * OPT).sum())
    iall = np.argsort(f)[:3000]
    Aall = conflict_matrix(iall)
    # greedy clique on all points below 2.5 OPT; count members with f >= 2.2 OPT
    best, bestcl = 0, None
    deg = Aall.sum(1)
    order = np.argsort(-deg)
    for s in order[:40]:
        cl = [s]
        cand = Aall[s].copy()
        for j in order:
            if cand[j]:
                cl.append(j)
                cand &= Aall[j]
        if len(cl) > best:
            best, bestcl = len(cl), cl
    out["omg"] = best
    out["omg_big"] = int((f[iall][bestcl] >= 2.2 * OPT).sum())
    out["npts"] = len(f)
    return out


if __name__ == "__main__":
    ns = [int(v) for v in sys.argv[1].split(",")]
    nseeds = int(sys.argv[2])
    outfile = sys.argv[3]
    kinds = sys.argv[4].split(",") if len(sys.argv) > 4 else ["gm", "gauss"]
    procs = int(sys.argv[5]) if len(sys.argv) > 5 else 12
    jobs = [(n, k, s) for n in ns for k in kinds for s in range(nseeds)]
    with Pool(procs) as pool, open(outfile, "w") as fo:
        for r in pool.imap_unordered(instance, jobs):
            fo.write(json.dumps(r) + "\n")
            fo.flush()
