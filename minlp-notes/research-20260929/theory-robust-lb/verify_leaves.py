"""Independent check of pruned leaves.  For each leaf, the B&B claims a lower bound lo = sum_e min_{A_e}
(shifted factor e) >= f* - eps, computed from polynomial critical points.  Here each factor minimum is
re-estimated independently (301x301 grid, then bounded L-BFGS-B from the 10 best grid points); if the
independent estimate is below the claimed minimum, the claimed bound was too high.  Reports the largest
excess  lo - sum_e (independent min)  (should be <= ~1e-9) and checks that the shifted factors still sum
to f (the split is a split).  Usage: python3 verify_leaves.py G CLS EPS"""
import sys
import numpy as np
from scipy.optimize import minimize
from robust_bb import gadget_chain, bb

G, cls, eps = int(sys.argv[1]), sys.argv[2], float(sys.argv[3])
fam = gadget_chain(G)
rec = []
r = bb(fam, cls, eps, record=rec)
print("B&B:", r, flush=True)
M = 301
excess = -np.inf; worst_tel = 0.0; minlo = np.inf
rng = np.random.default_rng(1)
for (l, u, split, lo) in rec:
    tot = 0.0
    for (A, B, bb_, lx, ux, ly, uy) in split:
        xs = np.linspace(lx, ux, M); ys = np.linspace(ly, uy, M)
        X, Y = np.meshgrid(xs, ys, indexing="ij")
        V = A(X.ravel()).reshape(X.shape) + B(Y.ravel()).reshape(Y.shape) + bb_ * X * Y
        best = V.min()
        fun = lambda p: float(A(np.array([p[0]]))[0] + B(np.array([p[1]]))[0] + bb_ * p[0] * p[1])
        for k in np.argsort(V.ravel())[:10]:
            p0 = [X.ravel()[k], Y.ravel()[k]]
            res = minimize(fun, p0, method="L-BFGS-B", bounds=[(lx, ux), (ly, uy)])
            best = min(best, res.fun)
        tot += best
    excess = max(excess, lo - tot)
    minlo = min(minlo, lo)
    for _ in range(3):
        x = rng.uniform(l, u)
        s = sum(A(np.array([x[e]]))[0] + B(np.array([x[e + 1]]))[0] + bb_ * x[e] * x[e + 1]
                for e, (A, B, bb_, *_rest) in enumerate(split))
        worst_tel = max(worst_tel, abs(s - fam.f(x)))
print("leaves checked: %d; min claimed bound %.3e (target %.1e); max excess of claimed bound over "
      "independent estimate %.2e; max split error %.1e" % (len(rec), minlo, -eps, excess, worst_tel))
