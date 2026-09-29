"""Numerical checks of the deterministic identities and inequalities of the
note (targeted checks; floating point).
 L1  KKT at x*: x* is a box minimizer iff zeta_i >= 0 for all i.
 L2  SDP identity: (v,t)' Z (v,t) = ||A d||^2 + sum zeta_i d_i^2, d = v - t x*.
 L3  Leave-one-out bound (Lemma 4.4): u*_j <= 2 (-c_j' r~_j)_+ / sigma_min(C)^2.
 L4  Barycenter formula (Section 6): f(xbar) - W = -2X + X^2/W + (rho/N)||H~perp c||^2.
 L5  Entropy lemma (Lemma 6.1): sum_i h(p_i) <= n h(q) - (lam k/2) log(n/(e k))
     whenever sum p = k, sum p^2 >= lam k, lam/2 >= e^2 k/n  (random p's and
     extremal two-level p's).
 L6  Witness closed form (Lemma 4.3): value = ||v||^2 X/(Q^2+X), Q = ||s||^2.
"""
import numpy as np
from scipy.optimize import nnls
from core import instance, box_min

rng = np.random.default_rng(11)

# L1
bad = 0
for t in range(300):
    N = int(rng.integers(3, 12)); M = N * int(rng.integers(1, 3))
    A, y, xs, B, w = instance(N, M, float(rng.choice([0.5, 3, 20])), int(rng.integers(1e9)))
    zeta = B.T @ w
    val, lb, u, ina = box_min(B, w)
    is_min = np.all(u < 1e-12)
    bad += (is_min != bool(np.all(zeta >= 0)))
print("L1 KKT characterization mismatches:", bad, "/ 300")

# L2
err = 0.0
for t in range(50):
    N = 8; M = 12
    A, y, xs, B, w = instance(N, M, 5.0, t)
    Q = np.zeros((N + 1, N + 1)); Q[:N, :N] = A.T @ A; Q[:N, N] = -A.T @ y; Q[N, :N] = -A.T @ y; Q[N, N] = y @ y
    xt = np.append(xs, 1.0)
    lam = (Q @ xt) / xt
    Z = Q - np.diag(lam)
    zeta = xs * (A.T @ w)
    for k in range(5):
        v = rng.standard_normal(N); tt = rng.standard_normal()
        d = v - tt * xs
        lhs = np.append(v, tt) @ Z @ np.append(v, tt)
        rhs = np.sum((A @ d) ** 2) + np.sum(zeta * d ** 2)
        err = max(err, abs(lhs - rhs) / (1 + abs(rhs)))
print("L2 SDP quadratic-form identity: max rel err %.2e" % err)

# L3
viol = 0; tot = 0
for t in range(40):
    N = 30; M = int(rng.choice([30, 45, 60]))
    C = rng.standard_normal((M, N)); v = rng.standard_normal(M) * 3
    sig = np.linalg.svd(C, compute_uv=False)[-1]
    u, _ = nnls(C, -v, maxiter=5000)
    for j in range(N):
        Cj = np.delete(C, j, axis=1)
        ut, _ = nnls(Cj, -v, maxiter=5000)
        r = v + Cj @ ut
        bound = 2 * max(-(C[:, j] @ r), 0.0) / sig ** 2
        tot += 1; viol += u[j] > bound + 1e-9
print("L3 leave-one-out bound violations:", viol, "/", tot)

# L4
err = 0.0
for t in range(30):
    N = 60; M = 60 * int(rng.integers(1, 3)); rho = 7.0
    A, y, xs, B, w = instance(N, M, rho, 1000 + t)
    W = w @ w; what = w / np.sqrt(W)
    Ht = (A * xs) * np.sqrt(N / rho)          # signed columns h~_i
    Hperp = Ht - np.outer(what, what @ Ht)
    c = np.zeros(N); T = rng.choice(N, 20, replace=False); c[T] = rng.uniform(0, 2, 20)
    zeta = B.T @ w
    X = -(zeta @ c)
    lhs = np.sum((w + B @ c) ** 2) - W
    rhs = -2 * X + X ** 2 / W + (rho / N) * np.sum((Hperp @ c) ** 2)
    err = max(err, abs(lhs - rhs) / (1 + abs(lhs)))
print("L4 barycenter formula: max rel err %.2e" % err)

# L5
def h(p):
    p = np.clip(p, 1e-300, 1 - 1e-16)
    return -p * np.log(p) - (1 - p) * np.log(1 - p)
worst = np.inf; checked = 0
for t in range(20000):
    n = int(rng.integers(200, 5000)); lam = float(rng.uniform(0.05, 0.9))
    kmax = int(lam * n / (2 * np.e ** 2))
    if kmax < 1:
        continue
    k = int(rng.integers(1, kmax + 1))
    # two-level family: j coords at level p1, rest spread
    j = int(rng.integers(1, max(2, 3 * k)))
    p1 = float(rng.uniform(0.0, 1.0))
    mass1 = min(j * p1, k)
    p = np.zeros(n)
    p[:j] = mass1 / j
    rest = (k - mass1) / (n - j)
    if rest > 1:
        continue
    p[j:] = rest
    if np.sum(p ** 2) < lam * k:
        continue
    q = k / n
    lhs = h(p).sum()
    rhs = n * h(q) - (lam * k / 2) * np.log(n / (np.e * k))
    worst = min(worst, rhs - lhs); checked += 1
print("L5 entropy lemma: %d feasible profiles checked, min(rhs - lhs) = %.3e (must be >= 0)" % (checked, worst))

# L6
err = 0.0
for t in range(20):
    N = 80; M = 80 * int(rng.integers(1, 3)); rho = 30.0
    A, y, xs, B, w = instance(N, M, rho, 2000 + t)
    i = 0
    v = w + 2 * B[:, i]; Bm = np.delete(B, i, axis=1)
    vhat = v / np.linalg.norm(v)
    Ht = Bm * np.sqrt(N / rho)
    g = vhat @ Ht; s = np.maximum(-g, 0)
    Hperp = Ht - np.outer(vhat, g)
    Q = s @ s; X = np.sum((Hperp @ s) ** 2)
    tau = np.sqrt(N / rho) * np.linalg.norm(v) * Q / (Q ** 2 + X)
    val = np.sum((v + Bm @ (tau * s)) ** 2)
    closed = (v @ v) * X / (Q ** 2 + X)   # = ||v||^2 (1 - Q^2/(Q^2 + X))
    err = max(err, abs(val - closed) / val)
print("L6 witness value closed form ||v||^2 X/(Q^2+X): max rel err %.2e" % err)
