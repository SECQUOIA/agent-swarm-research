"""Check of the review's ceiling for Theorem 4.2 (F4): with exact gadget bounds V, the full cube gives
Phi(mu) >= exp(-mu gamma), and a corner box with V > 0 gives Phi(mu) >= (vol/8) exp(mu V) >= 1 for mu >= 2.4.
So Theorem 4.2 cannot give more than exp(2.4 gamma) per gadget.  V is bounded below by the class-(a)
dual (split) bound of robust_bb.Relax, which is a valid lower bound on LB_(a)."""
import numpy as np
from robust_bb import gadget_chain, Relax
fam = gadget_chain(1)
gamma = 0.0761186
l = np.array([-1.0, -1.0, -1.0]); u = np.array([-0.48, -0.873, -0.813])
lo, up, it = Relax(fam, "a", K=9).bound(l, u, target=None, maxit=200, tol=1e-12)
vol8 = np.prod((u - l) / 2)
for mu in [2.3, 2.4, 2.5]:
    print("mu=%.1f: corner box V in [%.6f, %.6f], (vol/8) exp(mu V_lower) = %.4f;  exp(mu gamma) = %.4f per gadget, %.4f per variable"
          % (mu, lo, up, vol8 * np.exp(mu * lo), np.exp(mu * gamma), np.exp(mu * gamma / 3)))
