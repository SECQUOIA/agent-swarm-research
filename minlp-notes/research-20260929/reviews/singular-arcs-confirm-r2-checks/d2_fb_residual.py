"""Confirmation check d2 (diagnostic; uses the note's own functions, run from
theory-bangbang/singular/).  Which entries dominate the Fischer-Burmeister
residual of Part L, at the saved N = 200 point and at the two end points."""
import sys
sys.path.insert(0, ".")
import numpy as np
import revision2_catmix as R2
import catmix_trap as C
import catmix_windows as W

N = 200
R = C.Red(N)
an = W.analytic2(N)
i0, i1 = R2.arc_of(np.load("logs/catmix200_smooth_u.npy"))
A = np.arange(i0, i1 + 1)
for f in ("logs/catmix200_smooth_u.npy", "logs/catmix200_r2_attempt_u.npy", "logs/catmix200_r2_attempt4000_u.npy"):
    u = np.load(f)
    c, g, H = R2.exact_grad_hess(R, an, u)
    sc = 1.0 / np.max(np.abs(np.diag(H)[A]))
    r, rho = R2.fb(u[A], sc * g[A])
    o = np.argsort(-np.abs(r))[:6]
    print(f, "sc=%.3e |r|=%.3e" % (sc, np.linalg.norm(r)), "top entries (stage, r, u, g):",
          [(int(A[k]), "%.2e" % r[k], "u=%.2e" % u[A[k]], "g=%.2e" % g[A[k]]) for k in o], flush=True)
