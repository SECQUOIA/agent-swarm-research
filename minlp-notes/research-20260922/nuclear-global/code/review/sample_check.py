"""Independent spot check of the sampling statistics: uniform random F1 assignments (types permuted over slots;
each pattern class has exactly chains! assignments, so this is uniform over patterns), evaluated with the
reviewer's simulator. Also records whether every sample's fixed-point iteration converged.
usage: sample_check.py name n seed procs"""
import sys
import numpy as np
from multiprocessing import Pool
from rv_common import D, equilibrium

nm, n, seed, procs = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
BEST = {"nuclearva": 1.0143048557749, "nuclearvd": 1.0420785385512}
d = D(nm)
tied = {j for _, j in d.S.ties}; partner = dict(d.S.ties)
slots = [i for i in range(d.N) if i not in tied]


def one(s):
    rng = np.random.default_rng([seed, s])
    perm = rng.permutation(d.ng); typ = [None] * d.N
    for sl, g in zip(slots, perm):
        typ[sl] = int(g)
        if sl in partner: typ[partner[sl]] = int(g)
    e = equilibrium(d, typ)
    return e["lam"], e["peak"], e["res"]


if __name__ == "__main__":
    with Pool(procs) as P:
        A = np.array(P.map(one, range(n), chunksize=20))
    feas = A[:, 1] <= d.c
    print(f"{nm}: {n} samples; max fixed-point residual {A[:,2].max():.1e}; feasible {feas.mean():.4f} "
          f"(+-{2*np.sqrt(feas.mean()*(1-feas.mean())/n):.4f}); max feasible lam_T {A[feas,0].max():.7f}")
    for tol in (0.01, 0.005, 0.002):
        w = feas & (A[:, 0] >= BEST[nm] * (1 - tol))
        print(f"   feasible and within {tol:.3f} of {BEST[nm]:.7f}: {w.mean():.5f} (+-{2*np.sqrt(w.mean()*(1-w.mean())/n):.5f}), count {w.sum()}")
