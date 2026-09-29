"""All eight p = 3200 (lam = sqrt n) instances: additive saturated gain sum_l (|a_l|-m0)_+^2/n of
Heuristic 3.8, number of violators, realized tau^2 and price m0^2/lam (the stored root gaps are compared
in the report)."""
import os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    os.environ[_v] = "1"
import numpy as np
from rc_common import make_instance, fit
p, k, n = 3200, 5, 121
for seed in range(1000, 1008):
    X, y, lam, S = make_instance(n, p, k, seed, 'sqrtn')
    fS, bS, r = fit(X, y, lam, S)
    a = np.abs(X.T @ r); m0 = lam * np.abs(bS).min()
    nulls = np.array([j for j in range(p) if j not in set(S)])
    sat = np.sum(np.clip(a[nulls] - m0, 0, None) ** 2) / n
    print("seed %d: tau^2 %.3f  price %.3f  #viol %d  additive saturated gain %.2f  max own fit %.2f" % (
        seed, (m0 / np.linalg.norm(r)) ** 2, m0 ** 2 / lam, int((a[nulls] > m0).sum()), sat, a[nulls].max() ** 2 / (n + lam)))
