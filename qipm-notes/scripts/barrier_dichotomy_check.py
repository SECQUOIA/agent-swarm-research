"""Numerical check of the barrier-independent conditioning dichotomy.

Degenerate family (optimal face dim 1):
    min x3  s.t.  x1+x2+x3 = 1, x >= 0.
Optimal face: {x3=0, x1+x2=1, x>=0}, dual slack s* = (0,0,1) -> strict comp.
Prediction: for EVERY self-concordant barrier, kappa(reduced Hessian) = Theta(1/mu^2).

Vertex family (unique nondegenerate vertex optimum):
    min x3 + 2 x4  s.t.  x1+x3 = 1, x2+x4 = 1, x >= 0.
Prediction: log barrier reduced Hessian kappa -> O(1).
"""
import numpy as np

def central_point(c, A, b, grad, hess, x0, mu, iters=200):
    """Newton on the affine slice: min c^T x + mu F(x), Ax=b."""
    n = len(c)
    # null space basis of A
    _, _, Vt = np.linalg.svd(A)
    Z = Vt[A.shape[0]:].T  # n x (n-m)
    x = x0.copy()
    for _ in range(iters):
        g = Z.T @ (c + mu * grad(x))
        H = Z.T @ (mu * hess(x)) @ Z
        d = np.linalg.solve(H, -g)
        # damped Newton with feasibility backtracking
        t = 1.0
        lam = np.sqrt(d @ H @ d)
        if lam > 0.25:
            t = 1.0 / (1.0 + lam)
        while True:
            xn = x + t * (Z @ d)
            if np.all(xn > 0):
                break
            t *= 0.5
        x = xn
        if lam < 1e-12:
            break
    return x, Z

def kappa_reduced(hess, x, Z):
    H = Z.T @ hess(x) @ Z
    w = np.linalg.eigvalsh(H)
    return w[0], w[-1], w[-1] / w[0]

# ---------- degenerate family ----------
c = np.array([0.0, 0.0, 1.0])
A = np.array([[1.0, 1.0, 1.0]])
b = np.array([1.0])
x0 = np.array([1/3, 1/3, 1/3])

barriers = {
    "log (nu=3)": (
        lambda x: -1/x,
        lambda x: np.diag(1/x**2),
    ),
    "weighted log 2,1,3 (nu=6)": (
        lambda x: -np.array([2.0, 1.0, 3.0])/x,
        lambda x: np.diag(np.array([2.0, 1.0, 3.0])/x**2),
    ),
    "log + log(x1+x2) (nu=4)": (
        lambda x: -1/x - np.array([1.0, 1.0, 0.0])/(x[0]+x[1]),
        lambda x: np.diag(1/x**2) + np.outer(np.array([1.0,1.0,0.0]),
                                             np.array([1.0,1.0,0.0]))/(x[0]+x[1])**2,
    ),
    # an "adversarial" attempt: heavily reweight to flatten the blowup coord
    "log with tiny weight on x3 (nu=2.01)": (
        lambda x: -np.array([1.0, 1.0, 0.01])/x,
        lambda x: np.diag(np.array([1.0, 1.0, 0.01])/x**2),
    ),
}

print("=== degenerate family: min x3 on simplex (optimal face dim 1) ===")
mus = [10.0**(-k) for k in range(1, 8)]
for name, (grad, hess) in barriers.items():
    rows = []
    for mu in mus:
        x, Z = central_point(c, A, b, grad, hess, x0, mu)
        lmin, lmax, k = kappa_reduced(hess, x, Z)
        rows.append((mu, x[2], lmin, lmax * mu**2, k * mu**2))
    print(f"\nbarrier: {name}")
    print(f"{'mu':>10} {'x3(mu)':>12} {'lam_min':>12} {'lam_max*mu^2':>13} {'kappa*mu^2':>12}")
    for mu, x3, lmin, lm, km in rows:
        print(f"{mu:>10.1e} {x3:>12.4e} {lmin:>12.4e} {lm:>13.4f} {km:>12.4f}")

# ---------- vertex family ----------
print("\n=== vertex family: min x3+2x4, x1+x3=1, x2+x4=1 (nondegenerate vertex) ===")
c2 = np.array([0.0, 0.0, 1.0, 2.0])
A2 = np.array([[1.0, 0.0, 1.0, 0.0],
               [0.0, 1.0, 0.0, 1.0]])
b2 = np.array([1.0, 1.0])
x02 = np.array([0.5, 0.5, 0.5, 0.5])
grad_l = lambda x: -1/x
hess_l = lambda x: np.diag(1/x**2)
print(f"{'mu':>10} {'kappa_red(log)':>16}")
for mu in mus:
    x, Z = central_point(c2, A2, b2, grad_l, hess_l, x02, mu)
    _, _, k = kappa_reduced(hess_l, x, Z)
    print(f"{mu:>10.1e} {k:>16.6f}")
