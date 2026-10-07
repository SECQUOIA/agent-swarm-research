"""Numerical check of Lemma R (inradius bounds used in the convergence theorem).
For random points sbar in [-3, 3]^3 with q(sbar) > 0 (both sides of w = xy) and random unit
directions d:
  (i) SCIP's Case-4 set (Python model scout_sfree.ms_set) satisfies
      step(d) >= rho_S := q(sbar) / (sqrt(2) (|x_hat(sbar)| + |y_hat(sbar)|));
 (ii) the orbit set C_F with F^T = M(sbar)^{-1} satisfies step(d) >= sigma_min(M(sbar)) and
      sigma_min(M(sbar)) >= q(sbar) / ||M(sbar)||_F.
Usage: python3 check_inradius.py SEED NPOINTS NDIRS"""
import sys
import numpy as np
import mrcore as M
from core import bilinear_quadratic, Mmat
from scout_sfree import ms_set, step_length

seed, NP, ND = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
rng = np.random.default_rng(seed)
worst_s, worst_o, worst_b, n = np.inf, np.inf, np.inf, 0
for _ in range(NP):
    side = '+' if rng.random() < 0.5 else '-'
    Q, b, c = bilinear_quadratic(side)
    while True:
        s = rng.uniform(-3, 3, 3)
        q = float(s @ Q @ s + b @ s + c)
        if q > 1e-3:
            break
    sg = 1.0 if side == '+' else -1.0
    X, Y, W = s
    if side == '+':
        xh = np.array([(X - Y) / 2, (W + 1) / 2]); yh = np.array([(X + Y) / 2, (W - 1) / 2])
    else:
        xh = np.array([(X + Y) / 2, (1 - W) / 2]); yh = np.array([(X - Y) / 2, (-W - 1) / 2])
    assert abs(xh @ xh - yh @ yh - q) < 1e-9 * (1 + abs(q))
    rho = q / (np.sqrt(2) * (np.linalg.norm(xh) + np.linalg.norm(yh)))
    G, _ = ms_set(Q, b, c, s)
    Ms = Mmat(side, s); smin = np.linalg.svd(Ms, compute_uv=False)[-1]
    worst_b = min(worst_b, smin / (q / np.linalg.norm(Ms)))
    F = np.linalg.inv(Ms).T
    D = rng.normal(size=(ND, 3)); D /= np.linalg.norm(D, axis=1)[:, None]
    st = np.array([step_length(G, s, d) for d in D])
    so = M.FO.steps_A(F, side, s, D.T)
    worst_s = min(worst_s, st.min() / rho); worst_o = min(worst_o, so.min() / smin); n += ND
print('directions tested %d' % n)
print('(i)  min step / rho_S over all tests: %.6f (claim >= 1)' % worst_s)
print('(ii) min step / sigma_min(M(sbar)): %.6f (claim >= 1); min sigma_min / (q/||M||_F): %.6f (claim >= 1)' % (worst_o, worst_b))
