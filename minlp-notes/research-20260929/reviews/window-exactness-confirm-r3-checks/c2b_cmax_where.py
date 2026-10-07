"""Round-3 confirmation, item 3 probe: cmax on A and A0, log segment.  For s = t - tau in 1e-8 ... 0.049,
lambda_min(M) - 2 eps, ||R|| and the angle between the dominant eigenvector of R and beta, with P' from
five-point differences of the lam = log(s) dense output (steps 1e-2, 1e-3, 1e-4); last line: central t-difference
of step 0.1 s at s = 1e-8 (the second-revision scheme).  Imports c2_aniso.py."""
import sys, numpy as np
sys.path.insert(0, '.')
from c2_aniso import *
for ex in ("A", "A0"):
    p = EX[ex]; eps = 0.02
    Pf, _ = continuous_family(p, eps, delta1=None)
    th = find_switch(p)[0]; sol = solve_arcs(p, th); lay = th + 0.05
    segs_cl = [c.cell_contents for c in Pf.__closure__ if isinstance(c.cell_contents, list)][0]
    f_log = [f for lo, hi, f in segs_cl if abs(lo - th) < 1e-9 and abs(hi - lay) < 1e-12][0]
    sol2 = f_log.__defaults__[0]
    print(ex, 'lam range of dense output', sol2.t_min, sol2.t_max)
    Q = lambda lam: np.asarray(sol2(lam)).reshape(2, 2)
    for s in [1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 0.03, 0.049]:
        lam = np.log(s)
        for hl in (1e-2, 1e-3, 1e-4):
            P = Q(lam); dP = five(Q, lam, hl) / s
            M = dP + A.T @ P + P @ A + p.Hxx; M = (M + M.T) / 2
            ev = np.linalg.eigvalsh(M)
            beta = P @ B - p.w
            Rm = M - 2*eps*np.eye(2) - (2/(2*abs(sol['b']['sig'](th+s))))*np.outer(beta, beta)
            er, V = np.linalg.eigh(Rm)
            i = np.argmax(abs(er)); cosb = abs(V[:, i] @ beta)/np.linalg.norm(beta)
            print(f"  s={s:.0e} hl={hl:.0e} lminM-2eps={ev[0]-2*eps:+.2e} |M|={abs(ev).max():.3e} |R|={abs(er).max():.2e} cos(Rvec,beta)={cosb:.6f}")
    # central t-scheme: direction of the large residual at 1e-8
    t = th + 1e-8; hs = 0.1e-8
    P = Pf(t); dP = (Pf(t+hs) - Pf(t-hs))/(2*hs)
    M = dP + A.T @ P + P @ A + p.Hxx; M = (M + M.T)/2
    beta = P @ B - p.w
    Rm = M - 2*eps*np.eye(2) - (1/abs(sol['b']['sig'](t)))*np.outer(beta, beta)
    er, V = np.linalg.eigh(Rm); i = np.argmax(abs(er))
    print('  central t 1e-8: R eig', er, 'cos with beta', abs(V[:, i] @ beta)/np.linalg.norm(beta))
