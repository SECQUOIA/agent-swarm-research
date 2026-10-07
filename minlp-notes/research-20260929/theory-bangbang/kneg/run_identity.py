"""Check of the kappa-split identity (kappa-negative.md, Proposition 2.1) and of when the kappa-free part is
convex.

Identity (b constant, l_1 affine in x):  J(u) = Jt(u) + (h^2/2) sum_t kappa_t u_t^2,  kappa_t = -grad l_1(t)^T b,
where Jt evaluates l_1 at x_t + (h/2) b u_t instead of x_t.  Checked in exact rational arithmetic at random
rational controls on the scalar toy plus and on extension-n2.md's two-state examples A, A- and A0'.
Then the reduced Hessian H of J (J is an exact quadratic in u for these data) and G = H - h^2 diag(kappa_t)
(the Hessian of Jt): smallest eigenvalues / h^2 (float, numpy eigvalsh).

usage: OMP_NUM_THREADS=1 python3 run_identity.py   ->  logs/identity.json
"""
import json
import os
import random
import sys
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# two-state examples of extension-n2.md (data as in window/n2win.py; Phi = -a x1 + rho x2^2 / 2, a = 1)
EX2 = {
    "A (kappa=+0.3)": dict(rho=2, k1=-0.3, k2=-0.3, q=0.3, c=1, e=0.0, x10=0.0, x20=0.5, a=1.0),
    "A- (kappa=-0.3)": dict(rho=2, k1=-0.3, k2=0.3, q=0.3, c=1, e=0.0, x10=0.0, x20=0.5, a=1.0),
    "A0' (kappa=0)": dict(rho=2, k1=-0.3, k2=0.0, q=0.3, c=1, e=0.0, x10=0.0, x20=0.5, a=1.0),
}


def J2(p, N, u, tilde=False, F=Fr):
    """Euler cost of the two-state example; tilde: l_1 evaluated at x + (h/2) b u."""
    h = F(2) / N
    x1, x2 = F(p["x10"]), F(p["x20"])
    k1, k2, q, c, e = (F(p[k]) for k in ("k1", "k2", "q", "c", "e"))
    J = F(0)
    for t in range(N):
        ut = u[t]
        x2l = x2 + h * ut / 2 if tilde else x2
        J += h * (e * x2 + q * x1 * x1 / 2 - c * x2 * x2 / 2 + (k1 * x1 + k2 * x2l) * ut)
        x1, x2 = x1 + h * x2, x2 + h * ut
    J += -F(p["a"]) * x1 + F(p["rho"]) * x2 * x2 / 2
    return J


def Jtoy(N, u, tilde=False, k=Fr(1, 2)):
    """Toy plus: x' = u, a = 2 on [0, 1), -1 after, k x u, Phi = x."""
    h = Fr(2) / N
    x = Fr(0)
    J = Fr(0)
    for t in range(N):
        a = Fr(2) if 2 * t < N else Fr(-1)
        xl = x + h * u[t] / 2 if tilde else x
        J += h * ((x - a) ** 2 / 2 + k * xl * u[t])
        x += h * u[t]
    return J + x


def hess2(p, N):
    """Reduced Hessian of J (float): x_t = x_t(0) + sum_{s<t} M[t][s] u_s, M[t][s] = h F^{t-1-s} b."""
    h = 2.0 / N
    F = np.array([[1.0, h], [0.0, 1.0]])
    b = np.array([0.0, 1.0])
    M = np.zeros((N + 1, N, 2))
    for t in range(1, N + 1):
        M[t] = M[t - 1] @ F.T
        M[t, t - 1] = h * b
    Hl0 = np.diag([p["q"], -p["c"]])
    kv = np.array([p["k1"], p["k2"]])
    H = np.zeros((N, N))
    for t in range(N):
        Mt = M[t]
        H += h * Mt @ Hl0 @ Mt.T
        v = h * Mt @ kv                    # d(k.x_t)/du_s * h
        H[:, t] += v
        H[t, :] += v
    Phixx = np.diag([0.0, p["rho"]])
    H += M[N] @ Phixx @ M[N].T
    return H


def main():
    random.seed(1)
    out = dict(identity=[], spectra=[])
    # exact identity checks
    for N in (20, 50):
        u = [Fr(random.randint(-1000, 1000), 1000) for _ in range(N)]
        h = Fr(2) / N
        r = Jtoy(N, u) - Jtoy(N, u, tilde=True) - h * h / 2 * (-Fr(1, 2)) * sum(v * v for v in u)
        out["identity"].append(dict(example="toy plus (kappa=-0.5)", N=N, residual_exact=str(r)))
        for name, p in EX2.items():
            kap = -Fr(p["k2"])
            r = J2(p, N, u) - J2(p, N, u, tilde=True) - h * h / 2 * kap * sum(v * v for v in u)
            out["identity"].append(dict(example=name, N=N, residual_exact=str(r)))
    # spectra
    for N in (100, 200, 400, 800):
        h = 2.0 / N
        idx = np.arange(N)
        mx = np.maximum.outer(idx, idx)
        Ht = h * h * (h * (N - 1 - mx) + 0.0 + 0.5 * (1 - np.eye(N)))      # toy plus, kappa = -0.5
        ev = np.linalg.eigvalsh(Ht)
        evG = np.linalg.eigvalsh(Ht + 0.5 * h * h * np.eye(N))
        out["spectra"].append(dict(example="toy plus", N=N, kappa=-0.5, lam_min_H_over_h2=ev[0] / h ** 2,
                                   lam_min_G_over_h2=evG[0] / h ** 2, n_neg_H=int(np.sum(ev < 0)),
                                   n_neg_G=int(np.sum(evG < -1e-12 * abs(evG).max()))))
        for name, p in EX2.items():
            H = hess2(p, N)
            kap = -p["k2"]
            ev = np.linalg.eigvalsh(H)
            evG = np.linalg.eigvalsh(H - kap * h * h * np.eye(N))
            out["spectra"].append(dict(example=name, N=N, kappa=kap, lam_min_H_over_h2=ev[0] / h ** 2,
                                       lam_min_G_over_h2=evG[0] / h ** 2, n_neg_H=int(np.sum(ev < 0)),
                                       n_neg_G=int(np.sum(evG < -1e-12 * abs(evG).max()))))
    for r in out["identity"] + out["spectra"]:
        print(json.dumps(r, default=float))
    with open(os.path.join(HERE, "logs", "identity.json"), "w") as f:
        json.dump(out, f, indent=1, default=float)


if __name__ == "__main__":
    main()
