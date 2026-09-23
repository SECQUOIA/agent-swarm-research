# Cross-check of prop:degree-two-witness (Section 3) and the four-window claim
# (Section 4): log-det central path of
#     min X_22  s.t.  tr X = 1,  X_33 = X_12,  X >= 0.
import numpy as np
from scipy.optimize import minimize

def build(p):
    b, d, t, e = p
    return np.array([[1-d-b, b, t], [b, d, e], [t, e, b]])

def obj(p, mu):
    X = build(p)
    if np.linalg.eigvalsh(X).min() <= 0:
        return 1e18
    return p[1] - mu*np.log(np.linalg.det(X))

def svec_basis():
    B = []
    for i in range(3):
        M = np.zeros((3, 3)); M[i, i] = 1; B.append(M)
    for (i, j) in [(0, 1), (0, 2), (1, 2)]:
        M = np.zeros((3, 3)); M[i, j] = M[j, i] = 1/np.sqrt(2); B.append(M)
    return B

B = svec_basis()
svec = lambda M: np.array([np.sum(Bi*M) for Bi in B])
C2 = np.zeros((3, 3)); C2[2, 2] = 1; C2[0, 1] = C2[1, 0] = -0.5
_, _, vt = np.linalg.svd(np.vstack([svec(np.eye(3)), svec(C2)]))
W = vt[2:].T                                   # 6 x 4 orthonormal tangent basis

x0 = np.array([0.2, 0.3, 0.0, 0.0])
print(f"{'mu':>10} {'gap g':>12} {'kappa':>13} {'k*mu^1.5':>10} {'k*mu^2':>11} {'k*mu':>11}")
for mu in (1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6):
    x0 = minimize(obj, x0, args=(mu,), method='Nelder-Mead',
                  options={'xatol': 1e-14, 'fatol': 1e-18,
                           'maxiter': 200000, 'maxfev': 200000}).x
    X = build(x0); Xi = np.linalg.inv(X)
    H = np.array([[np.trace(Xi@B[i]@Xi@B[j]) for j in range(6)] for i in range(6)])
    w = np.linalg.eigvalsh(W.T @ H @ W)
    kap = w.max()/w.min()
    print(f"{mu:10.1e} {x0[1]:12.4e} {kap:13.4e} {kap*mu**1.5:10.4f} "
          f"{kap*mu**2:11.3e} {kap*mu:11.3e}")
    print("   reduced eigenvalues:", np.array2string(w, precision=3))
