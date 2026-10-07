"""Tangent-edge screen for families (A) and (B) on stored instances."""
import json, sys, numpy as np, warnings; warnings.filterwarnings('ignore')
from core import bilinear_quadratic, corner_bound, qval, best_orbit_bound
from bilinear import kappa_pencil, kappa_set_A, kappa_ok_B, bound
from scipy.optimize import minimize


def analyze(side, sbar, P, w, nm_restarts=20, seed=0, verbose=True):
    rng = np.random.default_rng(seed)
    Q, b, c = bilinear_quadratic(side)
    zk, lam = corner_bound(Q, b, c, sbar, P, w, return_point=True)
    supp = np.flatnonzero(lam > 1e-9)
    out = dict(zK=zk, support=supp.tolist())
    if len(supp) == 2:
        i, j = supp
        t0 = sbar + P @ lam
        V = [sbar + zk / w[k] * P[:, k] for k in range(P.shape[1])]
        G0, G1 = kappa_pencil(side, t0, V[i] - V[j])
        ivs = [kappa_set_A(G0, G1, side, v) for v in [sbar] + V]
        lo = max(iv[0] if iv else np.inf for iv in ivs); hi = min(iv[1] if iv else -np.inf for iv in ivs)
        out['A_kappa_sets'] = [None if iv is None else [float(iv[0]), float(iv[1])] for iv in ivs]
        out['A_kappa_feasible'] = bool(lo <= hi)
        kg = np.concatenate([-np.logspace(6, -6, 1500), [0.0], np.logspace(-6, 6, 1500)])
        okB = np.array([all(kappa_ok_B(G0, G1, side, v, k) for v in [sbar] + V) for k in kg])
        out['B_kappa_grid_feasible'] = bool(okB.any())
        if okB.any():
            out['B_kappa_range'] = [float(kg[okB].min()), float(kg[okB].max())]
    cert, hiA, F = best_orbit_bound(side, sbar, P, w, zk, iters=35)
    out['A_best_cert'] = cert / zk; out['A_bisect_hi'] = hiA / zk
    best = cert
    starts = [F] if F is not None else []
    for r in range(nm_restarts):
        F0 = rng.normal(size=(2, 2))
        if np.linalg.det(F0) < 0: F0[:, 0] *= -1
        starts.append(F0)
    for F0 in starts:
        f = lambda x: -min(bound(x.reshape(2, 2), side, sbar, P, w, 'B'), 1e9) if np.linalg.det(x.reshape(2, 2)) > 0 else 0.0
        res = minimize(f, F0.ravel(), method='Nelder-Mead', options=dict(maxiter=500, xatol=1e-10, fatol=1e-12))
        best = max(best, -res.fun)
    out['B_best_found'] = best / zk
    if verbose:
        print(json.dumps(out))
    return out


if __name__ == '__main__':
    inst = json.load(open('../logs/supp2_instances.json'))
    for I in inst:
        print('instance', I['id'], end=' ')
        analyze(I['side'], np.array(I['sbar']), np.array(I['P']), np.array(I['w']))
