"""Two-sided exact bounds on the optimum of an emfl instance (own code).

Structure (asserted from the OSIL file):
  min sum_k c_k t_k   (c_k >= 0; many cones have c_k = 0)
  t_k^2 - |w_k|^2 >= 0, t_k >= 0                      (quadratic G rows)
  w_k = A_k z + e_k                                  (each w in one E row)
  z >= 0 (base variables, no upper bounds).

Upper bound: any z >= 0 (rational), w from the E rows exactly, t_k := rational
upper bound of |w_k| is exactly feasible; the objective is exact. Checked with
the generic exact evaluator on the full OSIL model.

Lower bound (weak duality, derived here): for y_k with |y_k| <= c_k and
g = sum_k A_k^T y_k >= 0 componentwise, every feasible point satisfies
  sum c_k t_k >= sum c_k |w_k| >= sum y_k.w_k = g.z + sum y_k.e_k >= sum y_k.e_k.
y is taken from the numerical SOCP solution (cvxpy), rounded to rationals,
corrected exactly so that g >= 0 (least-norm exact correction of the negative
components), and scaled by a rational s <= 1 so that every |y_k| <= c_k
(checked exactly with integer square roots).
"""
import os
import sys
from fractions import Fraction as F
from math import isqrt

import cvxpy as cp
import numpy as np

import evalpt
import osil

HERE = os.path.dirname(os.path.abspath(__file__))


def sqrt_up(q, bits=200):
    """Rational >= sqrt(q) (q >= 0 Fraction)."""
    n, d = q.numerator, q.denominator
    v = (n * d) << (2 * bits)
    r = isqrt(v)
    if r * r != v:
        r += 1
    return F(r, d << bits)


def main(name, osil_path=None):
    M = osil.parse(osil_path) if osil_path else evalpt.model(name)
    assert M.sense == "min" and M.obj_const == 0 and not M.obj_quad and M.obj_nl is None
    cones = [i for i in range(M.m) if M.quad[i]]
    Tv, Wv = [], []
    for i in cones:
        assert not M.lin[i] and M.nl[i] is None and M.clb[i] == 0 and M.cub[i] is None and M.cconst[i] == 0
        pos = [a for a, b, c in M.quad[i] if c == 1 and a == b]
        neg = [a for a, b, c in M.quad[i] if c == -1 and a == b]
        assert len(pos) == 1 and len(neg) + 1 == len(M.quad[i])
        Tv.append(pos[0])
        Wv.append(neg)
    tset = set(Tv)
    wset = set(j for w in Wv for j in w)
    assert len(tset) == len(Tv) and all(M.lb[j] == 0 and M.ub[j] is None for j in tset)
    assert set(M.obj_lin) <= tset and all(v >= 0 for v in M.obj_lin.values())
    base = sorted(set(range(M.n)) - tset - wset)
    assert all(M.lb[j] == 0 and M.ub[j] is None and M.vtype[j] == "C" for j in base)
    assert all(M.lb[j] is None and M.ub[j] is None for j in wset)
    bidx = {j: k for k, j in enumerate(base)}
    defn = {}  # w var -> (dict base->coef, const)  with w = sum coef*z + const
    for i in range(M.m):
        if M.quad[i]:
            continue
        assert M.clb[i] is not None and M.clb[i] == M.cub[i] and M.nl[i] is None
        ws = [j for j in M.lin[i] if j in wset]
        assert len(ws) == 1 and set(M.lin[i]) - {ws[0]} <= set(base)
        w = ws[0]
        a = M.lin[i][w]
        coef = {j: -c / a for j, c in M.lin[i].items() if j != w}
        defn[w] = (coef, (M.cub[i] - M.cconst[i]) / a)
    assert set(defn) == wset
    nb = len(base)
    c = [M.obj_lin.get(t, F(0)) for t in Tv]
    # numerical SOCP
    z = cp.Variable(nb, nonneg=True)
    terms, cons, soc = [], [], []
    for k, ws in enumerate(Wv):
        if c[k] == 0:
            continue
        rows = []
        for w in ws:
            coef, e = defn[w]
            row = np.zeros(nb)
            for j, v in coef.items():
                row[bidx[j]] = float(v)
            rows.append((row, float(e)))
        A = np.array([r for r, _ in rows])
        e = np.array([v for _, v in rows])
        tk = cp.Variable()
        con = cp.SOC(tk, A @ z + e)
        cons.append(con)
        soc.append((k, con, A, e))
        terms.append(float(c[k]) * tk)
    prob = cp.Problem(cp.Minimize(sum(terms)), cons)
    prob.solve(solver="CLARABEL", tol_gap_abs=1e-12, tol_gap_rel=1e-12, tol_feas=1e-12, max_iter=500)
    print(f"{name}: numerical optimum {prob.value!r} status {prob.status}")
    zs = [max(F(0), F(float(v))) for v in z.value]
    # ---- upper bound: exact feasible point
    x = [F(0)] * M.n
    for j, v in zip(base, zs):
        x[j] = v
    for w, (coef, e) in defn.items():
        x[w] = e + sum(v * x[j] for j, v in coef.items())
    for t, ws in zip(Tv, Wv):
        x[t] = sqrt_up(sum(x[w] ** 2 for w in ws))
    vi = evalpt.violations(M, x)
    assert max(v for v, _, _ in vi) == 0, "upper-bound point not exactly feasible"
    UB = osil.obj_exact(M, x)
    # ---- lower bound: dual certificate
    y = {}
    for (k, con, A, e) in soc:
        mu = con.dual_value[1]
        y[k] = [F(float(-v)) for v in np.ravel(mu)]
    # choose sign so that sum y.e is close to the primal value
    def ye(yy):
        tot = F(0)
        for k, v in yy.items():
            for w, yv in zip(Wv[k], v):
                tot += yv * defn[w][1]
        return tot
    if abs(float(ye(y)) - prob.value) > abs(float(-ye(y)) - prob.value):
        y = {k: [-v for v in vv] for k, vv in y.items()}

    def gvec(yy):
        g = [F(0)] * nb
        for k, v in yy.items():
            for w, yv in zip(Wv[k], v):
                for j, a in defn[w][0].items():
                    g[bidx[j]] += a * yv
        return g
    g = gvec(y)
    print("  g before correction: min", float(min(g)), "max", float(max(g)))
    # exact least-norm correction of the negative components: B dy = d, dy = B^T u
    neg = [jj for jj in range(nb) if g[jj] < 0]
    if neg:
        # columns of B: every (k, component) of y
        cols = [(k, p) for k in y for p in range(len(Wv[k]))]
        def colvec(k, p):
            v = [F(0)] * nb
            for j, a in defn[Wv[k][p]][0].items():
                v[bidx[j]] += a
            return v
        Bc = {kp: colvec(*kp) for kp in cols}
        m = len(neg)
        G = [[sum(Bc[kp][a] * Bc[kp][b] for kp in cols) for b in neg] for a in neg]
        d = [-g[a] for a in neg]
        # exact Gaussian elimination
        Aug = [G[r] + [d[r]] for r in range(m)]
        for col in range(m):
            p = next(r for r in range(col, m) if Aug[r][col] != 0)
            Aug[col], Aug[p] = Aug[p], Aug[col]
            pv = Aug[col][col]
            Aug[col] = [v / pv for v in Aug[col]]
            for r in range(m):
                if r != col and Aug[r][col] != 0:
                    f = Aug[r][col]
                    Aug[r] = [a - f * b for a, b in zip(Aug[r], Aug[col])]
        u = [Aug[r][m] for r in range(m)]
        for kp in cols:
            k, p = kp
            y[k][p] += sum(Bc[kp][a] * u[r] for r, a in enumerate(neg))
        g = gvec(y)
    assert all(v >= 0 for v in g), "g not >= 0 after correction"
    # scaling: s = min(1, min_k c_k / |y_k|) (rational lower bound)
    s = F(1)
    for k, v in y.items():
        nrm = sqrt_up(sum(t * t for t in v))
        if nrm > c[k]:
            s = min(s, c[k] / nrm)
    y = {k: [s * t for t in v] for k, v in y.items()}
    assert all(sum(t * t for t in v) <= c[k] ** 2 for k, v in y.items())
    assert all(v >= 0 for v in gvec(y))
    LB = ye(y)
    print(f"  scaling s = 1 - {float(1 - s):.3e}")
    print(f"  exact optimum in [{float(LB)!r}, {float(UB)!r}], gap {float(UB - LB):.3e}")
    return LB, UB


if __name__ == "__main__":
    LB, UB = main(sys.argv[1], *(sys.argv[2:3]))
    for arg in sys.argv[3:]:
        lbl, val = arg.split("=")
        v = F(val)
        print(f"  {lbl} {val}: {'below LB (not attainable)' if v < LB else 'within [LB, UB]' if v <= UB else 'above UB'}; LB - value = {float(LB - v):.3e}")
