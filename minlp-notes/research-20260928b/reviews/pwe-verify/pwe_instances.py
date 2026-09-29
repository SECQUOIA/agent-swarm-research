"""Direct instances for PWE Theorem 2 (per-entry noise N(0, gamma^2), rho = sqrt n).

For each instance: P* by full enumeration of the k-subsets, the PWE Corollary 2 certificate at the
optimal support, P_IR from cvxpy (perspective SOCP) polished by projected gradient, a two-sided
bracket on P_IR (closed-form G(u) above, weak-duality value below), and an explicit feasible
point u_t (swap direction) whose closed-form value is below P* when the certificate fails.

Seeds 424242+s reproduce the reviewer's instances (same generation order); seeds 7000+s are fresh.
"""
import numpy as np
from pwe_lib import (instance, enumerate_opt, cert, relax_cvxpy, polish, G_of_u, dual_value,
                     swap_certificate)

d, k, b, gam = 50, 5, 1.0, 0.5
print(f"d={d} k={k} |w*_j|={b} gamma={gam} rho=sqrt(n); values are y'M y (no factor 1/2)")
print("c0_implied = n w_min^2 / ((gamma^2 + ||w*||^2) log d)")
hdr = ("n", "c0", "seed", "S_opt=S_true", "(2nd-P*)/P*", "cert", "max|a_l|/m0",
       "(P*-UB)/P*", "(P*-LB)/P*", "(P*-cvx)/P*", "(P*-swap)/P*")
print(" | ".join(hdr))
for n in (500, 5000):
    rho = np.sqrt(n)
    c0 = n * b * b / ((gam ** 2 + k * b * b) * np.log(d))
    for seed in [424242 + s for s in range(4)] + [7000 + s for s in range(4)]:
        X, y, S, w = instance(n, d, k, b, gam, seed)
        Pstar, Sopt, second = enumerate_opt(X, y, rho, k)
        a, m0, M0 = cert(X, y, rho, Sopt)[:3]
        vcvx, u = relax_cvxpy(X, y, rho, k)
        u, ub, lb = polish(X, y, rho, k, u)
        sw = swap_certificate(X, y, rho, Sopt, a) if M0 > m0 else np.nan
        print(f"{n} | {c0:.1f} | {seed} | {np.array_equal(np.sort(Sopt), S)} | {(second - Pstar) / Pstar:.2e} | "
              f"{M0 <= m0} | {M0 / m0:.3f} | {(Pstar - ub) / Pstar:.3e} | {(Pstar - lb) / Pstar:.3e} | "
              f"{(Pstar - vcvx) / Pstar:.2e} | {(Pstar - sw) / Pstar:.2e}", flush=True)
