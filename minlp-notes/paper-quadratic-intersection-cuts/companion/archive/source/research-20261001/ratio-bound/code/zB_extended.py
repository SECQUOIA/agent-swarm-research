"""Family (B) on the Theorem B family with the extended search (sbar may lie only in the upward
closure, 4-parameter X); every value is the exact (B) bound of an explicit X, i.e. a lower bound on z_B."""
import numpy as np
import warnings
import rb

warnings.filterwarnings('ignore')
P = np.array([[1.0, 1.0, 1.0], [-1.0, -2.0, 1.0], [0.0, 0.0, 1.0]])
c = np.ones(3)
for e in (5, 6, 8):
    eps = 10.0 ** -e
    sbar = np.array([0.0, 0.0, eps])
    z, _ = rb.zK(sbar, P, c)
    Pt = rb.scaled_rays(P, c, z)
    v, X = rb.zB_heur(sbar, Pt, restarts=16, seed=2)
    print('eps=1e-%d  zB_found/z_K = %.6g  per sqrt(eps) = %.4f  X = %s' % (e, v, v / np.sqrt(eps), np.round(X, 6).tolist()), flush=True)
