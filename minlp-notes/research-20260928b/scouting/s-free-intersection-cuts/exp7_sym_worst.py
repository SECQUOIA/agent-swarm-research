"""E7: 2D hyperbolic case, closed-form step lengths.  Adversarial search for the
worst ratio (best symmetric wedge bound)/(corner bound z_K), and check that the
best asymmetric wedge attains z_K (sufficiency of the full MPS family)."""
import numpy as np, json
from sfree import corner_bound, qval
from exp6_asym2d import transform

rng = np.random.default_rng(12)
ang = np.linspace(0, np.pi, 541)
U = np.stack([np.cos(ang), np.sin(ang)], 1)          # candidate g's (unit, g2 >= 0)


def bounds_all(xy, kappa, sbar, P, w):
    rk = np.sqrt(kappa)
    x0, y0 = xy(sbar)
    n = P.shape[1]
    # exit parameter through the upper line (y <= g.(x, rk)) and lower line (-y <= g.(x, rk)) per g and ray
    up = np.full((len(U), n), np.inf); lo = np.full((len(U), n), np.inf)
    for j in range(n):
        x1, y1 = xy(sbar + P[:, j])
        dx, dy = x1 - x0, y1 - y0
        s_up = y0 - (U[:, 0] * x0 + U[:, 1] * rk); d_up = dy - U[:, 0] * dx
        s_lo = -y0 - (U[:, 0] * x0 + U[:, 1] * rk); d_lo = -dy - U[:, 0] * dx
        with np.errstate(divide='ignore', invalid='ignore'):
            up[:, j] = np.where(d_up > 1e-15, -s_up / d_up, np.inf)
            lo[:, j] = np.where(d_lo > 1e-15, -s_lo / d_lo, np.inf)
    int_up = y0 - (U[:, 0] * x0 + U[:, 1] * rk) < 0
    int_lo = -y0 - (U[:, 0] * x0 + U[:, 1] * rk) < 0
    # symmetric: g+ = g- = u
    al = np.minimum(up, lo)
    zs = np.where(np.isfinite(al), al * w[None, :], np.inf).min(1)
    zs = np.where(int_up & int_lo, np.minimum(zs, 1e9), 0.0)
    # asymmetric: g+ = U[a], g- = U[b]
    alA = np.minimum(up[:, None, :], lo[None, :, :])
    zA = np.where(np.isfinite(alA), alA * w[None, None, :], np.inf).min(2)
    ok = int_up[:, None] & int_lo[None, :]
    anti = np.abs(U[:, None, 0] + U[None, :, 0]) + np.abs(U[:, None, 1] + U[None, :, 1]) < 1e-12
    zA = np.where(ok & ~anti, np.minimum(zA, 1e9), 0.0)
    return zs.max(), zA.max()


if __name__ == '__main__':
    worst = []
    cnt = 0
    while cnt < 1200:
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
        n = int(rng.integers(2, 4))
        P = rng.normal(size=(2, n)); w = rng.uniform(0.05, 1, n)
        zk = corner_bound(Q, b, c, sbar, P, w)
        if not np.isfinite(zk) or zk <= 0:
            continue
        cnt += 1
        zs, za = bounds_all(xy, kappa, sbar, P, w)
        worst.append((min(zs, zk) / zk, min(za, zk) / zk, n))
    worst.sort()
    rs = np.array([r[0] for r in worst]); ra = np.array([r[1] for r in worst])
    summ = dict(n=len(worst), sym_min=float(rs.min()), sym_q01=float(np.quantile(rs, .01)),
                sym_q10=float(np.quantile(rs, .1)), sym_mean=float(rs.mean()),
                asym_min=float(ra.min()), asym_q01=float(np.quantile(ra, .01)), asym_mean=float(ra.mean()),
                worst10=[(round(a, 4), round(b, 4), c) for a, b, c in worst[:10]])
    print(summ)
    json.dump(summ, open('exp7_sym_worst.json', 'w'), indent=1)
