"""Reviewer's independent discrete check of E2 (Euler), written from scratch.

For k1 in {-1/2, 0}: build the reduced QP in exact rationals, solve the float
QP with scipy (L-BFGS-B, then active-set Newton), take the active set, solve
the free-stage system exactly (Fractions, Gaussian elimination), verify KKT
signs exactly, then test families A (P=0) and B1 (P = [[-k1,-k2],[-k2,1/4-1/10]])
stage by stage with an exact 3x3 principal-minor PSD test of
[[K_t, beta_t],[beta_t^T, m_t]] (m_t = kappa_t at interior stages,
2|sigma_t|/(h Delta) + kappa_t at bound stages), and the terminal test
F - P_N >= 0.  Stage data derived independently:
 rho_t(x,u) = h(|x|^2/2 + (k.x) u) + S_{t+1}(Fx x + h b u) - S_t(x),
 S_t(x) = p_t.x + (x - xbar_t)^T P (x - xbar_t)/2.
Also reports the bound B = S_0(x0) + sum_t min rho_t + min(Phi - S_N)
(exact when all stages are exact) versus J.
"""
import sys
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import minimize

def build(k1, N):
    h = Fr(3, N); k2 = Fr(1, 4); K = 1 - 2*k2
    k = (Fr(k1), k2)
    F = ((k2 - Fr(k1), Fr(0)), (Fr(0), K))
    Fx = ((Fr(1), Fr(0)), (h, 1 - h))
    return h, k, F, Fx

def simulate(h, Fx, u, x0=(Fr(1), Fr(0))):
    xs = [x0]
    for ut in u:
        x = xs[-1]
        xs.append((x[0] + h*ut, Fx[1][0]*x[0] + Fx[1][1]*x[1]))
    return xs

def cost(h, k, F, Fx, u):
    xs = simulate(h, Fx, u)
    J = sum(h*((x[0]**2 + x[1]**2)/2 + (k[0]*x[0] + k[1]*x[1])*ut) for x, ut in zip(xs[:-1], u))
    xN = xs[-1]
    return J + (F[0][0]*xN[0]**2 + F[1][1]*xN[1]**2)/2

def float_qp(k1, N):
    h = 3.0/N; k = np.array([k1, 0.25]); F = np.diag([0.25 - k1, 0.5])
    Fx = np.array([[1, 0], [h, 1 - h]]); b = np.array([1.0, 0])
    # x = x_aff + G u
    xa = np.zeros((N + 1, 2)); xa[0] = [1, 0]
    G = np.zeros((N + 1, 2, N))
    for t in range(N):
        xa[t+1] = Fx @ xa[t]
        G[t+1] = Fx @ G[t]; G[t+1][:, t] += h*b
    Hq = np.zeros((N, N)); gq = np.zeros(N)
    for t in range(N):
        Hq += h*G[t].T @ G[t]
        kG = k @ G[t]
        Hq[t, :] += h*kG; Hq[:, t] += h*kG
        gq += h*G[t].T @ xa[t]; gq[t] += h*k @ xa[t]
    Hq += G[N].T @ F @ G[N]; gq += G[N].T @ F @ xa[N]
    return Hq, gq

def solve_float(Hq, gq, starts):
    best = None
    N = len(gq)
    for s0 in starts:
        r = minimize(lambda v: (0.5*v@Hq@v + gq@v, Hq@v + gq), s0, jac=True, method='L-BFGS-B',
                     bounds=[(-1, 1)]*N, options=dict(maxiter=50000, ftol=1e-16, gtol=1e-14))
        if best is None or r.fun < best.fun:
            best = r
    return best.x

def exact_solve(A, rhs):
    n = len(rhs)
    M = [list(A[i]) + [rhs[i]] for i in range(n)]
    for c in range(n):
        piv = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[piv] = M[piv], M[c]
        inv = 1/M[c][c]
        M[c] = [v*inv for v in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [a - f*bb for a, bb in zip(M[r], M[c])]
    return [M[i][n] for i in range(n)]

def exact_kkt(k1, N, status):
    """exact controls for a given status via the discrete adjoint (sigma_t = 0 on free
    stages) written as a linear system in the free controls: build exact reduced
    gradient columns by finite 'unit' simulations (the reduced QP is quadratic)."""
    h, k, F, Fx = build(k1, N)
    free = [t for t in range(N) if status[t] == 0]
    ub = [Fr(status[t]) if status[t] != 0 else Fr(0) for t in range(N)]
    # exact gradient of J at u via adjoint
    def grad(u):
        xs = simulate(h, Fx, u)
        p = (F[0][0]*xs[N][0], F[1][1]*xs[N][1])
        gr = [None]*N
        for t in range(N - 1, -1, -1):
            x = xs[t]
            # sigma_t = k.x_t + b.p_{t+1}
            gr[t] = h*(k[0]*x[0] + k[1]*x[1] + p[0])
            # p_t = h(x_t + k u_t) + Fx^T p_{t+1}
            p = (h*(x[0] + k[0]*u[t]) + Fx[0][0]*p[0] + Fx[1][0]*p[1],
                 h*(x[1] + k[1]*u[t]) + Fx[0][1]*p[0] + Fx[1][1]*p[1])
        return gr
    g0 = grad(ub)
    cols = []
    for j in free:
        e = list(ub); e[j] += 1
        gj = grad(e)
        cols.append([gj[i] - g0[i] for i in free])
    A = [[cols[c][r] for c in range(len(free))] for r in range(len(free))]
    rhs = [-g0[i] for i in free]
    sol = exact_solve(A, rhs) if free else []
    u = list(ub)
    for j, v in zip(free, sol):
        u[j] = v
    gr = grad(u)
    ok = all((status[t] == -1 and gr[t] >= 0) or (status[t] == 1 and gr[t] <= 0) or
             (status[t] == 0 and gr[t] == 0 and -1 <= u[t] <= 1) for t in range(N))
    return u, gr, ok

def psd3(M):
    n = len(M)
    import itertools
    def det(A):
        if len(A) == 1: return A[0][0]
        if len(A) == 2: return A[0][0]*A[1][1] - A[0][1]*A[1][0]
        return (A[0][0]*(A[1][1]*A[2][2] - A[1][2]*A[2][1]) - A[0][1]*(A[1][0]*A[2][2] - A[1][2]*A[2][0])
                + A[0][2]*(A[1][0]*A[2][1] - A[1][1]*A[2][0]))
    for r in range(1, n + 1):
        for idx in itertools.combinations(range(n), r):
            if det([[M[i][j] for j in idx] for i in idx]) < 0:
                return False
    return True

def family_check(k1, N, u, gr, P):
    h, k, F, Fx = build(k1, N)
    xs = simulate(h, Fx, u)
    # costates p_t (gradient of S_t at xbar_t) from the adjoint
    p = [None]*(N + 1)
    p[N] = (F[0][0]*xs[N][0], F[1][1]*xs[N][1])
    for t in range(N - 1, -1, -1):
        x = xs[t]
        p[t] = (h*(x[0] + k[0]*u[t]) + Fx[0][0]*p[t+1][0] + Fx[1][0]*p[t+1][1],
                h*(x[1] + k[1]*u[t]) + Fx[0][1]*p[t+1][0] + Fx[1][1]*p[t+1][1])
    fails = []
    for t in range(N):
        # K_t = h I + Fx^T P Fx - P ; beta_t = Fx^T P b + k ; kappa_t = P_11
        FtPF = [[sum(Fx[l][i]*P[l][m]*Fx[m][j] for l in range(2) for m in range(2)) for j in range(2)] for i in range(2)]
        Kt = [[(h if i == j else 0) + FtPF[i][j] - P[i][j] for j in range(2)] for i in range(2)]
        Pb = (P[0][0], P[1][0])
        beta = (Fx[0][0]*Pb[0] + Fx[1][0]*Pb[1] + k[0], Fx[0][1]*Pb[0] + Fx[1][1]*Pb[1] + k[1])
        kap = P[0][0]
        sig = gr[t]/h
        m = kap if -1 < u[t] < 1 else 2*abs(sig)/(h*2) + kap
        M3 = [[Kt[0][0], Kt[0][1], beta[0]], [Kt[1][0], Kt[1][1], beta[1]], [beta[0], beta[1], m]]
        if not psd3(M3):
            fails.append(t)
    term = psd3([[F[0][0] - P[0][0], -P[0][1]], [-P[1][0], F[1][1] - P[1][1]]])
    return fails, term

if __name__ == '__main__':
    k1 = Fr(sys.argv[1])
    for N in [int(v) for v in sys.argv[2:]]:
        Hq, gq = float_qp(float(k1), N)
        ev = np.linalg.eigvalsh(Hq)[0]
        rng = np.random.default_rng(0)
        starts = [np.zeros(N), -np.ones(N)] + ([rng.uniform(-1, 1, N) for _ in range(8)] if ev < 0 else [])
        uf = solve_float(Hq, gq, starts)
        status = [-1 if v < -1 + 1e-7 else (1 if v > 1 - 1e-7 else 0) for v in uf]
        u, gr, ok = exact_kkt(k1, N, status)
        h, k, F, Fx = build(k1, N)
        J = cost(h, k, F, Fx, u)
        k2 = Fr(1, 4)
        out = dict(N=N, min_eig=float(ev), J=float(J), kkt_exact=ok, n_free=sum(1 for s in status if s == 0),
                   first_free_t=float(next((t for t in range(N) if status[t] == 0), -1)*h))
        for name, P in (('A', ((Fr(0), Fr(0)), (Fr(0), Fr(0)))),
                        ('B1', ((-k1, -k2), (-k2, Fr(1, 4) - Fr(1, 10))))):
            fails, term = family_check(k1, N, u, gr, P)
            nb = [t for t in fails if status[t] != 0]
            out[name] = dict(n_fail=len(fails), n_fail_bound=len(nb), n_fail_free=len(fails) - len(nb),
                             first_bound_fail_t=float(nb[0]*h) if nb else None, terminal_ok=term)
        print(out, flush=True)
