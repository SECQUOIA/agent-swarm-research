"""Reviewer: median kappa_t/h and |beta_t|/sqrt(h) of family B2 (author's
fam_B2) on fractional stages, E2 with k1 = 0, N = 200 and 800 (float)."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import sys
import numpy as np
from fractions import Fraction as Fr
sys.path.insert(0, (_PUBLIC_REPO + '/research-20260929/theory-bangbang/singular'))
import lqsing as L
import lqsing_run as R
for N in (200, 800):
    d = L.data(Fr(0), N)
    Hq, gq, c0 = L.float_qp(d)
    u = L.solve_box_qp(Hq, gq)
    status = [(-1 if v <= -1 + 1e-12 else (1 if v >= 1 - 1e-12 else 0)) for v in u]
    sol = L.exact_kkt(d, status)
    P, broke = R.fam_B2(d, sol, status)
    h = float(d['h'])
    ks, bs = [], []
    for t in range(N):
        if status[t] == 0:
            Kt, beta, kap = L.stage_terms(d, P[t + 1], P[t])
            ks.append(float(kap)/h); bs.append(np.hypot(float(beta[0]), float(beta[1]))/np.sqrt(h))
    print('N=%d broke=%s fractional=%d median kappa/h=%.3f  median |beta|/sqrt(h)=%.3f  range |beta|/sqrt(h)=[%.3f, %.3f]'
          % (N, broke, len(ks), np.median(ks), np.median(bs), min(bs), max(bs)), flush=True)

# component-wise and O(h) normalization
for N in (200, 800):
    d = L.data(Fr(0), N)
    Hq, gq, c0 = L.float_qp(d)
    u = L.solve_box_qp(Hq, gq)
    status = [(-1 if v <= -1 + 1e-12 else (1 if v >= 1 - 1e-12 else 0)) for v in u]
    sol = L.exact_kkt(d, status)
    P, broke = R.fam_B2(d, sol, status)
    h = float(d['h'])
    b0, b1, bn = [], [], []
    for t in range(N):
        if status[t] == 0:
            Kt, beta, kap = L.stage_terms(d, P[t + 1], P[t])
            b0.append(abs(float(beta[0]))); b1.append(abs(float(beta[1]))); bn.append(np.hypot(float(beta[0]), float(beta[1])))
    print('N=%d median |beta_1|/sqrt(h)=%.3f |beta_2|/sqrt(h)=%.3f ; median |beta|/h=%.3f' %
          (N, np.median(b0)/np.sqrt(h), np.median(b1)/np.sqrt(h), np.median(bn)/h), flush=True)
