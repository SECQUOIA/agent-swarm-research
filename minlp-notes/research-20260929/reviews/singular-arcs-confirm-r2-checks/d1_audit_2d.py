"""Confirmation check d1 (independent code; nothing imported from the note's
scripts).  COPS catmix, trapezoidal rule, in the ORIGINAL 2-D form of the
COPS model (not the note's reduced projective model):

  x_{i+1} = x_i + h/2 (A(u_i) x_i + A(u_{i+1}) x_{i+1}),  i = 0..N-1,
  A(u) = [[-u, 10u], [u, -1-9u]],  x_0 = (1, 0),  J = x1_N + x2_N - 1.

Gradient: hand-written adjoint in mpmath (dps 40).  Hessian on the interior
arc stages: central differences of that gradient with step 1e-12 (truncation
~1e-24, rounding ~1e-28), converted to float for the eigen-decomposition.
Everything is in J units (the note's log(J+1) units differ by the factor
J+1 = 0.952; the rank-one term g g^T/(J+1)^2 is ~1e-18 and is ignored).

For each saved point: J; arc (first stage below 1 .. last stage above 0);
arc stages at a bound with their gradients and KKT signs; KKT signs on all
bang stages; max |g| on the interior arc stages; number of negative
eigenvalues, most negative eigenvalue, eigenvalues nearest zero; Newton step;
control range, deviation from the neighbour average, envelope sign changes.
For the Part L end points also: u and g at stages 129 and 138.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import sys
import time

import mpmath as mp
import numpy as np

mp.mp.dps = 40
TOL = 1e-9


def A(u):
    return mp.matrix([[-u, 10 * u], [u, -1 - 9 * u]])


AP = mp.matrix([[-1, 10], [1, -9]])
I2 = mp.eye(2)


def forward(u, h):
    N = len(u) - 1
    xs = [mp.matrix([1, 0])]
    Dinv = []
    for i in range(N):
        Di = mp.inverse(I2 - h / 2 * A(u[i + 1]))
        Dinv.append(Di)
        xs.append(Di * ((I2 + h / 2 * A(u[i])) * xs[-1]))
    return xs, Dinv


def grad(u, h):
    N = len(u) - 1
    xs, Dinv = forward(u, h)
    J = xs[N][0] + xs[N][1] - 1
    # r_i = dJ/dx_i (row), r_N = (1, 1); r_i = r_{i+1} M_i
    r = [None] * (N + 1)
    r[N] = mp.matrix([[1, 1]])
    for i in range(N - 1, -1, -1):
        r[i] = (r[i + 1] * Dinv[i]) * (I2 + h / 2 * A(u[i]))
    g = [mp.mpf(0)] * (N + 1)
    for i in range(N):
        # M_i = D_i^{-1} E_i, depends on u_i (E_i) and u_{i+1} (D_i)
        w = r[i + 1] * Dinv[i] * (h / 2 * AP)
        g[i] += (w * xs[i])[0]
        g[i + 1] += (w * xs[i + 1])[0]
    return J, g


def audit(path, N, extra=()):
    h = mp.mpf(1) / N
    uf = np.load(path)
    u = [mp.mpf(float(v)) for v in uf]
    t0 = time.time()
    J, g = grad(u, h)
    gf = np.array([float(v) for v in g])
    i0 = int(np.argmax(uf < 1 - TOL))
    i1 = int(np.max(np.where(uf > TOL)[0]))
    arc = list(range(i0, i1 + 1))
    atb = [j for j in arc if uf[j] <= TOL or uf[j] >= 1 - TOL]
    inter = [j for j in arc if j not in atb]
    wrong = [j for j in range(N + 1) if (uf[j] >= 1 - TOL and gf[j] > 1e-12) or (uf[j] <= TOL and gf[j] < -1e-12)]
    print("%s: N=%d J=%.13f arc %d..%d (m=%d); at a bound on the arc: %s with g %s; wrong KKT sign anywhere "
          "(tol 1e-12): %s; max|g| interior (%d stages) = %.3e"
          % (path, N, float(J), i0, i1, len(arc), atb, ["%.2e" % gf[j] for j in atb], wrong, len(inter),
             np.max(np.abs(gf[inter]))), flush=True)
    for j in extra:
        print("   stage %d: u = %.3e, g = %.3e" % (j, uf[j], gf[j]), flush=True)
    e = mp.mpf("1e-12")
    n = len(inter)
    H = np.zeros((n, n))
    for kk, k in enumerate(inter):
        up, um = list(u), list(u)
        up[k] += e
        um[k] -= e
        gp = grad(up, h)[1]
        gm = grad(um, h)[1]
        H[:, kk] = [float((gp[j] - gm[j]) / (2 * e)) for j in inter]
    asym = np.max(np.abs(H - H.T))
    H = (H + H.T) / 2
    ev, V = np.linalg.eigh(H)
    order = np.argsort(np.abs(ev))
    step = np.linalg.solve(H, -gf[inter])
    print("   Hessian (J units, %d x %d, asymmetry %.1e): #neg=%d, most negative %.4e, nearest 0 %s, largest %.3e; "
          "Newton step max|du| = %.3e  (%.0f s)"
          % (n, n, asym, int(np.sum(ev < 0)), ev[0], ["%.2e" % ev[k] for k in order[:4]], ev[-1],
             np.max(np.abs(step)), time.time() - t0), flush=True)
    idx = np.arange(i0 + 1, i1)
    dev = np.abs(uf[idx] - 0.5 * (uf[idx - 1] + uf[idx + 1]))
    env = ((-1.0) ** idx) * (uf[idx] - 0.5 * (uf[idx - 1] + uf[idx + 1]))
    ch = [int(idx[k]) for k in range(1, len(idx)) if env[k] * env[k - 1] < 0]
    print("   u range interior [%.4f, %.4f], whole arc [%.4f, %.4f]; max deviation from neighbour average %.3f "
          "(stage %d); envelope sign changes %s, spacings %s"
          % (uf[inter].min(), uf[inter].max(), uf[arc].min(), uf[arc].max(), dev.max(), int(idx[np.argmax(dev)]),
             ch, np.diff(ch).tolist()), flush=True)


if __name__ == "__main__":
    base = (_PUBLIC_REPO + '/research-20260929/theory-bangbang/singular/logs/')
    which = sys.argv[1:] or ["100", "200", "L400", "L4000"]
    if "100" in which:
        audit(base + "catmix100_smooth_u.npy", 100)
    if "200" in which:
        audit(base + "catmix200_smooth_u.npy", 200)
    if "L400" in which:
        audit(base + "catmix200_r2_attempt_u.npy", 200, extra=(118, 120, 129, 138))
    if "L4000" in which:
        audit(base + "catmix200_r2_attempt4000_u.npy", 200, extra=(118, 120, 129, 138))
