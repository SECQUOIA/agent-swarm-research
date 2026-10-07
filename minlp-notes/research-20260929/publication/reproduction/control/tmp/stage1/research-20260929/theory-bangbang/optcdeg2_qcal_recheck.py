"""Independent checks of optcdeg2_qcal_certify.py (exact rational arithmetic and sampling).

1. For a sample of stages (all stages within 30 of a switch, the first/last stages, and a
   random sample), the residual after exact y-minimization is evaluated in exact rational
   arithmetic straight from the definition
       rho_t = (h/2) y^2 + S_{t+1}(f_t(y, v, u)) - S_t(y, v),  S_t = py y + pv v + q/2 (v - c)^2,
   with y* found exactly (rho_t is a quadratic in y), at 15 points (d, D) of a 5 x 3 grid.
   Exact interpolation gives the 15 coefficients c_jk (j <= 4, k <= 2), which must lie in the
   interval coefficients computed by the certificate (stage_poly). This checks the algebra of
   the y-elimination and of the polynomial expansion independently.
2. Pointwise: for the same stages, the exact g(d, D) = rho~ - c00 at random points of the
   stage domain must be >= the stage's minimum cell bound (m = LB_t - c00_lo).
3. Float sampling over all stages: rho_t at random (y, v, u) in R x V_t x U (y = exact
   minimizer plus offsets) must be >= LB_t up to float rounding.
"""
import json
import sys
from fractions import Fraction as F

import numpy as np

import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../.."))
sys.path.insert(0, _REPO + "/research-20260929/open-instances")
import optcdeg2_qcal_certify as C  # noqa: E402

N = C.N
h = F(4, 10000)


def rho_exact(t, D, y, v, u):
    py0, pv0, q0, c0 = (F(float(D[k][t])) for k in ("py", "pv", "q", "c"))
    py1, pv1, q1, c1 = (F(float(D[k][t + 1])) for k in ("py", "pv", "q", "c"))
    y1 = y + h * v
    v1 = v + h * (u - F(1, 50) * y - F(1, 5) * v * v)
    S1 = py1 * y1 + pv1 * v1 + q1 / 2 * (v1 - c1) ** 2
    S0 = py0 * y + pv0 * v + q0 / 2 * (v - c0) ** 2
    return h / 2 * y * y + S1 - S0


def rho_tilde_exact(t, D, v, u):
    # rho_t is quadratic in y: recover it from three values and minimize exactly
    r0, r1, r2 = (rho_exact(t, D, F(k), v, u) for k in (0, 1, 2))
    a = (r2 - 2 * r1 + r0) / 2
    b = r1 - r0 - a
    assert a > 0
    return r0 - b * b / (4 * a)


def solve(A, b):
    n = len(b)
    M = [row[:] + [bb] for row, bb in zip(A, b)]
    for i in range(n):
        p = next(r for r in range(i, n) if M[r][i] != 0)
        M[i], M[p] = M[p], M[i]
        for r in range(n):
            if r != i and M[r][i] != 0:
                f = M[r][i] / M[i][i]
                M[r] = [x - f * z for x, z in zip(M[r], M[i])]
    return [M[i][n] / M[i][i] for i in range(n)]


def main():
    KH, KT = 1.0, 0.05
    D = C.certificate_data("logs/optcdeg2_kkt_u.npy", KH, KT)
    LB = np.load("logs/optcdeg2_qcal_stage_lb.npy")          # LB[t-1] for t = 1..N-1
    rng = np.random.default_rng(1)
    s1, s2 = D["s1"], D["s2"]
    sample = sorted(set(list(range(1, 31)) + list(range(s1 - 30, s1 + 31)) + list(range(s2 - 30, s2 + 31))
                        + list(range(N - 30, N)) + rng.integers(1, N, 150).tolist()))
    ts = np.array(sample)
    P = C.stage_poly(ts, D)
    mons = [(j, k) for j in range(5) for k in range(3)]
    dg = [F(-2, 10), F(-1, 10), F(0), F(1, 10), F(2, 10)]
    Dg = [F(-1, 10), F(0), F(1, 10)]
    worst_contain = 0.0
    viol_contain = 0
    viol_point = 0
    min_margin = np.inf
    vb = np.load(C.OI + "logs/optcdeg2_vbounds.npy")
    for i, t in enumerate(ts):
        vs, us = F(float(D["v"][t])), F(float(D["u"][t]))
        A, b = [], []
        for d in dg:
            for Dd in Dg:
                A.append([d ** j * Dd ** k for (j, k) in mons])
                b.append(rho_tilde_exact(t, D, vs + d, us + Dd))
        coef = dict(zip(mons, solve(A, b)))
        for mon in mons:
            cv = coef[mon]
            if mon in P:
                lo, hi = F(float(P[mon][0][i])), F(float(P[mon][1][i]))
            else:
                lo = hi = F(0)
            if not (lo <= cv <= hi):
                viol_contain += 1
                print("containment violation", t, mon, float(cv), float(lo), float(hi), flush=True)
            worst_contain = max(worst_contain, float(hi - lo))
        # pointwise check of the cell minimum: g >= m where m = LB_t - c00_lo
        c00lo = F(float(P[(0, 0)][0][i]))
        m = F(float(LB[t - 1])) - c00lo
        dl, du = vb[t, 0] - float(vs), vb[t, 1] - float(vs)
        for _ in range(40):
            d = F(float(rng.uniform(dl, du)))
            Dd = F(float(rng.choice([-0.2, 0.2, rng.uniform(-0.2, 0.2)]))) - us
            g = sum(coef[mon] * d ** mon[0] * Dd ** mon[1] for mon in mons if mon != (0, 0))
            min_margin = min(min_margin, float(g - m))
            if g < m:
                viol_point += 1
                print("point violation", t, float(d), float(Dd), float(g), float(m), flush=True)
    out = dict(stages_checked=len(ts), containment_violations=viol_contain, point_violations=viol_point,
               widest_coefficient_interval=worst_contain, min_point_margin=min_margin)
    print(json.dumps(out), flush=True)
    # 3. float sampling over all stages
    t = np.arange(1, N)
    worst = np.inf
    for rep in range(20):
        v = vb[t, 0] + (vb[t, 1] - vb[t, 0]) * rng.random(len(t))
        u = rng.choice([-0.2, 0.2], len(t)) if rep % 2 == 0 else rng.uniform(-0.2, 0.2, len(t))
        for yoff in (0.0, 1e-3, 1.0, 10.0):
            # exact y-minimizer of the float residual: rho quadratic in y
            def rf(y):
                y1 = y + C.hf * v
                v1 = v + C.hf * (u - 0.02 * y - 0.2 * v * v)
                return (C.hf / 2 * y * y + D["py"][t + 1] * y1 + D["pv"][t + 1] * v1
                        + D["q"][t + 1] / 2 * (v1 - D["c"][t + 1]) ** 2
                        - D["py"][t] * y - D["pv"][t] * v - D["q"][t] / 2 * (v - D["c"][t]) ** 2)
            r0, r1, r2 = rf(D["y"][t]), rf(D["y"][t] + 1), rf(D["y"][t] + 2)
            a = (r2 - 2 * r1 + r0) / 2; b = r1 - r0 - a
            ystar = D["y"][t] - b / (2 * a)
            val = rf(ystar + yoff * rng.standard_normal(len(t)))
            worst = min(worst, float(np.min(val - LB)))
    print(json.dumps(dict(float_sampling_min_rho_minus_LB=worst)), flush=True)
    out["float_sampling_min_rho_minus_LB"] = worst
    json.dump(out, open("logs/optcdeg2_qcal_recheck.json", "w"), indent=1)


if __name__ == "__main__":
    main()
