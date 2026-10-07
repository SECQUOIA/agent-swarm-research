"""Binary least squares  min ||y - A x||^2,  x in {-1,+1}^N,  with the box
relaxation x in [-1,1]^N and variable fixings.

Model (same generator as the scout's bls.py, so seeds are comparable):
    H in R^{M x N} iid N(0,1),  A = sqrt(rho/N) H,  x* uniform in {-1,1}^N,
    w ~ N(0, I_M),  y = A x* + w.

Everything is computed in the "error coordinates" of the note:
    b_i = x*_i a_i  (B = A diag(x*)),   u_i = 1 - x*_i x_i in [0, 2],
    y - A x = w + B u.
u_i = 0 is the correct value, u_i = 2 the wrong one.  A node fixes some u_i to
0 or 2; its relaxation is  min ||v + B_free u||^2,  u in [0,2]^free,  where
v = w + B_fixed u_fixed.

Node solver: NNLS (upper bounds dropped); if the NNLS solution has an entry
> 2, fall back to BVLS.  Every value is returned together with a certified
Frank-Wolfe lower bound  val + sum_j min_{t in [0,2]} g_j (t - u_j).
"""
import numpy as np
from scipy.optimize import nnls, lsq_linear


def instance(N, M, rho, seed):
    rng = np.random.default_rng(seed)
    H = rng.standard_normal((M, N))
    A = np.sqrt(rho / N) * H
    xs = rng.choice([-1.0, 1.0], N)
    y = A @ xs + rng.standard_normal(M)
    w = y - A @ xs
    B = A * xs
    return A, y, xs, B, w


def _box_active_set(Bf, v, u0, iters=30, tol=1e-10):
    """Upper-bound active set on top of NNLS: fix U = {u_j at 2}, solve NNLS
    on the rest, release j in U whose gradient says it wants to decrease,
    add new violators; stop at a KKT point.  Falls back to BVLS.  Only the
    tightness of the returned bound depends on reaching the optimum; the FW
    certificate computed by the caller is valid at any feasible point."""
    k = Bf.shape[1]
    U = u0 > 2.0
    for _ in range(iters):
        rest = ~U
        vv = v + 2.0 * Bf[:, U].sum(axis=1)
        u = np.full(k, 2.0)
        if rest.any():
            ur, _ = nnls(Bf[:, rest], -vv, maxiter=50 * k + 100)
            u[rest] = ur
        over = u > 2.0
        g = 2.0 * (Bf.T @ (v + Bf @ np.minimum(u, 2.0)))
        release = U & (g > tol * (1.0 + np.abs(g).max()))
        if not over.any() and not release.any():
            return u
        U = (U & ~release) | over
    r = lsq_linear(Bf, -v, bounds=(0.0, 2.0), method="bvls", tol=1e-13)
    return np.clip(r.x, 0.0, 2.0)


def box_min(Bf, v):
    """min ||v + Bf u||^2 over u in [0,2]^k.  Returns (val, lb, u, inactive)."""
    k = Bf.shape[1]
    if k == 0:
        val = float(v @ v)
        return val, val, np.zeros(0), True
    u, _ = nnls(Bf, -v, maxiter=50 * k + 100)
    inactive = bool(u.max(initial=0.0) <= 2.0)
    if not inactive:
        u = _box_active_set(Bf, v, u)
    res = v + Bf @ u
    val = float(res @ res)
    g = 2.0 * (Bf.T @ res)
    # FW / Lagrangian certificate: f(u') >= f(u) + g.(u' - u) for u' in box
    lb = val + float(np.sum(np.minimum(-g * u, g * (2.0 - u))))
    return val, lb, u, inactive


def node(B, w, fixed):
    """fixed: dict i -> 0 or 2 (u-value).  Returns (val, lb, ufull, inactive)."""
    N = B.shape[1]
    fi = np.array(sorted(fixed), dtype=int)
    free = np.setdiff1d(np.arange(N), fi)
    v = w.copy()
    if len(fi):
        uf = np.array([fixed[i] for i in fi], dtype=float)
        v = v + B[:, fi] @ uf
    val, lb, u, ina = box_min(B[:, free], v)
    ufull = np.zeros(N)
    if len(fi):
        ufull[fi] = [fixed[i] for i in fi]
    ufull[free] = u
    return val, lb, ufull, ina


def fval_u(B, w, u):
    r = w + B @ u
    return float(r @ r)


def single_fixings(B, w):
    """Relaxation values of the N single-wrong-fixing nodes u_i = 2.
    Returns arrays (val, lb, inactive)."""
    N = B.shape[1]
    vals = np.empty(N); lbs = np.empty(N); ina = np.empty(N, bool)
    for i in range(N):
        v = w + 2.0 * B[:, i]
        Bf = np.delete(B, i, axis=1)
        vals[i], lbs[i], _, ina[i] = box_min(Bf, v)
    return vals, lbs, ina


def bnb(B, w, rule="maxfrac", max_nodes=10**6, rtol=1e-9, UB0=None):
    """Best-first variable-branching B&B on the box relaxation.
    Incumbent: x* (u = 0) unless UB0 given; improved by rounding.
    rule: 'maxfrac' (u_j closest to 1, i.e. x_j closest to 0) or
          'static' (smallest free index).
    Returns dict(nodes, OPT, done, uopt)."""
    import heapq
    N = B.shape[1]
    UB = fval_u(B, w, np.zeros(N)) if UB0 is None else UB0
    ubest = np.zeros(N)
    heap = [(-np.inf, 0, {})]
    tie = 1
    nodes = 0
    while heap:
        plb, _, fx = heapq.heappop(heap)
        if plb >= UB - rtol * abs(UB):
            continue
        nodes += 1
        if nodes > max_nodes:
            return dict(nodes=nodes, OPT=UB, done=False, uopt=ubest)
        val, lb, u, _ = node(B, w, fx)
        ur = np.where(u > 1.0, 2.0, 0.0)
        vr = fval_u(B, w, ur)
        if vr < UB:
            UB, ubest = vr, ur
        if lb >= UB - rtol * abs(UB):
            continue
        free = [j for j in range(N) if j not in fx]
        if not free:
            continue
        if rule == "maxfrac":
            j = min(free, key=lambda t: abs(1.0 - u[t]))
        else:
            j = free[0]
        for val_j in (0.0, 2.0):
            f2 = dict(fx); f2[j] = val_j
            heapq.heappush(heap, (lb, tie, f2)); tie += 1
    return dict(nodes=nodes, OPT=UB, done=True, uopt=ubest)


def sdp_certificate_eig(A, xs, w):
    """lambda_min(A'A + diag(x* o A'w)).  >= 0 iff the SDP relaxation
    certifies x* (Section 7 of the note)."""
    zeta = xs * (A.T @ w)
    Mx = A.T @ A + np.diag(zeta)
    return float(np.linalg.eigvalsh(Mx)[0])


def sdp_value(A, y):
    """Shor SDP bound: min <Q, X>, X psd, diag X = 1, Q = [[A'A, -A'y],[-y'A, y'y]]."""
    import cvxpy as cp
    N = A.shape[1]
    Q = np.zeros((N + 1, N + 1))
    Q[:N, :N] = A.T @ A
    Q[:N, N] = -A.T @ y
    Q[N, :N] = -A.T @ y
    Q[N, N] = y @ y
    X = cp.Variable((N + 1, N + 1), PSD=True)
    prob = cp.Problem(cp.Minimize(cp.trace(Q @ X)), [cp.diag(X) == 1])
    prob.solve(solver=cp.CLARABEL)
    # certified lower bound from the dual: sum(lambda) with Q - diag(lambda)
    # shifted to be psd
    # cvxpy returns the multiplier of diag(X) == 1 with the opposite sign
    lam = -np.asarray(prob.constraints[0].dual_value).ravel()
    S = Q - np.diag(lam)
    emin = np.linalg.eigvalsh(S)[0]
    lb = float(lam.sum() + (N + 1) * min(emin, 0.0))
    return float(prob.value), lb
