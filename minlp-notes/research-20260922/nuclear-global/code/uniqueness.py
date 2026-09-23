"""Numerical study: is the equilibrium cycle of a fixed pattern unique, and is the cycle map contractive?

For random patterns:
  (1) fixed-point iteration from many random starts k_1 in the a-priori box [KF - a c (T-1) age_max, KF];
      report the spread of the limits (max |k_1 - k_1'|) and whether all starts converge;
  (2) Jacobian J = dPhi/dk_1 at the fixed point: spectral radius and infinity norm;
  (3) infinity norm of the Jacobian of Phi^m (m = number of ages) at random points of the a-priori box
      (a crude estimate of the global Lipschitz constant; not a proof).
usage: uniqueness.py name npatterns nstarts seed"""
import sys, numpy as np
from nucsim import Data, equilibrium, jacobian_Phi, random_asg, cycle

name, npat, nst, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
D = Data(name); rng = np.random.default_rng(seed)
lo = D.KF - D.a * D.c * (D.T - 1) * (D.nages - 1)
rows = []
for q in range(npat):
    asg = random_asg(D, rng)
    ref = equilibrium(D, asg)
    spread, maxit = 0.0, 0
    for s in range(nst):
        k0 = rng.uniform(lo, D.KF, D.N)
        r = equilibrium(D, asg, k0, newton=False, maxit=5000)
        spread = max(spread, np.max(np.abs(r["k1"] - ref["k1"]))); maxit = max(maxit, r["it"])
    J = jacobian_Phi(D, asg, ref["k1"])
    rhoJ = max(abs(np.linalg.eigvals(J))); nJ = np.abs(J).sum(1).max()
    # Phi^m Jacobian norm at random points
    f, R = D.reload_matrix(asg)
    Phi = lambda k: D.KF * f + R @ cycle(D, k)[0][-1]
    def Phim(k):
        for _ in range(D.nages): k = Phi(k)
        return k
    worst = 0.0
    for s in range(5):
        k0 = rng.uniform(lo, D.KF, D.N); Jm = np.zeros((D.N, D.N)); h = 1e-6
        for j in range(D.N):
            e = np.zeros(D.N); e[j] = h; Jm[:, j] = (Phim(k0 + e) - Phim(k0 - e)) / (2 * h)
        worst = max(worst, np.abs(Jm).sum(1).max())
    rows.append((ref["lam_T"], spread, maxit, rhoJ, nJ, worst))
    print(f"pattern {q}: lam_T={ref['lam_T']:.6f} spread over {nst} starts={spread:.1e} (max it {maxit}) "
          f"rho(J)={rhoJ:.3f} ||J||_inf={nJ:.3f} max ||J(Phi^{D.nages})||_inf at random points={worst:.3f}", flush=True)
A = np.array(rows)
print(f"SUMMARY {name}: patterns {npat}, max spread {A[:,1].max():.1e}, rho(J) range [{A[:,3].min():.3f},{A[:,3].max():.3f}], "
      f"||J||_inf max {A[:,4].max():.3f}, ||J(Phi^m)||_inf max {A[:,5].max():.3f}")
