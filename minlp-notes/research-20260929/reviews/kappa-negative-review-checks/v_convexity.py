"""Smallest eigenvalue of the reduced Hessian H of J (float) for the Section 9 toys at N = 1000.
H_ij = h^2 [h (N - 1 - max(i,j)) + phi2 + k_{max(i,j)} (1 - delta_ij)] (validated in v_single.py validate for
constant k; for piecewise k the l_1 term contributes h^2 k_j for i < j by the same computation)."""
import json
import numpy as np
from v_close import data
N = 1000
h = 2.0 / N
out = []
cfgs = [("9.1 kappa=+0.5", 0.5 * -1, 0.5 * -1), ("9.1 kappa=0", 0.0, 0.0), ("9.1 kappa=-0.5", 0.5, 0.5)]
cfgs += [(f"9.3 kappa {-k1:+.1f}->{-k2:+.1f}", k1, k2) for (k1, k2) in
         ((-0.5, 0.0), (0.0, -0.5), (-0.5, -0.3), (-0.3, -0.5), (-1.0, 0.0), (0.0, -1.0))]
for name, k1, k2 in cfgs:
    _, k = data(k1, k2, 0.6, 1.4, 0.59375, N)
    idx = np.arange(N)
    mx = np.maximum.outer(idx, idx)
    H = h * h * (h * (N - 1 - mx) + 1.0 + k[mx] * (1 - np.eye(N)))
    ev = np.linalg.eigvalsh(H)
    out.append((name, float(ev[0] / h ** 2), int((ev < -1e-12 * abs(ev).max()).sum())))
print(json.dumps(out, indent=0))
