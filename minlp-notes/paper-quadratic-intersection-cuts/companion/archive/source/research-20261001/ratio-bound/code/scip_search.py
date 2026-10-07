"""Adversarial search for SCIP's fixed-lambda rule (Case-4 set = upward closure of C_{R_theta})
under nondegeneracy constraints.  usage: python3 scip_search.py SEED RESTARTS D0 KAPPA0 MU0
Minimizes z_SCIP / z_K over (sbar, P) with costs 1, subject to
  D <= D0                       (invariant vertex-depth parameter of Theorem A),
  cond(P~) <= KAPPA0            (P~ = z_K-scaled rays; KAPPA0 <= 0 disables),
  |relative discriminant| >= MU0 for every ray (grazing margin),
  minimizer of z_K unique enough to be computed (z_K finite).
Reports, for the best instance, the SCIP ratio (families A and B), the parabolic-cylinder bound
rho_par (a lower bound on the orbit ratio), D, cond, margins."""
import sys
import json
import numpy as np
import warnings
from scipy.optimize import minimize
import rb

warnings.filterwarnings('ignore')


def build(th):
    sbar = np.array([th[0], th[1], th[0] * th[1] + np.exp(th[2])])
    P = th[3:12].reshape(3, 3)
    return sbar, P


def measures(sbar, P):
    c = np.ones(3)
    z, lam = rb.zK(sbar, P, c)
    if not np.isfinite(z) or z <= 0:
        return None
    Pt = rb.scaled_rays(P, c, z)
    qb = rb.q(sbar)
    disc = []
    for j in range(3):
        p = Pt[:, j]
        A_ = -p[0] * p[1]
        B_ = rb.grad(sbar) @ p
        disc.append((B_ * B_ - 4 * A_ * qb) / (B_ * B_ + abs(4 * A_ * qb)))
    return dict(z=z, Pt=Pt, D=rb.D_inv(sbar, Pt), cond=np.linalg.cond(Pt), mu=min(abs(d) for d in disc), disc=disc)


def objective(th, D0, K0, MU0):
    sbar, P = build(th)
    if abs(np.linalg.det(P)) < 1e-9 * (1 + np.abs(P).max() ** 3):
        return 2.0
    m = measures(sbar, P)
    if m is None or m['D'] > D0 or m['mu'] < MU0 or (K0 > 0 and m['cond'] > K0):
        return 2.0
    try:
        return rb.scip_ratio(sbar, m['Pt'], 'B')
    except Exception:
        return 2.0


if __name__ == '__main__':
    seed, restarts = int(sys.argv[1]), int(sys.argv[2])
    D0, K0, MU0 = float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
    rng = np.random.default_rng(seed)
    best = (2.0, None)
    for rs in range(restarts):
        for _ in range(5000):
            th = np.concatenate([rng.normal(size=2) * 3, [rng.normal() * 2], rng.normal(size=9)])
            f0 = objective(th, D0, K0, MU0)
            if f0 < 1.5:
                break
        else:
            continue
        res = minimize(objective, th, args=(D0, K0, MU0), method='Nelder-Mead',
                       options=dict(maxiter=3000, xatol=1e-9, fatol=1e-10))
        sbar, P = build(res.x)
        m = measures(sbar, P)
        out = dict(restart=rs, start=f0, scipB=res.fun, theta=res.x.tolist())
        if m is not None and res.fun < 1.5:
            out.update(scipA=rb.scip_ratio(sbar, m['Pt'], 'A'), rho_par=rb.rho_par(sbar, m['Pt'])[0], D=m['D'],
                       cond=m['cond'], mu=m['mu'], sbar=sbar.tolist())
        print(json.dumps(out), flush=True)
        if res.fun < best[0]:
            best = (res.fun, res.x)
    print('BEST', best[0])
