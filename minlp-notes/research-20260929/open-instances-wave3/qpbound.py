"""Rigorous third-order lower bound over boxes from center gradient/Hessian enclosures
and a box Hessian enclosure (shared by the ANN code; same mathematics as
kan_bb.Net._hess_bound).

For f in C^2 on the box X = c + [a, b] (a <= 0 <= b):
  f(c+d) = f(c) + g.d + d^T H(xi) d / 2,  g = grad f(c) in [gl, gh],  H(xi) in [HbL, HbH].
With a symmetric float matrix Hm (midpoint of the center Hessian enclosure),
  f(c+d) >= f(c) + gm.d + d^T Hm d / 2 - sum_i grad_rad_i r_i - r^T R r / 2,
  R >= |H(xi) - Hm| entrywise.  If Hm is positive definite (proved by Gershgorin on
  V^T Hm V, V = float eigenvectors: congruence preserves inertia), the convex quadratic
  q(d) = gm.d + d^T Hm d/2 satisfies q(d) >= q(y) + (gm + Hm y).(d - y) for any y, and the
  right side is minimized over the box in closed form (interval arithmetic).
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../..'))
import sys

import numpy as np

sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave3/kan")
from kan_iv import NI, dn, up  # noqa: E402


def ivmatmul3(V, Hm):
    n = V.shape[1]
    g = (2 * n + 2) * 2.0 ** -53 / (1 - (2 * n + 2) * 2.0 ** -53)
    T = np.einsum("nki,nkl->nil", V, Hm)
    Terr = g * np.einsum("nki,nkl->nil", np.abs(V), np.abs(Hm))
    B = np.einsum("nil,nlj->nij", T, V)
    Berr = g * np.einsum("nil,nlj->nij", np.abs(T), np.abs(V)) + np.einsum("nil,nlj->nij", Terr, np.abs(V)) * (1 + 2 * g)
    Berr = up(Berr * (1 + 1e-12)) + 1e-300
    return dn(B - Berr), up(B + Berr)


def third_order_bound(fclo, gl, gh, HcL, HcH, HbL, HbH, a, b):
    """fclo (N,), gl/gh (N,d), HcL/HcH/HbL/HbH (N,d,d), a/b (N,d) with a <= 0 <= b.
    Returns rigorous lower bounds (N,) (-inf where the PD test fails)."""
    N, d = gl.shape
    out = np.full(N, -np.inf)
    Hm = 0.5 * (HcL + HcH)
    Hm = 0.5 * (Hm + np.transpose(Hm, (0, 2, 1)))
    if not np.all(np.isfinite(Hm)):
        bad = ~np.all(np.isfinite(Hm), axis=(1, 2))
        Hm = np.where(bad[:, None, None], np.eye(d)[None], Hm)
    else:
        bad = np.zeros(N, bool)
    R = up(np.maximum(np.abs(up(HbH - Hm)), np.abs(up(Hm - HbL))))
    gm = 0.5 * (gl + gh)
    grad_rad = up(np.maximum(gh - gm, gm - gl))
    r = np.maximum(-a, b)
    try:
        w, V = np.linalg.eigh(Hm)
    except np.linalg.LinAlgError:
        return out
    Blo, Bhi = ivmatmul3(V, Hm)
    offmax = np.maximum(np.abs(Blo), np.abs(Bhi))
    idx = np.arange(d)
    offmax[:, idx, idx] = 0.0
    gersh = dn(Blo[:, idx, idx] - up(offmax.sum(axis=2) * (1 + 1e-15)))
    pd = np.all(gersh > 0, axis=1) & ~bad
    if not pd.any():
        return out
    with np.errstate(all="ignore"):
        Hs = np.where(pd[:, None, None], Hm, np.eye(d)[None])
        y = -np.linalg.solve(Hs, gm[:, :, None])[:, :, 0]
    y = np.where(np.isfinite(y), y, 0.0)
    y = np.clip(y, a, b)
    diag = np.maximum(Hm[:, idx, idx], 1e-300)
    for _ in range(30):
        for i in range(d):
            gi = gm[:, i] + np.einsum("nk,nk->n", Hm[:, i, :], y) - Hm[:, i, i] * y[:, i]
            y[:, i] = np.clip(-gi / diag[:, i], a[:, i], b[:, i])
    Y = NI(y)
    Hq = NI(Hm)
    HY = None
    for k in range(d):
        t = Hq[:, :, k] * Y[:, k:k + 1]
        HY = t if HY is None else HY + t
    rho = HY + NI(gm)
    qy = None
    for i in range(d):
        t = Y[:, i] * (NI(gm[:, i]) + HY[:, i] * 0.5)
        qy = t if qy is None else qy + t
    lin = qy
    for i in range(d):
        lin = lin + rho[:, i] * (NI(a[:, i], b[:, i]) - Y[:, i])
    pen = (grad_rad * r).sum(axis=1) + 0.5 * np.einsum("ni,nik,nk->n", r, R, r)
    pen = up(pen * (1 + 1e-12)) + 1e-300
    val = dn(dn(fclo + lin.lo) - pen)
    return np.where(pd, val, -np.inf)
