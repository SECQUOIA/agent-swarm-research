"""dtoc5: rigorous Lagrangian (affine value-function) dual bound and primal check.

Model (checked programmatically from the OSIL by the pattern test in main()):
  min  h * sum_{t=0}^{T-1} (u_t^2 + y_t^2)
  s.t. -h u_t + y_t - y_{t+1} + 4h y_t^2 = 0,  t = 0..T-1,   y_0 = 1,
  h = 2e-5 (OSIL coefficient 2e-05; 8e-05 = 4h), T = 49999, all other variables free.

Dual function (multipliers lam_t on  y_{t+1} - y_t - 4h y_t^2 + h u_t = 0):
  L = sum_t [h u_t^2 + h lam_t u_t] + sum_{t=1}^{T-1} [h(1-4 lam_t) y_t^2 + (lam_{t-1}-lam_t) y_t]
      + lam_{T-1} y_T + h(1-4 lam_0) - lam_0.
If lam_{T-1} = 0 and lam_t < 1/4 (t = 1..T-1), minimizing over the free u, y gives
  d(lam) = h(1-4 lam_0) - lam_0 - (h/4) sum_{t=0}^{T-1} lam_t^2
           - sum_{t=1}^{T-1} (lam_{t-1}-lam_t)^2 / (4h(1-4 lam_t)),
and every feasible point has objective >= d(lam) (weak duality). No variable
bounds are needed. lam is taken from the primal costate lam_t = -2 u_t.
d(lam) is evaluated in mpmath interval arithmetic with h = 1/50000 exactly.
"""
import json
import sys
import time

import mpmath as mp
import numpy as np

from osil_eval import check, load

T = 49999


def pattern_check(I):
    assert len(I["vt"]) == 2 * T + 1 and I["ncons"] == T
    for j in range(2 * T + 1):
        if j == T:
            assert I["lb"][j] == I["ub"][j] == 1.0
        else:
            assert I["lb"][j] == -float("inf") and I["ub"][j] == float("inf")
    obj = I["rows"][-1]
    assert obj["lin"] == {} and obj["nl"] is None
    assert sorted(obj["quad"]) == sorted([(j, j, 2e-5) for j in range(2 * T) if j != 2 * T])
    for r in range(T):
        row = I["rows"][r]
        assert row["lin"] == {r: -2e-5, T + r: 1.0, T + r + 1: -1.0}
        assert row["quad"] == [(T + r, T + r, 8e-5)] and row["nl"] is None and row["lb"] == row["ub"] == 0.0


def dual_interval(lam):
    iv = mp.iv
    iv.dps = 30
    h = iv.mpf(1) / 50000
    L = [iv.mpf(float(v)) for v in lam]  # exact binary floats
    four = iv.mpf(4)
    total = h * (1 - four * L[0]) - L[0]
    s1 = iv.mpf(0)
    for v in L:
        s1 += v * v
    total -= h / 4 * s1
    s2 = iv.mpf(0)
    for t in range(1, T):
        d = L[t - 1] - L[t]
        s2 += d * d / (four * h * (1 - four * L[t]))
    total -= s2
    return total


def main():
    t0 = time.time()
    I = load("dtoc5")
    pattern_check(I)
    y = np.load("logs/dtoc5_y.npy")
    h = 2e-5
    # controls from the states, computed in 50-digit arithmetic and then rounded once, so the
    # equality rows hold to about 1e-20 (computing them in double leaves 8e-17 row errors)
    mp.mp.dps = 50
    hm = mp.mpf(1) / 50000
    u = np.array([float((mp.mpf(y[t]) + 4 * hm * mp.mpf(y[t]) ** 2 - mp.mpf(y[t + 1])) / hm) for t in range(T)])
    x = np.concatenate([u, y])
    chk = check("dtoc5", x, I)
    lam = -2.0 * u
    lam[T - 1] = 0.0
    assert np.all(lam[1:] < 0.25)
    # float estimate
    hf = 2e-5
    dfl = hf * (1 - 4 * lam[0]) - lam[0] - hf / 4 * np.sum(lam ** 2) - np.sum((lam[:-1] - lam[1:]) ** 2 / (4 * hf * (1 - 4 * lam[1:])))
    D = dual_interval(lam)
    rec = dict(name="dtoc5", primal_obj=chk["obj"], primal_cons_viol=chk["cons_viol"], primal_bound_viol=chk["bound_viol"],
               worst_row=chk["worst_row"], dual_float=float(dfl), dual_interval=[float(mp.mpf(D.a)), float(mp.mpf(D.b))],
               dual_bound=float(mp.mpf(D.a)), max_lam=float(lam.max()), min_u=float(u.min()), seconds=time.time() - t0)
    print(json.dumps(rec))
    with open("logs/dtoc5_bound.json", "w") as f:
        json.dump(rec, f, indent=1)


if __name__ == "__main__":
    main()
