"""Check zk_fast.zK_upto2 (vectorized, reduced space) against core.corner_bound (the earlier
note's validated routine) on random corners with rho <= 2: bilinear quadratics embedded in a
larger space with linear variables (a third of them with two antiparallel rays), indefinite
quadratics with one positive eigenvalue, and the cone x^2 - y^2 with two null rays (q constant or
linear along them) and costs spread over 1e-3..1e3.  Disagreements are refereed by a brute-force
theta grid with core.one_ray."""
import sys, numpy as np
import zk_fast as Z
from core import corner_bound, bilinear_quadratic, qval, one_ray


def brute(Q, b, c, sbar, P, w, n=20001):
    """Referee: single rays plus a theta grid on every pair with the exact one-ray root."""
    N = P.shape[1]; best = min(w[j] * one_ray(Q, b, c, sbar, P[:, j]) for j in range(N))
    for i in range(N):
        for j in range(i + 1, N):
            for th in np.linspace(0, 1, n):
                best = min(best, one_ray(Q, b, c, sbar, th / w[i] * P[:, i] + (1 - th) / w[j] * P[:, j]))
    return best

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
T = int(sys.argv[2]) if len(sys.argv) > 2 else 200
worst = 0; nfin = 0; ninf_mis = 0; ndis = 0; worst_fast_vs_brute = 0; n_inf_real = 0
for t in range(T):
    kind = t % 3
    if kind == 2:           # cone x^2 - y^2 (+ optional linear var); rays include null directions of q
        k = int(rng.integers(2, 4))
        Q = np.zeros((k, k)); Q[0, 0], Q[1, 1] = 1.0, -1.0
        b = np.zeros(k); c = 0.0
        if k == 3:
            b[2] = rng.normal()
    elif kind == 0:
        Q3, b3, c3 = bilinear_quadratic('+' if rng.random() < .5 else '-')
        nl = int(rng.integers(0, 3)); k = 3 + nl
        Q = np.zeros((k, k)); Q[:3, :3] = Q3
        b = np.concatenate([b3, rng.normal(size=nl)]); c = float(rng.normal()) * 0.3
    else:
        k = int(rng.integers(2, 5))
        ev = np.concatenate([[rng.uniform(.2, 2)], -rng.uniform(.2, 2, k - 1)])
        U, _ = np.linalg.qr(rng.normal(size=(k, k))); Q = U @ np.diag(ev) @ U.T
        b = rng.normal(size=k); c = float(rng.normal())
    while True:
        sbar = rng.normal(size=k)
        if qval(Q, b, c, sbar) > 0.05: break
    N = int(rng.integers(2, 9)); P = rng.normal(size=(k, N)); w = rng.uniform(0.1, 1, N)
    if t % 3 == 0:          # antiparallel projected rays (occur in SCIP corners)
        P[:, 1] = -rng.uniform(0.3, 3) * P[:, 0]
    if kind == 2:           # two null rays (q linear or constant along them) and badly scaled costs
        P[:, 0] = 0; P[0, 0], P[1, 0] = 1.0, 1.0
        P[:, 1] = 0; P[0, 1], P[1, 1] = 1.0, -1.0
        P[:, :2] *= rng.uniform(0.3, 3, 2)
        w = np.exp(rng.uniform(np.log(1e-3), np.log(1e3), N))
    Qr, br, cr, sr, Pr, rho, npos = Z.reduce_space(Q, b, c, sbar, P)
    assert rho <= 2, rho
    z1, _ = Z.zK_upto2(Qr, br, cr, sr, Pr, w)
    z2 = corner_bound(Q, b, c, sbar, P, w)
    if np.isfinite(z1) and np.isfinite(z2):
        nfin += 1
        rel = abs(z1 - z2) / max(1e-12, abs(z2))
        if rel > 1e-6:
            zb = brute(Q, b, c, sbar, P, w)
            print('DISAGREE instance', t, 'zk_fast', z1, 'core.corner_bound', z2, 'brute-force grid', zb)
            ndis += 1; worst_fast_vs_brute = max(worst_fast_vs_brute, abs(z1 - zb) / zb)
        else:
            worst = max(worst, rel)
    elif np.isfinite(z1) != np.isfinite(z2):
        zb = brute(Q, b, c, sbar, P, w)
        ninf_mis += 1; print('INF MISMATCH', t, 'zk_fast', z1, 'core.corner_bound', z2, 'brute-force grid', zb)
        if np.isfinite(zb) and zb < 1e9:
            n_inf_real += 1
print('instances', T, 'finite', nfin, 'agree (rel <= 1e-6):', nfin - ndis, 'max rel diff among them', worst, 'disagreements', ndis, 'max rel |zk_fast - brute| on disagreements', worst_fast_vs_brute, 'inf mismatches', ninf_mis, 'of which brute-force value < 1e9:', n_inf_real)
