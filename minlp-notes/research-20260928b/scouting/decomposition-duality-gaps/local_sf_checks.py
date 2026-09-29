"""Exact small computations for the 'local Shapley-Folkman' question.

Scratch code for the decomposition-duality-gaps scouting report.  Every
problem below is small and solved exactly by HiGHS (LP by dual simplex so that
the convexified solution is a vertex; MILP for the original problem).

Checks
  A. Path coupling, domain-nonconvex binary blocks: Lagrangian dual (computed
     directly as max_lambda L(lambda)) vs integer optimum.  Gap grows linearly
     in the number m of coupling rows although every row touches 2 blocks and
     every block touches <= 2 rows (degree 2, treewidth 1).
  B. Same coupling, convex domains, nonconvex (concave) costs: the
     Udell-Boyd setting.  Gap again Theta(m).
  C. Parity chain: exactly one fractional block at the convexified optimum,
     yet the exact-feasibility gap is n/2.
  D. Random sparse incidence structures, tent costs: the true gap is at most
     the rho-weighted bipartite matching number nu_rho(G) of the block-row
     incidence graph, which can be far below the Udell-Boyd count; the
     tightness construction attains nu_rho(G).
  E. Transport network with fixed-charge generators: at an optimal LP vertex
     the number of fractional generators is at most the number of connected
     components of the graph of strictly uncongested lines.
"""
import itertools
import numpy as np
from scipy.optimize import linprog, milp, LinearConstraint, Bounds, linear_sum_assignment

TOL = 1e-7


def lp_vertex(c, A_ub=None, b_ub=None, A_eq=None, b_eq=None, bounds=None):
    r = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs-ds")
    assert r.status == 0, r.message
    return r.fun, r.x


def solve_milp(c, A, lb_rows, ub_rows, lb, ub, integrality):
    r = milp(c, constraints=[LinearConstraint(A, lb_rows, ub_rows)],
             bounds=Bounds(lb, ub), integrality=integrality)
    assert r.status == 0, r.message
    return r.fun, r.x


# ---------------------------------------------------------------- A
def check_A(n):
    """Blocks x_i in {0,1}, cost 1; rows 2x_i + 2x_{i+1} >= 1, i=1..n-1 (path)."""
    m = n - 1
    # Lagrangian dual: max_{lam>=0} sum_j lam_j + sum_i min(0, 1 - 2 sum_{j ni i} lam_j).
    # Variables (lam_1..lam_m, u_1..u_n): maximize sum lam + sum u, u_i <= 0,
    # u_i <= 1 - 2 sum_{j ni i} lam_j.  This is exactly max L(lambda).
    nv = m + n
    c = -np.r_[np.ones(m), np.ones(n)]
    A = np.zeros((n, nv)); b = np.ones(n)
    for i in range(n):
        A[i, m + i] = 1.0
        for j in (i - 1, i):
            if 0 <= j < m:
                A[i, j] = 2.0
    bounds = [(0, None)] * m + [(None, 0)] * n
    dual, _ = lp_vertex(c, A, b, bounds=bounds)
    dual = -dual
    # integer optimum
    Ar = np.zeros((m, n))
    for j in range(m):
        Ar[j, j] = Ar[j, j + 1] = 2.0
    p, _ = solve_milp(np.ones(n), Ar, np.ones(m), np.full(m, np.inf), np.zeros(n), np.ones(n), np.ones(n))
    return m, dual, p


# ---------------------------------------------------------------- B
def check_B(n, K=8.0):
    """x_i in [0,1], f_i(x)=min(Kx,1) (concave, rho=1-1/K), rows x_i+x_{i+1} >= 1/2."""
    m = n - 1
    Ar = np.zeros((m, n))
    for j in range(m):
        Ar[j, j] = Ar[j, j + 1] = 1.0
    # convexified: f** = x on [0,1]
    conv, x = lp_vertex(np.ones(n), -Ar, -0.5 * np.ones(m), bounds=[(0, 1)] * n)
    # original: variables x (n), t (n), z (n binary)
    N = 3 * n
    c = np.r_[np.zeros(n), np.ones(n), np.zeros(n)]
    rows, lo, hi = [], [], []
    for j in range(m):
        r = np.zeros(N); r[j] = r[j + 1] = 1.0; rows.append(r); lo.append(0.5); hi.append(np.inf)
    for i in range(n):
        r = np.zeros(N); r[n + i] = 1; r[i] = -K; r[2 * n + i] = -K; rows.append(r); lo.append(-K); hi.append(np.inf)
        r = np.zeros(N); r[n + i] = 1; r[2 * n + i] = 1; rows.append(r); lo.append(1.0); hi.append(np.inf)
    p, _ = solve_milp(c, np.array(rows), lo, hi, np.zeros(N), np.r_[np.ones(n), np.full(n, np.inf), np.ones(n)],
                      np.r_[np.zeros(2 * n), np.ones(n)])
    nfrac = int(np.sum((x > TOL) & (x < 1 - TOL)))
    return m, conv, p, nfrac, 1 - 1 / K


# ---------------------------------------------------------------- C
def check_C(n):
    """Parity chain: x_1..x_n in {0,1}, y in {0,1}; rows x_i + x_{i+1} = 1,
    x_n + 2y = 1; costs -1 on odd x_i.  n even."""
    assert n % 2 == 0
    N = n + 1
    c = np.zeros(N)
    c[0:n:2] = -1.0
    rows, rhs = [], []
    for i in range(n - 1):
        r = np.zeros(N); r[i] = r[i + 1] = 1; rows.append(r); rhs.append(1.0)
    r = np.zeros(N); r[n - 1] = 1; r[n] = 2; rows.append(r); rhs.append(1.0)
    A = np.array(rows); b = np.array(rhs)
    conv, x = lp_vertex(c, A_eq=A, b_eq=b, bounds=[(0, 1)] * N)  # blocks are single binaries: dual = LP
    p, _ = solve_milp(c, A, b, b, np.zeros(N), np.ones(N), np.ones(N))
    nfrac = int(np.sum((x > TOL) & (x < 1 - TOL)))
    # perturbed problem: relax only the y-row to 0 <= x_n + 2y <= 2
    lo = b.copy(); hi = b.copy(); lo[-1] = 0; hi[-1] = 2
    p_pert, _ = solve_milp(c, A, lo, hi, np.zeros(N), np.ones(N), np.ones(N))
    return conv, p, nfrac, p_pert


# ---------------------------------------------------------------- D
def max_weight_matching(inc, rho):
    """inc: bool matrix rows x blocks; weight rho_i on edge (j,i)."""
    W = np.where(inc, rho[None, :], 0.0)
    r, c = linear_sum_assignment(W, maximize=True)
    return float(W[r, c].sum())


def tent_instance_solve(Aeq, beq, Aub, bub, rho, cost):
    """min sum_i rho_i*(1-|2x_i-1|) + cost_i x_i on [0,1]^n with linear rows.
    Returns (convexified value, LP vertex, original value)."""
    n = len(rho)
    conv, x = lp_vertex(cost, Aub, bub, Aeq, beq, bounds=[(0, 1)] * n)
    # original: tent = min(2 rho x, 2 rho (1-x)); t_i >= 2rho x - 2rho z ; t_i >= 2 rho (1-x) - 2 rho (1 - z)
    N = 3 * n
    c = np.r_[cost, np.ones(n), np.zeros(n)]
    rows, lo, hi = [], [], []
    for A, b, eq in ((Aeq, beq, True), (Aub, bub, False)):
        if A is None:
            continue
        for j in range(A.shape[0]):
            r = np.zeros(N); r[:n] = A[j]; rows.append(r); lo.append(b[j] if eq else -np.inf); hi.append(b[j])
    for i in range(n):
        r = np.zeros(N); r[n + i] = 1; r[i] = -2 * rho[i]; r[2 * n + i] = 2 * rho[i]; rows.append(r); lo.append(0); hi.append(np.inf)
        r = np.zeros(N); r[n + i] = 1; r[i] = 2 * rho[i]; r[2 * n + i] = -2 * rho[i]; rows.append(r); lo.append(0); hi.append(np.inf)
    p, _ = solve_milp(c, np.array(rows), lo, hi, np.zeros(N), np.r_[np.ones(n), np.full(n, np.inf), np.ones(n)],
                      np.r_[np.zeros(2 * n), np.ones(n)])
    return conv, x, p


def check_D_random(rng, n=14, m=10, deg=2):
    """Random rows each touching `deg` blocks; heterogeneous rho."""
    inc = np.zeros((m, n), dtype=bool)
    for j in range(m):
        inc[j, rng.choice(n, deg, replace=False)] = True
    A = np.where(inc, rng.uniform(0.5, 1.5, (m, n)) * rng.choice([-1, 1], (m, n)), 0.0)
    x0 = rng.uniform(0.2, 0.8, n)
    b = A @ x0 + rng.uniform(0, 0.05, m)          # feasible, tight-ish
    rho = np.exp(rng.normal(0, 1.0, n))          # heterogeneous nonconvexities
    cost = rng.normal(0, 1.0, n)
    conv, x, p = tent_instance_solve(None, None, A, b, rho, cost)
    frac = (x > TOL) & (x < 1 - TOL)
    active = np.abs(A @ x - b) < 1e-6
    nu_all = max_weight_matching(inc, rho)
    nu_act = max_weight_matching(inc[active], rho) if active.any() else 0.0
    ub = float(np.sort(rho)[::-1][:min(int(active.sum()), n)].sum())   # Udell-Boyd count with active rows
    return p - conv, float(rho[frac].sum()), nu_act, nu_all, ub, int(frac.sum()), int(active.sum())


def check_D_tight(rng, n=12, m=9, deg=3, eps=0.05):
    """Tightness construction attaining nu_rho(G)."""
    inc = np.zeros((m, n), dtype=bool)
    for j in range(m):
        inc[j, rng.choice(n, deg, replace=False)] = True
    rho = np.exp(rng.normal(0, 1.0, n))
    W = np.where(inc, rho[None, :], 0.0)
    rr, cc = linear_sum_assignment(W, maximize=True)
    match = [(j, i) for j, i in zip(rr, cc) if inc[j, i]]
    B = {i for _, i in match}
    rowsB = {j for j, _ in match}
    A = np.where(inc, eps, 0.0)
    for j, i in match:
        A[j, i] = 1.0
    ub_blocks = np.array([1.0 if i in B else 0.0 for i in range(n)])  # unmatched blocks fixed at 0
    xstar = 0.5 * ub_blocks
    Aeq = A[sorted(rowsB)]
    beq = Aeq @ xstar
    others = [j for j in range(m) if j not in rowsB]
    Aub = A[others] if others else None
    bub = (A[others] @ xstar + 10.0) if others else None   # inactive rows
    n_ = n
    # fix unmatched blocks to 0 through bounds: emulate by equality rows
    fix = np.zeros((n_ - len(B), n_))
    for k, i in enumerate(sorted(set(range(n_)) - B)):
        fix[k, i] = 1.0
    Aeq2 = np.vstack([Aeq, fix]); beq2 = np.r_[beq, np.zeros(len(fix))]
    conv, x, p = tent_instance_solve(Aeq2, beq2, Aub, bub, rho, np.zeros(n_))
    return p - conv, max_weight_matching(inc, rho)


# ---------------------------------------------------------------- E
def check_E(n_side, cap, F=10.0, P=3.0, rng=None):
    """Grid transport network n_side x n_side; generator at each node with
    cost F*1{p>0} + c_v p on [0,P]; demand d_v; lines with capacity cap."""
    V = [(a, b) for a in range(n_side) for b in range(n_side)]
    idx = {v: k for k, v in enumerate(V)}
    E = [(idx[(a, b)], idx[(a + 1, b)]) for a in range(n_side - 1) for b in range(n_side)] + \
        [(idx[(a, b)], idx[(a, b + 1)]) for a in range(n_side) for b in range(n_side - 1)]
    nV, nE = len(V), len(E)
    cvar = rng.uniform(1.0, 2.0, nV)
    d = rng.uniform(0.2, 1.0, nV)
    # variables: p (nV), phi (nE)  -- convexified: cost (F/P + c) p
    A = np.zeros((nV, nV + nE))
    for v in range(nV):
        A[v, v] = 1.0
    for e, (u, w) in enumerate(E):
        A[u, nV + e] -= 1.0
        A[w, nV + e] += 1.0
    cost = np.r_[F / P + cvar, np.zeros(nE)]
    bounds = [(0, P)] * nV + [(-cap, cap)] * nE
    conv, x = lp_vertex(cost, A_eq=A, b_eq=d, bounds=bounds)
    p = x[:nV]; phi = x[nV:]
    frac = int(np.sum((p > TOL) & (p < P - TOL)))
    unc = [E[e] for e in range(nE) if abs(phi[e]) < cap - TOL]
    # components of (V, uncongested lines)
    parent = list(range(nV))
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    for (u, w) in unc:
        parent[find(u)] = find(w)
    comps = len({find(v) for v in range(nV)})
    # original MILP: p, phi, z (binary on/off)
    N = nV + nE + nV
    Am = np.zeros((nV + nV, N)); lo = np.r_[d, np.full(nV, -np.inf)]; hi = np.r_[d, np.zeros(nV)]
    Am[:nV, :nV + nE] = A
    for v in range(nV):
        Am[nV + v, v] = 1.0; Am[nV + v, nV + nE + v] = -P      # p <= P z
    cm = np.r_[cvar, np.zeros(nE), np.full(nV, F)]
    pm, _ = solve_milp(cm, Am, lo, hi, np.r_[np.zeros(nV), np.full(nE, -cap), np.zeros(nV)],
                       np.r_[np.full(nV, P), np.full(nE, cap), np.ones(nV)], np.r_[np.zeros(nV + nE), np.ones(nV)])
    return nV, pm - conv, frac, comps, len(unc), nE


if __name__ == "__main__":
    print("A. path, binary blocks, rows 2x_i+2x_{i+1}>=1: (m, dual, primal, gap, gap/m)")
    for n in (5, 9, 17, 33, 65):
        m, dval, p = check_A(n)
        print(f"   m={m:3d} dual={dval:7.3f} primal={p:5.1f} gap={p - dval:7.3f} gap/m={(p - dval) / m:.3f}")

    print("B. path, x in [0,1], f=min(8x,1): (m, conv, orig, gap, #frac, UB bound m*rho)")
    for n in (5, 9, 17, 33):
        m, cv, p, nf, rho = check_B(n)
        print(f"   m={m:3d} conv={cv:7.3f} orig={p:7.3f} gap={p - cv:7.3f} frac={nf:3d} m*rho={m * rho:7.3f}")

    print("C. parity chain: (n, LP=dual, integer opt, gap, #fractional blocks, opt with y-row relaxed)")
    for n in (4, 8, 16, 32, 64):
        cv, p, nf, pp = check_C(n)
        print(f"   n={n:3d} dual={cv:7.2f} primal={p:6.2f} gap={p - cv:6.2f} frac={nf} perturbed_opt={pp:6.2f}")

    print("D. random sparse incidence (deg 2), tent costs, heterogeneous rho:")
    rng = np.random.default_rng(1)
    viol = 0; rows = []
    for trial in range(200):
        gap, rfrac, nu_act, nu_all, ub, nf, na = check_D_random(rng)
        rows.append((gap, rfrac, nu_act, nu_all, ub))
        if gap > rfrac + 1e-6 or rfrac > nu_act + 1e-6:
            viol += 1
    R = np.array(rows)
    print(f"   200 instances: violations of gap<=sum_frac rho<=nu_rho(active G): {viol}")
    print(f"   mean gap={R[:, 0].mean():.3f}  mean sum_frac rho={R[:, 1].mean():.3f}  mean nu_act={R[:, 2].mean():.3f}"
          f"  mean UdellBoyd(active)={R[:, 4].mean():.3f}  ratio nu_act/UB={np.mean(R[:, 2] / np.maximum(R[:, 4], 1e-9)):.3f}")
    tight = [check_D_tight(rng) for _ in range(20)]
    print("   tightness construction (gap, nu_rho):", [(round(g, 4), round(v, 4)) for g, v in tight[:5]],
          " max |gap-nu| =", max(abs(g - v) for g, v in tight))

    print("E. grid transport network, fixed-charge generators: (nodes, cap, gap, #frac, #comp(uncongested), #uncongested/#lines)")
    rng = np.random.default_rng(7)
    for side in (3, 4, 5, 6):
        for cap in (100.0, 0.6, 0.3, 0.1):
            nV, gap, fr, comps, nu, nE = check_E(side, cap, rng=rng)
            flag = "OK" if fr <= comps else "VIOLATION"
            print(f"   nodes={nV:3d} cap={cap:6.1f} gap={gap:7.3f} frac={fr:3d} comps={comps:3d} unc={nu:3d}/{nE:3d} {flag}")
