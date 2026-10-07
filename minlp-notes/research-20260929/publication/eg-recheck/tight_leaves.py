"""Sampling check (evidence, not proof) of the certificates with the smallest margins.

For the N leaves with the smallest margins in each part, minimize in floating point over the
leaf box (integer coordinates relaxed to their interval, as in the certificates):
  F_free = min max_k (c_k + g_k(x))                    (row certificates ignore the side rows)
  F_side = min max_k (c_k + g_k(x)) s.t. side rows     (LP certificates and split leaves)
from many starts (SLSQP on the epigraph form).  A certified leaf with margin m claims
F_side >= theta* + m, and for a row certificate at the leaf itself F_free >= theta* + m.
A float minimum below the claim (beyond about 1e-12) would expose a certifier error.
Float model: g_k(x) = sum_m a_km exp(sum_i gamma_ki (mu_kmi + s_i x_i)^2) + lin_k . x, with the
data of the review's GAMS reader (indep_cert.Model)."""
import glob
import os
import sys

import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import margin_cert  # noqa: E402,F401  (sets the path to the review's code)
from indep_cert import Model  # noqa: E402

TH = 5.642100574331458
M = Model("eg_disc2_s")
HOW = ["row", "side", "lp", "farkas", "empty", "split"]


def g(x):
    t = M.MU + M.S * x
    return (M.A * np.exp((M.GA[:, None, :] * t * t).sum(-1))).sum(-1) + M.LIN @ x


side_lo = [(j, M.glo[j]) for j in range(4) if np.isfinite(M.glo[j])]
side_hi = [(j, M.ghi[j]) for j in range(4) if np.isfinite(M.ghi[j])]


def fmin(lo, hi, side, starts, rng):
    best = np.inf
    bnds = list(zip(lo, hi)) + [(None, None)]
    cons = [{"type": "ineq", "fun": lambda z: z[-1] - M.c - g(z[:-1])[:24]}]
    if side:
        cons.append({"type": "ineq", "fun": lambda z: np.array([M.ghi[j] - g(z[:-1])[24 + j] for j, _ in side_hi]
                                                               + [g(z[:-1])[24 + j] - M.glo[j] for j, _ in side_lo])})
    for s in range(starts):
        x0 = lo + rng.random(len(lo)) * (hi - lo) if s else 0.5 * (lo + hi)
        z0 = np.append(x0, (M.c + g(x0)[:24]).max())
        r = minimize(lambda z: z[-1], z0, method="SLSQP", bounds=bnds, constraints=cons,
                     options=dict(maxiter=300, ftol=1e-15))
        x = np.clip(r.x[:-1], lo, hi)
        gx = g(x)
        if side and (any(gx[24 + j] > M.ghi[j] + 1e-9 for j, _ in side_hi) or any(gx[24 + j] < M.glo[j] - 1e-9 for j, _ in side_lo)):
            continue
        best = min(best, (M.c + gx[:24]).max())
    return best


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    parts = [int(a) for a in sys.argv[2:]] or list(range(8))
    rng = np.random.default_rng(5)
    worst = np.inf
    for k in parts:
        files = sorted(glob.glob(os.path.join(HERE, "res", f"p{k}_c*.npz")))
        Z = [np.load(f) for f in files]
        mg = np.concatenate([z["mg"] for z in Z]); how = np.concatenate([z["how"] for z in Z])
        lo = np.concatenate([z["lo"] for z in Z]); hi = np.concatenate([z["hi"] for z in Z])
        kind = np.concatenate([z["kind"] for z in Z])
        fin = np.where(np.isfinite(mg))[0]
        for j in fin[np.argsort(mg[fin])[:N]]:
            free = fmin(lo[j], hi[j], False, 24, rng)
            side = fmin(lo[j], hi[j], True, 24, rng)
            claim_free = how[j] == 0
            gap = (free if claim_free else side) - (TH + mg[j])
            worst = min(worst, gap)
            print(f"part {k} leaf {j} ({'closed box' if kind[j] == 0 else 'slab'}, {HOW[how[j]]}): margin {mg[j]:.3e}; "
                  f"float min F - theta*: free {free - TH:.3e}, with side rows {side - TH:.3e}; "
                  f"float min minus certified bound {gap:.3e}", flush=True)
    print(f"smallest (float min - certified bound) over the checked leaves: {worst:.3e} "
          f"({'no contradiction' if worst > -1e-12 else 'CONTRADICTION'})")


if __name__ == "__main__":
    main()
