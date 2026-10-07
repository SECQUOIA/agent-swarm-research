"""How often does the maximal completion (B) lengthen the steps of the chosen orbit set?
LP corners of the 6x8 McCormick generator (seed 12)."""
import numpy as np, warnings; warnings.filterwarnings('ignore')
import exp_mccormick as E
from core import corner_bound, best_orbit_bound, bilinear_quadratic, Mmat
from bilinear import step_A, step_B, symm, EW, interior_shift
E.rng = np.random.default_rng(12)
cnt = diff = rec = tot = drays = shorter = 0
for trial in range(120):
    I = E.make_instance(6, 8, 4); out = E.solve_lp(I)
    if out is None: continue
    h, A, bb = out; bc = E.basis_cone(I, h, A, bb)
    if bc is None: continue
    x, R, w, Ab, rhs, zlp = bc; p = I['p']
    vmax, e = max((abs(x[p + e] - x[i] * x[j]), e) for e, (i, j) in enumerate(I['pairs']))
    if vmax < 1e-4: continue
    i, j = I['pairs'][e]; idx = [i, j, p + e]; sbar = x[idx]
    side = '+' if sbar[2] > sbar[0] * sbar[1] else '-'
    Q, bq, cq = bilinear_quadratic(side); P = R[idx, :]; wp = np.maximum(w, 1e-9 * w.max())
    zk = corner_bound(Q, bq, cq, sbar, P, wp)
    _, _, F = best_orbit_bound(side, sbar, P, wp, zk, iters=25)
    if F is None: continue
    F = interior_shift(F, side, sbar); cnt += 1
    sg = 1.0 if side == '+' else -1.0
    rec += int(np.linalg.eigvalsh(sg * symm(F.T @ Mmat(side, EW, h=0.0)))[0] >= -1e-12)
    aA = np.array([step_A(F, side, sbar, P[:, k]) for k in range(P.shape[1])])
    aB = np.array([step_B(F, side, sbar, P[:, k]) for k in range(P.shape[1])])
    big = lambda a: np.where(np.isfinite(a), a, 1e300)
    d = ~np.isclose(big(aA), big(aB), rtol=1e-6)
    shorter += int(np.sum(big(aB) < big(aA) * (1 - 1e-6)))
    tot += P.shape[1]; drays += int(d.sum()); diff += int(d.any())
print('corners', cnt, '| e_w recession direction of C_F:', rec, '| corners with a longer (B) step:', diff,
      '| rays with longer (B) step:', drays, 'of', tot, '| rays with SHORTER (B) step (should be 0):', shorter)
