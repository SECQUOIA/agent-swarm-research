"""Heuristic E-CG separation at a fixed point z: exact one-dimensional minimisation of the
piecewise-constant function F(v0, v) along lines, used inside random-restart line search.

Along v(t) = a + t d every quantity (v0^2, p_i, q_ij) is a quadratic in t; F changes only where
one of them crosses an integer.  All crossings inside the ellipsoid q_M < 1 are computed, and F
is evaluated at every crossing (with integer-snapping tolerance 1e-9, i.e. the boundary value,
which is the strongest cut of the adjacent cells) and between consecutive crossings.
Any F < 0 found is only a candidate; it must be re-verified exactly."""
import numpy as np
from bh import pairs, moment_matrix


class LineSearch:
    def __init__(self, n, z):
        self.n = n
        self.z = np.asarray(z, float)
        self.P = pairs(n)
        self.M = moment_matrix(n, z)
        # quantities as symmetric matrices Q_k: value = vh^T Q_k vh
        Qs = []
        Q0 = np.zeros((n + 1, n + 1)); Q0[0, 0] = 1
        for i in range(n):
            Q = np.zeros((n + 1, n + 1)); Q[i + 1, i + 1] = 1; Q[0, i + 1] = Q[i + 1, 0] = 1
            Qs.append(Q)
        for (i, j) in self.P:
            Q = np.zeros((n + 1, n + 1)); Q[i + 1, j + 1] = Q[j + 1, i + 1] = 1
            Qs.append(Q)
        self.Q0 = Q0
        self.Qs = np.array(Qs)
        self.w = self.z.copy()
        self.active = self.w > 0

    def F(self, V, snap=1e-9):
        """F for rows of V (N x (n+1)); v0 sign irrelevant."""
        v0sq = V[:, 0] ** 2
        vals = np.einsum('ni,kij,nj->nk', V, self.Qs, V)
        return np.floor(v0sq + snap) + np.ceil(vals - snap) @ self.w

    def line_min(self, a, d):
        M = self.M
        A2, A1, A0 = d @ M @ d, 2 * a @ M @ d, a @ M @ a - 1
        disc = A1 * A1 - 4 * A2 * A0
        if disc <= 0:
            return np.inf, None
        s = np.sqrt(disc)
        t_lo, t_hi = (-A1 - s) / (2 * A2), (-A1 + s) / (2 * A2)
        ts = [t_lo, t_hi]
        quads = [self.Q0] + [self.Qs[k] for k in range(len(self.Qs)) if self.active[k]]
        for Q in quads:
            c2, c1, c0 = d @ Q @ d, 2 * a @ Q @ d, a @ Q @ a
            tt = np.array([t_lo, t_hi])
            cand = [t_lo, t_hi]
            if abs(c2) > 1e-15:
                tv = -c1 / (2 * c2)
                if t_lo < tv < t_hi:
                    cand.append(tv)
            vals = c2 * np.array(cand) ** 2 + c1 * np.array(cand) + c0
            for k in range(int(np.floor(vals.min())), int(np.ceil(vals.max())) + 1):
                if abs(c2) > 1e-15:
                    dd = c1 * c1 - 4 * c2 * (c0 - k)
                    if dd >= 0:
                        r = np.sqrt(dd)
                        for t in ((-c1 - r) / (2 * c2), (-c1 + r) / (2 * c2)):
                            if t_lo < t < t_hi:
                                ts.append(t)
                elif abs(c1) > 1e-15:
                    t = (k - c0) / c1
                    if t_lo < t < t_hi:
                        ts.append(t)
        ts = np.sort(np.array(ts))
        mids = (ts[1:] + ts[:-1]) / 2
        allt = np.concatenate([ts[1:-1], mids])
        V = a[None, :] + allt[:, None] * d[None, :]
        Fv = self.F(V)
        k = int(np.argmin(Fv))
        return Fv[k], V[k]

    def search(self, rng, restarts=100, iters=60):
        n = self.n
        L = np.linalg.cholesky(self.M)
        Linv_T = np.linalg.inv(L).T
        best = (np.inf, None)
        for _ in range(restarts):
            u = rng.standard_normal(n + 1)
            u *= rng.random() ** (1 / (n + 1)) / np.linalg.norm(u)
            a = Linv_T @ u
            fa = self.F(a[None, :])[0]
            for _ in range(iters):
                if rng.random() < 0.5:
                    d = np.zeros(n + 1); d[rng.integers(n + 1)] = 1
                else:
                    d = rng.standard_normal(n + 1)
                f, v = self.line_min(a, d)
                if v is not None and f <= fa:
                    a, fa = v, f
            if fa < best[0]:
                best = (fa, a.copy())
        return best
