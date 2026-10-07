"""Exactness at a support-one contact point (Theorem C of the note).

If the unique corner minimizer t* is a vertex of T* (support one) and every edge of T* at t*
is transversal (h_v = grad q(t*)^T (v - t*) > 0 for the other vertices v), the orbit sets
(family A) containing t* are exactly C_{alpha,beta}: in coordinates centred at t*,
  C_{alpha,beta} = {w >= 0, 1 + beta x >= 0, 4 alpha w (1 + beta x) >= (alpha x + y + beta w)^2},
alpha > 0, beta real (F^T = [[alpha, 0], [beta, 1]]).  A point v = t* + (x, y, h) with q(v) = h - x y
lies in C_{alpha,beta} iff beta lies in
  I_v(alpha) = [(alpha x - y - 2 sqrt(alpha q(v)))/h, (alpha x - y + 2 sqrt(alpha q(v)))/h].
So family A attains z_K iff for some alpha the intervals of all vertices other than t* meet,
with beta in the interior of I_sbar.  beta = 0 is the parabolic cylinder (criterion H_cyl >= 1).
For family (B) a vertex may be lowered: I_v^B(alpha) is the union of the intervals of the points
t* + (x, y, h') over h' in (max(xy, 0), h].
"""
import numpy as np
import rb


def centred(sbar, P, c, z, lam):
    """Data of the vertices other than t*: arrays x, y, h, qv; index 0 is sbar."""
    tstar = sbar + P @ lam
    g = rb.grad(tstar)
    verts = [sbar] + [sbar + (z / c[j]) * P[:, j] for j in range(P.shape[1]) if lam[j] <= 1e-12]
    U = np.array([v - tstar for v in verts])
    return U[:, 0], U[:, 1], U @ g, np.array([rb.q(v) for v in verts]), tstar, U


def intervals_A(alpha, x, y, h, qv):
    r = 2.0 * np.sqrt(alpha * np.maximum(qv, 0.0))
    return (alpha * x - y - r) / h, (alpha * x - y + r) / h


def gap_A(alpha, x, y, h, qv):
    """max left - min right (<= 0 iff the closed intervals meet); also the strict version for sbar."""
    lo, hi = intervals_A(alpha, x, y, h, qv)
    return lo.max() - hi.min()


def intervals_B(alpha, x, y, h, qv, ngrid=400):
    lo = np.empty(len(x))
    hi = np.empty(len(x))
    for i in range(len(x)):
        wmin = max(x[i] * y[i], 0.0)
        ws = wmin + (h[i] - wmin) * np.concatenate([np.logspace(-9, 0, ngrid)])
        qs = ws - x[i] * y[i]
        r = 2.0 * np.sqrt(alpha * np.maximum(qs, 0.0))
        L = (alpha * x[i] - y[i] - r) / ws
        Rr = (alpha * x[i] - y[i] + r) / ws
        lo[i], hi[i] = L.min(), Rr.max()
    return lo, hi


def gap_B(alpha, x, y, h, qv):
    lo, hi = intervals_B(alpha, x, y, h, qv)
    return lo.max() - hi.min()


def min_gap(gapf, x, y, h, qv, ngrid=2001):
    ts = np.exp(np.linspace(-10, 10, ngrid))
    vals = np.array([gapf(t * t, x, y, h, qv) for t in ts])
    k = int(np.argmin(vals))
    lo, hi = np.log(ts[max(k - 1, 0)]), np.log(ts[min(k + 1, ngrid - 1)])
    gr = (np.sqrt(5) - 1) / 2
    f = lambda u: gapf(np.exp(2 * u), x, y, h, qv)
    for _ in range(100):
        m1, m2 = hi - gr * (hi - lo), lo + gr * (hi - lo)
        if f(m1) <= f(m2):
            hi = m2
        else:
            lo = m1
    u = 0.5 * (lo + hi)
    return (f(u), np.exp(u)) if f(u) <= vals[k] else (vals[k], ts[k])


def H_cyl(x, y, h):
    """max_t min_v 4 h_v / (t x_v + y_v / t)^2  (>= 1: the cylinder certifies exactness)."""
    ts = np.exp(np.linspace(-10, 10, 4001))
    best, tb = -1.0, None
    for t in ts:
        b = (t * x + y / t) ** 2
        with np.errstate(divide='ignore'):
            v = np.where(b > 0, 4 * h / np.where(b > 0, b, 1), np.inf).min()
        if v > best:
            best, tb = v, t
    return best, tb


def H_crude(x, y, h):
    """min_v h_v / (max|x| max|y|)  (>= 1 implies H_cyl >= 1)."""
    return float(h.min() / (np.abs(x).max() * np.abs(y).max()))


def analyze(sbar, P, c):
    z, lam = rb.zK(sbar, P, c)
    if (lam > 1e-12).sum() != 1:
        return None
    x, y, h, qv, tstar, U = centred(sbar, P, c, z, lam)
    if h.min() <= 0:
        return None
    gA, aA = min_gap(gap_A, x, y, h, qv)
    gB, aB = min_gap(gap_B, x, y, h, qv, ngrid=401)
    hc, tc = H_cyl(x, y, h)
    return dict(zK=z, tstar=tstar.tolist(), gapA=float(gA), alphaA=float(aA), gapB=float(gB),
                Hcyl=float(hc), tcyl=float(tc), Hcrude=H_crude(x, y, h),
                cos_edges=[float(hh / (np.linalg.norm(rb.grad(tstar)) * np.linalg.norm(u))) for hh, u in zip(h, U)],
                min_q_rel=float(qv.min() / qv.max()))
