"""Stronger convex relaxations of L0-constrained ridge regression (cvxpy models).

Problem:  OPT = min_{|S| <= k} f(S),  f(S) = min_b ||y - X_S b||^2 + lam ||b||^2.
Lifted variables: z (indicators), beta, B (proxy for beta beta').  Common objective
    y'y - 2 y'X beta + <X'X + lam I, B>.
Node fixings: z[S0] = 0, z[S1] = 1.

Models (all return the optimal value, a float, or None on solver failure):
  persp   : perspective relaxation (Clarabel, residual form; from ../../code/core.py)
  sdp1    : optimal perspective = Shor + perspective (Dong-Chen-Linderoth; Atamturk-Gomez sdp_1)
            [[1, beta'], [beta, B]] >= 0,  beta_i^2 <= z_i B_ii.
            spart=True adds the spartrahedron constraint k Diag(B) >= B (Cifuentes-Li).
  sdp2    : Atamturk-Gomez rank-one sdp_2: sdp1 plus, for every pair T = {i, j},
            0 <= w_T <= min(1, z_i + z_j),  [[w_T, beta_T'], [beta_T, B_T]] >= 0.
  L2      : exact lifted pairwise hull: sdp1 plus, for every pair, (z_T, beta_T, B_T) in
            cl conv{(zeta, b, b b') : zeta in {0,1}^2, b_i = 0 if zeta_i = 0}
            (disjunctive form with 4 pattern blocks and a PSD recession term).
  zb      : degree-2 moment relaxation in (zeta, beta) with RLT and product cones:
            Y = [[1, z', beta'], [z, Z, U], [beta, U', B]] >= 0, diag Z = z, diag U = beta,
            McCormick on Z, sum z <= k, Z 1 <= k z, and U_jm^2 <= Z_jm B_mm (j != m).
"""
import os, sys
for v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    os.environ.setdefault(v, "1")
import numpy as np
import cvxpy as cp
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message="Solution may be inaccurate")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "code"))
from core import instance, ridge, solve_node, dual_bound  # noqa: E402


SCS_OPTS = dict(eps=1e-7, max_iters=200000)


def _solve(prob, solver="CLARABEL"):
    try:
        if solver == "CLARABEL":
            prob.solve(solver=cp.CLARABEL, tol_gap_abs=1e-9, tol_gap_rel=1e-9, tol_feas=1e-9,
                       max_iter=400)
        else:
            prob.solve(solver=cp.SCS, **SCS_OPTS)
    except Exception:
        try:
            prob.solve(solver=cp.SCS, eps=1e-7, max_iters=200000)
        except Exception:
            return None
    if prob.status not in ("optimal", "optimal_inaccurate"):
        return None
    return float(prob.value)


def _base(X, y, lam, k, S0, S1):
    n, p = X.shape
    Q = X.T @ X + lam * np.eye(p)
    c = X.T @ y
    beta = cp.Variable(p)
    B = cp.Variable((p, p), symmetric=True)
    z = cp.Variable(p)
    one = np.ones((1, 1))
    M = cp.bmat([[one, cp.reshape(beta, (1, p), order="C")],
                 [cp.reshape(beta, (p, 1), order="C"), B]])
    cons = [M >> 0, z >= 0, z <= 1, cp.sum(z) <= k]
    dB = cp.diag(B)
    # perspective: beta_i^2 <= z_i B_ii  (rotated cone)
    cons.append(cp.SOC(z + dB, cp.vstack([2 * beta, z - dB]), axis=0))
    if len(S0):
        cons += [z[list(S0)] == 0]
    if len(S1):
        cons += [z[list(S1)] == 1]
    obj = float(y @ y) - 2 * c @ beta + cp.sum(cp.multiply(Q, B))
    return beta, B, z, cons, obj


def sdp1(X, y, lam, k, S0=(), S1=(), spart=False, solver="CLARABEL"):
    beta, B, z, cons, obj = _base(X, y, lam, k, S0, S1)
    if spart:
        cons.append(k * cp.diag(cp.diag(B)) - B >> 0)
    return _solve(cp.Problem(cp.Minimize(obj), cons), solver)


def _pairs(p):
    I, J = np.triu_indices(p, 1)
    return I, J


def sdp2(X, y, lam, k, S0=(), S1=(), solver="CLARABEL"):
    """Atamturk-Gomez sdp_2 (rank-one strengthening on all pairs)."""
    p = X.shape[1]
    beta, B, z, cons, obj = _base(X, y, lam, k, S0, S1)
    I, J = _pairs(p)
    w = cp.Variable(len(I))
    cons += [w >= 0, w <= 1, w <= z[I] + z[J]]
    for t, (i, j) in enumerate(zip(I, J)):
        Mt = cp.bmat([[cp.reshape(w[t], (1, 1)), cp.reshape(beta[i], (1, 1)), cp.reshape(beta[j], (1, 1))],
                      [cp.reshape(beta[i], (1, 1)), cp.reshape(B[i, i], (1, 1)), cp.reshape(B[i, j], (1, 1))],
                      [cp.reshape(beta[j], (1, 1)), cp.reshape(B[i, j], (1, 1)), cp.reshape(B[j, j], (1, 1))]])
        cons.append(Mt >> 0)
    return _solve(cp.Problem(cp.Minimize(obj), cons), solver)


def L2(X, y, lam, k, S0=(), S1=(), solver="CLARABEL"):
    """Exact lifted pairwise hull on every pair {i, j} (free-sign coefficients).
    Pattern blocks (moment matrices on {0} u pattern):
      P10: [[l10, u_i], [u_i, s_i]] >= 0,  P01: [[l01, v_j], [v_j, t_j]] >= 0,
      P11: 3x3 [[l11, g_i, g_j], [g_i, h_ii, h_ij], [g_j, h_ij, h_jj]] >= 0,  l00 >= 0,
      l00 + l10 + l01 + l11 = 1, z_i = l10 + l11, z_j = l01 + l11,
      beta_i = u_i + g_i, beta_j = v_j + g_j,
      [[B_ii - s_i - h_ii, B_ij - h_ij], [B_ij - h_ij, B_jj - t_j - h_jj]] >= 0 (recession)."""
    p = X.shape[1]
    beta, B, z, cons, obj = _base(X, y, lam, k, S0, S1)
    I, J = _pairs(p)
    m = len(I)
    l11 = cp.Variable(m)
    u = cp.Variable(m); s = cp.Variable(m); v = cp.Variable(m); tt = cp.Variable(m)
    g1 = cp.Variable(m); g2 = cp.Variable(m); h11 = cp.Variable(m); h12 = cp.Variable(m); h22 = cp.Variable(m)
    l10 = z[I] - l11
    l01 = z[J] - l11
    l00 = 1 - z[I] - z[J] + l11
    cons += [l11 >= 0, l10 >= 0, l01 >= 0, l00 >= 0]
    # 2x2 PSD as rotated cones: u^2 <= l10 s
    cons.append(cp.SOC(l10 + s, cp.vstack([2 * u, l10 - s]), axis=0))
    cons.append(cp.SOC(l01 + tt, cp.vstack([2 * v, l01 - tt]), axis=0))
    cons += [beta[I] == u + g1, beta[J] == v + g2]
    for t in range(m):
        i, j = I[t], J[t]
        P11 = cp.bmat([[cp.reshape(l11[t], (1, 1)), cp.reshape(g1[t], (1, 1)), cp.reshape(g2[t], (1, 1))],
                       [cp.reshape(g1[t], (1, 1)), cp.reshape(h11[t], (1, 1)), cp.reshape(h12[t], (1, 1))],
                       [cp.reshape(g2[t], (1, 1)), cp.reshape(h12[t], (1, 1)), cp.reshape(h22[t], (1, 1))]])
        cons.append(P11 >> 0)
        R = cp.bmat([[cp.reshape(B[i, i] - s[t] - h11[t], (1, 1)), cp.reshape(B[i, j] - h12[t], (1, 1))],
                     [cp.reshape(B[i, j] - h12[t], (1, 1)), cp.reshape(B[j, j] - tt[t] - h22[t], (1, 1))]])
        cons.append(R >> 0)
    return _solve(cp.Problem(cp.Minimize(obj), cons), solver)


def zb(X, y, lam, k, S0=(), S1=(), solver="CLARABEL", product_cones=True, rlt=True):
    """Degree-2 moment relaxation in (zeta, beta) with RLT and U_jm^2 <= Z_jm B_mm."""
    n, p = X.shape
    Q = X.T @ X + lam * np.eye(p)
    c = X.T @ y
    Y = cp.Variable((2 * p + 1, 2 * p + 1), symmetric=True)
    z = Y[0, 1:p + 1]
    beta = Y[0, p + 1:]
    Z = Y[1:p + 1, 1:p + 1]
    U = Y[1:p + 1, p + 1:]
    B = Y[p + 1:, p + 1:]
    cons = [Y >> 0, Y[0, 0] == 1, cp.diag(Z) == z, cp.diag(U) == beta,
            z >= 0, z <= 1, cp.sum(z) <= k]
    if rlt:
        ones = np.ones(p)
        cons += [Z >= 0, Z <= cp.reshape(z, (p, 1), order="C") @ ones[None, :],
                 Z >= cp.reshape(z, (p, 1), order="C") @ ones[None, :] + ones[:, None] @ cp.reshape(z, (1, p), order="C") - 1,
                 Z @ ones <= k * z]
    if product_cones:
        I, J = np.nonzero(~np.eye(p, dtype=bool))
        # U[j, m]^2 <= Z[j, m] * B[m, m]  for j != m (flatten in C order)
        Uv = cp.vec(U, order="C")[I * p + J]
        Zv = cp.vec(Z, order="C")[I * p + J]
        Bm = cp.diag(B)[J]
        cons.append(cp.SOC(Zv + Bm, cp.vstack([2 * Uv, Zv - Bm]), axis=0))
    if len(S0):
        cons += [z[list(S0)] == 0]
    if len(S1):
        cons += [z[list(S1)] == 1]
    obj = float(y @ y) - 2 * c @ beta + cp.sum(cp.multiply(Q, B))
    return _solve(cp.Problem(cp.Minimize(obj), cons), solver)


def persp(X, y, lam, k, S0=(), S1=()):
    """Perspective node relaxation: (certified dual bound, primal value)."""
    LB, val, z, a = solve_node(X, y, lam, k, S0, S1, tol=1e-10)
    return LB, val


MODELS = {"sdp1": sdp1, "sdp2": sdp2, "L2": L2, "zb": zb,
          "spart": lambda X, y, lam, k, S0=(), S1=(): sdp1(X, y, lam, k, S0, S1, spart=True)}
