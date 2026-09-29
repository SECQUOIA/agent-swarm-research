"""Theorem 3.2 (McCormick certificate integral) evaluated on the diag instance (k = 1, |c| = 2, W = 1):
N_cov >= 2^s J(s)^(-1) * int_{[0,1]^2} ((x+y-1)^2 + eps)^(-s),  J(s) = 2 Gamma(1-s)^2/Gamma(3-2s).
The integral reduces to int_{-1}^{1} (1-|t|) (t^2+eps)^(-s) dt.  Compared with the flat-stratum bound
(Theorem 3.6: 0.707/sqrt(eps)) and with the leaves of the best tree found (SCIP-type rule)."""
import math
from scipy import integrate

best_nodes = {1e-2: 29, 1e-3: 123, 1e-4: 391, 1e-5: 1255, 1e-6: 4035}
for eps in (1e-2, 1e-4, 1e-6):
    row = []
    for s in (0.5, 0.75, 0.9, 1 - 1 / math.log(1 / eps)):
        I = 2 * integrate.quad(lambda t: (1 - t) * (t * t + eps) ** (-s), 0, 1, points=[math.sqrt(eps)], limit=200)[0]
        J = 2 * math.gamma(1 - s) ** 2 / math.gamma(3 - 2 * s)
        row.append(f"s={s:.3f}: {2 ** s * I / J:8.2f}")
    print(f"eps={eps:.0e}: Thm3.2 bounds " + "; ".join(row) +
          f" | Thm3.6 bound {math.sqrt(0.5 / eps):7.1f} | best tree leaves {(best_nodes[eps] + 1) // 2}")
