"""E9: approximation factor of the CLOSURE of the constant-Gamma (symmetric wedge)
family versus the quadratic corner hull, 2D hyperbolic case (analog of
Averkov-Basu-Paat 2018 for lattice-free families).
closure bound z_fam(w) = min{w^T lam : lam >= 0, a(C)^T lam >= 1 for all C in family}
(computed by an LP over a fine grid of the family), compared with z_K(w)."""
import numpy as np, json
from scipy.optimize import linprog
from sfree import corner_bound, qval
from exp7_sym_worst import U, transform

rng = np.random.default_rng(21)


def cut_coeffs(xy, kappa, sbar, P, gp, gm):
    rk = np.sqrt(kappa)
    x0, y0 = xy(sbar)
    if y0 - (gp[0] * x0 + gp[1] * rk) >= 0 or -y0 - (gm[0] * x0 + gm[1] * rk) >= 0:
        return None
    a = []
    for j in range(P.shape[1]):
        x1, y1 = xy(sbar + P[:, j]); dx, dy = x1 - x0, y1 - y0
        t = np.inf
        s_up = y0 - (gp[0] * x0 + gp[1] * rk); d_up = dy - gp[0] * dx
        s_lo = -y0 - (gm[0] * x0 + gm[1] * rk); d_lo = -dy - gm[0] * dx
        if d_up > 1e-15: t = min(t, -s_up / d_up)
        if d_lo > 1e-15: t = min(t, -s_lo / d_lo)
        a.append(0.0 if not np.isfinite(t) else 1.0 / t)
    return np.array(a)


def closure_bound(cuts, w):
    A = -np.array(cuts); b = -np.ones(len(cuts))
    r = linprog(w, A_ub=A, b_ub=b, bounds=[(0, None)] * len(w), method='highs')
    return r.fun if r.status == 0 else np.inf


if __name__ == '__main__':
    res = []
    while len(res) < 400:
        A = rng.normal(size=(2, 2)); Q = (A + A.T) / 2
        th = np.linalg.eigvalsh(Q)
        if not (th.min() < -0.05 and th.max() > 0.05):
            continue
        b = rng.normal(size=2); c = rng.normal()
        import exp6_asym2d  # noqa (transform)
        xy, kappa = transform(Q, b, c)
        if kappa <= 0.01:
            continue
        sbar = rng.normal(size=2)
        if qval(Q, b, c, sbar) <= 0.01:
            continue
        n = int(rng.integers(2, 4))
        P = rng.normal(size=(2, n)); w = rng.uniform(0.05, 1, n)
        zk = corner_bound(Q, b, c, sbar, P, w)
        if not np.isfinite(zk) or zk <= 0:
            continue
        sym = [a for a in (cut_coeffs(xy, kappa, sbar, P, u, u) for u in U) if a is not None]
        asym = [a for a in (cut_coeffs(xy, kappa, sbar, P, u, v) for u in U[::6] for v in U[::6]
                            if abs(u[0] + v[0]) + abs(u[1] + v[1]) > 1e-9) if a is not None]
        zs = closure_bound(sym, w) if sym else 0.0
        za = closure_bound(asym, w) if asym else 0.0
        res.append((min(zs, zk) / zk, min(za, zk) / zk, n))
    res.sort()
    rs = np.array([r[0] for r in res]); ra = np.array([r[1] for r in res])
    summ = dict(n=len(res), symclosure_min=float(rs.min()), symclosure_q01=float(np.quantile(rs, .01)),
                symclosure_q10=float(np.quantile(rs, .1)), symclosure_mean=float(rs.mean()),
                asymclosure_min=float(ra.min()), asymclosure_mean=float(ra.mean()),
                worst5=[(round(a, 4), round(b_, 4), c_) for a, b_, c_ in res[:5]])
    print(summ)
    json.dump(summ, open('exp9_family_closure.json', 'w'), indent=1)
