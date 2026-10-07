"""Confirmation check c2: the saved catmix KKT points of catmix_trap.py
(logs/catmix{100,200}_smooth_u.npy) and the stored COPS chattering points.
Uses the note's reduced model (catmix_trap.Red: objective and adjoint
gradient), which the first review cross-checked against an independent 2-D
mpmath implementation.  Reports:
 (a) the alternating envelope and where it changes sign;
 (b) at N = 200: which arc stages sit at a bound, the KKT signs there,
     max |gradient| on interior stages, the Hessian on the interior stages
     (central differences, two step sizes), its eigenvalues nearest zero, the
     number of negative eigenvalues, and the size of the Newton step;
 (c) the arc stages of the stored COPS points (first stage below 1, last
     stage above 0).
Run from theory-bangbang/singular (relative paths), PYTHONDONTWRITEBYTECODE=1.
"""
import sys

import numpy as np

sys.path.insert(0, ".")
import catmix_trap as C  # noqa: E402

U_S = 0.227142082708498


def envelope(u, i0, i1):
    v = u[i0:i1 + 1]
    # alternating component: (-1)^k (v_k - (v_{k-1}+v_{k+1})/2) / 2
    k = np.arange(1, len(v) - 1)
    alt = ((-1.0) ** k) * (v[1:-1] - 0.5 * (v[:-2] + v[2:])) / 2
    s = np.sign(alt)
    ch = [int(k[j + 1] - 0) for j in range(len(s) - 1) if s[j] != 0 and s[j + 1] != 0 and s[j] != s[j + 1]]
    return alt, ch


def hess(R, u, free, e):
    n = len(free)
    H = np.zeros((n, n))
    for jj, j in enumerate(free):
        up, um = u.copy(), u.copy()
        up[j] += e
        um[j] -= e
        H[:, jj] = (R.grad_logJ(up)[1][free] - R.grad_logJ(um)[1][free]) / (2 * e)
    return (H + H.T) / 2


for N in (100, 200):
    R = C.Red(N)
    u = np.load("logs/catmix%d_smooth_u.npy" % N)
    i0 = int(np.argmax(u < 1 - 1e-9))
    i1 = int(np.max(np.where(u > 1e-9)[0]))
    alt, ch = envelope(u, i0, i1)
    sp = np.diff(ch)
    print("N=%d arc stages %d..%d (%d); arc u range [%.4f, %.4f]; envelope sign changes at arc offsets %s; "
          "spacings %s; mean spacing over the regular part %.2f"
          % (N, i0, i1, i1 - i0 + 1, u[i0:i1 + 1].min(), u[i0:i1 + 1].max(), ch, sp.tolist(),
             float(np.mean(sp[:min(len(sp), 7)]))), flush=True)
    cost, g = R.grad_logJ(u)
    inner = np.arange(i0, i1 + 1)
    atb = [int(j) for j in inner if u[j] <= 1e-9 or u[j] >= 1 - 1e-9]
    free = np.array([j for j in inner if j not in atb])
    print("   J=%.13f; arc stages at a bound: %s with u=%s and gradient %s (lower bound needs g >= 0, upper g <= 0)"
          % (np.exp(cost) - 1, atb, [float(u[j]) for j in atb], ["%.2e" % g[j] for j in atb]), flush=True)
    # KKT signs on the bang stages as well
    bad = [j for j in range(N + 1) if (u[j] >= 1 - 1e-9 and g[j] > 1e-12) or (u[j] <= 1e-9 and g[j] < -1e-12)]
    print("   bound stages with a wrong KKT sign (tolerance 1e-12): %s; max |g| on %d interior stages = %.2e"
          % (bad, len(free), np.max(np.abs(g[free]))), flush=True)
    for e in (1e-6, 1e-5):
        H = hess(R, u, free, e)
        ev, V = np.linalg.eigh(H)
        order = np.argsort(np.abs(ev))
        step = np.linalg.solve(H, -g[free])
        print("   FD step %.0e: #neg=%d, most negative %.4e, smallest |eig| %s, largest eig %.3e, "
              "Newton step max|du|=%.2e"
              % (e, int(np.sum(ev < 0)), ev[0], ["%.2e" % ev[i] for i in order[:4]], ev[-1],
                 np.max(np.abs(step))), flush=True)

for N in (100, 200, 400):
    uc = np.load(C.COPS % N)
    i0 = int(np.argmax(uc < 1 - 1e-9))
    i1 = int(np.max(np.where(uc > 1e-9)[0]))
    print("COPS stored N=%d: first arc stage %d (t=%.4f, stage interval starts %.4f), last arc stage %d, m=%d; "
          "u[i0-1..i0+2]=%s" % (N, i0, i0 / N, (i0 - 0.5) / N, i1, i1 - i0 + 1,
                                 np.round(uc[i0 - 1:i0 + 3], 4).tolist()), flush=True)
