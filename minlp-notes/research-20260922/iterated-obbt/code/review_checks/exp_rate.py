"""Prop. 7: exact iterated OBBT (eps = 0) for x^2 + y^2 + a x y from asymmetric boxes."""
import numpy as np
from obbt2d import Quad, obbt
e = (Quad(1.0), Quad(1.0))
rho = lambda a: (np.sqrt(2*a*a + 4*abs(a)) - abs(a)) / 2
boxes = [((-1, -1.2), (1.3, 1)), ((-0.1, -1), (2, 0.05)), ((-3, -0.01), (0.02, 5)), ((-1, -1), (1, 1))]
for a in [0.5, 1.0, 1.5, 1.9, -1.0]:
    print(f"a={a}  rho={rho(a):.6f}")
    for lo, hi in boxes:
        lo, hi = np.array(lo, float), np.array(hi, float)
        w0 = (hi - lo).max(); logw = 0.0; ratios = []
        K = 400
        for k in range(K):
            s = (hi - lo).max()
            nlo, nhi = obbt(e, a, lo, hi, 0.0)
            ns = (nhi - nlo).max()
            ratios.append(ns / s); logw += np.log(ns / s)
            lo, hi = nlo / ns, nhi / ns   # exact rescaling (zero remainder, eps = 0)
        shape = np.concatenate([-lo, hi])
        print(f"  box {tuple(np.round(-np.array(boxes[0][0]),2)) if False else ''}"
              f" ratio k=10 {ratios[9]:.6f} k=50 {ratios[49]:.6f} k={K} {ratios[-1]:.8f}"
              f"  geo-mean {np.exp(logw/K):.8f}  limit shape (d-,d+) {np.round(shape,4)}")
