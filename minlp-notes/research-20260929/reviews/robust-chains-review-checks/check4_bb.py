"""Reviewer's independent B&B counts (cg.py bounds; same rules as the note: widest-side bisection with
lowest index on ties, or 'spread' = largest marginal variance in the node's primal LP family).
Usage: python3 check4_bb.py FAMILY CLS RULE EPS n
  FAMILY chiral: CLS = P1 | P2 | P3   (b,g,ev) = (0.6,0.3,0.05), f* = 0
  FAMILY ud:     CLS = bal | unsplit | a   (UD chain, b = 0.6), f* by grid DP + polish
"""
import sys, json, time
import numpy as np
from scipy.optimize import minimize
from cg import *


def ud_fstar(u, B, n):
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
    f = lambda x: float(np.sum(u(x)) + B * np.sum(x[:-1] * x[1:]))
    r = minimize(f, x0, bounds=[(-1, 1)] * n, method="L-BFGS-B", options={"ftol": 1e-15, "gtol": 1e-13})
    return min(r.fun, f(x0))


if __name__ == "__main__":
    fam, cls, rule, eps, n = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), int(sys.argv[5])
    t0 = time.time()
    if fam == "chiral":
        ch = chiral_chain(n, 0.6, 0.3, 0.05); tests = poly_tests(int(cls[1:])); fs = 0.0
    else:
        u = ud_u(); B = 0.6
        base = "unsplit" if cls == "unsplit" else "balanced"
        ch = uniform_chain(n, u, B, base)
        tests = [PP.poly([0, 1])] if cls in ("bal", "unsplit") else [PP.poly([0, 1]), PP.poly([0, 0, 1]), u]
        fs = ud_fstar(u, B, n)
    cb = ClassBound(ch, tests, K=5)
    leaves, nodes = bb(cb, n, fs - eps, rule)
    print(json.dumps(dict(family=fam, cls=cls, rule=rule, eps=eps, n=n, fstar=fs, leaves=leaves, nodes=nodes,
                          lpfail=cb.lpfail, time=round(time.time() - t0, 1))), flush=True)
