"""Separation of row-hull cuts by column generation over row vertices.

Membership LP for a point (z^, t'^) with t' = t - chord:

    min s   s.t.  sum_v lam_v v = z^,  sum_v lam_v = 1,
                  sum_{v: j(v)=k} lam_v gamma_k(r_v) - rho_k s <= t'^_k   (k concave),
                  lam >= 0, s >= 0.

If s* > 0 the duals (pi, pi0, omega) give the cut  omega't' >= pi'z + pi0.  The
constant is recomputed from the pricing lower bound, so the cut is valid
whatever the LP accuracy.
"""
from __future__ import annotations

import numpy as np
import gurobipy as gp
from gurobipy import GRB

from .pricing import price


class RowSeparator:
    def __init__(self, row, kmax=4000, env=None):
        self.row, self.kmax = row, kmax
        self.conc = row.concave
        n = row.n
        m = gp.Model(env=env) if env is not None else gp.Model()
        m.Params.OutputFlag = 0
        m.Params.Method = 1
        self.m = m
        self.s = m.addVar(lb=0.0, obj=1.0)
        self.bigM = 1e3
        self.art = [(m.addVar(lb=0.0, obj=self.bigM), m.addVar(lb=0.0, obj=self.bigM)) for _ in range(n)]
        self.ceq = [m.addConstr(self.art[k][0] - self.art[k][1] == 0.0) for k in range(n)]
        self.art0 = m.addVar(lb=0.0, obj=self.bigM)
        self.cone = m.addConstr(self.art0 == 1.0)
        self.cgap = {k: m.addConstr(-row.items[k].rho * self.s <= 0.0) for k in self.conc}
        self.seen = set()
        self.ncols = 0
        m.update()

    def _add(self, mask, j, r):
        key = (mask, j)
        if key in self.seen:
            return False
        self.seen.add(key)
        row = self.row
        col = gp.Column()
        for i in range(row.n):
            if mask >> i & 1:
                col.addTerms(row.items[i].width, self.ceq[i])
        if r > 0:
            col.addTerms(r, self.ceq[j])
        col.addTerms(1.0, self.cone)
        if j in self.cgap:
            g = float(row.items[j].gap(np.array([r]))[0])
            if g > 0:
                col.addTerms(g, self.cgap[j])
        self.m.addVar(lb=0.0, obj=0.0, column=col)
        self.ncols += 1
        return True

    def separate(self, zhat, tphat, tol=1e-6, max_iter=200):
        """zhat: normalized point; tphat: dict k -> t'_k.  Returns cut dict or None."""
        row = self.row
        for k in range(row.n):
            self.ceq[k].RHS = float(zhat[k])
        for k in self.conc:
            self.cgap[k].RHS = float(max(tphat[k], 0.0))
        lower = None
        for _ in range(max_iter):
            self.m.optimize()
            if self.m.Status != GRB.OPTIMAL:
                return None
            pi = np.array([c.Pi for c in self.ceq])
            pi0 = self.cone.Pi
            # pi is defined up to a common shift because sum z = B on the row; remove it
            shift = float(np.median(pi))
            pi, pi0 = pi - shift, pi0 + shift * row.B
            omega = np.zeros(row.n)
            for k in self.conc:
                omega[k] = max(-self.cgap[k].Pi, 0.0)
            lower, cols = price(row, pi, omega, self.kmax)
            added = False
            for mask, j, r, val in cols:
                if val - pi0 < -1e-9:
                    added |= self._add(mask, j, r)
            if not added:
                break
        art = sum(a.X + b.X for a, b in self.art) + self.art0.X
        if art > 1e-7 or lower is None or not np.isfinite(lower):
            return None
        if lower > pi0 + 1e-6 * max(1.0, abs(pi0)):
            return None          # at convergence the pricing minimum is about pi0; otherwise distrust it
        pi0v = lower - 1e-9 * max(1.0, abs(lower))          # valid constant (up to floating point)
        viol = float(pi @ zhat + pi0v - sum(omega[k] * tphat[k] for k in self.conc))
        if viol <= tol:
            return None
        return {"pi": pi, "pi0": pi0v, "omega": omega, "viol": viol}


def cut_to_model(row, cut):
    """Express  omega't' >= pi'z + pi0  in model variables.

    Returns (coefs: dict var -> coef, rhs) meaning  sum coefs*var >= rhs.
    """
    pi, omega, pi0 = cut["pi"].copy(), cut["omega"], cut["pi0"]
    if row.slack is not None:            # z_slack = B - sum of the other z
        ps = pi[row.slack]
        pi0 += ps * row.B
        pi = pi - ps
        pi[row.slack] = 0.0
    coefs, rhs = {}, pi0
    for k, it in enumerate(row.items):
        if it.var is None:
            continue
        # -pi_k z_k, with z_k = a (v - lo) or |a| (hi - v)
        if it.a > 0:
            c, const = -pi[k] * it.a, pi[k] * it.a * it.lo
        else:
            c, const = pi[k] * (-it.a), -pi[k] * (-it.a) * it.hi
        rhs -= const
        if it.f is not None and omega[k] > 0:
            for tv, tc in it.tvar.items():
                coefs[tv] = coefs.get(tv, 0.0) + omega[k] * tc
            c -= omega[k] * it.chord[1]
            rhs += omega[k] * it.chord[0]
        if c != 0.0:
            coefs[it.var] = coefs.get(it.var, 0.0) + c
    return coefs, rhs
