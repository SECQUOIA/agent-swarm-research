"""Toy spatial branch-and-bound on the path family of PROGRAM.md, with exact node relaxations.

f(x) = sum_i (x_i^2 - kappa x_i^4 + c_i x_i) + b sum_{i<n} x_i x_{i+1},  x in [-1,1]^n,
c = 0 ("zero") or c ~ U(-0.3, 0.3) from numpy default_rng(seed) as in scratch/probe3.py.

Relaxations (solved by HiGHS, one thread; the solver value is used only for branching, see below):
  mc   x_i^2 exact, secant of -kappa x_i^4, McCormick envelope of b x_i x_{i+1}
       (the termwise factorable relaxation; satisfies hypothesis (M_b) of the note)
  mcx  g_i(x) = x^2 - kappa x^4 kept exactly (convex on [-1,1] for kappa <= 1/6; Kelley tangent cuts
       until the violation is below 1e-10), McCormick envelope of b x_i x_{i+1}; node bound = LP value
  abbU, abbS  per-factor alphaBB with box-dependent exact alpha, PROGRAM factorization (U) or balanced
       split of each g_i between neighbouring factors (S); any kappa; bisection only (see relax_split)
  abb  per-factor alphaBB of f_i = x_i^2 + b x_i x_{i+1} (+ linear), kappa must be 0;
       alpha_i = (sqrt(4 + 4 b^2) - 2)/4, the exact value for the constant factor Hessian.
Incumbent fixed at f* (computed by local optimisation, checked against relaxation points);
a node is pruned iff its CERTIFIED lower bound is >= f* - eps - TIE (TIE = 1e-12), so the tree does not
depend on node order and every pruned box is valid at eps + 1e-12 up to rounding.
Branching rules: bisect (widest, midpoint); viol (largest term violation at the relaxation
point, split at the point clamped to [l+0.2w, u-0.2w]); mid75 (same variable, split at
0.75*midpoint + 0.25*relaxation point, clamped likewise; SCIP 10's midpull 0.75); vw (widest
variable among those in a violated term, split like mid75); vwlp (vw variable, split at the
relaxation point clamped to [l+0.2w, u-0.2w]); oracle (widest variable whose
interval contains x*_i strictly inside, split at x*_i; otherwise widest bisection).
Certified bound (revision after review): weak duality for mc/mcx (separable dual function of the
McCormick relaxation), a Frank-Wolfe bound for abb/abbU/abbS; refined by dual ascent (and, for mc, a
Clarabel fallback) when the threshold lies between it and the value at a feasible point.  The counter
'undecided' counts nodes whose solver value was >= threshold but whose certified bound stayed below it;
nodes left undecided while the solver value is also below the threshold are branched (not counted).
Floating-point illustration, not a certified count.

Usage: python3 bb_path.py rel rule kappa cmode eps n1 n2 ...   (cmode: zero | seed0 | seed1)
"""
import math
import sys
import time
import numpy as np
import highspy
from scipy import optimize

INF = highspy.kHighsInf
B = 0.8


class Inst:
    def __init__(self, n, kappa, cmode, b=B):
        self.n, self.kappa, self.b = n, kappa, b
        if cmode == "zero":
            self.c = np.zeros(n)
        else:
            rng = np.random.default_rng(int(cmode[4:]))
            self.c = rng.uniform(-0.3, 0.3, n)
        self.lo, self.hi = -np.ones(n), np.ones(n)
        self.xstar, self.fstar = self.solve()

    def f(self, x):
        return float(np.sum(x * x - self.kappa * x ** 4 + self.c * x) + self.b * np.sum(x[:-1] * x[1:]))

    def grad(self, x):
        g = 2 * x - 4 * self.kappa * x ** 3 + self.c
        g[:-1] += self.b * x[1:]
        g[1:] += self.b * x[:-1]
        return g

    def solve(self):
        best = None
        rng = np.random.default_rng(12345)
        starts = [np.zeros(self.n)] + [rng.uniform(-1, 1, self.n) for _ in range(30)]
        for x0 in starts:
            r = optimize.minimize(self.f, x0, jac=self.grad, method="L-BFGS-B",
                                  bounds=list(zip(self.lo, self.hi)), options={"ftol": 1e-15, "gtol": 1e-12, "maxiter": 10000})
            if best is None or r.fun < best.fun - 1e-12:
                best = r
        return np.array(best.x), float(best.fun)


def alpha_abb(b):
    return (math.sqrt(4 + 4 * b * b) - 2) / 4


def relax(I, rel, l, u):
    """Return (LB, xhat, what)."""
    n, b, k = I.n, I.b, I.kappa
    if rel == "mcx":
        return relax_mcx(I, l, u)
    if rel == "mc":
        m = n - 1
        ncol = n + m
        cost = np.zeros(ncol)
        # secant of -kappa x^4 on [l,u]: slope -kappa (l+u)(l^2+u^2), value -kappa l^4 at l
        slope = -k * (l + u) * (l * l + u * u)
        const = float(np.sum(-k * l ** 4 - slope * l))
        cost[:n] = I.c + slope
        cost[n:] = b
        colL = np.concatenate([l, np.full(m, -INF)])
        colU = np.concatenate([u, np.full(m, INF)])
        # rows: for b > 0 the two lower McCormick inequalities; for b < 0 the two upper ones
        start, index, value = [0], [], []
        rlo, rhi = [], []
        rows = []
        for e in range(m):
            i, j = e, e + 1
            if b > 0:
                rows.append(([n + e, i, j], [-1.0, l[j], l[i]], l[i] * l[j]))
                rows.append(([n + e, i, j], [-1.0, u[j], u[i]], u[i] * u[j]))
            else:
                rows.append(([n + e, i, j], [1.0, -u[j], -l[i]], -l[i] * u[j]))
                rows.append(([n + e, i, j], [1.0, -l[j], -u[i]], -u[i] * l[j]))
        nrow = len(rows)
        cols = [[] for _ in range(ncol)]
        for r, (idx, val, rh) in enumerate(rows):
            for q, v in zip(idx, val):
                cols[q].append((r, v))
            rlo.append(-INF); rhi.append(rh)
        for q in range(ncol):
            for (r, v) in cols[q]:
                index.append(r); value.append(v)
            start.append(len(index))
        hst = list(range(n + 1)) + [n] * m
        hid = list(range(n))
        hva = [2.0] * n
    elif rel == "abb":
        assert k == 0.0
        a = alpha_abb(b)
        atot = np.full(n, 2 * a)
        atot[0] = atot[-1] = a
        ncol, nrow = n, 0
        cost = I.c - atot * (l + u)
        const = float(np.sum(atot * l * u))
        colL, colU = l.copy(), u.copy()
        start, index, value, rlo, rhi = [0] * (n + 1), [], [], [], []
        hst, hid, hva = [0], [], []
        for q in range(n):          # lower triangle, column-wise
            hid.append(q); hva.append(2 + 2 * atot[q])
            if q + 1 < n:
                hid.append(q + 1); hva.append(b)
            hst.append(len(hid))
    else:
        raise ValueError(rel)
    for tol in (1e-10, 1e-8, 1e-7):
        res = _highs(ncol, nrow, cost, colL, colU, rlo, rhi, start, index, value, hst, hid, hva, tol)
        if res is not None:
            return res[0] + const, res[1][:n], res[1][n:]
    val, sol = _clarabel(ncol, cost, colL, colU, start, index, value, rlo, rhi, hst, hid, hva)
    return val + const, sol[:n], sol[n:]


def relax_mcx(I, l, u):
    """Exact convex g_i plus McCormick, by Kelley's cutting planes on the separable convex part."""
    n, b, k = I.n, I.b, I.kappa
    g = lambda x: x * x - k * x ** 4
    dg = lambda x: 2 * x - 4 * k * x ** 3
    m = n - 1
    ncol = 2 * n + m                     # x, tau, w
    h = highspy.Highs()
    h.setOptionValue("output_flag", False)
    h.setOptionValue("threads", 1)
    h.setOptionValue("primal_feasibility_tolerance", 1e-10)
    h.setOptionValue("dual_feasibility_tolerance", 1e-10)
    inf = highspy.kHighsInf
    cost = np.concatenate([I.c, np.ones(n), np.full(m, b)])
    lo = np.concatenate([l, np.full(n + m, -inf)])
    hi = np.concatenate([u, np.full(n + m, inf)])
    lp = highspy.HighsLp()
    lp.num_col_, lp.num_row_ = ncol, 0
    lp.col_cost_ = cost
    lp.col_lower_, lp.col_upper_ = lo, hi
    lp.a_matrix_.format_ = highspy.MatrixFormat.kColwise
    lp.a_matrix_.start_ = np.zeros(ncol + 1, dtype=np.int32)
    lp.a_matrix_.index_ = np.array([], dtype=np.int32)
    lp.a_matrix_.value_ = np.array([], float)
    h.passModel(lp)
    for e in range(m):
        i, j, we = e, e + 1, 2 * n + e
        if b > 0:
            h.addRow(-inf, l[i] * l[j], 3, np.array([we, i, j], dtype=np.int32), np.array([-1.0, l[j], l[i]]))
            h.addRow(-inf, u[i] * u[j], 3, np.array([we, i, j], dtype=np.int32), np.array([-1.0, u[j], u[i]]))
        else:
            h.addRow(-inf, -l[i] * u[j], 3, np.array([we, i, j], dtype=np.int32), np.array([1.0, -u[j], -l[i]]))
            h.addRow(-inf, -u[i] * l[j], 3, np.array([we, i, j], dtype=np.int32), np.array([1.0, -l[j], -u[i]]))

    def cut(i, p):      # tau_i >= g(p) + g'(p)(x_i - p)   <=>   g'(p) x_i - tau_i <= g'(p) p - g(p)
        h.addRow(-inf, dg(p) * p - g(p), 2, np.array([i, n + i], dtype=np.int32), np.array([dg(p), -1.0]))

    for i in range(n):
        for p in set(np.linspace(l[i], u[i], 9).tolist()) | {min(max(I.xstar[i], l[i]), u[i])}:
            cut(i, p)
    for _ in range(200):
        h.run()
        if h.getModelStatus() != highspy.HighsModelStatus.kOptimal:
            raise RuntimeError(f"HiGHS status {h.getModelStatus()}")
        sol = np.array(h.getSolution().col_value)
        x, tau = sol[:n], sol[n:2 * n]
        viol = g(x) - tau
        bad = np.nonzero(viol > 1e-10)[0]
        if len(bad) == 0:
            break
        for i in bad:
            cut(int(i), x[i])
    return float(cost @ sol), x, sol[2 * n:]


def _highs(ncol, nrow, cost, colL, colU, rlo, rhi, start, index, value, hst, hid, hva, tol):
    h = highspy.Highs()
    h.setOptionValue("output_flag", False)
    h.setOptionValue("threads", 1)
    h.setOptionValue("primal_feasibility_tolerance", tol)
    h.setOptionValue("dual_feasibility_tolerance", tol)
    lp = highspy.HighsLp()
    lp.num_col_, lp.num_row_ = ncol, nrow
    lp.col_cost_ = np.array(cost, float)
    lp.col_lower_, lp.col_upper_ = np.array(colL, float), np.array(colU, float)
    lp.row_lower_, lp.row_upper_ = np.array(rlo, float), np.array(rhi, float)
    lp.a_matrix_.format_ = highspy.MatrixFormat.kColwise
    lp.a_matrix_.start_ = np.array(start, dtype=np.int32)
    lp.a_matrix_.index_ = np.array(index, dtype=np.int32)
    lp.a_matrix_.value_ = np.array(value, float)
    model = highspy.HighsModel()
    model.lp_ = lp
    hs = highspy.HighsHessian()
    hs.dim_ = ncol
    hs.format_ = highspy.HessianFormat.kTriangular
    hs.start_ = np.array(hst, dtype=np.int32)
    hs.index_ = np.array(hid, dtype=np.int32)
    hs.value_ = np.array(hva, float)
    model.hessian_ = hs
    h.passModel(model)
    h.run()
    if h.getModelStatus() != highspy.HighsModelStatus.kOptimal:
        return None
    return h.getInfo().objective_function_value, np.array(h.getSolution().col_value)


def _clarabel(ncol, cost, colL, colU, start, index, value, rlo, rhi, hst, hid, hva):
    """Fallback for rare HiGHS QP failures: the same QP solved by Clarabel through cvxpy."""
    import cvxpy as cp
    Q = np.zeros((ncol, ncol))
    for q in range(ncol):
        for p in range(hst[q], hst[q + 1]):
            Q[hid[p], q] = Q[q, hid[p]] = hva[p]
    nrow = len(rlo)
    A = np.zeros((nrow, ncol))
    for q in range(ncol):
        for p in range(start[q], start[q + 1]):
            A[index[p], q] = value[p]
    z = cp.Variable(ncol)
    cons = []
    fin = np.isfinite(colL) & (np.array(colL) > -1e29)
    if fin.any():
        cons.append(z[fin] >= np.array(colL)[fin])
    fin = np.isfinite(colU) & (np.array(colU) < 1e29)
    if fin.any():
        cons.append(z[fin] <= np.array(colU)[fin])
    if nrow:
        cons.append(A @ z <= np.array(rhi))
    pr = cp.Problem(cp.Minimize(0.5 * cp.quad_form(z, cp.psd_wrap(Q)) + np.array(cost) @ z), cons)
    pr.solve(solver="CLARABEL", tol_gap_abs=1e-11, tol_gap_rel=1e-11, tol_feas=1e-11)
    if pr.status not in ("optimal", "optimal_inaccurate"):
        raise RuntimeError(f"HiGHS and Clarabel failed: {pr.status}")
    return pr.value, np.array(z.value)


# ---------------------------------------------------------------------------------------------
# Certified node bounds (added in the revision after review).  HiGHS's QP solver sometimes returns
# a point whose objective lies up to 1.5e-4 ABOVE the QP optimum (kappa = 0, c = 0).  Pruning on that
# value can prune invalid boxes.  The functions below give a lower bound that is valid by weak
# duality, whatever the solver returns, and an upper bound from a feasible point.  A node is pruned
# only if the certified lower bound is >= f* - eps.
#
#   mc / mcx:  F(x) = sum_i phi_i(x_i) + sum_e |b| max(P_e(x), Q_e(x)),  P_e, Q_e affine.
#     For lam in [0,1]^(n-1):  d(lam) = min_box [sum_i phi_i + sum_e |b| (lam_e P_e + (1-lam_e) Q_e)]
#     is <= min_box F (weak duality) and separable: one-dimensional convex minimisations.
#     d is concave and differentiable (phi_i strictly convex); dd/dlam_e = |b| (P_e - Q_e)(x(lam)).
#   abb:  F smooth convex on the box;  F(x) >= F(xh) + min_box grad F(xh).(x - xh)  (Frank-Wolfe bound).
# ---------------------------------------------------------------------------------------------

def _edge_affine(I, l, u):
    """Coefficients of P_e, Q_e (affine in x_i, x_j): arrays (ci, cj, c0) for P and for Q."""
    n, b = I.n, I.b
    i, j = np.arange(n - 1), np.arange(1, n)
    if b > 0:
        P = (l[j], l[i], -l[i] * l[j])
        Q = (u[j], u[i], -u[i] * u[j])
    else:   # b w with w <= min(U1, U2)  ->  |b| max(-U1, -U2)
        P = (-u[j], -l[i], l[i] * u[j])
        Q = (-l[j], -u[i], u[i] * l[j])
    return P, Q


def _phi_min(I, rel, l, u, a):
    """argmin and min over [l_i,u_i] of phi_i(x) + a_i x, vectorised; phi from the relaxation."""
    k = I.kappa
    if rel == "mc":
        slope = -k * (l + u) * (l * l + u * u)
        const = -k * l ** 4 - slope * l
        lin = I.c + slope + a
        x = np.clip(-lin / 2, l, u)
        return x, x * x + lin * x + const
    # mcx: phi = x^2 - kappa x^4 + c x, convex on [-1,1] for kappa <= 1/6; derivative increasing
    dphi = lambda x: 2 * x - 4 * k * x ** 3 + I.c + a
    lo, hi = l.copy(), u.copy()
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        pos = dphi(mid) > 0
        hi = np.where(pos, mid, hi)
        lo = np.where(pos, lo, mid)
    x = np.where(dphi(l) >= 0, l, np.where(dphi(u) <= 0, u, 0.5 * (lo + hi)))
    return x, x * x - k * x ** 4 + (I.c + a) * x


def _F(I, rel, l, u, x):
    """Relaxation objective of the node box [l,u] at a point x of the box (an upper bound on the node
    bound).  For mc the univariate part is x^2 + secant of -kappa x^4 on [l_i,u_i] + c x."""
    (Pi, Pj, P0), (Qi, Qj, Q0) = _edge_affine(I, l, u)
    P = Pi * x[:-1] + Pj * x[1:] + P0
    Q = Qi * x[:-1] + Qj * x[1:] + Q0
    k = I.kappa
    if rel == "mc":
        slope = -k * (l + u) * (l * l + u * u)
        phi = x * x + (I.c + slope) * x - k * l ** 4 - slope * l
    else:                                                  # mcx: exact g
        phi = x * x - k * x ** 4 + I.c * x
    return float(np.sum(phi) + abs(I.b) * np.sum(np.maximum(P, Q)))


def _dual(I, rel, l, u, lam):
    (Pi, Pj, P0), (Qi, Qj, Q0) = _edge_affine(I, l, u)
    bb = abs(I.b)
    a = np.zeros(I.n)
    a[:-1] += bb * (lam * Pi + (1 - lam) * Qi)
    a[1:] += bb * (lam * Pj + (1 - lam) * Qj)
    c0 = bb * np.sum(lam * P0 + (1 - lam) * Q0)
    x, vals = _phi_min(I, rel, l, u, a)
    val = float(np.sum(vals) + c0)
    grad = bb * ((Pi - Qi) * x[:-1] + (Pj - Qj) * x[1:] + (P0 - Q0))
    return val, x, grad


STATS = {"nodes": 0, "refined": 0, "ambiguous": 0, "highs_too_high": 0}
TIE = 1e-12   # prune iff certified LB >= f* - eps - TIE; absorbs rounding at exact ties (LB = f* - eps)


def certified(I, rel, l, u, thr, xh):
    """Certified (LB, UB) of the node relaxation, refined only when thr lies between them."""
    xh = np.clip(xh, l, u)
    if rel == "abb":
        a = alpha_abb(I.b)
        at = np.full(I.n, 2 * a); at[0] = at[-1] = a
        def Fg(x):
            v = np.sum(x * x + I.c * x) + I.b * np.sum(x[:-1] * x[1:]) - np.sum(at * (x - l) * (u - x))
            g = 2 * x + I.c - at * (l + u - 2 * x)
            g[:-1] += I.b * x[1:]; g[1:] += I.b * x[:-1]
            return float(v), g
        def fw(x):
            v, g = Fg(x)
            return v + float(np.sum(np.minimum(g * (l - x), g * (u - x)))), v
        lb, ub = fw(xh)
        if lb < thr <= ub:
            STATS["refined"] += 1
            r = optimize.minimize(lambda x: Fg(x), xh, jac=True, method="L-BFGS-B", bounds=list(zip(l, u)),
                                  options={"ftol": 1e-16, "gtol": 1e-13, "maxiter": 2000})
            lb2, ub2 = fw(np.clip(r.x, l, u))
            lb, ub = max(lb, lb2), min(ub, ub2)
        return lb, ub
    (Pi, Pj, P0), (Qi, Qj, Q0) = _edge_affine(I, l, u)
    P = Pi * xh[:-1] + Pj * xh[1:] + P0
    Q = Qi * xh[:-1] + Qj * xh[1:] + Q0
    lam0 = np.where(P > Q + 1e-9, 1.0, np.where(Q > P + 1e-9, 0.0, 0.5))
    lb, _, _ = _dual(I, rel, l, u, lam0)
    ub = _F(I, rel, l, u, xh)
    if lb < thr <= ub:
        STATS["refined"] += 1
        best = [lb, ub]
        def negd(lam):
            v, x, g = _dual(I, rel, l, u, lam)
            best[0] = max(best[0], v)
            best[1] = min(best[1], _F(I, rel, l, u, x))
            return -v, -g
        optimize.minimize(negd, lam0, jac=True, method="L-BFGS-B", bounds=[(0, 1)] * (I.n - 1),
                          options={"ftol": 1e-16, "gtol": 1e-14, "maxiter": 3000})
        lb, ub = best
        if lb < thr <= ub and rel == "mc":
            # fallback: multipliers from an interior-point solve (Clarabel) of the epigraph QP
            STATS["clarabel"] = STATS.get("clarabel", 0) + 1
            lam_c, x_c = _clarabel_multipliers(I, l, u)
            v, _, _ = _dual(I, rel, l, u, lam_c)
            lb, ub = max(lb, v), min(ub, _F(I, rel, l, u, x_c))
    return lb, ub


def _clarabel_multipliers(I, l, u):
    """Solve min sum_i phi_i(x_i) + |b| sum_e w_e, w_e >= P_e(x), w_e >= Q_e(x), x in [l,u] with Clarabel;
    return lambda_e = y_P/(y_P + y_Q) from the constraint multipliers, and the primal x (clipped)."""
    import cvxpy as cp
    n, k = I.n, I.kappa
    (Pi, Pj, P0), (Qi, Qj, Q0) = _edge_affine(I, l, u)
    slope = -k * (l + u) * (l * l + u * u)
    x = cp.Variable(n)
    w = cp.Variable(n - 1)
    cP = w >= cp.multiply(Pi, x[:-1]) + cp.multiply(Pj, x[1:]) + P0
    cQ = w >= cp.multiply(Qi, x[:-1]) + cp.multiply(Qj, x[1:]) + Q0
    obj = cp.sum_squares(x) + (I.c + slope) @ x + abs(I.b) * cp.sum(w)
    pr = cp.Problem(cp.Minimize(obj), [cP, cQ, x >= l, x <= u])
    pr.solve(solver="CLARABEL", tol_gap_abs=1e-12, tol_gap_rel=1e-12, tol_feas=1e-12)
    yP, yQ = np.maximum(np.asarray(cP.dual_value), 0), np.maximum(np.asarray(cQ.dual_value), 0)
    lam = np.where(yP + yQ > 0, yP / np.maximum(yP + yQ, 1e-300), 0.5)
    return np.clip(lam, 0, 1), np.clip(np.asarray(x.value), l, u)


# ---------------------------------------------------------------------------------------------
# Per-factor alphaBB with a box-dependent exact alpha, for two factorizations (revision after review):
#   abbU: PROGRAM factorization, f_i = g_i(x_i) + b x_i x_{i+1} (+ c_i x_i), f_n = g_n;
#   abbS: split factorization,   f_i = s_i g_i(x_i) + b x_i x_{i+1} + t_{i+1} g_{i+1}(x_{i+1}), with
#         g_1 and g_n wholly in the end factors and interior g_i split 1/2 : 1/2 (balanced).
# Factor Hessian [[p, b], [b, q]] with p >= p_min, q >= q_min on the box; lambda_min is increasing in
# p and q, so alpha = max(0, -lambda_min(p_min, q_min))/2 is valid on the box.  The relaxation
# f - sum_i A_i (x_i - l_i)(u_i - x_i) is smooth and convex; it is minimised by L-BFGS-B and bounded
# below by the Frank-Wolfe inequality.  Its gap dominates the per-factor envelope gap of the same
# factorization, so for bisection with UBD = f* its tree contains the envelope tree.
# ---------------------------------------------------------------------------------------------

def _split_weights(n, rel):
    sb = np.zeros(n); ta = np.zeros(n)          # share of g_i in factor i (sb) and in factor i-1 (ta)
    if rel == "abbU":
        sb[:] = 1.0
    else:
        sb[:] = 0.5; ta[:] = 0.5
        sb[0], ta[0] = 1.0, 0.0
        sb[-1], ta[-1] = 0.0, 1.0
        if n == 2:
            sb[0], ta[1] = 1.0, 1.0
    return sb, ta


def relax_split(I, rel, l, u, thr):
    n, b, k = I.n, I.b, I.kappa
    sb, ta = _split_weights(n, rel)
    gmin = 2 - 12 * k * np.maximum(l * l, u * u)          # min of g'' on [l_i, u_i]
    p, q = sb[:-1] * gmin[:-1], ta[1:] * gmin[1:]
    lam = (p + q) / 2 - np.sqrt(((p - q) / 2) ** 2 + b * b)
    alf = np.maximum(0.0, -lam) / 2
    A = np.zeros(n); A[:-1] += alf; A[1:] += alf
    def Fg(x):
        v = np.sum(x * x - k * x ** 4 + I.c * x) + b * np.sum(x[:-1] * x[1:]) - np.sum(A * (x - l) * (u - x))
        g = 2 * x - 4 * k * x ** 3 + I.c - A * (l + u - 2 * x)
        g[:-1] += b * x[1:]; g[1:] += b * x[:-1]
        return float(v), g
    def fw(x):
        v, g = Fg(x)
        return v + float(np.sum(np.minimum(g * (l - x), g * (u - x)))), v
    x0 = np.clip(I.xstar, l, u)
    r = optimize.minimize(Fg, x0, jac=True, method="L-BFGS-B", bounds=list(zip(l, u)),
                          options={"ftol": 1e-15, "gtol": 1e-12, "maxiter": 2000})
    xh = np.clip(r.x, l, u)
    lb, ub = fw(xh)
    if lb < thr <= ub:
        STATS["refined"] += 1
        r = optimize.minimize(Fg, xh, jac=True, method="L-BFGS-B", bounds=list(zip(l, u)),
                              options={"ftol": 0.0, "gtol": 1e-15, "maxiter": 20000, "maxcor": 30})
        xh2 = np.clip(r.x, l, u)
        lb2, ub2 = fw(xh2)
        lb, ub = max(lb, lb2), min(ub, ub2)
    return lb, ub, xh


def choose(I, rel, rule, l, u, xh, wh):
    w = u - l
    if rule == "oracle":
        inside = [i for i in range(I.n) if l[i] + 1e-9 * w[i] < I.xstar[i] < u[i] - 1e-9 * w[i]]
        if inside:
            i = max(inside, key=lambda q: (w[q], -q))
            return i, I.xstar[i]
        rule = "bisect"
    if rule == "bisect":
        i = int(np.argmax(w))
        return i, 0.5 * (l[i] + u[i])
    if rule in ("viol", "mid75", "vw", "vwlp"):
        sc = np.zeros(I.n)
        if rel in ("mc", "mcx"):
            for e in range(I.n - 1):
                v = abs(I.b) * abs(wh[e] - xh[e] * xh[e + 1])
                sc[e] += v; sc[e + 1] += v
            if rel == "mc":
                slope = -I.kappa * (l + u) * (l * l + u * u)
                sec = -I.kappa * l ** 4 + slope * (xh - l)
                sc += np.abs(-I.kappa * xh ** 4 - sec)
        else:
            a = alpha_abb(I.b)
            atot = np.full(I.n, 2 * a); atot[0] = atot[-1] = a
            sc = atot * (xh - l) * (u - xh)
        cand = [q for q in range(I.n) if w[q] > 0]
        if rule in ("vw", "vwlp"):
            viol_c = [q for q in cand if sc[q] > 1e-9 * max(sc.max(), 1e-300)]
            i = max(viol_c or cand, key=lambda q: (w[q], sc[q]))
        else:
            i = max(cand, key=lambda q: (sc[q], w[q]))
        p = xh[i] if rule in ("viol", "vwlp") else 0.75 * 0.5 * (l[i] + u[i]) + 0.25 * xh[i]
        p = min(max(p, l[i] + 0.2 * w[i]), u[i] - 0.2 * w[i])
        return i, p
    raise ValueError(rule)


def run(I, rel, rule, eps, node_limit=4_000_000, time_limit=3000, record=False):
    stack = [(I.lo.copy(), I.hi.copy())]
    nodes = leaves = 0
    fmin_seen = math.inf
    leafinfo = []
    t0 = time.time()
    while stack:
        l, u = stack.pop()
        nodes += 1
        thr = I.fstar - eps - TIE
        if rel in ("abbU", "abbS"):
            lb, ub, xh = relax_split(I, rel, l, u, thr)
            lb_solver, wh = lb, None
        else:
            lb_solver, xh, wh = relax(I, rel, l, u)
            lb, ub = certified(I, rel, l, u, thr, xh)
        STATS["nodes"] += 1
        if lb_solver >= thr > lb and ub >= thr:
            STATS["ambiguous"] += 1              # still undecided after refinement: not pruned
        if lb_solver > ub + 1e-9:
            STATS["highs_too_high"] += 1         # solver value above a feasible point's value
        fmin_seen = min(fmin_seen, I.f(xh))
        if lb >= thr:
            leaves += 1
            if record:
                dist = float(np.max(np.maximum(0, np.maximum(l - I.xstar, I.xstar - u))))
                leafinfo.append((float(np.max(u - l)), float(np.prod(u - l)), dist,
                                 float(np.max(np.maximum(np.abs(l - I.xstar), np.abs(u - I.xstar))))))
            continue
        if nodes >= node_limit or time.time() - t0 > time_limit:
            return dict(nodes=nodes, leaves=leaves, status="limit", time=time.time() - t0,
                        fmin_seen=fmin_seen, leafinfo=leafinfo)
        i, p = choose(I, rel, rule, l, u, xh, wh)
        u1 = u.copy(); u1[i] = p
        l2 = l.copy(); l2[i] = p
        stack.append((l2, u))
        stack.append((l, u1))
    return dict(nodes=nodes, leaves=leaves, status="done", time=time.time() - t0,
                fmin_seen=fmin_seen, leafinfo=leafinfo)


def main():
    rel, rule, kappa, cmode, eps = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4], float(sys.argv[5])
    for n in [int(a) for a in sys.argv[6:]]:
        I = Inst(n, kappa, cmode)
        r = run(I, rel, rule, eps)
        chk = "ok" if r["fmin_seen"] >= I.fstar - 1e-9 else f"LOWER POINT {r['fmin_seen']}"
        print(f"{rel} {rule} kappa={kappa} {cmode} eps={eps:.0e} n={n} nodes={r['nodes']} leaves={r['leaves']} "
              f"{r['status']} t={r['time']:.1f}s fstar={I.fstar:.8f} |x*|inf={np.max(np.abs(I.xstar)):.4f} {chk} "
              f"[certified bounds: refined={STATS['refined']} undecided={STATS['ambiguous']} "
              f"solver-too-high={STATS['highs_too_high']}]", flush=True)
        for key in STATS:
            STATS[key] = 0


if __name__ == "__main__":
    main()
