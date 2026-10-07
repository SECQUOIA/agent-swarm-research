"""Family of Theorem B: sbar = (0, 0, eps), rays p1 = (1, -1, 0), p2 = (1, -k, 0), p3 = (1, 1, 1),
costs (1, 1, 1), S = {w <= x y}.  For each eps: exact z_K, the invariant D, relative ray
discriminants, cond(P), the parabolic-cylinder bound rho_par, the best family-(A) bound
(SDP bisection, Clarabel and SCS), a heuristic family-(B) bound, and SCIP's set (A and B
versions).  Ratios are to z_K; the last columns divide by sqrt(eps).
usage: python3 sharp_family.py [k]"""
import sys
import json
import numpy as np
import warnings
import rb

warnings.filterwarnings('ignore')
k = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
P = np.array([[1.0, 1.0, 1.0], [-1.0, -k, 1.0], [0.0, 0.0, 1.0]])
c = np.ones(3)
for e in range(1, 9):
    eps = 10.0 ** (-e)
    sbar = np.array([0.0, 0.0, eps])
    z, lam = rb.zK(sbar, P, c)
    Pt = rb.scaled_rays(P, c, z)
    D = rb.D_inv(sbar, Pt)
    disc = []
    for j in range(3):
        p = P[:, j]
        A_ = -p[0] * p[1]
        B_ = rb.grad(sbar) @ p
        disc.append((B_ * B_ - 4 * A_ * eps) / (B_ * B_ + abs(4 * A_ * eps)))
    rp, tb = rb.rho_par(sbar, Pt)
    cA, hA, XA = rb.zA_ratio(sbar, Pt, iters=40)
    cS, hS, _ = rb.zA_ratio(sbar, Pt, iters=30, solver='SCS')
    zB, XB = rb.zB_heur(sbar, Pt, X0s=[XA], restarts=12, seed=1)
    sA = rb.scip_ratio(sbar, Pt, 'A')
    sB = rb.scip_ratio(sbar, Pt, 'B')
    out = dict(eps=eps, zK=z, support=[int(i) for i in np.flatnonzero(lam > 1e-12)], D=D,
               thmA=rb.theoremA_bound(D), rel_disc=[round(d, 6) for d in disc], condP=np.linalg.cond(P),
               rho_par=rp, t=tb, zA_cert=cA, zA_hi_clarabel=hA, zA_hi_scs=hS, zB_found=zB,
               scipA=sA, scipB=sB,
               per_sqrt_eps=dict(rho_par=rp / np.sqrt(eps), zA=cA / np.sqrt(eps), zA_hi=hA / np.sqrt(eps),
                                 zB=zB / np.sqrt(eps), scipB=sB / np.sqrt(eps)))
    print(json.dumps(out), flush=True)
