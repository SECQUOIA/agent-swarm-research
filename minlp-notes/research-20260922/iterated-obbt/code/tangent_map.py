"""Tangent OBBT map for quadratic objectives with McCormick relaxations of the
off-diagonal terms, at an interior minimizer x* = 0.

Box shape D = [-dm, dp]. Relaxed function
  Q(D, xi) = sum_i H_ii xi_i^2 / 2 + sum_{i<j} H_ij * m_ij(xi)
where m_ij is the McCormick underestimator of xi_i xi_j if H_ij > 0 and the
McCormick overestimator if H_ij < 0 (both on D).
Phi_c(D) = box hull of {xi in D : Q(D, xi) <= c}.  c = 0 gives the homogeneous map.
"""
import numpy as np, cvxpy as cp

def phi(H, dm, dp, c=0.0):
    n = len(dm)
    lo, hi = -np.asarray(dm, float), np.asarray(dp, float)
    x = cp.Variable(n)
    terms = [cp.sum(cp.multiply(np.diag(H) / 2, cp.square(x)))]
    for i in range(n):
        for j in range(i + 1, n):
            h = H[i, j]
            if h == 0:
                continue
            li, ui, lj, uj = lo[i], hi[i], lo[j], hi[j]
            if h > 0:  # need underestimator of x_i x_j
                m = cp.maximum(lj * x[i] + li * x[j] - li * lj, uj * x[i] + ui * x[j] - ui * uj)
                terms.append(h * m)
            else:      # need overestimator of x_i x_j, times negative h
                m = cp.minimum(lj * x[i] + ui * x[j] - ui * lj, uj * x[i] + li * x[j] - li * uj)
                terms.append(h * m)
    Q = cp.sum(terms) if len(terms) > 1 else terms[0]
    cons = [Q <= c, x >= lo, x <= hi]
    newlo, newhi = np.zeros(n), np.zeros(n)
    for i in range(n):
        p = cp.Problem(cp.Maximize(x[i]), cons); p.solve(solver=cp.CLARABEL)
        newhi[i] = p.value
        p = cp.Problem(cp.Minimize(x[i]), cons); p.solve(solver=cp.CLARABEL)
        newlo[i] = p.value
    return -newlo, newhi

def rate(H, dm, dp, iters=40):
    dm, dp = np.array(dm, float), np.array(dp, float)
    ratios = []
    for k in range(iters):
        ndm, ndp = phi(H, dm, dp)
        s_old = max(dm.max(), dp.max()); s_new = max(ndm.max(), ndp.max())
        if s_new <= 1e-12:
            return 0.0, ratios
        ratios.append(s_new / s_old)
        dm, dp = ndm / s_new, ndp / s_new   # renormalize (power iteration)
    return ratios[-1], ratios

if __name__ == "__main__":
    for a in [0.5, 1.0, 1.5, 1.9]:
        H = np.array([[2, a], [a, 2]])
        r, rs = rate(H, [1, 1.2], [1.3, 1])
        print(f"toy a={a}: power-iteration ratio {r:.6f}, formula {(np.sqrt(2*a*a+4*a)-a)/2:.6f}")
    for n, a in [(3, 0.5), (5, 0.3), (10, 0.1), (20, 0.1)]:
        H = 2 * np.eye(n) + a * (np.ones((n, n)) - np.eye(n))
        r, rs = rate(H, np.ones(n), np.ones(n), iters=15)
        print(f"many-term n={n} a={a}: lambda_min(H/2)={np.linalg.eigvalsh(H/2).min():.3f}, ratio {r:.4f}")
