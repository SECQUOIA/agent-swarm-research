"""Seed 1007 (p = 3200): full unrestricted dual SOCP for the forced-in nodes of the null of rank 50
(j = 2119) and the weakest null (j = 1508), to confirm the column-generation values."""
import os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    os.environ[_v] = "1"
import numpy as np
from rc_common import make_instance, fit, node_value_dual_socp
X, y, lam, S = make_instance(121, 3200, 5, 1007, 'sqrtn')
fS = fit(X, y, lam, S)[0]
for j in [2119, 1508]:
    dv, dlb, _ = node_value_dual_socp(X, y, lam, 5, (), (j,))
    print("j=%d: dual SOCP value - f(S*) = %.4f, certified lb - f(S*) = %.4f" % (j, dv - fS, dlb - fS))
