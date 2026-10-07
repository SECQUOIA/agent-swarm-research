"""Independent rigorous bracket [LB, UB] on min F for the probe3 chain family.

F(x) = sum_i u_i(x_i) + b sum_i x_i x_{i+1},  u_i(x) = x^2 - kappa x^4 + c_i x,  x in [-1,1]^n.

Method (independent of chain_bb.py: no transfers, no Taylor bounds, no pruning):
value-function DP on a uniform grid G of K points including the endpoints -1, 1.
  V_n = u_n,  V_i(x) = u_i(x) + W_i(x),  W_i(x) = min_{y in [-1,1]} [b x y + V_{i+1}(y)].
W_i is concave in x (a minimum of affine functions), and u_i(x) - x^2 is concave
(kappa >= 0), so V_i(x) - x^2 is concave. Hence phi(y) = b x y + V_{i+1}(y) satisfies
phi - y^2 concave, and on any grid interval of width h,
  phi(y) >= min(phi at the two endpoints) - 2 h^2 / 8 = min(...) - h^2/4.
So, with Vhat <= V at grid points,
  Vhat_i(x_k) = u_i(x_k) + min_j [b x_k y_j + Vhat_{i+1}(y_j)] - h^2/4 - fp
is <= V_i(x_k), and LB = min_k Vhat_1(x_k) - h^2/4 - fp <= min F.
Total discretization loss: n h^2 / 4. fp: 1e-12 per stage (values are O(n), rounding
per stage is below 1e-13 for n <= 100).
UB: F at the grid argmin path, then L-BFGS-B polishing from it; UB = F at a point of the box.
"""
import sys, json, time
import numpy as np
from scipy.optimize import minimize

KAPPA, B = 0.1, 0.8


def coeffs(n, seed, amp):
    return np.random.default_rng(seed).uniform(-amp, amp, n)


def F(x, c):
    return float(np.sum(x * x - KAPPA * x**4 + c * x) + B * np.sum(x[:-1] * x[1:]))


def grad(x, c):
    g = 2 * x - 4 * KAPPA * x**3 + c
    g[:-1] += B * x[1:]
    g[1:] += B * x[:-1]
    return g


def grid_dp(c, K):
    n = len(c)
    y = np.linspace(-1.0, 1.0, K)
    h = 2.0 / (K - 1)
    loss = h * h / 4 + 1e-12
    V = y * y - KAPPA * y**4 + c[n - 1] * y          # V_n exact at grid points
    arg = []
    for i in range(n - 2, -1, -1):
        W = np.empty(K); A = np.empty(K, int)
        for k0 in range(0, K, 400):
            M = B * y[k0:k0 + 400, None] * y[None, :] + V[None, :]
            A[k0:k0 + 400] = M.argmin(axis=1)
            W[k0:k0 + 400] = M.min(axis=1)
        arg.append(A)
        V = y * y - KAPPA * y**4 + c[i] * y + W - loss
    LB = float(V.min()) - loss
    # grid argmin path
    k = int(V.argmin()); path = [k]
    for A in reversed(arg):
        k = int(A[k]); path.append(k)
    xg = y[np.array(path)]
    return LB, xg


def polish(x0, c):
    r = minimize(F, x0, jac=grad, args=(c,), method="L-BFGS-B", bounds=[(-1, 1)] * len(c),
                 options=dict(ftol=1e-15, gtol=1e-13, maxiter=20000))
    return r.x, F(r.x, c)


if __name__ == "__main__":
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 4001
    cases = json.loads(sys.argv[2]) if len(sys.argv) > 2 else \
        [[0.2, n, s] for n in (6, 10, 20, 50) for s in range(5)]
    for amp, n, seed in cases:
        c = coeffs(n, seed, amp)
        t0 = time.time()
        LB, xg = grid_dp(c, K)
        Fg = F(xg, c)
        xp, Fp = polish(xg, c)
        UB = min(Fg, Fp)
        rec = dict(amp=amp, n=n, seed=seed, K=K, LB=LB, UB_grid=Fg, UB=UB, gap=UB - LB,
                   disc_loss=n * (2.0 / (K - 1)) ** 2 / 4, n_at_bound=int((np.abs(xp) > 1 - 1e-9).sum()),
                   max_abs_x=float(np.abs(xp).max()), time=time.time() - t0)
        print(json.dumps(rec), flush=True)
