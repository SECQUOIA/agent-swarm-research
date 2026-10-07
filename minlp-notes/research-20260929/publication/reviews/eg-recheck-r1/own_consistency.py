"""Large-scale soundness consistency test of the recorded certificates (evidence, float64).

For every leaf of every part: evaluate F and the side rows (own model data, own_model.py, float64
with numpy exp) at the leaf centre and at 4 random points of the leaf (integer coordinates drawn
among the integers of the leaf).  A certified margin mg says: every point of the leaf that
satisfies the side rows has F >= theta* + mg (for row certificates at the leaf itself, every
point at all).  A float value F(p) < theta* + mg - 1e-9 at such a point would expose an unsound
certificate.  Also reports, per part, the smallest F - theta* seen at feasible points (where the
function is lowest), and saves per-leaf minima for the sample selection of own_sample.py.
"""
import os
import sys
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from own_model import OsilModel  # noqa: E402

TH = float(Fr("5.642100574331458"))
O = OsilModel()
R, Mt = 28, 97
# E_km(x) = sum_i g_ki (mu_kmi + s_i x_i)^2 = C0_km + sum_i B_kmi x_i + sum_i D_ki x_i^2
C0 = np.zeros((R, Mt)); B = np.zeros((R, Mt, 7)); D = np.zeros((R, Mt, 7)); A = np.zeros((R, Mt)); LIN = np.zeros((R, 7))
for k, r in enumerate(O.rows):
    for m, (a, facs) in enumerate(r["terms"]):
        A[k, m] = float(a)
        for i in range(7):
            s, mu, g = (float(v) for v in facs[i])
            C0[k, m] += g * mu * mu; B[k, m, i] = 2 * g * mu * s; D[k, m, i] = g * s * s
    for i, v in r["lin"].items():
        LIN[k, i] = float(v)
W = np.concatenate([B.reshape(R * Mt, 7), D.reshape(R * Mt, 7)], 1).T      # (14, R*Mt)
c = np.array([float(O.clb[k]) for k in range(24)])
side_hmax = {k: -float(O.clb[k]) for k in range(24, 28) if O.clb[k] is not None}
side_hmin = {k: -float(O.cub[k]) for k in range(24, 28) if O.cub[k] is not None}


def evalF(X):
    feats = np.concatenate([X, X * X], 1)
    E = feats @ W + C0.reshape(-1)[None]
    h = (np.exp(E).reshape(len(X), R, Mt) * A[None]).sum(-1) + X @ LIN.T
    F = (c[None] + h[:, :24]).max(1)
    viol = np.full(len(X), -np.inf)
    for k, v in side_hmax.items():
        viol = np.maximum(viol, h[:, k] - v)
    for k, v in side_hmin.items():
        viol = np.maximum(viol, v - h[:, k])
    return F, viol


def main():
    rng = np.random.default_rng(11)
    tot_bad = 0
    for p in range(8):
        z = np.load(os.path.join(HERE, f"leaves_p{p}.npz"))
        lo, hi, mg, how, isint = z["lo"], z["hi"], z["mg"], z["how"], z["isint"]
        n = len(lo)
        bound = TH + mg                                   # +inf for leaves proved infeasible
        minF_feas = np.full(n, np.inf)
        bad_feas = bad_row = 0
        worst = np.inf
        for s in range(0, n, 4000):
            L, H = lo[s:s + 4000], hi[s:s + 4000]
            for t in range(5):
                if t == 0:
                    X = 0.5 * (L + H)
                    X[:, isint] = np.floor(X[:, isint])
                else:
                    u = rng.random(L.shape)
                    X = L + u * (H - L)
                    X[:, isint] = np.floor(L[:, isint] + u[:, isint] * (H[:, isint] - L[:, isint] + 1))
                    X = np.minimum(X, H)
                F, viol = evalF(X)
                feas = viol <= -1e-9
                b = bound[s:s + 4000]
                gap = F - b
                bad_feas += int(((gap < -1e-9) & feas).sum())
                bad_row += int(((gap < -1e-9) & (how[s:s + 4000] == 0)).sum())
                fin = feas & np.isfinite(b)
                if fin.any():
                    worst = min(worst, gap[fin].min())
                minF_feas[s:s + 4000] = np.minimum(minF_feas[s:s + 4000], np.where(feas, F, np.inf))
        tot_bad += bad_feas + bad_row
        j = int(np.argmin(minF_feas))
        nfe = int(np.isfinite(minF_feas).sum())
        print(f"part {p}: {n} leaves x 5 points; leaves with a feasible sample point {nfe}; "
              f"violations F(p) < theta*+mg-1e-9: feasible points {bad_feas}, row-certified leaves (any point) {bad_row}; "
              f"smallest F(p) - (theta*+mg) at feasible points {worst:.4g}; smallest feasible F(p) - theta* {minF_feas[j] - TH:.4g} "
              f"(leaf {j}, its margin {mg[j]:.3g})", flush=True)
        np.save(os.path.join(HERE, f"minF_p{p}.npy"), minF_feas)
    print("NO VIOLATION" if tot_bad == 0 else f"VIOLATIONS: {tot_bad}")


if __name__ == "__main__":
    main()
