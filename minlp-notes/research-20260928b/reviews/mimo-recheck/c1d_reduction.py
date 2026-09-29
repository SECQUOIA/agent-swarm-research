"""Item (2): Theorem 3.1(d), the single-node reduction for beta = 1.

For rho = theta N, the node with the single wrong fixing u_i = 2 (everything
else free) has value r_i = min ||v_i + B_{-i} u||^2, u in [0,2]^{N-1},
v_i = w + 2 b_i.  The note claims r_i = c^2 R', c^2 = 1 + 4 theta, where R' is
the root box value (error coordinates) of the model with N' = N-1 unknowns,
M = N observations, noise xi = v_i/c, matrix H~_{-i}, SNR
rho' = theta (N-1)/(1 + 4 theta).

Checks:
 (a) the identity on a few instances (algebra);
 (b) the law: r_0/c^2 over many instances versus R' of fresh, independent
     instances of the (N', M, rho') model (two-sample KS test), and the same
     for the largest NNLS coefficient U;
 (c) finite-N behaviour of the conclusion at theta = 0.2 < 1/4: frequency of
     node-0 box inactivity and of r_0 < W, for N = 100, 200, 400.
"""
import os
os.environ["OMP_NUM_THREADS"] = "1"; os.environ["OPENBLAS_NUM_THREADS"] = "1"
import numpy as np
from scipy.optimize import nnls
from scipy.stats import ks_2samp
from rc_common import make_instance, box_value


def node0(N, theta, seed):
    A, y, xs = make_instance(N, N, theta * N, seed)
    w = y - A @ xs
    B = A * xs
    v = w + 2 * B[:, 0]
    C = B[:, 1:]
    val, lb, u = box_value(C, v)
    un, _ = nnls(C, -v, maxiter=5000)
    return dict(W=float(w @ w), r=val, lb=lb, inactive=bool(un.max() <= 2.0),
                v=v, Ht=(A * xs)[:, 1:] / np.sqrt(theta), unmax=float(un.max()))


def root_reduced(Hp, xi, rho_p):
    Np = Hp.shape[1]
    Bp = np.sqrt(rho_p / Np) * Hp          # x*' = 1, so B' = A'
    val, lb, u = box_value(Bp, xi)
    un, _ = nnls(Hp / np.sqrt(Np), -xi, maxiter=5000)
    return val, float(un.max())


def main():
    theta = 0.2
    # (a) identity
    print("(a) identity r_0 = c^2 R'(xi = v_0/c, H' = H~_{-0}, rho'), N = 60, theta = 0.2")
    N = 60
    c2 = 1 + 4 * theta
    rho_p = theta * (N - 1) / c2
    for s in range(3):
        d = node0(N, theta, s)
        Rp, U = root_reduced(d["Ht"], d["v"] / np.sqrt(c2), rho_p)
        print("   seed %d: r_0 = %.10f  c^2 R' = %.10f  rel diff %.1e" % (s, d["r"], c2 * Rp, abs(d["r"] - c2 * Rp) / d["r"]))
    # (b) law
    print("(b) law of r_0/c^2 versus fresh root values R' (N', M, rho'), N = 100, theta = 0.2, 400 + 400 samples")
    N = 100
    rho_p = theta * (N - 1) / c2
    a, b, Ua, Ub = [], [], [], []
    for s in range(400):
        d = node0(N, theta, s)
        a.append(d["r"] / c2); Ua.append(d["unmax"] * np.sqrt(rho_p))   # node NNLS solution = reduced NNLS at rho'; U = sqrt(rho') max
        A2, y2, xs2 = make_instance(N - 1, N, rho_p, 100000 + s)
        w2 = y2 - A2 @ xs2
        B2 = A2 * xs2
        val, lb, u = box_value(B2, w2)
        un, _ = nnls(B2, -w2, maxiter=5000)
        b.append(val); Ub.append(float(un.max()) * np.sqrt(rho_p))
    print("   mean r_0/c^2 = %.3f, mean R' = %.3f; KS p-value = %.3f" % (np.mean(a), np.mean(b), ks_2samp(a, b).pvalue))
    print("   U = sqrt(rho') max NNLS coefficient (inactive iff U <= 2 sqrt(rho') = %.2f)" % (2 * np.sqrt(rho_p)))
    print("   U: medians %.3f / %.3f; KS p-value = %.3f" % (np.median(Ua), np.median(Ub), ks_2samp(Ua, Ub).pvalue))
    # (c) finite-N conclusion
    print("(c) theta = 0.2: node 0 box-inactive, r_0 < W, mean (r_0 - W)/N versus the first-order (4 theta - 1)/2 = %.3f" % ((4 * theta - 1) / 2))
    for N, S in ((100, 200), (200, 200), (400, 100)):
        ina = 0; below = 0; gaps = []; umax = []
        for s in range(S):
            d = node0(N, theta, 5000 + s)
            ina += d["inactive"]; below += d["lb"] < d["W"] and d["r"] < d["W"]
            gaps.append((d["r"] - d["W"]) / N); umax.append(d["unmax"])
        rp = theta * (N - 1) / c2
        print("   N=%d (%d instances): inactive %d, r_0 < W %d, mean (r_0-W)/N = %.3f, max NNLS coefficient: median %.3f max %.3f (inactive iff <= 2)"
              % (N, S, ina, below, np.mean(gaps), np.median(umax), np.max(umax)), flush=True)


if __name__ == "__main__":
    main()
