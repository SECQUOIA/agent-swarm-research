"""Monte Carlo soundness test of own_psi.psi_af (not part of the proof): at random eps
(half of them vertices of the eps-cube), theta = c + rad eps and the float Psi(theta) must lie in
C + sum eps_k A_k +- R. Reports the largest used fraction of R."""
import os
import pickle
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import own_psi as P  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RG = pickle.load(open(os.path.join(HERE, "ranges.pkl"), "rb"))
AD = pickle.load(open(os.path.join(HERE, "author_data.pkl"), "rb"))
RA = pickle.load(open(os.path.join(HERE, "ranges_authorG.pkl"), "rb"))
lo = {g: np.minimum(np.minimum(np.array(RG["lo"][g]), AD["lo0"][g]), np.array(RA["lo"][g])) for g in P.GR}
hi = {g: np.maximum(np.maximum(np.array(RG["hi"][g]), AD["hi0"][g]), np.array(RA["hi"][g])) for g in P.GR}
rng = np.random.default_rng(7)
out = open(os.path.join(HERE, "logs", "af_soundness.log"), "w")
for label, (l, h) in [("root box (hull of both Theta)", (lo, hi)),
                      ("small box (1% of root widths around the centre)",
                       ({g: 0.5 * (lo[g] + hi[g]) - 0.005 * (hi[g] - lo[g]) for g in P.GR},
                        {g: 0.5 * (lo[g] + hi[g]) + 0.005 * (hi[g] - lo[g]) for g in P.GR}))]:
    H = P.psi_af(l, h)
    C, A, R = P.point_form(H)
    par = P.param_forms(l, h)
    cen = {g: np.array([float(par[g][t].cl) for t in range(16)]) for g in P.GR}
    rad = {g: np.array([float(par[g][t].ah[gi * 16 + t]) for t in range(16)]) for gi, g in enumerate(P.GR)}
    worst, bad, lam = 0.0, 0, -1.0
    for s in range(300):
        eps = rng.uniform(-1, 1, size=P.m) if s % 2 else rng.choice([-1.0, 1.0], size=P.m)
        th = {g: cen[g] + rad[g] * eps[gi * 16:(gi + 1) * 16] for gi, g in enumerate(P.GR)}
        Hp = P.psi_float(th)
        lin = C + np.tensordot(eps, A, axes=1)
        dev = np.abs(Hp - lin)
        bad += int(np.any(dev > R + 1e-13))
        worst = max(worst, float((dev / np.maximum(R, 1e-300)).max()))
        lam = max(lam, float(np.linalg.eigvalsh(Hp)[-1]))
    msg = (f"{label}: 300 samples, enclosure violations: {bad}, largest |Psi - linear part| / R = {worst:.3f}, "
           f"largest lambda_max(Psi) among samples = {lam:.4f}")
    print(msg)
    out.write(msg + "\n")
