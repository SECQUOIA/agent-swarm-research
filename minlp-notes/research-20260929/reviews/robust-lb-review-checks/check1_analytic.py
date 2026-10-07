"""Referee check 1: Lemma 3.1, Proposition 3.2 and the constants of Theorem 4.3(1), by brute force.
Usage: python3 check1_analytic.py > logs/check1_analytic.log"""
import numpy as np
from gadget_indep import Gadget

for (y1, eta, ev) in [(0.38, 0.05, 0.02), (0.38, 0.01, 0.005), (0.30, 0.005, 0.002), (0.5, 0.2, 0.25)]:
    G = Gadget(y1, eta, ev)
    print(f"== y1={y1} eta={eta} eps_v={ev}: b={G.b:.4f} bp={G.bp:.4f} c={G.c:.4f} z1={G.z1:.5f}")
    # u: continuity, C^1, convexity, u(1), u'(1)
    zz = np.linspace(-1, 1, 400001)
    uu = G.u(zz); du = np.gradient(uu, zz)
    print("  u continuity jump at z1: %.2e;  u'(1) = %.6f vs bp = %.6f;  u(1) = %.6f vs 1-(1-eta)y1^2 = %.6f"
          % (abs(G.u(G.z1 + 1e-13) - G.u(G.z1 - 1e-13)), float(G.du(1.0)), G.bp, float(G.u(1.0)),
             1 - (1 - eta) * y1 ** 2))
    print("  min second difference of u (convexity): %.3e" % np.min(np.diff(uu, 2)))
    # partial minima by brute force
    xs = np.linspace(-1, 1, 20001); ys = np.linspace(-1, 1, 801)
    h1_bf = np.array([np.min(y1 ** 2 * xs ** 2 + G.b * xs * y) for y in ys])
    h2_bf = np.array([np.min(G.u(xs) + G.bp * xs * y) for y in ys])
    h1 = np.where(np.abs(ys) <= y1, -ys ** 2, y1 ** 2 - 2 * y1 * np.abs(ys))
    h2 = -eta * ys ** 2 - (1 - eta) * np.maximum(np.abs(ys) - y1, 0) ** 2
    print("  |h1_bruteforce - h1| max %.2e ;  h2: %.2e (grid 1e-4 in x,z)" % (np.max(np.abs(h1_bf - h1)), np.max(np.abs(h2_bf - h2))))
    K = h1 + h2 + G.c * ys ** 2
    Kf = ev * ys ** 2 + eta * np.maximum(np.abs(ys) - y1, 0) ** 2
    print("  K formula error %.2e;  max K = %.6f vs eps_v + eta(1-y1)^2 = %.6f" % (np.max(np.abs(K - Kf)), K.max(), ev + eta * (1 - y1) ** 2))
    # growth g >= alpha (x^2 + z^2) and g >= 0 on random points
    rng = np.random.default_rng(0)
    P = rng.uniform(-1, 1, (2_000_000, 3))
    P[:500_000] *= 0.05                                   # concentrate some near 0
    gv = G.g(P[:, 0], P[:, 1], P[:, 2])
    alpha = ev * min(y1 ** 2 / 4, G.bp ** 2 / 16)
    ratio = gv / np.maximum(P[:, 0] ** 2 + P[:, 2] ** 2, 1e-300)
    print("  min g on 2e6 samples %.3e; min g/(x^2+z^2) = %.4e vs alpha = %.4e" % (gv.min(), ratio.min(), alpha))
    q = gv / np.maximum((P ** 2).sum(1), 1e-300)
    print("  min g/|p|^2 = %.4e vs (1/2)min(alpha, eps_v) = %.4e (c_g of Section 5)" % (q.min(), 0.5 * min(alpha, ev)))
    # Hessian at 0 and convexity threshold
    H = np.array([[2 * y1 ** 2, G.b, 0], [G.b, 2 * G.c, G.bp], [0, G.bp, G.bp ** 2 / (2 * eta)]])
    print("  Hessian det %.6e vs 2 y1^2 bp^2 eps_v/eta = %.6e; eigmin %.4e" % (np.linalg.det(H), 2 * y1 ** 2 * G.bp ** 2 * ev / eta, np.linalg.eigvalsh(H)[0]))
    Hout = H.copy(); Hout[2, 2] = G.bp ** 2 / 2
    print("  Hessian outside slab eigmin %.4e (should be < 0)" % np.linalg.eigvalsh(Hout)[0])
    # Proposition 3.2: five-point fooling
    A = 1 + ev - (1 - eta) * (1 - y1) ** 2
    ts = y1 / A; p = ts ** 2
    v1 = 0.5 * (y1 ** 2 * 1 + G.b * (-1) * ts) + 0.5 * (y1 ** 2 * 1 + G.b * 1 * (-ts))   # g1 = y1^2 x^2 + b x y
    v2 = (1 - p) * (G.c * 0 + G.u(0.0) + 0) + p / 2 * (G.c + G.u(-1.0) + G.bp * 1 * (-1)) + p / 2 * (G.c + G.u(1.0) + G.bp * (-1) * 1)
    gam = y1 ** 2 * (1 - A) / A
    mom1 = [0.5 * ts ** k + 0.5 * (-ts) ** k for k in range(1, 5)]
    mom2 = [p / 2 * (1 + (-1) ** k) for k in range(1, 5)]
    print("  A=%.6f (y1<A<1: %s) t*=%.6f; fooling value %.8f vs -gamma = %.8f" % (A, y1 < A < 1, ts, v1 + v2, -gam))
    print("  y-moments k=1..4: nu1 %s, nu2 %s  (agree for k<=3 only)" % (np.round(mom1, 6), np.round(mom2, 6)))
    # Lipschitz constants of the two factors (c y^2 in factor 1) on [-1,1]^2 by grid
    g_ = np.linspace(-1, 1, 1201)
    X, Y = np.meshgrid(g_, g_, indexing="ij")
    Lx = np.max(np.abs(2 * y1 ** 2 * X + G.b * Y))
    Ly1 = np.max(np.abs(G.b * X + 2 * G.c * Y))
    Ly2 = np.max(np.abs(G.bp * X))                          # d/dy of bp y z (X plays z)
    Lz = np.max(np.abs(G.du(X) + G.bp * Y))                  # d/dz of u(z) + bp y z (X plays z)
    Lam = 2 * max(Lx, Ly1 + Ly2, Lz)
    print("  Lipschitz: x %.4f  y %.4f  z %.4f;  Lambda %.4f;  gamma/Lambda %.6f;  base/gadget %.5f  per var %.5f"
          % (Lx, Ly1 + Ly2, Lz, Lam, gam / Lam, np.exp(gam / Lam), np.exp(gam / Lam / 3)))
    print("  alpha %.4e  2 alpha %.4e" % (alpha, 2 * alpha))
    for n in (100, 300, 1000, 3000):
        print("    analytic bound exp(gamma G/Lambda) at n=%d: %.3g" % (n, np.exp(gam * (n / 3) / Lam)))
