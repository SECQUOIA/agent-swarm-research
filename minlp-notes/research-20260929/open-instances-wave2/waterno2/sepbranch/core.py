"""Separator branching for waterno2_T: rigorous period bounds on cell pairs.

A cell is a closed float box [lo_k, hi_k] (k = tank 1..3) of the three tank
levels at one link (period t -> t+1).  For period t, an entry cell (link t-1)
and an exit cell (link t), the pair subproblem is

    phi_t(Din, Dout) = min  cost_t(x) - mu*h_t(x) + lam_in . s(x) - lam_out . e(x)
                       s.t. period-t rows, OSIL bounds, implied bounds,
                            s(x) in Din, e(x) in Dout,

where s(x) are the start levels (copies of link t-1) and e(x) the end levels
(copies of link t).  lam_in / lam_out are the slopes (multipliers) attached to
the entry / exit cell.  Any float slopes and any mu >= 0 are allowed.

rbb.solve (the wave-2 rigorous B&B, independently rechecked) gives a number
B <= phi_t(Din, Dout), or +inf if FBBT proves the pair box empty.
"""
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import period  # noqa: E402
import rbb  # noqa: E402

INF = float("inf")


def setup(T, implied):
    return period.setup(T, implied)


def level_box(D, t):
    """Box of the link-t levels: intersection of the bounds of both copies
    (OSIL bounds widened outward as in rbb, and implied bounds)."""
    M, S = D["M"], D["S"]
    lo, hi = [], []
    for (i, a, b) in S["link"][t]:
        l, h = -INF, INF
        for v in (a, b):
            lv = rbb.dec_iv(M["lb"][v])[0]
            hv = rbb.dec_iv(M["ub"][v])[1]
            if v in D["extra"]:
                lv, hv = max(lv, D["extra"][v][0]), min(hv, D["extra"][v][1])
            l, h = max(l, lv), min(h, hv)
        lo.append(float(l))
        hi.append(float(h))
    return np.array(lo), np.array(hi)


class PeriodBounder:
    """rbb.Window of one period, re-used for all cell pairs of that period."""

    def __init__(self, D, t):
        self.D, self.t, self.T = D, t, D["T"]
        self.W = rbb.Window(D, t, t + 1)
        self.lo0 = self.W.lo0.copy()
        self.hi0 = self.W.hi0.copy()
        S = D["S"]
        loc = self.W.loc
        self.sidx = [loc[b] for (i, a, b) in S["link"][t - 1]] if t > 0 else None
        self.eidx = [loc[a] for (i, a, b) in S["link"][t]] if t < self.T - 1 else None
        self.hidx = [loc[v] for v in D["hor"] if D["per_of"][v] == t]
        self.obbt_vars = sorted({a for kind, args in self.W.auxdef for a in args if not self.W.isbin[a]})

    def objective(self, lam_in, lam_out, mu):
        T = self.T
        lam = [[0.0, 0.0, 0.0] for _ in range(T - 1)]
        if self.t > 0:
            lam[self.t - 1] = [float(v) for v in lam_in]
        if self.t < T - 1:
            lam[self.t] = [float(v) for v in lam_out]
        return self.W.objective(lam, mu)

    def box(self, cin, cout):
        lo, hi = self.lo0.copy(), self.hi0.copy()
        if cin is not None:
            for k, j in enumerate(self.sidx):
                lo[j] = max(lo[j], cin[0][k])
                hi[j] = min(hi[j], cin[1][k])
        if cout is not None:
            for k, j in enumerate(self.eidx):
                lo[j] = max(lo[j], cout[0][k])
                hi[j] = min(hi[j], cout[1][k])
        return lo, hi

    def bound(self, cin, cout, lam_in, lam_out, mu, target, node_limit=2000, time_limit=60.0,
              obbt=True, rc=True):
        """Rigorous lower bound of phi_t on the pair (cin, cout); cells are
        (lo_array, hi_array) or None (period 0 entry / last period exit)."""
        assert mu >= 0
        W = self.W
        lo, hi = self.box(cin, cout)
        if np.any(lo > hi):
            return dict(bound=INF, status="empty", nodes=0, time=0.0)
        W.lo0, W.hi0 = lo, hi
        try:
            c = self.objective(lam_in, lam_out, mu)
            tic = time.time()
            res = rbb.solve(W, c, target, node_limit=node_limit, time_limit=time_limit, rc=rc,
                            obbt_vars=self.obbt_vars if obbt else None)
            res["time"] = time.time() - tic
        finally:
            W.lo0, W.hi0 = self.lo0, self.hi0
        return res
