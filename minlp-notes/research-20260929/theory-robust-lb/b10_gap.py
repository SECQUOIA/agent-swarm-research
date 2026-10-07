"""Relaxation LP (robust_bb.Relax) for classes b8, b9, b10 at the gadget root, reference parameters."""
import numpy as np
from robust_bb import gadget_chain, Relax
fam = gadget_chain(1)
for cls in ["b8", "b9", "b10"]:
    lo, up, it = Relax(fam, cls, K=9).bound(np.full(3, -1.0), np.full(3, 1.0), target=None, maxit=400, tol=1e-12)
    print("%s: relaxation LP  lower %.3e  upper %.3e  (gap = -LB)  iterations %d" % (cls, lo, up, it))
