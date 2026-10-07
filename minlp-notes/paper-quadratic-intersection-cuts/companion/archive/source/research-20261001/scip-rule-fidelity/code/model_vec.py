"""Vectorized step lengths of the modelled SCIP set along many rays.

For S = {s^T Q s + b^T s + c <= 0} and sbar with q(sbar) > 0, build the Chmiela-Munoz-Serrano
set with SCIP's lambda rule (lambda = xhat(sbar)/||xhat(sbar)||) and return, for each ray p_j,
alpha_j = sup{t >= 0 : G(sbar + t p_j) <= 0} by bisection (G convex along the ray, G(sbar) < 0).

variant 'note' : Case 4 as in scout_sfree.ms_set (x and y divided by (1+kappa^2)^(1/4), the extra
                 coordinate by 2 (1+kappa^2)^(1/4); not a positive multiple of q unless kappa = 0);
variant 'fixed': Case 4 as in SCIP's code (x, y unscaled; extra coordinate (w+kappa+-r)/(2 sqrt r)).
Cases 1-3 are identical in both.  amax: steps with G(sbar + amax p) <= 0 are reported as inf
(scout_sfree.step_length uses amax = 1e7).
"""
import numpy as np


def setup(Q, b, c, sbar, variant='fixed', eigtol=1e-9):
    k = len(sbar)
    th, V = np.linalg.eigh(Q)
    bb = V.T @ b
    Ip = th > eigtol
    Im = th < -eigtol
    I0 = ~(Ip | Im)
    kappa = c - 0.25 * np.sum(bb[Ip | Im] ** 2 / th[Ip | Im])
    bI0 = bb[I0]
    case4 = bI0.size > 0 and np.linalg.norm(bI0) > 1e-12
    if not case4:
        if abs(kappa) < 1e-12:
            cs = 1
        elif kappa > 0:
            cs = 2
        else:
            cs = 3
    else:
        cs = 4
    d = dict(th=th, V=V, bb=bb, Ip=Ip, Im=Im, I0=I0, kappa=kappa, bI0=bI0, case=cs, variant=variant)
    return d


def _xyw(d, S):
    """S: (k, M) points -> x (p+, M), y (p-, M), w (M,)."""
    psi = d['V'].T @ S
    th, bb = d['th'], d['bb']
    Ip, Im, I0 = d['Ip'], d['Im'], d['I0']
    x = np.sqrt(th[Ip])[:, None] * (psi[Ip] + (bb[Ip] / (2 * th[Ip]))[:, None])
    y = np.sqrt(-th[Im])[:, None] * (psi[Im] + (bb[Im] / (2 * th[Im]))[:, None])
    w = d['bI0'] @ psi[I0] if d['case'] == 4 else np.zeros(S.shape[1])
    return x, y, w


def gauge(d, S, lam=None):
    """G at points S (k, M); lam computed from sbar via d['lam'] (set by prepare)."""
    x, y, w = _xyw(d, S)
    kappa, cs = d['kappa'], d['case']
    L = d['lam']
    if cs == 1:
        return np.linalg.norm(y, axis=0) - L @ x
    if cs == 2:
        return np.linalg.norm(y, axis=0) - (L[:-1] @ x + L[-1] * np.sqrt(kappa))
    if cs == 3:
        return np.sqrt(np.sum(y ** 2, 0) - kappa) - L @ x
    r = np.sqrt(1 + kappa ** 2); f = np.sqrt(r)
    sx = f if d['variant'] == 'note' else 1.0
    xh = np.vstack([x / sx, (w + kappa + r) / (2 * f)])
    yh = np.vstack([y / sx, (w + kappa - r) / (2 * f)])
    lt = L[-1]
    ny = np.linalg.norm(yh, axis=0)
    phi_a = ny
    phi_b = np.sqrt(np.maximum(0.0, (1 - lt ** 2) * (ny ** 2 - yh[-1] ** 2))) + lt * yh[-1]
    phi = np.where(-lt * ny + yh[-1] <= 0, phi_a, phi_b)
    return phi - L @ xh


def prepare(Q, b, c, sbar, variant='fixed'):
    d = setup(Q, b, c, sbar, variant)
    x, y, w = _xyw(d, sbar[:, None])
    x = x[:, 0]; w = w[0]
    kappa, cs = d['kappa'], d['case']
    if cs in (1, 3):
        L = x / np.linalg.norm(x)
    elif cs == 2:
        v = np.append(x, np.sqrt(kappa)); L = v / np.linalg.norm(v)
    else:
        r = np.sqrt(1 + kappa ** 2); f = np.sqrt(r)
        sx = f if variant == 'note' else 1.0
        xh = np.append(x / sx, (w + kappa + r) / (2 * f)); L = xh / np.linalg.norm(xh)
    d['lam'] = L
    d['sbar'] = sbar
    return d


def steps(d, P, amax=1e7, iters=200):
    sbar = d['sbar']
    N = P.shape[1]
    g0 = gauge(d, sbar[:, None])[0]
    alpha = np.full(N, np.inf)
    if not g0 < 0:
        return np.full(N, np.nan), g0
    nz = np.linalg.norm(P, axis=0) > 1e-14
    far = gauge(d, sbar[:, None] + amax * P)
    fin = nz & (far > 0)
    idx = np.where(fin)[0]
    if idx.size:
        lo = np.zeros(idx.size); hi = np.ones(idx.size)
        Pi = P[:, idx]
        for _ in range(200):                       # bracket
            g = gauge(d, sbar[:, None] + hi * Pi)
            m = g <= 0
            if not m.any():
                break
            lo = np.where(m, hi, lo); hi = np.where(m, 2 * hi, hi)
        for _ in range(iters):
            mid = 0.5 * (lo + hi)
            g = gauge(d, sbar[:, None] + mid * Pi)
            m = g <= 0
            lo = np.where(m, mid, lo); hi = np.where(m, hi, mid)
        alpha[idx] = lo
    return alpha, g0
