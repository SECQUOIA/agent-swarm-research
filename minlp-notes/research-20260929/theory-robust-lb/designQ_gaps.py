"""Root gaps of the polynomial 'design Q' gadget x^2/(2a) + b x y + c y^2 + z^2/2 - beta z^4 + bp y z
on [-1,1]^3 for several split classes (LP relaxation of robust_bb.Relax)."""
import numpy as np
from robust_bb import Family, Relax
for (a, b, c, beta, bp) in [(4.0, 0.5, 0.5945, 0.35, 0.3), (6.0, 0.5, 0.9536, 0.25, 0.6)]:
    fam = Family([[0, 0, 1 / (2 * a)], [0, 0, c], [0, 0, 0.5, 0, -beta]], [b, bp])
    out = []
    for cls in ["env", "a", "b3", "b4", "b6", "b8"]:
        lo, up, it = Relax(fam, cls, K=9).bound(np.full(3, -1.0), np.full(3, 1.0), target=None, maxit=300, tol=1e-10)
        out.append("%s %.6f" % (cls, -up))
    print("a=%g b=%g c=%g beta=%g bp=%g  root gaps: " % (a, b, c, beta, bp) + ", ".join(out), flush=True)
