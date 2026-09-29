"""Numerical mixed-integer halfspace depth for n = 1, d = 2.

S = C ∩ (Z x R^2) is represented by its fibers C_j (convex polygons) at
integer heights j = 0..m.  The depth of (k, y) is

  h(k, y) = inf over closed halfspaces H containing (k, y) of
            sum_j area(C_j ∩ H_j),

where H_j = {x : a.x >= a.y - b (j - k)} for normal (b, a), |a| = 1, plus the
"horizontal" halfspaces (a = 0) which give sum_{j>=k} or sum_{j<=k}.
The limits b -> +-inf with a != 0 give sum_{j>k} v_j + area(C_k ∩ {a.x>=a.y})
(and the mirror), which are included explicitly.

Numerics: grid over (theta, b) then local refinement.  The computed depth is
an upper bound on the true depth up to refinement error (it is a min over
finitely many halfspaces, each evaluated exactly).
"""

import numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import minimize


def hull2(P):
    P = np.asarray(P, float)
    if len(P) < 3:
        return None
    try:
        h = ConvexHull(P)
    except Exception:
        return None
    V = P[h.vertices]
    # ConvexHull in 2D returns vertices in counterclockwise order
    return V


def poly_area(V):
    x, y = V[:, 0], V[:, 1]
    return 0.5 * np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y)


def clip_area(V, A, T):
    """Area of convex CCW polygon V intersected with {x : A_i . x >= T_i}.

    A: (N,2), T: (N,). Returns (N,) areas."""
    S = A @ V.T - T[:, None]  # (N, m)
    Vn = np.roll(V, -1, axis=0)
    Sn = np.roll(S, -1, axis=1)
    inside = S >= 0
    insn = Sn >= 0
    # parameter of crossing along edge
    with np.errstate(divide="ignore", invalid="ignore"):
        lam = S / (S - Sn)
    lam = np.where(np.isfinite(lam), lam, 0.0)
    Px = V[None, :, 0] + lam * (Vn[None, :, 0] - V[None, :, 0])
    Py = V[None, :, 1] + lam * (Vn[None, :, 1] - V[None, :, 1])
    cross_full = V[:, 0] * Vn[:, 1] - Vn[:, 0] * V[:, 1]  # (m,)
    both = inside & insn
    exit_ = inside & ~insn
    entry = ~inside & insn
    contrib = np.where(both, cross_full[None, :], 0.0)
    # exit edge: from v_i to P
    contrib += np.where(exit_, V[None, :, 0] * Py - Px * V[None, :, 1], 0.0)
    # entry edge: from P to v_{i+1}
    contrib += np.where(entry, Px * Vn[None, :, 1] - Vn[None, :, 0] * Py, 0.0)
    ex_x = np.sum(np.where(exit_, Px, 0.0), axis=1)
    ex_y = np.sum(np.where(exit_, Py, 0.0), axis=1)
    en_x = np.sum(np.where(entry, Px, 0.0), axis=1)
    en_y = np.sum(np.where(entry, Py, 0.0), axis=1)
    has = np.any(exit_, axis=1)
    closing = np.where(has, ex_x * en_y - en_x * ex_y, 0.0)
    return 0.5 * (contrib.sum(axis=1) + closing)


def slice_polytope(P3):
    """Given points in R^3 (z first), return fibers at integer z of conv(P3)."""
    P3 = np.asarray(P3, float)
    h = ConvexHull(P3)
    zmin, zmax = P3[:, 0].min(), P3[:, 0].max()
    fibers = []
    zs = []
    # all hull edges from simplices
    edges = set()
    for s in h.simplices:
        for i in range(3):
            a, b = s[i], s[(i + 1) % 3]
            edges.add((min(a, b), max(a, b)))
    edges = np.array(sorted(edges))
    for j in range(int(np.ceil(zmin - 1e-12)), int(np.floor(zmax + 1e-12)) + 1):
        pts = []
        for a, b in edges:
            za, zb = P3[a, 0], P3[b, 0]
            if abs(za - j) < 1e-12:
                pts.append(P3[a, 1:])
            if abs(zb - j) < 1e-12:
                pts.append(P3[b, 1:])
            if (za - j) * (zb - j) < 0:
                t = (j - za) / (zb - za)
                pts.append(P3[a, 1:] + t * (P3[b, 1:] - P3[a, 1:]))
        if len(pts) >= 3:
            V = hull2(np.array(pts))
            if V is not None and poly_area(V) > 1e-12:
                fibers.append(V)
                zs.append(j)
    return zs, fibers


class MISet:
    def __init__(self, fibers, zs=None, ntheta=240, nphi=121):
        self.F = [np.asarray(V, float) for V in fibers]
        self.z = np.arange(len(fibers)) if zs is None else np.asarray(zs)
        self.v = np.array([poly_area(V) for V in self.F])
        self.nu = self.v.sum()
        th = np.linspace(0, 2 * np.pi, ntheta, endpoint=False)
        ph = np.linspace(-np.pi / 2, np.pi / 2, nphi + 2)[1:-1]
        TH, PH = np.meshgrid(th, ph, indexing="ij")
        self.TH = TH.ravel()
        self.B = np.tan(PH.ravel())
        self.A = np.stack([np.cos(self.TH), np.sin(self.TH)], axis=1)
        self.th = th
        self.Ath = np.stack([np.cos(th), np.sin(th)], axis=1)

    def measure(self, k, y, A, B):
        """Mixed-integer measure of halfspaces through (k,y) with normals (B, A)."""
        t0 = A @ y
        tot = np.zeros(len(B))
        for zj, V in zip(self.z, self.F):
            tot += clip_area(V, A, t0 - B * (zj - k))
        return tot

    def depth(self, k, y, refine=True, return_arg=False):
        y = np.asarray(y, float)
        above = self.v[self.z > k].sum()
        below = self.v[self.z < k].sum()
        at = self.v[self.z == k].sum()
        cands = [above + at, below + at]
        Vk = self.F[list(self.z).index(k)]
        own = clip_area(Vk, self.Ath, self.Ath @ y)
        cands += [above + own.min(), below + own.min()]
        vals = self.measure(k, y, self.A, self.B)
        i = int(np.argmin(vals))
        best = vals[i]
        arg = (self.TH[i], self.B[i])
        if refine:
            order = np.argsort(vals)[:4]
            for i in order:
                x0 = np.array([self.TH[i], np.arctan(self.B[i])])

                def f(p):
                    a = np.array([[np.cos(p[0]), np.sin(p[0])]])
                    return self.measure(k, y, a, np.array([np.tan(np.clip(p[1], -1.5707, 1.5707))]))[0]

                r = minimize(f, x0, method="Nelder-Mead",
                             options=dict(xatol=1e-7, fatol=1e-12, maxiter=400))
                if r.fun < best:
                    best = r.fun
                    arg = (r.x[0], np.tan(r.x[1]))
        m = min([best] + cands)
        if return_arg:
            return m, arg
        return m

    def inside(self, k, y):
        V = self.F[list(self.z).index(k)]
        e = np.roll(V, -1, axis=0) - V
        w = y - V
        return np.all(e[:, 0] * w[:, 1] - e[:, 1] * w[:, 0] >= -1e-12)

    def best_point(self, refine_depth=True, starts=4, rng=None):
        rng = np.random.default_rng(0) if rng is None else rng
        best = (-1, None, None)
        for k, V in zip(self.z, self.F):
            c = centroid(V)
            x0s = [c] + [V[rng.integers(len(V))] * 0.3 + c * 0.7 for _ in range(starts - 1)]
            for x0 in x0s:
                def f(y):
                    if not self.inside(k, y):
                        return 1e3
                    return -self.depth(k, y, refine=False)
                r = minimize(f, x0, method="Nelder-Mead",
                             options=dict(xatol=1e-6, fatol=1e-9, maxiter=300))
                y = r.x
                if not self.inside(k, y):
                    continue
                dv = self.depth(k, y, refine=refine_depth)
                if dv > best[0]:
                    best = (dv, k, y)
        return best[0] / self.nu, best[1], best[2]


def centroid(V):
    x, y = V[:, 0], V[:, 1]
    cr = x * np.roll(y, -1) - np.roll(x, -1) * y
    A = 0.5 * cr.sum()
    cx = ((x + np.roll(x, -1)) * cr).sum() / (6 * A)
    cy = ((y + np.roll(y, -1)) * cr).sum() / (6 * A)
    return np.array([cx, cy])
