"""Example E2: a 2-D control-affine problem with a bang arc followed by an
order-1 singular arc, its Euler transcription, and calibration tests.

Continuous problem (q1 = q2 = 1, k2 = 1/4, gauge parameter k1):
  xdot1 = u, xdot2 = x1 - x2, u in [-1, 1], x(0) = (1, 0), T = 3,
  J = int_0^T [ (x1^2 + x2^2)/2 + (k1 x1 + k2 x2) u ] dt + x(T)^T F x(T)/2,
  F = diag(k2 - k1, q1 - 2 k2).
k1 enters only through the null Lagrangian k1 x1 u = d/dt (k1 x1^2/2),
compensated in F, so the continuous problem does not depend on k1.
Kelley quantity K = q1 - 2 k2 = 1/2, w = -(k1, k2), b = e1, b^T w = -k1.

Euler transcription: x_{t+1} = x_t + h (A x_t + b u_t), stage cost
h [ x^T x / 2 + (k^T x) u ], terminal x_N^T F x_N / 2, h = T/N.

This module provides: the float reduced QP, an exact rational KKT point for
a given active set (forward shooting in the two unknowns p_0), and the exact
stage quantities of Lemma 10 of extension-n2.md for quadratic families
S_t(x) = p_t^T x + (x - xbar_t)^T P_t (x - xbar_t)/2.
"""
from fractions import Fraction as Fr

import numpy as np

T = Fr(3)
Q = ((Fr(1), Fr(0)), (Fr(0), Fr(1)))
K2 = Fr(1, 4)
Q1 = Fr(1)
KELLEY = Q1 - 2 * K2
X0 = (Fr(1), Fr(0))


def data(k1, N):
    k1 = Fr(k1)
    h = T / N
    k = (k1, K2)
    Fm = ((K2 - k1, Fr(0)), (Fr(0), KELLEY))
    # F_x = I + h A, A = [[0,0],[1,-1]]
    Fx = ((Fr(1), Fr(0)), (h, 1 - h))
    return dict(k1=k1, N=N, h=h, k=k, F=Fm, Fx=Fx)


# ---------------- small exact 2x2 helpers ----------------
def mv(M, v):
    return (M[0][0] * v[0] + M[0][1] * v[1], M[1][0] * v[0] + M[1][1] * v[1])


def mtv(M, v):
    return (M[0][0] * v[0] + M[1][0] * v[1], M[0][1] * v[0] + M[1][1] * v[1])


def mm(A, B):
    return tuple(tuple(sum(A[i][l] * B[l][j] for l in range(2)) for j in range(2)) for i in range(2))


def tr(A):
    return ((A[0][0], A[1][0]), (A[0][1], A[1][1]))


def add(A, B, s=1):
    return tuple(tuple(A[i][j] + s * B[i][j] for j in range(2)) for i in range(2))


def scal(c, A):
    return tuple(tuple(c * A[i][j] for j in range(2)) for i in range(2))


def outer(a, b):
    return ((a[0] * b[0], a[0] * b[1]), (a[1] * b[0], a[1] * b[1]))


def psd2(M):
    """exact test M >= 0 for symmetric 2x2."""
    return M[0][0] >= 0 and M[1][1] >= 0 and M[0][0] * M[1][1] - M[0][1] * M[1][0] >= 0


# ---------------- float reduced QP ----------------
def float_qp(d, x0=(1.0, 0.0)):
    N = d["N"]
    h = float(d["h"])
    k = np.array([float(v) for v in d["k"]])
    Fm = np.array([[float(v) for v in r] for r in d["F"]])
    Fx = np.array([[float(v) for v in r] for r in d["Fx"]])
    b = np.array([1.0, 0.0])
    # x_t = Phi_t x0 + sum_{s<t} G_{t,s} u_s ; build via columns
    Phi = np.zeros((N + 1, 2, 2))
    Phi[0] = np.eye(2)
    for t in range(N):
        Phi[t + 1] = Fx @ Phi[t]
    # G[t, s] = Fx^{t-s-1} h b  for s < t
    Pw = np.zeros((N + 1, 2))
    Pw[0] = h * b
    for j in range(1, N + 1):
        Pw[j] = Fx @ Pw[j - 1]
    X0v = np.array(x0)
    xa = np.einsum("tij,j->ti", Phi, X0v)          # affine part (N+1, 2)
    # linear map: x_t = xa_t + sum_s Gts u_s, Gts = Pw[t-s-1]
    idx = np.arange(N + 1)[:, None] - np.arange(N)[None, :] - 1
    G = np.where(idx[..., None] >= 0, Pw[np.clip(idx, 0, N)], 0.0)  # (N+1, N, 2)
    # cost: sum_t h(x_t^T x_t/2 + k^T x_t u_t) + x_N^T F x_N / 2
    Gs = G[:N]
    Hq = h * np.einsum("tsi,tri->sr", Gs, Gs)
    kx = np.einsum("i,tsi->ts", k, Gs)              # k^T G_{t,s}  (N, N)
    Hq += h * (kx + kx.T)                           # bilinear term u_t k^T x_t
    GN = G[N]
    Hq += GN @ Fm @ GN.T
    gq = h * np.einsum("tsi,ti->s", Gs, xa[:N]) + h * (xa[:N] @ k) + GN @ Fm @ xa[N]
    c0 = 0.5 * h * np.sum(xa[:N] ** 2) + 0.5 * xa[N] @ Fm @ xa[N]
    return Hq, gq, c0


def solve_box_qp(Hq, gq, u0=None, iters=500):
    """projected Newton / active-set for min 1/2 u'Hu + g'u on [-1,1]^N;
    works for convex H; for nonconvex H returns a KKT point (local)."""
    N = len(gq)
    u = np.zeros(N) if u0 is None else u0.copy()
    for it in range(iters):
        gr = Hq @ u + gq
        act_lo = (u <= -1 + 1e-12) & (gr > 0)
        act_hi = (u >= 1 - 1e-12) & (gr < 0)
        free = ~(act_lo | act_hi)
        un = u.copy()
        un[act_lo] = -1.0
        un[act_hi] = 1.0
        if free.any():
            Hff = Hq[np.ix_(free, free)]
            rhs = -(gq[free] + Hq[np.ix_(free, ~free)] @ un[~free])
            try:
                uf = np.linalg.solve(Hff, rhs)
            except np.linalg.LinAlgError:
                uf = np.linalg.lstsq(Hff, rhs, rcond=None)[0]
            un[free] = uf
        # if Newton point infeasible, take projected step toward it
        if np.all(np.abs(un) <= 1 + 1e-14):
            if np.allclose(un, u, atol=1e-14, rtol=0):
                u = np.clip(un, -1, 1)
                break
            u = np.clip(un, -1, 1)
        else:
            # clip to box (projection); iterate
            u = np.clip(un, -1, 1)
    return u


def kkt_check_float(Hq, gq, u):
    gr = Hq @ u + gq
    viol = 0.0
    for ui, gi in zip(u, gr):
        if ui <= -1 + 1e-12:
            viol = max(viol, -gi)
        elif ui >= 1 - 1e-12:
            viol = max(viol, gi)
        else:
            viol = max(viol, abs(gi))
    return viol


# ---------------- exact KKT by forward shooting ----------------
def exact_kkt(d, status):
    """status[t] in {-1, +1, 0}: bound at -1, bound at +1, free (sigma_t = 0).
    Quantities are affine in the unknown p_0 = (a0, a1): stored as triples
    (c, c_a0, c_a1).  Returns exact x, u, p, sigma, J."""
    N, h, k, Fm, Fx = d["N"], d["h"], d["k"], d["F"], d["Fx"]
    # F_x^{-T}
    det = Fx[0][0] * Fx[1][1] - Fx[0][1] * Fx[1][0]
    FxT = tr(Fx)
    FxTi = ((FxT[1][1] / det, -FxT[0][1] / det), (-FxT[1][0] / det, FxT[0][0] / det))

    def A(c):  # affine const
        return (c, Fr(0), Fr(0))

    def lin(a, x, bb, y):  # a*x + bb*y for triples
        return tuple(a * xi + bb * yi for xi, yi in zip(x, y))

    def addt(x, y):
        return tuple(xi + yi for xi, yi in zip(x, y))

    def sc(a, x):
        return tuple(a * xi for xi in x)

    x = [(A(X0[0]), A(X0[1]))]
    p = [((Fr(0), Fr(1), Fr(0)), (Fr(0), Fr(0), Fr(1)))]
    u = []
    for t in range(N):
        xt, pt = x[t], p[t]
        # r = p_t - h Q x_t  (Q = I)
        r = (addt(pt[0], sc(-h, xt[0])), addt(pt[1], sc(-h, xt[1])))
        # p_{t+1} = FxTi (r - h k u)
        if status[t] == 0:
            # sigma_t = k.x_t + b.p_{t+1} = k.x_t + (FxTi r)_0 - h (FxTi k)_0 u = 0
            FrR0 = addt(sc(FxTi[0][0], r[0]), sc(FxTi[0][1], r[1]))
            Fk0 = FxTi[0][0] * k[0] + FxTi[0][1] * k[1]
            num = addt(addt(sc(k[0], xt[0]), sc(k[1], xt[1])), FrR0)
            ut = sc(1 / (h * Fk0), num)
        else:
            ut = A(Fr(status[t]))
        u.append(ut)
        rr = (addt(r[0], sc(-h * k[0], ut)), addt(r[1], sc(-h * k[1], ut)))
        pn = (addt(sc(FxTi[0][0], rr[0]), sc(FxTi[0][1], rr[1])),
              addt(sc(FxTi[1][0], rr[0]), sc(FxTi[1][1], rr[1])))
        p.append(pn)
        xn = (addt(sc(Fx[0][0], xt[0]), sc(Fx[0][1], xt[1])),
              addt(addt(sc(Fx[1][0], xt[0]), sc(Fx[1][1], xt[1])), (Fr(0), Fr(0), Fr(0))))
        xn = (addt(xn[0], sc(h, ut)), xn[1])
        x.append(xn)
    # terminal p_N = F x_N
    e0 = addt(p[N][0], sc(-1, addt(sc(Fm[0][0], x[N][0]), sc(Fm[0][1], x[N][1]))))
    e1 = addt(p[N][1], sc(-1, addt(sc(Fm[1][0], x[N][0]), sc(Fm[1][1], x[N][1]))))
    # solve e0 = e1 = 0 for (a0, a1)
    M = ((e0[1], e0[2]), (e1[1], e1[2]))
    rhs = (-e0[0], -e1[0])
    dm = M[0][0] * M[1][1] - M[0][1] * M[1][0]
    a0 = (rhs[0] * M[1][1] - M[0][1] * rhs[1]) / dm
    a1 = (M[0][0] * rhs[1] - M[1][0] * rhs[0]) / dm

    def ev(z):
        return z[0] + z[1] * a0 + z[2] * a1

    X = [(ev(xi[0]), ev(xi[1])) for xi in x]
    P = [(ev(pi[0]), ev(pi[1])) for pi in p]
    U = [ev(ui) for ui in u]
    sig = [k[0] * X[t][0] + k[1] * X[t][1] + P[t + 1][0] for t in range(N)]
    J = sum(h * ((X[t][0] ** 2 + X[t][1] ** 2) / 2 + (k[0] * X[t][0] + k[1] * X[t][1]) * U[t])
            for t in range(N))
    J += (Fm[0][0] * X[N][0] ** 2 + 2 * Fm[0][1] * X[N][0] * X[N][1] + Fm[1][1] * X[N][1] ** 2) / 2
    ok = True
    for t in range(N):
        if status[t] == -1:
            ok &= sig[t] >= 0
        elif status[t] == 1:
            ok &= sig[t] <= 0
        else:
            ok &= (-1 <= U[t] <= 1)
    return dict(x=X, p=P, u=U, sigma=sig, J=J, kkt_ok=ok)


# ---------------- stage quantities (exact) ----------------
def stage_terms(d, Pn, Pt):
    """For S_{t+1} Hessian Pn and S_t Hessian Pt: K_t, beta_t, kappa_t."""
    h, k, Fx = d["h"], d["k"], d["Fx"]
    Kt = add(add(scal(h, Q), mm(tr(Fx), mm(Pn, Fx))), Pt, -1)
    Pnb = (Pn[0][0], Pn[1][0])
    FtPb = mtv(Fx, Pnb)
    beta = (FtPb[0] + k[0], FtPb[1] + k[1])  # F_x^T P b - w, w = -k
    kappa = Pn[0][0]
    return Kt, beta, kappa


def stage_exact(d, Kt, beta, kappa, sigma, status, Delta=Fr(2)):
    """Lemma 10 of extension-n2.md (exactness over R^2 x U)."""
    h = d["h"]
    if status == 0:
        m = kappa
    else:
        m = 2 * abs(sigma) / (h * Delta) + kappa
    if m > 0:
        return psd2(add(Kt, scal(1 / m, outer(beta, beta)), -1)), m
    if m == 0:
        return (beta == (0, 0) and psd2(Kt)), m
    return False, m


def stage_loss_float(h, Kt, beta, kappa, sigma, ubar, status, ulo=-1.0, uhi=1.0):
    """inf over (d, omega) in R^2 x [ulo-ubar, uhi-ubar] of
    h sigma w + h w beta.d + d'Kd/2 + h^2 kappa w^2/2 (value at 0 is 0)."""
    K = np.array([[float(v) for v in r] for r in Kt])
    be = np.array([float(v) for v in beta])
    ev = np.linalg.eigvalsh(K)
    if ev[0] <= 0:
        # K not PD: if beta not in range or ev<0, unbounded over R^2
        if ev[0] < -1e-15 * max(1, abs(ev[-1])):
            return -np.inf
    Kinv_b = np.linalg.solve(K, be) if ev[0] > 0 else np.linalg.lstsq(K, be, rcond=None)[0]
    c2 = 0.5 * h * h * (float(kappa) - be @ Kinv_b)
    c1 = h * float(sigma)
    lo, hi = ulo - float(ubar), uhi - float(ubar)
    cands = [lo, hi, 0.0]
    if c2 > 0:
        wst = -c1 / (2 * c2)
        if lo < wst < hi:
            cands.append(wst)
    return min(c1 * w + c2 * w * w for w in cands)
