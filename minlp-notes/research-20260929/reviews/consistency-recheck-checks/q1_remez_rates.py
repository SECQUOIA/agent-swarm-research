"""Recheck Q1: best uniform approximation errors used in Section 5.4 / 7.1.

Independent of the note's LP and of the first review's grid Remez:
a Remez exchange whose extrema are refined by bounded scalar optimisation
between grid points (so the reference is not restricted to a grid).
Returned values: lev = min |error| on an alternating reference
(de la Vallee Poussin lower bound, up to rounding) and emax = max |error|
over refined local extrema (upper estimate).

  E_n(|x|)   : even best approximant; on [0,1] approximate x by T_0,T_2,..,T_2m
  E_n(x|x|)  : odd best approximant;  on (0,1] approximate x^2 by T_1,T_3,..,T_2m+1
"""
import sys
import time
import numpy as np
from numpy.polynomial import chebyshev as C
from scipy.optimize import minimize_scalar


def remez(f, degs, npts_grid, iters=80, tol=1e-12):
    d = len(degs)
    # grid on [0,1]: x = cos(theta), theta in [0, pi/2]; resolves oscillations
    th = np.linspace(0.0, np.pi / 2, npts_grid)
    x = np.sort(np.cos(th))
    x = x[x > 0]
    V = lambda t: C.chebvander(np.atleast_1d(t), max(degs))[:, degs]
    fx = f(x)
    Bx = V(x)
    # initial reference: d+1 points spread in (0,1]
    ref = np.sort(np.cos(np.pi * (np.arange(d + 1) + 0.5) / (2 * (d + 1))))
    lev = emax = None
    for it in range(iters):
        A = np.hstack([V(ref), ((-1.0) ** np.arange(d + 1))[:, None]])
        sol = np.linalg.solve(A, f(ref))
        c, h = sol[:d], sol[d]
        err = lambda t: f(np.atleast_1d(t)) - V(t) @ c
        e = fx - Bx @ c
        # local extrema candidates on the grid
        de = np.diff(e)
        idx = np.nonzero(de[:-1] * de[1:] <= 0)[0] + 1
        idx = np.concatenate([[0], idx, [len(x) - 1]])
        pts, vals = [], []
        for i in idx:
            lo = x[max(i - 1, 0)]
            hi = x[min(i + 1, len(x) - 1)]
            s = np.sign(e[i]) if e[i] != 0 else 1.0
            if i in (0, len(x) - 1):
                xs = x[i]
                # also try interior refinement next to an endpoint
                r = minimize_scalar(lambda t: -s * err(t)[0], bounds=(lo, hi), method="bounded",
                                    options={"xatol": 1e-15})
                if -r.fun > s * e[i]:
                    xs = r.x
            else:
                r = minimize_scalar(lambda t: -s * err(t)[0], bounds=(lo, hi), method="bounded",
                                    options={"xatol": 1e-15})
                xs = r.x if -r.fun >= s * e[i] else x[i]
            pts.append(xs)
            vals.append(err(xs)[0])
        pts, vals = np.array(pts), np.array(vals)
        order = np.argsort(pts)
        pts, vals = pts[order], vals[order]
        # merge same-sign runs keeping the largest |error|
        gp, gv = [], []
        for p, v in zip(pts, vals):
            if v == 0:
                continue
            if gv and np.sign(gv[-1]) == np.sign(v):
                if abs(v) > abs(gv[-1]):
                    gp[-1], gv[-1] = p, v
            else:
                gp.append(p); gv.append(v)
        gp, gv = list(gp), list(gv)
        emax = max(abs(v) for v in gv)
        while len(gp) > d + 1:
            if abs(gv[0]) < abs(gv[-1]):
                gp.pop(0); gv.pop(0)
            else:
                gp.pop(); gv.pop()
        if len(gp) < d + 1:
            raise RuntimeError(f"lost alternation: {len(gp)} < {d + 1}")
        ref = np.array(gp)
        lev = min(abs(v) for v in gv)
        if emax - lev <= tol * emax:
            break
    return lev, emax, it + 1


def E_abs(n):
    m = n // 2
    return remez(lambda t: t, list(range(0, 2 * m + 1, 2)), 60 * n + 2000)


def E_xabsx(n):
    m = (n - 1) // 2
    return remez(lambda t: t ** 2, list(range(1, 2 * m + 2, 2)), 60 * n + 2000)


if __name__ == "__main__":
    beta = 0.2801694990238691  # Varga-Carpenter
    t0 = time.time()
    print("E_n(|x|): gap = 2 E_n, n * gap (-> 2 beta = %.6f)" % (2 * beta))
    Eabs = {}
    for n in [4, 8, 16, 32, 64, 128, 256]:
        lo, hi, it = E_abs(n)
        Eabs[n] = lo
        print(f"  n={n:4d}: E_n in [{lo:.10e}, {hi:.10e}] ({it} it), n*2E_n = {2 * n * lo:.6f}")
    sys.stdout.flush()
    print("E_n(x|x|) = 2 E_n((x_+)^2): n^2 * gap")
    Eq = {}
    for n in [4, 8, 16, 32, 64, 128, 256, 512, 1024]:
        lo, hi, it = E_xabsx(n)
        Eq[n] = lo
        print(f"  n={n:4d}: E_n in [{lo:.10e}, {hi:.10e}] ({it} it), n^2 gap = {n * n * lo:.6f}")
        sys.stdout.flush()
    ns = [64, 128, 256, 512, 1024]
    v = [n * n * Eq[n] for n in ns]
    print("  differences:", ["%.6f" % (v[i] - v[i + 1]) for i in range(len(v) - 1)])
    print("  ratios of differences:",
          ["%.4f" % ((v[i + 1] - v[i + 2]) / (v[i] - v[i + 1])) for i in range(len(v) - 2)])
    # Aitken on the last three and a fit K + a/n + b/n^2 on the last three
    a, b, c = v[-3:]
    aitken = c - (c - b) ** 2 / ((c - b) - (b - a))
    nn = np.array(ns[-3:], float)
    K = np.linalg.solve(np.column_stack([np.ones(3), 1 / nn, 1 / nn ** 2]), np.array(v[-3:]))[0]
    print(f"  extrapolated limit: Aitken {aitken:.5f}; fit K+a/n+b/n^2 {K:.5f}")
    # Also from the note's three values only (n = 64, 128, 256)
    a, b, c = v[0:3]
    print(f"  extrapolation from n=64,128,256 only (Aitken): {c - (c - b) ** 2 / ((c - b) - (b - a)):.5f}")
    Klim = K
    print(f"  ideal gap ~ K/(4 R^2) = {Klim / 4:.5f}/R^2; [S] 2/(27 pi (2R+2)^2) ~ {1 / (54 * np.pi):.6f}/R^2;"
          f" ratio -> {Klim / 4 * 54 * np.pi:.3f}")
    print(f"  affine recourse: 9 pi beta = {9 * np.pi * beta:.4f}")
    print("finite-R ratios ideal / [S] explicit bound")
    for R in [2, 4, 8, 16, 32]:
        n = 2 * R
        ra = 2 * Eabs[n] * 9 * np.pi * (R + 1)
        rq = 2 * (Eq[n] / 2) / (2 / (27 * np.pi * (2 * R + 2) ** 2))
        print(f"  R={R:3d}: affine recourse {ra:.3f}; quadratic {rq:.3f}")
    print(f"elapsed {time.time() - t0:.1f} s")
