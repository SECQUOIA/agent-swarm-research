"""Toy spatial branch-and-bound with termwise McCormick relaxations (workstream spatial-face-exact).

Problem class (lifted form):
    min  c.x + sum_e coef_e * w_e + sum_k L_k |a_k.x - b_k| + 0.5 x'Qx      (Q PSD, optional)
    s.t. w_e = x_i x_j                                                          (bilinear terms)
         rlo <= A [x; w] <= rhi                                               (optional linear rows)
         x in box.
Node relaxation: every w_e = x_i x_j replaced by its four McCormick inequalities on the node box
(the convex/concave envelope pair), abs terms modelled exactly with auxiliary s_k, Q kept exactly.
Solved as an LP/QP with HiGHS (one thread, tight tolerances).

Incumbent fixed at the known optimal value fstar; a node is pruned iff LB >= fstar - eps, so the
processed set does not depend on node order.  Floating-point illustration, not a certified count.

Branching rules (only variables that occur in bilinear terms are branched on):
  bisect            widest candidate variable, midpoint
  xonly             variable 0 only, midpoint (for 2D illustrations)
  R(alpha,beta,sel) point = clamp(alpha*xhat + (1-alpha)*mid, [l+beta*w, u-beta*w])
                    (Speakman-Lee parametrisation: SCIP (1,.2), ANTIGONE (.75,.1),
                     BARON (.7,.01), COUENNE (.25,.2)); variable selection sel in
                     'widest' (widest variable of a violated term),
                     'viol'   (largest summed term violation, ties -> wider),
                     'central'(variable of a violated term whose xhat is most central),
                     'strong' (among variables of violated terms, maximise min child LB).
"""
import math
import numpy as np
import highspy

INF = highspy.kHighsInf


class Problem:
    def __init__(self, name, lo, hi, c=None, terms=(), absterms=(), Q=None, rows=None,
                 fstar=0.0, const=0.0):
        self.name = name
        self.lo = np.array(lo, float)
        self.hi = np.array(hi, float)
        self.n = len(self.lo)
        self.c = np.zeros(self.n) if c is None else np.array(c, float)
        self.terms = [(int(i), int(j), float(v)) for (i, j, v) in terms]   # coef * x_i x_j
        self.absterms = [(np.array(a, float), float(b), float(L)) for (a, b, L) in absterms]
        self.Q = None if Q is None else np.array(Q, float)
        # rows: (A (r x (n+m)), rlo, rhi)
        self.rows = rows
        self.fstar = float(fstar)
        self.const = float(const)
        self.cand = sorted({i for (i, j, _) in self.terms} | {j for (i, j, _) in self.terms})

    def f(self, x):
        v = self.const + self.c @ x
        for (i, j, cf) in self.terms:
            v += cf * x[i] * x[j]
        for (a, b, L) in self.absterms:
            v += L * abs(a @ x - b)
        if self.Q is not None:
            v += 0.5 * x @ self.Q @ x
        return v


def relax(P, l, u, want_sol=True):
    """Solve the McCormick relaxation on box [l,u].  Returns (LB, xhat, what) or (inf, None, None)."""
    if getattr(P, "custom_relax", None) is not None:      # exact closed-form node bound (tilt family)
        return P.custom_relax(l, u)
    n, m, k = P.n, len(P.terms), len(P.absterms)
    ncol = n + m + k
    cost = np.zeros(ncol)
    cost[:n] = P.c
    colL = np.empty(ncol)
    colU = np.empty(ncol)
    colL[:n], colU[:n] = l, u
    rows_idx, rows_val, rlo, rhi = [], [], [], []

    def addrow(idx, val, lo_, hi_):
        rows_idx.append(idx); rows_val.append(val); rlo.append(lo_); rhi.append(hi_)

    for e, (i, j, cf) in enumerate(P.terms):
        we = n + e
        cost[we] = cf
        li, ui, lj, uj = l[i], u[i], l[j], u[j]
        prods = (li * lj, li * uj, ui * lj, ui * uj)
        colL[we], colU[we] = min(prods), max(prods)
        # w >= lj xi + li xj - li lj ;  w >= uj xi + ui xj - ui uj
        addrow([we, i, j], [-1.0, lj, li], -INF, li * lj)
        addrow([we, i, j], [-1.0, uj, ui], -INF, ui * uj)
        # w <= uj xi + li xj - li uj ;  w <= lj xi + ui xj - ui lj
        addrow([we, i, j], [1.0, -uj, -li], -INF, -li * uj)
        addrow([we, i, j], [1.0, -lj, -ui], -INF, -ui * lj)
    for t, (a, b, L) in enumerate(P.absterms):
        st = n + m + t
        cost[st] = L
        colL[st], colU[st] = 0.0, INF
        nz = np.nonzero(a)[0].tolist()
        addrow(nz + [st], [a[q] for q in nz] + [-1.0], -INF, b)
        addrow(nz + [st], [-a[q] for q in nz] + [-1.0], -INF, -b)
    if P.rows is not None:
        A, lo_, hi_ = P.rows
        for r in range(A.shape[0]):
            nz = np.nonzero(A[r])[0].tolist()
            addrow(nz, [A[r, q] for q in nz], lo_[r], hi_[r])
    # column-wise matrix
    nrow = len(rlo)
    cols = [[] for _ in range(ncol)]
    for r in range(nrow):
        for q, v in zip(rows_idx[r], rows_val[r]):
            cols[q].append((r, v))
    start, index, value = [0], [], []
    for q in range(ncol):
        for (r, v) in cols[q]:
            index.append(r); value.append(v)
        start.append(len(index))
    for tol in (1e-10, 1e-8, 1e-7):   # HiGHS QP occasionally reports kSolveError at 1e-10; retry looser
        res = _solve(P, n, m, ncol, nrow, cost, colL, colU, rlo, rhi, start, index, value, tol)
        if res is not None:
            return res
    return _solve_clarabel(P, n, m, ncol, cost, colL, colU, rows_idx, rows_val, rlo, rhi)


def _solve_clarabel(P, n, m, ncol, cost, colL, colU, rows_idx, rows_val, rlo, rhi):
    """Fallback for rare HiGHS QP failures: same model solved by Clarabel (interior point, tol 1e-10)."""
    import cvxpy as cp
    z = cp.Variable(ncol)
    cons = []
    for q in range(ncol):
        if colL[q] > -INF:
            cons.append(z[q] >= colL[q])
        if colU[q] < INF:
            cons.append(z[q] <= colU[q])
    for idx, val, lo_, hi_ in zip(rows_idx, rows_val, rlo, rhi):
        expr = sum(v * z[q] for q, v in zip(idx, val))
        if lo_ > -1e29:
            cons.append(expr >= lo_)
        if hi_ < 1e29:
            cons.append(expr <= hi_)
    obj = cost @ z
    if P.Q is not None:
        obj = obj + 0.5 * cp.quad_form(z[:n], cp.psd_wrap(P.Q))
    pr = cp.Problem(cp.Minimize(obj), cons)
    pr.solve(solver="CLARABEL", tol_gap_abs=1e-11, tol_gap_rel=1e-11, tol_feas=1e-11)
    if pr.status == "infeasible":
        return math.inf, None, None
    if pr.status not in ("optimal", "optimal_inaccurate"):
        raise RuntimeError(f"HiGHS and Clarabel failed: {pr.status}")
    sol = np.array(z.value)
    return pr.value + P.const, sol[:n], sol[n:n + m]


def _solve(P, n, m, ncol, nrow, cost, colL, colU, rlo, rhi, start, index, value, tol):
    h = highspy.Highs()
    h.setOptionValue("output_flag", False)
    h.setOptionValue("threads", 1)
    h.setOptionValue("primal_feasibility_tolerance", tol)
    h.setOptionValue("dual_feasibility_tolerance", tol)
    h.setOptionValue("time_limit", 5.0)       # guard against rare QP stalls; falls through to a retry
    lp = highspy.HighsLp()
    lp.num_col_, lp.num_row_ = ncol, nrow
    lp.col_cost_ = cost
    lp.col_lower_, lp.col_upper_ = colL, colU
    lp.row_lower_, lp.row_upper_ = np.array(rlo, float), np.array(rhi, float)
    lp.a_matrix_.format_ = highspy.MatrixFormat.kColwise
    lp.a_matrix_.start_ = np.array(start, dtype=np.int32)
    lp.a_matrix_.index_ = np.array(index, dtype=np.int32)
    lp.a_matrix_.value_ = np.array(value, float)
    if P.Q is not None:
        model = highspy.HighsModel()
        model.lp_ = lp
        hs = highspy.HighsHessian()
        hs.dim_ = ncol
        hs.format_ = highspy.HessianFormat.kTriangular
        hst, hid, hva = [0], [], []
        for q in range(ncol):
            if q < n:
                for r in range(q, n):
                    if P.Q[r, q] != 0.0:
                        hid.append(r); hva.append(P.Q[r, q])
            hst.append(len(hid))
        hs.start_ = np.array(hst, dtype=np.int32)
        hs.index_ = np.array(hid, dtype=np.int32)
        hs.value_ = np.array(hva, float)
        model.hessian_ = hs
        h.passModel(model)
    else:
        h.passModel(lp)
    h.run()
    st = h.getModelStatus()
    if st == highspy.HighsModelStatus.kInfeasible:
        return math.inf, None, None
    if st != highspy.HighsModelStatus.kOptimal:
        return None
    val = h.getInfo().objective_function_value + P.const
    sol = np.array(h.getSolution().col_value)
    return val, sol[:n], sol[n:n + m]


def violations(P, xhat, what):
    # terms with coefficient 0 define lifted variables used only in constraints (pooling): weight 1
    return [(abs(cf) if cf != 0 else 1.0) * abs(what[e] - xhat[i] * xhat[j]) for e, (i, j, cf) in enumerate(P.terms)]


def choose(P, rule, l, u, xhat, what, eps):
    w = (u - l) / (P.hi - P.lo)      # widths relative to the root box (identical on [0,1]^n)
    cand = [i for i in P.cand if w[i] > 0]
    if rule == "bisect":
        i = max(cand, key=lambda q: (w[q], -q))
        return i, 0.5 * (l[i] + u[i])
    if rule == "xonly":
        return 0, 0.5 * (l[0] + u[0])
    kind, alpha, beta, sel = rule
    viol = violations(P, xhat, what)
    vmax = max(viol) if viol else 0.0
    vc = sorted({q for e, (i, j, _) in enumerate(P.terms) if viol[e] > 1e-12 * max(1.0, vmax)
                 for q in (i, j) if w[q] > 0}) or cand

    def point(i):
        mid = 0.5 * (l[i] + u[i])
        wi = u[i] - l[i]
        if kind == "INC":
            # incumbent branching (Shectman-Sahinidis; BARON as described by Tawarmalani-Sahinidis 2002
            # p.243): split at the incumbent's coordinate if it lies strictly inside the interval,
            # otherwise bisect.  P.xstar is an optimal point (the incumbent in the fixed-UBD model).
            xs = P.xstar[i]
            return xs if l[i] + 1e-12 * wi < xs < u[i] - 1e-12 * wi else mid
        a = alpha
        if kind == "Rscip":
            # SCIP 10 default: point = midpull_B*mid + (1-midpull_B)*xhat, midpull_B = midpull times the
            # relative domain width r if r < midpullreldomtrig (0.5); then clamp (beta = branching/clamp)
            midpull = alpha
            if w[i] < 0.5:
                midpull *= w[i]
            a = 1.0 - midpull
        p = a * xhat[i] + (1 - a) * mid
        return min(max(p, l[i] + beta * wi), u[i] - beta * wi)

    if sel == "widest":
        i = max(vc, key=lambda q: (w[q], -q))
    elif sel == "x":
        i = 0
    elif sel == "viol":
        score = {q: 0.0 for q in vc}
        for e, (a, b, _) in enumerate(P.terms):
            for q in (a, b):
                if q in score:
                    score[q] += viol[e]
        i = max(vc, key=lambda q: (round(score[q] / max(vmax, 1e-300), 9), w[q], -q))
    elif sel == "central":
        i = max(vc, key=lambda q: (round(min(xhat[q] - l[q], u[q] - xhat[q]) / (u[q] - l[q]), 9), w[q], -q))
    elif sel in ("strong", "strongp"):
        # strong branching: 'strong' maximises the smaller child bound (min score),
        # 'strongp' maximises the product of the two bound gains (SCIP-style product score)
        lb0 = relax(P, l, u)[0]
        best, i = -math.inf, vc[0]
        for q in vc:
            p = point(q)
            l1, u1 = l.copy(), u.copy(); u1[q] = p
            l2, u2 = l.copy(), u.copy(); l2[q] = p
            b1, b2 = relax(P, l1, u1)[0], relax(P, l2, u2)[0]
            if sel == "strong":
                s = min(b1, b2)
            else:
                g1 = min(b1 - lb0, 1e6); g2 = min(b2 - lb0, 1e6)
                s = max(g1, 1e-9) * max(g2, 1e-9)
            if s > best * (1 + 1e-9) + 1e-15:
                best, i = s, q
    else:
        raise ValueError(sel)
    return i, point(i)


def run(P, eps, rule, max_nodes=200000, record=False):
    """Number of processed nodes (relaxations solved at tree nodes), or None if max_nodes exceeded."""
    stack = [(P.lo.copy(), P.hi.copy())]
    nodes = 0
    leaves = []
    while stack:
        l, u = stack.pop()
        nodes += 1
        if nodes > max_nodes:
            return None
        lb, xhat, what = relax(P, l, u)
        if lb >= P.fstar - eps:
            if record:
                leaves.append((l, u))
            continue
        i, p = choose(P, rule, l, u, xhat, what, eps)
        if not (l[i] < p < u[i]):
            p = 0.5 * (l[i] + u[i])
        l1, u1 = l.copy(), u.copy(); u1[i] = p
        l2, u2 = l.copy(), u.copy(); l2[i] = p
        stack.append((l2, u2)); stack.append((l1, u1))
    return (nodes, leaves) if record else nodes


RULES = {
    "bisect": "bisect",
    "xonly": "xonly",
    "SCIP(1,.2)w": ("R", 1.0, 0.2, "widest"),
    "SCIP(1,.2)c": ("R", 1.0, 0.2, "central"),
    "ANTIG(.75,.1)w": ("R", 0.75, 0.1, "widest"),
    "BARON(.7,.01)w": ("R", 0.7, 0.01, "widest"),
    "COUEN(.25,.2)w": ("R", 0.25, 0.2, "widest"),
    "COUEN(.25,.2)c": ("R", 0.25, 0.2, "central"),
    "SCIP(1,.2)s": ("R", 1.0, 0.2, "strong"),
    "COUEN(.25,.2)s": ("R", 0.25, 0.2, "strong"),
    "SCIP(1,.2)sp": ("R", 1.0, 0.2, "strongp"),
    "COUEN(.25,.2)sp": ("R", 0.25, 0.2, "strongp"),
}
# Labels used after the review (2026-09-29).  "SCIP(1,.2)" above is NOT SCIP's default: it is the
# relaxation (LP) point with clamp 0.2, i.e. SCIP with branching/midpull = 0.  The names ANTIG/BARON/
# COUEN above denote only the (alpha, beta) values of formula (1) in Speakman-Lee, not those solvers.
RULES.update({
    "LP(1,.2)w": ("R", 1.0, 0.2, "widest"),
    "LP(1,.2)x": ("R", 1.0, 0.2, "x"),
    "LP(1,.2)sp": ("R", 1.0, 0.2, "strongp"),
    "LP(1,0)w": ("R", 1.0, 0.0, "widest"),
    "R(.25,.2)w": ("R", 0.25, 0.2, "widest"),
    "SCIPdef w": ("Rscip", 0.75, 0.2, "widest"),     # SCIP 10 defaults: midpull .75, reldomtrig .5, clamp .2
    "SCIPdef x": ("Rscip", 0.75, 0.2, "x"),
    "SCIPdef sp": ("Rscip", 0.75, 0.2, "strongp"),
    "INC w": ("INC", None, None, "widest"),
})
LABEL = {"SCIP(1,.2)w": "LP(1,.2)w", "SCIP(1,.2)c": "LP(1,.2)c", "SCIP(1,.2)s": "LP(1,.2)s",
         "SCIP(1,.2)sp": "LP(1,.2)sp", "ANTIG(.75,.1)w": "R(.75,.1)w", "BARON(.7,.01)w": "R(.7,.01)w",
         "COUEN(.25,.2)w": "R(.25,.2)w", "COUEN(.25,.2)c": "R(.25,.2)c", "COUEN(.25,.2)s": "R(.25,.2)s",
         "COUEN(.25,.2)sp": "R(.25,.2)sp"}
