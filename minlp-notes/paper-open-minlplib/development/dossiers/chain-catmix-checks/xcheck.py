"""Dossier cross-check: authors' stage_lb vs verifier's stage/terminal on IDENTICAL inputs
(same N, grid, chord values w). Both must be rigorous lower bounds of the same per-ray minima.
Also compare with dense float sampling (upper estimates of the true minima)."""
import sys, time
import numpy as np
import catmix_bound as A
import catmix_model as cmx
import v_catmix_dp as V

N = int(sys.argv[1]); mode = sys.argv[2]; nst = int(sys.argv[3])
if mode == 'coarse':
    grid = V.make_grid(11)
else:   # fine band near the singular arc, as in the final recheck designs
    grid = V.make_grid(13)
    d = 2.0 ** -21
    grid = np.unique(np.concatenate([grid, np.arange(np.ceil(0.0703 / d) * d, 0.0710, d)]))
assert np.all(grid * 2.0**30 == np.round(grid * 2.0**30))
p, q = 1.0 - grid, grid
m, K = cmx.extract(N)
MA = A.Maps(K); MA.check_positive()
MV = V.Maps(N)

def dense_float(Sflt, w_next, grid_next, terminal=False):
    """float sampling of min_u f(u) on 4001 points + local refinement (upper estimate of true min)."""
    a, b, c, ep, em = (float(eval_frac(K[k])) for k in ("a", "b", "c", "ep", "em"))
    best = np.full(len(grid), np.inf)
    for uu in np.linspace(0.0, 1.0, 4001):
        P = np.array([[1 + a * uu, -b * uu], [-a * uu, ep + c * uu]])
        Q = np.array([[1 - a * uu, b * uu], [a * uu, em - c * uu]])
        Pi = np.linalg.inv(P)
        if terminal:
            y = Pi @ np.vstack([p, q]); val = y[0] + y[1]
        else:
            y = (Q @ Pi) @ np.vstack([p, q]); s = y[0] + y[1]
            val = s * np.interp(y[1] / s, grid_next, w_next)
        best = np.minimum(best, val)
    return best
from fractions import Fraction
def eval_frac(s): return Fraction(s)

t0 = time.time()
wA, incA, stA = A.stage_lb(MA.term, p, q, "sum", 1e-14)
wV, stV = V.terminal(MV, grid)
dn = dense_float(None, None, None, terminal=True)
print("terminal: rays %d  max|wA-wV| %.2e  max(wA-dense) %.2e  max(wV-dense) %.2e  (%.1fs)" % (
    len(grid), np.max(np.abs(wA - wV)), np.max(wA - dn), np.max(wV - dn), time.time() - t0), flush=True)
w = np.maximum(np.minimum(wA, wV), 0.0)
for st in range(nst):
    t0 = time.time()
    ch = A.Chord(p, q, w)
    wA, incA, stA = A.stage_lb(MA.stage, p, q, ch, 1e-14)
    wV, stV = V.stage(MV.stage, grid, w, grid)
    dn = dense_float(None, w, grid)
    print("stage %d: max|wA-wV| %.2e  mean(wV-wA) %.2e  max(wA-dense) %.2e  max(wV-dense) %.2e  (%.1fs)" % (
        st, np.max(np.abs(wA - wV)), np.mean(wV - wA), np.max(wA - dn), np.max(wV - dn), time.time() - t0), flush=True)
    w = np.maximum(np.minimum(wA, wV), 0.0)
