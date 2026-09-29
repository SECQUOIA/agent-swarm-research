"""Check 6: numerical tests of the pointwise bounds, with z FIXED (reviewer code only).
 Prop 3.1(b):   SDP1(z) <= g_delta(z)           (delta = max_i x_i'(I + X_-i X_-i'/lam)^{-1} x_i / lam)
 Lemma 4.1(iii): SDP1(z) <= P(z, beta) + lam theta_F pi(z, beta)   (beta = perspective minimizer at z)
 Prop 5.1:      zb(z) >= min_beta [ G(beta) + (lam + Lambda_-) pi ] = g_{Lambda_-/lam}(z)
 (zb(z) >= SDP1(z) is also checked; zb(z) at a FIXED fractional z need not be <= OPT.)
 Prop 5.3:      zb(z) >= OPT - (L+ - L-)/(lam + L+) (OPT - f(A));  g(z) >= OPT - L+/(lam + L+) (OPT - f(A))
Instances: n = 7, p = 16, k = 3 (planted, weak, noise); z random in K with support A of size 5 (one z_j = 1)."""
import os as _os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"]:
    _os.environ[_v] = "1"
import itertools, json
import numpy as np
from rv_common import gen_core, sdp1, zb, opt_enum, fval


def g_eps(X, y, lam, z, eps):
    A = np.nonzero(z > 0)[0]
    XA = X[:, A]
    c = lam + lam * (1 + eps) * (1 / z[A] - 1)
    bA = np.linalg.solve(XA.T @ XA + np.diag(c), XA.T @ y)
    return float(np.sum((y - XA @ bA) ** 2) + np.sum(c * bA ** 2)), A, bA


rng = np.random.default_rng(5)
bad = 0
for it in range(9):
    n, p, k = 7, 16, 3
    b = [1.0, 0.3, 0.0][it % 3]
    X, y, lam, S = gen_core(n, p, k, b=b, sigma=0.5, seed=500 + it, lam=np.sqrt(n))
    A = sorted(rng.choice(p, 5, replace=False))
    z = np.zeros(p); z[A[0]] = 1.0
    frac = rng.dirichlet(np.ones(4)) * 2.0
    frac = np.minimum(frac, 0.95)
    z[A[1:]] = frac
    Q = X.T @ X + lam * np.eye(p)
    delta = max((1 / np.linalg.inv(Q)[i, i] - lam) / lam for i in range(p))
    gd, _, _ = g_eps(X, y, lam, z, delta)
    g0, Aidx, bA = g_eps(X, y, lam, z, 0.0)
    s1 = sdp1(X, y, lam, k, fix_z=z)
    # Lemma 4.1(iii): F = A, Z1 = rest (|Z1| = 11 >= n = 7)
    Z1 = [j for j in range(p) if j not in A]
    W = X[:, Z1] @ X[:, Z1].T
    theta = np.linalg.eigvalsh(X[:, A].T @ np.linalg.solve(W, X[:, A])).max()
    pi = float(np.sum(bA ** 2 * (1 / z[Aidx] - 1)))
    iii = g0 + lam * theta * pi
    ev = np.linalg.eigvalsh(X[:, A].T @ X[:, A])
    Lm, Lp = ev.min(), ev.max()
    gL, _, _ = g_eps(X, y, lam, z, Lm / lam)
    v = zb(X, y, lam, k, fix_z=z)
    OPT, _ = opt_enum(X, y, lam, k)
    fA = fval(X, y, lam, A)[0]
    b53_zb = OPT - (Lp - Lm) / (lam + Lp) * (OPT - fA)
    b53_g = OPT - Lp / (lam + Lp) * (OPT - fA)
    tol = 1e-6 * abs(OPT)
    checks = dict(p31b=s1 <= gd + tol, l41iii=s1 <= iii + tol, p51=v >= gL - tol, p53_zb=v >= b53_zb - tol,
                  p53_g=g0 >= b53_g - tol, zb_ge_sdp1=v >= s1 - tol)
    checks = {kk: bool(vv) for kk, vv in checks.items()}
    bad += sum(not c for c in checks.values())
    print(json.dumps(dict(it=it, b=b, delta=delta, theta=theta, SDP1z=s1, g_delta=gd, P_plus_theta=iii, g=g0,
                          zbz=v, g_Lminus=gL, bound53_zb=b53_zb, bound53_g=b53_g, OPT=OPT, fA=fA, checks=checks),
                     default=float), flush=True)
print('failed checks:', bad)
