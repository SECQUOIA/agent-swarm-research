"""Numerical check of the steps in PWE Appendix 7.1 (Lemmas 1 and 2), rho = sqrt n, per-entry noise.

A_j = X_j' M X_S w*_S / s, B_j = X_j' M eps / s, with s = rho n (the paper's definition of U_j)
or s = rho (the normalization used inside the proofs of Lemmas 1 and 2).
Lemma 1 claims max_j |B_j| < w_min/16 w.h.p.; Lemma 2 claims min_S |A_j| >= w_min/4 and
max_{S^c} |A_j| < w_min/16 w.h.p., once n > c0 (gamma^2 + ||w*||^2)/w_min^2 log d.
"""
import numpy as np
from pwe_lib import instance

d, k, b, gam, R = 50, 5, 1.0, 0.5, 40
print(f"d={d} k={k} w_min={b} gamma={gam} rho=sqrt(n); medians over {R} instances")
print(f"thresholds: w_min/4 = {b/4}, w_min/16 = {b/16}; gamma*sqrt(2 log d) = {gam*np.sqrt(2*np.log(d)):.3f}")

# (i) largest eigenvalue of M versus the claimed bound 1/rho
for n in (100, 500):
    X, y, S, w = instance(n, d, k, b, gam, 1)
    Mm = np.linalg.inv(np.eye(n) + X[:, S] @ X[:, S].T / np.sqrt(n))
    ev = np.linalg.eigvalsh(Mm)
    print(f"n={n}: lambda_max(M) = {ev[-1]:.12f}, multiplicity of eigenvalue 1: {np.sum(ev > 1 - 1e-9)}, "
          f"1/rho = {1/np.sqrt(n):.4f}")

print("n | s | med min_S|A_j| | med max_Sc|A_j| | med max_j|B_j| | med max_j Var(X_j'M eps/rho | X) | "
      "claimed 4 gamma^2/rho^2 | corrected 4 n gamma^2/rho^2")
for n in (500, 5000, 50000):
    rho = np.sqrt(n)
    rows = {"rho n": [], "rho": []}
    var = []
    for r in range(R):
        X, y, S, w = instance(n, d, k, b, gam, 500 + r)
        eps = y - X @ w
        XS = X[:, S]
        K = rho * np.eye(k) + XS.T @ XS
        Mapply = lambda v: v - XS @ np.linalg.solve(K, XS.T @ v)      # M v, PWE p.72 identity
        MX = Mapply(X)                                                  # M X (n x d)
        sig = X.T @ Mapply(XS @ w[S])
        noi = X.T @ Mapply(eps)
        off = np.setdiff1d(np.arange(d), S)
        for lab, s in (("rho n", rho * n), ("rho", rho)):
            rows[lab].append((np.min(np.abs(sig[S])) / s, np.max(np.abs(sig[off])) / s, np.max(np.abs(noi)) / s))
        var.append(np.max(gam ** 2 * np.sum(MX ** 2, axis=0) / rho ** 2))
    for lab in ("rho n", "rho"):
        m = np.median(np.array(rows[lab]), axis=0)
        print(f"{n} | {lab} | {m[0]:.4g} | {m[1]:.4g} | {m[2]:.4g} | {np.median(var):.4f} | "
              f"{4 * gam**2 / rho**2:.2e} | {4 * n * gam**2 / rho**2:.3f}")
