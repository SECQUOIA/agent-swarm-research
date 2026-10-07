"""Numerics for Proposition 16 (the code that produced logs/supp1_cex_numeric.log, run inline)."""
import numpy as np, warnings; warnings.filterwarnings('ignore')
from screen2 import analyze
from core import bilinear_quadratic, orbit_feasible, Mmat
from bilinear import step_A, interior_shift
from scout_sfree import corner_bound_scip, ms_set, ic_bound
Q, b, c = bilinear_quadratic('+')
sb = np.array([-2, 3, 2.]); V = [np.array([0, 0, 0.]), np.array([6, -2, .25]), np.array([1, -2.5, .5])]
P = np.stack([v - sb for v in V], 1); w = np.ones(3)
print('SCIP z_K', corner_bound_scip(Q, b, c, sb, P, w))
G, case = ms_set(Q, b, c, sb); print('SCIP set bound', ic_bound(G, sb, P, w)[0], case)
for z in (0.98, 0.984, 0.99):
    pts = [sb + z * P[:, j] for j in range(3)]
    for sv in ('CLARABEL', 'SCS'):
        F = orbit_feasible('+', [sb], pts, solver=sv)
        ex = min(step_A(interior_shift(F, '+', sb), '+', sb, P[:, j]) for j in range(3)) if F is not None else None
        print('z %.3f %s: %s' % (z, sv, 'infeasible' if F is None else 'feasible, exact bound of returned F %.5f' % ex))
analyze('+', sb, P, w, nm_restarts=20, seed=5)
