"""Closing audit (b), item 1: the largest c' admitted by the proof of Theorems 4.3/4.4
(phase-transition.md, Section 4.3, Step 2), and the small constants of Sections 4-5.

Constraints of the proof: c' < (1 - mu) theta, and (*) (1+mu)(1-theta) x / B > e^x - 1 with
B = 1 + 2 sqrt(c' x) + 2 c' x (pure noise); planted: (1 + kappa_s) < e^{-x} (1 + (1+mu)(1-theta) x / B).
For fixed (mu, theta) the largest c' solving (*) is explicit; we maximize over (mu, theta) by a
fine grid followed by Nelder-Mead refinement.  Own code.
"""
import os
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[v] = "1"
import numpy as np
from scipy.optimize import minimize, brentq

K = lambda x: np.exp(-x) * (1 + 2 * x) - 1


def cp(mu, th, x, kap=None):
    if not (0 < mu < 1 and 0 < th < 1):
        return 0.0
    A = (1 + mu) * (1 - th) * x
    den = (np.exp(x) - 1) if kap is None else ((1 + kap) * np.exp(x) - 1)
    Bmax = A / den
    if Bmax <= 1:
        return 0.0
    u = (-1 + np.sqrt(2 * Bmax - 1)) / 2           # 2u^2 + 2u + 1 = Bmax, u = sqrt(c' x)
    return min(u * u / x, (1 - mu) * th)


def best(x, kap=None):
    g = np.linspace(0.002, 0.998, 499)
    vals = np.array([[cp(m, t, x, kap) for t in g] for m in g])
    i, j = np.unravel_index(np.argmax(vals), vals.shape)
    r = minimize(lambda v: -cp(v[0], v[1], x, kap), [g[i], g[j]], method="Nelder-Mead",
                 options={"xatol": 1e-12, "fatol": 1e-15, "maxiter": 20000})
    return max(vals[i, j], -r.fun), r.x


x0 = brentq(lambda x: K(x), 0.5, 2)
print("x0 = %.10f, 2/x0 = %.4f, K(1/2) = %.4f, K/(e^x-1) at 0.1, 0.5, 1: %s" %
      (x0, 2 / x0, K(0.5), ", ".join("%.3f" % (K(x) / (np.exp(x) - 1)) for x in (0.1, 0.5, 1.0))))
print("limit x -> 0: sup (1-mu) theta s.t. (1+mu)(1-theta) >= 1 is 3 - 2 sqrt2 = %.5f at mu = sqrt2 - 1" % (3 - 2 * np.sqrt(2)))
print("   x      c'_max (noise)   (mu, theta)        c'_max planted kappa_s=K(x)/2   ratio")
for x in (1e-6, 1e-4, 1e-3, 1e-2, 0.05, 0.2, 0.5, 0.8, 1.0, 1.2):
    c, (m, t) = best(x)
    if x >= 0.05:
        cpl, _ = best(x, K(x) / 2)
        print("%8.0e  %.5f   (%.3f, %.3f)      %.6f                   %.1f" % (x, c, m, t, cpl, c / cpl) if x < 1e-3 else
              "%8.3f  %.5f   (%.3f, %.3f)      %.6f                   %.1f" % (x, c, m, t, cpl, c / cpl))
    else:
        print("%8.0e  %.5f   (%.3f, %.3f)" % (x, c, m, t))

# Conjecture 5.2: range (1+delta) k <= n <= (1-delta) n_IT nonempty iff (1+delta)/(1-delta) < n_IT/k,
# n_IT/k -> 2(1-gamma)/gamma; solve for delta.
for gam in (0.5, 0.6):
    lim = 2 * (1 - gam) / gam
    dstar = brentq(lambda d: (1 + d) / (1 - d) - lim, 0, 0.999)
    print("gamma = %.2f: largest delta with nonempty limit range = %.5f; (2-3g)/(2-g) = %.5f" %
          (gam, dstar, (2 - 3 * gam) / (2 - gam)))
for P in (1e4, 1e8, 1e16):
    kk = P ** 0.5
    print("n_IT/k at p = %.0e, gamma = 1/2, b/sigma = 2: %.3f" % (P, 2 * np.log(P / kk) / np.log(1 + kk * 4)))
