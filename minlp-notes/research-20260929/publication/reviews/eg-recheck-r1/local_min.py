"""Float evidence (not proof): how close does F come to theta* outside part 1?  For each part,
the 10 leaves with the smallest F at a feasible sample point (minF_p<k>.npy, own_consistency.py):
for every integer combination inside the leaf (at most 27 sampled) run SLSQP from 4 starts on
min t s.t. t >= c_k + h_k(x) (k < 24), side rows, x in the leaf; report the smallest F - theta*
at a point whose side-row violation is <= 1e-9."""
import itertools
import os
import sys

import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import own_consistency as oc  # noqa: E402

rng = np.random.default_rng(3)


def run(lo, hi, ints):
    best = (np.inf, None)
    cl, ch = lo[:4], hi[:4]

    def full(y):
        return np.concatenate([y[:4], ints])[None]

    def hrows(y):
        X = full(y)
        feats = np.concatenate([X, X * X], 1)
        E = feats @ oc.W + oc.C0.reshape(-1)[None]
        return ((np.exp(E).reshape(1, 28, 97) * oc.A[None]).sum(-1) + X @ oc.LIN.T)[0]

    def cons(y):
        h = hrows(y)
        out = list(y[4] - (oc.c + h[:24]))
        out += [v - h[k] for k, v in oc.side_hmax.items()]
        out += [h[k] - v for k, v in oc.side_hmin.items()]
        return np.array(out)

    for s in range(4):
        x0 = cl + rng.random(4) * (ch - cl)
        h0 = hrows(np.concatenate([x0, [0.0]]))
        y0 = np.concatenate([x0, [np.max(oc.c + h0[:24])]])
        r = minimize(lambda y: y[4], y0, method="SLSQP", constraints=[{"type": "ineq", "fun": cons}],
                     bounds=[(a, b) for a, b in zip(cl, ch)] + [(None, None)], options={"maxiter": 300, "ftol": 1e-12})
        F, viol = oc.evalF(full(r.x))
        if viol[0] <= 1e-9 and F[0] < best[0]:
            best = (F[0], full(r.x)[0])
    return best


for p in (0, 2, 3, 4, 5, 6, 7):
    z = np.load(os.path.join(HERE, f"leaves_p{p}.npz"))
    mf = np.load(os.path.join(HERE, f"minF_p{p}.npy"))
    best = (np.inf, None, None)
    for j in np.argsort(mf)[:10]:
        lo, hi = z["lo"][j], z["hi"][j]
        combos = list(itertools.product(*[range(int(lo[i]), int(hi[i]) + 1) for i in (4, 5, 6)]))
        if len(combos) > 27:
            combos = [combos[t] for t in rng.choice(len(combos), 27, replace=False)]
        for cmb in combos:
            F, x = run(lo, hi, np.array(cmb, float))
            if F < best[0]:
                best = (F, x, j)
    print(f"part {p}: smallest float F - theta* found {best[0] - oc.TH:.6g} at leaf {best[2]}, x {np.round(best[1], 6).tolist()}; "
          f"sampled minimum was {mf.min() - oc.TH:.4g}", flush=True)
