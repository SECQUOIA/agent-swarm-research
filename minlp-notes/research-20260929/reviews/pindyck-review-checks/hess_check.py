"""Hessian identity check (not part of any proof).

At points p of G' (p*, hit-and-run points, LP vertices of G' in random directions, and points
on faces of G' where some d_t < 0), compare
  (a) the finite-difference Hessian of J at 50 digits (own simulation, own_psi.J_mp),
  (b) own_psi.psi_float(theta(p)),
  (c) the author's psi_tm at the degenerate box theta(p) (centre matrix),
  (d) own_psi.psi_af at the degenerate box (enclosure must contain (a)).
Also records whether theta(p) lies in Theta' (own) and in the author's Theta.
"""
import os
import pickle
import sys
import time

os.environ.setdefault("OMP_NUM_THREADS", "1")
import mpmath as mp
import numpy as np
from scipy.optimize import linprog

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import own_psi as P  # noqa: E402
import author_exec  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = open(os.path.join(HERE, "logs", "hess_check.log"), "w")


def say(*a):
    s = " ".join(str(v) for v in a)
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


T = 16
RG = pickle.load(open(os.path.join(HERE, "ranges.pkl"), "rb"))
AD = pickle.load(open(os.path.join(HERE, "author_data.pkl"), "rb"))
W = np.array([[float(v) for v in row] for row in RG["Wq"]])
g = np.array([float(v) for v in RG["gq"]])
PRIM = os.path.join(HERE, "..", "..", "open-instances-wave2", "small", "logs", "pindyck_primal.txt")
vals = dict(line.split() for line in open(PRIM))
pstar = np.array([float(vals[f"x{t}"]) for t in range(1, 17)])

rng = np.random.default_rng(12345)
pts = [("p*", pstar)]
# LP vertices of G' in random directions (shrunk by 1e-9 towards p* to stay inside)
for k in range(6):
    c = rng.normal(size=T)
    res = linprog(-c, A_ub=W, b_ub=g, bounds=[(0, None)] * T, method="highs")
    v = res.x
    pts.append((f"vertex{k}", pstar + (1 - 1e-9) * (v - pstar)))
# hit-and-run
x = pstar.copy()
A_ = np.vstack([W, -np.eye(T)])
b_ = np.concatenate([g, np.zeros(T)])
for it in range(400):
    u = rng.normal(size=T)
    Au, sl = A_ @ u, b_ - A_ @ x
    tmax = np.min(np.where(Au > 1e-12, sl / np.where(Au > 1e-12, Au, 1), np.inf))
    tmin = np.max(np.where(Au < -1e-12, sl / np.where(Au < -1e-12, Au, 1), -np.inf))
    x = x + rng.uniform(tmin, tmax) * u
    if it % 100 == 99:
        pts.append((f"hr{it}", np.maximum(x, 0)))
# a point with high late prices (d_16 < 0 region): maximize p_16 + p_15
res = linprog(-np.eye(T)[15] - np.eye(T)[14], A_ub=W, b_ub=g, bounds=[(0, None)] * T, method="highs")
pts.append(("max p15+p16", pstar + (1 - 1e-9) * (res.x - pstar)))

say("loading the author's definitions (steps 1-4 rerun, output discarded) ...")
NS = author_exec.load()


def fd_hessian(p, h=mp.mpf("1e-12"), dps=50):
    with mp.workdps(dps):
        pm = [mp.mpf(float(v)) for v in p]
        J0 = P.J_mp(pm, dps)
        H = np.zeros((T, T))
        cache = {}

        def Jat(di):
            key = tuple(sorted(di.items()))
            if key not in cache:
                q = list(pm)
                for i, s in di.items():
                    q[i] = q[i] + s * h
                cache[key] = P.J_mp(q, dps)
            return cache[key]
        for i in range(T):
            H[i, i] = float((Jat({i: 2}) - 2 * J0 + Jat({i: -2})) / (4 * h * h))
            for j in range(i + 1, T):
                v = (Jat({i: 1, j: 1}) - Jat({i: 1, j: -1}) - Jat({i: -1, j: 1}) + Jat({i: -1, j: -1})) / (4 * h * h)
                H[i, j] = H[j, i] = float(v)
        return H


def inbox(th, lo, hi, tol=0.0):
    return all(lo[gr][t] - tol <= th[gr][t] <= hi[gr][t] + tol for gr in P.GR for t in range(T))


t0 = time.time()
worst_b = worst_c = 0.0
for name, p in pts:
    th, J = P.theta_mp(p)
    Hfd = fd_hessian(p)
    Hb = P.psi_float(th)
    lo = {gr: np.array(th[gr]) for gr in P.GR}
    Hc = NS["psi_tm"](lo, lo).c
    Haf = P.psi_af(lo, lo)
    C, A, R = P.point_form(Haf)
    inside_af = bool(np.all(np.abs(Hfd - C) <= R + 1e-12))
    db, dc = np.abs(Hb - Hfd).max(), np.abs(Hc - Hfd).max()
    worst_b, worst_c = max(worst_b, db), max(worst_c, dc)
    say(f"{name:12s} min d = {min(th['d']):8.3f}  lam_max(FD) = {np.linalg.eigvalsh(Hfd)[-1]:.5f}  "
        f"|own Psi - FD| = {db:.1e}  |author psi_tm - FD| = {dc:.1e}  own AF encloses FD: {inside_af} "
        f"(max R {R.max():.1e})  theta in own Theta': {inbox(th, RG['lo'], RG['hi'])}  "
        f"in author Theta: {inbox(th, AD['lo0'], AD['hi0'])}")
say(f"max |own Psi - FD| = {worst_b:.2e}, max |author psi_tm - FD| = {worst_c:.2e}; {len(pts)} points, {time.time() - t0:.0f} s")
