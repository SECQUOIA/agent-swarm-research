"""Search for violated E-CG cuts obtained by perturbing an 'exact' base point.

Base point: v* = rho*sigma, v0* = rho*tau (sigma in Z^n, a = rho^2, b = 2 a tau) such that
every coefficient 2 v_i v_j, v_i^2 + 2 v_i v0 is an integer and v0*^2 is an integer.
E-CG at v* + eps*delta (eps -> 0+): an integer coefficient k stays k if its first-order change
J_k.delta < 0 and becomes k+1 if J_k.delta > 0; floor(v0^2) drops by 1 if v0* delta_0 < 0.
So the perturbed cut is   f*(z) - 1 + sum_{k in S+} z_k >= 0,  S+ = {k : J_k.delta > 0}.
MILP: minimize this over z in P_pool (BH pool ⊇ P_BH), delta, S+ (binaries); if negative,
re-separate BH at z and repeat.  Strictness is enforced with margin eta (search only;
any hit is re-verified exactly)."""
import numpy as np
import gurobipy as gp
from gurobipy import GRB
from bh import pairs, dim, bh_ineq, separate_bh, complete_separation


def jacobian_rows(sigma, tau):
    """Rows (over delta = (d0, d1..dn)) of first-order changes, up to the positive factor 2 rho^2,
    ordered as z: x_1..x_n, X_ij; plus the row for v0^2."""
    n = len(sigma)
    rows = []
    for i in range(n):
        r = np.zeros(n + 1)
        r[0] = sigma[i]
        r[i + 1] = sigma[i] + tau
        rows.append(r)
    for (i, j) in pairs(n):
        r = np.zeros(n + 1)
        r[i + 1] = sigma[j]
        r[j + 1] = sigma[i]
        rows.append(r)
    r0 = np.zeros(n + 1)
    r0[0] = tau
    return np.array(rows), r0


class PerturbSearch:
    def __init__(self, pbh):
        self.P = pbh  # PBH object: reuse its constraint pool
        self.n = pbh.n

    def run(self, sigma, a, b, c, eta=1e-3, maxit=50):
        n = self.n
        d = dim(n)
        tau = float(b / (2 * a))
        coef = [a * s * s + b * s for s in sigma] + [2 * a * sigma[i] * sigma[j] for (i, j) in pairs(n)]
        coef = [float(t) for t in coef]
        J, r0 = jacobian_rows(sigma, tau)
        m = gp.Model()
        m.Params.OutputFlag = 0
        m.Params.Threads = 1
        m.Params.TimeLimit = 60
        z = m.addVars(d, lb=0, ub=1)
        for (aa, cc) in self.P.keys:
            m.addConstr(gp.quicksum(aa[k] * z[k] for k in range(d) if aa[k]) + cc >= 0)
        dl = m.addVars(n + 1, lb=-1, ub=1)
        s = m.addVars(d, vtype=GRB.BINARY)
        t = m.addVars(d, lb=0)
        U = 2 * (np.abs(J).sum(1) + 1)
        for k in range(d):
            m.addConstr(gp.quicksum(J[k, l] * dl[l] for l in range(n + 1) if J[k, l]) <= -eta + U[k] * s[k])
            m.addConstr(t[k] >= z[k] + s[k] - 1)
        m.addConstr(r0[0] * dl[0] <= -eta)
        m.setObjective(gp.quicksum(coef[k] * z[k] for k in range(d)) + (c - 1) + t.sum(), GRB.MINIMIZE)
        for it in range(maxit):
            m.optimize()
            if m.Status not in (GRB.OPTIMAL, GRB.TIME_LIMIT) or m.SolCount == 0:
                return None
            zv = np.array([z[k].X for k in range(d)])
            val = m.ObjVal
            if val >= -1e-7:
                return val, None
            cuts, _ = separate_bh(n, zv, W=6)
            wlist = [wv for _, wv in cuts]
            if not wlist:
                # fix the pattern and re-solve as an LP so that z is a clean vertex
                for k in range(d):
                    s[k].LB = s[k].UB = round(s[k].X)
                m.optimize()
                zv = np.array([z[k].X for k in range(d)])
                val = m.ObjVal
                for k in range(d):
                    s[k].LB, s[k].UB = 0, 1
                if val >= -1e-7:
                    return val, None
                cuts, _ = separate_bh(n, zv, W=6)
                wlist = [wv for _, wv in cuts]
            if not wlist:
                wlist, zr = complete_separation(n, zv)
                if not wlist:   # zr is certified (exactly) to lie in P_BH
                    return val, (zr, [dl[l].X for l in range(n + 1)], [int(round(s[k].X)) for k in range(d)])
            for wv in wlist:
                aa, cc = bh_ineq(wv[0], wv[1:])
                if self.P._add(aa, cc):
                    m.addConstr(gp.quicksum(aa[k] * z[k] for k in range(d) if aa[k]) + cc >= 0)
        return None
