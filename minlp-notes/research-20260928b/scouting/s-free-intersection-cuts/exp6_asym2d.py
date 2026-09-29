"""E6 (k = 2, 'case 2' hyperbola S = {y^2 >= x^2 + kappa} in eigen-coordinates).
All maximal S-free sets are C(g+, g-) = {y <= g+ . (x, sqrt k), -y <= g- . (x, sqrt k)}
with g+-, unit, second component >= 0, g+ != -g-  (Munoz-Paat-Serrano 2026, Thm 5).
Compare: SCIP default (g+ = g- = (xbar, sqrt k)/norm), best symmetric (g+ = g-),
best asymmetric, and the exact corner bound z_K."""
import numpy as np, json
from sfree import corner_bound, step_length, qval

rng = np.random.default_rng(11)


def transform(Q, b, c):
    th, V = np.linalg.eigh(Q)
    bb = V.T @ b
    ip, im = int(np.argmax(th)), int(np.argmin(th))
    kappa = c - 0.25 * (bb[ip] ** 2 / th[ip] + bb[im] ** 2 / th[im])

    def xy(s):
        psi = V.T @ s
        return (np.sqrt(th[ip]) * (psi[ip] + bb[ip] / (2 * th[ip])),
                np.sqrt(-th[im]) * (psi[im] + bb[im] / (2 * th[im])))
    return xy, kappa


def zset(xy, kappa, sbar, P, w, gp, gm):
    rk = np.sqrt(kappa)
    G = lambda s: max(xy(s)[1] - (gp[0] * xy(s)[0] + gp[1] * rk), -xy(s)[1] - (gm[0] * xy(s)[0] + gm[1] * rk))
    if G(sbar) >= -1e-12:
        return 0.0
    al = [step_length(G, sbar, P[:, j]) for j in range(P.shape[1])]
    vals = [w[j] * al[j] for j in range(len(w)) if np.isfinite(al[j])]
    return min(vals) if vals else 1e9


angles = np.linspace(0, np.pi, 181)  # second component >= 0
U = np.stack([np.cos(angles), np.sin(angles)], 1)
if __name__ == '__main__':
    res = []
    while len(res) < 60:
        A = rng.normal(size=(2, 2)); Q = (A + A.T) / 2
        th = np.linalg.eigvalsh(Q)
        if not (th.min() < -0.05 and th.max() > 0.05):
            continue
        b = rng.normal(size=2); c = rng.normal()
        xy, kappa = transform(Q, b, c)
        if kappa <= 0.01:
            continue
        sbar = rng.normal(size=2)
        if qval(Q, b, c, sbar) <= 0.01:
            continue
        n = rng.integers(2, 5)
        P = rng.normal(size=(2, n)); w = rng.uniform(0.1, 1, n)
        zk = corner_bound(Q, b, c, sbar, P, w)
        if not np.isfinite(zk):
            continue
        xb, yb = xy(sbar)
        g0 = np.array([xb, np.sqrt(kappa)]); g0 /= np.linalg.norm(g0)
        zdef = zset(xy, kappa, sbar, P, w, g0, g0)
        zsym = max(zset(xy, kappa, sbar, P, w, u, u) for u in U)
        zasym = max(zset(xy, kappa, sbar, P, w, u, v) for u in U[::3] for v in U[::3])
        rec = dict(n=int(n), default=min(zdef, zk) / zk, best_sym=min(zsym, zk) / zk, best_asym=min(zasym, zk) / zk)
        res.append(rec)
        print({k: round(v, 4) if isinstance(v, float) else v for k, v in rec.items()}, flush=True)
    d = np.array([r['default'] for r in res]); s = np.array([r['best_sym'] for r in res]); a = np.array([r['best_asym'] for r in res])
    summ = dict(n=len(res), default_mean=float(d.mean()), sym_mean=float(s.mean()), asym_mean=float(a.mean()),
                default_min=float(d.min()), sym_min=float(s.min()), asym_min=float(a.min()),
                frac_sym_opt=float(np.mean(s > 0.999)), frac_asym_opt=float(np.mean(a > 0.99)),
                frac_asym_beats_sym_by_5pct=float(np.mean(a > s * 1.05)))
    print('SUMMARY', summ)
    json.dump(dict(summary=summ, records=res), open('exp6_asym2d.json', 'w'), indent=1)
