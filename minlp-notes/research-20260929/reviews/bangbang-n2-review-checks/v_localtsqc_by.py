"""b.y along the layer at sampled times (not integrator trial stages), examples A and C."""
import numpy as np
import v_localtsqc as L

for name, eps, d1 in (("A", 0.02, 0.02), ("A", 0.02, 0.005), ("C", 0.02, 0.02)):
    P_and_M, siga, sigb, tau, w, info, by_min = L.build(name, eps, d1)
    b = L.b
    worst = np.inf
    for s in np.geomspace(1e-10, d1 * 0.999999, 4000):
        t = tau + s
        P, M = P_and_M(t)
        beta = P @ b - w
        G = M - 2 * eps * np.eye(2) - 2.0 / (2 * abs(sigb(t))) * np.outer(beta, beta)  # = y y^T / (b.y)
        worst = min(worst, np.linalg.eigvalsh(G)[0])
    print(name, eps, d1, "lambda=%.3f d2/d1=%.3g" % (info["lam"], info["d2"] / d1),
          "min eig of M-2eps-sing on sampled layer times = %.3e" % worst, "min b.y incl. trial stages = %.3g" % by_min[0],
          "status", info["status"])
