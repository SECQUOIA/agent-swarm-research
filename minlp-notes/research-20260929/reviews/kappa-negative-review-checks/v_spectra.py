"""Reviewer check of Section 2: (i) is lambda_min(G) = h^3/4 exactly for toy plus (G = Hessian of Jt)?
(ii) negative eigenvalue counts of H and G for [E]'s A- and A at N = 100 (Hessian by second differences
of the reviewer's own float cost implementation)."""
import json
import numpy as np
import mpmath as mp
out = {}
# (i) toy plus, k = 1/2, phi2 = 0: G_ij = h^2 [h (N - 1 - max(i, j)) + k]; exact-ish eigenvalue with mpmath
mp.mp.dps = 40
for N in (10, 40, 100):
    h = mp.mpf(2) / N
    G = mp.matrix(N, N)
    for i in range(N):
        for j in range(N):
            G[i, j] = h * (N - 1 - max(i, j)) + mp.mpf(1) / 2      # G / h^2
    ev = mp.eigsy(G)[0]
    lam = min(ev[i] for i in range(N))
    out[f"toy_N{N}"] = dict(lam_min_G_over_h2=float(lam), h_over_4=float(h / 4), rel_diff=float((lam - h / 4) / (h / 4)))
# (ii) two-state examples: x1' = x2, x2' = u, l0 = q x1^2/2 - c x2^2/2, l1 = k1 x1 + k2 x2, Phi = -x1 + rho x2^2/2
def J2(u, p, N):
    h = 2.0 / N
    x1, x2 = 0.0, 0.5
    J = 0.0
    for t in range(N):
        J += h * (p["q"] * x1 * x1 / 2 - p["c"] * x2 * x2 / 2 + (p["k1"] * x1 + p["k2"] * x2) * u[t])
        x1, x2 = x1 + h * x2, x2 + h * u[t]
    return J - x1 + p["rho"] * x2 * x2 / 2
for name, p in (("A-", dict(q=0.3, c=1.0, k1=-0.3, k2=0.3, rho=2.0)), ("A", dict(q=0.3, c=1.0, k1=-0.3, k2=-0.3, rho=2.0))):
    N = 100
    h = 2.0 / N
    u0 = np.zeros(N)
    J0 = J2(u0, p, N)
    Ji = np.array([J2(np.eye(N)[i], p, N) for i in range(N)])
    H = np.zeros((N, N))
    for i in range(N):
        for j in range(i, N):
            e = np.zeros(N); e[i] += 1; e[j] += 1
            H[i, j] = H[j, i] = J2(e, p, N) - Ji[i] - Ji[j] + J0 if i != j else (J2(2 * np.eye(N)[i], p, N) - 2 * Ji[i] + J0)
    kap = -p["k2"]
    G = H - kap * h * h * np.eye(N)
    eH, eG = np.linalg.eigvalsh(H), np.linalg.eigvalsh(G)
    tol = 1e-9 * np.abs(eH).max()
    out[name] = dict(N=N, lam_min_H_over_h2=eH[0] / h**2, lam_min_G_over_h2=eG[0] / h**2,
                     n_neg_H=int((eH < -tol).sum()), n_neg_G=int((eG < -tol).sum()))
print(json.dumps(out, indent=1))
