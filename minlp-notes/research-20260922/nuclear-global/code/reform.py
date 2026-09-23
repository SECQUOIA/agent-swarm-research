"""Check of the power-variable reformulation against the OSiL rows.

Part A (exact, structural): nucmodel.verify() regenerates every OSiL row and bound from the structured
data (G, V, c, a, KF, reload structure).  The reformulation below is written in terms of the same data.

Part B (60-digit numerical round trip): for a fixed assignment, compute the equilibrium cycle in power
variables at 60 digits (mpmath), map it to the original variables with
    phi_{i,t} = (G p_t)_i / lam_t,   k, lam unchanged,   binaries from the assignment,
    kappa_g = sum_j V_j k_{j,T} y_{j,pred g}  (F1),   z_ij = b_ij k_{j,T}  (F3),
and evaluate every OSiL row with the independent evaluator (osil_eval, mpmath backend).  Also evaluate
the reformulated rows R1-R5 at the power-variable point.  Residuals at the 1e-50 level show that the
map sends a solution of the power model to a solution of the OSiL model.

usage: reform.py name [seed]
"""
import sys, os, numpy as np, mpmath as mp
from nucsim import Data, equilibrium, random_asg
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../benchmark-observations/code"))
from osil_eval import Model, mp_backend

mp.mp.dps = 60


def perron_mp(G, k, phi0):
    """Newton on [G diag(k) - lam I] phi = 0, sum(phi) = 1 from a float start."""
    N = len(k); M = mp.matrix(N, N)
    for i in range(N):
        for j in range(N): M[i, j] = G[i][j] * k[j]
    phi = mp.matrix([mp.mpf(x) for x in phi0 / phi0.sum()])
    lam = sum((M * phi)[i] for i in range(N)) / sum(phi)
    for _ in range(12):
        r = M * phi - lam * phi
        J = mp.matrix(N + 1, N + 1); rhs = mp.matrix(N + 1, 1)
        for i in range(N):
            for j in range(N): J[i, j] = M[i, j] - (lam if i == j else 0)
            J[i, N] = -phi[i]; rhs[i] = -r[i]
            J[N, i] = 1
        rhs[N] = 1 - sum(phi)
        d = mp.lu_solve(J, rhs)
        for i in range(N): phi[i] += d[i]
        lam += d[N]
        if mp.norm(d) < mp.mpf(10) ** (-mp.mp.dps + 5): break
    return lam, phi


def cycle_mp(D, Gx, Vx, k1, phis0):
    ks, ps, lams = [], [], []
    k = list(k1)
    for t in range(D.T):
        lam, phi = perron_mp(Gx, k, phis0[t])
        p = [phi[i] * k[i] for i in range(D.N)]; s = sum(Vx[i] * p[i] for i in range(D.N)); p = [x / s for x in p]
        ks.append(k); ps.append(p); lams.append(lam)
        if t < D.T - 1: k = [k[i] - D.I.a_mp * p[i] for i in range(D.N)]
    return ks, ps, lams


def solve_mp(D, asg):
    I = D.I
    I.a_mp = mp.mpf(I.a.numerator) / I.a.denominator
    Gx = [[mp.mpf(x.numerator) / x.denominator for x in r] for r in I.G]
    Vx = [mp.mpf(x.numerator) / x.denominator for x in I.V]
    KF = mp.mpf(I.KF.numerator) / I.KF.denominator
    r0 = equilibrium(D, asg)
    phis0 = [p / r0["ks"][t] for t, p in enumerate(r0["ps"])]
    f, R = D.reload_matrix(asg)
    Rx = [[(Vx[j] if (D.fam == "F1" and R[i, j] != 0) else (mp.mpf(1) if R[i, j] != 0 else 0)) for j in range(D.N)] for i in range(D.N)]
    Phi = lambda k: [KF * f[i] + sum(Rx[i][j] * cycle_mp(D, Gx, Vx, k, phis0)[0][-1][j] for j in range(D.N)) for i in range(D.N)]
    from nucsim import jacobian_Phi
    A = np.linalg.inv(jacobian_Phi(D, asg, r0["k1"]) - np.eye(D.N))
    k = [mp.mpf(float(x)) for x in r0["k1"]]
    for it in range(14):
        kT = cycle_mp(D, Gx, Vx, k, phis0)[0][-1]
        r = [KF * f[i] + sum(Rx[i][j] * kT[j] for j in range(D.N)) - k[i] for i in range(D.N)]
        if max(abs(x) for x in r) < mp.mpf(10) ** (-55): break
        k = [k[i] - sum(mp.mpf(A[i, j]) * r[j] for j in range(D.N)) for i in range(D.N)]
    ks, ps, lams = cycle_mp(D, Gx, Vx, k, phis0)
    return ks, ps, lams, Gx, Vx, KF, max(abs(x) for x in r)


def to_osil(D, asg, ks, ps, lams, Gx, Vx):
    I = D.I; N, T = D.N, D.T
    x = [mp.mpf(0)] * len(I.vars)
    for t in range(T):
        for i in range(N):
            x[I.k[i][t]] = ks[t][i]
            x[I.phi[i][t]] = sum(Gx[i][j] * ps[t][j] for j in range(N)) / lams[t]
        x[I.lam[t]] = lams[t]
    kT = ks[-1]
    if D.fam == "F1":
        for i in range(N):
            for g in range(I.ntypes):
                y = mp.mpf(1 if asg[i] == g else 0)
                x[I.y[i][g]] = y
                if I.ycopy[i][g] is not None: x[I.ycopy[i][g]] = y
        for g in range(I.ntypes):
            if I.kappa[g] is not None:
                x[I.kappa[g]] = sum(Vx[j] * kT[j] for j in range(N) if asg[j] == I.pred[g])
    else:
        for i in range(N):
            x[I.b0[i]] = mp.mpf(1 if asg[i] < 0 else 0)
            for j in range(N):
                b = 1 if asg[i] == j else 0
                x[I.b[i][j]] = mp.mpf(b)
                if D.fam == "F3": x[I.z[i][j]] = b * kT[j]
    return x


def reform_residual(D, ks, ps, lams, Gx, Vx):
    """max residual of R1 (burn), R2 (norm), R4 (eigen in p), and min slack of R3 (peak), p >= 0, lam > 0."""
    I = D.I; N, T = D.N, D.T; c = [[mp.mpf(x.numerator) / x.denominator for x in r] for r in I.c]
    r1 = max(abs(ks[t + 1][i] - ks[t][i] + I.a_mp * ps[t][i]) for t in range(T - 1) for i in range(N))
    r2 = max(abs(sum(Vx[i] * ps[t][i] for i in range(N)) - 1) for t in range(T))
    r4 = max(abs(lams[t] * ps[t][i] - ks[t][i] * sum(Gx[i][j] * ps[t][j] for j in range(N))) for t in range(T) for i in range(N))
    s3 = min(c[i][t] - ps[t][i] for t in range(T) for i in range(N))
    return r1, r2, r4, s3, min(min(p) for p in ps), min(lams)


if __name__ == "__main__":
    name = sys.argv[1]; seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    D = Data(name); rng = np.random.default_rng(seed)
    # pick a random assignment that satisfies peaking (so that the OSiL point is feasible)
    for _ in range(200):
        asg = random_asg(D, rng)
        if equilibrium(D, asg)["feasible"]: break
    ks, ps, lams, Gx, Vx, KF, fpres = solve_mp(D, asg)
    r1, r2, r4, s3, pmin, lmin = reform_residual(D, ks, ps, lams, Gx, Vx)
    x = to_osil(D, asg, ks, ps, lams, Gx, Vx)
    M = Model(os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil"))
    chk = M.check(x, mp_backend(60))
    print(f"{name}: assignment {list(map(int, asg))}")
    print(f"  fixed-point residual {mp.nstr(fpres, 3)}; power model: burn {mp.nstr(r1, 3)} norm {mp.nstr(r2, 3)} "
          f"eigen {mp.nstr(r4, 3)} peak slack {mp.nstr(s3, 5)} min p {mp.nstr(pmin, 5)} min lam {mp.nstr(lmin, 8)}")
    print(f"  OSiL rows at mapped point: max row violation {mp.nstr(chk['row'][0], 3)} ({chk['row'][1]}), "
          f"max bound violation {mp.nstr(chk['bound'][0], 3)} ({chk['bound'][1]}), int {chk['int'][0]}; "
          f"objective {mp.nstr(M.objective(x, mp_backend(60)), 15)}")
