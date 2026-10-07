"""Reviewer's counterexample test for the headline of robust-chains.md Part 1 outside (H1).
Chain WALL: f_n = sum u(x_i) + b sum x_i x_{i+1} on [-1,1]^n, u = 1.022 t + 0.189 t^2 + 1.774 t^3 + 1.086 t^4,
b = 0.962 (symmetric coupling; bond phi minimized off the diagonal at (-1, c)).
mode roots: f*, balanced and class-(a) root gaps, n = 3..14.
mode sep n: wall configurations x^(j) (bulk phase A left, phase B right, wall bond (j,j+1), j odd) for even n;
  their values; class bound of the bounding box of each pair (balanced split = P_1 'bal', class (a) 'a').
  If every pair box has LB < f* - eps, no leaf of an S-cover contains two of them: N_S(eps) >= n/2.
mode bb CLS RULE EPS n: B&B leaves (cg4 bounds, rules as in the note).
Floating point."""
import sys, json, itertools, time
import numpy as np
from scipy.optimize import minimize, brentq
from cg4 import *

co = [0.0, 1.022, 0.189, 1.774, 1.086]; B = 0.962
u = PP.poly(co)
up = lambda t: np.polynomial.polynomial.polyval(t, np.polynomial.polynomial.polyder(co))


def fval(x):
    x = np.asarray(x, float)
    return float(np.sum(u(x)) + B * np.sum(x[:-1] * x[1:]))


def fstar(n):
    G = np.linspace(-1, 1, 4001)
    uG = u(G); V = uG.copy(); back = []
    for _ in range(1, n):
        M = V[:, None] + B * G[:, None] * G[None, :]
        j = np.argmin(M, axis=0); back.append(j)
        V = M[j, np.arange(len(G))] + uG
    k = int(np.argmin(V)); path = [k]
    for j in reversed(back):
        k = int(j[k]); path.append(k)
    x0 = G[np.array(path[::-1])]
    r = minimize(fval, x0, bounds=[(-1, 1)] * n, method="L-BFGS-B", options={"ftol": 1e-15, "gtol": 1e-13})
    return (r.fun, r.x) if r.fun < fval(x0) else (fval(x0), x0)


def tests(cls):
    return [PP.poly([0, 1])] if cls == "bal" else [PP.poly([0, 1]), PP.poly([0, 0, 1]), u]


c = brentq(lambda t: up(t) - 2 * B, -1, 1)   # interior site between two -1 neighbours: u'(c) = 2b
mode = sys.argv[1]
if mode == "roots":
    print(f"c = {c:.6f}; u'(-1) = {up(-1):.4f}", flush=True)
    for n in range(3, 15):
        fs, xs = fstar(n)
        out = dict(n=n, fstar=round(fs, 8), x=np.round(xs, 3).tolist())
        for cls in ("bal", "a"):
            cb = ClassBound(uniform_chain(n, u, B), tests(cls), K=7)
            lo, upb, it = cb.bound(np.full(n, -1.0), np.full(n, 1.0), None, maxit=200, tol=1e-9)
            out[cls] = [round(fs - upb, 6), round(fs - lo, 6)]
        print(json.dumps(out), flush=True)
elif mode == "sep":
    n = int(sys.argv[2]); eps = 1e-4
    fs, xs = fstar(n)
    confs = []
    for j in range(1, n, 2):          # wall bond (j, j+1), 1-based j odd
        x = np.zeros(n)
        for i in range(1, n + 1):
            if i <= j:
                x[i - 1] = -1.0 if i % 2 == 1 else c
            else:
                x[i - 1] = -1.0 if i % 2 == 0 else c
        confs.append(x)
    vals = [fval(x) for x in confs]
    print(f"n={n}: f* (DP) = {fs:.8f}; wall configurations: {len(confs)}, values - f* = {[round(v - fs, 10) for v in vals]}", flush=True)
    for cls in ("bal", "a"):
        worst = -np.inf; cnt_ok = 0
        for p, q in itertools.combinations(range(len(confs)), 2):
            l = np.minimum(confs[p], confs[q]); h = np.maximum(confs[p], confs[q])
            cb = ClassBound(uniform_chain(n, u, B), tests(cls), K=5)
            lo, upb, it = cb.bound(l, h, fs - eps, maxit=200, tol=1e-9)
            worst = max(worst, upb)        # upb: a consistent family on the pair box (upper bound on LB)
            cnt_ok += upb < fs - eps
        npairs = len(confs) * (len(confs) - 1) // 2
        print(f"   class {cls}: pairs with LB(pair box) < f* - eps (via primal family): {cnt_ok}/{npairs}; max primal value - f* = {worst - fs:+.5f}", flush=True)
elif mode == "bb":
    cls, rule, eps, n = sys.argv[2], sys.argv[3], float(sys.argv[4]), int(sys.argv[5])
    t0 = time.time()
    fs, xs = fstar(n)
    cb = ClassBound(uniform_chain(n, u, B), tests(cls), K=5)
    leaves, nodes = bb(cb, n, fs - eps, rule, maxnodes=60000)
    print(json.dumps(dict(family="WALL", cls=cls, rule=rule, eps=eps, n=n, fstar=fs, leaves=leaves, nodes=nodes, lpfail=cb.lpfail, time=round(time.time() - t0, 1))), flush=True)
