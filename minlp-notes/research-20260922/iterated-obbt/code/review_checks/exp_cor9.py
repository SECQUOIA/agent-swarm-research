"""Theorem 4(b) floor and Corollary 9 root gap with eps > 0, exact 2D OBBT."""
import numpy as np
from obbt2d import Quad, ExpTerm, obbt, lower_bound
cases = [("x^2+y^2+xy", (Quad(1.), Quad(1.)), 1.0, (-1, -1.2), (1.3, 1)),
         ("x^2+y^2+1.9xy", (Quad(1.), Quad(1.)), 1.9, (-1, -1.2), (1.3, 1)),
         ("e^x-1-x+y^2+xy", (ExpTerm(), Quad(1.)), 1.0, (-0.5, -0.4), (0.6, 0.5))]
for name, e, a, lo0, hi0 in cases:
    print(name)
    for eps in [1e-2, 1e-4, 1e-6, 1e-8, 1e-10]:
        lo, hi = np.array(lo0, float), np.array(hi0, float)
        for k in range(20000):
            nlo, nhi = obbt(e, a, lo, hi, eps)
            done = np.max(np.abs(np.concatenate([nlo - lo, nhi - hi]))) <= 1e-13 * np.max(hi - lo)
            lo, hi = nlo, nhi
            if done: break
        L = lower_bound(e, a, lo, hi)
        print(f"  eps={eps:.0e} rounds={k+1:5d} width/sqrt(eps)={(hi-lo).max()/np.sqrt(eps):.5f}"
              f"  box/sqrt(eps)=({lo[0]/np.sqrt(eps):.3f},{hi[0]/np.sqrt(eps):.3f})x({lo[1]/np.sqrt(eps):.3f},{hi[1]/np.sqrt(eps):.3f})"
              f"  (f*-L)/eps={-L/eps:.5f}")
