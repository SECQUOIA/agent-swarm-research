"""Near-tangent family (Section 3.3 of the note): sbar = (0, 0, 1),
    p1 = (1, -1, -2(1 - eta)),  p2 = (1, -k, -2 sqrt(k) (1 - eta)),  p3 = (1, 1, L),  costs 1.
Rays 1 and 2 pass within q = 2 eta - eta^2 of the boundary of S (relative discriminant
((1 - eta)^2 - 1)/((1 - eta)^2 + 1) ~ -eta) and never meet it; ray 3 crosses it transversally near s = L.
For each L: z_K (closed form of the sfree code), the depth D, the cylinder value rho_par, z_A (SDP bisection,
Clarabel), optionally a heuristic family-(B) value with an independent membership check of its set; the columns D * ratio show the constant in front of 1/D.
usage: python3 tangent_family.py ETA K [B|A] [L1,L2,...]   (B: also run the slow heuristic (B) search;
default L list 10,30,100,300,1000)"""
import sys
import json
import numpy as np
import warnings
import rb

warnings.filterwarnings('ignore')
eta, k = float(sys.argv[1]), float(sys.argv[2])
doB = len(sys.argv) > 3 and sys.argv[3] == 'B'
Ls = [float(t) for t in sys.argv[4].split(',')] if len(sys.argv) > 4 else [10.0, 30.0, 100.0, 300.0, 1000.0]
sbar = np.array([0.0, 0.0, 1.0])
for L in Ls:
    P = np.array([[1.0, 1.0, 1.0], [-1.0, -k, 1.0], [-2 * (1 - eta), -2 * np.sqrt(k) * (1 - eta), L]])
    c = np.ones(3)
    z, lam = rb.zK(sbar, P, c)
    Pt = rb.scaled_rays(P, c, z)
    D = rb.D_inv(sbar, Pt)
    rp, _ = rb.rho_par(sbar, Pt)
    cA, hA, XA = rb.zA_ratio(sbar, Pt, iters=40)
    out = dict(eta=eta, k=k, L=L, zK=z, support=np.flatnonzero(lam > 1e-12).tolist(), D=D,
               thmA=rb.theoremA_bound(D), rho_par=rp, zA_cert=cA, zA_hi=hA,
               D_times=dict(thmA=D * rb.theoremA_bound(D), rho_par=D * rp, zA=D * cA))
    if doB:
        zB, XB = rb.zB_heur(sbar, Pt, X0s=[XA], restarts=10, seed=1)
        out['zB_found'] = zB
        out['D_times']['zB_found'] = D * zB
        # independent check of the returned set: det > 0, sbar and the vertices of T_r, r = 0.999 zB,
        # lie in its upward closure (membership test of rb.in_B_X, normalized frame)
        Pn = rb.normalize(sbar, Pt)
        o = np.array([0.0, 0.0, 1.0])
        out['zB_check'] = bool(np.all(np.isfinite(XB)) and np.linalg.det(XB) > 0 and rb.in_B_X(XB, o) and
                               all(rb.in_B_X(XB, o + 0.999 * zB * Pn[:, j]) for j in range(3)))
        out['XB'] = np.round(XB, 8).tolist()
    print(json.dumps(out), flush=True)
