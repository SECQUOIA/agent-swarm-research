"""Application-like chain: production planning with a nonconvex production cost.

Periods t = 1..T, inventory s_t in [-S, S] (negative = backlog), s_0 = 0,
production p_t = s_t - s_{t-1} + d_t in [0, P], demand d_t ~ U(0.5, 1.5).
    minimize  sum_t g(p_t) + eta * sum_t s_t^2,
    g(p) = a p - b p^2 + c p^3   (increasing; concave for p < b/(3c): economies of
                                  scale; convex beyond: overtime).
Default a = 1, b = 0.6, c = 0.15 (g' >= 0.2 > 0), eta = 0.5, P = 2.5, S = 3.

In the inventory variables this is a path: unary eta s_t^2, pair
g(s_t - s_{t-1} + d_t) with the band constraint 0 <= s_t - s_{t-1} + d_t <= P.
"""
import numpy as np
from scipy.optimize import minimize

A, BB, C, ETA, PCAP, SCAP = 1.0, 0.6, 0.15, 0.5, 2.5, 3.0


def demands(T, seed):
    return np.random.default_rng(seed).uniform(0.5, 1.5, T)


def g(p):
    return A * p - BB * p * p + C * p**3


def g1(p):
    return A - 2 * BB * p + 3 * C * p * p


def g2(p):
    return -2 * BB + 6 * C * p


def objective_s(s, d):
    """s = (s_1..s_T); returns +inf if a bound or band constraint is violated."""
    p = np.diff(np.concatenate([[0.0], s])) + d
    if (p < -1e-9).any() or (p > PCAP + 1e-9).any() or (abs(s) > SCAP + 1e-9).any():
        return np.inf
    return float(g(p).sum() + ETA * (s * s).sum())


def local_opt_p(p0, d):
    """Local optimization in production space (box [0, P]^T); inventory bounds are
    checked afterwards (the returned value is +inf if they are violated)."""
    def fg(p):
        s = np.cumsum(p - d)
        val = g(p).sum() + ETA * (s * s).sum()
        suffix = np.cumsum((2 * ETA * s)[::-1])[::-1]
        return val, g1(p) + suffix
    r = minimize(fg, np.clip(p0, 0, PCAP), jac=True, method="L-BFGS-B", bounds=[(0, PCAP)] * len(d),
                 options=dict(ftol=1e-15, gtol=1e-12, maxiter=10000))
    s = np.cumsum(r.x - d)
    return s, objective_s(s, d)


class LotSizingChain:
    """Chain variables x_0 = s_0 (fixed at 0) and x_t = s_t, t = 1..T."""

    def __init__(self, d):
        self.d = np.asarray(d, float)
        T = len(d)
        self.n = T + 1
        self.lo = np.concatenate([[0.0], np.full(T, -SCAP)])
        self.hi = np.concatenate([[0.0], np.full(T, SCAP)])

    def F(self, x):
        return objective_s(x[1:], self.d)

    def local_opt(self, x0):
        p0 = np.diff(x0) + self.d
        s, f = local_opt_p(p0, self.d)
        return np.concatenate([[0.0], s]), f

    # unary pieces: phi_0 = 0, phi_t = eta s^2
    def unary_lb(self, i, p, q, Qt, Lt):
        from chain_bb import taylor2_lb
        eta = np.where(i == 0, 0.0, ETA)
        m, r = 0.5 * (p + q), 0.5 * (q - p)
        val = (eta - Qt) * m * m + Lt * m
        gr = 2 * (eta - Qt) * m + Lt
        return taylor2_lb(val, gr, 2 * (eta - Qt), r)

    def unary_hess(self, x):
        h = np.full(self.n, 2 * ETA); h[0] = 0.0
        return h

    # pair pieces: psi_e(x, y) = g(y - x + d_e) on the band 0 <= y - x + d_e <= P
    def pair_grad(self, x):
        gp = g1(np.diff(x) + self.d)
        return -gp, gp

    def pair_multipliers(self, x):
        """Multipliers mu_e of the band constraints from the KKT conditions
        dF/ds_t = mu_{t-1} - mu_t (t = 1..T, mu_T = 0), solved backward."""
        p = np.diff(x) + self.d
        gp = g1(p)
        dF = 2 * ETA * x[1:] + gp          # d/ds_t of eta s_t^2 + g(p_t)
        dF[:-1] -= gp[1:]                   # - g'(p_{t+1})
        mu = np.empty(self.n - 1)
        acc = 0.0
        for t in range(self.n - 1, 0, -1):  # variable t, left pair t-1
            acc = dF[t - 1] + acc
            mu[t - 1] = acc
        return mu

    def pair_hess(self, x):
        h = g2(np.diff(x) + self.d)
        return h, -h, h

    def pair_cross(self):
        raise NotImplementedError("use mode 'split' or 'affine'")

    def pair_lb(self, e, p, q, s, t, rhoL, alpha, rhoR, beta):
        """Second-order Taylor bound at the box center, minimized exactly over the
        box intersected with the production band. With Delta = dy - dx,
        psi(m + d) = psi(m) + grad.d + 0.5 g''(xi) Delta^2 + rhoL dx^2 + rhoR dy^2,
        and g''(xi) >= g''(p_lo) because g'' is increasing (c > 0) and xi lies in
        the production range [p_lo, p_hi] of the box. The remaining quadratic is
        minimized exactly over the box. Cell pairs whose production range misses
        [0, P] are infeasible (+inf)."""
        from chain_bb import quad_band_min, FP_REL
        dd = self.d[e]
        mx, rx, my, ry = 0.5 * (p + q), 0.5 * (q - p), 0.5 * (s + t), 0.5 * (t - s)
        pm = my - mx + dd
        val = g(pm) + rhoL * mx * mx - alpha * mx + rhoR * my * my - beta * my
        gp = g1(pm)
        gx = -gp + 2 * rhoL * mx - alpha
        gy = gp + 2 * rhoR * my - beta
        plo, phi = s - q + dd, t - p + dd
        # plo must stay the UNCLIPPED smallest production of the box: the Taylor
        # centre pm may lie outside the band, and xi ranges over the whole segment
        # from pm to the point. Clipping plo at 0 would make the bound invalid.
        Hlo = g2(plo)
        # band 0 <= p <= P in the shifted coordinates: -pm <= dy - dx <= P - pm
        lb = val + quad_band_min(0.5 * Hlo + rhoL, -Hlo, 0.5 * Hlo + rhoR, gx, gy, -rx, rx, -ry, ry,
                                 -pm, PCAP - pm)
        lb = lb - FP_REL * (1 + np.abs(val))
        return np.where((phi < 0) | (plo > PCAP), np.inf, lb)


def build_scip(T, seed):
    from pyscipopt import Model, quicksum
    d = demands(T, seed)
    m = Model(); m.hideOutput()
    p = [m.addVar(lb=0, ub=PCAP, name=f"p{t}") for t in range(T)]
    s = [m.addVar(lb=-SCAP, ub=SCAP, name=f"s{t}") for t in range(T)]
    z = [m.addVar(lb=None, name=f"z{t}") for t in range(T)]
    for t in range(T):
        prev = s[t - 1] if t > 0 else 0.0
        m.addCons(s[t] == prev + p[t] - float(d[t]))
        m.addCons(z[t] >= A * p[t] - BB * p[t] * p[t] + C * p[t] ** 3)
    w = m.addVar(lb=0, name="w")
    m.addCons(w >= quicksum(ETA * s[t] * s[t] for t in range(T)))
    m.setObjective(quicksum(z) + w, "minimize")
    return m, d
