"""(0) whether sbar lies in the interior of the set; (1) model_vec 'note' equals scout_sfree.ms_set + step_length (the earlier note's code) on random
corners of all four cases; (2) S-freeness check of the 'note' and 'fixed' Case-4 sets by sampling:
fraction of sampled points of int C (G < 0) with q < 0 (should be 0 for an S-free set)."""
import sys, numpy as np
import model_vec as M
from scip_rule import ms_set, step_length, ms_set_fixed
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
T = int(sys.argv[2]) if len(sys.argv) > 2 else 60
q = lambda Q, b, c, s: s @ Q @ s + b @ s + c
worst = {'note': 0.0, 'fixed': 0.0}; cnt = {1: 0, 2: 0, 3: 0, 4: 0}
viol = {'note': [0, 0], 'fixed': [0, 0]}
notint = {'note': 0, 'fixed': 0}
for t in range(T):
    k = int(rng.integers(2, 5)); kind = t % 4
    ev = rng.uniform(.3, 2, k) * np.where(np.arange(k) < max(1, k // 2), 1, -1)
    if kind == 3:      # zero eigenvalue with linear term -> Case 4
        ev[-1] = 0.0
    U, _ = np.linalg.qr(rng.normal(size=(k, k))); Q = U @ np.diag(ev) @ U.T
    b = rng.normal(size=k); c = float(rng.normal()) * 2
    if kind == 0:      # kappa = 0
        th, V = np.linalg.eigh(Q); bb = V.T @ b; nz = np.abs(th) > 1e-9
        c = 0.25 * np.sum(bb[nz] ** 2 / th[nz])
    while True:
        sbar = rng.normal(size=k) * 2
        if q(Q, b, c, sbar) > 0.05: break
    N = 5; P = rng.normal(size=(k, N))
    for var in ('note', 'fixed'):
        d = M.prepare(Q, b, c, sbar, var)
        a1, g0 = M.steps(d, P)
        if not g0 < 0:
            notint[var] += 1
            print('  instance', t, var, 'case', d['case'], 'kappa %.3f' % d['kappa'], ': sbar not in int C (G(sbar) = %.3g)' % g0)
            continue
        G = (ms_set(Q, b, c, sbar)[0] if var == 'note' else ms_set_fixed(Q, b, c, sbar)[0])
        a2 = np.array([step_length(G, sbar, P[:, j]) for j in range(N)])
        fin = np.isfinite(a1) & np.isfinite(a2)
        assert np.all(np.isfinite(a1) == np.isfinite(a2)), (a1, a2)
        if fin.any():
            worst[var] = max(worst[var], float(np.max(np.abs(a1[fin] - a2[fin]) / np.maximum(1, a2[fin]))))
        if d['case'] == 4 and abs(d['kappa']) > 0.1:
            pts = sbar[:, None] + rng.normal(size=(k, 4000)) * 3
            g = M.gauge(d, pts)
            inside = g < -1e-9
            qq = np.einsum('ij,ik,kj->j', pts, Q, pts) + b @ pts + c
            viol[var][0] += int(np.sum(inside & (qq < -1e-9))); viol[var][1] += int(np.sum(inside))
    cnt[M.setup(Q, b, c, sbar)['case']] += 1
print('cases', cnt)
print('corners with sbar not in the interior of the modelled set:', notint)
print('max |alpha_vec - alpha_ms_set| / max(1, alpha):', worst)
print('Case 4, |kappa| > 0.1: sampled interior points with q < 0 / interior points:', viol)
