"""Self-test of the reviewer's rigorous stage bound: for random rays (off-grid), the rigorous lower
bound must not exceed a dense float minimisation of W(n(u))/D(u) over u in [0,1], and should be close.
Also prints the primal trajectory theta_i = y_i2/(y_i1+y_i2) for the authors' controls."""
import os
import sys

import numpy as np

import v_catmix_dp as D

# research-20260929/ of this checkout (this file is in research-20260929/reviews/<dir>/)
R29 = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

N = int(sys.argv[1]) if len(sys.argv) > 1 else 100
maps = D.Maps(N)
grid = D.make_grid(11)
w, _ = D.terminal(maps, grid)
w = np.maximum(w, 0)
S = maps.stage
Dm = [D.mid(c) for c in S["D"]]


def dense_min(th, W_grid, W_w, S, nu=20001):
    r1, r2 = 1 - th, th
    u = np.linspace(0, 1, nu)
    best = np.full(len(th), np.inf)
    bu = np.zeros(len(th))
    for j in range(len(th)):
        n1 = sum(D.mid(S["N11"][d]) * r1[j] * u ** d + D.mid(S["N12"][d]) * r2[j] * u ** d for d in range(3))
        n2 = sum(D.mid(S["N21"][d]) * r1[j] * u ** d + D.mid(S["N22"][d]) * r2[j] * u ** d for d in range(3))
        dd = D.fpoly([D.mid(c) for c in S["D"]], u)
        f = (n1 + n2) * np.interp(n2 / (n1 + n2), W_grid, W_w) / dd
        k = np.argmin(f)
        # local refinement on a finer grid around the best sample
        lo, hi = max(0, u[k] - 2 / nu), min(1, u[k] + 2 / nu)
        uu = np.linspace(lo, hi, 20001)
        n1 = sum(D.mid(S["N11"][d]) * r1[j] * uu ** d + D.mid(S["N12"][d]) * r2[j] * uu ** d for d in range(3))
        n2 = sum(D.mid(S["N21"][d]) * r1[j] * uu ** d + D.mid(S["N22"][d]) * r2[j] * uu ** d for d in range(3))
        dd = D.fpoly([D.mid(c) for c in S["D"]], uu)
        ff = (n1 + n2) * np.interp(n2 / (n1 + n2), W_grid, W_w) / dd
        best[j] = min(f[k], ff.min())
        bu[j] = uu[np.argmin(ff)]
    return best, bu


rng = np.random.default_rng(0)
worst_viol, worst_gap = -np.inf, 0.0
for it in range(40):                     # walk the DP back 40 stages, testing each stage
    th = np.concatenate([rng.uniform(0, 0.1016, 12), rng.uniform(0.1016, 1, 3), [0.0, 1.0]])
    th = np.round(th * 2.0 ** 40) / 2.0 ** 40
    lb, st = D.stage(S, grid, w, th)
    dm, bu = dense_min(th, grid, w, S)
    worst_viol = max(worst_viol, float(np.max(lb - dm)))
    worst_gap = max(worst_gap, float(np.max(dm - lb)))
    w, _ = D.stage(S, grid, w, grid)
    w = np.maximum(w, 0)
print("N=%d stage self-test over 40 stages x 17 rays: max(LB - dense_min) = %.3g (must be <= ~1e-15), "
      "max(dense_min - LB) = %.3g" % (N, worst_viol, worst_gap))

# trajectory of the authors' controls
u = np.load(os.path.join(R29, "open-instances-wave2/cops/logs/catmix%d_u.npy") % N)
K = {k: float(v) for k, v in maps.K.items()}
a, b, c, ep, em = K["a"], K["b"], K["c"], K["ep"], K["em"]
x = np.array([1.0, 0.0])
ths = []
for i in range(N):
    Q = np.array([[1 - a * u[i], b * u[i]], [a * u[i], em - c * u[i]]])
    y = Q @ x
    ths.append(y[1] / y.sum())
    P = np.array([[1 + a * u[i + 1], -b * u[i + 1]], [-a * u[i + 1], ep + c * u[i + 1]]])
    x = np.linalg.solve(P, y)
ths = np.array(ths)
print("controls u (rounded):", np.round(u, 4).tolist())
print("theta_i range:", ths.min(), ths.max())
sing = np.where((u > 1e-6) & (u < 1 - 1e-6))[0]
print("interior-control stages:", sing.min() if len(sing) else None, sing.max() if len(sing) else None,
      "theta there:", ths[sing[sing < N]].min() if len(sing) else None, ths[sing[sing < N]].max() if len(sing) else None)
np.save("logs/catmix%d_theta_traj.npy" % N, ths)
