"""SCIP's rule without conditioning (Proposition S2): sbar = (0, 0, 1), rays p1 = (L, -1/L, 0),
p2 = (L, 1/L, 0), p3 = (0, 0, 1), costs 1.  This is the image of the L = 1 instance under the
automorphism (x, y, w) -> (L x, y / L, w).  D = 1 and all relative ray discriminants are +-1 for
every L; z_K = 1; the orbit ratio is 1 (cylinder t = 1/L); SCIP's set is the cylinder t = 1 and gives
2 / (L + 1/L) (step along ray 2; ray 1 gets 2 / (L - 1/L)), while cond(P~) = L^2."""
import numpy as np
import warnings
import rb

warnings.filterwarnings('ignore')
for L in (1.0, 2.0, 10.0, 100.0, 1000.0):
    sbar = np.array([0.0, 0.0, 1.0])
    P = np.array([[L, L, 0.0], [-1 / L, 1 / L, 0.0], [0.0, 0.0, 1.0]])
    c = np.ones(3)
    z, lam = rb.zK(sbar, P, c)
    Pt = rb.scaled_rays(P, c, z)
    disc = []
    for j in range(3):
        p = Pt[:, j]
        A_, B_ = -p[0] * p[1], rb.grad(sbar) @ p
        disc.append(round((B_ * B_ - 4 * A_ * rb.q(sbar)) / (B_ * B_ + abs(4 * A_ * rb.q(sbar))), 6))
    cyl = rb.cyl_steps(sbar, Pt, 1.0 / L).min()
    print('L=%g zK=%.6f supp=%s D=%.4f rel.disc=%s cond(P~)=%.4g orbit cylinder t=1/L: %.6f  SCIP A %.6f  SCIP B %.6f  '
          '2/(L+1/L)=%.6f' % (L, z, np.flatnonzero(lam > 1e-12).tolist(), rb.D_inv(sbar, Pt), disc, np.linalg.cond(Pt), cyl,
                             rb.scip_ratio(sbar, Pt, 'A'), rb.scip_ratio(sbar, Pt, 'B'),
                             2 / (L + 1 / L)))
