"""Boros-Hammer (BH) and Eigen-CG (E-CG) inequalities in the (x, X_ij) space.

Coordinates: z = (x_1..x_n, X_ij for i<j in lexicographic order).
Every inequality is stored as (a, c) meaning  a . z + c >= 0.

Definitions follow Dey-Jiang-Kazachkov-Lodi-Munoz, arXiv:2604.00932v1:
  BH (w0, w in Z^{n+1}), eq. (9):
     sum_{i<j} 2 w_i w_j X_ij + sum_i w_i (w_i + 2 w0 - 1) x_i + w0 (w0 - 1) >= 0
  E-CG (v0, v in R^{n+1}), eq. (8) / Definition 1:
     sum_{i<j} ceil(2 v_i v_j) X_ij + sum_i ceil(v_i^2 + 2 v_i v0) x_i + floor(v0^2) >= 0
"""
import itertools
import math
from fractions import Fraction

import numpy as np
import gurobipy as gp
from gurobipy import GRB


def pairs(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def dim(n):
    return n + n * (n - 1) // 2


def bh_ineq(w0, w):
    n = len(w)
    a = [w[i] * (w[i] + 2 * w0 - 1) for i in range(n)]
    a += [2 * w[i] * w[j] for (i, j) in pairs(n)]
    return a, w0 * (w0 - 1)


def ecg_ineq_exact(v0, v):
    """E-CG coefficients with exact arithmetic. v0, v: Fractions/ints or sympy numbers."""
    import sympy as sp
    n = len(v)
    fl = lambda t: int(sp.floor(sp.nsimplify(t))) if not isinstance(t, (int, Fraction)) else math.floor(t)
    ce = lambda t: int(sp.ceiling(sp.nsimplify(t))) if not isinstance(t, (int, Fraction)) else math.ceil(t)
    a = [ce(v[i] * v[i] + 2 * v[i] * v0) for i in range(n)]
    a += [ce(2 * v[i] * v[j]) for (i, j) in pairs(n)]
    return a, fl(v0 * v0)


def ecg_ineq_float(v0, v):
    n = len(v)
    a = [math.ceil(v[i] ** 2 + 2 * v[i] * v0) for i in range(n)]
    a += [math.ceil(2 * v[i] * v[j]) for (i, j) in pairs(n)]
    return a, math.floor(v0 ** 2)


def bh_pool(n, W=1):
    """All BH inequalities with |w_i| <= W, deduplicated using (w0,w) ~ (1-w0,-w),
    keeping only w0 for which t = w.x + w0 can take the values 0 or 1 on {0,1}^n."""
    seen = set()
    out = []
    for w in itertools.product(range(-W, W + 1), repeat=n):
        if not any(w):
            continue
        pos = sum(t for t in w if t > 0)
        neg = sum(t for t in w if t < 0)
        for w0 in range(-pos, 2 - neg):
            a, c = bh_ineq(w0, w)
            key = (tuple(a), c)
            if key in seen:
                continue
            seen.add(key)
            out.append(key)
    return out


def moment_matrix(n, z):
    """M = [[1, x^T],[x, Y]] with Y_ii = x_i, Y_ij = X_ij."""
    x = z[:n]
    M = np.zeros((n + 1, n + 1))
    M[0, 0] = 1
    M[0, 1:] = x
    M[1:, 0] = x
    for i in range(n):
        M[i + 1, i + 1] = x[i]
    for k, (i, j) in enumerate(pairs(n)):
        M[i + 1, j + 1] = M[j + 1, i + 1] = z[n + k]
    return M


def separate_bh(n, z, W=6, tol=1e-7, timelimit=60, pool=20):
    """Most violated BH inequality at z with |w_i| <= W (MIQP, Gurobi).
    Value of BH at z = w^T M w - c^T w, w=(w0,w), c=(1,x)."""
    M = moment_matrix(n, z)
    c = np.concatenate([[1.0], z[:n]])
    m = gp.Model()
    m.Params.OutputFlag = 0
    m.Params.Threads = 1
    m.Params.TimeLimit = timelimit
    m.Params.PoolSolutions = pool
    m.Params.NonConvex = 2
    w = m.addVars(n + 1, lb=-W, ub=W, vtype=GRB.INTEGER)
    w[0].LB = -W * n - 1
    w[0].UB = W * n + 1
    obj = gp.QuadExpr()
    for i in range(n + 1):
        for j in range(n + 1):
            if M[i, j] != 0:
                obj += M[i, j] * w[i] * w[j]
        obj += -c[i] * w[i]
    m.setObjective(obj, GRB.MINIMIZE)
    m.optimize()
    cuts = []
    for s in range(m.SolCount):
        m.Params.SolutionNumber = s
        wv = [int(round(w[i].Xn)) for i in range(n + 1)]
        a, cc = bh_ineq(wv[0], wv[1:])
        val = float(np.dot(a, z) + cc)
        if val < -tol:
            cuts.append((val, wv))
    return cuts, m.ObjVal if m.SolCount else None


class PBH:
    """LP over the BH closure P_BH(n) by cutting planes (pool + MIQP separation)."""

    def __init__(self, n, W0=1, Wsep=6, exact=False):
        self.n = n
        self.exact = exact
        self.last_certified = None
        self.Wsep = Wsep
        self.m = gp.Model()
        self.m.Params.OutputFlag = 0
        self.m.Params.Threads = 1
        self.m.Params.FeasibilityTol = 1e-9
        self.m.Params.OptimalityTol = 1e-9
        d = dim(n)
        self.z = self.m.addVars(d, lb=0.0, ub=1.0)
        self.d = d
        self.keys = set()
        for a, c in bh_pool(n, W0):
            self._add(a, c)

    def _add(self, a, c):
        key = (tuple(a), c)
        if key in self.keys:
            return False
        self.keys.add(key)
        self.m.addConstr(gp.quicksum(float(a[k]) * self.z[k] for k in range(self.d) if a[k]) + c >= 0)
        return True

    def minimize(self, a, maxit=200, verbose=False):
        self.m.setObjective(gp.quicksum(float(a[k]) * self.z[k] for k in range(self.d) if a[k]), GRB.MINIMIZE)
        for it in range(maxit):
            self.m.optimize()
            zv = np.array([self.z[k].X for k in range(self.d)])
            cuts, best = separate_bh(self.n, zv, W=self.Wsep)
            wlist = [wv for _, wv in cuts]
            if not wlist and self.exact:
                wlist, zr = complete_separation(self.n, zv)
                if not wlist:
                    self.last_certified = zr   # exact rational point of P_BH
            added = 0
            for wv in wlist:
                aa, cc = bh_ineq(wv[0], wv[1:])
                added += self._add(aa, cc)
            if verbose:
                print(it, self.m.ObjVal, best, added)
            if not wlist:
                return self.m.ObjVal, zv
            if added == 0:
                raise RuntimeError("separation returned only known cuts")
        raise RuntimeError("no convergence")


def rationalize(z, maxden=10 ** 4, tol=1e-8):
    from fractions import Fraction
    zr = [Fraction(float(t)).limit_denominator(maxden) for t in z]
    if max(abs(float(a) - float(b)) for a, b in zip(zr, z)) > tol:
        return None
    return zr


def complete_separation(n, z, Wlist=(12, 25, 50, 100)):
    """Called when the |w| <= 6 MIQP finds no violated BH at z.
    Returns (cuts, certified) where cuts is a list of violated BH (w0,w) and certified is the
    rational point proven (exactly) to satisfy all BH inequalities, if no cut exists."""
    from verify import exact_bh_separation_general as exact_bh_separation
    M = moment_matrix(n, z)
    if np.linalg.eigvalsh(M).min() < -1e-10:
        for W in Wlist:
            cuts, _ = separate_bh(n, z, W=W, timelimit=120)
            if cuts:
                return [wv for _, wv in cuts], None
        raise RuntimeError("M not PSD but no BH cut found with |w| <= %d" % Wlist[-1])
    zr = rationalize(z) or rationalize(z, maxden=10 ** 6, tol=1e-7)
    if zr is None:
        raise RuntimeError("could not rationalize z")
    w, info = exact_bh_separation(n, zr)
    if w is None:
        return [], zr
    if max(abs(t) for t in w) > 10 ** 4:
        for W in Wlist:
            cuts, _ = separate_bh(n, z, W=W, timelimit=120)
            if cuts:
                return [wv for _, wv in cuts], None
    return [w], None
